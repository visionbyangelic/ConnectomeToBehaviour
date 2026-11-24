# Part 3 rung 2 — Freeze record

**Frozen:** 24 Nov 2026. **Purpose:** the four-conditions ladder rung (rung 2) runs against exactly this preregistration, this implementation, this environment and these data hashes, so every rung-2 number can be named back to one commit and one tag. **Nothing was pushed to GitHub** — local commits in the working clone only; Part 6 still governs anything reaching the remote.

## The §12 freeze checklist, in order

**Item 1 — Preregistration approved. SATISFIED.** Full panel review complete (Amendment Passes 1–2; Reviewer 1's approval unconditional), the sensitivity-arms amendment confirmed by all three reviewers in the confirmation round (closed 3 of 3, no open items, 24 Nov 2026 — including Reviewer 2's CONFIRM after the arm (e) seed fix and Reviewer 1's express acceptance of the Part 5 §14 item-1 labelling treatment), and Angelic's explicit approval recorded 24 Nov 2026 (~11:34 WAT, `ANGELIC-DECISIONS.md`). The expert-check condition (D6) is **SATISFIED BY WAIVER**: no human domain-expert check was obtained; the waiver Angelic Charles signed on 24 Nov 2026 covers this freeze and the Part 5 freeze (recorded in `PART5-PREREG.md` §12 and `ANGELIC-DECISIONS.md`); the human check remains owed at the Part 8 final gate. This rung must not be described as expert-checked.

**Item 2 — Commit and tag. DONE.**

| | |
|---|---|
| Preparatory commit | `8651251` — "Parts 2b-5: loop builds, qualification-gate artefacts and track-log catch-up ahead of the rung-2 freeze" (the pending Part 3 §13 note, track-log catch-up, and the Part 2b / Part 5 / qualification-gate working state, committed so the freeze tree is clean) |
| Freeze commit | `b62a0fe70671a1f789e97ba7992120d060aae27a` — "Part 3 rung 2: freeze the four-conditions preregistration as approved (with the sensitivity-arms amendment)" |
| Freeze commit contents | `fresh/PART3-RUNG2-PREREG.md` only — byte-identical to the approved document (`cmp` verified against `~/workspace/connectome-work/fresh/PART3-RUNG2-PREREG.md`) |
| Tag | `part3-rung2-v1` (annotated), created 24 Nov 2026, 11:51:25 WAT (commit timestamp 2026-11-24T10:51:25Z) |
| Working tree at freeze | Clean (`git status --porcelain` empty) |

This is the first rung-2 tag ever created; no tag was moved or deleted. Nothing pushed.

**Item 3 — Frozen-implementation identity. VERIFIED.** `git diff 0cb9b8129236dc4200b5eaa600f59ccc072263f9..b62a0fe` over `fresh/ctb/`, `fresh/tests/`, `fresh/part2/` is **empty** — the implementation inside this freeze is byte-identical to the Part 3 implementation freeze. Part 1 data hashes re-verified against `PART3-FREEZE.md`:

| File | SHA-256 | Match |
|---|---|---|
| `2023_03_23_completeness_630_final.csv` | `e6b71e17671a9bdb05f55e4bc6774640a1418cb7a05125e0fc994ad40f9bfdfb` | ✓ |
| `2023_03_23_connectivity_630_final.parquet` | `94db8c650533bc36ffa3223f2e62325d5648b8d6bd31c3a4e1c804628c7557b3` | ✓ |
| `sugarR.parquet` (reference, context only) | `83921d50089d966785e402d6c0e3be5ab3eba5beb680410a09c557b0f22dcc28` | ✓ |

**Item 4 — Harness hashed and synthetically tested. DONE.** The rung-2 analysis script was verified on synthetic spike counts with known rates and known suppression ratios **before** touching any real output — all cases passed: a known constant rate recovered exactly (50.0 Hz, degenerate CI); active counts at the three §7 thresholds recovered exactly; a suppression ratio of exactly 1 classified equivalence; an exactly-half suppressed case (ratio 0.5) classified suppression; the pre-written mixed headline produced on a fabricated contrary per-side CI; difference CIs exact on identical and constant-shifted arrays; the Holm procedure checked on a known example.

| Artefact | SHA-256 |
|---|---|
| `work/analyze_rung2.py` (analysis) | `2cfea92b0ac4f5560225942f2f7e2b006c37eedb740afba8422d35bd8daa6294` |
| `work/run_rung2.py` (run driver) | `91ea95d298455934dea570097e14b8a557e3256caa625e61835465eb1aeb1b30` |
| `work/seed_disjointness_check.py` | `9d940da95029edc0873d7eed6516016e673c8f7ace85dc08f97e385c82536622` |

**Seed disjointness (Reviewer 1's mechanical check, confirmation round).** The script above parses the Part 5 §7 allocation table and this rung's §4 allocation paragraph out of the documents, adds the historical blocks of the closed parts, and asserts pairwise disjointness over the registered sets: **28 blocks, 684 seeds, PASS** (output recorded verbatim in the panel log's confirmation-round entry; the sub-seed stream 5701, 5702, … is modelled bounded by the next allocated block, 5800, as recorded there).

**Item 5 — Multi-entry stimulus verification. VERIFIED** (24 Nov 2026, before approval; recorded in the preregistration's §12 item 5: the frozen runner accepts two simultaneous stimulus entries with no code change; non-rung harness run at throwaway seed 9998 produced 823 sugar-population and 844 bitter-population spikes; artefacts in `work/rung2_verify/`).

**Item 6 — Timestamps.** Approval: 24 Nov 2026, ~11:34 WAT. Confirmation round closed: 24 Nov 2026 (before the freeze). Freeze commit and tag: 24 Nov 2026, 11:51:25 WAT. Determinism check and condition runs: recorded in `PART3-RUNG2-RESULTS.md`.

**Item 7 — Determinism check. PASSED** (24 Nov 2026, after the freeze, before the condition runs). Two independent 1-trial runs of the sugar configuration at seed 6220, run_id `part3-rung2-determinism-check`, under separate out-roots (`fresh/runs/rung2-det-a/`, `fresh/runs/rung2-det-b/`): both spike tables **bit-identical, SHA-256 `f8a537c906bfc05d0b1892bfcdad1befe5c8b6e95a3a950322f589b928a841d9`** (17,389 spikes each); both manifests show the freeze commit `b62a0fe…` and `working_tree_dirty: false`.

## Environment at freeze

The pinned brain env, unchanged from the Part 3 freeze (Python 3.12.3, Brian2 2.9.0, numpy 1.26.4, scipy 1.17.1, pandas 3.0.6, pyarrow 20.0.0). Runs execute through the frozen runner `ctb.brain.runner.run_experiment`; the driver adds no behaviour of its own.

## Addendum — execution stopped after the anchor (24 Nov 2026)

The rung began executing under this freeze on 24 Nov 2026: determinism check PASSED (bit-identical, SHA-256 `f8a537c9…`); sugar condition ran (506,683 spikes, 443 active); **the §8.1 anchor PASSED** (ΔL +1.07 [−1.23, +3.40] vs band ±23.14; ΔR −0.93 [−3.53, +1.53] vs band ±15.60; L > R preserved; no discrepancy); bitter condition ran (192,720 spikes, 94 active; MN9 0.00 Hz both sides, descriptive). The first sugar+bitter attempt was **killed by the shared machine** (SIGKILL under CPU throttling and memory contention; empty run directory — a void attempt under §4, logged; a labelled six-trial diagnostic completed cleanly at ≈17.5k spikes/trial, so the condition is not intrinsically heavy). Before its re-run, the owner's publication decision added two commits on top of this freeze commit (`25c649f`, `5ad2baa`; HEAD now `5ad2baacec7f3c2901d86d8de22ddbf0c31e29e3`), so §5's manifest premise (freeze commit, clean tree) can no longer be met in the main tree and **execution stopped with seven condition runs outstanding**. The frozen paths at the new HEAD remain byte-identical to `0cb9b81`, and this freeze's tag is unmoved. Full record: panel log, "RUNG 2 FREEZE AND EXECUTION" (24 Nov 2026). The remaining runs await a ruling (separate checkout pinned at this commit, or a formal amendment to §5).

## Addendum 2 — the remaining runs execute from a worktree at this freeze commit (24 Nov 2026)

**Ruling (parent decision, no amendment).** Option (a) from the stop record was chosen: the seven outstanding runs execute from a **git worktree pinned at this freeze commit** — `~/workspace/connectome-work/rung2-worktree`, detached HEAD `b62a0fe70671a1f789e97ba7992120d060aae27a`, working tree clean. A worktree at `b62a0fe` *is* the freeze commit with a clean tree, so §5 is satisfied as written; the preregistration is not amended, and no run executes from the main tree (HEAD `5ad2baa…`).

**Arrangement, verified before the first re-run.** The frozen runner derives the manifest's git info from the code's own repo root (`ctb/brain/runner.py`: `Path(__file__).resolve().parents[3]`), so importing `ctb` from the worktree makes each manifest record `repo_commit = b62a0fe…`, `working_tree_dirty = false` — verified directly against the worktree before any run (`_git_info` returned exactly that pair). Code and the Part 2 id sets come from the worktree (its `fresh/ctb`, `fresh/part2`, `fresh/tests` verified byte-identical to the Part 3 implementation freeze `0cb9b81`: diff empty). `data/` is not tracked, so the worktree has none: `data_dir` points at the main repo's Part 1 data, whose hashes were re-verified against this record (completeness `e6b71e17…`, connectivity `94db8c65…`) and are re-verified by the loader on every run and recorded in every manifest. Run outputs land in the main repo's `fresh/runs/` alongside sugar and bitter (`fresh/runs/` is gitignored in both trees). The driver is `work-rung2/run_rung2_wt.py` (SHA-256 `7461971e…`) — the verified run driver (`work/run_rung2.py`, `91ea95d2…`) with only the path arrangement and the sugar+bitter re-run's run_id changed. Sugar+bitter runs as `part3-rung2-sugarbitter-rerun1` (new run_id per §4's void rule, same seeds 6160–6189); attempt 1 stays on record as void.

## Addendum 3 — execution complete (24 Nov 2026)

All seven outstanding runs executed from the worktree under the Addendum 2 arrangement, and every manifest records this freeze commit with a clean tree. Four attempts were voided by the machine (two SIGKILLs under memory contention, two machine restarts; each left an empty run directory) and re-run under new run_ids with the same seeds per §4: sugar+bitter as `part3-rung2-sugarbitter-rerun1`, the sugar+bitter @ 100 Hz arm as `part3-rung2-sugarbitter100-rerun1`, and the bilateral condition as `part3-rung2-bilateral-rerun2` (after two void attempts). The anchor passed (§8.1), the suppression comparison's outcome is suppression (§8.3), all six §8.2 differences are claimed, and the rung is **complete under §8.4 with its record complete as amended under §8.5**. Full record: `PART3-RUNG2-RESULTS.md` (computed per preregistration, gate pending) and the panel log.

## Addendum 4: the GitHub push, recorded for the gate (24 Nov 2026)

This record's opening line ("Nothing was pushed to GitHub") stated the position at freeze time; it is superseded by events and is annotated here rather than rewritten. On the owner's direct order of 24 Nov 2026, the repository was pushed to GitHub main ahead of the original plan's timing, under which nothing was to be pushed until the Part 6 checkpoint. The push preserved the first build in full: on the annotated tag `v0-prototype-final`, which marks commit `ab30ab4` (the last old-build commit), and as the `v0-prototype/` folder, with the first build's original README preserved byte-identical as `v0-prototype/README-original.md` (SHA-256 `ca186f1b…`, verified against `ab30ab4:README.md`). The deviation is one of timing only: it was recorded at the time in `ANGELIC-DECISIONS.md` ("Publication moved forward", 24 Nov 2026) as a timing-only change, with the Part 6 comparison itself unchanged and still blind; the owner's order is the ratification of the deviation. This does not affect the validity of the rung result: the freeze commit and tag never moved, every condition run's manifest records the freeze commit with a clean tree (the later runs under the Addendum 2 worktree arrangement), and no rung artefact was altered by the push. The same process item is recorded in the panel log's gate section.
