"""Q4, fifth execution (SS7.5), 24 Nov 2026.

The Q3 cycle (revised Pass 6 chain) repeated in 5 independent runs
(fresh Simulation instances, identical commands, identical pinned
artefact). Pass: across runs, per-cycle peak E has range <= 0.05 rad,
and event onset times (SS4.4: first chunk where E >= 0.10 rad and stays
>= 0.10 for >= 2 consecutive chunks; onset = that chunk's start,
cycle-relative) have range <= 100 ms (one chunk). Onsets are read from
chunk-sampled E -- resolution one chunk, per SS7.5's explicit statement.
"""

import json
import time
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import PITCH_JOINTS, PROBOSCIS, build_sim, dof_index, settle  # noqa: E402
from gate_common3 import RESULTS, compiled_params  # noqa: E402
from gate_common5 import theta_ext_from_params  # noqa: E402
from q3_rerun5 import run_cycles  # noqa: E402


def onset_chunk(E):
    """SS4.4 onset on chunk-sampled E (cycle-relative chunk indices)."""
    for k in range(len(E) - 1):
        if E[k] >= 0.10 and E[k + 1] >= 0.10:
            return k
    return None


def main():
    t0 = time.time()
    q3 = json.loads((RESULTS / "q3_rerun5.json").read_text())
    assert q3["verdict"] == "PASS", "Q3 did not pass; Q4 must not run"
    q2 = json.loads((RESULTS / "q2_rerun5.json").read_text())
    signs = {j: q2["joints"][j]["extension_sign_s"] for j in PITCH_JOINTS}

    runs = []
    for r in range(5):
        tw = time.time()
        fly, world, sim = build_sim(with_adhesion=True)
        idx, order = dof_index(fly)
        params = compiled_params(sim)
        theta_ext = theta_ext_from_params(params, signs)
        st = settle(sim, fly, np.zeros(len(order)))
        assert st["settled"], f"run {r + 1}: settle failed"
        rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
        chunks, max_exc, finite = run_cycles(sim, fly, idx, params, rest,
                                             signs, theta_ext, n_cycles=1)
        sim.close()
        cyc = chunks[5:45]
        E = [c["E_rad"] for c in cyc]
        oc = onset_chunk(E)
        runs.append({
            "run": r + 1,
            "settled": True,
            "peak_E_rad": float(max(E)),
            "onset_chunk_cycle_relative": oc,
            "onset_ms_from_cycle_start": None if oc is None else oc * 100,
            "max_limit_excursion_rad": float(max_exc),
            "all_finite": bool(finite),
            "per_chunk_E_rad": E,
            "wall_clock_s": time.time() - tw,
        })
        print("run", r + 1, "peak", round(runs[-1]["peak_E_rad"], 4),
              "onset chunk", oc, flush=True)

    peaks = [r["peak_E_rad"] for r in runs]
    onsets = [r["onset_ms_from_cycle_start"] for r in runs]
    peak_range = float(max(peaks) - min(peaks))
    onset_range = (None if any(o is None for o in onsets)
                   else float(max(onsets) - min(onsets)))
    checks = {
        "peak_E_range_le_0.05": bool(peak_range <= 0.05),
        "onset_range_le_100ms": bool(onset_range is not None
                                     and onset_range <= 100),
        "all_finite": all(r["all_finite"] for r in runs),
    }
    result = {"step": "Q4 (rerun5)", "runs": runs,
              "peak_E_range_rad": peak_range,
              "onset_range_ms": onset_range,
              "checks": checks,
              "verdict": "PASS" if all(checks.values()) else "FAIL",
              "wall_clock_s": time.time() - t0}
    out = RESULTS / "q4_rerun5.json"
    out.write_text(json.dumps(result, indent=2))
    print("peak range", peak_range, "onset range ms", onset_range)
    print("Q4 verdict:", result["verdict"], "wall", result["wall_clock_s"])
    print("wrote", out)


if __name__ == "__main__":
    main()
