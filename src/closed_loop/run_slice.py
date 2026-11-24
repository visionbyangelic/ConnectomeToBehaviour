"""Thin FlyBody slice driver (SS6) -- body side of the bridge.

Runs in the BODY environment (FlyGym 2.1.1 / MuJoCo 3.16.0 / numpy
2.5.5) and spawns stub_worker.py as the brain-side process; the two
speak the JSON-lines contract in protocol.py (the Part 2b bridge's
form: one JSON object per line, replies in order, malformed replies
refused). One run:

  settle   -- the pinned FlyBody in the SS4.6 arena (pedestal + food,
              WITH the proboscis contact pairs of the gate's Q5 fix)
              settles per SS2.3 under zero command; t = 0 is the first
              chunk boundary after the settle criteria are met, and
              the feedback is armed only from t = 0.
  chunk k  -- 1. the driver sends the stub the SS4.5 taste-event state
                 at the end of body chunk k-1 (for k = 0: OFF) --
                 SS2.1's exactly-one-chunk feedback latency;
              2. the stub logs that state in its brain-side log and
                 returns the chunk's scripted SYNTHETIC pooled MN9
                 counts;
              3. the registered chain (chain.py: SS4.2 estimator +
                 SS4.3 mapping, the actual Part 5 code path) turns the
                 counts into proboscis ctrl values;
              4. the body steps 100 ms under those ctrls (zero-order
                 hold), the SS4.5 event is tracked per physics step
                 with the SS2.4 debounce, and labrum adhesion follows
                 SS4.3's chunk-level rule;
              5. per-chunk state is logged (rate, r_filt, e, targets,
                 ctrls, the five joint angles, E(t), contact state,
                 taste-event state).

Slice parameters, declared: r_lo = 5 Hz (SS4.3 FIXED); r_hi = 100 Hz
is a SLICE parameter, SYNTHETIC/provisional -- chosen so the scripted
profile's 100 Hz peak maps to e = 1 and the chain is exercised
through the contact regime. It is NOT Part 5's calibration: the
Part 5 r_hi is computed from designated calibration episodes under
SS4.3's rule and replaces this value at the freeze.

Before the episode, the driver audits chain.py against the gate's
own chain implementation (src/body_qualification/gate_common5.py) on the episode's
compiled params and settled rest: theta_ext and the ctrl vector must
agree to 1e-9 on an e grid, or the run does not start.

Usage:
  envs/body/bin/python run_slice.py --out runs/slice_run.json
"""

import argparse
import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]                       # repo/src/closed_loop -> repo root
WORKSPACE = HERE.parents[2]                  # connectome-work/
QUALGATE = HERE.parent / "body_qualification"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(QUALGATE))

import chain as chain_mod  # noqa: E402
import protocol  # noqa: E402

import mujoco as mj  # noqa: E402
from flygym.compose import ActuatorType  # noqa: E402

from gate_common import (CHUNK_STEPS, PROBOSCIS, build_sim,  # noqa: E402
                         dof_index, settle)
from gate_common3 import (FRONT_TARSUS_BODIES, compiled_params,  # noqa: E402
                          food_contact_forces, geom_ids_for_bodies,
                          labrum_tip_pos)
from gate_common5 import chain_ctrl_rev  # noqa: E402
from gate_common5 import theta_ext_from_params as gate_theta_ext  # noqa: E402
from q5_rerun5 import build_arena  # noqa: E402

N_CHUNKS = 60
CHUNK_MS = 100
SEED = 20261125
R_LO = 5.0                    # SS4.3 FIXED
R_HI_SLICE = 100.0            # SLICE parameter -- synthetic/provisional
SIGNS = {"c_head-c_rostrum-pitch": -1,
         "c_rostrum-c_haustellum-pitch": -1}   # gate record, execution #5
THETA_OFF = 0.01036           # gate output, frozen (SS4.4)
E_MAX_REF = 2.1746            # gate output (Q3, execution #5)
ONSET_RAD = 0.10              # SS4.4 event onset threshold, FIXED
ARENA_OFFSET_MM = 0.6         # SS4.6 final offset (gate Q5: unadjusted)
FREEZE_COMMIT = "e1f40462a68cfd2f87325ec0fc4e519bf667db09"
FREEZE_TAG = "part3-prereg-v2"


class StubLink:
    """The driver side of the slice bridge: owns the stub subprocess."""

    def __init__(self, seed, n_chunks, log_path, worker_log):
        self.proc = subprocess.Popen(
            [sys.executable, str(HERE / "stub_worker.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=worker_log, text=True, bufsize=1)
        profile = {"kind": "scripted_pooled_mn9_rate_profile",
                   "synthetic": True}
        self._send(protocol.make_start(seed, n_chunks, profile, log_path))
        reply = self._read()
        if reply.get("type") != "ready":
            raise RuntimeError(f"stub did not become ready: {reply!r}")
        self.ready_profile = reply.get("profile")

    def _send(self, message):
        self.proc.stdin.write(protocol.dumps_line(message))
        self.proc.stdin.flush()

    def _read(self):
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("stub worker closed its output "
                               "(see the worker log)")
        return protocol.loads_line(line)

    def chunk(self, chunk, taste_event):
        self._send(protocol.make_chunk(chunk, CHUNK_MS, taste_event))
        return protocol.validate_rate_reply(self._read(), chunk)

    def close(self):
        try:
            self._send(protocol.make_end())
            reply = self._read()
            if reply.get("type") != "bye":
                raise RuntimeError(f"stub did not say bye: {reply!r}")
        finally:
            self.proc.wait(timeout=60)


def git_ctb_state():
    """Criterion (v) evidence: src/brain_model/ status + HEAD, from git."""
    def git(*args):
        return subprocess.run(
            ["git", "-C", str(REPO), *args],
            capture_output=True, text=True, check=True).stdout.strip()
    return {"head": git("rev-parse", "HEAD"),
            "ctb_status_porcelain": git("status", "--porcelain",
                                        "--", "src/brain_model/")}


def first_run_at_least(values, threshold, start=0):
    """First k >= start with values[k] >= threshold and values[k+1] too."""
    for k in range(start, len(values) - 1):
        if values[k] >= threshold and values[k + 1] >= threshold:
            return k
    return None


def first_run_below(values, threshold, start):
    """First k >= start with values[k] < threshold and values[k+1] too."""
    for k in range(start, len(values) - 1):
        if values[k] < threshold and values[k + 1] < threshold:
            return k
    return None


def run_slice(out_path, stub_log_path):
    wall0 = time.time()
    result = {
        "deliverable": "thin FlyBody slice (PART4-SENSORY-SPECS SS6)",
        "synthetic_inputs": True,
        "config": {
            "n_chunks": N_CHUNKS, "chunk_ms": CHUNK_MS,
            "seed": SEED,
            "scripted_profile": ("SYNTHETIC pooled MN9 rate ramp: "
                                 "linear 0->100 Hz chunks 0-14, hold "
                                 "100 Hz chunks 15-34, linear 100->0 Hz "
                                 "chunks 35-49, 0 Hz chunks 50-59; "
                                 "seeded Poisson counts, split evenly "
                                 "over MN9 L/R"),
            "r_lo_hz": R_LO, "r_lo_status": "FIXED (SS4.3)",
            "r_hi_hz": R_HI_SLICE,
            "r_hi_status": ("SLICE parameter -- SYNTHETIC/provisional; "
                            "NOT Part 5 calibration (SS4.3 assigns r_hi "
                            "to designated calibration episodes; replaced "
                            "at the Part 5 freeze)"),
            "signs": SIGNS,
            "theta_off_rad": THETA_OFF,
            "E_max_reference_rad": E_MAX_REF,
            "arena": ("SS4.6 as revised: pedestal r 0.5 mm x h 0.28 mm "
                      "+ food disc r 0.5 mm x h 0.05 mm, top at ground "
                      "+ 0.33 mm; centre 0.6 mm in front of the labrum "
                      "tip's settled ground projection; proboscis "
                      "contact pairs included (gate Q5 fix)"),
            "declared_drives_SS2.2": (
                "brain side is a stub: the scripted pooled MN9 count "
                "profile (declared here, generated in full before the "
                "episode clock) and the SS4.5 taste-event feedback "
                "channel to the stub log. No Brian2, no populations."),
            "interpreters": {
                "driver": sys.executable,
                "stub_worker": sys.executable,
                "note": ("both processes run the body env's Python; "
                         "the stub involves no Brian2, so the brain "
                         "env is not used by this deliverable")},
            "ctb_freeze": {"commit": FREEZE_COMMIT, "tag": FREEZE_TAG},
        },
    }
    result["ctb_state_before"] = git_ctb_state()

    # --- pilot settle: arena placement from the tip projection -------
    fly, world, sim = build_sim(with_adhesion=True)
    idx0, order0 = dof_index(fly)
    st0 = settle(sim, fly, np.zeros(len(order0)))
    if not st0["settled"]:
        raise RuntimeError("pilot settle failed; cannot place the arena")
    tip = labrum_tip_pos(sim)
    head_id = mj.mj_name2id(sim.mj_model, mj.mjtObj.mjOBJ_BODY,
                            "flybody/c_head")
    head = sim.mj_data.xpos[head_id]
    forward = np.array([tip[0] - head[0], tip[1] - head[1]], dtype=float)
    forward /= np.linalg.norm(forward)
    tip_proj = np.array([tip[0], tip[1]], dtype=float)
    sim.close()
    centre = tip_proj + ARENA_OFFSET_MM * forward
    result["pilot"] = {
        "tip_settled_xyz_mm": [float(x) for x in tip],
        "arena_centre_xy_mm": [float(x) for x in centre],
        "offset_in_front_of_tip_projection_mm": ARENA_OFFSET_MM}

    # --- episode arena + settle (SS2.3), feedback armed from t = 0 ---
    fly, world, sim = build_arena(centre)
    m = sim.mj_model
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
    labrum_gids = {mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n) for n in
                   ("flybody/l_labrum_lower", "flybody/r_labrum_lower")}
    tarsus_gids = geom_ids_for_bodies(sim, FRONT_TARSUS_BODIES)
    adh_ids = [mj.mj_name2id(m, mj.mjtObj.mjOBJ_ACTUATOR,
                             f"flybody/{s}_labrum-adhesion")
               for s in ("l", "r")]

    def food_check():
        lf, tf = food_contact_forces(sim, food_gid, labrum_gids,
                                     tarsus_gids)
        return (lf + tf) > 0

    st = settle(sim, fly, np.zeros(len(order)), food_check=food_check)
    result["settle"] = {"settled": st["settled"],
                        "n_chunks": st["n_chunks"],
                        "food_contact_during_warmup":
                            st["food_contact_during_warmup"]}
    if not st["settled"] or st["food_contact_during_warmup"]:
        result["verdict"] = "FAIL"
        result["fail_reason"] = (
            "episode INVALID under SS2.3 (settle failed or food "
            "contact during warmup)")
        result["wall_clock_s"] = time.time() - wall0
        sim.close()
        out_path.write_text(json.dumps(result, indent=2))
        print(json.dumps(result["fail_reason"]), flush=True)
        return result
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    result["theta_rest_rad"] = rest

    # --- the registered chain, and the audit against the gate's ------
    fchain = chain_mod.FeedingChain(params, SIGNS, r_lo=R_LO,
                                    r_hi=R_HI_SLICE)
    fchain.set_rest(rest)
    gate_ext = gate_theta_ext(params, SIGNS)
    audit = {"theta_ext_chain": fchain.theta_ext,
             "theta_ext_gate": gate_ext,
             "max_ctrl_diff": 0.0}
    base = np.zeros(len(order))
    for e in [i / 20 for i in range(21)]:
        ctrls, _ = fchain.ctrls_for_e(e)
        gate_ctrl = chain_ctrl_rev(base, idx, params, e, rest, gate_ext)
        for j in PROBOSCIS:
            audit["max_ctrl_diff"] = max(
                audit["max_ctrl_diff"],
                abs(ctrls[j] - float(gate_ctrl[idx[j]])))
    audit["theta_ext_max_diff"] = max(
        abs(fchain.theta_ext[j] - gate_ext[j]) for j in gate_ext)
    audit["pass"] = bool(audit["max_ctrl_diff"] <= 1e-9
                         and audit["theta_ext_max_diff"] <= 1e-9)
    result["chain_audit_vs_gate_common5"] = audit
    if not audit["pass"]:
        result["verdict"] = "FAIL"
        result["fail_reason"] = ("chain.py disagrees with the gate's "
                                 "chain implementation; run stopped "
                                 "before the episode")
        result["wall_clock_s"] = time.time() - wall0
        sim.close()
        out_path.write_text(json.dumps(result, indent=2))
        print(json.dumps(result["fail_reason"]), flush=True)
        return result

    # --- the bridge episode ------------------------------------------
    worker_log = open(out_path.with_suffix(".worker.log"), "w")
    link = StubLink(SEED, N_CHUNKS, stub_log_path, worker_log)
    result["stub_ready_profile"] = link.ready_profile

    event_on = False            # SS4.5 state at the end of the last chunk
    on_streak = 0
    off_streak = 0
    adhesion = False            # applies during the current chunk
    adhesion_off_chunks = 0
    records = []
    worker_error = None
    try:
        for k in range(N_CHUNKS):
            reply = link.chunk(k, event_on)
            counts = reply["counts"]
            out = fchain.update(counts["mn9_left"], counts["mn9_right"])
            ctrl = np.zeros(len(order))
            for j in PROBOSCIS:
                ctrl[idx[j]] = out["ctrls"][j]
            sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
            for aid in adh_ids:
                sim.mj_data.ctrl[aid] = 1.0 if adhesion else 0.0
            max_labrum_force = 0.0
            max_tarsus_force = 0.0
            forces_finite = True
            for _ in range(CHUNK_STEPS):
                sim.step()
                lf, tf = food_contact_forces(sim, food_gid, labrum_gids,
                                             tarsus_gids)
                forces_finite = (forces_finite and math.isfinite(lf)
                                 and math.isfinite(tf))
                max_labrum_force = max(max_labrum_force, lf)
                max_tarsus_force = max(max_tarsus_force, tf)
                if (lf + tf) > 0:
                    on_streak += 1
                    off_streak = 0
                    if on_streak >= 10 and not event_on:
                        event_on = True
                else:
                    off_streak += 1
                    on_streak = 0
                    if off_streak >= 50 and event_on:
                        event_on = False
            angles_all = sim.get_joint_angles(fly.name)
            angles = {j: float(angles_all[idx[j]]) for j in PROBOSCIS}
            finite = bool(forces_finite
                          and np.all(np.isfinite(sim.mj_data.qpos))
                          and np.all(np.isfinite(sim.mj_data.qvel))
                          and all(math.isfinite(v) for v in angles.values()))
            records.append({
                "chunk": k,
                "scripted_rate_hz": reply["scripted_rate_hz"],
                "counts": counts,
                "r_window_hz": out["r_window_hz"],
                "r_filt_hz": out["r_filt_hz"],
                "e": out["e"],
                "targets_rad": out["targets"],
                "ctrls_rad": out["ctrls"],
                "angles_rad": angles,
                "E_rad": fchain.extension_E(angles),
                "max_labrum_food_force_N": max_labrum_force,
                "max_front_tarsus_food_force_N": max_tarsus_force,
                "taste_event_at_chunk_end": bool(event_on),
                "adhesion_during_chunk": bool(adhesion),
                "finite": finite,
            })
            # SS4.3 adhesion rule, decided at the chunk boundary:
            # engages in the first chunk after the event turns ON;
            # releases after the event has been OFF for 2 chunks.
            if event_on:
                adhesion_off_chunks = 0
                adhesion = True
            else:
                adhesion_off_chunks += 1
                if adhesion and adhesion_off_chunks >= 2:
                    adhesion = False
    except Exception as exc:
        worker_error = f"{type(exc).__name__}: {exc}"
    finally:
        try:
            link.close()
        except Exception as exc:
            if worker_error is None:
                worker_error = f"bridge close: {type(exc).__name__}: {exc}"
        worker_log.close()
        sim.close()
    result["worker_error"] = worker_error
    result["chunks"] = records

    # --- the brain-side stub log, read back ---------------------------
    stub_lines = [json.loads(line)
                  for line in Path(stub_log_path).read_text().splitlines()
                  if line.strip()]
    stub_chunks = {line["chunk"]: line for line in stub_lines
                   if line.get("type") == "chunk"}
    stub_taste = [stub_chunks[k]["taste_event"] for k in range(N_CHUNKS)
                  if k in stub_chunks]
    result["stub_log"] = {"path": str(stub_log_path),
                          "chunks_logged": len(stub_chunks)}

    # --- verdicts ------------------------------------------------------
    e_series = [r["E_rad"] for r in records]
    body_event = [r["taste_event_at_chunk_end"] for r in records]
    onset_chunk = first_run_at_least(e_series, ONSET_RAD)
    offset_chunk = (first_run_below(e_series, THETA_OFF, onset_chunk + 1)
                    if onset_chunk is not None else None)
    first_contact_chunk = next(
        (k for k, v in enumerate(body_event) if v), None)
    first_clear_chunk = None
    if first_contact_chunk is not None:
        first_clear_chunk = next(
            (k for k in range(first_contact_chunk + 1, N_CHUNKS)
             if not body_event[k]), None)
    expected_stub = [False] + body_event[:-1]
    checks = {
        "i_60_of_60_chunks_no_error_all_finite": bool(
            len(records) == N_CHUNKS and worker_error is None
            and all(r["finite"] for r in records)),
        "ii_E_rises_and_falls_onset_offset_SS4.4": bool(
            onset_chunk is not None and offset_chunk is not None
            and max(e_series) >= ONSET_RAD
            and e_series[-1] < ONSET_RAD),
        "iii_contact_event_on_during_high_rate_phase": bool(
            first_contact_chunk is not None
            and records[first_contact_chunk]["scripted_rate_hz"] >= 50.0),
        "iv_taste_event_in_stub_log_exactly_one_chunk_after": bool(
            len(stub_taste) == N_CHUNKS and stub_taste == expected_stub
            and first_contact_chunk is not None
            and first_clear_chunk is not None),
        "v_ctb_frozen_code_untouched": bool(
            result["ctb_state_before"]["ctb_status_porcelain"] == ""),
    }
    result["derived"] = {
        "peak_E_rad": max(e_series) if e_series else None,
        "onset_chunk_SS4.4": onset_chunk,
        "offset_chunk_SS4.4": offset_chunk,
        "first_contact_chunk": first_contact_chunk,
        "first_clear_chunk": first_clear_chunk,
        "stub_first_taste_on_chunk": next(
            (k for k, v in enumerate(stub_taste) if v), None),
        "E_final_chunk_rad": e_series[-1] if e_series else None,
        "max_labrum_food_force_N": max(
            (r["max_labrum_food_force_N"] for r in records), default=None),
    }
    result["ctb_state_after"] = git_ctb_state()
    checks["v_ctb_frozen_code_untouched"] = bool(
        checks["v_ctb_frozen_code_untouched"]
        and result["ctb_state_after"]["ctb_status_porcelain"] == ""
        and result["ctb_state_after"]["head"] == FREEZE_COMMIT
        and result["ctb_state_before"]["head"] == FREEZE_COMMIT)
    result["checks"] = checks
    result["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    result["wall_clock_s"] = time.time() - wall0
    out_path.write_text(json.dumps(result, indent=2))
    print("checks:", json.dumps(checks), flush=True)
    print("derived:", json.dumps(result["derived"]), flush=True)
    print("slice verdict:", result["verdict"],
          "wall", round(result["wall_clock_s"], 1), flush=True)
    print("wrote", out_path, flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--stub-log", type=Path, default=None)
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    stub_log = args.stub_log or args.out.with_suffix(".stub_log.jsonl")
    run_slice(args.out, stub_log)


if __name__ == "__main__":
    main()
