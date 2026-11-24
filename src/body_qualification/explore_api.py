"""Exploration only — dump FlyBody API facts needed by the gate scripts."""
import sys
from pathlib import Path

import mujoco as mj
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from q1_upstream_integrity import build_flybody

from flygym.compose import ActuatorType
from flygym.compose.world.flat_ground import FlatGroundWorld
from flygym.simulation import Simulation
from flygym.utils.math import Rotation3D

fly = build_flybody()
adh = fly.add_leg_adhesion()
print("adhesion actuators:", {k: v.name for k, v in adh.items()})

world = FlatGroundWorld()
world.add_fly(fly, (0, 0, 1.0), Rotation3D("quat", (1, 0, 0, 0)))
sim = Simulation(world)
sim.reset()
m = sim.mj_model

print("\n--- sites order ---")
for i, s in enumerate(fly.get_sites_order()):
    print(i, s.name)

print("\n--- bodysegs order ---")
for i, s in enumerate(fly.get_bodysegs_order()):
    print(i, s.name)

print("\n--- POSITION actuator order (proboscis/neck only) ---")
order = fly.get_actuated_jointdofs_order(ActuatorType.POSITION)
for i, d in enumerate(order):
    if any(k in d.name for k in ("rostrum", "haustellum", "labrum", "c_head", "c_thorax-c_head")):
        print(i, d.name)

print("\n--- compiled model: proboscis actuators/joints ---")
for i in range(m.nu):
    name = mj.mj_id2name(m, mj.mjtObj.mjOBJ_ACTUATOR, i)
    if any(k in name for k in ("rostrum", "haustellum", "labrum")):
        print("ACT", i, name, "ctrlrange", m.actuator_ctrlrange[i],
              "ctrllimited", bool(m.actuator_ctrllimited[i]))
for j in range(m.njnt):
    name = mj.mj_id2name(m, mj.mjtObj.mjOBJ_JOINT, j)
    if any(k in name for k in ("rostrum", "haustellum", "labrum")):
        print("JNT", j, name, "range", m.jnt_range[j], "solref", m.jnt_solref[j],
              "solimp", m.jnt_solimp[j], "armature", m.dof_armature[m.jnt_dofadr[j]])

print("\n--- adhesion actuator ids in compiled model ---")
for k, el in adh.items():
    aid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_ACTUATOR, el.name)
    print(k, el.name, "->", aid)

print("\n--- heights ---")
body_order = [s.name for s in fly.get_bodysegs_order()]
thorax_idx = body_order.index("c_thorax")
pos = sim.get_body_positions(fly.name)
print("thorax pos initial (after reset):", pos[thorax_idx])
print("qpos0[:7]:", m.qpos0[:7])
d2 = mj.MjData(m)
d2.qpos[:] = m.qpos0
mj.mj_forward(m, d2)
tbody = mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, "flybody/c_thorax")
print("thorax z at qpos0 (mj_forward):", d2.xpos[tbody])
# lowest geom z at qpos0 among leg geoms
print("min geom z at qpos0:", d2.geom_xpos[:, 2].min())
print("nq", m.nq, "nv", m.nv, "nu", m.nu)
sim.close()
