# Part 2 — Neuron ID sets: extraction, cross-checks, and the annotation pin

**The obligation (Reviewer 3, Part 1 gate):** extract and independently cross-check the GRN, MN9 and DN neuron ID sets using the v630 materialisation and the selection logic in `model.py`; record method, source references, counts and versioned artefacts; complete before any downstream use of these populations; any mismatch investigated and recorded, never silently resolved.

**Headline result: the extraction is clean.** Every population the published experiments use was extracted, every extracted ID is present in the v630 materialisation, the connectivity file's index↔ID mapping — which `model.py` trusts silently — was verified over all 14,687,178 edges with **zero mismatches**, and the independently written old-build constants agree with the notebook lists on every set they share. The one thing that could not be extracted is recorded as a gap with its reason (§5), not worked around.

## 1. Method

`model.py` contains no populations: `run_exp` takes FlyWire ID lists from its caller (see `PART2-READING-LOG.md`). The selection logic, such as it is, is *literal lists written into the upstream notebooks*. The extraction therefore:

1. Parsed `example.ipynb` and `figures.ipynb` **as text** (they are JSON) and pulled out every named ID list and single-neuron assignment. Nothing upstream was executed: no import of `model.py`, no notebook cells run, and `sez_neurons.pickle` was **not** loaded (a pickle is executable code; the file also failed an execution-risk check — see §5).
2. Required every repeated definition of the same list (the sugar list is written out four times across the notebooks) to be **identical** — order and content.
3. Cross-checked two independent ways (the obligation's two-way requirement):
   - **Against the old build's constants** (`src/brain/constants.py`), a separate transcription made from the paper at a different time;
   - **Against the v630 materialisation itself** (the hashed Part 1 files in `repo/data/`): membership of every ID, plus the full index↔ID correspondence check.
4. Saved the sets as versioned artefacts (§4) with a manifest.

Extraction script: `repo/fresh/part2/extract_id_sets.py` — written for this part, commented, re-runnable. It was run 23 Nov 2026 with the pinned brain env (pandas 3.0.6 / pyarrow 20.0.0 / numpy 1.26.4).

## 2. The sets

Sensory input populations (the GRNs and their mechanosensory counterparts):

| Set | Notebook name | Count | Defined in |
|---|---|---|---|
| Sugar GRNs, right | `neu_sugar` | 21 | example.ipynb cell 3; figures.ipynb cells 4, 23, 44 (identical all four times) |
| Sugar GRNs, left | `neu_sugar_left` | 10 | figures.ipynb cell 76 |
| Bitter GRNs | `neu_bitter` | 21 | figures.ipynb cell 23 |
| Water GRNs | `neu_water` | 18 | figures.ipynb cell 32 |
| Ir94e GRNs | `neu_ir94e` | 18 | figures.ipynb cell 23 (the second input class of the Fig. 3 interaction experiments) |
| JON-CE | `neu_JON_CE` | 70 | figures.ipynb cell 50 |
| JON-F | `neu_JON_F` | 60 | figures.ipynb cell 50 |
| JON-D (m) | `neu_JON_D_m` | 16 | figures.ipynb cell 50 |
| JON, all | `neu_JON_all` | 146 | constructed in cell 50 as CE + F + D_m, exactly as extracted |

Readout / motor / descending neurons:

| Set | Notebook name | IDs | Defined in |
|---|---|---|---|
| MN9 (proboscis-extension motor neuron) | `ids_mn9` | left 720575940660219265, right 720575940645521262 | figures.ipynb cell 17 ("# left and right", in that order); the left ID alone appears as `id_mn9` in example.ipynb cell 17 and figures.ipynb cells 8, 23, 36 |
| aDN1 | `id_DN1_1` | 720575940616185531 | figures.ipynb cells 54, 81 |
| aDN2, left | `id_DN2_l` | 720575940629806974 | figures.ipynb cells 54, 81 |
| aBN1 | `id_aBN1` | 720575940630907434 | figures.ipynb cell 62 |
| Three inhibitory (silenced in the JON-F experiment) | `three_inhibitory` | 720575940636066222, 720575940609957315, 720575940624986407 | figures.ipynb cell 70 |

On the obligation's "DN sets": the upstream model defines **no brain-wide DN population**. The descending neurons the published experiments actually use are the two readouts above, aDN1 and aDN2 (left) — the antennal-grooming descending neurons of the JON experiments. They are extracted and cross-checked here; any wider DN set would be a new, annotation-based construction (see §6), not something the upstream model contains.

Totals: **242 distinct FlyWire IDs** across all extracted sets. The sets are pairwise disjoint — no sensory set shares a neuron with another, and none of the readout neurons appears in any input set. The only overlaps found anywhere are the definitional ones (the left MN9 is a member of the MN9 pair; the three JON subsets are members of JON-all).

## 3. Cross-check results

**Notebook self-consistency:** every repeated definition identical (sugar ×4, MN9-left ×4, DN readouts ×2). No discrepancies.

**Old-build constants (independent transcription):** all seven comparisons **MATCH** — `SUGAR_GRNS_RIGHT`, `SUGAR_GRNS_LEFT`, `BITTER_GRNS`, `WATER_GRNS` (set equality), the MN9 pair including left/right order, `DN1_1`, `DN2_L`. The old build's constants and the upstream notebooks were written from the same paper at different times and agree everywhere they overlap.

**v630 membership:** all 242 extracted IDs are present in the completeness file's ID set (127,400 neurons). Zero missing. This matters mechanically, not just tidily: `run_exp` converts IDs to indices through the completeness order and would raise a bare `KeyError` on a missing ID — and would *not* raise anything on a wrong-but-present ID, which is why the transcription cross-check above had to pass too.

**Index↔ID correspondence (the silent assumption):** for every one of the 14,687,178 connectivity rows, `completeness_id[Presynaptic_Index] == Presynaptic_ID` and `completeness_id[Postsynaptic_Index] == Postsynaptic_ID` — **0 mismatches, pre and post**. The mapping `model.py` relies on without checking is exactly true for the hashed Part 1 files.

**Discrepancy record for this extraction: none found.** No ID was dropped, substituted, or resolved by hand at any point; had any check failed, the failing IDs would be listed here instead of this sentence.

## 4. Artefacts (versioned, as the obligation requires)

`repo/fresh/part2/id_sets_v1/` — one CSV per population (`sugar_grn_right.csv`, `sugar_grn_left.csv`, `bitter_grn.csv`, `water_grn.csv`, `ir94e_grn.csv`, `jon_ce.csv`, `jon_f.csv`, `jon_d_m.csv`, `jon_all.csv`, `mn9.csv`, `adn1.csv`, `adn2_left.csv`, `abn1.csv`, `three_inhibitory.csv`) plus `manifest.json` recording: extraction date (2026-11-23), method, upstream repo and commit (`91bdd1e7dcf193f3e7ca5a8933497fcef63b7960`), `model.py` SHA-256 (`fc45837d7122c6ce2a7f3f2f23c515992e4b232aadb919efabb72337fac88e4e`), SHA-256 of both data files (matching the Part 1 record: completeness `e6b71e17…fbfdfb`, connectivity `94db8c65…7557b3` — recomputed during extraction and identical), per-population counts, all check results, and the §5 gap. Downstream parts cite these files, not the notebooks.

## 5. The one gap, recorded plainly: the SEZ sets

The Figure 2 experiments drive SEZ (subesophageal-zone) neuron types taken from `sez_neurons.pickle` (`types_and_ids`, figures.ipynb cell 17). That pickle is the **only** place those sets exist — there is no text source for them anywhere in the repository, and the file is a binary pickle: loading it executes code, and it failed an execution-risk check on this machine. It was not loaded, and the SEZ sets are **not extracted**.

Consequences, stated rather than smoothed over: the obligation's named populations (GRNs, MN9, DNs) are fully discharged — none of them lives in the pickle. The SEZ sets are input populations for one figure's worth of published experiments; they become necessary only if a later part reproduces the Figure 2 battery or needs SEZ types for the decoder design. At that point the options are: Angelic explicitly authorises loading the pickle in a quarantined environment; or the sets are reconstructed from the paper's SEZ type descriptions against an annotation source (which raises the §6 crosswalk problem). Either way it is a decision on record when it is taken, not a silent load. The Part 5 decoder work should treat this as a known missing piece until then.

## 6. The annotation pin — settled

Part 1 deferred this here, to be fixed by reading what the model itself consumed. The reading is unambiguous:

- **The extracted identities rely on no annotation table, no annotation revision, and no crosswalk.** `model.py` reads exactly two data files — the completeness CSV (FlyWire ID + a `Completed` flag; there are no cell-type columns in it) and the connectivity parquet. The notebooks' populations are raw FlyWire IDs written literally into the code. The names attached to them ("sugar GRN", "MN9", "aDN1") come from Shiu et al. 2024 and the notebooks' own comments, at upstream commit `91bdd1e`.
- **The pin is therefore: none required.** The identity source of record for every population in §2 is *the v630 materialisation (hashed files, Part 1) + the upstream notebooks' literal lists (commit above)*. There is no external annotation revision to cite alongside them, and inventing one would be false provenance.
- **For Part 4's sensory specs:** no crosswalk is needed as long as the specs are written against these same ID sets — the per-stimulus pathways (register item 20) cite the notebook lists and the paper, per stimulus. A crosswalk becomes necessary only if a future population is defined *by annotation* (e.g. "all descending neurons" as a class, or a cell type the notebooks never list): current annotation releases are v783-era, their root IDs do not join onto v630, and that construction would need the explicit, recorded crosswalk Part 1 described. That boundary is now stated where Part 4 will meet it.

## 7. Correction — 24 Nov 2026 (Part 2b gate condition (d)): the aDN sets and bilaterality

Added under the Part 2b LIGHT gate (Reviewer 1, condition (d)); the frozen `id_sets_v1` artefacts are **not** changed by this section, and nothing was re-run. Full record: `PART2B-BUILD.md` §10.3; register entry: `PART0-PACKAGE.md` G2.

**The check.** The v630 materialisation carries no annotation table (completeness = ID + Completed flag; connectivity = pre/post/count/sign — no cell-type or side columns), so the check ran against the annotation-bearing sources on disk: the upstream notebooks, the old build's independently transcribed constants, and the paper as read in the reading log.

**Finding for aDN2: the type is bilateral; the set holds its left member only.** The upstream source names the extracted neuron `id_DN2_l` — the left suffix is the source's own. A right aDN2 exists in the v630 brain as anatomy, but its root ID appears in no text source in the project: the upstream notebooks contain exactly two descending-neuron identifiers (`id_DN1_1` and `id_DN2_l`, verified by exhaustive search of both notebooks on 24 Nov 2026), and the old build's constants likewise carry only `DN2_L`.

**Classification.** This is **not an extraction error**: the extraction obligation (§1) was the populations the published experiments define, and the published JON experiments read out the left aDN2 only — nothing charged was missed, and §3's "discrepancy record: none found" stands for the extraction as charged. It **is** an anatomical incompleteness in the set as a description of the type, and this section is the record that says which of the two it is. Consequence, as it played out: Part 2b's toy decoder is symmetric because the published readout is one-sided — no left/right differential command could have been decoded honestly from this set. If the set is ever completed (right aDN2 identified through a recorded crosswalk decision, per §6's boundary — never guessed from connectivity resemblance), a bilateral differential readout becomes possible in principle; that is a Part 4/5 design input. Until then, no part may claim a bilateral aDN readout.

**Finding for aDN1: undetermined.** Every source names it `id_DN1_1` — a numeric suffix, no side marker. Whether aDN1 is a bilateral pair or a single neuron cannot be settled from the project data on disk; it is recorded as undetermined, resolvable by the same crosswalk route.
