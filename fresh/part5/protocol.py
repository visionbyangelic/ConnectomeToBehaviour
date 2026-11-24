"""The thin-slice bridge contract (SS6), in the Part 2b bridge's form.

SS6 requires the slice to run through the SAME bridge as Part 2b: two
processes, one JSON object per line, 100 ms chunks, every reply
answering the chunk that was asked for, in order, and the driver
refusing malformed replies rather than manufacturing results. The
Part 2b schema itself (part2b/protocol.py) is brain-specific -- it
carries Brian2 spike counts for named populations -- so this module
states the slice's instance of the same contract: the brain side is a
stub (stub_worker.py) that emits a scripted, SYNTHETIC pooled MN9
rate (as seeded Poisson counts) and receives the SS4.5 taste-event
state back. The stub is not brain output and impersonates none.

Messages, driver -> worker:
  {"type": "start", "seed": int, "n_chunks": int,
   "profile": {...}, "log_path": str}
  {"type": "chunk", "chunk": int, "duration_ms": int,
   "taste_event": bool}
  {"type": "end"}

Messages, worker -> driver:
  {"type": "ready", "n_chunks": int, "profile": {...}}
  {"type": "rate", "chunk": int, "scripted_rate_hz": float,
   "counts": {"mn9_left": int, "mn9_right": int},
   "taste_event_received": bool}
  {"type": "bye"}
  {"type": "error", "message": str}     -- worker exits non-zero after

The "taste_event" a chunk request carries is the SS4.5 event state at
the end of the PREVIOUS body chunk (SS2.1: exactly one chunk of
feedback latency); the worker logs it in its brain-side stub log
against that chunk number, which is what SS6 criterion (iv) judges.
"""

import json


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


def make_start(seed, n_chunks, profile, log_path):
    return {"type": "start", "seed": int(seed),
            "n_chunks": int(n_chunks), "profile": profile,
            "log_path": str(log_path)}


def make_chunk(chunk, duration_ms, taste_event):
    return {"type": "chunk", "chunk": int(chunk),
            "duration_ms": int(duration_ms),
            "taste_event": bool(taste_event)}


def make_end():
    return {"type": "end"}


def validate_rate_reply(message, expected_chunk):
    """Check a worker 'rate' reply against the contract. Returns the
    reply dict. Raises on any mismatch -- same discipline as
    part2b/protocol.py's validate_counts_reply."""
    if message.get("type") == "error":
        raise RuntimeError(f"stub worker reported an error: "
                           f"{message.get('message')}")
    if message.get("type") != "rate":
        raise ValueError(f"expected a 'rate' reply, got {message!r}")
    if message.get("chunk") != expected_chunk:
        raise ValueError(f"rate reply is for chunk "
                         f"{message.get('chunk')}, expected "
                         f"{expected_chunk} (replies must be in order)")
    rate = message.get("scripted_rate_hz")
    if not isinstance(rate, (int, float)) or rate < 0:
        raise ValueError(f"scripted_rate_hz is not a non-negative "
                         f"number: {message!r}")
    counts = message.get("counts")
    if not isinstance(counts, dict):
        raise ValueError(f"'counts' is not an object: {message!r}")
    for name in ("mn9_left", "mn9_right"):
        value = counts.get(name)
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"count {name}={value!r} is not a "
                             f"non-negative int")
    if not isinstance(message.get("taste_event_received"), bool):
        raise ValueError(f"'taste_event_received' is not a bool: "
                         f"{message!r}")
    return message
