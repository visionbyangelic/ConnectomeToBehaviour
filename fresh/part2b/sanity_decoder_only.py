"""Part 2b decoder-only sanity run: brain disconnected, synthetic rates in.

The plan's Part 2b pass criteria require this run to exist and be
documented, so that decoder+body behaviour is never confused with brain
behaviour: everything the body does here is caused by the numbers I type
into the decoder, and by nothing else.

Synthetic pooled-DN rates, one 100 ms chunk at a time (the same cadence
as the closed loop), in four phases:

  A  0 Hz  for 1.0 s -- expect amplitude 0 and no travel (zero in, zero out)
  B 20 Hz  for 1.0 s -- mid-ramp rate: graded, partial command
  C 60 Hz  for 1.0 s -- above saturation: full command, full walking speed
  D  0 Hz  for 0.6 s -- command removed: the fly must halt, on the
                        timescale the Part 1b audit measured (~0.2 s)

Writes runs/sanity_decoder_only.json with per-chunk records.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
PART2B = HERE.parent
sys.path.insert(0, str(PART2B))

from decoder import ToyDecoder  # noqa: E402

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
CHUNK_S = 0.1
PHASES = [("A_zero", 0.0, 1.0), ("B_mid", 20.0, 1.0),
          ("C_full", 60.0, 1.0), ("D_halt", 0.0, 0.6)]
OUT = PART2B / "runs" / "sanity_decoder_only.json"


def main():
    wall0 = time.time()
    fly = make_locomotion_fly(name=FLY_NAME)
    world = FlatGroundWorld()
    world.add_fly(fly, (0, 0, 0.8), Rotation3D("quat", (1, 0, 0, 0)))
    sim = Simulation(world)
    sim.reset()
    sim.warmup(0.05)
    controller = HybridTurningController(timestep=sim.timestep)
    thorax_idx = [s.name for s in fly.get_bodysegs_order()].index("c_thorax")
    steps_per_chunk = int(round(CHUNK_S / sim.timestep))

    def thorax_xy():
        return np.asarray(sim.get_body_positions(FLY_NAME)[thorax_idx],
                          dtype=float)[:2]

    decoder = ToyDecoder()
    records = []
    prev_xy = thorax_xy()
    k = 0
    for phase_name, rate_hz, seconds in PHASES:
        for _ in range(int(round(seconds / CHUNK_S))):
            count = int(round(rate_hz * CHUNK_S))
            amplitude, rate_inst, rate_ema = decoder.update(count,
                                                            CHUNK_S)
            signal = np.array([amplitude, amplitude])
            for _ in range(steps_per_chunk):
                obs = HybridControllerObservation.from_sim(sim, FLY_NAME)
                action = controller.step(signal, obs)
                apply_locomotion_action(sim, FLY_NAME, action)
                sim.step()
            pos = thorax_xy()
            records.append({
                "chunk": k, "phase": phase_name,
                "synthetic_rate_hz": rate_hz, "synthetic_count": count,
                "amplitude": amplitude, "rate_ema_hz": rate_ema,
                "travel_mm": float(np.linalg.norm(pos - prev_xy)),
            })
            prev_xy = pos
            k += 1
    sim.close()

    by_phase = {}
    for phase_name, _, _ in PHASES:
        rows = [r for r in records if r["phase"] == phase_name]
        by_phase[phase_name] = {
            "travel_total_mm": float(sum(r["travel_mm"] for r in rows)),
            "amplitude_last_chunk": rows[-1]["amplitude"],
            "travel_last_0.3s_mm": float(
                sum(r["travel_mm"] for r in rows[-3:])),
        }
    result = {"part": "2b", "run": "decoder-only sanity (synthetic rates)",
              "phases": by_phase, "chunks": records,
              "wall_clock_s": round(time.time() - wall0, 1)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2))
    for name, s in by_phase.items():
        print(f"{name}: travel={s['travel_total_mm']:.3f} mm, "
              f"final amplitude={s['amplitude_last_chunk']:.3f}, "
              f"travel in last 0.3 s={s['travel_last_0.3s_mm']:.3f} mm",
              flush=True)
    print(f"wrote {OUT}", flush=True)


if __name__ == "__main__":
    main()
