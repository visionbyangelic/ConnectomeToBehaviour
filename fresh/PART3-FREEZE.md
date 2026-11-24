# Part 3 — Implementation freeze record

**Frozen:** 23 Nov 2026, as part of Part 3 preparation (Reviewer 3, Part 2 gate condition A). **Purpose:** the validation ladder of Part 3 runs against exactly this implementation, so that every validation number can be named back to one commit, one environment, one set of data hashes. **Nothing was pushed to GitHub** — this is a local commit in the working clone; Part 6 still governs anything reaching the remote.

## The commit

| | |
|---|---|
| Commit | `0cb9b8129236dc4200b5eaa600f59ccc072263f9` |
| Subject | "Part 2: my own implementation of the brain model — seeded, hash-checked, tested" |
| Parent | `ab30ab4` (the old build's history — the fresh tree is added alongside it, nothing replaced) |
| Files | 31 files, 2,484 insertions: `fresh/ctb/` (7), `fresh/tests/` (4), `fresh/part2/` (19, including the `id_sets_v1` artefacts), `fresh/track.md` (1) |

## Frozen paths and their status

The frozen paths are `repo/fresh/ctb/`, `repo/fresh/tests/`, and `repo/fresh/part2/`. Immediately after the commit, `git status --porcelain` over those paths is **empty — clean**, verified at freeze time. Two deliberate exceptions, stated so nobody has to guess:

- **`fresh/track.md` is a living document, not a frozen path.** Its copy inside the commit is the log as of the gate closure and test strengthening; the log keeps growing after the freeze (that is its job), so the working-tree copy will legitimately differ from the committed one. Track entries never change results; code does, and the code is frozen.
- **`fresh/runs/` is uncommitted run output.** Run directories hold spike parquets (gitignored by the repo's own `*.parquet` rule) plus manifests. A run's manifest records the code commit and dirty flag at run time, which is where run provenance lives — not in git.

Two staging catches worth recording, because both would have silently corrupted the freeze:

- The repo's `.gitignore` rule `data/` matches **any** directory named `data`, including `fresh/ctb/data/` — so the loader (`ctb/data/loader.py`, the module that verifies the data hashes) was initially left unstaged by a plain `git add`. It was force-added explicitly. A freeze commit missing the loader would have been a broken promise.
- The `*.csv` rule likewise covers the `id_sets_v1` population files; they are small, versioned artefacts (242 IDs), so they were force-added deliberately. The large connectome files under `repo/data/` remain untracked, as designed.

## Environment at freeze (read live from the pinned brain env, 23 Nov 2026)

| Component | Version |
|---|---|
| Python | 3.12.3 |
| Brian2 | 2.9.0 |
| numpy | 1.26.4 |
| scipy | 1.17.1 |
| pandas | 3.0.6 |
| pyarrow | 20.0.0 |
| pytest | 9.2.0 |
| Platform | Linux x86_64 (this VM; glibc 2.39) |

## Data at freeze (hashes from the Part 1 record, `PART1-DATA.md`)

| File | SHA-256 |
|---|---|
| `2023_03_23_completeness_630_final.csv` | `e6b71e17671a9bdb05f55e4bc6774640a1418cb7a05125e0fc994ad40f9bfdfb` |
| `2023_03_23_connectivity_630_final.parquet` | `94db8c650533bc36ffa3223f2e62325d5648b8d6bd31c3a4e1c804628c7557b3` |
| `sugarR.parquet` (the Part 3 reference) | `83921d50089d966785e402d6c0e3be5ab3eba5beb680410a09c557b0f22dcc28` |

The loader re-verifies the two connectome hashes on every load and raises on mismatch, so a silent data change under a frozen commit cannot pass unnoticed.

## Identity artefacts at freeze

`repo/fresh/part2/id_sets_v1/` — 14 population CSVs + `manifest.json` (extraction date 2026-11-23; method: parsed as text from the upstream notebooks at commit `91bdd1e7dcf193f3e7ca5a8933497fcef63b7960`, cross-checked against the old build's constants and the v630 materialisation; 242 distinct IDs, zero missing from v630, zero index↔ID mismatches over all 14,687,178 edges). Record: `PART2-ID-SETS.md`. The SEZ gap (G1) stands as registered; no SEZ population is in the frozen artefacts.

## Test result at freeze

Full suite in the pinned brain env (`pytest tests/ -q` from `repo/fresh/`): **18 passed, 0 failed** (~99 s, Brian2 compilation warm). That is the Part 2 suite of 16 plus the two Part 3-preparation additions required by Reviewer 3's condition E:

- `test_block_output_full_vector_many_outgoing_edges` — a hub neuron with four outgoing edges (mixed counts/signs); the complete before/after weight vector is compared: topology identical, exactly the four outgoing weights zero, every other weight bit-identical.
- `test_block_output_neuron_without_outgoing_edges_changes_nothing` — a neuron that receives but never sends; blocking its output zeroes 0 synapses, raises nothing, and leaves the complete vector bit-identical.

One comment-only correction is also inside the frozen state: the runner's `_git_info` docstring no longer claims the fresh tree is untracked (untrue from this commit on); the manifest records whatever git reports, unedited. No behavioural code changed between the Part 2 gate review and this freeze other than the added tests.

## The post-freeze rule

1. Any change to a frozen path after this record is a **post-freeze change**: it is logged in track.md with its reason before any run uses it, the affected tests are re-run (the full suite, unless the log entry argues convincingly for a subset), and the change is committed as its own commit — never folded silently into the freeze commit's identity.
2. **Outputs are never mixed across revisions.** A run's manifest records the commit it ran under; Part 3 results are reported per revision, and if a post-freeze change lands mid-Part-3, the affected runs are re-done under the new revision or the comparison is restricted to one revision, with the choice on record.
3. The freeze does not freeze documents: the plan, the preregistration, the registers and track.md all keep moving under their own rules.
