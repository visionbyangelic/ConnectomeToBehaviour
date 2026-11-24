# Part 3 Results — the `sugarR` benchmark rung

**Status: draft verdict report — the verdict below is computed exactly per the preregistration (`PART3-PREREG.md`, freeze tag `part3-prereg-v2`); the formal Part 3 HARD gate (full panel + my sign-off) follows separately. Verdict as computed: PASS.**

**Language discipline (preregistration §1, binding).** `sugarR.parquet` is Shiu et al.'s *simulation output*, not animal data. Everything here is **model-vs-model agreement**: my independent implementation reproducing a reference simulation. Nothing in this report is biological validation, agreement with a living fly, or evidence about animal electrophysiology or behaviour. The permitted summary sentence is: **"the sugarR benchmark rung passed"** — one rung of the Part 3 ladder (§12), not "the brain is validated".

## 1. Freeze and run record (§13 checklist, in order)

| Item | Record |
|---|---|
| Approval | I approved the preregistration document as amended (Pass 3, with Reviewer 1's typo correction) on **23 Nov 2026 at 22:51 WAT**, after the panel's Pass 3 re-check completed (Reviewer 1 confirmed subject to the correction, since applied; Reviewers 2 and 3 confirmed outright). Recorded in the preregistration's Amendment history. |
| Freeze commit | `e1f40462a68cfd2f87325ec0fc4e519bf667db09` — "Part 3: freeze the sugarR preregistration as approved (200 Hz primary) and the comparison harness", committed 23 Nov 2026, 21:55:45 UTC (22:55:45 WAT), in the working clone. **Nothing was pushed to GitHub.** |
| Tag | `part3-prereg-v2` (annotated), created on the freeze commit, 23 Nov 2026, 22:55 WAT. No preregistration tag existed before this one. |
| Freeze commit contents | The approved preregistration, the comparison harness (`fresh/part3/compare.py`, `reference_only.py`, `reference_only_values.json`), the current `track.md`, and one `.gitignore` addition (`fresh/runs/` — run outputs are uncommitted by design per `PART3-FREEZE.md`; ignoring the directory is what makes the clean-tree requirement of preregistration §5 achievable once run outputs exist). The frozen implementation is byte-identical between the implementation freeze (`0cb9b81`) and this commit — verified by an empty `git diff` over `fresh/ctb/`, `fresh/tests/`, `fresh/part2/`. |
| Reference hash (§13 item 3) | `sugarR.parquet` SHA-256 `83921d50089d966785e402d6c0e3be5ab3eba5beb680410a09c557b0f22dcc28` — re-verified at the freeze; the analysis re-verified it again before comparing. |
| Harness hashes (§13 item 4) | `compare.py` SHA-256 `46821323a222b09240dd6916489703dce65ae3d44aa2da6efa356897807a050a`; `reference_only.py` SHA-256 `f249b264f686d5eba61bb0b51631fd8c17cea8efc30ad0ca81d0ec5dcb234c10`. Frozen runner: commit `0cb9b8129236dc4200b5eaa600f59ccc072263f9` (`PART3-FREEZE.md`). |
| Environment | Brain env, confirmed live at the freeze: Python 3.12.3, Brian2 2.9.0, numpy 1.26.4, scipy 1.17.1, pandas 3.0.6, pyarrow 20.0.0 — matches `PART3-FREEZE.md` exactly. The run manifest records the same versions. |
| Harness synthetic test (§13 item 4) | Before touching real outputs, the comparison pipeline was verified on synthetic count tables with known agreement: identical tables → Spearman = Pearson = Jaccard = precision = recall = 1.0 exactly; disjoint active sets → overlap metrics exactly 0; a noised copy → high but imperfect correlations (0.9985 / 0.9990); split-half ceiling on constant trials → exactly 1.0. All passed. (First attempt at the noised case put background noise on silent rows, which genuinely changes the active set — the pipeline correctly reported the disagreement; the test case was fixed, the harness was not touched.) |
| Determinism check (§13 item 6, §4) | **Passed.** Two independent 1-trial runs, run_id `part3-determinism-check`, seed 9999, 200 Hz, under separate out roots: both spike tables SHA-256 `5fe11896d136b511eafe649afb0d5dd5fa08aa782b58d05d9176f2caae61e98a` — **bit-identical** (17,084 spikes, 415 active neurons each; both manifests show the freeze commit, `dirty=False`). One earlier attempt at this check was killed by a service restart before any simulation output existed; the empty run directory was removed and the check re-run clean — the attempt is logged here and in track.md, per the run-integrity rule. |
| Validation run | run_id `part3-sugarR-200Hz`; 30 trials × 1.0 s; sugar GRN right (21 IDs) at 200 Hz; seeds **3000–3029**. Manifest: commit `e1f4046…` (the freeze commit), **`working_tree_dirty = False`** (§5 satisfied), data hashes match the freeze record, wall clock **2,094.6 s** (≈ 35 min; inside the ≈ 57 min projection and the 2 h budget). Output: **508,915 spikes, 446 active neurons**; `spikes.parquet` SHA-256 `f97689c3ee188f9bc1891821eb93352386321ae9f5b9cff28c57275b18dcd6a0`. |
| Analysis | Through the frozen harness (`compare.py`) via a driver script (`work/analyze_part3.py`; full machine-readable results in `work/part3_analysis.json`). The preregistration fixes B = 2,000 (gap bootstrap) and 10,000 resamples (correlation CIs) but does not name those two RNG seeds; the driver used **20261125** (gap) and **20261126** (correlation CIs), declared here. Split seed 20261123 and MN9 bootstrap seed 20261124 are the preregistered ones. |

Pipeline identity checks (all passed): the reference active set re-counted at **448** (§7 stop-rule satisfied); R_ref,30 recomputed through the identical pipeline came out at Spearman 0.999463 / Pearson 0.999806, **exactly the pre-recorded §2.1 values**; the reference MN9 CIs recomputed identically are [92.10, 94.37] and [60.33, 63.30], exactly as pre-recorded.

## 2. Headline numbers

Comparison set: the union **U = 453 neurons** (reference active 448, ours active 446, intersection 441; 126,947 neurons silent on both sides). Reference: 511,566 spikes; ours: 508,915 spikes.

| Metric | Value | Criterion (§8) | Band |
|---|---|---|---|
| Spearman ρ over U | **0.99939** | ≥ C_cross − 0.02 (= 0.97946) and ≥ 0.90 | PASS |
| Pearson r over U | **0.99982** | ≥ C_cross − 0.02 (= 0.97980) | PASS |
| Signed gap G (Spearman) | +0.00007 (point); 95th pct of bootstrap **0.00094** | 95th pct ≤ 0.02 | PASS |
| Signed gap G_Pearson | −0.00001 (point); 95th pct **0.00034** | 95th pct ≤ 0.02 | PASS |
| Jaccard (primary threshold) | **0.9735** | ≥ 0.85 | PASS |
| Precision | **0.9888** | ≥ 0.90 | PASS |
| Recall | **0.9844** | ≥ 0.85 | PASS |

Secondary (reported, §7 item 2): over A_ref only, Spearman 0.99946, Pearson 0.99981.

**Cross-replicate ceiling (§7 item 4).** R_ref,30 (pre-recorded, §2.1): Spearman 0.99946, Pearson 0.99981. R_new,30 (ours, 200 splits, seed 20261123): Spearman **0.99946** (SD 0.00012), Pearson **0.99980** (SD 0.00005). **C_cross: Spearman 0.99946, Pearson 0.99980.** Our output's own trial-to-trial reliability is the same as the reference's to three decimal places — the observed correlations sit essentially *at* the ceiling: the Spearman point gap is +0.00007, and the Pearson correlation slightly **exceeds** its ceiling (signed gap −0.00001; exceeding is never penalised, §8). Ceiling bootstrap intervals (from the gap-bootstrap replicates, ceiling recomputed per replicate): C_cross,Spearman 95% [0.99938, 0.99955]; C_cross,Pearson 95% [0.99979, 0.99983]. Odd/even split-half for ours (Spearman–Brown corrected): Spearman 0.99943, Pearson 0.99976.

Correlation bootstrap CIs (§7 item 7; 10,000 resamples over trials on both sides): Spearman [0.99843, 0.99925]; Pearson [0.99942, 0.99976]. One observation, recorded so it is understood rather than discovered later: both point estimates sit slightly *above* the top of their percentile intervals. That is the known behaviour of this resampling for a statistic pressed against its upper bound of 1.0 — resampled trial sets duplicate trials, which attenuates the correlation a little, so the resample distribution sits a shade below the point estimate. It is also exactly why the preregistration's decision rule (Reviewer 1, R1) uses the **gap** bootstrap — ceiling recomputed inside the same resample — rather than these raw intervals; the gap intervals are consistent with the point gaps. These CIs are reporting quantities; no verdict clause uses them.

**Sensitivity table (§7 item 3)** — set overlap at the three pre-declared thresholds (floors apply at the primary threshold only):

| Threshold | Jaccard | Precision | Recall | (Spearman / Pearson over that union) |
|---|---|---|---|---|
| Primary (≥ 1 spike in 30 trials) | 0.9735 | 0.9888 | 0.9844 | 0.99939 / 0.99982 |
| ≥ 0.1 Hz | 0.9862 | 0.9954 | 0.9908 | 0.99947 / 0.99981 |
| ≥ 1 Hz | 0.9898 | 0.9974 | 0.9923 | 0.99948 / 0.99980 |

**Distribution diagnostic (§7 item 6, reported, not a criterion).** Over U, per-neuron rate differences (ours − reference): median −0.067 Hz, IQR [−0.467, +0.167] Hz. Fraction of U within the Part 0 agreement band (±25% of the reference rate or ±5 Hz, whichever is wider): **1.000** — every neuron in the union set.

## 3. MN9 endpoints (§7 item 5, §8 clause 4)

Per-trial rates, 30 trials each side; CIs are percentile bootstrap over trials, 10,000 resamples, seed 20261124.

| Neuron | Reference mean [95% CI] | Ours mean [95% CI] | Δ (ours − ref) [95% CI] | Equivalence margin | Decision |
|---|---|---|---|---|---|
| MN9 left (720575940660219265) | 93.27 Hz [92.10, 94.37] | **92.57 Hz** [91.10, 94.03] | **−0.70 Hz** [−2.50, +1.13] | ±23.3 Hz | CI entirely within margin ✓ |
| MN9 right (720575940645521262) | 61.80 Hz [60.33, 63.30] | **62.40 Hz** [60.50, 64.47] | **+0.60 Hz** [−1.87, +3.17] | ±15.5 Hz | CI entirely within margin ✓ |

Ordering: ours left (92.57) > right (62.40) — the reference's L > R ordering is preserved. Precision gate: our CI half-widths are 1.47 Hz (L) and 1.98 Hz (R), against the 15%-of-reference-mean limits of 13.99 Hz and 9.27 Hz — comfortably inside. CI-overlap (reporting only, §8 clause 4): each side's mean lies inside the other side's CI, both neurons. Spike counts: left 2,798 (ref) vs 2,777 (ours); right 1,854 vs 1,872.

**RQ-C5 boundary (§10).** These numbers say the MN9 asymmetry *appears* in my reproduction, at close to the reference's size (ours L−R = 30.2 Hz; reference 31.5 Hz). They say nothing about *why* — whether it is a circuit property, an artefact of the unequal GRN set sizes, or something else stays an open hypothesis for the dedicated RQ-C5 rung. No claim beyond "appears, and how large" is made here.

## 4. Verdict (§8 combination rule)

PASS requires **all** clauses; FAIL fires on **any** trigger; anything else is INCONCLUSIVE.

| Clause | Result |
|---|---|
| PASS 1 — Spearman point + gap | ✓ (0.99939 ≥ 0.97946; ≥ 0.90; gap 95th pct 0.00094 ≤ 0.02) |
| PASS 2 — Pearson point + gap | ✓ (0.99982 ≥ 0.97980; gap 95th pct 0.00034 ≤ 0.02) |
| PASS 3 — Jaccard / precision / recall floors | ✓ (0.9735 / 0.9888 / 0.9844 vs 0.85 / 0.90 / 0.85) |
| PASS 4 — MN9 equivalence + ordering | ✓ (both Δ CIs inside their margins; L > R preserved) |
| Precision gate (CI half-widths ≤ 15%) | ✓ (1.47 / 1.98 Hz vs 13.99 / 9.27 Hz) |
| Ceiling guard (C_cross,Spearman ≥ 0.90) | ✓ (0.99946) |
| FAIL triggers 1–5 | none fired (nearest: Jaccard 0.9735 vs the 0.75 fail line) |

**Verdict as computed under the preregistration: PASS.** The §8.1(a) N = 60 extension does not apply (nothing is inconclusive). The 150 Hz sensitivity arm has **not** been run: under §4.1/§8.2 it runs only after the primary verdict is recorded and the gate has seen it — it is a question for the HARD gate, not something to fire off on the back of this report.

**Scope (§12).** This certifies the sugarR rung only: one stimulus, one population, one experiment, model-vs-model. The remaining rungs (short trial; four conditions incl. bitter and sugar+bitter suppression; feeding prediction subset; weight-shuffle control; RQ-C5 resolution) each need their own preregistration before they run.

## 5. What happens next

The Part 3 HARD gate: this report and the run record go to the full panel and to my own sign-off. Until the gate closes, this verdict is *computed per preregistration, gate pending* — that label stays on it in every summary.

## 6. The 150 Hz sensitivity arm (§4.1) — NON-CONFIRMATORY

**Status: non-confirmatory throughout, as pre-declared.** This section was appended after the Part 3 HARD gate closed (the panel upheld the primary PASS; I signed off on 23 Nov 2026 at 23:48 WAT; Part 3 is closed for the sugarR rung). Under §4.1 the arm runs only after the primary verdict is recorded; under §8.2 it is reported alongside the primary verdict and **cannot change it**. The primary verdict is PASS and stands, whatever this section says.

**Run record.** run_id `part3-sugarR-150Hz-arm`; identical to the primary run in every respect except `rate_hz` = 150 and the seed block: 30 trials × 1.0 s, sugar GRN right (21 IDs) at 150 Hz, seeds **3030–3059**, same frozen implementation. Manifest: commit `e1f4046…` (the freeze commit), data hashes match the freeze record, wall clock **2,164.2 s** (≈ 36 min). Output: **409,726 spikes, 436 active neurons**; `spikes.parquet` SHA-256 `a03d7f6baa5c33e4825d98d3f63b4eba849f5966e55013ca925284c187a69d00`. Run on the night of 23/24 Nov 2026. One manifest difference from the primary run, stated plainly: `working_tree_dirty = True`. The dirt is exactly two documentation files — this preregistration's own §13 dated freeze note (a post-run annotation, kept identifiable as such) and `track.md`'s living entries — and at analysis time every code and data path (`fresh/ctb`, `fresh/part3`, `fresh/tests`, `fresh/part2`, `data`) was verified clean, so the code that executed is the frozen code at the freeze commit. §5's clean-tree validity rule bound the confirmatory primary run, which satisfied it; the arm is non-confirmatory, and the honest record of its tree state is this paragraph. Analysis: through the same frozen harness (`compare.py`) via `work/analyze_part3_arm.py`; full machine-readable results in `work/part3_analysis_arm.json`; same declared bootstrap seeds as the primary analysis (gap 20261125, correlation CIs 20261126; split seed 20261123 and MN9 seed 20261124 are the preregistered ones). Pipeline identity checks passed again: reference active set re-counted at 448; R_ref,30 recomputed through the identical pipeline exactly equals the pre-recorded §2.1 values (Spearman 0.99946, Pearson 0.99981).

**Headline numbers (arm's own 30 trials, §8 rules).** Comparison set: the union **U = 453 neurons** (reference active 448, arm active 436, intersection 431; 126,947 neurons silent on both sides). Reference: 511,566 spikes; arm: 409,726 spikes.

| Metric | Value | Criterion (§8) | Band |
|---|---|---|---|
| Spearman ρ over U | **0.98966** | ≥ C_cross − 0.02 (= 0.97938) and ≥ 0.90 | PASS |
| Pearson r over U | **0.99470** | ≥ C_cross − 0.02 (= 0.97978) | PASS |
| Signed gap G (Spearman) | +0.00972 (point); 95th pct of bootstrap **0.01153** | 95th pct ≤ 0.02 | PASS |
| Signed gap G_Pearson | +0.00508 (point); 95th pct **0.00575** | 95th pct ≤ 0.02 | PASS |
| Jaccard (primary threshold) | **0.9514** | ≥ 0.85 | PASS |
| Precision | **0.9885** | ≥ 0.90 | PASS |
| Recall | **0.9621** | ≥ 0.85 | PASS |

Secondary (reported, §7 item 2): over A_ref only, Spearman 0.99003, Pearson 0.99467.

**Cross-replicate ceiling (§7 item 4).** R_ref,30 (pre-recorded, §2.1): Spearman 0.99946, Pearson 0.99981. R_new,30 (arm, 200 splits, seed 20261123): Spearman **0.99930**, Pearson **0.99976** — the arm's own output is as self-consistent as the reference's; it is consistently *different from* the reference, not noisier. **C_cross: Spearman 0.99938, Pearson 0.99978.** Ceiling bootstrap intervals: C_cross,Spearman 95% [0.99933, 0.99951]; C_cross,Pearson 95% [0.99977, 0.99981]. Odd/even split-half for the arm (Spearman–Brown corrected): Spearman 0.99935, Pearson 0.99975. Correlation bootstrap CIs (10,000 resamples): Spearman [0.98755, 0.99053]; Pearson [0.99394, 0.99492]. The gaps tell the real story: the arm's Spearman point gap (+0.00972) is roughly 140 times the primary's (+0.00007) — the 150 Hz output sits measurably *below* its ceiling, where the 200 Hz output sat essentially on it — while remaining inside the 0.02 tolerance the preregistration allows.

**Sensitivity table (§7 item 3)** — floors apply at the primary threshold only:

| Threshold | Jaccard | Precision | Recall | (Spearman / Pearson over that union) |
|---|---|---|---|---|
| Primary (≥ 1 spike in 30 trials) | 0.9514 | 0.9885 | 0.9621 | 0.98966 / 0.99470 |
| ≥ 0.1 Hz | 0.9291 | 0.9927 | 0.9355 | 0.98904 / 0.99457 |
| ≥ 1 Hz | 0.9020 | 0.9809 | 0.9182 | 0.98922 / 0.99419 |

**Distribution diagnostic (§7 item 6, reported, not a criterion).** Over U, per-neuron rate differences (arm − reference): median **−5.90 Hz**, IQR [−9.10, −1.10] Hz — a systematic downward shift across the population, where the primary's median difference was −0.067 Hz. Fraction of U within the Part 0 agreement band: **0.8102** (primary: 1.000).

**MN9 endpoints (§7 item 5, §8 clause 4).**

| Neuron | Reference mean [95% CI] | Arm mean [95% CI] | Δ (arm − ref) [95% CI] | Equivalence margin | Decision |
|---|---|---|---|---|---|
| MN9 left (720575940660219265) | 93.27 Hz [92.10, 94.37] | **83.10 Hz** [81.60, 84.63] | **−10.17 Hz** [−12.03, −8.27] | ±23.3 Hz | CI entirely within margin ✓ |
| MN9 right (720575940645521262) | 61.80 Hz [60.33, 63.30] | **58.00 Hz** [56.37, 59.63] | **−3.80 Hz** [−6.03, −1.63] | ±15.5 Hz | CI entirely within margin ✓ |

Ordering: arm left (83.10) > right (58.00) — preserved. Precision gate: arm CI half-widths 1.52 Hz (L) and 1.63 Hz (R) against the limits 13.99 Hz and 9.27 Hz — inside. Spike counts: left 2,798 (ref) vs 2,493 (arm); right 1,854 vs 1,740. Both motor neurons fire clearly *less* at 150 Hz drive — left by about a tenth — but by less than the ±25% equivalence margins, so clause 4 is met.

**The driven-GRN readout — the measurement the arm exists for (reported, not a §8 criterion).** Under this model's drive a driven neuron fires at close to the Poisson rate by construction (§3/A1), so the driven population's own firing rate reads out the generating rate. In the reference file the 21 driven right sugar GRNs fire at mean **196.75 Hz** (median 197.27, range 191.3–202.1). In this arm — my own simulation driven at exactly 150 Hz — they fire at mean **147.95 Hz** (median 147.77, range 144.9–152.8). The ranges do not come close to overlapping. A file generated at 150 Hz would show its driven neurons at ~148 Hz, as this arm does; the reference shows ~197 Hz. This confirms with a full simulation what the reference-only discrimination check (§3/A1) read from the file's own statistics before the freeze: **the reference was generated at ~200 Hz, not at the 150 Hz code default** — and it is why the 200 Hz primary, not this arm, is the protocol-matched reproduction.

**Would-be verdict (§8 combination rule, applied to the arm's own trials).**

| Clause | Result |
|---|---|
| PASS 1 — Spearman point + gap | ✓ (0.98966 ≥ 0.97938; ≥ 0.90; gap 95th pct 0.01153 ≤ 0.02) |
| PASS 2 — Pearson point + gap | ✓ (0.99470 ≥ 0.97978; gap 95th pct 0.00575 ≤ 0.02) |
| PASS 3 — Jaccard / precision / recall floors | ✓ (0.9514 / 0.9885 / 0.9621 vs 0.85 / 0.90 / 0.85) |
| PASS 4 — MN9 equivalence + ordering | ✓ (both Δ CIs inside their margins; L > R preserved) |
| Precision gate (CI half-widths ≤ 15%) | ✓ (1.52 / 1.63 Hz vs 13.99 / 9.27 Hz) |
| Ceiling guard (C_cross,Spearman ≥ 0.90) | ✓ (0.99938) |
| FAIL triggers 1–5 | none fired (nearest: Jaccard 0.9514 vs the 0.75 fail line) |

**The arm's would-be verdict under §8 is PASS — and it changes nothing.** Stated exactly as §8.2 requires: the arm is non-confirmatory, it is reported alongside the primary verdict, and it cannot change the primary verdict. The primary (200 Hz) is PASS; §8.2's "protocol-ambiguous" annotation applies only where a primary FAIL or INCONCLUSIVE meets an arm that would have passed, which is not the case here, so no annotation is made. The honest reading of the arm passing §8 is about the criteria, not about the rate: §8's statistics were built to detect a failed reproduction, and a uniformly weaker drive preserves the population's rank order, keeps most of the active set, and moves MN9 by less than the wide ±25% margins — so the arm clears them while sitting visibly below its ceiling (gap 0.00972 vs the primary's 0.00007), shifted down across the population (median −5.90 Hz), and missing the driven neurons' own rates by ~49 Hz. The drive-rate question was never carried by the §8 summary statistics; it is carried by the driven-GRN readout above, and there the answer is unambiguous. The ambiguity the arm was pre-declared to measure is now measured: 150 Hz is the wrong rate, by simulation, not just by the file's statistics.
