"""Shared machinery for the qualification-gate FIFTH execution (rerun5).

Specification: PART4-SENSORY-SPECS.md as amended by Passes 1-3, 5 and 6
AS REVISED. The difference from gate_common3.py (third execution):

- The SS4.3 chain's extension extremes are the ACHIEVABLE extremes
  (Amendment Pass 6 revised): for each driven proboscis DoF,
  theta_ext = qhat_eff at the published range limit in the extension
  direction, computed from the compiled artefact's parameters via the
  clamped static map -- rostrum pitch ~ -0.954 rad, haustellum pitch
  ~ -1.223 rad, labrum pitches ~ +0.2625 rad. The e -> theta
  interpolation spans theta_rest -> theta_ext, and the feedforward
  command at e = 1 equals the published range limit exactly; no
  clipping occurs in normal operation. The 0.05 rad range safety
  margin is RETIRED for extension targets. (The third execution's
  chain aimed at margin-adjusted intended angles, -1.19 / -1.54 /
  1.00 rad, whose feedforward commands exceed the ranges and clip --
  the decoder dead zone Pass 6 removed.)
- Everything else (compiled-parameter reading per Pass 5, corrected
  labrum geom names, food-specific contact forces from the contact
  array) is inherited from gate_common3 / gate_common unchanged.
"""

from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import PITCH_JOINTS, PROBOSCIS, RANGES  # noqa: E402
from gate_common3 import (  # noqa: E402
    RESULTS, compiled_params, extension_E, feedforward_ctrl, qhat_eff,
)

LABRUM_JOINTS = ("c_haustellum-l_labrum-pitch",
                 "c_haustellum-r_labrum-pitch")
YAW_JOINT = "c_rostrum-c_haustellum-yaw"
DRIVEN_JOINTS = PITCH_JOINTS + list(LABRUM_JOINTS)


def theta_ext_from_params(params, signs):
    """Pass 6 achievable extremes for the four driven proboscis DoFs.

    theta_ext(j) = qhat_eff(params[j], range end in the extension
    direction): the pitch joints extend toward the end their Q2 sign
    names; the labrum joints extend toward their positive (opening)
    end. Computed from the compiled artefact's parameters -- the
    analytic rule is the object, never a fitted or copied constant.
    """
    ext = {}
    for j in PITCH_JOINTS:
        end = RANGES[j][0] if signs[j] < 0 else RANGES[j][1]
        ext[j] = qhat_eff(params[j], end)
    for j in LABRUM_JOINTS:
        ext[j] = qhat_eff(params[j], RANGES[j][1])
    return ext


def chain_targets_rev(e, rest, theta_ext):
    """SS4.3 target functions (Pass 6 revised) at command e.

    Each driven DoF interpolates theta_rest -> theta_ext; haustellum
    yaw is held at its settled rest value for all e.
    """
    targets = {j: rest[j] + e * (theta_ext[j] - rest[j])
               for j in DRIVEN_JOINTS}
    targets[YAW_JOINT] = rest[YAW_JOINT]
    return targets


def chain_ctrl_rev(base_ctrl, idx, params, e, rest, theta_ext):
    """Ctrl vector for the five proboscis DoFs under the revised chain.

    At e = 0 the chain writes ctrl = 0 to the five DoFs (SS4.3); for
    e > 0 each DoF's ctrl is the feedforward inverse of its target.
    All other entries of base_ctrl are left untouched.
    """
    ctrl = np.array(base_ctrl, dtype=float)
    if e == 0:
        for j in PROBOSCIS:
            ctrl[idx[j]] = 0.0
        return ctrl
    targets = chain_targets_rev(e, rest, theta_ext)
    for j in PROBOSCIS:
        ctrl[idx[j]] = feedforward_ctrl(params[j], targets[j])
    return ctrl


def predicted_E_rev(params, rest, signs, theta_ext, e):
    """Map-predicted achieved E at command e under the revised chain."""
    targets = chain_targets_rev(e, rest, theta_ext)
    achieved = {}
    for j in PITCH_JOINTS:
        ctrl = 0.0 if e == 0 else feedforward_ctrl(params[j], targets[j])
        achieved[j] = qhat_eff(params[j], ctrl)
    return extension_E(achieved, rest, signs)
