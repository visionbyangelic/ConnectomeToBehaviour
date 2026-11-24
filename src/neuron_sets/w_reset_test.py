"""What does Brian2 2.9.0 actually do with the upstream reset string?

The upstream model's reset is 'v = v_rst; w = 0; g = 0 * mV', but the neuron
equations define no `w` -- `w` is the *synapse* variable. The published results
were produced with this code, so under whatever Brian2 version upstream ran,
the clause did something (or nothing) without stopping the run. Reviewer 2's
Part 2 gate condition 1 requires this to be established by experiment at our
pinned Brian2 2.9.0, not assumed.

This script builds small networks that mirror the upstream construction
(same equations, same namespace style, same reset) in three variants:

  A  reset WITH the `w = 0` clause, synapses present (upstream's exact shape)
  B  reset WITHOUT the clause, synapses present (our candidate reset)
  C  reset WITH the clause, no synapses at all

For each variant it records: did construction/run raise, what warnings were
emitted, whether a variable named `w` exists on the neuron group afterwards,
and the spike train of a driven neuron. If A and B produce identical spike
trains, the clause is a no-op in effect whatever its mechanism; if A errors,
that is the finding, and it means the published code cannot run as written
under Brian2 2.9.0.

Run with the pinned brain env:
    envs/brain/bin/python repo/src/neuron_sets/w_reset_test.py
"""

import warnings

import numpy as np
from brian2 import (NeuronGroup, Network, PoissonInput, SpikeMonitor,
                    Synapses, defaultclock, mV, ms, Hz, seed, start_scope)

# The upstream equations and parameters, copied as *specification* from the
# reading log (docs/reading_log.md) -- values, not code.
EQS = """
dv/dt = (v_0 - v + g) / t_mbr : volt (unless refractory)
dg/dt = -g / tau               : volt (unless refractory)
rfc                            : second
"""

PARAMS = dict(v_0=-52 * mV, v_rst=-52 * mV, v_th=-45 * mV, t_mbr=20 * ms,
              tau=5 * ms, t_rfc=2.2 * ms, t_dly=1.8 * ms, w_syn=0.275 * mV)

RESET_WITH_W = "v = v_rst; w = 0; g = 0 * mV"   # upstream, verbatim
RESET_WITHOUT_W = "v = v_rst; g = 0 * mV"       # our candidate


def build_and_run(reset, with_synapses):
    """One small network in the upstream shape; returns (spikes_i, spikes_t,
    warnings_seen, error_or_None, group_has_w)."""
    start_scope()
    seed(12345)  # same seed for every variant, so spike trains are comparable
    defaultclock.dt = 0.1 * ms
    caught = []
    error = None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            neu = NeuronGroup(
                4, model=EQS, method="linear", threshold="v > v_th",
                reset=reset, refractory="rfc", namespace=dict(PARAMS),
                name="test_neurons")
            neu.v = PARAMS["v_0"]
            neu.g = 0 * mV
            neu.rfc = PARAMS["t_rfc"]
            objects = [neu]
            if with_synapses:
                syn = Synapses(neu, neu, "w : volt", on_pre="g += w",
                               delay=PARAMS["t_dly"], name="test_synapses")
                syn.connect(i=[0, 1, 2], j=[1, 2, 3])
                syn.w = 30 * mV  # strong, so downstream spikes are visible
                objects.append(syn)
            # Slam neuron 0 the way the upstream drive does: straight into v,
            # refractory removed -- it should fire at close to the drive rate.
            drive = PoissonInput(neu[0], target_var="v", N=1, rate=150 * Hz,
                                 weight=PARAMS["w_syn"] * 250)
            neu[0].rfc = 0
            mon = SpikeMonitor(neu)
            objects += [drive, mon]
            Network(*objects).run(200 * ms)
            has_w = "w" in neu.variables
            return (np.asarray(mon.i), np.asarray(mon.t / ms),
                    [str(w.message) for w in caught], None, has_w)
        except Exception as exc:  # the exception IS the datum here
            return (np.array([]), np.array([]),
                    [str(w.message) for w in caught],
                    f"{type(exc).__name__}: {exc}", None)


def main():
    import brian2
    print(f"Brian2 version: {brian2.__version__}")
    results = {}
    for label, reset, syn in [("A: reset with w=0, synapses present",
                               RESET_WITH_W, True),
                              ("B: reset without w clause, synapses present",
                               RESET_WITHOUT_W, True),
                              ("C: reset with w=0, NO synapses",
                               RESET_WITH_W, False)]:
        i, t, warns, err, has_w = build_and_run(reset, syn)
        results[label] = (i, t, err)
        print(f"\n{label}")
        print(f"  error: {err}")
        print(f"  warnings: {warns if warns else 'none'}")
        print(f"  neuron group has variable 'w' afterwards: {has_w}")
        print(f"  spikes recorded: {len(i)} "
              f"(neuron 0: {int(np.sum(i == 0))}, downstream 1-3: "
              f"{int(np.sum(i > 0))})")
    a_i, a_t, a_err = results["A: reset with w=0, synapses present"]
    b_i, b_t, _ = results["B: reset without w clause, synapses present"]
    if a_err is None:
        same = (len(a_i) == len(b_i) and np.array_equal(a_i, b_i)
                and np.allclose(a_t, b_t))
        print(f"\nA vs B spike trains identical (same seed): {same}")


if __name__ == "__main__":
    main()
