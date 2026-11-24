"""Part 5 registered feeding chain: SS4.2 rate estimator + SS4.3 mapping.

Specification: PART4-SENSORY-SPECS.md SS4.2 and SS4.3 (as amended by
Passes 1, 3, 5 and 6-as-revised). This module is the actual Part 5 code
path -- the thin FlyBody slice (SS6) exercises it end to end, and the
Part 5 closed loop imports it unchanged. It is deliberately free of
any body/brain imports: it consumes MN9 spike counts per 100 ms chunk
and produces actuator commands (ctrl values) for the five proboscis
DoFs, so it can be unit-tested without a simulator.

SS4.2 estimator (FIXED in the spec):
  - readout: the two MN9 neurons' spike counts per chunk, pooled
    (r = r_L + r_R; the L/R split is preserved in the logs by the
    caller, the decoder does not vote on it -- RQ-C5 owns the split);
  - window: trailing 500 ms boxcar over the pooled counts. Startup
    rule (Pass 1): while fewer than 5 chunks have elapsed, the pooled
    count accumulated since t = 0 is divided by the ELAPSED time
    (0.1 s per completed chunk), not by 0.5 s, so a constant-rate
    response reads at its true value from the first chunk;
  - smoothing: one exponential filter, tau = 0.2 s, exact per-chunk
    discretisation alpha = 1 - exp(-0.1/0.2) = 0.393469..., initial
    state r_filt = 0 at t = 0. No other transformation.

SS4.3 mapping (form FIXED in the spec; r_hi is the one constant the
spec assigns to calibration -- callers must state where their r_hi
came from):
  - e = clip((r_filt - r_lo)/(r_hi - r_lo), 0, 1); r_lo = 5 Hz FIXED.
  - joint targets interpolate theta_rest -> theta_ext per DoF, where
    theta_ext is the ACHIEVABLE extreme (Pass 6): the clamped static
    map's achieved angle when the servo command sits at the published
    range limit in the extension direction. Haustellum yaw is held at
    theta_rest for all e (its ctrl is the feedforward of theta_rest,
    except at e = 0 where the spec's rule below applies).
  - the ctrl written is the feedforward inverse of the intended
    achieved angle under the compiled static map,
        ctrl = ((kp + ks)*theta - ks*ref)/kp, clipped to the range,
    with kp, ks, ref read from the COMPILED artefact (Pass 5):
    kp = actuator gainprm[0], ks = jnt_stiffness, ref = qpos_spring.
  - at e = 0 (r_filt <= r_lo) the chain writes ctrl = 0 to the five
    proboscis DoFs; theta_rest is the settled pose under that command,
    so zero command reproduces the settled pose by construction.

The params dict format is exactly the qualification gate's
compiled_params() record (gate_common3.py): per joint, a dict with
"kp_gainprm0", "jnt_stiffness", "qpos_spring" and "yaml_range". Part 5
reads those values from the compiled model of the pinned artefact --
never from the YAML files and never from constants copied here.
"""

import math

CHUNK_S = 0.1                      # SS2.1 bridge cadence
WINDOW_CHUNKS = 5                  # SS4.2: trailing 500 ms boxcar
EMA_TAU_S = 0.2                    # SS4.2 smoothing time constant
EMA_ALPHA = 1.0 - math.exp(-CHUNK_S / EMA_TAU_S)   # 0.393469...

ROSTRUM = "c_head-c_rostrum-pitch"
HAUSTELLUM = "c_rostrum-c_haustellum-pitch"
YAW = "c_rostrum-c_haustellum-yaw"
LABRUM_L = "c_haustellum-l_labrum-pitch"
LABRUM_R = "c_haustellum-r_labrum-pitch"
PITCH_JOINTS = (ROSTRUM, HAUSTELLUM)
LABRUM_JOINTS = (LABRUM_L, LABRUM_R)
PROBOSCIS = (ROSTRUM, HAUSTELLUM, YAW, LABRUM_L, LABRUM_R)

R_LO_DEFAULT = 5.0                 # SS4.3: r_lo = 5 Hz pooled, FIXED


def qhat(p, ctrl):
    """Unclamped static map (SS4.3): servo/spring force balance."""
    kp, ks, ref = p["kp_gainprm0"], p["jnt_stiffness"], p["qpos_spring"]
    return (kp * ctrl + ks * ref) / (kp + ks)


def qhat_eff(p, ctrl):
    """Clamped static map (SS4.3): qhat limited to the published range."""
    lo, hi = p["yaml_range"]
    return float(min(max(qhat(p, ctrl), lo), hi))


def feedforward_ctrl(p, theta_intended):
    """Inverse map (SS4.3): ctrl achieving the intended angle, clipped."""
    kp, ks, ref = p["kp_gainprm0"], p["jnt_stiffness"], p["qpos_spring"]
    ctrl = ((kp + ks) * theta_intended - ks * ref) / kp
    lo, hi = p["yaml_range"]
    return float(min(max(ctrl, lo), hi))


def theta_ext_from_params(params, signs):
    """Pass 6 achievable extremes for the four driven proboscis DoFs.

    theta_ext(j) = qhat_eff at the published range limit in the
    extension direction: the pitch joints extend toward the end their
    gate-recorded sign names; the labrum joints toward their positive
    (opening) end. Yaw is held at rest and has no theta_ext.
    """
    ext = {}
    for j in PITCH_JOINTS:
        lo, hi = params[j]["yaml_range"]
        end = lo if signs[j] < 0 else hi
        ext[j] = qhat_eff(params[j], end)
    for j in LABRUM_JOINTS:
        ext[j] = qhat_eff(params[j], params[j]["yaml_range"][1])
    return ext


class RateEstimator:
    """SS4.2: MN9 L/R chunk counts -> pooled windowed rate -> r_filt."""

    def __init__(self):
        self._pooled_counts = []   # pooled MN9 count per chunk, since t=0
        self.r_window = 0.0
        self.r_filt = 0.0

    def update(self, n_left, n_right):
        """Advance one chunk. Returns (r_window_hz, r_filt_hz)."""
        if n_left < 0 or n_right < 0:
            raise ValueError("spike counts must be non-negative")
        self._pooled_counts.append(int(n_left) + int(n_right))
        window = self._pooled_counts[-WINDOW_CHUNKS:]
        # Startup rule: len(window) < 5 only before t = 0.5 s, where the
        # denominator 0.1*len(window) is exactly the elapsed time.
        self.r_window = sum(window) / (CHUNK_S * len(window))
        self.r_filt += EMA_ALPHA * (self.r_window - self.r_filt)
        return self.r_window, self.r_filt


class FeedingChain:
    """SS4.2 + SS4.3: MN9 counts in, proboscis ctrl values out.

    One instance per episode: construct with the compiled params and
    the gate-recorded extension signs, call set_rest() with the
    episode's settled pose (SS4.4) once the SS2.3 settle completes,
    then update() once per chunk.
    """

    def __init__(self, params, signs, r_lo=R_LO_DEFAULT, r_hi=None):
        if r_hi is None:
            raise ValueError(
                "r_hi must be supplied explicitly: SS4.3 assigns it to "
                "Part 5 calibration (or, for the SS6 slice, to a "
                "declared slice parameter) -- it is never defaulted")
        if not r_hi > r_lo:
            raise ValueError("r_hi must exceed r_lo")
        self.params = params
        self.signs = dict(signs)
        self.r_lo = float(r_lo)
        self.r_hi = float(r_hi)
        self.theta_ext = theta_ext_from_params(params, signs)
        self.estimator = RateEstimator()
        self.theta_rest = None

    def set_rest(self, theta_rest):
        """Register the episode's settled pose (SS4.4 reference pose)."""
        missing = [j for j in PROBOSCIS if j not in theta_rest]
        if missing:
            raise ValueError(f"theta_rest is missing joints: {missing}")
        self.theta_rest = {j: float(theta_rest[j]) for j in PROBOSCIS}

    def extension_command(self, r_filt):
        """SS4.3: e = clip((r_filt - r_lo)/(r_hi - r_lo), 0, 1)."""
        e = (r_filt - self.r_lo) / (self.r_hi - self.r_lo)
        return float(min(max(e, 0.0), 1.0))

    def targets_for_e(self, e):
        """SS4.3 target functions at command e (five proboscis DoFs)."""
        if self.theta_rest is None:
            raise RuntimeError("set_rest() must be called before use")
        targets = {}
        for j in PITCH_JOINTS + LABRUM_JOINTS:
            targets[j] = (self.theta_rest[j]
                          + e * (self.theta_ext[j] - self.theta_rest[j]))
        targets[YAW] = self.theta_rest[YAW]     # held at rest, all e
        return targets

    def ctrls_for_e(self, e):
        """Actuator ctrl values realising targets_for_e under the map.

        At e = 0 the chain writes ctrl = 0 to the five DoFs (SS4.3);
        for e > 0 each DoF's ctrl is the feedforward inverse of its
        target (yaw's target is theta_rest, so its ctrl is the value
        that holds it there).
        """
        targets = self.targets_for_e(e)
        if e == 0.0:
            return {j: 0.0 for j in PROBOSCIS}, targets
        ctrls = {j: feedforward_ctrl(self.params[j], targets[j])
                 for j in PROBOSCIS}
        return ctrls, targets

    def update(self, n_left, n_right):
        """Advance one chunk from MN9 counts. Returns a record dict:
        r_window, r_filt, e, targets {joint: rad}, ctrls {joint: ctrl}.
        """
        r_window, r_filt = self.estimator.update(n_left, n_right)
        e = self.extension_command(r_filt)
        ctrls, targets = self.ctrls_for_e(e)
        return {"r_window_hz": r_window, "r_filt_hz": r_filt, "e": e,
                "targets": targets, "ctrls": ctrls}

    def extension_E(self, angles):
        """SS4.4 extension angle from a {joint: angle} mapping."""
        if self.theta_rest is None:
            raise RuntimeError("set_rest() must be called before use")
        return float(sum(self.signs[j] * (angles[j] - self.theta_rest[j])
                         for j in PITCH_JOINTS))
