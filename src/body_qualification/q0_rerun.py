"""Q0 re-run (§7.1) + Pass 3 premise checks, 24 Nov 2026.

Re-verifies the five pinned FlyBody file hashes exactly as the first
execution did, then checks two premises the amended spec depends on:
(a) the compiled model's actuator ctrlrange equals the joints.yaml range
    for all five proboscis actuators (a mismatch stops the gate, §4.3);
(b) the compiled jnt_solref / jnt_solimp of the five proboscis joints,
    recorded (expected (0.001, 1) and (0.9, 0.95, 0.001, 0.5, 2)).
"""

import hashlib
import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

import flygym
from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import MODEL_DIR, PROBOSCIS, RANGES, build_sim  # noqa: E402
from q0_verify_artefact import PINNED as EXPECTED  # noqa: E402
from q0_verify_artefact import EXPERIMENTAL_LABEL as ENVIRONMENT_LABEL  # noqa: E402

HERE = Path(__file__).parent


def main():
    t0 = time.time()
    result = {"step": "Q0 (re-run)", "environment_label": ENVIRONMENT_LABEL}

    hashes = {}
    for name, expected in EXPECTED.items():
        digest = hashlib.sha256((MODEL_DIR / name).read_bytes()).hexdigest()
        hashes[name] = {"sha256": digest, "expected": expected,
                        "match": digest == expected}
    result["hashes"] = hashes
    result["hashes_all_match"] = all(h["match"] for h in hashes.values())

    fly, world, sim = build_sim(with_adhesion=False)
    m = sim.mj_model
    premise = {}
    all_equal = True
    for joint in PROBOSCIS:
        aid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_ACTUATOR,
                            f"flybody/{joint}-position")
        jid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_JOINT, f"flybody/{joint}")
        ctrlrange = [float(x) for x in m.actuator_ctrlrange[aid]]
        yaml_range = [float(x) for x in RANGES[joint]]
        equal = bool(np.allclose(ctrlrange, yaml_range, rtol=0, atol=0))
        all_equal = all_equal and equal
        premise[joint] = {
            "actuator_ctrlrange": ctrlrange,
            "joints_yaml_range": yaml_range,
            "ctrlrange_equals_yaml_range_exactly": equal,
            "ctrllimited": bool(m.actuator_ctrllimited[aid]),
            "jnt_range_compiled": [float(x) for x in m.jnt_range[jid]],
            "jnt_solref": [float(x) for x in m.jnt_solref[jid]],
            "jnt_solimp": [float(x) for x in m.jnt_solimp[jid]],
        }
    sim.close()
    result["premise_checks"] = premise
    result["ctrlrange_premise_holds"] = all_equal
    result["verdict"] = ("PASS" if result["hashes_all_match"] and all_equal
                         else "FAIL")
    result["wall_clock_s"] = time.time() - t0

    out = HERE.parents[1] / "results" / "body_qualification" / "q0_rerun.json"
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps({k: result[k] for k in
                      ("hashes_all_match", "ctrlrange_premise_holds",
                       "verdict", "wall_clock_s")}, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
