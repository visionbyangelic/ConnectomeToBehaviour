# Thin FlyBody slice — record (Part 4 specs §6)

**Deliverable:** the §6 thin slice — the registered feeding chain
(§4.2 estimator + §4.3 mapping, as the new Part 5 module
`repo/fresh/part5/chain.py`) carried over the bridge on the pinned
FlyBody in the §4.6 arena, driven by a scripted synthetic MN9-rate
profile from a brain-side stub, with the §4.5 constructed taste event
written back across the bridge. Executed 24 Nov 2026, after the
qualification gate passed (execution #5).

**Verdict: PASS — all five §6 success criteria, on attempt 2.**
Attempt 1 failed criterion (ii) on a profile-shape defect (below);
both attempts are recorded in full.

## Configuration (as run)

- **Bridge:** two processes, one JSON object per line, 100 ms chunks,
  replies in order and validated (`repo/fresh/part5/protocol.py`,
  the Part 2b contract's form). Driver (`run_slice.py`) and stub
  worker (`stub_worker.py`) both ran the body env's Python
  (FlyGym 2.1.1 / MuJoCo 3.16.0 / numpy 2.5.5). No Brian2 anywhere:
  the brain side is a stub and impersonates no brain output.
- **Scripted profile (SYNTHETIC in every artefact):** pooled MN9 rate
  ramp 0 → 100 → 0 Hz over 60 chunks — attempt 2's shape: linear up
  over chunks 0–14, hold at 100 Hz over chunks 15–34, linear down
  over chunks 35–49, 0 Hz over chunks 50–59 — realised as seeded
  Poisson counts (seed 20261125, split evenly over MN9 L/R),
  generated in full before the episode clock (§2.2's substance).
- **Slice parameters:** r_lo = 5 Hz (FIXED, §4.3). **r_hi = 100 Hz is
  a declared SLICE parameter — synthetic/provisional**, chosen so the
  profile's 100 Hz peak maps to e = 1 and the chain is exercised
  through the contact regime. It is **not** Part 5's calibration:
  the Part 5 r_hi is computed from designated calibration episodes
  under §4.3's rule and replaces this value at the freeze.
- **Body/arena:** the gate's pinned FlyBody, §4.6 arena as revised
  (pedestal r 0.5 × h 0.28 mm, food disc on top at ground + 0.33 mm,
  centre (1.016, 0.006) mm = 0.6 mm in front of the labrum tip's
  settled ground projection), **with the proboscis contact pairs**
  of the gate's Q5 fix — without them the §4.5 event cannot exist.
- **Settle:** §2.3, settled in 4 chunks, no food contact during
  warmup; feedback armed from t = 0. θ_rest (rad): rostrum −0.00328,
  haustellum pitch −0.00087, yaw −0.00000, labrum L −0.00004,
  R −0.00001.
- **Chain audit (pre-flight):** before the episode, `chain.py` was
  checked against the gate's own chain implementation
  (`qualgate/gate_common5.py`) on the episode's compiled parameters
  and settled rest: θ_ext identical and ctrl values identical
  (max diff 0.0) on an e grid of 0, 0.05, …, 1.0. The Part 5 code
  path and the gate's audited chain are the same mapping.
- **Unit tests:** `repo/fresh/part5/tests/test_chain.py` — 9 tests,
  all passing (zero rate → rest targets and ctrl = 0; startup rule
  reads the true rate from chunk 0; window slides; α is the exact
  discretisation; monotone in rate; feedforward endpoint at e = 1 is
  exactly the published range limit; θ_ext matches the gate values;
  yaw held; r_hi must be supplied explicitly).

## Attempt 2 — per-criterion verdicts (artefact: `runs/slice_run.json`)

| # | Criterion (§6) | Verdict | Numbers |
|---|---|---|---|
| (i) | 60/60 chunks, no worker error, no NaN/Inf | **PASS** | 60/60 chunks completed; worker error: none; qpos/qvel, all recorded angles and contact forces finite in every chunk |
| (ii) | E(t) rises and falls with the profile; onset/offset by §4.4 | **PASS** | onset chunk **5** (E ≥ 0.10 rad sustained ≥ 2 chunks); peak E **2.0598 rad** (chunk 16); offset chunk **53** (E < θ_off = 0.01036 rad sustained ≥ 2 chunks); E at chunk 59 = −6.4e-6 rad ≈ 0 |
| (iii) | Labrum–food contact event ON during the high-rate phase | **PASS** | event first ON at end of chunk **15** (scripted rate 100 Hz, e = 0.883, E = 1.866 rad); max labrum–food force **12.63 N**; front tarsi never contacted (0.0 N) |
| (iv) | Taste event in the brain-side stub log exactly one chunk after contact, and clearing exactly one chunk after the contact clears | **PASS** | contact ON at end of chunk 15 → stub log taste ON from chunk **16**; contact cleared at end of chunk 40 → stub log taste ON through chunk 40, OFF from chunk **41**; the stub log equals the previous chunk's body event state at **every** one of the 60 chunks |
| (v) | Frozen brain code untouched | **PASS** | `git status` over `fresh/ctb/` empty before and after; HEAD = freeze commit `e1f40462a68cfd2f87325ec0fc4e519bf667db09` (tag `part3-prereg-v2`) throughout |

Notes on the run's texture, for honesty: the realised r_filt peaked
at 109.8 Hz (the Poisson realisation overshot the scripted 100 Hz;
the estimator reports the realised counts and e clipped at 1.0, as
specified). Labrum adhesion engaged during chunk 16 per §4.3's rule
(first chunk after the event turned ON) and released after the event
had been OFF for 2 consecutive chunks, as Q5 demonstrated. Contact
onset at E/E_max = 0.858 sits near the gate's Q5 measurement (0.837)
under a different ramp; nothing was tuned to make it so.

Wall clock: 63.7 s for the run (settle, audit and 60 chunks), body
env, this machine.

## Attempt 1 — FAIL on criterion (ii), profile-shape defect (artefacts: `runs/slice_run_attempt1.*`)

Same everything, except the scripted profile was a trapezoid whose
down-ramp reached 0 Hz only at the final chunk (linear down over
chunks 40–59). Results: (i) PASS; (ii) **FAIL** — onset chunk 5,
peak E 2.0589 rad, contact chunk 19, stub taste ON at 20 and clear
after 45, criteria (iii), (iv), (v) all PASS — but **no §4.4 offset
occurred inside the window**: at chunk 59, E was still 0.212 rad.
The reason is arithmetic, not a chain or body fault: with the rate
reaching zero only at the last chunk, the trailing 500 ms window
still held the down-ramp's tail counts (r_filt = 14.1 Hz at
chunk 59 → e = 0.096), and the estimator lag (≈0.5 s window + τ =
0.2 s EMA) plus the body's relaxation cannot carry E below
θ_off = 0.01036 rad before the window ends — for any correct
implementation of the registered chain. The §4.4 offset definition
was therefore unexercisable in that profile shape. **Fix (slice
level, as §6 prescribes):** the profile shape — the one degree of
freedom §6 leaves to the implementer, stated in every artefact —
was changed so the ramp completes by chunk 49 and the last 10
chunks sit at 0 Hz, giving the estimator and the body room to decay
inside the 60 chunks. No chain code, threshold, arena or parameter
changed between the attempts. Attempt 2 (above) is the result.

## Artefacts

- `repo/fresh/part5/chain.py` — the registered chain (Part 5 code path)
- `repo/fresh/part5/tests/test_chain.py` — 9 unit tests, all passing
- `repo/fresh/part5/protocol.py` — the slice bridge contract
- `repo/fresh/part5/stub_worker.py` — the brain-side stub (synthetic)
- `repo/fresh/part5/run_slice.py` — the driver
- `repo/fresh/part5/runs/slice_run.json` — attempt 2, full per-chunk log
- `repo/fresh/part5/runs/slice_run.stub_log.jsonl` — attempt 2 brain-side stub log
- `repo/fresh/part5/runs/slice_run_attempt1.json` / `.stub_log.jsonl` / `.worker.log` — attempt 1, preserved

Nothing was pushed. track.md was not touched by this deliverable.
