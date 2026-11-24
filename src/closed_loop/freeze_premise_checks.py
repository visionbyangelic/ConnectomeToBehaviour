"""Part 5 freeze premise checks P1, P2 and P4 (preregistration section 3).

P3 is satisfied by its record (docs/resting_acceptance_test.md, PASS in
both configurations, 24 Nov 2026; no detector, threshold or arena
element has changed since). P5 was discharged by the executed toggle
probe (docs/closed_loop_preregistration.md section 3). P6 has its own
driver (two loop runs plus spike-table replays). This script executes
the remaining three and writes one JSON record:

P1  artefact identity: the five FlyBody files hash to the pinned
    values, and the compiled premise values hold on the gate's build
    (qpos_spring = qpos0 = 0, jnt_stiffness 3.0, gainprm[0] =
    -biasprm[1] with the pinned gains, ctrlranges equal to the
    joints.yaml ranges, solref (0.001, 1), solimp (0.9, 0.95, 0.001,
    0.5, 2)) for every proboscis and neck joint.
P2  contact-pair coverage by geom name on the Part 5 arena build
    (body_side.FeedingBody): each of the six proboscis geoms is paired
    with both arena geoms (food disc, pedestal); plus the
    contact-visibility test on that build: at rest (e = 0) the
    labrum-food force is exactly 0; under the Q5 ramp-and-hold the
    labrum registers force > 0 and the section 4.5 event turns ON.
P4  chain identity: chain.py against the gate's independently written
    chain (gate_common5) on the arena build's compiled parameters:
    identical theta_ext and ctrl agreement to <= 1e-9 over an e grid;
    plus chain.py's nine unit tests (brain env pytest).

Usage (body env):
    python freeze_premise_checks.py --out RECORD.json
Exit code 0 only if P1, P2 and P4 all pass.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "src" / "body_qualification"))
sys.path.insert(0, str(HERE))

import mujoco as mj  # noqa: E402
from gate_common import MODEL_DIR, NECK, PROBOSCIS, build_sim  # noqa: E402
from gate_common3 import compiled_params  # noqa: E402
from gate_common5 import chain_ctrl_rev  # noqa: E402
from q0_verify_artefact import PINNED  # noqa: E402
import chain as chain_mod  # noqa: E402
from body_side import FeedingBody  # noqa: E402
from run_loop5 import SIGNS  # noqa: E402

BRAIN_PYTHON = REPO.parent / "envs" / "brain" / "bin" / "python"
SOLREF = (0.001, 1.0)
SOLIMP = (0.9, 0.95, 0.001, 0.5, 2.0)


def check_p1():
    files = {}
    all_match = True
    for name, pinned in PINNED.items():
        digest = hashlib.sha256((MODEL_DIR / name).read_bytes()).hexdigest()
        files[name] = {"pinned": pinned, "measured": digest,
                       "match": digest == pinned}
        all_match &= digest == pinned
    fly, world, sim = build_sim(with_adhesion=True)
    params = compiled_params(sim)
    joints = {}
    values_ok = True
    for joint in PROBOSCIS + NECK:
        p = params[joint]
        exp_gain = 1.0 if "labrum" in joint else 10.0
        ok = bool(p["qpos_spring"] == 0.0 and p["qpos0"] == 0.0
                  and p["jnt_stiffness"] == 3.0
                  and p["kp_gainprm0"] == -p["biasprm1"]
                  and p["kp_gainprm0"] == exp_gain
                  and p["actuator_ctrlrange"] == p["yaml_range"]
                  and tuple(p["jnt_solref"]) == SOLREF
                  and tuple(p["jnt_solimp"]) == SOLIMP)
        values_ok &= ok
        joints[joint] = {**p, "premise_values_hold": ok}
    sim.close()
    return {"pass": bool(all_match and values_ok),
            "files": files, "hashes_all_match": bool(all_match),
            "compiled_values_all_hold": bool(values_ok),
            "joints": joints}


def check_p2():
    body = FeedingBody()
    sim = body.sim
    m = sim.mj_model
    def gname(gid):
        return mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, gid) or ""
    pairs = set()
    for i in range(m.npair):
        pairs.add((gname(m.pair_geom1[i]), gname(m.pair_geom2[i])))
    proboscis = sorted({g for pair in pairs for g in pair
                        if any(k in g for k in ("labrum", "rostrum", "haustellum"))})
    coverage = {}
    coverage_ok = len(proboscis) == 6
    for g in proboscis:
        with_food = (g, "food") in pairs or ("food", g) in pairs
        with_ped = (g, "pedestal") in pairs or ("pedestal", g) in pairs
        coverage[g] = {"paired_with_food": bool(with_food),
                       "paired_with_pedestal": bool(with_ped)}
        coverage_ok &= with_food and with_ped
    # configuration hash over the compiled pair list and geom list
    geom_names = sorted(gname(i) for i in range(m.ngeom))
    config = json.dumps({"pairs": sorted(pairs), "geoms": geom_names},
                        sort_keys=True)
    config_hash = hashlib.sha256(config.encode()).hexdigest()
    xml_hash = None
    try:
        xml = body.world.mjcf_root.to_xml_string()
        xml_hash = hashlib.sha256(xml.encode()).hexdigest()
    except Exception as exc:  # XML export is a bonus; the config hash stands
        xml_hash = f"unavailable: {exc!r}"
    # contact-visibility test on this build (Q5 protocol)
    chain = chain_mod.FeedingChain(body.params, SIGNS, r_hi=155.0)
    chain.set_rest(body.theta_rest)
    chunks = []
    def run(e, phase):
        ctrls, _targets = chain.ctrls_for_e(e)
        rec = body.step_chunk(ctrls)
        chunks.append({"phase": phase, "e": e,
                       "max_labrum_food_force_N": rec["max_labrum_food_force_N"],
                       "taste_event_at_chunk_end": rec["taste_event_at_chunk_end"]})
        return rec
    for _ in range(2):
        run(0.0, "rest")
    for e in (0.2, 0.4, 0.6, 0.8, 1.0):
        run(e, "ramp")
    for _ in range(10):
        run(1.0, "hold")
    rest_ok = all(c["max_labrum_food_force_N"] == 0.0
                  and not c["taste_event_at_chunk_end"]
                  for c in chunks if c["phase"] == "rest")
    hold = [c for c in chunks if c["phase"] in ("ramp", "hold")]
    force_seen = any(c["max_labrum_food_force_N"] > 0.0 for c in hold)
    event_seen = any(c["taste_event_at_chunk_end"] for c in hold)
    body.close()
    return {"pass": bool(coverage_ok and rest_ok and force_seen and event_seen),
            "proboscis_geoms": proboscis, "coverage_by_geom_name": coverage,
            "n_pairs_total": len(pairs),
            "configuration_sha256": config_hash, "arena_xml_sha256": xml_hash,
            "arena_centre_xy_mm": body.pilot["arena_centre_xy_mm"],
            "visibility": {"rest_force_zero_and_event_off": bool(rest_ok),
                           "force_seen_under_ramp_hold": bool(force_seen),
                           "event_on_under_ramp_hold": bool(event_seen),
                           "chunks": chunks}}


def check_p4():
    # mirrors run_slice.py's audit exactly: gate_common5's own
    # theta_ext_from_params and chain_ctrl_rev against chain.py
    from gate_common5 import theta_ext_from_params as gate_theta_ext
    body = FeedingBody()
    params, rest = body.params, body.theta_rest
    gate_ext = gate_theta_ext(params, SIGNS)
    chain = chain_mod.FeedingChain(params, SIGNS, r_hi=155.0)
    chain.set_rest(rest)
    theta_diff = max(abs(chain.theta_ext[j] - gate_ext[j]) for j in gate_ext)
    base_ctrl = np.zeros(len(body.order))
    max_ctrl_diff = 0.0
    for e in np.linspace(0.0, 1.0, 21):
        c_chain, _ = chain.ctrls_for_e(float(e))
        gate_vec = chain_ctrl_rev(base_ctrl, body.idx, params, float(e),
                                  rest, gate_ext)
        for j in PROBOSCIS:
            max_ctrl_diff = max(max_ctrl_diff,
                                abs(c_chain[j] - gate_vec[body.idx[j]]))
    body.close()
    proc = subprocess.run(
        [str(BRAIN_PYTHON), "-m", "pytest", "-q",
         str(HERE / "tests" / "test_chain.py")],
        capture_output=True, text=True)
    tests_ok = proc.returncode == 0
    return {"pass": bool(theta_diff == 0.0 and max_ctrl_diff <= 1e-9 and tests_ok),
            "theta_ext_max_abs_diff": float(theta_diff),
            "ctrl_max_abs_diff_over_e_grid": float(max_ctrl_diff),
            "test_chain_py": {"returncode": proc.returncode,
                              "tail": (proc.stdout + proc.stderr).strip().splitlines()[-3:]}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    record = {"what": "Part 5 freeze premise checks P1, P2, P4 "
                      "(preregistration section 3)"}
    record["P1"] = check_p1()
    print("P1:", record["P1"]["pass"], flush=True)
    record["P2"] = check_p2()
    print("P2:", record["P2"]["pass"], flush=True)
    record["P4"] = check_p4()
    print("P4:", record["P4"]["pass"], flush=True)
    record["all_pass"] = all(record[k]["pass"] for k in ("P1", "P2", "P4"))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2) + "\n")
    print("record:", out, "sha256:",
          hashlib.sha256(out.read_bytes()).hexdigest())
    return 0 if record["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
