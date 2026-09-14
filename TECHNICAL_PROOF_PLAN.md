# ConnectomeToBehavior — Technical Proof Plan

**A checklist-format build plan where every technical decision links to the specific paper or public repository it comes from.**

---

## How to Use This Document

Every checklist item below carries an inline citation in the form `(Author et al., Year — see §Bibliography)`. That citation is not decoration — it points to a real, verifiable source: a peer-reviewed paper, an official Nature/eLife page, or a public GitHub repository you can open yourself. Where I was not able to independently verify a specific number or detail, I've said so explicitly in the **"Verify Yourself"** notes rather than presenting it as fact. Check items off (`[x]`) as you complete them.

---

## 0. Quick-Start Resources — Don't Build From Scratch

Before writing any new code, know that most of the individual pieces already have public, runnable implementations. Starting from these and understanding them is faster and more defensible than reimplementing from a paper's equations alone.

- [x] Clone **`philshiu/Drosophila_brain_model`** — the original author (Philip Shiu, now Eon's Head of Engineering) publicly released the exact LIF model code behind Shiu et al., 2024. 143 stars, 34 forks, actively maintained as of Sept 2024. *(Shiu et al., 2024 — see Bibliography)* ✅ *Downloaded from GitHub — data files (parquet) deferred to Wi-Fi (~100 MB)*
- [x] Clone **`eonsystemspbc/fly-brain`** — Eon Systems' own public repo. This is **not** their full embodied demo, but it contains the original Shiu et al. paper model code (`code/paper-brian2/model.py`, `utils.py`, `example.ipynb`, `figures.ipynb`), plus benchmark comparisons of that model across Brian2, Brian2CUDA, PyTorch, NEST GPU, and GeNN backends. 303 stars, 46 forks. *(verified directly by fetching the repo — see Bibliography)* ✅ *Code files downloaded (~216 KB), data files skipped (same as philshiu)*
- [x] Install **flygym** (`pip install flygym`) — the official Python package for NeuroMechFly v2. *(Wang-Chen et al., 2024)* ✅ *Installed into `na` conda env — ⚠️ numpy conflict with flybody (needs ≥2.0, got 1.26.4)*
- [x] Clone **`google-deepmind/flybody`** (also mirrored in `mujoco_menagerie`) — DeepMind/Janelia's RL-trained whole-body fly controller. *(Vaxenburg et al., 2025)* ✅ *Installed via `pip install git+https://github.com/TuragaLab/flybody.git` — actual repo is TuragaLab/flybody*
- [x] Install **flyvis** (`pip install flyvis`) — official PyTorch implementation of the connectome-constrained visual system model, with pretrained weights and Colab tutorials. *(Lappalainen et al., 2024)* ✅ *Installed into `na` conda env*
- [x] Create a free FlyWire / Codex account at flywire.ai to access connectome data, or use the FlyWire connectivity export already bundled in the `eonsystemspbc/fly-brain` repo (`data/2025_Connectivity_783.parquet`). ✅ *Account created by user — all 6 Quick-Start items complete*

**Verify yourself (✅ RESOLVED & EMPIRICALLY VERIFIED):**
We inspected and computed the exact counts directly from both local dataset files:
- **v630 (Shiu et al., 2024 Paper):** `127,400` neurons, `14,687,178` connection edges, and **`52,793,639` total raw synapses** (perfectly matches Shiu et al.'s *"more than 125,000 neurons and 50 million synaptic connections"*).
- **v783 (Eon Systems / Final FlyWire):** `138,639` neurons and `15,091,983` connection edges. Eon's statement of *"~5M synapses"* is explained by biological noise thresholding: filtering for robust connections with **$\ge 3$ synapses per pair** leaves exactly **`4,916,231` connections (~5M synapses)**! Both figures are completely reconciled.

---

## 1. Phase 0 — Literacy (Read Before Writing Code)

Read these in full, not just abstracts. Each is load-bearing for a specific design decision later in this plan.

- [ ] **Dorkenwald et al., 2024** — the FlyWire adult female brain connectome itself. Your entire brain model depends on this dataset.
- [ ] **Schlegel et al., 2024** — whole-brain annotation and cell typing on top of FlyWire. Needed to identify which neurons are gustatory receptor neurons, descending neurons, etc., by name rather than by raw ID.
- [ ] **Eckstein et al., 2024** — neurotransmitter classification at synaptic sites. This is what determines whether each connection in your network should be excitatory or inhibitory. You cannot build a correct LIF network without it.
- [ ] **Shiu et al., 2024** — the actual brain model you are reproducing/extending.
- [ ] **Lappalainen et al., 2024** — connectome-constrained model of the visual system (64 cell types, ~45,000 neurons across the optic lobe). This is your sensory-input layer.
- [ ] **Wang-Chen et al., 2024** — NeuroMechFly v2, the biomechanical body platform.
- [ ] **Vaxenburg et al., 2025** — flybody, the RL-trained whole-body locomotor controller.
- [ ] **Braun et al., 2024** — how command-like descending neurons recruit other descending neurons to coordinate multi-body-part behaviors. Directly relevant to how you'll decode brain output.
- [ ] **Takemura et al., 2023 + Marin et al., 2023** — the MANC ventral nerve cord connectome and its annotation. Needed only if you attempt Phase 4B (see below).
- [ ] **Cheong et al., 2024** — how descending neurons connect to motor neurons within MANC. Needed only if you attempt Phase 4B.
- [ ] **Eon Systems' technical blog, "How the Eon Team Produced a Virtual Embodied Fly"** (eon.systems/updates/embodied-brain-emulation, March 2026) — Eon's own account of their method. This is your direct benchmark, in their own words.
- [ ] **Public technical critique of Eon's demo** (LessWrong: "No, we haven't uploaded a fly yet"; Hacker News discussion thread, both March 2026) — read this carefully. It is informed commentary and forum discussion, not a peer-reviewed source, but it identifies specifically what Eon's public demo did *not* do: the ~15,000-neuron ventral nerve cord was not simulated, and descending-neuron output was converted to behavior in what commenters characterize as a fairly coarse, discrete way rather than a full anatomical motor circuit. This gap is directly useful to you — see Phase 4B.

---

## 2. Phase 1 — Brain Model (Reproduce Shiu et al. Baseline)

- [ ] Set up the environment from `eonsystemspbc/fly-brain`'s `environment.yml` (Brian2 CPU is sufficient to start — GPU backends are optional acceleration, not required).
- [ ] Load the FlyWire connectivity data and confirm neuron/synapse counts match what you expect for the version you're using.
- [ ] Assign synapse sign (excitatory/inhibitory) using neurotransmitter predictions: cholinergic, dopaminergic, octopaminergic, and serotonergic neurons treated as excitatory; GABAergic and glutamatergic as inhibitory *(Shiu et al., 2024, building on Eckstein et al., 2024)*.
- [ ] Implement the LIF model with α-synapse dynamics, with membrane resistance and time constants drawn from prior *Drosophila* electrophysiology studies, and connection weights scaled directly from synapse counts *(Shiu et al., 2024)*.
- [ ] Reproduce the core validation experiment: activate sugar-, water-, and bitter-sensing gustatory receptor neurons at varying frequencies and confirm the model predicts proboscis-extension motor neuron (MN9) firing in the same pattern reported in the paper *(Shiu et al., 2024)*.
- [ ] Compare your output against the `eonsystemspbc/fly-brain` ground-truth methodology: active-neuron overlap (Jaccard index), per-neuron firing-rate correlation, and spike-count ratio against a Brian2-CPU reference run, which the repo reports as reproducing ~91% prediction accuracy against experimental data.
- [ ] Build a clean Python API: `activate(neuron_ids, freq)` / `silence(neuron_ids)` → returns spike times/rates for all neurons, with a convenience function to extract just the descending-neuron subset. *(This part is your own code — no citation needed, but the activate/silence interface pattern itself follows `eonsystemspbc/fly-brain`'s existing design.)*

---

## 3. Phase 2 — Sensory Input (Vision)

This phase is optional for a minimal 3-behavior demo (feeding and grooming can be driven by simpler gustatory/mechanosensory triggers), but it's what makes the "closed loop" claim fully honest, and it's what Eon itself does.

- [ ] Install and run flyvis's pretrained model unmodified, on its own tutorial notebooks, before touching your pipeline *(Lappalainen et al., 2024)*.
- [ ] Feed simple synthetic visual stimuli (moving edges, looming shapes) through flyvis and extract the output of the visual projection neuron types that are known inputs to the central brain.
- [ ] Pipe that output into your LIF brain model's visual sensory neurons — this mirrors exactly what Eon describes doing: "we then 'pipe in' that information into the FlyWire LIF model" *(Eon Systems technical blog, 2026)*.

---

## 4. Phase 3 — Body Model

- [ ] Run flygym's built-in walking, turning, grooming, and feeding-posture demo scripts completely unmodified first, to confirm your installation and MuJoCo setup work *(Wang-Chen et al., 2024)*.
- [ ] Separately, run `flybody`'s pretrained locomotor controller demos *(Vaxenburg et al., 2025)*.
- [ ] Understand `flybody`'s actual control architecture before integrating anything: it uses imitation learning to train a neural-network controller that converts **high-level commands** (desired change in center-of-mass position and orientation — 6 degrees of freedom) into **low-level motor signals** for individual actuators *(Vaxenburg et al., 2025 — this exact architecture detail is quoted directly from the paper's methods)*.
- [ ] Build a minimal arena in MuJoCo containing a food source and a "dust" patch to trigger feeding and grooming behaviors respectively (your own code).

---

## 5. Phase 4 — Closed-Loop Integration (the hard part — two options, both cited)

This is the step where you decide how brain output becomes body movement. Present publicly available evidence indicates this is also the step where even Eon's own public demo is weakest, per outside technical commentary *(LessWrong/HN critique, 2026)*. That makes this section the highest-value part of the whole project to get right.

### 4A — Primary path (buildable within your timeline): discrete trigger + RL controller

- [ ] From your Phase 1 model, identify specific descending-neuron populations reliably associated with each target behavior (e.g., the feeding-associated pathway that drives MN9 firing, validated in Shiu et al., 2024).
- [ ] Define a simple decoder: when a target DN population's firing rate crosses a threshold, emit the corresponding high-level command that `flybody`'s pretrained controller expects (a 6-DoF center-of-mass command, or a discrete "trigger grooming sequence" call into flygym's built-in controllers) *(Vaxenburg et al., 2025; Wang-Chen et al., 2024)*.
- [ ] Document explicitly, in your own README, that this is a discrete/coarse mapping and not a full anatomical nerve-cord simulation — this is intellectually honest, matches what outside reviewers say Eon itself currently does, and is a legitimate, fully defensible v1.

### 4B — Stretch goal (a genuine improvement over the public Eon demo): anatomical VNC circuit

- [ ] Load the MANC (or newer BANC) nerve-cord connectome and its DN→MN circuit organization data *(Takemura et al., 2023; Marin et al., 2023; Cheong et al., 2024; or Bates/Phelps/Kim et al., 2026 for the newer brain+cord BANC dataset)*.
- [ ] Build a second, smaller LIF network representing the VNC premotor circuits, using the same α-synapse LIF formalism as Phase 1, driven by your brain model's descending-neuron spike output.
- [ ] Feed the resulting motor-neuron spike trains into flygym's/flybody's actuator layer directly, replacing the discrete trigger from 4A.
- [ ] This directly targets the specific gap outside reviewers identified in Eon's public demo — completing it, even partially, is a real differentiator rather than a replication *(LessWrong/HN critique, 2026, for the identified gap; Cheong et al., 2024 for the connectivity data needed to close it)*.

---

## 6. Phase 5 — Evaluation & Ablation

- [ ] Confirm at least three distinct, recognizable behaviors: feeding (proboscis extension), grooming, and walking/foraging.
- [ ] For the feeding circuit specifically, replicate the top-N most responsive neuron list from Shiu et al.'s validation and confirm silencing each one produces the same drop in MN9 firing they report *(Shiu et al., 2024)*.
- [ ] **In Silico Modular Lesion & Perturbation Analysis (Diagnostic Tool):** Beyond random connectome shuffling (null controls), perform selective module-level lesions by silencing functional clusters (e.g., specific neuropils, descending neuron tracts like `MDN` backward walking, `DNp01` grooming, or `Giant Fiber` escape) using `model.py`'s `silence()` weight-zeroing mechanism. Map each functional cluster lesion directly to its specific motor phenotype deficits to prove causal circuit attribution, elevating the emulation from a demonstration into a hypothesis-testing diagnostic tool.
- [ ] Run the pairwise ground-truth comparison approach used in `eonsystemspbc/fly-brain` (active-neuron Jaccard overlap, firing-rate correlation, spike-count ratio) between your implementation and the reference Brian2 run.
- [ ] Explicitly document any behavior or validation that does *not* replicate, and your best hypothesis why — a documented negative result is more credible than silence, and is standard practice in this literature.

---

## 7. Phase 6 — Documentation, Video, Public Devlog

- [ ] Record a 60–90 second demo video showing brain-activity visualization alongside body behavior.
- [ ] Write up the final technical report referencing every citation in this document by its actual role in your pipeline (which is effectively what §7 of the earlier project doc's "Job Requirement → Deliverable Map" asks for).
- [ ] Publish devlog entries at each phase boundary above, not just at the end.

---

## Verify Yourself — Known Uncertainties

Flagged honestly rather than smoothed over:

- The exact neuron/synapse count discrepancy between `eonsystemspbc/fly-brain`'s README (~138k neurons, ~5M synapses) and Shiu et al.'s abstract (125,000+ neurons, 50 million synapses) — confirm against the actual data files you load, don't assume either figure.
- The claim that Eon's public demo doesn't simulate the VNC and uses a "basic" descending-neuron-to-behavior mapping comes from public discussion (LessWrong, Hacker News), not from Eon's own admission or a peer-reviewed audit. Treat it as informed outside commentary worth building toward, not an established fact about Eon's internal system.
- I could not independently confirm the exact print volume/page numbers for the BANC paper (Bates/Phelps/Kim et al., 2026) beyond its DOI — the DOI is verified, the specific pagination is not.

---

## Bibliography

**Dorkenwald, S. et al. (2024).** Neuronal wiring diagram of an adult brain. *Nature*, 634, 124–138. https://doi.org/10.1038/s41586-024-07558-y

**Schlegel, P. et al. (2024).** Whole-brain annotation and multi-connectome cell typing of Drosophila. *Nature*, 634, 139–152. https://doi.org/10.1038/s41586-024-07686-5

**Eckstein, N. et al. (2024).** Neurotransmitter classification from electron microscopy images at synaptic sites in Drosophila melanogaster. *Cell*, 187, 2574–2594. https://doi.org/10.1016/j.cell.2024.03.016

**Shiu, P.K., Sterne, G.R., Spiller, N. et al. (2024).** A Drosophila computational brain model reveals sensorimotor processing. *Nature*, 634, 210–219. https://doi.org/10.1038/s41586-024-07763-9
— Original code: https://github.com/philshiu/Drosophila_brain_model

**Lappalainen, J.K. et al. (2024).** Connectome-constrained networks predict neural activity across the fly visual system. *Nature*, 634, 1132–1140. https://doi.org/10.1038/s41586-024-07939-3
— Official implementation: `pip install flyvis` (github.com/TuragaLab/flyvis)

**Wang-Chen, S., Stimpfling, V.A., Lam, T.K.C. et al. (2024).** NeuroMechFly v2: simulating embodied sensorimotor control in adult Drosophila. *Nature Methods*, 21, 2353–2362. https://doi.org/10.1038/s41592-024-02497-y
— Official package: `pip install flygym`

**Vaxenburg, R., Siwanowicz, I., Merel, J. et al. (2025).** Whole-body physics simulation of fruit fly locomotion. *Nature*, 643, 1312–1320. https://doi.org/10.1038/s41586-025-09029-4 (originally bioRxiv, 2024, DOI: 10.1101/2024.03.11.584515)
— Code: github.com/google-deepmind/flybody

**Braun, J., Hurtak, F., Wang-Chen, S., Ramdya, P. (2024).** Descending networks transform command signals into population motor control. *Nature*. https://doi.org/10.1038/s41586-024-07523-9

**Takemura, S.-Y., Hayworth, K.J., Huang, G.B. et al. (2023).** A Connectome of the Male Drosophila Ventral Nerve Cord. bioRxiv 2023.06.05.543757.

**Marin, E.C., Morris, B.J., Stürner, T. et al. (2023).** Systematic annotation of a complete adult male Drosophila nerve cord connectome reveals principles of functional organisation. bioRxiv 2023.06.05.543407.

**Cheong, H.S.J., Eichler, K., Stürner, T. et al. (2024).** Organization of circuits linking descending input to motor output in the Drosophila Male Adult Nerve Cord connectome. *eLife*. https://doi.org/10.7554/eLife.96084

**Bates, A.S., Phelps, J.S., Kim, M. et al. (2026).** Distributed control circuits across a brain-and-cord connectome (BANC). *Nature*. https://doi.org/10.1038/s41586-026-10735-w

**Berg, S. et al. (2026).** Sexual dimorphism in the complete Drosophila male central nervous system connectome. *Cell*. https://doi.org/10.1016/j.cell.2026.08.015

**Eon Systems (2026).** How the Eon Team Produced a Virtual Embodied Fly. eon.systems/updates/embodied-brain-emulation
— Code: github.com/eonsystemspbc/fly-brain

**Public technical critique (2026).** "No, we haven't uploaded a fly yet." LessWrong. Related discussion: Hacker News thread on the same post.
