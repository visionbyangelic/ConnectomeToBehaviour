"""Part 2b gate-condition re-check: chunk equivalence, verified by hash.

Why this exists: the original probe (probe_brain_mechanisms.py, probe 2)
compared the single-run and chunked-run spike trains with
numpy.array_equal in memory and recorded only the spike COUNTS plus a
boolean in probe_results.json -- the trains themselves were never
archived, so the archived record, read strictly, rests on
5,243 = 5,243. Reviewer 1's Part 2b gate condition (4) asks for the
trains to be verified by neuron ID and spike time, or hashed, before
the "bit-for-bit" claim stands. This script does exactly that, and
archives both trains.

Method: probe 2's exact configuration (seed 4105, sugar GRNs right at
200 Hz, 300 ms; one build run as a single 300 ms run, one as three
100 ms runs on one persistent Network over the frozen Brain's objects).
For each train: take (neuron index, spike time) from the monitor, map
indices to FlyWire root IDs, sort canonically by (time, root ID), and
serialise as the raw bytes of the sorted int64 ID array followed by
the raw bytes of the sorted float64 time array. SHA-256 of that byte
string is the train's fingerprint. The trains are also compared
element-wise (counts, every ID in canonical order, max |time
difference|), and both canonical trains are saved as .npz next to
this script so the comparison can be re-done without re-running.

Outputs: equivalence_verification.json + the two .npz trains, here.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
from brian2 import Hz, Network, ms

HERE = Path(__file__).resolve()
DIR = HERE.parent                 # the probes directory
REPO = HERE.parents[3]            # repo/src/first_loop/probes -> repo root
sys.path.insert(0, str(REPO / "src"))

from brain_model.brain.model import Brain                      # noqa: E402
from brain_model.data.loader import load_connectome, load_populations  # noqa: E402

DATA_DIR = REPO / "data"
ID_SETS = REPO / "data" / "neuron_sets"
SEED = 4105                       # probe 2's seed -- same configuration

print("loading connectome (hash-verified)...", flush=True)
data = load_connectome(DATA_DIR)
pops = load_populations(ID_SETS, data)
sugar_ids = [int(x) for x in data.ids[pops["sugar_grn_right"]]]


def persistent_net(brain):
    return Network(brain.neurons, brain.synapses, brain.monitor,
                   *brain._drives)


def canonical_train(brain):
    """(root IDs, times) sorted by (time, root ID), plus SHA-256."""
    idx, t = brain.spikes()
    root_ids = np.asarray(data.ids[np.asarray(idx)], dtype=np.int64)
    times = np.asarray(t, dtype=np.float64)
    order = np.lexsort((root_ids, times))
    ids_sorted = root_ids[order]
    t_sorted = times[order]
    digest = hashlib.sha256(ids_sorted.tobytes()
                            + t_sorted.tobytes()).hexdigest()
    return ids_sorted, t_sorted, digest


trains = {}
t0 = time.time()
for label, chunk_list in (("single", [300]), ("chunked", [100, 100, 100])):
    print(f"building + running '{label}' {chunk_list} ms...", flush=True)
    b = Brain(data, seed=SEED)
    b.build()
    b.add_drive(sugar_ids, 200 * Hz)
    net = persistent_net(b)
    for c in chunk_list:
        net.run(c * ms)
    ids_sorted, t_sorted, digest = canonical_train(b)
    np.savez_compressed(DIR / f"equivalence_train_{label}.npz",
                        root_ids=ids_sorted, times_s=t_sorted)
    trains[label] = {"ids": ids_sorted, "t": t_sorted, "sha256": digest}
    print(f"  {label}: {len(ids_sorted)} spikes, sha256={digest}",
          flush=True)

a, b_ = trains["single"], trains["chunked"]
same_count = len(a["ids"]) == len(b_["ids"])
same_ids = bool(same_count and np.array_equal(a["ids"], b_["ids"]))
max_dt = (float(np.max(np.abs(a["t"] - b_["t"])))
          if same_count else None)
same_times_exact = bool(same_count and np.array_equal(a["t"], b_["t"]))
verdict = {
    "seed": SEED,
    "configuration": "sugar_grn_right at 200 Hz, 300 ms total; "
                     "single = one 300 ms run, chunked = 3 x 100 ms "
                     "runs on one persistent Network (probe 2's setup)",
    "spikes_single": int(len(a["ids"])),
    "spikes_chunked": int(len(b_["ids"])),
    "sha256_single": a["sha256"],
    "sha256_chunked": b_["sha256"],
    "hashes_equal": bool(a["sha256"] == b_["sha256"]),
    "elementwise_ids_equal": same_ids,
    "elementwise_times_exactly_equal": same_times_exact,
    "max_abs_time_difference_s": max_dt,
    "bit_for_bit_identical": bool(a["sha256"] == b_["sha256"]
                                  and same_ids and same_times_exact),
    "wall_clock_s": round(time.time() - t0, 1),
}
(DIR / "equivalence_verification.json").write_text(
    json.dumps(verdict, indent=2))
print(json.dumps(verdict, indent=2), flush=True)
