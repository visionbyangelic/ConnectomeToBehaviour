"""Post-failure diagnostic for the Q2 FAIL (NOT a gate step; no re-judging).

Two purposes, both factual:
1. Recompute, from the recorded Q2 steady states, the fit of the map with
   springref = 0 — the reference the compiled model actually carries
   (qpos0 = 0 for all five proboscis joints, verified here from the
   compiled model). This identifies the failure as a premise error in
   §4.3's map (springref 0.8 read from joints.yaml), not a body defect.
2. Re-measure the labrum tip displacement at the two pitch joints' range
   ends with corrected geom sampling (the gate script's name lookup
   resolved to geom id -1; the labrum geoms are 'l_labrum_lower' /
   'r_labrum_lower', one per labrum body), so the record carries the
   extension-sign determination the panel will need. The Q2 verdict is
   unchanged: FAIL on criterion (i) under the preregistered map.
"""

import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (KP, KS, PITCH_JOINTS, PROBOSCIS, RANGES,  # noqa: E402
                         build_sim, dof_index, settle)

HERE = Path(__file__).parent
HOLD_STEPS = 5000
STEADY_STEPS = 1000


def qhat_eff_ref0(joint, ctrl):
    lo, hi = RANGES[joint]
    q = KP[joint] * ctrl / (KP[joint] + KS[joint])  # springref = 0
    return float(min(max(q, lo), hi))


def main():
    t0 = time.time()
    out = {"diagnostic_for": "Q2 FAIL, criterion (i), pitch joints",
           "is_gate_step": False}

    # (0) compiled spring references
    fly, world, sim = build_sim(with_adhesion=True)
    m = sim.mj_model
    table = {}
    for jn in PROBOSCIS:
        jid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_JOINT, f"flybody/{jn}")
        table[jn] = {"qpos0_spring_reference": float(m.qpos0[m.jnt_qposadr[jid]]),
                     "jnt_stiffness": float(m.jnt_stiffness[jid])}
    out["compiled_spring_reference"] = table

    # (1) ref=0 map fit against the recorded Q2 steady states
    q2 = json.loads((HERE.parents[1] / "results" / "body_qualification" / "q2_rerun.json").read_text())
    fit = {}
    for jn, j in q2["joints"].items():
        errs = [abs(p["steady_state_rad"] - qhat_eff_ref0(jn, p["target_ctrl"]))
                for p in j["points"]]
        fit[jn] = {"max_error_ref0_map_rad": max(errs),
                   "errors_ref0_map_rad": errs}
    out["ref0_map_fit_from_recorded_q2"] = fit

    # (2) corrected tip sampling at the pitch joints' range ends
    idx, order = dof_index(fly)
    ctrl = np.zeros(len(order))
    st = settle(sim, fly, ctrl)
    out["settle_chunks"] = st["n_chunks"]
    labrum_gids = []
    for seg in ("l_labrum", "r_labrum"):
        bid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, f"flybody/{seg}")
        labrum_gids += [g for g in range(m.ngeom) if m.geom_bodyid[g] == bid]
    head_id = mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, "flybody/c_head")

    def tip():
        return np.mean([sim.mj_data.geom_xpos[g] for g in labrum_gids], axis=0)

    signs = {}
    for joint in PITCH_JOINTS:
        lo, hi = RANGES[joint]
        ends = {}
        for label, tgt in (("range_min", lo), ("range_max", hi)):
            c = ctrl.copy()
            c[idx[joint]] = tgt
            sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, c)
            for _ in range(HOLD_STEPS):
                sim.step()
            ends[label] = {"tip_pos_mm": [float(x) for x in tip()],
                           "head_pos_mm": [float(x) for x in
                                           sim.mj_data.xpos[head_id]]}
            sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
            for _ in range(HOLD_STEPS):
                sim.step()
        tmin = np.array(ends["range_min"]["tip_pos_mm"])
        tmax = np.array(ends["range_max"]["tip_pos_mm"])
        dmin = float(np.linalg.norm(tmin - np.array(ends["range_min"]["head_pos_mm"])))
        dmax = float(np.linalg.norm(tmax - np.array(ends["range_max"]["head_pos_mm"])))
        ext_at_max = (dmax > dmin) and (tmax[2] < tmin[2])
        ext_at_min = (dmin > dmax) and (tmin[2] < tmax[2])
        if ext_at_max and not ext_at_min:
            s_j, theta_ext = 1, hi - 0.05
        elif ext_at_min and not ext_at_max:
            s_j, theta_ext = -1, lo + 0.05
        else:
            s_j, theta_ext = None, None
        signs[joint] = {"ends": ends,
                        "tip_head_distance_min_end_mm": dmin,
                        "tip_head_distance_max_end_mm": dmax,
                        "extension_sign_s": s_j, "theta_ext_rad": theta_ext}
    out["extension_signs_corrected_sampling"] = signs
    sim.close()
    out["wall_clock_s"] = time.time() - t0
    p = HERE.parents[1] / "results" / "body_qualification" / "q2_diagnostic.json"
    p.write_text(json.dumps(out, indent=2))
    print(json.dumps({"ref0_max_errors": {k: round(v["max_error_ref0_map_rad"], 4)
                                          for k, v in fit.items()},
                      "signs": {k: (v["extension_sign_s"], v["theta_ext_rad"])
                                for k, v in signs.items()}}, indent=2))
    print("wrote", p)


if __name__ == "__main__":
    main()
