"""Dynamic-onset quantification check (calibration, NOT a gate step),
24 Nov 2026 -- Reviewer 3's condition on qualification execution #5.

Background. Execution #5's Q5 measured the contact-onset fraction --
achieved E/E_max at first labrum-food contact -- as 0.8371, against
the SS4.6 reach curve's quasi-static prediction f_c = 0.884 (residual
-0.047). The explanation on record is that the two numbers come from
different protocols: the reach curve swept e in 41 slow steps with
0.4 s holds (quasi-static poses), while Q5 ramped e in five 100 ms
chunks (a dynamic pose that sits lower -- execution #3's fast-ramp
diagnostic read the e = 1 surface at ~0.296 mm against the sweep's
0.3083 mm, a ~0.012 mm protocol bracket). Reviewers 1 and 2 reconciled
the residual analytically (~0.04 of f_c per 0.01 mm of surface height
from the sensitivity table <-> the ~0.012 mm bracket). This check
measures the claim directly instead of inferring it.

Method. Three runs, all with the revised Pass 6 chain, all recording
E (pitch-joint qpos excursions from the episode's own settled rest,
SS4.4 -- the E_now() Q5 used), E/E_max against Q3's E_max hold mean
(the reference Q5's 0.8371 was computed with), and z_true, the
labrum's lowest surface height by mj_geomDistance from each labrum
geom to the ground PLANE geom (the reach curve's governing
convention; NOT centre - rbound).

- Run A (the Q5 rebuild): q5_rerun5.build_arena -- pinned FlyBody,
  SS4.6 pedestal + food WITH the proboscis pairs, disc top at ground
  + 0.33 mm, centre 0.6 mm in front of the labrum tip's settled
  ground projection; settle per SS2.3; then Q5's own chunk profile
  (2 resting chunks at e = 0, 5 ramp chunks at e = 0.2 ... 1.0, hold
  chunks at e = 1), recording every physics step. Also recorded: the
  labrum->food-disc geomDistance and the labrum-food contact force,
  so the run replicates Q5's onset measurement itself. Adhesion is
  left off: in Q5 it engages only after the taste event turns ON,
  which is after first contact, so it cannot influence the onset.
  NOTE: in this arena the descending labrum LANDS on the disc -- at
  e = 1 its plane height is the disc-supported height (~0.331), not
  a free-descent reach.
- Run B (free dynamic): the plain Demo C construction (no arena),
  same chunk profile. The labrum descends freely; this gives the
  dynamic protocol's own (E, z) trace and its free dynamic R.
- Run C (same-chain quasi-static): the plain construction, e held
  0.4 s at five points spanning the onset region. The reach curve
  was swept under the pre-Pass-6 chain (identical achieved extremes
  at e = 1, but the labrum saturates earlier along that sweep), so
  this run gives a quasi-static comparison under the SAME chain as
  the dynamic runs -- the protocol effect with the chain held fixed.

Prescribed comparisons (the four numbers reported):
1. dynamic crossing fraction -- in Run A, E/E_max at first
   labrum-food contact (force > 0) and at the surface's landing on
   the disc-top level;
2. dynamic surface height at E/E_max = 0.8371 (Run A);
3. quasi-static surface height at E/E_max = 0.8371, interpolated
   from results/reach_curve.json (z_true series);
4. their difference. The explanation holds quantitatively if (2) is
   ~0.33 mm (within ~0.005) and (4) is ~0.010-0.014 mm.
Plus the dynamic R values for the bracket (Runs B and C; Run A's
e = 1 height is disc-supported and is labelled as such).
"""

import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (CHUNK_STEPS, PITCH_JOINTS, PROBOSCIS, build_sim,  # noqa: E402
                         dof_index, settle)
from gate_common3 import (FRONT_TARSUS_BODIES, LABRUM_GEOM_NAMES, RESULTS,  # noqa: E402
                          compiled_params, extension_E, food_contact_forces,
                          geom_ids_for_bodies, labrum_tip_pos)
from gate_common5 import chain_ctrl_rev, theta_ext_from_params  # noqa: E402
from q5_rerun5 import build_arena  # noqa: E402

T_DISC = 0.33                # food disc top surface, ground + 0.33 mm (SS4.6)
Q5_ONSET_FRACTION = 0.8370970470740771   # execution #5, q5_rerun5.json
Q5_ONSET_STEP = 6024                     # first labrum contact step, ditto
HOLD_CHUNKS = 15


def first_passage_value(xs, ys, x_level):
    """y interpolated where x first rises through x_level."""
    for i in range(1, len(xs)):
        if xs[i - 1] < x_level <= xs[i]:
            if xs[i] == xs[i - 1]:
                return float(ys[i])
            return float(ys[i - 1] + (x_level - xs[i - 1])
                         * (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1]))
    return None


def first_crossing(xs, ys, level):
    """First x where y falls to <= level, linear between samples."""
    for i in range(1, len(xs)):
        if ys[i - 1] > level >= ys[i]:
            if ys[i] == ys[i - 1]:
                return float(xs[i])
            return float(xs[i - 1] + (level - ys[i - 1])
                         * (xs[i] - xs[i - 1]) / (ys[i] - ys[i - 1]))
    return None


class Recorder:
    """Per-physics-step E / surface-height recording for one episode."""

    def __init__(self, sim, fly, rest, signs, e_max_ref, food_gid=None):
        self.sim, self.fly = sim, fly
        self.m, self.d = sim.mj_model, sim.mj_data
        self.rest, self.signs = rest, signs
        self.e_max_ref = e_max_ref
        params = compiled_params(sim)
        self.qadr = {j: int(self.m.jnt_qposadr[params[j]["joint_id"]])
                     for j in PITCH_JOINTS}
        self.labrum_gids = [mj.mj_name2id(self.m, mj.mjtObj.mjOBJ_GEOM, n)
                            for n in LABRUM_GEOM_NAMES]
        planes = [g for g in range(self.m.ngeom)
                  if self.m.geom_type[g] == mj.mjtGeom.mjGEOM_PLANE]
        assert len(planes) == 1, planes
        self.plane_gid = planes[0]
        self.food_gid = food_gid
        self.tarsus_gids = (geom_ids_for_bodies(sim, FRONT_TARSUS_BODIES)
                            if food_gid is not None else set())
        self.rows = []

    def z_plane(self):
        return float(min(mj.mj_geomDistance(self.m, self.d, gid,
                                            self.plane_gid, 10.0, None)
                         for gid in self.labrum_gids))

    def z_disc(self):
        return float(min(mj.mj_geomDistance(self.m, self.d, gid,
                                            self.food_gid, 10.0, None)
                         for gid in self.labrum_gids))

    def E_now(self):
        by = {j: float(self.d.qpos[self.qadr[j]]) for j in PITCH_JOINTS}
        return extension_E(by, self.rest, self.signs)

    def record(self, step_no, phase, e_cmd):
        E = self.E_now()
        row = {"step": step_no, "phase": phase, "e_cmd": e_cmd,
               "E_rad": E, "E_fraction": E / self.e_max_ref,
               "z_plane_mm": self.z_plane()}
        if self.food_gid is not None:
            lf, _ = food_contact_forces(self.sim, self.food_gid,
                                        set(self.labrum_gids),
                                        self.tarsus_gids)
            row["z_disc_mm"] = self.z_disc()
            row["labrum_force_N"] = lf
        self.rows.append(row)


def run_profile(sim, fly, rec, theta_ext, signs, e_max_ref):
    """Q5's chunk profile with per-step recording (resting, ramp, hold)."""
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    step_no = 0

    def run_chunk(e, phase):
        nonlocal step_no
        ctrl = chain_ctrl_rev(np.zeros(len(order)), idx, params, e,
                              rec.rest, theta_ext)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(CHUNK_STEPS):
            sim.step()
            step_no += 1
            rec.record(step_no, phase, float(e))

    for _ in range(2):                       # Q5 resting check, e = 0
        run_chunk(0.0, "resting_check")
    for i in range(5):                       # Q5 ramp, e = 0.2 ... 1.0
        run_chunk((i + 1) / 5, "ramp")
    for _ in range(HOLD_CHUNKS):             # hold at e = 1
        run_chunk(1.0, "hold")
    return rec.rows


def main():
    t0 = time.time()
    q5 = json.loads((RESULTS / "q5_rerun5.json").read_text())
    a5 = q5["attempts"][-1]
    e_max_ref = float(a5["E_max_reference_rad"])
    signs = {j: -1 for j in PITCH_JOINTS}

    # ---------- Run A: the Q5 rebuild --------------------------------
    # pilot settle -> arena centre, exactly as Q5's main()
    fly, world, sim = build_sim(with_adhesion=True)
    st = settle(sim, fly, np.zeros(len(dof_index(fly)[1])))
    assert st["settled"], "pilot settle failed"
    tip = labrum_tip_pos(sim)
    head_id = mj.mj_name2id(sim.mj_model, mj.mjtObj.mjOBJ_BODY,
                            "flybody/c_head")
    head = sim.mj_data.xpos[head_id]
    forward = np.array([tip[0] - head[0], tip[1] - head[1]])
    forward = forward / np.linalg.norm(forward)
    tip_proj = np.array([tip[0], tip[1]])
    sim.close()
    centre = tip_proj + 0.6 * forward

    fly, world, sim = build_arena(centre)
    m = sim.mj_model
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    theta_ext = theta_ext_from_params(params, signs)
    for j in PITCH_JOINTS:  # the chain must reproduce Q5's extremes
        assert abs(theta_ext[j] - a5["theta_ext_rad"][j]) < 1e-9
    food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
    labrum_set = {mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n)
                  for n in LABRUM_GEOM_NAMES}
    tarsus_gids = geom_ids_for_bodies(sim, FRONT_TARSUS_BODIES)

    def food_check():
        lf, tf = food_contact_forces(sim, food_gid, labrum_set, tarsus_gids)
        return (lf + tf) > 0

    stA = settle(sim, fly, np.zeros(len(order)), food_check=food_check)
    assert stA["settled"] and not stA["food_contact_during_warmup"]
    restA = {j: stA["rest_angles"][j] for j in PROBOSCIS}
    recA = Recorder(sim, fly, restA, signs, e_max_ref, food_gid=food_gid)
    rowsA = run_profile(sim, fly, recA, theta_ext, signs, e_max_ref)
    sim.close()

    # ---------- Run B: free dynamic, plain construction ---------------
    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    stB = settle(sim, fly, np.zeros(len(order)))
    assert stB["settled"], "run B settle failed"
    restB = {j: stB["rest_angles"][j] for j in PROBOSCIS}
    recB = Recorder(sim, fly, restB, signs, e_max_ref)
    rowsB = run_profile(sim, fly, recB, theta_ext, signs, e_max_ref)
    sim.close()

    # ---------- Run C: same-chain quasi-static mini-sweep -------------
    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    paramsC = compiled_params(sim)
    stC = settle(sim, fly, np.zeros(len(order)))
    assert stC["settled"], "run C settle failed"
    restC = {j: stC["rest_angles"][j] for j in PROBOSCIS}
    recC = Recorder(sim, fly, restC, signs, e_max_ref)
    sweepC = []
    for e in (0.78, 0.82, 0.86, 0.90, 0.94, 1.0):
        ctrl = chain_ctrl_rev(np.zeros(len(order)), idx, paramsC, e,
                              restC, theta_ext)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(4000):                # 0.4 s hold, as the reach curve
            sim.step()
        E = recC.E_now()
        sweepC.append({"e": e, "E_rad": E, "E_fraction": E / e_max_ref,
                       "z_plane_mm": recC.z_plane()})
    sim.close()

    # ---------- analysis ----------------------------------------------
    def col(rows, key):
        return np.array([r[key] for r in rows], dtype=float)

    # Run A: onset replication + landing + the prescribed surface value
    forceA = col(rowsA, "labrum_force_N")
    fracA = col(rowsA, "E_fraction")
    zA = col(rowsA, "z_plane_mm")
    zdiscA = col(rowsA, "z_disc_mm")
    stepsA = col(rowsA, "step")
    hit = int(np.argmax(forceA > 0))
    assert forceA[hit] > 0, "run A produced no labrum-food contact"
    onsetA = {"first_labrum_force_step": int(stepsA[hit]),
              "E_fraction_at_first_force": float(fracA[hit]),
              "z_disc_crossing_fraction":
                  first_crossing(fracA, zdiscA, 0.0),
              "z_plane_at_first_force_mm": float(zA[hit]),
              "landing_fraction_z_within_0.001_of_T":
                  first_crossing(fracA, zA, T_DISC + 0.001),
              "min_z_plane_mm": float(np.min(zA)),
              "z_plane_hold_mean_last_chunk_mm":
                  float(np.mean(zA[-CHUNK_STEPS:])),
              "q5_reference": {"step": Q5_ONSET_STEP,
                               "E_fraction": Q5_ONSET_FRACTION}}
    rampA = [r for r in rowsA if r["phase"] == "ramp"]
    z_dyn_at_onset = first_passage_value(
        [r["E_fraction"] for r in rampA], [r["z_plane_mm"] for r in rampA],
        Q5_ONSET_FRACTION)

    # Run B: free dynamic surface at the onset fraction + free dynamic R
    rampB = [r for r in rowsB if r["phase"] == "ramp"]
    zB = col(rowsB, "z_plane_mm")
    z_dyn_free_at_onset = first_passage_value(
        [r["E_fraction"] for r in rampB], [r["z_plane_mm"] for r in rampB],
        Q5_ONSET_FRACTION)
    R_dyn_free = float(np.mean(zB[-CHUNK_STEPS:]))

    # Run C: same-chain quasi-static surface at the onset fraction + R
    z_qs_samechain = float(np.interp(Q5_ONSET_FRACTION,
                                     [p["E_fraction"] for p in sweepC],
                                     [p["z_plane_mm"] for p in sweepC]))
    R_qs_samechain = sweepC[-1]["z_plane_mm"]

    # prescribed quasi-static comparison: reach_curve.json z_true series
    rc = json.loads((RESULTS / "reach_curve.json").read_text())
    qs_frac = [pt["E_fraction"] for pt in rc["curve"]]
    qs_z = [pt["z_true_mm"] for pt in rc["curve"]]
    z_qs_reachcurve = float(np.interp(Q5_ONSET_FRACTION, qs_frac, qs_z))

    diff_prescribed = z_dyn_at_onset - z_qs_reachcurve
    result = {
        "artefact": "dynamic-onset quantification check (calibration, "
                    "NOT a gate step)",
        "date": "24 Nov 2026",
        "purpose": "Reviewer 3's condition on execution #5: quantify "
                   "the dynamic-vs-quasi-static pose explanation for "
                   "the Q5 onset residual (predicted f_c 0.884, "
                   "measured 0.8371, residual -0.047).",
        "configuration": "Run A: q5_rerun5.build_arena (pedestal "
                         "T = 0.33 mm, offset 0.6 mm, proboscis pairs "
                         "in), settle SS2.3, revised Pass 6 chain, Q5 "
                         "chunk profile (2 resting + 5 ramp + 15 hold "
                         "chunks), adhesion off (engages only after "
                         "first contact in Q5). Runs B/C: plain Demo C "
                         "construction, same chain; B same chunk "
                         "profile, C 0.4 s holds at e = 0.78...1.0.",
        "E_max_reference_rad": e_max_ref,
        "arena_centre_xy_mm": [float(x) for x in centre],
        "run_A_onset": onsetA,
        "surface_at_q5_onset_fraction": {
            "fraction": Q5_ONSET_FRACTION,
            "dynamic_z_true_mm_runA": z_dyn_at_onset,
            "quasi_static_z_true_mm_reach_curve": z_qs_reachcurve,
            "difference_dynamic_minus_quasistatic_mm": diff_prescribed,
            "robustness_same_chain": {
                "dynamic_free_z_true_mm_runB": z_dyn_free_at_onset,
                "quasi_static_z_true_mm_runC": z_qs_samechain,
                "difference_dynamic_minus_quasistatic_mm":
                    z_dyn_free_at_onset - z_qs_samechain,
            },
        },
        "dynamic_R_values_for_the_bracket": {
            "free_dynamic_R_runB_mm": R_dyn_free,
            "quasi_static_R_same_chain_runC_mm": R_qs_samechain,
            "quasi_static_R_reach_curve_mm": float(qs_z[-1]),
            "execution3_fast_ramp_R_mm": 0.296,
            "runA_e1_height_is_disc_supported_mm":
                onsetA["z_plane_hold_mean_last_chunk_mm"],
        },
        "run_C_sweep": sweepC,
        "explanation_holds": bool(
            abs(z_dyn_at_onset - T_DISC) <= 0.005
            and 0.010 <= abs(diff_prescribed) <= 0.014),
        "wall_clock_s": time.time() - t0,
    }
    out = RESULTS / "onset_check.json"
    out.write_text(json.dumps(result, indent=2))

    print("Run A onset replication: first labrum force at step",
          onsetA["first_labrum_force_step"], "(Q5: 6024), E/E_max =",
          round(onsetA["E_fraction_at_first_force"], 4), "(Q5: 0.8371)")
    print("Run A: disc-distance zero-crossing at E/E_max =",
          None if onsetA["z_disc_crossing_fraction"] is None
          else round(onsetA["z_disc_crossing_fraction"], 4),
          "| surface lands within 0.001 of T at E/E_max =",
          None if onsetA["landing_fraction_z_within_0.001_of_T"] is None
          else round(onsetA["landing_fraction_z_within_0.001_of_T"], 4),
          "| min z_plane =", round(onsetA["min_z_plane_mm"], 4), "mm")
    print("at E/E_max = 0.8371: dynamic z_true (A) =",
          round(z_dyn_at_onset, 4), "mm | quasi-static (reach curve) =",
          round(z_qs_reachcurve, 4), "mm | difference =",
          round(diff_prescribed, 4), "mm")
    print("same-chain robustness: dynamic free (B) =",
          round(z_dyn_free_at_onset, 4), "mm | quasi-static (C) =",
          round(z_qs_samechain, 4), "mm | difference =",
          round(z_dyn_free_at_onset - z_qs_samechain, 4), "mm")
    print("bracket: free dynamic R (B) =", round(R_dyn_free, 4),
          "mm | quasi-static R same chain (C) =",
          round(R_qs_samechain, 4), "| reach curve 0.3083 | #3 ~0.296",
          "| run A e=1 height (disc-supported) =",
          round(onsetA["z_plane_hold_mean_last_chunk_mm"], 4), "mm")
    print("explanation holds (per the stated bands):",
          result["explanation_holds"])
    print("wrote", out, "| wall", round(result["wall_clock_s"], 1), "s")


if __name__ == "__main__":
    main()
