"""Q0, third execution (SS7.1 as amended by Pass 5), 24 Nov 2026.

Re-verifies the five pinned FlyBody file hashes, then the premise checks:
(a) compiled actuator ctrlrange == joints.yaml range for the five
    proboscis actuators (a mismatch stops the gate, SS4.3);
(b) compiled jnt_solref / jnt_solimp of the five proboscis joints;
(c) per Pass 5, per proboscis joint (labelled): qpos_spring, qpos0,
    jnt_stiffness, actuator gainprm[0] and -biasprm[1], asserting
    gainprm[0] == -biasprm[1] (the SS4.3 map assumes a pure position
    servo). Expected: qpos_spring = qpos0 = 0.0, stiffness 3.0, gains
    10/10 (head group) and 1/1 (labrum group). A deviation stops the gate
    as a premise failure;
(d) the exact construction call and the neutral pose it passes to the
    FlyBody construction, recorded (the spring references follow the
    neutral pose, Pass 5).
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import MODEL_DIR, PROBOSCIS, build_sim  # noqa: E402
from gate_common3 import RESULTS, compiled_params  # noqa: E402
from q0_verify_artefact import PINNED as EXPECTED  # noqa: E402
from q0_verify_artefact import EXPERIMENTAL_LABEL as ENVIRONMENT_LABEL  # noqa: E402

CONSTRUCTION_CALL = (
    "fly = q1_upstream_integrity.build_flybody()  # Part 1b Demo C construction: "
    "FlyBody(name='flybody'); skeleton = FlyBodySkeleton(axis_order=YAW_ROLL_PITCH, "
    "joint_preset=ALL_BIOLOGICAL); neutral = KinematicPosePreset.FLYBODY_NEUTRAL"
    ".get_pose_by_axis_order(YAW_ROLL_PITCH); fly.add_joints(skeleton, "
    "neutral_pose=neutral); fly.add_actuators(skeleton.get_actuated_dofs_from_preset"
    "(ALL), ActuatorType.POSITION, neutral_input=neutral); "
    "fly.add_leg_adhesion() for the Q2-Q6 builds (shipped defaults: leg gain 0.985, "
    "labrum gain 1.0, add_labrum=True); world = FlatGroundWorld(); "
    "world.add_fly(fly, (0, 0, 1.0), Rotation3D('quat', (1, 0, 0, 0))); "
    "sim = Simulation(world); sim.reset()"
)


def main():
    t0 = time.time()
    result = {"step": "Q0 (rerun3)", "environment_label": ENVIRONMENT_LABEL}

    hashes = {}
    for name, expected in EXPECTED.items():
        digest = hashlib.sha256((MODEL_DIR / name).read_bytes()).hexdigest()
        hashes[name] = {"sha256": digest, "expected": expected,
                        "match": digest == expected}
    result["hashes"] = hashes
    result["hashes_all_match"] = all(h["match"] for h in hashes.values())

    fly, world, sim = build_sim(with_adhesion=True)
    params = compiled_params(sim)

    premise = {}
    ctrlrange_ok = True
    servo_ok = True
    expected_ok = True
    for joint in PROBOSCIS:
        p = params[joint]
        equal = bool(np.allclose(p["actuator_ctrlrange"], p["yaml_range"],
                                 rtol=0, atol=0))
        ctrlrange_ok = ctrlrange_ok and equal
        pure_servo = bool(p["kp_gainprm0"] == p["neg_biasprm1"])
        servo_ok = servo_ok and pure_servo
        exp_gain = 10.0 if "labrum" not in joint else 1.0
        exp_ok = bool(p["qpos_spring"] == 0.0 and p["qpos0"] == 0.0
                      and p["jnt_stiffness"] == 3.0
                      and p["kp_gainprm0"] == exp_gain)
        expected_ok = expected_ok and exp_ok
        premise[joint] = {**p,
                          "ctrlrange_equals_yaml_range_exactly": equal,
                          "pure_position_servo_gainprm0_eq_neg_biasprm1":
                              pure_servo,
                          "expected_compiled_values_hold": exp_ok}
    result["premise_checks"] = premise
    result["ctrlrange_premise_holds"] = ctrlrange_ok
    result["pure_position_servo_holds"] = servo_ok
    result["expected_compiled_values_hold"] = expected_ok

    # (d) construction call + the neutral pose the construction passes.
    from flygym.compose import ActuatorType
    neutral_by_dof = fly.jointdof_to_neutralaction_by_type[ActuatorType.POSITION]
    order = fly.get_actuated_jointdofs_order(ActuatorType.POSITION)
    name_by_dof = {d: d.name for d in order}
    result["construction"] = {
        "call": CONSTRUCTION_CALL,
        "neutral_pose_source": ("KinematicPosePreset.FLYBODY_NEUTRAL"
                                ".get_pose_by_axis_order(FlyBodyAxisOrder"
                                ".YAW_ROLL_PITCH)"),
        "neutral_input_proboscis": {
            j: float(neutral_by_dof[d]) for d in order
            if (j := name_by_dof[d]) in PROBOSCIS},
        "note": ("Per Amendment Pass 5 the compiled spring references follow "
                 "the neutral pose the construction receives; a build with a "
                 "different neutral pose changes the SS4.3 map and must "
                 "re-read it under the Pass 5 rule."),
    }
    sim.close()

    ok = (result["hashes_all_match"] and ctrlrange_ok and servo_ok
          and expected_ok)
    result["verdict"] = "PASS" if ok else "FAIL"
    if not ok:
        result["fail_reason"] = (
            "premise failure at Q0: hashes_match=%s ctrlrange=%s pure_servo=%s "
            "expected_values=%s" % (result["hashes_all_match"], ctrlrange_ok,
                                    servo_ok, expected_ok))
    result["wall_clock_s"] = time.time() - t0
    out = RESULTS / "q0_rerun3.json"
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps({k: result[k] for k in
                      ("hashes_all_match", "ctrlrange_premise_holds",
                       "pure_position_servo_holds",
                       "expected_compiled_values_hold", "verdict",
                       "wall_clock_s")}, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
