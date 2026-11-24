"""Unit tests for the Part 5 closed loop's shared logic.

Run with the brain env's pytest (loop_protocol.py is pure stdlib):
  envs/brain/bin/python -m pytest repo/src/closed_loop/tests/test_loop.py

Covered here: the SS4.5 gating function (all five modes, both gates
always reported), scenario validation and the SS3 envelope labels,
and the bridge contract's reply validation. The manifest test reads a
produced smoke-run directory when one exists (SS6.1(3) record rules)
and skips otherwise -- the manifest is built by the driver in the body
env, which this test process cannot import.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import loop_protocol as lp  # noqa: E402

RUNS = Path(__file__).resolve().parents[3] / "results" / "closed_loop"


def scenario(**overrides):
    base = {"name": "T", "n_chunks": 10, "seed": 1,
            "drives": [{"name": "sugar",
                        "populations": ["sugar_grn_right"],
                        "rate_hz": 200.0, "mode": "event_or_window",
                        "window": [[0, 2]]}]}
    base.update(overrides)
    return base


# ----------------------------------------------------------------------
# gating (SS4.5)
# ----------------------------------------------------------------------

def test_gate_event_mode_follows_event_only():
    assert lp.gate_state("event", 0, True, [])["applied"] is True
    assert lp.gate_state("event", 0, False, [[0, 9]])["applied"] is False


def test_gate_window_mode_follows_window_only():
    assert lp.gate_state("window", 1, False, [[0, 2]])["applied"] is True
    assert lp.gate_state("window", 5, True, [[0, 2]])["applied"] is False


def test_gate_event_or_window_either_gate_applies():
    assert lp.gate_state("event_or_window", 1, False,
                         [[0, 2]])["applied"] is True
    assert lp.gate_state("event_or_window", 5, True,
                         [[0, 2]])["applied"] is True
    assert lp.gate_state("event_or_window", 5, False,
                         [[0, 2]])["applied"] is False


def test_gate_always_on_and_off():
    assert lp.gate_state("always_on", 0, False, [])["applied"] is True
    assert lp.gate_state("off", 0, True, [[0, 9]])["applied"] is False


def test_gate_both_gates_always_reported():
    state = lp.gate_state("event", 1, True, [[0, 2]])
    assert state == {"event_gate": True, "window_gate": True,
                     "applied": True}
    state = lp.gate_state("off", 7, False, [[0, 2]])
    assert state == {"event_gate": False, "window_gate": False,
                     "applied": False}


def test_window_bounds_are_inclusive():
    assert lp.in_window([[2, 4]], 2) and lp.in_window([[2, 4]], 4)
    assert not lp.in_window([[2, 4]], 1) and not lp.in_window([[2, 4]], 5)
    assert lp.in_window([[0, 1], [5, 5]], 5)


def test_gate_unknown_mode_raises():
    with pytest.raises(ValueError):
        lp.gate_state("sometimes", 0, False, [])


# ----------------------------------------------------------------------
# scenario validation + envelope labels (SS2.2, SS3)
# ----------------------------------------------------------------------

def test_validate_scenario_fills_defaults_and_labels_validated():
    out = lp.validate_scenario(scenario())
    assert out["readouts"] == list(lp.DEFAULT_READOUTS)
    assert out["drives"][0]["envelope"] == lp.VALIDATED_LABEL


@pytest.mark.parametrize("pops,rate", [
    (["sugar_grn_left"], 200.0),
    (["sugar_grn_right", "sugar_grn_left"], 200.0),
    (["bitter_grn"], 200.0),
    (["water_grn"], 200.0),
    (["sugar_grn_right"], 150.0),
])
def test_envelope_outside_for_non_sugarR_configurations(pops, rate):
    s = scenario(drives=[{"name": "d", "populations": pops,
                          "rate_hz": rate, "mode": "window",
                          "window": [[0, 1]]}])
    out = lp.validate_scenario(s)
    assert out["drives"][0]["envelope"] == lp.OUTSIDE_LABEL


@pytest.mark.parametrize("bad", [
    # JON is not a drivable set in the feeding loop (SS5 pathway)
    {"drives": [{"name": "x", "populations": ["jon_all"],
                 "rate_hz": 150.0, "mode": "event"}]},
    # Ir94e is not driven in v1 (SS3.3)
    {"drives": [{"name": "x", "populations": ["ir94e_grn"],
                 "rate_hz": 200.0, "mode": "event"}]},
    {"drives": [{"name": "x", "populations": ["sugar_grn_right"],
                 "rate_hz": 200.0, "mode": "sometimes"}]},
    {"drives": [{"name": "x", "populations": ["sugar_grn_right"],
                 "rate_hz": 200.0, "mode": "event"},
                {"name": "x", "populations": ["bitter_grn"],
                 "rate_hz": 200.0, "mode": "event"}]},   # duplicate name
    {"drives": [{"name": "x", "populations": ["sugar_grn_right"],
                 "rate_hz": 200.0, "mode": "window",
                 "window": [[4, 2]]}]},                   # reversed range
    {"drives": [{"name": "x", "populations": ["sugar_grn_right"],
                 "rate_hz": -1.0, "mode": "event"}]},
    {"n_chunks": 0},
    {"seed": "not-an-int"},
    {"drives": []},
])
def test_validate_scenario_rejects(bad):
    with pytest.raises(ValueError):
        lp.validate_scenario(scenario(**bad))


# ----------------------------------------------------------------------
# bridge reply validation
# ----------------------------------------------------------------------

def good_reply(chunk=3):
    return {"type": "counts", "chunk": chunk,
            "counts": {"total": 5, "mn9_left": 1, "mn9_right": 0},
            "applied": {"sugar": {"event_gate": False,
                                  "window_gate": True,
                                  "applied": True}},
            "taste_event_received": False, "t0_s": 0.3, "t1_s": 0.4}


def test_validate_counts_reply_accepts_good():
    out = lp.validate_counts_reply(good_reply(), 3, ["sugar"],
                                   ["total", "mn9_left", "mn9_right"])
    assert out["counts"]["mn9_left"] == 1


def test_validate_counts_reply_rejects_wrong_chunk():
    with pytest.raises(ValueError):
        lp.validate_counts_reply(good_reply(chunk=4), 3, ["sugar"],
                                 ["total"])


def test_validate_counts_reply_rejects_missing_readout():
    reply = good_reply()
    del reply["counts"]["mn9_right"]
    with pytest.raises(ValueError):
        lp.validate_counts_reply(reply, 3, ["sugar"],
                                 ["total", "mn9_right"])


def test_validate_counts_reply_rejects_missing_gate():
    reply = good_reply()
    del reply["applied"]["sugar"]["window_gate"]
    with pytest.raises(ValueError):
        lp.validate_counts_reply(reply, 3, ["sugar"], ["total"])


def test_validate_counts_reply_surfaces_worker_error():
    with pytest.raises(RuntimeError):
        lp.validate_counts_reply({"type": "error", "message": "boom"},
                                 3, ["sugar"], ["total"])


# ----------------------------------------------------------------------
# manifest completeness (SS6.1(3)) on a produced smoke run, if present
# ----------------------------------------------------------------------

def latest_smoke_manifest():
    if not RUNS.exists():
        return None
    manifests = sorted(RUNS.glob("*/manifest.json"))
    return manifests[-1] if manifests else None


@pytest.mark.skipif(latest_smoke_manifest() is None,
                    reason="no Part 5 run directory produced yet")
def test_manifest_completeness():
    path = latest_smoke_manifest()
    manifest = json.loads(path.read_text())
    # frozen ctb commit + tag, with the git status stated, not tidied
    assert manifest["git"]["head"] == manifest["ctb_freeze"][
        "expected_commit"]
    assert manifest["ctb_freeze"]["expected_tag"] in \
        manifest["git"]["tags_at_head"]
    assert "status_porcelain" in manifest["git"]
    # data hashes from the verifying loader
    assert set(manifest["data_hashes"]) == {
        "2023_03_23_completeness_630_final.csv",
        "2023_03_23_connectivity_630_final.parquet"}
    # SS2.2 declared drives + envelope labels
    assert manifest["declared_drives_SS2.2"]
    assert manifest["envelope_labels"]
    # configuration: r_hi WITH its provenance label
    cfg = manifest["configuration"]
    assert cfg["r_hi_hz"] > cfg["r_lo_hz"]
    assert cfg["r_hi_provenance"]
    # settle record + episode validity are recorded either way
    assert "settled" in manifest["settle"]
    assert manifest["episode_validity"] in ("VALID", "INVALID")
    # per-chunk applied drives: both gates, every chunk, in the log
    log_lines = (path.parent / manifest["logs"]["brain"]).read_text() \
        .splitlines()
    if manifest["episode_validity"] == "VALID":
        assert len(log_lines) == manifest["scenario"]["n_chunks"]
        for line in log_lines:
            reply = json.loads(line)
            for state in reply["applied"].values():
                assert set(state) == {"event_gate", "window_gate",
                                      "applied"}
