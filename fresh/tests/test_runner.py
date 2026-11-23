"""Runner tests: a run always leaves spikes + a complete manifest, the
same seed repeats exactly (upstream could not do this), and an existing
run is never silently skipped or overwritten (Reviewer 2's condition)."""

import json

import pandas as pd
import pytest

from ctb.brain.runner import run_experiment


def _config(run_id, seed=7):
    return {
        "run_id": run_id,
        "exp_name": "tiny_chain",
        "part": "2 (test)",
        "question": "runner mechanics only -- no science in this run",
        "seed": seed,
        "n_trials": 2,
        "duration_ms": 100,
        "stimuli": [{"flywire_ids": [201], "rate_hz": 150}],
    }


def test_run_writes_spikes_and_complete_manifest(chain_data, tmp_path):
    run_dir = run_experiment(_config("run-a"), tmp_path, data=chain_data)
    spikes = pd.read_parquet(run_dir / "spikes.parquet")
    assert set(spikes.columns) == {"t", "trial", "flywire_id", "exp_name"}
    assert set(spikes["trial"]) == {0, 1}
    assert set(spikes["exp_name"]) == {"tiny_chain"}
    assert len(spikes) > 0

    manifest = json.loads((run_dir / "manifest.json").read_text())
    assert manifest["run_id"] == "run-a"
    assert manifest["seed"] == 7
    assert manifest["trial_seeds"] == [7, 8]
    assert manifest["outputs"][0]["sha256"]  # output hashed, not just named
    assert manifest["config"]["duration_ms"] == 100
    assert manifest["result_summary"]
    assert manifest["environment"]["brian2"]


def test_runner_refuses_to_rerun_into_existing_outputs(chain_data, tmp_path):
    run_experiment(_config("run-b"), tmp_path, data=chain_data)
    with pytest.raises(FileExistsError):
        run_experiment(_config("run-b"), tmp_path, data=chain_data)


def test_same_seed_repeats_exactly(chain_data, tmp_path):
    first = run_experiment(_config("run-c1"), tmp_path, data=chain_data)
    second = run_experiment(_config("run-c2"), tmp_path, data=chain_data)
    a = pd.read_parquet(first / "spikes.parquet")
    b = pd.read_parquet(second / "spikes.parquet")
    pd.testing.assert_frame_equal(
        a.sort_values(["trial", "t", "flywire_id"]).reset_index(drop=True),
        b.sort_values(["trial", "t", "flywire_id"]).reset_index(drop=True))
