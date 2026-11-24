"""Part 5 freeze, premise check P6: spike-table replay for one episode.

The loop protocol returns per-chunk spike COUNTS from the brain worker,
not the spike table itself. P6 (preregistration section 3) requires the
30-chunk arm (a) episode at seed 5699, run twice from fresh processes,
to produce bit-identical spike tables. This script is the second half
of that check: it rebuilds the worker's exact construction in this
process (same Brain seed, same declared drive, same zero-duration
all-active compile warmup, same chunked runs), applying the per-chunk
applied flags recorded in a finished run's brain_log.jsonl, then
canonicalises the full spike table exactly as the toggle-equivalence
probe does (root IDs and times sorted by (time, root ID); SHA-256 over
the int64 ID bytes followed by the float64 time bytes) and cross-checks
its per-chunk readout counts against the recorded ones.

Run twice from fresh processes against the same recorded run; the two
table hashes must be equal, and every chunk's counts must match.

Usage (brain env):
    python replay_spike_table.py --brain-log RUN/brain_log.jsonl \
        --scenario SCEN.json
Prints a JSON record with the spike-table SHA-256.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from brian2 import Hz, Network, ms

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(HERE))

import loop_protocol as protocol  # noqa: E402
from brain_model.brain.model import Brain  # noqa: E402
from brain_model.data.loader import load_connectome, load_populations  # noqa: E402

DATA_DIR = REPO / "data"
ID_SETS = REPO / "data" / "neuron_sets"


def canonical(brain, data):
    idx, t = brain.spikes()
    root_ids = np.asarray(data.ids[np.asarray(idx)], dtype=np.int64)
    times = np.asarray(t, dtype=np.float64)
    order = np.lexsort((root_ids, times))
    return hashlib.sha256(root_ids[order].tobytes()
                          + times[order].tobytes()).hexdigest(), len(times)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brain-log", required=True)
    ap.add_argument("--scenario", required=True)
    args = ap.parse_args()
    scenario = protocol.validate_scenario(
        json.loads(Path(args.scenario).read_text()))
    recorded = [json.loads(ln) for ln in
                Path(args.brain_log).read_text().splitlines() if ln.strip()]
    recorded = [r for r in recorded if r.get("type") == "counts"]
    recorded.sort(key=lambda r: r["chunk"])
    assert len(recorded) == scenario["n_chunks"], (
        f"recorded {len(recorded)} chunks, scenario {scenario['n_chunks']}")

    data = load_connectome(DATA_DIR)
    pops = load_populations(ID_SETS, data)
    ids_of = {name: [int(x) for x in data.ids[idx]] for name, idx in pops.items()}
    brain = Brain(data, seed=scenario["seed"])
    brain.build()
    drive_inputs = {}
    for entry in scenario["drives"]:
        inputs = []
        for pop in entry["populations"]:
            inputs.extend(brain.add_drive(ids_of[pop], entry["rate_hz"] * Hz))
        for d in inputs:
            d.active = False
        drive_inputs[entry["name"]] = inputs
    net = Network(brain.neurons, brain.synapses, brain.monitor, *brain._drives)
    for inputs in drive_inputs.values():
        for d in inputs:
            d.active = True
    net.run(0 * ms)
    for inputs in drive_inputs.values():
        for d in inputs:
            d.active = False

    mismatches = []
    elapsed_ms = 0
    for rec in recorded:
        k = rec["chunk"]
        for entry in scenario["drives"]:
            applied = bool(rec["applied"][entry["name"]]["applied"])
            for d in drive_inputs[entry["name"]]:
                d.active = applied
        t0 = elapsed_ms / 1000.0
        net.run(100 * ms)
        elapsed_ms += 100
        t1 = elapsed_ms / 1000.0
        idx, t = brain.spikes()
        sel = idx[(t >= t0) & (t < t1)]
        counts = {}
        for name in scenario["readouts"]:
            if name == "total":
                counts[name] = int(len(sel))
            elif name == "mn9_left":
                counts[name] = int((sel == pops["mn9"][0]).sum())
            elif name == "mn9_right":
                counts[name] = int((sel == pops["mn9"][1]).sum())
            else:
                counts[name] = int(np.isin(sel, pops[name]).sum())
        if counts != rec["counts"]:
            mismatches.append({"chunk": k, "replayed": counts,
                               "recorded": rec["counts"]})
    digest, n_spikes = canonical(brain, data)
    print(json.dumps({
        "seed": scenario["seed"], "n_chunks": scenario["n_chunks"],
        "spike_table_sha256": digest, "n_spikes": n_spikes,
        "count_mismatches": mismatches,
        "counts_match_recorded": not mismatches,
    }, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
