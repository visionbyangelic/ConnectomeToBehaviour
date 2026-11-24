"""Q2 (§7.3): per-DoF static-map sweep on the FlyBody proboscis.

For each of the five proboscis DoFs: nine raw target points across the
published range, each commanded alone for a 0.5 s hold (raw ctrl = target;
the map is what is being measured), all other actuators at ctrl 0. Steady
state = mean angle over the final 0.1 s of the hold. Judged against the
clamped static map qhat_eff computed in-script from the pinned YAMLs.
Also records, per pitch joint, the labrum tip's steady-state positions at
the two range ends, from which the extension sign s_j and theta_ext are
frozen (the end where the tip sits farther from the head and lower).
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
                         build_sim, dof_index, labrum_tip_pos, qhat,
                         qhat_eff, settle)

HERE = Path(__file__).parent
HOLD_STEPS = 5000       # 0.5 s
STEADY_STEPS = 1000     # final 0.1 s
REEQ_STEPS = 5000       # 0.5 s re-equilibration at ctrl 0 before each sweep
WATCHED = PROBOSCIS + NECK


def main():
    t0 = time.time()
    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    ctrl = np.zeros(len(order))
    st = settle(sim, fly, ctrl)
    if not st["settled"]:
        out = {"step": "Q2", "verdict": "FAIL",
               "fail_reason": "initial settle did not complete within cap",
               "settle": st}
        (HERE / "results" / "q2_rerun.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2)[:1500])
        return
    head_id = mj.mj_name2id(sim.mj_model, mj.mjtObj.mjOBJ_BODY, "flybody/c_head")

    joints_out = {}
    all_pass = True
    for joint in PROBOSCIS:
        # re-equilibrate at ctrl 0 and take fresh rest values for this sweep
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
            expected = qhat_eff(joint, tgt)
            unclamped = qhat(joint, tgt)
            clamp_bound = unclamped < lo or unclamped > hi
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
                "qhat_eff_rad": expected,
                "qhat_unclamped_rad": float(unclamped),
                "clamp_bound": bool(clamp_bound),
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
        # return the driven joint to rest command
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)

        errs = [p["steady_state_error_rad"] for p in points]
        mono_ok, mono_notes = True, []
        for k in range(8):
            a, b = points[k], points[k + 1]
            if a["qhat_eff_rad"] == b["qhat_eff_rad"]:
                continue  # both clamped to the same limit: plateau expected
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
                "verdict": "PASS" if all(checks.values()) else "FAIL"}
        if joint in PITCH_JOINTS:
            t0p = np.array(tip_by_k[0]["tip_pos_mm"])
            t8p = np.array(tip_by_k[8]["tip_pos_mm"])
            h0p = np.array(tip_by_k[0]["head_pos_mm"])
            h8p = np.array(tip_by_k[8]["head_pos_mm"])
            d0 = float(np.linalg.norm(t0p - h0p))
            d8 = float(np.linalg.norm(t8p - h8p))
            # extension end: tip farther from the head and lower (toward
            # the food plane); s = +1 if that is the range_max end
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
    result = {"step": "Q2", "settle_chunks": st["n_chunks"],
              "joints": joints_out,
              "verdict": "PASS" if all_pass else "FAIL",
              "wall_clock_s": time.time() - t0}
    out = HERE / "results" / "q2_rerun.json"
    out.write_text(json.dumps(result, indent=2))
    print("Q2 verdict:", result["verdict"], "wall", result["wall_clock_s"])
    print("wrote", out)


if __name__ == "__main__":
    main()
