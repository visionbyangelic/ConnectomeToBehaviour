# Part 1b — Body-capability audit (body fact-sheet)

**Date:** 23 November 2026. **Object audited:** the *installed* FlyGym 2.1.1 package in the
body environment (`envs/body`, MuJoCo 3.16.0, numpy 2.5.5) — its source, model files and
demo package, read directly, plus headless runs. Not the web. **Why:** Part 1's smoke test
proved only that the stack runs (Reviewer 3's boundary at the Part 1 gate); capability is
established here. Demonstration script + raw output: `fresh/part1b_demos/audit_demos.py`,
`fresh/part1b_demos/audit_demos_output.txt`, `fresh/part1b_demos/halt_latency.py`.

**Shared facts (read from the model files):** units are **mm** throughout; physics
timestep **1e-4 s**, Euler integrator, gravity −9810 mm/s²
(`assets/model/neuromechfly/mujoco_globals.yaml`, same timestep in FlyBody's globals).
Two body models ship in the package and share one composition API (`BaseFly`):
**NeuroMechFly** (default; micro-CT model) and **FlyBody** (Vaxenburg et al., *Nature*
2025, TuragaLab whole-body model; upstream labels its FlyGym support "experimental").

---

## 1. Actuators / actions

**Legs — SUPPORTED.** The shipped locomotion configuration
(`flygym_demo/complex_terrain/common.py::make_locomotion_fly`) builds a legs-only
skeleton (`JointPreset.LEGS_ONLY`, 66 joint DoFs) with **42 position actuators**
(`ActuatedDOFPreset.LEGS_ACTIVE_ONLY`: 7 active DoFs per leg — coxa 3, trochanterfemur 2,
tibia 1, tarsus1 1; tarsus2–5 are passive spring joints) plus **6 leg adhesion actuators**
(tarsus5 grip, ctrl 0–1). Demo A (run): compiled model nu=48, nq=73. ✔

**Steering / descending-level command — SUPPORTED.** Beyond raw joint targets, the demo
package ships controllers that accept a low-dimensional descending signal (see §2).
There is no velocity-actuator locomotion config shipped; position targets are the
actuation currency.

**Proboscis / feeding actuation — SPLIT VERDICT (the question the web could not settle,
RESEARCH-CHECK F12):**
- **NeuroMechFly: NOT SUPPORTED as shipped.** The proboscis segments exist
  (`anatomy.py`: `PROBOSCIS_LINKS = [rostrum, haustellum]`, with meshes), and the
  composition API *can* attach generic position actuators to them — Demo B (run): an
  `ALL_BIOLOGICAL` skeleton + `ActuatedDOFPreset.ALL` yields 126 actuated DoFs including
  6 proboscis DoFs (rostrum pitch/roll/yaw, haustellum pitch/roll/yaw). **But** nothing
  calibrated ships with them: no joint ranges, no actuator gains, no neutral-pose values
  (the neutral pose file specifies leg joints only), and no example anywhere in the
  package actuates them. Driving a proboscis on NeuroMechFly would mean inventing the
  mechanism's parameters — exactly what this audit exists to prevent.
- **FlyBody: SUPPORTED.** Proboscis actuation is part of the published model itself.
  Its own config files define it: `assets/model/flybody/actuators.yaml` groups "head"
  (`c_head-c_rostrum-pitch`, `c_rostrum-c_haustellum-pitch`, `c_rostrum-c_haustellum-yaw`,
  neck `c_thorax-c_head-{pitch,roll,yaw}`) and "antenna-labrum"
  (`c_haustellum-{l,r}_labrum-pitch`, antennae); `joints.yaml` gives calibrated ranges —
  rostrum pitch [−1.24, 0.183] rad with springref 0.8 (retracted rest), haustellum pitch
  [−1.59, 0.7], labrum pitch [~0, 1.05]. Demo C (run): `ALL_BIOLOGICAL` FlyBody actuates
  exactly the 5 proboscis DoFs those files describe (rostrum pitch; haustellum pitch+yaw;
  labrum pitch ×2) among 102 actuated DoFs, and the model compiles and steps here
  (meshes are lazy-downloaded once from S3 by the package; that download succeeded and is
  cached). FlyBody also adds **labrum adhesion actuators** by default
  (`FlyBody.add_leg_adhesion(add_labrum=True)`) — a physical latch modelling labellar
  grip on food.

## 2. Walk / halt

**SUPPORTED — demonstrated.** The packaged descending-drive stack is:
`HybridTurningController.step(descending_signal, obs)` (`flygym_demo/complex_terrain/`)
→ a 6-oscillator CPG network (`CPGNetwork`, tripod/tetrapod/wave biases) whose amplitudes
are set by the descending signal → `PreprogrammedSteps` maps CPG phase/amplitude to the
42 leg position targets + adhesion timing → `Simulation.set_actuator_inputs`.
The descending signal is a **2-vector (left, right)**: magnitude sets CPG amplitude per
side, sign flips that side's stepping direction (forward/backward) — a descending-neuron-
style interface by design. A Walknet-style rule-based controller (local sensory rules,
no descending input) also ships as an alternative coordinator.

Demo A (run, flat ground): descending [1, 1] for 0.3 s → thorax travel **3.21 mm**
(~10.7 mm/s). Signal to [0, 0] → travel decays 0.537 → 0.060 → 0.006 mm per 0.1 s bin
(`halt_latency.py`): the fly is effectively stopped **within ~0.2 s** of the signal
zeroing (first-bin travel is CPG amplitude decay + momentum, not continued stepping).
Halt is real, and halt latency is a measurable quantity, as Core-B assumes.

**What the decoder must output (Part 4):** either (a) the 2-D descending signal into the
packaged turning controller — small, DN-like, but then a named part of the behaviour is
generated by an upstream controller, which the provenance ledger must record; or (b) the
42 leg position targets (+ 6 adhesion states) per control step directly — no upstream
controller in the loop, a much larger decoding problem. The audit establishes both
interfaces exist; choosing between them is a Part 4 design decision, not settled here.

## 3. Grooming

**NOT SUPPORTED as a packaged capability.** The word "groom" appears nowhere in
`flygym` or `flygym_demo`: no grooming controller, no grooming trajectory, no
preprogrammed antennal-cleaning step. Joint-level prerequisites do exist — front legs
carry the same 7 actuated DoFs as all legs, the head/neck is actuated (3 DoFs), and the
antennae are actuated (NeuroMechFly: 9 DoFs per antenna chain — pedicel, funiculus,
arista × pitch/roll/yaw, Demo B; FlyBody: 3 DoFs per antenna, Demo C) — but nothing in
the installed package demonstrates front-leg-to-antenna reachability or a coordinated
cleaning movement, and this audit ran no reachability study. **Per the plan's own rule
(grooming is dropped rather than faked if the audit fails it): body-level grooming does
not pass this audit and stays out of Core-B.** RQ-C6's neural-level question is
unaffected. This was pre-decided as optional, so it is not a scope change.

## 4. Sensors / observations

**SUPPORTED (proprioception + contact + vision). PARTIALLY SUPPORTED overall — no
chemical sensing exists.**
- **Joint proprioception:** `Simulation.get_joint_angles` / `get_joint_velocities` for
  every joint DoF; body positions/rotations; actuator forces; site positions.
- **Ground contact:** one MuJoCo contact sensor per leg (6 total; Demo A lists them:
  `ground_contact_{leg}_leg`), each reporting found/force/torque/position/normal/tangent
  for the whole-leg subtree (`Simulation.get_ground_contact_info`). Finer grain is
  available from `get_bodysegment_contact_forces` for **any** segment — individual
  tarsus segments, head, haustellum, labrum — which is what tarsal-contact and
  head/food-contact events would be built from.
- **Vision:** two eye cameras (`BaseFly.add_vision`) with ommatidia readouts via
  `flygym.vision.Retina` (`Simulation.get_ommatidia_readouts`; NMF ships
  `compound_eye.npz`). (FlyBody has no separate eye segments — eyes are part of its head.)
- **Gustatory / olfactory: NOT SUPPORTED.** No taste or odor sensor, channel, or hook
  exists anywhere in the installed package (full-text search: zero hits). The feeding
  loop's "taste" feedback therefore cannot be sensed by the body; it must be
  *constructed* — from labrum/tarsus contact events against a food geom (above) joined
  to the scripted stimulus definitions the encoder side already specifies (Part 4
  sensory-pathway specs). Contact is real; chemistry is a defined input event, and the
  documents must keep saying so.

## 5. Interface shape

External (Brian2-side) signals enter through `Simulation` between physics steps:
`set_actuator_inputs(fly_name, actuator_type, array)` writes `mj_data.ctrl` directly;
`set_leg_adhesion_states` and `set_tendon_actuator_inputs` do the same for adhesion and
FlyBody's abdomen tendons. Control may be refreshed every physics step (1e-4 s) or held
across steps — the cadence is the caller's choice, which is what a chunked brain↔body
loop (Parts 2b/5) needs. Observations are pulled from the same object after stepping
(§4). Packaged examples demonstrating descending-drive control live in
`flygym_demo/complex_terrain/` (CPG, hybrid, turning and rule-based controllers, plus
recorded single-step assets for both NeuroMechFly and FlyBody —
`FlyBodyPreprogrammedSteps`); `flygym_demo/muscle_imitation/` is a FlyBody
mocap-imitation environment; `flygym_demo/benchmark/` shows raw target-angle replay.

---

## Verdict summary

| Question | Verdict |
|---|---|
| Leg actuation / action space | **SUPPORTED** — 42 position actuators + 6 adhesion (shipped config) |
| Steering / descending-level command | **SUPPORTED** — 2-D descending signal → CPG → joint targets |
| Proboscis actuation, NeuroMechFly | **NOT SUPPORTED** as shipped (segments + generic API only; no calibrated parameters) |
| Proboscis actuation, FlyBody | **SUPPORTED** — 5 calibrated DoFs + labrum adhesion, from the published model |
| Walk / halt under descending drive | **SUPPORTED** — demonstrated; halt effective within ~0.2 s of zero signal |
| Antennal grooming (body level) | **NOT SUPPORTED** — no controller/trajectory/reachability evidence; stays out of Core-B |
| Sensors for the closed loop | **PARTIALLY SUPPORTED** — proprioception, per-leg + per-segment contact, vision ✔; taste/smell ✘ (must be constructed from contact events) |

## ⚠ SCOPE FLAG — HARD-gate escalation candidate (not resolved here)

Plan §5.2 defines the honest body-level feeding metric as proboscis-extension
angle/latency/duration **if** an actuated proboscis exists in the installed body,
otherwise a named proxy (decoder-command duration + head/food contact). This audit
settles the conditional: an actuated proboscis **does** exist in the installed package —
but in **FlyBody**, while the plan's body route names NeuroMechFly (the default model,
and the old build's body). Core-A therefore has a body-model decision the plan did not
pre-make: **(i)** adopt FlyBody (at least for feeding) and take the real
proboscis-extension metric; or **(ii)** stay on NeuroMechFly and take the §5.2 named
proxy. That is a scope-relevant choice, so per §0.2(c) Part 1b escalates to a **HARD
gate** on this point: full panel + Angelic's decision. Facts that bear on it, recorded
not argued: both models share the `BaseFly` API; FlyBody compiles and runs in this
environment (Demo C); FlyBody locomotion has its own preprogrammed-steps class;
upstream labels FlyBody support in FlyGym "experimental"; FlyBody's meshes are an S3
lazy-download (now cached here). **Kill criterion K2 is not triggered**: an honest
feeding metric exists on both routes (real extension metric, or the pre-named proxy).

---

**Correction note (24 Nov 2026).** This audit describes `flygym_demo/muscle_imitation/` as a FlyBody environment (§5). That is wrong, and I am correcting the record rather than the text above: the demo's own package documentation states its body model is FlyMimic's musculoskeletal MJCF, not FlyBody, and its environment module requires gymnasium, which is not in the pinned body environment. The error was carried from here into the Part 4 specifications (§7.2) unchecked, and the first feeding-body qualification-gate execution failed at Q1 for exactly that reason — a specification-premise failure, not a body failure (record: `FEEDING-BODY-QUALIFICATION.md`). The specs' fix is Amendment Pass 2. Everything else in this audit was verified against the installed package and stands.
