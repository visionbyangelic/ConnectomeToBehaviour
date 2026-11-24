# Part 0 — Preparation Pack (ConnectomeToBehaviour fresh rebuild)

Prepared 23 Nov 2026 while the panel's final approval (Claude, Reviewer 1) is awaited.
Status of the plan itself: FINAL-PLAN.md v2 — ChatGPT ✅ and Gemini ✅ approved (23 Nov 2026, after amendments); Claude pending.
**Nothing here starts the build.** No data downloaded, no packages installed, no repo files created or changed, FINAL-PLAN.md untouched.
Sources: FINAL-PLAN.md §4 (Part 0 row + gate mechanics), §5, §5.6, §7.4–7.6, §9.1–9.2; old `scripts/download_data.py` (audit clone).

---

## 1. Environment check — this VM, run 23 Nov 2026

| Check | Result |
|---|---|
| OS / kernel | Linux x86_64, kernel 7.0.0-44-generic |
| Python | **3.12.3** (`python3`) — note: the old build's conda envs pinned Python 3.11 |
| pip | present — pip 24.0 (`/usr/bin/pip3`) |
| CPUs | 4 (shared) |
| RAM | 7.7 GiB total. **Caution:** at check time only ~494 MiB was available (7.3 GiB in use by other work on this shared VM) — a snapshot, not a capacity figure; re-check before any benchmark or simulation run |
| Swap | 1.0 GiB (359 MiB used at check time) |
| Disk | 150 GB volume, **137 GB free** (9% used) — ample for the ~92 MB dataset and run outputs |

Import test (`python3 -c "import …"`):

| Package | Status |
|---|---|
| numpy | ✅ 1.26.4 |
| scipy | ✅ 1.11.4 |
| pandas | ✅ 2.1.4 |
| matplotlib | ✅ 3.6.3 |
| pyyaml | ✅ present |
| **brian2** | ❌ not installed |
| **mujoco** | ❌ not installed |
| **flygym** | ❌ not installed |
| **neuromechfly** (as a standalone import) | ❌ not installed |
| **pyarrow** | ❌ not installed (needed to read the `.parquet` data at all) |
| **pytest** | ❌ not installed |
| **joblib** | ❌ not installed |

**Verdict: base scientific stack ready; the entire simulation stack is missing.** Part 0 itself is mostly documents, decisions and a benchmark, so nothing blocks Part 0 from *starting* — but see the sequencing flag below.

**What will need installing (Part 1's pinned environment, per FINAL-PLAN §4 Part 1 and the old repo's dependency files):**
- Brain env: `brian2>=2.9.0`, `pyarrow>=14.0.0`, `joblib`, `mujoco>=3.2.0`, numpy **<2.0** (old `environment.yml`: Python 3.11, conda-forge).
- Body env (separate, as the old build did): `flygym>=1.2.0` (NeuroMechFly v2), `mujoco>=3.2.0`, numpy **>=2.0** (old `environment-flygym.yml`).
- FlyBody from git (`github.com/TuragaLab/flybody`) if the body route requires it — decided by the Part 1b audit, not assumed.
- `pytest` for the plan's interface/unit tests.

**Two flags for Part 0/1 (not resolved here):**
1. **Known version conflict, inherited from the old build:** the brain stack pins numpy <2 while FlyGym requires numpy ≥2. The old build solved this with two isolated conda environments; the fresh build must either do the same or prove a unified set of pins — a Part 1 decision, recorded in the lockfiles.
2. **Sequencing:** Part 0's pass criteria include a **wall-clock benchmark (100 ms brain trial on this VM)**, which needs a working Brian2 — but the pinned environment is only built at Part 1. Part 0 must choose: (a) a throwaway minimal Brian2 install purely for the benchmark, clearly separated from the Part 1 pinned env; or (b) formally defer the benchmark to the start of Part 1. Either is fine; it must be a logged choice, not an accident. Related: Brian2/FlyGym support for **Python 3.12** (vs the old 3.11 pins) is **UNVERIFIED** — to be confirmed at install time, before pins are frozen.

---

## 2. Data source verification — HEAD checks only, nothing downloaded

Source: the exact URLs in the old `scripts/download_data.py` (`philshiu/Drosophila_brain_model`, `main` branch, raw.githubusercontent.com). Checked 23 Nov 2026 with `curl -sI -L`.

| File | URL | HTTP | Served size | Script's stated size |
|---|---|---|---|---|
| `2023_03_23_completeness_630_final.csv` | https://raw.githubusercontent.com/philshiu/Drosophila_brain_model/main/2023_03_23_completeness_630_final.csv | **200 OK** | 3,057,611 B (~3.0 MB) | ~3.0 MB ✅ |
| `2023_03_23_connectivity_630_final.parquet` | https://raw.githubusercontent.com/philshiu/Drosophila_brain_model/main/2023_03_23_connectivity_630_final.parquet | **200 OK** | 86,630,944 B (~86.6 MB) | ~86.6 MB ✅ |
| `sugarR.parquet` (at `results/example/`) | https://raw.githubusercontent.com/philshiu/Drosophila_brain_model/main/results/example/sugarR.parquet | **200 OK** | 948,526 B (~0.95 MB) | ~2.2 MB ⚠️ |

**All three files are reachable.** Total download ≈ 90.6 MB (script's ~92 MB estimate is close).

⚠️ **One discrepancy to resolve at Part 1, not now:** `sugarR.parquet` is served at ~0.95 MB, not the ~2.2 MB the old script states. Either the script's estimate was always rough, or the upstream file changed. This is exactly what §7.5 exists for: at download, record the SHA-256 hash and verify the file's *contents* against the Part 3 benchmark expectations (trial count, MN9 columns) before trusting it as the reference. Do not silently accept it on size alone.

**Fallback if a URL fails at Part 1:** `git clone` of the same `philshiu/Drosophila_brain_model` repository (same source, different transport). Any other mirror is **UNVERIFIED** — none was checked, and none should be substituted without a hash/content check against expectations from the paper.

v783 files exist in the same script but are **not** needed for the core (D1: v630 core; v783 only as the late RQ-P9 sensitivity study) — not checked, deliberately.

---

## 3. Fresh scaffold plan — layout only, nothing created

Repo: `~/workspace/connectome-work/repo` (currently the old build, `main` @ `ab30ab4`). Per D7, fresh work stays local and replaces nothing until the Part 6 checkpoint; the old build is preserved on an immutable tag + archival branch at replacement time.

**Proposed arrangement (for Angelic/panel to confirm at Part 0):** a local-only branch `fresh-rebuild`, with all fresh code in a new top-level tree so fresh and old never mix:

```
repo/  (branch: fresh-rebuild, local only until Part 6)
├── ctb/                        # the fresh package (src layout, importable, tested)
│   ├── __init__.py
│   ├── data/                   # loading, counting rules, ID-set extraction      → Part 1
│   ├── brain/                  # LIF network build, activate/silence/block API    → Part 2
│   ├── body/                   # FlyGym wrapper, arena, sensory-event reporting  → Parts 1b, 4
│   ├── bridge/                 # encoder, population decoder, premotor layer    → Parts 2b, 5
│   ├── experiment/             # intervention arms, null families D1–D4,
│   │                           # matched lesions, rule baselines                → Part 7
│   └── analysis/               # metrics, CIs, TOST, provenance ledger builders → Parts 3, 7
├── configs/                    # one YAML per run family; the ONLY place numbers live
│   ├── brain_v630.yaml
│   ├── decoder.yaml
│   └── experiment_feeding.yaml
├── prereg/                     # pre-registrations, append-only, one file per part/gate
│   ├── part0-foundations.md
│   ├── part3-brain-validation.md
│   └── part5-7-intervention-feeding.md
├── registers/                  # living documents from §7
│   ├── model-assumption-register.md
│   ├── sensory-pathway-specs/
│   ├── behavioural-provenance-ledger-feeding.md
│   └── risk-register.md
├── runs/                       # per-run manifest.yaml (committed) + outputs/ (gitignored, hashed)
├── registry/                   # append-only experiment registry (§7.5):
│   └── registry.jsonl          # prereg → manifest → result → conclusion links
├── tests/                      # interface tests for brain/decoder/body boundaries (§7.5)
├── data/                       # GITIGNORED — downloaded v630 files + hashes.txt (§7.5)
├── env/                        # lockfiles: brain env + body env (see §1 conflict flag)
└── docs/                       # reading log (Part 0–2 literacy), body fact-sheet (Part 1b),
                                # comparison decision log (Part 6), release docs (Part 8)
```

Mapping rule: every directory names the part that creates it, and every part's deliverables from the §4 table have exactly one home above. Old `src/`, `experiments/`, `scripts/` stay untouched on this branch until the Part 6 decision.

---

## 4. Pre-registration skeleton — from FINAL-PLAN §5.6 (with §5.1–5.5, §7.4–7.6)

*One copy of this template per confirmatory part (Parts 3, 5, 7 at minimum). Saved, dated and panel-reviewed **before** any results exist. Exploratory work is labelled exploratory and does not use this form (§4 gate mechanics). Blanks are the Part 0/3/5 decisions.*

```
PRE-REGISTRATION — [part / gate ID: ______]   Date: ______   Panel gate: HARD / LIGHT
Reviewers seen: ______   Human expert check sought: Y/N, who: ______

1. QUESTION & HYPOTHESES
   Question (one sentence): ______
   H1 (directional, falsifiable): ______
   H0 / equivalence expectation: ______
   Linked RQs: [RQ-C__ / RQ-P__]

2. ESTIMANDS (§5.1)
   Primary: E-Total / E-Pathway (circle) — defined as: ______
   Secondary: E-Total with decoder refit per condition (§5.4): Y/N
   Frozen decoder + identical body for all primary arms: confirmed Y/N

3. CONDITIONS / ARMS (§5.3)
   A intact | B targeted lesion(s): ______ | matched control lesions: §6 below
   D null families run: D1 / D2 / D3 / D4 — independent networks per family: n = ______
   Sensory-input and readout neuron identities preserved in all nulls: Y/N
   Body-only / decoder-only baselines: zeros / constant / open-loop replay (§5.3)
   Rule baselines (§5.5): ______ (matched capacity, tuning budget declared: ______)

4. METRICS (§5.2) — computed from body state, not decoder internals
   Primary endpoint (one): ______
   Secondary metrics: ______
   Feeding body metric: proboscis-based / named proxy = ______ (per Part 1b audit)
   Calibration set vs evaluation set split (§7.3) recorded at: ______

5. STATISTICS (§5.6, §7.4)
   Experimental unit: independent networks (nulls) / independent seeds (trials)
   N trials = ______ ; N shuffle networks = ______ ; justification (precision/power
   vs effect size of interest ______): ______
   CI method: ______ (e.g. bootstrap over networks/trials)
   Alpha = ______ ; multiple-comparison correction across arms/metrics: ______
   Paired-seed design used where legitimate: Y/N, where: ______

6. MATCHED CONTROL-LESION PROCEDURE (§5.3, Reviewer 3 amendment — fixed BEFORE outcomes)
   Matching variables: neuron/connection count; in- & out-degree distributions;
   baseline activity distribution; neuron class + neurotransmitter-sign composition;
   neuropil/location; downstream connectivity/influence; perturbation magnitude.
   Number of independently selected controls per targeted lesion: ______
   Imbalance quantification method: ______
   Rule if matching is infeasible: quantify residual imbalance, restrict
   E-Pathway interpretation accordingly, report — never hide.

7. EQUIVALENCE BOUNDS (TOST, §5.6)
   For each primary metric, smallest scientifically meaningful effect: ______
   Equivalence bounds: ± ______ ; alpha: ______
   Standing rule: non-significant ≠ null. "No difference" may be claimed ONLY on
   demonstrated equivalence within these bounds; otherwise report INCONCLUSIVE.

8. SEEDS (§7.5)
   Master seed list for this part: ______ (published with results)
   Seed policy: ______

9. CONVINCING-POSITIVE CRITERIA (§5.6) — all must hold for a positive claim
   □ bitter suppression with NO hand-coded decoder override
   □ targeted lesion hurts more than matched control lesions
   □ null families degrade in a graded way (D1→D4)
   □ rule baselines fail held-out conditions where intact succeeds
   □ separation survives RQ-P1 / RQ-P2 sensitivity
   Even then, permitted claim = limited topology-contribution claim under THIS
   encoder/decoder/body only, worded per §7.6 table.

10. PERMITTED CONCLUSIONS (§7.6)
    Outcome → exact permitted wording table attached: Y/N
    (covers positive / equivalence / inconclusive / refit-erases-gap cases)

11. KILL / STOP CRITERIA IN FORCE (§9.1)
    K1 reproduction __  K2 body __  K3 separation __  K4 compute __
    K5 scope __  K6 Part 2b loop stability __   (mark which apply to this part)
    Part budget: ______ wall-clock weeks; ______ Angelic review hours.

12. AMENDMENTS — none permitted silently. Any change after results are seen:
    formal amendment, logged here, panel-reviewed, Angelic-approved.
```

Kill criteria in brief (§9.1, for §11 of the template): **K1** Part 3 reproduction failure after logged diagnosis → pivot to a reproduction-failure report, no embodiment on an untrusted brain. **K2** Part 1b shows no honest feeding metric, not even a proxy → Core-A re-scopes to neural-level (E1), Angelic decides. **K3** demonstrated equivalence intact-vs-nulls at Part 7 → write it up; no adding behaviours hoping for a positive. **K4** confirmatory N unaffordable on CPU + GPU parity gate fails → N reduced only by formal amendment with power consequence stated. **K5** stretch never eats core; threatening items defer automatically. **K6** Part 2b loop unstable after bounded, logged adjustments → stop; revise architecture, re-run 2b once; still unstable → re-scope Core-A to open-loop/E1, Angelic decides.

---

## 5. Run-manifest template — per FINAL-PLAN §7.5

*Every run produces one manifest. No manifest, no result.*

```yaml
manifest_version: 1
run_id: ______            # unique, e.g. p3-sugar-seed0007-2026-__-__
created_utc: ______
part: ______               # plan part (0–8)
panel_gate_id: ______      # gate this run belongs to
prereg_id: ______          # pre-registration it answers (confirmatory) or "exploratory"
question: ______

code:
  repo_commit: ______      # full git SHA of the fresh-rebuild branch
  working_tree_dirty: ______  # must be false for confirmatory runs
  entry_point: ______      # script/module + command line, verbatim

data:
  dataset: FlyWire v630    # version of record
  files:
    - name: 2023_03_23_completeness_630_final.csv
      sha256: ______
    - name: 2023_03_23_connectivity_630_final.parquet
      sha256: ______
    - name: sugarR.parquet          # if used by this run
      sha256: ______

environment:
  lockfile: ______         # path to env lockfile used
  lockfile_sha256: ______
  python: ______           # installed version, recorded from the interpreter
  key_packages: {}         # brian2 / flygym / mujoco / numpy versions, as installed
  host: ______             # machine + CPU count
  hardware: cpu            # or gpu model, if the §0.2a gate was passed

config:
  config_file: ______      # path under configs/
  config_sha256: ______
  overrides: {}            # any deviation from the file, spelled out

seed: ______               # this run's seed, from the part's master seed list
condition: ______          # arm / stimulus / lesion / null family + network index

outputs:
  - path: ______
    sha256: ______
wall_clock_s: ______
peak_memory_mb: ______     # feeds RQ-P7 compute benchmark
result_summary: ______     # one line; full numbers live in the outputs, not here
conclusion_class: ______   # per the §7.6 permitted-conclusions table, or "none yet"
```

The append-only registry (`registry/regis
...[truncated 2112 chars]