"""Q1 — unmodified upstream integrity (PART4-SENSORY-SPECS §7.2).

§7.2 names two pieces of upstream material:

  (a) the packaged FlyBody single-step assets, replayed through the packaged
      `FlyBodyPreprogrammedSteps` class (flygym_demo/complex_terrain/) on the
      pinned FlyBody;
  (b) a load-and-step of the flygym_demo/muscle_imitation/ environment.

Pass, per §7.2: both run without error, and all recorded body states are
finite over their durations.

Part (a) below does exactly that. The fly is built the way the Part 1b audit
built it (Demo C: ALL_BIOLOGICAL skeleton, ALL actuated-DoF preset, the
published FLYBODY_NEUTRAL pose, no gain overrides — so the actuators carry
their published parameters from the pinned actuators.yaml). The replay drives
the six legs through the packaged step trajectories with a tripod phase
offset; every other actuator is held at its neutral input. Nothing about the
body is modified: the script commands published actuators and records what
the physics does.

Part (b) is recorded, not run — see the gate record
(docs/feeding_body_qualification.md) for the full account. In short: the
demo's env module requires the optional dependency `gymnasium`, which is not
installed in the pinned body env (the module raises ImportError by its own
design), and the model that demo wraps is the FlyMimic musculoskeletal body,
not FlyBody. This script checks the dependency fact programmatically and
records the sub-item as NOT EXECUTED; §7.2's pass criterion ("both run
without error") is therefore not met, and the step verdict is FAIL with the
sub-verdicts preserved.
"""

import importlib.util
import json
import time
import traceback
from pathlib import Path

import numpy as np

from flygym.compose import ActuatorType
from flygym.compose.pose import KinematicPosePreset
from flygym.compose.world.flat_ground import FlatGroundWorld
from flygym.simulation import Simulation
from flygym.utils.math import Rotation3D

LEGS = ("lf", "lm", "lh", "rf", "rm", "rh")
# Tripod gait: these two leg triples step half a cycle apart.
TRIPOD_OFFSET = {"lf": 0.0, "rm": 0.0, "rh": 0.0,
                 "rf": np.pi, "lm": np.pi, "lh": np.pi}
REPLAY_SECONDS = 2.0


def build_flybody():
    """The Part 1b Demo C construction, unchanged."""
    from flygym.compose.fly.flybody import FlyBody
    from flygym.flybody.anatomy_flybody import (
        FlyBodyActuatedDOFPreset,
        FlyBodyAxisOrder,
        FlyBodyJointPreset,
        FlyBodySkeleton,
    )

    skeleton = FlyBodySkeleton(
        axis_order=FlyBodyAxisOrder.YAW_ROLL_PITCH,
        joint_preset=FlyBodyJointPreset.ALL_BIOLOGICAL,
    )
    fly = FlyBody(name="flybody")
    neutral = KinematicPosePreset.FLYBODY_NEUTRAL.get_pose_by_axis_order(
        FlyBodyAxisOrder.YAW_ROLL_PITCH
    )
    fly.add_joints(skeleton, neutral_pose=neutral)
    actuated = skeleton.get_actuated_dofs_from_preset(FlyBodyActuatedDOFPreset.ALL)
    fly.add_actuators(actuated, ActuatorType.POSITION, neutral_input=neutral)
    return fly


def leg_ctrl_indices(fly):
    """Map (leg, dof-spec) -> index in the POSITION actuator order.

    The packaged steps class returns seven angles per leg in its own
    _DOFS_PER_LEG order; FlyBody's DoF names spell the same segments out
    (e.g. ("thorax", "coxa", "pitch") is "c_thorax-lf_coxa-pitch"). Any DoF
    the mapping cannot find is reported rather than silently dropped.
    """
    from flygym_demo.complex_terrain.preprogrammed import _DOFS_PER_LEG

    order = fly.get_actuated_jointdofs_order(ActuatorType.POSITION)
    index_of = {d.name: i for i, d in enumerate(order)}
    mapping, missing = {}, []
    for leg in LEGS:
        for spec in _DOFS_PER_LEG:
            seg_a, seg_b, axis = spec
            a = "c_thorax" if seg_a == "thorax" else f"{leg}_{seg_a}"
            name = f"{a}-{leg}_{seg_b}-{axis}"
            if name in index_of:
                mapping[(leg, spec)] = index_of[name]
            else:
                missing.append(name)
    return mapping, missing


def run_replay():
    """Part (a): replay the packaged FlyBody steps; record state finiteness."""
    from flygym_demo.complex_terrain import FlyBodyPreprogrammedSteps
    from flygym_demo.complex_terrain.preprogrammed import _DOFS_PER_LEG

    steps = FlyBodyPreprogrammedSteps()  # loads the packaged .npz asset
    asset_info = {
        "n_phase_bins": int(steps._length),
        "step_cycle_frequency_hz": float(steps.step_cycle_frequency_hz),
        "swing_fractions": {
            leg: [float(x) for x in steps.swing_period[leg]] for leg in steps.legs
        },
    }

    fly = build_flybody()
    world = FlatGroundWorld()
    world.add_fly(fly, (0, 0, 1.0), Rotation3D("quat", (1, 0, 0, 0)))
    sim = Simulation(world)
    sim.reset()

    order = fly.get_actuated_jointdofs_order(ActuatorType.POSITION)
    neutral_by_dof = fly.jointdof_to_neutralaction_by_type[ActuatorType.POSITION]
    base_ctrl = np.array([neutral_by_dof[d] for d in order], dtype=float)

    mapping, missing = leg_ctrl_indices(fly)
    if missing:
        raise RuntimeError(f"leg DoFs not found in actuator order: {missing}")

    body_order = fly.get_bodysegs_order()
    thorax_idx = [s.name for s in body_order].index("c_thorax")

    sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, base_ctrl)
    sim.warmup(0.05)

    dt = sim.timestep
    n_steps = int(REPLAY_SECONDS / dt)
    freq = steps.step_cycle_frequency_hz
    angles = np.empty((n_steps, len(order)))
    positions = np.empty((n_steps, len(body_order), 3))
    thorax_start = sim.get_body_positions(fly.name)[thorax_idx].copy()

    for k in range(n_steps):
        t = k * dt
        ctrl = base_ctrl.copy()
        for leg in LEGS:
            phase = 2 * np.pi * freq * t + TRIPOD_OFFSET[leg]
            leg_angles = steps.get_joint_angles(leg, phase)
            for spec, value in zip(_DOFS_PER_LEG, leg_angles):
                ctrl[mapping[(leg, spec)]] = value
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        sim.step()
        angles[k] = sim.get_joint_angles(fly.name)
        positions[k] = sim.get_body_positions(fly.name)

    thorax_end = positions[-1, thorax_idx]
    finite = bool(np.isfinite(angles).all() and np.isfinite(positions).all())
    sim.close()
    return {
        "asset": asset_info,
        "n_actuated_dofs": len(order),
        "n_leg_dofs_driven": len(mapping),
        "replay_seconds": REPLAY_SECONDS,
        "n_physics_steps": n_steps,
        "all_states_finite": finite,
        "thorax_travel_mm": float(np.linalg.norm(thorax_end[:2] - thorax_start[:2])),
        "verdict": "PASS" if finite else "FAIL",
    }


def main() -> int:
    t0 = time.time()
    result = {"step": "Q1"}

    # --- Part (a): the FlyBody replay -------------------------------------
    ta = time.time()
    try:
        result["part_a_flybody_steps_replay"] = run_replay()
    except Exception:
        result["part_a_flybody_steps_replay"] = {
            "verdict": "FAIL",
            "error": traceback.format_exc(),
        }
    result["part_a_wall_clock_s"] = time.time() - ta

    # --- Part (b): muscle_imitation load-and-step --------------------------
    # The demo env module imports gymnasium at module level and raises
    # ImportError if it is absent. gymnasium is not part of the pinned body
    # env, so the env cannot even be constructed here. (The gate record gives
    # the other two reasons this sub-item cannot run, and the correction that
    # the demo's body is FlyMimic, not FlyBody.)
    result["part_b_muscle_imitation"] = {
        "executed": False,
        "gymnasium_installed": importlib.util.find_spec("gymnasium") is not None,
        "verdict": "NOT EXECUTED",
    }

    # §7.2: "Pass: both run without error". Part (b) did not run, so the step
    # fails on its stated criterion whatever part (a) did.
    a_pass = result["part_a_flybody_steps_replay"].get("verdict") == "PASS"
    result["verdict"] = "PASS" if (a_pass and result["part_b_muscle_imitation"]["executed"]) else "FAIL"
    result["wall_clock_s"] = time.time() - t0

    out = Path(__file__).resolve().parents[2] / "results" / "body_qualification" / "q1.json"
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"Q1(a) replay verdict: {result['part_a_flybody_steps_replay'].get('verdict')}")
    print(f"Q1(b) muscle_imitation: NOT EXECUTED "
          f"(gymnasium installed: {result['part_b_muscle_imitation']['gymnasium_installed']})")
    print(f"Q1 verdict: {result['verdict']} ({result['wall_clock_s']:.1f} s)")
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
