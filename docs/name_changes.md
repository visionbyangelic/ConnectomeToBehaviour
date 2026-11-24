# Name changes: the repository rearrangement of 24 Nov 2026

On 24 Nov 2026 I rearranged this repository to follow the arrangement of my
fatigue-detection project, and I did it immediately rather than at Part 8 as
previously planned. The old layout put everything under one folder called
`fresh/`, with stage-numbered file names (`PART3-RUNG2-RESULTS.md`,
`FEEDING-BODY-QUALIFICATION.md`) and code folders named for stages
(`part2b/`, `qualgate/`) or initials (`ctb/`). A reader could not tell what
anything was from its name. The new layout: the plan and the build log at
the root, every document in `docs/` under a descriptive name that says what
the document is, the code in `src/` in packages named for what they do, and
the recorded outputs in `results/`. No file or folder is named after me,
and no file names a tool; the reviewers are Reviewer 1, Reviewer 2 and
Reviewer 3.

Every move was made with `git mv`, so each file's history follows it. The
frozen tags (`part3-prereg-v2`, `part3-rung2-v1`) were not moved: they point
at the trees they froze, which keep the old layout, and that is expected.
`v0-prototype/` was not touched. Code imports and path references were
updated throughout, and the proof that nothing broke is the test record:
the brain model suite (18 tests), the first loop suite (16 tests) and the
closed loop suite (37 tests) all pass exactly as before the rearrangement,
and the body-side modules import cleanly in the pinned body environment.

Historical documents keep the citations they were written with; this record
is the key for following an old name to its new one. One live document was
updated in place: the closed-loop preregistration's paths and citations now
point at the new locations, recorded as a dated editorial amendment in its
own amendment history (no registered content changed).

## Root

| Before | After |
|---|---|
| `fresh/track.md` | `track.md` |
| `fresh/FINAL-PLAN.md` | `PLAN.md` |
| `fresh/FINAL-PLAN.pdf` | `docs/final_plan.pdf` |

## Documents: `fresh/` to `docs/`

| Before | After |
|---|---|
| `PART0-PACKAGE.md` | `docs/project_foundations.md` |
| `PART0-PREP.md` | `docs/preparation_notes.md` |
| `PART0-BENCHMARK.md` | `docs/benchmark_results.md` |
| `RESEARCH-CHECK.md` | `docs/research_check.md` |
| `PART1-DATA.md` | `docs/connectome_data.md` |
| `PART1-ENVIRONMENTS.md` | `docs/environments.md` |
| `PART1B-AUDIT.md` | `docs/body_audit.md` |
| `PART2-BUILD.md` | `docs/brain_model_build.md` |
| `PART2-ID-SETS.md` | `docs/neuron_sets.md` |
| `PART2-READING-LOG.md` | `docs/reading_log.md` |
| `PART2B-BUILD.md` | `docs/first_loop_build.md` |
| `PART3-PREREG.md` | `docs/brain_validation_preregistration.md` |
| `PART3-FREEZE.md` | `docs/brain_validation_freeze.md` |
| `PART3-RESULTS.md` | `docs/brain_validation_results.md` |
| `PART3-RUNG2-PREREG.md` | `docs/taste_conditions_preregistration.md` |
| `PART3-RUNG2-FREEZE.md` | `docs/taste_conditions_freeze.md` |
| `PART3-RUNG2-RESULTS.md` | `docs/taste_conditions_results.md` |
| `PART4-SENSORY-SPECS.md` | `docs/sensory_specifications.md` |
| `FEEDING-BODY-QUALIFICATION.md` | `docs/feeding_body_qualification.md` |
| `ACCEPTANCE-TEST.md` | `docs/resting_acceptance_test.md` |
| `THIN-SLICE.md` | `docs/thin_slice_test.md` |
| `REACH-CURVE-CALIBRATION.md` | `docs/reach_curve_calibration.md` |
| `PART5-BUILD.md` | `docs/closed_loop_build.md` |
| `PART5-PREREG.md` | `docs/closed_loop_preregistration.md` |
| `ANGELIC-DECISIONS.md` | `docs/decisions_log.md` |
| `EXPERT-CHECK-MAIL.md` | `docs/expert_check_mail.md` |
| `LICENCES.md` | `docs/licences.md` |

## Review records: `fresh/panel/` to `docs/reviews/`

| Before | After |
|---|---|
| `PART4-GATE-REVIEW.md` | `docs/reviews/gate_reviews.md` (the running gate log) |
| `PART0-SOURCE-CHECK.md` | `docs/reviews/source_check.md` |
| `PART1-GATE-REVIEW.md` | `docs/reviews/data_gate_review.md` |
| `PART1B-GATE-REVIEW.md` | `docs/reviews/body_audit_gate_review.md` |
| `PART2-GATE-REVIEW.md` | `docs/reviews/model_reading_gate_review.md` |
| `PART2B-GATE-REVIEW.md` | `docs/reviews/brain_model_implementation_gate_review.md` |
| `PART2B-LOOP-GATE-REVIEW.md` | `docs/reviews/first_loop_gate_review.md` |
| `PART3-PREREG-REVIEW.md` | `docs/reviews/brain_validation_preregistration_review.md` |
| `PART3-PREREG-CHANGED-PASSAGES.md` | `docs/reviews/brain_validation_preregistration_amendment_pass2_passages.md` |
| `PART3-PREREG-PASS3-CHANGES.md` | `docs/reviews/brain_validation_preregistration_amendment_pass3_changes.md` |
| `PASS6-REVISED-TEXT.md` | `docs/reviews/sensory_specifications_pass6_revised_text.md` |
| `REVIEWER-1-REVIEW.md` | `docs/reviews/final_plan_review_reviewer_1.md` |
| `REVIEWER-2-REVIEW.md` | `docs/reviews/final_plan_review_reviewer_2.md` |
| `REVIEWER-3-REVIEW.md` | `docs/reviews/final_plan_review_reviewer_3.md` |
| `FINAL-APPROVAL-reviewer-1.md` | `docs/reviews/final_plan_approval_reviewer_1.md` |
| `FINAL-APPROVAL-reviewer-2.md` | `docs/reviews/final_plan_approval_reviewer_2.md` |
| `FINAL-APPROVAL-reviewer-3.md` | `docs/reviews/final_plan_approval_reviewer_3.md` |
| `FINAL-APPROVAL-STATUS.md` | `docs/reviews/final_plan_approval_status.md` |

Earlier the same day, six of these files still carried tool names and were
renamed to reviewer numbers first (`CLAUDE-REVIEW.md` to
`REVIEWER-1-REVIEW.md`, and the five like it); that step is recorded in
`track.md`, and the table above gives the final names.

## Code: `fresh/` to `src/`, and the data sets to `data/`

| Before | After |
|---|---|
| `fresh/ctb/` (package `ctb`) | `src/brain_model/` (package `brain_model`) |
| `fresh/part2/` (scripts) | `src/neuron_sets/` |
| `fresh/part2/id_sets_v1/` | `data/neuron_sets/` |
| `fresh/part3/` | `src/validation/` |
| `fresh/part2b/` | `src/first_loop/` |
| `fresh/part5/` | `src/closed_loop/` |
| `fresh/qualgate/` | `src/body_qualification/` |
| `fresh/tests/` | `tests/` |

## Recorded outputs: to `results/`

| Before | After |
|---|---|
| `fresh/qualgate/results/` | `results/body_qualification/` |
| `fresh/part2b/runs/` | `results/first_loop/` |
| `fresh/part5/runs/` | `results/closed_loop/` |
| `fresh/part3/reference_only_values.json` | `results/validation/reference_only_values.json` |
| `fresh/runs/` (never committed) | `results/validation/runs/` (still not committed) |
