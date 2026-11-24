# §2.4 Resting Acceptance Test — Record

**Executed:** 24 Nov 2026 (before the Part 5 freeze, as pre-registered).
**Spec:** `PART4-SENSORY-SPECS.md` §2.4 (acceptance test and the Amendment Pass 1 operational definition of a false ignition), §2.3 (settle protocol), §4.5 (constructed taste event), §5.3 (JON channel).
**Code:** `repo/fresh/qualgate/acceptance_test.py` (body environment: FlyGym 2.1.1 / MuJoCo, Python 3.12).
**Machine-readable results:** `repo/fresh/qualgate/results/acceptance_test.json`.

## Pass rule (pre-registered)

N = 10 resting episodes per configuration; body settled per §2.3, then 3.0 s (30 chunks) with **no command and no stimulus pulse**, detectors armed from t = 0. **Pass: zero false ignitions across all 10 episodes.** A false ignition is (a) the constructed channel (taste event / JON channel) switching ON at any point, or (b) any single chunk exceeding its channel's on-threshold — JON: ≥ 8 leg-contact transitions in a chunk; taste: qualifying contact force > 0 against the food geom sustained ≥ 10 consecutive physics steps within a chunk.

## Verdicts

| Configuration | Verdict | Episodes valid | Episodes invalid | False ignitions | Wall clock |
|---|---|---|---|---|---|
| A — Feeding arena (FlyBody, §4.6 as qualified) | **PASS** | 10 / 10 | 0 | 0 | 239.8 s |
| B — Walk/halt arena (Part 2b loop configuration, NeuroMechFly) | **PASS** | 10 / 10 | 0 | 0 | 750.0 s |
| **Overall** | **PASS** | 20 / 20 | 0 | 0 | 989.7 s |

Invalid-episode rate: **0 / 20 attempts (0%)**. No replacement episodes were needed; every first attempt was valid.

## Configuration A — feeding arena

Construction exactly as qualified at gate execution #5: pinned FlyBody in the §4.6 arena — pedestal (r 0.5 mm, h 0.28 mm) + food disc on top (top surface at ground + 0.33 mm), centre 0.6 mm in front of the labrum tip's settled ground projection (pilot settle per episode; centre [1.016, 0.006] mm in episode 0's frame). The arena includes the execution-#5 proboscis contact pairs (six proboscis geoms paired with food and pedestal), without which the taste event is not measurable at all. Resting phase: e = 0 throughout (ctrl 0 on the proboscis DoFs; the all-zero vector is also the legs' command, as in the gate settle), labrum adhesion held off — the §4.3 adhesion rule engages only on a taste event, and the event detector is what this test judges.

Per episode (all 10 identical in every recorded number):

| Episode | Settle chunks | Food contact in warmup | Max qualifying run in warmup (steps) | Max qualifying run per resting chunk (steps) | Taste event ON | Max labrum–food force (N) | Max front-tarsus–food force (N) | False ignition |
|---|---|---|---|---|---|---|---|---|
| 0–9 (each) | 4 | none | 0 | 0 (all 30 chunks) | never | 0.0 | 0.0 | no |

The resting fly never touches the food: across all 300 resting chunks there was not one physics step with qualifying contact force, so neither the chunk threshold (≥ 10 consecutive steps) nor the event state machine was ever approached. The §2.3 feeding-arena addition also held: no labrum–food or tarsus–food contact during any warmup.

## Configuration B — walk/halt arena

Part 2b loop configuration: NeuroMechFly legs-only body (`make_locomotion_fly`), flat ground, spawn (0, 0, 0.8), descending signal (0, 0) through the packaged `HybridTurningController` for every step of warmup and rest (timestep 1e-4 s, 1000 steps per chunk). No `sim.warmup()` call — §2.3's chunked zero-command warmup is the warmup. JON channel armed from t = 0 with §5.3 hysteresis (ON ≥ 8, OFF ≤ 2 transitions per chunk).

Per episode (all 10 identical in every recorded number):

| Episode | Settle chunks | Warmup transitions per chunk | Max transitions per resting chunk | JON channel ON | False ignition |
|---|---|---|---|---|---|
| 0–9 (each) | 4 | 290, 0, 0, 0 | 0 (all 30 chunks) | never | no |

The spawn drop lands entirely in warmup chunk 0 (290 transitions, thorax Δh 1.085 mm) and is absorbed there — counted, never converted, exactly as §2.3 intends. From warmup chunk 1 onward the standing body produces exactly 0 transitions per chunk, matching the settled standing state §2.3 cites from Part 2b (0 from chunk 9 onward there; here 0 from chunk 1, because the §2.3 warmup runs from spawn rather than from a pre-warmed state). The on-threshold of 8 was never approached in any resting chunk.

## Determinism, stated plainly

Both bodies are deterministic and the spawns carry no stochastic element: within each configuration, all 10 episodes produced **identical** settle records and identical resting-chunk records (verified programmatically — one distinct record per configuration). The 10 episodes are therefore exact repetitions of one resting trajectory per configuration, not 10 independent samples of a distribution. That is the same situation the qualification gate's Q4 established for this body stack, and the test as pre-registered (N = 10 fresh instances, zero false ignitions) is satisfied on those terms; but no claim about variability across spawns should be read into this result — there is no spawn variability in the system as constructed.

## Surprises

None in the outcomes. The only point worth naming is the determinism above, and one construction note carried from the gate: the feeding configuration is only measurable because the arena pairs the proboscis geoms with the food and pedestal (the execution-#5 defect fix) — that pairing is part of the qualified arena and is used here unchanged.
