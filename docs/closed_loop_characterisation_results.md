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
