"""Clearance check + E definitions (pre-gate calibrations, NOT gate
steps), 24 Nov 2026 -- Reviewer 1's Pass 6 confirmation conditions 2
and 3.

CALIBRATION 1 -- whole-body pedestal clearance. The SS4.6 arena as
amended by Pass 6 (floor + pedestal cylinder r 0.5 mm, h 0.28 mm +
food disc r 0.5 mm, h 0.05 mm on top, disc top at ground + 0.33 mm;
pedestal centre 0.6 mm in front of the labrum tip's settled ground
projection, placed from a pilot settle exactly as Q5 constructs it).
The pedestal/food geoms carry NO contact pairs and contype/conaffinity
0: nothing steps against them. Poses are set by stepping the SS4.3
chain AS REVISED by Pass 6 (theta_ext = the achievable extremes:
rostrum -0.954, haustellum pitch -1.223, labrum +0.2625; feedforward
from the compiled artefact's parameters) quasi-statically, 0.4 s hold
per point as in reach_curve.py, and clearances are read with
mj_geomDistance. Distances are computed from the pedestal geom and
from the food-disc geom to EVERY non-labrum fly geom (all geoms except
l_labrum_lower / r_labrum_lower, the ground plane and the two arena
geoms). Pre-registered expectation: every non-labrum clearance
> 0.02 mm, across the sweep and at rest.

CALIBRATION 2 -- E definitions pinned exactly, from the compiled model
and the gate code's own extension_E (gate_common3), through the
revised chain: (a) E at e = 1 and the exact source of the 0.0041 rad
gap between E (2.1746) and the naive joint-angle sum (2.1787);
(b) Q3's raw-extremes E recomputed from q3_rerun3.py's own formula and
the reconciliation of 2.8258 (artefact) / 2.8264 (gate summary) against
1.24 + 1.59 = 2.83.
"""

import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType
from flygym.compose.world.flat_ground import FlatGroundWorld
from flygym.simulation import Simulation
from flygym.utils.math import Rotation3D
from flygym.utils.mjcf import GEOM_TYPES

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (PITCH_JOINTS, PROBOSCIS, RANGES, build_sim,  # noqa: E402
                         dof_index, settle)
from gate_common3 import (LABRUM_GEOM_NAMES, RESULTS, compiled_params,  # noqa: E402
                          extension_E, feedforward_ctrl, labrum_tip_pos,
                          qhat_eff)
from q1_upstream_integrity import build_flybody  # noqa: E402

HOLD_STEPS = 4000            # 0.4 s at dt = 1e-4 s, as in reach_curve.py
N_POINTS = 21                # e = 0, 0.05, ..., 1.0
DISTMAX = 10.0               # mm, as in reach_curve.py's distance check
CLEARANCE_MARGIN_MM = 0.02   # pre-registered expectation bound

SIGNS = {"c_head-c_rostrum-pitch": -1, "c_rostrum-c_haustellum-pitch": -1}
# SS4.3 as revised by Pass 6: achievable extremes (absolute angles, rad).
THETA_EXT_REV = {
    "c_head-c_rostrum-pitch": -0.954,
    "c_rostrum-c_haustellum-pitch": -1.223,
    "c_haustellum-l_labrum-pitch": 0.2625,
    "c_haustellum-r_labrum-pitch": 0.2625,
}
YAW = "c_rostrum-c_haustellum-yaw"


def chain_targets_rev(e, rest):
    """SS4.3 target functions as revised by Pass 6 (yaw held at rest)."""
    t = {j: rest[j] + e * (THETA_EXT_REV[j] - rest[j]) for j in THETA_EXT_REV}
    t[YAW] = rest[YAW]
    return t


def chain_ctrl_rev(base_ctrl, idx, params, e, rest):
    """Ctrl under the revised chain: e = 0 writes ctrl = 0 to the five
    DoFs (SS4.3); e > 0 writes the feedforward inverse of each target."""
    ctrl = np.array(base_ctrl, dtype=float)
    if e == 0:
        for j in PROBOSCIS:
            ctrl[idx[j]] = 0.0
        return ctrl
    targets = chain_targets_rev(e, rest)
    for j in PROBOSCIS:
        ctrl[idx[j]] = feedforward_ctrl(params[j], targets[j])
    return ctrl


def predicted_E_rev(params, rest, e):
    """Map-predicted achieved E at e under the revised chain."""
    targets = chain_targets_rev(e, rest)
    achieved = {}
    for j in PITCH_JOINTS:
        ctrl = 0.0 if e == 0 else feedforward_ctrl(params[j], targets[j])
        achieved[j] = qhat_eff(params[j], ctrl)
    return extension_E(achieved, rest, SIGNS)


# ----------------------------------------------------------------------
# Calibration 2 -- E definitions
# ----------------------------------------------------------------------

def calibration_E_definitions():
    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    st = settle(sim, fly, np.zeros(len(order)))
    assert st["settled"], "settle did not complete within the SS2.3 cap"
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}

    base_ctrl = np.zeros(len(order))
    # e = 0 sanity: E of the settled pose against its own rest is 0.
    angles0 = sim.get_joint_angles(fly.name)
    by0 = {j: float(angles0[idx[j]]) for j in PROBOSCIS}
    E_at_rest = extension_E(by0, rest, SIGNS)

    ctrl1 = chain_ctrl_rev(base_ctrl, idx, params, 1.0, rest)
    sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl1)
    for _ in range(HOLD_STEPS):
        sim.step()
    angles = sim.get_joint_angles(fly.name)
    by = {j: float(angles[idx[j]]) for j in PROBOSCIS}
    E1 = extension_E(by, rest, SIGNS)
    sim.close()

    ros, haus = PITCH_JOINTS
    naive_sum = abs(by[ros]) + abs(by[haus])
    rest_sum = rest[ros] + rest[haus]
    # Q3's own formula (q3_rerun3.py): extremes measured from theta_rest.
    e_raw_from_rest = float(sum(
        SIGNS[j] * ((RANGES[j][1] if SIGNS[j] > 0 else RANGES[j][0]) - rest[j])
        for j in PITCH_JOINTS))
    e_raw_from_zero = float(sum(
        SIGNS[j] * (RANGES[j][1] if SIGNS[j] > 0 else RANGES[j][0])
        for j in PITCH_JOINTS))
    ctrls_at_e1 = {j: float(ctrl1[idx[j]]) for j in PROBOSCIS}
    return {
        "construction": "Demo C FlyBody via gate_common.build_sim "
                        "(with_adhesion=True), plain flat ground",
        "chain": "SS4.3 as revised by Pass 6 (theta_ext = achievable "
                 "extremes); feedforward from compiled parameters",
        "theta_rest_rad": rest,
        "E_definition": ("extension_E (gate_common3), SS4.4: E = "
                         "s_ros*(theta_ros - theta_rest_ros) + "
                         "s_haus*(theta_haus - theta_rest_haus), s = -1 "
                         "for both pitch joints; theta from "
                         "get_joint_angles (the actuated joints' qpos "
                         "coordinates), theta_rest the same run's "
                         "settled angles under zero command. E sums "
                         "JOINT-ANGLE EXCURSIONS FROM THE SETTLED REST "
                         "POSE -- not segment orientations, and not "
                         "angles from qpos zero."),
        "E_at_rest_sanity_rad": E_at_rest,
        "angles_at_e1_rad": by,
        "ctrls_at_e1": ctrls_at_e1,
        "ctrl_range_limits": {j: [float(x) for x in RANGES[j]]
                              for j in PROBOSCIS},
        "E_at_e1_rad": E1,
        "E_predicted_map_at_e1_rad": predicted_E_rev(params, rest, 1.0),
        "naive_joint_angle_sum_at_e1_rad": naive_sum,
        "gap_naive_minus_E_rad": naive_sum - E1,
        "rest_angle_sum_rad": rest_sum,
        "gap_check": ("naive_sum - E == -(rest_ros + rest_haus): the "
                      "naive sum omits the -theta_rest terms of SS4.4's "
                      "definition; both rest angles are slightly "
                      "negative (the settled proboscis sits a hair into "
                      "the extension direction from qpos zero), so E "
                      "is smaller than the naive sum by exactly the "
                      "rest sum's magnitude."),
        "raw_extremes": {
            "q3_code_formula": ("sum over pitch joints of s_j * "
                                "(range_end_in_extension_direction_j - "
                                "theta_rest_j), range ends and rest from "
                                "the same run (q3_rerun3.py)"),
            "E_raw_from_rest_rad": e_raw_from_rest,
            "E_raw_from_qpos_zero_rad": e_raw_from_zero,
            "gap_zero_minus_rest_rad": e_raw_from_zero - e_raw_from_rest,
            "q3_artefact_recorded_rad": 2.8258492046987165,
            "gate_summary_recorded_rad": 2.8264,
            "reconciliation": ("Q3's raw-extremes E measures the "
                               "published range ends FROM THE SETTLED "
                               "REST POSE, not from qpos zero: with "
                               "s = -1 it is (1.24 + theta_rest_ros) + "
                               "(1.59 + theta_rest_haus) in magnitude "
                               "terms, i.e. 2.83 + (rest sum) = 2.83 - "
                               "0.0041508 = 2.8258. The 1.24 + 1.59 = "
                               "2.83 figure measures the same ends from "
                               "zero and overstates by the identical "
                               "rest offset that separates E from the "
                               "naive joint-angle sum."),
        },
    }


# ----------------------------------------------------------------------
# Calibration 1 -- whole-body pedestal clearance
# ----------------------------------------------------------------------

def build_arena(centre_xy):
    """SS4.6 arena (Pass 6): ground + pedestal + food disc, fly added;
    NO contact pairs for the arena geoms (set after construction)."""
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
    sim = Simulation(world)
    sim.reset()
    m = sim.mj_model
    for name in ("pedestal", "food"):
        gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, name)
        assert gid >= 0, f"arena geom not found: {name}"
        m.geom_contype[gid] = 0
        m.geom_conaffinity[gid] = 0
    return fly, world, sim


def calibration_clearance():
    # --- pilot settle: the SS4.6 placement measurement (as Q5) -------
    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    st = settle(sim, fly, np.zeros(len(order)))
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
    pilot = {"tip_settled_xyz_mm": [float(x) for x in tip],
             "tip_ground_projection_xy_mm": [float(x) for x in tip_proj],
             "forward_xy_unit": [float(x) for x in forward],
             "pedestal_centre_xy_mm": [float(x) for x in centre]}

    # --- arena --------------------------------------------------------
    fly, world, sim = build_arena(centre)
    m, d = sim.mj_model, sim.mj_data
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    ped_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "pedestal")
    food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
    labrum_gids = [mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n)
                   for n in LABRUM_GEOM_NAMES]
    assert all(g >= 0 for g in labrum_gids)
    plane_gids = [g for g in range(m.ngeom)
                  if m.geom_type[g] == mj.mjtGeom.mjGEOM_PLANE]
    excluded = set(labrum_gids) | set(plane_gids) | {ped_gid, food_gid}
    fly_geoms = [g for g in range(m.ngeom) if g not in excluded]
    geom_names = {g: (mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, g) or f"#{g}")
                  for g in fly_geoms}
    # no compiled pair may involve the arena geoms
    pair_geoms = set()
    for i in range(m.npair):
        pair_geoms.add(int(m.pair_geom1[i]))
        pair_geoms.add(int(m.pair_geom2[i]))
    arena_pairs = [int(g) for g in (ped_gid, food_gid) if g in pair_geoms]

    st = settle(sim, fly, np.zeros(len(order)))
    assert st["settled"], "arena settle failed"
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    tip_arena = labrum_tip_pos(sim)
    arena_settled_offset = float(np.dot(
        np.array([tip_arena[0], tip_arena[1]]) - tip_proj, forward))

    # --- sweep --------------------------------------------------------
    base_ctrl = np.zeros(len(order))
    # per (arena_label, fly_geom): [min_dist, e_at_min, dist_at_rest]
    track = {}
    labrum_track = {}   # per (arena_label, labrum_name): same triple
    contacts_with_arena = 0
    sweep_E = []
    for k in range(N_POINTS):
        e = k / (N_POINTS - 1)
        ctrl = chain_ctrl_rev(base_ctrl, idx, params, e, rest)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(HOLD_STEPS):
            sim.step()
            for i in range(d.ncon):
                if ped_gid in (int(d.contact.geom1[i]),
                                int(d.contact.geom2[i])) or \
                   food_gid in (int(d.contact.geom1[i]),
                                int(d.contact.geom2[i])):
                    contacts_with_arena += 1
        mj.mj_forward(m, d)
        angles = sim.get_joint_angles(fly.name)
        by = {j: float(angles[idx[j]]) for j in PROBOSCIS}
        sweep_E.append(extension_E(by, rest, SIGNS))
        for label, agid in (("pedestal", ped_gid), ("food", food_gid)):
            for g in fly_geoms:
                dist = float(mj.mj_geomDistance(m, d, agid, g,
                                                DISTMAX, None))
                key = (label, g)
                cur = track.get(key)
                if cur is None:
                    track[key] = [dist, e, dist]
                else:
                    if dist < cur[0]:
                        cur[0], cur[1] = dist, e
            for name, lgid in zip(LABRUM_GEOM_NAMES, labrum_gids):
                dist = float(mj.mj_geomDistance(m, d, agid, lgid,
                                                DISTMAX, None))
                key = (label, name)
                cur = labrum_track.get(key)
                if cur is None:
                    labrum_track[key] = [dist, e, dist]
                else:
                    if dist < cur[0]:
                        cur[0], cur[1] = dist, e
    sim.close()

    per_geom = {}
    for (label, g), (mind, e_at, d_rest) in track.items():
        per_geom.setdefault(label, []).append({
            "geom": geom_names[g], "geom_id": int(g),
            "min_clearance_mm": mind, "e_at_min": e_at,
            "clearance_at_rest_mm": d_rest})
    for label in per_geom:
        per_geom[label].sort(key=lambda r: r["min_clearance_mm"])
    all_mins = [r["min_clearance_mm"] for label in per_geom
                for r in per_geom[label]]
    below = [r for label in per_geom for r in per_geom[label]
             if r["min_clearance_mm"] <= CLEARANCE_MARGIN_MM]
    labrum_info = {}
    for (label, name), (mind, e_at, d_rest) in labrum_track.items():
        labrum_info.setdefault(label, {})[name] = {
            "min_distance_mm": mind, "e_at_min": e_at,
            "distance_at_rest_mm": d_rest}
    return {
        "arena": ("FlatGroundWorld + pedestal cylinder (r 0.5 mm, "
                  "h 0.28 mm, centre z 0.14) + food cylinder (r 0.5 mm, "
                  "h 0.05 mm, centre z 0.305, top at ground + 0.33 mm); "
                  "pedestal centre 0.6 mm in front of the labrum tip's "
                  "settled ground projection (pilot settle, as Q5)"),
        "pilot": pilot,
        "arena_settled_tip_offset_in_front_mm": arena_settled_offset,
        "theta_rest_rad": rest,
        "n_fly_geoms_checked": len(fly_geoms),
        "geom_classification": ("every compiled geom except the two "
                                "labrum geoms (l_labrum_lower / "
                                "r_labrum_lower), the ground plane(s) "
                                "and the two arena geoms"),
        "compiled_pairs_involving_arena_geoms": arena_pairs,
        "contacts_involving_arena_geoms_during_sweep": contacts_with_arena,
        "sweep": {"n_points": N_POINTS, "hold_per_point_s": HOLD_STEPS * 1e-4,
                  "E_at_each_e_rad": sweep_E},
        "pre_registered_expectation": ("all non-labrum clearances "
                                       "> 0.02 mm"),
        "global_min_clearance_mm": float(min(all_mins)),
        "all_clearances_above_margin": bool(
            min(all_mins) > CLEARANCE_MARGIN_MM),
        "geoms_at_or_below_margin": below,
        "per_geom": per_geom,
        "labrum_distances_for_information": labrum_info,
    }


def main():
    t0 = time.time()
    cal2 = calibration_E_definitions()
    cal1 = calibration_clearance()
    result = {
        "artefact": "clearance check + E definitions (pre-gate "
                    "calibrations, NOT gate steps)",
        "date": "24 Nov 2026",
        "spec": ("PART4-SENSORY-SPECS.md SS4.3-SS4.6, SS7.5 as amended "
                 "through Pass 6 revised; Reviewer 1 Pass 6 "
                 "confirmation conditions 2 and 3"),
        "calibration_1_clearance": cal1,
        "calibration_2_E_definitions": cal2,
        "wall_clock_s": time.time() - t0,
    }
    out = RESULTS / "clearance_check.json"
    out.write_text(json.dumps(result, indent=2))

    print("=== Calibration 2: E definitions ===")
    print("rest:", {j: round(cal2["theta_rest_rad"][j], 5)
                    for j in PITCH_JOINTS})
    print("angles at e=1:", {j: round(cal2["angles_at_e1_rad"][j], 4)
                             for j in PROBOSCIS})
    print("ctrls at e=1:", {j: round(v, 4) for j, v in
                            cal2["ctrls_at_e1"].items()})
    print("E at e=1:", round(cal2["E_at_e1_rad"], 6),
          "| map-predicted:", round(cal2["E_predicted_map_at_e1_rad"], 6))
    print("naive sum:", round(cal2["naive_joint_angle_sum_at_e1_rad"], 6),
          "| gap:", round(cal2["gap_naive_minus_E_rad"], 6),
          "| -rest sum:", round(-cal2["rest_angle_sum_rad"], 6))
    print("raw extremes from rest:", round(
        cal2["raw_extremes"]["E_raw_from_rest_rad"], 6),
        "| from zero:", cal2["raw_extremes"]["E_raw_from_qpos_zero_rad"])
    print()
    print("=== Calibration 1: clearance ===")
    print("geoms checked:", cal1["n_fly_geoms_checked"],
          "| arena pairs:", cal1["compiled_pairs_involving_arena_geoms"],
          "| arena contacts during sweep:",
          cal1["contacts_involving_arena_geoms_during_sweep"])
    print("global min clearance:", round(cal1["global_min_clearance_mm"], 4),
          "mm | all > 0.02:", cal1["all_clearances_above_margin"])
    for label in ("pedestal", "food"):
        print(f"smallest five vs {label}:")
        for r in cal1["per_geom"][label][:5]:
            print("  ", r["geom"], round(r["min_clearance_mm"], 4),
                  "mm at e =", r["e_at_min"],
                  "| at rest", round(r["clearance_at_rest_mm"], 4))
    print("at/below margin:", cal1["geoms_at_or_below_margin"])
    print("labrum info:", json.dumps(cal1["labrum_distances_for_information"],
                                     indent=1))
    print("wrote", out, "| wall", round(result["wall_clock_s"], 1), "s")


if __name__ == "__main__":
    main()
