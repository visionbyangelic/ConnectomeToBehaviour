"""Q1 re-run (§7.2 as revised by Amendment Pass 2), 24 Nov 2026.

(a) The packaged FlyBodyPreprogrammedSteps replay, re-run fresh on the
    Demo C construction (code path identical to the first execution).
(b) First-party load-and-step: same construction, ctrl = 0 on all 102
    actuators, 2.0 s = 20,000 steps at dt = 1e-4 s, qpos/qvel recorded at
    every step, judged against the rest-behaviour bounds fixed in §7.2
    before this run: thorax height within [0.5*h0, 1.5*h0] (h0 = thorax
    height in the constructed initial state); every actuated joint's
    |qvel| < published range / 0.01 s (free joint excluded); no joint
    outside its published joints.yaml range by more than eps = 0.005 rad.
    The h0 sanity check runs BEFORE stepping: the neutral-pose standing
    thorax height read from the compiled model's qpos0 kinematics (feet
    at z = 0) must lie within the same band.
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
from q1_upstream_integrity import run_replay  # noqa: E402

HERE = Path(__file__).parent
N_STEPS = 20000


def part_b():
    fly, world, sim = build_sim(with_adhesion=False)
    m, d = sim.mj_model, sim.mj_data
    mj.mj_forward(m, d)  # initial state kinematics, before any step
    h0 = thorax_z(sim)

    # h0 sanity check from the model files: kinematics at qpos0 (the
    # FLYBODY_NEUTRAL keyframe the construction uses). Feet touch z = 0
    # there, so the thorax height at qpos0 is the standing height.
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
    worst_limit = {names[int(np.argmax(excursion.max(axis=0)))]:
                   float(excursion.max())}
    per_joint_max_excursion = {
        n: float(excursion[:, i].max()) for i, n in enumerate(names)
        if excursion[:, i].max() > 0}
    rostrum_exc = float(excursion[:, idx["c_head-c_rostrum-pitch"]].max())
    verdict = finite and thorax_ok and vel_ok and limit_ok
    np.savez_compressed(HERE.parents[1] / "results" / "body_qualification" / "q1b_trace.npz",
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
        "worst_limit_joint": worst_limit,
        "rostrum_max_excursion_rad": rostrum_exc,
        "per_joint_max_positive_excursion_rad": per_joint_max_excursion,
        "joint_limits_hold_within_eps": limit_ok,
        "verdict": "PASS" if verdict else "FAIL",
    }


def main():
    t0 = time.time()
    ra = run_replay()
    ta = time.time() - t0
    result = {"step": "Q1 (re-run)",
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
    out = HERE.parents[1] / "results" / "body_qualification" / "q1_rerun.json"
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2)[:3000])
    print("wrote", out)


if __name__ == "__main__":
    main()
