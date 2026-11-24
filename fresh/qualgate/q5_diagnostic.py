"""Q5 diagnostic (NOT a gate step), 24 Nov 2026.

The Q5 attempts recorded zero labrum-food contact. Before the failure is
attributed, check the implementation: (a) do food pairs exist in the
compiled arena model; (b) where is the labrum tip, in 3D, at full
extension relative to the food disc; (c) can the labrum geoms physically
reach the food's top surface at all (minimum geom distance at e = 1).
"""

import json
from pathlib import Path

import mujoco as mj
import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import CHUNK_STEPS, PITCH_JOINTS, PROBOSCIS, dof_index, settle  # noqa: E402
from gate_common3 import (RESULTS, chain_ctrl, compiled_params,  # noqa: E402
                          labrum_tip_pos)
from q5_rerun3 import build_arena  # noqa: E402


def main():
    q5 = json.loads((RESULTS / "q5_rerun3.json").read_text())
    q2 = json.loads((RESULTS / "q2_rerun3.json").read_text())
    signs = {j: q2["joints"][j]["extension_sign_s"] for j in PITCH_JOINTS}
    theta_ext = {j: q2["joints"][j]["theta_ext_rad"] for j in PITCH_JOINTS}
    centre = q5["attempts"][1]["food_centre_xy_mm"]  # adjusted placement

    fly, world, sim = build_arena(centre)
    m, d = sim.mj_model, sim.mj_data
    food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
    pairs_with_food = [(m.pair_geom1[p], m.pair_geom2[p])
                       for p in range(m.npair)
                       if food_gid in (m.pair_geom1[p], m.pair_geom2[p])]
    print("food geom id:", food_gid, "| pairs involving food:", len(pairs_with_food))
    print("food geom pos:", d.geom_xpos[food_gid], "size:", m.geom_size[food_gid])

    idx, order = dof_index(fly)
    params = compiled_params(sim)
    st = settle(sim, fly, np.zeros(len(order)))
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    tip_rest = labrum_tip_pos(sim)
    print("tip at rest:", tip_rest)

    for i in range(10):  # ramp + hold at e = 1 for 1 s
        e = min(1.0, (i + 1) / 5)
        ctrl = chain_ctrl(np.zeros(len(order)), idx, params, e, rest,
                          signs, theta_ext)
        from flygym.compose import ActuatorType
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(CHUNK_STEPS):
            sim.step()
    tip_ext = labrum_tip_pos(sim)
    print("tip at e=1:", tip_ext, "| tip z above food top (0.05):",
          tip_ext[2] - 0.05)
    for name in ("flybody/l_labrum_lower", "flybody/r_labrum_lower"):
        gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, name)
        dist = mj.mj_geomDistance(m, d, gid, food_gid, 10.0, None)
        print(f"geomDistance {name} <-> food: {dist:.4f} mm",
              "| geom centre:", d.geom_xpos[gid], "| rbound:", m.geom_rbound[gid])
    # any contacts at all involving food right now?
    food_contacts = [c for c in range(d.ncon)
                     if food_gid in (d.contact[c].geom1, d.contact[c].geom2)]
    print("active contacts involving food at e=1:", len(food_contacts))
    out = {
        "artefact": "q5_diagnostic (not a gate step)",
        "food_centre_xy_mm": centre,
        "food_geom_id": int(food_gid),
        "food_pairs_in_compiled_model": len(pairs_with_food),
        "food_compiled_geom_pos_mm": [float(x) for x in m.geom_pos[food_gid]],
        "tip_at_rest_mm": [float(x) for x in tip_rest],
        "tip_at_e1_mm": [float(x) for x in tip_ext],
        "tip_centre_height_above_food_top_mm": float(tip_ext[2] - 0.05),
        "geom_distance_labrum_to_food_mm": {
            "l_labrum_lower": float(mj.mj_geomDistance(
                m, d, mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM,
                                    "flybody/l_labrum_lower"),
                food_gid, 10.0, None)),
            "r_labrum_lower": float(mj.mj_geomDistance(
                m, d, mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM,
                                    "flybody/r_labrum_lower"),
                food_gid, 10.0, None))},
        "active_contacts_involving_food_at_e1": len(food_contacts),
        "note": ("geom_xpos printed as [0,0,0] before the first step in an "
                 "earlier console run was a stale pre-forward array; the "
                 "compiled geom_pos above is the placed position and the "
                 "attempts stepped thousands of steps before judging."),
    }
    (RESULTS / "q5_diagnostic.json").write_text(json.dumps(out, indent=2))
    print("wrote", RESULTS / "q5_diagnostic.json")
    sim.close()


if __name__ == "__main__":
    main()
