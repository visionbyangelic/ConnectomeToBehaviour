# Part 2 (second half) — Build report: our own implementation of the brain model

**Built:** 23 Nov 2026, after Angelic signed off Part 2's first half (Reviewer 2 approved with three conditions — all three are discharged in this half, see §5). **Code:** `repo/fresh/ctb/` (package), `repo/fresh/tests/` (suite), `repo/fresh/part2/` (the `w` experiment + the smoke-run script), first run output in `repo/fresh/runs/part2-smoke-sugar-seed0/`. Nothing pushed to GitHub. Implemented from the reading log's specification (`PART2-READING-LOG.md`); upstream code was never copied, imported, or executed, and `sez_neurons.pickle` was never loaded.

## 1. Module map

| Module | What it does |
|---|---|
| `ctb/data/loader.py` | Loads the v630 completeness CSV + connectivity parquet **only after SHA-256 verification against the Part 1 record** (raises `DataHashMismatch` otherwise). Holds the index↔ID convention (Brian index = completeness row order), `check_index_consistency`, and `load_populations`, which reads the `id_sets_v1` artefacts and validates every count against their manifest. |
| `ctb/brain/model.py` | The model. `DEFAULT_PARAMS` (the paper's values, sources in comments), the LIF equations, `synapse_weights` (count × sign × 0.275 mV, computed from the component columns), and `Brain`: `build()` (seeded construction of neurons + all 14,687,178 synapses + spike monitor), `add_drive()` (upstream-style Poisson drive), `block_output()` (zeroes outgoing weights — honestly named), `run()`, `spikes()`. |
| `ctb/brain/runner.py` | `run_experiment(config, out_root)`: builds a fresh seeded `Brain` per trial (seed = config seed + trial), applies blocks then drives, writes `runs/<run_id>/spikes.parquet` (upstream output schema: `t, trial, flywire_id, exp_name`) + `manifest.json` (config, seeds, code commit + dirty flag, data hashes, package versions, wall clock, output hash). **Refuses, with `FileExistsError`, to write into a non-empty run directory.** |
| `ctb/README.md` | Package guide + the named deviations, in short form. |
| `tests/` (16 tests) | See §4. |
| `part2/w_reset_test.py` + `w_test_result.txt` | The `w` experiment (§2). |
| `part2/smoke_sugar.py` | The smoke run (§6). |

## 2. The `w` verdict (Reviewer 2, condition 1 — first half)

**The clause is a silent no-op in Brian2 2.9.0.** Three variants of a small network in upstream's exact shape (equations, namespace style, reset) were run at the pinned Brian2 2.9.0, seed fixed:

- Reset `'v = v_rst; w = 0; g = 0 * mV'` with synapses present: **no error, no warning about `w`** (only unrelated pyparsing deprecation notices from Brian2 internals), and the neuron group has **no variable named `w`** afterwards. 44 spikes.
- Reset without the clause: **bit-identical spike train** (same seed) — 44 spikes, same neurons, same times.
- The clause with no synapses at all: also silently accepted.

So Brian2 drops the assignment to the undefined variable without a word, and the published results were never affected by it. Our reset is `'v = v_rst; g = 0 * mV'` — identical dynamics, nothing undefined — and a unit test pins that string so the clause cannot creep back in unnoticed.

## 3. Deviations from upstream — named, with reasons

| # | Deviation | Reason |
|---|---|---|
| 1 | **Seeded runs.** Seed is a build/run parameter, recorded in every manifest; same seed + same stimulus ⇒ identical spike trains (tested). | Upstream has no seeds anywhere, so its individual runs are unrepeatable in principle. Ours must be repeatable; the cost is that comparisons against upstream outputs are statistical (distributional), never spike-for-spike — which Part 3's criteria already assume. |
| 2 | **Reset string omits `w = 0`.** | §2: the clause is undefined in the neuron equations and provably inert at Brian2 2.9.0. Keeping it would carry a silent no-op that a future Brian2 version might start erroring on — or worse, start honouring. |
| 3 | **`block_output`, not "silence".** Zeroes outgoing weights only; the neuron still receives input and spikes (functionally tested: a blocked driven neuron fires exactly as before and drives nothing). | That is what upstream's `silence()` does; its README's "to and from" misstates the code. Intervention conclusions in Parts 5/7 will be worded for output-blocking. Input-blocking and full ablation are different operations and are not smuggled into this one. |
| 4 | **Hash-verified loading.** The loader refuses data whose SHA-256 differs from the Part 1 record. | Upstream reads whatever it is pointed at. A silent upstream file change would otherwise change the connectome under every result. |
| 5 | **No-skip runner.** Existing non-empty run directory ⇒ `FileExistsError`. A re-run is a new run_id, chosen on the record. | Upstream's `run_exp` silently returns when its output exists, letting a stale file stand in for a run (Reviewer 2, condition 1 — second half). |
| 6 | **`on_pre='g_post += w'`** instead of upstream's bare `'g += w'`. | Same variable (Brian2 resolves the bare name to the postsynaptic side); the direction is written out so nobody has to know the resolution rule to read the model. |
| 7 | **Weights computed from the count and sign columns**, not from the file's precomputed `Excitatory x Connectivity` column. | The precomputed column is kept as a cross-check (sampled audit, §4); building from components is what makes a disagreement between them visible instead of inherited. |

Everything else follows the specification as read: no synapse threshold (all 14,687,178 edges), the drive injecting into `v` at 68.75 mV per event with the driven neurons' refractory period removed, per-neuron `PoissonInput` objects (Brian2 subgroups must be contiguous — a scattered population cannot be targeted at once, which is presumably why upstream loops too), the refractory period as a per-neuron state variable, `method='linear'`, dt 0.1 ms, one fresh network build per trial.

## 4. Tests — 16 passed, 0 failed

Suite: `repo/fresh/tests/`, run with the pinned brain env (`pytest tests/ -q` → **16 passed** in ~10–20 s once Brian2's code cache is warm; first-ever run ~2 min, most of it Brian2 compilation).

- **Loader (6):** data files match the Part 1 SHA-256 record; counts match Part 1 exactly (127,400 neurons; 14,687,178 edges; 52,793,639 synapses; 4,770,900 edges ≥3); index↔ID consistency re-verified over all edges (0 mismatches); populations match the `id_sets_v1` manifest with 242 distinct IDs; MN9 order is left-then-right; a non-v630 ID raises a named `KeyError`.
- **Model (7):** weight formula exact on a hand-built network (10×+1×0.275, 4×−1×0.275, …); **sampled sign audit** — our count×sign product reproduces the file's own `Excitatory x Connectivity` column on 2,000 random edges (plan Part 2 pass criterion, sampled form); reset string pinned clean; **silent network = 0 spikes** in 100 ms (plan pass criterion); **single-neuron response** — a driven neuron fires at ≈ the drive rate (≥20 spikes in 200 ms at 150 Hz), undriven edgeless neurons fire 0 (plan pass criterion); `block_output` zeroes *exactly* the target's outgoing weights (count and identity checked, incoming and unrelated weights untouched); blocked neuron still spikes, downstream stays silent.
- **Runner (3):** a run writes the spike table (upstream schema) + a complete manifest (seeds, trial seeds, output SHA-256, config, versions); re-running into the same run_id raises `FileExistsError`; two runs with the same seed produce **identical** spike tables.

**Three bugs the tests caught before any science depended on them** (all fixed, all recorded here because that is what the tests are for):
1. `block_output`'s first version assigned through a **boolean mask** on the Brian2 synapse variable — and Brian2 silently under-applied it: edge 0→1 was zeroed, edge 0→2 kept its weight. A lesion that half-applies, silently, is exactly the failure mode this project exists to avoid. Fixed with explicit integer indices (`np.flatnonzero`); the exactness test now guards it.
2. `syn.connect` with float64 index arrays (an empty fixture's default dtype) raises — indices are now cast to int64 in `build`, so the model does not depend on the caller's dtypes.
3. An edge-less connectome needs two Brian2 accommodations: skip `connect()` (zero-size arrays raise) and mark the `Synapses` inactive (an unconnected `Synapses` in a `Network` raises at run time). Both handled in `build`, with comments.

One more construction lesson, from the smoke run's first attempt: `add_drive` initially targeted a whole population as one subgroup; Brian2 subgroups must be contiguous, so the drive is built per neuron — as upstream does it.

## 5. Reviewer 2's three conditions — status

1. **`w` audit + no-skip runner:** done — §2 and deviation 5; both behaviours are pinned by tests.
2. **RQ-C5 stays an open hypothesis until Part 3:** recorded in the assumption register addendum (below) and in track.md; the smoke run's MN9 numbers (§6) are labelled sanity-only and are not an asymmetry claim.
3. **SEZ set into the gap register:** done — dated addendum appended to `PART0-PACKAGE.md` §1 (entry **G1**, appended rather than edited into v1), recording that the Figure 2 SEZ sets remain unextracted, why, what breaks if the gap is mishandled, and the two authorised ways to close it later. The same addendum carries the RQ-C5 cross-reference.

## 6. Smoke run — SANITY SIGNAL ONLY, not a validation result

`part2/smoke_sugar.py`: full v630 network, right sugar GRNs (21) at 150 Hz, 1 trial × 1.0 s, seed 0 → `runs/part2-smoke-sugar-seed0/` (manifest records data hashes, seed, code commit, wall clock 103.2 s; whole process ~114 s).

- Total spikes: **13,698**; active neurons: **375**.
- **MN9 left: 80 spikes = 80.0 Hz. MN9 right: 64 spikes = 64.0 Hz.**

Why this is sane, and no more than sane: the reference file's own trials average ~17,052 spikes and ~403 active neurons, with MN9 at 93.3 Hz (L) / 61.8 Hz (R) — a single seeded trial of our build lands in the same range, with the same left-dominant direction. One trial at one seed cannot validate anything; the distributional comparison against `sugarR` under pre-registered criteria is Part 3's work, and RQ-C5 (whether the asymmetry is circuit, set-size artefact, or bug) stays open until then, per condition 2.

## 7. Surprises

- The boolean-mask bug (§4) is the headline: Brian2 accepted the assignment, returned no error, and zeroed only part of the selection. Without an exactness test, `block_output` would have shipped broken in the worst possible way — quietly.
- Brian2's silence about the undefined `w` (§2) is the same species of surprise, inherited from upstream: two silent no-ops around the exact operations (reset, lesioning) whose correctness the intervention experiment rests on. Both are now pinned by tests.
- Nothing about the full-scale build surprised: 14.7M synapses connect and a 1 s trial runs in ~103 s end-to-end on this VM, consistent with the Part 0/1 benchmarks.

**Part 2 (second half) is complete.** Next per the plan: Part 2b's minimal end-to-end loop, and Part 3's pre-registered validation ladder — each with its own gate. Nothing has been pushed to GitHub.
