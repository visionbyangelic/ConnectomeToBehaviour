"""Q1, third execution (SS7.2 as revised by Amendment Pass 2), 24 Nov 2026.

Identical procedure to the second execution (q1_rerun.py), rerun3 outputs:
(a) the packaged FlyBodyPreprogrammedSteps replay, fresh, on the Demo C
    construction (102 actuators, published gains, no overrides);
(b) first-party load-and-step: ctrl = 0 on all 102 actuators, 2.0 s =
    20,000 steps at dt = 1e-4 s, qpos/qvel recorded at every step, judged
    against SS7.2's rest-behaviour bounds: thorax height within
    [0.5*h0, 1.5*h0] (h0 = initial-state thorax height, sanity-checked
    against the neutral-pose standing height BEFORE stepping); every
    actuated joint's |qvel| < published range / 0.01 s (free joint
    excluded); no joint outside its published range by more than
    eps = 0.005 rad at any step. Pass 5 expectation: no limit-resting in
    the proboscis (ctrl-0 equilibria ~ 0, interior).
"""

import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import EPS, RANGES, build_sim, dof_index, thorax_z  # noqa: E402
from gate_common3 import RESULTS  # noqa: E402
from q1_upstream_integrity import run_replay  # noqa: E402

N_STEPS = 20000


def part_b():
    fly, world, sim = build_sim(with_adhesion=False)
    m, d = sim.mj_model, sim.mj_data
    mj.mj_forward(m, d)
    h0 = thorax_z(sim)

    d2 = mj.MjData(m)
    d2.qpos[:] = m.qpos0
    mj.mj_forward(m, d2)
    tbody = mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, "flybody/c_thorax")
    standing = float(d2.xpos[tbody, 2])
    min_geom_z = float(d2.geom_xpos[:, 2].min())
    band = [0.5 * h0, 1.5 * h0]
    sanity_ok = band[0] <= standing <= band[1] and abs(min_geom_z) < 1e-9
    sanity = {"h0_mm": h0, "band_mm": band,
              "neutral_standing_thorax_height_mm": standing,
              "min_geom_z_at_qpos0_mm": min_geom_z,
              "sanity_check_pass": bool(sanity_ok)}
    if not sanity_ok:
        sim.close()
        return {"executed": False, "h0_sanity": sanity, "verdict": "FAIL",
                "fail_reason": "h0 sanity check failed; (b) not stepped"}

    idx, order = dof_index(fly)
    names = [dof.name for dof in order]
    vel_bound = np.array([(RANGES[n][1] - RANGES[n][0]) / 0.01 for n in names])
    range_lo = np.array([RANGES[n][0] for n in names])
    range_hi = np.array([RANGES[n][1] for n in names])

    sim.set_actuator_inputs(fly.name, ActuatorType.POSITION,
                            np.zeros(len(order)))
    qpos = np.empty((N_STEPS, m.nq))
    qvel = np.empty((N_STEPS, m.nv))
    angles = np.empty((N_STEPS, len(order)))
    vels = np.empty((N_STEPS, len(order)))
    thorax = np.empty(N_STEPS)
    for s in range(N_STEPS):
        sim.step()
        qpos[s] = d.qpos
        qvel[s] = d.qvel
        angles[s] = sim.get_joint_angles(fly.name)
        vels[s] = sim.get_joint_velocities(fly.name)
        thorax[s] = thorax_z(sim)
    sim.close()

    finite = bool(np.isfinite(qpos).all() and np.isfinite(qvel).all())
    thorax_ok = bool((thorax >= band[0]).all() and (thorax <= band[1]).all())
    vel_ratio = np.abs(vels) / vel_bound
    vel_ok = bool((vel_ratio < 1.0).all())
    excursion = np.maximum(range_lo - angles, angles - range_hi)
    limit_ok = bool((excursion <= EPS).all())
    verdict = finite and thorax_ok and vel_ok and limit_ok
    np.savez_compressed(RESULTS / "q1b_trace_rerun3.npz",
                        qpos=qpos, qvel=qvel, angles=angles, vels=vels,
                        thorax_z=thorax, dof_names=np.array(names))
    return {
        "executed": True,
        "h0_sanity": sanity,
        "n_steps": N_STEPS, "dt_s": float(m.opt.timestep),
        "all_states_finite": finite,
        "thorax_min_mm": float(thorax.min()), "thorax_max_mm": float(thorax.max()),
        "thorax_final_mm": float(thorax[-1]),
        "thorax_within_band_every_step": thorax_ok,
        "max_velocity_ratio_to_bound": float(vel_ratio.max()),
        "velocity_bound_holds_every_step": vel_ok,
        "max_limit_excursion_rad": float(excursion.max()),
        "joint_limits_hold_within_eps": limit_ok,
        "proboscis_final_angles_rad": {
            n: float(angles[-1, idx[n]]) for n in
            ("c_head-c_rostrum-pitch", "c_rostrum-c_haustellum-pitch",
             "c_rostrum-c_haustellum-yaw", "c_haustellum-l_labrum-pitch",
             "c_haustellum-r_labrum-pitch")},
        "verdict": "PASS" if verdict else "FAIL",
    }


def main():
    t0 = time.time()
    ra = run_replay()
    ta = time.time() - t0
    result = {"step": "Q1 (rerun3)",
              "part_a_replay": {"verdict": ra["verdict"],
                                "n_steps": ra["n_physics_steps"],
                                "all_states_finite": ra["all_states_finite"],
                                "thorax_travel_mm": ra["thorax_travel_mm"],
                                "wall_clock_s": ta}}
    t1 = time.time()
    rb = part_b()
    result["part_b_load_and_step"] = rb
    result["part_b_load_and_step"]["wall_clock_s"] = time.time() - t1
    result["verdict"] = ("PASS" if ra["verdict"] == "PASS"
                         and rb["verdict"] == "PASS" else "FAIL")
    result["wall_clock_s"] = time.time() - t0
    out = RESULTS / "q1_rerun3.json"
    out.write_text(json.dumps(result, indent=2))
    print("Q1(a):", result["part_a_replay"])
    print("Q1(b): verdict", rb["verdict"], "| thorax",
          rb.get("thorax_min_mm"), "-", rb.get("thorax_max_mm"),
          "| max vel ratio", rb.get("max_velocity_ratio_to_bound"),
          "| max excursion", rb.get("max_limit_excursion_rad"))
    print("Q1 verdict:", result["verdict"], "wall", result["wall_clock_s"])
    print("wrote", out)


if __name__ == "__main__":
    main()
