"""Exploration only — how do contacts happen in this model?"""
import sys
from pathlib import Path

import mujoco as mj
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import build_sim

fly, world, sim = build_sim(with_adhesion=True)
m, d = sim.mj_model, sim.mj_data

print("npair:", m.npair)
for i in range(min(m.npair, 10)):
    g1 = mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, m.pair_geom1[i])
    g2 = mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, m.pair_geom2[i])
    print("PAIR", i, g1, "<->", g2, "contype/conaffinity via pair?", )

cts = {}
for i in range(m.ngeom):
    key = (int(m.geom_contype[i]), int(m.geom_conaffinity[i]))
    cts[key] = cts.get(key, 0) + 1
print("geom (contype, conaffinity) histogram:", cts)

# step 1 s at ctrl 0 and inspect contacts
from flygym.compose import ActuatorType
order = fly.get_actuated_jointdofs_order(ActuatorType.POSITION)
sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, np.zeros(len(order)))
for _ in range(10000):
    sim.step()
print("ncon after settle:", d.ncon)
seen = {}
for i in range(d.ncon):
    g1 = mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, d.contact.geom1[i])
    g2 = mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, d.contact.geom2[i])
    seen[(g1, g2)] = seen.get((g1, g2), 0) + 1
for k, v in sorted(seen.items()):
    print("CONTACT", v, k)

# adhesion internal ids
from flygym.compose import ActuatorType as AT
ids = sim._intern_actuatorids_by_type_by_fly[AT.ADHESION][fly.name]
print("adhesion ids via ADHESION type:", ids,
      [mj.mj_id2name(m, mj.mjtObj.mjOBJ_ACTUATOR, int(a)) for a in ids])
sim.close()
