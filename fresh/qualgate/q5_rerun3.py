"""Q5, third execution (SS7.5 + SS4.6; spec text governs), 24 Nov 2026.

Arena per SS4.6: flat ground; food = flat cylinder, radius 0.5 mm, height
0.05 mm, top surface at ground + 0.05 mm, named "food", centre on the
ground 0.6 mm in front of the labrum tip's settled ground projection.
Placement is measured from a pilot settle (same construction, no food):
"in front" = the ground-projected head->labrum-tip direction (anatomical
anterior). The food geom is paired with the fly's contact-preset geoms
exactly as the ground plane is (same ContactParams), so it is a physical,
contact-reporting object in the arena.

Procedure: settle (SS2.3; food contact during warmup invalidates the
episode), ramp e to 1 through the SS4.3 chain (feedforward on), hold,
then retract. The SS4.5 taste event is computed per physics step from
food-specific contact forces (labrum segments or front-tarsus segments
vs the food geom only; >= 10 consecutive steps with force > 0 turns it
ON, >= 50 without turns it OFF; state sampled at chunk boundaries).
Labrum adhesion follows SS4.3's rule at chunk level: engages in the
first chunk after the event turns ON; releases after the event has been
OFF for 2 consecutive chunks.

Pass: (i) labrum-food contact force > 0 from the body's own contact
reporting, event ON, timestamps logged; (ii) with adhesion engaged, the
contact persists >= 1.0 s while e = 1 is held; (iii) on retract, adhesion
releases per the rule and the event turns OFF. If the 0.6 mm offset makes
(i) unreachable, the offset is adjusted ONCE (food centre moved to the
labrum tip's ground projection measured at full extension), the final
value recorded, and (i)-(iii) re-run at that value (SS7.5(iv)).
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
from gate_common3 import (FRONT_TARSUS_BODIES, RESULTS, chain_ctrl,  # noqa: E402
                          compiled_params, extension_E, food_contact_forces,
                          geom_ids_for_bodies, labrum_tip_pos)
from q1_upstream_integrity import build_flybody  # noqa: E402

HOLD_CHUNKS_MAX = 30
POST_RETRACT_CHUNKS = 15


def build_arena(food_centre_xy):
    """FlatGroundWorld + named food cylinder + fly, with food pairs."""
    world = FlatGroundWorld()
    world.mjcf_root.worldbody.add_geom(
        type=GEOM_TYPES["cylinder"], name="food",
        pos=(float(food_centre_xy[0]), float(food_centre_xy[1]), 0.025),
        size=(0.5, 0.025, 0))
    fly = build_flybody()
    fly.add_leg_adhesion()
    world.add_fly(fly, (0, 0, 1.0), Rotation3D("quat", (1, 0, 0, 0)))
    # Pair the food geom with the fly's contact-preset geoms, mirroring
    # BaseWorld._set_ground_contact's construction for the ground plane.
    preset = type(fly).CONTACT_BODIES_PRESET_CLASS("legs_thorax_abdomen_head")
    params = ContactParams()
    for seg in preset.to_body_segments_list():
        for geom in fly.bodyseg_to_mjcfgeom[seg]:
            world.mjcf_root.add_pair(
                geomname1=geom.name, geomname2="food",
                name=f"{geom.name}-food",
                friction=params.get_friction_tuple(),
                solref=params.get_solref_tuple(),
                solimp=params.get_solimp_tuple(),
                margin=params.margin)
    sim = Simulation(world)
    sim.reset()
    return fly, world, sim


def attempt(offset_centre_xy, signs, theta_ext, label):
    """One Q5 attempt at a given food centre. Returns the record dict."""
    rec = {"label": label, "food_centre_xy_mm": [float(x) for x in
                                                 offset_centre_xy]}
    fly, world, sim = build_arena(offset_centre_xy)
    m = sim.mj_model
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
    labrum_gids = {mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n) for n in
                   ("flybody/l_labrum_lower", "flybody/r_labrum_lower")}
    tarsus_gids = geom_ids_for_bodies(sim, FRONT_TARSUS_BODIES)
    adh_ids = [mj.mj_name2id(m, mj.mjtObj.mjOBJ_ACTUATOR,
                             f"flybody/{s}_labrum-adhesion") for s in ("l", "r")]
    rec["food_geom_id"] = int(food_gid)

    def food_check():
        lf, tf = food_contact_forces(sim, food_gid, labrum_gids, tarsus_gids)
        return (lf + tf) > 0

    st = settle(sim, fly, np.zeros(len(order)), food_check=food_check)
    rec["settle_chunks"] = st["n_chunks"]
    rec["settled"] = st["settled"]
    rec["food_contact_during_warmup"] = st["food_contact_during_warmup"]
    if not st["settled"] or st["food_contact_during_warmup"]:
        rec["verdict"] = "INVALID"
        rec["fail_reason"] = ("settle failed" if not st["settled"]
                              else "food contact during warmup (SS2.3/SS4.6)")
        sim.close()
        return rec
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    rec["theta_rest_rad"] = rest

    # --- event/adhesion state -------------------------------------------
    state = {"on_streak": 0, "off_streak": 0, "event_on": False,
             "adhesion": False, "off_chunks": 0,
             "event_on_step": None, "event_off_step": None,
             "engage_chunk": None, "release_chunk": None,
             "max_labrum_force_N": 0.0, "max_tarsus_force_N": 0.0,
             "contact_run_steps": 0, "best_contact_run_with_adhesion_s": 0.0,
             "tip_at_full_extension_xy": None}
    step_counter = {"n": 0}
    chunk_log = []

    def run_chunk(e, phase, chunk_idx):
        ctrl = chain_ctrl(np.zeros(len(order)), idx, params, e, rest,
                          signs, theta_ext)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        # adhesion decision for THIS chunk was made at the previous
        # chunk boundary (SS4.3 rule), applied via the ctrl array.
        for aid in adh_ids:
            sim.mj_data.ctrl[aid] = 1.0 if state["adhesion"] else 0.0
        for _ in range(CHUNK_STEPS):
            sim.step()
            step_counter["n"] += 1
            lf, tf = food_contact_forces(sim, food_gid, labrum_gids,
                                         tarsus_gids)
            state["max_labrum_force_N"] = max(state["max_labrum_force_N"], lf)
            state["max_tarsus_force_N"] = max(state["max_tarsus_force_N"], tf)
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
        # chunk-boundary adhesion rule (SS4.3)
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
    for i in range(5):                       # ramp e 0 -> 1
        run_chunk((i + 1) / 5, "ramp", chunk); chunk += 1
    hold_chunks = 0
    while hold_chunks < HOLD_CHUNKS_MAX:      # hold e = 1
        run_chunk(1.0, "hold", chunk); chunk += 1; hold_chunks += 1
        if (state["event_on"] and state["adhesion"]
                and state["best_contact_run_with_adhesion_s"] >= 1.0):
            # persistence demonstrated; a few more chunks of margin
            for _ in range(3):
                run_chunk(1.0, "hold", chunk); chunk += 1; hold_chunks += 1
            break
    tip_ext = labrum_tip_pos(sim)
    state["tip_at_full_extension_xy"] = [float(tip_ext[0]), float(tip_ext[1])]
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
    rec["tip_at_full_extension_xy_mm"] = state["tip_at_full_extension_xy"]
    rec["chunk_log"] = chunk_log
    checks = {
        "i_labrum_contact_and_event_on": bool(
            state["max_labrum_force_N"] > 0 and state["event_on_step"] is not None),
        "ii_contact_persists_ge_1s_with_adhesion": bool(
            state["best_contact_run_with_adhesion_s"] >= 1.0),
        "iii_event_off_and_adhesion_released_after_retract": bool(
            state["event_off_step"] is not None
            and state["release_chunk"] is not None),
    }
    rec["checks"] = checks
    rec["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    return rec


def main():
    t0 = time.time()
    q2 = json.loads((RESULTS / "q2_rerun3.json").read_text())
    assert q2["verdict"] == "PASS"
    signs = {j: q2["joints"][j]["extension_sign_s"] for j in PITCH_JOINTS}
    theta_ext = {j: q2["joints"][j]["theta_ext_rad"] for j in PITCH_JOINTS}

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
    a1 = attempt(centre1, signs, theta_ext, "offset 0.6 mm (SS4.6 start)")
    a1["offset_in_front_of_tip_projection_mm"] = 0.6
    attempts.append(a1)
    final_offset = 0.6
    adjusted = False
    if a1["verdict"] != "PASS":
        # SS7.5(iv): adjust the offset ONCE -- food centre to the labrum
        # tip's ground projection measured at full extension.
        tip_ext = np.array(a1["tip_at_full_extension_xy_mm"])
        centre2 = tip_ext
        final_offset = float(np.dot(centre2 - tip_proj, forward))
        a2 = attempt(centre2, signs, theta_ext,
                     "offset adjusted once (SS7.5(iv))")
        a2["offset_in_front_of_tip_projection_mm"] = final_offset
        attempts.append(a2)
        adjusted = True

    last = attempts[-1]
    result = {"step": "Q5 (rerun3)", "pilot": pilot,
              "attempts": attempts, "offset_adjusted_once": adjusted,
              "final_offset_in_front_of_tip_projection_mm": final_offset,
              "verdict": last["verdict"],
              "wall_clock_s": time.time() - t0}
    out = RESULTS / "q5_rerun3.json"
    out.write_text(json.dumps(result, indent=2))
    for a in attempts:
        print(a["label"], "->", a["verdict"],
              "| max labrum force", a.get("max_labrum_food_force_N"),
              "| event on at", a.get("event_on_time_s"),
              "| persistence", a.get("best_contact_persistence_with_adhesion_s"),
              "| engage/release chunks", a.get("adhesion_engage_chunk"),
              a.get("adhesion_release_chunk"))
    print("final offset mm:", final_offset, "| adjusted:", adjusted)
    print("Q5 verdict:", result["verdict"], "wall", result["wall_clock_s"])
    print("wrote", out)


if __name__ == "__main__":
    main()
