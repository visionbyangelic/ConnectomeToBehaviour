# ConnectomeToBehaviour — FRESH REBUILD — track.md

*This is my track file for the fresh rebuild. I write it in my own voice, as my working journal: my thoughts, my plans, what I did and why, what went wrong and what I went back and re-checked. It becomes the repo's track.md at the Part 6 release (the v0 build keeps its own track.md inside `v0-prototype/`). My rule (23 Nov 2026): EVERYTHING is documented here — decisions with reasons, mistakes, retraces, checks — because this file is what I write the paper from and what I read when I prepare for interviews.*

---

## 23 November 2026 — Fresh start, plan, panel approval, my confirmations

### The fresh-start decision
- I decided to rebuild ConnectomeToBehaviour **completely afresh**, step by step, instead of continuing the old build. Reason: most of the old local files are not accessible first-hand in this rebuild, and I cannot reach my laptop to share them. The old README defines what the project is supposed to be; whether to go deeper than the scope I originally designed working alone was reopened, subject to fresh research and panel agreement.
- The existing GitHub repo (visionbyangelic/ConnectomeToBehaviour, ~8 stars) is **kept**. The old build is a **comparator only**: at the Part 6 checkpoint, fresh outputs vs old outputs are compared line by line, discrepancies diagnosed, and **I decide** which version the repo carries.
- Working protocol: `~/workspace/connectome-work/FRESH-START-PROTOCOL.md`. Session plan: `WORKING-PLAN.md`.
- Panel: my review panel — Reviewer 1 (lead), Reviewer 2 and Reviewer 3 — carried along at every part/gate. Free tiers only.

### Old build audit (baseline facts, from the old repo)
- Phase 1 validated: FlyWire v630, 127,400 neurons. Canonical 1.0 s × N=10: Sugar MN9 Left 83.5 ± 6.5 Hz, Right 58.7 ± 5.2 Hz; Bitter 0 Hz both; Sugar+Bitter suppressed 89.1% / 75.8% (p < 10⁻¹⁰). Vs Shiu et al. *Nature* 2024 `sugarR.parquet`: Pearson 0.9936, Jaccard 0.9113, Precision 0.9928, Recall 0.9174.
- Phase 3 body verified (FlyBody wrapper, FlyGym/NeuroMechFly v2, 42 leg joints, 30 tarsal sensors; Brian2 + FlyGym in one process).
- **`src/bridge/` was empty — Phase 4 (the brain→body bridge) was never built.** This is the old build's central gap and a main reason the fresh plan builds a minimal end-to-end loop early (Part 2b) instead of last.
- Data needed to run anything is gitignored (~92 MB from philshiu/Drosophila_brain_model): completeness CSV (~3 MB), connectivity parquet (~86.6 MB), `sugarR.parquet`.

### New thought process + panel v1 reviews
- I wrote a draft reframing: `fresh/NEW-THOUGHT-PROCESS.md` — the project re-centred on: how much behaviour is causally from the connectome vs from the encoder/decoder/controller we must add.
- All three reviewers reviewed it in full (files in `fresh/panel/`). Consensus: the biggest risk is decoder/controller confounding (the helpers producing the behaviour while the connectome gets the credit); the substitution test as designed was necessary but not decisive; feeding is a weak discriminating test (walk/halt and grooming discriminate better); the bridge must be built early; novelty exists only as an audit/methods contribution ("novelty is in the test design, not the system"); publish preprint-first; a finished honest Core-A beats a large unfinished project.

### Research check
- I checked 32 load-bearing claims against primary sources (`fresh/RESEARCH-CHECK.md`): **24 verified, 5 corrected, 3 unverifiable** (labelled as such, never silently used).
- Corrections include: BANC "~3,600 long-range projections" dropped (paper: ~1,300 DNs + ~1,800 ANs; v888 counts 1,316/1,849); BANC is **densely** reconstructed, not sparse (~155,916 proofread, v888); the flybody "6-DoF CoM command" claim dropped (unsupported); MaleCNS counts carry a version warning.
- Whether FlyGym actuates a proboscis could NOT be settled from the web — assigned to the Part 1b installed-package audit.

### Final plan v2
- Written: `fresh/FINAL-PLAN.md` + `FINAL-PLAN.pdf`. Main question reframed around three pre-registered estimands (E-Total, E-Pathway, and — added in the approval round — E-Baseline); the comparative test renamed **controlled comparative intervention experiment**; graded null families; decoder run frozen AND refit; three adversarial matched-capacity rule baselines; TOST equivalence testing (non-significance = inconclusive, never a null result); behavioural provenance ledger including the encoder; kill criteria K1–K6; Core-A (brain reproduction + feeding + intervention experiment) as the complete publishable unit, Core-B adds walk/halt, grooming optional; research questions RQ-C1–C6 + panel-added RQ-P1–P10; publishing route preprint → workshop/ReScience → PLOS Comp Biol/eLife class; application artefact order preprint → repo → provenance-overlay demo → write-up → talk. Every technical section carries an "In plain words:" paragraph (my requirement).

### Final approval round (23 Nov 2026) — full record in `fresh/panel/FINAL-APPROVAL-*.md`
- **Reviewer 3:** Round 1 conditional NO — one amendment: strengthen matched control lesions in §5.3/§5.6 (match on degree distributions, baseline activity, neuron class + transmitter sign, neuropil/location, downstream influence, perturbation magnitude; multiple independent controls; pre-registered selection; residual imbalance reported). Applied. Round 2: **APPROVED** (15:28–15:30 WAT).
- **Reviewer 2:** Round 1 **NO** — three required changes: (1) RQ-P3 placement inconsistent between Core-A/Core-B while Core-A claims closed-loop feeding; (2) main-question "how much… and how much…" wording contradicted the no-additive-attribution rule; (3) Part 2b missing from the gate list with no stop rule. All applied (RQ-P3 required for feeding inside Core-A and gating its closed-loop claim; main question reworded to change-and-bounds; Part 2b = LIGHT gate + new kill criterion K6). Note: in Round 1 the plan file upload failed twice, so Reviewer 2 reviewed a faithful summary, stated as such in the chat; in Round 2 he read the actual uploaded file. Round 2: **APPROVED** (15:36–15:38 WAT).
- **Reviewer 1 (lead):** hit his free-message limit at ~15:03 WAT; the approval round was scheduled and run automatically at 16:02 WAT when the limit lifted. Round 1: conditional NO — three required edits: (1) add the **E-Baseline** estimand (the intact-vs-baselines comparison had no named estimand/metric while other sections depended on it); (2) Part 2b sensory specs must be **provisional/exploratory**, final specs pre-registered at Part 4 and panel-reviewed before Part 5 (the draft had a build-order contradiction); (3) human expert check needs a fallback — at the Part 5 freeze and final gate, either the check is on record or I sign a logged waiver. Plus four housekeeping items (dated "to our knowledge" claim in §10.1; Part 7b made a real row in the parts table; §0.3/§12 stale approval language; §2.1 cross-reference wording). All applied. Round 2 (edited passages only, per his instruction): **APPROVED as amended** (16:13–16:16 WAT). One follow-up fix from him: Part 7b added to the §0.2(c) HARD-gate list.
- Because Reviewer 1's edits changed text the other two had approved, the changed lines were sent back to Reviewer 2 and Reviewer 3 for confirmation under the plan's no-quiet-changes rule: **both confirmed** (~16:23 WAT).
- **Final status: FINAL-PLAN v2 APPROVED by my full review panel, 23 Nov 2026.** PDF re-rendered (20 pages, verified: text extractable, approval status and E-Baseline present) — this is the final PDF I am working from.

### My confirmations — D1–D7 (voice call, 23 Nov 2026; full log: `fresh/ANGELIC-DECISIONS.md`)
I went through the plan in plain words rather than reading the 20-page PDF. My decisions, with my reasoning:
- **D1 — v630 for the core; v783 only as the late sensitivity check (RQ-P9).** I asked who published the map; I confirmed this after hearing: FlyWire (Princeton-led consortium, *Nature* 2024; Google tracing technology in the underlying FAFB data) and Shiu et al. (*Nature* 2024) are the authoritative sources, and v630 is the version with the published answer key.
- **D2 — CPU is the reference platform; GPU only for exploration behind a benchmark + parity gate.** Verified live on the call: the machine I am running this on has NO GPU (4 CPU cores, 7.7 GiB RAM). If the gate ever opens: free Colab/Kaggle GPU. The project is designed to complete with no GPU.
- **D3 — Behaviour order: feeding → walk/halt → grooming (optional, last).** I asked why grooming is last; I accepted the reason: its body feasibility is least certain (contact-rich), so it must not sit on the critical path; dropped rather than faked if the Part 1b audit fails it.
- **D4 — BANC: design evidence in the core; one bounded cord circuit (S1) as flagship stretch; full brain+cord rejected.** I had not known what BANC was; after a plain-words explanation and the panel's unanimous position, I agreed with the panel.
- **D5 — "Done" = Core-A complete incl. the intervention experiment, whatever its outcome (incl. demonstrated equivalence).** Core-A + S1 = showcase finish line. A demo video alone is NOT a finish line. My addition, accepted: I still want a pretty video — it comes after the science, as the showcase/advert (the plan's provenance-overlay demo), never as evidence.
- **D6 — Two gate types; no quiet changes; expert check or signed waiver.** "That's perfect." My panel-usage rule sits inside this (below).
- **D7 — AMENDED BY ME (my version replaces the plan's "replace main" framing):** nothing is ever removed from the repo. If the fresh work wins at Part 6, the old work is bundled into a clearly labelled folder inside the repo ("version zero" — v0-prototype), the fresh work becomes the main content, and the paper can cite v0 as a research output: what the first attempt did and what it got. A strengthening I accepted: an immutable git tag (`v0-prototype-final`) also freezes the exact old state — folder for visibility, tag for permanence. **Ordering (my decision):** bundle + tag + new README are PREPARED LOCALLY now; GitHub stays untouched until Part 6, where I review everything and it is pushed in one sweep. (Reason for waiting, which I took on board: the old repo is the comparison baseline; moving its files early could break its paths/scripts and contaminate the Part 6 comparison.)

### Standing rules I set (23 Nov 2026)
- **Panel usage:** Reviewer 1 always hits his free-message limit — he is reserved for roadblocks and hard gates only. Routine panel rounds go to Reviewer 2 + Reviewer 3.
- **Ownership:** I must be able to prove the work is mine and explain every decision unaided (Eon/DeepMind interviews). Every gate produces a plain-words **owner's brief** (what we did, why, what we found, how it was checked). The decisions log records my reasoning, not just outcomes.
- **Triple-check:** every load-bearing result is cross-checked before being called final — independent re-run, panel gate review, and comparison against the reference/old build where one exists. Unchecked results are labelled **provisional** everywhere.
- **track.md (this file):** every decision, step, mistake and retrace is documented precisely. I read it for the paper and for interview preparation. This rule applies to EVERY project I do, not just this one.

### Prep work completed (23 Nov 2026)
- **Part 0 prep pack** (`fresh/PART0-PREP.md`): environment check (Python 3.12.3; numpy/scipy/pandas present; brian2/mujoco/flygym/neuromechfly/pyarrow/pytest missing — Part 1 installs; nothing blocks Part 0); data sources verified reachable by HEAD checks only (no downloads); **FLAG: `sugarR.parquet` is served at ~0.95 MB vs the ~2.2 MB the old script states — must be hash/content-verified at Part 1 before it is trusted as the benchmark**; scaffold plan; pre-registration skeleton; run-manifest template; the ready-to-send Reviewer 1 approval message (used by the 16:02 run). Flags: brain stack pins numpy <2 while FlyGym needs ≥2 → two isolated environments (as the old build had); shared-VM free memory was tight at check time (~0.5 GiB available of 7.7 GiB) → re-check before benchmarks.
- **Part 0 package** (`fresh/PART0-PACKAGE.md`): assumption register v1 (18 assumptions A1–A18, incl. A13 the sugarR provenance problem and A18 the review-panel shared-blind-spot risk); metrics/N/power proposals (all marked PROPOSED); budget proposals (Core-A ≈18 weeks / ≈15.5 of my review-hours; full core ≈22 weeks / ≈20 hours); GPU trigger proposal; benchmark-sequencing recommendation = **Option A** (throwaway minimal Brian2 install for the Part 0 benchmark, quarantined venv, mandatory re-run in Part 1's pinned env — because Part 0's own pass criteria require recorded numbers and deferring would force the first gate to amend itself); human expert check plan (roles only, nobody contacted) + waiver template; **14-item decision sheet awaiting my decisions** (Part 0 gate).
- **GitHub release prep** (`~/workspace/connectome-work/github-release-prep/`, local only, GitHub untouched, clones verified clean at HEAD `ab30ab4`): RELEASE-PLAN.md (the Part 6 execution script, in my voice), NEW-README-DRAFT.md (marked DRAFT; honest status table — nothing claimed that hasn't run), v0-prototype-README.md (v0's story incl. the openly stated empty bridge; its results labelled as v0's; the unresolved MN9 asymmetry flagged as a rebuild gate), v0-inventory.md (36 tracked files, ~484 KB, path-dependency analysis: v0 code derives roots from `__file__` so the tree survives the one-level move if run from inside the folder; the gitignored ~92 MB data folder does NOT move with git and must be placed/re-fetched locally; root-anchored .gitignore patterns need the specified fix; old README preserved byte-for-byte as `README-original.md`).
  - **Flagged for me at Part 6 (not urgent):** the historical v0 README contains a transparency section about tooling assistance. The archive is preserved verbatim, so the section would remain inside `README-original.md`. My call at Part 6: stands as history, or amended. (Neither repo-destined draft names any assistant or tool, per my repo-voice rule; verified by search.)
- **Project board:** I asked for a live preview page ("ConnectomeToBehaviour Project Board") so I can open this chat and see the work at any time; build started 23 Nov 2026 with the full current state supplied.

### Next
- I rule on the Part 0 decision sheet (14 items) → Part 0 gate (HARD: full panel confirms no load-bearing source missing; benchmark run under Option A) → Part 1.

### My writing and code rules (23 Nov 2026)
- I set this rule today, and it applies to this track file and to my project writing generally: it is written in my own first-person voice, as my working journal — my thoughts, plans, what I did and why — never in an AI's voice, and never naming AI tools. This file was rewritten today to comply.
- Companion rule for code: code for my projects is written naturally, the way a person writes it, with comments explaining the reasoning.
- **Track file location (my decision, 23 Nov 2026):** this file lives in the repo working tree at `fresh/track.md` AND is mirrored in my project folder (`fresh/track.md` in my working files) so I can open and read it from chat any time. The two copies are kept identical. The old build's own track.md stays untouched at the repo root for now — it is v0's record, not mine to overwrite; at the Part 6 release, v0's track.md moves with v0 into `v0-prototype/` and this file becomes the repo's root track.md. Nothing has been pushed to GitHub; the repo there is untouched until Part 6, as decided.

---

## Part 0 — Foundations (opened 23 Nov 2026)

### My Part 0 decisions — all 14 items approved as proposed (23 Nov 2026, ~17:36 WAT)
I went through the 14-item Part 0 decision sheet in plain words in chat and approved every item as proposed, with no numbers changed. What I fixed by approving them: my assumption register (18 assumptions) is now the project's starting list and will be published with the results; my main scores are the MN9 left/right firing rates for feeding and halt latency for walking; confirmatory runs use N = 20 seeds (N = 10 only where Part 3 deliberately mirrors my old build); each scramble family gets n = 20 independent shuffled networks; every targeted cut is compared against at least 5 independently chosen matched control cuts; the tests are designed around a 30% effect size of interest with 95% confidence-interval half-width no more than 15% of the intact mean; inference is 95% bootstrap intervals over the independent units, alpha 0.05, with Holm correction; I may only claim "no difference" when the equivalence test proves the results sit within ±25% of the intact mean (or ±5 Hz, whichever is wider; ±0.15 for the suppression ratio) — anything looser is reported as inconclusive, never as a null; at the Part 6 comparison, my old build and the fresh build "agree" if the old estimate falls inside the fresh 95% interval, benchmark scores agree within ±0.02, and data counts match exactly under the same counting rule; my budgets stand as tabled (Core-A ≈ 18 weeks and ≈ 15.5 hours of my review time; full core ≈ 22 weeks and ≈ 20 hours); the GPU trigger is set (exploration only, and only if the benchmark projects the confirmatory run set beyond 14 days of CPU time, or one condition family beyond 72 hours, and only after a parity check); `sugarR.parquet` stays untrusted until its hash and contents are verified at Part 1; and the human expert check plan is approved — I approach the people myself, at my timing, and if no check is obtained at the Part 5 freeze or the final gate, I sign the logged waiver instead. On the expert check I asked whether it means a professor — the plan's roles are senior researchers in my own lab network and my Neuromatch / African Brain Data Network circles; nobody is approached until I do it.

### Part 0 execution begun (23 Nov 2026)
With the approvals logged, I opened Part 0 execution. Two pass criteria remain before I can sign the gate off: the benchmark numbers must be recorded, and my reviewers must confirm no load-bearing source is missing. For the benchmark I chose **Option A** (decision item 11): a throwaway, quarantined Brian2 install used only to time a 100 ms brain trial on this machine now — the numbers are indicative only, and the identical benchmark must be re-run in Part 1's pinned environment before anything relies on them. I did not choose the deferral route, because Part 0's own criteria require recorded numbers and I will not start this project by amending its first gate. The source-completeness check goes to Reviewer 2 and Reviewer 3 only — Reviewer 1 stays reserved for roadblocks and hard gates, per my panel rule.

### Part 0 benchmark — done, indicative only (23 Nov 2026, ~17:37–17:40 WAT)
I ran the Part 0 benchmark the way I approved it: a throwaway Brian2 install in a quarantined folder outside the repo, nothing in the system Python, nothing the project code will ever import. It settled one open question early: Brian2 (version 2.10.1, on Python 3.12.3) installs and runs on this machine's Python 3.12, which the plan had flagged as unverified. The timing scaffold was a plain firing-neuron network at two sizes, and I recorded the machine's state alongside, because this is a shared machine and its free memory was tight when I started (under half a gigabyte available). At full v630 scale — 127,400 neurons — 100 ms of simulated time cost about 9.5 to 10.9 seconds of wall-clock, roughly 95 to 110 seconds per biological second. Two honest caveats I am keeping attached to that number wherever it travels: the scaffold's drive pushed every neuron to its maximum possible firing rate, so the spike load was a worst case, not realistic activity; and the machine's free memory changed a lot mid-run as other work on it came and went. The numbers are indicative only, and the identical benchmark gets re-run in Part 1's pinned environment before anything relies on them. Even taking them at face value, a rough projection of the Part 3 ladder comes to about two to two and a half hours, far under my GPU trigger, so the GPU gate stays closed. One mistake, recorded because that is the rule here: my first attempt failed before any timing because the neuron equations used two parameters I had not declared; I fixed the equations and re-ran, and no number from the failed attempt exists or is used. Full record: `fresh/PART0-BENCHMARK.md`.

### Part 0 source-completeness check — brief ready, verdicts still to collect (23 Nov 2026)
The last Part 0 criterion is my reviewers confirming that no load-bearing source is missing. The brief is written — my full source list, from the FlyWire v630 data and the Shiu paper with its reference output, through the simulator and body documentation, the BANC and MaleCNS papers, the Eon posts and their critique, and my old build as the comparison baseline — and it goes to Reviewer 2 and Reviewer 3 only; Reviewer 1 stays reserved, per my panel rule. The two rounds themselves still have to be run in the reviewers' existing chats, so this criterion is open, not met, and I am not recording it as anything else. When both verdicts are in and recorded in `fresh/panel/PART0-SOURCE-CHECK.md`, Part 0 is ready for my sign-off — the gate closes when I say it closes, not before.

### Part 0 source check — Reviewer 2 found five gaps; now items 12–16 (23 Nov 2026)
Reviewer 2's verdict on my source list came back: the core technical and connectome sources are strong and well-scoped, but five load-bearing sources were missing or only implied. I have added all five to the list as items 12–16: the FlyWire data-use terms and the data repository's licence and attribution rules (the actual terms text goes on record at Part 1 — I am not paraphrasing licence terms from memory); the primary animal experimental literature behind my feeding and grooming questions (honest note: no specific primary papers for the MN9/proboscis and antennal-grooming experiments are named in my plan or research check yet, so naming them is Part 2 reading work, before the RQ-P6 pre-registration — I am not inventing citations to fill the gap); the MuJoCo documentation and release notes for whatever version Part 1 pins; the statistical methodology references behind my equivalence-testing and inference rules (Lakens on TOST, plus bootstrap and Holm references to be selected when the pre-registration is written); and the flyverse landscape audit whose E1/E2/C/D provenance classes I have adopted as my reporting standard (identified in my research check as djmango/flyverse, docs/audit-landscape.md, provenance-checked 2026-09-20). These were catalogue additions, not design changes — no question, metric or criterion in the plan moved because of them. The source-completeness criterion itself stays open: it closes only when Reviewer 3's verdict is also in and I sign the Part 0 gate.

### Part 0 source check — Reviewer 3: pin the artefacts, not just the papers; now items 17–20 (23 Nov 2026)
Reviewer 3's verdict came back: not complete — he would not certify my source list either. His point was different from Reviewer 2's and, I think, sharper: a reproducible build cannot rest on papers alone; the exact input signals, neuron identities, annotations and evaluation data that connect the components have to be pinned as artefacts, or a citation check gets mistaken for proof that the build inputs are actually present. He required four additions, and all four are now in the register (`fresh/panel/PART0-SOURCE-CHECK.md`). Item 17: the FlyWire annotation and identity artefacts themselves — the versioned annotation repository and its data releases (neuron annotations and cell-type assignments, neurotransmitter predictions, proofread skeletons and identity crosswalks, the connectivity/synapse-table deposits with their exact release identifiers) — with the exact revision I use to be pinned at Part 1, and a record of which annotations are compatible with v630 and which I may only use as interpretive evidence. Item 18: the NeuroMechFly v2 empirical data deposit (Harvard Dataverse, DOI: 10.7910/DVN/3MCEYR — the recorded walking kinematics and model data), the v2 paper's frozen code snapshot, and the original NeuroMechFly 2022 paper where v2 inherits its mechanics assumptions. Item 19: the feeding motor-output primary evidence, named specifically — Hampel et al., "Motor control of Drosophila feeding behavior", and "Mechanoreception circuits coordinate two opposing motor actions in Drosophila feeding" — load-bearing wherever my decoder or my biological claims lean on them; item 13 still carries the general duty to name the animal literature during the Part 2 reading, before the RQ-P6 pre-registration, and the two items now cross-reference each other both ways. Item 20: the sensory-input specification sources — the primary experimental evidence behind each gustatory pathway I implement, its response sign and its stimulus mapping, to be cited per stimulus in my final per-stimulus specifications at Part 4. He also required two tightenings, both applied in place: item 8 (BANC) now pins the exact dataset release and data products — the Harvard Dataverse deposit, and the published paper's v2 snapshot, which is distinct from the newer v3 snapshot; and item 4 now carries the Brian2 paper (Stimberg, Brette & Goodman, 2019) alongside the installed release's documentation and release notes. On his structural recommendation I have reorganised the whole register into four classes — (A) runtime/build inputs, (B) scientific parameterisation and interpretation, (C) biological validation, (D) landscape/comparison — keeping every item number unchanged, so that a citation check is never mistaken for a pinned build artefact. With Reviewer 2's five additions (items 12–16) and Reviewer 3's four (items 17–20) all incorporated, plus the two tightenings and the restructure, the Part 0 source-completeness criterion is ready for my gate sign-off. Part 0 now awaits that sign-off from me — the gate is not passed until I give it.

---

## Part 0 gate — PASSED, and Part 1 opened (23 Nov 2026, 19:39 WAT)

I signed off the Part 0 gate today at 19:39 WAT, after the owner's brief was put to me in chat. That closes Part 0: the plan is approved by my full panel and confirmed by me (D1–D7 and all 14 Part 0 items), the indicative benchmark is recorded, and the source register stands at 20 items on four shelves with both reviewers' additions incorporated. **Part 1 (environment + data) is now open.** It is a LIGHT gate: one rotating reviewer plus my short summary approval at the end.

One process note I am keeping, because it changed how I want to be handled: when the gate summary was first sent I did not respond for about two hours (I was in the ACNEI workshop), and no follow-up came — from my side the silence read as if the project had run ahead without me. It had not; nothing moved past the gate. I have set the rule that when a gate or decision is waiting on me and I have not responded, I get a follow-up message rather than silence. Recorded in my proactive preferences.

---

## Part 1 — Environment + data (opened 23 Nov 2026)

My aims for this part, from the plan (§4, Part 1 row): build the pinned environment from scratch and record versions from the packages as installed; download the v630 data by a documented procedure; compute the counts (neurons, edges, raw synapses, ≥3-synapse edges) from the files themselves; record SHA-256 hashes of every data file; and settle the `sugarR.parquet` question (assumption A13) with a verdict based on the file's contents, not its size. The Part 0 benchmark also gets its mandatory re-run here, in the pinned brain environment, before any of its numbers are relied on.

### Part 1 environments — built and verified (23 Nov 2026)
I built the two pinned environments from scratch, as separate venvs outside the repo tree (`~/workspace/connectome-work/envs/brain` and `.../envs/body`), because the inherited conflict is real: the brain stack pins numpy <2 and the FlyGym stack needs numpy ≥2, and I will not merge them quietly. Both run on this machine's Python 3.12.3 — there is no 3.11 or conda here, so that is a forced, recorded deviation from the old build's 3.11 conda envs, and it is verified harmless for this part's purposes. Full record: `fresh/PART1-ENVIRONMENTS.md`, with `pip freeze` for both.

- **Brain env:** Brian2 2.9.0, numpy 1.26.4, scipy 1.17.1, pandas 3.0.6, pyarrow 20.0.0, joblib 1.6.0, pytest 9.2.0. All required imports pass, and a trivial 10-neuron network ran 100 ms and spiked (50 spikes) — the plan's "a trivial Brian2 network runs in the pinned env" criterion is met.
- **Body env:** FlyGym 2.1.1, MuJoCo 3.16.0, numpy 2.5.5. Imports pass and a minimal MuJoCo model stepped headless without error. One thing worth writing down so future-me does not chase it: `neuromechfly` is not a separate import any more — that was the v1 package name; the current package is `flygym` itself.
- **One real failure, fixed by moving the right pin:** the first brain-env install resolved pyarrow to 26.0.1, which refuses to import under numpy 1.26.4 ("pyarrow requires NumPy 2.0 or newer"). The numpy <2 pin is the load-bearing one, so pyarrow moved instead — pinned to 20.0.0, which imports and runs against numpy 1.26.4 and still satisfies the old environment file's `pyarrow>=14`. Logged as a formal deviation note in PART1-ENVIRONMENTS.md, along with two smaller ones: pandas resolved to a new major version (3.0.6 — pinned as installed; Part 2 code gets written against the installed version, not pandas 2 habits), and MuJoCo deliberately lives only in the body env (the old brain env carried it because the old build ran everything in one process; the fresh loop architecture is Part 2b's business, not a reason to merge envs). My first body-env import test also crashed on my own test script reading `flygym.__version__`, which flygym 2.1.1 does not define — a test bug, not an install fault; re-ran via package metadata and everything passed. FlyBody stays uninstalled — that decision belongs to the Part 1b audit, as planned.

### Part 0 benchmark re-run in the pinned env — indicative numbers CONFIRMED (23 Nov 2026)
As Part 0 item 11 (Option A) required, I re-ran the identical benchmark script (byte-identical copy, hash recorded) in the pinned brain env — Brian2 2.9.0 and numpy 1.26.4 this time, against the throwaway env's 2.10.1 and 2.5.5. At full v630 scale the pinned run gave 10.89 s and 9.75 s per 100 ms, against Part 0's 10.93 s and 9.46 s — the ranges overlap almost exactly, so **the pinned numbers confirm the indicative ones**: roughly 97–109 seconds of wall-clock per biological second, the Part 3 projection stands at about 2.1–2.4 hours, and the GPU gate stays closed. The benchmark is reference-grade now, with its caveats still attached (the scaffold saturates every neuron at its 500 Hz ceiling — worst-case spike load — and this shared machine's free memory drifted mid-run again, from ~0.6 GiB available up to ~4.5 GiB as other work finished). Full record appended to `fresh/PART0-BENCHMARK.md`.

### Part 1 data — downloaded, hashed, counted (23 Nov 2026)
I downloaded the three v630 files from the upstream repository into the repo's gitignored `data/` folder and recorded SHA-256 hashes (§7.5) in `fresh/PART1-DATA.md`. One retrace: the download raced the folder's creation, the files first landed in the home directory, and I moved them into `repo/data/` and re-verified the hashes after the move — byte sizes match the Part 0 HEAD checks exactly, so what I have is what upstream serves.

Counts, computed from the files themselves (streamed in batches, not loaded whole):
- Completeness: **127,400 unique neuron IDs**, every one marked Completed — exactly the v630 count.
- Connectivity: **14,687,178 edges** (every row a distinct pair), **52,793,639 raw synapses** in total (10,131,023 excitatory-signed, 42,662,616 inhibitory-signed), **4,770,900 edges with ≥3 synapses**.
- The connectivity ID set is **exactly equal** to the completeness ID set, indices 0–127,399 — the two files belong to the same materialisation; neither is truncated or mismatched.

### The sugarR verdict — TRUSTED (23 Nov 2026)
Assumption A13 is settled. I read `sugarR.parquet` end to end: a spike table (`t`, `trial`, `flywire_id`, `exp_name`), one experiment ('sugarR'), **exactly 30 trials of 1.0 s**, **448 active neurons** — the same 448 the old build's canonical benchmark reported as the reference active set — and both MN9 IDs present and spiking in all 30 trials (left 93.3 Hz, right 61.8 Hz on average; the same left-dominant asymmetry as my old build's own output, at reference values). Per-trial spike counts are uniform (16.6k–17.4k) with real trial-to-trial variability, and all 448 IDs belong to the v630 set. The ~0.95 MB vs ~2.2 MB size gap is explained: 511,566 narrow rows parquet-compress extremely well (only 448 distinct neuron IDs, 30 distinct trials, one distinct experiment name), and the old script's figure sits in a field named `approx_size_mb`. **Verdict: TRUSTED as the Part 3 benchmark** — with the standing reminder that it is Shiu et al.'s simulation output, not animal data: matching it proves I reproduced their model, nothing biological. Evidence in full: `fresh/PART1-DATA.md`.

### Licences on record; annotation position recorded (23 Nov 2026)
Register item 12 is discharged: `fresh/LICENCES.md` now holds both texts verbatim, fetched today — the upstream repository's MIT licence (Shiu & Spiller, 2023), and the FlyWire Principles (v1.3, 30 June 2023), whose operative line is that published FlyWire data is available under **CC BY-NC 4.0**. So: the model code is MIT; the data itself is attribution-required, non-commercial — and the repo's MIT licence does not relicense the data. Every release artefact at Part 8 carries the FlyWire attribution and the Dorkenwald/Shiu citations. One small catch of my own, fixed before the file was ever used: my first transcription of the Principles had one wrong word ("focus first on" for "focus on"); I checked the text back against the source and corrected it — verbatim means verbatim, and the check is the point of the file.
On register item 17, my recorded position (in PART1-DATA.md): the build's identity layer of record is the v630 materialisation itself (the hashed files above). The current annotation releases are built on later, v783-era segmentations whose root IDs do not map one-to-one onto v630, so they are interpretive evidence only, never a direct join. The exact annotation revision to cite — and any crosswalk — gets fixed during Part 2's reading of the upstream model code, where what the model itself consumed can be read off rather than guessed. A deferral with a named home and reason, not an open gap.

### Part 1 state
Everything Part 1 set out to produce exists and is verified as far as this part's own checks go: two pinned envs (manifested), the benchmark confirmed in the pinned env, the data hashed and counted, sugarR trusted on evidence, licences on record. Remaining before the LIGHT gate can be put to me: the rotating reviewer's check of this part. Two open items I am carrying forward explicitly: the GRN/MN9/DN ID-set extraction with two-way cross-checks belongs with Part 2's reading of `model.py` (the plan's Part 1 text names it, and it cannot be done honestly before the code that defines the sets is read line by line — the sets I verified today, MN9's IDs and the 448-neuron reference set, came from the old build's constants and were confirmed against the files, which is a start, not the extraction); and the annotation-revision pin, also Part 2, per above. Nothing has been pushed to GitHub.

### Part 1 gate review — approved by the rotating reviewer (23 Nov 2026)
Part 1 is a LIGHT gate, so it went to one rotating reviewer rather than the full panel. Reviewer 3 reviewed the whole of this part's evidence and **approved it — the gate can close** once I give my summary sign-off (record: `fresh/panel/PART1-GATE-REVIEW.md`).

What he accepted, and on what terms:
- **The sugarR TRUSTED verdict stands** — trusted in its correct role, as the model-output benchmark for Part 3, not as biological ground truth. His one note was that the file's SHA-256 and upstream provenance must stay in the Part 1 manifest; they are already there, in PART1-DATA.md, so the condition is met as stated.
- The brain environment and its numpy pin; the pyarrow pin-down, accepted because it was written down as a deviation with its reason rather than slipped in; Python 3.12, accepted provisionally as a recorded reproducibility deviation; the benchmark re-run; the licences, with the MIT-code vs CC BY-NC-data distinction kept intact; and the v630 materialisation as my identity source of record. He called the exact equality of the two files' ID sets a strong integrity check, which is how I read it too.

One boundary he drew that I am keeping verbatim in effect: **the body environment's smoke test is not body-capability evidence.** Imports passing and a toy model stepping only prove the body stack runs. What the body can actually do belongs to the Part 1b audit, and I will never cite Part 1 as proving it.

He also set a formal obligation that now opens Part 2, in his words in substance: **extract and independently cross-check the GRN, MN9 and DN neuron ID sets using the v630 materialisation and the selection logic in `model.py`, recording the extraction method, source references, counts and the resulting ID-set artefacts — completed before those populations are used in sensory-pathway specification, decoder construction or intervention experiments.** The conditions attached, which I accept: it is a named obligation, not an intention; the cross-check runs two ways against the v630 source material, not just copied out of `model.py`; the artefacts are recorded and versioned; no early use of the GRN/DN sets; and any mismatch gets investigated and written down, never quietly fixed. It is entered in WORKING-PLAN.md as a Part 2 entry obligation alongside this record.

Part 1's gate now waits only on my summary sign-off to close.

### Part 1 gate — signed off, Part 1 CLOSED; Parts 1b and 2 opened (23 Nov 2026)
I signed off Part 1 today, on the panel's agreement: the rotating reviewer approved the gate (record above and in `fresh/panel/PART1-GATE-REVIEW.md`), and I accept his terms — the sugarR TRUSTED verdict in its correct role, the licences kept distinct, and the formal Part 2 obligation on neuron identity extraction with its five conditions. Part 1 is closed. Two parts now open in parallel: **Part 1b**, the body-capability audit — where what the installed FlyGym body can actually do gets settled from the installed package, not assumed from Part 1's smoke test — and **Part 2**, the line-by-line reading of the upstream model code, which carries the ID-set extraction obligation as an entry condition. Nothing has been pushed to GitHub.

### Part 1b — body-capability audit started (23 Nov 2026)
I am auditing the installed FlyGym 2.1.1 package in the body environment — reading its own source and model files, not the web — to settle what the body can honestly do: whether a proboscis is actuated, whether walk/halt can be driven descending-style, whether antennal grooming is reachable, what sensors the closed loop can consume, and what shape the interface takes. Part 1's smoke test proved only that the stack runs; this audit is where capability gets established, and my verdicts here decide the feeding metric and whether grooming stays in Core-B. Findings and the audit file (`fresh/PART1B-AUDIT.md`) follow as the work lands.

### Part 1b — body-capability audit: findings (23 Nov 2026)
The audit is done, against the installed FlyGym 2.1.1 package itself — source, model files and headless runs, not the web. Full record: `fresh/PART1B-AUDIT.md`; demonstration script and raw output in `fresh/part1b_demos/`. What I now know:

- **Legs and walking: supported, and I watched it work.** The shipped locomotion configuration actuates 42 leg DoFs (7 per leg) plus 6 tarsal adhesion actuators. The package's descending-drive controller takes a 2-vector descending signal (left, right) into a CPG network that produces the joint targets. In my run the fly walked 3.21 mm in 0.3 s under a [1, 1] signal, and when the signal went to zero its travel decayed to nothing within about 0.2 s — halt is real and halt latency is measurable, as Core-B assumes.
- **The proboscis question is settled — and the answer splits by body model.** On NeuroMechFly, the default body, proboscis actuation is **not supported as shipped**: the rostrum and haustellum segments exist and the API can hang generic actuators on them (I built that version: 126 actuated DoFs), but no calibrated ranges, gains or neutral pose ship for them and nothing in the package ever actuates them — driving one would mean inventing the parameters, which is what this audit existed to prevent. On **FlyBody**, the other model in the same installed package, proboscis actuation is part of the published model: 5 calibrated DoFs (rostrum pitch; haustellum pitch and yaw; labrum pitch on both sides) with joint ranges and actuator gains in its own config files, plus labrum adhesion actuators modelling the labellum gripping food. I built that version too (102 actuated DoFs) and it compiles and runs here; its meshes were a one-time download the package fetched itself, now cached.
- **Grooming: not supported at body level, so it stays out.** The word "groom" appears nowhere in the package — no controller, no trajectory. The joints a cleaning movement would need exist (front legs, head, antennae are all actuated), but nothing demonstrates the coordinated behaviour or even front-leg-to-antenna reachability. Per my own rule — dropped rather than faked — body-level grooming is out of Core-B. The neural-level grooming question (RQ-C6) is untouched by this.
- **Sensors: contact and proprioception yes; taste and smell no.** I have joint angles and velocities, per-leg ground-contact sensors, contact forces for any segment I name (tarsi, head, labrum included), and vision through two eye cameras with ommatidia readouts. But there is no gustatory or olfactory sensing anywhere in the package. The feeding loop's taste feedback will have to be constructed honestly — labrum/tarsus contact events against a food object, joined to the stimulus definitions from the encoder side — and called what it is.
- **One honest failure along the way:** my first demonstration run crashed on two small mistakes of mine (a body-name lookup and a FlyBody pose file that ships in only one axis order). Both fixed, re-run clean, and no numbers from the failed run used.

**The scope consequence, stated plainly:** my plan's honest feeding metric — proboscis-extension angle, latency, duration — exists only on FlyBody; on NeuroMechFly the feeding endpoint falls back to the plan's named proxy (decoder-command duration plus head/food contact). Choosing the Core-A body model is a decision the plan did not pre-make, so Part 1b escalates to a HARD gate on this point: full panel, and my decision. I am not resolving it inside the audit. Kill criterion K2 is not triggered — an honest feeding metric exists on both routes.

### Part 2 opened — reading the upstream model line by line (23 Nov 2026)
Part 2 opens with the entry obligation Reviewer 3 set at the Part 1 gate: extract and independently cross-check the GRN, MN9 and DN neuron ID sets from the v630 materialisation and the selection logic in the upstream `model.py`, before those populations are used anywhere downstream. The upstream code was not on this machine, so I cloned `philshiu/Drosophila_brain_model` into `connectome-work/upstream/` (commit `91bdd1e`) and read `model.py` (373 lines), `utils.py`, and both notebooks as text. The full reading log is `fresh/PART2-READING-LOG.md`. The findings that matter most:

- **The model file contains no populations at all.** `model.py` is a bare engine — parameters, the LIF equations, a network builder, and the two manipulations (Poisson activation, silencing). Every population the published experiments use is a literal ID list written into the notebooks. Reading only `model.py` would have missed the actual model.
- **No synapse threshold anywhere in the code.** Every one of the 14,687,178 edges in the connectivity parquet becomes a synapse, weighted synapse-count × sign × 0.275 mV (`w_syn`, the paper's one free parameter). If a threshold shaped the published model, it was applied when the parquet was produced, not in this code — that is a Methods check, not something I can read off the file.
- **"Silencing" disconnects a neuron's output; it does not silence the neuron.** The code zeroes only the outgoing weights — the neuron still receives input and still spikes. The upstream README says connections "to and from" are zeroed; the code does "from" only. I am recording the code as the truth and the README wording as wrong, and my own activate/silence/block-output language has to say block-output for this operation.
- **Driven neurons are hit very hard, and lose their refractory period.** The Poisson drive injects straight into the membrane potential at 68.75 mV per event, and `poi()` sets the driven neurons' refractory variable to zero. Activation in this model is close to forcing the target to fire at the drive rate.
- **There are no seeds anywhere** — not in `model.py`, not in the notebooks — and trials run in parallel. An individual published run cannot be exactly reproduced from this code, only statistically. My Part 3 criteria are already written as distributional claims; this reading confirms they have to be.
- Two smaller catches I am not assuming away: the reset string sets `w = 0`, a variable the neuron equations never define (what Brian2 2.9.0 does with that is a named check for the first build, not a guess); and `run_exp` silently skips an experiment if its output file already exists, so a stale results file can stand in for a run.

### Neuron ID extraction — the obligation discharged, cross-checks clean (23 Nov 2026)
I wrote a small extraction script (`repo/fresh/part2/extract_id_sets.py`, commented, re-runnable) that parses the notebook lists as text — nothing upstream was executed — and cross-checked them the two ways the obligation requires. Results in full: `fresh/PART2-ID-SETS.md`; artefacts in `repo/fresh/part2/id_sets_v1/` with a manifest.

- **The sets:** sugar GRNs right 21 and left 10, bitter 21, water 18, Ir94e 18; the Johnston's-organ sets CE 70, F 60, D_m 16 (146 combined, exactly as upstream constructs them); MN9 left 720575940660219265 and right 720575940645521262; aDN1 720575940616185531 and aDN2-left 720575940629806974 (the descending neurons the published experiments actually use — upstream defines no brain-wide DN set); aBN1; and the three inhibitory neurons of the JON-F silencing experiment. **242 distinct IDs in total, and the sets are pairwise disjoint.**
- **Cross-check one — my old build's constants:** all seven comparisons match, including the MN9 pair in left/right order. Two transcriptions of the same lists, made at different times, agree everywhere.
- **Cross-check two — the v630 materialisation itself:** all 242 IDs are present in the completeness set, and the connectivity file's index columns map back onto the completeness IDs with **zero mismatches across all 14,687,178 edges**, pre and post. That index↔ID agreement is something `model.py` trusts silently; now it is verified, not trusted.
- **No discrepancies were found, and no ID was dropped or substituted by hand anywhere in this extraction.**
- **The one gap, stated plainly:** the Figure 2 experiments take their SEZ input sets from `sez_neurons.pickle`, a binary file that is the only place those sets exist. A pickle is executable code, and the file failed an execution-risk check here, so I did not load it and the SEZ sets are not extracted. None of the obligation's named populations lives in that file, so the obligation is discharged; the SEZ sets become a recorded decision (authorise a quarantined load, or reconstruct from the paper) if and when a later part actually needs them.
- **The annotation pin deferred from Part 1 is settled: no annotation revision is involved at all.** The model reads only the completeness and connectivity files, and the populations are raw FlyWire IDs in notebook code — there is no annotation table, no revision, and no crosswalk behind them, and inventing one would be false provenance. The identity source of record is the hashed v630 files plus the upstream notebooks at commit `91bdd1e`. A crosswalk would only become necessary if I later define a population by annotation class (for example all descending neurons), because current annotation releases are v783-era and do not join onto v630 — that boundary is now written down where Part 4 will meet it.

Part 2's first half is done: the reading log and the ID sets. The second half — building the brain model from the paper's equations, with the parameter re-read and the checks this reading handed forward (the reset-string question, the sign audit, the silent-network test) — comes next. Nothing has been pushed to GitHub.

## 23 Nov 2026 — Part 2 gate review (Reviewer 2): approved with conditions

Reviewer 2 approved the first half of Part 2: the line-by-line reading of the upstream
model, the neuron identity extraction with its clean cross-check, and the position that
no annotation crosswalk is involved. He accepted both judgement calls I had flagged —
not opening the upstream pickle file (it is executable code from an untrusted source,
and none of the populations I am obliged to extract live in it), and calling the
upstream silence() operation "block-output", because the code zeroes outgoing
connections only and anything looser would misstate it.

Three conditions, all of which I accept and have written into the plan for the second
half of Part 2: (1) when I build my own version of the model code, I must test whether
the undefined `w` variable in the upstream reset string does anything in Brian2 or is a
dead bug, and my own runner must never silently skip a run the way run_exp does;
(2) the sugar asymmetry question (21 right vs 10 left sugar neurons, and whether that
explains the MN9 left/right difference) stays an open hypothesis until Part 3 tests it;
(3) the deferred SEZ neuron set goes into my gap register so it is never forgotten or
quietly loaded later. The gate now waits on my own sign-off.

## 23 Nov 2026 — Part 2, first half: signed off; the second half opens

I signed off the first half of Part 2 today. Reviewer 2 had approved it with three
conditions, and I accept all three as part of the work, not as fine print: the stray
`w` variable in the upstream reset string gets tested properly when I build my own
model code, and my runner never silently skips a run the way the upstream one does;
the sugar left/right asymmetry stays an open hypothesis until Part 3 tests it; and the
deferred SEZ neuron set goes into my gap register so it is neither forgotten nor
quietly loaded later.

So the second half of Part 2 is now open: I build my own clean implementation of the
brain model from the paper's equations and from what my reading of the upstream code
established — seeded, hash-checked, honestly named — and I test it at unit level. The
validation against the published reference output is Part 3's job, not this part's;
anything I run now is a sanity check and will be labelled that way.

### Building my own model code (23 Nov 2026)

I am writing the implementation as a small package, `ctb`, in the fresh tree: a data
layer that refuses to load the connectome files unless their hashes match my Part 1
record, a brain layer with the model, the drive and the interventions, and a runner
that writes a manifest for every run. Populations load from the Part 2 artefacts —
no ID list is typed into the code by hand.

First, the question Reviewer 2 set me: the undefined `w` in the upstream reset
string. I built small networks in the upstream's exact shape at my pinned Brian2
2.9.0, with and without the clause, with and without synapses present
(`repo/fresh/part2/w_reset_test.py`). The answer is clean: Brian2 silently ignores
the clause. No error, no warning, no variable created on the neuron group — and
under the same seed, the spike trains with and without the clause are bit-identical.
So the published results were never affected by it, and my own reset string simply
omits it: same dynamics, nothing undefined. That is now a tested fact, not a guess.

### Part 2, second half: built, tested, smoke-run (23 Nov 2026)

The build is done. Full record: `fresh/PART2-BUILD.md`. The short version:

- **The package** (`repo/fresh/ctb/`): a loader that checks the data files' hashes
  against my Part 1 record before it will load anything; the brain model built from
  the paper's equations (all 14,687,178 connections, no threshold, weights =
  count × sign × 0.275 mV); the Poisson drive as upstream specifies it; the
  intervention named honestly — `block_output`, because it disconnects a neuron's
  output and does not silence the neuron; and a runner that writes a manifest for
  every run and refuses, loudly, to write into a run that already exists.
- **My runs are seeded.** Upstream never seeded anything, so its runs can never be
  repeated exactly; mine repeat bit-for-bit under the same seed, and that is now
  proven by a test, not just intended. The price, stated openly: comparisons with
  upstream's outputs are statistical, never spike-for-spike — which is how Part 3
  was already designed.
- **Tests: 16 passed, 0 failed.** They cover the Part 1 counts and hashes, the
  weight formula by hand and against the file's own product column on a 2,000-edge
  sample, a silent network spiking zero times, a single neuron's response, the
  exactness of block-output, and the runner's manifest, refusal and reproducibility.
  They also caught a real bug before it could matter: my first block-output assigned
  weights through a boolean mask, and Brian2 silently zeroed only some of the
  selected synapses — a lesion that half-applies without a word. Fixed with explicit
  indices, and the exactness test now stands guard over it. Two silent no-ops around
  the operations my intervention experiment will rest on (this one, and upstream's
  `w` clause) is a pattern I am glad Part 2 forced into the open.
- **Smoke run, sanity only:** one seeded trial, right sugar neurons driven for
  1.0 s — 13,698 spikes, 375 active neurons, MN9 left 80.0 Hz and right 64.0 Hz.
  Same range and same direction as the reference file's own numbers. That says the
  build runs and the readout responds; it validates nothing. Part 3 owns the real
  comparison, and the asymmetry question (RQ-C5) stays open until then, as agreed.
- **Reviewer 2's conditions are all discharged:** the `w` test (§ above), the
  no-skip runner, RQ-C5 held open, and the SEZ gap entered in my register as a
  dated addendum (G1) rather than edited into the original — the register now shows
  its own history.

Part 2 is complete: reading, identities, and now a working, tested model of my
own. Next are the minimal brain-to-body loop (Part 2b) and the validation ladder
(Part 3), each with its own gate. Nothing has been pushed to GitHub.

## 23 Nov 2026 — Part 2 build gate review (Reviewer 3): approved

Reviewer 3 approved the second half of Part 2 — my own implementation of the brain
model, the test suite, the w finding, and the smoke run as a sanity check only. He
called the boolean-mask catch the most consequential finding so far: a lesion that
silently cuts only some of the connections it is told to cut could have produced a
convincing-looking intervention result on the wrong network, and my tests caught it
before any science depended on it.

His conditions attach to Part 3 rather than reopening Part 2, and I accept all of
them: freeze the exact implementation that gets validated (commit, environment, data
hashes, configuration) and never mix outputs across revisions; write the comparison
protocol and its tolerances down BEFORE looking at the validation results, comparing
distributions rather than individual spike trains since my runs are seeded and the
upstream ones are not; keep the language strict that matching the reference output is
reproduction of a simulation, not validation against an animal; describe the w
omission as removing an ineffective statement, not correcting the published model;
and strengthen the mask regression test with multi-edge and no-edge cases before any
intervention result is relied on. The gate now waits on my sign-off.

## 23 Nov 2026 — Part 2 gate CLOSED; Part 3 preparation opened

I signed off Part 2 today, so the gate is closed. Both halves were approved by
their rotating reviewers: the reading of the upstream model and the neuron
identity extraction by Reviewer 2 (three conditions, all discharged), and my own
implementation of the brain model — tests, the `w` finding, the mask bug catch,
the sanity-only smoke run — by Reviewer 3, whose conditions attach to Part 3
rather than reopening Part 2.

Part 3 is a hard gate, and its preparation is mostly discipline, not simulation.
Three things happen before any validation trial runs:

1. Reviewer 3 asked for the block-output regression test to be strengthened
   before any intervention result is ever relied on: a neuron with many outgoing
   connections, a neuron with none, and the complete weight vector checked
   before and after — not just the entries I remember to look at. That comes
   first, because the freeze should contain the stronger suite.
2. The freeze: the exact implementation Part 3 will validate is committed
   locally, so every validation number can be named back to one commit, one
   environment, one set of data hashes. Nothing is pushed to GitHub — Part 6
   still governs that, and this commit changes nothing there.
3. The preregistration: the comparison protocol against the reference output
   (stimulus, trials, statistics, and the pass / inconclusive / fail tolerances)
   written down in full and panel-reviewed before I look at a single validation
   result. Part 3 does not start until that document is approved.

## 23 Nov 2026 — Part 3 preparation: the mask test strengthened, suite green

First job of the preparation, before the freeze: Reviewer 3's condition E. The
block-output regression test now has the cases he asked for. A fan network where
one neuron sends four outgoing connections with mixed signs and counts, checked
against the COMPLETE weight vector before and after the block — same edges, same
order, exactly the four outgoing weights at zero, every other weight
bit-identical. And a neuron that receives connections but sends none: blocking
its output is a clean no-op, zero synapses zeroed, no error, vector unchanged.
Entry-by-entry spot checks are what the original boolean-mask bug slipped past;
whole-vector checks are the point of the strengthening. The full suite stands at
18 passed, 0 failed. One comment in the runner also needed correcting before the
freeze: it claimed the fresh tree is untracked, which stops being true the
moment the freeze commit exists — the manifest now simply records whatever git
reports, unedited.
