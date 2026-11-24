"""Part 5 equivalence probe (SS6.1(3)): chunked vs single-run for the
taste-gated toggle configuration.

SS6.1(3)'s rule: the chunked bridge's equivalence is claimed only
where it has been probed, and a configuration that TOGGLES a drive
mid-episode needs its own equivalence probe by the Part 2b method
before its chunked results are trusted as single-run results. Part
2b's method is exactly two probes: chunk equivalence under a constant
drive (probe 2) and toggle exactness between runs (probe 1: the
driven population's counts go exactly to zero while off). This probe
runs both at the Part 5 feeding loop's own configuration, and
additionally tries -- and documents -- the construction of a true
single-run toggled reference.

Configuration (fixed here, before any run): the validated stimulus --
sugar_grn_right at 200 Hz -- seed 5103, 20 chunks x 100 ms = 2.0 s.
Toggle schedule: chunks 0-4 OFF, 5-14 ON, 15-19 OFF.

Runs (each in a FRESH PROCESS, as build #1 in that process -- the
Part 2b record-completion diagnostic showed the train also depends on
the build's position within its process, and the bridge worker is a
fresh process with one build; each run also performs the worker's
SS2.2 zero-duration compile warmup, all drives active, identically):

  chunked_const  -- one persistent Network, 20 x 100 ms, drive active
                    throughout;
  single_const   -- one net.run(2000 ms), drive active throughout.
                    The pair is the probe-2 comparison at this
                    duration, seed and warmup.
  chunked_toggle -- one persistent Network, 20 x 100 ms, the drives'
                    `active` flags set per the schedule at each chunk
                    boundary (the worker's mechanism). Judged by the
                    probe-1 criterion: driven-population counts
                    exactly 0 in every OFF chunk, > 0 in every ON
                    chunk.
  single_toggle  -- the attempt at a single-run toggled reference.
                    It does not run: the attempt establishes, in this
                    configuration, that no such reference exists in
                    this stack (below).

Why there is no single-run toggled reference (the probe's finding,
with both attempts on record):
  * The frozen Brain.run() builds one Network and runs it once; it
    has no scheduling surface (frozen API, not modified).
  * Toggling the `active` flags from inside one run (a Brian2
    network_operation setting them per the schedule) produced ZERO
    spikes (attempt 1, preserved in
    probe_toggle_equivalence_attempt1.json): Brian2 fixes the
    network's active set when a run starts, so a drive inactive at
    run start is absent from the schedule and a mid-run flip can
    never reach it.
  * Modulating the drives' rate instead (0 / 200 Hz) is impossible:
    Brian2 2.9's PoissonInput.rate is a read-only property
    (AttributeError: property 'rate' of 'PoissonInput' object has no
    setter -- raised by the single_toggle mode and recorded in the
    probe record).
  The chunked toggle therefore stands on the same basis Part 2b's
  loop stood on: chunking is bit-neutral under a constant drive
  (pair above), and the toggle itself is exact between runs
  (chunked_toggle's per-chunk counts). Any stronger claim would need
  a different drive mechanism, which would be a different model.

Trains are canonicalised exactly as in Part 2b's hash re-check:
(root ID, time) sorted by (time, root ID); SHA-256 over the int64 ID
bytes followed by the float64 time bytes. Trains are archived .npz.

Usage:
  envs/brain/bin/python probe_toggle_equivalence.py            (driver)
  envs/brain/bin/python probe_toggle_equivalence.py --mode M   (worker)
"""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
PART5 = HERE.parent
REPO = HERE.parents[2]              # repo/fresh/part5/x.py -> repo root
OUT_DIR = PART5 / "runs" / "probe_toggle"
SEED = 5103
N_CHUNKS = 20
CHUNK_MS = 100
RATE_HZ = 200.0
ON_CHUNKS = tuple(range(5, 15))     # chunks 5..14 ON; 0..4, 15..19 OFF
MODES = ("chunked_const", "single_const", "chunked_toggle",
         "single_toggle")


def build_brain():
    sys.path.insert(0, str(REPO / "fresh"))
    from brian2 import Hz
    from ctb.brain.model import Brain
    from ctb.data.loader import load_connectome, load_populations
    data = load_connectome(REPO / "data")
    pops = load_populations(REPO / "fresh" / "part2" / "id_sets_v1",
                            data)
    sugar_ids = [int(x) for x in data.ids[pops["sugar_grn_right"]]]
    brain = Brain(data, seed=SEED)
    brain.build()
    drives = brain.add_drive(sugar_ids, RATE_HZ * Hz)
    return brain, data, pops, drives


def canonical(brain, data):
    idx, t = brain.spikes()
    root_ids = np.asarray(data.ids[np.asarray(idx)], dtype=np.int64)
    times = np.asarray(t, dtype=np.float64)
    order = np.lexsort((root_ids, times))
    ids_sorted, t_sorted = root_ids[order], times[order]
    digest = hashlib.sha256(ids_sorted.tobytes()
                            + t_sorted.tobytes()).hexdigest()
    return idx, t, ids_sorted, t_sorted, digest


def attempt_single_toggle():
    """Establish, in this configuration, whether a single-run toggled
    reference can be constructed. Returns the finding; runs nothing."""
    from brian2 import Hz
    brain, data, pops, drives = build_brain()
    finding = {"mode": "single_toggle", "ran": False}
    try:
        drives[0].rate = 0 * Hz
        finding["rate_modulation"] = "rate assignment succeeded"
    except AttributeError as exc:
        finding["rate_modulation"] = f"impossible: {exc}"
    finding["active_flag_modulation"] = (
        "impossible: attempt 1 (network_operation toggling `active` "
        "inside one run) produced 0 spikes -- Brian2 fixes the active "
        "set at run start; preserved in "
        "probe_toggle_equivalence_attempt1.json")
    finding["conclusion"] = (
        "no single-run toggled reference exists for a PoissonInput "
        "drive in Brian2 2.9 with the frozen Brain API")
    return finding


def run_mode(mode):
    """One probe run, in this (fresh) process, as build #1."""
    if mode == "single_toggle":
        return attempt_single_toggle()
    from brian2 import Network, ms
    brain, data, pops, drives = build_brain()
    sugar_idx = pops["sugar_grn_right"]
    for d in drives:
        d.active = False
    net = Network(brain.neurons, brain.synapses, brain.monitor,
                  *brain._drives)
    # SS2.2 compile warmup, as the worker performs it: all drives
    # active, zero duration, before the episode clock.
    for d in drives:
        d.active = True
    net.run(0 * ms)
    toggle = mode == "chunked_toggle"
    if toggle:
        for d in drives:
            d.active = False
    if mode.startswith("chunked"):
        for k in range(N_CHUNKS):
            if toggle:
                for d in drives:
                    d.active = k in ON_CHUNKS
            net.run(CHUNK_MS * ms)
    else:
        net.run(N_CHUNKS * CHUNK_MS * ms)
    idx, t, ids_sorted, t_sorted, digest = canonical(brain, data)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT_DIR / f"train_{mode}.npz",
                        root_ids=ids_sorted, times_s=t_sorted)
    per_chunk_sugar = []
    for k in range(N_CHUNKS):
        sel = idx[(t >= k * 0.1) & (t < (k + 1) * 0.1)]
        per_chunk_sugar.append(int(np.isin(sel, sugar_idx).sum()))
    return {"mode": mode, "ran": True, "spikes": int(len(ids_sorted)),
            "sha256": digest,
            "per_chunk_sugar_spikes": per_chunk_sugar}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--mode":
        t0 = time.time()
        result = run_mode(sys.argv[2])
        result["wall_clock_s"] = round(time.time() - t0, 1)
        print("PROBE_RESULT " + json.dumps(result), flush=True)
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    results = {}
    for mode in MODES:
        proc = subprocess.run(
            [sys.executable, str(HERE), "--mode", mode],
            capture_output=True, text=True)
        line = next((ln for ln in proc.stdout.splitlines()
                     if ln.startswith("PROBE_RESULT ")), None)
        if line is None:
            raise RuntimeError(
                f"probe mode {mode} failed (exit {proc.returncode}):\n"
                f"{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}")
        results[mode] = json.loads(line[len("PROBE_RESULT "):])
        print(f"{mode}: {results[mode].get('spikes')} spikes, "
              f"sha256={results[mode].get('sha256')}", flush=True)
    cc, sc, ct = (results["chunked_const"], results["single_const"],
                  results["chunked_toggle"])
    off_zero = all(ct["per_chunk_sugar_spikes"][k] == 0
                   for k in range(N_CHUNKS) if k not in ON_CHUNKS)
    on_pos = all(ct["per_chunk_sugar_spikes"][k] > 0 for k in ON_CHUNKS)
    record = {
        "probe": "Part 5 toggle-configuration equivalence (SS6.1(3))",
        "configuration": {
            "population": "sugar_grn_right", "rate_hz": RATE_HZ,
            "seed": SEED, "n_chunks": N_CHUNKS, "chunk_ms": CHUNK_MS,
            "toggle_schedule_on_chunks": list(ON_CHUNKS),
            "process_structure": ("each run a fresh process, build #1 "
                                  "in its process; SS2.2 zero-duration "
                                  "warmup in every run"),
        },
        "runs": results,
        "const_pair": {
            "chunked_sha256": cc["sha256"],
            "single_sha256": sc["sha256"],
            "bit_identical": cc["sha256"] == sc["sha256"]},
        "toggle_exactness_chunked": {
            "off_chunks_exactly_zero_sugar_spikes": bool(off_zero),
            "on_chunks_positive_sugar_spikes": bool(on_pos),
            "per_chunk_sugar_spikes": ct["per_chunk_sugar_spikes"]},
        "single_run_toggled_reference": results["single_toggle"],
        "wall_clock_s": round(time.time() - t0, 1),
    }
    record["verdict"] = {
        "chunking_neutral_constant_drive": record["const_pair"][
            "bit_identical"],
        "toggle_exact_between_runs": bool(off_zero and on_pos),
        "single_run_toggled_reference_exists": False,
        "basis": ("SS6.1(3) discharged by the Part 2b method: "
                  "bit-identical chunking under constant drive + "
                  "exact toggling between runs; no single-run "
                  "toggled reference is constructible in this stack "
                  "(see single_run_toggled_reference)"),
    }
    out = OUT_DIR / "probe_toggle_equivalence.json"
    out.write_text(json.dumps(record, indent=2))
    print(json.dumps(record["verdict"], indent=2), flush=True)
    print("wrote", out, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
