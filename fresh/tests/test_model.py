"""Model tests: exact weights on hand-checkable networks, the plan's
Part 2 pass criteria in miniature (a silent network spikes zero times;
a single neuron's response to known input is correct), and block_output
doing exactly what its name says -- nothing more, nothing else."""

import numpy as np
from brian2 import Hz, mV

from ctb.brain.model import RESET, Brain, synapse_weights


def _weights_by_pair(brain):
    syn = brain.synapses
    return {(int(i), int(j)): float(w / mV)
            for i, j, w in zip(syn.i[:], syn.j[:], syn.w[:])}


def test_weight_formula_on_tiny_network(tiny_data):
    brain = Brain(tiny_data, seed=0).build()
    # count x sign x 0.275 mV, computed by hand from the fixture.
    assert _weights_by_pair(brain) == {
        (0, 1): 10 * 0.275, (1, 2): -4 * 0.275,
        (0, 2): 2 * 0.275, (3, 4): 1 * 0.275,
    }


def test_weight_formula_matches_files_own_product_column(connectome):
    # The sampled sign audit (plan Part 2 row): our count x sign product
    # must reproduce the file's precomputed 'Excitatory x Connectivity'
    # column on a random sample -- if the sign convention were inverted
    # anywhere, it would show up here.
    rng = np.random.default_rng(0)
    sample = connectome.edges.iloc[rng.choice(len(connectome.edges),
                                               size=2000, replace=False)]
    ours = np.asarray(synapse_weights(sample) / mV)
    theirs = sample["Excitatory x Connectivity"].to_numpy() * 0.275
    assert np.allclose(ours, theirs)


def test_reset_string_has_no_undefined_variable():
    # The `w` experiment (part2/w_reset_test.py) showed upstream's
    # `w = 0` clause is silently ignored by Brian2 2.9.0; our reset
    # omits it, so nothing in the reset is undefined.
    assert RESET == "v = v_rst; g = 0 * mV"


def test_silent_network_spikes_zero_times(tiny_data):
    brain = Brain(tiny_data, seed=0).build()
    brain.run(100)
    idx, _ = brain.spikes()
    assert len(idx) == 0


def test_single_neuron_response(solo_data):
    brain = Brain(solo_data, seed=0).build()
    brain.add_drive([301], 150 * Hz)
    brain.run(200)
    idx, _ = brain.spikes()
    counts = {n: int(np.sum(idx == n)) for n in range(3)}
    # 150 Hz for 200 ms with a suprathreshold kick and no refractory
    # period: the driven neuron fires at close to the drive rate (~30),
    # and with no synapses the others cannot fire at all.
    assert counts[0] >= 20
    assert counts[1] == 0 and counts[2] == 0


def test_block_output_zeroes_exactly_the_outgoing_weights(tiny_data):
    brain = Brain(tiny_data, seed=0).build()
    before = _weights_by_pair(brain)
    zeroed = brain.block_output([101])  # neuron 0
    after = _weights_by_pair(brain)
    assert zeroed == 2                       # edges 0->1 and 0->2
    assert after[(0, 1)] == 0 and after[(0, 2)] == 0
    # Everything else untouched -- including the incoming side of the
    # network and unrelated edges. Block-output is not ablation.
    assert after[(1, 2)] == before[(1, 2)]
    assert after[(3, 4)] == before[(3, 4)]


def _full_vectors(brain):
    """The complete synapse state -- (pre indices, post indices, weights
    in mV) in stored order. The whole vector, not picked entries."""
    syn = brain.synapses
    return (np.asarray(syn.i[:]), np.asarray(syn.j[:]),
            np.asarray(syn.w[:] / mV))


def test_block_output_full_vector_many_outgoing_edges(fan_data):
    # The Part 2 gate strengthening (Reviewer 3, condition E): the hub
    # neuron has four outgoing edges, and the check is the COMPLETE
    # before/after weight vector. The boolean-mask bug this guards
    # against zeroed some selected weights and left others standing --
    # entry-by-entry spot checks are exactly what can miss that.
    brain = Brain(fan_data, seed=0).build()
    pre_i, post_i, before = _full_vectors(brain)
    zeroed = brain.block_output([401])  # neuron 0, the hub
    pre_a, post_a, after = _full_vectors(brain)
    assert zeroed == 4
    # Topology untouched: same edges, same order, nothing rebuilt.
    assert np.array_equal(pre_a, pre_i) and np.array_equal(post_a, post_i)
    # Exactly the hub's four outgoing weights are zero; every other
    # weight in the vector is bit-identical to before.
    expected = before.copy()
    expected[pre_i == 0] = 0.0
    assert np.array_equal(after, expected)


def test_block_output_neuron_without_outgoing_edges_changes_nothing(fan_data):
    # Neuron 5 (ID 406) receives two edges and sends none. Blocking its
    # output must be a clean no-op: zero synapses zeroed, no error, and
    # the complete weight vector bit-identical afterwards. An operation
    # that crashes -- or quietly touches something else -- on a
    # no-outgoing-edge neuron would be a landmine for lesion lists,
    # which are not guaranteed to contain only well-connected neurons.
    brain = Brain(fan_data, seed=0).build()
    pre_i, post_i, before = _full_vectors(brain)
    zeroed = brain.block_output([406])
    pre_a, post_a, after = _full_vectors(brain)
    assert zeroed == 0
    assert np.array_equal(pre_a, pre_i) and np.array_equal(post_a, post_i)
    assert np.array_equal(after, before)


def test_blocked_neuron_still_spikes_but_drives_nothing(chain_data):
    driven = Brain(chain_data, seed=0).build()
    driven.add_drive([201], 150 * Hz)
    driven.run(200)
    idx, _ = driven.spikes()
    assert np.sum(idx == 0) >= 20 and np.sum(idx == 1) > 0

    blocked = Brain(chain_data, seed=0).build()
    blocked.block_output([201])
    blocked.add_drive([201], 150 * Hz)
    blocked.run(200)
    idx, _ = blocked.spikes()
    # The blocked neuron itself fires exactly as before (same seed, same
    # drive) -- it is disconnected, not silenced.
    assert np.sum(idx == 0) >= 20
    assert np.sum(idx == 1) == 0
