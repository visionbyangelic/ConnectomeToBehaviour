# Amendment to the frozen analysis code (src/closed_loop/analysis.py), recorded for Part 7

27 Nov 2026.

I found that four fields in the frozen analysis code did not match what I registered in section 6 of the closed-loop preregistration. The characterisation report already recorded this divergence formally and left a forward obligation: fix the code by a hashed amendment before Part 7's analysis freezes. This amendment discharges that obligation. It changes the code only; it does not change the preregistration text, and it does not alter the characterisation code or results retroactively. The characterisation results stand exactly as reported. This amendment applies to Part 7 going forward only.

## What was wrong, and what I corrected

1. **contact_onset_fraction (section 6, endpoint 6).** The code computed the fraction of stimulus-period chunks (0-59) with the taste event ON, which is a duty cycle, not the registered quantity. The registered definition is the achieved E divided by E_max at the first chunk whose end-state has the taste event ON, with E_max = 2.1746 rad (section 3). The code now computes exactly that. If no chunk has the event ON, the field is None (no contact). The field name is unchanged.

2. **contact_duration_s (section 6, endpoint 7).** The code counted taste-event ON chunks over chunks 0-59 only. The registered definition is the taste-event ON time within the episode, and the episode is 100 chunks (0-99). The code now counts ON chunks over the whole episode (0-99) and multiplies by 0.1 s. I also added the second quantity endpoint 7 names: contact_longest_stretch_s, the longest continuous run of ON chunks, times 0.1 s. The field name contact_duration_s is unchanged.

3. **duty_cycle (section 6, endpoint 7).** The code set it equal to the old contact_onset_fraction, the mean over chunks 0-59. The registered definition is ON chunks divided by chunks in the gate-armed period. The endpoints function now takes an arm parameter (default None). For arm (a) the gate-armed period is chunks 20-99 (80 chunks). For arms (b) and (d) it is chunks 0-99 (100 chunks). Arm (e) shares arm (a)'s gating structure (scripted ignition 0-19, taste-gated 20-59), so it uses chunks 20-99, the same as arm (a); this matches the gate-armed period for that arm and matches the characterisation report's reading of arm (e). For any other arm, or when no arm is given, it is chunks 0-99. The ON chunks counted are within the gate-armed period only. The field name is unchanged. Part 7 configurations run in arm (a)'s closed-loop configuration (section 8), so the Part 7 caller passes arm="a" explicitly.

4. **ignition_arm_a (section 6, endpoint 8).** The code required drive applied on at least one chunk at or after 20 AND the event ON on at least one chunk at or after 40. The registered definition is contact at all, plus drive persisting via the gate beyond the ignition window, meaning any gate-ON chunk in 20-59. The code now returns True when contact occurred at all (any chunk in the episode with the event ON) and the taste event is ON in chunks 20-59. The drive application itself is a consequence of the gate, not a separate condition, so the code no longer checks it separately. The field name and boolean type are unchanged.

## Verification

The updated self-test passes. I also checked the corrected code against the characterisation audit artefact (results/closed_loop/characterisation_analysis_audit.json): on all 100 characterisation episodes, the corrected contact_duration_s, contact_onset_fraction, contact_longest_stretch_s, the arm-aware duty_cycle and the corrected ignition_arm_a reproduce the section 6 values recorded in the audit exactly, for all five arms (a) to (e), including arm (e) duty cycle. The unchanged fields (peak E, mean E, MN9 rates) also match the audit exactly on all 100 episodes.

## Notes and open points

(a) **Ignition, gate-ON versus gate-applied.** This amendment defines gate-ON as the taste event ON in chunks 20-59, as the registered text states. The characterisation reconciliation checked the related quantity "drive applied through the event gate in 20-59", which differs from event ON in 20-59 by the one-chunk feedback lag and at the period boundaries. On the 100 characterisation episodes the two give the same result on every episode, so this distinction has no effect on the recorded characterisation results. I record it here so the Part 7 analysis states which one it uses.

(b) **TOST bound for contact_duration_s.** The hardcoded bound in the code is 1.2 s. It was set against the stimulus-period contact duration, where the arm (a) mean was 5.275 s, so 1.2 s is about 23 percent of that mean, close to the registered plus or minus 25 percent rule (which gives 1.319 s). On the corrected whole-episode definition the arm (a) mean is 8.995 s, so 1.2 s is about 13 percent of the mean, substantially stricter than the registered plus or minus 25 percent rule (which would give 2.249 s). I have not changed the bound. It still applies as a valid, conservative equivalence bound, but it is no longer calibrated to the registered plus or minus 25 percent rule on the corrected definition, and it should be noted or reconsidered before Part 7's TOST is run on contact duration.

(c) **Caller obligation.** The Part 7 caller must pass arm="a" explicitly when computing endpoints for Part 7 configurations. The default arm (None) gives the 0-99 duty cycle, which is wrong for Part 7's arm (a) configurations. This is stated in the endpoints function docstring.

(d) **contact_onset_fraction is now None when there is no contact** (a type change from the old code, which always returned a float). Any downstream code that assumes a float must handle None. No existing caller uses the field except the self-test, so nothing breaks now, but Part 7 analysis code should be written with this in mind.

(e) **No other callers need updating.** The only callers of endpoints() are the suppression_ratio function and the self-test inside analysis.py itself, and the already-run characterisation analysis script, which passes no arm and will not be re-run. The default arm (None) keeps them working. The characterisation reconciliation script imports the module but only uses its constants and inference helpers, not endpoints().

## Code hash

Pre-amendment SHA-256 of src/closed_loop/analysis.py: 6861428ec6f392f8a470d44928e87be53bfcba2f8553fffad158b2c6190fc2ff. Post-amendment SHA-256: 0e2c1c7e29febe06ef2ee0e43d6727d4770f201a68c9e72b02ecda052cac97f1. The amendment is recorded by this hash.
