"""Shared comparison pipeline for the Part 3 sugarR benchmark rung.

One code path serves both the main comparison (reference vs our output) and
the cross-replicate noise ceiling (split halves of one output against each
other). That is the point: the ceiling is computed through the identical
union-active-set and tie-handling code as the comparison, so a changed
support cannot leak in through a second implementation (Reviewer 1, R2).

Conventions, fixed here and in PART3-PREREG.md:
- A neuron is ACTIVE in an output if it emits at least one spike across
  that output's full evaluation window (mean rate > 0 Hz). The sensitivity
  thresholds (0.1 Hz, 1 Hz) are absolute mean-rate thresholds.
- The comparison set is the UNION of the two outputs' active sets; a neuron
  active on one side only enters with rate 0 on the other.
- Spearman uses average ranks for ties (scipy.stats.spearmanr default).
  Many ties at 0 are expected: most neurons in the union set are silent on
  at least one side, and the union set is dominated by low-rate neurons.
  Pearson is computed on the same mean-rate vectors, over the same set.
- Rates are mean spikes per second over the trials of the output being
  summarised; every trial is exactly 1.0 s.
"""

import numpy as np
import pandas as pd
from scipy import stats

# Fixed seeds, published in the preregistration before any run.
SPLIT_SEED = 20261123      # split-half partitions (ceiling machinery)
BOOTSTRAP_SEED = 20261124  # percentile bootstrap over trials (MN9 CIs)

MN9_LEFT = 720575940660219265
MN9_RIGHT = 720575940645521262


def load_spikes(path):
    """Load a spike table in the shared schema (t, trial, flywire_id)."""
    df = pd.read_parquet(path)
    return df


def counts_matrix(spikes, neuron_ids, n_trials):
    """Per-neuron, per-trial spike counts.

    Returns an int array of shape (len(neuron_ids), n_trials). Neurons
    absent from the spike table get a row of zeros — silent neurons are
    explicit zeros, never missing (prereg §6).
    """
    index = {nid: i for i, nid in enumerate(neuron_ids)}
    counts = np.zeros((len(neuron_ids), n_trials), dtype=np.int32)
    ids = spikes["flywire_id"].to_numpy()
    trials = spikes["trial"].to_numpy()
    rows = np.array([index.get(v, -1) for v in ids], dtype=np.int64)
    ok = rows >= 0
    # bincount over (row, trial) pairs; trials outside [0, n_trials) are ignored.
    ok &= (trials >= 0) & (trials < n_trials)
    flat = rows[ok] * n_trials + trials[ok]
    b = np.bincount(flat, minlength=len(neuron_ids) * n_trials)
    counts = b.reshape(len(neuron_ids), n_trials).astype(np.int32)
    return counts


def mean_rates(counts, duration_s=1.0):
    """Mean firing rate (Hz) per neuron over the trials in `counts`."""
    return counts.sum(axis=1) / (counts.shape[1] * duration_s)


def active_mask(total_spikes, window_s, threshold_hz=None):
    """Active mask for one output.

    Primary rule (threshold_hz=None): active iff at least one spike in the
    window (total_spikes >= 1), i.e. mean rate > 0 Hz.
    Sensitivity thresholds: active iff mean rate >= threshold_hz, i.e.
    total_spikes >= threshold_hz * window_s.
    """
    if threshold_hz is None:
        return total_spikes >= 1
    return total_spikes >= threshold_hz * window_s


def compare_outputs(counts_a, counts_b, threshold_hz=None):
    """Compare two outputs given as per-neuron per-trial count matrices.

    Builds each side's mean-rate vector and active set from its own counts,
    forms the union active set, and computes Spearman, Pearson, Jaccard,
    precision and recall over that set. This is the single function used
    for the main comparison AND for every split-half ceiling pair.
    """
    n_a = counts_a.shape[1]
    n_b = counts_b.shape[1]
    rates_a = mean_rates(counts_a)
    rates_b = mean_rates(counts_b)
    act_a = active_mask(counts_a.sum(axis=1), n_a, threshold_hz)
    act_b = active_mask(counts_b.sum(axis=1), n_b, threshold_hz)
    union = act_a | act_b
    inter = act_a & act_b
    ra = rates_a[union]
    rb = rates_b[union]
    if union.sum() < 3:
        spearman = pearson = float("nan")
    else:
        spearman = float(stats.spearmanr(ra, rb).statistic)
        pearson = float(np.corrcoef(ra, rb)[0, 1])
    jaccard = float(inter.sum() / union.sum()) if union.sum() else 1.0
    precision = float(inter.sum() / act_b.sum()) if act_b.sum() else 1.0
    recall = float(inter.sum() / act_a.sum()) if act_a.sum() else 1.0
    return {
        "n_union": int(union.sum()),
        "n_a": int(act_a.sum()),
        "n_b": int(act_b.sum()),
        "spearman": spearman,
        "pearson": pearson,
        "jaccard": jaccard,
        "precision": precision,
        "recall": recall,
    }


def _spearman_brown(rho_half):
    """Correct a split-half correlation to full-length reliability."""
    return 2.0 * rho_half / (1.0 + rho_half)


def split_half_ceiling(counts, n_splits=200, split_seed=SPLIT_SEED,
                       threshold_hz=None):
    """Cross-replicate ceiling component for ONE output (R_ref,30 or R_new,30).

    200 balanced splits: the trial indices are partitioned at random into
    two halves of 15 (without replacement), under the fixed split seed.
    Each half-pair is compared through compare_outputs (identical pipeline,
    union active set of the two halves, average-rank ties). Each half
    correlation is Spearman-Brown corrected to 30-trial reliability and the
    corrected values are averaged over splits.
    """
    n_trials = counts.shape[1]
    half = n_trials // 2
    rng = np.random.default_rng(split_seed)
    sp, pe = [], []
    for _ in range(n_splits):
        perm = rng.permutation(n_trials)
        h1, h2 = perm[:half], perm[half:2 * half]
        res = compare_outputs(counts[:, h1], counts[:, h2], threshold_hz)
        sp.append(_spearman_brown(res["spearman"]))
        pe.append(_spearman_brown(res["pearson"]))
    sp = np.array(sp)
    pe = np.array(pe)
    return {
        "R_spearman": float(sp.mean()),
        "R_pearson": float(pe.mean()),
        "R_spearman_sd": float(sp.std(ddof=1)),
        "R_pearson_sd": float(pe.std(ddof=1)),
        "R_spearman_95pct": [float(np.percentile(sp, 2.5)),
                             float(np.percentile(sp, 97.5))],
        "R_pearson_95pct": [float(np.percentile(pe, 2.5)),
                            float(np.percentile(pe, 97.5))],
        "n_splits": n_splits,
        "split_seed": split_seed,
    }


def split_half_overlap(counts, thresholds_hz, n_splits=200,
                       split_seed=SPLIT_SEED):
    """Reference-only split-half analogue for the set-overlap floors (R4).

    For each threshold, the two halves' active sets are compared (Jaccard,
    precision, recall) and averaged over the same 200 balanced splits.
    This is what "the same model, run again" scores against itself on the
    overlap metrics — the floors in the preregistration sit below these
    values, with room for seeded-vs-unseeded variation.
    """
    n_trials = counts.shape[1]
    half = n_trials // 2
    rng = np.random.default_rng(split_seed)
    out = {}
    for th in thresholds_hz:
        j, p, r = [], [], []
        for _ in range(n_splits):
            perm = rng.permutation(n_trials)
            h1, h2 = perm[:half], perm[half:2 * half]
            res = compare_outputs(counts[:, h1], counts[:, h2], th)
            j.append(res["jaccard"])
            p.append(res["precision"])
            r.append(res["recall"])
        out[th] = {
            "jaccard_mean": float(np.mean(j)),
            "jaccard_sd": float(np.std(j, ddof=1)),
            "precision_mean": float(np.mean(p)),
            "precision_sd": float(np.std(p, ddof=1)),
            "recall_mean": float(np.mean(r)),
            "recall_sd": float(np.std(r, ddof=1)),
        }
    return out


def bootstrap_mean_ci(rates_by_trial, n_resamples=10000,
                      seed=BOOTSTRAP_SEED):
    """Percentile bootstrap 95% CI for a mean rate over trials.

    rates_by_trial: 1-D array of per-trial rates for one neuron.
    """
    rng = np.random.default_rng(seed)
    n = len(rates_by_trial)
    idx = rng.integers(0, n, size=(n_resamples, n))
    means = rates_by_trial[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))
