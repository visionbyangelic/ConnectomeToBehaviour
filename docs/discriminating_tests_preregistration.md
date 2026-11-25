# Discriminating-tests preregistration: the Part 6 gate's three tests (D2/D4, D3, D7)

**Status: DRAFT. Not approved, not frozen. No trial has run under this document, no tag has been created, and no trial may run until the section 12 freeze checklist is complete.**

**Gate class: HARD.** These tests are the Part 6 gate's own requirement (comparison report section 17 item 2, decided 25 Nov 2026): the three discriminating runs that the Part 6 comparison named but did not run. They gate Part 7's MN9 claims: no Part 7 conclusion that leans on an MN9 number may be drawn until this gate closes. Any later change to this document is a formal amendment, logged, panel-reviewed, Angelic-approved (plan section 0.2c, D6).

**Why these tests, why now.** The Part 6 fresh-vs-old comparison (docs/fresh_vs_old_comparison.md) agreed with the old build and the paper on the main conditions, and left four items unresolved in detail: D2 (sugar plus bitter, right side, size), D3 (water response size), D4 (suppression ratio size), and D7 (RQ-C5 symmetry, unresolved in both builds). Each named a discriminating test it did not run, because Part 6 runs no new episodes. The Part 6 gate (closed 25 Nov 2026, decision (c) hybrid, itemised) decided that the three tests run as their own preregistration gate before Part 7 leans on any MN9 numbers, not inside Part 7's design. This document is that gate's preregistration.

**Scope.** Three tests, brain-only, under one freeze, plus a sugar anchor and a matched unilateral pair that test 3 needs:

- **Test 1 (D2/D4):** a fresh sugar plus bitter arm at 150/150 Hz, sugar at 150 Hz and bitter at 150 Hz, matching the old build's 1 s suite rate for both drives. It asks whether the drive rate explains the right-side size gap (old R 14.2 Hz against fresh 200/200 R 9.57 Hz) and the suppression-ratio size gap (old 0.164 against fresh 0.126).
- **Test 2 (D3):** a fresh water arm at 150 Hz, matching the old build's 1 s suite rate. It asks whether the drive rate explains the water size gap (old L 6.0 Hz against fresh 200 Hz L 30.23 Hz).
- **Test 3 (D7/RQ-C5):** a matched-count bilateral design: both sugar sets driven at 200 Hz with equal counts (10 left plus 10 right), plus the matched unilateral pair (left-only 10, right-only 10 from the same subset). It asks whether the L over R MN9 asymmetry survives when the driven counts are matched, which is the registered RQ-C5 resolution design (PLAN line 301: bilateral and unilateral runs at matched GRN counts).

**Frozen implementation.** All runs under this preregistration use the same frozen implementation as the Part 3 sugarR rung and the four-conditions rung: commit `0cb9b8129236dc4200b5eaa600f59ccc072263f9`, in the pinned brain env (Python 3.12.3, Brian2 2.9.0, numpy 1.26.4, scipy 1.17.1, pandas 3.0.6, pyarrow 20.0.0), on the Part 1 data files (hashes in the Part 3 freeze record). This gate's own freeze commit (section 12) must contain that implementation byte-identical, verified the same way the sugarR freeze verified it. Outputs are never mixed across revisions.

**Governing prior decisions.** PLAN.md section 4.1 (Part 6: fresh against old against paper; unresolved load-bearing discrepancies block any push), section 8 (RQ-C5: core, must be resolved before any MN9 number is published) and line 301 (matched-count resolution at Part 3 with dedicated bilateral and unilateral runs at matched GRN counts, before any MN9 claim); Part 0 rules (N conventions, bootstrap CIs, rate-agreement band plus or minus 25 percent or plus or minus 5 Hz whichever is wider, suppression-ratio equivalence bounds plus or minus 0.15 absolute); docs/fresh_vs_old_comparison.md section 15 (D2, D3, D4, D7: magnitudes, candidate causes, discriminating tests) and section 17 item 2 (the gate decision that these tests run as their own gate); docs/taste_conditions_preregistration.md (the four-conditions rung: drive conventions, firing-rate computation, MN9 endpoints, anchor rule, dose-response ladder); docs/brain_validation_preregistration.md section 8 (the ceiling-gap benchmark rule) and section 10 (RQ-C5 handling); docs/closed_loop_preregistration.md section 1 (the rung as Part 7's prerequisite, discharged; this gate as Part 7's further prerequisite for its MN9 claims); the Part 6 gate decision (c) hybrid, itemised, 25 Nov 2026, and its item 4 (RQ-C5 handling: logged deviation with my explicit ratification, every public MN9 figure labelled "RQ-C5 open" until the matched-count test runs).

---

## 1. The questions these tests answer

Three questions, one per test, each with a pre-written reading in section 8. No other question is registered here.

1. **Test 1:** does driving sugar plus bitter at 150/150 Hz reproduce the old build's right-side MN9 rate (14.2 Hz) and pooled suppression ratio (0.164), or does it reproduce the fresh build's 200/200 pattern (R 9.57 Hz, ratio 0.126)? In the first case the drive rate explains D2 and D4; in the second it does not.
2. **Test 2:** does driving water at 150 Hz reproduce the old build's MN9 rates (L 6.0 Hz, R 1.6 Hz), or does it reproduce the fresh build's 200 Hz pattern (L 30.23 Hz, R 11.87 Hz)? In the first case the drive rate explains D3; in the second it does not.
3. **Test 3:** does the MN9 L over R asymmetry survive when both sugar sets are driven at matched counts (10 left plus 10 right at 200 Hz)? If the asymmetry vanishes at matched counts, it was a set-size artefact; if it persists, it is a circuit property. The matched unilateral pair (left-only 10 against right-only 10) tests the same question from the other side: whether each side alone drives its own MN9 equally at matched counts.

**Language discipline (binding on every report of these tests).** These tests have **no external reference output**: no released simulation or dataset records what this model "should" do under a 150/150 sugar plus bitter drive, a 150 Hz water drive, or a matched-count bilateral drive. They are **measurements of our frozen model's own responses** under registered drive conventions, not a reproduction, not a benchmark, and not biological validation. The sugar anchor (section 8.1) touches validated ground only indirectly, through our own frozen implementation's realised values. Nothing here is evidence about a living fly, animal electrophysiology, or animal behaviour, and no report may word it that way. Every MN9 number from these tests is reported with its "RQ-C5 open" label until this gate closes (section 10).

## 2. The validated envelope, stated before the design

Part 3 certified exactly one stimulus configuration: **the right sugar GRN set (21 neurons) driven at 200 Hz**, brain-only, against Shiu et al.'s simulation output. That is the whole of the validated envelope. A 150 Hz sugar drive, any bitter or water drive at any rate, any combined drive, and any bilateral or unilateral matched-count drive are **OUTSIDE THE VALIDATED ENVELOPE**, and every result of these tests that uses them is labelled that way wherever it appears. These tests do not extend the envelope. Measuring a response is not validating it.

## 3. The conditions and the drive conventions

All runs use the frozen implementation's drive mechanism exactly as read at Parts 2 to 3: Poisson drive per driven neuron; each event injects `w_syn x f_poi` = 0.275 mV x 250 = **68.75 mV directly into `v`**; driven neurons' refractory variable set to 0 while driven; dt = 0.1 ms, `method='linear'`; fresh network build per trial; all 127,400 v630 neurons; all 14,687,178 edges; weight = count x sign x 0.275 mV; **no synapse threshold**; every spike of every neuron recorded. Trial duration 1.0 s; **N = 30 trials per run** (section 4).

| # | Run | Driven population(s) (`id_sets_v1`) | Rate |
|---|---|---|---|
| A | Sugar anchor | `sugar_grn_right` (21 right-hemisphere labellar sugar GRNs) | 200 Hz |
| 1 | Sugar plus bitter 150/150 | `sugar_grn_right` (21) **and** `bitter_grn` (21), simultaneously | 150 Hz each |
| 2 | Water 150 | `water_grn` (18 water GRNs) | 150 Hz |
| 3a | Bilateral matched | `sugar_grn_left` (10) **and** a 10-neuron subset of `sugar_grn_right`, simultaneously | 200 Hz each |
| 3b | Left-only matched | `sugar_grn_left` (10) | 200 Hz |
| 3c | Right-only matched | the same 10-neuron subset of `sugar_grn_right` as 3a | 200 Hz |

**The 10-neuron right subset (test 3) (PROPOSED)** *(reasoning: the subset must be chosen before any test 3 trial runs, by a rule that cannot favour either side, and it must be recorded where the panel can check it. A random subsample is unbiased; a deterministic rule such as the lowest 10 flywire IDs is auditable without a draw but risks an anatomical correlate of ID order that I cannot check from the record. I propose the random subsample, drawn once with numpy `default_rng` seed **20261134**, and the 10 IDs recorded in the freeze record before any trial runs. The panel rules on the method; if it prefers the deterministic rule, the document is amended to state it before the freeze.)* The subset is used identically in runs 3a and 3c, so the bilateral and right-only matched runs differ only in whether the left set is also driven. The left set is used whole (all 10) in runs 3a and 3b, so the left side needs no subset rule.

**Laterality, stated.** The bitter and water sets are used exactly as extracted, the upstream notebooks' single un-split lists, with no hemisphere assigned, because that is what the source records. No hemispheric composition is asserted for them. The sugar sets are split by hemisphere in the source (right 21, left 10), and test 3 uses that split.

**The 150 Hz convention for tests 1 and 2, stated honestly.** 150 Hz is the old build's 1 s suite rate, and the upstream model's own default drive rate. It is the rate the comparison must match to discriminate the rate explanation from a build difference. It is not claimed as biologically correct, and no reference exists to establish it against. Test 1 varies both drives together (sugar 150 plus bitter 150), so it matches no rung of the dose-response ladder (which varies bitter only, sugar fixed at 200 Hz); that is the point of the test, because the old run varied both together too.

## 4. Design

One run of the frozen runner (`src/brain_model/runner.py`, the Part 3 frozen runner path in the restructured repo) per condition, configured as:

| Config element | Anchor (A) | Test 1 (150/150) | Test 2 (water 150) | Test 3a (bilateral matched) | Test 3b (left-only) | Test 3c (right-only) |
|---|---|---|---|---|---|---|
| `run_id` | `part6-tests-anchor` | `part6-tests-sugarbitter150` | `part6-tests-water150` | `part6-tests-bilateral-matched` | `part6-tests-left-only` | `part6-tests-right-only` |
| Stimulus | one entry: `sugar_grn_right`, 200 Hz | two entries: `sugar_grn_right` 150 Hz + `bitter_grn` 150 Hz | one entry: `water_grn`, 150 Hz | two entries: `sugar_grn_left` 200 Hz + right subset 200 Hz | one entry: `sugar_grn_left`, 200 Hz | one entry: right subset, 200 Hz |
| Laterality | Right sugar set; left set not driven | Right sugar set + un-split bitter list | Un-split list (`neu_water`); no laterality recorded | Both sugar sets, counts matched 10 + 10 | Left sugar set only | Right subset only |
| Blocks | none | none | none | none | none | none |
| `duration_ms` | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 |
| `n_trials` | 30 | 30 | 30 | 30 | 30 | 30 |
| Base `seed` | 7000 | 7030 | 7060 | 7090 | 7120 | 7150 |
| Trial seeds | 7000-7029 | 7030-7059 | 7060-7089 | 7090-7119 | 7120-7149 | 7150-7179 |

**Why 30 trials.** Every comparison these tests make is against a 30-trial quantity (the fresh rung's conditions) or a 10-trial quantity (the old 1 s suite). Matching the 30-trial N keeps the sampling precision comparable with the fresh side of every comparison, and 30 exceeds Part 0's confirmatory floor (N = 20 seeds).

**Seed semantics.** As the Part 3 preregistration section 4: each seed initialises all stochastic components of its trial (in this model the only stochastic component is the Poisson drive), the runner derives trial seeds as base seed + trial index, per-trial streams are independent, and a trial's output is reproducible from its own seed alone. The seed lists are fixed by this document, published before any run, and **not** subject to re-rolling: a trial whose output looks odd stays in.

**Seed-block allocation (fixed here, in advance) (PROPOSED)** *(reasoning: one auditable 70xx-71xx range for everything this gate touches, disjoint from every prior block)*. **7000-7029** anchor; **7030-7059** test 1; **7060-7089** test 2; **7090-7119** test 3a; **7120-7149** test 3b; **7150-7179** test 3c; **7180** the determinism engineering check (below). Disjoint from: Part 3's blocks (3000-3029 primary, 3030-3059 arm, 3060-3089 extension, 9999 determinism), Part 2's runs (seed 0; 41xx/42xx), Part 5's blocks (5000s, including arm (e)'s 5800-5819), and the rung's blocks (6100-6379, 6220 determinism). No seed is used by more than one run, and no seed is re-rolled.

**Determinism (pre-declared engineering check, not a gate trial).** Before the condition runs and after the freeze (section 12 item 6): run_id `part6-tests-determinism-check` runs two independent 1-trial runs of the anchor configuration at seed **7180** under the frozen implementation; the two spike tables must be **bit-identical** (equal SHA-256). If they differ, STOP and diagnose. A determinism failure voids the frozen implementation's reproducibility claim and blocks the condition runs.

**Run order (fixed here).** Determinism check, then **anchor** (A), then the anchor evaluated (section 8.1), then **test 1**, then **test 2**, then **test 3a**, then **test 3b**, then **test 3c**. The anchor runs first so the stop rule is evaluated before the remaining compute is spent. Test 3's runs sit last because they depend on the subset draw (section 3), which is recorded at the freeze; the draw itself happens before any trial runs, at section 12 item 5.

**Wall-clock, measured basis, projected totals.** The per-condition figure is **measured, not estimated**: the Part 3 primary run, same code path, same full network, 30 trials x 1.0 s, took **2,094.6 s, about 35 min** of wall clock for its 30 trials, and about 35 min per 30-trial condition is the measured rate every figure in this paragraph is built on. Six runs project to **about 3.5 h** (about 3.1 to 3.9 h across the plausible range; the VM is shared and contention stretches wall-clock, not correctness). The determinism check adds two single trials (minutes). This is nowhere near the GPU trigger (14 days / 72 h per family, Part 0 section 4). The CPU reference platform stands, and K4 is not implicated.

**Run integrity.** The runner refuses a non-empty run directory, so a crashed or partial attempt voids the run: the attempt is logged, and the re-run takes a new `run_id`. No partial trial sets are ever analysed.

## 5. Outputs and run records

Each run produces `spikes.parquet` + `manifest.json` in its own run directory, in the shared spike-table schema (`t, trial, flywire_id, exp_name`). **A run counts under this preregistration only if its manifest shows this gate's freeze commit (section 12) and `dirty=False`** (the Part 3 preregistration section 5 rule, unchanged). A run under any other revision, or with a dirty tree, is a different revision's output and is reported as such; the dirt, if any, is named file by file in the results report, never tidied away after the fact.

## 6. Firing-rate computation

Identical to the four-conditions rung's section 6, so these tests' numbers are commensurable with the rung's:

- Per neuron, per trial: spike count with 0 <= t < 1.0 s, divided by 1.0 s, giving rate in Hz. (Every trial is exactly 1.0 s in every run.)
- Per neuron: the **mean of the 30 per-trial rates**, per run.
- **No burn-in, no transient trimming.** The onset transient from the resting start is part of every output, on the same terms as the rung.
- **Inactive neurons are explicit zeros.** Rate tables are built over all 127,400 v630 IDs; a neuron absent from a run's spike table has rate 0 in every trial of that run.

## 7. Comparison sets and statistics

**Active sets.** A neuron is *active* in a run if and only if it emits **at least one spike across that run's full 30-trial window**, equivalently mean rate **> 0 Hz** (one spike in 30 s is about 0.033 Hz), the Part 3 preregistration section 7 definition, unchanged. Per run, the active count is reported at the primary definition **and** at the two further thresholds the ladder pre-declared, **0.1 Hz** and **1 Hz** mean rate, so the set-size reporting stays comparable across rungs.

**MN9 endpoints.** MN9 left (720575940660219265) and right (720575940645521262), reported **separately, always**: per run, per-trial rates, mean, and **95% CI by percentile bootstrap over trials, 10,000 resamples**, computed identically for every run. Fixed bootstrap seed **20261131**, declared here in advance, serving all MN9 CIs in this document (**PROPOSED**) *(reasoning: Part 3's discipline is one declared-in-advance seed per bootstrap purpose; 20261131 continues the 202611xx sequence without reusing 20261123 (splits), 20261124 (Part 3 MN9), or the rung's seeds 20261127 to 20261130)*. The same seed serves the anchor differences of section 8.1 and the test 1 and test 2 comparisons against the old values.

**Driven-population readout (manipulation check, reported, not a criterion).** Under this model's drive a driven neuron fires at close to the Poisson rate by construction, so each run's driven set's own mean firing rate reads out the drive actually delivered. Per run, the mean rate of each driven population is reported (test 1 reports both), alongside the mean rates of the non-driven GRN populations. A driven set firing far from its registered rate is a diagnosis-path fact (section 9), not a verdict input: no claim in section 8 is decided by it, and it may not be promoted into a criterion after the fact.

**The test 1 suppression ratio.** Per trial, the **pooled MN9 rate** is (MN9 L spikes + MN9 R spikes) / 1.0 s, the sum of the two per-side rates (the same quantity Part 5's chain calls the pooled rate). The **suppression ratio** is (mean pooled MN9 rate in test 1) divided by (mean pooled MN9 rate in the **anchor**), with a **95% CI by percentile bootstrap over trials within each run, 10,000 resamples**, fixed bootstrap seed **20261132**, declared here in advance (**PROPOSED**) *(reasoning: a separate declared seed for the ratio, so the headline's resampling stream is independent of the MN9-CI stream and auditable on its own)*. The ratio is the **ratio of run means**; its CI comes from resampling trials **independently within each run**. Per-side ratios (L: test 1 divided by anchor on MN9 L; R likewise) are computed by the same procedure and **reported alongside**, descriptively: they are not the headline and not part of any claim rule. Note the denominator: the anchor is the sugar condition at 200 Hz, so this ratio is suppression at 150/150 **relative to sugar at 200 Hz**, and it is **not** directly comparable to the rung's headline ratio (sugar plus bitter 200/200 divided by sugar 200 Hz, 0.126) or to the old ratio (0.164, sugar plus bitter 150/150 divided by sugar 150 Hz, 23.3 over 142.2 Hz). The comparison against the old ratio in section 8.2 is made on the **MN9 rates themselves**, not by equating ratios with different denominators; the ratio is reported here so the size of suppression at 150/150 is on record in the same form as the rung's.

**The test 3 matched-count comparisons.** Within run 3a, the per-trial paired difference Δ = (MN9 L rate) minus (MN9 R rate) in the same trial, with a **95% CI by percentile bootstrap over trials, 10,000 resamples**, fixed bootstrap seed **20261133**, declared here in advance (**PROPOSED**) *(reasoning: the paired difference is test 3's deciding quantity, so it gets its own declared seed, separate from the MN9-CI stream and the ratio stream)*. The same seed serves the unilateral-pair comparison: Δ = (MN9 L rate in run 3b) minus (MN9 R rate in run 3c), with its 95% CI by percentile bootstrap over trials within each run, 10,000 resamples. The two runs use independent seed blocks (section 4), so no real pairing exists between them: trial-index pairing is **only a bookkeeping convention** for laying the two trial lists side by side, and nothing here averages per-trial ratios. The pooled MN9 mean of run 3a is reported alongside the bilateral secondary condition (v)'s pooled mean (L 93.17 plus R 64.87 Hz) for magnitude comparison only, descriptively, never pooled.

## 8. Decision rules

This gate is a measurement gate, not a benchmark: it has exactly one stop rule (the anchor, section 8.1) and one pre-written reading per test (sections 8.2 to 8.4). There is no gate-level PASS or FAIL beyond the anchor, and no outcome of sections 8.2 to 8.4 makes the gate "fail". Each test carries its own pre-stated reading, including *inconclusive*.

### 8.1 The anchor check (stop rule)

For each of L and R, let Δ = (this gate's anchor mean MN9 rate) minus (the Part 3 primary run's mean MN9 rate), where the Part 3 primary values are **L 92.57 Hz, R 62.40 Hz** (the reference file's own values, L 93.27 / R 61.80 Hz, are reported alongside for context but are **not** the anchor). The 95% CI for each Δ is computed by percentile bootstrap over trials on both sides (10,000 resamples, seed 20261131, section 7).

**The anchor passes if and only if:** both Δ CIs lie **entirely within the Part 0 band** (plus or minus 25 percent of the comparison value, or plus or minus 5 Hz, whichever is wider) applied to the Part 3 primary means, numerically **plus or minus 23.1 Hz for L** (25 percent of 92.57) and **plus or minus 15.6 Hz for R** (25 percent of 62.40); the plus or minus 5 Hz floor is not binding for either neuron, **and** the L over R ordering of the anchor's point estimates is preserved.

**If the anchor fails: STOP.** The gate does not complete. Any runs already made are quarantined as diagnostic outputs, they are not gate results and may not be reported as such, and the diagnosis path (section 9) runs before anything else. The failure is a statement about the frozen implementation's reproducibility under this freeze, and it goes to the HARD gate: no Part 7 reliance may be placed on these tests, and no re-run of the anchor under new seeds is permitted to convert the failure (seeds are never re-rolled, section 4).

**Non-gating report.** The anchor's Δ and its 95% CI are reported relative to zero in the results report, alongside the band check. If either side's Δ CI **excludes 0 by more than 5 Hz** (its nearer endpoint lies beyond plus or minus 5 Hz), that is reported to the panel as a **discrepancy**, an unexplained shift in the frozen implementation's output that sampling noise alone does not explain. It **does not** trigger STOP and does not change the anchor's pass or fail verdict: the plus or minus 25 percent band remains the gate, because a STOP is costly and the band is the pre-registered gate; the discrepancy rule exists so a shift of about 20 Hz inside the band is never silently passed.

### 8.2 Test 1 (D2/D4): does the rate explain the sugar plus bitter size gap?

The registered agreement rule (Part 0: the old point estimate inside the fresh CI, **or vice versa**) is applied per side to the test 1 MN9 means against the old 1 s suite values (10 trials, 1.0 s): L **9.1 Hz, CI [6.54, 11.66]**; R **14.2 Hz, CI [13.04, 15.36]**. The pooled ratio is read against the old pooled ratio **0.164** (23.3 over 142.2 Hz, a point from pooled means, with no CI): the ratio **agrees** if 0.164 lies inside the test 1 ratio's 95% CI (section 7), and **disagrees** if it lies outside it.

- **"Rate explains D2/D4"** if and only if the R side agrees **and** the pooled ratio agrees. (The L side already agreed at 200/200; if it disagrees at 150/150, that is reported as a separate finding and does not change this reading.)
- **"Rate does not explain D2/D4"** if and only if the R side disagrees in the fresh direction (the test 1 R mean sits near the fresh 200/200 R mean of 9.57 Hz, outside the old CI) **and** the pooled ratio disagrees (0.164 outside the test 1 ratio CI).
- **Otherwise inconclusive.** The numbers are reported per side and for the ratio, and the gate records that the rate explanation is neither established nor excluded.

The test 1 ratio is also tabulated against the dose-response ladder (0.573 at bitter 100 Hz, 0.330 at bitter 150 Hz, 0.126 at bitter 200 Hz, sugar fixed at 200 Hz throughout) descriptively, for magnitude only: test 1 varies both drives together, so it sits on no rung of that ladder, and no ladder comparison decides this test.

### 8.3 Test 2 (D3): does the rate explain the water size gap?

The registered agreement rule is applied per side to the test 2 MN9 means against the old 1 s suite values (10 trials, 1.0 s): L **6.0 Hz, CI [3.55, 8.45]**; R **1.6 Hz, CI [0.08, 3.12]**.

- **"Rate explains D3"** if and only if **both** sides agree.
- **"Rate does not explain D3"** if and only if **both** sides disagree in the fresh direction (the test 2 means sit near the fresh 200 Hz means, L 30.23 Hz and R 11.87 Hz, outside the old CIs).
- **Otherwise inconclusive**, reported per side. A split (one side agrees, the other does not) is reported as the finding it is, not averaged away.

Water carries no confirmatory claim anywhere in this project: this test is a measurement with a pre-written reading, not a PASS or FAIL. Its outcome decides only the D3 reading above, and the water number itself stays descriptive, outside the validated envelope, whatever the outcome.

### 8.4 Test 3 (D7/RQ-C5): does the asymmetry survive matched counts?

The deciding quantity is the bilateral matched Δ (section 7): the per-trial paired L minus R difference in run 3a, with its 95% CI.

- **"Resolved as a set-size artefact"** if and only if the bilateral matched Δ 95% CI **includes 0** and the unilateral-pair Δ 95% CI **includes 0**. The two tests must agree: bilateral matched counts give no asymmetry, and each side alone drives its own MN9 equally at matched counts.
- **"Resolved as a circuit property"** if and only if the bilateral matched Δ 95% CI **excludes 0** in the L over R direction, and the unilateral-pair Δ 95% CI **excludes 0** in the same direction. The asymmetry then survives matched counts on both tests, and the gap sizes are reported with their CIs as the resolved size of the asymmetry.
- **Otherwise the question stays open.** In particular: if the two tests disagree (one includes 0, the other excludes it), or if either CI is wide enough that its reading is fragile, RQ-C5 is **not** resolved by this gate. Both results are reported, the question stays open, and the MN9 numbers stay provisional under the section 10 labelling rule. No post-hoc combination of the two tests may be invented at report time to force a resolution.

The bilateral matched pooled mean is reported against condition (v)'s pooled mean descriptively, for magnitude only. No claim is registered on the pooled comparison.

### 8.5 What completion means

The gate **completes** when: the determinism check has passed; all six runs have run under the freeze with clean manifests (section 5); the anchor has passed (section 8.1); and every comparison of sections 8.2 to 8.4 has been reported under its pre-stated rule, with the section 7 tables complete. Completion is what Part 7's prerequisite requires: Part 7 may lean on MN9 numbers only once this gate has completed and its readings are recorded. Completion does not require any particular outcome: a "rate does not explain" or an unresolved RQ-C5 is a legitimate, reportable result of the gate, and it constrains Part 7's claims rather than blocking Part 7 outright.

## 9. On anchor failure: the diagnosis path

Per the plan's discrepancy rule: STOP, log, diagnose, in this pre-set order, each step's outcome recorded before the next begins (the four-conditions rung's section 9 order, adapted to a reproducibility failure):

1. **The analysis code first.** The gate's analysis script is re-verified on synthetic spike tables with known rates and a known suppression ratio (including a ratio of exactly 1 and a suppressed case). A bug in the measuring instrument is the cheapest explanation and is excluded first.
2. **Run provenance.** The anchor run's manifest: this gate's freeze commit, dirty flag, data hashes, environment. Any deviation voids the run, not the implementation.
3. **The driven set.** The 21 driven IDs and their Brian indices re-checked against `id_sets_v1`.
4. **The drive.** Rate, kick size (68.75 mV into `v`), and refractory handling re-read against the reading log and the frozen code; the section 7 driven-population readout is evidence here.
5. **The weights.** The sampled sign audit re-run; loader counts re-verified.
6. **The numerics.** dt, integration method, reset string re-checked against the spec.
7. **Only then**, freeze-integrity explanations (for example, the implementation inside this gate's freeze commit is not in fact byte-identical to `0cb9b81` despite the section 12 check, or an environment difference), and only with evidence, not as a resting place.

**No parameter is re-fit during diagnosis.** `w_syn` stays at the paper's 0.275 mV and every other parameter at its reading-log value; any proposal to change a parameter is a formal amendment that voids this gate's confirmatory status and must say so. K1 is **not** re-implicated by this gate: it was the sugarR rung's criterion and that rung is closed. But an anchor failure that survives diagnosis is a freeze-integrity finding, and it blocks Part 7 (whose prerequisite this gate is) until the HARD gate decides what it means.

## 10. RQ-C5 handling

**The question stays open until this gate closes.** RQ-C5 (whether the L over R MN9 asymmetry under sugar drive is a circuit property, an artefact of the unequal GRN set sizes, or a bug) is unresolved in both builds at the time this document is written. This gate's test 3 is the registered resolution design (PLAN line 301), and its section 8.4 rule is the only route to a resolution in this gate. Until the gate closes, every public MN9 figure is labelled **"RQ-C5 open"**, per the Part 6 gate's item 4 decision (logged deviation with my explicit ratification, recorded in `docs/decisions_log.md`). That labelling rule binds every report, figure and summary that cites an MN9 number from this gate, and every Part 7 document that leans on one.

**What test 3 may and may not support.** What it may support: whether the asymmetry *appears* at matched counts, and how large it is, per section 8.4's rule. What it may not support: any claim about *why* beyond the two pre-written readings (set-size artefact or circuit property). The per-side ratios and the pooled means travel with the headline precisely so no pooled number can hide a side-specific story.

## 11. Reporting commitments for these tests

- Results are reported in **`docs/discriminating_tests_results.md`**, in the style of the rung results report: a freeze-and-run record table (section 12 items in order, with commit, tag, hashes, timestamps, determinism outcome, per-run manifests and wall clocks); the anchor check (section 8.1) reported in full, before the test results; per-run headline tables (active counts at the three section 7 thresholds; MN9 L/R means with CIs; driven-population readouts); each test's reading under its pre-stated rule, with the numbers adjacent to the words; and a deviations section logging **every** deviation from this document, however small, with its consequence stated.
- **Anchor discrepancy reporting.** If the section 8.1 non-gating discrepancy rule triggers (either side's Δ CI excludes 0 by more than 5 Hz), the discrepancy is reported in `docs/discriminating_tests_results.md` **under its own heading**, alongside the band check, with Δ, its CI, and the panel referral stated, not folded into the anchor verdict.
- Language per section 1: measurement of the frozen model's responses. Test 1, test 2 and test 3 results are labelled **model responses under conventional drives, outside the validated envelope** (section 2) in every report, figure and summary, including any Part 7 document that cites them.
- Until the HARD gate closes on these tests, their results carry the label *computed per preregistration, gate pending* in every summary (the Part 3 results report's section 5 discipline).
- Any amendment to this document after approval follows the header rule: logged, panel-reviewed, Angelic-approved, and results already seen are still reported under the rules that were in force when they were produced.

## 12. Freeze checklist, before any trial runs

No trial runs until every item here is done, in order:

1. **This preregistration is approved.** Full panel review complete and Angelic's explicit approval recorded in the Amendment history below. **OPEN ITEM, not pre-decided:** the expert-check condition (D6) for this freeze. The waiver Angelic signed on 24 Nov 2026 covers the Part 5 freeze and the four-conditions rung freeze only; it does not cover this gate. This freeze needs either a new signed waiver in the same form, or the human domain-expert check itself. That is Angelic's call, recorded here, and it is made before the freeze, not after results exist.
2. **Commit and tag.** The approved preregistration is committed in the working clone and tagged. The first freeze tag for this gate will be created on the approved version of this document and named **`part6-tests-v1`** (**PROPOSED**) *(reasoning: this gate's own tag sequence, so no tag ever implies an earlier document was re-frozen; the Part 3 and rung sequences stand untouched)*. The tag is created only after approval; the tag name, commit hash and timestamp are recorded in the freeze record by dated note. If the preregistration changes afterwards, a new tag (`part6-tests-v2`, ...) is created. A tag is never moved or deleted.
3. **Frozen-implementation identity verified.** The freeze commit contains the implementation byte-identical to `0cb9b81` (empty `git diff` over the brain-model source, tests and run scripts, recorded); the Part 1 data-file hashes are re-verified against the Part 3 freeze record.
4. **Harness hash recorded and synthetically tested.** The gate's analysis script is hashed and the hash recorded in the run record; before it touches real outputs it is verified on synthetic spike tables with known rates and known suppression ratios (section 9 step 1's cases, run in advance as a harness test).
5. **Right subset drawn and recorded.** The test 3 right subset (section 3) is drawn by the approved method and its 10 IDs recorded in the freeze record, before any trial runs. If the panel prefers the deterministic rule, the document is amended to state it and the subset is fixed by that rule instead.
6. **Determinism check passed.** Two independent 1-trial runs of the anchor configuration at seed 7180 under the frozen implementation produce bit-identical spike tables (equal SHA-256). If they differ, STOP and diagnose before any condition runs.
7. **Run order and seed blocks confirmed.** The section 4 run order and seed blocks are confirmed against this document before the first run, and the freeze record states them.

## Amendment history

- **DRAFT, 25 Nov 2026.** Written after the Part 6 gate closed (decision (c) hybrid, itemised; section 17 item 2: the three tests run as their own preregistration gate before Part 7 leans on any MN9 numbers). Not yet panel-reviewed, not yet approved, not frozen. The PROPOSED items awaiting the panel's ruling: the 10-neuron right-subset method (section 3), the seed blocks (section 4), the bootstrap seeds 20261131 to 20261134 (sections 3 and 7), the freeze tag name `part6-tests-v1` (section 12 item 2). The OPEN item awaiting Angelic's call: the expert-check condition for this freeze (section 12 item 1).
