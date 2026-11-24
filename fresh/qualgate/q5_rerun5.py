"""Q5, fifth execution (SS7.5 + SS4.6 as revised by Pass 6), 24 Nov 2026.

Arena per SS4.6 as revised: flat ground; pedestal = cylinder radius
0.5 mm, height 0.28 mm; food = flat cylinder radius 0.5 mm, height
0.05 mm on top of the pedestal, top surface at ground + 0.33 mm, named
"food", centre 0.6 mm in front of the labrum tip's settled ground
projection (pilot settle, as in executions past). The pedestal never
moves and is never adjusted; if the starting offset makes (i)
unreachable, the food+pedestal assembly's horizontal centre is adjusted
ONCE (SS7.5(iv)), the final value recorded.

Chain: SS4.3 as revised by Pass 6 (theta_ext = achievable extremes from
the compiled parameters; feedforward on). The SS4.5 taste event is
computed per physics step from food-specific contact forces (labrum
segments or front-tarsus segments vs the food geom only; >= 10
consecutive steps with force > 0 turns it ON, >= 50 without turns it
OFF; state sampled at chunk boundaries). Labrum adhesion follows
SS4.3's rule at chunk level: engages in the first chunk after the event
turns ON; releases after the event has been OFF for 2 consecutive
chunks. Food/pedestal contact forces come from the body's own contact
reporting (the MuJoCo contact array), as in the third execution.

Pass: (i) labrum-food contact force > 0 from the body's own contact
reporting, event ON, timestamps logged; (ii) with adhesion engaged, the
contact persists >= 1.0 s while e = 1 is held; (iii) on retract,
adhesion releases per the rule and the event turns OFF; (v) resting
check -- in the settled e = 0 configuration the labrum-food force is 0
(contact must be caused by the extension); (vii) no contact between the
pedestal and any body part other than the labrum at any point of the
attempt (all pedestal contacts recorded). (vi) is a recording
requirement: the measured contact-onset fraction (achieved E/E_max at
first labrum-food contact, E read from the joint angles at the contact
step) is recorded against the predicted f_c = 0.884 from the SS4.6
reach curve; a material deviation is flagged for the panel.
"""

import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType
from flygym.compose.physics import ContactParams
from flygym.compose.world.flat_ground import FlatGroundWorld
from flygym.simulation import Simulation
from flygym.utils.math import Rotation3D
from flygym.utils.mjcf import GEOM_TYPES

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (CHUNK_STEPS, PITCH_JOINTS, PROBOSCIS, build_sim,  # noqa: E402
                         dof_index, settle)
from gate_common3 import (FRONT_TARSUS_BODIES, RESULTS, compiled_params,  # noqa: E402
                          extension_E, food_contact_forces,
                          geom_ids_for_bodies, labrum_tip_pos)
from gate_common5 import chain_ctrl_rev, theta_ext_from_params  # noqa: E402
from q1_upstream_integrity import build_flybody  # noqa: E402

HOLD_CHUNKS_MAX = 30
POST_RETRACT_CHUNKS = 15
PREDICTED_FC = 0.884


def build_arena(centre_xy):
    """FlatGroundWorld + pedestal + food on top + fly, with pairs.

    Both arena geoms are paired with the fly's contact-preset geoms
    exactly as the ground plane is (same ContactParams), so they are
    physical, contact-reporting objects. Neither is added to
    world.ground_geoms (that list must stay length 1 or the leg
    ground-contact sensors the settle protocol reads are disabled).

    DEFECT FIX (fifth execution, after the first Q5 run of this
    execution failed with zero contact): the preset
    "legs_thorax_abdomen_head" contains NO proboscis segment -- the
    artefact has exactly six proboscis geoms (rostrum body +
    bristle-brown, haustellum body + black, labrum lower L/R) and none
    of them was paired with anything, so the labrum was
    contact-invisible: the diagnostic (results/q5_diagnostic5.json)
    measured the labrum penetrating the food geom by 0.032-0.035 mm at
    e = 1 with zero contacts generated. SS7.5(i) was unmeasurable
    under that construction. The arena therefore also pairs the six
    proboscis geoms with both arena geoms, same ContactParams. No fly
    parameter is touched; the pairs are arena-side collision
    definitions, like the 69 preset pairs.
    """
    world = FlatGroundWorld()
    cx, cy = float(centre_xy[0]), float(centre_xy[1])
    world.mjcf_root.worldbody.add_geom(
        type=GEOM_TYPES["cylinder"], name="pedestal",
        pos=(cx, cy, 0.14), size=(0.5, 0.14, 0))
    world.mjcf_root.worldbody.add_geom(
        type=GEOM_TYPES["cylinder"], name="food",
        pos=(cx, cy, 0.305), size=(0.5, 0.025, 0))
    fly = build_flybody()
    fly.add_leg_adhesion()
    world.add_fly(fly, (0, 0, 1.0), Rotation3D("quat", (1, 0, 0, 0)))
    preset = type(fly).CONTACT_BODIES_PRESET_CLASS("legs_thorax_abdomen_head")
    params = ContactParams()

    def add_pair(geom_name, arena_name):
        world.mjcf_root.add_pair(
            geomname1=geom_name, geomname2=arena_name,
            name=f"{geom_name}-{arena_name}",
            friction=params.get_friction_tuple(),
            solref=params.get_solref_tuple(),
            solimp=params.get_solimp_tuple(),
            margin=params.margin)

    for seg in preset.to_body_segments_list():
        for geom in fly.bodyseg_to_mjcfgeom[seg]:
            for arena_name in ("food", "pedestal"):
                add_pair(geom.name, arena_name)
    proboscis_geoms = [g.name for g in fly.mjcf_root.geoms
                       if g.name and any(k in g.name for k in
                                         ("labrum", "rostrum", "haustellum"))]
    assert len(proboscis_geoms) == 6, proboscis_geoms
    for gname in proboscis_geoms:
        for arena_name in ("food", "pedestal"):
            add_pair(gname, arena_name)
    sim = Simulation(world)
    sim.reset()
    return fly, world, sim


def pedestal_scan(sim, ped_gid, labrum_gids):
    """Contacts involving the pedestal geom at the current state.

    Returns (nonlabrum_hit, labrum_hit, details): details lists
    (other_geom_name, is_labrum, |force| N) per pedestal contact.
    """
    m, d = sim.mj_model, sim.mj_data
    nonlabrum = False
    labrum = False
    details = []
    wrench = np.zeros(6)
    for i in range(d.ncon):
        g1, g2 = int(d.contact.geom1[i]), int(d.contact.geom2[i])
        if ped_gid not in (g1, g2):
            continue
        other = g2 if g1 == ped_gid else g1
        mj.mj_contactForce(m, d, i, wrench)
        mag = float(np.linalg.norm(wrench[:3]))
        is_lab = other in labrum_gids
        name = mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, other)
        details.append((name, is_lab, mag))
        if is_lab:
            labrum = True
        else:
            nonlabrum = True
    return nonlabrum, labrum, details


def attempt(centre_xy, signs, e_max_ref, label):
    """One Q5 attempt at a given arena centre. Returns the record dict."""
    rec = {"label": label,
           "arena_centre_xy_mm": [float(x) for x in centre_xy]}
    fly, world, sim = build_arena(centre_xy)
    m = sim.mj_model
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    theta_ext = theta_ext_from_params(params, signs)
    rec["theta_ext_rad"] = theta_ext
    food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
    ped_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "pedestal")
    labrum_gids = {mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n) for n in
                   ("flybody/l_labrum_lower", "flybody/r_labrum_lower")}
    tarsus_gids = geom_ids_for_bodies(sim, FRONT_TARSUS_BODIES)
    adh_ids = [mj.mj_name2id(m, mj.mjtObj.mjOBJ_ACTUATOR,
                             f"flybody/{s}_labrum-adhesion") for s in ("l", "r")]
    rec["food_geom_id"] = int(food_gid)
    rec["pedestal_geom_id"] = int(ped_gid)
    qadr = {j: int(m.jnt_qposadr[params[j]["joint_id"]])
            for j in PITCH_JOINTS}

    ped_state = {"nonlabrum_steps": 0, "first_nonlabrum": None,
                 "labrum_max_force_N": 0.0, "pairs_seen": set()}

    def scan_pedestal(step_no):
        nl, lab, details = pedestal_scan(sim, ped_gid, labrum_gids)
        for name, is_lab, mag in details:
            ped_state["pairs_seen"].add(
                f"pedestal x {name} ({'labrum' if is_lab else 'NON-LABRUM'})")
            if is_lab:
                ped_state["labrum_max_force_N"] = max(
                    ped_state["labrum_max_force_N"], mag)
        if nl:
            ped_state["nonlabrum_steps"] += 1
            if ped_state["first_nonlabrum"] is None:
                ped_state["first_nonlabrum"] = {
                    "step": step_no,
                    "geoms": [d[0] for d in details if not d[1]]}
        return nl

    warmup_steps = {"n": 0}

    def food_check():
        # settle() calls this every physics step: scan the pedestal as
        # a side effect (SS7.5(vii) covers the whole attempt, warmup
        # included), then report any qualifying food contact.
        warmup_steps["n"] += 1
        scan_pedestal(warmup_steps["n"])
        lf, tf = food_contact_forces(sim, food_gid, labrum_gids, tarsus_gids)
        return (lf + tf) > 0

    # --- settle (SS2.3), watching food + pedestal ---------------------
    st = settle(sim, fly, np.zeros(len(order)), food_check=food_check)
    rec["settle_chunks"] = st["n_chunks"]
    rec["settled"] = st["settled"]
    rec["food_contact_during_warmup"] = st["food_contact_during_warmup"]
    rec["pedestal_nonlabrum_during_warmup"] = (
        ped_state["first_nonlabrum"] is not None)
    if not st["settled"] or st["food_contact_during_warmup"]:
        rec["verdict"] = "INVALID"
        rec["fail_reason"] = ("settle failed" if not st["settled"]
                              else "food contact during warmup (SS2.3/SS4.6)")
        rec["pedestal"] = {
            "nonlabrum_contact_steps": ped_state["nonlabrum_steps"],
            "first_nonlabrum_contact": ped_state["first_nonlabrum"],
            "pairs_seen": sorted(ped_state["pairs_seen"])}
        sim.close()
        return rec
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    rec["theta_rest_rad"] = rest

    # --- event/adhesion state -----------------------------------------
    state = {"on_streak": 0, "off_streak": 0, "event_on": False,
             "adhesion": False, "off_chunks": 0,
             "event_on_step": None, "event_off_step": None,
             "engage_chunk": None, "release_chunk": None,
             "max_labrum_force_N": 0.0, "max_tarsus_force_N": 0.0,
             "contact_run_steps": 0, "best_contact_run_with_adhesion_s": 0.0,
             "first_labrum_contact_step": None,
             "E_at_first_labrum_contact_rad": None,
             "resting_max_labrum_force_N": 0.0}
    step_counter = {"n": 0}
    chunk_log = []

    def E_now():
        q = sim.mj_data.qpos
        by = {j: float(q[qadr[j]]) for j in PITCH_JOINTS}
        return extension_E(by, rest, signs)

    def run_chunk(e, phase, chunk_idx):
        ctrl = chain_ctrl_rev(np.zeros(len(order)), idx, params, e, rest,
                              theta_ext)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for aid in adh_ids:
            sim.mj_data.ctrl[aid] = 1.0 if state["adhesion"] else 0.0
        for _ in range(CHUNK_STEPS):
            sim.step()
            step_counter["n"] += 1
            scan_pedestal(step_counter["n"])
            lf, tf = food_contact_forces(sim, food_gid, labrum_gids,
                                         tarsus_gids)
            state["max_labrum_force_N"] = max(state["max_labrum_force_N"], lf)
            state["max_tarsus_force_N"] = max(state["max_tarsus_force_N"], tf)
            if phase == "resting_check":
                state["resting_max_labrum_force_N"] = max(
                    state["resting_max_labrum_force_N"], lf)
            if lf > 0 and state["first_labrum_contact_step"] is None:
                state["first_labrum_contact_step"] = step_counter["n"]
                state["E_at_first_labrum_contact_rad"] = E_now()
            qualifying = (lf + tf) > 0
            if qualifying:
                state["on_streak"] += 1
                state["off_streak"] = 0
                state["contact_run_steps"] += 1
                if state["adhesion"]:
                    state["best_contact_run_with_adhesion_s"] = max(
                        state["best_contact_run_with_adhesion_s"],
                        state["contact_run_steps"] * 1e-4)
                if state["on_streak"] >= 10 and not state["event_on"]:
                    state["event_on"] = True
                    state["event_on_step"] = step_counter["n"]
            else:
                state["off_streak"] += 1
                state["on_streak"] = 0
                state["contact_run_steps"] = 0
                if state["off_streak"] >= 50 and state["event_on"]:
                    state["event_on"] = False
                    state["event_off_step"] = step_counter["n"]
        angles = sim.get_joint_angles(fly.name)
        by_joint = {j: float(angles[idx[j]]) for j in PROBOSCIS}
        chunk_log.append({"phase": phase, "chunk": chunk_idx, "e": e,
                          "E_rad": extension_E(by_joint, rest, signs),
                          "event_on_at_chunk_end": state["event_on"],
                          "adhesion_on_during_chunk": state["adhesion"]})
        if state["event_on"]:
            state["off_chunks"] = 0
            if not state["adhesion"]:
                state["adhesion"] = True
                state["engage_chunk"] = chunk_idx + 1
        else:
            state["off_chunks"] += 1
            if state["adhesion"] and state["off_chunks"] >= 2:
                state["adhesion"] = False
                state["release_chunk"] = chunk_idx + 1

    chunk = 0
    for _ in range(2):                       # (v) resting check at e = 0
        run_chunk(0.0, "resting_check", chunk); chunk += 1
    for i in range(5):                       # ramp e 0 -> 1
        run_chunk((i + 1) / 5, "ramp", chunk); chunk += 1
    hold_chunks = 0
    while hold_chunks < HOLD_CHUNKS_MAX:      # hold e = 1
        run_chunk(1.0, "hold", chunk); chunk += 1; hold_chunks += 1
        if (state["event_on"] and state["adhesion"]
                and state["best_contact_run_with_adhesion_s"] >= 1.0):
            for _ in range(3):
                run_chunk(1.0, "hold", chunk); chunk += 1; hold_chunks += 1
            break
    tip_ext = labrum_tip_pos(sim)
    rec["tip_at_full_extension_xyz_mm"] = [float(x) for x in tip_ext]
    rec["hold_chunks_run"] = hold_chunks
    for i in range(5):                       # retract e -> 0
        run_chunk(1.0 - (i + 1) / 5, "retract", chunk); chunk += 1
    for _ in range(POST_RETRACT_CHUNKS):     # hold e = 0
        run_chunk(0.0, "post_retract", chunk); chunk += 1
    sim.close()

    rec["event_on_step"] = state["event_on_step"]
    rec["event_on_time_s"] = (None if state["event_on_step"] is None
                              else state["event_on_step"] * 1e-4)
    rec["event_off_step"] = state["event_off_step"]
    rec["event_off_time_s"] = (None if state["event_off_step"] is None
                               else state["event_off_step"] * 1e-4)
    rec["adhesion_engage_chunk"] = state["engage_chunk"]
    rec["adhesion_release_chunk"] = state["release_chunk"]
    rec["max_labrum_food_force_N"] = state["max_labrum_force_N"]
    rec["max_front_tarsus_food_force_N"] = state["max_tarsus_force_N"]
    rec["best_contact_persistence_with_adhesion_s"] = \
        state["best_contact_run_with_adhesion_s"]
    rec["resting_max_labrum_food_force_N"] = \
        state["resting_max_labrum_force_N"]
    rec["pedestal"] = {
        "nonlabrum_contact_steps": ped_state["nonlabrum_steps"],
        "first_nonlabrum_contact": ped_state["first_nonlabrum"],
        "labrum_pedestal_max_force_N": ped_state["labrum_max_force_N"],
        "pairs_seen": sorted(ped_state["pairs_seen"])}
    # (vi) measured contact-onset fraction vs the reach-curve prediction.
    if state["E_at_first_labrum_contact_rad"] is not None:
        frac = state["E_at_first_labrum_contact_rad"] / e_max_ref
        rec["onset_fraction_measured"] = float(frac)
        rec["onset_fraction_predicted"] = PREDICTED_FC
        rec["onset_fraction_deviation"] = float(frac - PREDICTED_FC)
        rec["onset_fraction_material_deviation_flag"] = bool(
            abs(frac - PREDICTED_FC) > 0.10)
    else:
        rec["onset_fraction_measured"] = None
        rec["onset_fraction_predicted"] = PREDICTED_FC
        rec["onset_fraction_deviation"] = None
        rec["onset_fraction_material_deviation_flag"] = None
    rec["first_labrum_contact_step"] = state["first_labrum_contact_step"]
    rec["E_at_first_labrum_contact_rad"] = \
        state["E_at_first_labrum_contact_rad"]
    rec["E_max_reference_rad"] = e_max_ref
    rec["chunk_log"] = chunk_log
    checks = {
        "i_labrum_contact_and_event_on": bool(
            state["max_labrum_force_N"] > 0 and state["event_on_step"] is not None),
        "ii_contact_persists_ge_1s_with_adhesion": bool(
            state["best_contact_run_with_adhesion_s"] >= 1.0),
        "iii_event_off_and_adhesion_released_after_retract": bool(
            state["event_off_step"] is not None
            and state["release_chunk"] is not None),
        "v_resting_labrum_food_force_zero": bool(
            state["resting_max_labrum_force_N"] == 0.0),
        "vii_no_nonlabrum_pedestal_contact": bool(
            ped_state["nonlabrum_steps"] == 0),
    }
    rec["checks"] = checks
    rec["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    return rec


def main():
    t0 = time.time()
    q4 = json.loads((RESULTS / "q4_rerun5.json").read_text())
    assert q4["verdict"] == "PASS", "Q4 did not pass; Q5 must not run"
    q3 = json.loads((RESULTS / "q3_rerun5.json").read_text())
    q2 = json.loads((RESULTS / "q2_rerun5.json").read_text())
    signs = {j: q2["joints"][j]["extension_sign_s"] for j in PITCH_JOINTS}
    e_max_ref = q3["E_max_measured_hold_mean_rad"]

    # --- pilot settle: measure the tip's settled ground projection -----
    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    st = settle(sim, fly, np.zeros(len(order)))
    assert st["settled"], "pilot settle failed"
    tip = labrum_tip_pos(sim)
    head_id = mj.mj_name2id(sim.mj_model, mj.mjtObj.mjOBJ_BODY, "flybody/c_head")
    head = sim.mj_data.xpos[head_id]
    forward = np.array([tip[0] - head[0], tip[1] - head[1]])
    forward = forward / np.linalg.norm(forward)
    tip_proj = np.array([tip[0], tip[1]])
    sim.close()
    pilot = {"tip_settled_xyz_mm": [float(x) for x in tip],
             "tip_ground_projection_xy_mm": [float(x) for x in tip_proj],
             "forward_xy_unit": [float(x) for x in forward]}
    centre1 = tip_proj + 0.6 * forward

    attempts = []
    a1 = attempt(centre1, signs, e_max_ref, "offset 0.6 mm (SS4.6 start)")
    a1["offset_in_front_of_tip_projection_mm"] = 0.6
    attempts.append(a1)
    final_offset = 0.6
    adjusted = False
    # SS7.5(iv): the single adjustment is available only when (i) is
    # unreachable at the starting offset and everything else was clean.
    only_i_unreachable = (
        a1["verdict"] != "PASS"
        and a1.get("checks", {}).get("i_labrum_contact_and_event_on") is False
        and a1.get("max_labrum_food_force_N") == 0.0
        and a1.get("checks", {}).get("v_resting_labrum_food_force_zero", False)
        and a1.get("checks", {}).get("vii_no_nonlabrum_pedestal_contact", False))
    if only_i_unreachable:
        tip_ext = np.array(a1["tip_at_full_extension_xyz_mm"][:2])
        centre2 = tip_ext
        final_offset = float(np.dot(centre2 - tip_proj, forward))
        a2 = attempt(centre2, signs, e_max_ref,
                     "offset adjusted once (SS7.5(iv)), same pedestal")
        a2["offset_in_front_of_tip_projection_mm"] = final_offset
        attempts.append(a2)
        adjusted = True

    last = attempts[-1]
    result = {"step": "Q5 (rerun5)", "pilot": pilot,
              "arena": ("pedestal cylinder r 0.5 mm, h 0.28 mm + food "
                        "cylinder r 0.5 mm, h 0.05 mm on top, disc top "
                        "at ground + 0.33 mm (SS4.6 as revised by "
                        "Pass 6); pedestal fixed, never adjusted"),
              "attempts": attempts, "offset_adjusted_once": adjusted,
              "final_offset_in_front_of_tip_projection_mm": final_offset,
              "verdict": last["verdict"],
              "wall_clock_s": time.time() - t0}
    out = RESULTS / "q5_rerun5.json"
    out.write_text(json.dumps(result, indent=2))
    for a in attempts:
        print(a["label"], "->", a["verdict"],
              "| max labrum force", a.get("max_labrum_food_force_N"),
              "| resting force", a.get("resting_max_labrum_food_force_N"),
              "| onset frac", a.get("onset_fraction_measured"),
              "| persistence", a.get("best_contact_persistence_with_adhesion_s"),
              "| pedestal nonlabrum steps",
              a.get("pedestal", {}).get("nonlabrum_contact_steps"))
    print("final offset mm:", final_offset, "| adjusted:", adjusted)
    print("Q5 verdict:", result["verdict"], "wall", result["wall_clock_s"])
    print("wrote", out)


if __name__ == "__main__":
    main()
