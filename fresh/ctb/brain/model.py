"""The whole-brain LIF model -- our own implementation of the published
specification.

The specification is Shiu et al. (2024) as read line by line from the
upstream code (project record: fresh/PART2-READING-LOG.md). This module was
written from that reading, not copied from upstream: no upstream code is
imported, executed, or reproduced here. Where the reading showed the
upstream *code* and the upstream *description* diverging, the code is what
is implemented, and the divergence is named.

The model, in one paragraph: every neuron is the same leaky
integrate-and-fire unit; a presynaptic spike adds the synapse's weight to
the postsynaptic neuron's input variable `g`, which then decays with a
5 ms time constant; weights are anatomical synapse count x predicted
transmitter sign x 0.275 mV, for every one of the 14,687,178 edges in the
connectivity file, with no threshold or filtering of any kind.

Deliberate deviations from upstream (each named, each with its reason --
also tabulated in fresh/PART2-BUILD.md):

1. SEEDED RUNS. Upstream sets no random seed anywhere, so an individual
   published run can never be repeated exactly. Here the seed is a build
   parameter: two builds with the same seed and the same stimulus produce
   identical spike trains. Our results are therefore reproducible in a
   way upstream's are not; comparisons against upstream outputs are
   necessarily statistical (distributional), never spike-for-spike.
2. THE RESET STRING CARRIES NO UNDEFINED VARIABLE. Upstream's reset is
   'v = v_rst; w = 0; g = 0 * mV', but the neuron equations define no `w`.
   A dedicated experiment at the pinned Brian2 2.9.0 (Part 2,
   part2/w_reset_test.py) established that the clause is silently
   ignored: no error, no warning, no variable created, and spike trains
   bit-identical with and without it. Our reset is 'v = v_rst; g = 0 * mV'
   -- same dynamics, nothing undefined.
3. HONEST NAMES FOR MANIPULATIONS. Upstream's silence() zeroes a neuron's
   outgoing weights only; the neuron still receives input and still
   spikes. That operation is named `block_output` here, because that is
   what it does. It is kept distinct from input-blocking and from full
   ablation, which are different operations and are not implemented by
   quietly widening this one.
4. EXPLICIT POSTSYNAPTIC TARGET. Upstream's on_pre is 'g += w'; ours is
   'g_post += w'. Same variable (Brian2 resolves the bare name to the
   postsynaptic side), written so the direction is visible in the code.
"""

import numpy as np
from brian2 import (Network, NeuronGroup, PoissonInput, SpikeMonitor,
                    Synapses, defaultclock, ms, mV, second, seed,
                    start_scope)

# The paper's parameters, as cited in the upstream code itself:
# resting/reset/threshold and membrane constant from Kakaria & de Bivort
# (2017); synaptic time constant from Jurgensen et al.; refractory period
# from Lazar et al.; delay from Paul et al. (2015). w_syn is the model's
# one free parameter (Shiu et al. 2024) -- it is never re-fit here.
DEFAULT_PARAMS = {
    "v_0": -52 * mV,      # resting potential
    "v_rst": -52 * mV,    # reset potential after a spike
    "v_th": -45 * mV,     # spike threshold
    "t_mbr": 20 * ms,     # membrane time constant
    "tau": 5 * ms,        # synaptic (alpha) time constant, via g's decay
    "t_rfc": 2.2 * ms,    # refractory period
    "t_dly": 1.8 * ms,    # uniform delay on every synapse
    "w_syn": 0.275 * mV,  # weight per anatomical synapse (free parameter)
    "f_poi": 250,         # Poisson drive scaling (see add_drive)
    "dt": 0.1 * ms,       # integration timestep
}

# A single voltage-like synaptic input g: a presynaptic spike jumps it by
# the synapse weight, then it decays exponentially -- the paper's "alpha
# synapse" is this jump-plus-decay, not a weight that itself decays.
# The refractory period is a per-neuron state variable (rfc), not a fixed
# duration, because the drive needs to switch it off for driven neurons
# (see add_drive) -- that is upstream's design, kept deliberately.
EQS = """
dv/dt = (v_0 - v + g) / t_mbr : volt (unless refractory)
dg/dt = -g / tau               : volt (unless refractory)
rfc                            : second
"""
THRESHOLD = "v > v_th"
RESET = "v = v_rst; g = 0 * mV"  # no `w` clause -- see deviation 2 above


def synapse_weights(edges, params=None):
    """Synaptic weights for an edges table: anatomical synapse count x
    predicted transmitter sign x w_syn, as a Brian2 quantity array.

    Computed from the count and sign columns directly. The connectivity
    file also carries a precomputed 'Excitatory x Connectivity' column;
    that column is used only as a cross-check (the sampled sign audit in
    the tests), never as the source -- if the two ever disagreed, the
    disagreement itself would be a finding, and building from the
    components is what makes it visible.
    """
    p = dict(DEFAULT_PARAMS)
    if params:
        p.update(params)
    signed_counts = (edges["Connectivity"].to_numpy(dtype=np.float64)
                     * edges["Excitatory"].to_numpy(dtype=np.float64))
    return signed_counts * p["w_syn"]


class Brain:
    """One build of the whole-brain network: neurons, synapses, a spike
    monitor, and whatever drives have been added.

    A Brain is single-use in the same way upstream's is: manipulations
    (drives, output blocks) are applied after build() and before run(),
    and a new trial means a new Brain with its own seed.
    """

    def __init__(self, data, params=None, seed=0):
        self.data = data
        self.params = dict(DEFAULT_PARAMS)
        if params:
            self.params.update(params)
        self.seed = seed
        self.neurons = None
        self.synapses = None
        self.monitor = None
        self._drives = []

    def build(self):
        """Create the Brian2 objects. Seeding happens here, before any
        random object exists, so the whole build+run is a function of
        (data, params, seed, manipulations) and nothing else."""
        start_scope()
        seed(self.seed)
        defaultclock.dt = self.params["dt"]
        p = self.params
        namespace = {k: p[k] for k in ("v_0", "v_rst", "v_th", "t_mbr",
                                       "tau")}
        neu = NeuronGroup(len(self.data), model=EQS, method="linear",
                          threshold=THRESHOLD, reset=RESET,
                          refractory="rfc", namespace=namespace,
                          name="ctb_neurons")
        neu.v = p["v_0"]
        neu.g = 0 * mV
        neu.rfc = p["t_rfc"]

        syn = Synapses(neu, neu, "w : volt", on_pre="g_post += w",
                       delay=p["t_dly"], name="ctb_synapses")
        edges = self.data.edges
        if len(edges):
            syn.connect(
                i=edges["Presynaptic_Index"].to_numpy(dtype=np.int64),
                j=edges["Postsynaptic_Index"].to_numpy(dtype=np.int64))
            syn.w = synapse_weights(edges, p)
        # An edge-less connectome (test fixtures, toy subnetworks) skips
        # connect() entirely: Brian2 raises on zero-size index arrays,
        # and an unconnected Synapses must be marked inactive to run.
        if not len(edges):
            syn.active = False

        self.neurons, self.synapses = neu, syn
        self.monitor = SpikeMonitor(neu)
        return self

    # -- manipulations -------------------------------------------------

    def add_drive(self, flywire_ids, rate):
        """Poisson-drive a population, upstream-style.

        The drive injects straight into the membrane potential v (it does
        not go through the synaptic variable g), with a kick of
        w_syn x f_poi = 68.75 mV per event -- several times the
        rest-to-threshold distance, so a driven neuron fires at close to
        the drive rate by construction. Driven neurons also lose their
        refractory period (rfc set to 0), exactly as upstream does; both
        properties are part of what "activation" means in this model and
        are stated here rather than discovered later.

        `rate` is a Brian2 frequency (e.g. 150*Hz). Returns the list of
        PoissonInput objects (already registered for the next run()).

        One PoissonInput per neuron, on a single-neuron subgroup: Brian2
        subgroups must be contiguous ranges, so a whole scattered
        population cannot be targeted at once. This is also exactly how
        upstream constructs the drive (its poi() loops over neurons).
        """
        idx = self.data.index_of(flywire_ids)
        weight = self.params["w_syn"] * self.params["f_poi"]
        drives = []
        for i in idx:
            target = self.neurons[int(i)]
            drives.append(PoissonInput(target, target_var="v", N=1,
                                       rate=rate, weight=weight))
            target.rfc = 0 * second
        self._drives.extend(drives)
        return drives

    def block_output(self, flywire_ids):
        """Zero every outgoing synaptic weight of the given neurons.

        This is what upstream calls silence() and what it actually does:
        the neurons keep receiving input and keep spiking -- their spikes
        simply stop doing anything downstream. Incoming weights are
        untouched. Returns the number of synapses zeroed.
        """
        idx = self.data.index_of(flywire_ids)
        pre = np.asarray(self.synapses.i[:])
        # Explicit integer indices, not a boolean mask: assigning through
        # a boolean mask on a Brian2 synapse variable silently under-applies
        # (only some of the selected weights were zeroed -- caught by
        # test_block_output_zeroes_exactly_the_outgoing_weights, Part 2).
        to_zero = np.flatnonzero(np.isin(pre, idx))
        self.synapses.w[to_zero] = 0 * mV
        return int(len(to_zero))

    # -- running --------------------------------------------------------

    def run(self, duration_ms):
        """Run the network for `duration_ms` milliseconds of model time."""
        net = Network(self.neurons, self.synapses, self.monitor,
                      *self._drives)
        net.run(duration_ms * ms)

    def spikes(self):
        """(Brian indices, times in seconds) of every recorded spike."""
        return (np.asarray(self.monitor.i),
                np.asarray(self.monitor.t / second))
