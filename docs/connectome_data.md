# Part 1 — Data: download record, hashes, counts, and the sugarR verdict

**Procedure:** the three v630 files were downloaded on 23 Nov 2026 (~19:40 WAT) from the exact URLs in the old build's `scripts/download_data.py` (`philshiu/Drosophila_brain_model`, `main` branch, raw.githubusercontent.com), into the fresh repo's gitignored data folder, `~/workspace/connectome-work/repo/data/` (the repo's `.gitignore` covers `data/`, `*.parquet` and `*.csv`, so nothing here can be committed by accident). Verification was done with the pinned brain env (`envs/brain`: pandas 3.0.6 / pyarrow 20.0.0), streaming the large parquet in batches rather than loading it whole.

**One retrace, recorded honestly:** the download command raced the creation of the `data/` folder, its `cd` failed, and the three files first landed in the home directory. They were moved into `repo/data/` immediately and their hashes re-verified after the move (identical before and after). No file was modified in transit — sizes and SHA-256 below are of the files as they now sit in `repo/data/`, and the byte sizes match the Part 0 HEAD checks exactly, which is the independent confirmation that what arrived is what upstream serves.

## Files, sizes, SHA-256 (§7.5 record)

| File | Bytes | SHA-256 |
|---|---|---|
| `2023_03_23_completeness_630_final.csv` | 3,057,611 | `e6b71e17671a9bdb05f55e4bc6774640a1418cb7a05125e0fc994ad40f9bfdfb` |
| `2023_03_23_connectivity_630_final.parquet` | 86,630,944 | `94db8c650533bc36ffa3223f2e62325d5648b8d6bd31c3a4e1c804628c7557b3` |
| `sugarR.parquet` | 948,526 | `83921d50089d966785e402d6c0e3be5ab3eba5beb680410a09c557b0f22dcc28` |

## Counts computed from the files (Part 1 pass-criterion numbers)

**Completeness CSV** — 2 columns (FlyWire ID, `Completed` flag):
- Rows / unique neuron IDs: **127,400** — exactly the v630 count the paper and the plan state. No nulls, no duplicates.
- `Completed` = True for all 127,400.

**Connectivity parquet** — 14,687,178 rows, columns `Presynaptic_ID`, `Postsynaptic_ID`, `Presynaptic_Index`, `Postsynaptic_Index`, `Connectivity` (synapse count for the pair), `Excitatory`, `Excitatory x Connectivity`:
- **Edges (unique pre→post pairs): 14,687,178** — every row is a distinct pair, so rows = edges.
- **Raw synapses (sum of `Connectivity`): 52,793,639** — of which excitatory-signed 10,131,023 and inhibitory-signed 42,662,616 (sign per the file's `Excitatory` column).
- **Edges with ≥3 synapses: 4,770,900.**
- Neurons appearing as presynaptic: 127,015; as postsynaptic: 126,793; union: **127,400**.
- **Cross-file consistency: the connectivity ID set is exactly equal to the completeness ID set** (subset both ways verified), and the index columns span exactly 0–127,399. The two files belong to the same materialisation and neither is truncated or mismatched.

These are the fresh build's own counts, computed from the downloaded files — they are the numbers Part 2 builds from and Part 3/Part 6 compare against, not numbers copied from the old build.

## The sugarR verdict (assumption A13) — **TRUSTED as the Part 3 benchmark**

The worry (Part 0): upstream serves `sugarR.parquet` at 948,526 B (~0.95 MB) while the old download script claims ~2.2 MB. I inspected the contents in full (the file parses end-to-end; 511,566 spike rows):

- **Structure:** a spike table — columns `t` (spike time, s), `trial`, `flywire_id`, `exp_name`. Exactly one experiment: `exp_name = 'sugarR'` throughout.
- **Trials:** `trial` takes exactly the values 0–29 → **30 trials**, and within every trial `t` spans [0, 1) s → **30 × 1.0 s**, precisely the protocol the old build documented for this file ("30 trials, 1 sec each") and the protocol Part 3 mirrors.
- **Active neurons: 448 unique `flywire_id`s** — exactly the reference active-neuron count the old build's canonical 1.0 s benchmark reported (its README: 411 shared of **448 reference active**). A truncated or wrong-export file would be very unlikely to reproduce that fingerprint. All 448 IDs belong to the v630 completeness set.
- **MN9 check:** MN9 is a neuron in the table, not a column — both MN9 IDs from the old build's constants are present, spiking in all 30 trials: MN9 left (720575940660219265) 2,798 spikes → **93.3 Hz** mean; MN9 right (720575940645521262) 1,854 spikes → **61.8 Hz**. Same left-dominant asymmetry and same range as the old build's own simulation output (83.5 ± 6.5 / 58.7 ± 5.2 Hz) — close enough to be the same phenomenon, different enough to be an independent run of the model, which is what a reference should be.
- **Trial structure is healthy:** 16,626–17,402 spikes per trial (mean 17,052), 388–415 active neurons per trial (mean 402.6) — real trial-to-trial variability (Part 3's noise ceiling has something to bite on), no NaNs, no negative times, no per-trial cliff that would suggest a cut-off file.

**Why the size differs, then:** 511,566 rows × 4 narrow columns is intrinsically small, and parquet's encoding is very effective on this shape — only 448 distinct `flywire_id` values, 30 distinct `trial` values and one distinct `exp_name` dictionary/RLE-compress to almost nothing, leaving the `t` column as most of the file. ~1.85 bytes/row as served is entirely consistent with that. The script's "~2.2 MB" sits in a field literally named `approx_size_mb` — an approximation, most plausibly written against a less-compressed or differently-encoded copy. **The discrepancy is explained by compression plus an approximate script annotation; the contents match every documented expectation. Verdict: `sugarR.parquet` (SHA-256 above) is TRUSTED as the Part 3 model-vs-model benchmark reference.** Standing reminder from the old build's own correction, which Part 3 inherits: this file is Shiu et al.'s *simulation output*, not animal recordings — matching it proves reproduction of their model, nothing biological.

## FlyWire annotation revision — the Part 1 position (register item 17)

What I can state from this part's own artefacts, and what I am deliberately not over-claiming:

- **The build's identity layer for the core is the v630 materialisation itself**: the completeness + connectivity files above, whose ID set is internally exact (127,400 IDs, indices 0–127,399). Neuron identity in Parts 2–3 (GRN sets, MN9, DNs) is taken from the paper and the upstream model's own constants, cross-checked against these IDs — as the old build did — not from a later annotation release.
- **The current FlyWire annotation releases (Schlegel et al. annotations / neurotransmitter predictions and their deposits) are built on later materialisations (the v783-era segmentation), not on v630.** Root IDs are not stable across materialisations — proofreading splits and merges change them — so a current annotation table **cannot** be joined directly onto v630 IDs and must never be used as if it could. Where an annotation's *content* (a cell-type call, a transmitter prediction) is needed for a v630 neuron, it is interpretive evidence that has to travel through an explicit ID crosswalk, with the mapping recorded — exactly the distinction register item 17 demands.
- **Recorded position:** the build pins **the v630 materialisation (files + hashes above)** as its only identity source of record for the core. The exact annotation-repository revision to cite alongside it — and the crosswalk, if Part 2's reading shows one is needed for the GRN/DN sets — is fixed during **Part 2's reading of Schlegel et al. and the upstream `model.py`**, where which annotations the model itself consumed can be read off the code rather than guessed. Pinning a specific annotation revision now, before that reading, would be pinning blind. This is a deferral with a named home (Part 2) and a named reason, not a gap left open.
