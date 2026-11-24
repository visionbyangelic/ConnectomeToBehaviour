# ConnectomeToBehaviour — FINAL PLAN v2 (Fresh Rebuild)

**For:** Angelic Charles — flagship project for applications to Eon Systems and Google DeepMind; publishing is a first-class goal.
**Date:** 23 November 2026. **Status:** APPROVED by the full panel (Reviewers 1–3), 23 Nov 2026 — Angelic's own confirmation still required; see §0.3.
**Governing document:** `FRESH-START-PROTOCOL.md` (Angelic's decisions, 23 Nov 2026). Where this plan and the protocol disagree, the protocol wins.
**Research check:** every load-bearing citation in this plan was checked against primary sources on 23 Nov 2026 — see `RESEARCH-CHECK.md` (32 claims: 24 verified, 5 corrected, 3 unverifiable). Corrections found there are already applied in this plan.
**Labelling rule:** **[OLD]** = from the previous repo's text, untrusted until re-derived. **[LIT]** = published literature / primary source, research-checked. **[INF]** = inference or recommendation, clearly opinion. No number appears without a label.
**How to read this document:** every technical section ends with an *In plain words:* paragraph. If a plain-words paragraph and its technical section ever seem to disagree, the technical section is the accurate one and the paragraph must be fixed — flag it.

---

## 0. What changed from v1, and the status of approval

### 0.1 Panel corrections incorporated (all of them, not a selection)

This v2 plan incorporates **all** load-bearing corrections from the three panel reviews of the v1 thought process (Claude/Reviewer 1 lead, Gemini/Reviewer 2, ChatGPT/Reviewer 3):

1. The "substitution test" is renamed and rebuilt as a **controlled comparative intervention experiment** with a defined estimand (§5). It is necessary, not decisive.
2. **Graded, multiple null families** replace the single shuffle (§5.3).
3. The decoder is run **frozen AND refit-per-condition** (§5.4).
4. The rule baseline must be **adversarial and matched in complexity/capacity**, with a declared optimisation budget — three baselines, not one strawman (§5.5).
5. **Equivalence testing (TOST):** a null result counts as a result only if equivalence is demonstrated, not merely if a difference is not found (§5.6).
6. A **behavioural provenance ledger** covering **encoder as well as decoder and controller**, per behaviour and per stage (§6).
7. A **model-assumption register** (§7.1) and a **sensory pathway specification** for every stimulus (§7.2).
8. **Calibration/evaluation separation:** the decoder is never tuned on the scenarios it is finally judged on (§7.3).
9. A **statistical power plan**: independent shuffle *networks* (not just reruns), seeds, effect sizes, CI method, multiple-comparison handling (§7.4).
10. **Kill criteria and time budgets** per part (§9), a **seed policy, data hashes and run manifests** (§7.5).
11. **Core-A / Core-B split** (§3): Core-A is a complete publishable unit on its own.
12. A **minimal end-to-end loop is built early** — the bridge is no longer the last thing built (§4, Part order).
13. A **body-capability audit is front-loaded** (Part 1b): does the installed FlyGym actually actuate a proboscis? Can it express contact-rich grooming? The research check could not settle this from the web (RESEARCH-CHECK F12) — the audit against the installed package settles it.
14. The **MN9 left/right asymmetry** from the old build (83.5 vs 58.7 Hz [OLD]) is a named open question to resolve, not a fact to inherit (§8, RQ-C5).
15. Reproduction metrics add **rank correlation on the active-neuron subset and a noise ceiling**; a Pearson correlation computed over ~127,000 mostly silent neurons is not used alone (§4, Part 3).

> *In plain words:* Three expert reviewers pulled the first draft apart. This version is what survived: every serious objection they raised is now built into the plan itself, instead of being left as a warning in the margins.

### 0.2 Panel disagreements — settled as recommendations (Angelic confirms)

| Disagreement | Positions | **Recommendation in this plan [INF]** | Rationale |
|---|---|---|---|
| (a) Compute: CPU-only vs GPU bursts | Gemini: pre-budgeted GPU bursts for sweeps, with CPU–GPU parity. Claude: CPU first, GPU only behind a pre-set trigger. ChatGPT: CPU agreed + early performance-feasibility gate. | **CPU is the reference platform for all confirmatory work. GPU bursts are allowed only for exploratory sweeps, only after (i) a wall-clock benchmark at Part 0/1 and (ii) a parity check against the CPU reference on identical v630 input. A pre-set trigger (e.g. projected confirmatory runtime above a budget Angelic sets) is what opens the GPU gate — not convenience.** | Majority (Claude + ChatGPT) is the safer position, and it protects the one thing this project cannot lose: that a fast result is the *same* result. Gemini's concern (sweeps are unaffordable on CPU) is met by allowing GPU for exploration, where a parity slip cannot contaminate a headline claim. |
| (b) Behaviour order | ChatGPT: feeding → grooming → walk/halt. Gemini: feeding → walk/halt → grooming. Claude: feeding is the simplest readout but a *weak* test; walk/halt and grooming are the discriminating cases; gate the order on the body audit. | **Feeding first (Core-A), then walk/halt, then grooming (Core-B, grooming explicitly optional).** | Feeding first is unanimous — it is the only behaviour with a validated brain-level readout (MN9 [LIT]). For second place, Gemini + Claude's reasoning wins over ChatGPT's order: walk/halt is more discriminating scientifically than grooming, and grooming is the behaviour whose body feasibility is *least* certain (contact-rich, F12) — it should not sit on the critical path. If the body audit shows grooming is easy and walking is hard in the installed body, Angelic can swap them at that gate with the reason logged. |
| (c) Panel at every gate vs only high-consequence gates | Angelic's protocol + Claude/ChatGPT: panel carried along throughout. Gemini: full panel only at high-consequence milestones; Angelic approving every part is a bottleneck. | **Two gate types, panel involved in both: HARD gates (Parts 0, 3, 5, 6, 7, 7b — pre-registration, brain validation, loop, comparison checkpoint, intervention experiment, walk/halt repeat) get the full panel + Angelic's explicit approval. LIGHT gates (Parts 1, 1b, 2, 2b, 4, 8 — Part 1b escalates to HARD if it changes scope, Part 2b is LIGHT with the hard stop rule K6 in §9.1) get one rotating panel reviewer + Angelic's short summary approval. No gate is skipped; the panel can escalate any light gate to hard. Any change to a question, metric or pass criterion after results are seen requires a formal amendment, logged, whoever proposes it. **Human expert check:** at the Part 5 pre-registration freeze, either the expert check is on record, or Angelic signs a logged waiver stating the mitigation was not obtained; the same rule applies at the final gate (Part 8) (Reviewer 1 final-approval amendment, 23 Nov 2026 — adopted).** | This honours Angelic's explicit instruction (panel carried along throughout; she approves before the next part) while answering Gemini's bottleneck objection: her time and the panel's are spent in proportion to consequence. ChatGPT's "no quiet changes" rule is adopted verbatim in spirit. |

> *In plain words:* Where the reviewers disagreed, this plan picks the safer side and says why — but these are recommendations, not orders. Angelic confirms or changes each one, and her decision is what gets written down.

### 0.3 Approval status — stated honestly

- v1 thought process: reviewed in full by Claude, Gemini and ChatGPT (reviews saved in `panel/`). Their verdicts: direction approved, protocol **not** approved unchanged (ChatGPT, verbatim in substance); Claude and Gemini likewise required major changes. Those changes are §0.1.
- This v2 final plan: **approved by the full panel on 23 Nov 2026** — Reviewer 1 (lead), Reviewer 2 and Reviewer 3 each approved the final amended text. The round is recorded in `panel/FINAL-APPROVAL-claude.md`, `panel/FINAL-APPROVAL-gemini.md` and `panel/FINAL-APPROVAL-chatgpt.md`, with `panel/FINAL-APPROVAL-STATUS.md` as the summary. Reviewer 1 first required three edits (E-Baseline estimand; Part 2b provisional specs; expert-check waiver fallback) plus housekeeping; all were applied as a logged amendment, Reviewer 1 then approved the amended text (16:15 WAT), and Reviewers 2 and 3 confirmed the changed lines only (~16:23 WAT). Approval covers the plan's internal consistency and design logic; citations were research-checked separately (RESEARCH-CHECK.md). **Angelic's own approval is still required and is separate from the panel's.**

> *In plain words:* The experts approved the direction and demanded big fixes; the fixes are in. Nobody has yet signed off on *this exact document*, and this plan will not pretend otherwise. The signature step is a named task, not a footnote.

### 0.4 Formal amendment — 23 Nov 2026: the Core-A feeding body is FlyBody (panel decision, delegated by Angelic)

**Decision and how it was reached.** The Part 1b body-capability audit (`PART1B-AUDIT.md`) settled the question §5.2 had left conditional: an actuated proboscis exists in the installed package, but only in **FlyBody** (5 calibrated proboscis DoFs with published ranges and gains, compiled and run in our environment); on NeuroMechFly the proboscis segments exist but no calibrated parameters ship, so driving them would mean inventing parameters. The Part 1b HARD gate first split 2–1 for staying on NeuroMechFly with the §5.2 named proxy — but one stated premise of that majority (that FlyBody "has no proboscis mechanism at all") was contradicted by the audit's verified finding. Angelic then delegated the decision to the panel ("consult all the ai and let them decide"), the corrected audit fact was put to all three reviewers, and the **final tally was FlyBody, unanimous 3–0**: Reviewers 1 and 2 **reversed** their first-round votes on the corrected fact; Reviewer 3 held his first-round FlyBody vote. Record: `panel/PART1B-GATE-REVIEW.md` (consultation sections). Part 1b is **CLOSED** on this decision. **Angelic accepted the panel's two delegated decisions on 23 Nov 2026, 22:44 WAT** ("Alright let's go with that") — this body decision and the Part 3 drive-rate switch (preregistration Amendment Pass 3).

**What is decided.**
- **Core-A's feeding body is FlyBody.** The body-level feeding metric is the real one: proboscis-extension angle / latency / duration, plus labrum contact events (§5.2 as amended below). The §5.2 named proxy is not the Core-A feeding endpoint.
- **Mandatory feeding-body qualification gate, before the Core-A implementation freeze** (Part 5 freeze; the gate itself is executed and recorded before that freeze is taken). The gate is **time-boxed** and must demonstrate, with **unmodified upstream demos** wherever a demo exists: (i) the 5 proboscis DoFs driven through their **published ranges and gains** (rostrum pitch [−1.24, 0.183] rad, springref 0.8; haustellum pitch [−1.59, 0.7]; labrum pitch [~0, 1.05] — from FlyBody's own `joints.yaml`/`actuators.yaml` as read by the audit), verifying the full movement cycle — **extension, holding at extension, and retraction** — without instability or coupling into other joints; (ii) **repeatability** — the same commands produce the same measured movement across repeated runs, within a stated tolerance; (iii) **measurement definitions stated in advance** — how extension angle is defined (which joints, which reference/retracted pose), and how onset, offset and duration are read from the body state, so the §5.2 metrics are reproducible rather than eyeballed; (iv) a **feeding-contact demo** — extension reaching the food, labrum adhesion engaging, and contact events logged from the body's own contact reporting (the contact interaction the constructed taste feedback will be built from); (v) **pinned versions/hashes recorded** for the body package and model files, together with upstream's **"experimental"** label for FlyBody support in FlyGym, stated wherever the body is described.
- **Body and parameters frozen identically across all experimental arms** (Reviewer 3's condition): once qualified, the body model, its version and every parameter are identical for intact, lesion, null and baseline arms alike — no arm ever runs on a different body or different body settings.
- **No quiet fallback in either direction.** If the qualification gate fails, the project does **not** silently fall back to NeuroMechFly-and-proxy, and does not silently persist with a failing FlyBody: the failure returns to the **panel for an explicit rescope decision**, recorded as a further formal amendment.
- **The full feeding chain is registered before the freeze:** MN9 L/R firing → population rate → **engineered mapping** → proboscis joint targets → labrum contact → **constructed taste feedback**, with the provenance of every link stated in the behavioural provenance ledger (§6.3). In particular: **the extension angle is a function of the decoder mapping, not independent evidence about the connectome** — no document may present a measured extension angle as if the wiring produced it directly.
- **Brain-to-muscle interface proven small first** (carried over from the first-round conditions, in substance): a controlled, repeatable mapping from motor-neuron activity to muscle/joint actuation is demonstrated on a small test case (single joint / single muscle group) before the full embodiment run; if it does not hold, stop and report the negative result.
- **Core-B's body is NOT committed by this amendment.** Part 1b demonstrated walk/halt on **NeuroMechFly only**. Whether Core-B runs on FlyBody is decided at the Core-B gate, after a FlyBody walk/halt audit; nothing in Core-B's planning may assume FlyBody locomotion works until that audit exists.
- **NeuroMechFly's remaining role:** a later, **labelled cross-check on non-proboscis aspects only** (see the S3 amendment in §3.3). It is no longer the Core-A body, and no feeding claim of any kind may be made from it or from any proxy.
- **Grooming stays out** of Core-B at the body level (Part 1b verdict: no controller, trajectory or reachability evidence in the installed package); RQ-C6's neural-level question is unaffected.
- **Taste feedback is labelled constructed everywhere** it appears: the body has no gustatory sensing; the feedback signal is built from labrum/tarsus contact events against a food geom, joined to the encoder-side stimulus definitions (§6.1, §7.2), and the three-way distinction (physical contact / constructed sensory signal / biological gustatory transduction) is kept in the wording.

**Environment verification (Reviewer 1's condition 6).** Verified from the Part 1b audit record and the Part 1 environment record: the audit — including the FlyBody compile-and-run demo (Demo C, 5 proboscis DoFs among 102 actuated) — ran against the installed package in the **pinned body environment** (`envs/body`: FlyGym 2.1.1, MuJoCo 3.16.0, **numpy 2.5.5**), exactly as the audit's header states. The numpy conflict on record is **between** the two pinned environments (brain env numpy 1.26.4 <2; body env numpy 2.5.5 ≥2) and was resolved by keeping the envs separate; nothing in either record indicates the conflict touched the audit, which ran wholly inside the body env. One clarification the records support: the separate TuragaLab `flybody` package was **not** installed at Part 1 (environment record, deviation note 5) — the audit used the FlyBody model that ships **inside** FlyGym 2.1.1, which is also the artefact the qualification gate must pin and hash.

> *In plain words:* The body question is settled, and not by me: I handed it to the panel with one wrong fact corrected, and all three reviewers ended up in the same place. The feeding work will use the body that actually has a working mouthpart with published settings, so the feeding measurement is a real measurement — how far the mouthpart extends, how fast, for how long — instead of a stand-in. But that body only earns its place by passing a qualification test before anything is frozen: its mouthpart joints driven through their published ranges using the makers' own demos, a demo of it actually reaching food and gripping it, and its exact version written down, including the makers' own "experimental" warning. If it fails that test, nobody quietly swaps bodies — the panel decides again, in the open. And one honesty rule is now written into the plan itself: how far the mouthpart extends depends on the translator we build between brain and body, so an extension measurement is never, by itself, evidence about the wiring.

---

## 1. What this project is

ConnectomeToBehaviour is an independent, fully documented test — in software, from public data and free tools only — of how much of a fruit fly's behaviour is already written in the wiring of its nervous system. It takes the real, synapse-resolution wiring diagram of the adult *Drosophila melanogaster* central brain (the FlyWire connectome), gives every neuron the same simple, standard firing rules (a leaky integrate-and-fire model, as in Shiu et al. 2024 [LIT]), connects the output of that simulated brain to a physically simulated fly body (MuJoCo, via FlyGym [LIT] — the Core-A feeding body is **FlyBody**, per the formal amendment in §0.4, 23 Nov 2026; the original text named NeuroMechFly v2 here), and closes the loop: what the body senses drives the brain, what the brain does moves the body, and the movement changes what the body senses next.

The project's defining discipline is **provenance**: for every behaviour it produces, it must show which parts came from the connectome, which from the hand-built layers we had to add on the way in (the *encoder*) and on the way out (the *decoder* and the body's own *controllers*). That honesty is the difference between this project and a demo video, and it is the standard the fresh rebuild is held to. All claims in this project are **model-conditional**: the experiment measures how *this model's* behaviour depends on *this model's* wiring, under documented encoder/decoder/body choices. It does not, by itself, measure a living fly (Claude's construct-validity correction, adopted).

> *In plain words:* We rebuild a fly's brain wiring in a computer, connect it to a fake fly body, and watch what it does. The special part is not the video — it is that we keep an honest account of what the wiring itself did, versus what we quietly helped with, because that help is exactly where other projects have fooled themselves.

---

## 2. Research questions

### 2.1 The main question

> **With neuron rules, body physics, encoder and decoder held fixed and documented, how do the target behaviours change — and within what bounds — when the biological connectome's topology is intervened on: intact versus each graded null family (E-Total), targeted lesion versus matched control lesion (E-Pathway), and intact versus connectome-free baselines and controllers run through the identical body (E-Baseline)?** [INF, reframed per panel; wording revised per Reviewer 2's final-approval amendment, 23 Nov 2026 — the earlier "how much … and how much …" phrasing implied additive shares, which the next paragraph forbids; this wording asks for change-and-bounds across the named comparisons, not for a percentage split]

Three estimands are pre-registered (ChatGPT's distinction, adopted):
- **E-Total — the total topology effect:** the difference in pre-registered behaviour metrics between the intact connectome and each null family, through the identical frozen decoder and body.
- **E-Pathway — the pathway-specific effect:** the difference between a targeted lesion and a matched control lesion (same number of neurons/connections removed, different identity), through the identical frozen decoder and body.
- **E-Baseline — the intact-vs-baseline effect (Reviewer 1 final-approval amendment, 23 Nov 2026 — adopted):** the difference in pre-registered behaviour metrics between the intact connectome and each connectome-free baseline — the rule baselines C1–C3 (§5.5) and the body-only / decoder-only baselines (§5.3) — through the identical body, on the held-out evaluation set, for the fixed-implementation test and the capability test separately (§5.5). Primary metric: the behaviour's pre-registered primary endpoint (§5.2); TOST equivalence bounds are stated per metric in the same way as for E-Total and E-Pathway (§5.6). Without a named estimand here, the "intact vs baselines" comparison that §5.6's convincing-positive criteria and §7.6's permitted-conclusions table depend on would have been exactly where an unregistered analysis could creep in.

No claim of the form "X% of the behaviour comes from the connectome" is permitted unless it names which estimand, which metric, and which null it is relative to. Additive attribution ("the connectome contributes a, the decoder contributes b") is **not** claimed: the panel is unanimous that the design does not support it.

> *In plain words:* The big question is: does the real wiring actually matter, or would any wiring — or even a few simple if-then rules — produce the same behaviour through the same body? We ask it three precise ways: "what changes if we scramble the wiring?", "what changes if we cut one specific pathway versus cutting a random one of the same size?", and "what changes if we replace the brain with simple rules, or with nothing at all?" We never claim a tidy percentage split, because the experiment cannot honestly give one.

### 2.2 Core sub-questions (from the draft, tightened)

- **RQ-C1 — Reproduction.** Can we rebuild Shiu et al.'s whole-brain LIF model [LIT] from the paper and upstream code, and reproduce its published behaviour to a pre-stated standard (Part 3 ladder, §4)? *Core.*
- **RQ-C2 — Feeding circuit.** Does sugar/bittersweet/water drive to the gustatory receptor neurons produce the feeding readout (MN9) pattern the paper predicts, including bitter suppression of the sugar response? *Core.*
- **RQ-C3 — The intervention experiment (feeding).** Through the identical decoder and body, does the intact connectome separate from (i) targeted lesions, (ii) graded shuffled nulls, and (iii) matched rule baselines, on pre-registered feeding metrics — or is equivalence demonstrated instead? *Core. This is Core-A's headline.*
- **RQ-C4 — Walk/halt (Core-B).** Does the model show the walk-OFF pattern described by Sapkal et al. [LIT] — halting for feeding via GABAergic inhibition of walking-promoting descending neurons in the brain — and does walk/halt separate intact vs null vs baseline more discriminatingly than feeding, as Claude predicts? *Core-B.*
- **RQ-C5 — The MN9 asymmetry.** The old build reported MN9 Left 83.5 Hz vs Right 58.7 Hz under right-side sugar stimulation, and exact symmetry (60.0 vs 60.0 Hz) under bilateral stimulation [OLD]. Is the unilateral asymmetry a real property of the circuit (e.g. contralateral projection structure), an artefact of unequal left/right GRN set sizes (21 right vs 10 left in the old constants [OLD]), or a bug? *Core — must be resolved before any MN9 number is published.*
- **RQ-C6 — Grooming (Core-B, optional).** Does mechanosensory (Johnston's organ) drive recruit the antennal grooming pathway (aDN1/aDN2 [LIT]) at the neural level, and — only if the body audit passes — at the body level? *Core-B optional, gated on Part 1b.*

> *In plain words:* The core questions are: (1) can we rebuild the published brain correctly; (2) does it respond to tastes the way the paper says; (3) the headline — does the real wiring beat scrambled wiring and simple rules when all of them drive the same body; (4) does the fly stop walking to feed the way real flies do; (5) one specific old number that might be a bug — we check it before trusting anything built on it; (6) cleaning its antennae, if the body can actually do it.

### 2.3 Panel-added research questions

Each labelled Core or Stretch, with effort as estimated by the panel (low / moderate / high). "Core" here means: included in a pre-registration in this project, not necessarily in Core-A.

| ID | Question | Core / Stretch | Effort | Source |
|---|---|---|---|---|
| RQ-P1 | **Parameter sensitivity:** do the headline results survive ±20–50% changes in synaptic weights, input rate, thresholds and time constants? | Core (at least for Core-A's headline metric) | Low–moderate | Claude Q1, ChatGPT 1.6 |
| RQ-P2 | **Sign-uncertainty Monte Carlo:** if a realistic fraction of excitatory/inhibitory signs (which are *predicted*, not measured [LIT]) are flipped at random, how much do results move? | Core | Low | Claude Q2, Gemini (Eckstein predictions are probabilistic) |
| RQ-P3 | **Closed-loop vs open-loop replay:** does closing the loop change the outcome versus replaying the same sensory drive open-loop? **Required for feeding inside Core-A (§3.1 item 5) and repeated for Core-B behaviours (§3.2 item 9).** | Core (feeding instance in Core-A) | Low | Claude Q3, ChatGPT (open/closed separation) |
| RQ-P4 | **Out-of-distribution / conflict / graded stimuli:** sugar-vs-bitter competition, graded intensities, conflicting cues — do intact and null/baseline separate *more* on hard cases than on easy ones? | Core-B | Moderate | Claude Q4, ChatGPT D3 note |
| RQ-P5 | **Decoder capacity sweep:** linear vs MLP vs refit decoders — how much behaviour can a more powerful decoder extract from *any* wiring (including nulls)? This is also the project's ML-depth evidence for DeepMind (§11). | Core | Moderate | Claude Q5 |
| RQ-P6 | **Prospective prediction vs animal data:** at least one pre-registered prediction (e.g. a silencing outcome) compared against *published animal* data, held out from all tuning. Minimum one case. | Core | Moderate | Claude Q6 |
| RQ-P7 | **Compute benchmark as a reported result:** wall-clock per biological second, memory, and full-run cost on stated hardware, published with the results. | Core | Low | Claude Q10, ChatGPT D2 |
| RQ-P8 | **Minimal-circuit sufficiency:** what is the smallest subcircuit that still produces the feeding separation? | Stretch | Moderate | Claude Q7 |
| RQ-P9 | **v783 sensitivity:** do the headline feeding results survive re-derivation on FlyWire v783 (new IDs, no published reference)? Run late, as a sensitivity study, never as a silent swap. | Stretch (late) | Low (panel estimate; flagged [INF] as optimistic — ID re-derivation may dominate) | Claude Q8, ChatGPT D1 |
| RQ-P10 | **Cross-dataset replication:** does sugar→MN9 with bitter suppression reproduce in an independent connectome (hemibrain / MaleCNS [LIT])? | Stretch | High | Claude Q9 |

> *In plain words:* The reviewers added the "what if we're fooling ourselves" questions: what if we nudge the settings, what if some wiring labels are wrong, what if a cleverer translator between brain and body can fake the result from any wiring, and does the model predict even one thing in a real fly that we didn't tune it to match. Those are the questions that turn a nice demo into research.

---

## 3. Scope: Core-A, Core-B, Stretch, and out of scope

### 3.1 Core-A — the complete publishable unit (must-do)

1. Brain reproduction to the Part 3 standard (§4).
2. Body-capability audit + body standalone verification for the feeding pathway.
3. A population-based decoder for feeding (§6), frozen before evaluation.
4. The controlled comparative intervention experiment for feeding (§5), with its full statistics (§7.4).
5. The sensitivity floor: RQ-P1, RQ-P2, RQ-P7, at least one RQ-P6 case, and **RQ-P3 for feeding** (closed-loop vs open-loop replay of the feeding loop — required inside Core-A, because Core-A's feeding claim is a closed-loop claim; Reviewer 2 final-approval amendment, 23 Nov 2026 — adopted. Core-A's closed-loop feeding claim is gated on this comparison being run and reported for feeding, whatever it shows).
6. Comparison checkpoint vs the old repo (§4, Part 6).

Core-A is a **complete publishable unit**: if the project stopped there, it would still be a finished piece of work with a defensible claim (positive *or* demonstrated-equivalence null). "Done" for Core-A is defined tightly (ChatGPT D5, adopted): baseline reproduced or discrepancy explained; body validated for the behaviours claimed; decoder frozen; all pre-registered conditions run; metrics reported with CIs and seeds; nulls replicated on independent networks; both signs of result reported; provenance ledger complete. A pretty video is not a finish line.

> *In plain words:* Core-A is the smallest version that still counts as a finished, publishable project: rebuild the brain properly, connect it to the body for feeding, and run the fair test of whether the real wiring matters. Even if the answer is "it doesn't, and here is the proof," Core-A is a result.

### 3.2 Core-B — the full core (after Core-A's gate)

7. Walk/halt end-to-end (RQ-C4), including the intervention experiment repeated for walk/halt.
8. Grooming at the neural level; at the body level **only** if the Part 1b audit passes (RQ-C6, optional within Core-B).
9. RQ-P4 and RQ-P5 completed for the Core-B behaviours, and RQ-P3 repeated/extended to the Core-B behaviours (RQ-P3 itself is already required for feeding inside Core-A — see §3.1 item 5; there is one RQ-P3, with a Core-A feeding instance and Core-B instances, not two different placements).

> *In plain words:* Core-B adds stopping-to-feed (walking, then halting) and, if the fake body can actually do it, antenna cleaning. This is the version that can aim at a journal rather than a workshop.

### 3.3 Stretch — each item separately gated, only after its entry condition

| # | Item | Entry condition |
|---|---|---|
| S1 | **BANC bounded cord circuit:** one behaviour's descending-neuron → premotor → motor-neuron pathway from BANC (female, one animal [LIT, corrected — see §10.4]), simulated as a second LIF network, compared with the core decoder for the same behaviour | Core Parts 1–5 passed; BANC data audit (counts computed by us, access, memory) passed at its own mini-gate |
| S2 | **GPU backend port (v630)** with parity suite vs the Brian2 reference | Part 3 passed; GPU access confirmed; parity tolerances pre-registered; trigger per §0.2(a) |
| S3 | **NeuroMechFly cross-body check (amended 23 Nov 2026, §0.4):** a core command sequence replayed in **NeuroMechFly**, as a labelled cross-check on **non-proboscis aspects only** — the original S3 (a flybody cross-check) is superseded because FlyBody is now the Core-A body itself, not a cross-check target; no feeding claim may be made from the NeuroMechFly replay | Part 5 passed |
| S4 | **Vision, neural-first:** flyvis looming → LC4/LPLC2 → DNp01 (giant fibre) activity in our brain; body escape only if the neural gate passes | Neural prediction confirmed in brain-only runs |
| S5 | **Cross-dataset replication** (RQ-P10) and **v783 sensitivity** (RQ-P9) | All core parts passed; dataset/version audit passed |
| S6 | **Fuller Shiu prediction battery:** extend the re-tested subset toward the paper's full testable set (164 predictions [LIT]) | Compute affordable (S2 or equivalent) |

**Explicitly out of scope [INF]:** flight as a claimed behaviour, courtship, learning/plasticity, internal-state (hunger) modelling, whole-CNS full-network simulation, any claim of "upload" or consciousness. Each would be a new project.

> *In plain words:* The stretch list is where we can go deeper now that Angelic is not working alone — a real piece of the nerve cord from the new BANC map is the flagship stretch item. Everything stretch is optional, separately approved, and never allowed to sink the core.

### 3.4 Reporting standard for every claim

Every behaviour claim carries its provenance class, adapted from the flyverse landscape audit [LIT — one group's taxonomy, adopted as our reporting standard, not as established fact]: **E1** = connectome dynamics, neural readout only; **E2** = connectome dynamics drive the body, with intact/null/baseline separation shown; **C** = a trained controller produced the movement; **D** = a hand-coded interface produced or triggered the movement. Classes combine (feeding in Core-A v1 will honestly be E1 + D, becoming E2 only to the extent the intervention experiment supports it). **No class, no claim.**

> *In plain words:* Every time we say "the fly did X," we must also say *how* it did X — from the wiring, from a trained controller, or from our own hand-written link. If we can't label it, we don't claim it.

---

## 4. Build order — parts, gates, and what "pass" means

**Gate mechanics (every part, no exceptions):** (i) **pre-registration** — question, method, metrics, pass/fail criteria and *permitted conclusions per outcome* saved before results exist (confirmatory parts only; exploratory work is labelled exploratory and is not pre-registered — Claude's correction); (ii) **verification** — the part's own tests run, raw outputs saved, never summarised from memory; (iii) **panel review** per §0.2(c) (hard/light); (iv) **Angelic's approval** on a short phone-readable summary; (v) **discrepancy rule** — any disagreement with Shiu et al., with the old repo, or between panelists on a load-bearing point = STOP, log, diagnose, decide with Angelic. Readouts (which neurons count as "the answer") are **fixed from the literature before simulation**, never chosen because they responded (Claude's circularity correction).

**Ordering change from v1 [INF]:** the minimal end-to-end loop is built in **Part 2b**, immediately after the brain model exists — a toy population decoder driving the audited body on synthetic rates, then on real brain output. The old build's failure mode (bridge last, therefore never) is designed out.

| Part | Type | Content | Pass criteria (detail pre-registered at the part's start) |
|---|---|---|---|
| **0. Foundations** | HARD | This plan confirmed; literacy **time-boxed and parallel, not a blocking gate** (Claude's correction — it already failed once as a gate): Shiu, Dorkenwald, Schlegel, Eckstein, Wang-Chen, Braun, Sapkal, Cheong read in full during Parts 0–2, with a reading log; Eon blog + critique read at Part 0; model-assumption register (§7.1) drafted; metrics/N justified (§7.4); **wall-clock benchmark**: time a 100 ms brain trial on the actual VM; GPU trigger set (§0.2a); ≥1 human expert check sought at pre-registration (Claude D6 — e.g. via Neuromatch / African Brain Data Network contacts [INF]; if none is on record by the Part 5 pre-registration freeze, the waiver rule in §0.2(c) applies) | Angelic approves scope (§3) and recommendations D1–D7 (§9.2); panel confirms no load-bearing source missing; benchmark numbers recorded |
| **1. Environment + data** | Light | Pinned environment built from scratch (versions recorded from installed packages); container/lockfiles; v630 data downloaded by a documented procedure; counts (neurons, edges, raw synapses, ≥3-synapse edges) computed from the files; GRN/MN9/DN ID sets extracted with provenance and cross-checked two independent ways; data hashes recorded (§7.5) | Counts match the *paper's* stated expectations or the discrepancy is diagnosed; every ID set has a cited source; a trivial Brian2 network runs in the pinned env |
| **1b. Body-capability audit** | Light (escalates to HARD if it changes scope) | Against the **installed** FlyGym/NeuroMechFly v2 package and its model files — not the web: full joint/actuator list; is there an actuated proboscis joint? Antenna/head actuation? Contact sensing usable for grooming (tarsal/head contact)? Which upstream controllers exist and what do they take as input? Units, timestep, sensor list read from the model files. Output: a one-page **body fact-sheet** | Fact-sheet complete and panel-checked; feeding metric defined honestly from what the body can express (if no proboscis actuation: the metric is a named proxy, §5.2); grooming in/out of Core-B decided on evidence. **Outcome (23 Nov 2026): audit complete; the body decision escalated to a HARD gate, was delegated by Angelic to the panel, and closed on FlyBody — §0.4 amendment; grooming out of Core-B** |
| **2. Brain model** | Light | LIF network from the paper's equations + upstream `model.py` understood line by line (the reading note is a deliverable); every parameter re-read from the paper Methods at this part (RESEARCH-CHECK A6); API for activate / silence / block-output with the *biological meaning* of each operation stated | Single-neuron response to known input correct; synapse-sign audit on a sampled subnetwork vs the neurotransmitter table; silent network = 0 spiking without drive [LIT] |
| **2b. Minimal end-to-end loop** | Light | Toy population decoder (synthetic rates first, then Part 2 brain output) → audited body → sensory event back. Loop timing architecture chosen and justified (brain chunk vs body step; Eon's 15 ms [LIT] is a reference point, not a default); timescale/rate-vs-spike interface specified (windowing, filtering, delays — Gemini's correction). Sensory events in 2b use **provisional specs, labelled exploratory and non-binding** (Reviewer 1 final-approval amendment, 23 Nov 2026 — adopted): the final sensory pathway specs are pre-registered at Part 4 (§7.2) and must be panel-reviewed before the Part 5 loop runs. | Loop runs stably for a pre-set duration; a decoder-only sanity run (brain disconnected, synthetic rates in) is documented, so decoder behaviour is never confused with brain behaviour |
| **3. Brain validation** | HARD | Ladder: short trial → 4 conditions (sugar / bitter / sugar+bitter / water) with CIs at the §7.4 N → `sugarR.parquet` benchmark labelled **model-vs-model** (metrics: Pearson **and** Spearman rank correlation on the active subset, thresholded Jaccard, precision, recall, **noise ceiling** from the reference's own trial-to-trial variability) → feeding prediction subset incl. silencing labelled **model-vs-animal** → weight-shuffle control with our own numbers → **RQ-C5 asymmetry resolution** | Each rung's criteria pre-set; failures reported as failures and diagnosed, not tuned away; w_syn is the paper's one free parameter [LIT] and is never re-fit silently |
| **4. Body standalone** | Light | Upstream FlyGym demos run unmodified; arena with food + dust stimuli defined as **sensory events** (what the body reports), per the §7.2 pathway specs | Demos reproduce upstream behaviour qualitatively; sensory-event definitions explicit and falsifiable |
| **5. Bridge + closed loop (feeding)** | HARD | The real population decoder (§6); feeding end-to-end; decoder **frozen** at this gate; calibration/evaluation split enforced (§7.3) | Behaviour metrics computed from body state, not decoder internals; full decoder published in the log with sources/sensitivity; freeze recorded in the run manifest |
| **6. COMPARISON CHECKPOINT** | HARD | Formal comparison vs old GitHub outputs (§4.1) | Decision log signed by Angelic. **Nothing is pushed before this gate** |
| **7. Intervention experiment** | HARD | §5 in full, for feeding (Core-A completion); repeated for walk/halt in Core-B (Part 7b) | Metrics/statistics exactly as pre-registered; panel reviews the analysis *before* conclusions are written; conclusions carry provenance classes |
| **7b. Intervention experiment — walk/halt repeat (Core-B)** | HARD | §5 repeated for walk/halt (Core-B), with walk/halt metrics (§5.2) and its own pre-registration | As Part 7, for walk/halt; conclusions carry provenance classes |
| **8. Documentation + release** | Light | New README (v1 §7 outline, retained); technical report/preprint (§10); demo video (brain + body, kept in the cloud, low-data preview for Angelic's phone) | Angelic approves exact text/numbers; only then, and only per the Part 6 decision, is anything pushed to the existing GitHub repo |

### 4.1 Comparison checkpoint protocol (Part 6)

Compared, three-way where possible (fresh vs old vs paper): data counts with counting rules stated; per-condition MN9 L/R rates (mean, SD, 95% CI, N, duration, seed policy); total spikes and active-neuron counts; the `sugarR` benchmark metrics; figure shapes; the symmetry outcome (RQ-C5). Agreement criteria are fixed at Part 0, before our numbers exist: MN9 results "agree" if the old point estimate falls inside our 95% CI (or vice versa); benchmark metrics agree within a pre-set tolerance under a protocol-matched comparison (the v1 draft's ±0.02 is retained only as a *starting proposal* — Gemini noted it is meaningless without naming the metric and CI method, which Part 0 must do); counts must match exactly under the same counting rule, or the rule difference must fully explain the gap. Every discrepancy gets a log entry (magnitude → candidate causes → discriminating test if needed → verdict: old wrong / fresh wrong / both right under stated conditions / unresolved). Unresolved load-bearing discrepancies block any push. Angelic then decides: (a) fresh replaces old in the existing repo; (b) old stands, fresh published as an additional/correcting section; (c) hybrid, itemised. **Panel caveat (Claude), adopted:** the old repo is a debugging aid and a provenance record, **not** a pass/fail target — the meaningful external reference is Shiu et al.'s released outputs. The checkpoint's scientific value is the *decision log*, not agreement for its own sake.

> *In plain words (for §4):* We build in small parts, and each part has a finish line written down *before* we start it. Two changes from the first draft matter most: we connect a simple version of the brain-to-body link almost immediately (instead of leaving it to the end, which is how the old project stalled), and we check what the fake body can physically do before promising any behaviour. At Part 6 we compare our fresh numbers with the old project's numbers and with the published paper, write down every difference and why, and only then does Angelic decide what goes on GitHub.

---

## 5. The centrepiece: controlled comparative intervention experiment

(Replaces the v1 "substitution test". The panel's rename is adopted because the old name promised more decisiveness than the design has.)

### 5.1 Estimands

As §2.1: **E-Total** (intact vs each null family, frozen decoder + body), **E-Pathway** (targeted lesion vs matched control lesion, frozen decoder + body), and **E-Baseline** (intact vs each connectome-free baseline — rule baselines C1–C3 and body-only / decoder-only baselines — identical body, held-out evaluation set, fixed-implementation and capability tests separately; Reviewer 1 final-approval amendment, 23 Nov 2026 — adopted). A secondary analysis repeats E-Total with the decoder **refit per condition** (§5.4) — the gap between frozen and refit results is itself a reported quantity: it measures how much of any "connectome effect" a flexible decoder can manufacture or hide.

### 5.2 Metrics (pre-registered per behaviour, from body state)

- **Feeding:** MN9 L/R firing rates (neural, E1); the body-level feeding metric defined at Part 1b — **resolved by the Part 1b audit and the §0.4 amendment (23 Nov 2026): proboscis-extension angle/latency/duration on FlyBody**, the body in which an actuated proboscis with calibrated parameters actually exists in the installed package, gated by the §0.4 feeding-body qualification gate before the Core-A freeze. (The original conditional text — "if an actuated proboscis exists in the installed body; otherwise a named proxy" — is superseded: the audit answered the conditional, and the panel's delegated decision took the real metric. The named proxy survives only as the recorded alternative the panel rejected, and as NeuroMechFly's narrowed cross-check context in S3; it is not a Core-A endpoint, and no feeding claim may be made from it.) Extension angle is a function of the decoder mapping, not independent evidence about the connectome (§0.4); bitter-suppression ratio (sugar+bitter vs sugar alone).
- **Walk/halt (Core-B):** forward velocity, yaw rate, tripod coordination index, halt latency after food contact, halt-context correctness (walk-OFF pattern present/absent in brain activity [LIT]).
- **Grooming (Core-B, if audited in):** T1 tarsus–head contact events, sweep frequency.
- Metrics inherited from the old plan's list [OLD] are re-justified at Part 0 or dropped; none is inherited silently.

### 5.3 Arms and graded null families

All arms run through the **identical** body and (for the primary analysis) the **identical frozen** decoder:

- **A — Intact** connectome.
- **B — Targeted lesions:** feeding pathway (Core-A); aDN pathway (Core-B) — via documented silencing whose biological meaning is stated (Part 2). Each targeted lesion is paired with **matched control lesions** (plural: multiple independently selected controls, never a single control). Matching neuron count / connection count alone is *not sufficient* (Reviewer 3, final-approval amendment, 23 Nov 2026 — adopted): a targeted lesion could otherwise appear more damaging simply because it removed more influential neurons, and E-Pathway would not isolate the pathway's specific causal role. Matched controls must therefore additionally match the targeted lesion, as far as feasible, on: (1) in-degree and out-degree distributions; (2) baseline firing/activity distributions; (3) neuron class and neurotransmitter-sign composition; (4) neuropil / anatomical location; (5) downstream connectivity and network influence; and (6) overall perturbation magnitude, where measurable. The matching procedure is specified in the preregistration *before* any intervention outcomes are observed. Where exact matching is impossible, the remaining imbalance is quantified and the interpretation of E-Pathway is restricted accordingly — the imbalance is reported, not hidden. A lesion result is interpretable only against its matched controls (ChatGPT's "dead circuit" confound, adopted).
- **D — Null families (graded, multiple):** D1 degree-preserving rewiring; D2 degree- + sign-preserving rewiring; D3 degree- + sign- + neuropil/spatially constrained rewiring; D4 weight/activity-matched label permutation. Each family is run on **multiple independent networks** (count from §7.4), not one shuffle rerun many times. The *gradient* across D1→D4 is a result in itself: it shows which preserved property, if any, carries the behaviour. In all null-network topology interventions, the designated **sensory-input and readout neuron identities are explicitly preserved** (Reviewer 3 amendment, 23 Nov 2026 — adopted): a null that silently rewires the input or readout layer would confound topology effects with interface damage.
- **Body-only / decoder-only baselines:** body + decoder with brain output replaced by (i) zeros, (ii) constant rates, (iii) recorded open-loop replay (RQ-P3) — to expose what the stack does with no connectome information at all (Claude's body-only baselines, adopted).

### 5.4 Decoder fairness

Primary analysis: decoder **frozen** (fitted, if at all, only on calibration scenarios, §7.3, then locked and hashed). Secondary analysis: decoder **refit per condition** with an identical, pre-declared fitting budget per condition. Both are reported; neither is hidden. If refitting erases the intact-vs-null gap, the honest conclusion is that the decoder, not the topology, was carrying the difference — and that is a publishable finding, not a failure to be edited away.

### 5.5 Rule baselines — adversarial, matched, budgeted

Three baselines (ChatGPT, adopted), each given a **pre-declared optimisation budget** (same number of tuning evaluations as the decoder received, on the same calibration scenarios):
- **C1 — Fixed rule script:** "if sugar, feed; if dust, groom; else walk" class, but built adversarially: stochasticity, latency, graded intensity, sugar-vs-bitter competition and state persistence included (Gemini's matched-complexity requirement) — written by someone/thing trying to *win*, not to lose.
- **C2 — Matched-capacity controller:** a small learned controller with parameter count matched to the decoder, taking the same sensory events as input, no connectome.
- **C3 — Direct sensory→actuator mapping:** the shortest possible hand mapping from sensory events to body commands.
Two comparisons are reported separately (ChatGPT): the **fixed-implementation test** (all baselines exactly as first built) and the **capability test** (all baselines after their declared optimisation budget). Held-out, diverse evaluation conditions (including conflict/graded cases, RQ-P4) are where baselines must perform — not the conditions they were tuned on.

### 5.6 Statistics for the experiment

Pre-registered at Part 0/5: primary endpoints, effect sizes of interest, CI method, seed policy (§7.4/7.5), multiple-comparison handling across arms/metrics, the **matched-control-lesion procedure of §5.3** (matching criteria, number of independent controls, imbalance quantification — all fixed before outcomes are observed), and **equivalence bounds for TOST**: for each primary metric — for E-Total, E-Pathway **and E-Baseline** alike — the smallest effect that would count as scientifically meaningful is stated in advance; "no difference" may be claimed only when the TOST procedure demonstrates equivalence within those bounds at the pre-set alpha. A non-significant difference without equivalence is reported as **inconclusive**, never as a null result. **Convincing-positive criteria** (ChatGPT, adopted): bitter suppression appears *without* any hand-coded override in the decoder; targeted lesions hurt more than matched control lesions; null families lose performance in a graded way; rule baselines fail on held-out conditions where the intact system succeeds; the separation survives RQ-P1/P2 sensitivity. Even if all are met, the permitted claim is a *limited topology-contribution claim under this encoder/decoder/body* — pre-registered wording, §7.6.

> *In plain words:* This is the experiment the whole project exists for. We run the same body and the same translator with four kinds of "brain": the real wiring, the real wiring with one specific pathway cut (plus a same-sized random cut, for fairness), several kinds of scrambled wiring — from lightly scrambled to very carefully scrambled — and no brain at all, just well-built simple rules that are genuinely trying to win. We also check whether a smarter translator could fake the result. And if we find "no difference," we have to *prove* they're equivalent, not just fail to spot a difference. Whatever comes out — positive, negative, or honestly inconclusive — is the headline result.

---

## 6. The bridge: encoder, decoder, and the provenance ledger

### 6.1 Encoder (body → brain) — a hand-built layer, treated as one

For every stimulus, a **sensory pathway specification** (§7.2) states: the physical event in the simulated world; what the body actually senses/reports; which sensory neuron population is driven; the encoding (rate, duration, pattern); timing relative to the body step; calibration source; and whether each element is grounded in literature or hand-built. The encoder is part of the experiment, not invisible plumbing: the intervention experiment's claims are conditional on it, and an encoder sensitivity check (vary encoding rate/duration within stated bounds) accompanies the headline result.

### 6.2 Decoder (brain → body) — population-based, layered, published in full

Design constraints from the literature [LIT]: read **populations/clusters** of descending neurons, never single "button" neurons (Braun et al.: command-like DNs recruit DN populations; clusters mutually inhibit); respect the **premotor structure** (Cheong et al.: direct DN→motor-neuron connections are infrequent; DNs act mostly through premotor communities) — the decoder therefore has an explicit, documented premotor/command layer and no direct DN-to-joint wires; for feeding, MN9 is the biological readout [LIT], and the step from "MN9 firing" to "body movement" is a **separate, labelled engineered layer** (ChatGPT 1.3, adopted): firing → recruitment → (modelled) muscle/force → movement → contact → feedback, with each unmodelled step named as unmodelled. Every threshold, gain and mapping is published with its source, or marked *chosen* with a sensitivity analysis. The decoder must pass **independent bridge tests** before the loop is trusted: zero input → zero command; calibration curve (input rate vs output) recorded; left/right symmetry where expected; conflict inputs behave as specified; **no hidden overrides** (e.g. no code path that suppresses feeding when bitter is present — suppression must come from the brain or not at all).

### 6.3 Behavioural provenance ledger

One ledger per behaviour, updated at every gate, published with the results. Columns: stage (sensory event → encoder → sensory population → pathway → readout population → decoder layer → controller → actuator → feedback) × (what it is; source [LIT]/chosen; provenance class E1/E2/C/D — multiple allowed per stage, per Gemini's "provenance drift per stage"); plus the evidence artefact for that stage. The ledger is the single place a reader can audit "what actually made the fly do that."

> *In plain words:* Two translators sit between the world and the brain, and between the brain and the body. Both are partly invented by us — there's no way around that — so we write down exactly what each one does, why, and where we got it from, in one public table per behaviour. Anyone reading our work can then see, step by step, what the wiring did and what we did. The feeding translator also has to pass simple honesty tests, like "no brain signal in, no movement out," and it's forbidden from secretly containing the answer (for example, code that stops feeding when bitter is present — that stopping has to come from the brain itself, or the whole experiment is fake).

---

## 7. Registers, statistics, and reproducibility

### 7.1 Model-assumption register

Drafted at Part 0, maintained throughout, published as a supplement. One row per assumption: statement; source; uncertainty; fixed across all conditions? (yes/no); which conclusions depend on it. Seed rows (ChatGPT 1.1, adopted): synapse count ≈ synaptic weight; excitatory/inhibitory sign from *predicted* neurotransmitter (probabilistic [LIT]); no gap junctions; no neuromodulation or internal state; no plasticity; uniform LIF dynamics for all neurons; single-specimen wiring; brain-only network = documented approximation of the omitted ventral nerve cord; Poisson sensory drive; the encoder/decoder choices of §6.

### 7.2 Sensory pathway specifications

One spec per stimulus (sugar, bitter, water, antennal mechanosensory/dust, plus Core-B locomotion-related feedback: proprioceptive/tarsal/labellar contact fed back into the loop — Gemini's closed-loop correction: without a feedback spec, behaviours are triggered programs, not closed-loop control, and the intervention experiment loses half its meaning). Format per §6.1. Specs are pre-registered at Part 4 and reviewed by the panel before the Part 5 loop is built (Reviewer 1 final-approval amendment, 23 Nov 2026 — adopted: Part 2b's minimal loop runs on provisional specs, labelled exploratory and non-binding, and does not count as the loop this rule guards).

### 7.3 Calibration / evaluation separation

Scenarios are split, in writing, before any fitting: **calibration set** (decoder fitting, baseline tuning, threshold choices allowed) and **evaluation set** (held out; used for all headline numbers; includes conflict/graded/OOD cases per RQ-P4). Anything tuned on the evaluation set invalidates it and must be disclosed. Decoder rejection criteria (what decoder behaviour would make us discard and rebuild it) are stated in advance.

### 7.4 Statistical power plan

Fixed at Part 0 for confirmatory work: independent experimental units defined honestly (for nulls: independent *networks*; for trials: independent seeds); N for trials and for shuffle networks set from a precision/power argument against the pre-registered effect sizes (the old build's N=10 / N≥20 figures [OLD] are starting points to justify or replace, not defaults); CI method named (e.g. bootstrap over networks/trials, stated); paired-seed designs used where they reduce variance legitimately; multiple-comparison correction named; TOST bounds per §5.6. Exploratory analyses are labelled exploratory and carry no confirmatory language.

### 7.5 Seeds, hashes, manifests, registry

Fixed seed policy (a master seed list per part, published); SHA-256 hashes of every data file used, recorded at download and in every run manifest; every run produces a **manifest**: code commit/version, dataset version + hashes, environment lockfile hash, full config, seed, panel-gate ID, output hashes. An immutable experiment registry (append-only log) ties pre-registrations → manifests → results → conclusions. Container/lockfiles from Part 1; interface tests for brain/decoder/body boundaries; where compute allows, a CI-style script that regenerates headline numbers from manifests (Claude's build-method list, adopted in full, including a **risk register** and a **negative-result write-up plan** — how a null/equivalence outcome will be written up is decided at Part 0, not improvised at Part 8).

### 7.6 Pre-registered permitted conclusions

At Part 5's pre-registration, an outcome → permitted-conclusion table is saved: for each combination of (intact vs nulls [E-Total], intact vs baselines [E-Baseline], lesion vs control-lesion [E-Pathway], frozen vs refit), the exact claim wording allowed — including the inconclusive and equivalence wordings. Conclusions written at Part 7/8 may not exceed this table without a formal amendment (logged, panel-reviewed, Angelic-approved).

> *In plain words:* This section is the anti-self-deception machinery. We keep a list of everything we're *assuming* (and what breaks if an assumption is wrong); we write down exactly how each sense is turned into brain activity; we never practise on the exam questions (the cases we tune on are kept separate from the cases we're judged on); we decide in advance how many repeats make a result trustworthy and what we'll be allowed to *say* for each possible outcome; and every run leaves a receipt — which data, which code, which settings — so anyone, including future us, can re-run it and get the same numbers.

---

## 8. Known open problems the plan must resolve (not inherit)

1. **MN9 asymmetry (RQ-C5)** — see §2.2. Resolved at Part 3 with dedicated bilateral/unilateral runs at matched GRN counts, before any MN9 claim.
2. **Proboscis/grooming body feasibility** — settled by audit at Part 1b, not by assumption (RESEARCH-CHECK F12: v1 NeuroMechFly actuated only leg joints; upstream FlyGym v2 proboscis actuation unverified from the web). **Resolution (23 Nov 2026):** the audit found calibrated proboscis actuation only in FlyBody; the body decision was delegated by Angelic to the panel, which decided FlyBody unanimously after a factual correction — see the formal amendment in §0.4. Body-level grooming failed the audit and stays out of Core-B.
3. **Pearson inflation** — reproduction fidelity is reported with rank correlation on the active subset + noise ceiling + thresholded Jaccard (Part 3); the old 0.9936 [OLD] is a comparison target only.
4. **Silent / runaway network failure modes** — gated checks at Parts 2–3: zero-drive silence [LIT], and pre-set activity bounds whose breach stops the run and is logged (Gemini).
5. **Sex/dataset mismatch** — brain and bodies are female; the best DN→motor circuit paper (Cheong) is male MANC [LIT]. Any cross-dataset DN matching goes through shared cell-type nomenclature (Schlegel et al. [LIT]) and match quality is reported, never assumed. BANC (female, one animal [LIT]) is the principled stretch route precisely because it removes this mismatch.
6. **Panel correlation** — four AIs can share a failure mode and agree on a wrong citation (Claude). Mitigations already in force: research-checking against primary sources (done for this plan), adversarial panel roles at hard gates, and ≥1 human expert check at pre-registration and at the final gate (sought, Part 0). Fallback (Reviewer 1 final-approval amendment, 23 Nov 2026 — adopted): if no expert check is on record by the Part 5 pre-registration freeze, Angelic signs a logged waiver stating the mitigation was not obtained; the same rule applies at the final gate — so the mitigation can never silently not happen.

> *In plain words:* These are the specific traps we already know about — one suspicious old number, a body that might not be able to do what we'd claim, a statistic that can look better than it is, and the fact that even four AIs can be wrong together. Each trap has a named place in the build where it gets checked, instead of a hope that we'll notice.

---

## 9. Kill criteria, time budgets, and decisions

### 9.1 Kill criteria and budgets [INF — Angelic sets the numbers at Part 0]

Budgets are set per part at Part 0 in two currencies: **wall-clock weeks** and **Angelic's review hours** (her time is the scarcest resource). A part that exceeds its budget stops and returns to Angelic with options — it does not silently expand. Standing kill / pivot criteria:

- **K1 (reproduction):** if Part 3 cannot reproduce the paper's feeding pattern to the pre-set standard after the logged diagnosis steps, the project pivots to a **reproduction-failure report** (itself publishable, §10) and does not proceed to embodiment on an untrusted brain.
- **K2 (body):** if Part 1b shows the body can express *no* honest feeding metric (not even a defensible proxy), Core-A is re-scoped to a neural-level (E1) intervention experiment and Angelic decides whether that still serves the flagship goal.
- **K3 (separation):** if feeding shows demonstrated equivalence (not mere non-significance) between intact and nulls at Part 7, we do **not** keep adding behaviours hoping for a positive; the equivalence result is written up, and Angelic decides on Core-B as a *new* bet with walk/halt as the discriminating case.
- **K4 (compute):** if confirmatory N is unaffordable on CPU and the GPU parity gate (S2) fails, N is reduced only by formal amendment with the power consequence stated — never silently.
- **K5 (scope):** any stretch item that threatens a core gate's budget is deferred automatically; stretch never eats core.
- **K6 (Part 2b loop stability — Reviewer 2 final-approval amendment, 23 Nov 2026, adopted):** Part 2b is a LIGHT gate with a hard stop rule. If the minimal closed loop cannot run stably for its pre-set duration after the logged diagnosis steps — adjusting, within their pre-registered bounds only, the brain-chunk duration, the rate/spike windowing and filtering, and interface delays — then work STOPS: Parts 3 and 5 investment does not proceed on an unstable loop. The loop timing/interface architecture is revised and Part 2b is re-run once. If it is still unstable, Core-A is re-scoped to an open-loop / neural-level (E1) design and Angelic decides whether that still serves the flagship goal — the same decision shape as K2, taken at Part 2b rather than discovered at Part 5.

### 9.2 Decisions D1–D7 — recommended choices

| # | Decision | **Recommended choice** | Panel position |
|---|---|---|---|
| D1 | Core brain dataset | **v630** for the core (matches Shiu's IDs, parameters and `sugarR` reference [LIT]); v783 only as the late sensitivity study RQ-P9, with a version audit first (provenance, ID overlap, same snapshot?) | Unanimous agree (ChatGPT conditional on the version audit — adopted) |
| D2 | Compute | **CPU reference; GPU bursts behind benchmark + parity gate** (§0.2a) | Majority (Claude, ChatGPT); Gemini's GPU concern met for exploration |
| D3 | Behaviour order | **Feeding → walk/halt → grooming (optional)** (§0.2b), with a checkpoint after feeding | Feeding-first unanimous; order thereafter per §0.2b rationale |
| D4 | Cord depth (BANC) | **(a) Decoder-design evidence only in core; (b) bounded BANC circuit (S1) as the flagship stretch**; full brain+cord network rejected as a different project | Unanimous agree (ChatGPT: core must state brain-only = documented approximation of the omitted cord — adopted in §7.1) |
| D5 | What counts as "done" | **Core-A complete incl. the intervention experiment, whatever its outcome (incl. demonstrated equivalence) = the scientific finish line. Core-A + S1 = the career-showcase finish line.** A look-alike demo video without controls is rejected as a finish line | Unanimous agree, tightened per ChatGPT D5 (§3.1) |
| D6 | Panel mechanics | **Two gate types (§0.2c); panel can reject a gate; no quiet changes to questions/metrics/criteria after results — formal amendment only; ≥1 human expert check at pre-registration and final; if none is obtained, Angelic signs a logged waiver at the Part 5 pre-registration freeze and at the final gate (Reviewer 1 final-approval amendment, 23 Nov 2026 — adopted)** | Protocol (Angelic) + Claude/ChatGPT, with Gemini's bottleneck fix |
| D7 | Push / replacement policy | **Repo kept (visionbyangelic/ConnectomeToBehaviour, ~8 stars [OLD — her count]); fresh work local until Part 6; at replacement, preserve the old build on an immutable tag + archival branch (with env spec, data hashes, outputs, comparison report, migration doc — ChatGPT's strengthening, adopted), then replace `main` as a separately versioned release; never force-push** | Unanimous agree, strengthened |

> *In plain words:* Every big choice is listed with the answer this plan recommends and who agreed. The dataset is the published one ( unanimous). "Done" means the fair test is finished — even if the answer is "the wiring didn't matter here, and we can prove it" — not that we made a video that looks impressive. And the old GitHub project is never deleted: it gets preserved, labelled, and only then replaced, if Angelic decides the fresh work is better.

---

## 10. Evidence base (research-checked summaries)

Full verification log: `RESEARCH-CHECK.md`. Summaries below use the **corrected** forms.

### 10.1 Shiu et al. 2024 — still the baseline [LIT, verified]

*Nature* 634, 210–219, DOI 10.1038/s41586-024-07763-9. Whole FlyWire central-brain LIF model in Brian2 (>125,000 neurons, ~50M synapses), weights from synapse counts × predicted-transmitter sign (Eckstein et al., *Cell* 2024 [LIT]), W_syn the single free parameter, baseline firing 0 Hz. Headline validation: 91% of 164 empirically testable predictions consistent with experiment (84% excluding the optogenetic screen) [LIT, verified]. There is, to our knowledge as of 23 Nov 2026, no newer whole-brain LIF model that supersedes it [INF] (search method and coverage: RESEARCH-CHECK.md — 32 claims checked against primary sources on that date; a negative from search is weak evidence, so this claim is dated, not absolute — Reviewer 1 final-approval housekeeping, 23 Nov 2026). Going deeper means going downstream (cord) and sideways (controls/metrics), not finding a better brain model.

### 10.2 Eon Systems 2026 — the benchmark and the gap [LIT, verified from Eon's own text]

Integration of the Shiu brain (~140,000 neurons [LIT]) + Lappalainen visual model + NeuroMechFly body (87 joints [LIT]), synced every 15 ms [LIT]; a small set of descending outputs (DNa01/DNa02, oDN1, antennal DNs, MN9) used as handles for imitation-trained controllers [LIT]; Eon itself states the mappings "can be somewhat arbitrarily chosen by hand (as is our case)", that vision is currently "somewhat decorative", that results "should not yet be interpreted as a proof that structure alone is sufficient", and that behaviours "lean heavily on the body model's existing controllers" [LIT, all verified verbatim]. Eon did not use flybody [LIT]. Our niche is exactly the space Eon leaves open: a smaller claim, fully evidenced. Eon is cited fairly, as a design input — never attacked (Claude's hiring-lens warning, adopted).

### 10.3 The critique [LIT — commentary, labelled as such]

Ariel Zeleznikow-Johnston, "No, we haven't uploaded a fly yet" (LessWrong/Substack, March 2026): the ventral nerve cord (~15,000 neurons) was not simulated; a rule script in place of the connectome would produce a visually similar video. Load-bearing here only because Eon concedes the same points (§10.2). The flyverse audit's E1/E2/C/D taxonomy and its "no peer-reviewed E2 system as of 2026-09-20" conclusion are adopted as a *reporting standard*, not treated as established fact [LIT/INF].

### 10.4 BANC 2026 — the deeper route, corrected [LIT, verified + corrected]

Bates, Phelps, Kim et al., *Nature* 656, 957–970 (2026), DOI 10.1038/s41586-026-10735-w, PMID 42259917, online 8 June 2026. A **densely** reconstructed connectome uniting brain + VNC in one adult **female**; ~160,000 neurons expected, 155,916 proofread/roughly-proofread in the v888 accounting; brain↔cord linked by ~1,300 descending and ~1,800 ascending neurons (v888 counts: 1,316 DNs, 1,849 ANs). Strongest influences on effector neurons are generally **local** sensory signals forming tight feedback loops, coordinated by long-range AN/DN circuits. *(Corrections vs the v1 draft: the "~3,600 long-range projections" figure is dropped — not in the paper; "sparse reconstruction" is corrected to densely reconstructed.)* BANC is stretch item S1, bounded to one behaviour's pathway — high cost, high distinctiveness.

### 10.5 MANC / Cheong, Braun, Sapkal — decoder design evidence [LIT, verified]

Cheong et al., *eLife* 13 RP96084 (version of record 2026): direct DN→MN connections are infrequent; premotor communities are organised by motor system (male data — cross-sex caveat, §8.5). Braun et al., *Nature* 630, 686–694 (2024): command-like DNs recruit DN populations via excitatory DN→DN connections; clusters mutually inhibit; recruitment is necessary for complete behaviours. Sapkal et al., *Nature* 634, 191–200 (2024): walk-OFF (brain, GABAergic, halting for feeding) vs brake (cord, cholinergic, halting/stability for grooming) — the circuit basis for RQ-C4.

### 10.6 Bodies and vision [LIT, verified]

NeuroMechFly v2 / FlyGym (Wang-Chen et al., *Nature Methods* 21, 2353–2362, 2024): vision, olfaction, ascending feedback, complex terrains, leg adhesion — the platform, and (per the §0.4 amendment, 23 Nov 2026) the body on which walk/halt was demonstrated at Part 1b and the later labelled cross-check body for non-proboscis aspects (S3 as amended); **no longer the Core-A feeding body** (the original text called it "core body" without qualification). flybody (Vaxenburg et al., *Nature* 643, 1312–1320, 2025): female whole-body MuJoCo model, walking + flight, RL controllers taking high-level steering commands; CGS units — **Core-A feeding body** per the §0.4 amendment (the original text's "stretch cross-check S3 only" is superseded: the Part 1b audit verified FlyBody ships the installed package's only calibrated proboscis actuation — 5 DoFs with published ranges/gains — and the panel's delegated decision adopted it, subject to the §0.4 qualification gate; upstream labels its FlyGym support "experimental"). *(The old plan's "6-DoF centre-of-mass command" specification for flybody is dropped — unverifiable, RESEARCH-CHECK F7.)* Lappalainen et al., *Nature* 634, 1132–1140 (2024): 64 cell types, 45,669 neurons, 1,513,231 synapses, 734 free parameters, agreement across 26 studies — vision is stretch S4, neural-first, because Eon's own experience (§10.2) shows its behavioural value is currently low.

### 10.7 MaleCNS 2026 [LIT, verified for the version of record]

Berg, Beckett, Costa et al., *Cell* 189, 5504–5526 (2026), DOI 10.1016/j.cell.2026.08.015: complete male CNS, 166,700 neurons, 11,710 types, 8,069 isomorphic types, fully proofread. **Version warning:** the preprint version reports different counts (166,691 / 11,691 / 7,205) — any use states its version. Wrong primary dataset for this project (male; our brain/bodies/baseline are female); best use is cross-dataset replication (RQ-P10).

> *In plain words:* Everything this plan leans on has been checked against the original papers, and two mistakes in the first draft (about the new brain-and-cord map) were caught and fixed. The short version: the published brain model we're rebuilding is still the best there is; the famous company demo openly admits its brain-to-body link was hand-made and its body did most of the work — that admitted gap is precisely the space our project occupies, honestly and with controls.

---

## 11. Publishing route and the application artefact order

### 11.1 Route [INF, from the panel's publishability analysis]

1. **Preprint first:** bioRxiv (or arXiv q-bio.NC, which may need an endorser) as soon as Core-A is complete — positive, equivalence-null, or reproduction-failure (K1) outcome alike; the pre-registration and registry (§7.5) make any of the three writeable without re-framing.
2. **Core-A** → NeurIPS/ICLR NeuroAI **workshop** paper (4–8 pp) or **ReScience C** (reproduction framing).
3. **Core-A + Core-B** (full factorial intervention experiment) → **PLOS Computational Biology / eLife (reviewed preprint) / Neuroinformatics** class venues.
4. BANC (S1) or cross-dataset (S5) results upgrade venue ambition **only after** the core is published — never as a reason to delay it.
5. Practical: a senior co-author/mentor materially helps (Claude) — Angelic's lab/Neuromatch/African Brain Data Network connections are the route to ask [INF]; this is her decision and her conversation to have.

### 11.2 What reviewers will demand (plan for it from Part 0)

Reproduction fidelity with noise ceiling + rank correlation + thresholded Jaccard; RQ-P1 + RQ-P2 sensitivity; the full factorial with CIs, effect sizes, seeds and equivalence testing; a stated estimand and model-scoped claims; the adversarial matched rule baseline; ≥1 animal-data comparison (RQ-P6); provenance ledger published; open code with a DOI (release tag + optional Zenodo DOI, D7); data-version statements; FlyWire/Shiu licence compliance; fair Eon citation.

### 11.3 Unpublishable if — the hard list

A video used as evidence; single-seed results; the loop never actually run closed; "how much" left undefined; biological claims drawn from model-vs-model data; straw-man baselines or a single weak null; Eon overlap unaddressed; code that a reviewer cannot re-run. **Any one of these present at Part 8 stops the release until fixed.**

### 11.4 Artefact order for Eon Systems / Google DeepMind applications (Claude, adopted)

1. **Preprint / technical report with the main result** (whatever it is, honestly stated).
2. **Repo quality:** one-command reproducibility, tests, manifests, the comparison/decision log.
3. **Provenance-overlay demo video** (brain activity + body + on-screen provenance classes) — supporting material, never the evidence.
4. **Plain-language write-up** of what was tested and found.
5. **Talk / poster.**
One further hiring-lens requirement, adopted as a project rule: **Angelic must be able to explain every equation, parameter and design choice herself, unaided** — the panel process is documented as review, and the work is presented as hers, in her voice, per the repo-voice rule. A finished, honest Core-A is a stronger application than a larger unfinished project (panel, unanimous in substance).

> *In plain words:* We publish the small finished thing first (a preprint, then a workshop), and only aim at a big journal when the walking work is done too. The list of things that would get a paper rejected is written down now, while we can still avoid them. For job applications, the order matters: paper first, then a tidy re-runnable code repo, then the video — the video is the advert, never the proof. And Angelic has to own every detail personally; that's what those teams actually test.

---

## 12. What happens next

1. Angelic confirms (or amends) the §0.2 recommendations and D1–D7 (§9.2).
2. The panel final-approval round for this v2 document is complete: **approved by the full panel (Reviewers 1–3) on 23 Nov 2026**, recorded in `panel/FINAL-APPROVAL-*.md` (see §0.3).
3. Part 0 opens: assumption register drafted, metrics/N/power fixed, VM wall-clock benchmark run, GPU trigger set, human expert check sought.
4. No project code is written before Part 0 closes. Nothing is pushed to GitHub before Part 6.

> *In plain words:* Angelic says yes (or changes things), the experts sign this exact plan (or we honestly record that one couldn't be reached), we do the paperwork-and-measuring part first — and only then do we write the first line of code.

---

*End of FINAL PLAN v2. Companion files: `RESEARCH-CHECK.md` (verification log), `panel/` (v1 reviews + final-approval records), `FRESH-START-PROTOCOL.md` (governing decisions), `NEW-THOUGHT-PROCESS.md` (v1 draft, superseded by this plan where they differ).*
