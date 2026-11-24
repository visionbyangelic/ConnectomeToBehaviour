"""Q2, third execution (SS7.3 as amended by Passes 1, 3, 5), 24 Nov 2026.

Per-DoF nine-point raw-target sweep (0.5 s holds, steady state = mean over
the final 0.1 s), all other actuators at ctrl 0, re-equilibrated before
each joint's sweep. Judged against the PRE-REGISTERED prediction table
(results/q2_predictions_prereg.json, computed from the Q0-recorded
compiled values before this sweep ran): (i) map-relative steady-state
error <= 0.05 rad at all nine points; (ii) no measured angle outside the
published range by more than eps = 0.005 rad at any step; (iii) coupling
<= 0.05 rad over the other four proboscis DoFs + the three neck joints;
(iv) no NaN/Inf. The empirical map must be strictly increasing in target
wherever the clamp does not bind (the prereg table identifies clamp-bound
points analytically; under the corrected map there are none).

Extension signs: tip = mean of the l_labrum_lower / r_labrum_lower geom
centres (the corrected sampling; gate_common.labrum_tip_pos names geoms
that resolve to id -1 in this model -- see the second execution's record).
The end where the tip sits farther from the head and lower is extension.
"""

import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (EPS, NECK, PITCH_JOINTS, PROBOSCIS, RANGES,  # noqa: E402
                         build_sim, dof_index, settle)
from gate_common3 import RESULTS, labrum_tip_pos  # noqa: E402

HOLD_STEPS = 5000       # 0.5 s
STEADY_STEPS = 1000     # final 0.1 s
REEQ_STEPS = 5000       # 0.5 s re-equilibration at ctrl 0 before each sweep
WATCHED = PROBOSCIS + NECK


def main():
    t0 = time.time()
    prereg = json.loads((RESULTS / "q2_predictions_prereg.json").read_text())
    pred = prereg["table"]

    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    ctrl = np.zeros(len(order))
    st = settle(sim, fly, ctrl)
    if not st["settled"]:
        out = {"step": "Q2 (rerun3)", "verdict": "FAIL",
               "fail_reason": "initial settle did not complete within cap",
               "settle": st}
        (RESULTS / "q2_rerun3.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2)[:1500])
        return
    head_id = mj.mj_name2id(sim.mj_model, mj.mjtObj.mjOBJ_BODY, "flybody/c_head")

    joints_out = {}
    all_pass = True
    for joint in PROBOSCIS:
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(REEQ_STEPS):
            sim.step()
        rest_angles = sim.get_joint_angles(fly.name)
        rest = {n: float(rest_angles[idx[n]]) for n in WATCHED}

        lo, hi = RANGES[joint]
        targets = [lo + k * (hi - lo) / 8 for k in range(9)]
        points = []
        tip_by_k = {}
        for k, tgt in enumerate(targets):
            c = ctrl.copy()
            c[idx[joint]] = tgt
            sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, c)
            trace = np.empty((HOLD_STEPS, len(WATCHED)))
            for s in range(HOLD_STEPS):
                sim.step()
                a = sim.get_joint_angles(fly.name)
                trace[s] = [a[idx[n]] for n in WATCHED]
            steady = float(trace[-STEADY_STEPS:, WATCHED.index(joint)].mean())
            p_pred = pred[joint]["points"][k]
            assert abs(p_pred["target_ctrl_rad"] - tgt) < 1e-12
            expected = p_pred["predicted_steady_state_rad"]
            coupling = {}
            for n in WATCHED:
                if n == joint:
                    continue
                coupling[n] = float(np.abs(trace[:, WATCHED.index(n)]
                                           - rest[n]).max())
            exc = np.maximum(
                np.array([RANGES[n][0] for n in WATCHED]) - trace,
                trace - np.array([RANGES[n][1] for n in WATCHED]))
            points.append({
                "k": k, "target_ctrl": float(tgt),
                "steady_state_rad": steady,
                "predicted_steady_state_rad": expected,
                "qhat_unclamped_rad": p_pred["qhat_unclamped_rad"],
                "clamp_bound": p_pred["clamp_bound"],
                "steady_state_error_rad": abs(steady - expected),
                "coupling_max_rad": max(coupling.values()),
                "coupling_by_joint": coupling,
                "max_limit_excursion_rad": float(exc.max()),
                "all_finite": bool(np.isfinite(trace).all()),
            })
            if joint in PITCH_JOINTS and k in (0, 8):
                tip_by_k[k] = {
                    "tip_pos_mm": [float(x) for x in labrum_tip_pos(sim)],
                    "head_pos_mm": [float(x) for x in
                                    sim.mj_data.xpos[head_id]],
                }
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)

        errs = [p["steady_state_error_rad"] for p in points]
        mono_ok, mono_notes = True, []
        for k in range(8):
            a, b = points[k], points[k + 1]
            if a["predicted_steady_state_rad"] == b["predicted_steady_state_rad"]:
                continue  # analytic clamp plateau: identified from the rule
            if not b["steady_state_rad"] > a["steady_state_rad"]:
                mono_ok = False
                mono_notes.append(f"k={k}->{k+1} not increasing")
        checks = {
            "map_error_le_0.05_all_points": all(e <= 0.05 for e in errs),
            "limits_within_eps": all(p["max_limit_excursion_rad"] <= EPS
                                     for p in points),
            "coupling_le_0.05_all_points": all(
                p["coupling_max_rad"] <= 0.05 for p in points),
            "all_finite": all(p["all_finite"] for p in points),
            "monotone_except_clamp_plateaus": mono_ok,
        }
        jout = {"range": [lo, hi], "rest_angle_rad": rest[joint],
                "points": points, "checks": checks,
                "max_steady_state_error_rad": max(errs),
                "monotone_notes": mono_notes,
                "clamp_bound_points": [p["k"] for p in points
                                       if p["clamp_bound"]],
                "verdict": "PASS" if all(checks.values()) else "FAIL"}
        if joint in PITCH_JOINTS:
            t0p = np.array(tip_by_k[0]["tip_pos_mm"])
            t8p = np.array(tip_by_k[8]["tip_pos_mm"])
            h0p = np.array(tip_by_k[0]["head_pos_mm"])
            h8p = np.array(tip_by_k[8]["head_pos_mm"])
            d0 = float(np.linalg.norm(t0p - h0p))
            d8 = float(np.linalg.norm(t8p - h8p))
            ext_at_max = (d8 > d0) and (t8p[2] < t0p[2])
            ext_at_min = (d0 > d8) and (t0p[2] < t8p[2])
            if ext_at_max and not ext_at_min:
                s_j, theta_ext = 1, hi - 0.05
            elif ext_at_min and not ext_at_max:
                s_j, theta_ext = -1, lo + 0.05
            else:
                s_j, theta_ext = None, None
                jout["verdict"] = "FAIL"
                jout["sign_failure"] = ("tip displacement criteria disagree "
                                        "or are ambiguous")
            jout["tip_at_range_min"] = tip_by_k[0]
            jout["tip_at_range_max"] = tip_by_k[8]
            jout["tip_head_distance_min_end_mm"] = d0
            jout["tip_head_distance_max_end_mm"] = d8
            jout["extension_sign_s"] = s_j
            jout["theta_ext_rad"] = theta_ext
        joints_out[joint] = jout
        all_pass = all_pass and jout["verdict"] == "PASS"
        print(joint, jout["verdict"], "max_err",
              round(jout["max_steady_state_error_rad"], 4),
              "s", jout.get("extension_sign_s"), flush=True)

    sim.close()
    result = {"step": "Q2 (rerun3)", "settle_chunks": st["n_chunks"],
              "predictions_artefact": "results/body_qualification/q2_predictions_prereg.json",
              "predictions_computed_at_utc": prereg["computed_at_utc"],
              "joints": joints_out,
              "verdict": "PASS" if all_pass else "FAIL",
              "wall_clock_s": time.time() - t0}
    out = RESULTS / "q2_rerun3.json"
    out.write_text(json.dumps(result, indent=2))
    print("Q2 verdict:", result["verdict"], "wall", result["wall_clock_s"])
    print("wrote", out)


if __name__ == "__main__":
    main()
