# Part 0 benchmark — 100 ms Brian2 trial on this VM (Option A, throwaway env)

**Status: INDICATIVE ONLY.** These numbers come from a quarantined throwaway environment (PART0-PACKAGE §5, Option A; decision sheet item 11, approved by Angelic 23 Nov 2026). They are **not** reference numbers. The identical benchmark must be re-run in Part 1's pinned environment, and any material difference logged, before any number here is relied on. The GPU trigger (item 12) is *set* from these numbers provisionally, exactly as the plan provides.

## Run manifest
- **Date/time:** 23 Nov 2026, ~17:37–17:40 WAT (install 17:37, runs finished ~17:40).
- **Machine:** Buddy's Linux VM — 4 shared CPU cores, 7.7 GiB RAM total, **no GPU**. Machine state during the run: `free -h` immediately before the runs showed only ~481 MiB available (shared VM under other load); MemAvailable readings during the runs fluctuated (see per-run values — other tenants' load changed mid-run). This is a second reason the numbers are indicative only.
- **Environment (throwaway, quarantined):** venv at `~/workspace/connectome-work/bench-venv` — outside the repo, never imported by project code, not the Part 1 env. Nothing was installed into the system Python.
  - Python 3.12.3 — **Brian2 installs and runs on Python 3.12**: the plan's UNVERIFIED 3.12 question is answered (install + run both succeed). Part 1 pin decisions take note.
  - Brian2 2.10.1; numpy 2.5.5 (whatever pip resolved, per Option A — the Part 1 brain env is expected to pin numpy <2 per the old build; another reason these numbers are indicative).
  - Brian2 device: runtime (numpy codegen target) — the conservative, no-compilation path.
- **Script:** `~/workspace/connectome-work/bench/benchmark_100ms.py` (kept with this file's outputs in `~/workspace/connectome-work/bench/benchmark_results.json`). Timing excludes network construction (build and run were separated in design; the recorded wall-clock is the `run()` call for 100 ms of simulated time at dt = 0.1 ms).
- **Network timed:** plain leaky integrate-and-fire neurons, sparse random internal synapses, Poisson drive onto the population. This is a timing scaffold, **not** the project's brain model.
  - Point A: 10,000 neurons, internal connection probability 0.01 (~1.0M synapses).
  - Point B: 127,400 neurons (the v630 neuron count — full-brain scale), internal connection probability 0.0001 (~1.62M synapses).

## Results — wall-clock for 100 ms of simulated time
| Point | Neurons | Internal synapses | Rep 1 | Rep 2 |
|---|---|---|---|---|
| A — small | 10,000 | ~999,000 | 1.02 s | 0.86 s |
| B — full v630 scale | 127,400 | ~1,622,000 | 10.93 s | 9.46 s |

- **Headline figure:** at full v630 scale, 100 ms of simulated time costs **≈ 9.5–10.9 s wall-clock** on this VM in this state → **≈ 95–110 s wall-clock per biological second**.
- **Activity caveat (important, read before quoting):** the scaffold's drive pushed every neuron to its refractory ceiling — the recorded mean rate was 500 Hz, the maximum possible with a 2 ms refractory period (total spikes were exactly neurons × 50 per 100 ms in every run). Real model activity is far sparser. These timings therefore carry a **worst-case spike load**; per-step neuron-update cost (the dominant term) is activity-independent, so the figures are best read as an upper-bound-flavoured estimate, not a prediction of Part 3 run times.
- **Free RAM observed:** ~390 MiB available at the end of the Point A runs; ~3.5 GiB by the end of the Point B runs (the shared machine's other load dropped mid-run — recorded as observed, not explained).
- **Projection (rough, Part 3 scale only):** at ≈ 95–110 s per 1.0 s trial, the Part 3 ladder (4 conditions × N = 20 seeds × 1.0 s) projects to roughly **2.1–2.4 hours** of wall-clock — far below the GPU trigger (14 days for a confirmatory run set, or 72 hours for one condition family). On these indicative numbers, **the GPU gate stays closed**; the full intervention-experiment projection belongs to the Part 1 re-run.

## Mistakes / retraces during this benchmark (logged per the track rule)
1. **First run failed before any timing:** the script's neuron equations used `v_rest` and `tau` without declaring them as parameters; Brian2 raised a KeyError at network preparation. Fixed by declaring both in the equations and setting their values; the re-run produced the numbers above. No timing from the failed attempt exists or is used.
2. The script's first draft also contained a clumsy three-line attempt at setting the Poisson drive rate; it was cleaned up to a single explicit line before the first successful run. Cosmetic, but recorded.

## What Part 1 must do with this file
Re-run the identical script in the pinned Part 1 environment; record the pinned-env numbers next to these; log any material difference and its likely cause (numpy pin, Brian2 pin, machine state); only then treat the benchmark as reference-grade (RQ-P7 will report the pinned numbers).

---

## Part 1 pinned-env re-run (23 Nov 2026) — the mandatory confirmation

Re-run as required by Part 0 decision item 11 (Option A): the **identical script** (SHA-256 `2c34294866858d095a627eabb1cb17ea95d8bdeac69cf74dc31414f1402ab8da`, byte-identical copy, run from `~/workspace/connectome-work/bench-part1/`; results in `~/workspace/connectome-work/bench-part1/benchmark_results.json`), in the pinned Part 1 brain env.

**Run manifest (re-run):**
- **Date/time:** 23 Nov 2026, ~19:48–19:50 WAT.
- **Environment:** `~/workspace/connectome-work/envs/brain` — Python 3.12.3, **Brian2 2.9.0**, **numpy 1.26.4** (the plan's pins; full manifest in `PART1-ENVIRONMENTS.md`). Differences from the throwaway env: Brian2 2.10.1 → 2.9.0, numpy 2.5.5 → 1.26.4.
- **Machine state:** `free -h` immediately before: ~593 MiB available of 7.7 GiB (shared VM under other load, as before). Per-run MemAvailable at end of each run is in the results table — note it *rose* to ~4.5–4.7 GiB during the Point B runs as other load on the machine dropped, the same mid-run drift seen in Part 0.
- **Activity caveat carries over unchanged:** the scaffold again saturated every neuron at the 500 Hz refractory ceiling (total spikes exactly neurons × 50 per 100 ms in every run), so these remain worst-case-spike-load timings, best read as an upper-bound-flavoured estimate.

**Results — wall-clock for 100 ms of simulated time:**
| Point | Neurons | Internal synapses | Rep 1 | Rep 2 | Part 0 (indicative) |
|---|---|---|---|---|---|
| A — small | 10,000 | ~1,001,000 | 1.40 s | 0.95 s | 1.02 s / 0.86 s |
| B — full v630 scale | 127,400 | ~1,622,000 | 10.89 s | 9.75 s | 10.93 s / 9.46 s |

**Verdict: the pinned-env numbers CONFIRM the indicative Part 0 numbers.** At full v630 scale the pinned range is **9.7–10.9 s per 100 ms ≈ 97–109 s wall-clock per biological second**, against Part 0's 9.5–10.9 s (≈95–110 s). The ranges overlap almost exactly; neither the numpy pin (2.5.5 → 1.26.4) nor the Brian2 minor version (2.10.1 → 2.9.0) moved the timing materially on this machine. The benchmark is therefore reference-grade as of this re-run, subject to the standing caveats (saturated activity; shared-machine state at run time). The Part 3 projection stands: roughly **2.1–2.4 hours** for the 4-condition × N=20 × 1.0 s ladder at ~100 s per biological second — far below the GPU trigger (14 days / 72 hours), so **the GPU gate stays closed**.
