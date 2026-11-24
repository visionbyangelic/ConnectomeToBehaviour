# Part 2 — Reading log: the upstream model, line by line

**What was read:** `model.py` (373 lines) and `utils.py` (84 lines) from the upstream repository `philshiu/Drosophila_brain_model`, cloned 23 Nov 2026 at commit `91bdd1e7dcf193f3e7ca5a8933497fcef63b7960`; `model.py` SHA-256 `fc45837d7122c6ce2a7f3f2f23c515992e4b232aadb919efabb72337fac88e4e`. The two notebooks (`example.ipynb`, `figures.ipynb`) were read as well, because — first finding — **the model file does not contain the experiments**. Everything below is from reading the code as text; line numbers refer to `model.py` at that commit unless stated otherwise.

## The shape of the thing

`model.py` is a bare engine with four moving parts:

- `default_params` (lines 15–53) — every constant and the neuron equations, in one dict.
- `create_model(path_comp, path_con, params)` (lines 129–188) — builds the Brian2 network from the two v630 files.
- `poi(...)` (lines 58–106) and `silence(...)` (lines 108–127) — the two manipulations: Poisson-drive a set of neurons; zero a set of neurons' outgoing weights.
- `run_trial(...)` / `run_exp(...)` (lines 250–373) — run one trial / run a whole experiment in parallel and save the spikes.

There are **no neuron populations in this file at all** — no GRN lists, no MN9, no DNs. `run_exp` receives FlyWire IDs from its caller. The populations live in the notebooks (see §6). Anyone who reads only `model.py` has not seen the model that produced the paper's figures.

## Parameters (lines 15–53), each with the source the code itself cites

| Parameter | Value | Meaning | Source as cited in the code |
|---|---|---|---|
| `t_run` | 1000 ms | trial duration | — |
| `n_run` | 30 | trials per experiment | — |
| `v_0` | −52 mV | resting potential | Kakaria & de Bivort 2017 |
| `v_rst` | −52 mV | reset potential after a spike | (same block) |
| `v_th` | −45 mV | spike threshold | (same block) |
| `t_mbr` | 20 ms | membrane time constant | Kakaria & de Bivort 2017 (comment: C·R = 0.002 µF × 10 MΩ) |
| `tau` | 5 ms | synaptic (alpha) time constant | Jürgensen et al. |
| `t_rfc` | 2.2 ms | refractory period | Lazar et al. |
| `t_dly` | 1.8 ms | uniform synaptic delay on every synapse | Paul et al. 2015 |
| `w_syn` | 0.275 mV | **the one free parameter** — weight per anatomical synapse | labelled "Free parameter" in the code (line 36) |
| `r_poi` | 150 Hz | default Poisson drive rate (first input class) | — |
| `r_poi2` | 0 Hz | second input class rate (default off) | — |
| `f_poi` | 250 | scaling factor for the Poisson drive | comment: "250 is sufficient to cause spiking" |

## The neuron equations (lines 44–52)

```
dv/dt = (v_0 - v + g) / t_mbr : volt (unless refractory)
dg/dt = -g / tau               : volt (unless refractory)
rfc                            : second
```

- A leaky integrate-and-fire neuron whose synaptic input is a single voltage-like variable `g`. On a presynaptic spike, `g += w` (the `on_pre` rule, line 175); between spikes `g` decays exponentially with the 5 ms `tau`. So the "alpha synapse" of the comment is realised as an instantaneous jump plus exponential decay — the comment on line 37 ("weight per synapse, modulated by exponential decay") refers to this decay of `g`, not to any decay of the weight itself. Loose wording, recorded so nobody goes hunting for a weight-decay term that does not exist.
- Threshold: `v > v_th` (line 50). Reset (line 52): `v = v_rst; w = 0; g = 0 * mV`. **Flag:** `w` is the *synapse* variable (`Synapses(..., 'w : volt', ...)`, line 175); the neuron equations define no `w`. Whether Brian2 accepts this reset string, ignores the clause, or errors is **not assumed** — it is a named check for the first build of the model in this rebuild (Part 2, second half). The published results were produced with this code, so something happens; what exactly must be established, not guessed.
- The refractory is unusual: instead of a fixed duration, the group is created with `refractory='rfc'` (line 166), where `rfc` is a per-neuron state variable declared in the equations (`rfc : second`). Every neuron's `rfc` is initialised to `t_rfc` (line 172) — and, crucially, `poi()` can then set an individual neuron's `rfc` to 0 (lines 92, 103). The refractory period is data, not configuration.
- Integration method: `method='linear'` (line 163) — exact integration of the linear equations.

## How the connectome is loaded and turned into synapses (lines 156–186)

1. `df_comp = pd.read_csv(path_comp, index_col=0)` — the completeness CSV's first column (the FlyWire ID) becomes the index. **The neuron order of the whole model is the CSV's row order**: Brian index *i* is `df_comp.index[i]`. Nothing sorts or re-keys anything.
2. `NeuronGroup(N=len(df_comp), ...)` — one neuron per CSV row (127,400 for v630), `v` initialised to `v_0`, `g` to 0.
3. `syn.connect(i=df_con['Presynaptic_Index'], j=df_con['Postsynaptic_Index'])` — connections are taken from the parquet's **index columns**, not its ID columns. The code never checks that index *k* in the connectivity file is the same neuron as row *k* of the CSV. That silent trust is the single most load-bearing assumption in the file; the Part 2 extraction verified it independently (0 mismatches over all 14,687,178 edges — see `PART2-ID-SETS.md`).
4. `syn.w = df_con['Excitatory x Connectivity'] * w_syn` — the weight of an edge is its synapse count times the excitatory sign (+1/−1 from the transmitter prediction baked into that column) times 0.275 mV.
5. **No threshold, no filtering, anywhere.** Every one of the 14,687,178 rows of the connectivity parquet becomes a synapse, including the ~9.9M edges with 1–2 synapses. If any synapse-count threshold shaped the published model, it was applied when the parquet was produced, upstream of this code — it cannot be read off `model.py`, and any claim about it has to come from the paper's Methods. (Part 1 counted 4,770,900 edges with ≥3 synapses; the model as coded uses all of them *and* the rest.)
6. One `SpikeMonitor` on the whole group records everything; outputs are read from it after the run.

## Activation — `poi()` (lines 58–106)

For each driven neuron, a `PoissonInput(target=neu[i], target_var='v', N=1, rate=r_poi, weight=w_syn * f_poi)`:

- The drive injects **directly into the membrane potential `v`**, not into `g` — it bypasses the synaptic dynamics entirely.
- The kick per Poisson event is 0.275 mV × 250 = **68.75 mV** — several times the rest-to-threshold distance (7 mV). A driven neuron is not nudged; it is slammed past threshold on essentially every input event. "Activation at 150 Hz" in this model means the target fires at close to the drive rate, by construction.
- Side effect, easy to miss: `neu[i].rfc = 0` — **driven neurons lose their refractory period entirely**, so nothing caps their firing rate except the drive itself.
- Two classes: `exc` at `r_poi`, `exc2` at `r_poi2`. The two-class design is how the paper's interaction experiments are built (sugar in one class, bitter or water in the other, rates swept independently — `figures.ipynb` cells 24, 27, 45). **Docstring error, recorded:** the `poi` docstring (line 71) says `exc2` gets `r_poi`; the code (line 100) uses `r_poi2`. The code is what ran.

## Silencing — `silence()` (lines 108–127)

For each silenced neuron, `syn.w[' {} == i'] = 0 * mV` — the weights of all synapses **from** that neuron are set to zero.

- **The neuron is not silenced. Its output is disconnected.** It still receives input, still integrates, still spikes (and its spikes still appear in the monitor); those spikes simply do nothing downstream. The biological meaning, for the plan's activate/silence/block-output API: this is *block-output*, not cell silencing, and conclusions must be worded that way.
- **Code-vs-documentation divergence:** the upstream README describes silencing as setting "all synaptic connections **to and from** those neurons to zero". The code zeroes only the *from* direction. Incoming synapses onto a "silenced" neuron keep their weights (they matter if the neuron is also being read as a relay, and they matter for what the monitor shows). Whether the paper's Methods describe it as the code does is a check item, not an assumption.
- The indexing expression is written with a leading space (`' {} == i'`) — Brian2 accepts it; it is brittle style worth knowing about before copying the idiom.

## Running an experiment — `run_trial` / `run_exp` (lines 250–373)

- `run_exp` builds the ID↔index maps from the completeness file (`flyid2i = {id: row}` line 343), converts the caller's FlyWire ID lists to Brian indices, and runs `n_run` trials in parallel with joblib (`parallel_backend('loky')`, `n_proc=-1` = all cores, line 356). Each trial rebuilds the entire network from disk (`run_trial` calls `create_model` afresh, line 279) — the connectome is re-read and re-built for every single trial.
- An ID in any input list that is absent from the completeness file raises a bare `KeyError` at line 357–359 — there is no validation or friendly failure. (This is also why the gate obligation's membership cross-check matters: it is the only thing standing between a typo'd ID and a crashed or, worse, silently mis-targeted run. A wrong-but-present ID would not crash at all.)
- **Seeds: there are none.** No `seed()` call, no NumPy seeding, nothing in `model.py`, `utils.py`, or either notebook. Brian2's default random number generation is unseeded, and the trials run in parallel worker processes. Trial-to-trial variability is genuine but unseeded entropy: **an individual published run cannot be exactly reproduced from this code, only statistically.** Any reproduction claim in this rebuild is a distributional claim, and Part 3's criteria are written that way already.
- **Skip-if-exists:** if the output parquet already exists and `force_overwrite` is False (the default), `run_exp` prints a line and returns without simulating (lines 337–339). A stale results file silently stands in for a run. Worth knowing before trusting any folder of upstream outputs.
- Output: spikes are collected by `construct_dataframe` (lines 214–248) into a table with columns `t, trial, flywire_id, exp_name` — exactly the schema of `sugarR.parquet` (Part 1 verified the reference file against it) — and saved with brotli compression (line 373).

## `utils.py` — the analysis helpers (84 lines)

- `load_exps` concatenates result parquets (and carries a stale comment about loading "metadata from pickle" over code that reads parquet — harmless, recorded for completeness).
- `get_rate` computes per-neuron firing rates per experiment: for each neuron that appears in the spike table, rate per trial = spikes / `t_run`, then mean and standard deviation across trials. Two properties that matter when comparing numbers: the standard deviation is NumPy's default (population, ddof=0), and **neurons that never spiked are absent from the table** — the notebooks patch this with `.fillna(0)` at the call sites. A rate table from this code and a rate table that includes silent neurons are different objects; Part 3 comparisons must use the same convention as the reference.

## Where the populations actually live — the notebooks

All population definitions are literal ID lists written into notebook cells (extraction and cross-checks: `PART2-ID-SETS.md`):

- `example.ipynb` cell 3: `neu_sugar` (21 right-hemisphere labellar sugar GRNs); cell 7 runs the `sugarR` experiment that produced the Part 3 reference file; cell 17 reads out **left MN9 only** (720575940660219265).
- `figures.ipynb`: the same sugar list (cells 4, 23, 44 — identical every time), `neu_bitter` (21, cell 23), `neu_ir94e` (18, cell 23), `neu_water` (18, cell 32), `neu_sugar_left` (10, cell 76), the Johnston's-organ sets `neu_JON_CE` (70), `neu_JON_F` (60), `neu_JON_D_m` (16) combined as `neu_JON_all` (146, cell 50), readout neurons MN9 left/right (cell 17), `id_DN1_1` = aDN1 (720575940616185531) and `id_DN2_l` = aDN2 left (720575940629806974) (cells 54, 81), `id_aBN1` (720575940630907434, cell 62), and `three_inhibitory` (3 IDs silenced in the JON-F experiment, cell 70).
- The Figure 2 experiments take their input populations from `sez_neurons.pickle` (`types_and_ids`, cell 17) — a binary artefact with **no text source anywhere in the repository**. Those SEZ sets could not be extracted by reading, and the pickle was not loaded (a pickle is executable code, and the file failed an execution-risk check). Recorded as a gap in `PART2-ID-SETS.md`, not worked around.
- The notebooks also derive *responder* sets from earlier runs (top-200/top-300 responders, stored as pickles between cells). Those are analysis artefacts of the paper's pipeline, not model definitions — Part 3 does not need them unless it reproduces a specific figure's two-stage procedure.

## Surprises, collected

1. The engine and the experiments are in different files; `model.py` alone defines no population, no stimulus, no readout.
2. No synapse threshold in the code — all 14,687,178 edges are used as served.
3. The reset string sets `w = 0`, a variable the neuron does not have. Unresolved until the first build.
4. Driven neurons lose their refractory period and are kicked 68.75 mV per Poisson event, straight into `v`.
5. "Silencing" disconnects a neuron's output only; the README says "to and from", the code does "from".
6. No seeds anywhere; parallel, unseeded trials; exact reproduction of a published run is impossible from this code.
7. `run_exp` silently skips work if an output file already exists.
8. The whole index system rests on the connectivity parquet's index columns agreeing with the completeness CSV's row order — trusted silently by the code, verified independently in this part.

## Code-vs-paper checks this reading hands forward (to verify, not assume)

- Whether the paper's Methods describe any synapse-count threshold that the parquet (not the code) embodies.
- Whether the paper describes silencing as output-block (code) or as full disconnection (README).
- What Brian2 does with the `w = 0` clause in the reset string, at the pinned Brian2 2.9.0.
- Whether the paper's stated Poisson parameters match the defaults here (150 Hz, `f_poi` 250) or the per-figure sweeps in the notebooks (10–260 Hz) — the figures sweep rates, so "the model's activation rate" is per-experiment, not a constant.
- The sign convention of the `Excitatory` column (transmitter predictions): the code multiplies it straight into the weight, so a sign error upstream would invert excitation and inhibition wholesale. Part 2's synapse-sign audit (plan §4, Part 2 row) covers this.
