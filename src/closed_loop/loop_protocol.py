"""The Part 5 closed-loop bridge contract + scenario/gating logic.

The Part 5 feeding loop crosses the same process boundary as Part 2b
and the SS6 slice: the driver (body env: FlyGym / MuJoCo / numpy 2.5.5)
spawns the brain worker (brain env: Brian2 / numpy 1.26.4) and the two
exchange one JSON object per line over the worker's stdin/stdout --
replies in order, answering the chunk that was asked for, malformed
replies refused rather than manufactured into results. This module is
the shared schema AND the shared stimulus logic: the scenario format,
its validation, and the per-chunk gating function live here in pure
stdlib Python, so the worker, the driver and the unit tests all run
the identical code and the two processes cannot drift apart.

Scenario format (a JSON object; declared in full before any run, per
SS2.2 -- every population any part of the run can drive is in the
manifest before the episode clock starts):

  {"name": str, "n_chunks": int, "seed": int,
   "drives": [{"name": str,                  # gate name, e.g. "sugar"
               "populations": [str, ...],    # Part 2 ID-set names
               "rate_hz": float,             # SS3: 200 gustatory
               "mode": "event" | "window" | "event_or_window"
                       | "always_on" | "off",
               "window": [[a, b], ...]},     # inclusive chunk ranges,
                                             # for the window modes
              ...],
   "readouts": [str, ...]}                   # optional; default below

Gating (SS4.5): a drive's applied state for brain chunk k is decided
from (a) the SS4.5 taste-event state at the end of body chunk k-1 --
the "event gate", carried by the chunk message -- and (b) the
scenario's scripted window -- the "window gate". The modes combine
them: "event" = event gate only; "window" = window gate only;
"event_or_window" = either (the SS4.5 two-gates case: a scripted
ignition window plus event gating, both logged separately so an
open-loop arm is never confused with the closed loop); "always_on";
"off" (declared under SS2.2 and warmed up, never applied).

Envelope labels (SS3, Amendment Pass 1): Part 3 certified exactly one
stimulus configuration -- sugar_grn_right at 200 Hz. A drive entry
whose population set is exactly ["sugar_grn_right"] at 200 Hz is
labelled VALIDATED; every other gustatory configuration (left,
bilateral, bitter, water, any combination) is labelled OUTSIDE THE
VALIDATED ENVELOPE, and the label travels into the run manifest.

Messages, driver -> worker:
  {"type": "start", "scenario": {...}}
  {"type": "chunk", "chunk": int, "duration_ms": int,
   "taste_event": bool}
  {"type": "end"}

Messages, worker -> driver:
  {"type": "ready", "populations": {name: n, ...},
   "data_hashes": {filename: sha256, ...},
   "declared_drives": [...], "readouts": [...]}
  {"type": "counts", "chunk": int, "counts": {name: int, ...},
   "applied": {drive_name: {"event_gate": bool, "window_gate": bool,
                            "applied": bool}, ...},
   "taste_event_received": bool, "t0_s": float, "t1_s": float}
  {"type": "bye"}
  {"type": "error", "message": str}     -- worker exits non-zero after
"""

import json

CHUNK_MS = 100

# Populations the worker can drive (SS3 stimulus sets). JON is Part 5's
# walk/halt pathway (SS5), not the feeding loop; Ir94e is not driven in
# v1 (SS3.3). Anything outside this set in a scenario is an error.
DRIVABLE_POPULATIONS = ("sugar_grn_right", "sugar_grn_left",
                        "bitter_grn", "water_grn")

# Readouts returned when a scenario does not declare its own list: the
# registered feeding readout (MN9 L/R, SS4.2) plus the driven sets and
# the Part 2b descending readouts, for the record.
DEFAULT_READOUTS = ("total", "mn9_left", "mn9_right",
                    "sugar_grn_right", "sugar_grn_left",
                    "bitter_grn", "water_grn",
                    "adn1", "adn2_left", "abn1")

GATE_MODES = ("event", "window", "event_or_window", "always_on", "off")

VALIDATED_LABEL = "validated envelope (sugarR: sugar_grn_right at " \
                  "200 Hz, Part 3)"
OUTSIDE_LABEL = "OUTSIDE THE VALIDATED ENVELOPE (SS3, Amendment " \
                "Pass 1)"


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


def in_window(window, chunk):
    """True iff `chunk` lies in any inclusive [a, b] range of `window`."""
    return any(a <= chunk <= b for a, b in window)


def gate_state(mode, chunk, taste_event, window):
    """One drive's gating decision for one brain chunk (SS4.5).

    Returns {"event_gate": bool, "window_gate": bool, "applied": bool}
    -- both gates are always reported, applied or not, so the run
    record shows which gate did what (the SS4.5 two-gates rule).
    """
    event_gate = bool(taste_event)
    window_gate = in_window(window, chunk)
    if mode == "event":
        applied = event_gate
    elif mode == "window":
        applied = window_gate
    elif mode == "event_or_window":
        applied = event_gate or window_gate
    elif mode == "always_on":
        applied = True
    elif mode == "off":
        applied = False
    else:
        raise ValueError(f"unknown gate mode {mode!r}")
    return {"event_gate": event_gate, "window_gate": window_gate,
            "applied": bool(applied)}


def envelope_label(drive):
    """SS3 envelope label for one drive entry, from its own content."""
    if (drive["populations"] == ["sugar_grn_right"]
            and float(drive["rate_hz"]) == 200.0):
        return VALIDATED_LABEL
    return OUTSIDE_LABEL


def validate_scenario(scenario):
    """Validate + normalise a scenario dict. Returns a new dict with
    defaults filled (window [], readouts) and each drive's envelope
    label attached. Raises ValueError on anything the loop must not
    quietly accept: undeclared-able populations, unknown modes,
    malformed windows, duplicate drive names, non-positive chunks.
    """
    if not isinstance(scenario, dict):
        raise ValueError("scenario is not an object")
    name = scenario.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("scenario needs a non-empty 'name'")
    n_chunks = scenario.get("n_chunks")
    if not isinstance(n_chunks, int) or n_chunks <= 0:
        raise ValueError("scenario 'n_chunks' must be a positive int")
    seed = scenario.get("seed")
    if not isinstance(seed, int):
        raise ValueError("scenario 'seed' must be an int")
    drives_in = scenario.get("drives")
    if not isinstance(drives_in, list) or not drives_in:
        raise ValueError("scenario 'drives' must be a non-empty list")
    drives = []
    seen = set()
    for d in drives_in:
        if not isinstance(d, dict):
            raise ValueError(f"drive entry is not an object: {d!r}")
        dname = d.get("name")
        if not isinstance(dname, str) or not dname:
            raise ValueError(f"drive entry needs a name: {d!r}")
        if dname in seen:
            raise ValueError(f"duplicate drive name {dname!r}")
        seen.add(dname)
        pops = d.get("populations")
        if not isinstance(pops, list) or not pops:
            raise ValueError(f"drive {dname!r}: 'populations' must be "
                             f"a non-empty list")
        for p in pops:
            if p not in DRIVABLE_POPULATIONS:
                raise ValueError(
                    f"drive {dname!r}: population {p!r} is not a "
                    f"drivable SS3 set {DRIVABLE_POPULATIONS}")
        rate = d.get("rate_hz")
        if not isinstance(rate, (int, float)) or rate <= 0:
            raise ValueError(f"drive {dname!r}: 'rate_hz' must be "
                             f"positive")
        mode = d.get("mode")
        if mode not in GATE_MODES:
            raise ValueError(f"drive {dname!r}: mode {mode!r} not in "
                             f"{GATE_MODES}")
        window = d.get("window", [])
        if not isinstance(window, list):
            raise ValueError(f"drive {dname!r}: 'window' must be a "
                             f"list of [a, b] ranges")
        norm_window = []
        for r in window:
            if (not isinstance(r, (list, tuple)) or len(r) != 2
                    or not all(isinstance(x, int) for x in r)
                    or r[0] < 0 or r[1] < r[0]):
                raise ValueError(f"drive {dname!r}: bad window range "
                                 f"{r!r} (want [a, b], 0 <= a <= b)")
            norm_window.append([int(r[0]), int(r[1])])
        entry = {"name": dname, "populations": list(pops),
                 "rate_hz": float(rate), "mode": mode,
                 "window": norm_window}
        entry["envelope"] = envelope_label(entry)
        drives.append(entry)
    readouts = scenario.get("readouts", list(DEFAULT_READOUTS))
    if not isinstance(readouts, list) or not readouts:
        raise ValueError("scenario 'readouts' must be a non-empty list")
    return {"name": name, "n_chunks": n_chunks, "seed": seed,
            "drives": drives, "readouts": list(readouts)}


def make_start(scenario):
    return {"type": "start", "scenario": scenario}


def make_chunk(chunk, duration_ms, taste_event):
    return {"type": "chunk", "chunk": int(chunk),
            "duration_ms": int(duration_ms),
            "taste_event": bool(taste_event)}


def make_end():
    return {"type": "end"}


def validate_counts_reply(message, expected_chunk, drive_names,
                          readout_names):
    """Check a worker 'counts' reply against the contract. Returns the
    reply dict. Raises on any mismatch -- same discipline as
    src/first_loop/protocol.py: a bridge that silently accepts a malformed
    reply would manufacture loop results."""
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
    missing = [n for n in readout_names if n not in counts]
    if missing:
        raise ValueError(f"counts reply is missing readouts {missing}")
    for rname, value in counts.items():
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"count {rname}={value!r} is not a "
                             f"non-negative int")
    applied = message.get("applied")
    if not isinstance(applied, dict):
        raise ValueError(f"'applied' is not an object: {message!r}")
    for dname in drive_names:
        state = applied.get(dname)
        if not isinstance(state, dict):
            raise ValueError(f"applied state missing drive {dname!r}")
        for key in ("event_gate", "window_gate", "applied"):
            if not isinstance(state.get(key), bool):
                raise ValueError(f"applied[{dname!r}][{key!r}] is not "
                                 f"a bool: {state!r}")
    if not isinstance(message.get("taste_event_received"), bool):
        raise ValueError("'taste_event_received' is not a bool")
    return message
