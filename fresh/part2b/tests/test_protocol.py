"""Tests for the bridge contract: message round-trips, and the driver
side refusing malformed, out-of-order, or incomplete worker replies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import protocol  # noqa: E402


def _good_counts(chunk=3):
    return {"type": "counts", "chunk": chunk,
            "counts": {name: 0 for name in protocol.COUNT_NAMES},
            "t0_s": 0.3, "t1_s": 0.4}


def test_message_round_trip():
    for msg in (protocol.make_start(4200, 200, 150),
                protocol.make_chunk(3, 100, True),
                protocol.make_end()):
        assert protocol.loads_line(protocol.dumps_line(msg)) == msg


def test_good_counts_reply_validates():
    counts = protocol.validate_counts_reply(_good_counts(), 3)
    assert counts["adn1"] == 0 and counts["total"] == 0


def test_out_of_order_reply_is_refused():
    try:
        protocol.validate_counts_reply(_good_counts(chunk=4), 3)
    except ValueError:
        pass
    else:
        raise AssertionError("out-of-order reply should have raised")


def test_missing_count_is_refused():
    msg = _good_counts()
    del msg["counts"]["jon_all"]
    try:
        protocol.validate_counts_reply(msg, 3)
    except ValueError:
        pass
    else:
        raise AssertionError("incomplete counts should have raised")


def test_worker_error_surfaces_as_runtime_error():
    try:
        protocol.validate_counts_reply(
            {"type": "error", "message": "boom"}, 3)
    except RuntimeError as exc:
        assert "boom" in str(exc)
    else:
        raise AssertionError("worker error should have raised")


def test_garbage_line_is_refused():
    for bad in ("not json", "[1, 2]", '{"no_type": true}'):
        try:
            protocol.loads_line(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{bad!r} should have raised")
