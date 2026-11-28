# Part 7 feeding intervention: analysis

Status: analysis complete. This report states the results of the Part 7 feeding intervention experiment and stops there.

What I analysed: 13 configurations (INT intact; L-MN9; L-GRN; C-MN9-1 to C-MN9-5; C-GRN-1 to C-GRN-5 matched controls), all in the arm (a) closed loop configuration. Frozen evaluation: 260 episodes, seeds 5200 to 5219 shared, under the frozen decoder (r_hi 172.64875034982174 Hz). Refit evaluation: 220 episodes, seeds 5300 to 5319 shared, each non-degenerate configuration under its own r_hi^X. L-GRN is degenerate (r_hi 0.0 Hz) and ran no refit evaluation episodes. INT has no refit evaluation episodes either, since its refit is the section 4 calibration itself. Calibration: 120 episodes, seeds 5400 to 5519.

The frozen evaluation is the primary analysis. The refit evaluation is the registered sensitivity check (preregistration section 8.2). No new episodes were run for this analysis and no results files were modified.

## 1. How I ran the analysis

I used the corrected analysis code in src/closed_loop/analysis.py, post-amendment version, SHA-256 0e2c1c7e29febe06ef2ee0e43d6727d4770f201a68c9e72b02ecda052cac97f1. Its self-test passes. I passed arm="a" explicitly for every Part 7 episode, since the default gives the wrong duty cycle for arm (a).

Before touching the Part 7 data, I re-ran the check from the analysis-code amendment: the corrected code reproduces the section 6 values in results/closed_loop/characterisation_analysis_audit.json exactly on all 100 characterisation episodes, 0 mismatches. I then recomputed the five Part 5 family members from the raw logs with the corrected code. All five match the audit and the reconciliation exactly: member 1 (a) vs (c) peak E, difference plus 2.0426, p 1/10001; member 2 (a) vs (c) mean E, difference plus 1.7925, p 1/10001; member 3 (a) vs (b) peak E, difference plus 0.0126, 95% CI minus 0.0034 to plus 0.0275, p 0.145385; member 4 (a) vs (b) contact duration on the registered whole-episode definition, difference plus 3.4900 s, 95% CI 2.7500 to 3.9100, p 1/10001 (the reconciled member, not the audit diagnostic); member 5 suppression, mean s_i minus 0.7840, ratio 0.121, 95% CI 0.116 to 0.127, per-side L 0.097, R 0.158, p 1/10001.

I checked every Part 7 episode structurally before computing anything: manifest seed, r_hi_hz against the frozen value or the configuration's r_hi^X record, block_output IDs against the frozen matched-controls artefact (L-GRN target identical to data/neuron_sets/sugar_grn_right.csv), INT carrying no block_output key, both logs exactly 100 lines, 100 chunks completed, validity VALID. Frozen: 260 checked, 0 problems. Refit: 220 checked, 0 problems.

Statistics follow preregistration section 7 exactly. Percentile bootstrap, 10,000 resamples, 95% intervals, alpha 0.05. Each comparison's bootstrap stream is spawned from its registered permutation seed (SeedSequence(seed).spawn(1)). Endpoint and gap CIs use seed 20261128. Permutations: B equals 10,000, p equals (1 plus the count of |T*| at least |Tobs|) divided by (B plus 1), so the smallest unadjusted p is 1/10001, about 0.0001. Lesion members use seed-stratified label permutation (within each seed stratum of 6 episodes, one drawn as pseudo-lesion; group sizes preserved 20/100). TOST uses the 90% CI within bounds rule. A difference is claimed only where the Holm-adjusted p is below 0.05.

TOST bounds: the preregistration registers the rule (rates plus or minus 25% of the intact-arm mean or plus or minus 5 Hz, whichever is wider; suppression ratio plus or minus 0.15; E endpoints plus or minus 25% of the intact arm's mean). I used rule-based bounds throughout: peak E plus or minus 0.5111 rad and mean E plus or minus 0.4387 rad (25% of the INT frozen means, 2.0443 and 1.7550 rad). The code's hardcoded TOST_BOUNDS (peak E 0.44, mean E 0.22, contact duration 1.2 s) were not used. See section 7 for the contact-duration bound note.

The machine-readable record of every computed number (per-episode endpoints for all 480 episodes, comparison statistics, Holm values, gap values, bootstrap settings and seeds) is work/part7_analysis_values.json, SHA-256 83ea2aef60e0dde1d7ea2f8b91be0ad80ff88df2ecee765815c36d2ee5b05e72. The script that produced it is work/part7_analysis.py. Re-running it reproduces the file byte-identically (same SHA-256 on repeat runs).

Definitions used below: peak E is the maximum E over the episode; mean E is the mean E over stimulus chunks 0 to 59 (section 6 endpoint 2); MN9 rates are means over chunks 0 to 59, left and right separately; contact duration is taste-event ON time within the whole episode, chunks 0 to 99 (section 6 endpoint 7, corrected definition); duty cycle is ON chunks divided by the gate-armed period (arm (a): chunks 20 to 99); contact onset fraction is achieved E divided by E_max (2.1746 rad) at the first chunk whose end-state has the taste event ON, and is undefined when there is no contact; ignition (arm (a) only) is contact at all AND any gate-ON chunk in 20 to 59. All CIs below are 95% bootstrap CIs unless labelled 90% for TOST.

## 2. Endpoint tables

Means with 95% bootstrap CIs over the 20 seeds. Contact and ignition are counts out of 20. Contact onset fraction is the mean over episodes with contact only.

### 2.1 Frozen evaluation (seeds 5200 to 5219, frozen decoder)

| Config | Peak E (rad) | Mean E (rad) | MN9 L (Hz) | MN9 R (Hz) | MN9 total (Hz) | Contact dur (s) | Duty cycle | Onset frac | Longest stretch (s) | Contact | Ignition |
|---|---|---|---|---|---|---|---|---|---|---|---|
| INT | 2.0443 [2.0266, 2.0555] | 1.7550 [1.6272, 1.8441] | 89.23 [81.82, 94.48] | 60.92 [56.14, 64.37] | 150.16 [137.97, 158.68] | 8.715 [7.665, 9.465] | 0.912 [0.778, 1.000] | 0.8492 | 8.715 | 20/20 | 20/20 |
| L-MN9 | 2.0209 [1.9932, 2.0455] | 1.6552 [1.4672, 1.8133] | 84.19 [73.73, 93.01] | 56.16 [48.97, 62.25] | 140.35 [122.71, 155.22] | 7.835 [6.355, 9.045] | 0.814 [0.634, 0.959] | 0.8478 | 7.805 | 20/20 | 18/20 |
| L-GRN | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | none | 0.000 | 0/20 | 0/20 |
| C-MN9-1 | 2.0239 [1.9988, 2.0447] | 1.6284 [1.4403, 1.7870] | 82.99 [72.60, 91.58] | 54.43 [47.46, 60.17] | 137.43 [120.07, 151.79] | 7.620 [6.170, 8.830] | 0.805 [0.631, 0.952] | 0.8488 | 7.550 | 20/20 | 19/20 |
| C-MN9-2 | 1.7069 [1.6755, 1.7363] | 0.5839 [0.5739, 0.5938] | 25.65 [25.14, 26.14] | 17.93 [17.52, 18.35] | 43.58 [42.88, 44.27] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | none | 0.000 | 0/20 | 0/20 |
| C-MN9-3 | 1.8471 [1.8258, 1.8661] | 0.6991 [0.6621, 0.7372] | 33.24 [31.24, 35.31] | 19.21 [18.14, 20.32] | 52.45 [49.47, 55.58] | 0.475 [0.290, 0.665] | 0.024 [0.012, 0.038] | 0.8516 | 0.455 | 13/20 | 9/20 |
| C-MN9-4 | 1.8876 [1.8559, 1.9210] | 0.9447 [0.7845, 1.1228] | 42.26 [34.15, 51.38] | 31.23 [25.27, 37.90] | 73.48 [59.42, 89.23] | 1.820 [0.955, 2.830] | 0.152 [0.059, 0.264] | 0.8460 | 1.755 | 15/20 | 11/20 |
| C-MN9-5 | 2.0416 [2.0178, 2.0566] | 1.7351 [1.5639, 1.8559] | 88.15 [78.74, 94.83] | 60.01 [53.58, 64.60] | 148.16 [132.34, 159.38] | 8.605 [7.355, 9.465] | 0.901 [0.753, 1.000] | 0.8511 | 8.550 | 20/20 | 19/20 |
| C-GRN-1 | 1.9641 [1.9340, 1.9926] | 1.4704 [1.2519, 1.6772] | 61.59 [51.47, 71.24] | 61.26 [51.28, 70.88] | 122.85 [102.73, 142.10] | 6.445 [4.745, 8.075] | 0.669 [0.471, 0.857] | 0.8473 | 6.385 | 20/20 | 16/20 |
| C-GRN-2 | 0.9880 [0.9562, 1.0208] | 0.3167 [0.3088, 0.3242] | 20.10 [19.69, 20.50] | 4.77 [4.48, 5.08] | 24.88 [24.25, 25.47] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | none | 0.000 | 0/20 | 0/20 |
| C-GRN-3 | 1.3009 [1.2703, 1.3308] | 0.4248 [0.4123, 0.4376] | 23.03 [22.52, 23.50] | 9.34 [8.93, 9.78] | 32.37 [31.58, 33.16] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | none | 0.000 | 0/20 | 0/20 |
| C-GRN-4 | 2.0587 [2.0585, 2.0589] | 1.9832 [1.9768, 1.9893] | 97.63 [96.92, 98.29] | 79.41 [78.83, 80.03] | 177.04 [175.93, 178.10] | 9.605 [9.575, 9.640] | 1.000 [1.000, 1.000] | 0.8558 | 9.605 | 20/20 | 20/20 |
| C-GRN-5 | 1.7548 [1.7103, 1.7913] | 0.5939 [0.5718, 0.6207] | 27.76 [26.69, 29.09] | 16.81 [16.17, 17.61] | 44.57 [42.94, 46.66] | 0.075 [0.000, 0.165] | 0.004 [0.000, 0.011] | 0.8537 | 0.075 | 3/20 | 2/20 |

Two facts in this table I want the panel to see plainly. First, the matched controls span almost the whole range: C-GRN-4 peaks at 2.0587 rad with mean E 1.9832, above INT on both, while C-GRN-2 peaks at 0.9880 rad with mean E 0.3167 and no contact at all. The pooled control mean averages over very different sets, so the per-set means in section 3 matter as much as the pooled comparison. Second, L-MN9 frozen sits close to INT on peak E (2.0209 vs 2.0443) and on MN9 rates (L 84.19 vs 89.23, R 56.16 vs 60.92), with contact in 20/20 episodes and ignition in 18/20, while L-GRN is exactly zero on every endpoint in all 20 episodes.

INT frozen persistence to the end of the episode: the taste event is ON at chunk 99 in 18 of 20 episodes. The two exceptions are seed 5216 (last ON chunk 25) and seed 5217 (last ON chunk 32). That is the same 2/20 dropout as the characterisation baseline.

### 2.2 Refit evaluation (seeds 5300 to 5319, each configuration under its own r_hi^X)

INT has no refit evaluation episodes (its refit is the section 4 calibration itself) and L-GRN ran none (degenerate, r_hi 0.0 Hz). The r_hi^X values used: L-MN9 168.2958659350477 Hz; C-MN9-1 171.40738725463828; C-MN9-2 143.532806292193; C-MN9-3 152.26550023501633; C-MN9-4 157.70651756334206; C-MN9-5 172.86823731841815; C-GRN-1 165.55356090776894; C-GRN-2 86.07268488014275; C-GRN-3 114.4746763414514; C-GRN-4 191.82395220732104; C-GRN-5 149.45339708509593.

| Config | Peak E (rad) | Mean E (rad) | MN9 L (Hz) | MN9 R (Hz) | MN9 total (Hz) | Contact dur (s) | Duty cycle | Onset frac | Longest stretch (s) | Contact | Ignition |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L-MN9 | 2.0468 [2.0354, 2.0569] | 1.7934 [1.6715, 1.8791] | 89.57 [82.98, 94.13] | 60.23 [55.38, 63.82] | 149.80 [138.37, 157.89] | 8.630 [7.585, 9.470] | 0.891 [0.760, 1.000] | 0.8487 | 8.610 | 20/20 | 20/20 |
| C-MN9-1 | 2.0427 [2.0298, 2.0524] | 1.7870 [1.7206, 1.8315] | 90.87 [87.11, 93.50] | 60.29 [57.17, 62.53] | 151.16 [144.32, 155.85] | 8.455 [7.565, 9.160] | 0.889 [0.776, 0.978] | 0.8494 | 8.435 | 20/20 | 20/20 |
| C-MN9-2 | 2.0511 [2.0438, 2.0566] | 1.8096 [1.7671, 1.8383] | 76.14 [73.92, 77.58] | 52.80 [51.04, 54.14] | 128.94 [125.12, 131.44] | 8.715 [8.075, 9.165] | 0.950 [0.866, 1.000] | 0.8465 | 8.595 | 20/20 | 20/20 |
| C-MN9-3 | 2.0194 [1.9943, 2.0408] | 1.5909 [1.3822, 1.7698] | 75.78 [64.85, 85.00] | 42.99 [36.79, 48.34] | 118.78 [101.64, 133.34] | 7.230 [5.730, 8.520] | 0.747 [0.558, 0.908] | 0.8512 | 7.200 | 20/20 | 19/20 |
| C-MN9-4 | 2.0392 [2.0196, 2.0536] | 1.6933 [1.5252, 1.8274] | 75.51 [67.31, 82.09] | 56.01 [49.83, 60.98] | 131.52 [117.22, 143.08] | 7.620 [6.310, 8.760] | 0.784 [0.627, 0.923] | 0.8517 | 7.620 | 20/20 | 19/20 |
| C-MN9-5 | 2.0526 [2.0482, 2.0562] | 1.8458 [1.8320, 1.8600] | 94.35 [93.47, 95.33] | 64.75 [63.88, 65.57] | 159.10 [157.67, 160.54] | 9.410 [9.340, 9.480] | 1.000 [1.000, 1.000] | 0.8505 | 9.410 | 20/20 | 20/20 |
| C-GRN-1 | 2.0418 [2.0305, 2.0511] | 1.7876 [1.6619, 1.8584] | 73.99 [68.25, 77.27] | 72.91 [67.36, 76.14] | 146.90 [135.76, 153.23] | 8.825 [7.860, 9.440] | 0.918 [0.799, 0.995] | 0.8511 | 8.775 | 20/20 | 19/20 |
| C-GRN-2 | 1.9186 [1.8642, 1.9669] | 0.9137 [0.7270, 1.1180] | 29.65 [23.16, 36.76] | 6.92 [5.25, 8.73] | 36.57 [28.46, 45.43] | 1.690 [0.940, 2.500] | 0.124 [0.046, 0.210] | 0.8507 | 1.570 | 18/20 | 9/20 |
| C-GRN-3 | 1.9804 [1.9420, 2.0153] | 0.9338 [0.8048, 1.0748] | 34.97 [29.77, 40.77] | 13.88 [11.61, 16.45] | 48.85 [41.35, 57.25] | 1.835 [1.260, 2.475] | 0.125 [0.063, 0.204] | 0.8511 | 1.775 | 18/20 | 14/20 |
| C-GRN-4 | 2.0471 [2.0372, 2.0549] | 1.8494 [1.8332, 1.8659] | 97.06 [96.20, 97.95] | 79.61 [78.59, 80.58] | 176.67 [175.03, 178.29] | 9.380 [9.265, 9.480] | 0.995 [0.985, 1.000] | 0.8478 | 9.350 | 20/20 | 20/20 |
| C-GRN-5 | 1.9808 [1.9475, 2.0133] | 1.1169 [0.9316, 1.3134] | 48.19 [39.32, 57.72] | 29.93 [24.30, 35.97] | 78.12 [63.67, 93.72] | 3.420 [2.230, 4.750] | 0.281 [0.139, 0.443] | 0.8484 | 3.395 | 20/20 | 15/20 |

## 3. The registered comparisons

The Holm family has nine members in fixed order, permutation seeds 6000 to 6008. Members 1 to 5 come from the Part 5 characterisation, recomputed here from the raw logs with the corrected code (section 1). Members 6 to 9 come from this Part 7 analysis, frozen variant only. A difference is claimed only where the Holm-adjusted p is below 0.05. Precision target for each lesion member: the 95% CI half-width at most 15% of the INT frozen mean for that endpoint (peak E 0.3066 rad, mean E 0.2632 rad). All four lesion members meet it.

| Member | Comparison | Endpoint | Difference [95% CI] | p (unadjusted) | Holm-adjusted p | Claimed |
|---|---|---|---|---|---|---|
| 1 (seed 6000) | (a) vs (c) | Peak E (rad) | plus 2.0426 [2.0322, 2.0513] | 0.0001 (1/10001) | 0.0009 | Yes |
| 2 (seed 6001) | (a) vs (c) | Mean E (rad) | plus 1.7925 [1.7057, 1.8443] | 0.0001 (1/10001) | 0.0009 | Yes |
| 3 (seed 6002) | (a) vs (b) | Peak E (rad) | plus 0.0126 [minus 0.0034, 0.0275] | 0.1454 | 0.1454 | No |
| 4 (seed 6003) | (a) vs (b) | Contact duration (s), whole-episode definition, reconciled | plus 3.4900 [2.7500, 3.9100] | 0.0001 (1/10001) | 0.0009 | Yes |
| 5 (seed 6004) | (d) vs (b) | Suppression, mean s_i | minus 0.7840; ratio 0.121 [0.116, 0.127] | 0.0001 (1/10001) | 0.0009 | Yes |
| 6 (seed 6005) | L-MN9 vs pooled C-MN9 | Peak E (rad) | plus 0.1195 [0.0850, 0.1500] | 0.0008 | 0.0016 | Yes |
| 7 (seed 6006) | L-MN9 vs pooled C-MN9 | Mean E (rad) | plus 0.5370 [0.3395, 0.7088] | 0.0001 (1/10001) | 0.0009 | Yes |
| 8 (seed 6007) | L-GRN vs pooled C-GRN | Peak E (rad) | minus 1.6133 [minus 1.6287, minus 1.5982] | 0.0001 (1/10001) | 0.0009 | Yes |
| 9 (seed 6008) | L-GRN vs pooled C-GRN | Mean E (rad) | minus 0.9578 [minus 0.9992, minus 0.9135] | 0.0001 (1/10001) | 0.0009 | Yes |

For members 6 to 9 the lesion mean and pooled control mean are: member 6, L-MN9 2.0209 vs pooled C-MN9 1.9014; member 7, L-MN9 1.6552 vs pooled C-MN9 1.1182; member 8, L-GRN 0.0000 vs pooled C-GRN 1.6133; member 9, L-GRN 0.0000 vs pooled C-GRN 0.9578.

### 3.1 Per-set means (section 8 rule)

Per-set means are reported alongside the pooled comparison. A targeted-vs-pooled difference that reverses against a majority of individual sets (3 or more of 5) would be reported as set-dependent, not pooled away. Neither family meets that threshold, but the L-MN9 peak E comparison comes closest, with 2 of 5 sets reversing.

L-MN9 minus each C-MN9 set, peak E: C-MN9-1 minus 0.0030 (set mean 2.0239); C-MN9-2 plus 0.3140 (1.7069); C-MN9-3 plus 0.1738 (1.8471); C-MN9-4 plus 0.1332 (1.8876); C-MN9-5 minus 0.0208 (2.0416). The pooled peak E difference of plus 0.1195 is carried mainly by C-MN9-2 and C-MN9-3; against C-MN9-1 and C-MN9-5 the lesion is slightly below the set.

L-MN9 minus each C-MN9 set, mean E: C-MN9-1 plus 0.0268 (set mean 1.6284); C-MN9-2 plus 1.0713 (0.5839); C-MN9-3 plus 0.9561 (0.6991); C-MN9-4 plus 0.7105 (0.9447); C-MN9-5 minus 0.0799 (1.7351). One reversal (C-MN9-5).

L-GRN minus each C-GRN set, peak E: C-GRN-1 minus 1.9641 (set mean 1.9641); C-GRN-2 minus 0.9880 (0.9880); C-GRN-3 minus 1.3009 (1.3009); C-GRN-4 minus 2.0587 (2.0587); C-GRN-5 minus 1.7548 (1.7548). No reversals.

L-GRN minus each C-GRN set, mean E: C-GRN-1 minus 1.4704 (set mean 1.4704); C-GRN-2 minus 0.3167 (0.3167); C-GRN-3 minus 0.4248 (0.4248); C-GRN-4 minus 1.9832 (1.9832); C-GRN-5 minus 0.5939 (0.5939). No reversals.

### 3.2 TOST equivalence (rule-based bounds)

Peak E bound plus or minus 0.5111 rad; mean E bound plus or minus 0.4387 rad (25% of the INT frozen means). Suppression ratio bound plus or minus 0.15.

- Member 6 (L-MN9 peak E): 90% CI [0.0908, 0.1454] lies inside plus or minus 0.5111. Equivalence demonstrated under the registered bound, and the difference is also claimed under Holm (p adjusted 0.0016). Both hold at once: the difference from zero is real by the permutation test, and it is small relative to the registered plus or minus 25% band. I flag this plainly because the two statements read as opposites and they are not.
- Member 7 (L-MN9 mean E): 90% CI [0.3749, 0.6856] is not inside plus or minus 0.4387 (upper end outside). Equivalence not demonstrated. The difference is claimed under Holm.
- Member 8 (L-GRN peak E): 90% CI [minus 1.6263, minus 1.6004], far outside plus or minus 0.5111. Equivalence not demonstrated. The difference is claimed under Holm.
- Member 9 (L-GRN mean E): 90% CI [minus 0.9930, minus 0.9205], far outside plus or minus 0.4387. Equivalence not demonstrated. The difference is claimed under Holm.
- Member 5 (suppression): the 90% CI of the ratio, [0.117, 0.126], is far below the equivalence band [0.85, 1.15]. Equivalence not demonstrated (as in the characterisation report).
- Member 3 ((a) vs (b) peak E): equivalent under the registered rule (90% CI [minus 0.001, 0.025] inside plus or minus 0.511 rad), as in the characterisation report; not claimed under Holm.
- Member 4 (contact duration): 90% CI [2.840, 3.900] s against the rule-based bound plus or minus 2.24875 s (25% of the characterisation arm (a) mean 8.995 s). Equivalence not demonstrated. No TOST claim is made on contact duration for Part 7 itself; see section 7 for the bound note.

Non-significance without demonstrated equivalence would be inconclusive, never a null. That case does not arise among the nine members: every member is either claimed under Holm or, for member 3, equivalent under TOST.

## 4. Secondary comparisons (no p-values)

### 4.1 INT vs each lesion and control configuration, frozen, paired by seed index

Differences are the configuration minus INT, with 95% bootstrap CIs. Secondary and descriptive only.

| Config | Peak E difference [95% CI] | Mean E difference [95% CI] |
|---|---|---|
| L-MN9 | minus 0.0234 [minus 0.0529, 0.0074] | minus 0.0998 [minus 0.3290, 0.1270] |
| L-GRN | minus 2.0443 [minus 2.0555, minus 2.0266] | minus 1.7550 [minus 1.8441, minus 1.6272] |
| C-MN9-1 | minus 0.0204 [minus 0.0474, 0.0055] | minus 0.1266 [minus 0.3555, 0.0853] |
| C-MN9-2 | minus 0.3374 [minus 0.3694, minus 0.3090] | minus 1.1711 [minus 1.2603, minus 1.0446] |
| C-MN9-3 | minus 0.1972 [minus 0.2250, minus 0.1685] | minus 1.0558 [minus 1.1649, minus 0.9132] |
| C-MN9-4 | minus 0.1567 [minus 0.1941, minus 0.1165] | minus 0.8103 [minus 1.0167, minus 0.5620] |
| C-MN9-5 | minus 0.0027 [minus 0.0297, 0.0220] | minus 0.0199 [minus 0.2265, 0.1690] |
| C-GRN-1 | minus 0.0802 [minus 0.1080, minus 0.0547] | minus 0.2845 [minus 0.5047, minus 0.0812] |
| C-GRN-2 | minus 1.0563 [minus 1.0857, minus 1.0257] | minus 1.4382 [minus 1.5252, minus 1.3147] |
| C-GRN-3 | minus 0.7434 [minus 0.7742, minus 0.7144] | minus 1.3301 [minus 1.4247, minus 1.1987] |
| C-GRN-4 | plus 0.0144 [0.0032, 0.0321] | plus 0.2282 [0.1380, 0.3586] |
| C-GRN-5 | minus 0.2895 [minus 0.3354, minus 0.2511] | minus 1.1611 [minus 1.2563, minus 1.0360] |

L-MN9 sits within the INT interval on both endpoints (both CIs include zero). C-GRN-4 sits above INT on both endpoints. The remaining controls sit below INT by amounts ranging from 0.02 to 1.06 rad on peak E.

### 4.2 Lesion comparisons, refit variant (secondary, no p-values)

- L-MN9 vs pooled C-MN9, peak E: difference plus 0.0058, 95% CI [minus 0.0073, 0.0181] (lesion mean 2.0468, pooled control mean 2.0410).
- L-MN9 vs pooled C-MN9, mean E: difference plus 0.0480, 95% CI [minus 0.0787, 0.1550] (lesion mean 1.7934, pooled control mean 1.7453).

The frozen separations (member 6 plus 0.1195, member 7 plus 0.5370) are not present under the refit variant: both refit CIs include zero and both point estimates are near zero. L-GRN has no refit variant.

### 4.3 Thresholded endpoints, lesion vs pooled controls, frozen (secondary, no p-values)

L-MN9 vs pooled C-MN9: contact duration 7.835 s vs 3.704 s, difference plus 4.131 [2.624, 5.461]; duty cycle 0.814 vs 0.377, difference plus 0.438 [0.259, 0.597]; longest continuous ON stretch 7.805 s vs 3.662 s, difference plus 4.143 [2.624, 5.475]; ignition 0.90 vs 0.58, difference plus 0.32 [0.14, 0.46]; contact occurrence 1.00 vs 0.68, difference plus 0.32 [0.27, 0.38]; contact onset fraction 0.8478 (20 of 20 episodes with contact) vs 0.8494 (68 of 100).

L-GRN vs pooled C-GRN: contact duration 0.000 s vs 3.225 s, difference minus 3.225 [minus 3.550, minus 2.886]; duty cycle 0.000 vs 0.335, difference minus 0.335 [minus 0.372, minus 0.295]; longest continuous ON stretch 0.000 s vs 3.213 s, difference minus 3.213 [minus 3.544, minus 2.866]; ignition 0.00 vs 0.38, difference minus 0.38 [minus 0.42, minus 0.34]; contact occurrence 0.00 vs 0.43, difference minus 0.43 [minus 0.46, minus 0.40]; contact onset fraction undefined for L-GRN (0 of 20 episodes with contact) vs 0.8517 (43 of 100).

## 5. Frozen vs refit gaps

Gap is refit minus frozen, paired by seed index, with 95% bootstrap CIs. The gap is not a family member and carries no permutation p-value. No TOST claim about any gap is made here. INT and L-GRN have no gap: INT has no refit evaluation episodes and L-GRN ran none.

| Config | Peak E gap [95% CI] | Mean E gap [95% CI] (section 6 definition, chunks 0 to 59) |
|---|---|---|
| L-MN9 | plus 0.0259 [0.0043, 0.0510] | plus 0.1382 [minus 0.0379, 0.3338] |
| C-MN9-1 | plus 0.0188 [minus 0.0073, 0.0483] | plus 0.1587 [minus 0.0124, 0.3585] |
| C-MN9-2 | plus 0.3442 [0.3141, 0.3776] | plus 1.2256 [1.1860, 1.2546] |
| C-MN9-3 | plus 0.1723 [0.1388, 0.2062] | plus 0.8918 [0.6741, 1.0787] |
| C-MN9-4 | plus 0.1515 [0.1111, 0.1886] | plus 0.7487 [0.5156, 0.9663] |
| C-MN9-5 | plus 0.0110 [minus 0.0059, 0.0351] | plus 0.1107 [minus 0.0161, 0.2886] |
| C-GRN-1 | plus 0.0777 [0.0466, 0.1100] | plus 0.3172 [0.0699, 0.5634] |
| C-GRN-2 | plus 0.9306 [0.8711, 0.9864] | plus 0.5970 [0.4103, 0.7999] |
| C-GRN-3 | plus 0.6795 [0.6297, 0.7266] | plus 0.5090 [0.3814, 0.6502] |
| C-GRN-4 | minus 0.0116 [minus 0.0215, minus 0.0039] | minus 0.1338 [minus 0.1485, minus 0.1193] |
| C-GRN-5 | plus 0.2261 [0.1773, 0.2798] | plus 0.5230 [0.3375, 0.7207] |

I recomputed these gaps myself from the episode data and checked them against the refit report. Peak E gap point estimates match the refit report exactly (maximum absolute difference 0.0 across all 11 configurations), and the peak E gap CIs agree within 0.0020 rad, which is the expected Monte Carlo difference between the refit verification's single advancing bootstrap stream and the per-call spawned streams used here. The mean E gaps differ from the refit report's mean E gaps, and the reason is a definition difference, not a discrepancy: the refit report defined mean E over all 100 chunks, while section 6 defines it over chunks 0 to 59 and this analysis uses the section 6 definition. I confirmed the definitional account exactly: recomputing the 100-chunk mean E per episode from the raw body logs reproduces the refit report's per-episode values with maximum absolute difference 0.0 in every configuration. The section 6 mean E is lower than the 100-chunk mean wherever contact persists into the tail (for example C-MN9-2: 0.5839 vs 0.3503 frozen), because the tail chunks hold E near its peak while the stimulus window includes the early rise.

The gaps are uneven across configurations. C-MN9-2, C-GRN-2 and C-GRN-3 move the most on peak E (plus 0.3442, plus 0.9306, plus 0.6795); C-GRN-4 moves slightly down on both endpoints (peak minus 0.0116, mean minus 0.1338). Contact counts move the same way as the gaps: frozen 0/20 vs refit 20/20 for C-MN9-2, and frozen 0/20 vs refit 18/20 for C-GRN-2 and C-GRN-3.

## 6. Materiality bands, INT frozen

- M1, contact onset fraction: INT frozen mean 0.8492 over the 20 episodes with contact (per-episode range 0.8392 to 0.8584), band [0.787, 0.887]. Inside.
- M2 analogue, rate-to-extension table: for the INT frozen steady window (chunks 50 to 59), mean E minus the table value at the window mean pooled rate is minus 0.0945 rad on average, band plus or minus 0.10 rad. The mean is inside the band, but 11 of the 20 episodes fall outside it, and all 20 differences are negative (range minus 0.1784 to minus 0.0000). The table over-predicts achieved E in every INT episode, by about 4 percent on average, the same direction and size as the characterisation M2 offset.
- M3, peak E under sustained full drive: INT frozen mean 2.0443, 95% CI [2.0266, 2.0555], against the prediction 2.1746, band [2.0746, 2.2746]. Outside, below the band. This is the same standing discrepancy as in the characterisation report; no band, constant or seed was adjusted.
- M4, MN9 rates: INT frozen L 89.23 Hz against reference 92.57, band [69.43, 115.71]. Inside. R 60.92 Hz against reference 62.40, band [46.80, 78.00]. Inside.
- M7, settle-invalid episodes: 0 invalid in 260 frozen episodes and 0 invalid in 220 refit episodes. No arm pauses.

## 7. Points I am flagging for the panel

I did not decide these silently. Each is a place where the preregistration leaves room, or where two registered readings sit side by side.

(a) Bootstrap resampling unit for the lesion comparisons. The preregistration registers the TOST bounds and the 90% CI rule, and it registers the permutation's stratification, but it does not name the bootstrap resampling unit for the unpaired lesion comparison. I resampled per-seed differences d_j, where d_j equals the lesion value at seed j minus the mean of the five matched controls at seed j, which is the same seed-stratum unit the permutation uses. The mean of d_j equals the lesion mean minus the pooled control mean exactly. A different resampling unit (for example resampling all 100 control episodes independently) would give somewhat different CI widths.

(b) TOST bounds, code vs rule. The code hardcodes TOST_BOUNDS peak E 0.44, mean E 0.22, contact duration 1.2 s. Those do not equal plus or minus 25% of the Part 7 INT frozen means (peak E 0.5111, mean E 0.4387). The preregistration registers the rule, so rule-based bounds govern and were used for every TOST result in this report. The contact-duration bound needs a separate note, in section 8.

(c) Member 6 holds two registered readings at once (section 3.2): the difference is claimed under Holm, and equivalence is demonstrated under the registered TOST bound. Both follow from the rules as written. The panel should say explicitly whether that combination is the intended reading, or whether the TOST bound for E endpoints needs revisiting before any conclusion is drawn from member 6.

(d) Per-set reversals. The pooled L-MN9 peak E difference reverses against 2 of 5 sets and the mean E difference against 1 of 5. The registered set-dependence threshold (a majority, 3 or more) is not met, so I report the pooled values as registered. But the pooled difference is carried by particular sets (C-MN9-2 and C-MN9-3 on both endpoints), and the two MN9 control sets that sit closest to INT (C-MN9-1 and C-MN9-5) both sit slightly above the lesion on peak E.

(e) Control heterogeneity. The pooled control means average over sets that behave very differently under the frozen decoder. The most extreme case is the GRN family: C-GRN-4 exceeds INT on both primary endpoints while C-GRN-2 and C-GRN-3 show no contact at all. Any reading of the pooled L-GRN comparison should carry that spread with it.

(f) Mean E definition. The refit report's mean E gaps use the 100-chunk mean; this analysis uses the section 6 definition (chunks 0 to 59). Both are computed and checked exactly (section 5). The gap table in this report is the section 6 one.

(g) The refit-variant lesion comparisons (section 4.2) are secondary and carry no p-values, as registered. Their CIs include zero on both endpoints. Whether that erases the frozen separation is a conclusions question for the panel, not a result I state here.

## 8. Disclosures

(1) Matched-control fallback. Both families exhausted their streams: the L-MN9 stream (5701 to 5749, 49 draws) passed 2 sets through the screen, and the L-GRN stream (5750 to 5799, 50 draws) passed 0 sets. Under the preregistration section 8.1 fallback, the five lowest-distance drawn sets were used in each family. No tolerance was widened. The fallback was applied in both families, and it is disclosed here as registered.

(2) Intact dropout baseline. In the Part 5 characterisation, contact persisted to the end of the episode in 18 of 20 intact arm (a) episodes (2/20 dropout). In this Part 7 INT frozen arm, contact persisted to the end in 18 of 20 episodes as well (seeds 5216 and 5217 dropped out early, last ON chunk 25 and 32). The 2/20 baseline reproduces.

(3) E is treated as measured, not table-predicted. The rate-to-extension table over-predicts achieved E by about 4 percent on average (M2 analogue, section 6: mean difference minus 0.0945 rad, all 20 INT episodes negative). Every E value in this report is the measured E from the body log.

(4) M3 stays a named discrepancy. INT frozen peak E mean 2.0443, 95% CI [2.0266, 2.0555], sits below the M3 band [2.0746, 2.2746] around the 2.1746 rad prediction. The shortfall stands as recorded in the characterisation report; no band, constant or seed was adjusted.

(5) TOST contact-duration bound note. The code's TOST_BOUNDS contact-duration value of 1.2 s is now stricter than the registered plus or minus 25% rule on the corrected whole-episode definition. On the characterisation arm (a) mean of 8.995 s, the registered rule gives 2.249 s, so 1.2 s is about 13% of the mean rather than 25%. On the Part 7 INT frozen mean of 8.715 s the rule gives 2.179 s. No TOST claim on contact duration is made in this report, so the bound choice changes no result stated here, but the panel should settle which bound governs before any TOST claim about contact duration is made at the gate.

(6) L-MN9 reading note. block_output zeroes outgoing synaptic weights only. MN9 keeps spiking, and the decoder reads MN9 spikes directly from the spike monitor, not through synapses, so an L-MN9 lesion does not abolish extension by itself. The synapse count in the brain worker log is the measure the lesion took effect (158 outgoing synapses zeroed for L-MN9 in every phase), not the MN9 spike counts. Read the L-MN9 episodes with this in mind: frozen L-MN9 MN9 rates are L 84.19 Hz and R 56.16 Hz, close to INT, and contact occurred in 20 of 20 episodes.

(7) Section 8.2 prediction failure. The preregistration expected L-MN9's refit to be rejected, stating its estimator input is identically zero under the lesion so its calibration counterpart yields r_hi^X equal to 0 by construction. That prediction is wrong under the implemented mechanism: block_output zeroes outgoing weights only, MN9 keeps spiking, and the decoder reads MN9 spikes directly. The measured r_hi^L-MN9 is 168.2958659350477 Hz, not degenerate, and L-MN9 ran a full refit evaluation (20 episodes, seeds 5300 to 5319). L-GRN was rejected at 0.0 Hz as expected, and ran no refit evaluation episodes. The degenerate rule itself is mechanical and unchanged: it fires only on a measured r_hi^X at or below 15 Hz.

(8) Seed 5515 void anomaly. In the refit calibration ledger, seed 5515 (calibration C-GRN-5) has two attempt-1 entries for the same void path, refit_void/calibration/C-GRN-5/seed5515_attempt1. The void-naming code reset its attempt counter on each restart and deleted an existing void directory, so the second void overwrote the first void's files. The first void's partial files are unrecoverable. The completed episode for seed 5515 is unaffected, and no other completed episode is affected. The bug was fixed during the run (attempt numbers now start after every void already recorded for that seed, and an existing void directory is never deleted); the fix was verified working by the clean seed 5316 evaluation void.

(9) Six stalls during the refit phase. Five VM restarts (about 06:16, 08:25, 10:16, 12:20 and 17:36 WAT on 28 Nov 2026) and one service restart (about 07:24 WAT on 28 Nov 2026, runner death with no reboot). No completed episode was lost in any stall; each stall was resumed from the next episode, with the incomplete attempt preserved as a void. The refit phase completed 120 of 120 calibration episodes and 220 of 220 evaluation episodes, all VALID.

Conclusions wait for the panel review of this analysis.
