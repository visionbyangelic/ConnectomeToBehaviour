# Panel review — ChatGPT (Reviewer 3)
Date: 23 Nov 2026, ~14:58-15:00 WAT. Free tier. Source chat: https://chatgpt.com/c/6b04469b-8bc0-83e8-bfe8-f867fdd5afb6
Status: COMPLETE. Overall verdict: APPROVE WITH MAJOR METHODOLOGICAL REVISIONS — direction approved, current protocol NOT approved unchanged. Governing distinction: a connectome CAN drive a behaviour ≠ the connectome CONTAINS the information necessary to produce it.

## 1. Missing (8, four potentially fatal)
1.1 Model-assumption register required: connectome ≠ functioning nervous system (weights≈counts, E/I predicted, no plasticity/neuromodulation/intrinsic properties, single specimen, no PNS/VNC). Every assumption logged with source, uncertainty, fixed-across-conditions?, conclusions-depend-on-it?
1.2 Multiple shuffled nulls — "probably the most important missing component": intact / degree-preserving / degree+neuropil-preserving / targeted lesions; preserve sign + weight distribution where feasible; null constraints pre-specified.
1.3 MN9 rate ≠ feeding: missing chain firing→recruitment→muscle→force→movement→contact→feedback. Two separate layers: biological readout vs mechanical actuator interface (labelled engineered).
1.4 Sensory-input pathway spec per stimulus: physical stimulus, sensor, sensory population, encoding, timing, calibration, grounded-or-handbuilt. Otherwise experimenter decides, not connectome.
1.5 Mandatory reading additions: Dorkenwald annotation, MANC, Hampel 2015, Calle-Schuler 2025/26 mechanosensory/grooming, Eon 2026 post as primary engineering source.
1.6 Sensitivity analyses: weight scaling, NT classification, thresholds/time constants, initial potentials, input timing, seeds.
1.7 Calibration vs evaluation separation: never tune decoder on final evaluation scenarios; held-out conditions + decoder rejection criteria.
1.8 Statistical power plan: independent shuffle replicates (networks, not just reruns), seeds, scenarios, effect size, CI method, multiple comparisons, paired seeds?

## 2. Could be wrong
- (1) Shiu: agree with qualification — frozen baseline for reproduction, NOT "best/definitive". Reproduction vs replication vs biological validation are three different things; Pearson 0.9936 would be model-to-model only.
- (3) Rule script: concern valid but test must use held-out diverse conditions; THREE baselines (fixed rule / matched-capacity controller / direct sensory-actuator) with declared comparison budget. Freeze decoder or it becomes "an invisible substitute brain".
- (4) BANC: direction correct, "anatomically correct" too strong — specimen-specific, unusually rigid phenotype, many mappings unestablished. Bounded circuit experiment only.
- (5) Cheong: don't universalise (male, circuit-specific). (6) Braun: population reading justified, but some command-like single neurons exist.
- Substitution test: NECESSARY BUT NOT DECISIVE. Rename "controlled comparative intervention experiment". Confounds + mitigations listed (decoder privilege, controller saturation, matched control lesions, open-loop replay vs closed-loop, etc.). Factorial restructure proposed. Two estimands: total topology effect vs pathway-specific effect. Convincing-result criteria specified (bitter suppression without hand-coded override; selective lesions vs matched controls; nulls lose performance; rule fails held-out; survives parameter changes) — even then only a limited topology-contribution claim.

## 3. Decisions — all 7 accepted, none rejected; D1/D6/D7 need safeguards
- D1 AGREE conditional: version audit first (provenance, ID overlap, did Shiu use this v630, did old repo use same snapshot); v783 = separate sensitivity study, never silent.
- D2 AGREE + early performance feasibility gate (time/biological second, memory, N=10 time, shuffle time).
- D3 AGREE (feeding→grooming→walk/halt); test feeding/grooming against conflicting stimuli.
- D4 STRONGLY AGREE; core must explicitly state brain-only = documented approximation of omitted VNC.
- D5 STRONGLY AGREE — "most important decision in the entire plan"; tightened definition of done (baseline reproduced/explained, body validated, decoder frozen, all conditions run, metrics reported, nulls replicated, both signs of result reported, provenance kept). A pretty video is not a finish line.
- D6 AGREE with change: panel can reject gates, but NO quiet changes to question/metrics/pass criteria after seeing results — formal amendment only.
- D7 AGREE with change: go further — immutable tag + archival branch + env spec + data hashes + outputs + comparison report + migration doc; new work as separately versioned release.

## 4. Scope
Core achievable ONLY if tightened: three ambitions of unequal difficulty — reproduction, body connection, causal topology claim (the real contribution; don't starve it). Narrower core question proposed. Behavioural fidelity levels must be defined per behaviour (no "naturalistic feeding" from proboscis movement alone). Stretch stricter entry criteria; flyvis deferred more aggressively; MaleCNS deferred (changes the question).

## 5. Biggest risk + extra requirements
Risk: decoder/controller contain more behavioural knowledge than connectome while project attributes behaviour to connectome. Mitigation: BEHAVIOURAL PROVENANCE LEDGER per behaviour (sensory input, neurons, pathway, output, decoder, controller, actuator, feedback, evidence, C/D/B classification — multiple allowed). Mandatory second test: baselines allowed a predeclared optimisation budget (fixed-implementation test vs capability test, reported separately).
Before Part 1 approval — 10-item checklist: assumption register; v630 provenance vs Shiu; spatially constrained nulls; sensory pathway spec; biological vs engineered decoder layers; matched-capacity baselines; open- vs closed-loop separation; metrics + power; provenance ledger; pre-registered permitted conclusions per outcome.
Pre-register CLAIMS not just experiments (outcome→permitted conclusion table). Immutable experiment registry (commit, dataset, hashes, lockfile, config, seed, versions, output hashes). Bridge independently testable (zero input, calibration curve, L/R, conflicts, no hidden overrides).
Final line: "Do not optimise for the most convincing fly video. Optimise for the experiment that can survive the hardest criticism."
Top 3 problems: (1) decoder/controller confounding, (2) inadequate nulls, (3) sensory/pathway assumptions.
