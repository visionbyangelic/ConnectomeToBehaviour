"""The bridge contract between the body-side driver and the brain worker.

The brain (Brian2, numpy 1.26.4) and the body (FlyGym/MuJoCo, numpy
2.5.5) live in two different Python environments that cannot import each
other's libraries, so the loop crosses the boundary as processes: the
driver (body env) spawns the brain worker (brain env) and they exchange
one JSON object per line over the worker's stdin/stdout. This module is
the shared schema -- both sides import it, and the tests pin it, so the
two processes cannot quietly drift into speaking different protocols.

Messages, driver -> worker:
  {"type": "start", "seed": int, "sugar_rate_hz": float,
   "jon_rate_hz": float}
  {"type": "chunk", "chunk": int, "duration_ms": int, "jon_on": bool}
  {"type": "end"}

Messages, worker -> driver:
  {"type": "ready", "populations": {name: n_neurons, ...}}
  {"type": "counts", "chunk": int, "counts": {name: int, ...},
   "t0_s": float, "t1_s": float}
  {"type": "bye"}
  {"type": "error", "message": str}     -- worker exits non-zero after

Rules: stdout carries protocol lines only (worker logs go to stderr);
every line is a complete JSON object; a "counts" reply must answer the
chunk that was asked for, in order -- the driver never pipelines.
"""

import json

COUNT_NAMES = ("adn1", "adn2_left", "abn1", "jon_all", "sugar_grn_right",
               "mn9_left", "mn9_right", "total")


def dumps_line(message):
    return json.dumps(message) + "\n"


def loads_line(line):
    try:
        obj = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ValueError(f"protocol line is not JSON: {line!r}") from exc
    if not isinstance(obj, dict) or "type" not in obj:
        raise ValueError(f"protocol message lacks a 'type': {obj!r}")
    return obj


def make_start(seed, sugar_rate_hz, jon_rate_hz):
    return {"type": "start", "seed": int(seed),
            "sugar_rate_hz": float(sugar_rate_hz),
            "jon_rate_hz": float(jon_rate_hz)}


def make_chunk(chunk, duration_ms, jon_on):
    return {"type": "chunk", "chunk": int(chunk),
            "duration_ms": int(duration_ms), "jon_on": bool(jon_on)}


def make_end():
    return {"type": "end"}


def validate_counts_reply(message, expected_chunk):
    """Check a worker 'counts' reply against the contract. Returns the
    counts dict. Raises ValueError on any mismatch -- a bridge that
    silently accepts a malformed reply would manufacture loop results."""
    if message.get("type") == "error":
        raise RuntimeError(f"brain worker reported an error: "
                           f"{message.get('message')}")
    if message.get("type") != "counts":
        raise ValueError(f"expected a 'counts' reply, got {message!r}")
    if message.get("chunk") != expected_chunk:
        raise ValueError(f"counts reply is for chunk "
                         f"{message.get('chunk')}, expected "
                         f"{expected_chunk} (replies must be in order)")
    counts = message.get("counts")
    if not isinstance(counts, dict):
        raise ValueError(f"'counts' is not an object: {message!r}")
    missing = [n for n in COUNT_NAMES if n not in counts]
    if missing:
        raise ValueError(f"counts reply is missing {missing}")
    for name, value in counts.items():
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"count {name}={value!r} is not a "
                             f"non-negative int")
    return counts
