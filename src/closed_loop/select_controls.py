"""Part 5 freeze: matched-control set selection (preregistration 8.1).

Selects the five matched-control sets for each targeted lesion family
(C-MN9-1..5 for L-MN9, C-GRN-1..5 for L-GRN), under selection seed 5700,
with sub-seeds drawn only from the two fixed per-lesion streams the
section 7 amendment registers: 5701-5749 for L-MN9, 5750-5799 for
L-GRN. Runs once, at the freeze, before any Part 7 episode exists
(section 14 item 3); the artefact (matched_controls.csv and
matched_controls.json, written next to this script) is hashed into the
freeze record.

Registered procedure (section 8.1), as implemented here:

- Candidate pool: every v630 neuron except the targeted sets, every
  driven population (sugar L/R, bitter, water, Ir94e, JON-CE/F/D_m/all),
  MN9, the three-inhibitory set, aDN1, aDN2-left and aBN1.
- Features, from frozen artefacts only: in-degree, out-degree, in and
  out synapse totals (Part 1 connectivity, hash-verified by the
  loader), predicted transmitter sign (the loader's Excitatory sign of
  the neuron's outgoing edges; every presynaptic neuron carries exactly
  one sign, verified on the file; neurons with no outgoing edges get
  sign 0 and count as non-excitatory in the excitatory fraction), and
  baseline mean firing rate from the Part 3 primary run's spikes
  (part3-sugarR-200Hz, 30 trials x 1.0 s; rate = spike count / 30;
  neurons that never spike have rate 0).
- Matching: within one draw, the target set's members are matched
  one-to-one to distinct pool neurons by nearest distance in the
  standardised feature space (each of the six features normalised by
  its pooled SD over the candidate pool). The sub-seed's role: a
  numpy default_rng(sub_seed) shuffles the order in which the target
  members are matched, because greedy nearest matching is
  order-dependent. Exact distance ties break to the lower FlyWire ID.
- Draws proceed in sub-seed order within the lesion's own stream.
  Every drawn candidate set consumes its neurons (no neuron is reused
  within or across the family's sets, drawn or accepted), which keeps
  the registered without-replacement rule true under any reading and
  keeps any fallback five mutually disjoint. The first five candidate
  sets passing all tolerances are the controls.
- Tolerances: exact set size (by construction); mean in-degree and
  mean out-degree within +/-25 percent of the target's; excitatory
  fraction within +/-0.10; mean baseline rate within +/-25 percent or
  +/-5 Hz, whichever is wider.
- Fallback (registered): if a lesion's stream is exhausted with fewer
  than five passing sets, the five lowest-distance drawn sets are used
  (set distance = mean matched-pair distance) and the screen's failure
  is reported; if fewer than five sets were drawn at all, all drawn
  sets are used and the shortfall is reported. No tolerance is widened.

Usage (brain env):
    python select_controls.py
Writes matched_controls.csv / matched_controls.json beside this file
and prints their SHA-256 hashes.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "src"))
from brain_model.data.loader import load_connectome  # noqa: E402

SELECTION_SEED = 5700
STREAMS = {"L-MN9": list(range(5701, 5750)), "L-GRN": list(range(5750, 5800))}
TARGET_FILES = {"L-MN9": "mn9.csv", "L-GRN": "sugar_grn_right.csv"}
EXCLUSION_FILES = [
    "mn9.csv", "sugar_grn_left.csv", "sugar_grn_right.csv",
    "bitter_grn.csv", "water_grn.csv", "ir94e_grn.csv", "jon_ce.csv",
    "jon_f.csv", "jon_d_m.csv", "jon_all.csv", "three_inhibitory.csv",
    "adn1.csv", "adn2_left.csv", "abn1.csv",
]
SPIKES = REPO / "results" / "validation" / "runs" / "part3-sugarR-200Hz" / "spikes.parquet"
N_TRIALS = 30  # 30 trials x 1.0 s in the Part 3 primary run
FEATURES = ["in_degree", "out_degree", "in_synapses", "out_synapses",
            "sign", "baseline_rate_hz"]


def read_set(name):
    with open(REPO / "data" / "neuron_sets" / name) as fh:
        return [int(r["flywire_id"]) for r in csv.DictReader(fh)]


def build_features():
    data = load_connectome(REPO / "data", verify=True)
    ids = data.ids
    n = len(ids)
    edges = data.edges
    pre = edges["Presynaptic_Index"].to_numpy()
    post = edges["Postsynaptic_Index"].to_numpy()
    conn = edges["Connectivity"].to_numpy(dtype=np.float64)
    exc = edges["Excitatory"].to_numpy(dtype=np.int64)
    feats = {name: np.zeros(n) for name in FEATURES}
    np.add.at(feats["in_degree"], post, 1)
    np.add.at(feats["out_degree"], pre, 1)
    np.add.at(feats["in_synapses"], post, conn)
    np.add.at(feats["out_synapses"], pre, conn)
    # one sign per presynaptic neuron (verified unique on the file)
    sign = np.zeros(n)
    seen = np.zeros(n, dtype=bool)
    sign[pre] = exc
    seen[pre] = True
    feats["sign"] = sign
    spikes = pd.read_parquet(SPIKES, columns=["flywire_id"])
    counts = spikes.groupby("flywire_id").size()
    rate = np.zeros(n)
    idx = data.index_of([int(x) for x in counts.index])
    rate[idx] = counts.to_numpy(dtype=np.float64) / N_TRIALS
    feats["baseline_rate_hz"] = rate
    return data, feats


def set_summary(feats, idx):
    return {
        "size": int(len(idx)),
        "mean_in_degree": float(np.mean(feats["in_degree"][idx])),
        "mean_out_degree": float(np.mean(feats["out_degree"][idx])),
        "excitatory_fraction": float(np.mean(feats["sign"][idx] > 0)),
        "mean_baseline_rate_hz": float(np.mean(feats["baseline_rate_hz"][idx])),
    }


def passes(summary, target):
    rate_band = max(0.25 * target["mean_baseline_rate_hz"], 5.0)
    checks = {
        "size_exact": summary["size"] == target["size"],
        "mean_in_degree_pm25pct": abs(summary["mean_in_degree"] - target["mean_in_degree"]) <= 0.25 * target["mean_in_degree"],
        "mean_out_degree_pm25pct": abs(summary["mean_out_degree"] - target["mean_out_degree"]) <= 0.25 * target["mean_out_degree"],
        "excitatory_fraction_pm0.10": abs(summary["excitatory_fraction"] - target["excitatory_fraction"]) <= 0.10,
        "mean_baseline_rate_band": abs(summary["mean_baseline_rate_hz"] - target["mean_baseline_rate_hz"]) <= rate_band,
    }
    return all(checks.values()), checks


def select_family(data, feats, pool_idx, target_idx, stream, family):
    """pool_idx: candidate Brian indices (array). target_idx: target
    members' Brian indices. Returns (record, remaining_pool_mask_set)."""
    pool_ids = data.ids[pool_idx]
    sd = {f: float(np.std(feats[f][pool_idx])) for f in FEATURES}
    def z(idx_arr, f):
        return feats[f][idx_arr] / sd[f]
    target_z = np.column_stack([z(target_idx, f) for f in FEATURES])
    pool_z = np.column_stack([z(pool_idx, f) for f in FEATURES])
    consumed = set()
    drawn = []       # (sub_seed, member pool positions, mean pair distance)
    accepted = []
    for sub_seed in stream:
        if len(accepted) == 5:
            break
        rng = np.random.default_rng(sub_seed)
        order = rng.permutation(len(target_idx))
        available = np.array([p for p in range(len(pool_idx))
                              if int(pool_idx[p]) not in consumed], dtype=int)
        if len(available) < len(target_idx):
            break
        avail_z = pool_z[available]
        avail_ids = pool_ids[available]
        chosen_pos = []
        pair_distances = []
        used_local = set()
        for t in order:
            d = np.sqrt(((avail_z - target_z[t]) ** 2).sum(axis=1))
            for j in used_local:
                d[j] = np.inf
            dmin = d.min()
            tied = np.flatnonzero(d == dmin)
            pick = tied[np.argmin(avail_ids[tied])]  # tie: lower FlyWire ID
            used_local.add(int(pick))
            chosen_pos.append(int(available[pick]))
            pair_distances.append(float(dmin))
        member_idx = pool_idx[np.array(chosen_pos)]
        consumed.update(int(x) for x in member_idx)
        summary = set_summary(feats, member_idx)
        ok, checks = passes(summary, set_summary(feats, target_idx))
        rec = {"sub_seed": sub_seed,
               "member_flywire_ids": [int(x) for x in data.ids[member_idx]],
               "mean_pair_distance": float(np.mean(pair_distances)),
               "summary": summary, "checks": checks, "passed": bool(ok)}
        drawn.append(rec)
        if ok:
            accepted.append(rec)
    fallback = False
    shortfall = False
    if len(accepted) < 5:
        fallback = True
        ranked = sorted(drawn, key=lambda r: r["mean_pair_distance"])
        chosen = ranked[:5]
        shortfall = len(chosen) < 5
        accepted = chosen
    return {
        "family": family,
        "selection_seed": SELECTION_SEED,
        "stream": [stream[0], stream[-1]],
        "target": set_summary(feats, target_idx),
        "target_flywire_ids": [int(x) for x in data.ids[target_idx]],
        "n_draws": len(drawn),
        "draws": drawn,
        "accepted_via_fallback": fallback,
        "shortfall_fewer_than_five_drawn": shortfall,
        "control_sets": accepted,
    }


def main():
    data, feats = build_features()
    excluded = set()
    for name in EXCLUSION_FILES:
        excluded.update(read_set(name))
    pool_mask = np.array([int(fid) not in excluded for fid in data.ids])
    pool_idx = np.flatnonzero(pool_mask)
    record = {
        "what": "Part 5 matched-control sets artefact (preregistration 8.1), "
                "generated at the Part 5 freeze, before any Part 7 episode",
        "selection_seed": SELECTION_SEED,
        "pool_size": int(len(pool_idx)),
        "features": FEATURES,
        "families": {},
    }
    rows = []
    for family, stream in STREAMS.items():
        target_idx = data.index_of(read_set(TARGET_FILES[family]))
        fam = select_family(data, feats, pool_idx, target_idx, stream, family)
        record["families"][family] = fam
        label = "C-MN9" if family == "L-MN9" else "C-GRN"
        for k, s in enumerate(fam["control_sets"], start=1):
            for fid in s["member_flywire_ids"]:
                i = int(data.index_of([fid])[0])
                rows.append({"family": family, "control_set": f"{label}-{k}",
                             "sub_seed": s["sub_seed"], "flywire_id": fid,
                             **{f: float(feats[f][i]) for f in FEATURES}})
        print(f"{family}: draws={fam['n_draws']} accepted={len(fam['control_sets'])} "
              f"fallback={fam['accepted_via_fallback']} shortfall={fam['shortfall_fewer_than_five_drawn']}")
    csv_path = HERE / "matched_controls.csv"
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json_path = HERE / "matched_controls.json"
    json_path.write_text(json.dumps(record, indent=2) + "\n")
    for p in (csv_path, json_path):
        print(p.name, hashlib.sha256(p.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
