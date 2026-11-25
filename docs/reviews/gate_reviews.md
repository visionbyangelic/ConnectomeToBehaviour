# Part 4 gate — panel review under Angelic's overnight delegation

Gate: Part 4 sensory specifications (`fresh/PART4-SENSORY-SPECS.md`, 8,485 words). Panel majority decides under the delegation (24 Nov 2026, 02:18 WAT); Angelic ratifies or reverses on waking.

## Reviewer 3 — REQUIRE CHANGES (24 Nov 2026, 02:38 WAT)

Architecture, cadence, feeding pathway and qualification structure all accepted; the Part 2b conditions are genuinely incorporated. Four bounded specification clarifications required before approval (resolvable by amendment, no new experiments):
1. **Define the rate-to-joint mapping explicitly** — the normalised ramp equation and clipping; how the normalised value maps to each pitch joint's target; how Q2's measured extension signs enter the mapping; each joint's neutral/reference target; yaw and neck confirmed fixed at registered rest values. The signs may stay Q2 outputs, but the RULE for using them must not stay open.
2. **Make Q2's pass calculation reproducible** — the nine command points, the settling/measurement window per point, the steady-state-error definition, how coupling is measured and which joints count.
3. **Close the calibration/evaluation separation rule** — episodes designated calibration or evaluation BEFORE either runs; only calibration sugar-only episodes determine r_hi; evaluation never contributes to fitting/revising r_hi; r_hi recorded and hashed before evaluation begins; if r_hi fails the rejection bound (≤ r_lo + 10 Hz) the decoder is rejected, not rescued by changing the rule, data or split. Part 5 chooses scenarios and counts, not the separation rule.
4. **Make the false-ignition criterion operational** — define "false ignition" and a chunk "over any on-threshold"; an episode reaching the 30-chunk settle cap without settling is recorded INVALID, not silently replaced or extended.

## Reviewer 2 — APPROVE (24 Nov 2026, 02:39 WAT)

Voted after obtaining and checking verbatim extracts (§7 in full, the named constants-register rows, §§3.2–3.4, section list and word count) against the summary. All specification choices accepted, including the settle protocol, the registered feeding chain with r_hi's fixed fitting rule and rejection bound, and the Q0–Q6 gate with its no-adjustment/no-fallback rule. Three points checked and accepted as non-blockers: bitter's 200 Hz is a stated convention under §10 sensitivity obligations; Q5's single recorded food-offset adjustment is the one bounded pre-authorised exception to the no-tuning rule; Q4's ≤100 ms onset tolerance is exactly one chunk and must not be widened at gate time.

Status: R2 APPROVE, R3 REQUIRE CHANGES (amendment in flight), R1 pending. The gate closes when the amendment satisfies R3's re-check and a majority stands in favour.

## Reviewer 1 — REQUIRE CHANGES (24 Nov 2026, 02:39 WAT)

Design judged strong; five fixes (A–E) required before Part 5 builds against the specs, then re-read of changed passages only. (A) Stimulus envelope: Part 3 certified sugarR only — the specs must state which GRN set contact drives; stimuli beyond sugarR-right must either get follow-up benchmark rungs before Part 5 or be labelled outside the validated envelope (right-only drive would break the symmetric contact rule and contaminate RQ-C5). (B) Add the outstanding Part 2b conditions as gated deliverables between the qualification gate and Part 5: the 10–20 s episode with pre-fixed criteria and wall-clock, the aDN v630-annotation check, and the record rules. (C) Walk/halt: name the brain-side halt source or put it explicitly on the not-decided list; the walk/halt spec is an interface spec only until then. (D) Settle/thresholds across bodies: state whether the 2/8 transition thresholds and settle cap are re-derived for FlyBody (different geoms/units — state the mm conversion), that warmup uses no brain input so an invalid episode cannot depend on the experimental arm, and report the invalid-episode rate. (E) Resolve the 0.05 rad three-jobs problem and the hair-trigger onset in the register BEFORE r_hi calibration: offset threshold set at a multiple of the Q2/Q4-measured residual and frozen as a gate output; Q4's onset resolution stated (chunk vs physics-step); a pre-registered pooled-rate→expected-extension table; thresholded endpoints (onset, duration) declared secondary to graded endpoints (peak/mean angle) for the sugar+bitter conflict. Plus: contact carry-over timing for the one-chunk slice criterion (mid-chunk contact requirement or a carry-over rule); the 500 ms boxcar startup rule and EMA initial state; Q6's provisional ramp stated (r_hi is assigned later). Non-blocking Part 5 notes recorded in his vote (disjoint calibration/evaluation seeds; sensitivity coverage for r_lo, boxcar length, tau, hysteresis band; dust has no body channel in v1; FlyBody worker numpy check).

Status: R1 REQUIRE CHANGES, R2 APPROVE, R3 REQUIRE CHANGES — majority requires changes. One combined amendment (Pass 1) covers both reviewers' lists; re-check of changed passages follows with Reviewers 1 and 3.

## Amendment Pass 1 — re-checks (24 Nov 2026)

Pass 1 applied to PART4-SENSORY-SPECS.md (8,485 → 12,706 words), folding both reviewers' lists into one dated amendment with an Amendment history section; track.md entry appended, both copies SHA-256 identical (c7b1bfc9…). Substantive resolutions: offset threshold is now θ_off = 3 × ε_res (largest of Q2 steady-state errors / Q3 post-retraction residuals), formula fixed in §4.4, value frozen as a qualification-gate output; Q6 provisional r_hi = 155 Hz (Part 3's measured pooled MN9 response); all stimuli beyond sugarR-right labelled OUTSIDE THE VALIDATED ENVELOPE; calibration/evaluation separation rule binding in §4.3; walk/halt halt source NOT DECIDED, §5 declared interface spec only.

- **Reviewer 3 — CONFIRM (02:45 WAT).** Verified against the verbatim amended §4.3, §7.3, §2.4, §2.3, §9 and §8 r_hi row supplied on request. All four of his items resolved; none remain open.
- **Reviewer 2 — APPROVE STANDS (02:45 WAT).** No objection, no new conditions; checked item by item that no Pass 1 change loosens a definition, widens a tolerance, or reopens the Q0–Q6 verdict/no-tuning rules; confirmed θ_off does not loosen the Q2/Q3 ≤ 0.05 rad pass limits.
- **Reviewer 1 — re-check pending** (verbatim passages supplied on request; verdict to follow).

## Reviewer 1 — CONFIRMED (24 Nov 2026, 02:47 WAT)

All items A–E and small items (4)–(6) confirmed against the verbatim amended passages and the text-search results. During the re-check he caught a genuine hole in E(1): the gate tolerances permit ε_res up to 0.05 rad, so θ_off = 3 × ε_res could reach 0.15 rad — at or above the 0.10 rad onset, inverting the hysteresis band — and no passage guarded against it. Confirmed on search that none existed; the **band guard** was added to §4.4 and §7.7 as the R1-E(1) addendum (θ_off must lie strictly below onset; if 3 × ε_res ≥ 0.10 rad, θ_off is not frozen, the qualification gate FAILS at that step, and the failure returns to the panel by formal amendment — multiplier, onset and tolerances not adjusted to fit). Reviewer 1 confirmed E(1) including the guard. His standing note on (A): labelling gives honesty, not validity — non-sugarR results remain extrapolations unless the panel requires a follow-up rung.

## GATE CLOSED — Part 4 approved under delegation (24 Nov 2026, 02:47 WAT)

Final tally on the amended document (Amendment Pass 1, incl. the band-guard addendum): Reviewer 1 CONFIRMED, Reviewer 2 APPROVE STANDS, Reviewer 3 CONFIRMED — unanimous. Part 4 is CLOSED under Angelic's overnight delegation; she ratifies or reverses on waking. Next authorised steps: the §7 feeding-body qualification gate (Q0–Q6), the §2.4 acceptance test, the §6 thin FlyBody slice and the §6.1 companion deliverables, then the Part 5 build and freeze.

## Qualification gate failure + Amendment Pass 2 (24 Nov 2026)

The §7 qualification gate was executed and **FAILED at Q1**, stopped per §7.7 (record: `fresh/FEEDING-BODY-QUALIFICATION.md`). Q0 PASS (all five pinned files hash-match, no download). Q1(a) PASS (packaged single-steps replay, 2.0 s, finite states, 28.86 mm travel). Q1(b) NOT EXECUTED → Q1 FAIL under the "both run without error" criterion: `flygym_demo/muscle_imitation/` is **not FlyBody** — its own package documentation states the body model is FlyMimic's musculoskeletal MJCF — and its env module requires gymnasium, absent from the pinned body env. Verified independently from the installed package source. The misdescription entered at the Part 1b audit (§5) and was carried into §7.2 unchecked; a dated correction note has been appended to the audit. A specification-premise failure, not a body failure: no parameter adjusted, no fallback, nothing frozen; ε_res/θ_off not evaluated.

**Amendment Pass 2 (proposed):** strike the muscle_imitation sub-item from §7.2; replace with a load-and-step of the pinned FlyBody artefact itself through the standard FlyGym Simulation construction (Part 1b Demo C configuration), zero command, 2.0 s; pass rule unchanged (both run without error, all states finite); the amendment text itself records the history in §7.2. On approval the gate re-runs from Q0 with no carry-over.

- **Reviewer 2 — APPROVE (02:55 WAT).** No changes, no new conditions: the replacement preserves Q1's purpose and weakens nothing; zero command avoids a control confound.
- Reviewers 1 and 3: votes pending.
- **Reviewer 3 — APPROVE (02:55 WAT).** Striking muscle_imitation loses no FlyBody evidence (it tested a different body); the replacement tests the pinned artefact itself with no tuning that could mask a defect; the conjunctive pass criterion is retained; the gate correctly restarts from Q0 rather than carrying Q1(a) forward. Scope noted: approval covers the §7.2 wording only.
- **Reviewer 1 — vote pending** at the time of application.

**Pass 2 APPLIED under delegation (24 Nov 2026, 02:56 WAT)** on the 2–0 majority (Reviewers 2 and 3), per Angelic's rule that authorised work does not wait. §7.2 replaced with the approved text; Amendment history gained the Pass 2 entry. The qualification gate re-runs from Q0 under the amended §7.2.

## Reviewer 1 — Pass 2: REQUIRE CHANGES, revision applied (24 Nov 2026, 02:58 WAT)

Reviewer 1 verified the premise evidence himself against the published package and confirmed the Q1 FAIL under the unamended text was correct. Two required changes: (1) honest framing — the replacement Q1(b) is a net smaller test, is first-party code not an upstream demo, and FlyBody integrity rests on Q1(a) + Q2–Q6; the "strengthened, not weakened" framing is withdrawn. (2) Rest-behaviour criteria for Q1(b), bounds fixed before (b) is first executed and recorded in the constants register, each sourced from the pinned model: thorax height within stated bounds, a stated per-joint velocity bound, no joint-limit violations (proboscis included) with an explicit tolerance. Both accepted and applied: §7.2 revised (bounds: thorax ∈ [0.5·h_0, 1.5·h_0], h_0 = the pinned artefact's initial-state thorax height recorded before (b) runs; |qvel_j| < published range_j / 0.01 s; joint-limit tolerance ε = 0.005 rad per §7.3(ii); 20,000 steps at dt = 1e-4 s from the pinned mujoco_globals.yaml; qpos/qvel recorded every step), §8 register row added, Pass 2 history entry revised. The in-flight re-run under the unrevised text was stopped before Q1(b) executed. Reviewer 1 confirms the revised verbatim text as final; the gate then re-runs from Q0. Reviewers 2 and 3 are sent the revised text as a confirmation check (their approvals covered the strike/replace substance; the revision only adds criteria and honest labels).

## Part 2b record completion — discharged (24 Nov 2026, 02:58 WAT)

All of Reviewer 1's Part 2b conditions are now discharged (record: PART2B-BUILD.md §10; gate log updated). Bit-for-bit claim STANDS with a qualification: chunked ≡ single exactly at a fixed build position (SHA-256 of canonicalised trains equal under both structures), but successive same-seed builds in one process alternate between two RNG streams — the original probe's archived evidence was luck, its conclusion right; the bridge (fresh process, one build per episode) and Part 3 are unaffected. Clarifications applied from the data (pulse = decaying EMA tail; 12.72 mm = mean of the three closed episodes' chunks 10–19; loop speed ≈12.7 mm/s vs the audit's ≈10.7 over a different window; 0.474 = the ramp value at 20 Hz; JON rate 150 Hz confirmed; wall clock 46.5–50.5 s per simulated second closed, 34.5 open). Bilaterality: aDN2 is a bilateral type and the set holds its left member only — NOT an extraction error (the published experiments read out the left only); anatomical incompleteness, registered as G2; aDN1 undetermined; frozen sets unchanged. Long episode (15 s, seed 4203): ALL pre-fixed criteria PASSED — 150/150 chunks, posture drift 0.003 mm, memory growth 3.4 MB, 47.2 s/sim-s (first attempt killed by a machine reboot, re-run unchanged, recorded).
- **Reviewer 2 — APPROVE STANDS on the revised Pass 2 (03:00 WAT).** Accepted Reviewer 1's framing correction as his own; checked the rest-behaviour bounds criterion by criterion; noted the stopped re-run leaves no (b) result to contaminate the re-run.
- Reviewer 1's confirmation of the revised §7.2 and Reviewer 3's confirmation check: pending.
- **Reviewer 3 — APPROVE CONFIRMED on the revised Pass 2 (03:01 WAT).** No outstanding objection; bounds, sourcing and failure handling all accepted; scope noted (wording only — the gate must still pass in full).
- Reviewer 1's confirmation of the revised §7.2: pending — the last vote needed before the re-run.

## Reviewer 1 — Pass 2 NOT confirmed as final; Q2/Q3 finding (24 Nov 2026, 03:03 WAT)

Both Pass 2 changes are carried and the bound sourcing is sound, but Reviewer 1 confirms §7.2 as final only once three one-line additions are made: (A) an h_0 sanity check before (b) runs (h_0 may be a drop height, not a standing height — the gate stops and the criterion is amended if the neutral-pose standing height falls outside the band); (B) the velocity bound scoped to the 102 actuated joints, the free joint excluded; (C) "zero command" defined as ctrl = 0 on all 102 actuators, with the spring-rest expectation recorded (42 springref joints; rostrum pitch rests at q̂(0) ≈ 0.185 against its 0.183 limit, inside ε by ≈0.002 rad). **More serious:** his file analysis shows Q2 and Q3 may fail by construction — the proboscis servos fight their passive springs (q̂ = (kp·ctrl + ks·ref)/(kp + ks)); pitch-joint raw error ≤ 0.05 rad only for ctrl ∈ [0.583, 1.017], outside the rostrum's range; labrum achieves 0.25 × ctrl. **Verified independently against the Q0-hashed pinned files: the arithmetic is exact** (joints.yaml group_003 stiffness 3; springref 0.8 on both pitch joints, none on labrum/yaw; actuators.yaml kp 10 head / kp 1 antenna-labrum; 42 springref entries). Reviewers 2 and 3 confirmed the revised Pass 2 (03:00/03:01 WAT) before this finding landed; their confirmations stand for §7.2's substance and are superseded in sequence by Pass 3, which they now vote on.

## Amendment Pass 3 — applied as draft, panel vote open (24 Nov 2026)

A–C added to §7.2. The spring-fight fix: §4.3 gains the published-parameter static map + feedforward inverse (chain targets are intended achieved angles; map never fitted); Q2 judges map-relative error ≤ 0.05 rad and records the empirical map (monotone required); Q3 reach judged against map-predicted achieved E; ε_res takes Q2's map-relative errors; §8 registers the map; the labrum's achieved full-open is q̂(1.05) ≈ 0.26 rad, and E_max is the achieved E at e = 1 measured at Q3. No body parameter touched. The gate re-run stays HELD until the panel confirms Pass 3 (Reviewer 1 confirms §7.2 + Pass 3 as final; Reviewers 2 and 3 vote).
- **Reviewer 2 — APPROVE Amendment Pass 3 (03:06 WAT).** Independently recomputed the spring-fight arithmetic; map-relative Q2 and the feedforward preserve the gate's purpose; A–C correct; no conditions.
- Reviewer 1's final confirmation and Reviewer 3's Pass 3 vote: pending.
- **Reviewer 3 — REQUIRE CHANGES on Pass 3, one bounded issue (03:07 WAT):** Q3 as amended can be vacuous — reaching 90% of a small map-predicted extension certifies model-consistency, not functional feeding capability. Either a pre-run independently sourced minimum functional extension, or an explicit narrowing of Q3's claim with functional reach carried by Q5. **Fix applied (the narrowing route):** §7.4 gains "Q3's claim, stated narrowly" — Q3 qualifies model-consistent extension only; functional reach is qualified at Q5 (labrum contact with body-reported force inside the single allowed offset adjustment; failure there is a gate failure and the body is not accepted on Q3's evidence); §7.7's verdict rule now states the gate's feeding acceptance rests on Q5; §8's map row now states Q2's errors and ε_res are map-relative to q̂ (his register point). Sent to Reviewer 3 for confirmation.
- Reviewer 1's final confirmation of §7.2 + Pass 3: pending.
- **Reviewer 3 — CONFIRM, Pass 3 as amended APPROVED (03:09 WAT).** The narrowing resolved his objection in full; no further changes from Reviewer 3; no outstanding Part 4 objections.
- **Reviewer 1 — §7.2 with A–C CONFIRMED AS FINAL (03:08 WAT). Pass 3: one required change + four clarifications.** Required: the map must be the CLAMPED map q̂_eff(ctrl) = clamp(q̂(ctrl), published range) — unclamped, q̂ at the rostrum's top sweep points exceeds the 0.183 limit (q̂(0.183) = 0.325) while the measured state sits at the limit, so map-relative Q2 still failed by construction there (verified: error 0.142 > 0.05). Clarifications: (1) state which range clips ctrl (joint range vs actuator ctrlrange, from the pinned files); (2) define the zero-extension command (what the chain writes at r ≤ r_lo; rest = the settled pose at ctrl 0, not intended angle 0); (3) monotonicity — plateaus accepted only where the clamp binds; (4) the analytic rule is the frozen object for Part 5, the empirical map its audit; disagreement beyond tolerance is Q2 failing. Panel note recorded: the Part 1b "calibrated ranges" rationale for FlyBody is weakened — achievable rostrum ≈ −0.77 rad (not −1.24), labrum full-open ≈ 0.26 rad; loop closure (the deciding reason) still holds and Reviewer 1 would not reverse the choice; the spec must call extension amplitudes servo-limited model outputs, not physiological quantities, and report E_max as a fraction of the published range.

## Pass 3 revision — applied (24 Nov 2026, ~03:14 WAT)

Reviewer 1's required change and all four clarifications carried: the map is the clamped map q̂_eff everywhere (§4.3, §7.3, §8); the ctrl clip is the published joint range — verified equal to the compiled model's actuator ctrlrange for all five proboscis actuators (Demo C construction, read from the compiled model directly), re-read and recorded at Q0 as a premise check; e = 0 defined as ctrl = 0 on the five DoFs with θ_rest the settled pose under it; empirical map strictly increasing wherever the clamp does not bind, plateaus only at clamp-bound points (§7.3, and the same clause added to Q6); the analytic rule named the frozen object for Part 5, the empirical map its audit, disagreement beyond tolerance = Q2 failure; §4.3 now states extension amplitudes are servo-limited model outputs, not physiological quantities, with E_max reported as a fraction of the raw-range extension. Sent to Reviewer 1 for final confirmation; Reviewers 2 and 3 notified (revision corrects the map's definition and adds clarifications; nothing loosened).
- **Reviewer 2 — APPROVE STANDS on Pass 3 as revised (03:12 WAT).** The clamp is a correction, not a loosening (recomputed q̂(0.183) ≈ 0.325); clarifications and the panel note accepted; no conditions.
- Reviewer 1's final confirmation and Reviewer 3's stands-check: pending.
- **Reviewer 3 — CONFIRM STANDS on Pass 3 as revised (03:13 WAT)**, with one proviso: the clamped map must be used consistently in all acceptance calculations, with no residual unclamped reference, and a Q0 ctrlrange mismatch must stop the gate rather than invite a choice. Proviso discharged in the text: a grep over the document found exactly one bare-q̂ use (§7.2's expectation sentence — narrative, not a criterion), now rewritten to name q̂_eff(0) = 0.183 as the resting value; §4.3's Q0 premise check now states a mismatch stops the gate. All acceptance calculations (Q2 error, Q3 prediction, feedforward, ε_res) reference q̂_eff.
- Reviewer 1's final confirmation of Pass 3 as revised: pending — the last vote.

## Reviewer 1 — Pass 3 as revised CONFIRMED AS FINAL (24 Nov 2026, 03:13 WAT). Panel complete on Passes 1–3

All five of his points carried (clamp, four clarifications, panel note). Reviewers 2 and 3 both re-confirmed the revised lines (APPROVE STANDS 03:12; CONFIRM STANDS 03:13), so the panel is complete on the final text, 3 of 3. Four record items from Reviewer 1: (1) clamp-bound identified from the analytic rule — **applied to §7.3**; (3) the safety margin's locus stated once — **applied to §4.4** (margin applies to intended achieved angles in the chain/Q3/Q6; Q2's sweep exempt by design); the §4.3 force-cap parenthetical corrected per his check (caps do not bind inside the proboscis's clamped ranges); (4) Q3's narrowed claim to be kept in the gate record's wording — noted for the re-run record. **(2) Limit penetration — the estimate does NOT clear ε:** computed from the pinned files (solreflimit τ = 0.001 s from joints.yaml; effective constraint mass at the rostrum joint from the compiled model, m_c ≈ 0.000101 — essentially the armature alone; net static force into the limit at the top sweep point ≈ 1.85), the predicted penetration is **≈0.018 rad, about 3.6× ε = 0.005**. So §7.3(ii)'s out-of-range criterion would fail by construction at the rostrum's clamp-bound points even with the body behaving exactly as published. Per Reviewer 1's own rule, amending ε is a loosening and returns to the panel: **Amendment Pass 4 (bounded) is now before the panel** — judge out-of-range at each point against max(ε, δ_pred(point)), with δ_pred computed from the pinned files per point and recorded before the sweep runs; ε remains the floor everywhere else. Q1(b) is unaffected (at ctrl 0 the rostrum's net force into its limit is ≈0.02, δ ≈ 0.0002 rad).
- **Reviewer 2 — APPROVE Pass 4 (03:18 WAT)**, no conditions (noted the first-order formula is ≈0.002 rad conservative vs the self-consistent value).
- **Reviewer 3 — REQUIRE CHANGES on Pass 4 (03:17 WAT)**, bounded and technical: the structure (per-point max(ε, δ_pred), pre-recorded) is accepted, but δ_pred = F·τ²/m_c is not accepted as established — the compiled constraint's solimplimit impedance and solver configuration also govern penetration. Required: a pinned-model derivation or pre-run static calculation accounting for the compiled solimplimit and constraint-space response, with the full per-point record frozen before the sweep (source values with signs, ctrlrange, solreflimit AND solimplimit, m_c and its extraction, the exact equation/procedure, resulting thresholds); no measured outcome may enter. Derivation under way from the compiled model + MuJoCo's documented constraint relation.
- Reviewer 1's Pass 4 vote: pending.

## Pass 4 — WITHDRAWN; panel converged; gate re-run launched (24 Nov 2026, ~03:22 WAT)

Reviewer 1 REQUIRE CHANGES on Pass 4 as worded (03:19 WAT): his one-joint MuJoCo replica from the pinned parameters measures ≈0.0018 rad penetration at the top point (formula said 0.018 — the closed form omits the solimp impedance factor) and ≈0.0009 at ctrl 0; his preferred path was withdrawal + calibration. Reviewer 3's required derivation is supplied by MuJoCo's documented rest-penetration relation (r = a_u·(1 − d)·τ²·ζ²): with the compiled values — solref (0.001, 1), default solimp (0.9, 0.95, 0.001, 0.5, 2) on all five proboscis joints, read from the compiled model — it gives ≈0.0009–0.002 rad, agreeing with the replica. Reviewer 2's APPROVE of the loosening is moot: no loosening occurs. **ε = 0.005 stands unamended; the calibrated expectation (≈0.001–0.002 rad at the rostrum's clamp-bound points, inside ε) is recorded as a pre-gate calibration.** The qualification gate re-runs from Q0 under Passes 1–3 only.
- Reviewer 3 — no objection to the Pass 4 withdrawal (03:21 WAT): the derivation requirement is met and dissolves the amendment; no tolerance changed at all.
- Reviewer 2 — NO OBJECTION to the Pass 4 withdrawal (03:21 WAT), his Pass 4 APPROVE withdrawn with it; acknowledged his own self-consistency check missed the impedance factor too. Panel fully converged: ε unamended, calibration recorded, gate re-running under Passes 1–3.
- Reviewer 1 — NO OBJECTION to the withdrawal route (03:22 WAT); his preferred path's steps are met (compiled values = replica's assumptions; calibration recorded; no amendment). One wording condition for the gate record: the ctrl = 0 (Q1(b)) expectation must be stated as "≪ ε, about 0.001 rad or less" and described as an expectation, not a measurement — the documented relation under-predicts the replica there (≈2e-4 vs ≈9e-4), an unexplained gap that changes nothing. Noted to the re-run. The Q0–Q6 results go to the panel for review when the re-run finishes.

## Qualification gate re-run (24 Nov 2026, ~03:34 WAT) — Q0 PASS, Q1 PASS, Q2 FAIL (specification premise)

Q0 PASS (incl. ctrlrange premise check: compiled ctrlranges equal the YAML ranges exactly; solref/solimp as expected). Q1 PASS both parts (replay 28.86 mm reproduced; load-and-step clean, h_0 = 2.34 mm, no joint left its range at any step). **Q2 FAIL, criterion (i), both pitch joints:** steady-state error vs q̂_eff ≈ 0.186–0.188 rad (tolerance 0.05); yaw/labrum pass at ≤0.0002; coupling, limits, monotonicity all clean. Diagnostic (not a gate step; independently re-verified by the author): **the compiled model's spring reference is qpos0 = 0 for all five proboscis joints** — the package's construction does not carry joints.yaml's springref (0.8) into the compiled model, while stiffness 3 is applied. The measured offset equals the missing term exactly, (3/13)·0.8 = 0.1846; the same recorded steady states fit the ref = 0 map to ≤0.0035 rad on every joint. A third specification-premise failure — the map read a parameter from the YAML; the pinned compiled artefact is the body. Q3–Q6 not run; no E_max, no arena offset, no ε_res frozen (band guard moot: Q2's error term alone would give θ_off ≥ 0.563). **Amendment Pass 5 is now before the panel:** the map's parameters are read from the compiled artefact (kp from compiled gainprm, ks from compiled jnt_stiffness, ref from compiled qpos0 — here 10/1, 3, and 0 for all five joints); Q0 records those values as a premise check; the springref-dependent text is corrected (§7.2's limit-resting expectation withdrawn — the re-run measured rest −0.0033 rad, no penetration, consistent with ref = 0; achievable rostrum pitch under the corrected map reaches q̂(−1.24) ≈ −0.954 rad, and no proboscis point is clamp-bound); the gate re-runs from Q0 on approval.
- **Reviewer 2 — APPROVE Pass 5 (03:36 WAT)**, no conditions: compiled-artefact provenance is the right general rule (closes the YAML→compiled divergence class; Q0 recording makes it enforceable); the full re-run from Q0 is required, not wasteful (Q0's scope changes; the no-carry-over rule keeps every record under the spec version in force); noted the ≤0.0035 rad fit is diagnostic evidence, not a gate result — the re-run must re-measure.
- Reviewers 1 and 3: pending.
- **Reviewer 3 — APPROVE Pass 5 (03:36 WAT)** with the provenance/freeze requirements explicit (met in the text; Q0 record labelled per joint, map authority = compiled parameters, the fit recorded as corroboration not estimation; the failed run's Q2 failure stands, not relabelled).
- **Reviewer 1 — APPROVE Pass 5 conditional on three one-line edits (03:37 WAT)**, all verified and incorporated: (1) ref read from **qpos_spring** (not qpos0 — separate fields; both recorded at Q0 and both verified 0.0 for the five joints; gainprm[0] = −biasprm[1] verified 10/10 and 1/1); (2) the corrected prediction table (9 × 5) pre-registered with a timestamp before Q2 runs (§7.3); (3) the construction call and its neutral pose recorded in the gate record (§7.1). He also confirmed the mechanism from the wheel source (add_joints' neutral-pose override) and owned the Pass 3 analysis error on the record. **Pass 5 is panel-complete (3 of 3) and APPLIED; the gate re-runs in full from Q0 under Passes 1–3 and 5.**

## Qualification gate, third execution (24 Nov 2026, ~03:56 WAT) — Q0–Q4 PASS, Q5 FAIL (a real functional finding)

Q0 PASS (Pass 5 premise record confirmed per joint; construction + neutral pose recorded). Prediction table pre-registered before Q2 (no clamp-bound points). Q1 PASS (replay exact; load-and-step clean, no limit-resting, as Pass 5 predicted). **Q2 PASS — max map-relative error 0.0035 rad (rostrum), others ≤0.0011: the corrected map is confirmed as a genuine pre-registered prediction.** Extension signs s = −1 (both pitch joints); θ_ext −1.19 / −1.54 rad. Q3 PASS (narrowed claim): all cycles reach 1.0008 × predicted; **E_max = 2.1746 rad = 0.7695 of the raw-extremes E**. Q4 PASS (peak-E range 0.0 across 5 fresh instances; onset range 0 ms). **Q5 FAIL:** at full extension (E = 2.1746) the labrum surface stops ≈0.246 mm short of the ground-level food disc's top — a vertical shortfall; both placements the rule allows were tried (0.6 mm spec offset; the one adjustment, 0.146 mm, food under the extended tip's projection) with zero contact force from labrum and tarsi; the arena itself verified sound (food compiled at the placed position, 69 contact pairs). Q6 not run; ε_res/θ_off NOT frozen (arithmetic recorded as such: 0.0035 → θ_off ≈ 0.0105, inside the guard). This is the functional-reach question Pass 3 reserved to Q5, answered no for a ground-level substrate in this construction: model-consistent extension (Q3) does not reach the ground. Per §7.7 the failure returns to the panel by formal amendment — **Pass 6 question now before the panel**: (a) amend §4.6's substrate (food disc on a fixed low pedestal whose top sits within the measured reach, height derived from the recorded geometry and registered before any re-run); (b) amend the registered chain to include head pitch in the extension (a larger change — the decoder's meaning changes); (c) the Part 1b pre-named rescope (primary endpoint becomes MN9 plus a stated non-feeding measure; feeding contact dropped).
- **Reviewer 3 — Pass 6 vote: OPTION (a), substrate amendment (03:58 WAT)**, with binding conditions: (1) the pedestal height is derived from the recorded geometry (labrum surface reach ≈0.296 mm at e = 1), never searched; (2) a predeclared clearance margin ≥ 0.05 mm below the measured reach — z_top ≤ 0.246 mm (the floated 0.25 mm does NOT meet it; 0.20–0.24 defensible); (3) one height/geometry/placement frozen and hashed in the amendment before the re-run, no adjustment after seeing Q5; (4) Q5's criteria unchanged, contact must result from the registered movement, and the resting configuration must not already produce contact; (5) nothing else changes (food shape, contact properties, body, event definition, chain). Full re-run from Q0; ε_res/θ_off not frozen from arithmetic. Reviewers 1 and 2 pending.
- **Reviewer 2 — Pass 6 vote: OPTION (a) (03:59 WAT)**, conditions: pedestal derived from recorded geometry and bounded both sides — food top T with R ≤ T ≤ R + 0.05 mm (R ≈ 0.296, press/overlap 0–0.05); predicted contact-onset e registered; pedestal fully specified in §4.6 (footprint, height, under the disc only, no intersection with body/legs, arena re-verified); Q5 criteria unchanged, both horizontal placements on the same fixed pedestal; **one-time** — if Q5 fails under (a), no further pedestal change, the panel returns to (b)/(c); full re-run from Q0. **CONFLICT NOTED:** Reviewer 3's condition (2) bounds z_top ≤ R − 0.05, which on the recorded geometry (labrum surface's lowest point z = 0.296 at e = 1; contact requires T ≥ 0.296) would guarantee no contact — the two approving reviewers' height bounds are mutually exclusive. The discrepancy has been put back to Reviewer 3 for confirmation or correction, and flagged to Reviewer 1 (vote pending) to arbitrate. Pass 6 direction (a) has a majority (R2 + R3); the height is NOT yet fixed.
- **Reviewer 3 — geometric correction (04:01 WAT):** his z_top ≤ R − 0.05 condition is withdrawn as a **sign slip**; Reviewer 2's bound R ≤ T ≤ R + 0.05 is the geometrically correct one, and the candidate T = 0.33 mm (press ≈0.034) is accepted within it, subject to the pre-run compiled-geometry and resting-contact checks. **Pass 6 is therefore agreed by both voting reviewers on identical terms and is APPLIED** (§4.6 pedestal, T = 0.33 mm; §7.5 resting-contact check + predicted-onset registration; one-time clause). The gate re-runs in full from Q0 under Passes 1–3, 5 and 6. Reviewer 1's Pass 6 vote is still pending; it will be logged when it lands and any dissent handled on the record.
- **Reviewer 1 — Pass 6 vote: OPTION (a) (04:03 WAT) — Pass 6 is UNANIMOUS.** His arbitration confirms the bound R ≤ T ≤ R + 0.05 and T = 0.33 as a value (press 0.034), and his review of execution #3 finds Q0–Q4 coherent (E_max fraction 0.7694 ≈ map slope 10/13), with one caution recorded: **Q4's zero ranges show determinism/reproducibility, not robustness — never to be cited as variability evidence.** His vote carries conditions that revise the amendment's machinery: (1) a **reach curve** (labrum lowest surface z against achieved E/E_max, kinematics only, no food) recorded before the re-run; (2) a **plausibility cap** on pedestal height (≤0.6 mm ≈ a quarter of the 2.34 mm standing thorax height; T = 0.33 satisfies it); (3) a **pre-registered decision rule**: default T = R + 0.034 = 0.33, compute the contact-onset fraction f_c(T); if f_c > 0.95 use the window's upper end (T = R + 0.05) and recompute; if f_c still > 0.95 the geometry gives no usable graded range and **(c) applies**; T and the rule frozen and hashed before the re-run — and 0.33 needs its stated rule, not a bare number; (4) Q5 additions: measured onset fraction recorded; no pedestal contact with any other body part; (5) **honest labelling**: the pedestal is an engineered arena parameter (class D); every claim states this body as registered cannot contact ground-level food with the neck held, and feeding is demonstrated on a raised substrate; neck pitch joins §9's not-decided list; (6) **the dead-zone fix is part of the amendment**: the registered intended angles at e = 1 (rostrum −1.19, haustellum pitch −1.54) need feedforward ctrl of 1.3·θ = −1.547 / −2.002, beyond the published ranges, so they clip and achieved extension saturates at e ≈ 0.80/0.79 — the top fifth of the decoder's range is dead, and r_hi sits in it; the e→θ interpolation must be redefined so e = 1 is the achievable extreme; (7) a sensitivity obligation (onset fractions at other window heights); (8) full re-run from Q0. **One discrepancy to reconcile:** his one-shot rule makes (c) automatic on a Q5 failure; Reviewers 2+3's agreed wording returns the choice to the panel between (b) and (c).
- **Action taken (04:04 WAT):** the fourth execution, ~90 seconds in and not yet at Q5, was STOPPED before it could produce a result under the unrevised text; nothing from it counts. The reach-curve calibration runs now; a revised Pass 6 text (decision rule + dead-zone fix + conditions) goes to all three reviewers with the reach table, and the one-shot discrepancy is put to Reviewers 2 and 3.
- **Reviewer 3 — CONFIRM Pass 6 revised text (04:12 WAT)**, with the standing record-keeping qualification (execution #3's Q2–Q4 passes are historical results under their configuration, never carried into the amended re-run — the full re-run from Q0 resolves it). **Reconciliation: he joins Reviewer 1 — a valid Q5 FAIL under the amended substrate triggers the Part 1b rescope (c) AUTOMATICALLY** (a further chain change after the bounded accommodation fails would be outcome-dependent scope tailoring; the rescope was pre-named for this), with the distinction that an invalid/interrupted Q5 execution is resolved under the execution rules, not misclassified as a scientific failure. The one-shot clause therefore carries R1 + R3 (majority) for automatic rescope; Reviewer 2's answer will be logged when it lands. Confirmations of the revised text still pending from Reviewers 1 and 2.
- **Reviewer 2 — CONFIRM Pass 6 revised text (04:13 WAT)**, no changes; he verified f_c by interpolation and added a checked clarification now in the record: the labrum's feedforward factor is (kp+ks)/kp = 4, so its old θ_ext = 1.00 needed ctrl 4.00 against a 1.05 limit and the labrum saturated from e ≈ 0.26 — the worst of the dead zones. His Q5(vi) understanding is recorded: a material deviation of the measured onset from 0.884 is a discrepancy for the panel, not a number to be passed over. On reconciliation he held the panel-return wording (see below).
- **Reviewer 3 — CONFIRM (04:12 WAT)** (logged earlier).
- **Reviewer 1 — CONFIRM, conditional on four additions (04:14 WAT)**: (1) f_c stated on the measured E/E_max axis and Q5(vi) measured on the same axis — clarified in §4.6 (E is achieved, so the axis is definition-independent); (2) a **whole-body pedestal clearance check before the re-run** (mj_geomDistance, pedestal vs every non-labrum geom across e ∈ [0,1] and at rest, minimum clearance per geom recorded, all clearances pre-registered > 0 with a stated margin) — running as a calibration now; (3) register reconciliation — E_max 2.1746 (the §4.4 segment-pitch sum) vs the joint-angle sum 2.1787, and the raw-extremes E 2.8264 vs 1.24 + 1.59 = 2.83: both definitions to be pinned exactly (the calibration in (2) also computes these); (4) the 0.05 rad safety margin stated as no longer applying to extension targets, with all citing text updated — done (§§4.3, 4.4, 8). His risk note is recorded: the 0.022 mm press margin is only ≈1.7× the 0.013 mm protocol discrepancy, and a sub-0.03 mm shortfall in the Q5 episode would use up the one shot. His Part 5 limitation (contact onset at ≈88% of E_max makes the taste feedback threshold-like) is added to §9. **Pass 6 revised is panel-complete (3 of 3 confirms, R1 conditional on the additions above).** Note: Reviewer 1 is out of free messages until 07:20 WAT.
- **One-shot clause — FINAL reconciliation:** Reviewer 1, in his confirmation, **accepted the panel-return wording** with two conditions (no further geometry adjustment; a chain move only as a fresh pre-registered amendment; default to the rescope if no majority forms). Latest positions: panel-return — Reviewers 1 and 2; automatic rescope — Reviewer 3 (dissenting). **The text carries panel-return with Reviewer 1's conditions.** The clause flipped twice during the night (R2+R3 panel-return → R1+R3 automatic → R1+R2 panel-return); the full history is in the specs' Amendment history.
- **Reviewer 3 — no objection to the reconciliation record (04:15 WAT):** panel-return is the majority position, his dissent is correctly recorded as dissent, and Reviewer 1's conditions materially address the concern behind his automatic-rescope vote. The one-shot clause is settled. Awaiting the clearance/E-definition calibration, then execution #5.
- **Clearance + E-definition calibrations COMPLETE (04:19 WAT) — Reviewer 1's additions 2 and 3 discharged.** Clearance: every non-labrum geom (83 checked) clears pedestal and disc by > 0.02 mm across e ∈ [0,1] and at rest; global minimum 0.097 mm (haustellum body vs disc at e = 1, ~5× the margin); the labrum's kinematic press into the disc at e = 1 is 0.026–0.028 mm, inside the registered 0.022–0.034 bracket. E definitions pinned in §4.4: E sums joint-angle excursions **from the settled rest pose**; both of Reviewer 1's gaps are the same 0.00415 rest offset; raw-extremes E = **2.8258** (the earlier summary's 2.8264 is an unreproducible transcription slip, superseded by the artefact value; fraction 0.7695). **Execution #5 — full gate from Q0 under Passes 1–3, 5 and 6 (revised) — now runs.**

## QUALIFICATION GATE — EXECUTION #5: **PASS** (24 Nov 2026, ~04:38 WAT)

Full re-run from Q0 under Passes 1–3, 5 and 6 (revised); record in FEEDING-BODY-QUALIFICATION.md; artefacts in repo/fresh/qualgate/results/ (rerun5). Q0 PASS (premise record confirmed). Prediction table pre-registered before Q2. Q1 PASS (replay exact; load-and-step clean). Q2 PASS (max error 0.0035 rad vs the pre-registered table). Q3 PASS, narrowed claim (E_max = 2.1746 rad = 0.7695 of raw-extremes 2.8258). Q4 PASS (determinism caution recorded). **Q5 PASS** at the starting offset 0.6 mm (adjustment unused): resting force 0.0 N; event ON at 2.0338 s; max labrum–food force 25.30 N (tarsi 0.0); adhesion persistence 1.3985 s; release on retract per rule; zero pedestal contacts of any kind. **(vi) measured onset fraction 0.8371 vs predicted 0.884 (deviation −0.047)** — no materiality bound was pre-registered; reported for the panel (the direction matches the known protocol bracket: the dynamic ramp pose sits lower than the quasi-static sweep, so contact comes earlier in E). **Q6 PASS** (first execution of the step): ladder monotone, zero-in/zero-out exact, no clipped commands, curve saved. **Band guard HOLDS: ε_res = 0.00345, θ_off = 0.01036 rad < 0.10.** Freeze outputs recorded (signs, θ_ext incl. labrum +0.2625, empirical map, arena offset 0.6 mm, Q6 curve).
**The Q5 defect, for the panel's scrutiny:** Q5's first attempt in this execution failed with zero contact because the arena's contact pairs came from the "legs_thorax_abdomen_head" preset, which contains **no proboscis segment** — the labrum was contact-invisible while geometrically penetrating the food by 0.032–0.035 mm (the registered press, reached). Shown to be a gate-script defect (penetration measured, pairs demonstrably absent), fixed in arena construction only (the six proboscis geoms paired with food and pedestal under the same ContactParams; no fly parameter touched), Q5 re-run in full → PASS; the defective artefact is preserved (`q5_rerun5_defective_construction.json`). Execution #3's arena had the same defect, but its Q5 verdict stands — its 0.246 mm geometric shortfall made contact impossible regardless of pairs. The record flags proboscis pair coverage as a Part 5 checklist item: Part 5's arena must include the proboscis pairs or the §4.5 event cannot exist. **The feeding body is QUALIFIED.** Next: the §2.4 resting acceptance test and the §6 thin FlyBody slice, then Part 5.
- **Reviewer 3 — review of execution #5 (04:41 WAT): PASS stands.** Defect-and-rerun legitimate under §7.7 (narrow harness correction; Q5-only re-run sufficient — Q0–Q4 do not depend on pair coverage). Record requirements (discharged in the gate record's classification note): the defective attempt classified INVALID, not a valid failure; both arena configurations preserved; execution #3's visibility defect disclosed. Onset −0.047: not convertible into a failure (no pre-registered tolerance); both numbers stay visible with the signed residual; Part 5 uses the measured onset; the dynamic-pose explanation to be quantified by a recorded check before reliance (running). Part 5 flags: (A) pair coverage becomes a pre-run premise check with a contact-visibility test, recorded against frozen hashes; (B) the 25.30 N is a contact diagnostic only until its meaning (peak/aggregate/units/solver sensitivity) is established — claims say "body reports contact", not a biological force; (C) r_hi = 155 stays provisional; (D) Q4 determinism operationalised for Part 5 (what was deterministic, variation sources, frozen seeds/tolerances).
- **Reviewer 1 — review of execution #5 (04:41 WAT; composed in full, posting to his chat deferred by his message limit until 07:20): NO OBJECTION.** Defect-and-rerun legitimate: the attempt was void, not a body failure; carrying Q0–Q4 and Q6 is sound (the added pairs are inert outside Q5); the boundary is explicit — had the fix changed a registered quantity, a formal amendment and full re-run would have been required. Onset −0.047 **not material**, and quantified: ≈0.04 f_c per 0.01 mm in the sensitivity table, so −0.047 ↔ ≈0.012 mm, exactly the recorded protocol difference; it is in the safe direction; Part 5 uses the measured ≈0.84 as operative. Carry-overs concur with Reviewer 3's flags; the one-shot condition is spent (Q5 passed). Reviewer 2's review is pending.
- **Reviewer 2 — review of execution #5 (04:41 WAT): PASS STANDS.** Defect-and-rerun legitimate (unmeasurable criterion, not a body failure; fix confined to arena construction; #3's verdict stands on independent geometric grounds). Onset −0.047 **not material**: inside the ≈0.05 f_c variation implied by the 0.012 mm R bracket and explained by it; Part 5 uses the measured 0.8371 (± ~0.05) for contact timing. Flags concur with Reviewers 1 and 3, plus: the Q6 ladder's rate→extension shape is nonlinear — Part 5 must not assume linearity; and Part 5 should pre-register uncertainty/materiality bands for predictions before runs execute. **Panel review of the qualification gate is complete: 3 of 3, the PASS stands, no illegitimacy found.** The gate's freeze outputs are Part 5 inputs. Remaining pre-Part-5 deliverables: §2.4 resting acceptance test and §6 thin slice (both running), plus the dynamic-onset quantification check (Reviewer 3's condition).
- **Dynamic-onset quantification check — COMPLETE (04:50 WAT), Reviewer 3's condition discharged on measurement.** The exact Q5 rebuild replicated the onset step-for-step (first force at step 6024, E/E_max = 0.8371). Dynamic labrum surface at that fraction: 0.3309 mm (the disc top); quasi-static at the same fraction: 0.3409 mm; difference −0.0101 mm, inside the pre-stated band. Mechanism corrected by a five-case diagnostic: not ramp speed, not the chain (paired cases agree <0.0002 mm) — the graded sweep's trajectory lifts the body (thorax +0.0071 mm, labrum +0.0134 mm at e = 1) as it re-settles through intermediate extensions, and the reach curve's f_c = 0.884 inherits that lift. The [0.296, 0.308] reach bracket is a protocol split, not an uncertainty. Part 5 predicts onset from the direct-protocol curve (measured 0.837).
- **Thin FlyBody slice (§6) — PASS (04:50 WAT)**, record fresh/THIN-SLICE.md. Chain module built as the Part 5 code path (9/9 tests; bit-equal commands to the gate's chain); synthetic 0→100→0 profile (r_hi = 100 declared slice parameter); contact ON at chunk 15, taste event in the stub log exactly +1 chunk at all 60 chunks; onset chunk 5, offset chunk 53 by §4.4; slice contact onset E/E_max = 0.858. Attempt 1 failed criterion (ii) on the slice script's own profile shape (offset arithmetically unreachable); fixed at slice level, both attempts recorded.
- **§2.4 resting acceptance test — PASS (05:08 WAT)**, record fresh/ACCEPTANCE-TEST.md. Both configurations: 10/10 episodes valid, zero invalid, **zero false ignitions**. Feeding: no qualifying food contact at any physics step in 300 resting chunks (max run 0 steps vs the ≥10-step threshold). Walk/halt: exactly 0 transitions in all 300 resting chunks (vs ≥8 on-threshold); the spawn drop (290 transitions) was absorbed in warmup chunk 0 per §2.3 and never converted. Recorded caveat (as with Q4): the bodies are deterministic, so each configuration's 10 episodes are byte-identical repetitions of one resting trajectory — the pre-registered test is satisfied on those terms; no cross-spawn variability claim may be read into it. **All pre-Part-5 deliverables are complete: qualification gate PASS + panel review, thin slice PASS, acceptance test PASS, onset check recorded.**

## PART 5 PREREGISTRATION — panel review (24 Nov 2026)
- **Reviewer 1 — REQUIRE CHANGES (05:17 WAT; from the summary — he cannot read the draft until his messages reset at 07:20; items he marked "confirm" are to be checked against the text).** Six required items: (1) E-Total/E-Baseline — register the D1–D4/C1–C3 constructions in the text now, or explicitly exclude the two estimands from the freeze with any follow-on amendment frozen before Part 5/Part 7 data are examined. (2) The four-conditions ladder rung becomes a **Part 7 prerequisite** (run and registered before Part 7 begins; state whether any Part 5 conclusion depends on it). (3) PROPOSED choices fixed before the freeze: an explicit chunk map (ignition 0–19, calibration window 20–59, tail 60–99, per-arm phase behaviour) and the exact percentile computation stated as fixed, not proposed. (4) Reconcile the two r_hi numbers with derivation and units — **note: his summary reading inverted the rejection direction** (the draft's bound is r_hi ≤ 15 Hz, a degenerate-LOW rejection; ≲184 Hz is the opposite tail, threshold clearance); the revision must state both tails, the steady-drive assumption (≈155 Hz, Part 3) and the consequence of a rejected calibration for the freeze. (5) Each materiality band justified from measurement/protocol uncertainty, not observed deviations (the onset band by the ≈0.012 mm protocol bracket). (6) The refit rejection rule's direction and consequence stated unambiguously. Conditions to confirm (present in the text, to be verified with him verbatim after 07:20): premise-check failure consequences; waiver recording; toggle probe specification; counts/seeds hashed; neuropil accepted as unmatched with restricted wording; compute accepted. Endorsed and to keep: threshold prediction as finding-not-retune; hashing before evaluation; L-MN9 degenerate case decided in advance; −0.047 kept visible; expert-check honesty.
- **Reviewer 3 — REQUIRE CHANGES (05:17 WAT), core scope decisions APPROVED.** Approves: the E-Total/E-Baseline deferral (with binding pre-construction amendments + §10 claim prohibitions — R3-4); separation of the ladder rung (NOT a Part 7 prerequisite — disagrees with Reviewer 1) with a strict claim boundary (Part 7 in-loop results may not support brain-only ladder claims); episode shape; the pooled percentile definition (to be frozen with its implementation); the threshold prediction + graded fallback (with pathway-output vs functional-contact endpoints kept distinct in wording); calibration rejection; frozen/refit incl. the degenerate ruling; arms/endpoints/statistics; P1–P6; the toggle probe; compute (with run-preservation conditions). Required: **R3-1** M1's ±0.05 onset band needs an independent prospective rationale or demotion to descriptive — as centred it places the known −0.047 "just inside", an appearance of post-hoc accommodation (both values and the signed residual stay visible either way). **R3-2** Expert check resolved before freeze approval: completed, or the waiver formally invoked (rationale/owner/limitations) with correct labelling — the freeze may be approved without being called expert-checked, but not with the check unresolved and no waiver invoked. **R3-3** Matching/refit isolation verified in the text (outcome-blind metric/scaling/pool/tie-breaking; refit designation + hash before evaluation) — may already be satisfied; check and record. **R3-4** §10/§11 claim boundary completed (no E-Total/E-Baseline claims, no null/rule-baseline superiority, no ladder claims from arm (d) or Part 7). Reviewer 2's review is pending; the R1–R3 split on gap (2) (rung as Part 7 prerequisite) turns on it.
- **Reviewer 2 — REQUIRE CHANGES, items A–D (05:22 WAT), the rest APPROVED AS WRITTEN** (he ruled on verbatim text in two batches and checked the arithmetic). **Item A: the ladder rung is a Part 7 prerequisite** — with Reviewer 1, a **majority (2–1) over Reviewer 3's dissent**: no Part 7 episode until the four-conditions rung is preregistered, run and recorded. Item B: §6 endpoint-3 "Never pooled" wording made consistent with endpoint 4's pooled suppression ratio (one sentence). Item C: the GPU trigger's application to the Part 7 projection stated explicitly (per run set vs per family), K4/§13 governing. Item D: a per-episode resumability provision in §14, or explicit acceptance of void-and-restart cost. Approved as written: gap (1) deferral with conditions (amendments panel-approved before those arms run and justified on their own terms, not by reference to known intact results); episode shape; calibration design; the percentile sampling unit; the refit degenerate ruling; **M1–M7 including M1's ±0.05**; P1–P6; arms/endpoints/statistics; gating/threshold arithmetic; the §9 probe design; matching; gap (3). Expert check: a condition, not a blocker — **the freeze tag must not be created until §14 records the check or Angelic's signed waiver**. Panel position after round 1: document approved in substance by all three subject to one consolidated revision (R1's 6, R3's 4, R2's 4, plus the §9 rewrite the build's impossibility finding requires).
- **Part 5 build — COMPLETE (05:21 WAT)**, record fresh/PART5-BUILD.md, 37/37 tests. Smoke S1: the loop self-sustained — scripted ignition chunks 0–9, then the taste event alone gated the drive for chunks 10–39; contact onset at E/E_max = 0.851; peak E 2.058 rad. S2 (no-drive): perfectly silent. **§9 premise finding:** a single-run internally-toggled reference does not exist in this stack (Brian2 fixes the active set at run start — the attempt yielded zero spikes; PoissonInput.rate is read-only); the probe was discharged by constant-drive chunked-vs-single bit-identity (SHA-256 7675ebe1…, 34,013 spikes) + between-run toggle exactness (0ead53e3…; driven counts exactly 0 in OFF chunks), reproduced across two executions. **Measured wall clock ≈54 s per 40-chunk episode** — the §2 compute projection (≈500 s/episode) is ~9× pessimistic and is updated in the revision.
- **Amendment Pass 1 APPLIED to PART5-PREREG.md (05:26 WAT; 13,469 words)** — all R1 items, R2 items A–D, R3-1..R3-4 + (e), and the §9 rewrite: rung recorded as Part 7 prerequisite (§1/§8, majority ruling, R3 dissent recorded) with "no Part 5 conclusion depends on the rung" stated; E-Total/E-Baseline declared not registered outcomes with the merged amendment conditions + §11 prohibitions (statements 7–8, incl. graded-vs-contact wording); chunk-map table (§2); two-tails r_hi derivation (§4/§8.2); §6 endpoint-3 exception sentence; compute updated to measured (≈136 s/episode; Part 7 ≈24 h; trigger read per family and in total, both satisfied); resumability provision (§14); §9 replaced by the executed probe with narrowed claim language + the seed-5103 collision resolved (characterisation list = 5100–5119 excluding 5103, plus 5120); M1 rationale rewritten as prospective protocol uncertainty; expert-check/freeze-execution distinction (§12); PROPOSED marks resolved on the panel's rulings; §8.1 tie-breaks made deterministic. One cross-reference typo (§3's "§9" → "§10" for the onset explanation) corrected. Re-checks sent to all three reviewers.
- **Four-conditions ladder rung preregistration DRAFTED** (fresh/PART3-RUNG2-PREREG.md, ~4,850 words): four conditions × 30 trials, seeds 6100–6219, anchor check against the sugarR rung with a stop rule, suppression ratio as headline with CI/TOST ±0.15, Holm family of six, tag part3-rung2-v1 proposed. One gap registered in its §12: whether the frozen Part 3 runner accepts two simultaneous stimulus entries (sugar+bitter) is unverified — a pre-freeze verification item; silently patching the frozen runner is excluded. Sent to the panel for review.
- **Two-drive verification — PASSED (05:29 WAT)**: the frozen Part 3 runner accepts two simultaneous stimulus entries unchanged (run_experiment iterates the stimuli list; add_drive accumulates). Non-rung smoke (seed 9998, 200 ms): sugar 823 spikes, bitter 844 (≈840 expected each). The rung preregistration's §12 item 5 is settled affirmatively and the verification is recorded in the document.
- **Reviewer 3 — CONFIRM on Part 5 Pass 1 (05:30 WAT, on verbatim text)**: R3-1..R3-4 satisfied; no remaining substantive objection to the document's approval, subject to its execution conditions. **Reviewer 3 — APPROVE the rung preregistration**, conditional on the multi-entry verification — which has passed (above).
- **Reviewer 1 — conditional CONFIRM on Part 5 Pass 1 (record composed 05:29 WAT for posting at 07:20)**: all six items discharged on the summary; he records owning his inverted reading of the rejection direction. Confirmation is conditional on verbatim passages at 07:20 matching the summary; remaining verification items: (a) M2/M3 rationales verbatim; (b) rung verbatim + two-drive closure (now closed — to be supplied); (c) the basis for the 15 Hz threshold (§4.3's r_lo + 10 Hz rule, inherited from Part 4 §4.3); (d) full probe hashes (7675ebe18c3775ad48542b62f7557a0331ad3023d2291da2f1284469fa0fe5d1; 0ead53e3d83b163a610de1701f5a390503822d271db5ff9526355437e9778387). He conditionally confirms the rung on the same terms.
- **Reviewer 2 — CONFIRM on Part 5 Pass 1 (05:37 WAT, on verbatim text)**: items A–D discharged; M2/M3 flag resolved (Q6's departure is a pre-freeze gate calibration measurement, not an outcome under this freeze — the ±0.10 rad grounding is legitimate); one one-line §14 item 8 clarification requested and applied as a Pass 1 clarification (the crashed episode is itself re-attempted under a new run_id with the same seed; "next" = the next not-yet-completed episode) — non-blocking. **Reviewer 2 — APPROVE the rung preregistration, no remaining items** (the §12 item 5 gap closed by the verification).
- **PANEL OUTCOME (24 Nov 2026, 05:37 WAT, under the overnight delegation): the Part 5 preregistration document is APPROVED** (R2 CONFIRM, R3 CONFIRM, R1 conditional CONFIRM pending 07:20 verbatim verification) **and the four-conditions rung preregistration is APPROVED** (R2 APPROVE, R3 APPROVE with its condition satisfied, R1 conditional on the same verification). Both freezes remain UNEXECUTED by their own rules: Part 5's awaits the expert check or Angelic's signed waiver (§14 item 6) plus her ratification; the rung's §12 item 1 requires her explicit approval. Everything is logged as delegated for her ratification on waking.
- **Reviewer 1 — verbatim verification round COMPLETE (07:51 WAT, Messages 43–46)**: no supplied passage differed from the summary, so no confirmation lapsed. Part 5 Pass 1 CONFIRM on items (a) M2/M3, (c) 15 Hz basis, (d) full probe hashes as quoted. Rung APPROVE, conditional on three additions before the tag: (1) laterality of the bitter/water sets written into §§3–4; (2) per-condition criteria/scope stated (bitter-alone and water-alone descriptive; no condition compared against a reference output — model behaviour, not reproduction; "the ratio" defined as pooled sugar+bitter over pooled sugar, with the per-side requirement stated); (3) anchor strength — a non-gating discrepancy report if the anchor Δ CI excludes 0 by more than ~5 Hz. Plus two Part 5 items to close from quotes: the §9 (ii) heading must say run-to-run reproducibility of the chunked toggle train, and the full §4 derivation paragraph for the 15 Hz bound to be confirmed against the quoted bound/consequence. R1 resolved the TOST point himself (ratio TOST is on the linear scale). The three rung additions + the §9 heading tweak are being applied as an Amendment Pass 1 (rung) / clarification addendum (Part 5), then returned to R1 verbatim for his final confirm. Standing blocks unchanged: expert check OUTSTANDING; the rung remains a Part 7 prerequisite.
- **Rung Amendment Pass 1 + Part 5 §9/§4 addendum APPLIED (07:53 WAT)**: laterality written into the rung's §§3–4 (bitter/water are the upstream un-split lists, no laterality recorded; sugar+bitter pairs the right sugar set with bitter); new §7.1 (bitter-alone/water-alone descriptive only; no condition compared against a reference output — model behaviour, not reproduction; "the ratio" defined as pooled sugar+bitter over pooled sugar, no per-side condition required for the headline); the §8.1 non-gating discrepancy rule (Δ CI excluding 0 by >5 Hz goes to the panel, no STOP) + §11 reporting; Part 5 §9 (ii) heading now states run-to-run reproducibility of the chunked toggle train. All four returned to Reviewer 1 verbatim with the full §4 derivation paragraph for his final confirm.
- **Reviewer 1 — FINAL verbatim round COMPLETE (07:56 WAT, Messages 47–48)**: rung approval is now UNCONDITIONAL on its three conditions; Part 5 Pass 1 STANDS on the §9 heading and §4 paragraph as quoted. §4 arithmetic confirmed by him: (154.97 − 5)/(184 − 5) = 0.838; 154.97 Hz = the Part 3 pooled steady rate (92.57 + 62.40). Three non-blocking items folded in as pre-freeze text fixes: (1) rung "mixed" headline wording (pooled suppression/enhancement with a contrary per-side result); (2) rung ratio resampling corrected to independent resampling within each condition (trial-index pairing is bookkeeping only — §7 did not average per-trial ratios, but its paired-bootstrap wording is replaced); (3) Part 5 §4 cites 0.837's provenance (measured direct-protocol onset, execution #5 Q5(vi) 0.8371) — with 0.884 the clearance threshold would be ≈175 Hz, not 184 Hz; either way the decoder is retained. **Panel review of both documents is now COMPLETE — all three reviewers, both documents, no remaining items.** Standing blocks unchanged: expert check OUTSTANDING; both freezes await Angelic (Part 5: expert check or signed waiver + ratification; rung: her explicit approval).
- **Rung Amendment Pass 2 + Part 5 §4 provenance note APPLIED (07:57 WAT)**: ratio resampling is now independent within each condition (trial-index pairing is bookkeeping only — §7 never averaged per-trial ratios; the paired-bootstrap wording is replaced); the pre-written "mixed" headline rule is in §8.3; §4 cites 0.837's provenance (measured direct-protocol onset, execution #5 Q5(vi) 0.8371, vs the 0.884 prediction). One honest edit note: the editor's first attempt hit a history entry instead of §7.1 — caught on verification, reverted, applied correctly; "paired by trial index" remains once, inside the Pass 1 history entry quoting what Pass 1 wrote, which is the correct record. **Both documents are now final as panel-approved. No panel item remains open on either.**

## OWNER'S TWO QUESTIONS — panel round (24 Nov 2026, 11:05–11:08 WAT)

Round put to all three reviewers at the owner's direction ("Ask the AI panel instead so we can go ahead"), after external sourcing of the D6 human expert check proved non-viable this morning. Two items: (1) whether the panel's review can stand as the check for the Part 5 freeze; (2) the owner's question — "If we are still not sure can we do more than one test to see? Or we need to lock in one?"

### Item 1 — the panel standing as the check for the Part 5 freeze (D6)

- **Reviewer 2 — ACCEPT WITH CONDITIONS (5).** (1) Dual recording: a panel verification record PLUS the owner's signed/dated authorisation substituting the panel check under PART0-PACKAGE §6.3, noting why external sourcing was non-viable. (2) The freeze record states what the panel check IS: internal consistency, preregistration completeness, statistical/seed integrity, arithmetic and code-to-spec correspondence, gate-rule adherence. (3) What it IS NOT — a ban on "expert-checked" / "reviewed by a Drosophila neurobiologist" labelling; the label is "AI-panel checked under owner-authorized substitution waiver (no external human domain check prior to freeze)". (4) Residual risk stated: unwritten SEZ/gustatory-motor field conventions an AI panel cannot catch. (5) The human check remains owed at Part 8.
- **Reviewer 3 — ACCEPT WITH CONDITIONS** (answered via the continuation chat "Review ConnectomeToBehaviour Plan (2)", https://chatgpt.com/c/6b0561a5-0950-83ea-a5e2-07e8de38c5aa, after the original chat hit its context limit). The panel review cannot satisfy the human-check route; it must be accompanied by the owner's explicit signed waiver under the D6 waiver route — signed/dated, identifying the exact preregistration version and intended freeze, not inferred from a general instruction. The freeze record must state: the review performed; its nature (AI-assisted methodological/internal-consistency review); what it is not (not human expert review, not biological validation, not external peer review); the D6 route taken; the residual risk; human review outstanding for Part 8. Boundary: these decisions do not themselves create a freeze tag or authorise any episodes.
- **Reviewer 1 — REJECT the panel AS the check; ACCEPT proceeding on the owner's signed waiver.** Reason: D6 guards against shared-blind-spot agreement, and the project's own history shows the risk — the YAML spring-rest premise passed review rounds and was caught by execution at the qualification gate, not by review; likewise the Pass 4 penetration estimate. Waiver conditions: (1) freeze-record wording "Human domain-expert check: NOT obtained. Waived by Angelic Charles on [date]"; the panel is never described as the expert check. (2) The panel review is described as a multi-round adversarial review of design/statistics/internal consistency — a substitute control, not an independent review (the reviewers are language models with shared blind spots; material was relayed by the bringer; several rounds were reviews of summaries, not full files; no lab experience of Drosophila feeding or connectome annotation). (3) Residual risks listed: biological assumptions incl. the MN9 readout, the GRN sets, aDN roles/laterality; literature/data misattribution; errors only execution reveals. (4) Scope: the waiver covers the Part 5 freeze and the rung freeze only, not blanket. (5) The human check remains owed at Part 8 — Reviewer 1 recommends seeking it before Part 7's first confirmatory evaluation episodes; a second waiver at Part 8 is permitted, but any paper/application must then state "no human domain-expert review of the pre-registration". (6) No "expert-reviewed" language in any README/preprint/application. Sourcing note: the eventual human check need not be a connectomics PI — a human computational neuroscientist or statistician reviewing design/endpoints/equivalence logic (ABDN/Neuromatch/WiNN networks) meets the bar; posting the preregistration publicly with a timestamp also invites review.
- **CONSOLIDATED OUTCOME — Item 1: unanimous in substance.** The freeze may proceed on the owner's signed waiver, with the panel review recorded as what it is; the panel is never labelled the expert check; the human check remains owed at Part 8. Awaiting the owner's signature on the waiver.

### Item 2 — more than one test, or lock in one?

- **UNANIMOUS RULE.** One locked primary governs all confirmatory claims. Additional alternatives may run only as pre-registered, non-confirmatory sensitivity arms — Reviewer 1's terms: every choice classified LOCKED or ARMED before the freeze; anything unclassified is a specification gap. Arms are declared before any outcome is seen, use disjoint/pre-allocated seeds, sit outside the confirmatory/Holm/TOST families, are reported separately with their labels, and can never rescue, replace or redefine a failed or inconclusive primary. No arm may be added after a primary result is seen (later additions are exploratory, or by formal amendment before execution).
- **Bitter/water 200 Hz convention: ARMED (all three).** The primary stays 200 Hz, its rationale stated honestly as "matched to sugar, not independently justified". Reviewer 1's concrete proposal: arms for bitter alone and for sugar+bitter (bitter varied, sugar fixed) at 100 Hz and 150 Hz in the rung, read as a dose-response (the suppression ratio depends on bitter drive by mechanism), the claim scoped to the registered rates; ≈3–4 extra CPU-hours; water arms skipped unless the cost is trivial.
- **Right-only vs bilateral sugar: ARMED, right-only primary (all three).** Reviewer 3's stricter framing recorded: bilateral recruits a different population, so it is registered as a separate secondary stimulus condition, not a mere parameter setting; labelled OUTSIDE THE VALIDATED ENVELOPE; never pooled with, substituted for, or used to rescue the right-only anchor.
- **Encoder conventions generally: LOCKED (all three).** Endpoints, metrics, equivalence margins, decision rules, calibration/evaluation separation, seeds, decoder structure and the r_hi rule, brain/body identity stay single-locked. Individual uncertain constants are handled through the preregistration's existing sensitivity obligations (Part 5 §10) with stated perturbation ranges on a reduced design, not by new arms.
- **Timing note (Reviewer 1).** Part 5 is approved but not frozen, so adding these arms now is a cheap pre-freeze amendment; after the freeze it becomes a formal change.

**STATUS: panel round COMPLETE, 3 of 3. All three owner items now CLOSED (24 Nov 2026).** (a) sign the waiver — **DONE, 24 Nov 2026** (see note below); (b) approve folding the Item 2 arms into both preregistrations as a pre-freeze amendment — **DONE, 24 Nov 2026 (~11:34 WAT)**; (c) ratify the overnight delegated closes and approve the rung freeze (asked 08:25 WAT) — **DONE, 24 Nov 2026 (~11:34 WAT)**: the delegated closes (Part 2b gate + record completion, Part 4 gate, qualification PASS, thin slice, acceptance test, Part 5 build) are ratified, and the rung freeze is approved (rung §12 item 1 satisfied). Recorded in ANGELIC-DECISIONS.md. Both freezes are cleared to execute under their checklists, with the arms amendment applied to both documents before any tag is cut.

**Waiver signed by Angelic Charles, 24 Nov 2026 (~11:15 WAT).** Her instruction, verbatim: "Yes to the waiver but don't add the ai panel thing just say I couldn't reach a professional in this field so I did what I could according to my personal research." The waiver is recorded in her own wording; it does not present the panel as the check or as the basis for proceeding. Waiver text:

> Human domain-expert check: NOT obtained. I could not reach a professional working in this field, so I proceeded on the basis of my own research and the checks I could carry out myself. Waived by Angelic Charles, 24 Nov 2026. Scope: the Part 5 freeze and the four-conditions rung freeze only. The human expert check remains owed at the Part 8 final gate.

With the waiver signed, the §12 / §6.3 condition for both freezes is satisfied. Items (b) and (c) were both approved by Angelic on 24 Nov 2026 (~11:34 WAT) — see the status line above and ANGELIC-DECISIONS.md — so no owner item remains open for either freeze.

## CONFIRMATION ROUND — sensitivity-arms amendment (24 Nov 2026)

The arms amendment (Part 5 arm (e); the rung's bitter dose-response arms + condition (v)) went to all three reviewers for confirmation before any freeze tag is cut.

- **Reviewer 3 — CONFIRM.** His REQUIRE CHANGES was over the bringer's summary shorthand for the fourth rung arm; the document itself was verified correct — §4's arms table, seed allocation, run order and amendment history all name the arms in full — and his confirm stands on the document.
- **Reviewer 1 — CONFIRM, with before-the-tag record checks.** He states he judged the described amendment, not the files; the checks are therefore discharged against the files themselves and recorded here: (1) **arm (e)'s seed block disjoint from every other registered block** — discharged in the text: Part 5 §7 now states the disjointness of 5800–5819 explicitly against calibration, characterisation, both Part 7 evaluation blocks, refit calibration, the P6 determinism seed (5699) and the control-selection seed (5700) (the block itself was moved under Reviewer 2's item below). (2) **Waiver annotations read SATISFIED BY WAIVER where the waiver is the basis** — discharged: Part 5 §14 item 6 now reads "SATISFIED BY WAIVER" verbatim (it previously read "SATISFIED BY THE WAIVER ROUTE"), and the rung's §12 item 1 annotation now records the D6 expert-check condition for that freeze as SATISFIED BY WAIVER, with the Part 5 §12 cross-reference — the rung previously carried no waiver annotation at all. The approval annotations themselves (Part 5 §14 item 1; the rung §12 item 1's approval clause) remain "SATISFIED" on their stated basis — panel review complete plus the owner's recorded approval — because the waiver is not what satisfies them; relabelling them would misstate the record. If Reviewer 1 meant the approval annotations themselves, that is a question for his re-confirmation round, not a silent edit. (3) **Rung runtime basis stated as measured vs projected** — discharged: rung §4 now states the per-condition figure (≈35 min per 30-trial condition) is MEASURED from the Part 3 primary run (2,094.6 s for 30 trials), and the ≈5.2 h total for the nine conditions is a projection built on that measured rate. (4) **Each alternative rate justified in writing** — discharged: rung §8.5 states 150 Hz is the upstream model's own default drive rate (the released code's default; the other candidate generating rate adjudicated in Part 3) and therefore the most decision-relevant alternative, and 100 Hz is a design choice — the evenly spaced lower rung of the ladder {100, 150, 200} Hz — with no literature source claimed for it; §4 cross-references the justification. (5) **Arm (e)'s pre-run expectation stated** — discharged: Part 5 §5, design choice (iv) now states, before any arm (e) episode runs, that bilateral drive will likely push the pooled MN9 rate above the right-only r_hi, so e will probably saturate, and arm (e) reads as whether the loop runs under bilateral drive and where e saturates — not as a graded decoding test. (6) **Bilateral labelled "(v) secondary" wherever the rung lists it alongside conditions (i)–(iv)** — discharged: the label completed in §§2 and 4 (design paragraph, arms table, seed allocation, run order); §8.4's completion definition remains the four conditions, restated at §8.5.
- **Reviewer 2 — REQUIRE CHANGES (one change) + a wording note.** The change: he read arm (e)'s seed block 5600–5619 as colliding with the §9 probe's allocation of 5600–5601. That allocation was draft-era and was removed in Pass 1 (the executed probe consumed 5103), so no live collision existed — but rather than argue the reading, **the fix was adopted in full: arm (e) is moved to the clean block 5800–5819** (Part 5 §§5, 7 and the amendment-history entry, which records the move and its reason; the rung's §4 cross-reference updated to match). The only remaining "5600" occurrences in either document are historical/explanatory: the Pass 1 removal note and the move note. His wording note — §8.5's prose must write the fourth arm out in full, no shorthand — is discharged: §8.5 now names all four arms in full, the fourth as "sugar+bitter @ 150 Hz" (sugar fixed at 200 Hz; seeds 6320–6349). **Re-confirmation is to be sought from Reviewer 2 on the seed fix**; his stated position: "Once that seed conflict is resolved, CONFIRM stands from my side."
- **OUTCOME: the amendment is CONFIRMED by Reviewer 1 and Reviewer 3; Reviewer 2's confirm is pending only the seed fix, which is now applied — his re-confirmation is the last panel item before the freeze tags.** No tag has been created; no calibration or evaluation episode has run.

**Confirmation round CLOSED — 3 of 3, no open items (24 Nov 2026).**

- **Reviewer 2 — CONFIRM (24 Nov 2026).** On the applied seed fix (arm (e) moved to 5800–5819, §8.5's fourth arm written in full): his required change and wording note are discharged in full; CONFIRM stands from his side, no remaining items.
- **Reviewer 1 — CONFIRM of the amendment, and express acceptance of the §14 item-1 treatment (24 Nov 2026).** His words on the labelling deviation: "Your deviation is correct... Leaving it on its stated basis and annotating the D6 item is the right treatment." His one mechanical requirement — that seed disjointness be verified by a script, not by eye — is discharged below.
- **Seed disjointness, verified by script (24 Nov 2026, before any freeze tag).** Script: `work/seed_disjointness_check.py` (parses the Part 5 §7 allocation table and this rung's §4 allocation paragraph out of the documents themselves, cross-checks them against the canonical list, adds the historical blocks of the closed parts, and asserts pairwise disjointness over sets — the characterisation list is treated as the set it is registered as, 5100–5119 excluding the consumed probe seed 5103 plus 5120; the matched-control sub-seed stream 5701, 5702, … is modelled as 5701–5799, bounded by the next allocated block, the only reading under which the table is consistent). Output, verbatim:

```
SEED DISJOINTNESS CHECK -- 24 Nov 2026
blocks checked: 28
  hist:part2-seed-0                            n=   1  span 0
  hist:part2b-episodes-4200-4203               n=   4  span 4200-4203
  hist:part2b-probes-4102-4105                 n=   4  span 4102-4105
  hist:part3-arm-3030-3059                     n=  30  span 3030-3059
  hist:part3-determinism-9999                  n=   1  span 9999
  hist:part3-extension-3060-3089               n=  30  span 3060-3089
  hist:part3-primary-3000-3029                 n=  30  span 3000-3029
  hist:rung2-verify-throwaway-9998             n=   1  span 9998
  part5:5000-5009                              n=  10  span 5000-5009
  part5:5100-5119 excl 5103 plus 5120          n=  20  span 5100-5120
  part5:5103                                   n=   1  span 5103
  part5:5200-5219                              n=  20  span 5200-5219
  part5:5300-5319                              n=  20  span 5300-5319
  part5:5400-5519                              n=  120  span 5400-5519
  part5:5699                                   n=   1  span 5699
  part5:5700                                   n=   1  span 5700
  part5:5800-5819                              n=  20  span 5800-5819
  part5:subseeds-5701-5799-modelled            n=  99  span 5701-5799
  rung:6100-6129                               n=  30  span 6100-6129
  rung:6130-6159                               n=  30  span 6130-6159
  rung:6160-6189                               n=  30  span 6160-6189
  rung:6190-6219                               n=  30  span 6190-6219
  rung:6220                                    n=   1  span 6220
  rung:6230-6259                               n=  30  span 6230-6259
  rung:6260-6289                               n=  30  span 6260-6289
  rung:6290-6319                               n=  30  span 6290-6319
  rung:6320-6349                               n=  30  span 6320-6349
  rung:6350-6379                               n=  30  span 6350-6379
total seeds across blocks: 684; distinct seeds in union: 684
RESULT: PASS -- all blocks pairwise disjoint
```

**The sensitivity-arms amendment is CONFIRMED 3 of 3 with no open items.** Both freeze checklists may now execute; the rung freeze follows (§12 of its preregistration).

## PUBLICATION NOTE — v0 bundle + GitHub push moved forward by the owner (24 Nov 2026, ~13:04 WAT)

At Angelic's direct instruction, the Part 6/8 publication sequencing was superseded for timing only: the old build is bundled into `v0-prototype/` and the repository (fresh build included) is pushed to GitHub now. Restructure commit `25c649f`; tags pushed: `v0-prototype-final` (on the last old-build commit `ab30ab4`), `part3-prereg-v2`, `part3-rung2-v1`. The Part 6 comparison is unchanged and still happens at Part 6; the new root README claims no rung or Part 5 results. Full record: `ANGELIC-DECISIONS.md`, section "Publication moved forward" (24 Nov 2026). The rung freeze and its in-progress runs were not disturbed.

## RUNG 2 FREEZE AND EXECUTION — freeze DONE, anchor PASS, execution STOPPED at the sugar+bitter condition (24 Nov 2026)

- **Freeze executed (§12, in order).** Preparatory commit `865125121fd5a66bfbdd58e117ffdef915df4a5a` (pending Part 3 §13 note, track-log catch-up, Part 2b/Part 5/qualification-gate working state — committed so the freeze tree is clean). **Freeze commit `b62a0fe70671a1f789e97ba7992120d060aae27a`** (24 Nov 2026, 11:51:25 WAT), containing `fresh/PART3-RUNG2-PREREG.md` only, byte-identical to the approved document; **annotated tag `part3-rung2-v1`** on it; nothing pushed at freeze time. **Identity verified:** `git diff 0cb9b81..b62a0fe` over `fresh/ctb/`, `fresh/tests/`, `fresh/part2/` is empty; Part 1 data hashes re-verified against PART3-FREEZE.md (completeness `e6b71e17…`, connectivity `94db8c65…`, sugarR `83921d50…` — all match). Freeze record: `fresh/PART3-RUNG2-FREEZE.md`. Harness: analysis script `work/analyze_rung2.py` SHA-256 `2cfea92b…`, driver `work/run_rung2.py` SHA-256 `91ea95d2…`; the analysis script passed its synthetic verification (known rates, ratio exactly 1, suppressed case, mixed-headline case, Holm example) before touching real output (§12 item 4).
- **Determinism check — PASS (§12 item 7).** Two independent 1-trial sugar runs at seed 6220: spike tables bit-identical, SHA-256 `f8a537c906bfc05d0b1892bfcdad1befe5c8b6e95a3a950322f589b928a841d9` (17,389 spikes each); both manifests at the freeze commit, clean tree.
- **Sugar condition — RUN.** `part3-rung2-sugar`: 506,683 spikes, 443 active neurons (431 at 0.1 Hz, 391 at 1 Hz), runner wall 200.4 s; manifest at the freeze commit, clean tree. (Wall clocks came in far under the §4 projection — the shared VM's load, not the code, is the variable; the projection stands as written.)
- **ANCHOR — PASS (§8.1).** Against the Part 3 primary run's realised means (recomputed from its spike file: L 92.567, R 62.40 Hz — matching the recorded 92.57 / 62.40): rung sugar MN9 L **93.63 Hz**, Δ = **+1.07**, 95% CI [−1.23, +3.40], inside the ±23.14 band; R **61.47 Hz**, Δ = **−0.93**, CI [−3.53, +1.53], inside the ±15.60 band; L > R preserved. **The non-gating discrepancy rule does not trigger** (neither CI excludes 0 by more than 5 Hz). The frozen implementation reproduces its own Part 3 output under this freeze; the rung proceeded.
- **Bitter condition — RUN.** `part3-rung2-bitter`: 192,720 spikes, 94 active neurons (91 / 85 at the higher thresholds), runner wall 193.9 s; manifest at the freeze commit, clean tree. Descriptive (§7.1, no confirmatory claim): **MN9 is exactly 0.00 Hz on both sides under bitter alone** — bitter drive by itself does not recruit the feeding readout.
- **Sugar+bitter attempt — VOID (killed), logged per §4 run integrity.** The first attempt (run_id `part3-rung2-sugarbitter`, seeds 6160–6189) was killed by the shared machine mid-run: observed alive 34 min in at ~27% of one core (severe CPU throttling) with ~3.4 GB RSS while other tenants held most of the VM's memory; found `Killed` (SIGKILL) at the next inspection; the run directory is **empty** — no output was written, no partial trial set exists, and the attempt is void, exactly the §4 case. **Diagnostic (labelled, not a rung run):** six trials of the same configuration through the frozen runner completed cleanly — 105,014 spikes, 411 active neurons, ≈17.5k spikes/trial, the same weight as sugar — so the condition is not intrinsically heavy; the kill is attributed to the shared cell's throttling plus memory contention, not to the model or the harness. The re-run requires a new run_id (§4) with the same seeds.
- **EXECUTION STOPPED — a premise failure, not a result (§5).** Before the re-run could start, the owner's publication decision (recorded in track.md, 24 Nov 2026, ~13:05 WAT) added two commits on top of the freeze commit (`25c649f` v0-prototype bundle/release, `5ad2baa` front-page header; 13:07–13:09 WAT) and pushed. **HEAD is now `5ad2baacec7f3c2901d86d8de22ddbf0c31e29e3`, not the freeze commit** — so any run executed in the main tree would record a manifest commit ≠ `b62a0fe…` and would **not count under §5**. The remaining seven condition runs (sugar+bitter re-run, water, bitter100, bitter150, sugarbitter100, sugarbitter150, bilateral) were therefore **not started**. Verified at the stop: the frozen paths at the new HEAD are still byte-identical to `0cb9b81` (diff empty), tag `part3-rung2-v1` still points at the freeze commit, the tree is clean, and every completed run's manifest is at the freeze commit with a clean tree — nothing already earned is lost. **What is needed is a ruling, not an improvisation:** (a) execute the remaining runs from a separate checkout pinned at the freeze commit (a git worktree at `b62a0fe`, data directory pointed at the main repo's hash-verified data — manifests would then show the freeze commit and a clean tree, satisfying §5 as written); or (b) a formal amendment redefining the §5 validity check (e.g. manifest commit must carry the frozen implementation byte-identical over the frozen paths, verified per run). Until one is chosen, the rung stands incomplete: §8.2's family, §8.3's headline and the U2 tables cannot be computed, and `PART3-RUNG2-RESULTS.md` is not yet written (it reports a completed rung or it does not report).

## RUNG 2 EXECUTION RESUMED — the worktree ruling (24 Nov 2026)

- **Ruling (parent decision, no amendment): option (a).** The seven outstanding runs execute from a git worktree pinned at the freeze commit — `~/workspace/connectome-work/rung2-worktree`, detached HEAD `b62a0fe70671a1f789e97ba7992120d060aae27a`, clean tree. A worktree at `b62a0fe` is the freeze commit with a clean tree, so §5's manifest premise is satisfied as written; the preregistration is not amended and nothing runs from the main tree.
- **Verified before the first re-run:** the frozen runner takes the manifest's git info from the code's own repo root, and importing `ctb` from the worktree returns exactly (`b62a0fe…`, dirty = False); the worktree's `fresh/ctb`, `fresh/part2`, `fresh/tests` are byte-identical to `0cb9b81` (diff empty); `data_dir` points at the main repo's Part 1 data with hashes re-verified (`e6b71e17…`, `94db8c65…` — the loader re-verifies on every run and each manifest records them); outputs land in the main repo's `fresh/runs/` (`fresh/runs/` is gitignored in both trees). Driver: `work-rung2/run_rung2_wt.py` (SHA-256 `7461971e…`), the verified driver with only paths and the re-run's run_id changed.
- **Sugar+bitter re-run** takes the new run_id `part3-rung2-sugarbitter-rerun1` per §4 (same seeds 6160–6189); attempt 1 (`part3-rung2-sugarbitter`, empty directory) stays on record as void. Remaining order per §4: sugar+bitter re-run → water → bitter100 → bitter150 → sugarbitter100 → sugarbitter150 → bilateral secondary condition (v). The analysis script is the verified `work/analyze_rung2.py` (`2cfea92b…`) with a single relabelling — the sugar+bitter key carries the re-run's run_id, as §4's void rule requires a new one; the copy is diffed against the original and re-passes the synthetic test before use, and the relabel is declared in the results report.
- **Sugar+bitter re-run — RUN, clean.** `part3-rung2-sugarbitter-rerun1`: 521,251 spikes, 440 active neurons; runner wall 735.9 s; manifest at the freeze commit, clean tree, trial seeds 6160–6189, data hashes matching the freeze record. Attempt 1 stays on record as void.
- **Water — RUN, clean.** `part3-rung2-water`: 226,920 spikes, 345 active; wall 1,589.8 s; manifest at the freeze commit, clean tree, seeds 6190–6219.
- **Bitter arm @ 100 Hz — RUN, clean.** `part3-rung2-bitter100`: 85,780 spikes, 66 active; wall 2,123.3 s (the shared cell throttled hard through this one; wall-clock is contention, not correctness); manifest at the freeze commit, clean tree, seeds 6230–6259.
- **Bitter arm @ 150 Hz — RUN, clean.** `part3-rung2-bitter150`: 140,035 spikes, 83 active; wall 192.6 s; manifest at the freeze commit, clean tree, seeds 6260–6289.
- **Sugar+bitter arm @ bitter 100 Hz, attempt 1 — VOID (machine restart), logged per §4.** The attempt (run_id `part3-rung2-sugarbitter100`, seeds 6290–6319) was killed mid-run when the machine itself restarted (uptime reset observed; the run directory is **empty** — no output, no partial trial set). Exactly the §4 case: the attempt is void and the re-run takes a new run_id, `part3-rung2-sugarbitter100-rerun1`, same seeds. The remaining sequence (sugarbitter100 re-run → sugarbitter150 → bilateral) relaunches from the worktree.
- **Sugar+bitter arm @ bitter 100 Hz, re-run — RUN, clean.** `part3-rung2-sugarbitter100-rerun1`: 504,190 spikes, 465 active; wall 1,716.0 s; manifest at the freeze commit, clean tree, seeds 6290–6319.
- **Sugar+bitter arm @ bitter 150 Hz — RUN, clean.** `part3-rung2-sugarbitter150`: 513,237 spikes, 454 active; wall 2,112.6 s; manifest at the freeze commit, clean tree, seeds 6320–6349.
- **Bilateral secondary condition (v), attempt 1 — VOID (killed), logged per §4.** The attempt (run_id `part3-rung2-bilateral`, seeds 6350–6379) was killed by the shared machine (SIGKILL) ~42 min in, at ~5.2 GB RSS — the bilateral drive produces the rung's largest spike output and the runner holds all 30 trials in memory, so this condition is the most exposed to the cell's memory contention. The run directory is **empty** — no output, no partial trial set; the attempt is void, exactly the §4 case. The re-run takes a new run_id, `part3-rung2-bilateral-rerun1`, same seeds, per §4. No harness change is made or permitted: the frozen runner is what it is, and the void/re-run rule is the preregistration's own answer to a killed run.
- **Bilateral re-run attempt (rerun1) — VOID (machine restart), logged per §4.** The re-run (run_id `part3-rung2-bilateral-rerun1`, seeds 6350–6379) was killed ~7 min in when the machine restarted a second time (uptime reset observed); the run directory is **empty** — no output, no partial trial set. Void under §4, like the attempts before it. The re-run takes the next run_id, `part3-rung2-bilateral-rerun2`, same seeds. The condition itself is not in question: every completed condition in this rung ran through the same frozen runner, and the bilateral configuration's weight was already shown by attempt 1's 42 minutes of clean progress before the memory kill.
- **Bilateral re-run (rerun2) — RUN, clean.** `part3-rung2-bilateral-rerun2`: 640,305 spikes, 510 active neurons (496 / 452 at the higher thresholds); wall 464.1 s; manifest at the freeze commit, clean tree, seeds 6350–6379. MN9 L 93.17 Hz [91.53, 94.80], R 64.87 Hz [62.87, 66.80], pooled 158.03 Hz, descriptive only.
- **ANALYSIS — COMPLETE.** Executed through the relabelled copy of the verified analysis script (`work-rung2/analyze_rung2_rerun.py`, SHA-256 `12ebded4…`): the diff against the verified original (`2cfea92b…`) is exactly six lines, all run_id labels carrying the re-runs' new ids, as §4's void rule requires; the copy re-passed the synthetic test in full before the real analysis ran. Every run passed the script's own §5 assertions (freeze commit, clean tree, registered trial seeds, spike-file hash). Machine-readable output: `work/rung2_analysis.json`; U2 rate table: `work/rung2_u2_rates.csv`.
- **RUNG 2 RESULTS (computed per preregistration, gate pending) — `PART3-RUNG2-RESULTS.md`.** Anchor **PASS** (ΔL +1.07 [−1.23, +3.40] vs ±23.14; ΔR −0.93 [−3.53, +1.53] vs ±15.60; L > R preserved; discrepancy rule not triggered). **Headline (§8.3): SUPPRESSION** — pooled ratio **0.126 [0.115, 0.138]**; per-side L 0.106 [0.094, 0.120], R 0.156 [0.142, 0.170], both on the same side of 1, so the pre-written mixed headline is not triggered. §8.2 family: **all six differences claimed** (Holm-adjusted p = 0.0000 throughout; bitter and sugar+bitter and water all below sugar on both sides). U2 = 638 neurons; 126,762 silent in all four primaries. Dose-response [NON-CONFIRMATORY]: pooled ratio 0.573 [0.550, 0.596] at bitter 100 Hz, 0.330 [0.310, 0.351] at 150 Hz, 0.126 [0.115, 0.138] at the 200 Hz convention — monotone in the bitter rate; the outcome does not flip at any registered rate, its size is convention-dependent, and that dependence is the arms' recorded finding. Bitter alone leaves MN9 at exactly 0.00 Hz at all three rates; water alone gives a nonzero network-mediated MN9 response (L 30.23, R 11.87 Hz), descriptive. Condition (v): pooled 158.03 Hz vs sugar's 155.10; the L > R asymmetry is similar in size (L − R 28.30 vs 32.16 Hz); no test, no RQ-C5 resolution.
- **COMPLETION (§8.4 / §8.5).** Determinism passed; all four primaries ran under the freeze with clean manifests; the anchor passed; §§8.2–8.3 are reported under their rules with the §7 tables complete; the arms and condition (v) ran and are reported under §8.5. **The rung is complete under §8.4 and its record is complete as amended.** Part 7's prerequisite is met on this rung's side. The rung now goes to its HARD gate (full panel + the owner's sign-off); until then every number above is "computed per preregistration, gate pending".

## RUNG 2 HARD GATE: verdicts on the results report (24 Nov 2026)

The rung results (`PART3-RUNG2-RESULTS.md`, computed per preregistration) went to the full panel for the rung's HARD gate. Verdicts received:

- **Reviewer 2: PASS.** Two non-blocking notes: (1) the six-line diff between the verified analysis script and the executed copy belongs in the audit trail; (2) the p-values should be stated as bounds, not as 0.0000. Both are discharged by the gate fixes recorded below.
- **Reviewer 1: PASS, with three required report-text items and a set of record items; no re-run required for any of them.** Required items: (1) wherever the report states a p-value of 0.0000, replace it with a bound: the smallest attainable value given the resample count, stated with the count (for bootstrap tests with B resamples, p < 1/(B+1) with B named). (2) Claim language: every quoted suppression ratio carries the qualifier "bitter at 200 Hz, sugar right-only", or an immediately adjacent sentence saying exactly that; add the registered-scope sentence (only the direction, a ratio below 1, held across the bitter rates run; those arms are non-confirmatory; the size is convention-dependent); confirm the report makes no claim to reproduce Shiu et al. or the first build in this rung and no comparison to first-build numbers anywhere. (3) The GitHub push process item recorded for the gate (next bullet). Record items: (a) laterality kept descriptive (the L/R ratio split and water's sidedness are not interpreted; RQ-C5 not advanced); (b) the void-attempt log completed (each void run_id, its cause as recorded, same seeds re-used, partial outputs never inspected or analysed); (c) the analysis copy's hash and a reference to the recorded six-line diff; (d) completeness confirmed (all nine conditions reported, including the bitter-alone arms at 100 and 150 Hz with their MN9 values); (e) bitter-alone stated with its degenerate interval [0, 0] under zero variance across trials.
- **GitHub push process item (Reviewer 1's item 3), recorded here for the gate.** The first build is preserved on the annotated tag `v0-prototype-final` (marking commit `ab30ab4`, the last old-build commit) and as the `v0-prototype/` folder in the repository, with its original README preserved byte-identical as `v0-prototype/README-original.md` (SHA-256 `ca186f1b…`, verified against `ab30ab4:README.md`). The early push was to main. It deviated from the original plan's timing, under which nothing was to be pushed until the Part 6 checkpoint; the deviation was made at the owner's direct order on 24 Nov 2026 and was recorded at the time in `ANGELIC-DECISIONS.md` ("Publication moved forward") as a timing-only change, with the Part 6 comparison unchanged and still blind. The owner's order is the ratification of the deviation. Stated plainly: this does not affect the rung result's validity. The freeze commit and tag never moved; every condition run's manifest records the freeze commit with a clean tree (the later runs under the worktree ruling recorded above); no rung artefact was altered by the push. The same item stands as Addendum 4 of `PART3-RUNG2-FREEZE.md`.
- **Reviewer 3: provisionally REQUIRE CHANGES, on evidence, not on the result.** He will not pass the gate from a summary and requires the report's verbatim sections. His requirement is being met by supplying the verbatim sections of the fixed report (execution record, deviations and provenance with the six-line diff shown in the report itself, anchor, suppression and the Holm family, completion and the sensitivity arms). His verdict on that evidence is outstanding.

**Gate fixes applied to `PART3-RUNG2-RESULTS.md` (24 Nov 2026), each visible in the report as a dated gate-fix note (its §13), no number changed, no re-run:** the six family p-values (unadjusted and Holm-adjusted) are now stated as p < 0.0001, the bound p < 1/(B+1) at B = 10,000 bootstrap resamples, with the construction stated in §7 and the artefact's stored values (exactly 0.0, unrounded) noted; the suppression ratios carry the "bitter at 200 Hz, sugar right-only" scope in the status line, §6 and §9, with the registered-scope sentence added in §6; laterality sentences added in §§5 and 10; the void-attempt log confirmed complete in §3 (four attempts: two SIGKILLs, of which one under CPU throttling and memory contention and one at about 5.2 GB RSS under memory contention, and two machine restarts; same seeds re-used under new run_ids; every attempt left an empty directory, so no partial output existed to inspect or analyse); the analysis copy's full hash recorded (`12ebded4448de853a2b13e258e64fe09436fd3bcdbd56c2b2a35fba7353205f4`) and the complete six-line diff shown in the report's §13 (all six lines are run_id labels; the copy's B = 10,000 and every statistic are unchanged from the verified original, `2cfea92b0ac4f5560225942f2f7e2b006c37eedb740afba8422d35bd8daa6294`); completeness confirmed (all nine conditions, including the bitter-alone arms at 100 and 150 Hz with MN9 at 0.00 Hz on both sides); the degenerate interval [0, 0] stated for bitter alone in §5; and the report confirmed to carry no reproduction claim for this rung and no first-build comparison anywhere. Reviewer 2's two notes are discharged by the same fixes.

**Gate status: NOT CLOSED.** Reviewer 1 and Reviewer 2 have passed the rung, Reviewer 1's required items are applied, and Reviewer 3's provisional requirement is being met with the verbatim sections; his verdict and the owner's sign-off remain outstanding.

**Correction to the results report's §12 (24 Nov 2026).** One sentence in `PART3-RUNG2-RESULTS.md` §12 said that nothing was pushed or re-tagged during execution. That was imprecise about timing: the owner's publication push did take place during the execution window and carried the already-created freeze tag `part3-rung2-v1` to GitHub, as this log and the freeze record's Addendum 4 already state. The sentence has been corrected in place (recorded as item 9 of the report's §13 gate-fix notes): the tag was not moved or re-created after the freeze, and no frozen file was altered. No number is affected.

**Reviewer 3's objection on the Holm bound, and the correction (24 Nov 2026).** Reviewing the verbatim §7 text, Reviewer 3 objected that the bound p < 1/(B+1) at B = 10,000, which the report stated for the unadjusted and the Holm-adjusted p-values alike, does not carry over to the adjusted values: Holm's step-down multiplies the ordered unadjusted values by up to 6 for a family of six, so an adjusted value can conservatively be as large as 6/(B+1), about 0.0006. The objection is correct and is accepted. The report's §7 now reports the Holm-adjusted values at p < 0.0006 with the reasoning stated, keeps the unadjusted bound at p < 0.0001 with B named, and states that the 0.0 stored in the artefact is the observed resampling tail fraction, not a claim that the underlying p-value is exactly zero. The correction is recorded as item 10 of the report's §13 gate-fix notes, superseding item 1 on the adjusted bound only. No claim changes: all six differences remain claimed, and 0.0006 is far below the 0.05 line.

**Reviewer 3's verdict on the verbatim sections: REQUIRE CHANGES (24 Nov 2026). Gate status remains NOT CLOSED.**

Reviewer 3 has now read the fixed report's sections verbatim (execution record, deviations and provenance with the literal six-line diff, anchor, suppression and the Holm family, completion and the sensitivity arms) and returned his full verdict.

**Accepted.** The execution and freeze provenance, on the documentary record: the worktree arrangement, the run IDs and seed blocks, the four void attempts with same-seed re-runs under new run_ids and no partial-set analysis, the literal unified diff confirming exactly six run_id substitutions and no scientific-parameter change, the D6 waiver properly disclosed with the rung never represented as expert-checked, and the GitHub push and tag timing disclosed with nothing indicating the frozen tag moved or a frozen file was altered. He states the limit of this acceptance himself: he has not independently inspected the repository, manifests, audit JSON or source files, so it is acceptance of the supplied provenance evidence, not an independent audit. **Anchor: PASS** (both deltas inside their bands, L > R preserved; his rounding note is reconciled below). **Primary suppression estimate and classification: supported** as a descriptive model result: the ratio of pooled means is about 0.126 with its 95% interval entirely below 1, so the preregistered classification rule yields SUPPRESSION for the registered drive convention, with scope and non-biological status correctly stated. **Sensitivity arms and bilateral condition: accepted as reported**, non-confirmatory, resolving neither RQ-C5 nor the encoder question. He also records what remains usable regardless of the blocker: the anchor and its equivalence assessment; the MN9 means and bootstrap CIs as estimates; the suppression ratio and its interval as an effect estimate; the arms and bilateral measurements; and the direction and magnitude of the six observed differences.

**Not accepted: the six-comparison confirmatory inference of §7.** The reported p-values are computed as 2 × min(Pr*(Δ* ≤ 0), Pr*(Δ* ≥ 0)) over the ordinary bootstrap distribution of the difference, resampling trials independently within each observed condition. Reviewer 3's objection: that distribution is centred on the observed data, not constructed under a null of equality, so when the observed groups are well separated every replicate can preserve the separation and the tail fraction returns zero without that zero being evidence about the null-tail probability. The 1/(B+1) reporting convention does not repair this, so neither the unadjusted bound (p < 0.0001) nor the Holm-adjusted bound (p < 0.0006) is established as a calibrated hypothesis-test p-value; the Holm step is downstream of the same problem, since adjusting uncalibrated inputs does not produce calibrated adjusted values. What cannot currently stand, in his words, is the statement that all six differences have confirmatory Holm-adjusted statistical significance on the basis of the stated bootstrap tail calculation.

**His four required-resolution items.** (1) Supply the exact preregistered §8.2 wording and the literal two analysis functions (`diff_pvalue` and the Holm function), to establish whether the code matches the frozen protocol and to settle the Holm indexing. (2) Do not silently replace the analysis after seeing the results: any alternative inferential procedure must be treated as a formal amendment or a clearly labelled post hoc analysis, with its assumptions and multiplicity treatment explicit. (3) Preserve the current results and audit artefacts; do not overwrite or relabel the original analysis as though a new method had been preregistered. (4) If the confirmatory inference cannot be justified under the frozen protocol, report the six comparisons descriptively and mark their confirmatory inferential status unresolved; a new confirmatory test would require a separately approved protocol and execution.

**Disposition and consequences, as he states them.** The rung may be operationally complete in the sense that all registered conditions ran and were reported, but he does not certify Part 7's prerequisite as satisfied for downstream execution on the basis of this results report. The verdict does not overturn the Part 3 sugarR 200 Hz PASS, does not alter the frozen run set, and establishes no biological claim; it is limited to this results gate and the inferential validity of §7. Gate status: NOT CLOSED. Reviewer 1 and Reviewer 2 have passed the rung; Reviewer 3 requires changes; the owner's sign-off remains outstanding.

**The rounding note, reconciled.** Reviewer 3 noted a small 1.06 versus 1.07 difference in the anchor's L delta. The artefact (`work/rung2_analysis.json`, anchor object) stores the unrounded value: ΔL = 1.066666666666677 (rung mean 93.63333333333334 against the Part 3 realised mean 92.56666666666666; CI [−1.2333333333333343, 3.399999999999992]; ΔR = −0.93333333333333). The unrounded value rounds to +1.07, the figure the report carries; 1.06 arises only by truncation. The artefact governs, and the difference cannot affect the anchor verdict.

**Primary sources extracted for the panel question (24 Nov 2026).** Item (1) of his required resolution has been gathered verbatim into `work/rung2_gate_panel_question.md`: the frozen §8.2 in full, the §7 and §8 passages that specify the p-value computation, the literal `diff_bootstrap`, `diff_pvalue` and `holm` code with line numbers from the executed copy, and the unrounded anchor deltas. The extraction's stated finding: the frozen preregistration itself specifies the tail-fraction construction in §8.2's second paragraph ("Each comparison's two-sided bootstrap p-value is p = 2 × min(P(Δ ≤ 0), P(Δ ≥ 0)) over the bootstrap distribution, capped at 1"), and the code implements that formula as written (the Holm enumeration is zero-based but the (m − rank) multiplier reproduces the standard (m, m−1, …, 1) sequence, so the indexing settles in the code's favour). The dispute is therefore about the validity of a procedure the panel froze at the preregistration gate, not about a departure from it, and it goes to the full panel as a panel question.

## RUNG 2 HARD GATE: Reviewer 2's ruling on Reviewer 3's p-value objection (24 Nov 2026)

Reviewer 3's objection (recorded above) went to the full panel as a panel question, with the frozen §8.2 wording, the literal analysis functions and the unrounded anchor deltas in front of each reviewer (`work/rung2_gate_panel_question.md`). **Reviewer 2 has ruled:**

- **On the statistics, Reviewer 3 is mathematically right in general.** Resampling around the observed sample difference without centering under H0 estimates a percentile-CI-inversion, posterior-like tail probability rather than a null-calibrated frequentist p-value, and its resolution is bounded at 2/(B+1), about 2×10⁻⁴, when 0 of 10,000 draws cross zero.
- **On the gate, the claims stand as executed.** The executed functions (`diff_bootstrap`, `diff_pvalue`, `holm`) implement frozen PART3-RUNG2-PREREG.md §8.2 word for word. Retroactively invalidating a literal, pre-registered formula after seeing the results violates the preregistration contract; and the effect sizes are overwhelmingly separated from zero (bitter is identically 0.00 Hz across 30 trials against sugar's 93.64 / 61.47 Hz; sugar+bitter drops by about 85 to 89 percent; water drops by about 68 to 81 percent), so no borderline inference turns on the calibration nuance.
- **Option 2 (downgrade all six §8.2 comparisons to descriptive, confirmatory status unresolved): REJECTED.** It would retroactively strip confirmatory status from a procedure the full panel explicitly reviewed and approved before execution, despite zero deviation from the frozen text and massive separation from zero across all six comparisons, and it sets a precedent under which any post hoc methodological preference can erase a pre-registered outcome.
- **Option 3 (formal amendment plus a labelled post hoc replacement test, as a gate blocker): REJECTED as a gate blocker.** A post hoc replacement test cannot restore confirmatory status once the data are known; a new test run after inspecting the results is post hoc by definition. Blocking Part 7 on re-analysing differences of this size is process friction for no scientific gain. A non-blocking robustness note remains allowed.
- **Part 7 prerequisite (§8.4): CERTIFIED by Reviewer 2 (PASS STANDS).** Completion under §8.4 is the determinism check, the four primary conditions with clean manifests, the anchor pass, and §§8.2–8.3 reported under their pre-stated rules; Reviewer 3 already accepts the provenance, the anchor PASS and the §8.3 suppression result (0.126 [0.115, 0.138]), so holding up Part 7 over a §8.2 p-value-definition dispute, after the frozen formula was executed verbatim, is unwarranted.

**His required wording addition to `PART3-RUNG2-RESULTS.md` (mandatory, non-blocking editorial qualification), recorded here as he specified it:**

1. *Literal preregistration compliance:* state explicitly that all six §8.2 comparisons were evaluated strictly by the frozen PART3-RUNG2-PREREG.md §8.2 formula (p = 2 × min(P(Δ ≤ 0), P(Δ ≥ 0)) over B = 10,000 independent within-condition bootstrap draws, seed 20261127, followed by standard 6-test Holm step-down).
2. *Calibration and finite-resolution disclosure:* note openly that because diff_bootstrap resamples from the empirical distributions without centering under H0, diff_pvalue measures the two-sided tail mass of the uncentered bootstrap difference distribution across zero (a percentile-CI inversion quantity bounded in resolution by 2/(B+1) ≈ 2×10⁻⁴ when zero draws cross 0, reported as < 0.0002 or 0.0000 per formatter) rather than a null-centered permutation/studentized p-value; and note that across all six comparisons the unadjusted 95% CIs exclude 0 by wide margins (bitter identically 0.00 Hz on both sides), so the directional separation does not depend on tail interpolation.
3. *Anchor rounding reconciliation:* record the unrounded ΔL = +1.0667 Hz (+1.07 Hz rounded) alongside the already-accepted anchor PASS, and note that Part 3 sugarR used correlation, overlap-floor, and CI-equivalence criteria rather than diff_pvalue.

The qualification is applied to the results report as item 11 of its §13 gate-fix notes, with a short note at its §7; no frozen output, table bound or claim is changed by it. One detail stays open by design: the report's §7 table states the unadjusted bound at the 1/(B+1) convention prescribed earlier in this gate, Reviewer 2's disclosure raises the 2/(B+1) two-sided resolution, and Reviewer 1's ruling on that detail is pending tonight.

**His forward point, for the Part 5 freeze:** PART5-PREREG.md is not yet frozen (tag `part5-prereg-v1` not created, zero Part 5 evaluation data exist), so if its §7 uses the same 2 × min tail-fraction wording for its Holm family, it can and should be upgraded before the freeze to a null-centred bootstrap or an exact/Monte Carlo permutation test (with floor 1/(B+1)), eliminating Reviewer 3's objection for Part 5 and Part 7 before any data are generated. The check was run the same day, and its finding is recorded here: PART5-PREREG.md §7 names its Holm family and fixes its inference settings (percentile bootstrap, 10,000 resamples over the seed as independent unit, paired resampling of seed pairs, 95% intervals, alpha 0.05 including TOST by the 90% CI within bounds rule), but **nowhere in the document is a per-comparison p-value construction defined**: no tail-fraction formula, no permutation construction, no null-centring; the only test carrying an explicit decision rule is TOST. So what Part 5 carries is not the rung's formula but a specification gap where the rung had a formula, and closing it before the freeze is exactly the upgrade Reviewer 2 recommends. It is recorded here as an open pre-freeze item; the Part 5 document is not edited by this ruling.

**Panel state: Reviewer 1 PASS (pre-objection; ruling on the objection scheduled tonight), Reviewer 2 PASS STANDS with mandatory disclosure, prerequisite certified; Reviewer 3 REQUIRE CHANGES, prerequisite not certified; gate NOT CLOSED.**

## PART 5 PRE-FREEZE AMENDMENT: Reviewer 2's ruling on the §7 p-value construction draft (24 Nov 2026)

The open pre-freeze item recorded above (Part 5's §7 names its Holm family but defines no per-comparison p-value construction) was drafted into an amendment supplying the missing construction: `work/part5_pvalue_amendment_draft.md`. The draft proposes a Monte Carlo permutation test for every family member (B = 10,000; p = (1 + the number of permuted statistics at least as extreme, two-sided) / (B + 1), so a p-value of exactly 0 can never be reported; statistic the difference in means of the endpoint), sign-flip for the paired comparisons, label permutation for the two pooled matched-control comparisons, under a new reserved analysis-seed block (6000-6099), with Holm, the claim rule, the bootstrap CIs and TOST unchanged. PART5-PREREG.md itself is not edited; the draft goes to the panel and to Angelic first. **Reviewer 2 has ruled: CONFIRM, with the revisions below, all of which are now folded into the draft.**

- **Flagged question 1 (the refit variant): CONFIRMED AS DRAFTED.** The construction covers the frozen-variant family members only and does not extend to the refit variant: §7's family names the lesion members in the frozen variant, §8.3 gives refit-variant comparisons secondary status with unadjusted CIs, and configurations whose refit is rejected under §8.2 (L-MN9 by construction) have no refit episodes and so no refit comparison of any kind. The frozen-vs-refit gap stays descriptive: it is paired by configuration, not by seed, because the two variants use different seed lists (5200-5219 against 5300-5319), so no per-seed sign-flip exists for it; it keeps bootstrap CIs and TOST as §8.3 provides, and carries no p-value.
- **Flagged question 2 (seed strata in the label permutation): RESOLVED, seed-stratified adopted.** The draft had adopted an unrestricted label permutation across the 120 episodes of a pooled-control comparison and flagged the stricter seed-restricted variant for ruling. Reviewer 2 ruled for the stratified construction: within each of the 20 shared seeds, the stratum holds six episodes (one targeted, five control); each permutation chooses one of the six at random to carry the targeted label and gives the other five the control label, independently across the 20 seeds, so the group sizes (20 targeted, 100 control) are preserved exactly in every permutation. His stated ground: either construction is valid if the exchangeability unit is stated unambiguously, and the stratified form states it (labels are exchangeable within a seed stratum, never across strata), respects the paired-seed blocking used everywhere else in §7, and keeps seed-to-seed variance out of the null distribution. Insert 1 and Insert 3 of the draft now specify the stratified construction.
- **Edge-case note 1 (all-zero comparison).** The p-value formula's comparison is non-strict (at least as large in absolute value), so if the observed statistic is 0 and every permuted statistic is 0, the formula returns (1 + B)/(B + 1) = 1.0; neither 0 nor an undefined value can arise. This is now stated in Insert 1 in advance.
- **Edge-case note 2 (zero denominator in the suppression-ratio member).** If any seed's arm (b) rate is 0, that seed's per-seed ratio is undefined; the seed's pair is excluded from that member's sign-flip test, the exclusion and the reduced pair count are reported with the member's result, and no substitute value is imputed. This is now stated in Insert 1 in advance.

**Panel state on the draft amendment: Reviewer 2 CONFIRMED with the revisions above; Reviewer 3's ruling outstanding; Reviewer 1's ruling outstanding.** The draft, as revised, is at `work/part5_pvalue_amendment_draft.md`; nothing in PART5-PREREG.md changes until the panel round completes and Angelic approves.

## PART 5 PRE-FREEZE AMENDMENT: Reviewer 3's ruling on the §7 p-value construction draft (24 Nov 2026)

Reviewer 3 has ruled on the same draft amendment Reviewer 2 confirmed above (`work/part5_pvalue_amendment_draft.md`). His reply came from a new continuation chat, because the previous one had filled: **"Review ConnectomeToBehaviour Plan (3)", https://chatgpt.com/c/6b05b89c-74f8-83e9-9aaa-f627e0acc54c**, recorded here as his current chat. **His verdict: ACCEPT WITH REQUIRED CLARIFICATIONS.** The clarifications are incorporated into the draft revision of the same date.

- **Substance.** The permutation construction answers his objection for future, not-yet-executed confirmatory families, and is substantially preferable to treating the tail fraction of an ordinary, uncentred bootstrap distribution as a hypothesis-test p-value. Retaining bootstrap confidence intervals for estimation while using permutation tests for hypothesis testing is, in his words, a coherent division of labour. The plus-one Monte Carlo formula is accepted: it avoids reporting zero, and its reference distribution is generated under a specified null transformation rather than from the tails of a distribution centred on the observed data.
- **Standing note on the rung, recorded as he states it.** This amendment cannot retroactively repair the completed four-conditions rung analysis: that rung's reported bootstrap tail fractions remain uncalibrated as inferential p-values under the method described, its descriptive estimates and confidence intervals remain usable, and its six confirmatory significance claims remain unresolved in his judgement unless addressed through a separately approved procedure. The new method can govern future families, not past ones. The rung question itself awaits Reviewer 1's ruling, scheduled for tonight. This ruling is approval of the amendment's methodological direction, not approval of the amendment as frozen, and not a Part 5 or Part 7 execution-gate PASS.
- **Clarification A: state the exchangeability assumptions.** A permutation test does not become valid merely because it permutes something; the amendment must state, for each test, what units are exchangeable under the null, what transformation is permitted, what feature of the design justifies that transformation, and whether the test is exact under the stated assumptions or a Monte Carlo approximation. For the sign-flip tests, the assumption is to be stated as exchangeable signs of the paired differences under the null (distributional symmetry about zero); shared seeds alone do not establish it. Disposition: a per-test exchangeability paragraph is now in Insert 1, covering the sign-flip members, the suppression-ratio member, and the label-permutation members (within a seed stratum, under the null the six episodes' labels are exchangeable because the configurations at that seed differ only in the registered lesion or control identity), and stating that all of the tests are Monte Carlo approximations.
- **Clarification B: flagged question 1 (the refit variant) ACCEPTED, with a wording correction.** He accepts leaving the frozen-vs-refit gap without a permutation p-value, provided it remains explicitly descriptive and is not used to make superiority or difference claims; an unpaired test could be designed, but it would be a different inferential procedure requiring its own assumptions and preregistration, and there is no need to invent one merely to give every contrast a p-value. The correction: the phrase "descriptive with bootstrap CIs and TOST" is not statistically consistent, because TOST is an inferential procedure, not descriptive reporting. If the preregistration specifies a valid TOST equivalence assessment for the gap, it may remain a separate equivalence claim under its registered bounds and multiplicity rules; otherwise the gap is reported descriptively without any equivalence claim; and failure to obtain a difference p-value is not evidence of equivalence. **Finding on the check this required:** §8.3 registers the gap as reported descriptively with bootstrap CIs and provides that a TOST equivalence claim about the gap follows §7's rules if one is made; §7's equivalence paragraph names frozen vs refit expressly among the comparisons where a no-difference claim is made only on demonstrated equivalence, with bounds for E endpoints of ±25% of the intact arm's mean for that endpoint and the 90% CI within bounds rule (each one-sided test at 0.05). On multiplicity, the gap is not a member of §7's Holm family, and §8.3 classes refit-variant comparisons as secondary, reported with unadjusted CIs. The first branch therefore applies: the TOST route is registered, and the draft's gap sentence is now written in those terms (descriptive report with bootstrap CIs; a TOST claim, if made, a separate inferential claim under §7's registered rules, outside the permutation and Holm families; absence of a difference test never evidence of equivalence).
- **Clarification C: flagged question 2, within-seed restricted permutation REQUIRED.** He does not approve the unrestricted label permutation: the 20 targeted and 100 pooled-control episodes share seeds 5200-5219, so each seed defines a matched group of one targeted and five control episodes, and unrestricted reassignment would break those groups and treat observations from different seed strata as exchangeable even though the design matched them by seed. The required construction is the within-seed restricted permutation: each stratum's six observations kept together, one assigned the targeted label at random, independently across the 20 strata, group sizes 20 and 100 preserved, the preregistered permutation seed and the plus-one formula used; the exchangeability assumption within each stratum must be stated and defended. This converges with Reviewer 2's adoption of the seed-stratified form above; the draft already specifies it, and the exchangeability paragraph now states the assumption.
- **Clarification D: implementation requirements, now written into Insert 1.** The observed statistic and every permuted statistic use the same difference-in-means calculation and the same absolute-value convention. The sign-flip transformation is independent sign assignment to each paired per-seed difference, with 10,000 assignments sampled from the 2^20 (not enumerated) and the plus-one formula retained. The ratio member's tested paired quantity is r_i minus 1, its statistic the mean, with the zero-denominator handling defined before execution (the draft's edge-case guard, whose wording is now aligned to this). The Holm adjustment is stated with the full family size (m = 9) and the conventional indexing (multipliers m down to 1, running maximum, adjusted values in the original family order), with family membership and order fixed from the preregistration and no outcome-dependent reordering. The audit artefact records the actual permutation counts and the unrounded p-values. The amendment and the analysis code must be approved and frozen before the relevant outcome data are inspected or analysed. The reserved seed block 6000-6099 is suitable in principle, subject to the disjointness check and one-to-one allocation already in the draft.

**Panel state on the draft amendment: Reviewer 2 CONFIRMED (revisions incorporated); Reviewer 3 ACCEPT WITH REQUIRED CLARIFICATIONS (clarifications incorporated in the draft revision of 24 Nov 2026); Reviewer 1's ruling outstanding, scheduled for tonight.** PART5-PREREG.md itself is unchanged; nothing in it changes until the panel round completes and Angelic approves.

## Note — repository restructure (24 Nov 2026)

At the owner's direction the repository was rearranged on 24 Nov 2026 to follow the arrangement of her fatigue-detection project: documents in `docs/` under descriptive names, code in `src/`, recorded outputs in `results/`, nothing named after her. This log is now `docs/reviews/gate_reviews.md`. The Part 5 preregistration is now `docs/closed_loop_preregistration.md`; its path references were updated by a dated editorial amendment in its amendment history, with no registered content changed. The Part 5 p-value amendment draft stands unaffected in substance: the document it will amend, if approved, is the same document at its new path. The frozen tags were not moved. Full old-to-new mapping: `docs/name_changes.md`.

---

## RUNG 2 HARD GATE: Reviewer 1's follow-up session (24 Nov 2026, evening)

Session in Reviewer 1's chat (https://claude.ai/chat/e3e2b04f-0f06-4905-bb69-f068f549879b), after the free-message limit reset at 20:50 WAT. Five replies, messages 58, 60, 62, 64 and 66, all recorded verbatim below. Replies 62 and 64 arrived while the messages were still being sent (the dispute message first, then the materials, then the draft), so they rule on (a) and (b) and give requirements for (c); reply 66, given after all three messages had landed, is the ruling on (c) and supersedes the (c) requirement lists. Times are as reported, approximate.

### Reply 1 — item 3 and the planned fixes (message 58, ~20:58 WAT)

Reviewer 1: item 3 and the planned fixes

Item 3: resolved. The old build is preserved on the named tag v0-prototype-final at ab30ab4. It is also kept inside the repo as v0-prototype/ with its original README byte-identical, and that satisfies D7. The push to main was owner-ordered and recorded at the time as a timing-only change, so recording it as an owner-ordered deviation, with her order as the ratification, is the right treatment. I agree it does not affect the rung result.

Two notes for the record, neither blocking:

1. The public README still carries the known flaws. A byte-identical v0 README keeps the early "electrophysiology ground truth" wording and the old numbers. That is correct for preservation. I'd add a short note outside the preserved file, for example in the top-level README, saying the v0 build is superseded and that its known issues are documented in the Part 6 comparison. That is the "what I got wrong and fixed" framing the hiring lens favoured.

2. Say what "blind" now means. The old numbers are public, so the Part 6 comparison's blindness depends on process, not on access. In the gate record, state the rule: the fresh outputs (the rung and every Part 5 and Part 7 result) are hashed and locked before anyone opens v0 numbers for comparison. The report should give the hash of each locked output and the time it was locked.

Items 1 and 2 and the record items

The planned changes are what I required:

- p-values reported as bounds with the resample count stated;
- every quoted ratio carrying "bitter at 200 Hz, sugar right-only";
- direction-only language across the rates, with the dose-response arms described as non-confirmatory;
- no reproduction or old-build comparison claims;
- the void log with causes, the analysis-copy hash and diff reference, the bitter-alone arms' values, the degenerate [0, 0] interval, and descriptive laterality.

When you send the text for my check

Please include these verbatim:

- §8.2's table, with the Holm-adjusted bounds;
- §8.3's verdict wording;
- the void-attempt log;
- the nine-condition summary table (so I can confirm every condition is reported, including bitter alone at 100 and 150 Hz);
- the sentence that scopes the headline claim.

My verdict stands as given: PASS, provided those fixes land as described.

### Reply 2 — rung results text check (message 60, ~21:05 WAT)

Reviewer 1: rung results text check

Verdict: PASS stands. The numbers hang together and the claim language is correctly scoped. One required fix is to the p-value bound, which is a reporting correction with no effect on any verdict. A few smaller wording items follow.

Arithmetic and consistency, checked against the text

- Pooled rates: 93.63 + 61.47 = 155.10; 9.97 + 9.57 = 19.54 (reported 19.53, rounding); 30.23 + 11.87 = 42.10; 55.00 + 33.83 = 88.83; 29.30 + 21.93 = 51.23; 93.17 + 64.87 = 158.04 (reported 158.03, rounding). All are fine.
- Ratios: 19.53/155.10 = 0.126, 9.97/93.63 = 0.106, 9.57/61.47 = 0.156, 88.83/155.10 = 0.573 and 51.23/155.10 = 0.330. All match.
- Differences against sugar: −93.63 and −61.47 for bitter, −83.67 and −51.90 for sugar+bitter, and −63.40 and −49.60 for water. All match. The CIs equal the sugar CI negated for bitter, and the combined widths are consistent for the others.
- Nesting: each 90% CI sits inside its 95% CI.
- "About an eighth": 0.126 ≈ 1/8, which is correct.
- Void log: four attempts, two SIGKILL and two machine restarts, matches the earlier summary. All nine conditions are reported, including bitter alone at both arm rates, with the degenerate [0, 0] stated.

Required fix: the p-value bound

The note defines each p-value as twice the smaller tail fraction, but gives the bound as 1/(B+1). That bound applies to a one-sided tail fraction. For the two-sided definition stated, with zero resamples at or beyond zero, the add-one convention gives 2/(B+1) ≈ 0.0002.

- On the Holm point you flagged: you are right that Holm-adjusted values cannot be reported at the unadjusted bound (the extract's "< 0.0001" is wrong). But the report's "< 0.0006" is 6/(B+1), which also uses the one-sided bound.
- Corrected under the two-sided definition: unadjusted p < 0.0002, and Holm-adjusted p < 12/(B+1) ≈ 0.0012.
- Either way is acceptable as long as the definition and bound match: restate the bounds as 0.0002 and 0.0012, or redefine p as the one-sided tail fraction and say so. The extract's sentence "The Holm-adjusted values are reported at the same bound" must go in either case. All six comparisons remain claimed.

Smaller wording items

1. Void log. Only the bilateral re-run's new run_id is named. List the new run_ids for the sugar+bitter and sugar+bitter 100 Hz re-runs too, and state that no output from any voided attempt was inspected.
2. Scope sentence. Add "brain-only, 1.0 s trials, N = 30" and name the bitter set as the upstream neu_bitter list (21 neurons, laterality not recorded). Say that "suppression" refers to the MN9 feeding readout in this model.
3. "Bitter drive … does not recruit the feeding readout." Add "in this model, brain-only".
4. No old-build comparison: it is absent here, as it should be. Keep it so.

Forward note for Part 5 (not a change to the frozen design)

The sugar+bitter residual of 19.5 Hz pooled is above r_lo = 5 Hz, so the decoder will command a small extension in arm (d). If r_hi comes out near 184 Hz, e ≈ 0.08 and E ≈ 0.18 rad. That exceeds the registered 0.10 rad onset threshold but sits far below the contact threshold (~0.84–0.88 of E/E_max), so arm (d) would show an extension onset with no food contact.

Record that as a pre-evaluation expectation in the Part 5 record now, and confirm that graded endpoints, not the thresholded onset, carry the sugar+bitter comparison. It must not read as a surprise, or as a decoder failure, when the data come in.

Send the corrected §7 paragraph and the amended void log when ready. I don't need to see the rest again.

### Reply 3 — rulings on (a), (b), (c) (message 62, ~21:12 WAT; sent before the materials and the draft had arrived)

Reviewer 1: rulings on (a), (b), (c)

The message says the frozen §8.2 text and the Part 5 draft amendment "follow below", but neither arrived. I can rule on (a) and (b) from the described procedure. For (c) I can only give requirements until I see the text.

(a) Does the registered procedure stand? It stands as executed, and Reviewer 3's objection is right about what the quantity is. These two positions are compatible, and both reviewers are right about part of it.

• Reviewer 2 is right on the contract. The executed code matches the frozen formula. Redefining the test after seeing results would breach the preregistration. Claims shouldn't be voided or recomputed to a different construction on that ground.
• Reviewer 3 is right on the construction. Twice the smaller tail fraction of a bootstrap distribution centred on the observed difference is a confidence-interval-inversion quantity, not a null-distribution p-value. It isn't calibrated, and Holm applied to it gives nominal values, not guaranteed family-wise control. My earlier instruction to report these as bounds left that unaddressed. That was my miss.
• The claims are not at risk. From the reported CI half-widths, the six differences sit between about 46 and 105 standard errors from zero. Any valid test gives p far below any threshold.

Resolution I require (three items, all in the report):
1. A dated methodological disclosure. State exactly what the quantity is: the bootstrap tail fraction, which is not a null-distribution p-value, and Holm over it is nominal. State that the registered procedure was executed as frozen.
2. Rename the columns. "p (unadj.)" and "p (Holm)" become "bootstrap tail fraction (two-sided)" and "Holm over tail fractions (nominal)". The "Claimed" column stays, labelled "claimed under the registered rule".
3. A supplementary calibrated check, labelled post-hoc and non-governing. For each of the six comparisons, run a Monte Carlo permutation test: pool the 60 trials of the two conditions, permute labels, use the absolute difference in means, report p = (1 + k)/(B + 1), with B and the seed declared, and apply Holm across the six.
• With B = 10,000 and zero exceedances, each p is 1/(B+1), and Holm gives < 6/(B+1) ≈ 0.0006.
• If the supplementary result ever disagreed with the registered one, that goes to the panel as a discrepancy. The registered rule governs the registered claim.
• The permutation null is the sharp one (the condition has no effect on the trial distribution). That null is appropriate here, including for bitter versus sugar, where the bitter group has zero variance.

On the Part 7 prerequisite. §8.4 completion (determinism check, four primaries, anchor) is untouched by this dispute. I certify it, conditional on items 1–3 being in the report. That makes two of three. I'd prefer Reviewer 3 to confirm the amended wording instead of being overruled.

(b) The 1/(B+1) versus 2/(B+1) bound

For the two-sided quantity as the report defines it (twice the smaller tail), the add-one convention gives 2/(B+1) ≈ 0.0002 , not 1/(B+1). The report's table should therefore say unadjusted < 0.0002, and Holm over the tail fractions < 12/(B+1) ≈ 0.0012. The report's current Holm bound of < 0.0006 is correct for the permutation quantity in item 3 (6/(B+1)), but not for the registered tail fraction. Use each number only with its own quantity. Also state the plain fact, which needs no convention: "0 of 10,000 resamples crossed zero in any of the six tests." Note that add-one is a reporting convention for permutation p-values. For a bootstrap tail fraction it is only conventional, and the table should say so.

(c) The Part 5 draft amendment

I haven't received the text, so I can't rule on it as written. Please resend it. In the meantime, these are my requirements. The "seed-stratified" construction Reviewers 2 and 3 adopted is consistent with them if stratification follows how seeds and scenarios are actually shared across arms.
1. Exchangeability. State the permutation unit (episode, seed or scenario block) and why units are exchangeable under the null. If arms share seeds or scenarios, permute within strata (paired by seed).
2. Statistic and tail fixed in advance. Define the statistic, and use the absolute difference for two-sided tests.
3. B large enough for the family. The minimum attainable p is 1/(B+1), and for Holm across m tests it must sit below α/m. Declare B and the seed, and report p as (1 + k)/(B + 1), never 0.
4. Equivalence (TOST) construction. Part 5 has TOST criteria, so state how equivalence intervals are built (for example, a percentile bootstrap CI at the 90% level, with declared seeds). Permutation does not give that directly.
5. Zero-variance and tied cases. State how a condition with identical values (for example, all MN9 zero) is handled.
6. Family and Holm order. State the family and its members.
7. A synthetic null check before the freeze. Part 5 has no data yet, so use synthetic data with the same n and structure and the actual test code. Confirm the false-positive rate is near its nominal level at α = 0.05, record the output, and hash it with the code.
8. No evaluation seed enters the test construction, and the amendment is time-stamped before the Part 5 freeze.

If the draft meets these, I'll confirm it. Send the text and I'll check it against them.

### Reply 4 — the materials (message 64, ~21:13 WAT; after the materials arrived, before the draft)

Reviewer 1: the materials

The rung materials arrived. The Part 5 draft amendment did not, so my ruling on (c) is still the requirement list, not a check of the text. My rulings on (a) and (b) are unchanged. I checked the materials against them.

What the materials settle
• Registered formula vs executed code. diff_pvalue is 2 × min(P(d ≤ 0), P(d ≥ 0)) capped at 1, matching §8.2 word for word. Reviewer 2 is right about the facts, and Reviewer 3 has not alleged a departure.
• holm. Zero-based rank with (m − rank) gives multipliers 6, 5, …, 1 in ascending order, with the running maximum. That is the correct step-down procedure, and the indexing concern is answered. (Holm also stays valid when the six bootstrap distributions share index draws, which they do here because of the shared seed and sample sizes.)
• Anchor deltas. +1.0667 rounds to +1.07, and I confirm 62.4 − 0.9333 = 61.4667. The Δ interval of [−1.23, +3.40] is wider than the rung's own sugar CI would give, which is correct, since both sides of the difference carry uncertainty.
• One immaterial inconsistency. The ±23.1425 Hz band equals 0.25 × 92.57, the rounded primary, while Δ uses the unrounded 92.5667 (0.25 × that = 23.1417). The difference is under 0.001 Hz and changes nothing. State in the report which constant the band uses.

Ruling (a): unchanged
I accept Reviewer 3's point on what the quantity is, and I accept Reviewer 2's point on the contract. I also own my part. I approved the rung preregistration, and the p-value construction was in the frozen text. I did not flag that it is a bootstrap tail fraction and not a null-calibrated p-value, and I then advised reporting it as a bound. That advice papered over the problem. To let Reviewer 3 lift his block without breaching the preregistration:
1. The dated methodological disclosure, with the columns renamed as I specified ("bootstrap tail fraction (two-sided)" and "Holm over tail fractions (nominal)"), and "claimed under the registered rule".
2. The supplementary Monte Carlo permutation check, labelled post-hoc and non-governing: pooled labels, absolute difference in means, p = (1 + k)/(B + 1), Holm across the six.
3. A discrepancy between the two goes to the panel. The registered rule governs the registered claim.

An exact calculation worth adding. With 30 trials per group, if every one of the six comparisons is perfectly separated (every value in one condition beyond every value in the other, which the Δ-to-CI ratios suggest and the trial data can confirm), the exact two-sided permutation p-value is 2/C(60,30) ≈ 1.7 × 10⁻¹⁷. No test at this sample size can be more significant. State that, and the conclusions no longer depend on the choice of construction. Check the separation from the stored trial rates, which I can't see.

Ruling (b): unchanged
For the registered two-sided quantity under an add-one convention, the bound is 2/(B+1) ≈ 0.0002, and the Holm bound is 12/(B+1) ≈ 0.0012. The 1/(B+1) and 6/(B+1) figures (0.0001 and 0.0006) belong to the one-sided and permutation quantities. Each bound must be paired with its own definition. The simplest and most honest statement is "0 of 10,000 resamples crossed zero in each of the six tests".

Still needed
• The Part 5 draft amendment text. Please resend it. I'll check it against my eight requirements (exchangeability unit and strata, fixed statistic and tail, B large enough for Holm, an equivalence construction, zero-variance handling, the family and Holm order, a synthetic null check before the freeze, and no evaluation seeds in the construction).
• Prerequisite certification. I certify the §8.4 Part 7 prerequisite conditional on items 1–3 above being in the report, and I'd like Reviewer 3 to confirm those items.

### Reply 5 — ruling on the Part 5 p-value amendment (message 66, ~21:15 WAT)

Reviewer 1: ruling on the Part 5 p-value amendment

Verdict: CONFIRM, with three required changes. The construction is right in principle. Seed-stratified label permutation, the plus-one formula, the edge cases, the per-test exchangeability statements and the family and Holm order are all as I required. I agree with both flagged rulings: the frozen-vs-refit gap stays descriptive with TOST as a separate inferential route, and the label permutation is stratified by seed. I ran one check on the draft, and it found a defect.

Required change 1: the suppression-ratio member uses an invalid statistic

The draft sign-flips r_i − 1. A sign-flip is valid only for a statistic that is odd under swapping the two arms' values within a seed. Swapping d and b turns r into 1/r. If r = 2, then r − 1 = +1, but after the swap r = 0.5 and r − 1 = −0.5, not −1. So the signs of r_i − 1 are not exchangeable, even under the strict null that the two arms are interchangeable at each seed.

I simulated this. Arms were exchangeable, so the null was true, with lognormal rates, n = 20 pairs and 10,000-style sign-flip draws. The observed false-positive rates at α = 0.05:

| Per-seed spread (σ) | mean(r − 1) | (d − b)/(d + b) | mean log r |
|---|---|---|---|
| 0.5 | 0.150 | 0.045 | 0.045 |
| 1.0 | 0.361 | 0.049 | 0.049 |
| 1.5 | 0.563 | 0.043 | 0.041 |

The draft's statistic rejects a true null 15–56% of the time in this toy. It's an exact failure of the property this amendment was written to establish.

Fix. Replace the tested quantity with s_i = (d_i − b_i)/(d_i + b_i), where d_i and b_i are that seed's arm (d) and arm (b) rates. The statistic is the mean of s_i, with sign-flip as drafted.

- s_i is exactly odd under swapping, so it is valid under the stated null.
- It handles zero rates. A seed with d_i = 0 gives s_i = −1 (the strongest suppression stays in), and a seed with both rates 0 is set to s_i = 0 and kept.
- The zero-denominator exclusion rule is then no longer needed.
- The registered suppression ratio, its CI and the claim rule are unchanged. Only the quantity feeding the p-value changes, and the amendment should say that.
- State the null in the text: within each seed, the two arms' values are exchangeable. Say that it is the sharp null, and that the symmetry of paired differences follows from it. This also corrects the wording "each paired difference is assumed symmetric", which is a consequence of exchangeability, not a separate assumption.

Required change 2: the synthetic null check, which I asked for and is missing

The draft says the code is frozen before outcome data are inspected. It doesn't say the code is validated. Before the freeze, run the actual analysis code on synthetic data with the real design (20 paired seeds for the sign-flip members, 20 strata of six for the label-permutation members, and the ratio member). Record:

- the false-positive rate at α = 0.05 under a true null, with the number of simulations (at least 1,000);
- the rejection rate under a known effect, as a sanity check on power and sign;
- the output file and its hash, together with the code hash.

A check like this would have caught change 1. Include a skewed case, such as lognormal rates, in the null simulation.

Required change 3: the seed-range claim does not hold at the cap

The amendment says sub-seeds start at 5701 and cannot pass 5900 at the cap of 100 draws per lesion. Arm (e) uses 5800–5819, which falls inside 5701–5900. At the cap, lesion 1 would draw 5701–5800 and lesion 2 would draw 5801–5900, both overlapping arm (e).

- In practice the draws needed may be far fewer than the cap, so no collision may occur.
- The Part 5 text claims disjointness without caveat. Either restrict the sub-seed range to one that ends before 5800 (for example 5701–5799 shared between both lesions, with a stated rule if the cap would be exceeded), or move arm (e) again.
- Check this by script, not by eye. The script should enumerate the worst-case ranges of every block and assert they are pairwise disjoint, with its output recorded in the document's record. This is the same recommendation I made earlier for seed collisions.

Smaller items

- Wording consistency. "The four arm comparisons" are sign-flip members, the suppression-ratio member is a fifth, and "the two lesion comparisons" are four members (peak and mean for each lesion). Total 4 + 1 + 4 = 9, matching m = 9 and seeds 6000–6008.
- Sharp null. In the rationale and every claim, say these tests assess the sharp null that arms or labels are exchangeable. They don't test a difference in means alone, and the CIs carry the effect size.
- RNG. Pin the generator and library version (for example NumPy default_rng, PCG64) and record them in the audit artefact.
- Smallest attainable values. State that the smallest unadjusted p is 1/(B + 1) ≈ 0.0001 and the smallest Holm-adjusted p is 9/(B + 1) ≈ 0.0009, so a reader isn't surprised by a floor.

Not changed

- The seed block 6000–6099 is disjoint from every block the draft lists, and I found nothing wrong with its assignment, apart from the 5701–5900 issue above.
- The frozen-vs-refit handling (descriptive with bootstrap CIs, a TOST claim as a separate inferential route, outside Holm) is accepted as drafted.
- The edge-case treatment of an all-zero comparison (p = 1.0) is correct.

With changes 1–3 made, I'll confirm. I need to see only the revised suppression-ratio paragraph, the synthetic-check output with its hashes, and the seed-disjointness script output.

### Panel state after this session (24 Nov 2026, ~21:15 WAT)

- **Reviewer 1, rung gate: PASS stands**, conditional on (i) the text-check fixes (bound restated as unadjusted < 0.0002 and Holm < 0.0012 with definition matched, or a one-sided redefinition; the "same bound" sentence removed; void log naming all re-run run_ids and stating no voided output was inspected; scope sentence carrying "brain-only, 1.0 s trials, N = 30", the neu_bitter list of 21 neurons, and suppression as the MN9 feeding readout in this model; "in this model, brain-only" on the bitter-recruitment sentence) and (ii) the (a) resolution items 1–3 in the report (dated methodological disclosure, renamed columns, supplementary post-hoc permutation check). He **certifies the §8.4 Part 7 prerequisite** conditional on items 1–3 being in the report, and prefers Reviewer 3 confirm the amended wording rather than be overruled.
- **Reviewer 1, Part 5 draft amendment: CONFIRM, with three required changes** (suppression-ratio statistic replaced by s_i = (d − b)/(d + b); synthetic null check run and recorded with hashes; seed-range claim fixed with a script-checked disjointness assertion). He will confirm once he has seen the revised suppression-ratio paragraph, the synthetic-check output with its hashes, and the seed-disjointness script output. The draft is not yet confirmed as final text, and `PART5-PREREG.md` (`docs/closed_loop_preregistration.md`) is unchanged.
- **Follow-ups Reviewer 1 asked for, not part of this session's messages:** (i) the corrected §7 paragraph and amended void log for the rung report; (ii) the Part 5 pre-evaluation expectation recorded in the Part 5 record (arm (d) extension onset with no food contact; graded endpoints, not the thresholded onset, carry the sugar+bitter comparison). Also outstanding from reply 1, non-blocking: a note outside the preserved v0 file (e.g. top-level README) saying v0 is superseded with known issues documented in the Part 6 comparison, and the gate record stating the hash-and-lock rule for "blind" (fresh outputs hashed and locked before anyone opens v0 numbers, with hash and lock time in the report).
- **Gate status: NOT CLOSED.** Reviewer 3's REQUIRE CHANGES still stands until he confirms the (a) resolution wording; Reviewer 2 PASS STANDS with the disclosure; Reviewer 1 PASS stands as above; the owner's sign-off remains outstanding.

*Transcription note: Claude's collapsed activity labels above each reply ("Checking the old build was preserved correctly", "Checking how the extension threshold treats residual firing", "Weighing the p-value convention against the two-sided statistic", "Checking exact permutation p-values for separated groups", "Ran a command") are tool-use labels, not reply text, and are excluded. In message 62 the bound sentence is reproduced exactly as shown, including the space before the comma in "0.0002 , not 1/(B+1)".*

---

## Hash-and-lock rule for the Part 6 comparison (24 Nov 2026)

"Blind" for the Part 6 comparison means process, not access, since the old numbers are public. Fresh outputs (the rung and every Part 5 and Part 7 result) are hashed and locked before anyone opens v0 numbers for comparison, with the hash and lock time stated in the report.

Lock record for the rung: `docs/taste_conditions_results.md`, SHA-256 `54c8dccda026afb259fa64b0b44e7ec052859b892e8bbfa429881b6ef689cd2f`, locked 24 Nov 2026, evening, after Reviewer 1's fixes.

## Rung gate follow-up: fixes and checks recorded (24 Nov 2026, evening)

Reviewer 1's follow-up items are now in the record.

Rung report fixes, in `docs/taste_conditions_results.md` (SHA-256 `54c8dccda026afb259fa64b0b44e7ec052859b892e8bbfa429881b6ef689cd2f`, repo copy and local mirror byte-identical): bounds restated (unadjusted < 0.0002, Holm < 0.0012), columns renamed, disclosure added, void log completed, scope and band-constant notes added, exact-permutation note added (separation confirmed in all six comparisons).

Supplementary post-hoc permutation check: seed 20261124, B = 10,000, all six k = 0, p = 0.0001, Holm = 0.0006, no disagreement with the frozen analysis. Script `work/rung2_supplementary_permutation.py` (SHA-256 `8e1b8dfd627244db51860d20a333878ea915240bf7c22e89f0a66494199057d1`); artefact `work/rung2_supplementary_permutation.json` (SHA-256 `315a10ea44df4090508a143946c37d1160e5a58f5b00afb84418ff82fc093d6c`).

Part 5 draft changes, in `work/part5_pvalue_amendment_draft.md` (draft only; `docs/closed_loop_preregistration.md` unchanged apart from the expectation note below): statistic replaced by s_i = (d_i - b_i)/(d_i + b_i). Synthetic null check executed and passing with the actual test code (true null normal: per-member false-positive rate 0.041 to 0.061, family-wise 0.060; lognormal: 0.040 to 0.065, family-wise 0.056; known effect: rejection 0.982 to 1.000). Code `work/part5_permutation_test.py` (SHA-256 `825e5157f102d248b2cefd24fbbf083a506ea3b29e41c7113ea8fd6e64a006da`); output `work/part5_synthetic_null_check_output.txt` (SHA-256 `df214b60c4138657c958900523f39c9c25c35087a104c182d91529086501b505`).

Seed-disjointness check PASS: 35 blocks, 990 seeds, all pairwise disjoint; sub-seed range restricted to 5701-5799 shared stream. Script `work/part5_seed_disjointness_check.py` (SHA-256 `61dc7c461b52471b40ddaf2cfcd474eff113a91b6f9f80bc6f20c14af14df5f8`); output `work/part5_seed_disjointness_output.txt` (SHA-256 `95b11e84dda7b3118b50cdfb67470ecf94f0789873be3a24042c31b2a8d802c0`).

Expectation note: a dated pre-evaluation expectation note was added to §10 of `docs/closed_loop_preregistration.md` (sugar+bitter residual 19.5 Hz pooled above r_lo = 5 Hz, so arm (d) is expected to show an extension onset with no food contact; graded endpoints, not the thresholded onset, carry the sugar+bitter comparison). It is labelled as expectation, not result, and no registered content was changed.

README note: a short note was added to the top-level README, outside the preserved v0 file, saying the v0 build is superseded and its known issues are documented in the Part 6 comparison.

Hash-and-lock rule: recorded above in this gate record, with the rung report's hash and lock time.

Reviewer 1's conditional certification of the §8.4 Part 7 prerequisite stands: certified, conditional on items 1-3 being in the report, which they now are. **The gate is still NOT CLOSED**, pending Reviewer 3's confirmation of the amended wording and the owner's sign-off.

## Reviewer 1 follow-up reply: per-lesion sub-streams and 5,000-simulation re-run (24 Nov 2026, evening)

Reviewer 1 replied to the draft-confirmation message. His rulings, as received: changes 1 and 2 confirmed; change 3 confirmed once the per-lesion sub-stream sentence is amended; the family-wise criterion to be restated as one-sided (a family-wise error rate is checked against an upper bound only, not a two-sided band); the synthetic null check to be re-run at 5,000 simulations per null case on the actual code to settle the pooled 116/2000 = 0.058 family-wise figure. He asked to see only the amended sub-stream sentence and the re-run script output, nothing else.

NOTE ON THE VERBATIM RECORD: the full verbatim text of this reply was not in the inherited context of the agent who applied these fixes, and a search of the workspace, memory and /tmp found no copy of it. The summary above is therefore NOT a verbatim transcription. The verbatim text must be supplied by the parent agent and appended here before this entry is complete.

Fixes applied to the draft (`work/part5_pvalue_amendment_draft.md`; the preregistration itself not edited):

- Per-lesion sub-streams: 5701-5749 for L-MN9, 5750-5799 for L-GRN, fixed in advance, deterministic and order-independent, each lesion falling back within its own stream under the section 8.1 fallback. Applying the amendment also amends section 8.1's generation sentence to the two fixed streams in place of the shared 5701, 5702, ... sequence.
- Seed-disjointness script re-run with the two streams as separate blocks: PASS, 39 blocks, 993 seeds, all pairwise disjoint; worst-case assertions (L-MN9 max 5749, L-GRN max 5799, both below 5800; the two streams partition 5701-5799 exactly). Script `work/part5_seed_disjointness_check.py` (SHA-256 `039bf97c48cf530fc00bcd016c87e6c39059c42f137368579994517d33184570`); output `work/part5_seed_disjointness_output.txt` (SHA-256 `f4bef7a672132eb622328733f9d9a30d391137b2b673fe35a9416fa891b103a5`).
- Coverage additions: rung bootstrap seeds 20261128, 20261129, 20261130 added; Part 5 declares no 202611xx bootstrap seed for its own confidence intervals (verified against section 7, which resamples seed pairs under the episode seeds and names no bootstrap RNG seed), so none added; the 20261124 and 20261125 wording reconciled to their registered identities (Part 3 MN9 and gap bootstrap seeds) with the reuse recorded, and the preregistration's section 7 sentence labelling them by that reuse flagged in Insert 2 for editorial correction at the freeze; a scan of the run artefacts under repo/results (63 JSON files, 342 distinct seeds used) confirms every seed actually used falls inside a listed block and none falls inside the new permutation blocks 6000-6099.
- Family-wise criterion restated as one-sided in the draft, in the synthetic-check record, and in the check code: a family-wise error rate is checked against an upper bound only, not a two-sided band.
- Synthetic null check re-run at 5,000 simulations per null case on the actual code: PASS. Per-member false-positive rates under a true null: normal 0.046 to 0.055, lognormal 0.047 to 0.054, all inside the 0.05 plus or minus 0.009 band; family-wise: normal 0.052 (261/5000), lognormal 0.043 (213/5000), both below the 0.059 one-sided upper bound; pooled family-wise 0.0474 (474/10000), below 0.05 and below its one-sided upper bound of 0.0565, settling the earlier pooled 116/2000 = 0.058 figure as noise at the smaller simulation count. Known effect: per-member rejection 0.986 to 1.000, family-wise 1.000. Code `work/part5_permutation_test.py` (SHA-256 `32ab7eab49db97b2611255a1b44c6b5e2818eb0e515fc8fc97b7bc0d961eaaef`); output `work/part5_synthetic_null_check_output_5000.txt` (SHA-256 `410c210e97dcd2bd4303e426ad1d8515b648df685844863d85fe301b2756c830`); elapsed 333.5 s.
- Confirmation message written to `work/r1_substream_confirmation_message.md` (SHA-256 `5a12e701afa3a2ca7a9610cac60930d0e814e14f03802e2d31d4e21335b3f49f`): the amended sub-stream sentence verbatim, the re-run disjointness script output verbatim, and the 5,000-simulation figures. Nothing else in the message.
- Draft status header updated: Reviewer 1 confirmed changes 1 and 2; change 3 confirmed once the per-lesion sub-stream sentence is amended (done in this revision); Reviewers 2 and 3 re-confirmation of the statistic change still outstanding (their browser rounds are in flight).

The gate is still NOT CLOSED: Reviewer 3's confirmation of the amended rung wording, Reviewer 1's confirmation of the revised paragraph and outputs (carried by the message above), Reviewers 2 and 3's re-confirmation of the statistic change, and the owner's sign-off remain outstanding.

## Rung results gate: final confirmations and closure (24 Nov 2026, evening)

The three replies below arrived tonight and are appended verbatim. Verbatim reviewer text keeps its own punctuation throughout.

**Completion note (24 Nov 2026).** The entry above headed "Reviewer 1 follow-up reply: per-lesion sub-streams and 5,000-simulation re-run" summarised Reviewer 1's reply and carried a note that the verbatim text still had to be supplied before that entry is complete. That text is now supplied by the parent agent and appended directly below as Verbatim Reply A, which completes that entry.

### Verbatim Reply A: Reviewer 1, on the Part 5 amendment's three required changes (24 Nov 2026, evening)

Reviewer 1: the three required changes

I checked the text and output against my ruling. I have not re-run your code or script.

Change	Status
1. Suppression-ratio statistic	Satisfied
2. Synthetic null check	Satisfied, with a note on the family-wise criterion
3. Seed-range claim	Satisfied on the stated defect; one issue introduced by the fix

I confirm changes 1 and 2. I confirm change 3 once one sentence in the amendment is changed. After that, the amendment can go to the owner.

Change 1: satisfied

The revised paragraph does what I asked:

s_i = (d_i − b_i)/(d_i + b_i) is odd under swapping.
A seed with d_i = 0 gives −1 and stays in. A seed with both rates 0 gives 0 and is kept. The exclusion rule is gone.
The sharp null is stated, and the symmetry now follows from exchangeability.
The registered ratio, its CI and the claim rule are unchanged.
Change 2: satisfied
The pass criterion was stated before the run. All 18 null cells and both family-wise figures are inside 0.05 ± 0.021. The mean across the 18 cells is 0.0504.
The power check is near 1.0, and the self-tests pass.
The diagnostic reproduces my own simulation. The r − 1 statistic gives 0.159 / 0.365 / 0.579 (mine 0.150 / 0.361 / 0.563) and s_i stays near 0.045. That is independent agreement between two simulations on the same defect.
One note on the family-wise figures. The two values, 0.060 and 0.056, sit slightly above the nominal 0.05 ceiling for Holm. A two-sided ±0.021 band is too lenient for a family-wise error rate, which should only be checked against an upper bound. Pooled, the two are 116/2000 = 0.058, about 1.6 standard errors above 0.05. That isn’t evidence of a problem, but a re-run at 5,000 simulations (the whole check took 117 s) would settle it cheaply. State the family-wise criterion as one-sided in the record. This is not blocking.
Change 3: the stated defect is fixed, but the fix creates a starvation risk

I confirmed the arithmetic. The block sizes sum to 990, which matches the script’s total, and the union is 990 distinct seeds. The worst-case assertion (the sub-seed stream ends at 5799, below arm (e) at 5800) is right.

The problem: the sub-seed stream is now a single shared stream “drawn in order … across both lesions”. If the first lesion needs many candidates before it finds five sets that pass the screen, it can use most of the 99 sub-seeds and leave the second lesion with few or none. The fallback then means “all drawn sets are used and the shortfall reported”. That would leave one lesion with fewer controls than the design needs, and the outcome would depend on processing order.

Required change: give each lesion its own fixed sub-stream, for example 5701–5749 for L-MN9 and 5750–5799 for L-GRN. Say that the ranges are fixed in advance and that each lesion falls back within its own stream. This is deterministic, order-independent, and keeps the stream below 5800. Rerun the disjointness script with the two ranges listed as separate blocks.

Coverage items for the disjointness script (non-blocking, but cheap)
Bootstrap seeds. The script lists analysis seeds 20261123–20261127 but not the rung’s 20261128, 20261129 and 20261130. Add them, along with any bootstrap seeds Part 5 declares for its own CIs.
Labels. Insert 2’s disjointness paragraph describes 20261124 and 20261125 as “gate and slice synthetic seeds”, while the script and the rung preregistration label them the Part 3 MN9 and gap bootstrap seeds. Reconcile the wording so the record agrees with itself.
Seeds actually used. The script checks documented ranges. Add a scan of the run manifests in the repository to confirm that every seed actually used (including any from the Part 4 gate and slice) falls inside a listed block and that none falls inside the new ones.

Send the amended sub-stream sentence and the re-run script output. I need to see nothing else.

### Verbatim Reply B: Reviewer 2, re-confirmation of the Part 5 amendment (24 Nov 2026, evening)

Part 5 Preregistration (PART5-PREREG.md §7) Permutation Amendment (Revised) — Reviewer 2 Re-Confirmation (CONFIRM)

Reviewer: Reviewer 2 (Gemini)

Subject: Re-confirmation of revised PART5-PREREG.md §7 permutation-test amendment (replacing r_i - 1 with s_i = (d_i - b_i) / (d_i + b_i) for the suppression-ratio test statistic, explicit sharp-null exchangeability statement, bounded control sub-seed stream 5701–5799, and verified synthetic null / seed-disjointness artefacts)

Verdict: CONFIRM — No further changes required. Logged as delegated under Angelic Charles's authority/delegation (subject to ratification).

1) Why s_i = (d_i - b_i) / (d_i + b_i) Replaces r_i - 1 Cleanly

Exact Oddness Under Within-Seed Swap (s_i vs. r_i - 1):

Under swapping (d_i, b_i) ↔ (b_i, d_i) within seed i, r_i - 1 maps to (1/r_i) − 1, which is not antisymmetric around zero and inflates false positives severely under skewed/lognormal rates (0.159, 0.365, and 0.579 on the actual code at σ ∈ {0.5, 1.0, 1.5}, closely reproducing Reviewer 1's 0.150, 0.361, 0.563 and reaching up to 56% in lognormal null checks).

By contrast, the normalized difference

s_i = (d_i − b_i) / (d_i + b_i)

satisfies s_i(b_i, d_i) = −s_i(d_i, b_i) identically. Under the sharp null that (d_i, b_i) are exchangeable within each seed, sign-flipping s_i produces an exact null distribution without distorting ratio asymmetry.

Boundary Behavior & Removal of Zero-Denominator Guard:

When d_i = 0 and b_i > 0, s_i = −1 (preserving full-suppression sensitivity).

When d_i = b_i = 0 (both zero), defining s_i = 0 keeps the seed cleanly in the test without division by zero or ad-hoc exclusion rules, making the old zero-denominator exclusion guard unnecessary.

Preserved Scope: Only the test statistic feeding the p-value for the suppression-ratio family member changes; the registered suppression ratio endpoint, its bootstrap CI, TOST equivalence rules, and the claim rule remain unchanged.

Sharp-Null Exchangeability Wording:

Stating the sharp null (within-seed exchangeability of the paired values) explicitly and noting that symmetry around zero follows from that exchangeability—rather than treating sign-symmetry as an ungrounded extra assumption—is statistically clean and transparent.

2) Verification of Synthetic Null Check & Seed Disjointness

Synthetic Null & Power Check (work/part5_permutation_test.py, SHA-256 825e5157f102d248b2cefd24fbbf083a506ea3b29e41c7113ea8fd6e64a006da; output work/part5_synthetic_null_check_output.txt, SHA-256 df214b60c4138657c958900523f39c9c25c35087a104c182d91529086501b505):

At α = 0.05 (B = 10,000 permutations, PCG64 seed 987654321, 1,000 simulations per null case), both the normal-rate null (per-member 0.041–0.061, family-wise 0.060) and the skewed/zero-containing lognormal null (per-member 0.040–0.065, family-wise 0.056) fall well within the pre-registered 0.05 ± 0.021 pass band, while the 500-trial known-effect check achieves 0.982–1.000 per-member and 1.000 family-wise power.

The diagnostic comparison confirms mean(s_i) holds nominal type-I error (0.044, 0.045, 0.048) where mean(r_i - 1) inflates (0.159, 0.365, 0.579).

Seed Disjointness (work/part5_seed_disjointness_check.py, SHA-256 61dc7c461b52471b40ddaf2cfcd474eff113a91b6f9f80bc6f20c14af14df5f8; output work/part5_seed_disjointness_output.txt, SHA-256 95b11e84dda7b3118b50cdfb67470ecf94f0789873be3a24042c31b2a8d802c0):

Restricting the control-selection sub-seed stream to 5701–5799 (with fallback to §8.1 if exhausted) keeps it cleanly below arm (e) starting at 5800, and PASS across 35 blocks (990 seeds, all pairwise disjoint) is verified.

3) Remaining Elements Confirmed

Seed-stratified label permutation (1 targeted vs. 5 controls within each of the 20 shared seeds 5200–5219), plus-one permutation p-value formula (1 + count) / (B + 1), edge-case handling, per-test exchangeability statements, descriptive treatment of the frozen-vs.-refit gap (with bootstrap CIs and TOST as a separate inferential route under registered rules), Holm family (m = 9, seeds 6000–6008), and the implementation specification all stand confirmed.

My CONFIRM applies to the amendment as now drafted for application to PART5-PREREG.md. (As always, I cannot modify files directly in this chat, so please paste this confirmation into your panel/ gate log.)

### Verbatim Reply C, first reply: Reviewer 3, final confirmation on the rung results gate (24 Nov 2026, evening)

Reviewer 3 — final confirmation: Part 3 Rung 2 Results HARD gate
PASS

I confirm that the amended wording lifts my REQUIRE CHANGES objection. Reviewer 3's vote is now PASS for the four-conditions rung results gate.

The decisive improvement is that the report no longer misrepresents the registered bootstrap quantity as a conventional null-distribution p-value. It preserves the analysis actually preregistered and executed, while making its statistical meaning and limitations explicit.

Assessment of the amendments

1. Registered bootstrap procedure — accepted with the qualification. The table now identifies bootstrap tail fractions, not p-values. It also distinguishes the nominal Holm adjustment from guaranteed family-wise error control. This resolves my central objection: readers are no longer invited to interpret an uncentred bootstrap tail calculation as a calibrated null test.

2. The revised numerical bounds — accepted as reporting conventions. The 2/(B+1) and 12/(B+1) figures are explicitly identified as add-one reporting conventions for this bootstrap calculation, not as evidence that the underlying null p-value has been bounded. That distinction must remain visible wherever these numbers are repeated.

3. Methodological disclosure — accepted. The report accurately records that the frozen procedure was executed as written, and that the limitation concerns the interpretation of its output, not an undocumented departure from the preregistration.

4. Supplementary permutation check — accepted as post-hoc corroboration. The plus-one Monte Carlo calculation, separate seed, script and artefact are disclosed. Its results agree with the registered claims. It does not replace or retroactively modify the registered analysis, which is the correct treatment.

5. Exact-permutation note — accepted with its stated scope. Given the reported complete separation of the 30 observations in each group, the exact two-sided permutation probability 2/C(60,30) is consistent with the stated exchangeability-based comparison. This is useful supplementary evidence, not a conversion of the original bootstrap tail fractions into null p-values.

One boundary I want preserved

The report must not later shorten its conclusion to “six Holm-significant differences” or “Holm-controlled significance.” Its accurate conclusion is:

Six differences satisfy the registered claim rule.

The reported bootstrap tail fractions and their nominal Holm adjustment are not calibrated null-distribution p-values or guaranteed family-wise error control.

The separate post-hoc permutation analysis provides additional corroboration, but remains post-hoc and non-governing.

The confidence intervals and the supplementary permutation results support the substantive direction of the observed model differences. None of this establishes biological validity, causal connectome contribution, or validation of the sensory encoder.

Final disposition

Gate component — Reviewer 3
Freeze and execution provenance — Accepted on supplied documentary evidence
Anchor — PASS
MN9 endpoints and suppression classification — Accepted within registered scope
Six registered comparisons — Accepted under the explicitly qualified registered rule
Sensitivity and bilateral conditions — Accepted as non-confirmatory/descriptive
Statistical qualification and disclosures — Accepted
Part 3 Rung 2 Results HARD gate — PASS

I withdraw the outstanding REQUIRE CHANGES and cast PASS.

This closes Reviewer 3's objection and supports certification of the Part 7 prerequisite on this rung's side, consistent with Reviewer 1's ruling. It does not substitute for the owner's sign-off or the remaining panel process.

The human expert check remains owed at the Part 8 final gate.

### Verbatim Reply C, second reply: Reviewer 3, re-confirmation of the Part 5 permutation amendment (24 Nov 2026, evening)

Reviewer 3 — re-confirmation of the Part 5 permutation amendment
ACCEPT — UPDATED DRAFT

I re-confirm my approval of the amendment as now described. The replacement suppression statistic resolves the substantive objection I raised to the earlier draft. I have no further methodological change to require before the amendment is submitted for panel and owner approval.

The change is substantive, and I have assessed it as such rather than treating it as a minor implementation correction.

1. Replacement suppression statistic

I accept:

s_i = (d_i - b_i)/(d_i + b_i), T = (1/20) sum_{i=1}^{20} s_i.

The key property is the one the previous statistic lacked. Swapping the two arms within a seed gives:

s_i(b_i, d_i) = -s_i(d_i, b_i).

Under the stated sharp null of within-seed exchangeability, the sign-flip transformation is therefore justified, subject to the independence of the paired seed units and the permitted within-pair swaps.

This is materially better than r_i - 1, whose sign and magnitude do not transform symmetrically under arm exchange.

The zero-rate handling is also correct:

d_i = 0, b_i > 0 gives s_i = -1.

d_i = b_i = 0 gives s_i = 0.

Both cases remain in the analysis.

Removing the zero-denominator exclusion guard is therefore appropriate for this statistic. It avoids dropping observations that may carry important suppression information.

The registered suppression ratio, its confidence interval and its decision rule remain unchanged. The amendment changes the test statistic for the permutation member, not the estimand or the substantive suppression endpoint. That distinction should remain explicit in the frozen document.

2. Synthetic null validation
Reported criteria pass

The diagnostic is particularly useful because it tests the actual analysis code under the stated design rather than validating an abstract description of the method.

The results support the change:

Diagnostic — Earlier r_i - 1 — Replacement s_i
Lognormal null, sigma = 0.5 — 0.159 — 0.044
Lognormal null, sigma = 1.0 — 0.365 — 0.045
Lognormal null, sigma = 1.5 — 0.579 — 0.048

The replacement's per-member false-positive rates and reported family-wise rates also fall within the stated tolerance under both normal and lognormal null cases. The known-effect rejection rates are encouraging.

I accept this as a successful implementation diagnostic against the preregistered simulation criterion. It does not prove exact calibration for every possible data-generating process, but it supplies relevant empirical evidence for the intended design.

One qualification should remain in the report: the synthetic validation supports the stated null scenarios and design; it does not establish universal robustness to arbitrary dependence or departures from within-seed exchangeability.

3. Seed-stratified label permutation

My earlier ruling required restricted permutation within the 20 shared-seed strata. The updated draft retains that design.

I confirm that the pooled-control comparison should preserve each six-observation seed stratum and reassign one targeted label within that stratum. This respects the matched structure rather than treating all 120 observations as freely exchangeable.

No further change is required on this point, provided the frozen implementation actually enforces the restriction for every permutation.

4. Control-selection seed stream

The revised allocation also resolves my earlier concern:

The shared control-selection sub-seed stream is restricted to 5701–5799.

It is consumed in a specified order across both lesions.

It ends before arm (e)'s block begins at 5800.

The registered fallback applies if the stream is exhausted.

The reported disjointness check covers 35 blocks and 990 seeds, with all pairwise comparisons passing. This is an acceptable allocation rule.

5. Remaining design elements

I retain my earlier approval of the following:

Plus-one Monte Carlo permutation p-values.

The stated exchangeability rationale for each test family member.

Conventional Holm step-down with fixed family size m = 9, fixed order and permutation seeds 6000–6008.

The seed-restricted label permutation.

Descriptive-only treatment of the frozen-versus-refit gap where no registered difference test applies.

TOST only as its own separately specified inferential equivalence procedure, not as a substitute for an absent difference test.

Bootstrap intervals retained for estimation, distinct from the permutation tests used for hypothesis testing.

The family membership, endpoints, thresholds and experimental seed allocations remain unchanged as described.

Final ruling

Amendment element — Reviewer 3
Replace r_i - 1 with s_i — Accept
Sign-flip justification under sharp null — Accept
Zero-rate handling — Accept
Synthetic null diagnostic — Pass on reported criteria
Seed-stratified label permutation — Accept
Control-selection seed stream — Accept
Holm family and reserved permutation seeds — Accept
Frozen-versus-refit treatment — Accept with stated inferential boundary

Reviewer 3 verdict: ACCEPT — UPDATED DRAFT.

The earlier approval is superseded by this ruling. I approve the revised statistical construction for submission to the full panel and owner, before it is applied to the preregistration.

This is approval of the amendment's methodological design, not permission to execute it before the required approval and freeze. It is also not a Part 5 execution-gate PASS. I have assessed the supplied description and reported diagnostics; I have not independently executed the scripts or verified the supplied file hashes.

### Record note on the amendment's seed-stream versions (24 Nov 2026)

For the record, stated plainly: Reviewer 2's CONFIRM (Verbatim Reply B) and Reviewer 3's ACCEPT (Verbatim Reply C, second reply) were given on the amendment as then drafted, whose control-selection sub-seed stream was the shared stream restricted to 5701-5799, drawn in order across both lesions. The per-lesion refinement (5701-5749 for L-MN9, 5750-5799 for L-GRN, each lesion falling back within its own stream) was applied afterwards, at Reviewer 1's requirement in Verbatim Reply A, and is recorded in the entry above on the per-lesion fix and the re-run checks. Reviewer 1's confirmation of that per-lesion sentence was sent to him tonight (the message at `work/r1_substream_confirmation_message.md`, carrying the amended sentence and the re-run disjointness output, nothing else) and is pending. The amendment itself has not been applied to `docs/closed_loop_preregistration.md`; it goes to the owner for approval first.

### GATE CLOSED: four-conditions rung results gate (24 Nov 2026)

- **Panel: 3 of 3 PASS.** Reviewer 1 PASS stands (his three required items are in the report). Reviewer 2 PASS stands (his ruling on the panel question is recorded above; his re-confirmation of the Part 5 amendment is Verbatim Reply B). Reviewer 3 withdrew his REQUIRE CHANGES and cast PASS tonight (Verbatim Reply C, first reply).
- **Owner sign-off: Angelic Charles, 24 Nov 2026, 22:11 WAT** ("Yes, sign off and close the rung gate").
- **GATE CLOSED.** The "gate pending" label in `docs/taste_conditions_results.md` is replaced by a dated closure note (§13 item 17 of the report, with the status line updated); no results text was altered. The report's post-closure SHA-256 is `d121fcf855f1a8e8ac6c5221507a4fe8f4f93d11b3f1a5e21c27ad9df597362b` (the pre-closure locked hash was `54c8dccda026afb259fa64b0b44e7ec052859b892e8bbfa429881b6ef689cd2f`).
- **The Part 7 prerequisite (§8.4) is discharged.** Reviewer 1 certified it conditional on his items being in the report, which they are; Reviewer 2 certified it in his ruling; Reviewer 3's PASS supports certification on this rung's side, consistent with Reviewer 1's ruling.
- **Reviewer 3's boundary, recorded with the closure:** the report's conclusion must never be shortened to "six Holm-significant differences" or "Holm-controlled significance". The accurate conclusion is "six differences satisfy the registered claim rule". The reported bootstrap tail fractions and their nominal Holm adjustment are not calibrated null-distribution p-values or guaranteed family-wise error control. The separate post-hoc permutation analysis provides additional corroboration, but remains post-hoc and non-governing.
- The human expert check remains owed at the Part 8 final gate.


### Part 5 p-value amendment: Reviewer 1's final confirmation (24 Nov 2026, night)

Reviewer 1's reply to the sub-stream confirmation message (the amended per-lesion sentence, the re-run disjointness output and the 5,000-simulation figures), verbatim:

---

Reviewer 1: change 3 and the re-run

Change 3 is satisfied, and so are all three required changes. The amendment can go to the owner. I checked the text and the new output against my ruling. I haven’t re-run the code or the script.

Change 3: confirmed

- Per-lesion streams. 5701–5749 for L-MN9 and 5750–5799 for L-GRN are fixed in advance, order-independent, and each ends below arm (e)’s block at 5800. The fallback works within each lesion’s own stream, so one lesion can no longer starve the other. §8.1’s generation sentence is amended to match.
- Arithmetic. 49 + 50 = 99 seeds, the same as the earlier shared stream. 990 + 3 new bootstrap-seed blocks = 993 total seeds. 35 − 1 + 2 + 3 = 39 blocks. The union equals the total (993), so all blocks are disjoint.
- Coverage. The rung’s bootstrap seeds 20261128, 20261129 and 20261130 are now listed. The manifest scan found 342 distinct seeds across 63 JSON files, all inside listed blocks and none in the permutation block. That closes my coverage items.

Change 2, re-run: confirmed

- Per-member criterion. At n = 5,000 the standard error is 0.0031, so ±0.009 is about three standard errors, and I confirm that arithmetic. All 18 null cells fall within [0.041, 0.059]. The extremes are 0.046 and 0.055 (normal) and 0.047 and 0.054 (lognormal).
- Family-wise. 261/5000 and 213/5000 sum to 474/10000 = 0.0474. That is under the one-sided bound of 0.059, and consistent with Holm being conservative. The earlier family-wise figures (0.060 and 0.056) were sampling noise, as I suspected.
- Power and self-tests. Power is 0.986 to 1.000 on all members, and the self-tests pass.

What the record must say

1. The code hash changed. The code’s SHA-256 is now 32ab7eab…. The earlier run cited 825e5157…. Say so, say what changed (the one-sided family-wise criterion, the larger simulation count, the pooled figure), and keep the first run as superseded, not deleted. Note that the criterion was revised after seeing the first run, at my suggestion.
2. Fresh hashes. The amendment must cite the new output file’s SHA-256 and the new disjointness script and output hashes. You’ve given the code hash only for the synthetic check, and the seed script has changed too.
3. The diagnostic table. In this run the mean of s_i gives 0.058 / 0.063 / 0.050 at 1,000 simulations each, a little above the earlier 0.044 / 0.045 / 0.048. That is compatible with sampling noise (one standard error is about 0.007) and sits outside the pass criterion. The registered member itself ran at n = 5,000 with 0.055 and 0.050. Don’t interpret the diagnostic row beyond showing that r − 1 fails and s_i doesn’t.
4. Stream sizes. The two streams have 49 and 50 sub-seeds. Say so in the text, and that exhaustion is the binding limit.
5. The amendment-history entry. It still says the two pairing questions were “flagged to the panel rather than settled”. Both are now resolved, so update it.

Sequence from here

1. The owner approves the amendment.
2. Apply it to docs/closed_loop_preregistration.md and re-hash.
3. Re-run the disjointness script and the synthetic check against the applied text.
4. Tag only after that. Do not create part5-prereg-v1 before the owner’s approval is recorded.

I don’t need to see anything else from this thread. If any text changes in the application step beyond what’s listed, send me only the changed passages.

---

With this reply the amendment is panel-complete: Reviewer 1 CONFIRM (all three required changes satisfied, including the per-lesion sub-stream sentence), Reviewer 2 CONFIRM and re-CONFIRM on the statistic change, Reviewer 3 ACCEPT and re-ACCEPT on the statistic change. Reviewer 2's and Reviewer 3's confirmations were given on the shared-stream seed version; the per-lesion refinement followed at Reviewer 1's requirement and is confirmed by him above.

### Owner approval of the Part 5 p-value amendment (24 Nov 2026, 22:24 WAT)

Angelic Charles approved the amendment tonight ("Yes, approve the Part 5 amendment", 22:24 WAT). Reviewer 1's prescribed sequence governs from here: (1) this approval recorded; (2) the amendment applied to `docs/closed_loop_preregistration.md` as a formal pre-freeze amendment pass and the document re-hashed; (3) the seed-disjointness script and the synthetic null check re-run against the applied text; (4) the freeze executed under section 14 and the tag `part5-prereg-v1` created only after all of that. No tag existed before this approval was recorded.

### Reviewer 1 on the Part 5 freeze record (24 Nov 2026, night; verbatim)

Reviewer 1: the application-step change

I have no objection to the change.

Replacing “flagged here for editorial correction at the freeze” with “corrected in this same amendment pass” is a faithful description of what happened, and it closes the §7 sentence cleanly. The same pass applied both the amendment and the editorial correction, so there is no longer a deferred fix hanging over the frozen text.

I haven’t seen the tag or the applied document, so everything below is a request for the freeze record, not a confirmation of it.

What the freeze record should hold

1. The tag and its content. The commit hash that part5-prereg-v1 points to, and the SHA-256 of docs/closed_loop_preregistration.md at that commit.
2. Owner approval before the tag. The amendment’s approval by Angelic, with its timestamp, recorded as earlier than the tag. The sequence we agreed was approval, application, re-run of the two checks, then tag.
3. Both checks re-run against the applied text. The synthetic-null check and the seed-disjointness script, each with its output file and SHA-256. The applied document’s streams and blocks are what the script’s lists should be compared against, so check that the script’s lists match the document as it now reads, not only the draft.
4. The amendment-history entry updated to say the two pairing questions were resolved, with the per-lesion sub-streams, the s_i statistic and the synthetic check recorded. Keep the superseded first synthetic run on record, with its code hash.
5. Waiver and expert check. The waiver text as signed, and the statement that the human check is owed at Part 8. I’d still recommend asking for it before the first confirmatory evaluation in Part 7.

Standing conditions for what follows

• No further edits to the frozen document without a formal amendment. That includes the editorial change just described, now that the tag exists: record it in the history as an editorial correction applied before the tag.
• Calibration seeds and evaluation seeds stay separate, as registered, and no evaluation data are inspected before the analysis code is frozen and hashed.
• Report all registered outcomes, including nulls and arms that disagree with the primary, in the registered wording.

If any of items 1–4 cannot be shown, tell me which. Otherwise I have nothing further on this thread.

### Verification of the freeze record against Reviewer 1's requests (24 Nov 2026, night)

Each item in Reviewer 1's reply above was checked against `docs/closed_loop_freeze.md`, the frozen preregistration as it stands at the tag, the decisions log and the check artefacts on disk. Outcome per item:

1. **Tag and content: SHOWN.** The freeze record's dated note records the freeze commit `b88520be5a7a652a7c96e4203347c5d4411ed38b`, and the tag `part5-prereg-v1` points at that commit (verified). Item 1 of the freeze record states the preregistration's SHA-256 as `81191895af32ce3dfbf17e556579c4de5cfdb8a4236447aa1d0088895b237a00`; hashing the file as it stands at the tag gives exactly that value.
2. **Owner approval before the tag: SHOWN.** The freeze record (item 1) and `decisions_log.md` both record the approval of the amendment by Angelic Charles on 24 Nov 2026 at 22:24 WAT. The tag's tagger timestamp is 24 Nov 2026, 22:07:51 UTC, which is 23:07:51 WAT, so the approval precedes the tag, in the agreed sequence of approval, application, re-run of the two checks, then tag.
3. **Both checks re-run against the applied text: SHOWN, no mismatch.** The freeze record cites the disjointness script (SHA-256 `d84798f2c586738df5f5478810fdc92c0e3ccda51beaff697f65deb09b1793f2`), its applied-text output (`d19241b15e7a23dc7bfcb1b7694dbc7ba0d452b7d52457caef647b5d0ab366bc`), the synthetic check code (`32ab7eab49db97b2611255a1b44c6b5e2818eb0e515fc8fc97b7bc0d961eaaef`) and its applied-text output (`761b1234d0b326a48bc4a24f7e4addfce4d56b1abbd65e94c62ce8375bd3bc2b`); all four hashes were verified against the files on disk, and both outputs record PASS (disjointness: 39 blocks, 993 seeds, all pairwise disjoint, manifest scan clean; synthetic: per-member 0.046 to 0.055 and 0.047 to 0.054, pooled family-wise 0.0474). The script parses the Part 5 seed table out of the document itself and fails loudly if the parsed blocks differ from its canonical list; the document it parses is byte-identical to the document at the tag (same SHA-256 as item 1 above), and its parsed blocks match the applied table exactly: 5000-5009; 5100-5119 excluding 5103, plus 5120; 5800-5819; 5103; 5200-5219; 5300-5319; 5400-5519; 5699; 5700; 6000-6099, with the permutation block now taken from the document's own table, as the freeze record describes. The script's two sub-seed stream blocks (5701-5749 for L-MN9, 5750-5799 for L-GRN) match the applied document's section 7 text. One wording slip in the script's own header comment, recorded for accuracy: it says each stream holds 49 sub-seeds, where the L-GRN stream holds 50; the block lists the script actually checks are correct, and the preregistration states 49 and 50 correctly.
4. **Amendment-history entry: SHOWN.** The entry records the two pairing questions as resolved, not merely flagged; the per-lesion sub-streams with their sizes (49 and 50); the s_i statistic and why it replaced the draft's first statistic; and the validation record keeps the superseded first synthetic run on record with its code hash (`825e5157f102d248b2cefd24fbbf083a506ea3b29e41c7113ea8fd6e64a006da`), marked superseded, not deleted, with the reason for the change (the one-sided family-wise criterion, the larger simulation count, the pooled figure) stated.
5. **Waiver and expert check: SHOWN.** Item 6 of the freeze record carries the waiver text as signed and states that the human expert check remains owed at the Part 8 final gate.

No item was missing, so no addendum to the freeze record was needed. Reviewer 1's standing conditions, and his recommendation to seek the human check before Part 7's first confirmatory evaluation, stand as recorded in his reply above.

### Reviewer 1: acceptance of the Part 5 freeze record (24 Nov 2026, night; verbatim)

Reviewer 1: freeze record

I accept the freeze record as shown.

Items 1 to 5 are present as described. I’m relying on your report of the record, since I haven’t seen the file.

- Sequence. Approval at 22:24 WAT and the tag at 23:07:51 WAT are 43 minutes 51 seconds apart, which matches the “about 44 minutes” in your note. Approval came first, as agreed.
- Hash check. Re-hashing the document at the tag and getting exactly the recorded SHA-256 is the check I wanted.
- Applied-text checks. The seed script parses the seed table out of the applied document and fails if its canonical list differs. The sub-seed blocks match the §7 text (5701–5749 and 5750–5799), so the check does not depend on my reading of the draft. 39 blocks and 993 seeds match what I confirmed earlier, and the pooled family-wise figure of 0.0474 matches.
- Superseded run and history entry. The earlier synthetic run stays on record with code hash 825e5157, and the amendment history records the per-lesion streams, the s_i statistic and the resolved questions.
- Waiver. The waiver text is in the record, and the human check is stated as owed at Part 8.

The script’s header comment

I agree with leaving the script untouched so its recorded hash stands. The comment says 49 sub-seeds per stream where the L-GRN stream holds 50, which affects nothing the script checks. Put the same note in the freeze record, next to the script’s hash, and not only in the gate log. A future reader who opens the script will see the discrepancy before the log.

Standing items

- The human check before Part 7. My earlier recommendation stands: seek it before the first confirmatory evaluation episode, when outcomes first become visible. The waiver covers the freeze, not a later decision to skip it.
- No edits to the frozen document without a formal amendment, as before.

I have nothing further on this gate. For future rounds, send results with their hashes and I’ll check them against the registered rules.

## Part 5 characterisation results gate (25 Nov 2026)

The characterisation results (report `docs/closed_loop_characterisation_results.md`, original SHA-256 `285488efcd685a59dfdd6c08dd368ca0063433214d53146a81e6ab0ce625dce2`; audit artefact `results/closed_loop/characterisation_analysis_audit.json`, original SHA-256 `ec28f5871bfbcc981d1e8706828b60a01c31a59df2dd3e39913921e69332ba4c`; commit 4dea348; freeze tag part5-prereg-v1) went to the full panel as a HARD gate. Reviewer 2 returned PASS with no required changes. Reviewer 1 returned PASS conditional on report items, including one recomputation. Reviewer 3 returned REQUIRE CHANGES on one material point: endpoint reconciliation. The three replies follow verbatim. The reconciliation they required is recorded as section 9 of the results report and in the audit artefact's `reconciliation_2026_11_25` entry (updated audit SHA-256 `4115c963b46823bece0ca898cea1d16a1a7afab18617878fa66e71ebfe662222`; updated report SHA-256 `c671f8130e823b5caf91e865ca3f8aa362638c679aa69c22ea6cff261d22dca7`). The gate stays open pending Reviewer 3's re-review of the reconciliation and Reviewer 1's recomputation from the per-seed artefact.

### Reviewer 2: characterisation results gate (25 Nov 2026; verbatim)

Part 5 Characterisation Results Gate (docs/closed_loop_characterisation_results.md) — Reviewer 2 Verdict Recorded (PASS)

Reviewer: Reviewer 2 (Gemini)

Subject: HARD-gate review of Part 5 closed-loop characterisation results (docs/closed_loop_characterisation_results.md, SHA-256 285488efcd685a59dfdd6c08dd368ca0063433214d53146a81e6ab0ce625dce2; audit artefact results/closed_loop/characterisation_analysis_audit.json, SHA-256 ec28f5871bfbcc981d1e8706828b60a01c31a59df2dd3e39913921e69332ba4c; commit 4dea348, freeze tag part5-prereg-v1)

Verdict: PASS — No required changes, no blockers, no re-run required. Logged as delegated under Angelic Charles's authority/delegation (subject to ratification).

1) Verification of Ledger, Provenance & Headline Findings

Provenance & Ledger Hygiene:

All 100 characterisation episodes (5 arms × 20 episodes) verified against the ledger before computation, using registered disjoint seed blocks (5100–5119 \ {5103} ∪ {5120} across arms (a)–(d); 5800–5819 for arm (e)), matching frozen analysis hash, passing synthetic self-test, recording r_hi = 172.64875034982174 Hz (≤ 184.2 Hz threshold clearance bound, > 15 Hz rejection bound) and r_lo = 5 Hz in every manifest, logging the single environmental two-attempt episode (arm (c), seed 5107, service restart, same seed), and recording 0/100 settle-invalid episodes (M7 satisfied).

Core Closed-Loop Demonstration ((a) vs. (b) vs. (c)):

Arm (a) (Closed-Loop Sugar): Peak E = 2.043 rad [2.032, 2.051], mean E = 1.793 rad [1.706, 1.844], MN9 L 92.60 Hz / R 60.97 Hz (inside M4), 20/20 contact, 20/20 ignition (§6 item 8), and sustained closed-loop contact after the scripted ignition window closed (chunks 20–59).

Arm (b) (Open-Loop Sugar): Peak E = 2.030 rad [2.016, 2.043], MN9 L 94.88 Hz / R 62.39 Hz, 20/20 contact during the 0–59 stimulus window followed by complete extension offset across all 20/20 episodes once the scripted window closed—reproducing the Part 2b causal contrast cleanly in the feeding loop.

Arm (c) (No-Drive Control): Identically 0 on every measure across all 20 episodes (0 false positives).

Arm (d) (Sugar + Bitter, OUTSIDE THE VALIDATED ENVELOPE): Pooled suppression ratio 0.121 [0.116, 0.127] (L 0.097 [0.091, 0.103], R 0.158 [0.151, 0.166]), peak E = 0.344 rad, 20/20 extension onset, 0/20 food contact—matching the §10 advance prediction cleanly (r_filt suppressed below the ~0.837 contact-reach threshold).

Arm (e) (OUTSIDE THE VALIDATED ENVELOPE, Descriptive): Bilateral sugar (L 10 + R 21 @ 200 Hz) yields peak E = 2.056 rad, MN9 L 93.29 Hz / R 66.38 Hz, 20/20 contact, reported strictly descriptively without pooling or RQ-C5 asymmetry claims.

Permutation & TOST Inference: (a) vs. (c) on peak E and mean E, and (d) vs. (b) suppression on s_i (mean s_i = −0.784), sit at the exact Monte Carlo floor p = 1/10,001 ≈ 9.999 × 10^-5. (a) vs. (b) peak E (Δ = +0.013 rad [−0.003, 0.028], p = 0.1454) and contact duration (Δ = −0.130 s [−0.390, 0.000], p = 1.0) satisfy TOST equivalence within the pre-registered bounds using only permitted equivalence wording.

2) Rulings on Items 1 to 3

Item 1 — Deferred Holm Adjustment Across the Full Family of Nine (m = 9)

Ruling: APPROVED AS RECORDED — Yes, reporting null for Holm-adjusted p-values in this interim characterisation report with the explicit reason in the audit artefact is the exact right treatment, and this results gate CAN close with the full 9-member Holm adjustment deferred until Part 7 completes.

Rationale:

The preregistered amendment fixes Holm step-down across the single confirmatory family of m = 9 in fixed order (members 1–5 from Part 5 characterisation, seeds 6000–6004; members 6–9 from Part 7 lesions, seeds 6005–6008). Because Holm step-down sorting depends on all 9 raw p-values simultaneously, computing an interim 5-member Holm adjustment would violate the pre-registered m = 9 family correction.

Recording raw permutation p-values and extreme counts now, setting adjusted p-values to null with explicit audit provenance, and deferring any confirmatory Holm-adjusted claim language for members 1–5 until all 9 p-values are combined in the final freeze synthesis (§11) preserves strict family-wise error control without blocking the Part 5 characterisation gate. (Note: even under the worst-case multiplier m = 9, the three floor results at 1/10,001 ≈ 1.0 × 10^-4 will yield p_Holm ≤ 9/10,001 ≈ 9.0 × 10^-4 ≪ 0.05, while (a) vs. (b) peak E and contact duration are non-significant on raw p and evaluated via TOST equivalence.)

Item 2 — Materiality Band M3 Discrepancy (2.030 rad vs. [2.0746, 2.2746] rad)

Ruling: ACCEPTED AS A RECORDED DISCREPANCY (DIAGNOSED, NOT A GATE BLOCKER OR RETUNING TRIGGER).

Physical Reading of the Discrepancy:

Why Arm (b) Sits Below E_max = 2.1746 rad (Δ = -0.1446 rad): E_max = 2.1746 rad was measured in Q3 under saturating command (e = 1.0, requiring r_filt ≥ r_hi = 172.65 Hz). In arm (b), the intact brain's steady pooled MN9 firing rate under 200 Hz right-sugar drive is 94.88 + 62.39 = 157.27 Hz (matching Part 3's 154.97 Hz within M4). Because r_hi was calibrated as the 95th percentile of per-chunk filtered rates (172.65 Hz), the mean steady rate (157.27 Hz) sits below r_hi by design (§4 threshold arithmetic), producing a steady-state normalized drive of:

e_steady ≈ (157.27 − 5.0) / (172.65 − 5.0) = 152.27 / 167.65 ≈ 0.908

Exact Quantitative Reconciliation: At e ≈ 0.908, the rostrum and haustellum pitch joints are already saturated (e ≥ 0.80–0.825 from the Pass 6 reach curve), leaving only the labrum pitch joint (0.2625 rad full-scale contribution) scaling linearly with e: the unsaturated labrum shortfall (1 − 0.908) × 0.2625 ≈ 0.024 rad plus the ~0.08–0.10 rad dynamic tracking lag (M2 mean -0.091 rad, with 8/20 episodes slightly below -0.10 rad from Poisson spike variability) accounts for the ~0.145 rad gap between 2.1746 rad and 2.030 rad.

Scientific Consequence: Crucially, e_steady ≈ 0.908 still clears the contact-onset fraction (0.8371 ± 0.05) comfortably, which is why 20/20 episodes achieved contact in both (a) and (b). Recording M3 openly as a discrepancy without adjusting any band, constant, or seed follows the §13 / M1–M7 preamble rule to the letter.

Item 3 — Code-vs.-§6 Field Divergences (contact_onset_fraction and ignition)

Ruling: ACCEPTABLE AS HANDLED — Recording both the frozen-code fields and the §6 definitions transparently without silently altering frozen code or data is the right resolution.

Rationale:

contact_onset_fraction (M1): Computing the §6 item 6 definition directly from the raw episode logs for M1 while keeping the frozen code's contact_onset_fraction field (stimulus-event fraction) intact and documented avoids post-hoc modification of frozen code while ensuring M1 is evaluated on the exact quantity it was preregistered to check.

ignition (19/20 vs. 20/20, differing only on seed 5111): Reporting both the stricter frozen-code ignition field (19/20) and the §6 item 8 definition (20/20), and naming seed 5111 explicitly as the sole difference, prevents any selective reporting.

contact duration: Using the frozen code's endpoint for the primary (a) vs. (b) family comparison while reporting §6's full-episode duration alongside ensures the confirmatory statistic comes strictly from the frozen pipeline while giving readers complete visibility into the full-episode metric.

Gate Closure Summary

Verdict: PASS on docs/closed_loop_characterisation_results.md (commit 4dea348).

Next Step: Part 5 characterisation is closed; Part 7 lesion runs may proceed under part5-prereg-v1 (with the Part 3 four-conditions rung prerequisite already closed and certified), and the full 9-member Holm adjustment will be evaluated once Part 7 members 6005–6008 complete.

(Note: I do not have write access to your local filesystem in this chat, so please paste this PASS verdict and rulings 1–3 into your panel/ gate log alongside Reviewers 1 and 3.)

### Reviewer 1: characterisation results gate (25 Nov 2026; verbatim)

Reviewer 1: Part 5 characterisation results gate

Verdict: PASS, conditional on the report-text items below. None needs an episode re-run. I’m judging your summary, not docs/closed_loop_characterisation_results.md. One finding (the contact-duration p-value, in my extra points) needs a recomputation before I can close, and I’d treat that as a real condition.

Consistency checks on the summary
Suppression: s_i = (r − 1)/(r + 1). At r = 0.121 that gives −0.784, matching the reported mean s_i. The closed-loop ratio of 0.121 [0.116, 0.127] is close to the rung’s brain-only 0.126.
(a) vs (b): 2.043 − 2.030 = 0.013 ✓. 1453 extreme permutations give (1 + 1453)/10001 = 0.1454 ✓.
Contact thresholds: the registered r_hi of 172.65 Hz exceeds r_lo + 10 = 15 Hz. The measured pooled rates (about 153.6 Hz in (a), 157.3 Hz in (b)) clear the contact threshold of about 145 Hz, so contact in (a) and (b) fits. (d)’s peak E of 0.344 with pooled rate about 19.5 Hz sits far below it, so contact 0/20 fits.
(c): exactly zero everywhere matches the silent baseline from Part 3.
M3 band: 2.1746 ± 0.10 = [2.0746, 2.2746] ✓. The observed 2.030 is 0.045 below the lower edge and 0.145 below E_max.
Ruling 1: Holm

Not reporting Holm-adjusted values now is correct. Holm over only the five available members would use multipliers of 5 down to 1 instead of the registered 9 down to 1. That would be anti-conservative and unregistered.

A valid bound is available today. For any member, the registered Holm-adjusted p is at most min(1, 9·p). Each term of the running maximum is at most 9 times a p-value that is at most this member’s own. So:

the three members at the floor (p = 1/10001) have adjusted p ≤ 0.0009, far below 0.05, so they are claimed under the registered rule whatever the four lesion members turn out to be;
(a) vs (b) peak E (p = 0.1454) and contact duration (p = 1.0) are not claimed under any adjustment.

State this in the report as an upper bound labelled “Bonferroni-9 bound, not the registered adjusted value”. It settles the claim status of all five members. The gate can close with the exact adjusted values pending, on three conditions:

they are computed by the frozen code over all nine members at Part 7, with no change to the family or order;
they can only be at or below these bounds;
the audit artefact’s nulls carry the reason.

Also say that (a) vs (c) is a sanity check, not evidence. With no drive, every measure is exactly zero by construction, so its significance shows the loop is silent without drive and carries no other weight.

Ruling 2: the M3 discrepancy

My reading: M3’s expected value was mis-specified, and the result is explained by quantities already registered. It is not a body or brain failure.

E reaches E_max only when the filtered pooled rate reaches r_hi = 172.65 Hz. Under sugar the pooled steady rate is about 157 Hz in arm (b).
With the registered linear map, e_steady = (157.27 − 5)/167.65 ≈ 0.908, so E ≈ 1.975. A peak of 2.030 implies e_peak ≈ 0.934, a filtered rate of about 161 Hz, which is about 4 Hz above steady. That is ordinary fluctuation.
“Sustained full drive” in M3 should have meant “pooled rate at or above r_hi”, not “sugar present”. Sugar-only drive never gets there.

What the panel should do:

Record M3 as OUTSIDE with this explanation and adjust nothing, exactly as registered.
Verify the explanation from the logged e and rate series: confirm e_peak ≈ 0.93 and that E tracks e·E_max within M2’s band. If it holds, the discrepancy lies upstream of the body.
A related question for the calibration. r_hi is the 95th percentile of the filtered rate over calibration sugar-only episodes. In characterisation, the episode peaks of that same rate sit about 10 Hz below it. Compare the upper tail of the filtered-rate distribution in arm (a) with the calibration distribution. If the calibration set had a heavier tail (for example from onset transients or a different window length), say why. Nothing is adjusted, but Part 7 should know that intact arms saturate near e ≈ 0.93, not at 1.
M2: a mean of −0.091 with 8 of 20 episodes below −0.10 is a systematic negative offset, slightly beyond Q6’s recorded 0.08. Record it as a known dynamic offset (the table over-predicts achieved E by about 4%). In Part 7, treat E as a measured quantity, not as table-predicted.
Ruling 3: the code-versus-§6 divergences

The handling is acceptable in principle, with three conditions. Reporting both values and not resolving silently was right.

The registered text governs. Where the frozen code’s field disagrees with §6, the §6 definition defines the endpoint and the code’s field is reported as a sensitivity. For ignition: 20/20 under §6 item 8, and 19/20 under the code’s stricter rule (seed 5111). The contact-onset quantity M1 judges is the §6 one, which you computed from raw logs. That is correct.
The §6 quantity needs its own provenance. Computing it from raw logs is itself analysis code written after the freeze. Say so, hash the script, and show it implements §6 item 6 as written. Have a second person (or a second reviewer) check it independently.
Run the family contact-duration member on the §6 endpoint too. The frozen permutation code can take the raw-log-derived values as input, with no change to the code. Report both results. If they agree, there is nothing to resolve. If they disagree, the §6 endpoint governs and the discrepancy goes to the panel.

Also record the code-versus-text mismatch as a deviation, and fix the code fields by a hashed amendment before Part 7’s analysis freezes. Do not alter the characterisation code retroactively.

Extra points

1. A p-value that doesn’t look right (my condition). For contact duration, 10,000 of 10,000 permutations were extreme, giving p = 1.0, with an observed difference of −0.130 s and CI [−0.390, 0.000].

If the non-zero per-seed differences all had the same sign, the observed |sum| would be the largest possible and p would be tiny, not 1.
p = 1.0 is possible only with large differences of mixed sign that nearly cancel. The CI’s upper end of exactly 0.000 suggests many zero differences.
Please send the 20 per-seed differences (on both the frozen-code endpoint and the §6 one). I will recompute exactly by hand. If the two don’t reproduce, the gate does not close.

2. The closed-versus-open contrast has no family member. The substantive contrast between (a) and (b) is persistence: (a)’s gate is sustained after the window and (b)’s extension offsets in all 20. The family tests peak E, mean E and contact duration, none of which captures this. State it as the registered binary result (20/20 against 0/20) with the claim rule the preregistration gives for RQ-P3. If the registered rule doesn’t cover it, don’t upgrade it. Say plainly that the equivalence on peak E and contact duration means feedback does not change those endpoints.

3. TOST wording. Give the numerical bounds. ±25% of (a)’s peak E is about ±0.51 rad, which is generous, so the result should read “equivalent within ±25%”, not “no difference”.

4. Bilateral and sugar+bitter. They are outside the validated envelope and descriptive. Keep that label in the report’s wording.

To close

Send the 20 per-seed contact-duration differences for my recomputation, and the revised paragraphs for rulings 1–3 once written. Everything else I accept as described.

### Reviewer 3: characterisation results gate (25 Nov 2026; verbatim)

Reviewer 3 — Part 5 characterisation results HARD gate
REQUIRE CHANGES

The 100-episode execution and the transparency of the report are encouraging. I do not see a reason to reject the episode set or rerun the characterisation. However, I cannot close the results gate yet. The unresolved distinction between the frozen analysis fields and the preregistered endpoint definitions is material to what the reported results actually test.

My rulings follow.

1. Holm adjustment across the nine-member family

Ruling: ACCEPT the current treatment. The adjusted values should remain null.

The preregistration fixed a family of nine members, with the four lesion members unavailable until Part 7. Reporting adjusted values for only the five currently available members would either change the family or imply an adjustment that has not yet been performed over the registered family.

The report is right to:

Preserve the nine-member family and its fixed order.

Report the five available members' unadjusted permutation results.

Record adjusted values as null, with the reason.

Avoid describing any of those results as having passed the registered Holm-adjusted decision rule.

There is an important distinction between closing the Part 5 characterisation execution and closing the full nine-member inferential family. The former need not wait for Part 7; the latter does. Part 5 may report its results provisionally with adjustment pending, but no final confirmatory claim requiring the registered Holm decision may be made until all nine members exist and the full adjustment is calculated.

I would not treat the missing four members as failed tests, nor would I approve a partial-family Holm adjustment as a substitute.

2. M3 outside its materiality band

Ruling: ACCEPT the discrepancy as reported. It is not grounds for an automatic execution failure, but it must remain an explicit unresolved discrepancy.

Arm (b)'s mean peak E is 2.030 rad, below the registered band of [2.0746, 2.2746]. That is an actual miss against M3. It should not be described as approximately inside, explained away by the confidence interval, or corrected by changing the band.

The correct interpretation is:

M3 is outside.

The result is a discrepancy between the observed open-loop characterisation and the registered expectation.

No adjustment or post-hoc recalibration is warranted.

Any downstream interpretation that depends on the expected open-loop magnitude must account for this miss.

M2 is a different case. If its registered criterion is evaluated on the mean, then a mean deviation of −0.091 rad is inside the ±0.10 band. The fact that 8 of 20 episodes individually exceed −0.10 is useful distributional information, but it does not change the registered mean-based verdict. Report both facts; do not silently convert a mean-based materiality criterion into an episode-wise one.

M1, M4, M5 on the mean, and M7 being inside does not cancel M3. M6 being inapplicable is also not a pass or a failure.

I would carry M3 forward as a named limitation for interpretation, not demand a new run or an unregistered correction.

3. Divergence between frozen-code fields and Section 6 definitions

Ruling: REQUIRE CHANGES to the endpoint reconciliation before the results gate can pass.

I accept the decision to disclose the two divergences rather than silently resolve them. But disclosure alone does not establish that the registered endpoint was analysed.

There are two separate cases.

Contact onset fraction

The code's contact_onset_fraction field represents the stimulus-event fraction, whereas Section 6 item 6 defines a different quantity. Recomputing the Section 6 quantity from raw logs is the correct response.

The report must keep the two quantities separately named and state unambiguously which one is used for M1. Since you say the Section 6 quantity is what M1 judges, that is acceptable. The frozen-code field must not be presented as though it were the Section 6 endpoint.

Ignition

The frozen code's ignition field is stricter than Section 6 item 8, producing 19/20 rather than 20/20 for arm (a), with seed 5111 responsible for the difference.

Both values should remain visible. But the registered Section 6 definition must govern the registered ignition claim. The stricter code field can be retained as a separate implementation diagnostic; it cannot silently replace the preregistered definition.

Contact duration — the material issue

Here the report says the permutation-family member uses the frozen code's endpoint, while Section 6's full episode duration is reported alongside it.

That is not sufficient if the frozen-code endpoint and the Section 6 endpoint are different quantities. The fact that the analysis code is frozen does not give its field semantics priority over the preregistered endpoint definition. A frozen implementation can contain an endpoint-definition discrepancy; the freeze does not turn that discrepancy into a protocol amendment.

I therefore require:

An explicit mapping between the code's contact-duration field and the Section 6 definition, including whether they are genuinely the same endpoint or different estimands.

If they are different, the registered contact-duration permutation member must use the Section 6 endpoint, computed from the raw logs using the already frozen permutation procedure, family position, and reserved permutation seed.

The frozen-code endpoint may remain as a separately labelled diagnostic, but must not substitute for the registered endpoint.

The audit artefact and report must identify which endpoint supports each claim and which endpoint enters the nine-member family.

This does not authorise changing the endpoint definition, permutation method, or family. It requires the analysis to implement the endpoint already registered.

Final verdict

Item

Reviewer 3 ruling

1. Holm pending Part 7

Accept. Keep adjusted values null; no final family-level confirmatory decision until all nine members are available.

2. M3 outside

Accept as an explicit discrepancy; no adjustment or rerun.

3. Code/Section 6 divergences

Require endpoint reconciliation, particularly for the contact-duration permutation member.

Reviewer 3 verdict: REQUIRE CHANGES.

The outstanding work is an analysis/report reconciliation, not a request to repeat the 100 characterisation episodes. Preserve the existing frozen outputs, raw logs, report history and audit trail. Do not overwrite the original results or retroactively alter the freeze.

Once the registered contact-duration endpoint has been established and analysed correctly, and the ignition and onset fields are unambiguously labelled against their registered definitions, I am prepared to re-review the results gate. The Holm adjustment can remain pending Part 7 under the conditions above.

This is my Reviewer 3 vote, not a statement of panel majority or owner sign-off. I have reviewed the results and methodological details supplied in your message; I have not independently inspected the report, audit JSON, repository, or hashed files.

### Reviewer 1: characterisation reconciliation re-review (25 Nov 2026; verbatim)

Reviewer 1: characterisation reconciliation

Verdict: my conditions are discharged and my PASS stands for the gate. I recomputed everything that can be recomputed from the differences you sent. Two wording items remain for the report. I could not independently re-derive the differences from the raw logs.

Recomputation from the per-seed differences
Quantity	Your value	My recomputation
Frozen-code endpoint, mean	−0.130 s	−0.130 (19 zeros, one −2.6)
Frozen-code endpoint, exact sign-flip p	1.0	all 2²⁰ assignments extreme, so exactly 1.0
Frozen-code endpoint, 95% CI	[−0.390, 0.000]	[−0.390, 0.000]
§6 endpoint, mean difference	+3.490 s	+3.490 (sum 69.8)
§6 endpoint, 95% CI	[2.750, 3.910]	[2.755, 3.910] (different bootstrap seed)
§6 endpoint, 90% CI	[2.840, 3.900]	[2.845, 3.900]
§6 endpoint, exact sign-flip p	at the floor (0 of 10,000)	6/2²⁰ ≈ 5.7 × 10⁻⁶, so a Monte Carlo count of 0 is what to expect
TOST bound	±2.24875 s	25% of 8.995 = 2.24875 ✓
Peak E bound	±0.511 rad	25% of 2.043 = 0.511 ✓
The p = 1.0 is explained. With one non-zero difference, every sign assignment gives the same |sum|, so every permutation is extreme. That is the configuration I suspected, and the reconciliation to the §6 endpoint is right.
TOST on the §6 endpoint: the 90% CI [2.84, 3.90] lies wholly outside ±2.249, so equivalence is not demonstrated. The sentence superseding the earlier equivalence wording is correct.
The Bonferroni-9 bound (9/10,001 ≈ 0.0009) puts the contact-duration member with the three floor members, claimed under the registered rule. This keeps registered claims unchanged.
M3: I was wrong, and your log reading is right

I inferred e_peak ≈ 0.93 by assuming peak E tracks e·E_max. Your logs show e_peak ≈ 0.987 (the 170.8 Hz peak maps to e = 0.989 under the registered map). The rate does rise to the top of the map. 0.987 × 2.1746 − 2.030 = 0.116, matching your 0.117, so the shortfall is dynamic tracking in the body, not the rate. M3 stays OUTSIDE with nothing adjusted. M2’s mean offset of −0.091 rad (about 4%), with 8 of 20 episodes beyond −0.10, is larger than Q6’s recorded 0.08. That is the thin margin I flagged when the band was registered. Treat it as a known dynamic offset, as you’ve done, and have Part 7 measure E and not predict it.

Remaining items

1. Seed 5111 and the persistence wording.

The single negative difference (−2.7 s on the §6 endpoint, with contact “released early”) and the code’s stricter ignition field (19/20) are the same episode.
The report’s persistence statement (“gate-sustained ignition 20/20 in (a)”) must not be stronger than that episode supports. State the 19/20 versus 20/20 distinction beside the claim, with what the code’s rule requires that §6 item 8 doesn’t, and what happened in 5111.
Describe the 5111 time series (gate state, drive state, e) in the report as a descriptive note. A rare dropout in an intact closed loop affects the variance baseline Part 7 will compare lesions against.

2. The independence of the §6 derivation.

I recomputed the statistics from the differences, not the differences from the raw logs. My re-review is therefore not the independent check of the §6 endpoint.
What exists is the analysis script and a reconciliation script that agree on all 100 episodes. They may share an author. Say who wrote each, and have a reviewer who didn’t write either re-derive the §6 endpoints from the raw logs for at least the 20 arm (a)/(b) pairs. If you send me the raw ledger for those episodes, I’ll do it.
This does not change my verdict, but the registered claim now rests on that derivation, so it should be checked.
Smaller notes
Calibration tail. Your explanation (calibration scripted on throughout the window vs arm (a) gate-sustained with momentary drive-off chunks) is sufficient. Add a line telling Part 7 to expect intact arms to peak near e ≈ 0.99 and achieved E/E_max ≈ 0.93.
Contact-duration difference. It is almost constant across seeds (3.8–4.0 s, apart from two seeds). That is structural: the sustained loop keeps contact for the remainder of the episode, and the scripted window ends earlier in arm (b). Say so in the interpretation, so nobody reads it as a noisy effect estimate.
Wording. The headline reads “closed-loop contact lasted longer than open-loop by 3.49 s [2.75, 3.91] on the registered endpoint”, and not “the loop improves feeding”. The §11 permitted-conclusions wording governs.
Exact p-value. Add the exact 5.7 × 10⁻⁶ as a note beside the Monte Carlo floor. It doesn’t replace the registered value.

My PASS stands. If the 5111 description and the raw-log re-derivation come back consistent, I have nothing further on this gate.

### Reviewer 3: characterisation results re-review (25 Nov 2026; verbatim)

Reviewer 3 — Part 5 characterisation results re-review
PASS

Yes. The reconciliation discharges my REQUIRE CHANGES. My PASS now stands for the Part 5 characterisation results gate, with the nine-member Holm adjustment pending Part 7 under the conditions previously stated.

The decisive correction is that the registered contact-duration member now tests the actual Section 6 endpoint, rather than the frozen code's different, stimulus-window-only diagnostic.

1. Contact-duration endpoint — accepted

The distinction is now unambiguous:

Registered endpoint: taste-event ON time across chunks 0–99, with the longest continuous stretch also reported.

Implementation diagnostic: the same event totalled only over chunks 0–59.

Those are different estimands. The report no longer conflates them or allows the implementation diagnostic to substitute for the registered endpoint.

The corrected registered analysis uses the prescribed seed list, family position four, permutation seed 6003, B = 10,000, and the frozen permutation functions. The reported result is:

Arm (a): 8.995 s.

Arm (b): 5.505 s.

Paired difference: +3.490 s.

95% CI: [2.750, 3.910].

Permutation extreme count: 0; reported p = 1/(B+1).

The per-seed cross-check against the audit artefact is an important reconciliation control. The 19 positive differences and the one negative difference at seed 5111 are also consistent with the supplied explanation of the earlier diagnostic's result.

The corrected TOST result is handled properly: equivalence is not demonstrated for contact duration under the registered bound. Superseding the earlier equivalence sentence is necessary and correct. Peak-E equivalence remains a separate result and is not affected by this correction.

The old code-field result remains useful as an implementation diagnostic, but it does not enter the registered family. Accepted.

2. Onset and ignition — accepted

The reconciliation now explicitly distinguishes:

Section 6's registered contact-onset fraction from the frozen code's stimulus-event fraction.

Section 6's registered ignition definition, which gives 20/20, from the stricter code diagnostic, which gives 19/20 because of seed 5111.

The registered definitions govern the registered claims. The diagnostic fields remain visible without being misrepresented as the registered endpoints.

This resolves my earlier objection.

3. Holm adjustment — accepted as pending

Keeping the adjusted values null is still the correct treatment. The full family has nine members, and the four Part 7 members do not yet exist.

The additional paragraph is acceptable because it is explicitly labelled a Bonferroni-9 bound, not the registered adjusted value. For a permutation member reported at the Monte Carlo floor, 9(1/10001) ≈ 0.0009.

That supplies a conservative bound for those floor members without pretending that the registered Holm calculation has been completed.

The conditions remain:

Do not report partial-family Holm-adjusted values as the registered adjustment.

Keep the nine-member family and its fixed order unchanged.

Complete the registered Holm procedure once all four Part 7 members are available.

Do not make final family-level confirmatory claims dependent on that adjustment before it is completed.

This does not prevent the Part 5 characterisation results gate from passing.

4. M3 and the other materiality findings

My previous ruling on M3 stands. The open-loop peak-E mean remains outside its registered band and must remain a named discrepancy. The reconciliation does not erase or explain it away.

Likewise, the mean-based M2 result remains inside its registered band, while the eight individual episodes outside that band remain useful distributional information. No retrospective change to the registered materiality criteria is warranted.

Final verdict

Registered contact-duration endpoint — Accepted
Implementation diagnostic kept separate — Accepted
Onset and ignition endpoint mapping — Accepted
Contact-duration TOST correction — Accepted
Holm adjustment pending Part 7 — Accepted with conditions
M3 discrepancy retained — Accepted

REQUIRE CHANGES DISCHARGED — PASS

Reviewer 3 vote: PASS for the Part 5 characterisation results HARD gate.

This closes the characterisation results gate on the supplied record. It does not close the nine-member inferential family, certify Part 7, or establish biological validity or causal connectome contribution.

As before, this is my Reviewer 3 vote, not a claim about panel majority or owner sign-off. I have reviewed the reconciliation and numerical evidence supplied here; I have not independently inspected the updated report, audit artefact, per-seed JSON, repository, or file hashes.

### Panel complete: characterisation results gate (25 Nov 2026)

With the two re-reviews above, the panel for the Part 5 characterisation results gate is complete at 3 of 3 PASS: Reviewer 2 PASS with no required changes; Reviewer 1 PASS, his conditions discharged at his re-review, with his hand recomputation from the per-seed differences matching (his bootstrap intervals differ from the report's in the third decimal, 2.755 against 2.750 on the 95% interval, from a different bootstrap seed, which he accepted); Reviewer 3 PASS on re-review, his REQUIRE CHANGES discharged. Reviewer 1's two remaining wording items and his independence item are completed in section 9.10 of the results report: the seed 5111 descriptive note with the 19 of 20 against 20 of 20 distinction stated beside the persistence claim, the authorship statement for the two section 6 scripts (same working process, shared author, so their agreement is not an independent check), and the event series artefact prepared for his own independent re-derivation from the raw logs (`results/closed_loop/characterisation_event_series_ab.json`, SHA-256 `3e8ad949db9411d36edf896e27c4eb6a6970def5f26b16b2251d1fde21da3981`), which has not yet been performed and is not claimed. Updated report SHA-256: `f318d9e20690c02a42d96b5076e4a85ac45b0f789faaf5edcc07b044431ff510` (the report's section 9.10 records the audit artefact's updated hash, `cda5ed6d437b742adfa023b5027d1f563f2114b9487eae6185b7298b5e3e406e`). The gate is panel complete and awaits my sign-off; it is not closed by this entry.

### Reviewer 1: independent count of the event series (25 Nov 2026; verbatim)

Reviewer 1: independent count of the event series

All 20 paired differences match. I counted the 1s in all 40 strings with a script, and every string has length 100. I took the counts from the strings only and compared them to your list afterwards.

Seed	Arm (a) 1s	Arm (b) 1s	Seed	Arm (a) 1s	Arm (b) 1s
5100	91	51	5111	28	55
5101	92	53	5112	95	56
5102	93	54	5113	94	55
5104	95	56	5114	94	55
5105	93	53	5115	95	57
5106	96	58	5116	95	56
5107	93	54	5117	94	55
5108	95	56	5118	94	55
5109	95	56	5119	97	58
5110	78	55	5120	92	53

Differences: ×0.1 s, these give +4.0, +3.9, +3.9, +3.9, +4.0, +3.8, +3.9, +3.9, +3.9, +2.3, −2.7, +3.9, +3.9, +3.9, +3.8, +3.9, +3.9, +3.9, +3.9, +3.9. That is your list, entry for entry.
Means: 8.995 s for (a) and 5.505 s for (b), with a paired mean of 3.490 s, as reported.
Frozen-code endpoint (chunks 0–59): counting only that window, the strings give 19 zeros and one −2.6 (seed 5111: 28 against 54 ones), also matching.
What this covers

It covers my count and the statistics downstream of it. I took the strings as supplied and did not check that they were extracted correctly from the raw body logs, which stays with your two scripts. I also can’t verify the artefact hash. If the artefact’s strings differ from these, that is a discrepancy to log.

Two findings in the strings

1. Seed 5110 is also an early release in arm (a), and the report says only 5111.

Arm (a), seed 5110: event ON for chunks 6–83, then OFF for chunks 84–99. Contact ended at 8.4 s. That is why its difference is +2.3 s and not about +3.9.
Every other arm (a) episode except 5111 stays ON to chunk 99. So contact persisted to the end of the episode in 18 of 20 episodes, not 19.
The code’s ignition field (ON at or after chunk 40) passes 5110, which is why the report’s 19/20 versus 20/20 split names only 5111.
The persistence claim should say that explicitly: ignition 20/20 (§6), the code’s stricter rule 19/20, and contact persisting to episode end in 18/20 closed-loop episodes (5110 ends at chunk 84, 5111 at chunk 31). Describe 5110’s time series as you did for 5111.

2. The 5111 gap shows a vulnerability of the closed loop that open loop masks.

In arm (a), seed 5111 has contact on chunks 3–30, then off for good.
In arm (b), the same seed has an identical prefix, then a three-chunk gap (chunks 31–33), then contact again from chunk 34 to 60.
So the same seed-specific physical event interrupts contact in both arms at chunk 31. Open loop rides through it because the scripted drive is on. Closed loop shuts the drive off one chunk later and never recovers.
This is a real property of the loop: a brief contact interruption (about 0.3 s here) can switch the loop off permanently. It is worth stating in the interpretation. It does not change any registered result.
Consequence for Part 7
The closed-loop dropout rate with an intact brain is 2/20 for persistence to episode end (95% CI roughly 1–32% by an exact interval).
Any Part 7 comparison that uses persistence or duration as its outcome starts from a baseline that already drops out at that rate, so a lesion effect has to be judged against it. Say so in the report so that Part 7’s power and interpretation account for it.
Status

With the 5110 addition and the contact-interruption sentence in the report, the independent re-derivation is complete and my PASS stands, with these conditions discharged. Nothing in the counts changes the contact-duration result: a paired difference of +3.490 s, 95% CI [2.75, 3.91], claimed under the registered rule.

### Independent count: comparison outcome (25 Nov 2026)

Reviewer 1 counted the 1s in all 40 event series strings himself, blind to the counts in the artefact: he took his counts from the strings only and compared them to the artefact's list afterwards. The comparison, checked entry by entry in this pass: all 40 of his counts match the artefact's `event_on_chunks` values for arms (a) and (b) at the 20 paired seeds exactly, and all 20 paired differences match (his list: +4.0, +3.9, +3.9, +3.9, +4.0, +3.8, +3.9, +3.9, +3.9, +2.3, -2.7, +3.9, +3.9, +3.9, +3.8, +3.9, +3.9, +3.9, +3.9, +3.9, in seed order; means 8.995 s for arm (a) and 5.505 s for arm (b), paired mean +3.490 s). His frozen-code window counts also match: over chunks 0 to 59 the paired differences are 19 zeros and one of -2.6 (seed 5111: 28 against 54). His PASS stands, with the re-derivation conditions discharged, subject to the two report additions his reply requires (the seed 5110 description and the contact interruption statement), which are recorded as section 9.11 of the results report.

His scope note, recorded as he stated it: he counted from the supplied strings; he did not check that the strings were extracted correctly from the raw body logs, which rests on the two project scripts (the extraction script `work/run_characterisation_event_series.py` and the analysis chain behind the per-seed artefact); and he could not verify the artefact hash (SHA-256 `3e8ad949db9411d36edf896e27c4eb6a6970def5f26b16b2251d1fde21da3981`, as recorded in section 9.10 of the report). In this pass, as a consistency check by the same author and not as an independent check, the artefact's 40 strings were compared against the raw body logs' `taste_event_at_chunk_end` fields for all 40 episodes of arms (a) and (b), and every string matched its log exactly.
