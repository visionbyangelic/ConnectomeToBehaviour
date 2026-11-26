# Discriminating-tests results: the Part 6 gate's three tests (D2/D4, D3, D7)

**Status: computed per preregistration, gate pending (26 Nov 2026).** The numbers below are computed exactly per the preregistration (`docs/discriminating_tests_preregistration.md`, freeze tag `part6-tests-v1`); the HARD gate on these tests has not closed, and the panel review and my sign-off are pending. **Headline as computed: the anchor passed; test 1 is inconclusive (a partial rate effect); test 2 reads "rate explains D3"; test 3 reads "asymmetry persists under the tested matched-count configurations".** The gate completes under section 8.5 on its four conditions (determinism passed, seven runs under the freeze with clean manifests, anchor passed, every comparison reported under its pre-stated rule); completion is what Part 7's prerequisite requires, and the gate itself closes on the panel review and my sign-off.

**RQ-C5 open: every MN9 number in this report is provisional until this gate closes (preregistration section 10).** The label applies to every MN9 table and reading below, and is repeated at each table.

**Amended 26 Nov 2026, afternoon, twice: after Reviewer 3's REQUIRE CHANGES review (Deviations, item 2) and after his re-review (Deviations, item 4).** No headline reading and no previously reported number changed; the amendments add readouts, an audit table, a provenance record and the prominent RQ-C5 label.

**Language discipline (preregistration sections 1, 2, 11, binding).** These tests have no external reference output. Everything here is a **measurement of my frozen model's own responses** under the registered drive conventions: not a reproduction, not a benchmark, and not biological validation. Only the anchor touches validated ground, and only indirectly, through the anchor check (section 8.1) against my own frozen implementation's realised Part 3 output. The test 1, test 2 and test 3 results are **model responses under conventional drives, outside the validated envelope**, and are labelled that way throughout. Nothing in this report is evidence about a living fly, animal electrophysiology, or animal behaviour.

## 1. Freeze and run record

| Item | Record |
|---|---|
| Approval (§12 item 1) | Panel complete on the amended draft at commit `d5822d9` (SHA-256 `60ba4572ac88d4a9b82b67d901023ca390578529c4beb5b7427a287bc944bf78`, 211 lines): Reviewer 1 PASS on this version, Reviewer 2 CONFIRM of the changed passages, Reviewer 3 PASS of the changed passages. I approved the freeze 26 Nov 2026, 06:36 WAT. The expert-check condition (D6) for this freeze is resolved by my signed waiver of 25 Nov 2026, 22:53 WAT (scope: the discriminating-tests freeze only; the human expert check remains owed at the Part 8 final gate), with the dated scope-clarifying note in section 12 item 1 and in the freeze record. |
| Commit and tag (§12 item 2) | Freeze commit `1861238afd01cefdf83899b7e2fd61744024038f`, annotated tag `part6-tests-v1`, 26 Nov 2026, 06:41 WAT (`docs/discriminating_tests_freeze.md`). |
| Frozen implementation (§12 item 3) | Verified file by file against the Part 3 implementation freeze `0cb9b81` under the restructure mapping: every difference is from the restructure rename only (the runner differs by exactly one line, its entry-point string); the Brian group names are identifiers only and do not enter the numerics; all ID-set CSVs and the manifest are byte-identical. Part 1 data hashes re-verified (completeness `e6b71e17…`, connectivity `94db8c65…`, sugarR `83921d50…`); the loader re-verifies the two brain data files on every run and every manifest records their hashes, and the sugarR reference hash is recorded in the freeze record (the runner does not load the reference file, so it does not appear in the manifests). |
| Harness (§12 item 4) | Analysis script `work/analyze_part6_tests.py`, SHA-256 `1beb2cc04252d465122f2a1cccb1aa8b675d8f9cba677a594bb5f0da4dd2cba6`, verified on synthetic spike tables with known rates and a known suppression ratio (including a ratio of exactly 1 and a suppressed case) before touching any real output: **ALL PASS (13 cases)**, recorded in `work/part6_tests_harness_record.json`. One bug was found and fixed during the work; see Deviations, item 1. The run driver is `work/run_part6_tests.py` (a work harness script, not part of the frozen implementation). |
| Right subset (§12 item 5) | Drawn by the approved method at the freeze (`default_rng(20261134).choice(21, size=10, replace=False)`, indices `[12, 6, 2, 10, 4, 20, 5, 17, 3, 16]`, the 10 IDs in canonical order, numpy 1.26.4), with the left set's and the subset's cell-type labels and outgoing synapse totals recorded in the freeze record (all 20 are sugar GRNs; left total 2,295, mean 229.5; right subset total 3,016, mean 301.6). |
| Determinism check (§12 item 6) | **Passed.** Two independent 1-trial anchor runs at seed 7180, run_id `part6-tests-determinism-check`: spike tables bit-identical, SHA-256 `34f92769037913d06205b4369c04104b4821e7dd3362ed953fe8944775327427` (17,415 spikes, 412 active neurons each); both manifests at the freeze commit, clean tree. |
| Seed registry (§12 item 7) | Confirmed by script, not by hand: `work/part6_tests_seed_disjointness_check.py` (SHA-256 `530a4f136611e54ccaf650c006c5006bd152d588d11e9e33d2168934d4693295`), re-run at the freeze against the tagged text: **PASS, 53 blocks, 1210 seeds, all pairwise disjoint**; manifest scan 297 JSON files, 396 distinct seeds used, all inside listed blocks, none inside this gate's blocks. Output `work/part6_tests_seed_disjointness_output.txt` (SHA-256 `bb079c250c3ebd20b63db5c06874397aabd545ee9cf2fe2d7fda21122b727a25`). |
| Analysis outputs | `work/part6_tests_analysis.json` (machine-readable, complete), `work/part6_tests_harness_record.json`, `work/part6_tests_run_record.json`. Bootstrap seeds as preregistered: 20261131 (MN9 CIs, anchor differences, S-versus-arm D), 20261132 (descriptive ratio), 20261133 (test 3 deltas, 95% and 90% CIs), 20261135 (protocol-matched ratio), 20261136 (old ratio CI, recomputed); 10,000 resamples throughout. |

**Per-run manifest audit (added 26 Nov 2026, afternoon, Reviewer 3 item R3-3).** Every completed run's manifest, checked individually. The manifest's recorded timestamp is its creation time (UTC; WAT is UTC plus 1 hour) at completion; the run's start is that timestamp minus its wall clock, derived, not separately recorded. All nine manifests record the freeze commit `1861238…` with a clean tree, the registered trial seeds, and the two brain data hashes (completeness `e6b71e17…`, connectivity `94db8c65…`) matching the freeze record. The sugarR reference hash (`83921d50…`) is recorded in the freeze record, not in the manifests: the runner does not load the reference file, so it does not appear there. The spike SHA-256 is the hash of that run's `spikes.parquet` as recorded in its manifest.

| Run | Manifest SHA-256 | Commit / dirty | Seeds | Created (UTC) | Wall (s) | Spike SHA-256 |
|---|---|---|---|---|---|---|
| Anchor (`part6-tests-anchor-rerun2`) | `0bc1428aaa16e242c9d4e6310b8a4673dfdde77c18d81ec09e36c0dec96e8e48` | `1861238…` / clean | 7000-7029 | 2026-11-26 06:48:13 | 694.46 | `dc90dc86…` |
| Test 1 (`part6-tests-sugarbitter150-rerun1`) | `441311bb437901e215a4f244dae24ac1b26bdc6ec488cc542841bb0d88aa1662` | `1861238…` / clean | 7030-7059 | 2026-11-26 08:01:23 | 1745.49 | `f1d0a284…` |
| Sugar 150 control (`part6-tests-sugar150`) | `53d48a8142afcf7f48c6f317188e0e9afd28ef4045e2a8f48fb8d13b078d1b93` | `1861238…` / clean | 7190-7219 | 2026-11-26 08:33:39 | 1836.27 | `406366e1…` |
| Test 2 (`part6-tests-water150`) | `ee77fe0a0520128f0555d19de5ed3e4f00c16b2ec06c7c861b74bf4b187c7e3c` | `1861238…` / clean | 7060-7089 | 2026-11-26 09:09:18 | 2008.42 | `f1d775fb…` |
| Test 3a (`part6-tests-bilateral-matched`) | `de4575de9696cb49a77419ebe3eaaf6b9efb4a390ecde4d430fe2452be9f36ef` | `1861238…` / clean | 7090-7119 | 2026-11-26 09:44:16 | 2029.28 | `7ce2d998…` |
| Test 3b (`part6-tests-left-only`) | `2709b6d48b0415a7d8caee4f9513bc9d6851215735df0923b9fc7886026af5f1` | `1861238…` / clean | 7120-7149 | 2026-11-26 09:56:12 | 639.35 | `50467ae4…` |
| Test 3c (`part6-tests-right-only`) | `9315d980988416534c39af4b6234c8f8072b433b8f5dce6b13b4af58cc009401` | `1861238…` / clean | 7150-7179 | 2026-11-26 10:00:13 | 215.82 | `35347171…` |
| Determinism, first (`part6-tests-determinism-check`, out-root `part6-tests-det-a`) | `479acec49c22d900c70fb917f7e908a18f8cc04eed46c74be8877291471ee3cf` | `1861238…` / clean | 7180 | 2026-11-26 05:46:07 | 8.24 | `34f92769…` |
| Determinism, second (`part6-tests-determinism-check`, out-root `part6-tests-det-b`) | `3d1d256d8f3e1defb4ff35204db38217aa9da224ab835476ab89dc7cd0c35c5e` | `1861238…` / clean | 7180 | 2026-11-26 05:46:29 | 9.79 | `34f92769…` |

The two determinism runs record the same spike SHA-256 (`34f92769…`), which is the bit-identity check of section 12 item 6. The wall clocks here are the manifests' exact values; section 3 rounds them to one decimal.

## 2. How section 5 was satisfied for the runs (declared arrangement)

All seven runs executed from a git worktree pinned at the freeze commit (`~/workspace/connectome-work/part6-tests-worktree`, detached HEAD `1861238…`, clean tree). The main tree's HEAD was already one commit past the freeze commit when the runs started (the dated-note commit `816b8ae`), so a main-tree run would have recorded a manifest commit other than the freeze commit and would not have counted under section 5. This is the rung's Addendum 2 arrangement: the frozen runner derives the manifest's git info from the code's own repo root, so every worktree run's manifest records the freeze commit and `working_tree_dirty = false`, which is section 5 satisfied as written. Code and id sets came from the worktree (byte-identical to the freeze commit); `data_dir` pointed at the main repo's hash-verified Part 1 data (the `data/` directory is untracked, so the worktree has none); outputs landed in the main repo's `results/validation/runs/`. Every manifest below was checked individually: freeze commit, clean tree, registered trial seeds, data hashes matching the freeze record. The worktree itself was checked fresh against the tag on 26 Nov 2026, afternoon: its HEAD is the freeze commit `1861238…`, its tree is clean, there is no diff over `src/`, `data/neuron_sets/` and `tests/`, and its ID sets are byte-identical to the main repo's. Nothing was committed or pushed during the runs; the frozen tags are unmoved.

## 3. The runs

All runs: 30 trials x 1.0 s through the frozen runner, sequentially, no concurrent load. Wall clocks are the runner's recorded seconds. The seven completed runs took about 2.5 hours in total, under the section 4 projection of about 4.1 hours: the unilateral runs are much cheaper (only 10 GRNs driven), and the re-attempts ran faster on a warm Brian2 cache (see the void attempts below).

| Condition | run_id | Seeds | Spikes | Active (>0 / >=0.1 / >=1 Hz) | Wall (s) |
|---|---|---|---|---|---|
| Anchor | `part6-tests-anchor-rerun2` | 7000-7029 | 511,004 | 447 / 429 / 389 | 694.5 |
| Test 1 (sugar+bitter 150) | `part6-tests-sugarbitter150-rerun1` | 7030-7059 | 403,157 | 436 / 398 / 321 | 1,745.5 |
| Sugar 150 control (S) | `part6-tests-sugar150` | 7190-7219 | 410,800 | 439 / 408 / 363 | 1,836.3 |
| Test 2 (water 150) | `part6-tests-water150` | 7060-7089 | 156,536 | 285 / 184 / 115 | 2,008.4 |
| Test 3a (bilateral matched) | `part6-tests-bilateral-matched` | 7090-7119 | 430,758 | 463 / 423 / 382 | 2,029.3 |
| Test 3b (left-only) | `part6-tests-left-only` | 7120-7149 | 221,764 | 390 / 344 / 295 | 639.4 |
| Test 3c (right-only) | `part6-tests-right-only` | 7150-7179 | 252,460 | 384 / 364 / 326 | 215.8 |

**Void attempts (section 4 run integrity; each left an empty run directory, no partial trial set exists, and none is analysed).** Anchor attempt 1 (`part6-tests-anchor`): OOM-killed by the kernel about 35.7 min in, near the expected completion; re-attempted as `part6-tests-anchor-rerun1`, which was itself killed about 11.5 min in by a runtime restart (RSS 2.34 GB, not an OOM); re-attempted again as `part6-tests-anchor-rerun2`, same seeds. Test 1 attempt 1 (`part6-tests-sugarbitter150`): OOM-killed about 40.8 min in, RSS about 5.2 GB, near the end of the 30 trials; re-attempted as `part6-tests-sugarbitter150-rerun1`, same seeds, which completed, wall clock 1,745.5 s, because the failed attempt had compiled that condition's code into the Brian2 cache. Each re-run took a new run_id with the same seeds, as section 4 requires; the attempts stay on record here and in `work/part6_tests_run_record.json`. All runs used `MALLOC_TRIM_THRESHOLD_=0`. Two non-void interruptions: the sugar 150 driver's session was interrupted by a runtime restart at about 08:35, after the run had written its files at 08:33, and the run was verified complete from the manifest on disk; one test 3a launch failed on a wrong working directory (no run started) and was relaunched correctly. No output from any voided attempt was inspected: each attempt left an empty run directory, so no partial output existed to inspect.

## 4. The anchor check (section 8.1): PASS

Against the Part 3 primary run's realised MN9 means (recomputed from its spike file: L 92.57 Hz, R 62.40 Hz). MN9 numbers below: RQ-C5 open.

| Side | This gate's anchor mean [95% CI] | Δ [95% CI] | Band (±25%) | Verdict |
|---|---|---|---|---|
| L | 92.27 Hz [90.57, 94.10] | -0.30 [-2.57, 2.07] | ±23.14 Hz | inside |
| R | 62.60 Hz [60.77, 64.37] | +0.20 [-2.53, 2.80] | ±15.60 Hz | inside |

L over R ordering preserved (92.27 above 62.60). **The anchor passes.** The non-gating discrepancy rule does not trigger (neither Δ CI excludes 0 by more than 5 Hz), so there is no discrepancy to report. The frozen implementation reproduces its own Part 3 output under this freeze almost exactly, and the gate proceeded past its only stop rule. Band constant, recorded for the record: the L band is ±23.1425 Hz, which is 25% of the rounded primary 92.57 Hz; 25% of the unrounded primary 92.5667 Hz is 23.1417 Hz, a difference under 0.001 Hz, immaterial to the verdict.

## 5. Per-run headline numbers

MN9 means are the mean of 30 per-trial rates (spike count in 0 <= t < 1.0 s, divided by 1.0 s), with 95% percentile bootstrap CIs (10,000 resamples, seed 20261131). Pooled is L plus R per trial. Driven readouts are the mean rate of each driven population over the 30 trials. All MN9 numbers in this section: RQ-C5 open.

| Run | MN9 L [95% CI] | MN9 R [95% CI] | Pooled | Driven readout |
|---|---|---|---|---|
| Anchor | 92.27 [90.57, 94.10] | 62.60 [60.77, 64.37] | 154.87 | sugar right 197.1 Hz |
| Test 1 (sugar+bitter 150) | 7.67 [6.73, 8.67] | 12.07 [11.17, 12.93] | 19.73 | sugar right 147.2 Hz, bitter 148.0 Hz |
| Sugar 150 control (S) | 82.63 [81.03, 84.23] | 58.33 [56.80, 59.93] | 140.97 | sugar right 148.5 Hz |
| Test 2 (water 150) | 4.87 [4.13, 5.70] | 0.77 [0.43, 1.13] | 5.63 | water 147.7 Hz, sugar right 0.29 Hz |
| Test 3a (bilateral matched) | 55.03 [53.00, 57.13] | 42.40 [40.83, 43.97] | 97.43 | sugar left 196.9 Hz, right subset 195.5 Hz (sugar right, all 21, 93.1 Hz) |
| Test 3b (left-only) | 40.73 [39.40, 42.03] | 52.00 [50.33, 53.73] | 92.73 | sugar left 195.3 Hz |
| Test 3c (right-only) | 55.40 [53.97, 56.97] | 34.70 [33.63, 35.83] | 90.10 | right subset 195.4 Hz (sugar right, all 21, 93.2 Hz) |

The driven readouts are all as expected: sugar right fires about 197 Hz at a 200 Hz drive and about 147 to 149 Hz at a 150 Hz drive; bitter and water fire about 148 Hz at a 150 Hz drive; the left set and the drawn right subset fire about 195 to 197 Hz at a 200 Hz drive. The two unilateral runs show the contralateral side firing above the ipsilateral side (left-only: R 52.00 above L 40.73; right-only: L 55.40 above R 34.70); that pattern is reported as observed, and no claim is made about it beyond the section 8.4 readings below.

**Non-driven GRN population readouts (added 26 Nov 2026, afternoon, Reviewer 3 item R3-2).** Preregistration section 7 requires the mean rate of each driven population alongside the mean rates of the non-driven GRN populations. The driven readouts are in the table above; the non-driven readouts are below, each the mean rate over that population's neurons across the 30 trials, by the same definition as the driven readouts.

| Run | Non-driven GRN populations: mean rate (Hz) |
|---|---|
| Anchor | sugar left 0.00, bitter 0.00, water 0.00, ir94e 0.00 |
| Test 1 (sugar+bitter 150) | sugar left 0.00, water 0.00, ir94e 0.00 |
| Sugar 150 control (S) | sugar left 0.00, bitter 0.00, water 0.00, ir94e 0.00 |
| Test 2 (water 150) | sugar right 0.29, sugar left 0.00, bitter 0.00, ir94e 0.00 |
| Test 3a (bilateral matched) | bitter 0.00, water 0.00, ir94e 0.00, undriven 11 right sugar GRNs 0.01 |
| Test 3b (left-only) | sugar right 0.00, bitter 0.00, water 0.00, ir94e 0.00 |
| Test 3c (right-only) | sugar left 0.00, bitter 0.00, water 0.00, ir94e 0.00, undriven 11 right sugar GRNs 0.21 |

The only non-zero readout among the wholly non-driven populations is the sugar right set at 0.29 Hz under water drive: the set is not driven in that run, so that rate is downstream activity, not drive. In runs 3a and 3c the sugar right population is partly driven (the drawn 10-neuron subset); the 11 undriven right sugar GRNs read 0.01 Hz and 0.21 Hz respectively, essentially silent, and the all-21 sugar right means (93.09 Hz and 93.17 Hz) are the mix of the driven subset and those 11.

## 6. Test 1 (D2/D4): does the rate explain the sugar plus bitter size gap?

Registered agreement rule (Part 0: the old point estimate inside the fresh CI, or vice versa), per side, against the old 1 s suite (10 trials, 1.0 s): L 9.1 Hz, CI [6.54, 11.66]; R 14.2 Hz, CI [13.04, 15.36]. The pooled ratio is read against the old pooled ratio 0.164 (23.3 over 142.2 Hz), whose 95% CI is [0.144, 0.185] (recomputed from the old suite's per-trial lists, seed 20261136: point 0.1639, CI [0.1444, 0.1853], matching the registered values), using the protocol-matched ratio only (test 1 pooled divided by the sugar 150 control pooled, seed 20261135). MN9 numbers below: RQ-C5 open.

| Quantity | Fresh value [95% CI] | Old value | Agreement |
|---|---|---|---|
| L | 7.67 [6.73, 8.67] | 9.1 [6.54, 11.66] | agrees (fresh point inside old CI) |
| R | 12.07 [11.17, 12.93] | 14.2 [13.04, 15.36] | does not agree (neither clause holds) |
| Protocol-matched ratio | 0.140 [0.129, 0.152] | 0.164 [0.144, 0.185] | disagrees (0.164 outside fresh CI; fresh point 0.140 below old CI) |
| Per-side ratio, L (descriptive) | 0.093 [0.081, 0.105] | no old per-side value (the old ratio is pooled only) | descriptive only, decides nothing |
| Per-side ratio, R (descriptive) | 0.207 [0.191, 0.223] | no old per-side value (the old ratio is pooled only) | descriptive only, decides nothing |
| Descriptive ratio vs 200 Hz anchor | 0.127 [0.117, 0.138] | 0.164 [0.144, 0.185] | reported alongside, decides nothing |

The per-side ratios (added 26 Nov 2026, afternoon, Reviewer 3 item R3-2) are the test 1 MN9 side mean divided by the sugar 150 control MN9 side mean, with 95% CIs by the same bootstrap procedure as the deciding ratio (10,000 resamples, seed 20261135, trials resampled independently within each run, ratio of run means). They are reported descriptively, per preregistration section 7, and are not part of any claim rule.

**Reading, in the registered wording: "Inconclusive (partial rate effect)".** The R side does not agree, but its mean (12.07 Hz) sits above 10.40 Hz (the upper end of the fresh 200/200 R CI [8.77, 10.40]) and below 13.04 Hz (the lower end of the old R CI), which is the named intermediate case: a partial rate effect. The partial-effect zone applies here because neither clause of the agreement rule holds for the R side or for the ratio. "Rate explains D2/D4" would need the R side to agree and the ratio to agree; "rate does not explain D2/D4" would need the R mean at or below 10.40 Hz and the ratio to disagree. Neither holds. The rate moved both the R side (9.57 Hz at 200/200 to 12.07 Hz at 150/150) and the ratio (0.126 at 200/200 to 0.140 protocol-matched) toward the old numbers without reaching agreement, and the gate records that the rate explanation is neither established nor excluded. For magnitude only, against the dose-response ladder (0.573 at bitter 100 Hz, 0.330 at bitter 150 Hz, 0.126 at bitter 200 Hz, sugar fixed at 200 Hz throughout): test 1 varies both drives together, so it sits on no rung of that ladder, and no ladder comparison decides this test.

## 7. Test 2 (D3): does the rate explain the water size gap?

Registered agreement rule, per side, against the old 1 s suite: L 6.0 Hz, CI [3.55, 8.45]; R 1.6 Hz, CI [0.08, 3.12]. MN9 numbers below: RQ-C5 open.

| Quantity | Fresh value [95% CI] | Old value | Agreement |
|---|---|---|---|
| L | 4.87 [4.13, 5.70] | 6.0 [3.55, 8.45] | agrees (fresh point inside old CI) |
| R | 0.77 [0.43, 1.13] | 1.6 [0.08, 3.12] | agrees (fresh point inside old CI) |

**Reading, in the registered wording: "Rate explains D3".** Both sides agree. The huge water disagreement from Part 6 (fresh 200 Hz L 30.23 Hz against old 6.0 Hz; R 11.87 Hz against old 1.6 Hz) was a rate effect: at the matched 150 Hz drive the fresh water numbers fall to L 4.87 Hz and R 0.77 Hz, inside the old intervals. Water carries no confirmatory claim anywhere in this project; this test is a measurement with a pre-written reading, and the water number itself stays descriptive, outside the validated envelope, whatever the outcome.

## 8. Test 3 (D7/RQ-C5): does the asymmetry survive matched counts?

The three deciding quantities (section 7, bootstrap seed 20261133). MN9 numbers below: RQ-C5 open.

| Quantity | Definition | Value [95% CI] | 90% CI | Percent of level |
|---|---|---|---|---|
| Δ_bilateral | Run 3a, paired L minus R | 12.63 [10.53, 14.77] | [10.83, 14.40] | 25.9% |
| Δ_ipsi | L in run 3b minus R in run 3c | 6.03 [4.33, 7.70] | [4.60, 7.43] | 16.0% |
| Δ_contra | R in run 3b minus L in run 3c | -3.40 [-5.70, -1.17] | [-5.33, -1.50] | 6.3% |

No Δ meets the section 7 equivalence criterion (no 90% CI lies entirely within [minus 5, plus 5] Hz). All three 95% CIs exclude 0 in the consistent direction: Δ_bilateral excludes 0 in the L over R direction; Δ_ipsi excludes 0 in the same direction (L in run 3b above R in run 3c); Δ_contra excludes 0 in the consistent direction (L in run 3c above R in run 3b, which is why its sign is negative). The overlap zone of the precedence rule does not apply (no Δ is near 2.5 to 2.9 Hz).

**Reading, in the registered wording: "Asymmetry persists under the tested matched-count configurations".** The asymmetry appears at matched counts, and its size under those configurations is 12.63 Hz on the bilateral comparison (25.9% of the level of 48.72 Hz). The matched-count bilateral gap (12.63 Hz) is descriptively smaller than the unmatched gap (28.30 Hz, condition (v) of the rung: L 93.17, R 64.87). Asymmetry nevertheless persists under the tested matched-count configurations. The registered set-size-artefact resolution is not obtained. This test does not determine whether set size contributes to the difference in gap magnitude, nor whether the remaining asymmetry is a circuit property. The claim is scoped to the tested matched-count configurations: one realised 10-neuron right subset cannot establish a universal property of the entire right GRN population, so no general circuit-property claim is made. A persisting asymmetry can be small, below the equivalence margin in size; "persists" says the asymmetry is present under the tested configurations, not that it is large. The bilateral matched pooled mean (97.43 Hz) is reported against condition (v)'s pooled mean (158.04 Hz) descriptively, for magnitude only; no claim is registered on the pooled comparison.

## 9. The sugar 150 control against the Part 3 150 Hz arm (section 3)

D = S pooled mean minus the Part 3 150 Hz arm pooled mean: **-0.13 Hz, 95% CI [-3.97, 3.73]** (percentile bootstrap over trials within each run, resampled independently, 10,000 resamples, seed 20261131). MN9 numbers below: RQ-C5 open. The CI includes 0, so S agrees with the arm and the discrepancy trigger (a CI excluding 0 by more than 5 Hz) does not fire. Per-side re-evaluation on S's per-side means and CIs: L 82.63 [81.03, 84.23] against old 83.5 (agrees, as on the arm); R 58.33 [56.80, 59.93] against old 58.7 (agrees, as on the arm). No verdict changes. The Part 6 matched-rate conclusions **stand within that tolerance**: the arm's numbers are corroborated by a clean-tree run, and the D4 decision itself rests on S (the protocol-matched ratio of section 6), not on the arm.

## 10. What this means for Part 7

Section 8.5 completion is met: the determinism check passed; all seven runs ran under the freeze with clean manifests; the anchor passed; every comparison of sections 8.2 to 8.4 is reported under its pre-stated rule, with the section 7 tables complete. Part 7 may lean on MN9 numbers once this gate closes (panel review and my sign-off). Completion does not require any particular outcome, and the readings constrain Part 7's claims rather than blocking Part 7 outright:

- **D2/D4 stays inconclusive.** The rate explanation is neither established nor excluded. The next step is the section 8.5 no-run comparison (compare how the two builds drive two populations and whether any neuron sits in both sets): a Part 6 follow-up, not part of this gate, and not a new run.
- **D3 is explained by rate.** The water disagreement was a rate effect, and the water number stays descriptive.
- **RQ-C5: the registered set-size-artefact resolution is not obtained, and the asymmetry persists at matched counts.** No general circuit-property claim is made from one realised subset, and whether the persisting asymmetry is a circuit property or something else is not decided by this gate. The "RQ-C5 open" labelling of every public MN9 figure stays in force until this gate closes (section 10); what the "persists" reading means for the label after closure is a decision for the gate, not something this report decides.

## 11. Deviations

Every deviation from the preregistration, however small, with its consequence stated.

1. **Harness bug, found and fixed during the work (no consequence for any number).** The analysis script's S-versus-arm per-side loop reused the variable names `old_point` and `old_ci`, overwriting the recomputed old-ratio values in the report display: the first full run displayed the old sugar R mean and CI (58.7 Hz, [54.99, 62.41]) where the old ratio (0.164, [0.144, 0.185]) belonged. The `matches_registered` check itself was computed before the loop and was correct, and no decision reading uses those variables (the readings use the registered constants). The loop variables were renamed, the synthetic test was re-run (ALL PASS, 13 cases), and the full analysis was re-run with the fixed script. The governing script hash is `1beb2cc0…` (the fixed version); the run record (`work/part6_tests_run_record.json`) still carries the pre-fix hash `f5c9c655…` from when it was first written, which refers to the same script before the fix. The numbers in this report come from the fixed script, and the old ratio is reported here as recomputed (point 0.1639, CI [0.1444, 0.1853]).

2. **Amendment after Reviewer 3's results review (26 Nov 2026, afternoon; no new run, no headline changed).** Reviewer 3 returned REQUIRE CHANGES on this report (five items, R3-1 to R3-5; the four headline readings were found correct). This report was amended to address them: (R3-1) the section 8 sentence attributing part of the gap reduction causally to set size was replaced with descriptive wording, and the section 10 "excluded" wording was corrected to "the registered set-size-artefact resolution is not obtained"; (R3-2) the test 1 per-side suppression ratios (L 0.093 [0.081, 0.105], R 0.207 [0.191, 0.223]) and the non-driven GRN population readouts were added to sections 5 and 6; (R3-3) the per-run manifest audit table was added to section 1; (R3-4) the corrected analysis-execution record was added as item 3 below; (R3-5) the RQ-C5 open label was made prominent at the top of the report and at each MN9 table. No headline reading changed, and no previously reported number changed; the added numbers were computed from the recorded spike tables and manifests and verified independently before inclusion (every MN9 mean recomputed exactly; the per-side ratio CIs recomputed, matching within 0.0002, Monte Carlo noise at the third decimal; every GRN population rate recomputed exactly).

3. **Corrected analysis-execution record (Reviewer 3 item R3-4; dated correction, the earlier record is preserved, not overwritten).** The analysis that generated the numbers in this report was run with the fixed analysis script `work/analyze_part6_tests.py`, SHA-256 `1beb2cc04252d465122f2a1cccb1aa8b675d8f9cba677a594bb5f0da4dd2cba6` (the version after the item 1 fix). Its machine-readable output is `work/part6_tests_analysis.json`, SHA-256 `17a1bfdbcc8e0495814568ceda0e5b3f4b4e061365271fe2b2a1265e19fbb610`. The harness record is `work/part6_tests_harness_record.json`, SHA-256 `676baff2fb43693ebf7f5e1773e2049ecbd2e427ed72d561fb3d59de3ad86095`. The run record `work/part6_tests_run_record.json`, SHA-256 `a896f517e6d06e8ef26e83fb83c73ec24e156ec544f85cb00ad26aef932e1f38`, still carries the pre-fix script hash `f5c9c6556e5aa5d1e0de060883d2b3849f49087441b8b2ec5004ca17089fba1c` in its harness section, because that file was written before the fix and has not been edited; the governing script hash is the fixed `1beb2cc0…` above. Confirmation: the numbers in this report were verified independently against the recorded spike tables (every MN9 mean recomputed exactly; three bootstrap CIs recomputed exactly; the per-side ratios recomputed, matching within Monte Carlo noise; every GRN population rate recomputed exactly), so the corrected script's output is the source of the reported values.

4. **Second amendment after Reviewer 3's re-review (26 Nov 2026, afternoon; no new run, no headline changed).** His re-review returned REQUIRE CHANGES with two minor corrections. (R3-2) The section 5 sentence calling the 0.29 Hz sugar right readout the only non-zero non-driven readout was corrected: the 11 undriven right sugar GRNs in runs 3a and 3c read 0.01 Hz and 0.21 Hz, which are also non-driven readouts, so the sentence now reads "The only non-zero readout among the wholly non-driven populations is the sugar right set at 0.29 Hz under water drive." (R3-3) The manifest audit was corrected, but not in the wording he proposed: his wording would have said all nine manifests record all three Part 1 data hashes, and I checked all nine manifests individually and the sugarR hash is not in any of them, because the runner does not load the reference file (the freeze record lists sugarR.parquet as reference, context only). The section 1 audit sentence now states that the manifests record the two brain data hashes and that the sugarR reference hash is recorded in the freeze record, and the section 1 freeze table's "every manifest records them" clause is corrected the same way. No headline reading changed, and no previously reported number changed.

No other deviation occurred. The void attempts, the sugar 150 driver interruption and the test 3a launch failure are recorded in section 3; none of them breaks a registered rule.

## 12. Reproduction

The frozen preregistration is `docs/discriminating_tests_preregistration.md` at commit `d5822d9` (SHA-256 `60ba4572…`), tag `part6-tests-v1` on freeze commit `1861238…`. The analysis script is `work/analyze_part6_tests.py` (SHA-256 `1beb2cc0…`); the run driver is `work/run_part6_tests.py`; the seed-disjointness script is `work/part6_tests_seed_disjointness_check.py` (SHA-256 `530a4f13…`). Run artefacts are in `results/validation/runs/part6-tests-*/` (spike tables and manifests; the void attempts survive as empty directories). The machine-readable analysis is `work/part6_tests_analysis.json`; the run record is `work/part6_tests_run_record.json`; the harness record is `work/part6_tests_harness_record.json`. Re-running the analysis script against the recorded spike tables reproduces every number in this report.
