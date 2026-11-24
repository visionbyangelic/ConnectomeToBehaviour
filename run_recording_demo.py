"""Recording demo: one real closed loop feeding episode, run live.

What this script is for
-----------------------
This runs ONE short, real episode of the ConnectomeToBehaviour closed
loop on this laptop, printing what happens chunk by chunk, so the run
can be recorded on camera (terminal and IDE in shot) and checked
afterwards against the files it writes. It is the project's own smoke
scenario S1 from src/closed_loop/run_loop5.py:

  - the frozen brain is driven by the right sugar taste neurons at
    200 Hz, seed 5101, for 40 chunks of 100 ms (4 seconds of fly time);
  - for chunks 0 to 9 a scripted window switches the drive on (the
    ignition); after that, only the taste event can keep it on, and
    the taste event only exists if the body actually touches the food;
  - in the recorded S1 run on the project machine the proboscis
    reached the food at chunk 5 and the loop then kept itself going
    to the end. That is the behaviour this demo should reproduce.

It is a demonstration, not a science result: it uses the smoke value
r_hi = 155 Hz exactly as run_loop5.py defines it for S1, labelled
PROVISIONAL there, so its numbers can be compared line by line with
the recorded run in results/closed_loop/s1_smoke/. The Part 5
evaluation episodes use the calibrated r_hi from the freeze instead,
and none of them is run by this script.

How it works
------------
The loop is the project's own code, not a copy of it. The driver runs
in the body environment (FlyGym and MuJoCo) and spawns the brain
worker (src/closed_loop/brain_worker.py) in the brain environment as
a second process; the two talk over a JSON lines contract, one
message per 100 ms chunk. This script drives the same pieces the
project driver drives, in the same order (brain chunk, then the
registered chain in chain.py, then the body chunk), and adds three
things the project driver does not do: a printed banner, a plain
words progress line per chunk, and picture/video capture.

Run it from the repository root, with the body environment's Python:

  ../envs/body/bin/python run_recording_demo.py

Outputs land in results/closed_loop/recording_demo/ inside the repo:
summary.json, the two per chunk logs, three still pictures and, if
rendering works on this machine, a short video. The SHA-256 hash of
summary.json is printed at the end; anyone with the file can check
that the file on disk is the file this run produced.
"""

import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------- repo
# The script sits in the repository root. If it is run from somewhere
# else, fall back to the current folder, as long as one of the two
# really is the repo root.
def find_repo_root():
    for candidate in (Path(__file__).resolve().parent, Path.cwd()):
        if (candidate / "src" / "closed_loop" / "run_loop5.py").exists():
            return candidate
    raise SystemExit(
        "Could not find the repository root. Run this script from the "
        "ConnectomeToBehaviour folder, where it sits at the root.")


REPO = find_repo_root()
CLOSED_LOOP = REPO / "src" / "closed_loop"
sys.path.insert(0, str(CLOSED_LOOP))   # run_loop5, chain, body_side
sys.path.insert(0, str(REPO / "src"))  # not strictly needed here, but
                                       # matches how the worker imports

import chain as chain_mod          # noqa: E402  the registered chain
import loop_protocol as protocol   # noqa: E402  scenario validation
import run_loop5                   # noqa: E402  driver pieces + S1
from body_side import FeedingBody  # noqa: E402  the qualified body

OUT_DIR = REPO / "results" / "closed_loop" / "recording_demo"
CAMERA = "hero"        # a camera built into the pinned FlyBody model
VIDEO_FPS = 10         # one rendered frame per 100 ms chunk, played
                       # back at 10 frames per second, so the video
                       # runs at the same speed as the simulated fly


# ------------------------------------------------------------- banner
def print_banner(scenario):
    git = run_loop5.git_state()
    now = datetime.now().strftime("%A %d %B %Y, %H:%M:%S")
    print("=" * 68)
    print("ConnectomeToBehaviour: live closed loop recording demo")
    print("=" * 68)
    print(f"Date and time on this laptop : {now}")
    print(f"Git commit                   : {git['head']}")
    tags = ", ".join(git["tags_at_head"]) or "(none at this commit)"
    print(f"Git tags at this commit      : {tags}")
    print(f"Scenario                     : {scenario['name']}")
    print(f"Brain seed                   : {scenario['seed']}")
    print(f"Chunks                       : {scenario['n_chunks']} "
          f"chunks of 100 ms (4 seconds of fly time)")
    print("What should happen: the sugar drive switches the brain on,")
    print("the feeding neurons answer, the proboscis (feeding tube)")
    print("reaches out, touches the food at about chunk 5, and after")
    print("chunk 9 the touch alone keeps the loop running.")
    print("=" * 68, flush=True)
    return git


def preflight():
    """Fail early, in plain words, if the setup is not in place."""
    if sys.platform.startswith("win"):
        raise SystemExit(
            "This script is running under plain Windows Python, and "
            "the project driver cannot run there: it looks for the "
            "brain environment at a Linux style path, "
            "envs/brain/bin/python, which a Windows environment does "
            "not have. Nothing has been changed or damaged. On a "
            "Windows laptop this demo runs inside WSL2 (the Linux "
            "layer inside Windows) instead, with the project code "
            "completely untouched. Follow the section called "
            "'Windows first: setting up WSL2 (the Linux layer inside "
            "Windows)' at the top of docs/laptop_recording_guide.md, "
            "then run "
            "this script again from the Ubuntu terminal there.")
    brain_python = run_loop5.BRAIN_PYTHON
    if not brain_python.exists():
        raise SystemExit(
            "The brain environment was not found where the driver "
            f"expects it:\n  {brain_python}\n"
            "The driver looks for envs/brain/bin/python in the folder "
            "that CONTAINS the repository folder. See the setup steps "
            "in docs/laptop_recording_guide.md; the two environments "
            "must be created as a sibling folder of the repo, named "
            "envs. "
            "On a Windows laptop, also check the section called "
            "'Windows first: setting up WSL2 (the Linux layer inside "
            "Windows)' at the top of that guide: this script must be "
            "running inside Ubuntu in WSL2, with the repo and the "
            "envs folder in the Ubuntu home folder, not under "
            "/mnt/c.")
    for name in ("2023_03_23_connectivity_630_final.parquet",):
        if not (REPO / "data" / name).exists():
            raise SystemExit(
                f"Data file missing: data/{name}. The clone looks "
                "incomplete; clone the repository again.")


# ---------------------------------------------------------- rendering
class FrameCapture:
    """Picture and video capture, using FlyGym's own renderer.

    PREPARED BUT NOT YET TESTED END TO END: no code in this project
    has ever rendered the feeding body, so this class is written
    against the documented API of the pinned FlyGym 2.1.1 (the
    Simulation.set_renderer method and the flygym Renderer, which
    buffers one RGB frame per call to render_as_needed and can save
    them as a video). If anything about rendering fails on this
    laptop, the episode still runs and is still recorded in the logs;
    only the pictures are skipped, and the script says so out loud.

    One frame is taken at rest (straight after the settle) and one
    after every chunk. The renderer is told the frames are 0.1 s of
    fly time apart (playback_speed 1.0 at 10 frames per second), so
    it takes exactly one frame per chunk.
    """

    def __init__(self, body):
        self.ok = False
        self.renderer = None
        self.snapshots = []      # (label, frame) pairs, in order
        try:
            self.renderer = body.sim.set_renderer(
                CAMERA, camera_res=(480, 640),
                playback_speed=1.0, output_fps=VIDEO_FPS)
            self.ok = True
        except Exception as exc:
            print(f"WARNING: rendering could not be started "
                  f"({type(exc).__name__}: {exc}). The episode will "
                  "still run; pictures and video will be skipped.",
                  flush=True)

    def snap(self, body, label):
        """Render the body's current pose and keep the frame."""
        if not self.ok:
            return
        try:
            if body.sim.render_as_needed():
                frames = self.renderer.frames[CAMERA]
                self.snapshots.append((label, frames[-1]))
        except Exception as exc:
            print(f"WARNING: rendering stopped ({exc}). Continuing "
                  "without pictures.", flush=True)
            self.ok = False

    def save_stills(self, out_dir, contact_chunk, peak_chunk):
        """Save the rest, first contact and peak extension frames."""
        if not self.snapshots:
            return []
        import imageio.v3 as iio   # ships with the body environment
        by_label = dict(self.snapshots)
        wanted = [("frame_rest", "rest"),
                  ("frame_contact", f"chunk {contact_chunk}"),
                  ("frame_peak_extension", f"chunk {peak_chunk}")]
        saved = []
        for stem, label in wanted:
            frame = by_label.get(label)
            if frame is None:
                continue
            path = out_dir / f"{stem}.png"
            iio.imwrite(path, frame)
            saved.append(path)
        return saved

    def save_video(self, out_dir):
        if not self.ok or self.renderer is None:
            return None
        path = out_dir / "recording_demo_video.mp4"
        try:
            self.renderer.save_video(path)
            return path
        except Exception as exc:
            print(f"WARNING: the video could not be saved ({exc}).",
                  flush=True)
            return None


# -------------------------------------------------------------- main
def main():
    scenario_in = dict(run_loop5.SCENARIOS["S1"])
    preflight()
    git = print_banner(scenario_in)
    scenario = protocol.validate_scenario(scenario_in)
    r_hi = run_loop5.R_HI_SMOKE            # 155 Hz, the S1 smoke value
    r_hi_label = run_loop5.R_HI_SMOKE_LABEL

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wall0 = time.time()
    worker_log = open(OUT_DIR / "brain_worker.log", "w")
    link = run_loop5.BrainLink(scenario, worker_log)
    brain_records, body_records = [], []
    capture = None
    summary = {}
    try:
        # The body settles while the brain builds; the settle uses no
        # brain input at all, exactly as in the project driver.
        print("Building the brain and settling the body. The brain "
              "build took about 9 seconds on the project machine...",
              flush=True)
        body = FeedingBody()
        ready = link.read_ready()
        print(f"Brain ready. Body settled in "
              f"{body.settle_record['n_chunks']} chunks. "
              f"Episode valid: {body.valid}", flush=True)
        if not body.valid:
            raise SystemExit(
                "The episode is INVALID: the body did not settle, or "
                "it touched the food during the settle. Nothing was "
                "run. This is recorded behaviour, not a crash; try "
                "the run once more and keep the log either way.")

        capture = FrameCapture(body)
        capture.snap(body, "rest")

        fchain = chain_mod.FeedingChain(body.params, run_loop5.SIGNS,
                                        r_lo=run_loop5.R_LO, r_hi=r_hi)
        fchain.set_rest(body.theta_rest)
        event_state = False   # taste event at the end of chunk k - 1
        first_contact = None
        peak_chunk, peak_e = None, -1.0
        for k in range(scenario["n_chunks"]):
            # 1. brain chunk, gated by the taste event from chunk k-1
            reply = link.chunk(k, event_state)
            brain_records.append(reply)
            counts = reply["counts"]
            # 2. the registered chain turns MN9 counts into commands
            out = fchain.update(counts["mn9_left"],
                                counts["mn9_right"])
            # 3. body chunk under those commands
            rec = body.step_chunk(out["ctrls"])
            angles = {j: rec["angles_rad"][j]
                      for j in chain_mod.PROBOSCIS}
            rec["E_rad"] = fchain.extension_E(angles)
            rec["r_window_hz"] = out["r_window_hz"]
            rec["r_filt_hz"] = out["r_filt_hz"]
            rec["e"] = out["e"]
            rec["targets_rad"] = out["targets"]
            rec["ctrls_rad"] = out["ctrls"]
            rec["taste_event_sent_to_brain"] = event_state
            body_records.append(rec)
            event_state = rec["taste_event_at_chunk_end"]
            capture.snap(body, f"chunk {k}")
            if event_state and first_contact is None:
                first_contact = k
            if rec["E_rad"] > peak_e:
                peak_e, peak_chunk = rec["E_rad"], k
            contact = "ON " if event_state else "off"
            print(f"Chunk {k + 1:2d} of {scenario['n_chunks']}: "
                  f"feeding neurons {out['r_filt_hz']:6.1f} Hz, "
                  f"extension {rec['E_rad']:5.2f} rad, "
                  f"food contact {contact}", flush=True)
        summary = run_loop5.summarise(scenario, brain_records,
                                      body_records)
        body.close()
    finally:
        try:
            link.close()
        except Exception:
            link.proc.kill()
        worker_log.close()

    # ------------------------------------------------------ outputs
    wall = time.time() - wall0
    summary["wall_clock_s"] = wall
    summary_path = OUT_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    with open(OUT_DIR / "brain_log.jsonl", "w") as fh:
        for reply in brain_records:
            fh.write(protocol.dumps_line(reply))
    with open(OUT_DIR / "body_log.jsonl", "w") as fh:
        for rec in body_records:
            fh.write(json.dumps(rec) + "\n")
    digest = hashlib.sha256(summary_path.read_bytes()).hexdigest()
    record = {"git_head": git["head"], "git_tags_at_head":
              git["tags_at_head"], "scenario": scenario["name"],
              "seed": scenario["seed"], "r_hi_hz": r_hi,
              "r_hi_provenance": r_hi_label, "wall_clock_s": wall,
              "summary_sha256": digest}
    (OUT_DIR / "demo_record.json").write_text(json.dumps(record,
                                                         indent=2))

    stills = []
    video = None
    if capture is not None:
        stills = capture.save_stills(
            OUT_DIR, summary.get("first_contact_event_chunk"),
            peak_chunk)
        video = capture.save_video(OUT_DIR)

    print("=" * 68)
    print(f"Done in {wall:.1f} seconds of wall clock time.")
    print(f"Smoke verdict (the S1 checks in run_loop5.py): "
          f"{summary.get('smoke_verdict')}")
    print(f"First food contact at chunk: "
          f"{summary.get('first_contact_event_chunk')}")
    print(f"Peak extension: {summary.get('peak_E_rad')} rad")
    print(f"Total feeding neuron (MN9) spikes: "
          f"{summary.get('total_mn9_spikes')}")
    print(f"Summary file : {summary_path}")
    print(f"Summary SHA-256 hash: {digest}")
    for path in stills:
        print(f"Still picture: {path}")
    if video is not None:
        print(f"Video        : {video}")
    print("Compare with the recorded S1 run at "
          "results/closed_loop/s1_smoke/summary.json: contact at "
          "chunk 5, peak extension 2.058 rad, verdict PASS.")
    print("=" * 68, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
