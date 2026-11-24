"""Part 2b closed-loop driver: one episode of brain -> body -> brain.

Runs in the BODY environment (FlyGym / MuJoCo / numpy 2.5.5) and spawns
brain_worker.py in the brain environment as a subprocess; the two speak
the JSON-lines contract in protocol.py. One episode:

  for each 100 ms chunk of simulated time:
    1. BRAIN  -- the worker runs the frozen brain for one chunk, with
       the sugar drive on (200 Hz, the Part 3 protocol) and the JON
       mechanosensory drive on or off as this chunk's sensory state
       dictates; it returns the readout spike counts for the chunk.
    2. DECODE -- the toy decoder (decoder.py) turns the pooled
       aDN1 + aDN2-left count into the body's descending 2-vector.
    3. BODY   -- the audited Part 1b pathway (HybridTurningController ->
       CPG -> preprogrammed steps) steps the NeuroMechFly body for the
       same 100 ms of physics, under that signal.
    4. SENSE  -- leg ground-contact flags are watched at every physics
       step; contact transitions in this body chunk set the sensory
       state for the NEXT brain chunk (sensory.py). Feedback latency is
       therefore exactly one chunk (100 ms simulated), plus the decoder
       filter's lag -- both stated here, not hidden.

Sensory state for a chunk is ON if any of these holds:
  - the chunk is one of the scripted TOUCH PULSE chunks (default 2-3,
    t = 0.2-0.4 s): a single encoder-side stimulus event at the start of
    the episode, labelled scripted/constructed -- the analogue of
    switching the sugar stimulus on, and the bootstrap that gives the
    contact-feedback loop something to sustain;
  - mode is "closed" and the previous body chunk contained at least one
    contact transition (the feedback path).
In mode "open" the feedback path is logged but never connected: the
control episode that shows whether the loop, rather than the pulse,
sustains the walking.

Brain and body chunks have the same simulated duration but run
sequentially in wall-clock (a brain chunk costs ~10 s of compute, a
body chunk ~1 s). Wall-clock latency is not part of the simulated
system and is reported only as a cost figure.

Usage:
  python run_loop.py --mode closed --seed 4200 --out runs/ep_closed_4200.json
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
PART2B = HERE.parent
REPO = HERE.parents[2]                    # repo/fresh/part2b -> repo root
WORKSPACE = REPO.parent                   # connectome-work/
BRAIN_PYTHON = WORKSPACE / "envs" / "brain" / "bin" / "python"
WORKER = PART2B / "brain_worker.py"
sys.path.insert(0, str(PART2B))

import protocol  # noqa: E402
from decoder import ToyDecoder  # noqa: E402
from sensory import ContactTransitions  # noqa: E402

from flygym.compose.world.flat_ground import FlatGroundWorld  # noqa: E402
from flygym.simulation import Simulation  # noqa: E402
from flygym.utils.math import Rotation3D  # noqa: E402
from flygym_demo.complex_terrain import (  # noqa: E402
    HybridControllerObservation,
    HybridTurningController,
    apply_locomotion_action,
    make_locomotion_fly,
)

FLY_NAME = "nmf"
CHUNK_MS = 100
N_CHUNKS = 20
PULSE_CHUNKS = (2, 3)
SUGAR_RATE_HZ = 200.0
JON_RATE_HZ = 150.0


class BrainLink:
    """The driver side of the protocol: owns the worker subprocess."""

    def __init__(self, seed, sugar_rate_hz, jon_rate_hz, worker_log):
        self.proc = subprocess.Popen(
            [str(BRAIN_PYTHON), str(WORKER)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=worker_log, text=True, bufsize=1)
        self._send(protocol.make_start(seed, sugar_rate_hz, jon_rate_hz))
        reply = self._read()
        if reply.get("type") != "ready":
            raise RuntimeError(f"worker did not become ready: {reply!r}")

    def _send(self, message):
        self.proc.stdin.write(protocol.dumps_line(message))
        self.proc.stdin.flush()

    def _read(self):
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("brain worker closed its output "
                               "(see the worker log)")
        return protocol.loads_line(line)

    def chunk(self, chunk, duration_ms, jon_on):
        self._send(protocol.make_chunk(chunk, duration_ms, jon_on))
        return protocol.validate_counts_reply(self._read(), chunk)

    def close(self):
        try:
            self._send(protocol.make_end())
            self._read()
        finally:
            self.proc.wait(timeout=60)


def _finite(*arrays):
    return all(bool(np.all(np.isfinite(a))) for a in arrays)


def run_episode(mode, seed, out_path):
    chunk_s = CHUNK_MS / 1000.0
    wall0 = time.time()

    fly = make_locomotion_fly(name=FLY_NAME)
    world = FlatGroundWorld()
    world.add_fly(fly, (0, 0, 0.8), Rotation3D("quat", (1, 0, 0, 0)))
    sim = Simulation(world)
    sim.reset()
    sim.warmup(0.05)
    controller = HybridTurningController(timestep=sim.timestep)
    thorax_idx = [s.name for s in fly.get_bodysegs_order()].index("c_thorax")
    steps_per_chunk = int(round(chunk_s / sim.timestep))

    def contact_flags():
        contact, *_ = sim.get_ground_contact_info(FLY_NAME)
        flags = np.asarray(contact).reshape(-1)
        if len(flags) != 6:
            raise RuntimeError(f"expected 6 leg contact flags, "
                               f"got {len(flags)}")
        return [bool(f) for f in flags]

    def thorax_xyz():
        return np.asarray(sim.get_body_positions(FLY_NAME)[thorax_idx],
                          dtype=float)

    transitions = ContactTransitions(n_legs=6)
    transitions.set_baseline(contact_flags())

    worker_log = open(out_path.with_suffix(".worker.log"), "w")
    link = BrainLink(seed, SUGAR_RATE_HZ, JON_RATE_HZ, worker_log)
    decoder = ToyDecoder()

    records = []
    pending_feedback = False
    prev_xy = thorax_xyz()[:2]
    try:
        for k in range(N_CHUNKS):
            pulse = k in PULSE_CHUNKS
            jon_on = pulse or (mode == "closed" and pending_feedback)
            jon_source = ("pulse" if pulse else
                          "feedback" if jon_on else "off")
            counts = link.chunk(k, CHUNK_MS, jon_on)
            dn_count = counts["adn1"] + counts["adn2_left"]
            amplitude, rate_inst, rate_ema = decoder.update(dn_count,
                                                            chunk_s)
            signal = np.array([amplitude, amplitude])

            chunk_transitions = 0
            for _ in range(steps_per_chunk):
                obs = HybridControllerObservation.from_sim(sim, FLY_NAME)
                action = controller.step(signal, obs)
                apply_locomotion_action(sim, FLY_NAME, action)
                sim.step()
                chunk_transitions += transitions.update(contact_flags())
            pos = thorax_xyz()
            travel = float(np.linalg.norm(pos[:2] - prev_xy))
            prev_xy = pos[:2]
            angles = sim.get_joint_angles(FLY_NAME)
            if isinstance(angles, dict):
                angles = np.array(list(angles.values()), dtype=float)
            finite = _finite(pos, np.asarray(angles, dtype=float))
            records.append({
                "chunk": k, "t_s": [k * chunk_s, (k + 1) * chunk_s],
                "jon_on": jon_on, "jon_source": jon_source,
                "counts": counts, "dn_count": dn_count,
                "dn_rate_inst_hz": rate_inst, "dn_rate_ema_hz": rate_ema,
                "amplitude": amplitude, "travel_mm": travel,
                "thorax_z_mm": float(pos[2]),
                "contact_transitions": chunk_transitions,
                "finite": finite,
            })
            pending_feedback = chunk_transitions > 0
    finally:
        link.close()
        worker_log.close()
        sim.close()

    travels = np.array([r["travel_mm"] for r in records])
    amps = np.array([r["amplitude"] for r in records])
    summary = {
        "completed_chunks": len(records),
        "all_finite": bool(all(r["finite"] for r in records)),
        "thorax_z_min_mm": float(min(r["thorax_z_mm"] for r in records)),
        "thorax_z_max_mm": float(max(r["thorax_z_mm"] for r in records)),
        "total_travel_mm": float(travels.sum()),
        "travel_signal_on_chunks_mm": float(
            travels[amps >= 0.8].sum()) if (amps >= 0.8).any() else 0.0,
        "travel_signal_off_chunks_mm": float(
            travels[amps <= 0.05].sum()) if (amps <= 0.05).any() else 0.0,
        "jon_spikes_feedback_chunks": int(sum(
            r["counts"]["jon_all"] for r in records
            if r["jon_source"] == "feedback")),
        "jon_spikes_off_chunks": int(sum(
            r["counts"]["jon_all"] for r in records
            if r["jon_source"] == "off")),
        "wall_clock_s": round(time.time() - wall0, 1),
    }
    episode = {
        "part": "2b", "mode": mode, "seed": seed,
        "config": {"chunk_ms": CHUNK_MS, "n_chunks": N_CHUNKS,
                   "pulse_chunks": list(PULSE_CHUNKS),
                   "sugar_rate_hz": SUGAR_RATE_HZ,
                   "jon_rate_hz": JON_RATE_HZ,
                   "decoder": "toy (decoder.py): pooled aDN1+aDN2-left "
                              "rate, EMA tau=0.2 s, ramp 2->40 Hz",
                   "sensory": "contact transitions in body chunk k -> "
                              "JON drive in brain chunk k+1 "
                              "(provisional/constructed)"},
        "chunks": records, "summary": summary,
    }
    out_path.write_text(json.dumps(episode, indent=2))
    print(f"[{mode} seed={seed}] " +
          " ".join(f"{k}={v}" for k, v in summary.items()), flush=True)
    return episode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("closed", "open"), required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    run_episode(args.mode, args.seed, args.out)


if __name__ == "__main__":
    main()
