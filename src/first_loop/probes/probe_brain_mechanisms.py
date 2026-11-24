"""Part 2b mechanism probes -- run BEFORE the loop is built, on purpose.

Three questions the closed-loop design stands on, answered empirically:

1. TOGGLE + RECRUITMENT AT CHUNK SCALE. Can a PoissonInput added through
   the frozen Brain.add_drive be switched off and on between run() calls
   of ONE persistent Brian2 Network, and does the JON (mechanosensory)
   population, when driven, recruit the descending readouts aDN1 /
   aDN2-left within a single 100 ms chunk?
   Why one persistent Network: Brain.run() builds a fresh Network per
   call, and Brian2 2.9 forbids re-adding already-simulated objects to a
   new Network (RuntimeError, seen in my first toggle experiment). So the
   bridge holds one Network built from the frozen Brain's own objects
   (neurons, synapses, monitor, drives). The frozen code is used exactly
   as shipped and is not modified; only the run scaffolding is mine.
2. CHUNK EQUIVALENCE. Do three 100 ms runs on one Network give exactly
   the spike train of one 300 ms run, same seed, same drives? If
   chunking changed the dynamics, the chunked-loop design would be
   invalid and I would need a different bridge.
3. RECRUITMENT RATES. With the JON population driven continuously for
   1 s (no sugar), what do aDN1 / aDN2-left fire at, at 150 Hz drive
   (the upstream default rate) and at 200 Hz (the Part 3 rate)? Part 3's
   output already showed both DNs are silent under sugar alone (0 spikes
   in 30 trials), so the loop's walking signal stands or falls on this.

Outputs: probe_results.json next to this script + progress on stdout.
Seeds: 4102 (toggle), 4105 (equivalence), 4103/4104 (recruitment) --
the Part 2b probe seed block, recorded here before any of them ran.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
from brian2 import Hz, Network, ms

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]            # repo/src/first_loop/probes -> repo root
sys.path.insert(0, str(REPO / "src"))

from brain_model.brain.model import Brain                      # noqa: E402
from brain_model.data.loader import load_connectome, load_populations  # noqa: E402

DATA_DIR = REPO / "data"
ID_SETS = REPO / "data" / "neuron_sets"
OUT = HERE.parent / "probe_results.json"

results = {}
t_start = time.time()

print("loading connectome (hash-verified)...", flush=True)
data = load_connectome(DATA_DIR)
pops = load_populations(ID_SETS, data)
ids_of = {name: [int(x) for x in data.ids[idx]] for name, idx in pops.items()}
assert ids_of["mn9"][0] == 720575940660219265, "MN9[0] is not the left one"
assert ids_of["mn9"][1] == 720575940645521262, "MN9[1] is not the right one"
READOUTS = ["adn1", "adn2_left", "abn1", "jon_all", "sugar_grn_right"]


def counts_in_window(brain, t0, t1):
    """Spike counts per readout population in [t0, t1) seconds."""
    idx, t = brain.spikes()
    sel = idx[(t >= t0) & (t < t1)]
    out = {"total": int(len(sel))}
    for name in READOUTS:
        out[name] = int(np.isin(sel, pops[name]).sum())
    out["mn9_left"] = int((sel == pops["mn9"][0]).sum())
    out["mn9_right"] = int((sel == pops["mn9"][1]).sum())
    return out


def persistent_net(brain):
    """One Network over the frozen Brain's objects -- the bridge pattern."""
    return Network(brain.neurons, brain.synapses, brain.monitor,
                   *brain._drives)


# ----------------------------------------------------------------------
# Probe 1: toggle + chunk-scale recruitment (seed 4102)
# Sugar on throughout (200 Hz, the validated protocol). JON drive added
# but held inactive for chunk 1, active for chunk 2, inactive for chunk 3.
# ----------------------------------------------------------------------
print("probe 1: toggle, 3 x 100 ms...", flush=True)
brain = Brain(data, seed=4102)
brain.build()
brain.add_drive(ids_of["sugar_grn_right"], 200 * Hz)
jon_drives = brain.add_drive(ids_of["jon_all"], 150 * Hz)
for d in jon_drives:
    d.active = False
net = persistent_net(brain)
chunks = []
for k, jon_on in enumerate((False, True, False)):
    for d in jon_drives:
        d.active = jon_on
    net.run(100 * ms)
    c = counts_in_window(brain, 0.1 * k, 0.1 * (k + 1))
    c["jon_commanded_on"] = jon_on
    chunks.append(c)
    print(f"  chunk {k} (jon_on={jon_on}): {c}", flush=True)
results["probe1_toggle"] = {
    "seed": 4102,
    "chunks": chunks,
    "toggle_works": bool(chunks[0]["jon_all"] == 0
                         and chunks[1]["jon_all"] > 500
                         and chunks[2]["jon_all"] == 0),
}

# ----------------------------------------------------------------------
# Probe 2: chunk equivalence (seed 4105, sugar 200 Hz, 300 ms)
# ----------------------------------------------------------------------
print("probe 2: chunk equivalence, 2 builds x 300 ms...", flush=True)
trains = {}
for label, chunk_list in (("single", [300]), ("chunked", [100, 100, 100])):
    b = Brain(data, seed=4105)
    b.build()
    b.add_drive(ids_of["sugar_grn_right"], 200 * Hz)
    n = persistent_net(b)
    for c in chunk_list:
        n.run(c * ms)
    trains[label] = b.spikes()
same = (np.array_equal(trains["single"][0], trains["chunked"][0])
        and np.array_equal(trains["single"][1], trains["chunked"][1]))
results["probe2_chunk_equivalence"] = {
    "seed": 4105,
    "spikes_single": int(len(trains["single"][0])),
    "spikes_chunked": int(len(trains["chunked"][0])),
    "bit_identical": bool(same),
}
print(f"  single={len(trains['single'][0])} chunked="
      f"{len(trains['chunked'][0])} identical={same}", flush=True)

# ----------------------------------------------------------------------
# Probe 3: recruitment rates, JON only, 1 s, at 150 Hz and 200 Hz
# ----------------------------------------------------------------------
for rate_hz, seed in ((150, 4103), (200, 4104)):
    print(f"probe 3: JON recruitment at {rate_hz} Hz, 1 s...", flush=True)
    b = Brain(data, seed=seed)
    b.build()
    b.add_drive(ids_of["jon_all"], rate_hz * Hz)
    n = persistent_net(b)
    n.run(1000 * ms)
    c = counts_in_window(b, 0.0, 1.0)
    results[f"probe3_recruitment_{rate_hz}hz"] = {"seed": seed, "counts_1s": c}
    print(f"  {c}", flush=True)

results["wall_clock_s"] = round(time.time() - t_start, 1)
OUT.write_text(json.dumps(results, indent=2))
print(f"done in {results['wall_clock_s']} s -> {OUT}", flush=True)
