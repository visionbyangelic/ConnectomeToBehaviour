# ConnectomeToBehavior — Project Overview

## What This Project Is

A closed-loop whole-brain emulation of *Drosophila melanogaster* (fruit fly). We take the real, publicly available wiring diagram of the fly's entire nervous system (the connectome), give each neuron standard biophysical rules (leaky integrate-and-fire), connect the network to a physically realistic virtual fly body (MuJoCo), and ask: **does recognizable behavior emerge from structure alone?**

Target behaviors: walking/foraging, antennal grooming, proboscis extension (feeding).

**Author:** Angelic Charles  
**Started:** 6 September 2026  
**License:** MIT

---

## Core Pipeline

```
Environment → Sensory Input → Brain Model (LIF on connectome) → Descending Neurons → Body Model → Environment
                                                                                         ↑                    |
                                                                                         └────────────────────┘
```

| Component | Tool | Source |
|-----------|------|--------|
| Brain model | Brian2 (LIF + α-synapse) | Shiu et al., 2024 |
| Connectome data | FlyWire v783 | Dorkenwald et al., 2024 |
| Visual system | flyvis (PyTorch) | Lappalainen et al., 2024 |
| Body simulation | MuJoCo + flygym (NeuroMechFly v2) | Wang-Chen et al., 2024 |
| Locomotion controller | flybody (RL-trained) | Vaxenburg et al., 2025 |

---

## Key Repos & Packages

| Repo / Package | Location in workspace | Status |
|---|---|---|
| `philshiu/Drosophila_brain_model` | To be added (downloaded from GitHub) | ✅ Code ready, data deferred to Wi-Fi |
| `eonsystemspbc/fly-brain` | `fly-brain/` | ✅ Code downloaded (216 KB) |
| `flygym` | pip installed in `na` env | ✅ Installed (numpy conflict ⚠️) |
| `flybody` (TuragaLab) | pip installed in `na` env | ✅ Installed |
| `flyvis` | pip installed in `na` env | ✅ Installed |

---

## Current Phase

**Phase 0 — Quick-Start Resources (§0 of Technical Proof Plan)**  
Setting up the environment, cloning repos, installing dependencies.

**Next up:** Phase 1 (Literacy — reading core papers) → Phase 1 (Brain Model — run and inspect Shiu et al. code)

---

## Daily Session Log

### Day 1 — Sunday 14 September 2026

**What we did:**
1. Reviewed the project README and Technical Proof Plan
2. Analyzed `philshiu/Drosophila_brain_model` repo — confirmed connectome parquet files and code are locally available.
3. Analyzed `eonsystemspbc/fly-brain` repo and downloaded code files & SEZ neuron mapping.
4. Identified `TuragaLab/flybody` and pip-installed it into `na`.
5. Installed `flygym`, `flyvis`, and `brian2` via pip into the `na` conda environment.
6. Created FlyWire / Codex account — completed all 6/6 Quick-Start (§0) items in Technical Proof Plan.
7. Created `overview.md` and `track.md` for project tracking.
8. Resolved v630 vs v783 ID mapping differences.
9. Ran first live whole-brain connectome simulation on local machine (100 ms, 1,306 spikes, 323 active neurons).
10. Generated visual spike raster and population firing rate plots.
11. Established clean repository architecture (`src/brain/`, `src/body/`, `src/bridge/`, `experiments/`) and `.gitignore` to keep third-party repos and 100MB+ data files off GitHub.
12. Incorporated technical review feedback into Phase 5 of [TECHNICAL_PROOF_PLAN.md](file:///c:/Users/nerdyalgorithm/Desktop/top%20project/ConnectomeToBehaviour/TECHNICAL_PROOF_PLAN.md): added **In Silico Modular Lesion & Perturbation Analysis** to turn the simulation into a causal diagnostic tool.
13. Empirically resolved the "Verify Yourself" section in §0: proved why Shiu et al. reports 125k+ neurons and 50M synapses (v630 unthresholded), while Eon reports 138k neurons and ~5M synapses (v783 thresholded at $\ge 3$ synapses/connection: exactly 4,916,231 edges).

**Known issues & status:**
- ✅ **Connectome data files found locally!** All needed files exist on disk.
- ✅ **NumPy test:** Tested `import flybody` and `import flygym` on NumPy 1.26.4 — both loaded without error.
- ✅ **Brian2 installed:** Version `2.9.0` installed into `na` environment and verified.
- ✅ **LIVE SIMULATION VERIFIED:** Ran a live 100 ms simulation on local CPU in 35s. Output verified in `results/test/test_sugar_100ms.parquet`.
- ✅ **Clean Git Repo:** Only your project code and docs will be pushed to GitHub.
- 🎯 **Diagnostic Milestone Added:** Selective neuropil / descending neuron lesions to map functional modules to specific motor deficits.
- 🔍 **"Verify Yourself" Resolved:** Fully reconciled the neuron and synapse count discrepancy empirically.

**Where we stopped (Day 1 End — 8:36 PM):**
- **§0 (Quick-Start Setup) is 100% complete:** All 6 checklist items done, plus the "Verify Yourself" neuron/synapse mystery empirically resolved.
- Full scientific stack (`brian2`, `flybody`, `flygym`, `flyvis`, `pandas`, `pyarrow`, `joblib`) installed, verified, and running in `na` conda environment.
- Live whole-brain connectome simulation ran on local CPU (35s for 100ms, 1,306 spikes, 323 active neurons).
- Visual spike raster and population histogram generated and confirmed.
- Clean project structure (`src/brain/`, `src/body/`, `src/bridge/`, `experiments/`) and `.gitignore` active.
- Added In Silico Modular Lesion & Perturbation Analysis to Phase 5.
- **Next session starts at:** **§1: Phase 0 — Literacy (Core Papers Executive Digest)** followed by building our clean `src/brain/` connectome API class.

---


