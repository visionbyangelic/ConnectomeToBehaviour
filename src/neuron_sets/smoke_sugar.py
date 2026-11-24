"""Part 2 smoke run: does the freshly built model, driven the way the
paper's first experiment drives it, produce a sane MN9 signal?

One trial, 1.0 s, right sugar GRNs at the default 150 Hz, seed 0, full
v630 network. The numbers printed are a SANITY SIGNAL ONLY -- they say
the build runs end to end and the feeding readout responds in the
expected direction and range. They are NOT a validation result: Part 3
owns the comparison against the sugarR reference, with its pre-registered
criteria, trial counts and statistics. Nothing here should be quoted as
a reproduction of anything.

Run with the pinned brain env from the repo root:
    ../envs/brain/bin/python src/neuron_sets/smoke_sugar.py
"""

import sys
from pathlib import Path

import pandas as pd

REPO_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_DIR / "src"))

from brain_model.brain.runner import run_experiment  # noqa: E402

MN9_LEFT = 720575940660219265
MN9_RIGHT = 720575940645521262

CONFIG = {
    "run_id": "part2-smoke-sugar-seed0",
    "exp_name": "smoke_sugarR",
    "part": "2",
    "question": "Sanity only: does the fresh build run end to end and "
                "does MN9 respond to right-sugar drive in a sane range? "
                "NOT a validation run (Part 3 owns validation).",
    "seed": 0,
    "n_trials": 1,
    "duration_ms": 1000,
    "stimuli": [{"population": "sugar_grn_right", "rate_hz": 150}],
    "data_dir": str(REPO_DIR / "data"),
    "id_sets_dir": str(REPO_DIR / "data" / "neuron_sets"),
}


def main():
    run_dir = run_experiment(CONFIG, REPO_DIR / "results" / "validation" / "runs")
    spikes = pd.read_parquet(run_dir / "spikes.parquet")
    duration_s = CONFIG["duration_ms"] / 1000
    print(f"\nrun directory: {run_dir}")
    print(f"total spikes: {len(spikes)}; active neurons: "
          f"{spikes['flywire_id'].nunique()}")
    for label, fid in [("MN9 left", MN9_LEFT), ("MN9 right", MN9_RIGHT)]:
        n = int((spikes["flywire_id"] == fid).sum())
        print(f"{label} ({fid}): {n} spikes = {n / duration_s:.1f} Hz")
    print("\nSANITY SIGNAL ONLY -- not a validation result. "
          "Part 3 owns the sugarR comparison.")


if __name__ == "__main__":
    main()
