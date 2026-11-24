"""Exploration only — facts needed by the rerun3 gate scripts."""
import sys
from pathlib import Path

import mujoco as mj
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import build_sim

fly, world, sim = build_sim(with_adhesion=True)
m = sim.mj_model

print("--- bodysegs order ---")
for i, s in enumerate(fly.get_bodysegs_order()):
    print(i, s.name)

print("\n--- adhesion actuators in compiled model ---")
for i in range(m.nu):
    name = mj.mj_id2name(m, mj.mjtObj.mjOBJ_ACTUATOR, i)
    if "adhesion" in name:
        print("ACT", i, name, "ctrlrange", m.actuator_ctrlrange[i],
              "gainprm", m.actuator_gainprm[i])

print("\n--- ADHESION order via get_actuated_jointdofs_order ---")
try:
    from flygym.compose import ActuatorType
    order = fly.get_actuated_jointdofs_order(ActuatorType.ADHESION)
    for i, d in enumerate(order):
        print(i, d)
except Exception as e:
    print("ERR", type(e).__name__, e)

print("\n--- ground plane + a leg geom collision params ---")
gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "ground_plane")
print("ground_plane contype/conaffinity:", m.geom_contype[gid], m.geom_conaffinity[gid])
for gname in ("flybody/lf_tarsus5", "flybody/l_labrum", "flybody/l_labrum_lower"):
    gid2 = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, gname)
    print(gname, "-> id", gid2, end=" ")
    if gid2 >= 0:
        print("contype/conaffinity:", m.geom_contype[gid2], m.geom_conaffinity[gid2],
              "body:", mj.mj_id2name(m, mj.mjtObj.mjOBJ_BODY, m.geom_bodyid[gid2]))
    else:
        print()

print("\n--- geoms with 'labrum' in name ---")
for i in range(m.ngeom):
    name = mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, i)
    if name and "labrum" in name:
        print("GEOM", i, name, "type", m.geom_type[i], "size", m.geom_size[i])

print("\n--- contact force function smoke test ---")
f = sim.get_bodysegment_contact_forces(fly.name, ["l_labrum", "r_labrum"],
                                       ground_only=False)
print("forces shape", f.shape, f)
sim.close()
