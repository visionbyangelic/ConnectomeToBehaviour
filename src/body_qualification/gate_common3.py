"""Shared machinery for the qualification-gate THIRD execution (rerun3).

Specification: PART4-SENSORY-SPECS.md as amended by Passes 1-3 and 5
(Pass 4 withdrawn). The difference from gate_common.py (second execution):

- The §4.3 static map's parameters (kp, ks, spring reference) are read from
  the COMPILED artefact (Amendment Pass 5): kp from the compiled actuator
  gainprm, ks from the compiled jnt_stiffness, ref from the compiled
  qpos_spring -- never from the YAML files. The YAMLs supply the published
  ranges that the criteria cite (Q0 verifies the compiled ctrlrange equals
  the YAML range for the five proboscis actuators).
- labrum_tip_pos uses the correct labrum geoms (l_labrum_lower /
  r_labrum_lower). gate_common.labrum_tip_pos names geoms "l_labrum" /
  "r_labrum", which resolve to id -1 in this model; the second execution's
  record documents that defect and its corrected re-measurement.
- Food-geom contact forces are computed from the MuJoCo contact array
  (mj_contactForce) filtered by geom id: the packaged
  get_bodysegment_contact_forces cannot address the labrum (it is not a
  registered BodySegment in FlyBody's anatomy) and cannot filter by a
  single non-ground geom, while SS4.5 requires forces tested against the
  food geom only. Same underlying contact reporting, food-specific filter.
"""

from pathlib import Path

import mujoco as mj
import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (  # noqa: E402
    CHUNK_STEPS, EPS, MODEL_DIR, NECK, PITCH_JOINTS, PROBOSCIS, RANGES,
    build_sim, dof_index, settle, thorax_z,
)

RESULTS = Path(__file__).resolve().parents[2] / "results" / "body_qualification"
LABRUM_GEOM_NAMES = ("flybody/l_labrum_lower", "flybody/r_labrum_lower")
FRONT_TARSUS_BODIES = tuple(
    f"flybody/{leg}_tarsus{n}" for leg in ("lf", "rf") for n in range(1, 6)
)


def compiled_params(sim):
    """Per-joint compiled parameters for the proboscis + neck joints.

    Returns {joint: dict} with the published (YAML) range, the compiled
    ctrlrange/jnt_range, kp = actuator gainprm[0], biasprm[1], ks =
    jnt_stiffness, ref_spring = qpos_spring, qpos0, solref, solimp.
    """
    m = sim.mj_model
    out = {}
    for joint in PROBOSCIS + NECK:
        jid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_JOINT, f"flybody/{joint}")
        aid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_ACTUATOR,
                            f"flybody/{joint}-position")
        qadr = int(m.jnt_qposadr[jid])
        out[joint] = {
            "joint_id": int(jid), "actuator_id": int(aid),
            "yaml_range": [float(x) for x in RANGES[joint]],
            "compiled_jnt_range": [float(x) for x in m.jnt_range[jid]],
            "actuator_ctrlrange": [float(x) for x in m.actuator_ctrlrange[aid]],
            "ctrllimited": bool(m.actuator_ctrllimited[aid]),
            "kp_gainprm0": float(m.actuator_gainprm[aid][0]),
            "biasprm1": float(m.actuator_biasprm[aid][1]),
            "neg_biasprm1": float(-m.actuator_biasprm[aid][1]),
            "jnt_stiffness": float(m.jnt_stiffness[jid]),
            "qpos_spring": float(m.qpos_spring[qadr]),
            "qpos0": float(m.qpos0[qadr]),
            "jnt_solref": [float(x) for x in m.jnt_solref[jid]],
            "jnt_solimp": [float(x) for x in m.jnt_solimp[jid]],
        }
    return out


def qhat(p, ctrl):
    """Unclamped static map (SS4.3) from compiled parameters."""
    kp, ks, ref = p["kp_gainprm0"], p["jnt_stiffness"], p["qpos_spring"]
    return (kp * ctrl + ks * ref) / (kp + ks)


def qhat_eff(p, ctrl):
    """Clamped static map (SS4.3): qhat limited to the published range."""
    lo, hi = p["yaml_range"]
    return float(min(max(qhat(p, ctrl), lo), hi))


def feedforward_ctrl(p, theta_intended):
    """Inverse map (SS4.3): ctrl achieving the intended angle, range-clipped."""
    kp, ks, ref = p["kp_gainprm0"], p["jnt_stiffness"], p["qpos_spring"]
    ctrl = ((kp + ks) * theta_intended - ks * ref) / kp
    lo, hi = p["yaml_range"]
    return float(min(max(ctrl, lo), hi))


def labrum_tip_pos(sim):
    """Mean of the two labrum geom centres (correct geom names; see header)."""
    m = sim.mj_model
    pts = []
    for name in LABRUM_GEOM_NAMES:
        gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, name)
        assert gid >= 0, f"labrum geom not found: {name}"
        pts.append(sim.mj_data.geom_xpos[gid])
    return np.mean(pts, axis=0)


def extension_E(angles_by_joint, rest, signs):
    """SS4.4 extension angle from a {joint: angle} mapping."""
    return float(sum(signs[j] * (angles_by_joint[j] - rest[j])
                     for j in PITCH_JOINTS))


def chain_targets(e, rest, signs, theta_ext):
    """SS4.3 target functions at command e, for the five proboscis DoFs."""
    targets = {}
    for j in PITCH_JOINTS:
        targets[j] = rest[j] + e * (theta_ext[j] - rest[j])
    for j in ("c_haustellum-l_labrum-pitch", "c_haustellum-r_labrum-pitch"):
        targets[j] = rest[j] + e * (1.00 - rest[j])
    targets["c_rostrum-c_haustellum-yaw"] = rest["c_rostrum-c_haustellum-yaw"]
    return targets


def chain_ctrl(base_ctrl, idx, params, e, rest, signs, theta_ext):
    """Ctrl vector for the five proboscis DoFs under the SS4.3 chain.

    At e = 0 the chain writes ctrl = 0 to the five DoFs (SS4.3); for e > 0
    each DoF's ctrl is the feedforward inverse of its target. All other
    entries of base_ctrl are left untouched.
    """
    ctrl = np.array(base_ctrl, dtype=float)
    if e == 0:
        for j in PROBOSCIS:
            ctrl[idx[j]] = 0.0
        return ctrl
    targets = chain_targets(e, rest, signs, theta_ext)
    for j in PROBOSCIS:
        ctrl[idx[j]] = feedforward_ctrl(params[j], targets[j])
    return ctrl


def predicted_E(params, rest, signs, theta_ext, e):
    """Map-predicted achieved E at command e (SS7.4(i) reference value)."""
    targets = chain_targets(e, rest, signs, theta_ext)
    achieved = {}
    for j in PITCH_JOINTS:
        ctrl = 0.0 if e == 0 else feedforward_ctrl(params[j], targets[j])
        achieved[j] = qhat_eff(params[j], ctrl)
    return float(sum(signs[j] * (achieved[j] - rest[j]) for j in PITCH_JOINTS))


def geom_ids_for_bodies(sim, body_names):
    m = sim.mj_model
    bids = {mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, b) for b in body_names}
    return {g for g in range(m.ngeom) if int(m.geom_bodyid[g]) in bids}


def food_contact_forces(sim, food_gid, labrum_gids, tarsus_gids):
    """Food-specific contact force magnitudes from the contact array.

    Returns (labrum_N, front_tarsus_N): summed |force| over contacts between
    the food geom and the labrum geoms / front-tarsus geoms respectively.
    This is the body's own MuJoCo contact reporting (mj_contactForce on
    mj_data.contact), filtered to the food geom as SS4.5 requires.
    """
    m, d = sim.mj_model, sim.mj_data
    labrum_f = 0.0
    tarsus_f = 0.0
    wrench = np.zeros(6)
    for i in range(d.ncon):
        g1, g2 = int(d.contact.geom1[i]), int(d.contact.geom2[i])
        if food_gid not in (g1, g2):
            continue
        other = g2 if g1 == food_gid else g1
        mj.mj_contactForce(m, d, i, wrench)
        mag = float(np.linalg.norm(wrench[:3]))
        if other in labrum_gids:
            labrum_f += mag
        elif other in tarsus_gids:
            tarsus_f += mag
    return labrum_f, tarsus_f
