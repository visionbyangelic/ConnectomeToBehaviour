# ConnectomeToBehaviour — Architecture & Project Overview

This document provides a concise architectural reference for the system. For current empirical status, benchmarks, and reproducibility instructions, see [README.md](README.md). For the complete chronological audit trail, see [track.md](track.md). For the phased roadmap and citations, see [TECHNICAL_PROOF_PLAN.md](TECHNICAL_PROOF_PLAN.md).

---

## What This Project Is

A closed-loop whole-brain emulation of adult *Drosophila melanogaster*. I take the real biological wiring diagram of the fruit fly central nervous system (FlyWire connectome v630), simulate its spiking dynamics with leaky integrate-and-fire equations in Brian2, connect the descending neural outputs to a 42-degree-of-freedom virtual fly body in MuJoCo (NeuroMechFly v2 via FlyGym), and test whether functional behavior emerges from connectome architecture.

Target behaviors:
1. **Proboscis extension (feeding)** upon labellar sugar contact.
2. **Antennal grooming** upon mechanosensory stimulation.
3. **Coordinated walking and exploration**.

---

## System Architecture

```text
       +-------------------------------------------------------------+
       |                        Environment                          |
       |  (MuJoCo Physics Arena: Flat Terrain / Food & Odor Patches) |
       +-------------------------------------------------------------+
                   │                                     ▲
   Sensory contact │                                     │ Joint angles &
   forces & odors  │                                     │ torques (42 DoF)
                   ▼                                     │
       +-----------------------+             +-----------------------+
       |     Sensory GRNs/     |             |        FlyBody        |
       |     Mechanoreceptors  |             |  (NeuroMechFly v2)    |
       +-----------------------+             +-----------------------+
                   │                                     ▲
     Poisson drive │                                     │ Joint position
     (e.g. 150 Hz) │                                     │ targets (rad)
                   ▼                                     │
       +-------------------------------------------------------------+
       |                          FlyBrain                           |
       |  Whole-Brain LIF Spiking Connectome Model (Brian2, v630)   |
       |  127,400 Neurons · ~52.8M Raw Synapses · α-Synapse Dynamics |
       +-------------------------------------------------------------+
                   │
                   │ Descending Neuron population spike rates
                   ▼
       +-------------------------------------------------------------+
       |                      Motor Decoder Bridge                   |
       |  Evidence-Based Anatomical Mapping (DNs → Premotor → Joints)|
       +-------------------------------------------------------------+
```

---

## Core Components & Repository Structure

| Subsystem | Primary Module | Core Technology | Role |
|---|---|---|---|
| **Brain** | [`src/brain/fly_brain.py`](src/brain/fly_brain.py) | Brian2, NumPy, Parquet | 127k-neuron LIF spiking model with `.activate()`, `.block_output()`, `.silence()`, and rate extraction |
| **Constants** | [`src/brain/constants.py`](src/brain/constants.py) | Python | Biophysical parameters and verified FlyWire IDs (GRNs, MN9, JON targets) |
| **Evaluation** | [`src/brain/evaluation.py`](src/brain/evaluation.py) | Pandas, SciPy | Correlation, Jaccard overlap, precision, recall, and hypothesis tests |
| **Body** | [`src/body/fly_body.py`](src/body/fly_body.py) | FlyGym, MuJoCo 3.2.7 | 42-actuator body simulation with verified millimetre units and tarsal force sensors |
| **Bridge** | `src/bridge/` | Python | Evidence-based mapping from descending pathways to motor targets |

---

## Canonical Data & Environment Specifications

* **Connectome Baseline:** FlyWire materialization **v630** (`2023_03_23_completeness_630_final.csv` and `2023_03_23_connectivity_630_final.parquet`). Stored locally on disk in `Drosophila_brain_model-main/` (omitted from Git tracking due to file size). Downloadable via `scripts/download_data.py`.
* **Execution Environment:** Single unified in-process runtime under Conda environment `na` (Python 3.11, NumPy 1.26.4, Brian2 2.9.0, FlyGym 1.2.1, MuJoCo 3.2.7). Verified running synchronously in the same process without IPC overhead.
* **Licensing & Attribution:** Core LIF connectome simulation adapted from the reference implementation in Shiu et al. (*Nature* 2024). Open-source under MIT License.
