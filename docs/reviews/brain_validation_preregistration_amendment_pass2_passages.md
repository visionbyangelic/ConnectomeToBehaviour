# Part 3 Preregistration — changed passages for Reviewer 1's re-read (Amendment Pass 2)

**What this file is.** Reviewer 1 reviewed a summary of the preregistration, not the
document, and asked to re-read only the changed passages after Amendment Pass 2.
This file lists every change Pass 2 made, with section references and before/after
quotations, so the changed passages can be found and judged in the document
(`PART3-PREREG.md`) without re-reading it in full. Unchanged text is not listed.
The frozen implementation (commit `0cb9b81`) is unaffected — protocol-text
amendments only. No validation trial has run or may run under this document yet.

**The one finding that changes the picture.** Pass 2 ran the reference-only
discrimination check Reviewer 1 asked for (R3(ii)), and it discriminates —
decisively, toward 200 Hz. It is recorded in full in §3/A1 (change 5 below)
and in §2.1 (change 3). The 150 Hz primary is kept in this pass exactly as
Reviewer 1's R3 specified it (the amendment was written before the check was
run), but the finding is stated in the document so the panel and Angelic can
decide, before the freeze, whether the primary should switch to 200 Hz by
formal amendment. Nothing in this pass switches it quietly.

---

## 1. R1 — the PASS rule now uses the gap bootstrap, not point estimates (§8, §7 item 7)

**Before (§8, PASS clauses 1–2):** PASS required only point criteria —
"Spearman ρ over U ≥ C_cross,Spearman − 0.02 and ρ ≥ 0.90" and "Pearson r over
U ≥ C_cross,Pearson − 0.02". Bootstrap uncertainty was reported (§7 item 7)
but played no part in the verdict, and no combination rule was stated.

**After (§8, PASS clauses 1–2, and the new overall rule):**
- Clause 1 now reads: "Spearman ρ over U ≥ C_cross,Spearman − 0.02 **and**
  ρ ≥ 0.90 **and** the 95th percentile of the gap bootstrap distribution for
  the Spearman gap (C_cross,Spearman − ρ) ≤ 0.02 (§7 item 7)."
- Clause 2 now reads: "Pearson r over U ≥ C_cross,Pearson − 0.02 **and** the
  95th percentile of the gap bootstrap distribution for the Pearson gap
  (C_cross,Pearson − r) ≤ 0.02 (§7 item 7)."
- New overall rule, stated explicitly at the head of §8: "PASS only if ALL
  criteria in the PASS list are met, including the gap upper bounds. FAIL if
  ANY FAIL trigger fires. Anything else is INCONCLUSIVE. The FAIL triggers
  are point-based; the gap bootstrap interval gates PASS only — a straddling
  interval can demote a PASS to INCONCLUSIVE, but never converts a FAIL into
  an INCONCLUSIVE."
- New INCONCLUSIVE bullet: "the gap bootstrap straddles the tolerance for
  either correlation — the point gap is ≤ 0.02 but its 95th percentile
  exceeds 0.02 (the result is consistent with the tolerance and consistent
  with exceeding it; the same equivalence logic as TOST in FINAL-PLAN §5.6)".

**New method text (§7 item 7, appended):** the gap bootstrap — "B = 2,000
nested replicates; in each replicate, 30 trials are resampled with replacement
from our trials AND 30 from the reference's trials, the mean-rate vectors and
the union set U are recomputed by the same code, the observed correlations are
recomputed, and C_cross is recomputed within the replicate from 50 balanced
splits (the first 50 of the split sequence under seed 20261123). The gap in
each replicate is gap_b = C_cross,b − ρ_b (Spearman) and the Pearson analogue.
The computations operate on the union-set rows only: a neuron active in any
resampled or split window is necessarily active in the full window, so the
restriction is exact, not an approximation. The 95th percentile of each gap
distribution is reported and used in §8."

## 2. R2 — ceiling through the identical pipeline; our split-half; tie handling (§7 item 4)

**Before (§7 item 4):** the ceiling method was fixed (200 balanced 15/15
splits, seed 20261123, Spearman–Brown correction, C_cross = √(R_ref,30 ×
R_new,30)) but did not state that the ceiling uses the identical code as the
comparison, did not write down the tie handling, and did not mention our own
split-half beyond R_new,30.

**After (§7 item 4, new paragraph appended):**
- "The ceiling is computed through the identical `compare_outputs` code as
  the main comparison (`repo/fresh/part3/compare.py`): the same
  union-active-set construction, the same mean-rate vectors, the same
  Spearman and Pearson computations."
- "Tie handling, written down: Spearman ranks use average ranks for tied
  values (scipy.stats.spearmanr default); many ties at 0 are expected,
  because most neurons in the union set are silent on at least one side and
  the union set is dominated by low-rate neurons."
- "The halves' union set is built from the halves themselves by the same
  code — a neuron active in a half is necessarily active in the full
  30-trial window, so the halves' support is a subset of the full support,
  never an ad-hoc redefinition."
- "Our own split-half is reported too: after the runs, R_new,30 is computed
  by the same 200-split machinery (seed 20261123), and the odd/even split-half
  (odd trials vs even trials, same Spearman–Brown correction) is reported as
  an additional quantity — the odd/even split can only be computed after the
  runs, so it is recorded here as a to-be-reported quantity, while the
  reference's component is pre-recorded now (§2.1)."
- "Pre-recorded: R_ref,30 is Spearman 0.9995 and Pearson 0.9998 (§2.1) — the
  'ceiling below 0.90 → INCONCLUSIVE' branch would require R_new,30 < 0.81,
  so it is retained as a guard but is not expected to fire."

## 3. R2 — pre-recorded reference-only values (new §2.1)

**Before:** §2 stated the reference file's hash, counts and MN9 means (448
active neurons; MN9 L 93.3 Hz, R 61.8 Hz) but recorded no ceiling, no CIs, and
no split-half values.

**After (new §2.1, in full):** every quantity below comes from the reference
file alone (computed with `repo/fresh/part3/reference_only.py` through the
`compare.py` pipeline; values saved at
`repo/fresh/part3/reference_only_values.json`), with the reference hash
restated (SHA-256
`83921d50089d966785e402d6c0e3be5ab3eba5beb680410a09c557b0f22dcc28`):
- Active-set size re-counted: **448** (matches Part 1); **434** at ≥ 0.1 Hz;
  **391** at ≥ 1 Hz.
- Reference MN9 means: left **93.27 Hz**, 95% CI [92.10, 94.37]; right
  **61.80 Hz**, 95% CI [60.33, 63.30] (percentile bootstrap over trials,
  10,000 resamples, fixed bootstrap seed **20261124**, declared here in
  advance). Ordering: **left > right**.
- Reference ceiling component R_ref,30: Spearman **0.9995** (SD 0.0001;
  2.5–97.5 percentiles [0.9992, 0.9996]); Pearson **0.9998** (SD 0.0001;
  [0.9997, 0.9999]). The "ceiling below 0.90 → INCONCLUSIVE" branch would
  require R_new,30 < 0.81 (Spearman 0.8104; Pearson 0.8102) — retained as a
  guard, not expected to fire.
- Reference-only split-half analogue for the set-overlap floors: primary
  threshold Jaccard **0.974** (SD 0.004), precision **0.987**, recall
  **0.987**; at 0.1 Hz 0.975 / 0.988 / 0.987; at 1 Hz 0.978 / 0.989 / 0.989.
- Driven-GRN firing rates: the 21 driven right sugar GRNs at mean **196.8 Hz**
  (median 197.3, range 191.3–202.1, n = 21); left sugar, bitter and water GRNs
  all **0.0 Hz**.

## 4. R4 — sensitivity table; floors re-justified from the split-half analogue (§7 item 3, §8 PASS clause 3)

**Before (§7 item 3):** "Set overlap: Jaccard(A_ref, A_ours); precision …;
recall … Thresholded variant: both sets restricted to neurons with mean rate
≥ 1 Hz (reliably active, not one-spike noise), Jaccard reported." The §8
intro called the old build's numbers "the empirical anchor for the
set-overlap floors".

**After (§7 item 3):** "Set overlap and sensitivity table. Jaccard(A_ref,
A_ours); precision …; recall … — computed at the primary active definition
(≥ 1 spike in 30 trials) **and** at two further thresholds, **0.1 Hz** and
**1 Hz** mean rate, as a pre-declared sensitivity table (Reviewer 1, R4):
all three thresholds are reported for all three metrics. The PASS/FAIL floors
in §8 apply at the primary threshold; the other two columns are reported
alongside so a threshold-sensitive result cannot hide. The ≥ 1 Hz column is
the 'reliably active' variant (not one-spike noise)." The active definition
itself is unchanged. The §7 intro sentence about the thresholded variant now
reads: "(The 0.1 Hz and 1 Hz columns of the sensitivity table in §7 item 3
are pre-declared variants; they do not redefine the comparison set for any
other metric.)"

**After (§8 PASS clause 3):** the floors (Jaccard ≥ 0.85, precision ≥ 0.90,
recall ≥ 0.85) are unchanged numerically, but the justification is re-stated:
"the floors sit below the reference-only split-half analogue — the same model
scored against itself over 200 balanced 15/15 splits gives Jaccard 0.974,
precision 0.987, recall 0.987 at the primary threshold (0.975 / 0.988 / 0.987
at 0.1 Hz; 0.978 / 0.989 / 0.989 at 1 Hz; §2.1) — with room left for
seeded-vs-unseeded variation, and the 15-trial halves are a conservative
analogue (smaller active sets than a 30-trial comparison). The floors also sit
below the old build's achieved values (Jaccard 0.9113, precision 0.9928,
recall 0.9174). **Stated openly: those old-build values were seen when the
floors were chosen** — the split-half analogue is the justification; the old
values are disclosed, not hidden." The §8 intro paragraph now reads: "The old
build's numbers … are disclosed alongside the floors; the floors'
justification rests on the reference-only split-half analogue, not on the old
build (see PASS clause 3)."

## 5. R3 — the 150 vs 200 Hz ambiguity becomes a pre-declared arm; the Methods read; the discrimination finding (§3/A1, §4.1, §8.2)

**Before (§3/A1):** the ambiguity was recorded (notebook prose 200 Hz vs code
default 150 Hz; choice 150 Hz because "the code is what ran") with the
sentence "A 200 Hz sensitivity run may be informative at a later rung, but it
must never be used to rescue a failed 150 Hz reproduction…". No arm was
pre-declared; the Methods text had not been read; no reference-only check had
been run.

**After (§3/A1, three new paragraphs appended):**
- *Methods read.* "I have now read the Shiu et al. *Nature* 2024 Methods
  text (DOI 10.1038/s41586-024-07763-9, sections 'Computational modelling'
  and 'Computational modelling of water and sugar GRN activity'). It states:
  'GRNs were activated at particular frequencies using Poisson distributed
  input to generate 10–200 Hz firing (sugar) or 20–260 Hz firing (water)';
  '30 simulations of 1,000 ms for each experiment were performed'; and W_syn
  was chosen 'such that activation of sugar GRNs at 100 Hz resulted in
  roughly 80% of maximal MN9 firing'. … **The Methods text states no single
  canonical rate for the released sugarR file** — the 150 Hz figure rests
  only on the code default, the 200 Hz figure only on the notebook prose, and
  neither is confirmed by the paper."
- *Reference-only discrimination.* "The reference file's own statistics DO
  discriminate the two rates, and they favour 200 Hz: the 21 driven right
  sugar GRNs fire at mean **196.8 Hz** (median 197.3, range 191.3–202.1,
  n = 21) in the reference file, while the undriven control populations —
  left sugar GRNs, bitter GRNs, water GRNs — fire at exactly **0.0 Hz**
  (§2.1). Under the model's drive (68.75 mV kick per Poisson event,
  refractory removed while driven — §3 table), a driven neuron fires at close
  to the Poisson rate by construction, so the driven rate reads out the
  generating drive rate: ~200 Hz, not 150 Hz (150 Hz sits 47 Hz from the
  observed mean, against a per-neuron spread of a few Hz; network input cannot
  explain the gap, since the undriven control populations are completely
  silent). Corroboration: the paper reports 455 neurons responding at 200 Hz
  drive versus 45 at 10 Hz (main text, Fig. 1d); the file has 448 active
  neurons. **Consequence, stated plainly:** the reference-only evidence says
  the file was most likely generated at 200 Hz, so the 150 Hz primary protocol
  in this document is now known to be a likely mis-specification. This pass
  keeps 150 Hz as the primary confirmatory protocol (Reviewer 1's R3 as
  written, specified before this check was run) and pre-declares the 200 Hz
  arm below (§4.1, §8.2) — but the finding is recorded here in full so that
  the panel and Angelic can decide, BEFORE the freeze, whether the primary
  should switch to 200 Hz. Such a switch would be a further formal amendment
  (a corrected protocol needs its own new preregistration), never a quiet edit
  to this document."
- *Hemisphere note.* "The Methods state 'we performed unilateral left
  hemisphere activation for all simulations, except for Extended Data Fig.
  1d', while the notebook's driven list is the 21 right-hemisphere GRNs —
  and the paper elsewhere notes the FAFB volume was found left–right
  inverted, with 'right hemisphere GRNs' in the paper corresponding to 'left
  hemisphere GRNs' described previously. The file's own MN9 asymmetry (L 93.3
  > R 61.8 Hz, contralateral stronger per the main text) is consistent with
  the notebook's right-hemisphere list. The driven population in this
  preregistration is defined by the literal ID list, not by a hemisphere
  label, so the protocol is unaffected; the inconsistency is recorded here so
  it is never discovered as an excuse after the fact."

**New §4.1 (the 200 Hz sensitivity arm, pre-declared, non-confirmatory):**
"Configuration: identical to the primary run in every respect except
`rate_hz` = 200 and the seed block **3030–3059**; run_id
`part3-sugarR-200Hz-arm`; 30 trials × 1.0 s; same frozen implementation. It
runs **only after the primary verdict is recorded**, takes ≈ 1 hour, and is
labelled **non-confirmatory** throughout. Its result is evaluated under the
same §8 rules applied to its own 30 trials, reported alongside the primary
verdict, and governed by §8.2."

**New §8.2 (the 200 Hz arm and protocol-ambiguity):** "if the primary is FAIL
or INCONCLUSIVE and the 200 Hz arm would have passed, the verdict stays FAIL
or INCONCLUSIVE, annotated **'protocol-ambiguous'**. A corrected (200 Hz)
protocol then needs its own new preregistration — the pass bar cannot be moved
after the fact by pointing at the arm. This rule holds even though the
reference-only evidence (§3/A1) now favours 200 Hz as the generating rate:
the arm's purpose is to measure the ambiguity, not to rescue the primary."

**§9 (new final paragraph):** "The 200 Hz arm is not a diagnosis step. It
runs after the verdict is recorded (§8.2), under its own rules. If the primary
FAILs, the diagnosis path above runs first; ambiguity A2 (the protocol is a
reconstruction) is interrogated at step 7, last — and it now has a known
candidate, the drive rate (§3/A1), which the diagnosis must weigh with
evidence, not assume. A failed primary does not become a passed 200 Hz primary
by re-labelling; a corrected protocol needs its own new preregistration."

## 6. R5 — INCONCLUSIVE now has pre-registered paths (§4.2, §8.1)

**Before (§8):** "An inconclusive verdict … goes to the gate with its
diagnosis and options (e.g. more trials, by formal amendment) for Angelic's
decision." No extension was pre-registered; no path distinguished
precision-only inconclusive outcomes from other ones.

**After (new §4.2, the N = 60 extension):** "If — and only if — the primary
result is inconclusive SOLELY because the MN9 95% CI half-widths exceed 15%
of the reference means (the §8 precision gate), with no other criterion in an
intermediate or fail band, ONE extension to N = 60 is allowed: 30 additional
trials at 150 Hz under the same frozen implementation and protocol, seeds
**3060–3089**, run_id `part3-sugarR-benchmark-n60`, ≈ 1 hour."

**After (new §8.1, paths out of INCONCLUSIVE):**
- "(a) Precision-only extension, once. … The comparison is then recomputed
  over all 60 trials against the reference's 30: the active set is redefined
  over the 60-trial window; the ceiling becomes C_cross,60 = √(R_ours,60 ×
  R_ref,30), with R_ours,60 from 200 balanced 30/30 splits of our 60 trials
  corrected to 60 trials; the MN9 CIs are recomputed from 60 trials and the
  gap bootstrap resamples 60 trials from ours and 30 from the reference's;
  the PASS/FAIL bands of §8 apply unchanged with C_cross,60 in place of
  C_cross. The original 30 trials are retained, never replaced. If the result
  is still inconclusive after the extension, path (b) applies."
- "(b) Any other inconclusive outcome — including a gap-bootstrap straddle,
  an intermediate Pearson/Spearman band, or a still-inconclusive result after
  the N = 60 extension — goes to the gate for a panel decision, or a logged
  waiver signed by Angelic following the §0.2(c) pattern (a signed, dated
  record that the decision path was followed — the same discipline as the
  expert-check waiver in PART0-PACKAGE §6.3: the mitigation may fail, it may
  never *silently* not happen)."

## 7. R6 — scope of what Part 3 certifies (new §12)

**Before:** the Scope paragraph in the header listed the remaining rungs in
one sentence and said nothing about what a sugarR pass does or does not
certify.

**After (new §12, in full substance):** "Part 3 certifies **the sugarR rung
only**. The feeding experiment depends on bitter and on sugar+bitter
suppression, about which a sugarR pass says nothing — a sugarR pass is
evidence about one stimulus, one population, one experiment, not about the
feeding circuit." The six-rung ladder is listed (1. short trial; 2. four
conditions — sugar / bitter / sugar+bitter / water — with CIs; 3. sugarR
benchmark — this document; 4. feeding prediction subset incl. silencing,
labelled model-vs-animal; 5. weight-shuffle control; 6. RQ-C5 asymmetry
resolution), each rung getting "its own preregistration document before its
runs, under the same HARD gate". "A sugarR-only pass must not be reported as
'brain validated'. The permitted wording is 'the sugarR benchmark rung
passed'." The header Scope paragraph now points to §12, and §11 gains the
reporting bullet: "A sugarR-only pass is reported as 'the sugarR benchmark
rung passed' … — never as 'brain validated' (§12)."

## 8. Non-blocking points

- **Seeds and determinism (§4, new paragraphs).** "Brian2 state is reset
  between trials: the runner builds a fresh seeded network per trial, so no
  state carries across trials; each trial's seed is independent; the CPU
  backend is deterministic." Pre-declared engineering check (not a validation
  trial): run_id `part3-determinism-check`, "two 1-trial runs at seed 9999
  under the frozen implementation; the two spike tables must be bit-identical
  (equal SHA-256). … If the tables differ, STOP and diagnose — a
  determinism failure voids the frozen implementation's reproducibility claim
  and blocks the validation runs." Seed-block allocation is fixed: 3000–3029
  primary, 3030–3059 the 200 Hz arm, 3060–3089 the N = 60 extension, 9999 the
  determinism check.
- **`w` wording (§3/A4).** Before: "removal of an ineffective statement".
  After: "removal of a statement shown to have no effect under these tests"
  — "the evidence is Part 2's before/after tests (bit-identical spike trains
  with and without the clause under the same seed; no `w` variable created on
  the group; weight vectors verified before and after). … 'ineffective' must
  never be claimed in general, only 'no effect under these tests'."
- **Freeze procedure (new §13).** A six-item freeze checklist: approval;
  commit and tag `part3-prereg-v1` (created only after approval; never moved
  or deleted); reference-file hash; harness hash (analysis pipeline and
  frozen runner commit `0cb9b81`); timestamps kept; determinism check first.
  "No validation trial runs until the checklist is complete."
- **Verified, no change.** The arithmetic is consistent (0.275 mV × 250 =
  68.75 mV) — noted in the Amendment history, no text changed. The MN9
  difference-with-CI decision test was already in Pass 1 (§8 clause 4) and
  was verified, not re-added — noted in the Amendment history.

## 9. Minor consistency fixes made during the re-read

- §8 INCONCLUSIVE bullet: "the same equivalence logic as TOST in §5.6"
  corrected to "…in FINAL-PLAN §5.6" (this document has no §5.6).
- §7 intro: the sentence about the thresholded Jaccard variant updated to
  refer to the sensitivity table's 0.1 Hz and 1 Hz columns.
- §8 intro: the old build's numbers are now described as "disclosed
  alongside the floors" with the justification resting on the split-half
  analogue (PASS clause 3), not as "the empirical anchor".
- §4 wall-clock: the 200 Hz arm and the N = 60 extension are noted as each
  adding ≈ 1 hour if they run.
- §8.1(a): the N = 60 recomputation now states explicitly that the gap
  bootstrap resamples 60 trials from ours and 30 from the reference's.

## 10. What did NOT change

- The frozen implementation (commit `0cb9b81`): untouched.
- The primary protocol: 150 Hz, 30 trials, seeds 3000–3029 — unchanged.
- The PASS/FAIL numeric bands and floors (Spearman/Pearson ±0.02/±0.05,
  Jaccard 0.85/0.75, precision 0.90, recall 0.85, MN9 equivalence margins
  ±23.3 Hz / ±15.5 Hz): unchanged numerically; R1 only added the gap-bound
  condition, R4 only re-justified the floors.
- The active definition (≥ 1 spike in 30 trials ≈ 0.033 Hz): unchanged.
- The diagnosis path (§9) and K1: unchanged except the added paragraph
  (change 5) stating the 200 Hz arm is not a diagnosis step.
