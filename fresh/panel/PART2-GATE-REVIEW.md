# Part 2 (first half) LIGHT-gate review — record

Reviewer: Reviewer 2 (rotating reviewer for this gate), 23 Nov 2026, ~20:03–20:04 WAT.
Scope: the upstream model.py reading log, the GRN/MN9/DN identity extraction with its
two-way cross-check (the formal Part 1 gate obligation), and the annotation pin position.

## Verdict: APPROVED, with three conditions

The reviewer approved the reading log (engine vs notebook-held populations; no synapse
threshold; silence() as outgoing-only; un-refractory drive; no seeds; the undefined `w`
in the reset string; run_exp's silent skip), the extraction (242 disjoint IDs, all in
the v630 set, 0 index-to-ID mismatches across all 14,687,178 edges, manifest + hashes),
and the annotation pin (identity = hashed v630 files + upstream notebooks at commit
91bdd1e; no crosswalk needed for Part 4 while it uses these ID sets).

Specific answers:
- Pickle decision (do not load the upstream sez_neurons.pickle; record and defer):
  ACCEPTED — right call on security and reproducibility grounds; the obligated
  populations do not live in the pickle, so it does not block Part 2.
- "block-output" language for silence(): ACCEPTED — outgoing-edge zeroing is the exact
  description; unqualified "silencing" would misstate the code.

## Conditions (carried into Part 2's second half)
1. Audit the `w` reset variable and the run_exp skip behaviour when building our own
   LIF code: test whether `w` has any effect in Brian2 or is a no-op/bug, and our own
   runner must never silently skip a run because an output file already exists.
2. RQ-C5 (sugar GRN right 21 vs left 10; MN9 asymmetry) stays flagged as an open
   hypothesis until Part 3 tests it.
3. The deferred Figure-2 SEZ set goes into the assumption/gap register, so it is
   neither forgotten nor loaded later without an explicit security/provenance check.

Gate status: reviewer-approved; Angelic's sign-off pending.
