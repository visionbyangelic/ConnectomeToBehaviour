# Part 3 Preregistration — panel review record

Document under review: `PART3-PREREG.md` (the `sugarR` benchmark rung), draft of 23 Nov 2026.
Gate class: HARD — full panel review and Angelic's explicit approval are required before any validation trial runs.
Frozen implementation: commit `0cb9b8129236dc4200b5eaa600f59ccc072263f9` (record: `PART3-FREEZE.md`). The reviews below concern protocol text only; no reviewer asked for code changes, and none were made.

---

## Reviewer 2 — verdict: APPROVE after required amendments (23 Nov 2026)

Required amendments (all incorporated in Amendment Pass 1, 23 Nov 2026):

1. **MN9 ordering source.** State explicitly that the left>right ordering requirement is a property of the `sugarR` reference output itself (left 93.3 Hz, right 61.8 Hz in the reference data) — a model-vs-model benchmark check, not a biological assumption and not the old build's ordering. RQ-C5's "whether, never why" is untouched.
2. **Pearson classification closed.** State the full Pearson bands explicitly, mirroring the Spearman structure: PASS if r ≥ C_cross,Pearson − 0.02; FAIL if r is more than 0.05 below C_cross,Pearson or below 0.80; otherwise INCONCLUSIVE — including the case where Spearman passes and Pearson does not. The overall verdict follows the worst applicable band per metric, with the rule stated in the document.
3. **Active definition (jointly with Reviewer 3).** A neuron is active if and only if it emits at least one spike across the full 30-trial evaluation window (equivalently mean rate > 0 Hz; the numeric equivalent, 1 spike / 30 s ≈ 0.033 Hz, stated explicitly). The same union active set is used identically for Spearman, Pearson and Jaccard — never varied per metric.

## Reviewer 3 — verdict: APPROVE after required amendments (23 Nov 2026)

Required amendments (all incorporated in Amendment Pass 1, 23 Nov 2026):

1. **Cross-replicate noise ceiling (replaces the reference-only ceiling).** Estimate split-half reliability for BOTH datasets (R_ref,30 from the reference's halves corrected to 30 trials; R_new,30 the same for our runs), and define C_cross = √(R_ref,30 × R_new,30) as the expected ceiling for both Spearman and Pearson, each computed with its own correlation type. Split method preregistered: average over multiple balanced 15/15 splits, with the number of splits, the split-generation method and a fixed split seed all published in the document. Report R_ref,30, R_new,30 and C_cross alongside the observed correlations. The INCONCLUSIVE rule "ceiling below 0.90" now refers to C_cross.
2. **MN9 agreement test (replaces CI-overlap as the decision).** For each MN9 neuron, Δ = r_new − r_ref with a confidence interval for the difference; agreement requires the difference to lie within a prespecified equivalence margin, taken from Part 0's existing tolerance (PART0-PACKAGE §2.4: ±25% of the mean rate, or ±5 Hz, whichever is wider) and stated numerically in the preregistration. CI-overlap (Part 0 §2.3) is retained as reporting, not as the decision. The 15% CI half-width rule stays as a precision gate (INCONCLUSIVE if exceeded). The left>right ordering stays as a separate requirement. The FAIL clause "MN9 deviation over 50% with non-overlapping CIs" is reworded to use the amended test.
3. **Shortfall clarification.** "Within 0.02 of ceiling" means observed ≥ C_cross − 0.02 (a maximum permitted shortfall); observed values may exceed the ceiling without penalty. Uncertainty: report trial-resampling (bootstrap over trials) uncertainty for both the observed correlations and the ceiling estimate; the ceiling is an estimate, not a constant.
4. **Documentation details.** The reconstruction record preserves the exact producing notebook cell, the upstream commit, the default-parameter definition and the conflicting 200 Hz prose; 150 Hz is labelled "reconstructed protocol, not independently verified from the reference parquet"; a 200 Hz sensitivity run may be informative later but must never be used to rescue a failed 150 Hz reproduction. Seed semantics stated: each seed initialises all stochastic components of its trial (the Poisson drive), streams independent across trials, reproducible without reliance on execution order or hidden global state.

## Reviewer 1 — verdict: NOT APPROVED as written; six required amendments (23 Nov 2026, ~21:04 WAT)

Important scope note: the preregistration document itself was **not** attached
to this review — the chat's uploads folder contains only the plan files. This
review therefore covers the summary as sent, not the document text. He requires
the six amendments below before the freeze, and asks that the file then be sent
to him so he can re-read only the changed passages, as in the plan round.

Required amendments:

1. **R1 — The pass rule uses point estimates, so a result can land on the
   tolerance by chance.** The 0.02 tolerance on the Spearman gap is small
   relative to sampling noise over 30 trials. Pre-register a bootstrap over
   trials, resampling both our trials and the reference's, for each primary
   statistic and for the gap to the ceiling. PASS should require the point
   criterion AND the upper 95% bound of the gap ≤ 0.02. If the interval
   straddles the tolerance, the result is INCONCLUSIVE, not PASS — the same
   equivalence logic as TOST in §5.6. State the combination rule explicitly:
   PASS only if all criteria are met, FAIL if any FAIL trigger fires,
   otherwise INCONCLUSIVE.
2. **R2 — The noise ceiling needs the same pipeline as the comparison.** A
   split-half ceiling uses 15-trial halves; whether a neuron counts as active,
   and how many tie at zero, depends on how many trials were averaged, and
   Spearman-Brown corrects the reliability but not a changed support. Compute
   the ceiling through the identical union-active-set and tie-handling code,
   and write down the tie handling (many ties at 0 are expected). Our 30
   seeded trials give an odd/even split for free — report our own split-half
   as well, and flag a mismatch with the reference's. Every quantity that
   comes from the reference alone should be recorded in the preregistration
   with the reference file's hash, before any trial runs: the ceiling, the
   reference MN9 means and ordering, and the reference active-set size. These
   analyses see no model output, so doing them now is clean — and it tells us
   now whether the "ceiling below 0.90 → INCONCLUSIVE" branch is already
   live.
3. **R3 — Turn the 150 vs 200 Hz ambiguity into a pre-declared sensitivity
   arm.** The code-reading argument for 150 Hz is sound; keep 150 Hz as the
   primary, confirmatory protocol. But an unresolved ambiguity this important
   (K1 is on the line) should not be left to the last step of a diagnosis
   path: pre-declare a 200 Hz arm (~1 hour), labelled non-confirmatory, with
   the rule that if the primary is FAIL or INCONCLUSIVE and the 200 Hz arm
   would have passed, the verdict stays FAIL or INCONCLUSIVE, annotated
   "protocol-ambiguous". A corrected protocol then needs its own new
   preregistration, so the pass bar cannot be moved after the fact. Before the
   freeze, also read the Shiu et al. methods text for the stated rate, and
   check whether the reference file's reference-only statistics discriminate
   the two rates.
4. **R4 — Define "active", and don't anchor the floors to the old build.**
   Define the activity threshold exactly: a neuron with one spike in one of
   30 trials is active at about 0.03 Hz if the rule is "any spike", and
   Jaccard is highly sensitive to this boundary. Add a sensitivity table at
   two other thresholds, e.g. 0.1 Hz and 1 Hz. The precision, recall and
   Jaccard floors are "set below the old build's achieved values"; the plan
   treats those numbers as unverified and the comparison checkpoint is meant
   to be blind to the old results — justify the floors from a reference-only
   split-half analogue, as in R2, and state openly that the old values were
   seen when the floors were chosen.
5. **R5 — Give INCONCLUSIVE a pre-registered path.** Only FAIL has one now,
   and the gate does not pass on INCONCLUSIVE. For a result that is
   inconclusive only because the MN9 CI half-widths exceed 15%, allow one
   extension to N=60. For anything else, require a panel decision or a logged
   waiver signed by Angelic, as in §0.2(c).
6. **R6 — State the scope of what Part 3 certifies.** The feeding experiment
   depends on bitter and on sugar+bitter suppression; a sugarR pass says
   nothing about those. State whether Part 3 requires every rung and where
   each later rung is pre-registered — each must be registered before its own
   runs. A sugarR-only pass must not be reported as "brain validated".

Non-blocking points:

- Arithmetic check: 0.275 mV × 250 = 68.75 mV, so the kick size is consistent
  with w_syn = 0.275 mV and a 250 input scale.
- MN9 CI-overlap rule: it is conservative, since overlapping intervals can
  still differ. Also report the difference with its CI.
- Seeds: state that Brian2 state is reset between trials, that each trial's
  seed is independent, and that the CPU backend is deterministic. A short
  determinism check should be pre-declared as an engineering test, not a
  validation trial.
- The "w omission" wording: cite the before/after weight-vector tests as the
  evidence. Claim "no effect under these tests", not "ineffective" in general.
- Freeze: commit and tag the preregistration, the reference-file hash and the
  harness hash before any trial runs. Keep the timestamps.

What he calls already sound: the diagnosis order, with protocol reconstruction
last; the K1 link and the ban on refitting w_syn; the "reproduction of a
reference output, not biological validation" language; naming the 150/200 Hz
ambiguity openly — R3 only turns that disclosure into a control.

### Relation to Amendment Pass 1 (note, not Reviewer 1's words)

Reviewer 1 reviewed the original draft summary, so some of his requirements
overlap work Pass 1 already did; the overlap is recorded here so Amendment
Pass 2 can build on it rather than redo it:

- R1: partly new. Pass 1 added bootstrap-over-trials uncertainty reporting for
  the observed correlations and the ceiling, but did not make the upper 95%
  bound of the gap part of the PASS rule, and did not state the combination
  rule explicitly.
- R2: partly new. Pass 1 already made the ceiling cross-replicate (C_cross
  from 200 balanced 15/15 splits, seed 20261123). New here: the ceiling
  computed through the identical union-active-set and tie-handling code with
  the tie handling written down, our own split-half reported, and the
  reference-only quantities pre-recorded with the reference file's hash.
- R3: new in form. Pass 1 said a 200 Hz sensitivity run may be informative
  later but must never rescue a failed 150 Hz reproduction; R3 pre-declares
  the arm with the "protocol-ambiguous" annotation rule.
- R4: partly new. Pass 1 already defined "active" exactly (at least one spike
  across the full 30-trial window, ≈0.033 Hz) and uses the same union set for
  all metrics. New here: the sensitivity table at 0.1 Hz and 1 Hz, floors
  justified from a reference-only split-half analogue, and the open statement
  that the old values were seen when the floors were chosen.
- R5: new.
- R6: new.
- Non-blocking MN9 point: already satisfied in substance — Pass 1 replaced
  CI-overlap as the decision with a difference-based equivalence test, with
  CI-overlap retained as reporting only.

---

## Status after Amendment Pass 1

- Reviewer 2: approved subject to the amendments above — incorporated.
- Reviewer 3: approved subject to the amendments above — incorporated.
- Reviewer 1: **NOT approved as written** — six required amendments (R1–R6)
  above, plus non-blocking points. Amendment Pass 2 required; after it, the
  file goes to Reviewer 1 for a changed-passages re-read.
- Angelic's approval: pending.

No validation trial may run until Reviewer 1's amendments are incorporated and
re-confirmed, and Angelic has approved the preregistration.

## Confirmation round

- Reviewer 2 (23 Nov 2026, ~20:38–20:39 WAT): CONFIRMED — all three of his required
  amendments are cleanly satisfied (MN9 ordering sourced to the reference output;
  Pearson classification fully specified with the worst-band rule; active threshold
  exact and the cross-replicate ceiling computation concrete: 200 balanced 15/15
  splits, seed 20261123).
- Reviewer 3: confirmation pending.
- Reviewer 1: review received 23 Nov 2026, ~21:04 WAT — NOT approved as
  written; six required amendments (R1–R6) recorded above. Re-confirmation
  after Amendment Pass 2 pending; he will re-read only the changed passages
  from the file itself (his review covered the summary, not the document
  text, because the file was not attached).
- Reviewer 3 (23 Nov 2026, ~20:38–20:39 WAT): CONFIRMED — all three of his required
  amendments are satisfied; no line falls short. He noted the confirmation covers the
  amended lines as presented, not an independent re-inspection of the full document,
  and that his confirmation is not Angelic's approval and authorises no runs by itself.
  NOTE: his original panel chat reached its context limit ("Context window full"), so
  the confirmation was taken in ChatGPT's own continuation chat,
  "Review ConnectomeToBehaviour Plan (1)"
  (https://chatgpt.com/c/6b049669-98e4-83ea-a99d-d3a3d1110434) — future Reviewer 3
  rounds go to that chat.

## Panel decision consultation — Reviewer 1 (23 Nov 2026, 22:40 WAT)

Angelic delegated Decision B (primary drive rate) to the panel. Reviewer 1's vote: **(1) switch the primary to 200 Hz**; 150 Hz becomes the non-confirmatory sensitivity arm. Reasons: the R3 discrimination check discriminates decisively (driven GRNs 196.8 Hz mean, controls exactly 0.0 Hz; driven rate reads out the generating rate by construction); corroborated by the paper's 455-responding-at-200 Hz figure vs the file's 448 active neurons; keeping a primary the document itself calls "a likely mis-specification" would waste the confirmatory run and still need a new preregistration; a two-trial calibration has no decision value (it tests our runner, not the reference's generating rate). The switch must be a formal **Amendment Pass 3** before the freeze, rewriting (not re-numbering): §3/A1 choice and reason; §4 primary rate_hz = 200; §4.1 arm becomes 150 Hz under the same rules; §4.2/§8.1 extension rate follows the primary (200 Hz); §8.2/§9 protocol-ambiguous annotation inverted; seed blocks swapped (primary keeps 3000–3029; the 150 Hz arm takes 3030–3059; no seed reuse across arms).

**Preregistration confirmation:** Reviewer 1 CONFIRMS the Pass 2 changed passages faithfully implement R1–R6 and the non-blocking points (his per-item confirmation is recorded in his reply of 22:40 WAT; one note: the 50-split within-replicate ceiling is noisier than the 200-split main ceiling, declared in advance and conservative — no change required). He does NOT confirm the Pass 2 document as freezable with 150 Hz as primary: no validation trial may run until Pass 3 is made, the full panel has reviewed it, and Angelic has approved it under the §13 freeze checklist.

## Panel decision consultation — Reviewer 2 (23 Nov 2026, 22:41 WAT)

Reviewer 2's Decision B vote: **(1) switch the primary to 200 Hz** — same reasoning (the reference-only evidence is decisive; a calibration would only re-confirm our implementation's mapping, not the generating rate). Conditions match Reviewer 1's Pass 3 specification: formal amendment with a new preregistration version/tag, never a quiet edit; 200 Hz primary, 30 trials, seeds 3000–3029; 150 Hz non-confirmatory arm at seeds 3030–3059 after the verdict, §8.2 non-rescue bar applying to it; N = 60 extension at 200 Hz, seeds 3060–3089; §§3/A1, 4, 4.1, 8.2 and 9 updated. **Preregistration re-confirmation:** Pass 2 changed passages CONFIRMED item by item (R1–R6 + non-blocking + minor fixes). He did NOT approve freezing the 150 Hz-primary version; freeze is approved only for the amended 200 Hz-primary version after it is applied and re-checked.

**Decision B tally so far: switch to 200 Hz, 2–0** (Reviewers 1 and 2; Reviewer 3's vote still to come but cannot change the majority). The panel's decision, under Angelic's delegation: **the primary switches to 200 Hz by formal Amendment Pass 3.**

## Panel decision consultation — Reviewer 3 (23 Nov 2026, 22:41 WAT)

Reviewer 3's Decision B vote: **(1) switch the primary to 200 Hz** — **Decision B is unanimous: switch, 3–0.** His required-amendment specification adds two details to Reviewers 1 and 2's: the primary run_id becomes `part3-sugarR-200Hz` and the arm `part3-sugarR-150Hz-arm`; and a new freeze tag/version must be used (the Pass 2 tag `part3-prereg-v1` is never moved). **Pass 2 re-confirmation:** items 1–4, 6, 7, 9 CONFIRMED; item 5 confirmed with the Decision B change; item 8 confirmed with the seed-label update; item 10 requires the amendment (the 150 Hz primary and its labels are superseded). One statistical qualification, to be folded into Pass 3: the gap must be kept explicit and SIGNED in the frozen document — G = C_cross − ρ_observed (and the Pearson analogue) — with the 95th-percentile condition applied to the signed gap, not an absolute difference, so exceeding the ceiling is never penalised. His Pass 1 and Pass 2 confirmations remain valid for the statistical/documentation amendments but do not authorise runs under the superseded 150 Hz primary.

## Angelic's acceptance of Decision B (23 Nov 2026, 22:44 WAT)

Angelic accepted the panel's decisions ("Alright let's go with that"), including the switch of the Part 3 primary to 200 Hz. Her formal approval of the amended preregistration itself is still taken at the §13 freeze step, after the panel's Pass 3 re-check.

## Pass 3 re-check — Reviewer 3 (23 Nov 2026, 22:48 WAT)

**CONFIRMED — no corrections required before the freeze.** Reviewer 3 verified the 16 Pass 3 changed passages against Decision B and against his own recorded vote and qualification: the 200 Hz primary with the full history and discrimination evidence in §3/A1; his run-ID specification verbatim (part3-sugarR-200Hz / part3-sugarR-150Hz-arm / part3-sugarR-200Hz-n60) and the seed blocks; §8.2 inverted with the non-rescue rule intact; the signed gap G = C_cross − ρ_observed with the 95th-percentile condition on the signed gap; §13's honest tag statement (first tag part3-prereg-v2). Scope note (his): the re-check is of the changed passages as listed in full, cross-checked against his recorded vote — no separate live copy of the document was present in his chat. His confirmation does not itself grant document approval or the freeze.

## Pass 3 re-check — Reviewer 1 (23 Nov 2026, 22:48 WAT)

Reviewer 1 verified all 16 Pass 3 passages against the verbatim amended document text (supplied through the panel channel, since the file is not in his chat): **confirmed subject to ONE required correction** — the Pass 3 amendment-history bullet for §4.2/§8.1(a) ended "run_id unchanged", contradicting §4.2, §8.1(a) and the same entry's earlier bullet (the extension run_id did change, to `part3-sugarR-200Hz-n60`). The correction was applied exactly as he prescribed and recorded as a typo correction inside the Pass 3 entry; no protocol text was affected. With that correction, his re-check is complete. Scope note (his): the untouched Pass 1/Pass 2 sections were not independently re-read in this round; the "nothing else changed" claim rests on the supplied material and the earlier consistency sweep.

## Pass 3 re-check — Reviewer 2 (23 Nov 2026, 22:48 WAT)

**CONFIRMED — no corrections required.** Reviewer 2 verified all 16 changed passages against Decision B as recorded in his consultation thread: the 200 Hz primary and run_id, the 150 Hz arm and its seed block, §8.2 inverted with the non-rescue bar, the extension at 200 Hz, the §3/A1 justification and history, the signed gap, and §13's tag statement (first tag part3-prereg-v2).

**Panel re-check of Amendment Pass 3: COMPLETE** (Reviewer 1 confirmed with the typo correction applied; Reviewers 2 and 3 confirmed outright). Remaining before any validation trial: Angelic's formal approval of the amended preregistration document, then the §13 freeze checklist (commit + tag part3-prereg-v2, reference and harness hashes, timestamps, determinism check first).

## Part 3 HARD gate — results review, Reviewer 1 (23 Nov 2026, 23:41 WAT)

**PASS stands as computed for the sugarR rung (200 Hz primary); deviations acceptable as logged; the Part 3 gate can close for this rung only, subject to Angelic's sign-off.** Reviewer 1 verified the numbers as presented (including the internal consistency of U = 453 with TP 441 / FP 5 / FN 7), judged all five logged deviations acceptable, and recorded no objections. Scope per §12: this certifies the sugarR 200 Hz rung only. His review was on the presented verdict-relevant numbers, not a re-run of compare.py or the git objects.

## Part 3 HARD gate — results review, Reviewer 3 (23 Nov 2026, 23:42 WAT)

**PASS stands — the Part 3 gate can close, subject to Angelic's sign-off, for the sugarR 200 Hz rung only.** Reviewer 3 verified the freeze/run integrity and every verdict number from the reported computation (noting the Pearson gap differs by 0.00001 from subtracting the rounded printed values — rounding-level, no threshold affected). All five deviations judged acceptable as logged, with conditions that are already met by construction: the §13 note must remain identifiable as a post-run annotation and the commit/tag unmoved; the declared bootstrap seeds (20261125, 20261126) are now fixed for any re-analysis; later track.md entries are not amendments to the frozen preregistration.

## Part 3 HARD gate — results review, Reviewer 2 (23 Nov 2026, 23:42 WAT)

**PASS stands — upheld as computed under the preregistration; deviations acceptable as logged; the Part 3 gate can close subject to Angelic's sign-off; no re-run required.** Reviewer 2 recomputed the verdict from the reported numbers (all mutually consistent), judged none of the five deviations to touch a decision rule, threshold, seed, stimulus or analysis path, and recorded two non-blocking suggestions for future preregistrations: name all bootstrap seeds, and word §13 to expressly permit the post-run dated note.

**Part 3 HARD gate — panel side COMPLETE (23 Nov 2026):** all three reviewers uphold the PASS for the sugarR 200 Hz rung, deviations accepted as logged. Remaining: Angelic's gate sign-off, after which Part 3 closes for this rung and the non-confirmatory 150 Hz arm may run (§8.2).

## Part 3 HARD gate — Angelic's sign-off (23 Nov 2026, 23:48 WAT)

Angelic signed off ("Okay — Part 3 works"). **Part 3 is CLOSED for the sugarR rung**: preregistration approved and frozen (part3-prereg-v2), determinism verified, primary run PASS as computed, panel HARD gate upheld the verdict unanimously, owner sign-off recorded. Next per the plan: the non-confirmatory 150 Hz arm (§8.2), then Part 2b.
