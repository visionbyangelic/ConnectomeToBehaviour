# Part 1b HARD-gate review — body-model decision

Gate class: HARD — full panel review and Angelic's decision required before the
Core-A body model is fixed. Gate question (from `PART1B-AUDIT.md` §5.2): the
plan's honest feeding metric (proboscis-extension angle/latency/duration) exists
only on FlyBody; on NeuroMechFly the feeding endpoint falls back to the plan's
named proxy (decoder-command duration + head/food contact). The options:

- **(i)** Adopt FlyBody (at least for feeding) and take the real proboscis-extension metric.
- **(ii)** Stay on NeuroMechFly and take the §5.2 named proxy.

Audit verdicts the gate rests on (installed FlyGym 2.1.1, verified from the
package itself): walking **CONDITIONAL PASS** (the fly walked 3.21 mm in 0.3 s
under a [1, 1] descending signal; halt within ~0.2 s of the signal going to
zero; condition is the proxy-labelling requirement); feeding **NOT YET DECIDED**
(proboscis actuation is calibrated and shipped on FlyBody — 5 DoFs with ranges
and gains — but not on NeuroMechFly, where driving the rostrum/haustellum would
mean inventing parameters); sensors **PARTIAL** (joint angles/velocities,
per-leg ground contact, per-segment contact forces, vision; no taste or smell,
so taste feedback must be constructed from contact events and labelled as
built); body-level grooming **out** of Core-B (no grooming controller or
trajectory anywhere in the package). Kill criterion K2 is not triggered — an
honest feeding metric exists on both routes.

---

## Reviewer 2 — verdict: (ii) NeuroMechFly, with the proxy labelled everywhere (23 Nov 2026)

Recommends staying on NeuroMechFly, with the proxy labelled everywhere it is
reported.

## Reviewer 3 — verdict: (i) FlyBody, with a mandatory feeding-body qualification gate (23 Nov 2026)

Recommends adopting FlyBody, with a mandatory feeding-body qualification gate
attached. His reasoning prioritises not claiming more than can be supported.

## Reviewer 1 — verdict: (ii) NeuroMechFly, with five conditions (23 Nov 2026, ~21:03 WAT)

Recommends (ii) NeuroMechFly, with the proxy labelled everywhere. This is the
decision he had already argued for in the earlier round, and neither of the
other reviewers' verdicts changes it. His deciding consideration: FlyBody is a
different body, not a more faithful one, and on a task about how a specific
brain drives a specific body, that is disqualifying, not a fidelity detail.

Why (ii) over (i), in his words in substance: (i) fails the task on its own
terms — validation is of a brain, not a walking score, so moving better in a
wrong body does not validate the brain. FlyBody cannot produce the behaviours
the feeding experiment needs — its legs are too short to reach the food at
z=0, and there is no proboscis mechanism at all — and fixing either would be a
major engineering task on a body whose proportions are not the fly's. And
NeuroMechFly already works end to end, with a body built from the actual
morphology and an IK solver written for it, so this is not a choice between a
finished system and a research project. (ii) is unproven on two fronts, both
priced in: the proxy is honest — it does not validate the feeding body, and the
plan already says so explicitly; and the brain-to-muscle interface is genuinely
unproven (the literature gives muscle anatomy and MN innervation, but no
demonstrated method for mapping neuron activity to muscle activation) — if the
interface fails, that is a negative result about the method, not a reason to
retreat to a body that cannot do the task. Neither option is a proven path, but
(ii) fails on the thing actually being attempted, while (i) fails on a premise.

Conditions — stated as terms of the approval, not optional extras:

1. **Proxy labelled everywhere.** Every figure, table, README and paper draft
   reporting a behaviour from the proxy states, in the caption or immediately
   adjacent text, that the leg model is NeuroMechFly's five-segment
   approximation, not the fly's leg. The NeuroMechFly model itself is not the
   claim — it is a well-documented, published model. The approximation is the
   thing that must be labelled.
2. **Feeding-body gate.** No behavioural claim for the feeding experiment may
   be made from the proxy. A body (real or modelled) whose legs reach the food
   and whose proboscis mechanism is represented must be built before any
   feeding claim is made. The proxy is a stepping-stone for walking and for
   the brain-to-muscle pipeline, not a substitute for the feeding body.
3. **Brain-to-muscle interface validated in a targeted way before the
   embodiment run.** Before the full embodiment run, demonstrate a controlled,
   repeatable mapping from MN activity to muscle activation on a test case
   (e.g. a single joint or a single muscle group). If it does not hold, stop
   and report the negative result rather than running the full pipeline on an
   unvalidated interface.
4. **Audit coverage applies to what is actually built.** The plan's audit
   requirements — unit tests, reproduction checks, review of the interface and
   the proxy — apply to the NeuroMechFly integration as implemented, not to
   the literature model in the abstract. The audit does not get lighter
   because the model is published.
5. **If the interface fails, no silent switch to (i).** The next step is a
   panel decision about whether to redesign the interface, build the feeding
   body first, or report the failure — not an automatic fallback to FlyBody.

Objection to the other audit verdicts: he does **not** object to Reviewer 2's
verdict — he agrees with it, including the proxy-labelling condition. He
**partly** objects to Reviewer 3's: he adopts Reviewer 3's feeding-body
qualification gate as condition 2 above, and would strengthen it from a
qualification to an outright prohibition on feeding claims from the proxy until
the feeding body exists — but a qualification gate does not fix (i), because
FlyBody still cannot reach the food, still has no proboscis, and still moves in
a body whose proportions are not the fly's. Choosing (i) would mean choosing a
body that cannot do the experiment, then gating ourselves from claiming we did
it.

Audit-verdict agreement: walking — agrees with **CONDITIONAL PASS**, the
condition being exactly the proxy-labelling requirement; feeding — agrees with
**NOT YET DECIDED**, the gate in condition 2 being the decision; sensors
**PARTIAL** — agrees, per-segment contact forces and vision being enough for
the constructed approach, with vision staying out of Core as planned.

---

## Panel tally and gate status

- Reviewer 1: (ii) NeuroMechFly, five conditions.
- Reviewer 2: (ii) NeuroMechFly, proxy labelled everywhere.
- Reviewer 3: (i) FlyBody, mandatory feeding-body qualification gate.

**Tally: 2–1 for (ii) NeuroMechFly.** The panel is complete. The body decision
is now Angelic's; no body-model choice is fixed until she decides.

## Panel decision consultation — Reviewer 1 final vote (23 Nov 2026, 22:40 WAT)

Angelic delegated the body decision to the panel ("Consult all the ai and let them decide"). Reviewer 1's final vote: **(i) FlyBody** — a REVERSAL of his first-round (ii) vote. Reason: his first-round reasoning rested on the claim that FlyBody "has no proboscis mechanism at all"; the audit's verified finding (5 calibrated proboscis DoFs, compiled and run in our env) removes that premise, and with it the case for (ii) collapses. Deciding argument: loop closure — NeuroMechFly ships no proboscis parameters, so feeding there means invented parameters or a proxy that does not change body state, leaving RQ-P3 (closed-loop vs open-loop) untestable for feeding; labelling a proxy does not create feedback. FlyBody closes the loop physically (extension command → labrum contact event → constructed taste feedback). Conditions: (1) mandatory feeding-body qualification gate before the implementation freeze (adopting Reviewer 3's condition; time-boxed, upstream demos unmodified, feeding-contact demo, pinned versions/hashes); (2) no quiet fallback in either direction — a gate failure goes to an explicit panel decision with rescope, by formal amendment; (3) the full feeding chain registered before the freeze (MN9 L/R → population rate → engineered mapping → proboscis joint targets → labrum contact → constructed taste feedback, provenance stated); (4) provenance wording — extension angle is a function of the decoder mapping, not independent evidence about the connectome; (5) Core-B body deferred — audit FlyBody walk/halt at the Core-B gate before committing Core-B to FlyBody (Part 1b demonstrated walk/halt on NeuroMechFly only); (6) confirm the audit ran in the pinned environment, old numpy conflict notwithstanding; (7) formal amendment to the plan where FlyBody currently sits as a stretch cross-check (S3). His first-round (ii) conditions carry over in substance: no feeding claims from any proxy; brain-to-muscle interface proven on a small test case first. Record note (his own flag): the Claude chat already contained an earlier Reviewer 1 Part 1b verdict recommending (i) with seven conditions, which differs from the first-round (ii) framing in the consultation assignment; he re-decided from the panel record as instructed, the corrected fact leads to the same (i) conclusion, and he flags the discrepancy for the record rather than letting it pass silently.

## Panel decision consultation — Reviewer 2 final vote (23 Nov 2026, 22:41 WAT)

Reviewer 2's final vote: **(i) FlyBody** — also a REVERSAL of his first-round (ii) vote, on the same ground: the corrected audit fact overturns the (ii) case. Conditions: mandatory feeding-body qualification gate before the freeze (the 5 proboscis DoFs demonstrated through their published ranges/gains); brain-to-muscle interface proven on a small test case first; no feeding claim beyond what qualification demonstrates, with version/commit, ranges/gains and the upstream "experimental" status recorded; taste feedback scoped as constructed; grooming out; no quiet fallback or silent switch if the gate fails — return to the panel; NeuroMechFly only as a later, labelled cross-check on non-proboscis aspects.

**FINAL TALLY — Decision A: FlyBody, unanimous (3–0).** Reviewer 1 (i, reversed), Reviewer 2 (i, reversed), Reviewer 3 (i, held). Angelic delegated this decision to the panel on 23 Nov 2026; the decision is therefore made: **Core-A's feeding body is FlyBody**, subject to the qualification gate and the no-quiet-fallback rule above. Part 1b is CLOSED on this decision.

## Panel decision consultation — Reviewer 3 final vote (23 Nov 2026, 22:41 WAT)

Reviewer 3 held his first-round vote: **(i) FlyBody**. Conditions: mandatory feeding-body qualification before the Core-A freeze (extension, holding, retraction, repeatability, measurement definitions, contact interaction, using the published FlyBody parameters); brain-to-muscle interface proven on a small controlled test case first; body and parameters frozen identically across all experimental arms; independent Core-B locomotion qualification (feeding capability does not establish walk/halt); no silent fallback — a qualification failure returns the body decision to the panel; upstream "experimental" caveat and exact source revision preserved; taste feedback labelled constructed; grooming excluded. **Decision A is unanimous: FlyBody, 3–0.**

## Angelic's acceptance (23 Nov 2026, 22:44 WAT)

Angelic accepted the panel's decisions ("Alright let's go with that"): FlyBody for Core-A feeding, and the Part 3 primary switch to 200 Hz. Part 1b stands closed on the panel's decision with her acceptance recorded.
