# Part 6 readiness check (repo-held copy)

Verbatim copy of the readiness note written 25 Nov 2026 and held outside the repo at `~/workspace/connectome-work/work/part6_readiness_check.md`, placed here so the section 1 lock claim in `docs/fresh_vs_old_comparison.md` is checkable at this commit. Nothing in the note below has been altered.

---

# Part 6 readiness check (25 Nov 2026)

Readiness only. No Part 6 comparison has been run, no v0 number has
been opened, and no Part 6 episode exists. Part 6 is a HARD gate:
its comparison runs at its place in the plan, after the Part 5
results gate closes, under the hash-and-lock rule (fresh outputs
hashed and locked before any v0 numbers are opened for comparison).
This note records that the fresh side is locked and lists what the
fresh side brings to the comparison in PLAN.md section 4.1, so the
gate can start from a verified lock instead of a fresh assembly.

## The fresh lock, re-verified 25 Nov 2026

- Characterisation ledger
  (results/closed_loop/characterisation/ledger.json): 100 episodes,
  500 recorded files, re-hashed against disk just now: 0 mismatches.
  Freeze tag part5-prereg-v1, r_hi 172.64875034982174 Hz, r_lo 5 Hz.
  One void attempt, arm (c) seed 5107, preserved and re-attempted
  under the same seed, as section 14 item 8 registers.
- Characterisation report
  (docs/closed_loop_characterisation_results.md): SHA-256
  45d446ce7cf1613075cccfeb35221a670c822da2ea210eefd3c7315d5dd6a889,
  the value in the gate record after the reconciliation and the
  independent count.
- Characterisation audit artefact
  (results/closed_loop/characterisation_analysis_audit.json):
  SHA-256 cda5ed6d437b742adfa023b5027d1f563f2114b9487eae6185b7298b5e3e406e,
  the value in the gate record.
- Part 5 preregistration (docs/closed_loop_preregistration.md):
  SHA-256 81191895af32ce3dfbf17e556579c4de5cfdb8a4236447aa1d0088895b237a00,
  the frozen value.

## The fresh side of the section 4.1 comparison

All values below are from already published reports. Nothing new
was computed for this note.

- Data counts (Part 1, docs/connectome_data.md): 127,400 unique
  IDs; 14,687,178 edges; 52,793,639 synapses.
- Part 3 primary, sugarR rung (docs/brain_validation_results.md):
  30 trials of 1.0 s, seeds 3000 to 3029; MN9 L 92.57 Hz
  [91.10, 94.03], R 62.40 [60.50, 64.47]; Spearman 0.99939;
  508,915 spikes; 446 active neurons.
- Four-conditions rung (docs/taste_conditions_results.md): sugar
  anchor L 93.63 Hz, R 61.47 (deltas +1.07 and -0.93 against the
  Part 3 primary); suppression ratio 0.126 [0.115, 0.138];
  bitter alone MN9 exactly 0.00 Hz both sides; water alone
  L 30.23, R 11.87 Hz; bitter dose-response 0.573 (100 Hz),
  0.330 (150), 0.126 (200); bilateral (v) descriptive
  L 93.17, R 64.87.
- Characterisation (docs/closed_loop_characterisation_results.md):
  arm (a) peak E 2.043 rad [2.032, 2.051], contact 20/20;
  arm (b) peak E 2.030 [2.016, 2.043], contact 20/20 then
  offset in all 20; arm (c) exactly zero on every measure;
  arm (d) suppression ratio 0.121 [0.116, 0.127], no contact;
  arm (e) peak E 2.056, contact 20/20.
- RQ-C5 symmetry outcome: L greater than R preserved in the
  Part 3 primary, in the rung anchor, and in every
  characterisation sugar arm.

## What Part 6 still needs

- The v0 side: the preserved old build in v0-prototype/ (its
  structure is intact; its numbers were not opened for this
  note and must not be opened until the fresh lock above is
  recorded at the gate, per the hash-and-lock rule).
- The paper side: Shiu et al.'s released outputs, which the
  panel's adopted caveat names as the meaningful external
  reference. The old repo is a debugging aid and a provenance
  record, not a pass/fail target.
- The per-item discrepancy log (PLAN.md section 4.1): every
  difference gets magnitude, candidate causes, a
  discriminating test if needed, and a verdict (old wrong /
  fresh wrong / both right under stated conditions /
  unresolved). Unresolved load-bearing discrepancies block
  any push.
- Angelic's decision at the end of the comparison: (a) fresh
  replaces old in the existing repo; (b) old stands, fresh
  published as an additional or correcting section; (c) hybrid,
  itemised.
- One plan-text note: PLAN.md section 4.1 still says nothing
  is pushed before this gate. That timing was superseded by
  Angelic's order of 24 Nov 2026 to publish the project now;
  the comparison itself and her decision at its end still
  happen at Part 6, unchanged.

## Standing items carried into Part 6 and Part 7

- The human expert check remains owed at Part 8. Reviewer 1
  recommends seeking it before Part 7's first confirmatory
  evaluation episodes. That is his recommendation, not
  Angelic's decision; it is raised once, plainly, before those
  episodes start.
- Before Part 7's analysis freezes: the frozen analysis code's
  field semantics (contact_onset_fraction, ignition_arm_a,
  contact_duration_s windows) are fixed by a hashed amendment.
  The characterisation code is not altered retroactively.
- The intact closed loop dropout baseline (2 of 20 episodes
  not persisting to the end) and the M3 named discrepancy
  travel into every Part 7 report.
