"""Diagnostic for the onset check (calibration, NOT a gate step).

The onset check found: under the revised Pass 6 chain, a dynamic
chunked ramp and a quasi-static 0.4 s-hold sweep agree on the labrum
surface to 0.0001 mm (R = 0.2966 dynamic / 0.2968 quasi-static),
while the reach curve (old, pre-Pass-6 chain; slow 41-point sweep)
read R = 0.3083. This diagnostic isolates why, at e = 1 in the plain
construction: (a) old chain, single 0.4 s hold; (b) old chain, the
reach curve's own 41-step sweep; (c) revised chain, single hold;
(d) revised chain, 41-step sweep; (e) old chain, Q5-style chunked
ramp. All five angles, thorax height and z_true recorded per case.
"""

import json

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (CHUNK_STEPS, PITCH_JOINTS, PROBOSCIS, build_sim,  # noqa: E402
                         dof_index, settle)
from gate_common3 import (LABRUM_GEOM_NAMES, compiled_params, chain_ctrl,  # noqa: E402
                          extension_E)
from gate_common5 import chain_ctrl_rev, theta_ext_from_params  # noqa: E402

SIGNS = {j: -1 for j in PITCH_JOINTS}
OLD_THETA_EXT = {"c_head-c_rostrum-pitch": -1.19,
                 "c_rostrum-c_haustellum-pitch": -1.54}
from gate_common import thorax_z  # noqa: E402


def fresh():
    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    st = settle(sim, fly, np.zeros(len(order)))
    assert st["settled"]
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    return fly, sim, idx, order, rest


def probe(sim, fly, idx, rest):
    m, d = sim.mj_model, sim.mj_data
    planes = [g for g in range(m.ngeom)
              if m.geom_type[g] == mj.mjtGeom.mjGEOM_PLANE]
    z = min(float(mj.mj_geomDistance(
        m, d, mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n), planes[0],
        10.0, None)) for n in LABRUM_GEOM_NAMES)
    angles_all = sim.get_joint_angles(fly.name)
    by = {j: float(angles_all[idx[j]]) for j in PROBOSCIS}
    return {"angles_rad": by, "E_rad": extension_E(by, rest, SIGNS),
            "z_true_mm": z, "thorax_z_mm": thorax_z(sim)}


def hold(sim, fly, ctrl, steps):
    sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
    for _ in range(steps):
        sim.step()


out = {}

# (a) old chain, single 0.4 s hold at e = 1
fly, sim, idx, order, rest = fresh()
params = compiled_params(sim)
ctrl = chain_ctrl(np.zeros(len(order)), idx, params, 1.0, rest, SIGNS,
                  OLD_THETA_EXT)
hold(sim, fly, ctrl, 4000)
out["a_old_single_hold"] = probe(sim, fly, idx, rest)
hold(sim, fly, ctrl, 20000)          # +2 s: creep under sustained load?
out["a_old_single_hold_plus2s"] = probe(sim, fly, idx, rest)
sim.close()

# (b) old chain, the reach curve's 41-step sweep
fly, sim, idx, order, rest = fresh()
params = compiled_params(sim)
for k in range(41):
    e = k / 40
    ctrl = chain_ctrl(np.zeros(len(order)), idx, params, e, rest, SIGNS,
                      OLD_THETA_EXT)
    hold(sim, fly, ctrl, 4000)
out["b_old_sweep41"] = probe(sim, fly, idx, rest)
sim.close()

# (c) revised chain, single 0.4 s hold at e = 1
fly, sim, idx, order, rest = fresh()
params = compiled_params(sim)
theta_ext = theta_ext_from_params(params, SIGNS)
ctrl = chain_ctrl_rev(np.zeros(len(order)), idx, params, 1.0, rest,
                      theta_ext)
hold(sim, fly, ctrl, 4000)
out["c_rev_single_hold"] = probe(sim, fly, idx, rest)
hold(sim, fly, ctrl, 20000)
out["c_rev_single_hold_plus2s"] = probe(sim, fly, idx, rest)
sim.close()

# (d) revised chain, 41-step sweep
fly, sim, idx, order, rest = fresh()
params = compiled_params(sim)
theta_ext = theta_ext_from_params(params, SIGNS)
for k in range(41):
    e = k / 40
    ctrl = chain_ctrl_rev(np.zeros(len(order)), idx, params, e, rest,
                          theta_ext)
    hold(sim, fly, ctrl, 4000)
out["d_rev_sweep41"] = probe(sim, fly, idx, rest)
sim.close()

# (e) old chain, Q5-style chunked ramp (5 x 100 ms), then 0.4 s hold
fly, sim, idx, order, rest = fresh()
params = compiled_params(sim)
for i in range(5):
    ctrl = chain_ctrl(np.zeros(len(order)), idx, params, (i + 1) / 5,
                      rest, SIGNS, OLD_THETA_EXT)
    hold(sim, fly, ctrl, CHUNK_STEPS)
out["e_old_chunked_ramp"] = probe(sim, fly, idx, rest)
hold(sim, fly, ctrl, 4000)
out["e_old_chunked_ramp_plus04s"] = probe(sim, fly, idx, rest)
sim.close()

for k, v in out.items():
    print(k, "| z_true =", round(v["z_true_mm"], 4),
          "| E =", round(v["E_rad"], 4),
          "| thorax_z =", round(v["thorax_z_mm"], 4),
          "| labrum L/R =",
          round(v["angles_rad"]["c_haustellum-l_labrum-pitch"], 4),
          round(v["angles_rad"]["c_haustellum-r_labrum-pitch"], 4),
          "| rostrum =", round(v["angles_rad"]["c_head-c_rostrum-pitch"], 4),
          "| haust =", round(v["angles_rad"]["c_rostrum-c_haustellum-pitch"], 4))
print(json.dumps({k: v["z_true_mm"] for k, v in out.items()}, indent=1))
