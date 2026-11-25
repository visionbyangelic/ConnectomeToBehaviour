# Part 5 characterisation results

**Status: characterisation results, pending panel review.** This report covers the 100 characterisation episodes of the Part 5 freeze (tag `part5-prereg-v1`), analysed under sections 6, 7 and 10 of `docs/closed_loop_preregistration.md` exactly as frozen. No Part 7 episode exists yet, and nothing in this report is a Part 7 result. One question is flagged for the panel in section 5 below: the Holm adjustment across the confirmatory family cannot be completed until the family's four lesion members exist, so no Holm-adjusted value is reported here and no claim in this report rests on one.

**Standing scoping statements (section 11), which travel with every claim in this report.** Feeding in this project is demonstrated on a raised substrate (the section 4.6 pedestal, an engineered arena parameter, class D) with the neck joints held at their settled values: this body, as registered, cannot contact ground-level food with the neck held, and no feeding claim in this report omits that. The taste signal is a constructed sensory signal built from physical contact. The extension angle is a function of the decoder mapping, not independent evidence about the connectome. Extension amplitudes are servo-limited model outputs (E_max = 2.1746 rad is 0.7695 of the raw published extremes), never physiological quantities. Contact forces are diagnostics only and no force number is claimed anywhere below. Arm (d) is OUTSIDE THE VALIDATED ENVELOPE and arm (e) is OUTSIDE THE VALIDATED ENVELOPE; both are labelled so wherever they appear. No result here is evidence for the connectome's total contribution to feeding, for any topology-versus-null comparison, or for any general fraction-of-behaviour claim (section 11, item 7). A separation on graded endpoints is worded as a change in the loop's extension response unless the contact endpoints also show it (section 11, item 8).

## 1. What was analysed, and how the set was verified before any number was computed

The run set is the characterisation set of the freeze: five arms, 20 episodes each, 100 episodes, every episode VALID, recorded in `results/closed_loop/characterisation/` with its hash ledger at `results/closed_loop/characterisation/ledger.json`. Before computing anything, I verified the set against the ledger and the preregistration:

- 100 episodes, 20 per arm; arms (a) to (d) on the registered paired seed list (5100 to 5119 excluding 5103, plus 5120), arm (e) on its own block (5800 to 5819). Every list matches exactly.
- Every manifest carries the frozen decoder values: r_hi = 172.64875034982174 Hz, r_lo = 5 Hz.
- Every file hash in the ledger still matches the file on disk (manifest, brain log, body log, summary, worker log, for all 100 episodes).
- One episode took two attempts: arm (c), seed 5107, voided by a service restart during the runs and re-run under the same seed under the resumability provision. It is not a settle failure. The settle-invalid count is zero in every arm.
- The measuring instrument was checked before the data, in the order section 13 prescribes: the frozen analysis code (`src/closed_loop/analysis.py`) hashes to `6861428ec6f392f8a470d44928e87be53bfcba2f8553fffad158b2c6190fc2ff`, exactly the value in the freeze record, and its self-test on synthetic records with known endpoint values passes.

## 2. How the endpoints were computed

Graded and thresholded endpoints follow section 6. All registered inference goes through the frozen analysis code: percentile bootstrap, 10,000 resamples over the seed as the independent unit, paired resampling of seed pairs for paired comparisons, 95% intervals; permutation p-values by the section 7 amendment's construction (B = 10,000, p = (1 + extreme count)/(B + 1), NumPy default_rng under each member's registered permutation seed). The permutation extreme counts were recomputed with the identical draw sequence the frozen code uses and cross-checked against the frozen functions' p-values for every member; they agree exactly.

Two definitional divergences between the frozen code and the section 6 text were found while setting up the pass, and are recorded here rather than resolved silently:

- The frozen code's field named `contact_onset_fraction` is the fraction of stimulus-period chunks with the event ON. Section 6 item 6 defines the contact onset fraction differently: the achieved E/E_max at the first chunk whose end-state has the taste event ON. The section 6 definition is the one materiality band M1 is written against, so the section 6 quantity is what this report calls the contact onset fraction; it is computed from the raw per-chunk logs. The frozen code's field is reported, where relevant, as the stimulus-period event fraction.
- The frozen code's `ignition_arm_a` field requires the event ON at a chunk of 40 or later; section 6 item 8 words ignition as contact occurring at all plus drive persisting via the gate beyond the ignition window (any gate-applied chunk in 20 to 59). Both are reported in section 4; they differ on exactly one episode (seed 5111, whose contact ended at chunk 30 when the episode released and retracted).
- Contact duration for the confirmatory family member (a) vs (b) is the frozen code's endpoint: event-ON time within the stimulus period, chunks 0 to 59. Section 6 item 7's full-episode duration (total ON chunks over chunks 0 to 99) and longest continuous ON stretch are reported alongside as secondary quantities.

One error of my own, in the supplementary script that computes the section 6 quantities the frozen code does not carry: the first pass computed the duty cycle without conditioning on the event being ON, which returned the impossible value 1.0 for the silent arm (c). The sanity check caught it before any number was reported; the script was corrected and the whole pass re-run, and every confirmatory number reproduced identically on the re-run. No frozen code, and no episode record, was touched.

## 3. Per-arm results

Means across the 20 episodes of each arm, with 95% bootstrap intervals. MN9 rates are stimulus-period means (chunks 0 to 59), L and R always separate. Contact duration in this table is the frozen endpoint (stimulus period); full-episode ON time and duty cycle follow section 6 item 7 (duty denominator: chunks 20 to 99 for arms (a) and (e), chunks 0 to 99 for arms (b), (c) and (d)).

| Endpoint | (a) Closed-loop sugar | (b) Open-loop sugar | (c) No drive | (d) Sugar+bitter | (e) Bilateral sugar |
|---|---|---|---|---|---|
| Peak E (rad) | 2.043 [2.032, 2.051] | 2.030 [2.016, 2.043] | 0.000 [0.000, 0.000] | 0.344 [0.317, 0.376] | 2.056 [2.055, 2.057] |
| Mean E (rad) | 1.793 [1.706, 1.844] | 1.832 [1.817, 1.848] | 0.000 [0.000, 0.000] | 0.182 [0.173, 0.194] | 1.857 [1.848, 1.866] |
| MN9 L rate (Hz) | 92.60 [87.52, 95.58] | 94.88 [94.00, 95.77] | 0.00 | 9.18 [8.68, 9.73] | 93.29 [92.52, 94.02] |
| MN9 R rate (Hz) | 60.97 [57.61, 63.05] | 62.39 [61.68, 63.20] | 0.00 | 9.87 [9.43, 10.33] | 66.38 [65.76, 67.01] |
| Contact duration, stimulus (s) | 5.275 [4.985, 5.455] | 5.405 [5.340, 5.465] | 0.000 | 0.000 | 5.400 [5.280, 5.505] |
| Event ON chunks, full episode | 89.95 | 55.05 | 0 | 0 | 93.65 |
| Duty cycle (section 6 item 7) | 0.947 [0.851, 1.000] | 0.551 [0.543, 0.558] | 0.000 | 0.000 | 0.996 [0.987, 1.000] |
| Onset latency (chunks) | 0 in all 20 | 0 in all 20 | no onset in 20 of 20 | 2.05 [0.80, 3.55] | 0 in all 20 |
| Contact onset fraction (section 6 item 6) | 0.852 [0.849, 0.855] | 0.852 [0.849, 0.855] | no contact in 20 of 20 | no contact in 20 of 20 | 0.852 [0.849, 0.855] |
| Episodes with contact | 20 of 20 | 20 of 20 | 0 of 20 | 0 of 20 | 20 of 20 |

Arm (d) and arm (e) are OUTSIDE THE VALIDATED ENVELOPE. Arm (e) is a separate secondary condition: its numbers are descriptive, are never pooled with arm (a)'s, and enter no confirmatory family.

## 4. What each arm shows

**Arm (a), closed-loop sugar (primary).** Contact occurred in all 20 episodes. Ignition under section 6 item 8: 20 of 20 episodes show contact plus drive applied through the taste-event gate inside chunks 20 to 59, after the scripted ignition window closed (under the frozen code's stricter field, 19 of 20; seed 5111 is the exception, and it is the episode that released and retracted mid-episode, its extension offset at chunk 41). In 18 of 20 episodes the extension never offset before the episode ended; the two offsets are seed 5111 at chunk 41 and seed 5110 at chunk 94. The claim this arm carries stands on the gate-sustained period, and the gate-sustained period is what the logs show: after chunk 19 the only drive applied arrived through the contact gate, and contact, once made, held the loop on.

**Arm (b), open-loop sugar.** Contact in all 20 episodes during the scripted window, and in every episode the extension offset followed once the window closed at chunk 59: the event is ON for about 55 chunks, almost all of them inside the stimulus period (54.1 of 55.1 on average), and off through nearly all of the tail. Arm (b) is the comparison that gives arm (a)'s sustainment its meaning: the same stimulus, delivered without the gate, does not persist past its script.

**Arm (c), no-drive control.** Silence, exactly as registered: zero MN9 spikes on both sides in all 20 episodes, zero extension, zero contact, zero taste events. No false positive of the assembled system was observed in this arm.

**Arm (d), sugar+bitter (OUTSIDE THE VALIDATED ENVELOPE).** The graded endpoints carry this comparison, as section 6's hierarchy prescribes. The suppression ratio (endpoint 4, per-seed pooled ratio, arm (d) against arm (b)) is 0.121, 95% CI [0.116, 0.127]; the ratio of condition means is 0.121. Per side: L 0.097 [0.091, 0.103], R 0.158 [0.151, 0.166]. The interval excludes 1, and the graded endpoints agree: against arm (b), peak E differs by -1.686 rad [-1.719, -1.648], mean E by -1.649 rad [-1.670, -1.628], MN9 L by -85.71 Hz [-86.83, -84.52], MN9 R by -52.53 Hz [-53.43, -51.57]. Under section 11's permitted wording: bitter drive suppressed the sugar response in the embodied loop, through the brain's response to the bitter GRN drive; the decoder contains no bitter path. On the thresholded side, arm (d) shows an extension onset in all 20 episodes (peak E 0.344 rad) and no food contact in any episode, which is the outcome section 10's pre-evaluation expectation described in advance; the graded endpoints, not the onset, carry the claim, and no feeding claim is made from arm (d): its extension response changed, and it did not feed. Suppression equivalence (TOST, ratio within plus/minus 0.15) is not met, as expected under a demonstrated suppression: the 90% CI [0.117, 0.126] sits far below the equivalence band [0.85, 1.15].

**Arm (e), bilateral sugar (OUTSIDE THE VALIDATED ENVELOPE, secondary condition, descriptive only).** The loop runs under bilateral drive: contact in all 20 episodes, duty cycle 0.996 over the gate-armed period, no extension offset in any episode. The pre-run expectation that the command e would saturate at 1 through much of the driven phase did not hold as stated: e reached 0.99 or above in only 9.4% of stimulus chunks, because the pooled MN9 rate (L 93.29 plus R 66.38 Hz) sits below the frozen r_hi of 172.65 Hz, so the loop held contact at a high but unsaturated command. No graded-decoding conclusion is drawn from this arm, and no asymmetry claim is made from it.

## 5. The confirmatory family: the five characterisation members

Permutation results under the section 7 amendment's construction. Each member's bootstrap interval is the paired percentile interval of section 7. Holm-adjusted values are **not reported**: the amendment fixes Holm over the full family of nine members, in the family's fixed order, and the four lesion members (permutation seeds 6005 to 6008) cannot exist until Part 7 runs. Adjusting over a subset would either use the wrong family size or the wrong ordering, and the preregistration forbids reordering or revising the family in light of outcomes. This is the one open question this report puts to the panel: whether the characterisation members may be claimed on their unadjusted permutation values with the adjustment recorded as pending, or whether every family claim waits for Part 7. No claim below rests on an adjusted value.

| Member | Permutation seed | Extreme count (of 10,000) | Unadjusted p (unrounded) | Paired mean difference, 95% CI |
|---|---|---|---|---|
| (a) vs (c), peak E | 6000 | 0 | 0.00009999000099990001 | +2.043 rad [2.032, 2.051] |
| (a) vs (c), mean E | 6001 | 0 | 0.00009999000099990001 | +1.793 rad [1.706, 1.844] |
| (a) vs (b), peak E | 6002 | 1453 | 0.14538546145385461 | +0.013 rad [-0.003, 0.028] |
| (a) vs (b), contact duration | 6003 | 10000 | 1.0 | -0.130 s [-0.390, 0.000] |
| Suppression, (d) vs (b), mean of s_i | 6004 | 0 | 0.00009999000099990001 | mean s_i = -0.784; ratio 0.121 [0.116, 0.127] |

The two (a) vs (c) members and the suppression member sit at the construction's floor: zero of 10,000 permutations reached the observed statistic, so each reports the smallest value the construction can report, 1/(B + 1). The (a) vs (b) contact-duration member reports p = 1.0: the per-seed differences are concentrated at zero (most seeds give identical durations in the two arms), and every sign assignment produced a statistic at least as large in absolute value as the observed one, which is the amendment's stated all-zero-style edge behaviour operating on a near-zero difference.

**Closed against open, read under section 7's equivalence rule.** (a) vs (b) shows no separation on peak E (interval includes 0) and none on contact duration. A no-difference claim is permitted only on demonstrated equivalence, so TOST was run: for peak E, the 90% interval of the paired difference, [-0.001, 0.025] rad, lies inside plus/minus 25% of arm (a)'s mean peak E (plus/minus 0.511 rad); for contact duration, the 90% interval [-0.390, 0.000] s lies inside plus/minus 25% of arm (a)'s mean contact duration (plus/minus 1.319 s), and also inside the frozen code's hardcoded bound of 1.2 s. Equivalence on both registered (a) vs (b) endpoints is therefore demonstrated, and section 11's permitted wording applies: under this decoder and body, closing the loop made no demonstrated difference to the feeding endpoints, within the registered equivalence bounds. That sentence is about the endpoints during the stimulus period. It does not erase the structural difference the logs show: arm (a)'s contact is sustained by the gate after its script ends (section 4), while arm (b)'s ends with its script. The endpoints registered for the comparison do not separate the two arms; the sustainment difference is carried by the ignition and tail behaviour, reported above as registered secondary endpoints.

**Precision target.** Section 7's target (95% CI half-width at most 15% of the intact arm's mean on the primary endpoints) is met for every characterisation member: half-widths 0.010 rad against a target of 0.306 for (a) vs (c) peak E, 0.069 against 0.269 for (a) vs (c) mean E, and 0.015 against 0.306 for (a) vs (b) peak E.

## 6. Materiality bands (section 10)

A value outside its band is a discrepancy for the panel, not a verdict on any arm.

| Band | Quantity | Result | Inside? |
|---|---|---|---|
| M1 | Contact onset fraction, prediction 0.8371, band [0.787, 0.887] | Mean 0.852 over the 60 episodes with contact (arms (a), (b), (e)); per-arm means 0.852, 0.852, 0.852; every episode between 0.839 and 0.872 | Inside |
| M2 | E(r) table, band plus/minus 0.10 rad | Arm (b) steady window (chunks 50 to 59): measured E sits below the table value at the same window's pooled rate by 0.091 rad on average, per-episode range -0.131 to -0.046; 8 of 20 episodes fall below -0.10 | Mean inside; per-episode spread crosses the band on the low side (see below) |
| M3 | Peak E under sustained full drive (arm (b)), prediction 2.1746, band [2.0746, 2.2746] | Arm (b) mean peak E 2.030, 95% CI [2.016, 2.043]; per-episode range 1.968 to 2.060 | **Outside, below the band: a discrepancy for the panel** |
| M4 | MN9 rates under 200 Hz right-sugar drive, band plus/minus 25% (wider than plus/minus 5 Hz) | Arm (b): L 94.88 against [69.43, 115.71], R 62.39 against [46.80, 78.00]; arm (a): L 92.60, R 60.97, both inside | Inside |
| M5 | Estimator convergence, at most 10% of r after 2.0 s of constant drive | Arm (b), chunks 20 to 59: mean per-chunk relative gap 0.025, 95th percentile 0.060, maximum 0.122; 3 of 800 chunks above 0.10 | Inside on the mean; three single chunks above the band |
| M6 | Contact force | No band by registration; diagnostic only; no force claim made | Not applicable |
| M7 | Settle invalid rate | Zero invalid episodes in every arm; no arm paused | Inside |

On M3 and M2, stated together because they are one observation read two ways: the realised extension under sustained drive peaks at about 2.03 to 2.06 rad rather than the static map's 2.1746 rad, and the steady-window extension sits about 0.09 rad below the steady-state table. The direction is consistent (the dynamic body does not reach the quasi-static map's extreme), the size is at the edge of the M2 band and outside the M3 band, and nothing in the runs was adjusted in response: both are recorded here as discrepancies for the panel under section 10, with diagnosis, if the panel wants one, following section 13's pre-set order. The thin slice's peak of 2.0598 rad under a synthetic ramp sits in the same range, so the behaviour predates these episodes and is a property of the dynamic stack, not of any single episode.

## 7. Audit artefact

The machine-readable audit artefact for this pass is `results/closed_loop/characterisation_analysis_audit.json`, SHA-256 `ec28f5871bfbcc981d1e8706828b60a01c31a59df2dd3e39913921e69332ba4c`. It records, for every family member: the permutation seed, the permutations drawn (10,000), the extreme count, and the unrounded p-value; the bootstrap intervals; the TOST results and their bounds; the precision checks; the materiality computations; the per-arm endpoint summaries; the per-episode endpoint table for all 100 episodes; and the NumPy version (the body environment's NumPy 2.5.5; the frozen code's bootstrap streams are spawned from each member's permutation seed by the frozen code's own recorded convention). The Holm-adjusted value for each member is recorded as null, with the pending reason stated in section 5.

## 8. What this report does not claim

No Part 7 claim of any kind. No E-Total or E-Baseline claim. No claim that the closed loop improves feeding over the open loop: the registered endpoints show demonstrated equivalence within the registered bounds, and the sustainment difference is reported in its registered secondary form, not promoted. No biological claim: every number here is a property of this frozen brain model, this decoder and this body, on a raised substrate with the neck held, under the envelope labels stated. The characterisation stage of Part 5 is complete with this report; the results go to the panel with their hashes, and Part 7 follows under the same freeze.

## 9. Reconciliation (25 Nov 2026): endpoint definitions, required at the results gate

This section is a dated addition, written after the panel review of sections 1 to 8. The original text above is unchanged. Reviewer 2 returned PASS with no required changes. Reviewer 1 returned PASS conditional on report items, including one recomputation. Reviewer 3 returned REQUIRE CHANGES on one material point: endpoint reconciliation. All three replies are recorded verbatim in `docs/reviews/gate_reviews.md`. No episode was re-run, no frozen code was edited, and no registered definition, family member, seed or threshold was changed. Where this section and the original text differ, this section governs, and it says so at each point.

### 9.1 The endpoint mapping, established from the sources

Section 6 item 7 of the preregistration defines the contact duration endpoint as: "taste-event ON time within the episode (total ON chunks), and the longest continuous ON stretch". The episode is 100 chunks (section 2), so the registered endpoint totals the taste event over chunks 0 to 99.

The frozen analysis code (`src/closed_loop/analysis.py`, hash unchanged) computes its field `contact_duration_s` as the taste-event ON chunks over chunks 0 to 59 only, times 0.1 s: the stimulus period, not the episode. Its own header states this: "contact duration: event-ON time over chunks 0-59 (chunks x 0.1 s)".

**Conclusion: these are different estimands.** They total the same per-chunk taste event over different windows, the whole 100-chunk episode (section 6) against the 60-chunk stimulus period (the frozen code). The family member in section 5 was computed on the code's quantity. Under Reviewer 3's ruling, the registered section 6 definition governs the family member, and the code's quantity is retained as an implementation diagnostic. The same labelling applies to the other two divergences recorded in section 2:

- **Contact onset fraction.** The registered endpoint is section 6 item 6 (achieved E/E_max at the first chunk whose end-state has the taste event ON); it is the quantity M1 judges, and the section 3 and section 6 values stand on it. The frozen code's field of the same name holds the stimulus-period event fraction and is an implementation diagnostic.
- **Ignition.** The registered definition is section 6 item 8, and it governs the ignition claim: 20 of 20 for arm (a). The frozen code's stricter field (19 of 20, seed 5111) is an implementation diagnostic.

### 9.2 The family member, recomputed on the registered endpoint

The section 6 contact duration was recomputed per episode from the raw body logs for arms (a) and (b) on the registered seed list, and only the fourth family member was re-run, with the frozen procedure unchanged: sign-flip of the 20 per-seed paired differences, permutation seed 6003, B = 10,000, p = (1 + extreme count)/(B + 1), the frozen code's own functions imported and called. Every recomputed per-episode value was cross-checked against the audit artefact's recorded section 6 values and matched exactly.

| Member 4, (a) vs (b), contact duration | Value |
|---|---|
| Registered endpoint (section 6 item 7) | Arm (a) mean 8.995 s, arm (b) mean 5.505 s |
| Paired mean difference | +3.490 s, 95% CI [2.750, 3.910] |
| Extreme count (of 10,000) | 0 |
| Unadjusted p (unrounded) | 0.00009999000099990001 |
| TOST, section 7 rule | Bound plus/minus 2.24875 s (25% of arm (a)'s mean on this endpoint); 90% CI [2.840, 3.900]; equivalence NOT demonstrated |
| Holm adjusted p | null, pending Part 7 (as section 5 records) |

The frozen-code endpoint result (p = 1.0, paired difference -0.130 s [-0.390, 0.000]) stays in section 5's table and in the audit artefact as an implementation diagnostic. It is not the family member and supports no family claim.

Two consequences, stated plainly. First, the equivalence sentence in section 5 is superseded for contact duration: on the registered endpoint the arms are not equivalent; they separate, because arm (a)'s contact persists through the observation tail under the gate while arm (b)'s ends with its script. The peak E equivalence stands as written, restated in the registered wording: arms (a) and (b) are equivalent within plus/minus 25 percent on peak E (bound plus/minus 0.511 rad; 90% CI [-0.001, 0.025] rad). Section 8's sentence about demonstrated equivalence on the registered endpoints is likewise superseded for contact duration and stands for peak E. Second, the per-seed differences Reviewer 1 asked for are published as a machine-readable artefact, `results/closed_loop/characterisation_contact_duration_per_seed.json`, SHA-256 `738f7762cd6c3abf089b46353565f60efb2a74f0c2c5d4ab5a61915fbd973edf`, holding each arm's per-seed values on both endpoints and both differences, so the permutation result can be recomputed by hand. On the diagnostic endpoint the differences are mostly zero with a few of mixed sign nearly cancelling, which is exactly the configuration under which the frozen procedure returns p = 1.0; on the section 6 endpoint the differences are positive at every seed.

### 9.3 Holm: the Bonferroni-9 bound

Reviewer 1's bound, added at his requirement and labelled exactly as he prescribed: **Bonferroni-9 bound, not the registered adjusted value.** Each member's registered Holm adjusted value is at most min(1, 9 times its unadjusted value). On the five members as originally computed, the three floor members (unadjusted p = 1/10001) therefore have adjusted values at most 0.0009 and are claimed under the registered rule whatever the lesion members give, while (a) vs (b) peak E and the contact duration member as then computed are not claimed under any adjustment. The reconciliation in 9.2 changes the contact duration member's position: on the registered endpoint it also sits at the floor (unadjusted p = 1/10001, bound at most 0.0009), so it too is claimed under the registered rule; (a) vs (b) peak E (unadjusted p = 0.14538546145385461, bound at most 1.0) is not claimed under any adjustment. The exact adjusted values are computed by the frozen code over all nine members at Part 7, with no change to the family or its order; the audit artefact's nulls carry the reason, verified in this pass. One wording condition from the same ruling: the (a) vs (c) members are a sanity check, not evidence. With no drive every measure is zero by construction; their result shows the loop is silent without drive and carries no other weight, and nothing in this report rests on them beyond that.

### 9.4 M3 verification from the logged series (Reviewer 1's check; nothing adjusted)

Reviewer 1's explanation of the M3 discrepancy was checked against arm (b)'s logged command and filtered-rate series. His steady-state arithmetic holds: the logged filtered rate over chunks 20 to 59 averages 157.34 Hz, which the registered map reads as e = 0.909, matching his figure. The logged peak command is higher than the 0.93 his inference from peak E suggested: per-episode peak e averages 0.987 (range 0.958 to 1.000), and the logged filtered rate at the peak-command chunk averages 170.8 Hz (the map implies 170.5 Hz at that e). The shortfall sits between command and achieved extension: over chunks 20 to 59 the achieved E sits below e times E_max by 0.092 rad on average (95th percentile 0.118, maximum 0.119), and peak E sits 0.117 rad below e_peak times E_max on average. So the discrepancy is carried by the dynamic tracking offset between the commanded and the achieved extension, the same offset M2 records, not by the filtered rate failing to rise. M3 stays OUTSIDE its band as an explicit discrepancy; no band, constant or seed was adjusted. M2 is recorded as a known dynamic offset: the rate-to-extension table over-predicts achieved E by about 4 percent. Two forward notes from the same ruling, recorded for Part 7: intact arms peak at an achieved E/E_max of about 0.93, not at 1; and in Part 7, E is treated as a measured quantity, not as table-predicted.

On the calibration tail question from the same ruling: over chunks 20 to 59, the calibration episodes' pooled filtered rate (400 chunks) has its 95th percentile at 172.65 Hz (that is r_hi by construction), 10.8 percent of chunks at or above 170 Hz, and per-episode peaks averaging 171.9 Hz. Arm (a)'s pooled distribution over the same chunk range (800 chunks) is close in its upper tail (95th percentile 171.5 Hz; 7.6 percent of chunks at or above 170 Hz; per-episode peaks averaging 170.8 Hz) and lower in its mean (152.4 Hz against the calibration's 158.2 Hz). The records settle the composition part of the question: the calibration window is scripted on throughout, while arm (a)'s chunks 20 to 59 are gate-sustained and include chunks where contact, and with it the drive, was momentarily off, which lowers arm (a)'s pooled mean without much changing its peaks. No heavier onset-transient tail in the calibration set is visible in these records beyond that composition difference.

### 9.5 The persistence contrast, in its registered form

The registered binary result: gate-sustained ignition under section 6 item 8 in 20 of 20 arm (a) episodes, against extension offset in 20 of 20 arm (b) episodes once the scripted window closed (arm (a) offset in only 2 of 20 episodes, both late). The preregistration's claim rule for this contrast is the permitted-conclusions table in section 11 of the preregistration, first row, which covers exactly this outcome and gives the wording: "Closing the loop changed the feeding outcome under this encoder/decoder/body: contact-sustained drive maintained extension after the scripted window ended." The contrast is reported under that rule and not upgraded beyond it. And the plain sentence the equivalence requires: the equivalence on peak E means feedback does not change that endpoint; on contact duration, the registered endpoint, feedback does change the outcome, as 9.2 records.

### 9.6 Provenance of the section 6 quantities

The section 6 quantities were computed from the raw logs by analysis code written after the freeze: `work/run_characterisation_analysis.py`, SHA-256 `bafc1136a36ed07823baafa64f2aaf9efaafa7a2e9cbe4d3b22a4090e37d4ae6` (kept outside the repository, as with the earlier rungs' analysis scripts; the frozen code it supplements is `src/closed_loop/analysis.py`, hash unchanged). This reconciliation checked that script's outputs against section 6's text directly: in this pass, an independent script (`work/run_characterisation_reconciliation.py`, SHA-256 `da994ce68e1928422f63038f51d6fe1e9b7267cb3fe5587c9e330555358e8d14`) recomputed the section 6 contact duration, the longest stretch and the section 6 item 6 onset fraction from the raw body logs for all 100 episodes, and every value matched the audit artefact exactly. That recomputation is the check recorded here; the panel's re-review of this section is the independent check.

### 9.7 Deviation record and forward obligation

Recorded formally as a deviation: the frozen analysis code's field semantics diverge from the preregistration's section 6 text at three points (contact duration window, contact onset fraction, ignition strictness). The registered text governs in each case, per the rulings above. Forward obligation, recorded and not discharged here: the code fields are to be fixed by a hashed amendment before Part 7's analysis freezes. The characterisation code is not altered retroactively.

### 9.8 Envelope labels, re-checked

Arms (d) and (e) carry the OUTSIDE THE VALIDATED ENVELOPE label in the standing statements, in section 3's table note, and in their section 4 headings and text; arm (e) is additionally labelled a separate secondary, descriptive condition everywhere it is reported. Verified in this pass; no wording change was needed.

### 9.9 Updated audit artefact

The audit artefact has been updated in the same dated form: its original entries are preserved unchanged, and a `reconciliation_2026_11_25` entry adds the endpoint mapping, the reconciled member with its own fields (endpoint definition used, permutation seed 6003, extreme count 0, unrounded p, both bootstrap intervals), the reconciled TOST entry, the per-seed artefact reference, both script hashes, the M3 verification numbers, the filtered-rate tail comparison and the persistence counts. Updated SHA-256: `4115c963b46823bece0ca898cea1d16a1a7afab18617878fa66e71ebfe662222`. The gate remains open at the panel: Reviewer 3's REQUIRE CHANGES is answered by this section and awaits his re-review; Reviewer 1's conditions are discharged here except his closing request, which this section and the per-seed artefact now supply for his recomputation.
