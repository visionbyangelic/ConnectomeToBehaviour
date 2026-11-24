# Part 1 — Pinned environments (built 23 Nov 2026)

**What this file is:** the record of the two isolated environments the fresh build runs in, with versions taken from the packages *as installed* (`pip freeze` output, reproduced in full below). Built under FINAL-PLAN §4 Part 1 ("Pinned environment built from scratch (versions recorded from installed packages); container/lockfiles").

**Why two environments:** the inherited conflict from the old build — the brain stack pins numpy <2, the FlyGym stack requires numpy ≥2. The old build solved it with two conda environments; the fresh build does the same with two venvs, kept **outside the repo tree** at `~/workspace/connectome-work/envs/` so no environment ever gets committed.

**Machine / date:** Buddy's Linux VM (4 shared CPU cores, 7.7 GiB RAM, no GPU), 23 Nov 2026, ~19:42–19:47 WAT. System Python is 3.12.3 — there is no Python 3.11 or conda on this machine, so both envs are Python 3.12.3 venvs (the old build used 3.11 conda envs; see deviation note 1).

---

## Brain env — `~/workspace/connectome-work/envs/brain`

Install commands (in order):
```
python3 -m venv ~/workspace/connectome-work/envs/brain
envs/brain/bin/pip install --upgrade pip
envs/brain/bin/pip install "numpy>=1.24,<2.0" "brian2>=2.9.0" "pandas>=2.0.0" "scipy>=1.10.0" "pyarrow>=14.0.0" "joblib>=1.3.0" "pytest"
envs/brain/bin/pip install "pyarrow==20.0.0"     # ← corrective pin, see failure 1 below
```

Key versions as installed: **Brian2 2.9.0 · numpy 1.26.4 · scipy 1.17.1 · pandas 3.0.6 · pyarrow 20.0.0 · joblib 1.6.0 · pytest 9.2.0 · Python 3.12.3**

Verification run (23 Nov 2026): all six required imports succeed; a trivial 10-neuron LIF network with constant drive ran 100 ms in the pinned env and produced 50 spikes — the Part 1 pass criterion "a trivial Brian2 network runs in the pinned env" is met.

Full `pip freeze`:
```
Brian2==2.9.0
cloudpickle==3.1.3
Cython==3.3.1
iniconfig==2.3.1
Jinja2==3.1.6
joblib==1.6.0
MarkupSafe==3.0.4
mpmath==1.3.0
numpy==1.26.4
packaging==26.3
pandas==3.0.6
pluggy==1.7.0
pyarrow==20.0.0
Pygments==2.21.0
pyparsing==3.3.3
pytest==9.2.0
python-dateutil==4.0.0
scipy==1.17.1
setuptools==84.2.1
sympy==1.14.0
tzdata==2026.6
```

## Body env — `~/workspace/connectome-work/envs/body`

Install commands (in order):
```
python3 -m venv ~/workspace/connectome-work/envs/body
envs/body/bin/pip install --upgrade pip
envs/body/bin/pip install "flygym>=1.2.0" "numpy>=2.0" "mujoco>=3.2.0"
```

Key versions as installed: **flygym 2.1.1 · mujoco 3.16.0 · numpy 2.5.5 · scipy 1.18.1 · Python 3.12.3**

Verification run (23 Nov 2026): `flygym` and `mujoco` import; a minimal MuJoCo model (one free sphere) compiled and stepped 10 steps headless without error. **`neuromechfly` is not a separate import in this install** — that module name belonged to the v1 package; in the current FlyGym (NeuroMechFly v2) line the importable package is `flygym` itself. Recorded so nobody goes looking for a missing module later.

Full `pip freeze`:
```
absl-py==2.5.1
asttokens==3.0.2
contourpy==1.4.0
cycler==0.12.1
etils==1.15.0
executing==2.3.0
flygym==2.1.1
fonttools==4.68.0
fsspec==2026.9.0
glfw==2.11.0
ImageIO==2.38.2
imageio-ffmpeg==0.6.0
ipython==9.19.1
ipython_pygments_lexers==1.1.1
jaxtyping==0.3.7
jedi==0.20.1
kiwisolver==1.5.1
llvmlite==0.50.0
loguru==0.7.3
matplotlib==3.11.2
matplotlib-inline==0.2.2
mediapy==1.2.7
mujoco==3.16.0
numba==0.68.1
numpy==2.5.5
packaging==26.3
parso==0.8.7
pexpect==4.9.0
pillow==12.3.0
prompt_toolkit==3.0.53
psutil==7.2.2
ptyprocess==0.7.0
pure_eval==0.2.4
Pygments==2.21.0
PyOpenGL==3.1.10
pyparsing==3.3.3
python-dateutil==4.0.0
PyYAML==6.0.4
scipy==1.18.1
stack-data==0.6.3
tabulate==0.9.0
traitlets==5.16.1
typing_extensions==4.16.0
tzdata==2026.6
wadler_lindig==0.1.8
wcwidth==0.9.5
websockets==17.4
zipp==4.1.2
```

---

## Failures and retraces during the build (logged per the track rule)

1. **pyarrow 26.0.1 refused to import under numpy 1.26.4.** The first brain-env install resolved `pyarrow>=14.0.0` to pyarrow 26.0.1, which at import time raises `ImportError: pyarrow requires NumPy 2.0 or newer, found 1.26.4`. The brain env's numpy <2 pin is load-bearing (it is the old brain stack's pin, carried into the plan), so pyarrow — not numpy — moved: pinned to **pyarrow 20.0.0**, the newest line verified here to import and run against numpy 1.26.4. This is a deviation from "latest pyarrow" but **not** from the plan: the old `environment.yml` specified `pyarrow>=14.0.0`, and 20.0.0 satisfies it. No other package was affected.
2. **First body-env import test crashed on a test-script bug, not an environment fault:** the check read `flygym.__version__`, which flygym 2.1.1 does not define. Re-run using `importlib.metadata.version('flygym')` → 2.1.1, all checks passed. Recorded so the failed first attempt is not mistaken for an install problem.

## Deviation notes (formal, per the pin discipline)

1. **Python 3.12.3 instead of the old build's 3.11.** This machine has no Python 3.11 and no conda; both envs are 3.12.3 venvs. The Part 0 benchmark already proved Brian2 installs and runs on 3.12, and both envs here verify on 3.12 (imports + trivial network + MuJoCo stepping). The deviation is forced by the machine, is verified harmless for Part 1's purposes, and is recorded here rather than silently absorbed.
2. **Brian2 pinned at 2.9.0 in the brain env** (the plan's `brian2>=2.9.0` floor, resolved exactly), vs 2.10.1 in the Part 0 throwaway env — the benchmark re-run in `PART0-BENCHMARK.md` therefore compares across a Brian2 minor version as well as the numpy pin, and says so.
3. **pandas resolved to 3.0.6** in the brain env (constraint was `pandas>=2.0.0`). A major-version pandas is a real surface for API differences in later parts; it is pinned as installed (3.0.6) so the behaviour is at least reproducible, and Part 2 code must be written against the installed version, not against pandas 2 habits.
4. **MuJoCo is not installed in the brain env.** The old `environment.yml` carried mujoco in the brain env because the old build ran brain+body in one process on Windows. The fresh build's two-env split puts MuJoCo in the body env only; any future one-process bridge work must go through the plan's loop architecture (Part 2b), not by quietly merging the envs.
5. **FlyBody (TuragaLab, from git) is not installed** — per plan and prep, that decision belongs to the Part 1b body-capability audit, not to Part 1.
