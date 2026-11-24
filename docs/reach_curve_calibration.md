# Reach-curve calibration — 24 Nov 2026

Pre-gate calibration for Reviewer 1's Pass 6 condition 1. **Not a gate
step**: kinematics only, no food geom, no verdicts. Script:
`repo/fresh/qualgate/reach_curve.py`; machine-readable results:
`repo/fresh/qualgate/results/reach_curve.json` (full 41-point curve) and
`reach_curve.csv`.

## Method

Demo C FlyBody construction (as in Q3; adhesion actuators present, never
commanded), settled per §2.3 under zero command (settled in the recorded
chunks; θ_rest below). The extension command e was then swept 0 → 1 in
41 equal steps (0.025 apart) through the §4.3 chain exactly as
registered — feedforward inverse from the compiled artefact's parameters
(kp 10/1, ks 3, ref 0; Amendment Pass 5), yaw and neck held at rest, at
e = 0 ctrl = 0 on the five proboscis DoFs. Signs and θ_ext are this
gate's Q2 outputs (s = −1 both pitch joints; θ_ext rostrum −1.19 rad,
haustellum pitch −1.54 rad; labrum full-open target 1.00 rad). Each e
was held 0.4 s and the final state recorded: the five achieved joint
angles, E (§4.4 two-segment pitch sum), and the labrum surface height,
by **two methods, because they differ materially**:

- **centre − rbound (as prescribed for this calibration):** per labrum
  geom (`l_labrum_lower`, `r_labrum_lower`), `geom_xpos.z −
  geom_rbound`; the smaller of the two.
- **true surface (execution #3's diagnostic method):**
  `mj_geomDistance` from each labrum geom to the ground plane geom —
  the actual lowest-surface height above ground; the smaller of the two.

**The two methods do not measure the same thing.** `geom_rbound` is
0.1822 mm — the bounding-*sphere* radius of an elongated geom that in
this pose extends only ≈0.097 mm below its centre. Centre − rbound is
therefore a conservative lower bound on the surface height, ≈0.086 mm
below the true surface. It is recorded as prescribed, but it is **not**
the lowest surface point, and the two series give different f_c values;
they must not be mixed.

## Numbers

θ_rest (rad): rostrum −0.00328, haustellum pitch −0.00087, yaw ≈ 0,
labrum L −0.00004, R −0.00001.

**E_max = 2.1746 rad** (E at e = 1) — identical to Q3's measured hold
mean (2.17459 rad).

Achieved angles at e = 1 (rad), against the §4.3 clamped map's
prediction: rostrum **−0.9550** (map −0.9538), haustellum pitch
**−1.2237** (map −1.2231), yaw 0, labrum L **0.2623** / R **0.2624**
(map 0.2625). The chain achieves exactly what the map says it can.

**Saturation (dead zone), grid resolution 0.025, 1e-4 rad band:**
rostrum achieved angle stops changing from **e = 0.825**, haustellum
pitch from **e = 0.800**. (Analytic clip onsets are e ≈ 0.801 / 0.794;
the rostrum's grid point lands one step later because its pre-clip
angle still sits 0.0011 rad from the final value.) This confirms
Reviewer 1's dead zone: above e ≈ 0.80 the pitch joints are at their
ctrl clip and E is flat (E/E_max = 0.9995 already at e = 0.8).

Surface height at rest (e = 0): centre − rbound **0.5319 mm**; true
surface **0.6115 mm**.

### Reach at e = 1 and contact-onset fractions f_c(T)

f_c(T) = the smallest achieved fraction E/E_max at which the surface
height falls to ≤ T (linear interpolation between sweep points).

| Quantity | centre − rbound | true surface |
|---|---|---|
| Reach R at e = 1 | 0.2226 mm | **0.3083 mm** |
| f_c(0.330) | 0.5675 | **0.8836** |
| f_c(0.346) | 0.5171 | **0.8162** |
| f_c(0.296) | 0.6818 | never (surface stays above) |
| f_c(0.306) | 0.6471 | never |
| f_c(0.316) | 0.6133 | 0.9480 |
| f_c(0.326) | 0.5805 | 0.9014 |
| f_c(0.336) | 0.5484 | 0.8577 |
| f_c(0.346) | 0.5171 | 0.8162 |
| T at onset fraction 0.60 | 0.3200 mm | 0.4054 mm |
| T at onset fraction 0.80 | 0.2644 mm | 0.3501 mm |
| T at onset fraction 0.95 | 0.2299 mm | 0.3156 mm |

## Reconciliation with execution #3's ≈0.296 mm, stated plainly

Execution #3's diagnostic measured `mj_geomDistance` from the labrum to
the *food cylinder* (0.2455 mm) and read it as a vertical gap above the
food top (0.05 mm), implying a surface height of ≈0.296 mm. In that
run the labrum geom centres sat at z = 0.3930 mm; in this sweep they
sit at 0.4059 mm — the poses differ by ≈0.013 mm (fast chunked ramp
with a 0.5 s hold vs this slow 41-step sweep). Read consistently, the
two runs bracket the true e = 1 surface height at **≈0.296–0.308 mm**.
The centre − rbound figure (0.2226 mm) is not part of that bracket; it
is a bounding-sphere artefact, not a surface measurement.

Consequence for the Pass 6 numbers, recorded without deciding them:
under the true-surface series the labrum never reaches a 0.296 or
0.306 mm food top at any e; at the panel's T = 0.330 mm the onset
fraction is f_c = 0.884 (inside Reviewer 1's 0.95 bound) and the press
at e = 1 is 0.330 − 0.3083 ≈ 0.022 mm, not the 0.034 mm computed from
the 0.296 figure.

---

## Clearance check and E definitions, 24 Nov 2026

Two further pre-gate calibrations, for Reviewer 1's Pass 6 confirmation
conditions 2 and 3. **Not gate steps.** Script:
`repo/fresh/qualgate/clearance_check.py`; machine-readable results:
`repo/fresh/qualgate/results/clearance_check.json`.

### Calibration 1 — whole-body pedestal clearance

**Method.** The §4.6 arena as amended by Pass 6: flat ground, pedestal
cylinder (radius 0.5 mm, height 0.28 mm) with the food disc on top
(radius 0.5 mm, height 0.05 mm, top surface at ground + 0.33 mm),
pedestal centre placed from a pilot settle exactly as Q5 constructs it
— 0.6 mm in front of the labrum tip's settled ground projection, along
the ground-projected head→tip direction. The pedestal and food geoms
carry **no contact pairs** (verified: no compiled pair involves them)
and contype/conaffinity 0; during the whole sweep **zero** contacts
involved them — nothing stepped against them, so every number below is
kinematics only. Poses were set by stepping the §4.3 chain **as
revised by Pass 6** (θ_ext = achievable extremes: rostrum −0.954,
haustellum pitch −1.223, labrum +0.2625; feedforward from the compiled
parameters) through e = 0 → 1 in 21 steps, 0.4 s hold per point as in
the reach curve, and clearances read with `mj_geomDistance` from the
pedestal geom and from the food-disc geom to **every non-labrum fly
geom**: all 83 compiled geoms except `l_labrum_lower` /
`r_labrum_lower`, the ground plane and the two arena geoms.
Pre-registered expectation: every non-labrum clearance > 0.02 mm,
across the sweep and at rest.

**Result: the expectation holds everywhere.** Global minimum clearance
**0.097 mm**; no geom at or below 0.02 mm, at any e or at rest.

Smallest five vs the **pedestal** (min over the sweep; e at min; value
at rest):

| Geom | Min (mm) | at e | At rest (mm) |
|---|---|---|---|
| c_haustellum_body | 0.147 | 1.0 | 0.477 |
| c_haustellum_black | 0.174 | 1.0 | 0.507 |
| c_rostrum_bristle-brown | 0.285 | 0.6 | 0.341 |
| c_rostrum_body | 0.309 | 1.0 | 0.393 |
| lf_tarsus2_body | 0.384 | 1.0 | 0.406 |

Smallest five vs the **food disc**:

| Geom | Min (mm) | at e | At rest (mm) |
|---|---|---|---|
| c_haustellum_body | **0.097** | 1.0 | 0.429 |
| c_haustellum_black | 0.124 | 1.0 | 0.460 |
| c_rostrum_bristle-brown | 0.235 | 0.6 | 0.292 |
| c_rostrum_body | 0.259 | 1.0 | 0.344 |
| lf_tarsus1_body | 0.380 | 1.0 | 0.399 |

**For information — the labrum itself.** Minimum distance from the
labrum geoms to the pedestal geom: 0.022 mm (right) / 0.024 mm
(left), both at e = 1 — the labrum passes close by the pedestal's top
rim as it descends but does not touch it. Minimum distance to the food
disc: **−0.026 mm (left) / −0.028 mm (right)** at e = 1 — negative,
i.e. in this kinematic pose the labrum surface presses ≈0.026–0.028 mm
into the disc's top, inside the registered press bracket (0.022–0.034
mm across the reach bracket). At rest the labrum sits 0.30 mm clear of
the disc.

**Stated plainly:** the closest non-labrum part is the **haustellum**
(the segment carrying the labrum), not the front tarsi — the tarsi
never come closer than 0.38 mm. The haustellum's 0.097 mm clearance at
full extension is the tightest point of the whole configuration and is
still ~5× the 0.02 mm margin, so Q5(vii) (any non-labrum pedestal
contact fails) is not threatened by the geometry at the registered
placement. Nothing here burns the gate's one shot.

### Calibration 2 — E definitions, pinned exactly

Recomputed from the compiled model with the gate code's own
`extension_E` (gate_common3), through the revised chain, on the plain
Demo C construction. §4.4's definition, verbatim in operational terms:

**E = s_ros·(θ_ros − θ_rest,ros) + s_haus·(θ_haus − θ_rest,haus)**,
s = −1 for both pitch joints, where θ are the **joint angles** returned
by `get_joint_angles` (the actuated joints' qpos coordinates) and
θ_rest is the **same run's settled angle under zero command**. E sums
joint-angle *excursions from the settled rest pose*. It is not a sum of
segment orientations, and it is not measured from qpos zero.

**(a) E at e = 1 and the 0.0041 gap.** Through the revised chain
(0.4 s hold): achieved rostrum −0.9550 rad, haustellum pitch −1.2236
rad (commands at e = 1: rostrum ctrl −1.24, clipped from −1.2402;
haustellum pitch ctrl −1.5899, 0.0001 inside the −1.59 limit; labrum
ctrl 1.05, the limit exactly; achieved labrum 0.2623/0.2624). E =
**2.1745 rad** (reach curve: 2.1746; Q3 hold mean: 2.1746 — one number
at the precision any run repeats it). The naive joint-angle sum
|−0.9550| + |−1.2237| = **2.1787**. The difference is **exactly the
rest offset**: E subtracts θ_rest, and the settled rests are
θ_rest,ros = −0.00328 and θ_rest,haus = −0.00087 (the settled
proboscis sits a hair into the extension direction from qpos zero), so
E = 2.1787 − (0.00328 + 0.00087) = 2.1787 − 0.00415 = 2.1745. Verified
numerically in this run: naive sum − E = 0.004151 = −(θ_rest,ros +
θ_rest,haus) to all printed digits. No segment-orientation term, no
neck contribution, no rounding — the two series differ by the rest
reference alone.

**(b) Raw-extremes E.** Q3's code (q3_rerun3.py) defines it as
**Σ_j s_j·(range_end_j − θ_rest,j)** over the two pitch joints — the
published range ends in the extension direction (rostrum −1.24,
haustellum pitch −1.59) measured **from the same run's settled rest
pose**, not from zero. With the recorded rests this gives
(1.24 − 0.00328) + (1.59 − 0.00087) in magnitude terms = **2.8258
rad**, reproducing Q3's artefact value 2.8258492 exactly. The naive
1.24 + 1.59 = **2.83** measures the same ends from qpos zero and
overstates by the identical 0.00415 rest offset as in (a) — one
systematic difference explains both gaps. The gate summary's
**2.8264** cannot be reproduced from Q3's recorded inputs (it sits
0.0006 rad, 0.02%, above the artefact value and is inconsistent with
the summary's own fraction at the fourth decimal); the artefact's
2.8258, recomputed here from the definition, is the value of record.
E_max as a fraction of the raw extremes is therefore 2.1745 / 2.8258 =
0.7695.

---

## Dynamic-onset quantification check, 24 Nov 2026

Reviewer 3's condition on qualification execution #5. **Not a gate
step.** Scripts: `repo/fresh/qualgate/onset_check.py` (Runs A–C) and
`onset_diag.py` (the isolating diagnostic); results:
`repo/fresh/qualgate/results/onset_check.json`.

**Why.** Execution #5's Q5 measured the contact-onset fraction as
0.8371 against the reach curve's quasi-static prediction f_c = 0.884
(residual −0.047). The explanation on record was a protocol
difference: the reach curve swept e in 41 slow 0.4 s-hold steps,
while Q5 ramped e in five 100 ms chunks, and execution #3's fast ramp
had read the e = 1 surface ≈0.012 mm lower than the sweep. This check
measures that claim directly, in the reach curve's own convention
(labrum lowest surface by `mj_geomDistance` to the ground plane;
E as excursions from the episode's settled rest, against Q3's
E_max = 2.1746 rad).

**Run A — the Q5 rebuild** (arena with proboscis pairs, pedestal
T = 0.33, offset 0.6 mm, §2.3 settle, revised chain, Q5's chunk
profile; adhesion off — it engages only after first contact, so it
cannot affect the onset). The run **replicates Q5's onset exactly**:
first labrum–food force at step **6024**, at E/E_max = **0.8371** —
Q5's own step and fraction. The descending surface lands on the disc:
it comes within 0.001 mm of the disc-top level at E/E_max = 0.8366
and rests at a plane height of 0.3309 mm (it does not pass through;
the arena's e = 1 height is disc-supported).

**The four numbers.** At E/E_max = 0.8371: the dynamic surface
height is **0.3309 mm** — the disc top, within 0.001. The
quasi-static reach curve's surface at the same fraction is
**0.3409 mm**. Difference: **−0.0101 mm** (dynamic lower). By the
bands stated before the check ran (dynamic within ~0.005 of 0.33;
difference ≈0.010–0.014), **the explanation holds quantitatively** —
the difference sits at the lower edge of its band.

**What the mechanism actually is — the diagnostic.** Five e = 1
cases in the plain construction (single 0.4 s hold, 41-step sweep,
Q5-style chunked ramp; old chain and revised chain) end with
*identical* joint angles (rostrum −0.9550, haustellum pitch −1.2237,
labrum 0.2623/0.2624; E = 2.1746) but two different surface heights:

| Protocol to e = 1 | z_true (mm) | Thorax z (mm) |
|---|---|---|
| Single hold, either chain | 0.2949 | 1.2815 |
| Chunked ramp (Q5-style), old chain | 0.2950 | 1.2815 |
| Single hold + 2 s more | 0.2967 | 1.2825 |
| 41-step sweep, old chain | 0.3083 | 1.2886 |
| 41-step sweep, revised chain | 0.3084 | 1.2886 |

So it is **not the chain** (old and revised agree to <0.0002 mm in
every paired case) and **not ramp speed** (chunked ramp = single
hold). The graded sweep's *trajectory* lifts the whole body — thorax
+0.0071 mm, labrum surface +0.0134 mm at e = 1 — relative to any
direct application of the extension: passing slowly through every
intermediate extension lets the body re-settle into a higher posture
than the one it keeps when extension is applied at once (whose
thorax height, 1.2815 mm, is the ordinary resting settle of Q1(b)).
The reach curve's f_c = 0.884 inherits that lift, and Q5's onset
sits on the direct-protocol curve. The reviewers' analytic
reconciliation had the sign and magnitude right; its "dynamic vs
quasi-static" framing is now sharpened to "sweep trajectory vs
direct application".

**Bracket, restated.** The free reach at e = 1 is **0.2949–0.2968
mm** under every direct protocol (execution #3's ≈0.296 among them)
and **0.3083–0.3084 mm** under the 41-step sweep. The [0.296, 0.308]
bracket recorded earlier is therefore a protocol split, not a
measurement uncertainty. The gate's operative onset remains the
measured one: **0.8371**, under the revised chain and the Q5
protocol, now replicated step-for-step.
