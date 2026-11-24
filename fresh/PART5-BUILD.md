# Part 5 build — the full closed feeding loop (record)

**Deliverable:** the Part 5 full closed loop, feeding configuration,
built against `PART4-SENSORY-SPECS.md` (§§2, 4.1–4.7, 6.1(3)):
frozen brain → §4.2 estimator → §4.3 mapping → pinned FlyBody →
§4.5 constructed taste event → sugar drive gate → brain. Plus the
§6.1(3) equivalence probe for the toggled-drive configuration and
two labelled smoke runs. Executed 24 Nov 2026, after the
qualification gate passed (execution #5), the §2.4 acceptance test
passed, and the §6 thin slice passed.

**Status: BUILT. Probe discharged by the Part 2b method (see §3 —
one part of the original probe plan proved impossible, and that is a
finding, recorded as one). Both smoke runs PASS.** No calibration or
evaluation episodes were run: those designs belong to the Part 5
preregistration, which this build precedes.

---

## 1. Architecture

All code in `repo/fresh/part5/`. The frozen model (`fresh/ctb/`) is
used exactly as shipped and was not modified (git status over
`fresh/ctb/` empty before and after; HEAD at the freeze commit
`e1f40462a68cfd2f87325ec0fc4e519bf667db09`, tag `part3-prereg-v2`,
throughout).

- **`loop_protocol.py`** — the bridge contract and the stimulus
  logic, in pure stdlib Python so the worker, the driver and the
  tests run identical code. A **scenario** declares, in full, before
  any run (§2.2): name, chunk count, brain seed, and a drive list —
  each drive has a gate name, its Part 2 population set(s), its rate,
  a **gating mode**, and a scripted window. Modes: `event` (the §4.5
  taste event only), `window` (scripted window only),
  `event_or_window` (§4.5's two-gates case), `always_on`, `off`
  (declared and warmed up, never applied). `gate_state()` returns
  **both gates and the applied flag** for every drive in every chunk,
  so the run record always shows which gate did what. The module also
  attaches the §3 envelope label to each drive: exactly
  `sugar_grn_right` at 200 Hz is the validated envelope; everything
  else is labelled OUTSIDE THE VALIDATED ENVELOPE.
- **`brain_worker.py`** — brain env (Brian2 2.9.0 / numpy 1.26.4).
  The Part 2b pattern unchanged: one frozen Brain, one persistent
  Network over its objects, drives added once for every declared
  population and held inactive, a **zero-duration warmup with all
  declared drives active** before the episode clock (§2.2 — pays
  Brian2's first-active compile costs outside the episode). Per
  chunk it receives the taste-event state at the end of the previous
  body chunk, computes each drive's gate, sets the `active` flags
  (chunk boundaries only — the harness rule), runs 100 ms, and
  replies with the declared readouts' spike counts (MN9 L/R always
  available; the default readout list also carries the driven sets,
  aDN1, aDN2-left, aBN1 and the total) plus the full applied-state
  record. Its `ready` reply carries the loader-verified data hashes.
- **`body_side.py`** — the body half, in the driver process (as in
  Part 2b and the slice, only the brain crosses a process boundary).
  Construction reuses the qualification gate's own machinery: a pilot
  settle places the §4.6 arena centre 0.6 mm in front of the labrum
  tip's settled ground projection; `qualgate.q5_rerun5.build_arena`
  builds the pedestal + food **with the six proboscis contact pairs**
  of the gate's Q5 fix; the episode settle is §2.3 under zero command
  with the food-contact check that invalidates the episode on any
  warmup contact. Per chunk it writes the chain's five proboscis
  ctrls as a zero-order hold (all other position actuators at ctrl 0,
  as at the gate), steps 1000 physics steps, tracks the §4.5 event
  per physics step from food-geom-filtered labrum/front-tarsus forces
  with the §2.4 debounce (ON ≥ 10 steps, OFF ≥ 50), and applies
  §4.3's adhesion rule at the chunk boundary. Records per chunk: the
  five proboscis + three neck angles, both food-force maxima, the
  event state at chunk end, adhesion, thorax position, finiteness.
- **`run_loop5.py`** — the driver. Chunk order is §2.1's: brain
  chunk *k* (sensory state from body chunk *k−1*) → chain (the
  slice's `chain.py`, unmodified) → body chunk *k*. Every run writes
  a directory with `manifest.json`, `brain_log.jsonl`,
  `body_log.jsonl`, `summary.json` (§2 below). Built-in scenarios S1
  and S2; arbitrary scenarios load from a JSON file.
- **`chain.py`** — the registered chain, as built and audited by the
  thin slice (9 unit tests; bit-identical ctrls to the gate's chain).
  Unchanged by this build.

**r_hi for the smoke runs: 155 Hz, labelled PROVISIONAL** (§7.6's Q6
value — Part 3's measured pooled MN9 response, 92.57 + 62.40 Hz) —
chosen over the slice's 100 Hz because it is the value tied to the
validated response; the calibrated r_hi replaces it at the freeze,
per §4.3's separation rule. Recorded with that provenance label in
every manifest.

## 2. Run records (§6.1(3))

Each manifest records: the full validated scenario (the §2.2 declared
drives), the frozen ctb commit + tag and the git status — stated, not
tidied: both smoke manifests record `working_tree_dirty: true` (the
tree carries the project's untracked part2b/part5/qualgate work and
two modified documents) with `fresh/ctb/` itself clean and HEAD at
the freeze commit; the loader-verified SHA-256 of both data files;
the brain seed (the body is deterministic MuJoCo and has no seed —
recorded as such); the configuration (r_lo = 5 FIXED; r_hi with its
provenance label; gate signs −1/−1; θ_off = 0.01036 rad; E_max =
2.1746 rad; the arena as qualified); the settle record and the
episode's validity; and per-chunk applied drives — both gates,
separately — in `brain_log.jsonl`.

## 3. Equivalence probe (§6.1(3)) — method, verdict, and the part that proved impossible

Configuration fixed before running: sugar_grn_right at 200 Hz, seed
5103, 20 chunks × 100 ms. Toggle schedule: chunks 0–4 OFF, 5–14 ON,
15–19 OFF. Every run in a **fresh process, build #1 in its process**
(the Part 2b diagnostic's RNG-stream qualification), each with the
worker's §2.2 zero-duration warmup. Canonicalisation and SHA-256
exactly as Part 2b's hash re-check; trains archived as `.npz`.
Artefacts: `repo/fresh/part5/runs/probe_toggle/`.

- **Constant pair (the probe-2 comparison):** chunked (20 × 100 ms,
  persistent Network) vs single (one 2000 ms run), drive on
  throughout. **Bit-identical:** 34,013 spikes each, SHA-256
  `7675ebe18c3775ad48542b62f7557a0331ad3023d2291da2f1284469fa0fe5d1`
  both. Chunking is neutral at this duration, seed and warmup.
- **Toggle exactness (the probe-1 criterion), on the chunked worker
  path:** the driven population's count is **exactly 0 in every OFF
  chunk** and positive in every ON chunk (per-chunk sugar spikes:
  0,0,0,0,0, then 383–439 per ON chunk, then 0,0,0,0,0). Chunked
  toggle train: 17,379 spikes, SHA-256
  `0ead53e3d83b163a610de1701f5a390503822d271db5ff9526355437e9778387`.
  Both probe executions (the script ran twice, see below) reproduced
  these hashes exactly.
- **A true single-run toggled reference does not exist in this
  stack — a finding, not a gap in effort.** Two constructions were
  attempted and both are on record:
  1. *Toggling the `active` flags from inside one run* (a Brian2
     network_operation applying the schedule): produced **zero
     spikes** — Brian2 fixes the network's active set when a run
     starts, so a drive inactive at run start is absent from the
     schedule and a mid-run flip can never reach it. Preserved:
     `probe_toggle_equivalence_attempt1.json` (single_toggle train
     hash = the empty train's hash, `e3b0c442…`).
  2. *Modulating the drives' rate* (0 / 200 Hz) from inside the run:
     impossible — Brian2 2.9's `PoissonInput.rate` is a read-only
     property (`AttributeError: property 'rate' of 'PoissonInput'
     object has no setter`, raised in-configuration by the probe's
     single_toggle mode and recorded in the probe record).
  The frozen `Brain.run()` has no scheduling surface either. So
  §6.1(3) is discharged **by the Part 2b method** — the method the
  section itself names: bit-identical chunking under a constant drive
  plus exact toggling between runs. Any stronger claim would require
  a different drive mechanism, which would be a different model.

## 4. Smoke runs (labelled smoke, not science)

### S1 — event-gated sugar with scripted ignition (`runs/s1_smoke/`)

Scenario: sugar_grn_right at 200 Hz (validated envelope), mode
`event_or_window`, scripted window chunks 0–9, 40 chunks, seed 5101,
r_hi = 155 PROVISIONAL. Settle: 4 chunks, VALID. **Verdict: PASS** —
all five checks:

- **Ignition and contact:** MN9 answered the drive from chunk 0
  (L/R counts 7/6 in the first chunk, pooled filtered rate 51.2 Hz
  and climbing); E crossed the §4.4 onset at chunk 0 and reached
  1.851 rad by chunk 5, where the labrum first contacted the food
  (6.79 N) and the §4.5 event turned ON at the chunk's end. Contact
  onset at E/E_max = 0.851 — beside the gate's measured 0.837 and the
  slice's 0.858, under a third protocol; nothing was tuned to make
  them agree.
- **The event took over the gating:** from chunk 6 the brain-side
  record shows the event gate ON alongside the window; the window
  closed after chunk 9, and for chunks 10–39 the drive was applied
  **only** via the event gate — verified mechanically over the log
  (`applied == event_gate` for every post-window chunk, with the
  event sustaining the drive in all of them). Both gates are logged
  separately in every chunk, as §4.5 requires.
- **The loop sustained itself** for the remaining 3.0 s: contact
  force 5.8–6.6 N every chunk (peak 10.78 N at chunk 7), adhesion
  engaged from chunk 6, the event ON in 35 of 40 chunks (every chunk
  from 5 on), E held at 1.86–2.06 rad (peak 2.058 rad), r_filt
  141–162 Hz. Total MN9 spikes 608 (L ≈ 9, R ≈ 6 per chunk — the
  Part 3 L>R asymmetry visible in the loop, unprompted). All body
  states finite in all 40 chunks. Wall clock 54.4 s.
- One honest note: peak E (2.058 rad) sits below the gate's static
  E_max (2.1746 rad) — the filtered rate hovers at the r_hi knee
  (e mostly 0.95–1.00, dipping with Poisson variability) and the
  dynamic pose differs from Q3's static holds. The chain commanded
  what the estimator reported; nothing was adjusted.

### S2 — no-drive control (`runs/s2_smoke/`)

Scenario: the sugar drive declared (§2.2) with mode `off`, 30
chunks, seed 5102. Settle: 4 chunks, VALID. **Verdict: PASS** — all
five checks: drive never applied (0 chunks); **MN9 exactly silent —
0 spikes in 30 chunks** (the model's verified undriven floor, §4.3);
no taste event ever; both food-force maxima exactly 0.0 N; E at rest
throughout (|E| ≤ 1.2 × 10⁻⁶ rad). Wall clock 40.6 s.

## 5. Tests

`repo/fresh/part5/tests/test_loop.py` (new) + the slice's
`test_chain.py`: **37 passed** under the brain env's pytest. The new
tests cover the gating function (all five modes; both gates always
reported; window bounds inclusive), scenario validation (drivable
sets only — JON and Ir94e rejected; duplicate names, reversed
windows, bad rates rejected), the §3 envelope labels (right-only at
200 Hz validated; left, bilateral, bitter, water, and right-only at
150 Hz all OUTSIDE), bridge reply validation (wrong chunk, missing
readout, missing gate, worker error), and manifest completeness
against a produced smoke-run directory (§6.1(3) keys: freeze commit
+ tag, git status, data hashes, declared drives, r_hi with
provenance, settle record, validity, per-chunk both-gates log).

## 6. Deviations and surprises, plainly

1. **The probe's single-run toggled reference does not exist**
   (§3): two constructions attempted, both impossible for stated
   Brian2 reasons, both preserved on record. §6.1(3) discharged by
   the Part 2b method it names. The probe script was rewritten once
   to carry this honestly; the first execution's record is preserved
   as `probe_toggle_equivalence_attempt1.json`.
2. **The body side is a component in the driver process**
   (`body_side.py`), not a third process — the Part 2b/slice bridge
   structure, in which only the brain crosses a process boundary.
   The task's body-worker duties (arena, settle, per-chunk stepping,
   event, records) are all implemented there.
3. **Brain chunks are far cheaper than Part 2b's record suggested**
   (~1 s per chunk here vs ~10 s there — the difference is Part 2b's
   146 JON drives and their compile/behaviour costs, absent here);
   whole smoke episodes took under a minute. Recorded because
   Part 5's calibration/evaluation budgeting will use these numbers.
4. **The repository working tree is dirty** (untracked
   part2b/part5/qualgate work, two modified documents) — the
   manifests say so, per §6.1(3); `fresh/ctb/` is clean and HEAD is
   the freeze commit. Nothing was committed or pushed by this build.
5. No calibration or evaluation episodes were run, and no scenario
   beyond the two smokes: the preregistration fixes those designs.

## Artefacts

- `repo/fresh/part5/loop_protocol.py`, `brain_worker.py`,
  `body_side.py`, `run_loop5.py`, `probe_toggle_equivalence.py`
- `repo/fresh/part5/tests/test_loop.py` (37 tests with test_chain.py,
  all passing)
- `repo/fresh/part5/runs/probe_toggle/` — probe record + attempt-1
  record + four archived trains
- `repo/fresh/part5/runs/s1_smoke/`, `runs/s2_smoke/` — manifest,
  brain log, body log, summary, worker log per run
- This record: `fresh/PART5-BUILD.md`

Nothing was pushed. track.md was not touched by this deliverable.
