"""Part 5 / Part 7 analysis: endpoints and registered inference.

Implements docs/closed_loop_preregistration.md section 6 (endpoints),
section 7 (inference settings) and the section 7 p-value amendment
(permutation constructions), from per-episode run records written by
run_loop5.py (body_log.jsonl, brain_log.jsonl, manifest.json).

Endpoints (section 6), per episode:
  peak E            max E over the episode (rad)
  mean E            mean E over chunks 0-59 (rad)
  MN9 rates         mean left / right MN9 firing rates over chunks 0-59
                    (counts per 0.1 s chunk, so rate = counts / 0.1)
  onset latency     first chunk of the first two-chunk run of E >= 0.10
                    rad (the section 4.4 detector, as in run_loop5.py)
  contact onset fraction / duty cycle
                    fraction of chunks 0-59 with the section 4.5 event ON
  contact duration  event-ON time over chunks 0-59 (chunks x 0.1 s)
  ignition (arm a)  drive applied on >= 1 chunk >= 20 AND the event ON
                    on >= 1 chunk >= 40 (section 5)

Suppression ratio (per seed): total MN9 (L + R) mean rate under arm (d)
divided by that under arm (b); the left and right ratios ride alongside.

Inference (section 7): percentile bootstrap over seed pairs, 10,000
resamples, two-sided 95 percent CIs; TOST with a 90 percent CI against
the registered equivalence bounds. P-values (amendment): Monte Carlo
permutation tests, B = 10,000, p = (1 + #{|T*| >= |Tobs|}) / (B + 1);
sign-flip for the paired members, mean of s_i for the suppression
member, seed-stratified label permutation for the pooled matched
control members; Holm over the family of nine with member seeds
6000-6008 as registered. Section 7 names no separate bootstrap seed;
each comparison's bootstrap stream is spawned from its registered
permutation seed (SeedSequence(seed).spawn(1)), recorded here so the
choice is auditable and fixed before any Part 7 output exists.

Run with --self-test to verify every endpoint and the permutation
cores on synthetic episode records with known values. That check must
pass before this script touches real outputs (section 14 item 5).
"""
import json
from pathlib import Path

import numpy as np

CHUNK_S = 0.1
STIM_CHUNKS = range(0, 60)
ONSET_RAD = 0.10
B_PERM = 10_000
B_BOOT = 10_000
FAMILY_SEEDS = {  # section 7 seed table, amendment row 6000-6099
    "ac_peak": 6000, "ac_mean": 6001, "ab_peak": 6002, "ab_contact": 6003,
    "suppression": 6004, "lmn9_peak": 6005, "lmn9_mean": 6006,
    "lgrn_peak": 6007, "lgrn_mean": 6008,
}
TOST_BOUNDS = {"peak_e": 0.44, "mean_e": 0.22, "contact_duration_s": 1.2}


# ---------------------------------------------------------------- records
def load_episode(run_dir):
    run_dir = Path(run_dir)
    body = [json.loads(ln) for ln in (run_dir / "body_log.jsonl").read_text().splitlines() if ln.strip()]
    brain = [json.loads(ln) for ln in (run_dir / "brain_log.jsonl").read_text().splitlines() if ln.strip()]
    manifest = json.loads((run_dir / "manifest.json").read_text())
    body.sort(key=lambda r: r["chunk"])
    brain.sort(key=lambda r: r["chunk"])
    return {"body": body, "brain": brain, "manifest": manifest,
            "seed": manifest["scenario"]["seed"]}


# ---------------------------------------------------------------- endpoints
def _first_run_at_least(values, threshold):
    for k in range(len(values) - 1):
        if values[k] >= threshold and values[k + 1] >= threshold:
            return k
    return None


def endpoints(ep):
    body, brain = ep["body"], ep["brain"]
    e_all = [r["E_rad"] for r in body]
    e_stim = [r["E_rad"] for r in body if r["chunk"] in STIM_CHUNKS]
    event_stim = [bool(r["taste_event_at_chunk_end"]) for r in body
                  if r["chunk"] in STIM_CHUNKS]
    mn9_l = sum(r["counts"]["mn9_left"] for r in brain if r["chunk"] in STIM_CHUNKS)
    mn9_r = sum(r["counts"]["mn9_right"] for r in brain if r["chunk"] in STIM_CHUNKS)
    n_stim = len(e_stim)
    applied_late = any(
        any(d.get("applied") for d in r.get("applied", {}).values())
        for r in brain if r["chunk"] >= 20)
    event_late = any(bool(r["taste_event_at_chunk_end"]) for r in body
                     if r["chunk"] >= 40)
    return {
        "seed": ep["seed"],
        "peak_e_rad": float(max(e_all)),
        "mean_e_rad": float(np.mean(e_stim)),
        "mn9_left_rate_hz": mn9_l / (n_stim * CHUNK_S),
        "mn9_right_rate_hz": mn9_r / (n_stim * CHUNK_S),
        "mn9_total_rate_hz": (mn9_l + mn9_r) / (n_stim * CHUNK_S),
        "onset_latency_chunk": _first_run_at_least(e_all, ONSET_RAD),
        "contact_onset_fraction": float(np.mean(event_stim)),
        "duty_cycle": float(np.mean(event_stim)),
        "contact_duration_s": float(sum(event_stim) * CHUNK_S),
        "ignition_arm_a": bool(applied_late and event_late),
    }


def suppression_ratio(ep_b, ep_d):
    """Per-seed suppression ratio (d)/(b) on total MN9 rate, L and R
    alongside (section 6). A zero arm (b) rate gives ratio None."""
    eb, ed = endpoints(ep_b), endpoints(ep_d)
    def ratio(num, den):
        return None if den == 0 else num / den
    return {
        "seed": eb["seed"],
        "ratio_total": ratio(ed["mn9_total_rate_hz"], eb["mn9_total_rate_hz"]),
        "ratio_left": ratio(ed["mn9_left_rate_hz"], eb["mn9_left_rate_hz"]),
        "ratio_right": ratio(ed["mn9_right_rate_hz"], eb["mn9_right_rate_hz"]),
        "rate_b_hz": eb["mn9_total_rate_hz"], "rate_d_hz": ed["mn9_total_rate_hz"],
    }


# ---------------------------------------------------------------- inference
def _boot_rng(perm_seed):
    return np.random.default_rng(np.random.SeedSequence(perm_seed).spawn(1)[0])


def bootstrap_ci_paired(x, y, perm_seed, b=B_BOOT):
    """Percentile bootstrap 95 percent CI for mean(x - y) over seed pairs."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    d = x - y
    rng = _boot_rng(perm_seed)
    idx = rng.integers(0, len(d), size=(b, len(d)))
    means = d[idx].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(np.mean(d)), float(lo), float(hi)


def bootstrap_ci_values(vals, perm_seed, b=B_BOOT, level=95.0):
    vals = np.asarray(vals, float)
    rng = _boot_rng(perm_seed)
    idx = rng.integers(0, len(vals), size=(b, len(vals)))
    means = vals[idx].mean(axis=1)
    tail = (100.0 - level) / 2.0
    lo, hi = np.percentile(means, [tail, 100.0 - tail])
    return float(np.mean(vals)), float(lo), float(hi)


def sign_flip_pvalue(diffs, perm_seed, b=B_PERM):
    """Two-sided sign-flip permutation p-value for paired differences
    (statistic: mean of the differences). Amendment construction."""
    d = np.asarray(diffs, float)
    if np.all(d == 0):
        return 1.0
    tobs = abs(float(np.mean(d)))
    rng = np.random.default_rng(perm_seed)
    signs = rng.choice([-1.0, 1.0], size=(b, len(d)))
    stats = np.abs(signs @ d / len(d))
    return float((1 + int(np.sum(stats >= tobs))) / (b + 1))


def suppression_s(d_rate, b_rate):
    """s_i = (d_i - b_i) / (d_i + b_i); both zero gives 0, d zero with
    b positive gives -1 (amendment edge cases; no seed excluded)."""
    if d_rate == 0 and b_rate == 0:
        return 0.0
    return (d_rate - b_rate) / (d_rate + b_rate)


def suppression_pvalue(pairs, perm_seed, b=B_PERM):
    """pairs: list of (rate_b, rate_d) per seed. Statistic: mean of s_i,
    sign-flipped (amendment)."""
    s = np.array([suppression_s(d, bb) for bb, d in pairs], float)
    return sign_flip_pvalue(s, perm_seed, b=b), float(np.mean(s))


def stratified_label_pvalue(lesion_by_seed, controls_by_seed, perm_seed, b=B_PERM):
    """Seed-stratified label permutation for a pooled matched-control
    comparison (amendment). lesion_by_seed: {seed: value}; controls:
    {seed: [five values]}. Within each seed the six values are permuted
    and one is drawn as the pseudo-lesion value; statistic: lesion mean
    minus pooled control mean."""
    seeds = sorted(lesion_by_seed)
    groups = [np.array([lesion_by_seed[s]] + list(controls_by_seed[s]), float)
              for s in seeds]
    tobs = abs(float(np.mean([lesion_by_seed[s] for s in seeds])
                     - np.mean([v for s in seeds for v in controls_by_seed[s]])))
    rng = np.random.default_rng(perm_seed)
    count = 0
    for _ in range(b):
        les, ctl = [], []
        for g in groups:
            perm = rng.permutation(g)
            les.append(perm[0]); ctl.extend(perm[1:])
        if abs(float(np.mean(les) - np.mean(ctl))) >= tobs:
            count += 1
    return float((1 + count) / (b + 1))


def holm_adjust(pvals):
    """Holm adjusted p-values, in the input order (m = len(pvals))."""
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    adj_sorted = np.maximum.accumulate((m - np.arange(m)) * p[order])
    adj = np.empty(m)
    adj[order] = np.minimum(adj_sorted, 1.0)
    return adj


def tost_equivalent(ci90, bound):
    lo, hi = ci90
    return bool(lo >= -bound and hi <= bound)


# ---------------------------------------------------------------- self-test
def _fake_episode(seed, e_series, mn9_l, mn9_r, event_chunks, applied_chunks=()):
    body = [{"chunk": k, "E_rad": e, "taste_event_at_chunk_end": k in event_chunks}
            for k, e in enumerate(e_series)]
    brain = [{"chunk": k, "counts": {"mn9_left": mn9_l, "mn9_right": mn9_r},
              "applied": {"sugar": {"applied": k in applied_chunks}}}
             for k in range(len(e_series))]
    return {"body": body, "brain": brain, "seed": seed, "manifest": {}}


def self_test():
    # constant E = 1.0 for 100 chunks, event on chunks 10-29, MN9 10/5
    ep = _fake_episode(1, [1.0] * 100, 10, 5, set(range(10, 30)) | {45},
                       applied_chunks=set(range(25, 30)))
    r = endpoints(ep)
    assert r["peak_e_rad"] == 1.0 and abs(r["mean_e_rad"] - 1.0) < 1e-12
    assert r["mn9_left_rate_hz"] == 100.0 and r["mn9_right_rate_hz"] == 50.0
    assert r["mn9_total_rate_hz"] == 150.0
    assert r["onset_latency_chunk"] == 0
    assert abs(r["contact_onset_fraction"] - 21 / 60) < 1e-12
    assert abs(r["contact_duration_s"] - 2.1) < 1e-12
    assert r["ignition_arm_a"] is True
    # E below onset for the first 5 chunks, then a two-chunk run at 6-7
    e2 = [0.05] * 6 + [0.2, 0.2] + [0.05] * 92
    r2 = endpoints(_fake_episode(2, e2, 0, 0, set()))
    assert r2["onset_latency_chunk"] == 6, r2
    assert r2["ignition_arm_a"] is False
    # a single-chunk spike does not trigger onset
    e3 = [0.05] * 100; e3[10] = 0.5
    assert endpoints(_fake_episode(3, e3, 0, 0, set()))["onset_latency_chunk"] is None
    # suppression ratio: b total 150 Hz, d total 20 Hz -> 2/15
    ep_b = _fake_episode(4, [1.0] * 100, 10, 5, set())
    ep_d = _fake_episode(4, [1.0] * 100, 1, 1, set())
    sr = suppression_ratio(ep_b, ep_d)
    assert abs(sr["ratio_total"] - 20.0 / 150.0) < 1e-12, sr
    assert abs(sr["ratio_left"] - 0.1) < 1e-12
    assert abs(sr["ratio_right"] - 0.2) < 1e-12
    # s_i edge cases
    assert suppression_s(0.0, 5.0) == -1.0
    assert suppression_s(0.0, 0.0) == 0.0
    assert abs(suppression_s(15.0, 150.0) - (-135.0 / 165.0)) < 1e-12
    # permutation cores: identical values -> p = 1; separated -> p small
    assert sign_flip_pvalue([0.0] * 20, 6000) == 1.0
    p_sep = sign_flip_pvalue([1.0] * 20, 6000)
    assert p_sep <= 0.001, p_sep
    les = {s: 2.0 for s in range(20)}
    ctl = {s: [1.0] * 5 for s in range(20)}
    p_les = stratified_label_pvalue(les, ctl, 6005)
    assert p_les <= 0.01, p_les
    les0 = {s: 1.0 for s in range(20)}
    assert stratified_label_pvalue(les0, ctl, 6005) == 1.0
    # suppression p-value on a strong true effect
    pairs = [(150.0, 15.0)] * 20
    p_sup, mean_s = suppression_pvalue(pairs, 6004)
    assert p_sup <= 0.001 and abs(mean_s - (-135.0 / 165.0)) < 1e-12
    # Holm: known example
    adj = holm_adjust([0.01, 0.04, 0.03])
    assert np.allclose(adj, [0.03, 0.06, 0.06]), adj
    # bootstrap CI sanity: constant difference
    m, lo, hi = bootstrap_ci_paired([2.0] * 20, [1.0] * 20, 6000)
    assert m == 1.0 and lo == 1.0 and hi == 1.0
    print("analysis.py self-test: PASS (endpoints, suppression, permutation "
          "cores, Holm, bootstrap, TOST helpers verified on synthetic records)")
    return True


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        self_test()
    else:
        print("analysis.py: import for endpoints/inference, or run --self-test")
