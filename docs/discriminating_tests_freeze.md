# Discriminating-tests freeze record

**Frozen:** 26 Nov 2026 (morning), executing the checklist in §12 of `docs/discriminating_tests_preregistration.md`. **Purpose:** from this commit on, the discriminating tests (the Part 6 gate's prerequisite to Part 7) run against exactly this preregistration, this implementation, these seeds and this subset, so every later number can be named back to one frozen state. The freeze commit and the annotated tag `part6-tests-v1` are recorded in the dated note appended to this record after tagging, and in the tag annotation itself. No discriminating-test trial run had happened when this freeze executed; the freeze is the deliverable of this step.

## Item 1: Approval

The preregistration is panel-approved at commit `d5822d9` (SHA-256 `60ba4572ac88d4a9b82b67d901023ca390578529c4beb5b7427a287bc944bf78`, 211 lines): Reviewer 1 PASS on this version (26 Nov 2026, about 04:11 WAT, all five PROPOSED items approved); Reviewer 2 CONFIRM of the Pass 3 and Pass 4 changed passages (26 Nov 2026, about 04:16 WAT, his PASS on Amendment Pass 1 stands); Reviewer 3 PASS of the changed passages (26 Nov 2026, about 04:17 WAT, his approval on Amendment Pass 2 stands). The full verdicts are in `docs/reviews/gate_reviews.md`.

The owner approved the freeze of the amended draft on 26 Nov 2026, 06:36 WAT, tapping "Approve the freeze" and typing it. She also corrected the earlier reading of her conditional approval (25 Nov 2026, 23:50 WAT): she pre-approved the freeze as "freeze if he passes", and Reviewer 1 has passed, so the extra approval ask was unnecessary. The freeze proceeds on her approval of the amended draft.

Logged deviation on §12 item 1's recording location: the approval is recorded in this freeze record, in the gate log, in the decisions log and in track.md, not in the preregistration's Amendment history, because editing the panel-passed document would change its SHA-256 and void the panel's "this version only" coverage. The Part 5 freeze followed the same pattern (ratification in the freeze record).

**The expert-check condition (D6) for this freeze** is resolved by the signed waiver, in the same form as 24 Nov 2026, signed 25 Nov 2026, 22:53 WAT: "Human domain-expert check: NOT obtained. I could not reach a professional working in this field, so I proceeded on the basis of my own research and the checks I could carry out myself. Waived by Angelic Charles, 25 Nov 2026. Scope: the discriminating-tests (Part 7) freeze only. The human expert check remains owed at the Part 8 final gate." Clarifying note, 26 Nov 2026 (repeated here, as §12 item 1 requires): the waiver's scope refers to the discriminating-tests preregistration, tag part6-tests-v1, a prerequisite of Part 7. It does not cover Part 7's evaluation or analysis freeze, which needs its own waiver or the human expert-check. The human expert check remains owed at the Part 8 final gate.

## Item 2: Commit and tag

The approved preregistration is committed in the working clone at commit `d5822d9`. The tag `part6-tests-v1` (annotated) is created on the freeze commit, which is the commit carrying this record, after this record is committed. The tag name, commit hash and timestamp are recorded in the dated note appended to this record after tagging, and in the tag annotation itself. If the preregistration changes afterwards, a new tag (`part6-tests-v2`, ...) is created. A tag is never moved or deleted.

## Item 3: Frozen-implementation identity

The implementation inside this freeze is the brain-model implementation at the freeze commit, compared file by file against the Part 3 implementation freeze `0cb9b81` under the restructure mapping (`fresh/ctb/` to `src/brain_model/`, `fresh/tests/` to `tests/`, `fresh/part2/` scripts to `src/neuron_sets/`, `fresh/part2/id_sets_v1/` to `data/neuron_sets/`). §12 item 3's identity check covers content, not path, as §4 states. Every difference found is from the restructure rename only:

- `fresh/ctb/brain/runner.py` to `src/brain_model/brain/runner.py`: exactly one line, the entry-point string (`ctb.brain.runner.run_experiment` to `brain_model.brain.runner.run_experiment`).
- `fresh/ctb/brain/model.py` to `src/brain_model/brain/model.py`: docstring path references (`fresh/PART2-READING-LOG.md` to `docs/reading_log.md`, `fresh/PART2-BUILD.md` to `docs/brain_model_build.md`, `part2/w_reset_test.py` to `src/neuron_sets/w_reset_test.py`) and the Brian group names (`ctb_neurons` to `brain_model_neurons`, `ctb_synapses` to `brain_model_synapses`). The group names are identifiers only; they do not enter the numerics.
- `fresh/ctb/data/loader.py`, `fresh/ctb/__init__.py`, `fresh/ctb/README.md`, the test files and the part2 scripts: docstring, import and path references from the rename only (`ctb` to `brain_model`, `fresh/` paths to `docs/`, `src/`, `data/` paths). The part2 scripts' run-output path (`fresh/runs` to `results/validation/runs`) and the old-constants path (`repo/src/brain/constants.py` to `repo/v0-prototype/src/brain/constants.py`) are path changes only.
- `fresh/ctb/brain/__init__.py`, `fresh/ctb/data/__init__.py`, `fresh/part2/w_test_result.txt`, `fresh/part2/id_sets_v1/manifest.json` and every ID-set CSV: byte-identical.

No substantive code change was found. The anchor run (§8.1) is the empirical cross-layout check: it must reproduce the Part 3 primary (L 92.57 Hz, R 62.40 Hz) within the registered bands, and §9 step 7 names a freeze-integrity explanation if it does not.

Part 1 data-file hashes re-verified against the Part 3 freeze record (`docs/taste_conditions_freeze.md` item 3):

| File | SHA-256 | Match |
|---|---|---|
| `2023_03_23_completeness_630_final.csv` | `e6b71e17671a9bdb05f55e4bc6774640a1418cb7a05125e0fc994ad40f9bfdfb` | yes |
| `2023_03_23_connectivity_630_final.parquet` | `94db8c650533bc36ffa3223f2e62325d5648b8d6bd31c3a4e1c804628c7557b3` | yes |
| `sugarR.parquet` (reference, context only) | `83921d50089d966785e402d6c0e3be5ab3eba5beb680410a09c557b0f22dcc28` | yes |

## Item 4: Harness

The gate's analysis script is written, hashed and verified on synthetic spike tables with known rates and a known suppression ratio (including a ratio of exactly 1 and a suppressed case) before it touches any real output, per §9 step 1. The harness test runs after the tag and before the determinism check, and its hash and result are recorded in the run record before the first condition run. (At freeze time the harness is not yet run; this item is recorded as the plan, and its completion is a pre-run gate.)

## Item 5: Right subset drawn and recorded

Drawn by the approved method at freeze time, in the pinned brain env (numpy 1.26.4): `default_rng(20261134).choice(21, size=10, replace=False)`, indexing the 21 right IDs in sorted ascending order. The ordered list is pinned by its SHA-256 `9d6e69dfea39d22c9a1e2abb054229bd3fa653dbc8359f560e1db85257dc7da8` (§3). The draw indices are `[12, 6, 2, 10, 4, 20, 5, 17, 3, 16]`; the first six match the start of Reviewer 1's list under numpy 2.5.4 exactly (his full list was truncated in the page view, so only the first six were compared).

`720575940616885538, 720575940617000768, 720575940617937543, 720575940620900446, 720575940621502051, 720575940629176663, 720575940630797113, 720575940637568838, 720575940638202345, 720575940640649691`

The subset has no overlap with the left set. The numpy version used for the draw is 1.26.4 (the pinned brain env).

Composition, recorded at the freeze so that a persisting asymmetry can be examined against it. The source data carries no finer subtype label than the population: every neuron in both sets is a sugar GRN (gustatory receptor neuron, sugar-sensing), left or right side. Outgoing synapse totals are the sum of the `Connectivity` column over outgoing edges in `2023_03_23_connectivity_630_final.parquet` (the synapse count per edge; weight is count times sign times 0.275 mV):

Left set (sugar GRN, left), per neuron:

| FlyWire ID | Outgoing synapses |
|---|---|
| 720575940606801282 | 268 |
| 720575940608305161 | 226 |
| 720575940616167218 | 150 |
| 720575940617398502 | 326 |
| 720575940620296641 | 93 |
| 720575940620589838 | 346 |
| 720575940627961104 | 97 |
| 720575940629388135 | 454 |
| 720575940630968335 | 166 |
| 720575940631147148 | 169 |

Left set total 2,295, mean 229.5, min 93, max 454.

Chosen right subset (sugar GRN, right), per neuron:

| FlyWire ID | Outgoing synapses |
|---|---|
| 720575940616885538 | 261 |
| 720575940617000768 | 302 |
| 720575940617937543 | 413 |
| 720575940620900446 | 557 |
| 720575940621502051 | 240 |
| 720575940629176663 | 240 |
| 720575940630797113 | 185 |
| 720575940637568838 | 236 |
| 720575940638202345 | 394 |
| 720575940640649691 | 188 |

Right subset total 3,016, mean 301.6, min 185, max 557. For context, the full 21-neuron right set totals 7,430, mean 353.8.

## Item 6: Determinism check

Two independent 1-trial runs of the anchor configuration at seed 7180 under the frozen implementation must produce bit-identical spike tables (equal SHA-256). If they differ, STOP and diagnose before any condition runs. (At freeze time the check is not yet run; it runs after the tag and before the condition runs.)

## Item 7: Run order and seed blocks confirmed by script

The section 4 run order is: determinism check (seed 7180), anchor (7000-7029), anchor evaluated, test 1 (7030-7059), sugar 150 control (7190-7219), test 2 (7060-7089), test 3a (7090-7119), test 3b (7120-7149), test 3c (7150-7179). The runs execute sequentially with no concurrent load. The seed registry is confirmed by script, not by hand: `work/part6_tests_seed_disjointness_check.py` (SHA-256 `530a4f136611e54ccaf650c006c5006bd152d588d11e9e33d2168934d4693295`). It was re-run at freeze time against the current text, which is byte-identical to the text the tag will contain (the preregistration is unchanged since commit `d5822d9`; its SHA-256 at the tag is verified after tagging): result PASS, 53 blocks, 1210 seeds, all pairwise disjoint; manifest scan 297 JSON files under repo/results, 396 distinct seeds used, all inside listed blocks, none inside this gate's blocks. Output `work/part6_tests_seed_disjointness_output.txt` (SHA-256 `bb079c250c3ebd20b63db5c06874397aabd545ee9cf2fe2d7fda21122b727a25`), byte-identical to the pre-freeze run's output. Seed 20261125 appears once in the registry although it was used more than once as an analysis seed (its registered identity is the Part 3 gap bootstrap seed; it was also used as a synthetic-input seed for the thin slice and as the Part 6 recount seed, under separate RNG streams): the reuse is analysis-only, collides no episode stream, and is an explicit exception in the same form as seed 7180's repeated use in section 4.

## Editorial note from Reviewer 3 (non-blocking)

Reviewer 3 noted that the Amendment history says the old-ratio CI differs by "0.001 Hz", but the ratio is dimensionless, so it should read "0.001 ratio units" (or simply "0.001"). He is right, and it changes no interval or rule. The passed document is not edited to fix it, because the panel's verdicts cover this version only (commit `d5822d9`, SHA-256 `60ba4572…`) and any edit, however small, would make a new version they have not passed. The correction is recorded here and in the gate log.

## Dated note (appended after tagging)
