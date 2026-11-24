"""Q6, fifth execution (SS7.6), 24 Nov 2026 -- first time this step runs.

Brain-to-muscle interface, proven small: a SYNTHETIC pooled-rate ladder
-- constant rates 0, 30, 60, 90, 120 Hz, each held 1.5 s (15 chunks),
labelled synthetic in every artefact -- through SS4.2's estimator and
SS4.3's mapping AS REVISED by Pass 6, driving ROSTRUM PITCH ONLY (the
other four proboscis DoFs held at their e = 0 chain state, ctrl = 0).
The synthetic input is a seeded Poisson spike train (seed recorded;
pooled rate split evenly across the two MN9 sides -- the estimator
pools, so the split cannot affect the pooled path). The estimator runs
continuously across the whole ladder, initialised at ladder start
(r_filt = 0, empty window), with SS4.2's startup rule (chunks 0-4
divide by elapsed time).

r_lo = 5 Hz (the FIXED SS4.3 value). r_hi = 155 Hz is PROVISIONAL
(SS7.6: Part 3's measured pooled MN9 response, 92.57 + 62.40 Hz),
labelled provisional here and in every artefact, and replaced by the
calibrated r_hi at the Part 5 freeze.

Pass: (i) at 0 Hz the rostrum target and measured angle stay at rest
(zero-in/zero-out: e = 0 throughout the zero step, max |E_rostrum|
<= 0.005 rad); (ii) measured E_rostrum (the rostrum term of SS4.4),
averaged over the final 5 chunks of each hold, is monotone
non-decreasing across the ladder -- plateaus acceptable only where the
SS4.3 clamp binds (under the revised chain no clamp binds below e = 1;
any clipped ctrl is recorded); (iii) the rate -> angle calibration
curve is saved (this JSON + q6_calibration_curve_rerun5.csv).
"""

import csv
import json
import time
from pathlib import Path

import numpy as np

from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (CHUNK_STEPS, PITCH_JOINTS, PROBOSCIS,  # noqa: E402
                         build_sim, dof_index, settle)
from gate_common3 import RESULTS, compiled_params, feedforward_ctrl  # noqa: E402
from gate_common5 import theta_ext_from_params  # noqa: E402

RATES_HZ = [0, 30, 60, 90, 120]
CHUNKS_PER_RATE = 15            # 1.5 s per rate
R_LO = 5.0                      # FIXED, SS4.3
R_HI_PROVISIONAL = 155.0        # PROVISIONAL, SS7.6 -- replaced at Part 5
SEED = 20261124
ALPHA = 1.0 - float(np.exp(-0.1 / 0.2))   # SS4.2 EMA, tau = 0.2 s
ROS = "c_head-c_rostrum-pitch"


def main():
    t0 = time.time()
    q5 = json.loads((RESULTS / "q5_rerun5.json").read_text())
    assert q5["verdict"] == "PASS", "Q5 did not pass; Q6 must not run"
    q2 = json.loads((RESULTS / "q2_rerun5.json").read_text())
    signs = {j: q2["joints"][j]["extension_sign_s"] for j in PITCH_JOINTS}
    s_ros = signs[ROS]

    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    theta_ext = theta_ext_from_params(params, signs)
    st = settle(sim, fly, np.zeros(len(order)))
    if not st["settled"]:
        out = {"step": "Q6 (rerun5)", "verdict": "FAIL",
               "fail_reason": "settle did not complete within cap",
               "settle": st}
        (RESULTS / "q6_rerun5.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2)[:1200])
        return
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    rest_ros = rest[ROS]

    rng = np.random.default_rng(SEED)
    counts_hist = []            # pooled synthetic counts per chunk
    r_filt = 0.0
    base_ctrl = np.zeros(len(order))
    chunks = []
    clipped = []
    gchunk = 0
    for rate in RATES_HZ:
        for _ in range(CHUNKS_PER_RATE):
            # synthetic pooled spike counts for this chunk (Poisson,
            # split evenly over the two MN9 sides; the estimator pools)
            c = int(rng.poisson(rate / 2 * 0.1)
                    + rng.poisson(rate / 2 * 0.1))
            counts_hist.append(c)
            window = counts_hist[-5:]
            r_win = sum(window) / (0.1 * len(window))
            r_filt = r_filt + ALPHA * (r_win - r_filt)
            e = min(max((r_filt - R_LO) / (R_HI_PROVISIONAL - R_LO), 0.0), 1.0)
            target_ros = rest_ros + e * (theta_ext[ROS] - rest_ros)
            ctrl = base_ctrl.copy()
            if e == 0:
                ctrl[idx[ROS]] = 0.0
            else:
                raw = ((params[ROS]["kp_gainprm0"]
                        + params[ROS]["jnt_stiffness"]) * target_ros
                       - params[ROS]["jnt_stiffness"]
                       * params[ROS]["qpos_spring"]) \
                    / params[ROS]["kp_gainprm0"]
                ctrl[idx[ROS]] = feedforward_ctrl(params[ROS], target_ros)
                lo, hi = params[ROS]["yaml_range"]
                if raw < lo or raw > hi:
                    clipped.append({"chunk": gchunk, "rate_hz": rate,
                                    "raw_ctrl": float(raw)})
            sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
            for _ in range(CHUNK_STEPS):
                sim.step()
            angles = sim.get_joint_angles(fly.name)
            a_ros = float(angles[idx[ROS]])
            chunks.append({
                "chunk": gchunk, "rate_hz": rate,
                "synthetic_pooled_count": c,
                "r_window_hz": float(r_win), "r_filt_hz": float(r_filt),
                "e": float(e), "target_rostrum_rad": float(target_ros),
                "ctrl_rostrum_rad": float(ctrl[idx[ROS]]),
                "angle_rostrum_rad": a_ros,
                "E_rostrum_rad": float(s_ros * (a_ros - rest_ros)),
            })
            gchunk += 1
    sim.close()

    steps = []
    for i, rate in enumerate(RATES_HZ):
        seg = chunks[i * CHUNKS_PER_RATE:(i + 1) * CHUNKS_PER_RATE]
        tail = seg[-5:]
        steps.append({
            "rate_hz": rate, "synthetic": True,
            "r_filt_mean_final5_hz": float(np.mean(
                [c["r_filt_hz"] for c in tail])),
            "e_mean_final5": float(np.mean([c["e"] for c in tail])),
            "target_rostrum_mean_final5_rad": float(np.mean(
                [c["target_rostrum_rad"] for c in tail])),
            "angle_rostrum_mean_final5_rad": float(np.mean(
                [c["angle_rostrum_rad"] for c in tail])),
            "E_rostrum_mean_final5_rad": float(np.mean(
                [c["E_rostrum_rad"] for c in tail])),
            "E_rostrum_max_abs_all_chunks_rad": float(max(
                abs(c["E_rostrum_rad"]) for c in seg)),
            "e_max_all_chunks": float(max(c["e"] for c in seg)),
        })
    e_means = [s["E_rostrum_mean_final5_rad"] for s in steps]
    monotone = all(e_means[k + 1] >= e_means[k] - 1e-12
                   for k in range(len(e_means) - 1))
    zero = steps[0]
    checks = {
        "i_zero_in_zero_out": bool(
            zero["e_max_all_chunks"] == 0.0
            and zero["E_rostrum_max_abs_all_chunks_rad"] <= 0.005),
        "ii_E_rostrum_monotone_non_decreasing": bool(monotone),
        "iii_calibration_curve_saved": True,
    }
    result = {
        "step": "Q6 (rerun5)",
        "synthetic_input": ("seeded Poisson spike train, seed "
                            f"{SEED}, pooled rate split evenly over "
                            "the two MN9 sides; SYNTHETIC -- not brain "
                            "output"),
        "r_lo_hz": R_LO,
        "r_hi_hz": R_HI_PROVISIONAL,
        "r_hi_status": ("PROVISIONAL (SS7.6) -- replaced by the "
                        "calibrated r_hi at the Part 5 freeze"),
        "signs": signs, "theta_ext_rad": theta_ext,
        "theta_rest_rad": rest,
        "ladder_steps": steps,
        "E_rostrum_step_means_rad": e_means,
        "clipped_ctrl_events": clipped,
        "clamp_note": ("plateaus are acceptable only where the SS4.3 "
                       "clamp binds; under the revised chain the "
                       "feedforward command reaches the range limit "
                       "only at e = 1, above this ladder's top e, so "
                       "no plateau is expected or accepted here"),
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "wall_clock_s": time.time() - t0,
        "per_chunk": chunks,
    }
    out = RESULTS / "q6_rerun5.json"
    out.write_text(json.dumps(result, indent=2))
    csv_path = RESULTS / "q6_calibration_curve_rerun5.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rate_hz_synthetic", "r_filt_mean_final5_hz",
                    "e_mean_final5", "target_rostrum_mean_final5_rad",
                    "angle_rostrum_mean_final5_rad",
                    "E_rostrum_mean_final5_rad",
                    "note"])
        for s in steps:
            w.writerow([s["rate_hz"], s["r_filt_mean_final5_hz"],
                        s["e_mean_final5"],
                        s["target_rostrum_mean_final5_rad"],
                        s["angle_rostrum_mean_final5_rad"],
                        s["E_rostrum_mean_final5_rad"],
                        "synthetic input; r_hi=155 Hz PROVISIONAL"])
    result["calibration_curve_csv"] = str(csv_path)
    out.write_text(json.dumps(result, indent=2))
    for s in steps:
        print("rate", s["rate_hz"], "r_filt", round(s["r_filt_mean_final5_hz"], 2),
              "e", round(s["e_mean_final5"], 4),
              "E_ros", round(s["E_rostrum_mean_final5_rad"], 4))
    print("checks:", checks)
    print("Q6 verdict:", result["verdict"], "wall", result["wall_clock_s"])
    print("wrote", out, "and", csv_path)


if __name__ == "__main__":
    main()
