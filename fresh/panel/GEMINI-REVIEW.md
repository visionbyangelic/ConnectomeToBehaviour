# Panel review — Gemini (Reviewer 2)
Date: 23 Nov 2026, ~14:58-15:00 WAT. Free tier, default Auto mode. Source chat: https://gemini.google.com/app/2ea60e6534c5fe87
Status: COMPLETE, all 5 sections answered, no refusals. Flagged 2 claims needing verification: (a) "no published embodied demo has passed the substitution test", (b) BANC exact publication status / release scope / proofread completeness / modelling tooling.

## 1. Missing
- Closed-loop sensorimotor feedback + sensory gating spec (proprioceptive / tarsal / labellar contact back into brain/premotor). Without it behaviours are triggered programs, not closed-loop control; substitution test "loses half its meaning".
- Timescale / rate-vs-spike mismatch spec: Brian2 ~0.1-1ms vs physics multi-ms; windowing/filtering, delays, aliasing/lag oscillation, smoothing hiding dynamics.
- Literature: Seeds et al. 2014 grooming hierarchy; Hampel/Simpson aDN grooming; Bidaye/Rayshubskiy/Sapkal locomotion/halting; initiation vs VNC CPG stepping distinction. Eckstein neurotransmitter predictions are probabilistic, not ground truth; gap junctions + neuromodulation missing in LIF graphs.
- Nulls underspecified: need multiple null families (degree/sign rewired + weight/activity-matched / label-permuted), multi-seed; pre-register exact endpoints/effect sizes/CIs ("±0.02" vague without metric); multiple-comparisons handling.
- Ungated failure modes: silent/runaway LIF states; decoder leakage/overfitting ("Clever Hans" decoder) — decoder must be FIXED before comparisons; provenance drift per stage (initiation vs kinematics vs termination).

## 2. Could be wrong
- Shiu as gold standard: approximation, not truth; calling cord "downstream/sideways" dangerous — behaviour depends heavily on VNC + feedback.
- Rule script is a strawman: needs matched-complexity baselines (stochasticity, latency, graded intensity, sugar-vs-bitter competition, state persistence), not a 3-line if/else.
- BANC: verify status/tooling; wiring ≠ calibrated dynamical model; scope-creep risk.
- Substitution test only PARTIALLY decisive: decoder is a bottleneck/amplifier; body controller already solves inverse dynamics; lesion "dead circuit" confound; shuffle rate-drop confound; null is ambiguous unless failure mode diagnosed.

## 3. Decisions
- D1 v630: AGREE (legacy snapshot, state caveats).
- D2 CPU-only: DISAGREE (conditional) — CPU for smoke/baseline, pre-budgeted GPU bursts for sweeps with strict CPU-GPU parity.
- D3 order: DISAGREE — feeding → walk/halt → grooming (locomotion central, don't squeeze it last).
- D4 cord depth: AGREE (BANC bounded stretch, full brain+cord = scope trap).
- D5 done: AGREE with tightening — null only after ruling out pipeline/decoder bugs.
- D6 panel every gate: DISAGREE — full panel only at high-consequence milestones, lightweight otherwise.
- D7 preserve old on branch/tag: AGREE.

## 4. Scope
Core achievable ONLY if tightly scoped; null defensible iff positive/negative controls prove decoder+body stack works. Stretch well gated; BANC and flyvis are each standalone subprojects — isolate strictly.

## 5. Biggest risk
Conflating decoder/controller engineering with connectome causality. Mitigation: lock decoder before substitution test; controllability sanity checks first; report intermediate neural/decoder signals for every condition, not just behaviour outcomes.
