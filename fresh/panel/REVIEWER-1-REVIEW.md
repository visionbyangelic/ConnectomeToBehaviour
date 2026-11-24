# Panel review — Claude (Reviewer 1, lead)
Date: 23 Nov 2026, 14:58-15:03 WAT. Free tier, Sonnet 5.5 Medium, account "Nerdy · Free". Source: https://claude.ai/chat/e3e2b04f-0f06-4905-bb69-f068f549879b
Status: COMPLETE sections 1-10 (two responses). Free-message limit hit AFTER completion (until 16:00).
CAVEAT (Claude's own): no live searches; knowledge to ~mid-2026; many claims flagged MUST-VERIFY against sources before plan/application use.

## 1-2. Missing / could be wrong
- Missing literature: Lappalainen 2024, Pospisil 2024 effectome, Eckstein sign accuracy must be quantified, Sapkal/Bidaye walk-halt animal data, Hampel grooming, PER literature, Dorkenwald/Schlegel versioning, Marin DN-type matching across datasets (male MANC evidence -> female brain decoder).
- Model limits to document: no gap junctions/neuromodulation, uniform weight-per-synapse, Poisson drive assumptions, NO parameter-sensitivity analysis yet.
- NEW failure mode named: the ENCODER (body state -> sensory input) is a second hand-built layer — provenance must cover encoder too, not just decoder/controller.
- Readout circularity: readout neurons must be fixed from literature BEFORE simulation, not chosen because they respond.
- Body feasibility UNCERTAIN: not sure FlyGym actuates a proboscis or supports contact-rich grooming — audit required.
- Old MN9 L/R asymmetry (83.5 vs 58.7) must be resolved: real asymmetry or bug.
- Pearson across 127k mostly-silent neurons inflated by sparsity — add rank correlation on active subset, noise ceiling.
- Panel correlation: 4 AIs share failure modes; can agree on a wrong citation.
- Conclusions: (1) is a negative universal — log search protocol; (3) critics = grey literature, label as hypothesis not finding; (4) BANC wording check vs MaleCNS; (2)/(7) rest on blog+repo — cite versions/dates.
- Substitution test "NOT decisive as designed": estimand undefined (no additive attribution); straw-man nulls (add graded nulls); decoder fairness — run frozen AND refit-per-condition decoder; rule script must be adversarial/parameter-matched; add body-only baselines; lesions test the MODEL unless compared to published animal silencing data; pre-register effect sizes/power/seeds/equivalence (TOST) — null = success only if equivalence demonstrated; FEEDING IS A WEAK TEST CASE (MN9 threshold -> PER is nearly a rule) — walk/halt + grooming are discriminating.

## 3. Decisions
D1 AGREE (+ late v783 sensitivity check; confirm v630 downloadable). D2 AGREE CONDITIONAL (early wall-clock benchmark + pre-set GPU trigger). D3 PARTLY AGREE (gate order on body-capability audit; walk/halt may come first / be discriminating; feeding = simplest readout). D4 AGREE. D5 AGREE (+ equivalence requirement). D6 AGREE WITH CHANGES (add >=1 human expert check at pre-registration + final; assign adversarial panel roles). D7 AGREE (release tag, optional Zenodo DOI, never force-push, README pointer to legacy).

## 4-5. Scope / biggest risk
Core defensible but large for one researcher: split Core-A (brain reproduction + feeding + substitution test = complete publishable unit) / Core-B (+ walk/halt; grooming optional).
Biggest risk: CONSTRUCT VALIDITY — design measures the MODEL's behaviour dependence on the MODEL's wiring under hand-built encoder/decoder/body, not a real fly's behaviour. Mitigation: rewrite question/title as model-conditional; pre-register factorial estimand; fix readouts from literature; frozen+refit decoder controls; adversarial rule script; graded nulls + equivalence; >=1 held-out prospective prediction vs published animal data.

## 6. NOVELTY
Verdict: worth doing ONLY as an audit/methods contribution, NOT a discovery paper. "The novelty is in the test design, not the system."
Not new: embodied connectome fly (Eon did a demo), reproducing Shiu, lesion/shuffle controls per se, provenance labelling (reporting convention), raising the rule-script criticism.
Potentially genuinely new (verify via systematic search first): (1) pre-registered quantitative substitution test of an embodied whole-brain model; (2) factorial attribution brain x encoder x decoder x body; (3) graded nulls + refit-decoder controls = measurable gradient; (4) demonstrated-equivalence null as first-class outcome.

## 7. BUILD METHOD
- Bridge comes TOO LATE in our plan — repeats old build's failure mode. Build a minimal end-to-end loop (toy decoder) FIRST.
- Front-load de-risking in first weeks: body-capability audit, wall-clock benchmark, encoder design.
- Literacy as gated part = wasteful (already failed once): time-box, parallel, no gate.
- Pre-register ONLY confirmatory parts; don't pre-register exploratory work.
- Freeze estimand/metrics/readouts BEFORE building decoder.
- Two gate types: hard (pre-registration, substitution design) vs light check-ins — Angelic approving every part is a bottleneck.
- Comparison checkpoint: LOW scientific value + anchoring risk — meaningful reference is Shiu's released outputs; old repo = debugging aid, not pass/fail target.
- Missing: kill criteria + time budget per part, risk register, seed policy, data hashes, run manifests, container/lockfiles, interface tests, CI regenerating headline numbers, negative-result write-up plan.

## 8. ADDITIONAL RESEARCH QUESTIONS
Core: Q1 parameter sensitivity (±20-50% weights/rate/thresholds/tau) low-mod; Q2 sign-uncertainty Monte Carlo flips low; Q3 closed-loop vs open-loop replay low; Q4 out-of-distribution/conflict/graded stimuli moderate; Q5 decoder capacity sweep (linear vs MLP vs refit) moderate; Q6 prospective prediction vs animal data (min 1 case) moderate; Q10 compute benchmark as reported result low.
Stretch: Q7 minimal-circuit sufficiency moderate; Q8 v783 sensitivity low (late core/stretch); Q9 cross-dataset replication (hemibrain/MaleCNS) high.

## 9. PUBLISHABILITY
Path: preprint first (bioRxiv, or arXiv q-bio.NC — may need endorser). Core-A -> NeurIPS/ICLR NeuroAI workshop (4-8pp) or ReScience C. Core-A+B full factorial -> PLOS Comp Biol / eLife (reviewed preprint) / Neuroinformatics. BANC/cross-dataset upgrades ambition only after core.
Reviewers will demand: reproduction fidelity with noise ceiling + thresholded Jaccard + rank correlation; Q1+Q2 sensitivity; full factorial with CIs/effect sizes/seeds/equivalence; stated estimand, model-scoped claims; adversarial matched rule baseline; >=1 animal-data comparison; provenance labels; open code with DOI; data-version statements; FlyWire/Shiu licence compliance; fair Eon citation.
Unpublishable if: video as evidence, single-seed results, loop never run, undefined "how much", biological claims from model-vs-model, straw-man baselines/nulls, unaddressed Eon overlap, irreproducible code.
Practical: senior co-author/mentor if possible (ABDN/Neuromatch connections noted).

## 10. HIRING LENS (Eon / DeepMind)
Eon hires: whole-brain emulation engineering, honest limitations, full-stack building. DeepMind: rigour, ML/RL fundamentals, ablation discipline, engineering quality. Fly project alone does NOT demonstrate ML/RL depth — address via ML-flavoured analyses (Q5 etc.) or elsewhere.
Impresses: finished small honest core (or equivalence null) > large unfinished; pre-registered design that could have gone against you; one-command reproducibility, tests, CI, manifests; provenance-overlay demo video; clear public writing.
Raises doubts: old repo's empty bridge/stale stats/mislabel (address openly); scope creep / wish-list stretch; AI-generated perception — Angelic must be able to explain every equation/parameter/choice herself; tone attacking Eon (frame as hypothesis test); still "planned" at application time.
Artefact order: (1) preprint/tech report with main result, (2) repo quality/reproducibility, (3) provenance-overlay demo (supporting, not evidence), (4) plain-language write-up, (5) talk/poster.
"An honest Core-A finished well is stronger for both teams than a larger project unfinished."
