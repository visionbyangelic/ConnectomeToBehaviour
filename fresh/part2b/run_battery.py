"""Part 2b stability battery: sanity run + loop episodes + criteria.

Runs, in order:
  1. the decoder-only sanity run (sanity_decoder_only.py),
  2. three CLOSED-loop episodes (seeds 4200, 4201, 4202),
  3. one OPEN-loop control episode (seed 4200; feedback logged, never
     connected),
then evaluates the pre-set stability criteria (below) from the episode
JSONs and writes runs/part2b_summary.json.

THE CRITERIA -- fixed here, before any episode ran. (The Part 2b probes
ran earlier and informed the DESIGN -- decoder constants, chunk size,
the JON channel; the amplitude bands in C3 are set from the decoder's
own ramp geometry and the probe-measured DN rates, and are recorded in
PART2B-BUILD.md alongside the probe numbers they came from. No episode
output existed when these lines were written.)

  C1 completion/finiteness: every closed episode completes 20/20
     chunks, every recorded body state finite (no NaN/Inf anywhere).
  C2 physical bounds: thorax height stays within (0, 3) mm and total
     travel < 100 mm per episode (explosion detectors, not science).
  C3 walking-while-active: in each closed episode, mean per-chunk
     travel in chunks with decoder amplitude >= AMP_ON exceeds mean
     travel in chunks with amplitude <= AMP_OFF by >= 0.3 mm.
  C4 sensory re-entry: in each closed episode, chunks whose JON drive
     was commanded by FEEDBACK show mean JON spike count >= 20, and
     chunks with the drive off show mean count 0 (the Part 3-verified
     baseline) or at most a tenth of the feedback chunks' mean.
  C5 closed-vs-open contrast (exploratory): the open control's travel
     over chunks 10-19 is less than half the closed episodes' mean
     travel over the same chunks -- the loop, not the scripted pulse,
     is what sustains the walking.

K6 (FINAL-PLAN S9.1) is about C1/C2-class failure -- the loop cannot
run stably. C3-C5 failing with C1/C2 intact is a weak or negative
scientific result, reported as such; it is not K6 and it is not
rescued by retuning.
"""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
PART2B = HERE.parent
BODY_PYTHON = sys.executable          # this script runs in the body env
RUNS = PART2B / "runs"

AMP_ON = 0.5      # decoder mid-ramp: (rate_ema - 2) / 38 >= 0.5 at 21 Hz
AMP_OFF = 0.05
CLOSED_SEEDS = (4200, 4201, 4202)
OPEN_SEED = 4200


def run(cmd):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True)


def load(name):
    return json.loads((RUNS / name).read_text())


def evaluate(episodes, control):
    checks = {}

    def chunks(ep):
        return ep["chunks"]

    c1 = all(ep["summary"]["completed_chunks"] == 20
             and ep["summary"]["all_finite"] for ep in episodes)
    checks["C1_completion_and_finiteness"] = bool(c1)

    c2 = all(0.0 < ep["summary"]["thorax_z_min_mm"]
             and ep["summary"]["thorax_z_max_mm"] < 3.0
             and ep["summary"]["total_travel_mm"] < 100.0
             for ep in episodes)
    checks["C2_physical_bounds"] = bool(c2)

    c3_detail = []
    for ep in episodes:
        rows = chunks(ep)
        on = [r["travel_mm"] for r in rows if r["amplitude"] >= AMP_ON]
        off = [r["travel_mm"] for r in rows if r["amplitude"] <= AMP_OFF]
        diff = (float(np.mean(on)) - float(np.mean(off))) \
            if on and off else None
        c3_detail.append({"seed": ep["seed"], "n_on": len(on),
                          "n_off": len(off), "mean_diff_mm": diff})
    checks["C3_walking_while_active"] = bool(
        all(d["mean_diff_mm"] is not None and d["mean_diff_mm"] >= 0.3
            for d in c3_detail))
    checks["C3_detail"] = c3_detail

    c4_detail = []
    for ep in episodes:
        rows = chunks(ep)
        fb = [r["counts"]["jon_all"] for r in rows
              if r["jon_source"] == "feedback"]
        off = [r["counts"]["jon_all"] for r in rows
               if r["jon_source"] == "off"]
        ok = bool(fb) and float(np.mean(fb)) >= 20 and (
            not off or float(np.mean(off)) <= 0.1 * float(np.mean(fb)))
        c4_detail.append({"seed": ep["seed"], "n_feedback": len(fb),
                          "mean_jon_feedback": float(np.mean(fb)) if fb
                          else None,
                          "mean_jon_off": float(np.mean(off)) if off
                          else None, "ok": bool(ok)})
    checks["C4_sensory_reentry"] = bool(all(d["ok"] for d in c4_detail))
    checks["C4_detail"] = c4_detail

    def late_travel(ep):
        return float(sum(r["travel_mm"] for r in chunks(ep)
                         if r["chunk"] >= 10))

    closed_late = float(np.mean([late_travel(ep) for ep in episodes]))
    open_late = late_travel(control)
    checks["C5_closed_vs_open_exploratory"] = bool(
        open_late < 0.5 * closed_late)
    checks["C5_detail"] = {"closed_mean_late_travel_mm": closed_late,
                           "open_late_travel_mm": open_late}

    checks["stability_verdict"] = (
        "STABLE" if checks["C1_completion_and_finiteness"]
        and checks["C2_physical_bounds"] else "UNSTABLE (K6 territory)")
    return checks


def main():
    RUNS.mkdir(parents=True, exist_ok=True)
    run([BODY_PYTHON, PART2B / "sanity_decoder_only.py"])
    names = []
    for seed in CLOSED_SEEDS:
        name = f"ep_closed_{seed}.json"
        run([BODY_PYTHON, PART2B / "run_loop.py", "--mode", "closed",
             "--seed", seed, "--out", RUNS / name])
        names.append(name)
    control_name = f"ep_open_{OPEN_SEED}.json"
    run([BODY_PYTHON, PART2B / "run_loop.py", "--mode", "open",
         "--seed", OPEN_SEED, "--out", RUNS / control_name])

    episodes = [load(n) for n in names]
    control = load(control_name)
    sanity = load("sanity_decoder_only.json")
    checks = evaluate(episodes, control)
    summary = {"part": "2b", "criteria": checks,
               "episodes": {n: load(n)["summary"] for n in names},
               "control": {control_name: control["summary"]},
               "sanity_phases": sanity["phases"]}
    (RUNS / "part2b_summary.json").write_text(json.dumps(summary,
                                                         indent=2))
    print(json.dumps(checks, indent=2), flush=True)
    print(f"wrote {RUNS / 'part2b_summary.json'}", flush=True)


if __name__ == "__main__":
    main()
