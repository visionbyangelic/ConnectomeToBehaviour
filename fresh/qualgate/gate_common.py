"""Shared machinery for the qualification-gate re-run (Passes 1-3 spec).

Everything here reads the body's numbers from the pinned package files at
run time (joints.yaml / actuators.yaml in the installed FlyGym 2.1.1), never
from constants copied into this file, so the gate judges the artefact that
Q0 hash-verified. The constructions are the Part 1b Demo C construction
(q1_upstream_integrity.build_flybody), with labrum adhesion actuators added
for Q2-Q6 (the shipped default configuration, §4.3; ctrl held 0 wherever
adhesion must be off).
"""

from pathlib import Path

import mujoco as mj
import numpy as np
import yaml

import flygym
from flygym.compose import ActuatorType
from flygym.compose.world.flat_ground import FlatGroundWorld
from flygym.simulation import Simulation
from flygym.utils.math import Rotation3D

import sys

sys.path.insert(0, str(Path(__file__).parent))
from q1_upstream_integrity import build_flybody  # noqa: E402

MODEL_DIR = Path(flygym.__file__).parent / "assets" / "model" / "flybody"

PROBOSCIS = [
    "c_head-c_rostrum-pitch",
    "c_rostrum-c_haustellum-pitch",
    "c_rostrum-c_haustellum-yaw",
    "c_haustellum-l_labrum-pitch",
    "c_haustellum-r_labrum-pitch",
]
PITCH_JOINTS = ["c_head-c_rostrum-pitch", "c_rostrum-c_haustellum-pitch"]
NECK = ["c_thorax-c_head-pitch", "c_thorax-c_head-roll", "c_thorax-c_head-yaw"]
EPS = 0.005  # joint-limit numerical-noise allowance, §7.2/§7.3(ii)
CHUNK_STEPS = 1000  # 100 ms at dt = 1e-4 s


def load_pinned_params():
    """Ranges, servo gains, spring stiffness and springrefs from the pinned YAMLs."""
    j = yaml.safe_load((MODEL_DIR / "joints.yaml").read_text())
    a = yaml.safe_load((MODEL_DIR / "actuators.yaml").read_text())
    ranges = {k: (float(v["range"][0]), float(v["range"][1]))
              for k, v in j["ranges"].items()}
    springref = {k: float(v["springref"]) for k, v in j["ranges"].items()
                 if "springref" in v}
    stiffness = {}
    for spec in j["params"].values():
        if "stiffness" in spec:
            for name in spec["apply_to"]:
                stiffness[name] = float(spec["stiffness"])
    kp = {}
    for spec in a.values():
        for name in spec["apply_to"]:
            kp[name] = float(spec["general"]["gainprm"])
    return ranges, kp, stiffness, springref


RANGES, KP, KS, SPRINGREF = load_pinned_params()


def qhat(joint, ctrl):
    """Unclamped static map (§4.3): servo/spring force balance."""
    kp, ks = KP[joint], KS[joint]
    ref = SPRINGREF.get(joint, 0.0)
    return (kp * ctrl + ks * ref) / (kp + ks)


def qhat_eff(joint, ctrl):
    """Clamped static map (§4.3, Amendment Pass 3): qhat limited to the range."""
    lo, hi = RANGES[joint]
    return float(min(max(qhat(joint, ctrl), lo), hi))


def feedforward_ctrl(joint, theta_intended):
    """Inverse map (§4.3): ctrl that achieves the intended angle, range-clipped."""
    kp, ks = KP[joint], KS[joint]
    ref = SPRINGREF.get(joint, 0.0)
    ctrl = ((kp + ks) * theta_intended - ks * ref) / kp
    lo, hi = RANGES[joint]
    return float(min(max(ctrl, lo), hi))


def build_sim(with_adhesion=False, world=None):
    """Demo C construction + Simulation on flat ground, spawned as in Q1."""
    fly = build_flybody()
    if with_adhesion:
        fly.add_leg_adhesion()  # shipped defaults: leg gain 0.985, labrum 1.0
    if world is None:
        world = FlatGroundWorld()
    world.add_fly(fly, (0, 0, 1.0), Rotation3D("quat", (1, 0, 0, 0)))
    sim = Simulation(world)
    sim.reset()
    return fly, world, sim


def dof_index(fly):
    """Joint-DoF name -> index in the POSITION order used by get_joint_angles."""
    order = fly.get_actuated_jointdofs_order(ActuatorType.POSITION)
    return {d.name: i for i, d in enumerate(order)}, order


def thorax_z(sim):
    return float(sim.mj_data.xpos[
        mj.mj_name2id(sim.mj_model, mj.mjtObj.mjOBJ_BODY, "flybody/c_thorax"), 2])


def labrum_tip_pos(sim):
    """Mean of the two labrum geom centres (the body ships no sites; §7.3's
    'site position' is read from the labrum geoms, whose centres are fixed in
    the labrum bodies and offset from the pitch axes)."""
    m = sim.mj_model
    pts = []
    for seg in ("l_labrum", "r_labrum"):
        gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, f"flybody/{seg}")
        pts.append(sim.mj_data.geom_xpos[gid])
    return np.mean(pts, axis=0)


def settle(sim, fly, ctrl, *, max_chunks=30, food_check=None):
    """§2.3 settle under a constant ctrl vector (zero command for the gate).

    Steps in 100 ms chunks; per chunk counts leg ground-contact transitions
    (all six legs, flag changes between consecutive physics steps) and the
    thorax height range. Settled when 3 consecutive chunks each have
    transitions <= 2 and thorax height change <= 0.01 mm. If food_check is
    given (a callable returning True when a qualifying food contact exists),
    any food contact during warmup marks the episode invalid (§2.3 feeding
    addition) and is reported.
    """
    idx, _ = dof_index(fly)
    sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
    prev_flags = None
    chunks = []
    good_streak = 0
    food_contact_seen = False
    for c in range(max_chunks):
        transitions = 0
        heights = []
        for _ in range(CHUNK_STEPS):
            sim.step()
            flags = sim.get_ground_contact_info(fly.name)[0] > 0
            if prev_flags is not None:
                transitions += int(np.count_nonzero(flags != prev_flags))
            prev_flags = flags
            heights.append(thorax_z(sim))
            if food_check is not None and food_check():
                food_contact_seen = True
        heights = np.array(heights)
        dh = float(heights.max() - heights.min())
        ok = transitions <= 2 and dh <= 0.01
        chunks.append({"chunk": c, "transitions": transitions,
                       "thorax_dh_mm": dh, "ok": bool(ok)})
        good_streak = good_streak + 1 if ok else 0
        if good_streak >= 3:
            break
    angles = sim.get_joint_angles(fly.name)
    rest = {name: float(angles[i]) for name, i in idx.items()}
    return {
        "settled": good_streak >= 3,
        "n_chunks": len(chunks),
        "chunks": chunks,
        "rest_angles": rest,
        "food_contact_during_warmup": food_contact_seen,
    }
