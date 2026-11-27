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
  contact onset fraction
                    achieved E / E_max at the first chunk whose end-state
                    has the taste event ON (E_max = 2.1746 rad, section 3);
                    None if no chunk has the event ON (no contact)
  contact duration  taste-event ON time within the episode, chunks 0-99
                    (total ON chunks x 0.1 s), and the longest continuous
                    ON stretch in seconds (contact_longest_stretch_s)
  duty cycle        ON chunks divided by chunks in the gate-armed period
                    (arms (a) and (e): chunks 20-99; arms (b)/(d):
                    chunks 0-99; other arms or no arm given: chunks 0-99)
  ignition (arm a)  contact occurred at all AND the taste event ON in
                    chunks 20-59 (gate-ON beyond the ignition window)

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
E_MAX = 2.1746  # rad, preregistration section 3 (frozen E_max)
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


def endpoints(ep, arm=None):
    """Per-episode endpoints (preregistration section 6).

    arm: the arm whose gate-armed period sets the duty-cycle denominator
    ("a" and "e": chunks 20-99, both share arm (a)'s gating structure;
    "b"/"d": chunks 0-99; anything else or None: chunks 0-99). Part 7
    configurations run in arm (a)'s closed-loop configuration (section 8),
    so pass arm="a" for them. The remaining endpoints do not depend on arm.
    A chunk missing from the body log counts as event OFF for the
    whole-episode fields.
    """
    body, brain = ep["body"], ep["brain"]
    e_all = [r["E_rad"] for r in body]
    e_stim = [r["E_rad"] for r in body if r["chunk"] in STIM_CHUNKS]
    e_by_chunk = {r["chunk"]: r["E_rad"] for r in body}
    # taste event over the whole episode, chunks 0-99, by chunk number
    event_by_chunk = {r["chunk"]: bool(r["taste_event_at_chunk_end"]) for r in body}
    event_ep = [event_by_chunk.get(k, False) for k in range(100)]
    mn9_l = sum(r["counts"]["mn9_left"] for r in brain if r["chunk"] in STIM_CHUNKS)
    mn9_r = sum(r["counts"]["mn9_right"] for r in brain if r["chunk"] in STIM_CHUNKS)
    n_stim = len(e_stim)
    # section 6 item 6: achieved E / E_max at the first chunk whose
    # end-state has the taste event ON; None if no contact
    first_contact = next((k for k in range(100) if event_ep[k]), None)
    if first_contact is None:
        onset_frac = None
    else:
        onset_frac = float(e_by_chunk[first_contact] / E_MAX)
    # section 6 item 7: total ON chunks in the episode, and the longest
    # continuous ON stretch
    total_on = int(sum(event_ep))
    longest, run = 0, 0
    for on in event_ep:
        run = run + 1 if on else 0
        longest = max(longest, run)
    # section 6 item 7: duty cycle over the gate-armed period
    if arm in ("a", "e"):
        gate_chunks = range(20, 100)
    else:
        gate_chunks = range(0, 100)
    on_in_gate = sum(1 for k in gate_chunks if event_ep[k])
    duty = on_in_gate / len(gate_chunks)
    # section 6 item 8 (arm (a) only): contact at all, and gate-ON in
    # chunks 20-59 (taste event ON in 20-59, beyond the ignition window)
    contact_any = first_contact is not None
    gate_on = any(event_ep[k] for k in range(20, 60))
    return {
        "seed": ep["seed"],
        "peak_e_rad": float(max(e_all)),
        "mean_e_rad": float(np.mean(e_stim)),
        "mn9_left_rate_hz": mn9_l / (n_stim * CHUNK_S),
        "mn9_right_rate_hz": mn9_r / (n_stim * CHUNK_S),
        "mn9_total_rate_hz": (mn9_l + mn9_r) / (n_stim * CHUNK_S),
        "onset_latency_chunk": _first_run_at_least(e_all, ONSET_RAD),
        "contact_onset_fraction": onset_frac,
        "duty_cycle": float(duty),
        "contact_duration_s": float(total_on * CHUNK_S),
        "contact_longest_stretch_s": float(longest * CHUNK_S),
        "ignition_arm_a": bool(contact_any and gate_on),
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
    # section 6 item 6: E at first contact chunk (chunk 10, E = 1.0) / E_max
    assert abs(r["contact_onset_fraction"] - 1.0 / E_MAX) < 1e-12
    # section 6 item 7: 21 ON chunks in the episode (10-29 is 20, plus 45)
    assert abs(r["contact_duration_s"] - 2.1) < 1e-12
    # longest continuous ON stretch: chunks 10-29 is 20 chunks
    assert abs(r["contact_longest_stretch_s"] - 2.0) < 1e-12
    # duty cycle, default arm (None): 21 ON chunks over chunks 0-99
    assert abs(r["duty_cycle"] - 21 / 100) < 1e-12
    # duty cycle, arm (a): ON chunks in 20-99 are 20-29 (10) plus 45 (1)
    ra = endpoints(ep, arm="a")
    assert abs(ra["duty_cycle"] - 11 / 80) < 1e-12
    # duty cycle, arms (b) and (d): 21 ON chunks over chunks 0-99
    assert abs(endpoints(ep, arm="b")["duty_cycle"] - 21 / 100) < 1e-12
    assert abs(endpoints(ep, arm="d")["duty_cycle"] - 21 / 100) < 1e-12
    # duty cycle, arm (e): same gate-armed period as arm (a), 20-99
    assert abs(endpoints(ep, arm="e")["duty_cycle"] - 11 / 80) < 1e-12
    # section 6 item 8: contact at all, and gate-ON in 20-59 (chunks 20-29)
    assert r["ignition_arm_a"] is True
    # E below onset for the first 5 chunks, then a two-chunk run at 6-7
    e2 = [0.05] * 6 + [0.2, 0.2] + [0.05] * 92
    r2 = endpoints(_fake_episode(2, e2, 0, 0, set()))
    assert r2["onset_latency_chunk"] == 6, r2
    assert r2["ignition_arm_a"] is False
    # no contact: onset fraction is None, durations and duty cycle are zero
    assert r2["contact_onset_fraction"] is None
    assert r2["contact_duration_s"] == 0.0
    assert r2["contact_longest_stretch_s"] == 0.0
    assert r2["duty_cycle"] == 0.0
    # a single-chunk spike does not trigger onset
    e3 = [0.05] * 100; e3[10] = 0.5
    assert endpoints(_fake_episode(3, e3, 0, 0, set()))["onset_latency_chunk"] is None
    # event ON only in the tail (chunk 70): whole-episode window counts it,
    # but there is no gate-ON in 20-59, so no ignition
    r4 = endpoints(_fake_episode(4, [1.0] * 100, 0, 0, {70}))
    assert abs(r4["contact_duration_s"] - 0.1) < 1e-12
    assert abs(r4["contact_longest_stretch_s"] - 0.1) < 1e-12
    assert abs(r4["contact_onset_fraction"] - 1.0 / E_MAX) < 1e-12
    assert abs(endpoints(_fake_episode(4, [1.0] * 100, 0, 0, {70}), arm="a")["duty_cycle"] - 1 / 80) < 1e-12
    assert r4["ignition_arm_a"] is False
    # event ON only in the ignition window (chunks 5-9): contact, no gate-ON
    r5 = endpoints(_fake_episode(5, [1.0] * 100, 0, 0, set(range(5, 10))))
    assert abs(r5["contact_duration_s"] - 0.5) < 1e-12
    assert r5["ignition_arm_a"] is False
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
