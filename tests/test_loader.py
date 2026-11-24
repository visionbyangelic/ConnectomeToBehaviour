"""Loader tests: the files are the ones Part 1 hashed, the counts are
the ones Part 1 computed, and the populations are the ones Part 2
extracted. These numbers are the project's ground truth -- if a test
here fails, everything downstream is standing on different data than
the record says."""

import numpy as np
import pytest

from conftest import DATA_DIR, ID_SETS_DIR
from brain_model.data.loader import (EXPECTED_SHA256, check_index_consistency,
                             load_populations, verify_data_files)


def test_data_files_match_part1_hashes():
    assert verify_data_files(DATA_DIR) == EXPECTED_SHA256


def test_counts_match_part1(connectome):
    assert len(connectome) == 127_400
    assert len(np.unique(connectome.ids)) == 127_400
    edges = connectome.edges
    assert len(edges) == 14_687_178                      # edges
    assert int(edges["Connectivity"].sum()) == 52_793_639  # raw synapses
    assert int((edges["Connectivity"] >= 3).sum()) == 4_770_900


def test_index_id_consistency(connectome):
    # The correspondence upstream trusts silently; Part 2 verified it and
    # the loader must keep verifying it. 0 is the only acceptable count.
    assert check_index_consistency(connectome) == 0


def test_populations_match_manifest(connectome):
    import json
    manifest = json.loads((ID_SETS_DIR / "manifest.json").read_text())
    populations = load_populations(ID_SETS_DIR, connectome)
    assert set(populations) == set(manifest["populations"])
    for name, info in manifest["populations"].items():
        assert len(populations[name]) == info["count"], name
    # 242 distinct FlyWire IDs across all sets (jon_all adds none -- it
    # is exactly the union of the three JON subsets).
    all_ids = set()
    for indices in populations.values():
        all_ids.update(connectome.ids[indices].tolist())
    assert len(all_ids) == 242


def test_mn9_left_right_order(connectome):
    populations = load_populations(ID_SETS_DIR, connectome)
    mn9_ids = connectome.ids[populations["mn9"]]
    # The artefacts list MN9 left first, then right; the asymmetry
    # question (RQ-C5) depends on never confusing the two.
    assert mn9_ids.tolist() == [720575940660219265, 720575940645521262]


def test_missing_id_fails_loudly(connectome):
    with pytest.raises(KeyError):
        connectome.index_of([12345])  # not a v630 neuron
