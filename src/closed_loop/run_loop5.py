"""Part 5 closed-loop driver: brain -> chain -> body -> taste -> brain.

Runs in the BODY environment (FlyGym 2.1.1 / MuJoCo 3.16.0 / numpy
2.5.5) and spawns brain_worker.py in the brain environment; the two
speak the JSON-lines contract in loop_protocol.py. One episode
(PART4-SENSORY-SPECS SS2.1 cadence, SS4.1 registered chain):

  settle   -- the pinned FlyBody in the SS4.6 arena settles per SS2.3
              under zero command (body_side.FeedingBody; no brain
              input of any kind, per SS2.3); t = 0 is the first chunk
              boundary after the settle criteria are met. An episode
              whose settle fails, or with food contact during warmup,
              is INVALID: it is recorded INVALID in the manifest and
              no chunks run.
  chunk k  -- 1. BRAIN: the worker receives the SS4.5 taste-event
                 state at the end of body chunk k-1 (OFF for k = 0),
                 applies the scenario's gating (loop_protocol), runs
                 100 ms of the frozen brain, and returns the readout
                 spike counts plus the per-drive applied-state record;
              2. CHAIN: the registered chain (chain.py: SS4.2 estimator
                 + SS4.3 mapping) turns the chunk's MN9 L/R counts into
                 the five proboscis ctrls;
              3. BODY: the body steps 100 ms under those ctrls
                 (zero-order hold) and the SS4.5 event is tracked per
                 physics step (SS2.4 debounce), its end-of-chunk state
                 gating brain chunk k+1 -- exactly one chunk of
                 feedback latency (SS2.1).

Run records (SS6.1(3)): every run writes a directory containing
  manifest.json  -- the full scenario as validated (the SS2.2 declared
                    drives), the frozen brain-model commit + tag and the git
                    status (a dirty tree says so here, it is not tidied
                    away), the loader-verified data hashes, the seeds,
                    the configuration (r_lo; r_hi WITH its provenance
                    label; the gate-recorded signs, theta_off and
                    E_max), the settle record and the episode's
                    validity, and pointers to the per-chunk logs;
  brain_log.jsonl -- one line per chunk: the worker's counts reply,
                    including the applied state of every drive with
                    both gates shown separately (SS4.5 two-gates rule);
  body_log.jsonl  -- one line per chunk: ctrls, targets, r_filt, e,
                    the five proboscis + three neck angles, E (SS4.4),
                    the food-contact forces, the taste-event state,
                    adhesion, thorax position, finiteness;
  summary.json   -- derived quantities and, for the built-in smoke
                    scenarios, their pass/fail checks.

Usage:
  envs/body/bin/python run_loop5.py --scenario S1 --out runs/s1_smoke
  envs/body/bin/python run_loop5.py --scenario-file scen.json --out DIR
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]                       # repo/src/closed_loop -> repo
WORKSPACE = REPO.parent                      # connectome-work/
BRAIN_PYTHON = WORKSPACE / "envs" / "brain" / "bin" / "python"
WORKER = HERE / "brain_worker.py"
sys.path.insert(0, str(HERE))

import chain as chain_mod  # noqa: E402
import loop_protocol as protocol  # noqa: E402
from body_side import ARENA_OFFSET_MM, FeedingBody  # noqa: E402

CHUNK_MS = 100
R_LO = 5.0                    # SS4.3 FIXED
R_HI_SMOKE = 155.0
R_HI_SMOKE_LABEL = ("PROVISIONAL (SS7.6 Q6 value: Part 3's measured "
                    "pooled MN9 response, 92.57 + 62.40 Hz; replaced "
                    "by the calibrated r_hi at the Part 5 freeze)")
SIGNS = {"c_head-c_rostrum-pitch": -1,
         "c_rostrum-c_haustellum-pitch": -1}   # gate record, execution #5
THETA_OFF = 0.01036           # gate output, frozen (SS4.4)
E_MAX_REF = 2.1746            # gate output (Q3, execution #5)
ONSET_RAD = 0.10              # SS4.4 event onset threshold, FIXED
FREEZE_COMMIT = "e1f40462a68cfd2f87325ec0fc4e519bf667db09"
FREEZE_TAG = "part3-prereg-v2"

SCENARIOS = {
    "S1": {
        "name": "S1_smoke_event_gated_sugar_with_ignition",
        "kind": "smoke",
        "n_chunks": 40,
        "seed": 5101,
        "drives": [{
            "name": "sugar", "populations": ["sugar_grn_right"],
            "rate_hz": 200.0, "mode": "event_or_window",
            "window": [[0, 9]],
        }],
        "purpose": ("SMOKE, not science: the closed loop must ignite "
                    "under the scripted window (chunks 0-9), reach "
                    "labrum-food contact, and the SS4.5 event must "
                    "then take over the gating -- after chunk 9 the "
                    "drive may be applied only via the event gate, "
                    "with both gates logged separately."),
    },
    "S2": {
        "name": "S2_smoke_no_drive_control",
        "kind": "smoke",
        "n_chunks": 30,
        "seed": 5102,
        "drives": [{
            "name": "sugar", "populations": ["sugar_grn_right"],
            "rate_hz": 200.0, "mode": "off", "window": [],
        }],
        "purpose": ("SMOKE, not science: the sugar drive is declared "
                    "(SS2.2) but never applied; the record must show "
                    "no contact, no taste event, E at rest, and a "
                    "silent MN9."),
    },
}


class BrainLink:
    """The driver side of the loop protocol: owns the worker process."""

    def __init__(self, scenario, worker_log):
        self.proc = subprocess.Popen(
            [str(BRAIN_PYTHON), str(WORKER)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=worker_log, text=True, bufsize=1)
        self.scenario = scenario
        self._send(protocol.make_start(scenario))
        self.ready = None

    def _send(self, message):
        self.proc.stdin.write(protocol.dumps_line(message))
        self.proc.stdin.flush()

    def _read(self):
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("brain worker closed its output "
                               "(see the worker log)")
        return protocol.loads_line(line)

    def read_ready(self):
        reply = self._read()
        if reply.get("type") != "ready":
            raise RuntimeError(f"worker did not become ready: {reply!r}")
        self.ready = reply
        return reply

    def chunk(self, chunk, taste_event):
        self._send(protocol.make_chunk(chunk, CHUNK_MS, taste_event))
        return protocol.validate_counts_reply(
            self._read(), chunk,
            [d["name"] for d in self.scenario["drives"]],
            self.scenario["readouts"])

    def close(self):
        try:
            self._send(protocol.make_end())
            reply = self._read()
            if reply.get("type") != "bye":
                raise RuntimeError(f"worker did not say bye: {reply!r}")
        finally:
            self.proc.wait(timeout=120)


def git_state():
    """SS6.1(3) evidence: HEAD, tags at HEAD, working-tree status."""
    def git(*args):
        return subprocess.run(["git", "-C", str(REPO), *args],
                              capture_output=True, text=True,
                              check=True).stdout.strip()
    porcelain = git("status", "--porcelain")
    return {"head": git("rev-parse", "HEAD"),
            "tags_at_head": git("tag", "--points-at", "HEAD").split(),
            "status_porcelain": porcelain,
            "ctb_status_porcelain": git("status", "--porcelain", "--",
                                        "src/brain_model/"),
            "working_tree_dirty": bool(porcelain)}


def first_run_at_least(values, threshold, start=0):
    for k in range(start, len(values) - 1):
        if values[k] >= threshold and values[k + 1] >= threshold:
            return k
    return None


def first_run_below(values, threshold, start):
    for k in range(start, len(values) - 1):
        if values[k] < threshold and values[k + 1] < threshold:
            return k
    return None


def run_episode(scenario, out_dir, r_hi, r_hi_label):
    wall0 = time.time()
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_kind = scenario.get("kind", "episode")
    raw_purpose = scenario.get("purpose")
    scenario = protocol.validate_scenario(scenario)
    manifest = {
        "part": "5",
        "run_kind": raw_kind,
        "purpose": raw_purpose,
        "scenario": scenario,
        "ctb_freeze": {"expected_commit": FREEZE_COMMIT,
                       "expected_tag": FREEZE_TAG},
        "git": git_state(),
        "configuration": {
            "chunk_ms": CHUNK_MS,
            "r_lo_hz": R_LO, "r_lo_status": "FIXED (SS4.3)",
            "r_hi_hz": r_hi, "r_hi_provenance": r_hi_label,
            "signs": SIGNS, "theta_off_rad": THETA_OFF,
            "E_max_reference_rad": E_MAX_REF,
            "arena": ("SS4.6 as revised: pedestal r 0.5 mm x h 0.28 mm "
                      "+ food disc r 0.5 mm x h 0.05 mm, top at ground "
                      "+ 0.33 mm; centre "
                      f"{ARENA_OFFSET_MM} mm in front of the labrum "
                      "tip's settled ground projection; proboscis "
                      "contact pairs included (gate Q5 fix)"),
            "body_seed": None,
            "body_seed_note": ("MuJoCo stepping is deterministic; the "
                               "body has no stochastic element and no "
                               "seed. The brain seed is the "
                               "scenario's."),
            "interpreters": {"driver": sys.executable,
                             "brain_worker": str(BRAIN_PYTHON)},
        },
        "declared_drives_SS2.2": scenario["drives"],
        "envelope_labels": {d["name"]: d["envelope"]
                            for d in scenario["drives"]},
        "logs": {"brain": "brain_log.jsonl", "body": "body_log.jsonl"},
    }

    worker_log = open(out_dir / "brain_worker.log", "w")
    link = BrainLink(scenario, worker_log)
    brain_records = []
    body_records = []
    summary = {}
    try:
        # The worker builds while the body settles (wall-clock only;
        # the settle uses no brain input, SS2.3).
        body = FeedingBody()
        manifest["pilot"] = body.pilot
        manifest["settle"] = body.settle_record
        manifest["theta_rest_rad"] = body.theta_rest
        ready = link.read_ready()
        manifest["worker_ready"] = {
            "populations": ready["populations"],
            "data_hashes": ready["data_hashes"],
            "declared_drives": ready["declared_drives"]}
        manifest["data_hashes"] = ready["data_hashes"]
        if not body.valid:
            manifest["episode_validity"] = "INVALID"
            manifest["invalid_reason"] = (
                "settle failed" if not body.settle_record["settled"]
                else "food contact during warmup (SS2.3)")
            summary = {"completed_chunks": 0,
                       "episode_validity": "INVALID"}
        else:
            manifest["episode_validity"] = "VALID"
            fchain = chain_mod.FeedingChain(body.params, SIGNS,
                                            r_lo=R_LO, r_hi=r_hi)
            fchain.set_rest(body.theta_rest)
            event_state = False     # taste event at end of chunk k-1
            for k in range(scenario["n_chunks"]):
                reply = link.chunk(k, event_state)
                brain_records.append(reply)
                counts = reply["counts"]
                out = fchain.update(counts["mn9_left"],
                                    counts["mn9_right"])
                rec = body.step_chunk(out["ctrls"])
                angles = {j: rec["angles_rad"][j]
                          for j in chain_mod.PROBOSCIS}
                rec["E_rad"] = fchain.extension_E(angles)
                rec["r_window_hz"] = out["r_window_hz"]
                rec["r_filt_hz"] = out["r_filt_hz"]
                rec["e"] = out["e"]
                rec["targets_rad"] = out["targets"]
                rec["ctrls_rad"] = out["ctrls"]
                rec["taste_event_sent_to_brain"] = event_state
                body_records.append(rec)
                event_state = rec["taste_event_at_chunk_end"]
            summary = summarise(scenario, brain_records, body_records)
        body.close()
    finally:
        try:
            link.close()
        except Exception:
            link.proc.kill()
        worker_log.close()
    manifest["wall_clock_s"] = time.time() - wall0
    summary["wall_clock_s"] = manifest["wall_clock_s"]
    (out_dir / "manifest.json").write_text(json.dumps(manifest,
                                                      indent=2))
    with open(out_dir / "brain_log.jsonl", "w") as fh:
        for reply in brain_records:
            fh.write(protocol.dumps_line(reply))
    with open(out_dir / "body_log.jsonl", "w") as fh:
        for rec in body_records:
            fh.write(json.dumps(rec) + "\n")
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print("summary:", json.dumps(summary), flush=True)
    print("wrote", out_dir, flush=True)
    return manifest, summary


def summarise(scenario, brain_records, body_records):
    e_series = [r["E_rad"] for r in body_records]
    events = [r["taste_event_at_chunk_end"] for r in body_records]
    onset = first_run_at_least(e_series, ONSET_RAD) if e_series else None
    offset = (first_run_below(e_series, THETA_OFF, onset + 1)
              if onset is not None else None)
    applied = {d["name"]: [b["applied"][d["name"]] for b in brain_records]
               for d in scenario["drives"]}
    derived = {
        "completed_chunks": len(body_records),
        "all_finite": bool(body_records
                           and all(r["finite"] for r in body_records)),
        "peak_E_rad": max(e_series) if e_series else None,
        "final_E_rad": e_series[-1] if e_series else None,
        "onset_chunk_SS4.4": onset,
        "offset_chunk_SS4.4": offset,
        "first_contact_event_chunk": next(
            (k for k, v in enumerate(events) if v), None),
        "event_on_chunks": int(sum(events)),
        "max_labrum_food_force_N": max(
            (r["max_labrum_food_force_N"] for r in body_records),
            default=None),
        "max_front_tarsus_food_force_N": max(
            (r["max_front_tarsus_food_force_N"] for r in body_records),
            default=None),
        "total_mn9_spikes": int(sum(
            b["counts"]["mn9_left"] + b["counts"]["mn9_right"]
            for b in brain_records)),
        "drive_applied_chunks": {
            name: int(sum(s["applied"] for s in states))
            for name, states in applied.items()},
    }
    checks = {}
    if scenario["name"].startswith("S1"):
        sugar = applied["sugar"]
        after = [(s["event_gate"], s["window_gate"], s["applied"])
                 for s in sugar[10:]]
        checks = {
            "contact_occurred_event_on": derived[
                "first_contact_event_chunk"] is not None,
            "E_rose_to_onset": onset is not None,
            "event_sustained_drive_after_window": any(
                ev and not win and app for ev, win, app in after),
            "after_window_applied_equals_event_gate": all(
                app == ev for ev, win, app in after),
            "both_gates_logged_separately": all(
                set(s.keys()) == {"event_gate", "window_gate", "applied"}
                for s in sugar),
        }
        derived["smoke_verdict"] = ("PASS" if all(checks.values())
                                    else "FAIL")
    elif scenario["name"].startswith("S2"):
        checks = {
            "no_taste_event_ever": not any(events),
            "no_food_contact_force": bool(
                derived["max_labrum_food_force_N"] == 0.0
                and derived["max_front_tarsus_food_force_N"] == 0.0),
            "E_stayed_below_onset": bool(
                e_series and max(e_series) < ONSET_RAD),
            "mn9_silent": derived["total_mn9_spikes"] == 0,
            "drive_never_applied": all(
                not s["applied"] for s in applied["sugar"]),
        }
        derived["smoke_verdict"] = ("PASS" if all(checks.values())
                                    else "FAIL")
    derived["smoke_checks"] = checks
    return derived


def main():
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--scenario", choices=sorted(SCENARIOS))
    group.add_argument("--scenario-file", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--r-hi", type=float, default=R_HI_SMOKE)
    ap.add_argument("--r-hi-label", default=R_HI_SMOKE_LABEL)
    args = ap.parse_args()
    if args.scenario:
        scenario = dict(SCENARIOS[args.scenario])
    else:
        scenario = json.loads(args.scenario_file.read_text())
    run_episode(scenario, args.out, args.r_hi, args.r_hi_label)


if __name__ == "__main__":
    main()
