"""Reference-only analysis for the Part 3 preregistration (Reviewer 1, R2/R4).

Computes, from sugarR.parquet ALONE (no model output exists yet):
- the reference active-set size (re-count; must be 448),
- the reference MN9 means, bootstrap CIs and ordering,
- the reference split-half ceiling component R_ref,30 (Spearman and
  Pearson) through the identical compare_outputs pipeline,
- the reference-only split-half analogue for the set-overlap floors,
- the driven-GRN firing rates (the R3 rate-discrimination check).

Run: brain-env python reference_only.py
Output: prints the values and writes reference_only_values.json next to
this file. These values are then quoted in PART3-PREREG.md (Pass 2) with
the reference file's hash. This script sees no model output, so running it
now is clean.
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare import (BOOTSTRAP_SEED, MN9_LEFT, MN9_RIGHT, SPLIT_SEED,
                     bootstrap_mean_ci, compare_outputs, counts_matrix,
                     mean_rates, split_half_ceiling, split_half_overlap)

HERE = Path(__file__).resolve().parent
DATA = Path.home() / "workspace/connectome-work/repo/data"
REF = DATA / "sugarR.parquet"
EXPECTED_SHA256 = ("83921d50089d966785e402d6c0e3be5ab3eba5beb680410a09c557b0f22dcc28")
ID_SETS = Path.home() / "workspace/connectome-work/repo/fresh/part2/id_sets_v1"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_ids(name):
    return pd.read_csv(ID_SETS / f"{name}.csv")["flywire_id"].tolist()


def main():
    got = sha256(REF)
    assert got == EXPECTED_SHA256, f"hash mismatch: {got}"
    print(f"reference hash verified: {got}")

    spikes = pd.read_parquet(REF)
    assert set(spikes["exp_name"].unique()) == {"sugarR"}
    assert sorted(spikes["trial"].unique()) == list(range(30))
    assert spikes["t"].min() >= 0 and spikes["t"].max() < 1.0
    print(f"spike rows: {len(spikes)}")

    completeness = pd.read_csv(DATA / "2023_03_23_completeness_630_final.csv")
    # Header is ",Completed": the ID column is unnamed (first column).
    ids = completeness.iloc[:, 0].tolist()
    assert len(ids) == 127400
    counts = counts_matrix(spikes, ids, 30)
    rates = mean_rates(counts)
    id_index = {nid: i for i, nid in enumerate(ids)}

    # --- Active-set recount (primary rule: >= 1 spike in 30 trials) ---
    active = counts.sum(axis=1) >= 1
    n_active = int(active.sum())
    print(f"active set size (re-count): {n_active}")
    for th in (0.1, 1.0):
        n = int((rates >= th).sum())
        print(f"active at >= {th} Hz: {n}")

    # --- MN9 endpoints ---
    out = {"reference_sha256": got, "n_spike_rows": int(len(spikes)),
           "active_set_size": n_active}
    for label, nid in (("left", MN9_LEFT), ("right", MN9_RIGHT)):
        row = counts[id_index[nid]].astype(float)  # per-trial counts = Hz
        mean = float(row.mean())
        lo, hi = bootstrap_mean_ci(row)
        out[f"mn9_{label}"] = {"mean_hz": mean, "ci95": [lo, hi],
                               "n_spikes": int(row.sum())}
        print(f"MN9 {label}: mean {mean:.2f} Hz, 95% CI [{lo:.2f}, {hi:.2f}], "
              f"spikes {int(row.sum())}")
    out["mn9_ordering"] = "left > right" if out["mn9_left"]["mean_hz"] > \
        out["mn9_right"]["mean_hz"] else "right >= left"

    # --- Driven-GRN rates: the R3 rate-discrimination check ---
    # Driven neurons fire at close to the Poisson drive rate by construction
    # (68.75 mV kick per event, no refractory while driven), so the mean
    # rate of the 21 driven right sugar GRNs reads out the drive rate used
    # to generate this file. Left sugar GRNs (not driven) are the control.
    for label, name in (("sugar_grn_right (driven)", "sugar_grn_right"),
                        ("sugar_grn_left (control)", "sugar_grn_left"),
                        ("bitter_grn (control)", "bitter_grn"),
                        ("water_grn (control)", "water_grn")):
        pop = load_ids(name)
        pop_rates = rates[[id_index[n] for n in pop]]
        out[f"rates_{name}"] = {
            "mean_hz": float(pop_rates.mean()),
            "median_hz": float(np.median(pop_rates)),
            "min_hz": float(pop_rates.min()),
            "max_hz": float(pop_rates.max()),
        }
        print(f"{label}: mean {pop_rates.mean():.1f} Hz, median "
              f"{np.median(pop_rates):.1f}, range [{pop_rates.min():.1f}, "
              f"{pop_rates.max():.1f}]")

    # --- Split-half ceiling component R_ref,30 (identical pipeline) ---
    ceil = split_half_ceiling(counts, n_splits=200, split_seed=SPLIT_SEED)
    out["R_ref_30"] = ceil
    print(f"R_ref,30 Spearman: {ceil['R_spearman']:.4f} "
          f"(SD {ceil['R_spearman_sd']:.4f}, 95% pct "
          f"[{ceil['R_spearman_95pct'][0]:.4f}, {ceil['R_spearman_95pct'][1]:.4f}])")
    print(f"R_ref,30 Pearson:  {ceil['R_pearson']:.4f} "
          f"(SD {ceil['R_pearson_sd']:.4f}, 95% pct "
          f"[{ceil['R_pearson_95pct'][0]:.4f}, {ceil['R_pearson_95pct'][1]:.4f}])")
    # The "ceiling below 0.90 -> INCONCLUSIVE" branch needs C_cross < 0.90,
    # i.e. R_new,30 < 0.81 / R_ref,30. Report the implied threshold.
    for key in ("R_spearman", "R_pearson"):
        thr = 0.81 / ceil[key]
        print(f"  branch live only if R_new,30 ({key}) < {thr:.4f}")
        out[f"R_new_threshold_for_branch_{key}"] = thr

    # --- Split-half overlap analogue for the floors (R4) ---
    ov = split_half_overlap(counts, [None, 0.1, 1.0], n_splits=200,
                            split_seed=SPLIT_SEED)
    out["split_half_overlap"] = {str(k): v for k, v in ov.items()}
    for th, v in ov.items():
        print(f"split-half overlap at threshold {th}: Jaccard "
              f"{v['jaccard_mean']:.4f} (SD {v['jaccard_sd']:.4f}), precision "
              f"{v['precision_mean']:.4f}, recall {v['recall_mean']:.4f}")

    with open(HERE / "reference_only_values.json", "w") as f:
        json.dump(out, f, indent=2)
    print("wrote reference_only_values.json")


if __name__ == "__main__":
    main()
