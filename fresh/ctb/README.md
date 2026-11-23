# ctb — the fresh brain-model implementation

My own implementation of the Shiu et al. (2024) whole-brain LIF model on
the FlyWire v630 connectome, written in Part 2 of the fresh rebuild from
the paper's equations and from my line-by-line reading of the upstream
code (project record: `fresh/PART2-READING-LOG.md`). Nothing here imports
or executes upstream code, and no neuron ID list is typed into this
package by hand — populations come from the versioned Part 2 artefacts
in `../part2/id_sets_v1/`.

## Layout

- `data/loader.py` — loads the v630 completeness + connectivity files
  **only after their SHA-256 hashes match the Part 1 record**; holds the
  index↔ID conventions; loads the ID-set artefacts with their counts
  validated against their manifest.
- `brain/model.py` — the LIF network (equations, parameters, synapse
  construction), the Poisson drive, and `block_output`. The module
  docstring carries the full specification and the named deviations.
- `brain/runner.py` — runs an experiment config into
  `runs/<run_id>/` (spike table in the upstream output schema + a
  manifest with config, seeds, code version, data hashes, wall clock).
  It **refuses** to write into a non-empty run directory: no run is ever
  silently skipped or overwritten.

## Named deviations from upstream

1. **Seeded runs** — upstream sets no seed anywhere; here the seed is a
   recorded run parameter, so our runs repeat exactly and comparisons
   with upstream outputs are statistical, as they have to be.
2. **Reset string** — upstream's reset sets `w = 0`, a variable the
   neuron does not have. Tested at Brian2 2.9.0 (`../part2/w_reset_test.py`):
   the clause is silently ignored and changes nothing. Ours omits it.
3. **`block_output`, not "silence"** — the operation zeroes outgoing
   weights only; the neuron keeps receiving input and spiking. The name
   says what the operation does.
4. **Hash-checked data** — upstream reads whatever files it is pointed
   at; the loader verifies SHA-256 against the Part 1 record first.
5. **No-skip runner** — upstream's `run_exp` returns silently when its
   output file already exists; this runner raises instead.

Everything else follows the upstream specification as read: all
14,687,178 edges used with no synapse threshold; weights = count ×
predicted transmitter sign × 0.275 mV; the drive injects into `v` at
68.75 mV per event and removes the driven neurons' refractory period.

## Tests

From `repo/fresh/`, with the pinned brain env:

```
../../envs/brain/bin/python -m pytest tests/ -q
```

(adjust the env path to wherever the brain env lives). The suite checks
the data hashes and Part 1 counts, the weight formula by hand and
against the file's own product column on a sample, the Part 2 pass
criteria in miniature (silent network = 0 spikes; single-neuron response),
`block_output` exactness, and the runner's manifest / refusal /
reproducibility behaviour.
