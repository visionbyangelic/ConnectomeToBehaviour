# Version 0 — My First Build (Archived Prototype)

*This folder is the preserved first version of ConnectomeToBehaviour — my original build, kept exactly
as it was, as a research output in its own right. The current version of the project lives at the root
of this repository, under `fresh/`. Nothing in here has been deleted or rewritten; if the fresh build
and this one ever disagree, the disagreement is documented, not hidden.*

---

## What v0 was

Version 0 was my first attempt at the whole pipeline: take the FlyWire connectome of the adult
*Drosophila melanogaster* central brain (materialisation **v630**, 127,400 neurons), simulate it with
leaky integrate-and-fire neurons in Brian2 following Shiu et al. (*Nature* 2024), verify the body stack
(NeuroMechFly v2 / FlyGym in MuJoCo), and then connect brain to body in a closed loop.

It got two of those three stages done, and it stopped at the third — honestly, and in the open:

- **Phase 1 — brain model: validated.** I reproduced Shiu et al.'s published model output to a high
  standard (below).
- **Phase 3 — body: verified.** The FlyGym/NeuroMechFly v2 body wrapper works, and I proved Brian2 and
  FlyGym can run together inside a single process.
- **Phase 4 — the bridge: never built.** `src/bridge/` in this folder is empty apart from its
  `__init__.py`. The descending-neuron decoder that was supposed to turn brain activity into body
  movement was designed and debated in `track.md`, but it was never implemented — so v0 never ran a
  true closed loop, and I never claimed that it did.

## What v0 found (v0 results — cite them as v0)

Canonical protocol: **1.0 s of biological time × N=10 trials**, FlyWire v630.

| Condition | MN9 Left | MN9 Right | Reading |
| :--- | :---: | :---: | :--- |
| Sugar (right-side GRNs) | **83.5 ± 6.5 Hz** | **58.7 ± 5.2 Hz** | Feeding motor activation |
| Bitter | **0.0 Hz** | **0.0 Hz** | No feeding response |
| Sugar + Bitter | **9.1 ± 3.6 Hz** (↓ 89.1%) | **14.2 ± 1.6 Hz** (↓ 75.8%) | Bitter suppresses sugar (p < 10⁻¹⁰) |
| Water | 6.0 ± 3.4 Hz | 1.6 ± 2.1 Hz | Distinct, weaker circuit |

Against Shiu et al.'s published simulation output (`sugarR.parquet` — their *model's* output, not
recordings from a living fly): **Pearson correlation 0.9936 · Jaccard overlap 0.9113 · Precision
0.9928 · Recall 0.9174** (411 shared active neurons). That benchmark establishes *reproduction
fidelity* — that my implementation faithfully reproduces their published connectome model — not a
match to a living fly.

**One open question v0 left behind, stated plainly:** under right-side sugar stimulation the left MN9
fires faster than the right (83.5 vs 58.7 Hz), while bilateral stimulation gives exact symmetry
(60.0 vs 60.0 Hz). I did not resolve whether that asymmetry is a real property of the circuit, an
artefact of the unequal left/right sensory-neuron sets in my constants (21 right vs 10 left), or a bug.
The rebuild treats resolving this as a gate: no MN9 number gets published until it is answered.

Full detail lives in this folder, unchanged: `README-original.md` (v0's own front page),
`track.md` (the complete chronological build log), `TECHNICAL_PROOF_PLAN.md` (v0's plan),
`overview.md` (v0's architecture), and `results/validation/` (the tracked validation summaries and figures).

## Why there is a new version

I rebuilt the project from zero because v0's gap was not a missing feature — it was a missing test.
V0 could show a brain responding; it could not answer the question the project actually asks:
*does the real wiring itself matter, or would scrambled wiring — or a few hand-written rules driving
the same body — do just as well?* Answering that needs the bridge built as a measured, documented
layer, the controls (lesioned, shuffled and rule-based comparisons) designed in from the start, and
every claim labelled by what actually produced it. That is what the current version, under `fresh/`
at the root of this repository, is built to do. I moved this bundle into the open on 24 Nov 2026,
ahead of the comparison checkpoint (Part 6) — my call, and it changes the timing only: the comparison
itself still happens at Part 6, its verdict and every discrepancy will be written into the decision
log then, and nothing about publishing early pre-judges it.

V0 is not an embarrassment to be tidied away. It is the first attempt, it produced real validated
results, and someone starting where I started may well learn more from it — including its empty
`src/bridge/` — than from the polished version alone.

## How to cite v0

> Charles, A. (2026). *ConnectomeToBehaviour, Version 0 (archived prototype)* [Software/research
> project]. Preserved in this repository under `v0-prototype/` and frozen at the git tag
> `v0-prototype-final`. GitHub: https://github.com/visionbyangelic/ConnectomeToBehaviour

In the paper, v0 is described as the first implementation: what it built, the validation results
above, where it stopped, and what the rebuild changed and why.

## Running v0

V0's code finds its own root from its file locations, so it still runs from inside this folder:

```bash
cd v0-prototype
python scripts/download_data.py   # fetches the v630 data into ./Drosophila_brain_model-main/ (not stored on GitHub)
# brain stack and body stack use separate environments — see environment.yml and environment-flygym.yml
python experiments/run_1s_n10_validation.py
```

The exact pre-archive state of this work — every file as it stood before the move, in its original
root layout — is frozen at the git tag **`v0-prototype-final`**.

## License

MIT — see `LICENSE` in this folder.
