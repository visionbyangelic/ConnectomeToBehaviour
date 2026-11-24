<div align="center">

# ConnectomeToBehaviour
<img width="1170" height="639" alt="Whole-brain render of the Drosophila connectome, neurons coloured by type" src="assets/whole-brain-fly-render.jpg" />

### Does the wiring matter? A closed-loop simulation of the fruit fly's whole central brain, the FlyWire connectome driving a simulated body, testing with pre-registered controls how much of its behaviour is written in the wiring itself.

<br>

[![Status](https://img.shields.io/badge/●_Ongoing-1a1a1a?style=for-the-badge&labelColor=1a1a1a&color=f0c14b)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-1a1a1a?style=for-the-badge&labelColor=1a1a1a&color=6ee7b7)](LICENSE)
[![Started](https://img.shields.io/badge/Started-6_Sep_2026-1a1a1a?style=for-the-badge&labelColor=1a1a1a&color=93c5fd)](https://github.com/)


**Author:** [Angelic Charles](https://visionbyangelic.github.io)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--7279--9663-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0008-7279-9663)

</div>

---

## Overview

ConnectomeToBehaviour is a closed-loop simulation of the adult *Drosophila melanogaster* central brain,
built from the FlyWire connectome (materialisation v630: 127,400 neurons and about 14.7 million
connections). Every neuron is a leaky integrate-and-fire unit simulated in Brian2, following the model of
Shiu et al. (*Nature*, 2024), and the brain is connected to a physically simulated fly body in MuJoCo,
through FlyGym and the FlyBody model.

The loop runs in both directions. What the body senses drives the brain; what the brain does moves the
body; and the movement changes what the body senses next. The connectome is the only biological wiring in
the system. Everything else, the sensory encoder on the way in and the motor decoder and body controllers
on the way out, is an engineered layer that I document and account for.

## Why it matters

Connectomics now delivers complete wiring diagrams of real brains. A wiring diagram on its own, however,
does not say how much of an animal's behaviour it explains. Whole-brain simulations usually demonstrate
that a model *can* produce activity or movement. The harder question is whether the specific wiring is
doing the work, or whether the layers wrapped around it are: the encoder that turns stimuli into neural
drive, the decoder that turns neural activity into movement, and the controllers built into the body.

This project is built to answer that question with controlled interventions instead of demonstrations,
and to account for every behaviour it produces: which part came from the connectome, and which parts came
from the added layers. As more connectomes are published, that accounting is the difference between a
research result and a demo.

## Research questions

The main question:

> With neuron rules, body physics, encoder and decoder held fixed and documented, how do the target
> behaviours change, and within what bounds, when the connectome's topology is intervened on?

I ask it in three precise forms:

- **E-Total.** How does behaviour change when the intact connectome is replaced by graded shuffled
  versions of itself, which preserve connection statistics while destroying the specific topology?
- **E-Pathway.** How does behaviour change when a behaviour's own pathway is lesioned, compared with
  matched control lesions of the same size elsewhere in the network?
- **E-Baseline.** How does the intact system compare with connectome-free, rule-based controllers
  driving the identical body?

Two supporting measurements run alongside. The first is the model's gustatory baseline: how it responds
to sugar, to bitter, to both together, and to water, including whether bitter suppresses the feeding
response to sugar (research question RQ-C2). The second is provenance accounting: for each behaviour,
how much of the outcome is attributable to the encoder and decoder layers rather than to the wiring.
Feeding is the first behaviour under test; walk and halt behaviour follows.

## Approach

The pipeline is a single loop: connectome, spiking brain, decoder, body, and constructed sensory
feedback, coupled every 100 ms. The intervention design is comparative throughout. Every comparison
runs through the identical body, decoder and conditions; only the wiring changes. A shuffled network,
a lesioned network and the intact network therefore face exactly the same test, and any difference in
behaviour is attributable to the wiring itself.

The working discipline is fixed in advance. The comparisons, metrics and decision criteria for each
experiment are written down and frozen before the runs they govern. The decoder is calibrated on
separate data and frozen before evaluation, with a refit control run alongside. Every claim the project
makes is conditional on the model and its documented choices, and is stated that way: these experiments
measure how *this* model's behaviour depends on *this* model's wiring. They do not, by themselves,
measure a living fly.

## Current work

The brain model has been rebuilt from the published sources and validated against the published
reference output, and the closed feeding loop is built and running. I am currently measuring the
model's gustatory baseline conditions and preparing the feeding intervention experiment, the first full
test of the research questions above.

## Earlier prototype

A first build of this project is preserved in [`v0-prototype/`](v0-prototype/) (tag
`v0-prototype-final`) for the record. It validated the brain model and verified the body stack; its
brain-to-body bridge was never built.

## Key references

- Shiu, P.K. et al. (2024). A *Drosophila* computational brain model reveals sensorimotor processing. *Nature* 634, 210 to 219. https://doi.org/10.1038/s41586-024-07763-9
- Dorkenwald, S. et al. (2024). Neuronal wiring diagram of an adult brain. *Nature* 634, 124 to 138. https://doi.org/10.1038/s41586-024-07558-y
- Wang-Chen, S. et al. (2024). NeuroMechFly v2: simulating embodied sensorimotor control in adult *Drosophila*. *Nature Methods* 21, 2353 to 2362. https://doi.org/10.1038/s41592-024-02497-y
- Sapkal, N. et al. (2024). Neural circuit mechanisms of behavioural choice in *Drosophila*. *Nature* 634, 191 to 200.
- Bates, A.S., Phelps, J.S., Kim, M. et al. (2026). Distributed control circuits across a brain-and-cord connectome. *Nature* 656, 957 to 970. https://doi.org/10.1038/s41586-026-10735-w

This project builds entirely on public data and open-source tools from the FlyWire Consortium, the
FlyEM Project Team at HHMI Janelia, the BANC-FlyWire Consortium, and the NeuroMechFly team at EPFL.
None of the underlying connectome or body-simulation data was generated by me; my contribution is the
closed-loop integration, the controlled intervention design, and the validation.

## How to cite

> Charles, A. (2026). *ConnectomeToBehaviour: Does the wiring matter? A closed-loop simulation of the
> fruit fly's whole central brain, testing how much of its behaviour is written in the wiring itself*
> [Software/research project]. GitHub: https://github.com/visionbyangelic/ConnectomeToBehaviour.
> Version 0 (archived prototype) is preserved under `v0-prototype/`, tag `v0-prototype-final`.

## License

MIT. See [LICENSE](LICENSE).
