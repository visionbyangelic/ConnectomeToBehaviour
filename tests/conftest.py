"""Shared fixtures for the brain model test suite.

The real-data fixtures load the hashed v630 files once per module -- the
connectivity parquet is 87 MB, and re-reading it per test would make the
suite slow enough that nobody would run it. The tiny synthetic connectomes
exist so the model and runner tests can check exact numbers by hand
instead of trusting the big files to be right.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_DIR / "src"))

DATA_DIR = REPO_DIR / "data"
ID_SETS_DIR = REPO_DIR / "data" / "neuron_sets"


def make_data(ids, edges):
    """A ConnectomeData from hand-written rows. `edges` is a list of
    (pre_index, post_index, synapse_count, sign)."""
    from brain_model.data.loader import ConnectomeData
    ids = np.asarray(ids, dtype=np.int64)
    frame = pd.DataFrame({
        "Presynaptic_ID": [ids[e[0]] for e in edges],
        "Postsynaptic_ID": [ids[e[1]] for e in edges],
        "Presynaptic_Index": [e[0] for e in edges],
        "Postsynaptic_Index": [e[1] for e in edges],
        "Connectivity": [e[2] for e in edges],
        "Excitatory": [e[3] for e in edges],
    })
    return ConnectomeData(ids, frame, source="synthetic (test fixture)")


@pytest.fixture(scope="module")
def connectome():
    from brain_model.data.loader import load_connectome
    return load_connectome(DATA_DIR, verify=True)


@pytest.fixture()
def tiny_data():
    """Five neurons, four edges with hand-checkable weights:
    0->1: 10 excitatory (2.75 mV), 1->2: 4 inhibitory (-1.1 mV),
    0->2: 2 excitatory (0.55 mV), 3->4: 1 excitatory (0.275 mV)."""
    return make_data([101, 102, 103, 104, 105],
                     [(0, 1, 10, +1), (1, 2, 4, -1),
                      (0, 2, 2, +1), (3, 4, 1, +1)])


@pytest.fixture()
def chain_data():
    """Two neurons, one strong excitatory edge 0->1 (40 synapses,
    11 mV) -- enough for the driven neuron to fire the other one."""
    return make_data([201, 202], [(0, 1, 40, +1)])


@pytest.fixture()
def solo_data():
    """Three neurons, no edges at all: whatever a driven neuron does is
    its own response, with no network in between."""
    return make_data([301, 302, 303], [])


@pytest.fixture()
def fan_data():
    """Six neurons built to stress block_output: neuron 0 fans out to
    four targets with mixed counts and signs, neuron 5 receives but has
    NO outgoing edges at all, and the fan's targets also connect onward
    and to each other -- so a complete before/after weight-vector check
    can tell a surgical block from a clumsy one:
    0->1: 3 exc, 0->2: 5 inh, 0->3: 7 exc, 0->4: 2 inh,
    1->2: 4 exc, 2->5: 6 exc, 3->5: 1 inh, 4->1: 8 exc."""
    return make_data([401, 402, 403, 404, 405, 406],
                     [(0, 1, 3, +1), (0, 2, 5, -1), (0, 3, 7, +1),
                      (0, 4, 2, -1), (1, 2, 4, +1), (2, 5, 6, +1),
                      (3, 5, 1, -1), (4, 1, 8, +1)])
