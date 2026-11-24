"""Part 5 brain worker: the brain side of the feeding closed loop.

Runs in the BRAIN environment (Brian2 2.9.0 / numpy 1.26.4). The
driver (run_loop5.py, body environment) spawns this process and talks
to it over stdin/stdout using the JSON-lines contract in
loop_protocol.py. stdout carries protocol lines only; diagnostics go
to stderr.

What it does: builds ONE frozen Part 2 Brain (ctb, used exactly as
shipped -- no frozen file is modified), adds a Poisson drive for every
population the scenario declares (SS2.2: every drivable population is
declared up front, in the start message, before the episode clock),
and holds ONE persistent Brian2 Network over the Brain's objects --
Brain.run() builds a fresh Network per call and Brian2 2.9 refuses to
re-add already-simulated objects, so the bridge pattern Part 2b proved
is used unchanged.

Per chunk message, the worker:
  1. computes each declared drive's gating state from the scenario
     (loop_protocol.gate_state: the SS4.5 taste-event state carried by
     the message -- the event state at the end of the PREVIOUS body
     chunk, SS2.1's exactly-one-chunk latency -- combined with the
     scenario's scripted window per the drive's mode);
  2. sets the drives' `active` flags accordingly (drives change only
     at chunk boundaries -- the SS2.2 harness rule);
  3. runs the network for the chunk's duration;
  4. replies with the spike counts of the declared readouts in the
     chunk's window and the full applied-state record (both gates and
     the applied flag, per drive), so the run manifest can show which
     gate did what in every chunk.

Compile warmup (SS2.2): Brian2 compiles each drive's code object the
first time that drive is ACTIVE; Part 2b measured ~10 minutes of gcc
when 146 JON drives were first activated mid-episode. The worker
therefore performs a zero-duration run with ALL declared drives active
before the first timed chunk, paying every compile cost outside the
episode. It advances no simulated time.
"""

import sys
import time
from pathlib import Path

import numpy as np
from brian2 import Hz, Network, ms

HERE = Path(__file__).resolve()
PART5 = HERE.parent
REPO = HERE.parents[2]              # repo/fresh/part5/x.py -> repo root
sys.path.insert(0, str(REPO / "fresh"))   # for ctb
sys.path.insert(0, str(PART5))            # for loop_protocol

import loop_protocol as protocol  # noqa: E402
from ctb.brain.model import Brain                      # noqa: E402
from ctb.data.loader import load_connectome, load_populations  # noqa: E402

DATA_DIR = REPO / "data"
ID_SETS = REPO / "fresh" / "part2" / "id_sets_v1"


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
        self.scenario = None
        self.drive_inputs = {}      # drive name -> [PoissonInput, ...]
        self.elapsed_ms = 0

    def start(self, message):
        t0 = time.time()
        scenario = protocol.validate_scenario(message["scenario"])
        self.scenario = scenario
        self.data = load_connectome(DATA_DIR)
        self.pops = load_populations(ID_SETS, self.data)
        self.ids_of = {name: [int(x) for x in self.data.ids[idx]]
                       for name, idx in self.pops.items()}
        brain = Brain(self.data, seed=scenario["seed"])
        brain.build()
        # SS2.2: every declared drive is added now, before any chunk,
        # and held inactive until its gate first applies it.
        for entry in scenario["drives"]:
            inputs = []
            for pop in entry["populations"]:
                inputs.extend(brain.add_drive(
                    self.ids_of[pop], entry["rate_hz"] * Hz))
            for d in inputs:
                d.active = False
            self.drive_inputs[entry["name"]] = inputs
        self.brain = brain
        self.net = Network(brain.neurons, brain.synapses, brain.monitor,
                           *brain._drives)
        # Compile warmup: zero-duration run, all declared drives
        # active (SS2.2). Advances no simulated time.
        for inputs in self.drive_inputs.values():
            for d in inputs:
                d.active = True
        self.net.run(0 * ms)
        for inputs in self.drive_inputs.values():
            for d in inputs:
                d.active = False
        log(f"worker ready: build + compile warmup took "
            f"{time.time() - t0:.1f} s")
        send({"type": "ready",
              "populations": {name: int(len(idx))
                              for name, idx in self.pops.items()},
              "data_hashes": dict(self.data.file_hashes),
              "declared_drives": scenario["drives"],
              "readouts": scenario["readouts"]})

    def counts_in_window(self, t0, t1):
        idx, t = self.brain.spikes()
        sel = idx[(t >= t0) & (t < t1)]
        counts = {}
        for name in self.scenario["readouts"]:
            if name == "total":
                counts[name] = int(len(sel))
            elif name == "mn9_left":
                counts[name] = int((sel == self.pops["mn9"][0]).sum())
            elif name == "mn9_right":
                counts[name] = int((sel == self.pops["mn9"][1]).sum())
            else:
                counts[name] = int(np.isin(sel, self.pops[name]).sum())
        return counts

    def chunk(self, message):
        if self.net is None:
            raise RuntimeError("chunk received before start")
        k = int(message["chunk"])
        taste_event = bool(message["taste_event"])
        applied = {}
        for entry in self.scenario["drives"]:
            state = protocol.gate_state(entry["mode"], k, taste_event,
                                        entry["window"])
            applied[entry["name"]] = state
            for d in self.drive_inputs[entry["name"]]:
                d.active = state["applied"]
        duration_ms = int(message["duration_ms"])
        t0 = self.elapsed_ms / 1000.0
        self.net.run(duration_ms * ms)
        self.elapsed_ms += duration_ms
        t1 = self.elapsed_ms / 1000.0
        send({"type": "counts", "chunk": k,
              "counts": self.counts_in_window(t0, t1),
              "applied": applied,
              "taste_event_received": taste_event,
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
