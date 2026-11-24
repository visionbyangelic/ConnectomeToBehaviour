"""Part 2b brain worker: the brain side of the brain<->body bridge.

Runs in the BRAIN environment (Brian2 / numpy 1.26.4). The body-side
driver (run_loop.py, body environment) spawns this process and talks to
it over stdin/stdout using the JSON-lines contract in protocol.py.
stdout carries protocol lines only; diagnostics go to stderr.

What it does: builds ONE frozen Part 2 Brain (brain_model, used exactly as
shipped -- no frozen file is modified), adds the sugar drive (200 Hz,
the Part 3-validated protocol, on for the whole episode) and the JON
mechanosensory drive (added once, then switched off/on per chunk via
the PoissonInputs' `active` flag), and holds ONE persistent Brian2
Network over the Brain's objects. Each "chunk" message runs the network
for one chunk of simulated time and returns the spike counts of the
readout populations in that chunk's window.

Why a persistent Network instead of Brain.run(): Brain.run() builds a
fresh Network on every call, and Brian2 2.9 refuses to add
already-simulated objects to a new Network (RuntimeError). The bridge
therefore builds its Network once from the same objects Brain.run()
would use -- neurons, synapses, monitor, drives -- and runs it in
chunks. The Part 2b probes verified on the record that (a) the `active`
toggle silences/restores the JON drive exactly, and (b) chunked running
on one Network reproduces the single-run spike train bit for bit, so
the chunking is scaffolding, not a model change.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
from brian2 import Hz, Network, ms

HERE = Path(__file__).resolve()
PART2B = HERE.parent
REPO = HERE.parents[2]              # repo/src/first_loop -> repo root
sys.path.insert(0, str(REPO / "src"))   # for brain_model
sys.path.insert(0, str(PART2B))           # for protocol

import protocol  # noqa: E402
from brain_model.brain.model import Brain                      # noqa: E402
from brain_model.data.loader import load_connectome, load_populations  # noqa: E402

DATA_DIR = REPO / "data"
ID_SETS = REPO / "data" / "neuron_sets"
READOUTS = ("adn1", "adn2_left", "abn1", "jon_all", "sugar_grn_right")


def log(*args):
    print(*args, file=sys.stderr, flush=True)


def send(message):
    sys.stdout.write(protocol.dumps_line(message))
    sys.stdout.flush()


class Worker:
    def __init__(self):
        self.data = None
        self.pops = None
        self.ids_of = None
        self.brain = None
        self.net = None
        self.jon_drives = []
        self.elapsed_ms = 0

    def start(self, message):
        t0 = time.time()
        self.data = load_connectome(DATA_DIR)
        self.pops = load_populations(ID_SETS, self.data)
        self.ids_of = {name: [int(x) for x in self.data.ids[idx]]
                       for name, idx in self.pops.items()}
        brain = Brain(self.data, seed=int(message["seed"]))
        brain.build()
        # Sugar: the validated stimulus, on for the whole episode.
        brain.add_drive(self.ids_of["sugar_grn_right"],
                        float(message["sugar_rate_hz"]) * Hz)
        # JON: the sensory-return channel. Added once, held inactive,
        # switched per chunk by the driver (see protocol.py).
        self.jon_drives = brain.add_drive(
            self.ids_of["jon_all"], float(message["jon_rate_hz"]) * Hz)
        for d in self.jon_drives:
            d.active = False
        self.brain = brain
        self.net = Network(brain.neurons, brain.synapses, brain.monitor,
                           *brain._drives)
        # Compile warmup: Brian2 generates and compiles each drive's
        # code object at the first run in which that drive is ACTIVE
        # (measured in the Part 2b probes: activating 146 JON drives
        # mid-episode cost ~10 min of gcc, once, then cached on disk).
        # A zero-duration run with every drive active pays that cost
        # here, before the episode clock starts, instead of inside a
        # timed chunk. It advances no simulated time.
        for d in self.jon_drives:
            d.active = True
        self.net.run(0 * ms)
        for d in self.jon_drives:
            d.active = False
        log(f"worker ready: build + compile warmup took "
            f"{time.time() - t0:.1f} s")
        send({"type": "ready",
              "populations": {name: int(len(idx))
                              for name, idx in self.pops.items()}})

    def counts_in_window(self, t0, t1):
        idx, t = self.brain.spikes()
        sel = idx[(t >= t0) & (t < t1)]
        counts = {"total": int(len(sel))}
        for name in READOUTS:
            counts[name] = int(np.isin(sel, self.pops[name]).sum())
        counts["mn9_left"] = int((sel == self.pops["mn9"][0]).sum())
        counts["mn9_right"] = int((sel == self.pops["mn9"][1]).sum())
        return counts

    def chunk(self, message):
        if self.net is None:
            raise RuntimeError("chunk received before start")
        jon_on = bool(message["jon_on"])
        for d in self.jon_drives:
            d.active = jon_on
        duration_ms = int(message["duration_ms"])
        t0 = self.elapsed_ms / 1000.0
        self.net.run(duration_ms * ms)
        self.elapsed_ms += duration_ms
        t1 = self.elapsed_ms / 1000.0
        send({"type": "counts", "chunk": int(message["chunk"]),
              "counts": self.counts_in_window(t0, t1),
              "t0_s": t0, "t1_s": t1})


def main():
    worker = Worker()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = protocol.loads_line(line)
            if message["type"] == "start":
                worker.start(message)
            elif message["type"] == "chunk":
                worker.chunk(message)
            elif message["type"] == "end":
                send({"type": "bye"})
                return 0
            else:
                raise ValueError(f"unknown message type "
                                 f"{message['type']!r}")
        except Exception as exc:  # fail loudly, never silently
            log(f"worker error: {exc!r}")
            try:
                send({"type": "error", "message": f"{type(exc).__name__}: "
                                                  f"{exc}"})
            finally:
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
