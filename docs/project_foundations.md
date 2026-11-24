# Part 0 Package — ConnectomeToBehaviour (Fresh Rebuild)

Prepared 23 Nov 2026. **Groundwork only:** no project code written, no packages installed, no data downloaded. Sources: FINAL-PLAN.md (panel-approved 23 Nov 2026; D1–D7 confirmed by Angelic, see `ANGELIC-DECISIONS.md`), PART0-PREP.md (environment check, data verification, pre-registration skeleton).

**Status going in:** Part 0 is a HARD gate. Its pass criteria (FINAL-PLAN §4, Part 0 row): Angelic approves scope and D1–D7 *(done — D1–D7 confirmed 23 Nov 2026)*; panel confirms no load-bearing source missing; benchmark numbers recorded. This package supplies the remaining Part 0 deliverables in draft/proposal form: the assumption register (§7.1), metrics/N justification (§7.4), budgets (§9.1), the GPU trigger (§0.2a), the benchmark-sequencing decision (flagged in PART0-PREP §1), and the human-expert-check plan (D6 / §8.6). **Every number in §§2–4 is PROPOSED, not fixed.** §7 is the decision sheet: Part 0 closes when Angelic has decided each item on it.

Two open items carried in from the prep pack, both dealt with below:
- **`sugarR.parquet` size discrepancy** — served at ~0.95 MB vs the old script's stated ~2.2 MB. Carried into the assumption register (A13) and the decision sheet (item 13): the file is not trusted until SHA-256 + content verification at Part 1.
- **Benchmark sequencing catch** — Part 0's pass criteria include a 100 ms Brian2 wall-clock benchmark, but the pinned environment is only built at Part 1. Resolved as a recommendation in §5 below; decision sheet item 11.

---

## 1. Assumption register v1 (draft — FINAL-PLAN §7.1 + §8)

Drafted at Part 0 per §7.1; maintained throughout; published as a supplement with the results. Format per §7.1, expanded per Part 0's brief: **what we assume — why — what breaks if it's wrong — how the plan tests or bounds it.** "Fixed" = held identical across all conditions in the intervention experiment (a non-fixed assumption can manufacture or hide an effect; a fixed one mostly cannot).

| ID | Assumption | Why we make it | What breaks if it's wrong | How the plan tests / bounds it | Fixed? |
|---|---|---|---|---|---|
| A1 | **Synapse count ≈ synaptic weight.** Connection strength is derived from anatomical synapse counts, scaled by the single free parameter W_syn (Shiu et al. 2024 method [LIT]). | It is the published model's construction; no per-synapse physiological strength data exists at whole-brain scale. | If real strengths depart systematically from counts, firing patterns — and any topology conclusion — are conditional on a wrong weight map. | RQ-P1 parameter sensitivity (±20–50% on weights and other parameters) bounds how much headline results move; W_syn is never re-fit silently (Part 3 rule). Conclusions are stated as model-conditional (§1). | Yes |
| A2 | **Excitatory/inhibitory sign comes from *predicted* neurotransmitter identity** (Eckstein et al. predictions — probabilistic, not measured [LIT]). | No measured sign data exists at this scale; the predictions are the field's standard source. | A wrong sign flips a pathway's effect (excitation ↔ inhibition); bitter suppression, walk-OFF and every lesion interpretation depend on signs being mostly right. | RQ-P2 sign-uncertainty Monte Carlo: flip a realistic fraction of signs at random and measure how far results move. Sign audit on a sampled subnetwork vs the transmitter table is a Part 2 pass criterion. | Yes |
| A3 | **No gap junctions** (electrical synapses are absent from the model). | The FlyWire connectivity used is the chemical-synapse table; Shiu et al. likewise model chemical transmission. | Electrical coupling could synchronise or rescue activity in ways the model cannot show; a null result could be an artefact of the omission. | Not directly testable inside this design; registered as a scope limit on every claim. The permitted-conclusions table (§7.6) bars claims the omission could explain away. | Yes |
| A4 | **No neuromodulation and no internal state** (no hunger, arousal, or modulatory tone). | Out of scope by design (§3.3: internal-state modelling explicitly excluded); the published model has the same limit. | Real feeding is state-dependent; the model can only ever show the state-independent skeleton of the behaviour. | Claim wording is restricted accordingly (§7.6); RQ-P6 requires ≥1 prediction checked against published *animal* data held out from tuning, which is where a state effect would surface. | Yes |
| A5 | **No plasticity** — weights are static within and across trials. | Matches the published model; learning is explicitly out of scope (§3.3). | Trial-to-trial adaptation in a real fly is unmodelled; repeated-stimulus results are about the fixed circuit only. | Registered as a scope limit; no claim is worded as if adaptation were present or absent in the animal. | Yes |
| A6 | **Uniform LIF dynamics for all neurons** — every neuron is a leaky integrate-and-fire unit with the paper's shared parameters; no cell-type-specific dynamics, no bursting, no adaptation currents. | It is the published model's simplification and the only tractable whole-brain choice; per-type dynamics are not known at scale. | Real neurons differ; dynamics-driven effects (e.g. a pathway that works by bursting) are invisible to the model. Construct-validity limit on all conclusions (Claude's correction, §1). | RQ-P1 sensitivity on thresholds/time constants; conclusions are model-conditional by construction; the assumption is named in the paper supplement (this register is published). | Yes |
| A7 | **Single-specimen wiring** — the connectome is one individual fly's brain (FlyWire v630, the version of record per D1). | v630 is the only version with the paper's parameters and reference outputs (D1 rationale). | Individual variation is unmeasured; results are about *this* wiring diagram, not the species average. | RQ-P9 (v783 sensitivity, stretch) and RQ-P10 (cross-dataset replication, stretch) test robustness across specimens/datasets later; never silently swapped in. Part 1 re-confirms the exact snapshot from the data files (ChatGPT D1 condition). | Yes |
| A8 | **Brain-only network = documented approximation of the omitted ventral nerve cord** (ChatGPT D4 condition, adopted §7.1). The cord's real circuitry is replaced by the decoder's engineered premotor/command layer (§6.2). | The core dataset is brain-only; a full brain+cord simulation was unanimously rejected as a different project (D4). | Descending commands in reality recruit cord circuitry with its own computation (e.g. the cord "brake" for grooming, Sapkal et al. [LIT]); our decoder cannot reproduce cord computation it doesn't contain. Behaviour-level claims inherit this gap. | The approximation is stated wherever brain-only results are reported; BANC is used in-core as decoder-*design evidence* (D4a); bounded BANC circuit S1 (D4b) tests one pathway through real cord wiring as the flagship stretch. Provenance ledger (§6.3) marks every decoder stage as engineered. | Yes |
| A9 | **Poisson sensory drive** — sensory neuron populations are driven as Poisson processes at specified rates (per the §7.2 sensory pathway specifications). | Matches the published model's stimulation method; real transduction time-series are unavailable. | Real sensory responses have adaptation, latency structure and correlations a Poisson drive lacks; absolute rates (not just comparisons) could shift. | Encoder sensitivity check (§6.1): headline result re-run with encoding rate/duration varied within stated bounds. All primary comparisons hold the drive identical across arms, so drive shape cannot favour one arm. | Yes |
| A10 | **Encoder choices are hand-built** (§6.1): which population is driven, at what rate, for how long, with what timing relative to the body step — each element either literature-grounded or marked *chosen*. | No alternative exists: something must translate body sensor events into brain drive, and no published standard covers our exact body. | A badly chosen encoding could create or destroy the behaviour before the connectome is involved — the project's central confound, on the input side. | Every element is specified in a §7.2 pathway spec before runs; the encoder is *inside* the provenance ledger (§6.3) and inside the intervention design: all arms share the identical frozen encoder, and the encoder sensitivity check accompanies the headline result. | Yes (frozen for confirmatory runs) |
| A11 | **Decoder choices are engineered, and the decoder is a hypothesis, not plumbing** (§6.2): population/cluster readout of descending neurons (never single "button" neurons, per Braun et al. [LIT]); an explicit premotor/command layer with **no direct DN-to-joint wires** (per Cheong et al. [LIT]); for feeding, MN9 firing → movement is a separate labelled engineered chain (recruitment → modelled force → movement → contact → feedback), each unmodelled step named. | The literature constrains the shape (populations, premotor structure) but not the exact gains/thresholds; those are ours. | This is the panel's #1 identified risk: a powerful or hand-tuned decoder can manufacture behaviour from *any* wiring — including nulls — and the connectome gets the credit. If the decoder is doing the work, the headline claim is false. | Decoder frozen before evaluation (§5.4) and re-fit per condition only as a separately reported secondary analysis; decoder capacity sweep (RQ-P5: linear vs MLP vs refit) measures how much behaviour a stronger decoder can extract from nulls; independent bridge honesty tests (§6.2: zero-in → zero-out, calibration curve, symmetry, **no hidden overrides** — bitter suppression must come from the brain or not at all); rule baselines (§5.5) are adversarial and capacity-matched. | Yes (frozen; refit variant reported separately) |
| A12 | **Upstream body controllers are taken as given** — the FlyGym/NeuroMechFly v2 body's built-in controllers (leg coordination etc.) do part of the work of moving, and their internal logic is not ours. | Rebuilding locomotion control is a different project; the audited body is the field-standard body [LIT]. | Body controllers can supply behaviour the brain never asked for — the output-side version of the A11 confound (and Eon's own admitted weakness, §10.2). | Part 1b body-capability audit documents exactly which controllers exist and what they take as input; body-only / decoder-only baselines (§5.3) measure what the body+decoder do with no brain; provenance ledger (§6.3) has an explicit *controller* stage so the contribution is never hidden. | Yes |
| A13 | **The reference files are what they claim to be** — in particular `sugarR.parquet` is Shiu et al.'s released reference output, usable as the Part 3 benchmark. **Currently UNVERIFIED:** the file is served at ~0.95 MB against the old script's stated ~2.2 MB (PART0-PREP §2). | The benchmark is load-bearing for Part 3 validation; the old build used this source. | If the file changed, is truncated, or is a different export, Part 3 would validate against the wrong target — silently, since a plausible-looking correlation could still result. | SHA-256 recorded at download (§7.5); contents verified against paper expectations (trial count, MN9 columns, value ranges) *before* it is trusted (Part 1); the benchmark is always labelled **model-vs-model**, never animal data (Part 3). Decision sheet item 13. | n/a (data provenance) |
| A14 | **Readouts are fixed from the literature before simulation** — e.g. MN9 is the feeding readout because the paper says so [LIT], never because it responded in our runs (§4 gate mechanics, Claude's circularity correction). | Choosing readouts post hoc would make every "result" circular. | If a literature readout is wrong for our exact configuration, we may miss where the signal actually is — an accepted cost of non-circularity. | Readout definitions are pre-registered per part; any additional responsive population found is reported as *exploratory* only. Includes resolving **RQ-C5** (the old build's MN9 L/R asymmetry: real circuit property, unequal GRN set sizes — 21 right vs 10 left in the old constants [OLD] — or bug) at Part 3 before any MN9 number is published (§8.1). | Yes |
| A15 | **Correlation-with-reference is a weak fidelity measure on its own** — the old build's headline Pearson 0.9936 [OLD] can be inflated by the many jointly-silent neurons (§8.3). | — (this is a known failure mode being registered, not a modelling choice) | Trusting a single correlation would overstate reproduction fidelity and contaminate every downstream comparison. | Part 3 reports Spearman rank correlation on the active subset + thresholded Jaccard + precision/recall + a **noise ceiling** from the reference's own trial-to-trial variability; 0.9936 is a comparison target only, never a target to hit. | Yes (reporting standard) |
| A16 | **The closed loop's timing architecture is a modelling choice** — brain-chunk duration, rate/spike windowing, filtering and interface delays (§4 Part 2b; Eon's 15 ms sync [LIT] is a reference point, not a default). | Some chunking is unavoidable when coupling a Brian2 brain to a physics body in separate steps. | A badly chosen chunk/delay can destabilise the loop or smear cause and effect in time, producing artefacts that look like behaviour. | Chosen and justified at Part 2b, inside pre-registered adjustment bounds only; K6 hard stop rule if the loop cannot run stably; RQ-P3 (closed- vs open-loop replay, required for feeding in Core-A) measures whether closing the loop changes the outcome at all. | Yes (within pre-registered bounds) |
| A17 | **Sex/dataset consistency is maintained by nomenclature, not anatomy** — brain and bodies are female; the best DN→motor circuit evidence (Cheong et al.) is male MANC [LIT]; any cross-dataset neuron matching goes through shared cell-type nomenclature (Schlegel et al. [LIT]) (§8.5). | No female DN→motor dataset of comparable completeness exists; BANC (female) is the principled fix but is stretch (D4). | A mismatched cell-type match would import male circuit structure into a female model without anyone noticing. | Match quality is reported wherever cross-dataset matching is used, never assumed; BANC S1 removes the mismatch for its one pathway. | Yes |
| A18 | **Four AI reviewers can share a blind spot** (process assumption, §8.6) — panel agreement is not proof. | The project's review mechanism is an AI panel (D6); this failure mode is inherent to it. | A wrong citation, method or assumption could pass every gate with unanimous wrong agreement. | Primary-source research-checking (done for the plan: 32 claims, RESEARCH-CHECK.md); adversarial panel roles at hard gates; **≥1 human expert check at the Part 5 pre-registration freeze and at the final gate** — or Angelic's signed logged waiver (§6 of this package). | n/a (process) |

*Maintenance rule (§7.1):* any assumption discovered mid-build is added here with a dated entry before the work that depends on it proceeds; the register is published as a supplement, so late additions are visible as late.

### Addendum — 23 Nov 2026 (Part 2): gap entries

Appended, not edited into v1 above, per the maintenance rule. Entered during Part 2 at Reviewer 2's gate condition 3.

| ID | Gap / assumption | Why it exists | What breaks if it is mishandled | How it is bounded |
|---|---|---|---|---|
| G1 | **The Figure 2 SEZ input sets are not extracted.** They exist only inside the upstream `sez_neurons.pickle`, which was deliberately not loaded (a pickle is executable code; the file failed an execution-risk check). The Part 2 ID sets (`id_sets_v1`) therefore cover every population the published experiments define in text — GRNs, JON sets, MN9, aDN1/aDN2, aBN1, three-inhibitory — and not the SEZ types. | The upstream repository offers no text source for these sets; loading the pickle without authorisation would break the project's no-untrusted-execution rule. | If a later part needs SEZ inputs (Figure 2 battery reproduction, or Part 5 decoder design) and treats the gap as filled, it would either silently load the pickle or invent the sets — both are provenance failures. | The gap is on record here and in `PART2-ID-SETS.md` §5. Closing it requires a decision on record at the time: Angelic authorises a quarantined load, or the sets are reconstructed from the paper's SEZ type descriptions (which raises the v783-crosswalk problem, also on record). Until then, no part may use SEZ populations. |
| — | **RQ-C5 cross-reference (not a new entry):** the sugar GRN count asymmetry behind RQ-C5 is now confirmed from the upstream notebooks themselves — 21 right vs 10 left sugar GRNs (Part 2 extraction, `id_sets_v1`) — and RQ-C5 remains an **open hypothesis** until Part 3's dedicated runs resolve it (A14; Reviewer 2 gate condition 2). No MN9 asymmetry claim is made before then. | — | — | — |
| G2 | **The aDN2 set holds the left member of a bilateral type only** (entered 24 Nov 2026, Part 2b gate condition (d); full record in `PART2-ID-SETS.md` §7 and `PART2B-BUILD.md` §10.3). The upstream source names the extracted neuron `id_DN2_l` — aDN2 is a sided type and a right aDN2 exists in the v630 brain, but its root ID appears in no text source in the project, and the v630 materialisation carries no type/side annotation to identify it from. aDN1's bilaterality is undetermined from the project data (named `id_DN1_1`, no side marker). | The published JON experiments read out the left aDN2 only; the extraction obligation was the published populations, so nothing charged was missed — the set is complete for the published experiments and anatomically incomplete for aDN2. | If a later part treats the DN sets as the complete anatomy, a decoder design could silently inherit a one-sided readout; if it instead guesses the right aDN2 from connectivity resemblance, that is a provenance failure of the same kind as G1's. | The frozen `id_sets_v1` artefacts are unchanged and nothing was re-run. Part 2b's symmetric decoder is recorded as forced by the published readout. Identifying the right aDN2 (and settling aDN1) requires a recorded crosswalk decision (v783-era annotations do not join onto v630 — see G1's bounding and `PART2-ID-SETS.md` §6), taken on record before any Part 4/5 bilateral readout is designed. Until then, no part may claim a bilateral aDN readout. |

---

## 2. Metrics / N / power proposals — all PROPOSED (FINAL-PLAN §5.2, §5.6, §7.4)

§7.4 requires Part 0 to fix: the independent experimental units, N for trials and for shuffle networks (from a precision/power argument; the old build's N=10 / N≥20 figures [OLD] are starting points to justify or replace), the CI method, paired-seed use, the multiple-comparison correction, and TOST equivalence bounds per §5.6. Proposals below; the decision lines are repeated on the decision sheet (§7).

### 2.1 Primary metrics per behaviour

| Behaviour | PROPOSED primary endpoint | Source / note |
|---|---|---|
| Feeding (neural, E1) | MN9 firing rate (L and R reported separately), sugar condition, mean over the pre-registered trial window | §5.2. L/R kept separate because of RQ-C5 (A14) — never pooled until the asymmetry is resolved. |
| Feeding (body level) | **Deferred to Part 1b by design:** proboscis-extension angle/latency/duration *if* the installed body has an actuated proboscis; otherwise the named proxy (decoder-command duration + head/food contact event), called a proxy in every document | §5.2 + §4 Part 1b. Part 0 fixes the *rule* (audit decides, proxy named honestly), Part 1b fixes the metric. K2 applies if no honest metric exists. |
| Feeding (secondary) | Bitter-suppression ratio (sugar+bitter response ÷ sugar-alone response) | §5.2. Also a §5.6 convincing-positive criterion (suppression must appear with no decoder override). |
| Part 3 benchmark (model-vs-model) | Spearman rank correlation on the active subset (primary), with Pearson, thresholded Jaccard, precision, recall, and noise ceiling reported alongside | Part 3 row, §4; §8.3 / A15. Old-build comparison values [OLD]: Pearson 0.9936, Jaccard 0.9113, precision 0.9928, recall 0.9174 — comparison targets only. |
| Walk/halt (Core-B) | Halt latency after food contact (primary); forward velocity, yaw rate, tripod coordination index, halt-context correctness as secondaries | §5.2. Fixed now so Core-B inherits them; confirmed again at the Part 7b pre-registration. |
| Grooming (Core-B, only if Part 1b audits it in) | T1 tarsus–head contact events (primary); sweep frequency (secondary) | §5.2. |

### 2.2 Experimental units, N, and precision

- **Units (per §7.4):** for null families, the independent unit is the **independent shuffle network** — not the trial; for intact/lesion/baseline arms, the unit is the **independent seed** (trial). Reporting trials-within-one-network as if they were independent networks is prohibited.
- **PROPOSED — trials per condition/arm: N = 20 seeds.** Justification: the old build's canonical result used N=10 [OLD] and its SDs (e.g. MN9 sugar L 83.5 ± 6.5 Hz) imply a standard error of ~1.5 Hz at N=20 vs ~2.1 Hz at N=10; N=20 is also the old build's own upper starting figure (§7.4's "N≥20"). N=10 is retained **only** where Part 3 deliberately mirrors the old build's canonical configuration for comparability, and is labelled as such.
- **PROPOSED — independent shuffle networks per null family: n = 20** (for each of D1–D4 run in a confirmatory experiment), each network run with the same seed set as the intact arm (paired-seed design, below). Justification: §7.4 names independent networks as the unit and N≥20 [OLD] as the starting point; n=20 gives a bootstrap CI over networks whose width is driven by genuine network-to-network variance, which is the variance the E-Total claim actually rests on.
- **PROPOSED — matched control lesions: ≥5 independently selected controls per targeted lesion** (§5.6 requires the number fixed before outcomes; the §5.3 matching procedure itself — degree, baseline activity, class + transmitter-sign composition, neuropil, downstream influence, perturbation magnitude — is already fixed by Reviewer 3's adopted amendment).
- **PROPOSED — effect size of interest:** a **≥30% change** in the primary endpoint between intact and a comparison arm is the smallest effect the confirmatory design is built to resolve; smaller effects are reported with their CIs but not claimed as separations unless equivalence/separation criteria are met at the pre-registered bounds.
- **PROPOSED — precision target:** 95% CI half-width ≤ **15% of the intact-condition mean** for the primary endpoint. If the Part 3 pilot variances imply N=20 cannot meet this, N is raised by logged amendment *before* confirmatory runs — never after seeing confirmatory outcomes (K4 governs the unaffordable case).

### 2.3 Inference settings

- **PROPOSED — CI method:** percentile bootstrap, 10,000 resamples, resampling over the independent unit (networks for null comparisons, seeds otherwise), 95% intervals. (§7.4 requires the method named; bootstrap over networks/trials is its stated example.)
- **PROPOSED — alpha:** 0.05 throughout, including TOST (each one-sided test at 0.05, i.e. the 90% CI within bounds rule).
- **PROPOSED — multiple comparisons:** Holm correction across the arms × primary/secondary metrics family within each experiment's pre-registration.
- **PROPOSED — paired seeds:** the same master seed list is used across arms wherever the comparison is paired by design (intact vs each null network vs baselines), reducing variance legitimately per §7.4; the seed list is published with results (§7.5).
- **Part 6 agreement criteria (§4.1 requires these fixed at Part 0):** PROPOSED — MN9 results "agree" if the old point estimate falls inside our 95% CI (or vice versa); benchmark metrics agree within **±0.02** (the v1 starting proposal, §4.1) applied to the *named* primary benchmark metric (Spearman on the active subset) with the bootstrap CI method above; data counts must match exactly under the same counting rule, or the rule difference must fully explain the gap.

### 2.4 Equivalence bounds (TOST) — approach

Per §5.6: for **each** primary metric — for E-Total, E-Pathway **and** E-Baseline alike — the smallest scientifically meaningful effect is stated in advance; "no difference" may be claimed **only** on demonstrated equivalence within the bounds; a non-significant difference without equivalence is reported **inconclusive**, never as a null.

- **PROPOSED operationalisation:** for firing-rate endpoints, equivalence bounds = **±25% of the intact-condition mean**, or an absolute floor of **±5 Hz**, whichever is wider (the floor prevents a near-silent condition from acquiring absurdly tight bounds). For the bitter-suppression ratio, bounds = **±0.15** absolute. For body-level metrics, bounds are set at the Part 5 pre-registration using the same 25%-of-intact rule against the audited metric.
- **PROPOSED check:** bounds are sanity-checked against the Part 3 noise ceiling — a bound narrower than the reference's own trial-to-trial variability would make equivalence unprovable by construction and must be widened, with the reason logged, *before* confirmatory runs.

> **Decision lines (§7, items 2–8):** primary metrics; trials N; networks n; controls per lesion; effect size of interest + precision target; CI method + alpha + correction; Part 6 agreement criteria; TOST bounds rule. Each is PROPOSED above and becomes fixed only on Angelic's approval.

---

## 3. Budget proposals — all PROPOSED (FINAL-PLAN §9.1)

§9.1: budgets are set per part at Part 0 in two currencies — **wall-clock weeks** and **Angelic's review hours** (her time is the scarcest resource). A part that exceeds its budget stops and returns to Angelic with options; it does not silently expand. K1–K6 (§9.1) are in force throughout and are not re-proposed here.

| Part | PROPOSED wall-clock | PROPOSED Angelic review | Notes |
|---|---|---|---|
| 0. Foundations | 1 week | 2 h | This package + decision sheet; benchmark per §5. |
| 1. Environment + data | 2 weeks | 1 h | Includes the Python 3.12-vs-3.11 pin question and the sugarR verification (A13). |
| 1b. Body-capability audit | 1 week | 1 h | Fact-sheet approval decides the feeding metric and grooming's Core-B fate. |
| 2. Brain model | 2 weeks | 1.5 h | Reading note is a deliverable; literacy runs parallel per §4. |
| 2b. Minimal end-to-end loop | 1 week | 1 h | K6 stop rule in force. |
| 3. Brain validation | 3 weeks | 2 h | HARD gate; includes RQ-C5 resolution and the sugarR benchmark ladder. |
| 4. Body standalone | 1 week | 1 h | |
| 5. Bridge + closed loop (feeding) | 3 weeks | 2 h | HARD gate; decoder freeze; **human expert check point #1** (pre-registration freeze). |
| 6. Comparison checkpoint | 1 week | 2 h | Her decision meeting; nothing pushed before this gate. |
| 7. Intervention experiment (feeding) | 3 weeks | 2 h | HARD gate; **Core-A completes here.** |
| **Core-A subtotal (Parts 0–7)** | **≈18 weeks** | **≈15.5 h** | |
| 7b. Intervention — walk/halt (Core-B) | 2 weeks | 1.5 h | HARD gate. |
| 8. Documentation + release | 2 weeks | 3 h | Exact-text approval is hers; **human expert check point #2** (final gate). |
| **Core-B + release subtotal** | **≈4 weeks** | **≈4.5 h** | |
| **Full core total** | **≈22 weeks** | **≈20 h** | Stretch items (S1–S6) are budgeted separately, only when gated in (K5). |

Review-hour figures assume the §0.2(c) pattern: a short phone-readable summary per gate, full panel at HARD gates, one rotating reviewer at LIGHT gates — her hours buy decisions, not document-reading; anything longer than the summary is Buddy's job to compress.

> **Decision lines (§7, items 9–10):** the week budget and the review-hour budget per part (table above as the proposal; she may set a single global cap instead, in which case parts are fitted to it in order and the fit is shown back to her before Part 1 opens).

---

## 4. GPU trigger proposal — PROPOSED (D2 / FINAL-PLAN §0.2a)

D2 (confirmed): CPU is the reference platform for all confirmatory work; GPU bursts are allowed **only** for exploratory sweeps, and only after (i) a wall-clock benchmark at Part 0/1 and (ii) a parity check against the CPU reference on identical v630 input. §0.2(a) requires the trigger itself to be pre-set — a number, fixed now, not a feeling later.

**PROPOSED trigger statement (for Angelic to set the threshold):**

> The GPU gate opens for exploratory work when the Part 0/1 benchmark projects that the full confirmatory run set for the next confirmatory part (arms × networks × trials × trial duration, at the §2 Ns) would exceed **14 days of continuous wall-clock on this VM** — or, equivalently, when any single condition family projects beyond **72 hours**. Below the trigger, everything runs on CPU, however tempting. Above it, GPU may be used **for exploratory sweeps only**, and only after the parity check: the GPU backend must reproduce the CPU reference's MN9 L/R rates on identical v630 input within the Part 6-style tolerance (±0.02 on the primary benchmark metric; rates inside the CPU 95% CI). Confirmatory runs stay on CPU regardless, unless a separate formal amendment — with the parity evidence attached — says otherwise. If confirmatory N becomes unaffordable on CPU *and* the parity gate fails, K4 applies: N is reduced only by formal amendment with the power consequence stated.

Practical notes (from PART0-PREP §1 and ANGELIC-DECISIONS D2): this VM has **no GPU** (4 shared CPU cores, 7.7 GiB RAM — and only ~0.5 GiB was free at the prep check, so benchmark numbers must be re-taken on a quiet machine state); the realistic GPU routes are free-tier Google Colab or Kaggle, so "GPU access confirmed" (the S2 entry condition) means a named one of those, tested, not an assumption. S2 (the GPU backend port itself) additionally requires Part 3 passed + pre-registered parity tolerances.

> **Decision line (§7, item 11 is the benchmark; the trigger threshold is item 12):** the two numbers — 14 days / 72 hours as proposed — are hers to set.

---

## 5. Benchmark sequencing — recommendation (resolves the PART0-PREP §1 catch)

**The catch:** Part 0's pass criteria require recorded benchmark numbers (time a 100 ms brain trial on the actual VM), and the GPU trigger (§4) must be *set* at Part 0 — but a benchmark needs a working Brian2, and the pinned environment is a Part 1 deliverable. Brian2/FlyGym support for this VM's Python 3.12 (vs the old build's 3.11 pins) is UNVERIFIED.

**Option A — throwaway minimal Brian2 install for the Part 0 benchmark.**
A single-purpose virtual environment (own directory, quarantined from everything else), Brian2 + numpy installed at whatever versions resolve, versions recorded in the benchmark note, used for the 100 ms trial timing and nothing else, then deleted or left quarantined — it is never imported by project code and never becomes the Part 1 env.
- *Cost:* roughly an hour of setup/timing work; ~a few hundred MB of disk (137 GB free).
- *Risk:* the numbers come from an unpinned env, so they are **indicative, not reference** — Part 1 re-runs the identical benchmark in the pinned env and any material difference is logged. Small risk of the throwaway silently becoming load-bearing; mitigated by quarantine + the Part 1 re-run rule.
- *Bonus:* it answers the Python 3.12 question *now* — if Brian2 will not install/run on 3.12, Part 1 learns this before freezing pins, not during.

**Option B — formally defer the benchmark to the start of Part 1.**
Part 0 closes with the benchmark as a logged open item (or by formal amendment to the Part 0 pass criteria), the benchmark runs as Part 1's first task in the pinned env, and the GPU trigger is set from those numbers before any Part 3+ run planning.
- *Cost:* zero extra installs; benchmark numbers are reference-grade from the start.
- *Risk:* Part 0 cannot honestly meet its own written pass criteria ("benchmark numbers recorded") — closing it requires either an amendment or a knowingly incomplete gate, both of which set a bad precedent at the very first gate of a project whose entire discipline is "no quiet changes" (D6). The GPU trigger also stays a formula without a number for one more part.

**RECOMMENDATION: Option A — the throwaway minimal install.**
Part 0's criteria were written the way they were for a reason: the trigger and every later compute decision need a real number from *this* machine before Part 1 planning, and a first gate that amends its own criteria teaches the whole project the wrong lesson. Option A's only real cost — indicative rather than reference numbers — is fully controlled by the mandatory Part 1 re-run in the pinned env. It also converts the UNVERIFIED Python 3.12 question into a verified one a full part early, which de-risks Part 1's pin decisions either way the answer falls.

> **Decision line (§7, item 11):** Angelic approves Option A (recommended) or Option B.

---

## 6. Human expert check plan (D6 / FINAL-PLAN §4 Part 0, §8.6, §11.1)

**Why:** A18 — four AI reviewers can share a blind spot. The plan's mitigation is ≥1 human expert check at two named moments. **Nobody is contacted under this plan** — §11.1 is explicit that the approach is Angelic's decision and her conversation to have. This section only prepares: who could plausibly be asked (by role), what they would be asked, and the fallback.

### 6.1 Who could plausibly be asked (roles only — no individuals named, nobody approached)

In rough order of reachability through Angelic's existing networks (§11.1: her lab / Neuromatch / African Brain Data Network connections are the route):

1. **A senior computational-neuroscience researcher in her own lab network** (e.g. a PI-level or senior-postdoc role at the Africa Neuro Data Research Lab) — closest context, most likely to understand the project's constraints.
2. **A Neuromatch Academy instructor, TA, or senior community researcher** with whole-brain modelling or *Drosophila* experience — the Academy network is built for exactly this kind of methods feedback.
3. **A senior fellow / mentor in the African Brain Data Network** (MRI/fMRI cohort network) — methods-literate, though connectomics-specific experience would need confirming.
4. **A *Drosophila* connectomics researcher reachable through any of the above** (e.g. a FlyWire-community member) — the most domain-exact check, the least certain to be reachable; a stretch ask, not the plan's dependency.

One person covering one check is enough to satisfy the rule; the two check points may use the same or different people.

### 6.2 What they would be asked to check

**At the Part 5 pre-registration freeze** (before any Part 5/7 results exist) — a bounded, written review of the frozen pre-registration, ~1–2 hours of their time:
- Are the estimands (E-Total, E-Pathway, E-Baseline) the right comparisons for the claim being made?
- Are the null families and the matched control-lesion procedure (§5.3) genuinely fair — could a sceptic call any arm a straw man?
- Are the equivalence bounds (§2.4) defensible — neither trivially passable nor unprovable?
- Does the decoder design (§6.2) contain any path by which the answer could be built in?
- Anything load-bearing the panel and Angelic have all missed?

**At the final gate (Part 8)** — a bounded, written review of claims against evidence, ~1–2 hours:
- Does each headline claim match its permitted-conclusions wording (§7.6) and its provenance-ledger evidence (§6.3)?
- Is the assumption register (§1) complete — is any load-bearing assumption missing from it?
- Would they, as a reviewer, accept the reproduction and the intervention result as reported?

Their comments are recorded verbatim in the gate log either way; disagreement triggers the §4 discrepancy rule (STOP, log, diagnose, decide with Angelic), not silent edits.

### 6.3 Waiver template (if no expert check is obtained)

Per §0.2(c) / §8.6: if no expert check is on record by the Part 5 pre-registration freeze, Angelic signs a logged waiver stating the mitigation was not obtained; the same rule applies at the final gate. The mitigation may fail — it may never *silently* not happen.

```
HUMAN EXPERT CHECK — WAIVER
Project: ConnectomeToBehaviour (fresh rebuild)
Gate: [ Part 5 pre-registration freeze / Part 8 final gate ]
Date: __________

The approved plan (FINAL-PLAN.md, D6 / §8.6) requires at least one human
expert check at this gate, as a mitigation against shared AI-panel blind
spots. No such check is on record for this gate.

Efforts made to obtain one: ________________________________________
(e.g. roles/networks approached, dates, responses)

I, Angelic Charles, acknowledge that this gate is proceeding without the
human expert check, that the mitigation was not obtained, and that the
panel's review stands as the only external review of this stage. This
waiver is logged in the gate record and will be reported wherever the
gate's outcome is reported.

Signed: ______________________  Date: __________
```

> **Decision line (§7, item 14):** Angelic approves the approach plan (roles in §6.1, ask content in §6.2) — the actual approaching is hers, at her timing; the Part 0 obligation is only that the seeking starts (per §4 Part 0: "human expert check sought at pre-registration").

---

## 7. Part 0 decision sheet — for Angelic

**STATUS: APPROVED by Angelic, 23 Nov 2026 (~17:36 WAT) — all 14 items approved as proposed, no numbers changed** (plain-words walkthrough in the Connectome side chat; full record in `ANGELIC-DECISIONS.md`). Remaining Part 0 pass criteria: benchmark numbers recorded (Option A, item 11) and panel confirmation that no load-bearing source is missing; the gate closes on Angelic's sign-off.

*Every item below is one decision. Approving this sheet (with any numbers changed) closes Part 0, subject to the panel confirming no load-bearing source is missing and — under §5's recommendation — the benchmark being run.*

1. Approve the assumption register v1 (§1) as the project's starting list of what we take for granted, to be published with the results.
2. Approve the primary metrics: MN9 left/right firing rates for feeding, the Part 1b audit to fix the body-level feeding metric, and halt latency for walk/halt (§2.1).
3. Set trials per condition at N = 20 seeds for confirmatory runs, with N = 10 used only where Part 3 deliberately mirrors the old build (§2.2).
4. Set independent shuffle networks at n = 20 per null family (§2.2).
5. Set matched control lesions at a minimum of 5 independently selected controls per targeted lesion (§2.2).
6. Approve the precision plan: design for a 30% effect size of interest, with 95% CI half-width no more than 15% of the intact mean on the primary endpoint (§2.2).
7. Approve the inference settings: 95% bootstrap CIs over the independent units, alpha 0.05, Holm correction across each experiment's metrics (§2.3).
8. Approve the equivalence rule: "no difference" may only be claimed when TOST proves equivalence within ±25% of the intact mean (or ±5 Hz, whichever is wider; ±0.15 for the suppression ratio) — otherwise the result is reported as inconclusive (§2.4).
9. Approve the Part 6 agreement criteria: the old estimate inside our 95% CI counts as agreement, benchmark metrics agree within ±0.02, and data counts must match exactly under the same counting rule (§2.3).
10. Set the part budgets: the wall-clock weeks and your review hours in the §3 table (Core-A ≈18 weeks and ≈15.5 of your hours; full core ≈22 weeks and ≈20 hours).
11. Decide how the 100 ms benchmark is run: a throwaway minimal Brian2 install now, re-run in the pinned Part 1 environment (recommended, §5) — or defer the benchmark to the start of Part 1.
12. Set the GPU trigger: exploratory GPU use opens only if the benchmark projects the confirmatory run set beyond 14 days of CPU time (or one condition family beyond 72 hours), and only after a parity check against the CPU reference (§4).
13. Agree that `sugarR.parquet` is not trusted as the Part 3 benchmark until its hash and contents are verified at Part 1, because the served file is ~0.95 MB against the expected ~2.2 MB (§1, A13).
14. Approve the human expert check plan: the roles in §6.1 are approached (by you, at your timing), asked the questions in §6.2 at the Part 5 freeze and the final gate — or you sign the §6.3 waiver at either gate if none is obtained.

---

*End of Part 0 package. Companion files: `FINAL-PLAN.md` (approved plan), `PART0-PREP.md` (prep pack), `ANGELIC-DECISIONS.md` (D1–D7 confirmations), `RESEARCH-CHECK.md` (citation verification log), `panel/` (reviews + final approvals).*
