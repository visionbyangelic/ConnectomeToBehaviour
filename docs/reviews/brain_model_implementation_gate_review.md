# Part 2 (second half) LIGHT-gate review — record

Reviewer: Reviewer 3 (rotating reviewer for this gate), 23 Nov 2026, ~20:21–20:23 WAT.
Scope: our own brain-model implementation (fresh/ctb/), the `w` test, the test suite
including the boolean-mask bug catch, and the smoke run's status.

## Verdict: APPROVED — Part 2 may close; Part 3 may proceed

The reviewer approved the implementation (hash-verified loading, manifested
populations, spec-traceable parameters and weight formula, seeded drive as a named
deviation, block_output semantics, per-run manifests with no-silent-skip), the `w`
verdict, the test suite and bug fix, and the smoke run as sanity-only. He called the
boolean-mask catch the most consequential finding of the report: a lesion that
silently zeroes only some selected outgoing weights can produce an apparently
successful intervention on the wrong topology.

## Conditions — all attached to Part 3, none reopening Part 2
A. FREEZE the implementation being validated: exact commit, dirty flag, environment
   versions, data hashes, ID-set manifest and configuration recorded for the Part 3
   run; code changes after the freeze are recorded and affected tests re-run; outputs
   from different revisions are never mixed.
B. PREREGISTER the comparison protocol before looking at the 30-trial results:
   stimulus and duration; driven population and input-rate convention; trial duration
   and transient/burn-in handling; neurons and output fields compared; firing-rate
   calculation and treatment of inactive neurons; summary statistics and acceptable
   tolerances. Seeded (ours) vs unseeded (upstream) means distributions and summary
   statistics are compared, never individual spike trains as if they should match.
C. Keep model-output replication separate from biological validation in all language:
   agreement with sugarR supports reproduction of the reference simulation output;
   it does not establish agreement with animal data.
D. Documentation: the `w` omission is described as removal of an ineffective
   statement (what upstream contains vs what Brian2 2.9.0 executes vs what ours
   does), never as a behavioural correction to the published model.
E. Strengthen the boolean-mask regression test before intervention results are
   relied upon: cases with multiple selected outgoing edges and a neuron with no
   outgoing edges, verifying complete before/after weight vectors.

Gate status: reviewer-approved; Angelic's sign-off pending.
