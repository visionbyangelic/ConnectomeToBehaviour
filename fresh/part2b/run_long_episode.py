"""Part 2b gate-condition run: ONE long closed-loop episode (15 s).

Reviewer 1's Part 2b gate condition (c) asks for one 10-20 s closed
episode with criteria fixed beforehand (state drift, memory growth,
wall-clock) before Part 4's main work -- because the battery's
"STABLE" verdict covers 2 s episodes, and 2 s says nothing about
long-run robustness. This script IS the fixing: the criteria below
were written into this file before the run, and the runner evaluates
exactly them, reporting pass/fail per criterion whatever happens.
Nothing is retuned after the fact; if a criterion fails, the failure
is the result.

Configuration: the battery's closed loop, unchanged -- same frozen
brain, same toy decoder, same constructed contact->JON feedback, same
100 ms chunks, same scripted touch pulse at chunks 2-3. Seed 4203,
the next unused seed in the Part 2b battery block (4200-4202 closed,
4200 open). Duration 15 s simulated = 150 chunks.

Criteria (fixed here, before the run):
  L1 completion: 150/150 chunks recorded.
  L2 finiteness: every recorded body state finite (run_loop's
     per-chunk check: thorax position + all joint angles).
  L3 thorax bounds: thorax height within (0, 3) mm at every chunk --
     the battery's C2 explosion detector, unchanged.
  L4 no state drift beyond a stated band:
     (i) posture -- |mean thorax height over the final 20 chunks
         minus mean over chunks 20-39| <= 0.15 mm (the battery's
         episodes held thorax height inside a ~0.26 mm total range,
         so 0.15 mm of mean drift is a real band, not a formality);
     (ii) behaviour -- mean travel over the final 20 chunks
         >= 0.5 mm/chunk (the loop is still walking at the end, not
         stalled or decayed to the open-control's ~0 mm), and total
         travel < 400 mm (15 s at the loop's ~13 mm/s is ~200 mm;
         400 mm is the explosion bound).
  L5 memory growth bounded: process-tree RSS (this driver + the
     brain worker) is sampled every 2 s. Baseline = median RSS over
     the window [180 s, 240 s] of wall time (build and compile
     warmup long finished, episode underway). Criterion: peak RSS
     after 240 s <= baseline + 250 MB. One-off model-build
     allocation is not growth; this bounds growth DURING the run.
Wall clock is recorded and reported per simulated second; it is a
cost figure, not a pass/fail criterion.

Outputs: runs/ep_long_4203.json (the episode, by run_loop),
runs/ep_long_4203.worker.log, runs/long_episode_verdict.json.
"""

import json
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve()
PART2B = HERE.parent
sys.path.insert(0, str(PART2B))

import run_loop  # noqa: E402

SEED = 4203
N_CHUNKS = 150                    # 15.0 s at 100 ms chunks
MODE = "closed"
OUT = PART2B / "runs" / f"ep_long_{SEED}.json"
VERDICT_OUT = PART2B / "runs" / "long_episode_verdict.json"

# --- criteria, fixed before the run (see docstring) ---
DRIFT_BAND_MM = 0.15
MIN_LATE_TRAVEL_MM_PER_CHUNK = 0.5
MAX_TOTAL_TRAVEL_MM = 400.0
THORAX_BOUNDS_MM = (0.0, 3.0)
MEMORY_GROWTH_BUDGET_MB = 250.0
BASELINE_WINDOW_S = (180.0, 240.0)
SAMPLE_EVERY_S = 2.0


def _tree_rss_mb(root_pid):
    """RSS (MB) of root_pid plus all descendants, from /proc."""
    children = {}
    rss = {}
    for stat in Path("/proc").glob("[0-9]*/stat"):
        try:
            parts = stat.read_text().rsplit(")", 1)
            pid = int(stat.parent.name)
            ppid = int(parts[1].split()[1])
            children.setdefault(ppid, []).append(pid)
        except Exception:
            continue
    for status in Path("/proc").glob("[0-9]*/status"):
        try:
            for line in status.read_text().splitlines():
                if line.startswith("VmRSS:"):
                    rss[int(status.parent.name)] = (
                        int(line.split()[1]) / 1024.0)
                    break
        except Exception:
            continue
    total, stack = 0.0, [root_pid]
    while stack:
        pid = stack.pop()
        total += rss.get(pid, 0.0)
        stack.extend(children.get(pid, []))
    return total


def main():
    import os
    samples = []                  # (wall_s_since_start, tree_rss_mb)
    stop = threading.Event()
    t_start = time.time()

    def sampler():
        while not stop.is_set():
            samples.append((round(time.time() - t_start, 1),
                            round(_tree_rss_mb(os.getpid()), 1)))
            stop.wait(SAMPLE_EVERY_S)

    thread = threading.Thread(target=sampler, daemon=True)
    thread.start()
    run_loop.N_CHUNKS = N_CHUNKS
    try:
        episode = run_loop.run_episode(MODE, SEED, OUT)
    finally:
        stop.set()
        thread.join(timeout=5)
    wall_s = time.time() - t_start

    chunks = episode["chunks"]
    summary = episode["summary"]
    z = [r["thorax_z_mm"] for r in chunks]
    travel = [r["travel_mm"] for r in chunks]

    def mean(xs):
        return sum(xs) / len(xs) if xs else float("nan")

    drift = abs(mean(z[-20:]) - mean(z[20:40]))
    late_travel = mean(travel[-20:])

    baseline_samples = [r for (t, r) in samples
                        if BASELINE_WINDOW_S[0] <= t <= BASELINE_WINDOW_S[1]]
    baseline = (sorted(baseline_samples)[len(baseline_samples) // 2]
                if baseline_samples else None)
    after = [r for (t, r) in samples if t > BASELINE_WINDOW_S[1]]
    peak_after = max(after) if after else None
    growth = (peak_after - baseline
              if baseline is not None and peak_after is not None else None)

    criteria = {
        "L1_completion": len(chunks) == N_CHUNKS,
        "L2_finiteness": bool(summary["all_finite"]),
        "L3_thorax_bounds": bool(
            min(z) > THORAX_BOUNDS_MM[0] and max(z) < THORAX_BOUNDS_MM[1]),
        "L4i_posture_drift": bool(drift <= DRIFT_BAND_MM),
        "L4ii_still_walking": bool(
            late_travel >= MIN_LATE_TRAVEL_MM_PER_CHUNK),
        "L4iii_no_explosion": bool(
            summary["total_travel_mm"] < MAX_TOTAL_TRAVEL_MM),
        "L5_memory_growth": bool(
            growth is not None and growth <= MEMORY_GROWTH_BUDGET_MB),
    }
    verdict = {
        "part": "2b",
        "run": "long_episode_gate_condition_c",
        "seed": SEED, "mode": MODE, "n_chunks": N_CHUNKS,
        "simulated_duration_s": N_CHUNKS * run_loop.CHUNK_MS / 1000.0,
        "criteria_fixed_before_run": {
            "drift_band_mm": DRIFT_BAND_MM,
            "min_late_travel_mm_per_chunk": MIN_LATE_TRAVEL_MM_PER_CHUNK,
            "max_total_travel_mm": MAX_TOTAL_TRAVEL_MM,
            "thorax_bounds_mm": list(THORAX_BOUNDS_MM),
            "memory_growth_budget_mb": MEMORY_GROWTH_BUDGET_MB,
            "memory_baseline_window_s": list(BASELINE_WINDOW_S),
        },
        "measurements": {
            "chunks_completed": len(chunks),
            "all_finite": bool(summary["all_finite"]),
            "thorax_z_min_mm": min(z), "thorax_z_max_mm": max(z),
            "thorax_z_mean_chunks_20_39_mm": mean(z[20:40]),
            "thorax_z_mean_final_20_mm": mean(z[-20:]),
            "posture_drift_mm": drift,
            "total_travel_mm": summary["total_travel_mm"],
            "late_travel_mm_per_chunk": late_travel,
            "memory_baseline_mb": baseline,
            "memory_peak_after_baseline_mb": peak_after,
            "memory_growth_mb": growth,
            "memory_samples": len(samples),
            "wall_clock_s": round(wall_s, 1),
            "wall_clock_s_per_simulated_s": round(
                wall_s / (N_CHUNKS * run_loop.CHUNK_MS / 1000.0), 1),
        },
        "criteria": criteria,
        "all_criteria_passed": bool(all(criteria.values())),
    }
    VERDICT_OUT.write_text(json.dumps(verdict, indent=2))
    print(json.dumps(verdict, indent=2), flush=True)
    return verdict


if __name__ == "__main__":
    main()
