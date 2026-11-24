# Part 3 Results — the four-conditions rung (rung 2)

**Status: computed per preregistration, gate pending.** The numbers below are computed exactly per the preregistration (`PART3-RUNG2-PREREG.md`, freeze tag `part3-rung2-v1`); the formal Part 3 rung-2 HARD gate (full panel + my sign-off) follows separately. **Headline as computed: the anchor passed, and the suppression comparison's outcome is SUPPRESSION (ratio 0.126, 95% CI [0.115, 0.138]; bitter at 200 Hz, sugar right-only). The rung is complete under §8.4, and its record is complete as amended under §8.5.**

**Language discipline (preregistration §§1, 7.1, binding).** This rung has no external reference output for three of its four conditions. Everything here is a **measurement of my frozen model's own responses** under the registered drive conventions: not a reproduction, not a benchmark, and not biological validation. Only the sugar condition touches validated ground, and only indirectly, through the anchor check (§8.1) against my own frozen implementation's realised Part 3 output. The bitter, water and sugar+bitter results are **model responses under conventional drives, outside the validated envelope**, and are labelled that way throughout. Nothing in this report is evidence about a living fly, animal electrophysiology, or animal behaviour.

## 1. Freeze and run record

| Item | Record |
|---|---|
| Freeze | Commit `b62a0fe70671a1f789e97ba7992120d060aae27a`, annotated tag `part3-rung2-v1`, 24 Nov 2026 (`PART3-RUNG2-FREEZE.md`). The expert-check condition (D6) was satisfied by my signed waiver of 24 Nov 2026; this rung is not expert-checked, and the human check remains owed at the Part 8 final gate. |
| Frozen implementation | Byte-identical to the Part 3 implementation freeze `0cb9b81` over `fresh/ctb/`, `fresh/tests/`, `fresh/part2/` (empty diff, verified at the freeze and again from the execution worktree). |
| Data | Part 1 data hashes re-verified (completeness `e6b71e17…`, connectivity `94db8c65…`); the loader re-verifies on every run and every manifest records them. |
| Determinism check (§12 item 7) | **Passed.** Two independent 1-trial sugar runs, seed 6220, run_id `part3-rung2-determinism-check`: spike tables bit-identical, SHA-256 `f8a537c906bfc05d0b1892bfcdad1befe5c8b6e95a3a950322f589b928a841d9` (17,389 spikes each); both manifests at the freeze commit, clean tree. |
| Harness | Run driver `work/run_rung2.py`, SHA-256 `91ea95d2…`; analysis `work/analyze_rung2.py`, SHA-256 `2cfea92b…`, verified on synthetic spike tables before touching any real output (freeze record, item 4). Two declared execution adaptations, neither touching any statistic: (1) the remaining runs executed through a worktree copy of the driver (`work-rung2/run_rung2_wt.py`, final SHA-256 `223db10d…`) whose only changes are the path arrangement of §2 below and the re-run run_ids the void rule required, each recorded in its run's manifest question text; (2) the analysis was executed through a copy (`work-rung2/analyze_rung2_rerun.py`, SHA-256 `12ebded4…`) differing from the verified original in exactly six lines, all of them run_id labels carrying the re-runs' new ids (§4's void rule requires a new run_id; the verified script's keys are the original ids). The copy's diff is recorded in the panel log, and the copy re-passed the full synthetic test before the real analysis ran. |
| Analysis outputs | `work/rung2_analysis.json` (machine-readable, complete) and `work/rung2_u2_rates.csv` (per-neuron mean rates over U2 for the four primary conditions). Bootstrap seeds as preregistered: 20261127 (MN9 and Δ CIs), 20261128 (suppression ratio), 20261129 (arm MN9 CIs), 20261130 (arm ratios); 10,000 resamples throughout. |

## 2. How §5 was satisfied for the later runs (declared arrangement)

Sugar and bitter ran in the main tree at the freeze commit. Before the sugar+bitter re-run, my publication decision added two commits on top of the freeze commit (`25c649f`, `5ad2baa`), so a main-tree run would have recorded a manifest commit other than the freeze commit and would not have counted under §5. **Ruling (recorded in the panel log and in `PART3-RUNG2-FREEZE.md`, Addendum 2; no amendment): the remaining runs executed from a git worktree pinned at the freeze commit** (`~/workspace/connectome-work/rung2-worktree`, detached HEAD `b62a0fe…`, clean tree). The frozen runner derives the manifest's git info from the code's own repo root, so every worktree run's manifest records the freeze commit and `working_tree_dirty = false`, which is §5 satisfied as written. Code and id sets came from the worktree (byte-identical to `0cb9b81`, diff-verified); `data_dir` pointed at the main repo's hash-verified Part 1 data (the `data/` directory is untracked, so the worktree has none); outputs landed in the main repo's `fresh/runs/`. Every manifest below was checked individually: freeze commit, clean tree, registered trial seeds, data hashes matching the freeze record.

## 3. The runs

All runs: 30 trials × 1.0 s through the frozen runner, no blocks. Wall clocks are the runner's recorded seconds; several ran far above the §4 projection because the shared cell throttled hard and restarted twice during the day (§4 itself records that contention stretches wall clock, not correctness).

| Condition | run_id | Seeds | Spikes | Active (>0 / ≥0.1 / ≥1 Hz) | Wall (s) |
|---|---|---|---|---|---|
| (i) Sugar | `part3-rung2-sugar` | 6100–6129 | 506,683 | 443 / 431 / 391 | 200.4 |
| (ii) Bitter | `part3-rung2-bitter` | 6130–6159 | 192,720 | 94 / 91 / 85 | 193.9 |
| (iii) Sugar+bitter | `part3-rung2-sugarbitter-rerun1` | 6160–6189 | 521,251 | 440 / 410 / 354 | 735.9 |
| (iv) Water | `part3-rung2-water` | 6190–6219 | 226,920 | 345 / 318 / 227 | 1,589.8 |
| Bitter arm @ 100 Hz | `part3-rung2-bitter100` | 6230–6259 | 85,780 | 66 / 61 / 53 | 2,123.3 |
| Bitter arm @ 150 Hz | `part3-rung2-bitter150` | 6260–6289 | 140,035 | 83 / 82 / 76 | 192.6 |
| Sugar+bitter arm @ bitter 100 Hz | `part3-rung2-sugarbitter100-rerun1` | 6290–6319 | 504,190 | 465 / 448 / 399 | 1,716.0 |
| Sugar+bitter arm @ bitter 150 Hz | `part3-rung2-sugarbitter150` | 6320–6349 | 513,237 | 454 / 435 / 381 | 2,112.6 |
| Bilateral secondary condition (v) | `part3-rung2-bilateral-rerun2` | 6350–6379 | 640,305 | 510 / 496 / 452 | 464.1 |

**Void attempts (§4 run integrity; each left an empty run directory, no partial trial set exists, and none is analysed).** Sugar+bitter attempt 1 (`part3-rung2-sugarbitter`): killed by the shared machine (SIGKILL under CPU throttling and memory contention). Sugar+bitter arm @ 100 Hz attempt 1 (`part3-rung2-sugarbitter100`): killed when the machine restarted mid-run. Bilateral attempt 1 (`part3-rung2-bilateral`): SIGKILL ~42 min in at ~5.2 GB RSS under memory contention (the bilateral drive produces the rung's largest output and the runner holds all trials in memory). Bilateral attempt 2 (`part3-rung2-bilateral-rerun1`): killed ~7 min in by a second machine restart. Each re-run took a new run_id with the same seeds, as §4 requires; the attempts stay on record here and in the panel log.

## 4. The anchor check (§8.1) — PASS

Against the Part 3 primary run's realised MN9 means (recomputed from its spike file: L 92.57 Hz, R 62.40 Hz):

| Side | This rung's sugar mean | Δ [95% CI] | Band (±25%) | Verdict |
|---|---|---|---|---|
| L | 93.63 Hz | +1.07 [−1.23, +3.40] | ±23.14 Hz | inside |
| R | 61.47 Hz | −0.93 [−3.53, +1.53] | ±15.60 Hz | inside |

L > R ordering preserved. **The anchor passes.** The non-gating discrepancy rule does not trigger (neither Δ CI excludes 0 by more than 5 Hz), so there is no discrepancy to report. The frozen implementation reproduces its own Part 3 output under this freeze; the rung proceeded past its only stop rule.

## 5. MN9 endpoints (§7)

Per condition: mean per-trial MN9 rate [95% CI], percentile bootstrap over trials, 10,000 resamples (seed 20261127 for the primary conditions, 20261129 for the arms and condition (v)). Pooled = L + R spikes per 1.0 s trial, the §7 pooled rate.

| Condition | MN9 L (Hz) | MN9 R (Hz) | Pooled (Hz) |
|---|---|---|---|
| (i) Sugar | 93.63 [91.87, 95.37] | 61.47 [59.80, 63.07] | 155.10 |
| (ii) Bitter | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 |
| (iii) Sugar+bitter | 9.97 [8.87, 11.17] | 9.57 [8.77, 10.40] | 19.53 |
| (iv) Water | 30.23 [28.23, 32.33] | 11.87 [10.70, 13.07] | 42.10 |
| Bitter @ 100 Hz (arm) | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 |
| Bitter @ 150 Hz (arm) | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 |
| Sugar+bitter @ bitter 100 Hz (arm) | 55.00 [53.20, 56.87] | 33.83 [32.17, 35.63] | 88.83 |
| Sugar+bitter @ bitter 150 Hz (arm) | 29.30 [27.27, 31.33] | 21.93 [20.53, 23.33] | 51.23 |
| Bilateral (v) | 93.17 [91.53, 94.80] | 64.87 [62.87, 66.80] | 158.03 |

Descriptive notes (no claim attaches to any of them, §7.1): bitter alone, at 200 Hz and at both arm rates, leaves MN9 at exactly 0.00 Hz on both sides, against the model's silent undriven baseline: bitter drive by itself does not recruit the feeding readout at any registered rate. For bitter alone at all three rates, every one of the 30 trials has an MN9 rate of exactly 0 on each side, so there is zero variance across trials and the bootstrap interval is degenerate: [0, 0] is the whole interval, not a rounded one. Water alone produces a nonzero, network-mediated MN9 response (L 30.23, R 11.87 Hz), reported descriptively as §7 provides. Water's response is sided (left larger than right); that sidedness is descriptive only and is not interpreted anywhere in this report (see §10: laterality is not interpretable in this rung, and RQ-C5 is not advanced by it).

## 6. The headline: the suppression ratio (§8.3) — SUPPRESSION

Ratio of condition means, pooled MN9 rate in sugar+bitter ÷ pooled MN9 rate in sugar; 95% CI by percentile bootstrap resampling trials independently within each condition (seed 20261128):

| Quantity | Ratio | 95% CI | 90% CI |
|---|---|---|---|
| **Pooled (headline)** | **0.126** | **[0.115, 0.138]** | [0.116, 0.136] |
| Per-side L | 0.106 | [0.094, 0.120] | [0.096, 0.117] |
| Per-side R | 0.156 | [0.142, 0.170] | [0.144, 0.167] |

**Claim rule applied in order:** the 95% CI lies entirely below 1, so **suppression** is claimed. Neither per-side CI lies on the opposite side of 1 (both lie entirely below 1, the same side as the pooled result), so the pre-written mixed headline is **not** triggered and the headline reads plainly: **suppression**. In words, scoped as the preregistration requires: under the registered convention (bitter at 200 Hz, sugar right-only at 200 Hz), adding the bitter drive reduces the model's pooled MN9 response to about an eighth of its sugar-only value. This is the project's RQ-C2 brain-only measurement: a model response under conventional drives, outside the validated envelope, not a biological finding.

**Registered scope of every ratio quoted in this report (gate-fix note, 24 Nov 2026):** the primary ratio, 0.126, is for bitter at 200 Hz with sugar right-only. Across the bitter rates run (§9), only the direction held: a ratio below 1 at 100, 150 and 200 Hz. Those arms are non-confirmatory, and the size of the ratio is convention-dependent (0.573, 0.330 and 0.126 across the ladder); no ratio in this report is quoted outside that scope.

## 7. The named family (§8.2, Holm across six)

Δ = condition mean MN9 rate − sugar mean, per side; 95% CI by the §7 bootstrap (seed 20261127); a difference is claimed only at Holm-adjusted p < 0.05.

| Comparison | Δ (Hz) | 95% CI | p (unadj.) | p (Holm) | Claimed |
|---|---|---|---|---|---|
| Bitter − sugar, L | −93.63 | [−95.37, −91.87] | < 0.0001 | < 0.0006 | yes |
| Bitter − sugar, R | −61.47 | [−63.07, −59.80] | < 0.0001 | < 0.0006 | yes |
| Sugar+bitter − sugar, L | −83.67 | [−85.73, −81.57] | < 0.0001 | < 0.0006 | yes |
| Sugar+bitter − sugar, R | −51.90 | [−53.70, −50.07] | < 0.0001 | < 0.0006 | yes |
| Water − sugar, L | −63.40 | [−66.03, −60.63] | < 0.0001 | < 0.0006 | yes |
| Water − sugar, R | −49.60 | [−51.60, −47.53] | < 0.0001 | < 0.0006 | yes |

(How the p-values are stated, gate-fix note, 24 Nov 2026, with the Holm bound corrected the same day at Reviewer 3's objection, see §13 item 10: each unadjusted p-value is a bootstrap tail fraction over B = 10,000 resamples of the difference distribution, trials resampled independently within each condition (seed 20261127), computed as twice the smaller of the fractions of resampled differences at or below and at or above zero. No resample crossed zero in any of the six tests, so the observed tail fraction is 0 in each test; that 0 is the observed resampling tail fraction, not a claim that the underlying p-value is exactly zero. A bootstrap p-value is therefore reported as a bound, not as 0.0000: the smallest reportable bound at this resample count is p < 1/(B+1), that is p < 0.0001 with B = 10,000 named, and the unadjusted values are reported at that bound. The Holm-adjusted values are reported at the conservative bound p < 0.0006: Holm's step-down multiplies the ordered unadjusted values by up to 6 for a family of six, so the adjusted bound is 6/(B+1), about 0.0006, and the tighter unadjusted bound does not carry over to the adjusted values. The claim decisions are unchanged, because 0.0006 sits far below the 0.05 line. The analysis artefact, `work/rung2_analysis.json`, retains the p-values exactly as computed (0.0, unrounded); no more precise value exists behind the bound.) All six differences are claimed. The bitter comparisons restate §5's descriptive fact in the family's terms: bitter alone sits exactly at the silent baseline, so its Δ against sugar is the whole sugar response, with the sign negative.

**Methodological qualification on these p-values (Reviewer 2's ruling at this gate, 24 Nov 2026; §13 item 11).** All six comparisons in this table were evaluated strictly by the frozen §8.2 formula: p = 2 × min(P(Δ ≤ 0), P(Δ ≥ 0)) over the bootstrap distribution, B = 10,000 independent within-condition resamples, seed 20261127, followed by the standard six-test Holm step-down; the executed code implements that formula as written. The qualification the panel requires to stand next to it: the resampling is not centred under a null, so the quantity is the two-sided tail mass of the uncentred bootstrap difference distribution across zero, a percentile-CI-inversion quantity, not a null-centred permutation or studentised p-value, and its resolution when zero resamples cross zero is bounded by 2/(B+1), about 0.0002, for the two-sided quantity. The table's unadjusted bound above is stated at the 1/(B+1) convention prescribed earlier in this gate; Reviewer 2's disclosure raises the 2/(B+1) two-sided resolution, and Reviewer 1's ruling on that detail is pending tonight (24 Nov 2026), so no bound in this table changes in this note. What does not rest on the tail calculation at all: every comparison's unadjusted 95% CI excludes 0 by a wide margin (bitter alone is identically 0.00 Hz on both sides), so the directional separation does not depend on tail interpolation.

## 8. Active sets and the union set U2 (§7)

Active counts per condition are in §3's table (primary definition >0 Hz, plus the 0.1 Hz and 1 Hz thresholds rung 3 pre-declared). The union of the four primary conditions' active sets, **U2 = 638 neurons**; **126,762 neurons are silent in all four conditions** and enter no comparison. Per-neuron mean rates over U2 for the four primary conditions are tabulated in `work/rung2_u2_rates.csv`.

## 9. The bitter dose-response (§§7.2, 8.5) — [PRE-REGISTERED SENSITIVITY ARM — NON-CONFIRMATORY]

The arms are reported under §8.5's rules: non-confirmatory, unadjusted CIs, outside the §8.2 family and every TOST family, and they neither rescue nor modify the §8.3 headline, which was decided on the primary conditions alone. Suppression ratios computed exactly as §7 defines the headline ratio, against the primary sugar condition (seed 20261130):

| Bitter drive rate | Pooled ratio [95% CI] | L ratio [95% CI] | R ratio [95% CI] |
|---|---|---|---|
| 100 Hz | 0.573 [0.550, 0.596] | 0.587 [0.565, 0.610] | 0.550 [0.520, 0.582] |
| 150 Hz | 0.330 [0.310, 0.351] | 0.313 [0.291, 0.336] | 0.357 [0.333, 0.382] |
| 200 Hz (primary) | 0.126 [0.115, 0.138] | 0.106 [0.094, 0.120] | 0.156 [0.142, 0.170] |

The reading, in §8.5's scoped form: under the registered convention (bitter at 200 Hz, sugar right-only), the §8.3 outcome is suppression; across the registered dose-response the ratio moved monotonically with the bitter drive rate, from 0.573 at 100 Hz through 0.330 at 150 Hz to 0.126 at 200 Hz, the direction the mechanism predicts (a stronger bitter drive is a stronger suppressive input). In every arm the sugar drive is right-only at 200 Hz and only the bitter rate varies, so the arm ratios carry that same scope: only the direction (a ratio below 1) held across the rates run, the arms are non-confirmatory, and the size of the ratio is convention-dependent (§6's registered-scope sentence). At every registered rate the ratio's CI lies below 1, so the suppression outcome does not flip anywhere on the registered ladder, but its size depends strongly on the convention, and that dependence is the finding the arms exist to record. The arms do not establish which rate is biologically correct (no reference exists to establish it against) and do not validate the encoder.

## 10. Bilateral secondary condition (v) (§§7.2, 8.5) — descriptive

Condition (v) is a separate secondary stimulus condition, OUTSIDE THE VALIDATED ENVELOPE, reported descriptively with no test registered and none constructed. Both sugar sets driven together (left 10 + right 21, at their natural unequal counts): 640,305 spikes, 510 active neurons (496 at 0.1 Hz, 452 at 1 Hz), the largest response of the rung. MN9 L 93.17 Hz [91.53, 94.80], R 64.87 Hz [62.87, 66.80], pooled 158.03 Hz, against condition (i)'s L 93.63, R 61.47, pooled 155.10, reported for comparison of magnitude only. The L > R asymmetry is present at a similar size under bilateral input (L − R = 28.30 Hz, against 32.16 Hz under right-only drive). Per §8.5, this condition reports measurements on RQ-C5's open question and resolves nothing: the sets are at unequal counts by design, and rung 6's matched-count design owns resolution. The same discipline applies to the per-side suppression ratios in §6 (L 0.106, R 0.156, bitter at 200 Hz, sugar right-only): the split is reported because the preregistration requires per-side ratios alongside the pooled headline, and both sides lie on the same side of 1, but no laterality conclusion is drawn from the difference between them. Laterality in this rung is kept descriptive throughout (here, and for water's sided response in §5), and RQ-C5 is not advanced.

## 11. Driven-population readouts (§7, manipulation check — reported, not a criterion)

Mean rate of each GRN population per condition (Hz). Driven sets read at close to their registered Poisson rates, as constructed; non-driven sets read 0.0 except where noted.

| Condition | sugar R | sugar L | bitter | water | Ir94e |
|---|---|---|---|---|---|
| (i) Sugar | **195.74** | 0.0 | 0.0 | 0.0 | 0.0 |
| (ii) Bitter | 0.0 | 0.0 | **195.60** | 0.0 | 0.0 |
| (iii) Sugar+bitter | **195.86** | 0.0 | **196.66** | 0.0 | 0.0 |
| (iv) Water | 0.58 | 0.0 | 0.0 | **197.34** | 0.0 |
| Bitter @ 100 | 0.0 | 0.0 | **98.79** | 0.0 | 0.0 |
| Bitter @ 150 | 0.0 | 0.0 | **148.38** | 0.0 | 0.0 |
| Sugar+bitter @ 100 | **196.32** | 0.0 | **98.41** | 0.0 | 0.0 |
| Sugar+bitter @ 150 | **197.17** | 0.0 | **148.30** | 0.0 | 0.0 |
| Bilateral (v) | **196.00** | **195.73** | 0.0 | 0.0 | 0.0 |

(Bold = driven in that condition.) The one nonzero non-driven readout, sugar_grn_right at 0.58 Hz under water drive, is a small network-mediated response, recorded here as §7 provides; no claim is decided by any readout in this table.

## 12. Completion (§8.4, §8.5)

§8.4's conditions, one by one: the determinism check passed (§1); all four primary conditions ran under the freeze with clean manifests (§§2, 3); the anchor passed (§4); every comparison of §§8.2–8.3 has been reported under its pre-stated rule (§§6, 7), and the §7 tables are complete (§§5, 8, 11). **The rung is complete under §8.4.** The sensitivity arms and condition (v) have also run under the freeze and are reported under §8.5's rules (§§9, 10), so **the rung's record is complete as amended**. The suppression comparison carries exactly one of its four outcomes: suppression. Completion, not the particular outcome, is what Part 7's prerequisite requires, and that prerequisite is now met on this rung's side.

**Deviations and execution events, all declared above and in the panel log:** the §5 worktree arrangement (§2, a ruling, not an amendment; the preregistration text is untouched); four void attempts, each an environmental kill (two SIGKILLs under memory contention, two machine restarts), each re-run under a new run_id with the same seeds per §4; the analysis executed through a relabelled copy of the verified script (§1), diff-recorded and re-verified on synthetic data. No seed was re-rolled, no trial was excluded, and no partial trial set was analysed. One publication event did fall inside the execution window: my publication push to GitHub, which carried the already-created freeze tag `part3-rung2-v1` with it, took place while the runs were under way; it is what moved main HEAD and made the §2 worktree arrangement necessary, and it is recorded in §2 and in Addendum 4 of `PART3-RUNG2-FREEZE.md`. The tag itself was not moved or re-created after the freeze, and no frozen file was altered.

## 13. Gate-fix notes (24 Nov 2026)

The panel's review of this report required the following text fixes and record completions. Each was applied on 24 Nov 2026, is listed here so no edit is silent, and none required or received a re-run; no number changed.

1. **P-values stated as bounds (§7).** The six §8.2-family p-values were printed as 0.0000. They are bootstrap tail fractions over B = 10,000 resamples; with no resample crossing zero, the computed value is exactly 0 and the reportable form is the bound p < 1/(B+1), printed as p < 0.0001 with B named, for the unadjusted and the Holm-adjusted values alike. The construction and the bound are stated in §7 itself. The artefact `work/rung2_analysis.json` retains the p-values exactly as computed (0.0, unrounded).
2. **Claim language (§§Status line, 6, 9).** Every suppression ratio quoted in this report now carries its scope: the primary ratio is bitter at 200 Hz, sugar right-only. The registered-scope sentence in §6 states that only the direction (a ratio below 1) held across the bitter rates run, that those arms are non-confirmatory, and that the size is convention-dependent. Confirmed for this fix: this report makes no claim to reproduce Shiu et al. or the first (v0) build in this rung, and contains no comparison to first-build numbers anywhere; the only external anchor is §4's check against my own frozen implementation's Part 3 output, as the preregistration registers it.
3. **Laterality kept descriptive (§§5, 10).** Sentences added stating that the per-side ratio split (L 0.106, R 0.156) and water's sided response are reported descriptively, are not interpreted, and do not advance RQ-C5.
4. **Void-attempt log confirmed complete (§3).** The log in §3 names each void run_id with its cause as recorded (sugar+bitter attempt 1: SIGKILL under CPU throttling and memory contention; sugar+bitter @ 100 Hz arm attempt 1: machine restart; bilateral attempt 1: SIGKILL about 42 minutes in at about 5.2 GB RSS under memory contention; bilateral attempt 2, run_id `part3-rung2-bilateral-rerun1`: a second machine restart about 7 minutes in), records that each re-run used the same seeds under a new run_id, and that each attempt left an empty run directory: no partial output existed, and none was inspected or analysed.
5. **Analysis copy: full hash and the diff, shown (§1 and here).** The executed analysis copy is `work-rung2/analyze_rung2_rerun.py`, SHA-256 `12ebded4448de853a2b13e258e64fe09436fd3bcdbd56c2b2a35fba7353205f4`, against the verified original `work/analyze_rung2.py`, SHA-256 `2cfea92b0ac4f5560225942f2f7e2b006c37eedb740afba8422d35bd8daa6294`. The complete diff between them is six lines, every one a run_id label carrying a re-run's new id, as §4's void rule requires; no statistic, seed, resample count or threshold differs. The diff is shown here in full so it stands in the audit trail, not merely described:

```diff
58c58
<     "part3-rung2-sugarbitter": (6160, ["sugar_grn_right", "bitter_grn"]),
---
>     "part3-rung2-sugarbitter-rerun1": (6160, ["sugar_grn_right", "bitter_grn"]),
62c62
<     "part3-rung2-sugarbitter100": (6290, ["sugar_grn_right", "bitter_grn"]),
---
>     "part3-rung2-sugarbitter100-rerun1": (6290, ["sugar_grn_right", "bitter_grn"]),
64c64
<     "part3-rung2-bilateral": (6350, ["sugar_grn_left", "sugar_grn_right"]),
---
>     "part3-rung2-bilateral-rerun2": (6350, ["sugar_grn_left", "sugar_grn_right"]),
67c67
<            "part3-rung2-sugarbitter", "part3-rung2-water"]
---
>            "part3-rung2-sugarbitter-rerun1", "part3-rung2-water"]
419c419
<     sb = summaries["part3-rung2-sugarbitter"]
---
>     sb = summaries["part3-rung2-sugarbitter-rerun1"]
434c434
<     for run_id, label in (("part3-rung2-sugarbitter100", "100"),
---
>     for run_id, label in (("part3-rung2-sugarbitter100-rerun1", "100"),
```

6. **Completeness confirmed (§§3, 5).** All nine conditions are reported: the four primary conditions, the four sensitivity arms and condition (v), each with its run_id, seeds, spike count, active counts and MN9 values, including the bitter-alone arms at 100 Hz and 150 Hz, whose MN9 values are 0.00 Hz on both sides (§5).
7. **Bitter-alone interval (§5).** A sentence added stating that with zero variance across trials the interval is degenerate [0, 0].
8. **GitHub push process item.** Recorded in the panel log's gate section and in Addendum 4 of `PART3-RUNG2-FREEZE.md`: the early push to main, the preservation of the first build on tag `v0-prototype-final` and in the `v0-prototype/` folder, the timing-only deviation from the original plan at my direct order, and the statement that it does not affect this rung's validity.
9. **Push-timing sentence corrected (§12).** The deviations paragraph in §12 originally closed by saying that nothing was pushed or re-tagged during execution. That sentence was imprecise about the push's timing: the publication push, carrying the already-created freeze tag `part3-rung2-v1`, did take place during the execution window, as §2 and Addendum 4 of the freeze record already stated. The sentence has been corrected in place to say so, and to state what remains true: the tag was not moved or re-created after the freeze, and no frozen file was altered. The correction was made before the gate closes; no number is affected.
10. **Holm-adjusted bound corrected (§7).** Item 1 above stated the bound p < 1/(B+1), at B = 10,000, for the unadjusted and the Holm-adjusted values alike. Reviewer 3 objected, correctly, before the gate closed: that bound holds for an individual bootstrap tail probability, but Holm's step-down multiplies the ordered unadjusted values by up to 6 for a family of six, so a Holm-adjusted value can conservatively be as large as 6/(B+1), about 0.0006, and the same p < 0.0001 bound cannot be asserted for the adjusted values without justification. The §7 table and note now report the Holm-adjusted values at p < 0.0006, with that reasoning stated, and state expressly that the 0.0 stored in the artefact is the observed resampling tail fraction (zero of 10,000 resampled differences crossed zero), not a claim that the underlying p-value is exactly zero. This item supersedes item 1's statement on the adjusted bound only; the unadjusted bound stands as item 1 states it. No claim or number is otherwise changed: all six differences remain claimed, and 0.0006 sits far below the 0.05 line.
11. **Methodological qualification on the §8.2 p-values (Reviewer 2's ruling, 24 Nov 2026).** Reviewer 3's deeper objection (item 10 corrected the bound his first objection raised; the objection itself is recorded in the panel log) went to the full panel as a panel question. Reviewer 2 ruled: Reviewer 3 is mathematically right in general, in that an uncentred bootstrap tail fraction is a percentile-CI-inversion quantity rather than a null-calibrated p-value; but the executed code implements frozen §8.2 word for word, the separations are overwhelming, and retroactively invalidating a literal pre-registered formula after seeing the results would break the preregistration contract, so the six claims stand as executed, with this qualification recorded rather than the test discarded or rewritten. Downgrading the six comparisons to descriptive was rejected, and a replacement test as a gate blocker was rejected; the Part 7 prerequisite is certified by Reviewer 2. The qualification itself, which also stands as a note at §7: (a) literal compliance: all six comparisons were evaluated strictly by the frozen PART3-RUNG2-PREREG.md §8.2 formula, p = 2 × min(P(Δ ≤ 0), P(Δ ≥ 0)) over B = 10,000 independent within-condition bootstrap draws, seed 20261127, followed by the standard six-test Holm step-down. (b) Calibration and finite-resolution disclosure: because the resampling draws from the empirical distributions without centring under a null, the computed quantity measures the two-sided tail mass of the uncentred bootstrap difference distribution across zero, a percentile-CI-inversion quantity, rather than a null-centred permutation or studentised p-value, and its resolution when zero draws cross zero is bounded by 2/(B+1), about 0.0002, for the two-sided quantity. (c) The unadjusted 95% CIs exclude 0 by wide margins in all six comparisons (bitter identically 0.00 Hz on both sides), so the directional separation does not depend on tail interpolation. (d) Anchor reconciliation: the anchor's unrounded ΔL is +1.0667 Hz, reported as +1.07 Hz rounded, alongside the accepted anchor PASS; and Part 3's sugarR analysis used correlation, overlap-floor and CI-equivalence criteria, not this p-value construction, so nothing already closed depends on it. On the one open detail: the §7 table's unadjusted bound remains stated at the 1/(B+1) convention prescribed earlier in this gate (item 1, as item 10 corrected it for the adjusted values); Reviewer 2's disclosure raises the 2/(B+1) two-sided resolution for the unadjusted quantity as well; Reviewer 1's ruling on that detail is pending tonight (24 Nov 2026). No frozen output, table bound or claim changes in this item.
