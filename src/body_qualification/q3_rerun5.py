"""Q3, fifth execution (SS7.4 as amended by Pass 3; chain as revised by
Pass 6), 24 Nov 2026.

Five extend-hold-retract cycles, all five proboscis DoFs driven together
through SS4.3's target functions AS REVISED by Pass 6 (theta_ext = the
achievable extremes, computed from the compiled artefact's parameters
via the clamped map; the feedforward command at e = 1 equals the
published range limit exactly), with the feedforward inverse computed
from the Q0-recorded compiled values (at e = 0 the chain writes ctrl = 0
to the five DoFs; theta_rest is the settled pose under that command,
recorded after the SS2.3 settle). Adhesion OFF (actuators present, ctrl
held 0). Profile per cycle: ramp e 0->1 over 0.5 s (5 chunks), hold
e = 1 for 2.0 s (20 chunks), ramp back over 0.5 s (5 chunks), hold 1.0 s
(10 chunks); ctrl updated per chunk (zero-order hold, SS4.3), E sampled
per chunk (SS4.4). Extension signs are this run's Q2 outputs
(results/q2_rerun5.json); theta_ext is recomputed here from this build's
compiled parameters and checked against Q2's recorded values.

Pass, every cycle: (i) E at the end of the ramp >= 90% of the
map-predicted achieved E at e = 1; (ii) hold-phase E within +-0.05 rad of
its mean; (iii) post-retraction E within 0.05 rad of the pre-cycle
reference; (iv) no joint beyond its published range (eps = 0.005), no
NaN/Inf. Q3's claim is the narrowed one (Pass 3): model-consistent
extension only; functional reach is Q5's question.
"""

import json
import time
from pathlib import Path

import numpy as np

from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (CHUNK_STEPS, EPS, PITCH_JOINTS, PROBOSCIS,  # noqa: E402
                         RANGES, build_sim, dof_index, settle)
from gate_common3 import RESULTS, compiled_params, extension_E  # noqa: E402
from gate_common5 import (chain_ctrl_rev, predicted_E_rev,  # noqa: E402
                          theta_ext_from_params)

CYCLE_CHUNKS = 40  # 5 ramp + 20 hold + 5 retract + 10 hold


def cycle_e_profile():
    e = []
    e += [(i + 1) / 5 for i in range(5)]          # ramp up
    e += [1.0] * 20                                # hold
    e += [1.0 - (i + 1) / 5 for i in range(5)]     # ramp down
    e += [0.0] * 10                                # post-retract hold
    return e


def run_cycles(sim, fly, idx, params, rest, signs, theta_ext, n_cycles,
               lead_in_chunks=5):
    """Run n_cycles of the SS7.4 profile; return per-chunk records.

    Angles are read per physics step from qpos for the five proboscis
    DoFs (range/finiteness checks) and per chunk for E.
    """
    m = sim.mj_model
    qadr = {j: int(m.jnt_qposadr[params[j]["joint_id"]]) for j in PROBOSCIS}
    base_ctrl = np.zeros(len(idx))
    profile = cycle_e_profile()
    chunks = []          # per-chunk dicts across lead-in + all cycles
    max_excursion = -1e9
    all_finite = True

    def do_chunk(e):
        nonlocal max_excursion, all_finite
        ctrl = chain_ctrl_rev(base_ctrl, idx, params, e, rest, theta_ext)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(CHUNK_STEPS):
            sim.step()
            q = sim.mj_data.qpos
            for j in PROBOSCIS:
                a = float(q[qadr[j]])
                if not np.isfinite(a):
                    all_finite = False
                lo, hi = RANGES[j]
                max_excursion = max(max_excursion, lo - a, a - hi)
        angles = sim.get_joint_angles(fly.name)
        by_joint = {j: float(angles[idx[j]]) for j in PROBOSCIS}
        chunks.append({"e": e, "angles": by_joint,
                       "E_rad": extension_E(by_joint, rest, signs)})

    for _ in range(lead_in_chunks):
        do_chunk(0.0)
    for _ in range(n_cycles):
        for e in profile:
            do_chunk(e)
    return chunks, max_excursion, all_finite


def analyse_cycles(chunks, lead_in_chunks, n_cycles, e_pred_1):
    """Per-cycle SS7.4 verdicts from the per-chunk record."""
    cycles = []
    for c in range(n_cycles):
        start = lead_in_chunks + c * CYCLE_CHUNKS
        seg = chunks[start:start + CYCLE_CHUNKS]
        if c == 0:
            ref = float(np.mean([ch["E_rad"] for ch in
                                 chunks[lead_in_chunks - 5:lead_in_chunks]]))
        else:
            prev = chunks[start - 10:start]
            ref = float(np.mean([ch["E_rad"] for ch in prev[-5:]]))
        e_ramp_end = seg[4]["E_rad"]
        hold_E = [ch["E_rad"] for ch in seg[5:25]]
        hold_mean = float(np.mean(hold_E))
        hold_dev = float(max(abs(x - hold_mean) for x in hold_E))
        post = float(np.mean([ch["E_rad"] for ch in seg[35:40]]))
        residual = abs(post - ref)
        cycles.append({
            "cycle": c + 1,
            "pre_cycle_reference_E_rad": ref,
            "E_at_ramp_end_rad": float(e_ramp_end),
            "reach_fraction_of_predicted": float(e_ramp_end / e_pred_1),
            "reach_ge_90pct": bool(e_ramp_end >= 0.9 * e_pred_1),
            "hold_mean_E_rad": hold_mean,
            "hold_max_deviation_rad": hold_dev,
            "hold_within_0.05": bool(hold_dev <= 0.05),
            "post_retraction_mean_E_rad": post,
            "post_retraction_residual_rad": float(residual),
            "retract_within_0.05": bool(residual <= 0.05),
            "peak_E_rad": float(max(ch["E_rad"] for ch in seg)),
        })
    return cycles


def main():
    t0 = time.time()
    q2 = json.loads((RESULTS / "q2_rerun5.json").read_text())
    assert q2["verdict"] == "PASS", "Q2 did not pass; Q3 must not run"
    signs = {j: q2["joints"][j]["extension_sign_s"] for j in PITCH_JOINTS}

    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    theta_ext = theta_ext_from_params(params, signs)
    # Integrity: this build's achievable extremes must reproduce Q2's.
    for j in PITCH_JOINTS:
        assert abs(theta_ext[j] - q2["joints"][j]["theta_ext_rad"]) < 1e-9, (
            f"theta_ext mismatch for {j}: {theta_ext[j]} vs Q2's "
            f"{q2['joints'][j]['theta_ext_rad']}")

    st = settle(sim, fly, np.zeros(len(order)))
    if not st["settled"]:
        out = {"step": "Q3 (rerun5)", "verdict": "FAIL",
               "fail_reason": "settle did not complete within cap",
               "settle": st}
        (RESULTS / "q3_rerun5.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2)[:1200])
        return
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    e_pred_1 = predicted_E_rev(params, rest, signs, theta_ext, 1.0)
    e_raw = float(sum(signs[j] * ((RANGES[j][1] if signs[j] > 0 else RANGES[j][0])
                                  - rest[j]) for j in PITCH_JOINTS))

    chunks, max_exc, finite = run_cycles(sim, fly, idx, params, rest, signs,
                                         theta_ext, n_cycles=5)
    sim.close()
    cycles = analyse_cycles(chunks, 5, 5, e_pred_1)
    hold_means = [c["hold_mean_E_rad"] for c in cycles]
    e_max_measured = float(np.mean(hold_means))
    checks = {
        "reach_ge_90pct_all_cycles": all(c["reach_ge_90pct"] for c in cycles),
        "hold_within_0.05_all_cycles": all(c["hold_within_0.05"]
                                           for c in cycles),
        "retract_within_0.05_all_cycles": all(c["retract_within_0.05"]
                                              for c in cycles),
        "no_range_violation_beyond_eps": bool(max_exc <= EPS),
        "all_finite": bool(finite),
    }
    result = {
        "step": "Q3 (rerun5)",
        "claim": ("model-consistent extension only (Amendment Pass 3); "
                  "functional feeding reach is Q5's question"),
        "chain": ("SS4.3 as revised by Pass 6: theta_ext = achievable "
                  "extremes from the compiled parameters"),
        "signs": signs, "theta_ext_rad": theta_ext,
        "theta_rest_rad": rest,
        "E_predicted_achieved_at_e1_rad": e_pred_1,
        "E_max_measured_hold_mean_rad": e_max_measured,
        "E_raw_extremes_rad": e_raw,
        "E_raw_extremes_definition": ("sum over pitch joints of s_j * "
                                      "(range end in the extension "
                                      "direction - theta_rest_j), SS4.4 as "
                                      "pinned by Pass 6 (= 2.8258 rad at "
                                      "the recorded rests; an earlier "
                                      "summary's 2.8264 was a "
                                      "transcription slip)"),
        "E_max_fraction_of_raw_extremes": float(e_max_measured / e_raw),
        "cycles": cycles,
        "max_limit_excursion_rad": float(max_exc),
        "checks": checks,
        "post_retraction_residuals_rad": [c["post_retraction_residual_rad"]
                                          for c in cycles],
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "wall_clock_s": time.time() - t0,
        "per_chunk_E_rad": [c["E_rad"] for c in chunks],
    }
    out = RESULTS / "q3_rerun5.json"
    out.write_text(json.dumps(result, indent=2))
    for c in cycles:
        print("cycle", c["cycle"], "reach", round(c["reach_fraction_of_predicted"], 4),
              "hold_dev", round(c["hold_max_deviation_rad"], 4),
              "residual", round(c["post_retraction_residual_rad"], 4))
    print("E_pred", round(e_pred_1, 4), "E_max meas", round(e_max_measured, 4),
          "fraction of raw", round(result["E_max_fraction_of_raw_extremes"], 4))
    print("Q3 verdict:", result["verdict"], "wall", result["wall_clock_s"])
    print("wrote", out)


if __name__ == "__main__":
    main()
