"""The experiment runner: one config in, one run directory out -- spikes
plus a manifest, every time, with no silent shortcuts.

Two upstream behaviours are deliberately NOT reproduced here:

- Upstream's run_exp silently skips a run if its output file already
  exists, so a stale results file can stand in for a simulation that
  never happened. This runner refuses, loudly: if the run directory
  exists and is not empty, run_experiment raises FileExistsError. A
  re-run is a new run_id, chosen by a person, on the record.
- Upstream sets no seeds. Here every trial's seed is derived from the
  config's seed (seed + trial number) and written into the manifest, so
  any run in this project can be repeated exactly.

Output layout: <out_root>/<run_id>/spikes.parquet + manifest.json.
The spike table uses the same schema as the upstream outputs (and hence
as the Part 3 reference file sugarR.parquet): columns t (seconds),
trial, flywire_id, exp_name.
"""

import json
import platform
import socket
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import brian2
import numpy as np
import pandas as pd
from brian2 import Hz

from ..data.loader import load_connectome, load_populations, sha256_of
from .model import Brain

MANIFEST_VERSION = 1


def _git_info(repo_root):
    """(commit, dirty) of the working clone, for the manifest. Whatever
    git reports is recorded unedited -- an untracked or modified tree
    shows up as dirty=True, and that is the honest answer either way."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, capture_output=True,
            text=True, check=True).stdout.strip()
        dirty = bool(subprocess.run(
            ["git", "status", "--porcelain"], cwd=repo_root,
            capture_output=True, text=True, check=True).stdout.strip())
        return commit, dirty
    except Exception:
        return None, None


def _resolve_ids(entry, data, populations):
    """A stimulus/block entry names either a population from the Part 2
    artefacts or an explicit FlyWire ID list. Returns FlyWire IDs."""
    if "population" in entry:
        name = entry["population"]
        if populations is None or name not in populations:
            raise KeyError(f"unknown population {name!r} "
                           f"(id_sets_dir not loaded or name not in it)")
        return data.ids[populations[name]]
    return np.asarray(entry["flywire_ids"], dtype=np.int64)


def run_experiment(config, out_root, data=None, populations=None):
    """Run the experiment described by `config` (a plain dict, JSON-able).

    Config keys: run_id, exp_name, part, seed, n_trials, duration_ms,
    stimuli (list of {population|flywire_ids, rate_hz}), block_output
    (same entry shape, optional), data_dir and id_sets_dir (paths, used
    unless `data`/`populations` are passed in directly -- the tests pass
    a small synthetic connectome that way).

    Returns the run directory (Path). Raises FileExistsError if the run
    directory already holds anything.
    """
    run_id = config["run_id"]
    run_dir = Path(out_root) / run_id
    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(
            f"run directory {run_dir} already exists and is not empty. "
            f"Refusing to overwrite or silently skip -- a re-run needs a "
            f"new run_id.")
    run_dir.mkdir(parents=True, exist_ok=True)

    if data is None:
        data = load_connectome(config["data_dir"], verify=True)
    if populations is None and config.get("id_sets_dir"):
        populations = load_populations(config["id_sets_dir"], data)

    seed = int(config["seed"])
    duration_ms = float(config["duration_ms"])
    started = time.time()
    frames = []
    for trial in range(int(config["n_trials"])):
        brain = Brain(data, seed=seed + trial).build()
        for entry in config.get("block_output", []):
            brain.block_output(_resolve_ids(entry, data, populations))
        for entry in config.get("stimuli", []):
            brain.add_drive(_resolve_ids(entry, data, populations),
                            float(entry["rate_hz"]) * Hz)
        brain.run(duration_ms)
        idx, t = brain.spikes()
        frames.append(pd.DataFrame({
            "t": t, "trial": trial,
            "flywire_id": data.ids[idx],
            "exp_name": config["exp_name"],
        }))
    spikes = (pd.concat(frames, ignore_index=True) if frames
              else pd.DataFrame(columns=["t", "trial", "flywire_id",
                                        "exp_name"]))
    spikes_path = run_dir / "spikes.parquet"
    spikes.to_parquet(spikes_path, index=False)
    wall_clock = time.time() - started

    repo_root = Path(__file__).resolve().parents[3]
    commit, dirty = _git_info(repo_root)
    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "part": config.get("part", "2"),
        "prereg_id": config.get("prereg_id", "exploratory"),
        "question": config.get("question", ""),
        "code": {
            "repo_commit": commit,
            "working_tree_dirty": dirty,
            "entry_point": "ctb.brain.runner.run_experiment",
        },
        "data": {
            "dataset": "FlyWire v630",
            "source": data.source,
            "files_sha256": data.file_hashes,
        },
        "environment": {
            "python": platform.python_version(),
            "brian2": brian2.__version__,
            "numpy": np.__version__,
            "host": socket.gethostname(),
            "cpus": len(__import__("os").sched_getaffinity(0)),
        },
        "config": {k: v for k, v in config.items()
                   if k not in ("data_dir", "id_sets_dir")},
        "data_dir": config.get("data_dir"),
        "id_sets_dir": config.get("id_sets_dir"),
        "seed": seed,
        "trial_seeds": [seed + t for t in range(int(config["n_trials"]))],
        "outputs": [{"path": "spikes.parquet",
                     "sha256": sha256_of(spikes_path)}],
        "wall_clock_s": round(wall_clock, 2),
        "result_summary": (
            f"{len(spikes)} spikes from {spikes['flywire_id'].nunique()} "
            f"active neurons over {int(config['n_trials'])} trial(s) of "
            f"{duration_ms} ms"),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return run_dir
