# Feeding-body qualification gate — record

**Gate:** the mandatory feeding-body qualification gate of FINAL-PLAN §0.4, protocol in
`PART4-SENSORY-SPECS.md` §7. **Executed:** 24 Nov 2026, from ~02:50 WAT, under my overnight
delegation (the Part 4 gate closed unanimously at ~02:47 WAT; I ratify or reverse this record
on waking). **Environment:** the pinned body env `envs/body` — FlyGym 2.1.1, MuJoCo 3.16.0,
numpy 2.5.5. **Scripts:** `repo/fresh/qualgate/`; machine-readable results in
`repo/fresh/qualgate/results/`. **Time-box:** ≤ 4 h including reruns (§7). The gate stopped at
Q1, far inside the box; no rerun was needed or taken.

## Verdict: GATE FAILED at Q1 — Q2–Q6 not run

| Step | Verdict |
|---|---|
| Q0 — pinned artefact verified | **PASS** |
| Q1 — unmodified upstream integrity | **FAIL** (sub-item (a) PASS; sub-item (b) NOT EXECUTED — see below) |
| Q2 — range and gain sweep | not run (gate stopped at Q1) |
| Q3 — extension / hold / retraction cycles | not run |
| Q4 — repeatability | not run |
| Q5 — feeding contact | not run |
| Q6 — brain-to-muscle interface, small | not run |
| Band guard (§4.4: θ_off = 3 × ε_res < 0.10 rad) | not evaluated — ε_res comes from Q2/Q3, which did not run |

Per §7.7 and the §7 no-quiet-fallback rule: **no body parameter was adjusted, no fallback was
taken, and nothing is frozen.** Partial passes freeze nothing. This failure returns to the panel
for an explicit rescope decision by formal amendment. What kind of failure it is matters, and
the record below is precise about it: **the body did not fail. A premise of the protocol did.**
Sub-item (a) — the sub-item that actually exercises FlyBody through unmodified upstream
material — passed cleanly. Sub-item (b) names a demo that is not FlyBody material and cannot
run in the pinned environment at all; the details are in the Q1 section.

---

## Q0 — Pinned artefact, verified before anything ran — PASS

Script: `qualgate/q0_verify_artefact.py` (wall-clock 0.01 s; ~4 s including interpreter start).
SHA-256 of the five model files in the installed package
(`envs/body/lib/python3.12/site-packages/flygym/assets/model/flybody/`), measured at gate
execution against the values §7.1 pinned:

| File | Pinned (§7.1) | Measured | Match |
|---|---|---|---|
| `fruitfly.xml` | `66e49595…bfb1a2c` | `66e49595…bfb1a2c` | ✔ |
| `joints.yaml` | `b90bf60c…431f977a` | `b90bf60c…431f977a` | ✔ |
| `actuators.yaml` | `31feee85…277fd317` | `31feee85…277fd317` | ✔ |
| `mujoco_globals.yaml` | `7ea81498…c4901e350` | `7ea81498…c4901e350` | ✔ |
| `rigging.yaml` | `eb852760…d628737` | `eb852760…d628737` | ✔ |

(Full hashes in `qualgate/results/q0.json`.) **5/5 match** — the artefact under qualification
is byte-identical to the artefact the specs froze.

**Mesh cache state (§7.1):** cache root `/home/hatch/.cache/flygym_assets/`; the FlyBody mesh
directory `flybody_fullsize_meshes_20260623a/` is present (cached at Part 1b) and is the only
cached asset directory. The listing was identical before Q0 and after Q1 ran: **no download
occurred during the gate.**

**Upstream's label, quoted as §7.1 requires** (FlyBody class docstring,
`flygym/compose/fly/flybody.py`): *"Support for the FlyBody body model is experimental."*

**Versions recorded:** FlyGym 2.1.1, MuJoCo 3.16.0, numpy 2.5.5 — the pinned body env, as
specified.

## Q1 — Unmodified upstream integrity — FAIL

Script: `qualgate/q1_upstream_integrity.py` (wall-clock 21.6 s). §7.2's pass criterion, in its
own words: both named pieces of upstream material run without error, all recorded body states
finite. The two sub-items came out differently, and both outcomes are recorded in full.

### Q1(a) — Packaged FlyBody single-step assets / `FlyBodyPreprogrammedSteps` replay — PASS

- The packaged asset loaded through the packaged class, unmodified:
  `FlyBodyPreprogrammedSteps` over `flygym_demo/complex_terrain/assets/single_steps_flybody.npz`
  — 200 phase bins, nominal step-cycle frequency 12.0 Hz, swing periods per leg recorded in
  `qualgate/results/q1.json`.
- The body was built exactly as the Part 1b audit built it (its Demo C construction):
  ALL_BIOLOGICAL FlyBody skeleton, ALL actuated-DoF preset (102 position actuators), the
  published FLYBODY_NEUTRAL pose as neutral input, **no gain overrides** — the actuators carry
  their published parameters from the pinned `actuators.yaml`.
- Replay: flat ground, 0.05 s warmup at neutral inputs, then **2.0 s (20,000 physics steps)**
  of stepping with the 42 leg DoFs driven through the packaged step trajectories (tripod phase
  offsets; all other actuators held at neutral throughout).
- Result: ran **without error**; **all recorded states finite** — every joint angle and every
  body position at every one of the 20,000 steps. Thorax travel over the replay: **28.86 mm**,
  i.e. the replayed steps genuinely walked the body (~14 mm/s), they did not merely twitch in
  place.
- Two upstream warnings were emitted by the package's own code during construction and are
  recorded for completeness: the position actuators take their kp from the published
  general actuator config (that is the published-gains route working as designed), and the two
  haltere-pitch DoFs have no entry in `actuators.yaml` (a gap in the published config, not
  something this gate may patch).

### Q1(b) — `flygym_demo/muscle_imitation/` load-and-step — NOT EXECUTED

This sub-item was not run, for three independent reasons, each sufficient on its own:

1. **Its required optional dependency is absent from the pinned env.** The demo's env module
   imports `gymnasium` at module level and raises ImportError if it is missing (its own
   guard). `gymnasium` is not installed in `envs/body` — verified directly (`pip list`: no
   gymnasium, no stable-baselines3, no torch) and programmatically by the gate script
   (`importlib.util.find_spec("gymnasium")` → None). The env therefore cannot even be
   constructed here. Installing packages into the pinned env mid-gate would change the
   environment the gate is qualifying under, so that route was not taken.
2. **My tooling barred me from importing it.** When I read the demo's source files, the file
   content failed an execution-risk check and I was instructed not to run, import, load or
   source that content. I complied; the demo module was never imported.
3. **Its meshes are not cached.** The musculoskeletal model's meshes are a separate S3
   lazy-download (`neuromechfly_musculoskeletal_meshes_20260623a`) that is not in the local
   cache — only the FlyBody meshes are. Even the underlying model load would have required a
   mid-gate download.

**And the correction that explains how this happened:** the demo is **not a FlyBody
environment**. Its factory builds `flygym.compose.build_musculoskeletal_simulation`, which
loads the **FlyMimic musculoskeletal model** — a pre-authored NeuroMechFly-derived MJCF
(`assets/model/musculoskeletal/best_combined_arm_damping_stiff_cvt3.xml`; FlyMimic body names
such as `LFFemur`; only the left-front leg is muscle-driven). §7.2's description of it as "the
`flygym_demo/muscle_imitation/` FlyBody environment" repeats a misdescription that entered at
the Part 1b audit (§5 of that audit calls it "a FlyBody mocap-imitation environment"). The
audit read the folder's purpose, not the model's provenance; I repeated it into the specs
without re-checking. Folder names are not evidence — that is the lesson, and it is the same
class of error this rebuild keeps catching.

**Q1 verdict: FAIL.** §7.2's criterion is "both run without error"; one of the two did not
run. I am not rewriting the criterion after the fact — §7.7 permits reruns only for
gate-script defects, and this is not one: the script is fine, the sub-item is unexecutable as
specified. The honest summary for the panel is narrow: **FlyBody itself passed every part of
Q1 that touches FlyBody.** The failure is a protocol-premise failure, and the rescope it needs
is small and obvious — strike or replace the `muscle_imitation` sub-item of §7.2 (it can never
bear on FlyBody integrity, and in this env it can never run) — but making that change is the
panel's decision, by formal amendment, not mine at the bench.

---

## What did not happen, stated plainly

- **Q2–Q6 did not run.** The gate stopped at Q1 per §7.7. No extension signs, no θ_ext values,
  no arena offset, no Q6 calibration curve exist from this gate — none are reported because
  none were measured.
- **The band guard was not evaluated.** ε_res is defined from Q2's steady-state errors and
  Q3's post-retraction residuals; with Q2/Q3 unrun there is no ε_res and no θ_off to check.
- **No body parameter was adjusted at any point** (adjusting one is an automatic gate failure;
  none was). The only commands ever sent to the body were the packaged step trajectories of
  Q1(a), inside the published actuator ranges, on the published gains.
- **No fallback was taken** — not NeuroMechFly-and-proxy, not a persisted-with FlyBody. Per §7,
  the failure returns to the panel for an explicit rescope by formal amendment.
- **Nothing is frozen.** The Q0 hashes stand as verified facts about the installed artefact;
  they become Part 5 freeze inputs only when a gate passes in full.

## Wall-clock

| Item | Wall-clock |
|---|---|
| Q0 script | 0.01 s (~4 s including interpreter start) |
| Q1 script (incl. FlyBody compile + 20,000-step replay) | 21.6 s |
| Gate session, first script to stop | ~2 min (02:50–02:52 WAT), of the ≤ 4 h box |

## Artefacts

- Scripts: `repo/fresh/qualgate/q0_verify_artefact.py`, `repo/fresh/qualgate/q1_upstream_integrity.py`
- Results: `repo/fresh/qualgate/results/q0.json`, `repo/fresh/qualgate/results/q1.json`
- This record: `fresh/FEEDING-BODY-QUALIFICATION.md`

---

## Re-run under Amendment Passes 1–3, 24 Nov 2026

Full re-run from Q0 under the final specification (Part 4 specs as amended by Passes 1–3,
including the revised §7.2, the §4.3 static map with feedforward, and the narrowed Q3 claim).
Rules as before: no body parameter adjusted, no fallback, first failure stops the gate.
Scripts: `repo/fresh/qualgate/q0_rerun.py`, `q1_rerun.py`, `q2_sweep.py`, plus the shared
`gate_common.py`; machine-readable results in `repo/fresh/qualgate/results/` with the
`_rerun` suffix. The record above stands untouched.

### Q0 — PASS

All five pinned FlyBody files hash-match §7.1 exactly (same digests as the first execution;
`results/q0_rerun.json`). The two Pass 3 premise checks, recorded there:

- **Ctrlrange premise holds.** For all five proboscis actuators the compiled model's
  actuator ctrlrange equals the joints.yaml range exactly (float equality, no rounding):
  rostrum [−1.24, 0.183], haustellum pitch [−1.59, 0.7], haustellum yaw [−0.0873, 0.0873],
  both labrum pitches [−0.00524, 1.05]; ctrllimited true for all five.
- **Compiled limit-solver values** for the five proboscis joints: jnt_solref (0.001, 1) and
  jnt_solimp (0.9, 0.95, 0.001, 0.5, 2) on every one — as expected from the Pass 4 calibration.

### Q1 — PASS

**(a) Packaged replay, re-run fresh** (Demo C construction, 102 actuators, published gains,
no overrides): 20,000 steps, all states finite, thorax travel 28.86 mm — the first
execution's numbers reproduced. Verdict PASS (13.1 s).

**(b) First-party load-and-step** (same construction, ctrl = 0 on all 102 actuators,
2.0 s = 20,000 steps at dt = 1e-4 s, qpos/qvel recorded at every step;
trace in `results/q1b_trace.npz`):

- h_0 = 2.34 mm (thorax height in the constructed initial state). The h_0 sanity check ran
  before stepping and passed: the neutral-pose standing thorax height read from the compiled
  model's qpos0 kinematics is 2.34 mm with the lowest geom at z = 0, inside [1.17, 3.51].
- All recorded states finite. Thorax height stayed within the band at every step
  (min 1.281 mm, max 2.34 mm, final 1.282 mm — the body sags from its spawn height and
  settles; it does not collapse).
- Velocity bound held at every step: worst actuated joint reached 0.243 of its bound
  (published range / 0.01 s).
- Joint limits held with room to spare: **no joint left its published range at any step**
  (the largest excursion over all joints and steps is negative — every joint stayed inside).
  On the recorded expectation for the rostrum at ctrl = 0: limit-resting there was an
  expectation, not a measurement; the expectation was penetration ≪ ε, about 0.001 rad or
  less (MuJoCo's documented relation under-predicts an independent replica at ctrl 0,
  ≈2e-4 vs ≈9e-4 rad; both are far inside ε = 0.005). In the event the rostrum never
  reached its limit at all — it stayed at least 0.179 rad inside its range for the whole
  run, because (as Q2 established, below) the compiled spring reference is 0, so the
  joint's zero-command equilibrium is interior, not on the 0.183 limit. The top-sweep-point
  expectation (≈0.001–0.002 rad penetration, inside ε) stands as recorded in the Pass 4
  calibration; Q2's sweep likewise recorded no limit excursion at any point.

Verdict PASS (11.4 s).

### Q2 — FAIL (criterion (i), both pitch joints). The gate stops here.

Per-DoF nine-point raw-target sweeps (0.5 s holds, steady state = mean over the final
0.1 s), judged against the clamped static map q̂_eff computed from the pinned YAMLs
(kp 10/1, stiffness 3, **springref 0.8 on the two pitch joints**). Full per-point data:
`results/q2_rerun.json`.

| Joint | Max steady-state error vs q̂_eff | Coupling max | Limits | Monotone | Verdict |
|---|---|---|---|---|---|
| Rostrum pitch | **0.1877 rad** | 0.0025 | within ε | yes | FAIL (i) |
| Haustellum pitch | **0.1857 rad** | 0.0014 | within ε | yes | FAIL (i) |
| Haustellum yaw | 0.0000 rad | 0.0001 | within ε | yes | PASS |
| Labrum pitch L | 0.0002 rad | 0.0000 | within ε | yes | PASS |
| Labrum pitch R | 0.0001 rad | 0.0000 | within ε | yes | PASS |

The pitch-joint error is a **constant offset**: measured steady state sits 0.184–0.188 rad
below q̂_eff at essentially every non-clamped point of both joints. Everything else about
the sweeps is clean — coupling ≤ 0.0025 rad, no limit excursion anywhere, strictly
increasing empirical maps, all states finite.

**Cause, established from the compiled model (diagnostic, `results/q2_diagnostic.json`):**
the map's springref premise is false in the compiled artefact. In MuJoCo a joint's spring
reference is its qpos0 entry; in the compiled FlyBody model qpos0 = 0.0000 for all five
proboscis joints (stiffness 3.0 applied correctly). The joints.yaml springref of 0.8 on the
pitch joints is not carried into the compiled spring reference by the package's
construction. The offset the sweeps measured is exactly the missing term:
(ks/(kp+ks))·0.8 = (3/13)·0.8 = 0.1846 rad. Recomputing the map with springref = 0 against
the **same recorded steady states** fits all five joints to ≤ 0.0035 rad (rostrum 0.0035,
haustellum pitch 0.0011, yaw 0.0000, labrum 0.0002/0.0001) — inside the 0.05 tolerance
everywhere. So the servo/spring physics behaves exactly as the map family describes; the
single wrong input was the spring reference. This is a specification-premise failure of
the same family as the first execution's Q1(b) failure (a fact about the artefact that
the spec text, written from the package's files, got wrong) — **not** a defect of the body,
and not something this gate may repair: §7.7 allows reruns only for gate-script defects,
and adjusting the map's premise mid-gate would be exactly the quiet change the gate
exists to prevent. The failure returns to the panel by formal amendment.

Two record items from the diagnostic, for the panel's use (neither changes the verdict):

- **Extension signs, measured with corrected sampling.** The gate script's first tip
  sampling was defective (a geom name lookup resolved to id −1 and read an unrelated leg
  geom; the labrum geoms are `l_labrum_lower` / `r_labrum_lower`, one per labrum body).
  Re-measured at the two pitch joints' range ends, tip = mean of the two labrum geom
  centres: **s = −1 for both pitch joints** — extension is toward the negative range end
  (tip farther from the head and lower there). θ_ext: rostrum −1.19 rad, haustellum
  pitch −1.54 rad (range end pulled 0.05 rad inside, per §4.4).
- **The band guard could not have rescued this gate.** θ_off is defined from ε_res, whose
  Q2 term alone, on the recorded numbers, is 0.1877 rad; 3 × 0.1877 = 0.563 rad ≥ 0.10 rad.
  Stated as arithmetic on recorded numbers only — the band-guard step itself was not
  executed, because the gate stopped at Q2 and Q3 never ran.

### Q3–Q6 — did not run

The gate stopped at Q2 per §7.7. No Q3 cycles, no E_max, no Q4 repeats, no Q5 arena or
offset, no Q6 calibration curve exist from this re-run. **No body parameter was adjusted
at any point; no fallback was taken; nothing is frozen.** The Q0 hashes and premise
checks stand as verified facts about the installed artefact. What the panel is asked to
decide, by formal amendment: the §4.3 map's spring reference — the compiled artefact
implements springref = 0 (qpos0), whatever joints.yaml declares — and the consequential
re-derivation of every map-dependent number in §§4.3–4.4 and §7 (rest equilibria,
feedforward, Q3's predicted achieved E, ε_res inputs) before any further gate run.

### Wall-clock (re-run)

| Item | Wall-clock |
|---|---|
| Q0 script (hashes + premise checks) | 7.2 s |
| Q1 script ((a) 13.1 s + (b) 11.4 s) | 24.5 s |
| Q2 script (settle + 45 holds) | 56.5 s |
| Post-failure diagnostic (not a gate step) | 12.9 s |
| Gate session total | ~2 min of script time, of the ≤ 4 h box |

### Artefacts (re-run)

- Scripts: `repo/fresh/qualgate/gate_common.py`, `q0_rerun.py`, `q1_rerun.py`,
  `q2_sweep.py`, `q2_diagnostic.py` (plus `explore_api.py`, exploration only)
- Results: `repo/fresh/qualgate/results/q0_rerun.json`, `q1_rerun.json`,
  `q1b_trace.npz`, `q2_rerun.json`, `q2_diagnostic.json`
- This record: `fresh/FEEDING-BODY-QUALIFICATION.md` (this section appended; earlier
  sections untouched)

---

## Re-run under Amendment Passes 1–3 and 5, 24 Nov 2026

Third execution of the gate, in full from Q0, under the specification as
amended by Passes 1, 2 (revised), 3 (revised) and 5; Pass 4 was proposed
and withdrawn, so ε = 0.005 rad stands unamended. Scripts and results in
`repo/fresh/qualgate/` (`gate_common3.py`, `q0_rerun3.py`,
`q2_predictions.py`, `q1_rerun3.py`, `q2_rerun3.py`, `q3_rerun3.py`,
`q4_rerun3.py`, `q5_rerun3.py`, `q5_diagnostic.py`; results under
`results/` with `rerun3` naming; summary at
`results/gate_summary_rerun3.json`). Environment as pinned: FlyGym
2.1.1, MuJoCo 3.16.0, numpy 2.5.5 (body env). Total gate script wall
clock ≈ 236 s of the 4 h box. **Gate verdict: FAIL at Q5.** Q0–Q4 pass;
Q5 fails on functional reach (below); Q6 was not run; nothing is frozen;
no body parameter was adjusted at any point and no fallback was taken.

### Q0 — artefact pin and premise checks (§7.1 as amended): PASS

All five pinned files hash-match §7.1 exactly (same SHA-256 values as
the earlier executions; `results/q0_rerun3.json`). Premise checks, all
recorded per joint in the artefact:

- (a) compiled actuator ctrlrange equals the `joints.yaml` range exactly
  for all five proboscis actuators (ctrllimited true).
- (b) compiled solref (0.001, 1) and solimp (0.9, 0.95, 0.001, 0.5, 2)
  on all five joints.
- (c) Pass 5 compiled-parameter record, labelled by joint: for every
  proboscis joint **qpos_spring = 0.0, qpos0 = 0.0, jnt_stiffness = 3.0**;
  per actuator **gainprm[0] = −biasprm[1] = 10.0** for the three head
  joints and **1.0** for the two labrum joints — pure position servos,
  exactly the expected values; no premise failure.
- (d) construction recorded: the Demo C construction
  (`q1_upstream_integrity.build_flybody()` — `FlyBody` with the
  ALL_BIOLOGICAL skeleton, YAW_ROLL_PITCH, neutral pose
  `KinematicPosePreset.FLYBODY_NEUTRAL`, POSITION actuators with the
  neutral input, `add_leg_adhesion()` with shipped defaults for the
  Q2–Q6 builds) in a `FlatGroundWorld`, fly added at (0, 0, 1.0) with
  identity rotation. The neutral pose's POSITION inputs for the five
  proboscis DoFs are all 0.0 rad. Spring references follow this neutral
  pose (§7.1); the upstream "experimental" label for FlyBody support is
  on the Q0 artefact.

### Pre-registered Q2 prediction table (§7.3, Pass 5)

Computed after Q0 and **before** the Q2 sweep ran, from the Q0-recorded
compiled values (kp from gainprm, ks = 3.0, ref = qpos_spring = 0):
`results/q2_predictions_prereg.json`, timestamped 2026-11-24T02:43:44Z.
Predicted achieved ranges: rostrum pitch [−0.954, +0.141],
haustellum pitch [−1.223, +0.538], haustellum yaw [−0.067, +0.067],
labrum pitches [−0.001, +0.263]. **No point on any joint is clamp-bound**
under the corrected map, as Pass 5 expected.

### Q1 — unmodified upstream integrity (§7.2 as revised): PASS

(a) The packaged replay reproduced exactly: 20,000 steps, all states
finite, thorax travel **28.86 mm**. (b) First-party load-and-step,
ctrl = 0 on all 102 actuators, 20,000 steps with qpos/qvel recorded at
every step: h₀ = 2.34 mm and the h₀ sanity check passed before stepping
(neutral-pose standing height 2.34 mm, lowest geom at z = 0, inside
[1.17, 3.51]); all states finite; thorax within band at every step
(min 1.281 mm — the same settle sag as before, max 2.34); worst
actuated-joint velocity 0.243 of its bound; **no joint left its
published range at any step** (max excursion negative). The Pass 5
expectation held: the proboscis rests at its interior ctrl-0 equilibria
(rostrum −0.0033 rad final), with no limit-resting anywhere. Wall clock
25.1 s. Trace: `results/q1b_trace_rerun3.npz`.

### Q2 — per-joint range sweeps (§7.3): PASS

Judged against the pre-registered table. Max map-relative steady-state
errors: **rostrum 0.0035 rad, haustellum pitch 0.0011, haustellum yaw
0.0000, labrum L 0.0002, labrum R 0.0001** — the corrected map, recorded
as a prediction before the sweep, is confirmed by measurement on all
five joints (the second execution's failure is resolved at its cause:
the map now reads its spring reference from the compiled artefact).
Coupling ≤ 0.0025 rad everywhere; no limit excursion at any step; all
finite; **the empirical map is strictly increasing in target on all five
joints**, with no clamp-bound points to exempt. Extension signs, by the
§7.3 tip-displacement method (tip sampled at the corrected
`l_labrum_lower`/`r_labrum_lower` geoms — see the deviations note):
**s = −1 for both pitch joints**; θ_ext: rostrum **−1.19 rad**,
haustellum pitch **−1.54 rad**. Wall clock 56.3 s.

### Q3 — extend–hold–retract cycles (§7.4): PASS (narrowed claim)

Five cycles through the registered chain with the feedforward inverse
from the Q0-recorded compiled values; θ_rest = the settled ctrl-0 pose
(rostrum −0.0033, haustellum pitch −0.0009, yaw ≈ 0, labrum ≈ 0).
Map-predicted achieved E at e = 1: **2.1728 rad**; measured hold-mean
**E_max = 2.1746 rad**, which is **0.7695 of the raw-extremes E**
(2.8264 rad). Every cycle: E at ramp end = 1.0008 × predicted (≥ 90%
required); hold deviation ≤ 1.8 × 10⁻⁶ rad; post-retraction residuals
≤ 1.5 × 10⁻⁶ rad; no range violations; all finite. Per the Pass 3
narrowing, this certifies **model-consistent extension only**; whether
the extension functionally reaches food is Q5's question — and Q5's
answer below is no. Wall clock 48.1 s.

### Q4 — repeatability (§7.5): PASS

The Q3 cycle in five fresh Simulation instances with identical commands:
peak E = 2.1746 rad in every run (**range 0.0 rad**); onset (chunk
resolution) at cycle chunk 0 in every run (**range 0 ms**). Wall clock
64.3 s.

### Q5 — feeding-contact demonstration (§§7.5, 4.6): FAIL

The §4.6 arena as written: flat ground; food = flat cylinder, radius
0.5 mm, height 0.05 mm, top at ground + 0.05 mm, named `food`,
contact-reporting, centre 0.6 mm in front of the labrum tip's settled
ground projection (pilot settle: tip projection (0.416, 0.004) mm;
forward = the ground-projected head→tip direction ≈ +x; first centre
(1.016, 0.006) mm). Food-specific contact forces were taken from the
body's own contact reporting (see deviations). Two attempts, both with
clean settles (4 chunks, no food contact during warmup) and full
extension reached (E = 2.1746 rad):

- **Attempt 1 (offset 0.6 mm):** maximum labrum–food contact force
  **0.0 N**; maximum front-tarsus–food force 0.0 N; the §4.5 event never
  turned ON; adhesion never engaged. Criterion (i) unreachable at this
  placement.
- **Attempt 2 (the single §7.5(iv) adjustment):** food centre moved to
  the labrum tip's ground projection measured at full extension,
  (0.563, −0.003) mm — a final offset of **0.146 mm** in front of the
  settled tip projection. Same result: zero contact force from either
  segment class; event never ON.

A diagnostic run (`results/q5_diagnostic.json`; not a gate step)
establishes why, and that the failure is the body's reach, not the
arena: the food geom is compiled at the placed position and paired with
the fly's contact-preset geoms (69 food pairs in the compiled model);
at e = 1 the labrum tip centre sits at z = **0.393 mm** (food top at
0.05 mm), and the true surface-to-surface distance between each labrum
geom and the food geom is **≈ 0.246 mm** — at full extension, under the
registered chain, the labrum stops about a quarter of a millimetre
short of a ground-level food disc. The §7.5(iv) adjustment moves the
food horizontally; the shortfall is vertical, so no placement the rule
allows can close it. Per §7.5, a second failure is a Q5 FAIL: it is
recorded here, and nothing further was adjusted.

### Q6 — NOT RUN; ε_res / θ_off — NOT FROZEN

The gate stopped at Q5 under §7.7, so Q6 did not run and the §4.4
freeze arithmetic was not executed as a gate step. As arithmetic only:
ε_res would be max(0.0035, 1.5 × 10⁻⁶) = 0.0035 rad and θ_off = 3 ×
ε_res ≈ 0.0105 rad, inside the 0.10 rad band guard — recorded here so
the panel can see the numbers, explicitly **not** a freeze output.

### Verdict (§7.7)

**FAIL at Q5.** Q0–Q4 pass under the amended specification — the
compiled-artefact map of Pass 5 is confirmed by pre-registered
prediction — but the body, driven through the registered chain, does
not functionally reach the §4.6 food placement, and §7.4 as narrowed
by Pass 3 states that the gate's acceptance of the body for the feeding
experiment rests on Q5's contact demonstration. No body parameter was
adjusted, no tolerance was loosened, and no fallback was taken. Under
§7.7 the failure returns to the panel by formal amendment; the rescope
option named at the Part 1b decision (primary endpoint becomes MN9 plus
a stated non-feeding measure) is among the panel's options, as is any
amendment to §4.6's food placement that the panel chooses to register
explicitly. Nothing from this run is frozen for Part 5.

### Deviations and implementation notes (third execution)

- `gate_common.labrum_tip_pos` names geoms (`flybody/l_labrum`,
  `flybody/r_labrum`) that resolve to MuJoCo id −1 in this model; Q2's
  sign measurement and all Q5 tip positions used the corrected
  `l_labrum_lower`/`r_labrum_lower` geoms, as in the second execution's
  corrected measurement. The broken helper was not used.
- §4.5 names `get_bodysegment_contact_forces` for the taste event, but
  the labrum is not a registered BodySegment in this artefact (the call
  raises) and that function cannot filter contacts by a single
  non-ground geom. Food-specific forces were therefore computed from
  the MuJoCo contact array (`mj_contactForce` over contacts involving
  the food geom) — the same underlying contact reporting the packaged
  function reads. Labrum geoms: the two `labrum_lower` geoms; front
  tarsi: all geoms on the `lf`/`rf` tarsus1–5 bodies.
- The artefact's geoms collide only through explicit MJCF `pair`
  elements (contype/conaffinity are 0), so the food geom was paired
  with the contact-preset geoms exactly as the ground plane is (same
  `ContactParams`). The food was deliberately **not** added to
  `world.ground_geoms`: that list must stay length 1 or the leg
  ground-contact sensors the settle protocol reads are disabled.
- The adhesion actuators are not registered under
  `ActuatorType.ADHESION` in this artefact's bookkeeping; the two
  labrum adhesion actuators were controlled by direct ctrl writes
  resolved by actuator name, following §4.3's chunk-level rule. Leg
  adhesion ctrl stayed 0 throughout Q5 (the rule engages the labrum
  latch only). In the event, the event never turned ON, so adhesion
  never engaged.
- Q6's ladder and the ε_res/θ_off freeze were not executed (gate
  stopped at Q5); no Q6 calibration curve exists from this run.
- One console diagnostic printed the food geom's `geom_xpos` as
  [0, 0, 0] before the first physics step — a stale pre-forward array;
  the compiled `geom_pos` (recorded in `results/q5_diagnostic.json`)
  is the placed position, and both Q5 attempts stepped thousands of
  steps before judging. Not a gate defect.

### Artefacts (third execution)

- Scripts: `repo/fresh/qualgate/gate_common3.py`, `q0_rerun3.py`,
  `q2_predictions.py`, `q1_rerun3.py`, `q2_rerun3.py`, `q3_rerun3.py`,
  `q4_rerun3.py`, `q5_rerun3.py`, `q5_diagnostic.py` (plus `probe_rerun3.py`,
  `probe2_rerun3.py`, exploration only)
- Results: `repo/fresh/qualgate/results/q0_rerun3.json`,
  `q2_predictions_prereg.json`, `q1_rerun3.json`,
  `q1b_trace_rerun3.npz`, `q2_rerun3.json`, `q3_rerun3.json`,
  `q4_rerun3.json`, `q5_rerun3.json`, `q5_diagnostic.json`,
  `gate_summary_rerun3.json`
- This record: `fresh/FEEDING-BODY-QUALIFICATION.md` (this section
  appended; earlier sections untouched)

---

## Re-run under Amendment Passes 1–3, 5 and 6 (revised), 24 Nov 2026

Fifth execution of the gate: a full re-run from Q0 under the final
specification — Passes 1–3 and 5 as before, plus Pass 6 as revised:
§4.3's extension targets are the ACHIEVABLE extremes θ_ext (the
clamped-map achieved angles at the range-limit commands — rostrum
pitch −0.954 rad, haustellum pitch −1.223 rad, labrum L/R +0.2625 rad;
the feedforward command at e = 1 equals the published range limit
exactly and no clipping occurs in normal operation; the 0.05 rad
safety margin is retired for extension targets), E is §4.4's pinned
definition (excursions of the two pitch joints from the same run's
settled rest), and Q5's arena is §4.6 as revised (food disc on the
fixed pedestal, top at ground + 0.33 mm). No earlier step's result is
carried over; nothing was adjusted to pass; no fallback was taken.
Scripts: `gate_common5.py` (the revised chain) and the `q*_rerun5.py`
step scripts in `repo/fresh/qualgate/`; per-step results under
`results/` with rerun5 naming. Environment as before (FlyGym 2.1.1,
MuJoCo 3.16.0, numpy 2.5.5, body env). Total gate script wall clock
≈ 5.5 min of the 4 h box, including the Q5 diagnostic and re-run
described below.

**Verdict: PASS.** Q0–Q6 all pass and the §4.4 band guard holds
(θ_off = 0.0104 rad < 0.10 rad). The freeze outputs are collected at
the end of this section. One deviation required a gate-script defect
fix and a Q5 re-run inside this execution; it is recorded in full
under Q5 below.

### Q0 — artefact pin and Pass 5 premise checks: PASS

All five pinned files hash-match §7.1 exactly (fruitfly.xml
`66e49595…1a2c`, joints.yaml `b90bf60c…77a`, actuators.yaml
`31feee85…17`, mujoco_globals.yaml `7ea81498…50`, rigging.yaml
`eb852760…37`). Premise checks, read from the compiled artefact and
labelled per joint (`results/q0_rerun5.json`): for all five proboscis
joints qpos_spring = 0.0 and qpos0 = 0.0; jnt_stiffness = 3.0;
gainprm[0] = −biasprm[1] exactly (10 for the three head-group joints,
1 for the two labrum joints — pure position servos); compiled
actuator ctrlranges equal the joints.yaml ranges exactly; compiled
solref (0.001, 1) and solimp (0.9, 0.95, 0.001, 0.5, 2) as recorded
before. The construction call and the neutral pose it receives are
recorded in the artefact (all five proboscis neutral inputs 0.0). The
mesh cache listing (87 files) was recorded before the gate and is
identical after it — no download occurred. Wall clock 6.8 s.

### Predicted steady-state table (pre-registered before Q2)

Computed from the Q0-recorded compiled values under the clamped map
and written to `results/q2_predictions_prereg5.json`, timestamped
2026-11-24T03:27:29Z, before Q2 ran. No point on any joint is
clamp-bound under the corrected map. Predicted achieved ranges:
rostrum [−0.9538, +0.1408], haustellum pitch [−1.2231, +0.5385], yaw
[−0.0672, +0.0672], labrum [−0.0013, +0.2625] rad.

### Q1 — upstream integrity (revised §7.2): PASS

(a) Packaged replay, run fresh: 20,000 steps, all states finite,
thorax travel 28.86 mm — the recorded value, reproduced exactly.
(b) First-party load-and-step of the pinned artefact at ctrl = 0 on
all 102 actuators, 20,000 steps at dt = 1e-4 s, qpos/qvel recorded
every step. h₀ = 2.34 mm; the sanity check ran before stepping and
passed (neutral-pose standing height from qpos0 = 2.34 mm, lowest
geom at z = 0, inside the band [1.17, 3.51] mm). All states finite;
thorax height within [0.5·h₀, 1.5·h₀] at every step (min 1.281, max
2.34, settles at 1.282 mm — sag, not collapse); worst joint velocity
0.2426 of its §7.2 bound; no joint outside its published range at any
step (max excursion −0.0052 rad — every joint stayed inside its
range). The Pass 5 expectation held: no limit-resting is expected at
ctrl = 0 under the compiled spring rests, and none occurred. Wall
clock 25.0 s.

### Q2 — per-joint range sweep against the pre-registered map: PASS

Nine raw targets per joint, 0.5 s holds, steady state = mean over the
final 0.1 s, judged against the pre-registered prediction table.
Maximum steady-state errors: rostrum 0.0035 rad, haustellum pitch
0.0011, yaw 0.0000, labrum L 0.0002, labrum R 0.0001 — all inside the
0.05 rad map-relative tolerance. Coupling ≤ 0.0025 rad; no joint
outside its published range beyond ε at any sample; all states
finite; the empirical map is strictly increasing in target on all
five joints (no clamp-bound points, so no plateau question arises).
Extension signs re-derived: s = −1 for both pitch joints. θ_ext
recorded under the Pass 6 definition (the clamped-map achieved angle
at the range limit in the extension direction): rostrum −0.9538 rad,
haustellum pitch −1.2231 rad. Wall clock 57.2 s.

### Q3 — extend–hold–retract cycles through the revised chain: PASS

Narrowed claim only (Pass 3): model-consistent extension; functional
reach is Q5's question, and nothing here is feeding-capability
evidence. Five cycles through §4.3 as revised (θ_ext = the achievable
extremes above; feedforward from the compiled parameters; ctrl = 0 on
the five DoFs at e = 0). Map-predicted achieved E at e = 1: 2.1728
rad. Every cycle: reach at ramp end 1.0008 × predicted; hold-phase
deviation from the hold mean ≤ 1.8e-6 rad; post-retraction residuals
1.2e-6 to 1.4e-6 rad; no joint outside its published range at any
step; all states finite. **E_max = 2.1746 rad** (mean of the five
hold means), **= 0.7695 of the raw-extremes E**. The raw-extremes E,
by §4.4's pinned formula (range ends measured from the same run's
settled rest), is **2.8258 rad** (artefact value 2.8258492). An
earlier summary figure of 2.8264 rad cannot be reproduced from the
recorded inputs and is superseded by 2.8258 wherever it appears.
Wall clock 48.6 s.

### Q4 — repeatability: PASS

Five fresh Simulation instances, one Q3 cycle each: peak E = 2.1746
rad in every run (range 0.0 rad ≤ 0.05); onset chunk 0 in every run
(onset range 0 ms ≤ 100 ms). As recorded at the third execution, the
zero ranges show determinism/reproducibility of the pinned artefact
under identical commands — not robustness — and are not cited as
variability evidence. Wall clock 61.6 s.

### Q5 — feeding-contact demonstration on the pedestal arena: PASS (after a gate-script defect fix and re-run, recorded in full)

**First run of this execution — FAIL, and the failure was a defect
in the gate script's arena construction, not a measurement of the
body.** With the arena built exactly as in the third execution
(preset pairs only), both attempts failed criterion (i) with zero
labrum–food force, clean settles, full extension (E = 2.1746) and the
full 30-chunk hold — the third execution's outcome repeated on the
pedestal. The diagnostic (`q5_diagnostic5.py`,
`results/q5_diagnostic5.json`; not a gate step) established why:

- The arena was sound in placement: 69 food pairs and 69 pedestal
  pairs compiled; food at the placed position, top at ground +
  0.33 mm.
- At e = 1 the labrum geoms **penetrate** the food geom:
  mj_geomDistance(labrum, food) = −0.032 / −0.034 mm (min over a
  10-chunk dynamic hold −0.033 / −0.035), dynamically and
  kinematically — the registered press bracket (0.022–0.034 mm)
  reached.
- Yet **zero** contacts involving food or pedestal were generated,
  because **none of the 69 pairs involves any proboscis geom**. The
  preset "legs_thorax_abdomen_head" contains no proboscis segment;
  the artefact's six proboscis geoms (rostrum body, rostrum
  bristle-brown, haustellum body, haustellum black, labrum lower
  L/R) were paired with nothing, and every fly geom is
  contype/conaffinity 0, so the labrum was contact-invisible:
  criterion (i) was unmeasurable under that construction, however
  deep the penetration.

The defect is in the gate script (the arena construction is the
gate's, not the artefact's; no fly parameter is involved). It is
also present in the third execution's arena — that record's
diagnostic conclusion "the arena is sound" rested on the pair count
without checking which geoms were paired. The third execution's Q5
verdict is unaffected: its 0.246 mm reach shortfall was real and
decisive, and no contact could have occurred either way. The
first-run artefact of this execution is preserved as
`results/q5_rerun5_defective_construction.json`.

**Fix (arena construction only):** the six proboscis geoms are now
paired with both arena geoms under the same ContactParams — 75 pairs
per arena geom (69 preset + 6 proboscis). No body parameter, gain,
stiffness, spring, range or arena dimension was changed; the
pedestal was not moved or resized. Q5 was then re-run in full.

**Re-run — PASS at the starting offset; the §7.5(iv) adjustment was
not needed and the final offset is 0.6 mm.** Pilot settle: labrum tip
at (0.416, 0.004, 0.714) mm; arena centre (1.016, 0.006) mm. Attempt
settled in 4 chunks with no food contact during warmup. (v) Resting
check: settled e = 0 labrum–food force 0.0 N over 2 chunks. (i) The
§4.5 event turned ON at episode t = 2.0338 s; maximum labrum–food
contact force 25.30 N from the body's own contact reporting (front
tarsi never contacted: 0.0 N throughout — the contact is the
labrum's). (vi) Measured contact-onset fraction: **0.8371**, against
the reach curve's predicted f_c = 0.884 — deviation −0.0469. No
numerical materiality bound is defined in the specification or was
defined for this run; the number is reported here for the panel to
judge. (ii) With adhesion engaged (chunk 7), the contact persisted
1.3985 s at e = 1 ≥ 1.0 s; the hold ran 13 chunks (persistence met,
plus the 3 margin chunks). (iii) On retract the event turned OFF at
t = 2.1051 s and adhesion released at chunk 23, per the rule. (vii)
No pedestal contact with any body part at any step of the attempt
(warmup included); no labrum–pedestal contact either — consistent
with the clearance calibration's 0.022 mm rim clearance. Wall clock
20.5 s (defective-construction run 38.1 s; diagnostic ≈ 47 s).

### Q6 — brain-to-muscle interface, small test case: PASS (first execution of this step)

Synthetic pooled-rate ladder 0 / 30 / 60 / 90 / 120 Hz, 1.5 s per
rate, through §4.2's estimator and §4.3's mapping as revised, driving
rostrum pitch only (the other four DoFs held at their e = 0 chain
state). The input is a seeded synthetic Poisson spike train (seed
20261124, recorded in the artefacts; pooled rate split evenly over
the two MN9 sides — the estimator pools, so the split cannot affect
the pooled path), labelled synthetic in every artefact. r_lo = 5 Hz
(the FIXED §4.3 value); r_hi = 155 Hz is PROVISIONAL (§7.6) and is
replaced by the calibrated r_hi at the Part 5 freeze. Results
(hold-mean E_rostrum over the final 5 chunks of each step):
0 Hz → 0.0000 rad; 30 Hz → 0.1498; 60 Hz → 0.3742; 90 Hz → 0.5295;
120 Hz → 0.8066. (i) Zero-in/zero-out: at 0 Hz e stayed exactly 0 for
all 15 chunks and max |E_rostrum| = 1.2e-6 rad ≤ 0.005. (ii) The step
means are monotone non-decreasing; no feedforward command was
clipped at any chunk (the clamp binds nowhere below e = 1 under the
revised chain, as registered). (iii) Calibration curve saved:
`results/q6_rerun5.json` and
`results/q6_calibration_curve_rerun5.csv`. Wall clock 18.2 s.

### ε_res, θ_off and the band guard

ε_res = max(Q2's map-relative steady-state errors, Q3's
post-retraction residuals) = max(0.00345, 0.0000014) = **0.00345
rad**. θ_off = 3 × ε_res = **0.01036 rad**, strictly below the
0.10 rad onset threshold — **the band guard holds** and θ_off is
frozen at 0.01036 rad.

### Gate verdict: PASS

Q0–Q6 all pass under the specification as amended by Passes 1–3, 5
and 6 (revised), and the band guard holds. The feeding body (the
FlyBody model shipping inside FlyGym 2.1.1, pinned at Q0) is
accepted for the Core-A feeding experiment on the registered
substrate (raised pedestal arena, §4.6 as revised — an engineered
arena parameter, class D; this body as registered cannot contact
ground-level food with the neck held, and feeding is demonstrated on
the raised substrate).

### Freeze outputs (Part 5 inputs)

- Pinned artefact hashes: fruitfly.xml `66e49595…1a2c`, joints.yaml
  `b90bf60c…77a`, actuators.yaml `31feee85…17`, mujoco_globals.yaml
  `7ea81498…50`, rigging.yaml `eb852760…37` (full values in
  `results/q0_rerun5.json`).
- Compiled premise values (per joint, labelled, in
  `results/q0_rerun5.json`): qpos_spring = qpos0 = 0.0, jnt_stiffness
  3.0 for all five proboscis joints; gainprm[0] = −biasprm[1] = 10
  (head group) / 1 (labrum); compiled ctrlranges = joints.yaml
  ranges; solref (0.001, 1), solimp (0.9, 0.95, 0.001, 0.5, 2);
  construction call and neutral pose recorded there. The analytic
  clamped map computed from these values is the frozen object; the
  empirical map below is its audit.
- Prediction table: `results/q2_predictions_prereg5.json`,
  computed 2026-11-24T03:27:29Z, before Q2 ran.
- Extension signs: s = −1 (rostrum pitch), s = −1 (haustellum pitch).
- θ_ext (Pass 6 achievable extremes): rostrum −0.9538 rad,
  haustellum pitch −1.2231 rad, labrum L/R +0.2625 rad; yaw held at
  rest (no θ_ext).
- Empirical map: the nine-point steady states per joint in
  `results/q2_rerun5.json` (max deviation from the analytic map
  0.0035 rad).
- ε_res = 0.00345 rad; θ_off = 0.01036 rad; band guard passes.
- E_max = 2.1746 rad = 0.7695 of the raw-extremes E (2.8258 rad).
- Arena: pedestal r 0.5 mm × h 0.28 mm, food disc r 0.5 mm × h
  0.05 mm, top at ground + 0.33 mm; final horizontal offset 0.6 mm in
  front of the labrum tip's settled ground projection (the §7.5(iv)
  adjustment was not used in the passing run). Arena construction
  includes MJCF pairs for the six proboscis geoms against both arena
  geoms (see the Q5 defect record above) — Part 5's arena must do
  the same or the §4.5 event cannot exist.
- Q5 measured contact-onset fraction 0.8371 (predicted 0.884).
- Q6 calibration curve: `results/q6_rerun5.json`,
  `results/q6_calibration_curve_rerun5.csv`; r_lo = 5 Hz FIXED;
  r_hi = 155 Hz PROVISIONAL, replaced at the Part 5 freeze.

### Deviations and surprises, stated plainly

1. **The Q5 arena pair defect** (above, in full): the first Q5 run
   of this execution failed both attempts with zero contact because
   no proboscis geom was paired with the arena geoms; the labrum
   penetrated the food by 0.032–0.035 mm invisibly. Shown to be a
   gate-script defect (criterion (i) unmeasurable by construction),
   fixed in the arena construction only, Q5 re-run in full and
   passed. The same construction defect was present in the third
   execution's arena; that execution's verdict stands on its real
   reach shortfall. This is the second time a labrum measurement
   channel defect has been found in this gate's scripts (the first
   was the geom-name defect of the second execution) — the pattern
   is that the artefact's proboscis is easy to leave out of
   constructions built from its presets, and Part 5's build should
   treat proboscis coverage as a checklist item.
2. The Q5 diagnostic script itself failed once on a KeyError (the
   yaw DoF has no θ_ext — it is held at rest) before producing its
   results; fixed in the diagnostic only. No gate script or gate
   result was affected.
3. Q6's synthetic input construction (seeded Poisson train, even
   L/R split of the pooled rate) is a choice the specification
   leaves open; it is declared in the step's artefacts and above.
4. The measured Q5 onset fraction (0.8371) sits 0.0469 below the
   reach curve's prediction (0.884). The reach curve is a
   quasi-static kinematic sweep and the Q5 episode is dynamic with
   live contacts; no materiality bound was pre-registered for this
   comparison, so the deviation is reported, not judged.
5. Q4's zero ranges again reflect determinism of the pinned
   artefact, not robustness (standing caution from the panel).

---

**Classification note — 24 Nov 2026 (panel review of execution #5, Reviewers 1 and 3).** Execution #5's first Q5 attempt is classified **INVALID (harness defect)**, not a valid Q5 failure: the arena's contact pairs omitted all six proboscis geoms, so §7.5(i)'s body-reported force was unmeasurable by construction while the labrum geometrically penetrated the food by the registered press. The corrected run used the complete, unchanged Q5 protocol; the correction altered no physical or scientific parameter outside contact-pair eligibility; the original (defective) and corrected arena configurations and their artefacts are both preserved (`q5_rerun5_defective_construction.json`; `q5_rerun5.json`). An invalid attempt does not engage the Pass 6 one-shot clause. **Disclosure for execution #3:** its arena carried the same contact-visibility defect, and its "arena is sound" diagnostic rested on pair count, which is not evidence of contact coverage; execution #3's Q5 verdict stands because its failure was geometric (a 0.246 mm geom-distance shortfall — contact was impossible regardless of pairs) and did not depend on that diagnostic. **Onset residual, kept visible:** predicted f_c = 0.884, measured 0.8371, signed residual −0.047. Reviewer 1's reconciliation: the sensitivity table gives ≈0.04 of f_c per 0.01 mm of surface height, so −0.047 corresponds to ≈0.012 mm — the recorded dynamic-vs-quasi-static protocol difference; a direct dynamic measurement check is being recorded as a calibration. Part 5 uses the measured onset (≈0.84) as the operative threshold.
