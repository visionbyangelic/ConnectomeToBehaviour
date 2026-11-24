"""Part 5 freeze calibration: compute r_hi from the calibration episodes.

Registered procedure (docs/closed_loop_preregistration.md section 4): ten
scripted-window sugar-only episodes, seeds 5000-5009, run through the
closed loop (run_loop5.py) under the provisional r_hi = 155, labelled
PROVISIONAL. The decoder's r_filt is computed before the e mapping, so
the pooled r_filt samples do not depend on the provisional value.

r_hi is the 95th percentile of the pooled per-chunk r_filt over chunks
20-59 across the ten episodes (400 values), numpy's default linear
interpolation. It is computed once, here, and frozen with the decoder
and the completed E(r) table (section 4, section 14 item 2).

Rejection rule (section 4): if r_hi <= 15 Hz (r_lo 5 + 10) the decoder
is rejected with no rescue; this script reports the rejection and no
evaluation episode may run.

Also reported, per section 4: each episode's steady-window mean r_filt
and the pooled figure, e_steady = (mean - r_lo) / (r_hi - r_lo), and
the contact margin e_steady - 0.837, where 0.837 is the e at which
contact first became visible in qualification (0.840 rounded down).

Usage (body env not required; stdlib + numpy):
    python calibrate_rhi.py --runs-dir DIR --out RECORD.json
where DIR holds one subdirectory per calibration episode, each with a
body_log.jsonl. The record is written as JSON and its SHA-256 printed.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

R_LO = 5.0
E_MAX = 2.1746
REJECTION_BOUND = 15.0
CONTACT_E = 0.837
STEADY_CHUNKS = range(20, 60)
SEEDS = list(range(5000, 5010))
E_TABLE_RATES = [0, 25, 50, 75, 100, 125, 155]


def read_rfilt(body_log_path):
    rows = []
    for line in Path(body_log_path).read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    rows.sort(key=lambda r: r["chunk"])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    runs_dir = Path(args.runs_dir)

    pooled = []
    per_episode = []
    run_dirs = sorted(p for p in runs_dir.iterdir() if p.is_dir())
    assert len(run_dirs) == 10, f"expected 10 calibration run dirs, found {len(run_dirs)}"
    for run_dir in run_dirs:
        manifest = json.loads((run_dir / "manifest.json").read_text())
        seed = manifest["scenario"]["seed"]
        rows = read_rfilt(run_dir / "body_log.jsonl")
        assert len(rows) == 100, f"{run_dir}: expected 100 chunks, found {len(rows)}"
        steady = [r["r_filt_hz"] for r in rows if r["chunk"] in STEADY_CHUNKS]
        assert len(steady) == 40
        pooled.extend(steady)
        per_episode.append({
            "run_dir": run_dir.name,
            "seed": seed,
            "steady_window_mean_r_filt_hz": float(np.mean(steady)),
            "body_log_sha256": hashlib.sha256(
                (run_dir / "body_log.jsonl").read_bytes()).hexdigest(),
        })
    seeds_found = sorted(e["seed"] for e in per_episode)
    assert seeds_found == SEEDS, f"calibration seeds {seeds_found} != {SEEDS}"
    assert len(pooled) == 400

    pooled_arr = np.array(pooled, dtype=float)
    r_hi = float(np.percentile(pooled_arr, 95))  # numpy default: linear
    pooled_mean = float(np.mean(pooled_arr))
    e_steady = (pooled_mean - R_LO) / (r_hi - R_LO) if r_hi > R_LO else None
    e_table = {str(r): float(min(max((r - R_LO) / (r_hi - R_LO), 0.0), 1.0) * E_MAX)
               for r in E_TABLE_RATES} if r_hi > R_LO else None

    record = {
        "what": "Part 5 freeze calibration record (preregistration section 4)",
        "seeds": SEEDS,
        "n_episodes": 10,
        "steady_window_chunks": [20, 59],
        "n_pooled_values": 400,
        "per_episode": per_episode,
        "pooled_mean_r_filt_hz": pooled_mean,
        "r_hi_hz": r_hi,
        "percentile": "95th, numpy.percentile default linear interpolation",
        "r_lo_hz": R_LO,
        "rejection_bound_hz": REJECTION_BOUND,
        "decoder_rejected": bool(r_hi <= REJECTION_BOUND),
        "e_steady": e_steady,
        "contact_e_from_qualification": CONTACT_E,
        "contact_margin": (e_steady - CONTACT_E) if e_steady is not None else None,
        "e_table_rad": e_table,
        "e_max_rad": E_MAX,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2) + "\n")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(json.dumps({"r_hi_hz": r_hi, "pooled_mean_r_filt_hz": pooled_mean,
                      "e_steady": e_steady, "contact_margin": record["contact_margin"],
                      "decoder_rejected": record["decoder_rejected"],
                      "record": str(out), "record_sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
