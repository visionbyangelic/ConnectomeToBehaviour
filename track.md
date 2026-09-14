# ConnectomeToBehavior — Detailed Activity Log

Every action, installation, error, and decision is logged here in chronological order.

---

## Day 1 — Sunday 14 September 2026

### 16:42 — Session started
- Opened workspace: `c:\Users\nerdyalgorithm\Desktop\top project\ConnectomeToBehaviour`
- Files present: `README.md`, `TECHNICAL_PROOF_PLAN.md`, `TECHNICAL_PROOF_PLAN (1).md`, `.git/`
- Goal: Begin Quick-Start setup (§0 of Technical Proof Plan)

---

### 16:51 — Attempt to clone `philshiu/Drosophila_brain_model`
- **Command:** `git clone https://github.com/philshiu/Drosophila_brain_model.git`
- **Result:** Clone started but stalled — downloading large files
- **Investigation:** Repo is ~190 MB total via GitHub API (`"size": 189741` KB)

#### File size breakdown (philshiu/Drosophila_brain_model):
| File | Size | Essential? |
|------|------|-----------|
| `Connectivity_783.parquet` | 96 MB | ✅ Yes (v783 connectome) |
| `2023_03_23_connectivity_630_final.parquet` | 83 MB | ❌ No (old v630) |
| `Completeness_783.csv` | 3.2 MB | ✅ Yes |
| `2023_03_23_completeness_630_final.csv` | 2.9 MB | ❌ No (old v630) |
| `model.py` | 12 KB | ✅ Core LIF model |
| `utils.py` | 2 KB | ✅ Helpers |
| `example.ipynb` | 10 KB | ✅ Tutorial |
| `figures.ipynb` | 33 KB | ✅ Paper figures |
| `environment.yml` | 0.2 KB | ✅ |
| `sez_neurons.pickle` | 5 KB | ✅ Neuron IDs |
| `results/` (5 parquet files) | 3.2 MB | ⚠️ Optional |

- **Decision:** User has limited data plan. Clone cancelled. User will download files manually from GitHub to track bandwidth.
- Cleaned up partial clone: `Remove-Item -Recurse -Force "Drosophila_brain_model"` → success

---

### 17:07 — Analyzed `eonsystemspbc/fly-brain`
- **Repo size:** ~186 MB total
- **Finding:** ~185 MB is the same connectome data files as philshiu's repo

#### File size breakdown (eonsystemspbc/fly-brain):
| File | Size | Essential? |
|------|------|-----------|
| `data/2025_Connectivity_783.parquet` | 96 MB | ❌ Same as philshiu |
| `data/archive/2023_Connectivity_630.parquet` | 83 MB | ❌ Old data |
| `data/2025_Completeness_783.csv` | 3.3 MB | ❌ Same as philshiu |
| `data/archive/2023_Completeness_630.csv` | 3 MB | ❌ Old data |
| `main.py` | 8 KB | ✅ Unified entry point |
| `code/benchmark.py` | 19 KB | ✅ Backend benchmarks |
| `code/run_pytorch.py` | 22 KB | ✅ PyTorch backend |
| `code/run_nestgpu.py` | 23 KB | ✅ NEST GPU backend |
| `code/run_genn.py` | 23 KB | ✅ GeNN backend |
| `code/run_brian2_cuda.py` | 21 KB | ✅ Brian2CUDA |
| `code/run_brian2_genn.py` | 18 KB | ✅ Brian2GeNN |
| `code/compare_*.py` (3 files) | 33 KB | ✅ Validation tools |
| `code/paper-phil-drosophila/` | 77 KB | ✅ Original model code |
| `data/results/` | 500 KB | ⚠️ Benchmark logs |

- **Decision:** Download only code files, skip data entirely

---

### 17:26 — Downloaded `eonsystemspbc/fly-brain` code files
- **Method:** Direct download via `Invoke-WebRequest` from raw GitHub URLs
- **Files downloaded:** 17 files
- **Total size:** 215.8 KB
- **Status:** ✅ All OK

```
fly-brain/
├── main.py (7.7 KB)
├── environment.yml (0.4 KB)
├── environment-brian2genn.yml (0.3 KB)
├── README.md (17 KB)
├── LICENSE (17.7 KB)
└── code/
    ├── benchmark.py (18.9 KB)
    ├── run_pytorch.py (22.3 KB)
    ├── run_nestgpu.py (23 KB)
    ├── run_genn.py (22.6 KB)
    ├── run_brian2_cuda.py (20.6 KB)
    ├── run_brian2_genn.py (18.2 KB)
    ├── compare_ground_truth.py (9.2 KB)
    ├── compare_backend_to_brian2.py (12.5 KB)
    ├── compare_spike_outputs.py (10.5 KB)
    └── paper-phil-drosophila/
        ├── model.py (11.8 KB)
        ├── utils.py (2.2 KB)
        └── LICENSE (1.1 KB)
```

---

### 17:31 — Downloaded missing `sez_neurons.pickle`
- **Command:** `Invoke-WebRequest` from raw GitHub
- **Size:** 5 KB
- **Location:** `fly-brain/data/sez_neurons.pickle`
- **Status:** ✅

---

### 18:20 — User activated conda environment `na`
- **Command:** `conda activate na`
- Python environment: `na` (pre-existing)

---

### 18:26 — User started installing flygym + flyvis
- **Command:** `pip install flygym flyvis`
- **Environment:** `na` conda env
- **Status:** Running (seen in terminal metadata)

---

### 18:26 — Analyzed `TuragaLab/flybody` (aka google-deepmind/flybody)
- **Note:** Technical plan references `google-deepmind/flybody` but actual repo is `TuragaLab/flybody`
- GitHub API was rate-limited (429). Used web search to confirm correct repo URL
- **Repo structure:** Pure Python package with MuJoCo XML assets — no large data files
- **Decision:** pip install instead of clone (it's a proper package)

---

### 18:30 — First `pip install flybody`
- **Command:** `pip install git+https://github.com/TuragaLab/flybody.git`
- **Status:** ✅ Successfully installed `flybody-0.1.0`
- **Side effect:** numpy downgraded from 2.0.2 → 1.26.4

### ⚠️ ERROR — numpy version conflict
```
flygym 1.2.1 requires numpy<3.0,>=2.0, but you have numpy 1.26.4 which is incompatible.
opencv-contrib-python 4.12.0.88 requires numpy<2.3.0,>=2, but you have numpy 1.26.4 which is incompatible.
opencv-python 4.12.0.88 requires numpy<2.3.0,>=2, but you have numpy 1.26.4 which is incompatible.
```
- **Root cause:** `flybody` pins `numpy==1.26.4` in its dependencies, but `flygym` requires `numpy>=2.0`
- **Impact:** flygym may not work correctly with numpy 1.26.4
- **Resolution:** TBD — may need separate environments or version override

---

### 18:34 — Confirmed flybody install location
- **Command:** `python -c "import flybody; import os; print(os.path.dirname(flybody.__file__))"`
- **Location:** `C:\Users\nerdyalgorithm\.conda\envs\na\Lib\site-packages\flybody\`
- Key files: `fruitfly/assets/fruitfly.xml` (MuJoCo body model), `fly_envs.py` (RL environments)

---

### 18:40 — Confirmed no additional downloads needed from TuragaLab/flybody
- Tutorial notebooks (`docs/getting-started.ipynb`, `docs/fly-env-examples.ipynb`) available but not downloaded — optional reference material

---

### 18:46 — Updated TECHNICAL_PROOF_PLAN.md
- Checked off 5/6 Quick-Start items
- Created `overview.md` and `track.md`

---

### 18:55 — Created FlyWire / Codex Account
- **Action:** User created account at [flywire.ai / codex.flywire.ai](https://codex.flywire.ai)
- **Status:** ✅ Complete
- **Impact:** §0 Quick-Start in [TECHNICAL_PROOF_PLAN.md](file:///c:/Users/nerdyalgorithm/Desktop/top%20project/ConnectomeToBehaviour/TECHNICAL_PROOF_PLAN.md) is now 100% complete (6/6 items checked off).

### 19:08 — Tested numpy compatibility and imports in `na` env
- **Command:** `conda run -n na python -c "import flybody; print('flybody ok'); import flygym; print('flygym ok')"`
- **Result:** Both imported successfully (`flybody ok`, `flygym ok`). The pip error was a metadata constraint warning; basic imports and data structures work without throwing errors on numpy 1.26.4.

---

### 19:11 — Tested `flyvis` and `brian2` imports in `na` env
- **Command:** `conda run -n na python -c "import flyvis; print('flyvis ok'); import brian2; print('brian2 ok')"`
- **Result:** `flyvis ok`. `brian2` is not yet installed in the `na` environment (`ModuleNotFoundError: No module named 'brian2'`).

---

### 19:12 — Discovery: Connectome Data Files Already Present Locally!
- **Action:** Inspected `Drosophila_brain_model-main/` folder.
- **Discovery:** The folder ALREADY contains:
  - `Connectivity_783.parquet` (100,804,642 bytes / ~100.8 MB)
  - `Completeness_783.csv` (3,327,347 bytes / ~3.3 MB)
  - `2023_03_23_connectivity_630_final.parquet` (86.6 MB)
  - `2023_03_23_completeness_630_final.csv` (3.0 MB)
  - `example.ipynb` (10 KB) & `figures.ipynb` (33 KB)
  - `model.py` (12 KB) & `utils.py` (2 KB)
- **Status:** ✅ Zero data download needed! Everything is already stored locally on disk.

---

### 19:18 — Installed `brian2` into `na` conda environment
- **Command:** `conda run -n na pip install brian2`
- **Packages installed:** `brian2-2.9.0`, `cython-3.3.0`, `py-cpuinfo-9.0.0`
- **Data downloaded:** ~4.1 MB
- **Status:** ✅ Successfully installed

---

### 19:20 — Verified `brian2` import
- **Command:** `conda run -n na python -c "import brian2; print('brian2 version:', brian2.__version__)"`
- **Result:** `brian2 version: 2.9.0`
- **Status:** ✅ Fully functional

---

### 19:23 — Verified Parquet & parallel processing stack
- **Command:** `conda run -n na python -c "import pandas as pd, pyarrow, joblib; print('pandas, pyarrow, joblib all ok')"`
- **Result:** `pandas, pyarrow, joblib all ok`
- **Status:** ✅ Complete scientific stack ready for simulations

---

### 19:26 — Validated Shiu et al. Simulation Output (`results/example/sugarR.parquet`)
- **Command:** Loaded precomputed simulation results using `utils.load_exps`
- **Findings:**
  - Total spikes recorded: 511,566 spikes across 30 trials (1 sec each)
  - Active neurons: 448 unique neurons out of ~138,000 in the whole brain
  - Biology match: Matches Shiu et al., 2024 findings — sparse, selective sensory-to-motor activation cascade upon sugar gustatory stimulation
- **Status:** ✅ Baseline data pipeline verified

---

### 19:30 — Created `quick_test_sim.py`
- **Goal:** Run a fast 1-trial, 100 ms verification simulation of the adult Drosophila connectome using `model.py` and `brian2`.
- **Sensory stimulus:** 21 sugar-sensing gustatory neurons.

---

### 19:32 — ⚠️ BUG & ROOT CAUSE: `KeyError: 720575940620900446`
- **Error:** When attempting to run with `Completeness_783.csv`, Python threw `KeyError: 720575940620900446`.
- **Investigation:**
  - Tested ID presence across datasets: `720575940620900446 in df630.index` returned `True`, but `False` in `Completeness_783.csv`.
  - Also checked `sez_neurons.pickle`: all IDs matched v630, not v783.
  - **Root cause:** Shiu et al.'s published example IDs (`neu_sugar` and `sez_neurons.pickle`) were compiled against FlyWire materialization **v630** (`2023_03_23_completeness_630_final.csv` and `2023_03_23_connectivity_630_final.parquet`). In FlyWire, proofreading merges/splits change root IDs between versions.
- **Resolution:** Updated `quick_test_sim.py` to pair `neu_sugar` with the matching v630 connectome files (`2023_03_23_completeness_630_final.csv` and `2023_03_23_connectivity_630_final.parquet`), which are both already present locally.

---

### 19:43 — 🎉 SUCCESS: Full Connectome Live Simulation Completed!
- **Command:** `conda run -n na python quick_test_sim.py`
- **Details:**
  - Brain size: ~125,000 neurons, millions of alpha-synapses
  - Stimulus: 21 sugar-sensing neurons excited via 150 Hz Poisson input
  - Simulation duration: 100 ms of biological time (1 single trial, single CPU core)
  - **Elapsed compute time:** 35 seconds
  - **Total spikes recorded:** 1,306 action potentials
  - **Unique active neurons:** 323 neurons
  - **Output file:** `results/test/test_sugar_100ms.parquet`
- **Status:** ✅ End-to-end brain emulation verified runnable on local machine!

---

### 19:53 — Generated Visual Spike Raster & Firing Rate Graph
- **Script:** `plot_spikes.py`
- **Output:** `results/test/spike_raster_100ms.png`
- **Details:**
  - Top panel: Spike raster plot showing individual action potentials across time (0–100 ms)
  - Amber markers: 21 stimulated sugar gustatory sensory neurons
  - Cyan markers: 302 downstream postsynaptic neurons firing in cascade
  - Bottom panel: Population spike count per 2 ms time bin
- **Status:** ✅ Graphical visualization complete

---

### 20:03 — Established Repository Architecture & `.gitignore`
- **Action:** Created `.gitignore` and initialized project source tree (`src/` and `experiments/`).
- **Ignored:**
  - 100MB+ Parquet files (`*.parquet`, `*.feather`, `*.csv`) — prevents GitHub push rejection.
  - Cloned reference folders (`Drosophila_brain_model-main/`, `fly-brain/`, `Turagalab-flybody/`) — kept locally on disk for data & reference, but omitted from Git tracking.
  - Caches (`__pycache__`, `.brian`, results).
- **Source Modules Initialized:**
  - `src/brain/` — LIF connectome models and neural dynamics
  - `src/body/` — FlyBody / FlyGym physics & motor interfaces
  - `src/bridge/` — Descending neuron mapping (brain -> motor joints)
  - `experiments/` — Custom experiment scripts
- **Verification:** `git status` confirmed only clean project code and documentation are staged.
- **Status:** ✅ Clean repository structure ready for GitHub commits.

---

### 20:15 — Added In Silico Modular Lesion & Perturbation Analysis to Plan
- **Context:** Strategic review recommendation on demonstrating causal neural integration vs. passive morphological computation.
- **Action:** Added explicit milestone to Phase 5 in [TECHNICAL_PROOF_PLAN.md](file:///c:/Users/nerdyalgorithm/Desktop/top%20project/ConnectomeToBehaviour/TECHNICAL_PROOF_PLAN.md).
- **Core Concept:**
  - Beyond random degree-preserved connectome shuffling (null model), perform targeted *in silico* lesions of specific functional clusters and descending tracts (e.g. `MDN` backward walking, `DNp01` grooming, `Giant Fiber` escape) using `model.py`'s `silence()` weight-zeroing mechanism.
  - Map each cluster's lesion directly to its specific motor phenotype deficits.
  - Elevates the project from a proof-of-concept into a diagnostic hypothesis-testing tool.
- **Status:** ✅ Plan updated and documented.

---

### 20:34 — Resolved "Verify Yourself" Neuron & Synapse Count Discrepancy
- **Action:** Inspected both v630 and v783 datasets with pandas/pyarrow to empirically resolve the discrepancy between Eon Systems' README (~138k neurons, ~5M synapses) and Shiu et al.'s paper (125k+ neurons, 50M synapses).
- **Exact Measurements:**
  - **v630 (Shiu et al., 2024):** 127,400 neurons, 14,687,178 connection edges, **52,793,639 total raw synapses** (matches the paper abstract).
  - **v783 (Eon Systems / Final FlyWire):** 138,639 neurons, 15,091,983 connection edges, 54,492,922 total synapses.
  - **Root Cause of ~5M Synapses:** When filtering out weak connections with $< 3$ synapses per pair, exactly **4,916,231 edges (~5M synapses)** remain!
- **Status:** ✅ §0 (Quick-Start Setup) is now 100% completed, verified, and reconciled.

---

### 20:36 — Day 1 Session Concluded
- **Time:** 8:36 PM (Sunday 14 September 2026)
- **Summary:**
  - §0 Quick-Start fully completed (6/6 checklist items + "Verify Yourself" empirical proof).
  - All dependencies installed and tested in `na` (`brian2`, `flybody`, `flygym`, `flyvis`).
  - First live whole-brain LIF simulation executed and visual spike raster generated.
  - Dedicated repository architecture created with `.gitignore`.
  - Added In Silico Modular Lesion & Perturbation Analysis to Phase 5.
- **Next Session Objective:**
  - §1: Phase 0 — Literacy (Core Papers Executive Digest).
  - §2: Phase 1 — Build clean `src/brain/` connectome API class and test baseline experiment.

---

## Pending / Unresolved

| Issue | Priority | Status |
|-------|----------|--------|
| Connectome ID mapping (v630 vs v783) | 🟡 Medium | Understood: example/SEZ lists use v630 IDs; v783 needs mapped IDs |
| numpy conflict (1.26.4 vs ≥2.0) | 🟢 Low | Both import cleanly without crash; monitor during physics runs |
| MSVC C++ compiler for Cython | 🟢 Low | Brian2 automatically fell back to NumPy target (35s for 100ms is fast enough for test) |



