<div align="center">

# ConnectomeToBehaviour

### Does the wiring matter? A controlled test of how much of a fruit fly's behaviour is written in its connectome

[![License](https://img.shields.io/badge/License-MIT-1a1a1a?style=for-the-badge&labelColor=1a1a1a&color=6ee7b7)](LICENSE)

**Author:** [Angelic Charles](https://visionbyangelic.github.io)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--7279--9663-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0008-7279-9663)

</div>

---

## What this project is

I am rebuilding, from public data and free tools only, a fruit fly that runs on its real brain wiring —
and then testing, honestly and with controls, whether the wiring itself is doing the work.

The system takes the synapse-resolution wiring diagram of the adult *Drosophila melanogaster* central
brain (the **FlyWire connectome, materialisation v630**), gives every neuron the same simple, standard
firing rules (a leaky integrate-and-fire model, as in Shiu et al., *Nature* 2024), connects the brain's
output to a physically simulated fly body (MuJoCo, via NeuroMechFly v2 / FlyGym), and closes the loop:
what the body senses drives the brain, what the brain does moves the body, and the movement changes
what the body senses next.

The defining discipline of this project is **provenance**. For every behaviour it produces, I account
for which parts came from the connectome and which came from the layers I had to add — the *encoder*
on the way in, the *decoder* and the body's own *controllers* on the way out. That accounting is the
difference between a research result and a demo video. Every claim here is also **model-conditional**:
the experiments measure how *this model's* behaviour depends on *this model's* wiring, under documented
encoder, decoder and body choices. They do not, by themselves, measure a living fly.

## The question

> With neuron rules, body physics, encoder and decoder held fixed and documented, how do the target
> behaviours change — and within what bounds — when the biological connectome's topology is intervened
> on: intact versus graded shuffled versions of itself, targeted lesions versus matched control
> lesions, and intact versus connectome-free baselines and controllers run through the identical body?

In plain words: does the real wiring actually matter, or would any wiring — or even a few simple
if-then rules — produce the same behaviour through the same body? I ask it three precise ways, and I
never claim a tidy percentage split ("the connectome contributes X%"), because this design cannot
honestly give one.

This is the project's centrepiece — a **controlled comparative intervention experiment**, run
identically for each behaviour, with the comparisons, metrics and pass criteria written down *before*
the results exist.

## What is being built

**Core-A — the complete, publishable unit.** Rebuild the published brain model to a stated standard;
audit what the simulated body can actually do; build a population-based decoder for feeding and freeze
it before evaluation; then run the intervention experiment for feeding (intact vs lesioned vs shuffled
vs rule-based), with sensitivity checks (parameter changes, sign-uncertainty, closed-loop vs open-loop
replay) and a compute benchmark reported as a result. If the project stopped at Core-A it would still
be a finished piece of work — a positive separation *or* a demonstrated equivalence are both results.

**Core-B — the full core.** The same treatment for **walk/halt** (does the model stop walking to feed,
the way real flies do?). Grooming was in the original design and was dropped by the body audit
(Part 1b): the shipped body cannot honestly express it, so it is out rather than faked.

**Stretch — separately gated, never allowed to sink the core.** A bounded circuit from BANC (the 2026
brain-and-nerve-cord connectome) for one behaviour's pathway; a GPU backend held to a parity check
against the CPU reference; a cross-body check in flybody; vision, neural-first; replication on an
independent connectome; and a sensitivity run on FlyWire v783.

**Explicitly out of scope:** flight as a claimed behaviour, courtship, learning/plasticity, hunger
modelling, whole-CNS simulation, and any claim of "upload" or consciousness.

## Status — in progress, gated, nothing hidden

This is a fresh rebuild, built in parts. Each part has its pass criteria pre-registered before work
starts, is independently reviewed, and is only marked passed when the evidence is in. The rebuild was
developed off-GitHub through its early gates; on 24 Nov 2026 I decided to publish the work in
progress as it stands, ahead of the original schedule. This page describes the project and the state
of the evidence — it claims no results the runs have not produced. The rebuild's code,
preregistrations and tests live under [`fresh/`](fresh/).

| Part | What | State |
| :--- | :--- | :--- |
| 0 | Foundations: plan, registers, metrics, benchmark | **Passed** — closed 23 Nov 2026 |
| 1 / 1b | Environment + v630 data · Body-capability audit | **Passed** — closed 23 Nov 2026; the audit chose FlyBody for the feeding body |
| 2 / 2b | Brain model · Minimal end-to-end loop (built early, on purpose) | **Passed** — closed 23–24 Nov 2026; the minimal loop runs stably |
| 3 | Brain validation against Shiu et al. | Sugar rung **passed** (closed 23 Nov 2026). The four-conditions rung is preregistered, frozen 24 Nov 2026, and its runs are in progress — no results claimed yet |
| 4 | Sensory specifications · Feeding-body qualification | **Passed** — closed 24 Nov 2026; the feeding body qualified at its pre-registered gate |
| 5 | Full closed loop (feeding) + preregistration freeze | Loop **built** and tested; preregistration approved — the freeze (calibration first) comes next |
| 6 | **Comparison checkpoint vs Version 0** | Not yet run — the comparison still happens here. The v0 bundle and this publication were moved forward to 24 Nov 2026 at my decision; only the timing changed |
| 7 / 7b | Intervention experiment — feeding · walk/halt | Not started — Part 7 waits on the four-conditions rung completing |
| 8 | Documentation + release | In progress — this publication is an early act of it, moved forward; the full release still closes the project |

Two stop rules I hold myself to: if the published brain cannot be reproduced to the pre-set standard,
the project pivots to a reproduction-failure report rather than building on an untrusted brain; and a
part that exceeds its budget stops and comes back to me with options — it does not silently expand.

## Version 0 — my first build, preserved in full

The first version of this project lives in [`v0-prototype/`](v0-prototype/) — bundled, labelled, and
kept in this repository on purpose, because it is a research output that may help somebody else, and
because this project's paper trail should show the first attempt, not just the polished one.

What v0 did: it validated the whole-brain model against Shiu et al.'s published output (Pearson
**0.9936**; sugar drove the feeding motor neuron MN9 to **83.5 ± 6.5 Hz** left / **58.7 ± 5.2 Hz**
right, bitter alone gave **0 Hz**, and bitter suppressed the sugar response by **89.1% / 75.8%**),
verified the body stack, and then stopped — its brain-to-body bridge was never built. Its full
results, its open questions (including an MN9 left/right asymmetry I had not resolved), and its
complete build log are in the folder, unchanged, and its exact pre-archive state is frozen at the
tag `v0-prototype-final`.

## How to reproduce

*(Commands are finalised at the release gate; the shape of it is fixed now.)*

- **CPU is the reference platform** for every confirmatory result. GPU runs are exploration-only,
  and only count after passing a parity check against the CPU on identical input.
- The environment is pinned and built from scratch (lockfiles in the repo); the brain and body stacks
  are isolated environments, as they were in v0.
- Data is public and fetched by a documented procedure: FlyWire v630 from the Shiu et al. release,
  with file hashes recorded. The datasets themselves are not stored on GitHub.
- Every run records its code version, data hashes, seeds and configuration in a run manifest, so any
  number on this page can be traced to the exact run that produced it.

## Where this goes

Preprint first, as soon as Core-A is complete — whatever its outcome. Core-A then goes to a NeuroAI
workshop or a reproduction venue; Core-A + Core-B is the journal version. The demo video comes after
the science, as the advert for it — never as the evidence.

## Key references

- Shiu, P.K. et al. (2024). A *Drosophila* computational brain model reveals sensorimotor processing. *Nature* 634, 210–219. https://doi.org/10.1038/s41586-024-07763-9
- Dorkenwald, S. et al. (2024). Neuronal wiring diagram of an adult brain. *Nature* 634, 124–138. https://doi.org/10.1038/s41586-024-07558-y
- Wang-Chen, S. et al. (2024). NeuroMechFly v2: simulating embodied sensorimotor control in adult *Drosophila*. *Nature Methods* 21, 2353–2362. https://doi.org/10.1038/s41592-024-02497-y
- Bates, A.S., Phelps, J.S., Kim, M. et al. (2026). Distributed control circuits across a brain-and-cord connectome. *Nature* 656, 957–970. https://doi.org/10.1038/s41586-026-10735-w
- Sapkal, N. et al. (2024). Neural circuit mechanisms of behavioural choice in *Drosophila*. *Nature* 634, 191–200.

This project builds entirely on public data and open-source tools from the FlyWire Consortium, the
FlyEM Project Team at HHMI Janelia, the BANC-FlyWire Consortium, and the NeuroMechFly team at EPFL.
None of the underlying connectome or body-simulation data was generated by me — my contribution is
the closed-loop integration, the controlled intervention design, the empirical validation, and the
documentation.

## How to cite

> Charles, A. (2026). *ConnectomeToBehaviour: Does the wiring matter? A controlled test of connectome
> contributions to Drosophila behaviour* [Software/research project]. GitHub:
> https://github.com/visionbyangelic/ConnectomeToBehaviour — Version 0 (archived prototype) under
> `v0-prototype/`, tag `v0-prototype-final`.

## License

MIT — see [LICENSE](LICENSE).
