"""Unit tests for part5/chain.py (SS4.2 estimator + SS4.3 mapping).

Run with the brain env's pytest (chain.py is pure numpy/math):
  envs/brain/bin/python -m pytest repo/src/closed_loop/tests/test_chain.py

The fake compiled params below carry the pinned artefact's Q0 values
(gate record, execution #5): kp 10 (head group) / 1 (labrum), ks 3,
qpos_spring 0 for all five proboscis DoFs, published ranges from
joints.yaml. They are test fixtures, not code constants -- chain.py
itself reads everything from the params dict it is given.
"""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chain  # noqa: E402

ROS, HAUS, YAW, LAB_L, LAB_R = (chain.ROSTRUM, chain.HAUSTELLUM,
                                chain.YAW, chain.LABRUM_L, chain.LABRUM_R)

PARAMS = {
    ROS: {"kp_gainprm0": 10.0, "jnt_stiffness": 3.0, "qpos_spring": 0.0,
          "yaml_range": [-1.24, 0.183]},
    HAUS: {"kp_gainprm0": 10.0, "jnt_stiffness": 3.0, "qpos_spring": 0.0,
           "yaml_range": [-1.59, 0.7]},
    YAW: {"kp_gainprm0": 10.0, "jnt_stiffness": 3.0, "qpos_spring": 0.0,
          "yaml_range": [-0.0873, 0.0873]},
    LAB_L: {"kp_gainprm0": 1.0, "jnt_stiffness": 3.0, "qpos_spring": 0.0,
            "yaml_range": [-0.00524, 1.05]},
    LAB_R: {"kp_gainprm0": 1.0, "jnt_stiffness": 3.0, "qpos_spring": 0.0,
            "yaml_range": [-0.00524, 1.05]},
}
SIGNS = {ROS: -1, HAUS: -1}
# Settled rests in the shape the gate measured (small offsets from 0).
REST = {ROS: -0.00328, HAUS: -0.00087, YAW: 0.0, LAB_L: 0.0, LAB_R: 0.0}
R_HI_SLICE = 100.0    # the SS6 slice's declared parameter (not calibration)


def make_chain(r_hi=R_HI_SLICE):
    c = chain.FeedingChain(PARAMS, SIGNS, r_lo=5.0, r_hi=r_hi)
    c.set_rest(REST)
    return c


def feed(chain_obj, n_left, n_right, chunks):
    out = None
    for _ in range(chunks):
        out = chain_obj.update(n_left, n_right)
    return out


def test_zero_rate_gives_rest_targets_and_zero_ctrl():
    c = make_chain()
    out = feed(c, 0, 0, 10)
    assert out["r_window_hz"] == 0.0
    assert out["r_filt_hz"] == 0.0
    assert out["e"] == 0.0
    # SS4.3: at e = 0 every driven joint's target is exactly theta_rest,
    # and the ctrl written to the five DoFs is 0.
    for j in chain.PROBOSCIS:
        assert out["targets"][j] == pytest.approx(REST[j], abs=1e-12)
        assert out["ctrls"][j] == 0.0


def test_estimator_startup_rule_reads_true_rate_from_chunk_0():
    c = make_chain()
    # 10 pooled spikes in the first 100 ms chunk = a true 100 Hz rate;
    # the Pass 1 startup rule divides by elapsed time (0.1 s), not 0.5 s.
    out = c.update(5, 5)
    assert out["r_window_hz"] == pytest.approx(100.0)
    assert out["r_filt_hz"] == pytest.approx(chain.EMA_ALPHA * 100.0)
    # The window stays at the true rate while the input is constant,
    # including across the chunk-5 boundary where the full 500 ms
    # trailing window takes over.
    for _ in range(9):
        out = c.update(5, 5)
        assert out["r_window_hz"] == pytest.approx(100.0)


def test_estimator_window_slides():
    est = chain.RateEstimator()
    for _ in range(5):
        est.update(5, 5)                    # 100 Hz for 0.5 s
    r_window, _ = est.update(0, 0)          # one silent chunk
    assert r_window == pytest.approx(80.0)  # 40 spikes / 0.5 s
    for _ in range(4):
        r_window, _ = est.update(0, 0)
    assert r_window == 0.0                  # window fully slid past


def test_ema_alpha_is_the_exact_discretisation():
    assert chain.EMA_ALPHA == pytest.approx(1.0 - math.exp(-0.5),
                                             abs=1e-15)
    assert chain.EMA_ALPHA == pytest.approx(0.3935, abs=1e-3)


def test_monotone_in_rate():
    rates = [0, 20, 40, 60, 80, 100, 120, 140]
    e_steady, ext_steady = [], []
    for rate in rates:
        c = make_chain()
        per_chunk = rate // 10              # spikes per 100 ms chunk
        out = feed(c, per_chunk, 0, 60)     # pooled: split is irrelevant
        e_steady.append(out["e"])
        # steady-state achieved extension predicted by the static map
        achieved = {j: chain.qhat_eff(PARAMS[j], out["ctrls"][j])
                    for j in chain.PITCH_JOINTS}
        ext_steady.append(c.extension_E(achieved))
    assert all(b >= a - 1e-12 for a, b in zip(e_steady, e_steady[1:]))
    assert all(b >= a - 1e-12 for a, b in zip(ext_steady, ext_steady[1:]))
    assert e_steady[0] == 0.0
    assert e_steady[-1] == 1.0              # 140 Hz > r_hi -> saturated


def test_feedforward_endpoint_is_the_range_limit_at_e1():
    c = make_chain()
    out = feed(c, 20, 20, 60)               # 400 Hz pooled: e pinned at 1
    assert out["e"] == 1.0
    # Targets at e = 1 are the Pass 6 achievable extremes...
    assert out["targets"][ROS] == pytest.approx(-0.9538, abs=1e-3)
    assert out["targets"][HAUS] == pytest.approx(-1.2231, abs=1e-3)
    assert out["targets"][LAB_L] == pytest.approx(0.2625, abs=1e-9)
    assert out["targets"][LAB_R] == pytest.approx(0.2625, abs=1e-9)
    # ...and the feedforward commands that achieve them are exactly the
    # published range limits (no clipping short of the limit, no overrun).
    assert out["ctrls"][ROS] == pytest.approx(-1.24, abs=1e-9)
    assert out["ctrls"][HAUS] == pytest.approx(-1.59, abs=1e-9)
    assert out["ctrls"][LAB_L] == pytest.approx(1.05, abs=1e-9)
    assert out["ctrls"][LAB_R] == pytest.approx(1.05, abs=1e-9)


def test_theta_ext_matches_gate_values():
    ext = chain.theta_ext_from_params(PARAMS, SIGNS)
    # Gate record, execution #5 (Pass 6 definition, from compiled values).
    assert ext[ROS] == pytest.approx(-0.9538, abs=1e-3)
    assert ext[HAUS] == pytest.approx(-1.2231, abs=1e-3)
    assert ext[LAB_L] == pytest.approx(0.2625, abs=1e-9)
    assert YAW not in ext                   # yaw held; no theta_ext


def test_yaw_held_at_rest_for_all_e():
    c = make_chain()
    for counts in [(0, 0), (2, 2), (5, 5), (20, 20)]:
        out = feed(c, counts[0], counts[1], 30)
        assert out["targets"][YAW] == pytest.approx(REST[YAW], abs=1e-12)


def test_r_hi_must_be_supplied():
    with pytest.raises(ValueError):
        chain.FeedingChain(PARAMS, SIGNS, r_lo=5.0, r_hi=None)
    with pytest.raises(ValueError):
        chain.FeedingChain(PARAMS, SIGNS, r_lo=5.0, r_hi=5.0)
