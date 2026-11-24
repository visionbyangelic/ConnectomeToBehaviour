"""Q5 diagnostic, fifth execution -- NOT a gate step, changes no verdict.

The fifth execution's Q5 recorded zero labrum-food force in both
attempts although the SS4.6 reach curve predicted a 0.022-0.034 mm
press at e = 1 on the pedestal arena. This diagnostic discriminates:
(a) are the food/pedestal collision pairs present in the compiled
model of q5_rerun5.build_arena? (b) in the dynamic episode posture at
e = 1, what is the true labrum-surface distance to the food geom and
to the ground plane (mj_geomDistance, the calibration's method)?
(c) does the kinematic posture (proboscis qpos forced to the chain's
e = 1 angles in the same settled body, clearance-check style) give a
different distance -- i.e. is the gap dynamic (posture/joint
deflection under load) or present in both?
"""

import json
from pathlib import Path

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (CHUNK_STEPS, PITCH_JOINTS, PROBOSCIS, dof_index,  # noqa: E402
                         settle)
from gate_common3 import RESULTS, compiled_params, labrum_tip_pos  # noqa: E402
from gate_common5 import chain_ctrl_rev, theta_ext_from_params  # noqa: E402
from q5_rerun5 import build_arena  # noqa: E402

FROMTO = np.zeros(6)


def gdist(m, d, g1, g2):
    return float(mj.mj_geomDistance(m, d, g1, g2, 2.0, FROMTO))


def main():
    q5 = json.loads((RESULTS / "q5_rerun5.json").read_text())
    q2 = json.loads((RESULTS / "q2_rerun5.json").read_text())
    signs = {j: q2["joints"][j]["extension_sign_s"] for j in PITCH_JOINTS}
    centre = q5["attempts"][-1]["arena_centre_xy_mm"]  # attempt 2 centre

    fly, world, sim = build_arena(centre)
    m, d = sim.mj_model, sim.mj_data
    food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
    ped_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "pedestal")
    ground_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "ground")
    lab = [mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n) for n in
           ("flybody/l_labrum_lower", "flybody/r_labrum_lower")]
    pair_count = {"food": 0, "pedestal": 0}
    for i in range(m.npair):
        g1, g2 = int(m.pair_geom1[i]), int(m.pair_geom2[i])
        if food_gid in (g1, g2):
            pair_count["food"] += 1
        if ped_gid in (g1, g2):
            pair_count["pedestal"] += 1

    idx, order = dof_index(fly)
    params = compiled_params(sim)
    theta_ext = theta_ext_from_params(params, signs)
    st = settle(sim, fly, np.zeros(len(order)))
    assert st["settled"]
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    thorax_id = mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, "flybody/c_thorax")

    def measure(tag):
        mj.mj_forward(m, d)
        return {
            "tag": tag,
            "labrum_to_food_mm": [gdist(m, d, g, food_gid) for g in lab],
            "labrum_to_ground_mm": [gdist(m, d, g, ground_gid) for g in lab],
            "tip_xyz_mm": [float(x) for x in labrum_tip_pos(sim)],
            "thorax_z_mm": float(d.xpos[thorax_id][2]),
            "ncon": int(d.ncon),
            "ncon_food_or_pedestal": int(sum(
                1 for i in range(d.ncon)
                if food_gid in (int(d.contact.geom1[i]),
                                int(d.contact.geom2[i]))
                or ped_gid in (int(d.contact.geom1[i]),
                               int(d.contact.geom2[i])))),
        }

    out = {"arena_centre_xy_mm": centre,
           "compiled_pairs_involving": pair_count,
           "food_geom_pos": [float(x) for x in m.geom_pos[food_gid]],
           "food_top_z_mm": float(m.geom_pos[food_gid][2]
                                  + m.geom_size[food_gid][1])}
    out["at_rest"] = measure("settled, e = 0")

    # dynamic: ramp to e = 1 over 5 chunks, hold 10 chunks
    for k in range(5):
        e = (k + 1) / 5
        ctrl = chain_ctrl_rev(np.zeros(len(order)), idx, params, e, rest,
                              theta_ext)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(CHUNK_STEPS):
            sim.step()
    min_food = [1e9, 1e9]
    for _ in range(10):
        ctrl = chain_ctrl_rev(np.zeros(len(order)), idx, params, 1.0, rest,
                              theta_ext)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(CHUNK_STEPS):
            sim.step()
            mj.mj_forward(m, d)
            for i, g in enumerate(lab):
                min_food[i] = min(min_food[i], gdist(m, d, g, food_gid))
    out["dynamic_e1_hold"] = measure("after dynamic ramp + 10-chunk hold")
    out["dynamic_e1_hold_min_labrum_to_food_mm"] = min_food

    # kinematic: force the five proboscis qpos to the chain's e = 1
    # achieved angles in the same body state, clearance-check style
    qadr = {j: int(m.jnt_qposadr[params[j]["joint_id"]]) for j in PROBOSCIS}
    for j in PROBOSCIS:
        target = theta_ext.get(j, rest[j])  # yaw: held at rest, no theta_ext
        d.qpos[qadr[j]] = rest[j] + 1.0 * (target - rest[j])
    out["kinematic_e1_same_body"] = measure(
        "proboscis qpos forced to chain e = 1 angles, same body state")
    sim.close()

    out_path = RESULTS / "q5_diagnostic5.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    print("wrote", out_path)


if __name__ == "__main__":
    main()
