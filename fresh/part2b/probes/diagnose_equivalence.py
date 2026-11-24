"""Diagnostic for the chunk-equivalence re-check (gate condition 4).

The hash re-check (verify_chunk_equivalence.py) did NOT reproduce
probe 2 as recorded: in a fresh process, the single 300 ms run gave
5,539 spikes and the chunked 3 x 100 ms run gave 5,243 -- and 5,243
is exactly probe 2's recorded count for BOTH. In probe 2's process,
the "single" build was the second Brain build of the process (probe 1
had built one before it); in the re-check it was the first. This
diagnostic separates build order from run structure:

  process A (this script, mode A): builds in order
      #1 single, #2 single, #3 chunked, #4 chunked   (all seed 4105)
  process B (mode B): build #1 chunked only.

Comparisons that decide the question:
  A#2 vs A#3 -- warm-build single vs chunked (probe 2's effective
      comparison, if build order is the confound);
  A#1 vs B#1 -- first-build single vs first-build chunked (the
      bridge's actual situation: the worker is a fresh process whose
      only build is run chunked);
  A#1 vs A#2 and A#3 vs A#4 -- same-structure reproducibility across
      build order.

Same canonicalisation as the re-check: (root ID, time) sorted by
(time, root ID), SHA-256 over int64 IDs bytes + float64 times bytes.
Output: diagnose_equivalence_<mode>.json next to this script.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
from brian2 import Hz, Network, ms

HERE = Path(__file__).resolve()
DIR = HERE.parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "fresh"))

from ctb.brain.model import Brain                      # noqa: E402
from ctb.data.loader import load_connectome, load_populations  # noqa: E402

DATA_DIR = REPO / "data"
ID_SETS = REPO / "fresh" / "part2" / "id_sets_v1"
SEED = 4105

mode = sys.argv[1] if len(sys.argv) > 1 else "A"
plans = {"A": [("single", [300]), ("single", [300]),
               ("chunked", [100, 100, 100]), ("chunked", [100, 100, 100])],
         "B": [("chunked", [100, 100, 100])]}[mode]

print("loading connectome (hash-verified)...", flush=True)
data = load_connectome(DATA_DIR)
pops = load_populations(ID_SETS, data)
sugar_ids = [int(x) for x in data.ids[pops["sugar_grn_right"]]]

results = []
t0 = time.time()
for n, (label, chunk_list) in enumerate(plans, start=1):
    b = Brain(data, seed=SEED)
    b.build()
    b.add_drive(sugar_ids, 200 * Hz)
    net = Network(b.neurons, b.synapses, b.monitor, *b._drives)
    for c in chunk_list:
        net.run(c * ms)
    idx, t = b.spikes()
    root_ids = np.asarray(data.ids[np.asarray(idx)], dtype=np.int64)
    times = np.asarray(t, dtype=np.float64)
    order = np.lexsort((root_ids, times))
    digest = hashlib.sha256(root_ids[order].tobytes()
                            + times[order].tobytes()).hexdigest()
    entry = {"build_number_in_process": n, "structure": label,
             "spikes": int(len(root_ids)), "sha256": digest}
    results.append(entry)
    print(f"  build #{n} {label}: {entry['spikes']} spikes "
          f"sha256={digest}", flush=True)

out = {"mode": mode, "seed": SEED, "builds": results,
       "wall_clock_s": round(time.time() - t0, 1)}
(DIR / f"diagnose_equivalence_{mode}.json").write_text(
    json.dumps(out, indent=2))
print(json.dumps(out, indent=2), flush=True)
