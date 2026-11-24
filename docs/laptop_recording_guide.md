# Laptop run guide: recording the closed loop on your own machine

This guide takes you from nothing on your laptop to a finished recording of one real ConnectomeToBehaviour closed loop episode running in your own terminal and IDE, with the files to prove it afterwards. Do the setup on a separate day, not on recording day. The setup is the long part. The run itself takes about a minute.

Words used below: a **chunk** is 100 ms of fly time, the step the loop works in. The **proboscis** is the fly's feeding tube. **MN9** is the pair of feeding motor neurons whose firing drives the proboscis. A **venv** is an isolated Python environment. **UNVERIFIED** means: true as far as the project records go, but nobody has done this exact step on a fresh laptop yet, so treat it as "should work, check it on setup day".

## Windows first: setting up WSL2 (the Linux layer inside Windows)

**If your laptop runs Windows, do this section first, before section 0.** Linux and Mac laptops skip this section completely.

### What WSL2 is, in plain words

WSL2 stands for Windows Subsystem for Linux, version 2. It is a free feature built into Windows by Microsoft that runs a real Ubuntu Linux system inside your Windows laptop, in its own terminal window, alongside Windows. Nothing about Windows is removed and nothing about the project code changes. That last point matters for the recording: the project driver was written expecting a Linux style folder layout (it looks for the brain environment at `envs/brain/bin/python`), and plain Windows keeps Python in a different place (`Scripts/python.exe`), so plain Windows cannot run the driver as it is written. Inside WSL2 the layout is exactly the Linux layout the code expects, so the code runs completely untouched, which is what makes the recording honest proof.

### Step W1. Install WSL2 and Ubuntu 24.04

You need Windows 10 version 2004 or higher, or Windows 11 (that is Microsoft's stated requirement for the install command below).

1. Open PowerShell as administrator. Click the Start button, type `PowerShell`, right click on Windows PowerShell in the results, and choose "Run as administrator". The administrator part is required; a normal PowerShell window will not do it.
2. In that window, type this one command and press Enter:

```
wsl --install -d Ubuntu-24.04
```

Plain `wsl --install` is Microsoft's single install command: it switches on the Windows features WSL needs and installs Ubuntu. The extra `-d Ubuntu-24.04` part is there on purpose. Microsoft does not pin which Ubuntu version the plain command gives you (it just says "Ubuntu"), and the current default can move over time. Ubuntu 24.04 is the version this project wants, for the Python reason in step W3 below, so this guide names it directly instead of hoping the default is right.
3. Restart the laptop when the command tells you to. The install is not finished until you have restarted.

### Step W2. First launch of Ubuntu, and your Ubuntu user

1. After the restart, open Ubuntu from the Start menu (search for "Ubuntu"). The first launch finishes the install, which can take a few minutes, and then asks you to create a user account for Ubuntu: a username and a password.
2. Pick any username you like; it does not have to match your Windows name. While you type the password, nothing appears on screen, not even dots. That is normal Linux behaviour, not a frozen keyboard. You will type this password whenever a command in this guide starts with `sudo`, so use one you will remember on setup day.
3. From this moment on, **everything project related happens inside the Ubuntu terminal**: the clone in section 2, the environments in section 3, and the run in section 6. Wherever the rest of this guide says "open a terminal", on a Windows laptop that means the Ubuntu terminal (or the terminal inside VS Code once it is connected to WSL, step W5). PowerShell is only for the install in step W1 and the version check in step W3.

### Step W3. Check your Ubuntu and Python versions before going further

Still in the Ubuntu terminal, run:

```
lsb_release -a
python3 --version
```

You want to see Ubuntu 24.04 and Python 3.12.something (3.12.3 is ideal; it is the exact version the project environments were built and verified on). Ubuntu 24.04 ships Python 3.12 as its own system Python (that is from Ubuntu's official Python availability page: 24.04 lists 3.12 as its Python), so if you installed Ubuntu 24.04 in step W1, this check should pass with nothing extra to do.

You can also confirm WSL2 itself is the version in use. In PowerShell, run `wsl -l -v`; your Ubuntu 24.04 line should show VERSION 2.

If the Python check does not show 3.12 (for example, you already had a different Ubuntu installed and used that instead), add Python 3.12 alongside it through the deadsnakes archive, which is a long running community archive that packages Python versions Ubuntu does not ship itself:

```
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-venv
```

If you took this deadsnakes route, then in section 3 create the two environments with `python3.12 -m venv` instead of `python3 -m venv`, so the environments are built on 3.12 even though the plain `python3` command still points at the other version. If neither route gives you Python 3.12, stop and tell Buddy before going on; do not build the environments on a different Python and hope.

### Step W4. Install the extra Ubuntu packages the project needs

Before the environment builds in section 3, Ubuntu needs four things: git (to clone the repo), a C compiler (Brian2 builds C code the first time the brain runs, and a fresh Ubuntu has no compiler until you add one), Python 3.12 itself, and the venv package (without it, creating the environments in section 3 fails with a message about ensurepip). One block does all of it:

```
sudo apt update
sudo apt install -y git build-essential python3.12 python3.12-venv
```

`build-essential` is the package that brings in the standard C compiler and build tools. Type your Ubuntu password when `sudo` asks.

### Step W5. Where the project lives inside WSL, and why

Put everything in your Ubuntu home folder. That is the folder you start in when the Ubuntu terminal opens, written as `~` and living at `/home/<your Ubuntu username>`. Section 1's parent folder (`connectome-recording`) goes there, and the clone and the `envs` folder go inside it, exactly as section 1 shows.

Do **not** put the project under `/mnt/c`. Inside Ubuntu, `/mnt/c` is your Windows C: drive seen through a translation layer. Two problems follow. First, speed and behaviour: Microsoft's own guidance is to store files in the WSL file system when you are working in the Linux command line, because working across the two file systems is slower and can trip over differences like file permissions and letter case. Second, this project's driver is fussy about layout: it looks for `envs/brain/bin/python` in the folder beside the repo, in the Linux style. Keeping the whole thing inside the Ubuntu home folder keeps every path in this guide true, word for word.

### Step W6. VS Code on Windows, opened into WSL

This is how you get the recording shot you want: the code in an IDE on Windows, with a real Ubuntu terminal underneath it.

1. Install VS Code on the **Windows** side (from Microsoft, as a normal Windows program; do not try to install it inside Ubuntu). During the Windows install, when it offers additional tasks, tick "Add to PATH". That tick is what makes the `code` command in the next step work.
2. In VS Code, install the extension called **WSL** (by Microsoft). Open the Extensions view (the squares icon on the left), search for "WSL", and install it. This extension is what lets the Windows VS Code window work on files that live inside Ubuntu as if they were local.
3. In the **Ubuntu terminal**, go to the repository folder and open it in VS Code with:

```
cd ~/connectome-recording/ConnectomeToBehaviour
code .
```

The first time, VS Code downloads and installs a small helper (called VS Code Server) inside Ubuntu; that takes a little while and happens only once. Then a VS Code window opens showing the project. Look at the bottom left corner: it should show a WSL indicator naming your Ubuntu. That indicator is your on camera proof that the IDE is working inside Linux, not on the Windows side.
4. The terminal inside that VS Code window (Terminal menu, New Terminal) is an Ubuntu terminal, already in the project folder. That is the terminal you run the demo from in section 6, and the one to record.

### Step W7. Getting the picture and video files out to Windows afterwards

The run leaves its files inside Ubuntu (section 7 lists them). To copy them to Windows for editing or uploading:

- Easiest: in the Ubuntu terminal, go to the output folder and open it in Windows Explorer with `explorer.exe .` (type it exactly like that, with the dot). An Explorer window opens on that Linux folder. Copy the files and paste them into a normal Windows folder.
- Or: open Windows Explorer, type `\\wsl$` in the address bar at the top, and press Enter. You will see your Ubuntu distribution listed; open it, then `home`, then your username folder, and walk down to the project from there.

Both routes are Microsoft documented ways of reaching WSL files from Windows. Copy the files out; do not move them, so the originals stay inside Ubuntu next to the run's other records.

### What in this section is verified, and what is not

Verified against Microsoft and Ubuntu sources on 25 Nov 2026: the administrator PowerShell requirement and the `wsl --install` command installing Ubuntu (Microsoft's "Install WSL" page); the restart and the create a user step after install (same page); the VS Code on Windows plus WSL extension arrangement, the "Add to PATH" tick, and opening a WSL folder from the terminal with `code .` (Microsoft's VS Code "Developing in WSL" page); the advice to keep project files in the WSL file system rather than under `/mnt/c`, the `explorer.exe .` command, and the `\\wsl$` Explorer address (Microsoft's "Working across file systems" page); Ubuntu 24.04 shipping Python 3.12 (Ubuntu's official Python availability page). UNVERIFIED: that the default Ubuntu from a plain `wsl --install` is any particular version, which is exactly why step W1 names Ubuntu-24.04 directly; and the whole WSL2 route end to end for this project, because nobody has run this project inside WSL2 yet. Setup day, with the practice run in the checklist in section 9, is where that gets verified.

## 0. What you need

- A laptop. Linux and macOS laptops go straight to section 1. **Windows laptops do the WSL2 section above first** and then follow the rest of this guide inside Ubuntu: plain Windows cannot run the project driver as written, because the driver looks for the brain environment at a fixed path written in the Unix style, `envs/brain/bin/python`, and a normal Windows venv keeps its Python at `Scripts/python.exe` instead. The project code is not changed for this; WSL2 gives it the Linux layout it expects.
- Python 3.12 (the project environments were built and verified on Python 3.12.3; other versions are UNVERIFIED).
- Git.
- A C compiler for the brain build (on Linux this is the usual build tools package; on macOS the Xcode command line tools). Brian2 compiles code the first time the brain runs. This was present on the project machine; whether your laptop has it is UNVERIFIED, and setup day is when to find out.
- Roughly 2 GB of free disk space and a decent internet connection for setup day (the clone is about 282 MB on the project machine, and the two environments download several hundred MB more of packages). Time estimate for the whole setup: 30 to 60 minutes, mostly waiting on downloads. That estimate is UNVERIFIED for your connection.

## 1. The folder layout (read this first, it matters)

The project driver finds the brain environment by a fixed rule: it looks for a folder called `envs` **next to** the repository folder, not inside it. So everything lives inside one parent folder, like this:

```
connectome-recording/
    envs/
        brain/     (first environment, created in step 3)
        body/      (second environment, created in step 3)
    ConnectomeToBehaviour/    (the repository, cloned in step 2)
```

If the `envs` folder ends up anywhere else, the run will stop with a message telling you exactly that. Pick a parent folder name you like; only the inside layout matters.

## 2. Clone the repository

Open a terminal, go to where you want the parent folder, and run:

```
mkdir connectome-recording
cd connectome-recording
git clone https://github.com/visionbyangelic/ConnectomeToBehaviour.git
```

The clone includes the data files the run needs (the wiring map and the neuron lists are tracked in the repo), so there is nothing else to download for the run itself.

Check what you have (you will show this on camera later):

```
cd ConnectomeToBehaviour
git log --oneline -3
git tag -l
```

You should see the tag `part5-prereg-v1` in the list. That tag marks the Part 5 freeze commit, `b88520b`, the frozen state of the experiment this demo belongs to.

## 3. Build the two environments

The brain stack and the body stack need different versions of the same library (numpy), so the project keeps them in two separate environments. These are the exact install commands recorded in the project's own `docs/environments.md`. Run them from the **parent** folder (`connectome-recording`), not from inside the repo:

```
cd ..        (so you are in connectome-recording, beside the repo)

python3 -m venv envs/brain
envs/brain/bin/pip install --upgrade pip
envs/brain/bin/pip install "numpy>=1.24,<2.0" "brian2>=2.9.0" "pandas>=2.0.0" "scipy>=1.10.0" "pyarrow>=14.0.0" "joblib>=1.3.0" "pytest"
envs/brain/bin/pip install "pyarrow==20.0.0"

python3 -m venv envs/body
envs/body/bin/pip install --upgrade pip
envs/body/bin/pip install "flygym>=1.2.0" "numpy>=2.0" "mujoco>=3.2.0"
```

Notes:

- The second pyarrow line is deliberate, not a repeat: the newest pyarrow refuses to work with the brain stack's numpy, and 20.0.0 is the version the project verified. It is in the project's environment record.
- The versions you should end up with (from the project record): brain environment: Brian2 2.9.0, numpy 1.26.4, pyarrow 20.0.0. Body environment: FlyGym 2.1.1, MuJoCo 3.16.0, numpy 2.5.5. Small differences in the minor packages are fine; if Brian2, FlyGym or MuJoCo land on very different versions, stop and note it, because the recorded comparison numbers come from these versions.
- There is no single requirements file in the repo for this. The commands above, taken from `docs/environments.md`, are the setup. That is a gap in the repo, recorded here honestly rather than papered over.
- Quick check that both environments import what they need:

```
envs/brain/bin/python -c "import brian2, numpy; print('brain ok', numpy.__version__)"
envs/body/bin/python -c "import flygym, mujoco; print('body ok')"
```

## 4. Check the demo script is in place

`run_recording_demo.py` already sits at the repository root (beside `README.md`) when you clone or pull this repo, so there is nothing to copy. Just check it is there: `ls run_recording_demo.py` from the repository root should name the file. The script finds the repo from its own location, so it has to sit there, and it is run from the repo root.

Then do one full practice run off camera (step 6 has the command). The first ever run on a new machine is the one that finds missing compilers and slow downloads. Never let the recording be the first run.

## 5. Set up the recording

- Open the `ConnectomeToBehaviour` folder in your IDE (VS Code or whichever you use). On a Windows laptop, do this the WSL way from step W6 above (`code .` in the Ubuntu terminal), so the IDE is connected to WSL and its terminal is an Ubuntu terminal.
- Open `run_recording_demo.py` in the editor, so the code is on screen. Scroll to the top so the opening explanation is visible.
- Open the IDE's built in terminal at the bottom (in VS Code: Terminal menu, New Terminal) and make sure it starts in the repository root. Run `pwd` and `ls`; you should see `README.md` and `src`.
- Screen layout for the shot: code in the top two thirds, terminal in the bottom third, font large enough to read on a phone (terminal text is the evidence here, make it big).
- Optional but strong for believability: keep a clock visible, and say the date and your name at the start. The script also prints the date, time and git commit itself, in the terminal, at the moment of the run.

## 6. The run: one command

From the repository root, in the IDE terminal:

```
../envs/body/bin/python run_recording_demo.py
```

That is the whole run. The body environment's Python drives; the script spawns the brain environment's Python itself, as the project driver does.

What you will see, in order:

1. A banner: project name, the date and time on your laptop, the git commit, the scenario name, and the brain seed (5101).
2. "Building the brain and settling the body." On the project machine the brain build plus its compile warmup took about 9 seconds, and the body settled in 4 chunks. First run on your machine may take longer here (compiler caches are cold).
3. One line per chunk, 40 lines, in plain words: chunk number, the filtered feeding neuron rate in Hz, the extension in radians, and whether food contact is ON or off. Watch for contact switching ON at about chunk 5, and staying on after chunk 9, when the scripted ignition window has closed and only the touch is keeping the drive alive. That hand over is the closed loop moment; it is worth saying out loud on the recording.
4. A closing block: the verdict of the smoke checks (expect PASS), first contact chunk, peak extension, the file paths, and the SHA-256 hash of the summary file.

How long: the recorded run of this exact scenario on the project machine took 54.4 seconds of wall clock in total, about 1.36 seconds per chunk. Your laptop will differ (faster or slower, UNVERIFIED), and rendering the pictures and video adds a little time that has never been measured (UNVERIFIED). Budget two minutes on camera, not more.

If the body does not settle or touches the food during the settle, the script stops and says the episode is INVALID, in those words. That is the project's own rule, not a crash. Run it once more; keep both attempts if it happens on camera, it is honest footage.

## 7. What the run leaves behind

Everything lands in `results/closed_loop/recording_demo/` inside the repo:

- `summary.json`: the episode's measured summary (chunks completed, first contact chunk, peak extension, total MN9 spikes, the smoke verdict).
- `demo_record.json`: the git commit, seed, settings and the summary's hash, in one small file.
- `brain_log.jsonl` and `body_log.jsonl`: the full per chunk records, brain side and body side.
- `brain_worker.log`: the brain process's own log, including its build time.
- `frame_rest.png`: the body at rest after settling.
- `frame_contact.png`: the body at the first food contact chunk.
- `frame_peak_extension.png`: the body at its widest extension.
- `recording_demo_video.mp4`: one frame per chunk at 10 frames per second, about 4 seconds of video, the extension and contact as they happened.

About the pictures and video: **UNVERIFIED end to end.** No project code had ever rendered this body before this pack, so the capture is written against the pinned FlyGym renderer's own documented API (the model even ships a camera called "hero", which the script uses), and it is built to fail politely: if rendering does not work on your laptop, the episode still runs, the logs and summary are still written, and the terminal says pictures were skipped. Test this on setup day. If the video is missing after the practice run, that is a known possible outcome, not a surprise to discover on camera.

## 8. How a viewer can check it is real

This is the part to say on the recording, and to put in the video description:

1. **The commit.** The banner prints the git commit of the code that ran. The same commit is public on GitHub at https://github.com/visionbyangelic/ConnectomeToBehaviour, and the freeze tag `part5-prereg-v1` is there for anyone to inspect.
2. **The hash.** The terminal prints the SHA-256 hash of `summary.json` at the end of the run. Anyone with that file can run `sha256sum results/closed_loop/recording_demo/summary.json` (on macOS: `shasum -a 256 ...`) and get the identical string, proving the file was not edited after the run. The same hash is stored in `demo_record.json`.
3. **The comparison.** The repository already contains the recorded run of this same scenario from the project machine, at `results/closed_loop/s1_smoke/summary.json`: first contact at chunk 5, peak extension 2.058 rad, 608 MN9 spikes, verdict PASS. Your run should land on the same numbers or extremely close. Small differences in the last decimal places can come from a different processor; the shape of the result (contact chunk, verdict, spike count) is the check. Whether a different laptop reproduces the numbers bit for bit is UNVERIFIED.
4. **The code is the project's code.** The demo script only drives the existing modules (`src/closed_loop/run_loop5.py`, `brain_worker.py`, `body_side.py`, `chain.py`) and prints what they report. Nothing in the episode is drawn, scripted frame by frame, or typed in by hand.

## 9. Recording checklist

Setup day (not on camera):

- [ ] Parent folder layout correct: `envs` beside `ConnectomeToBehaviour`
- [ ] Both environments built; both import checks pass
- [ ] Demo script copied into the repository root
- [ ] One full practice run done; summary written; verdict PASS
- [ ] (Windows only) Inside WSL, the practice run completed AND the outputs are really there and reachable from Windows: `frame_rest.png`, `frame_contact.png`, `frame_peak_extension.png` and `recording_demo_video.mp4` all exist in `results/closed_loop/recording_demo/`, you copied them out to a Windows folder using `explorer.exe .` or the `\\wsl$` address from step W7, and the MP4 opens and plays on the Windows side
- [ ] Pictures and video checked: do the three PNGs and the MP4 exist? (If not, see the UNVERIFIED note in section 7 and decide before recording day whether to proceed with logs only)
- [ ] Battery charged, notifications off, terminal font enlarged

Recording day, in this order:

- [ ] Shot 1: IDE open, `run_recording_demo.py` on screen, scroll slowly through the top explanation
- [ ] Shot 2: terminal in view; show `git log --oneline -3` and `git tag -l` (the freeze tag on screen)
- [ ] Shot 3: type the run command slowly, press enter, let the banner fill the screen (date, time, commit, seed)
- [ ] Shot 4: the 40 chunk lines; narrate the contact moment at about chunk 5 and the hand over after chunk 9
- [ ] Shot 5: the closing block; read out the verdict and the first part of the hash
- [ ] Shot 6: open the `recording_demo` folder; play the MP4; open `summary.json`
- [ ] Shot 7 (optional, strong): the GitHub page for the repo, showing the same tag and commit

## 10. Honest list: what is verified and what is not

Verified from the project records and code:

- The scenario (S1: event gated sugar, seed 5101, 40 chunks, ignition window chunks 0 to 9) exists in `src/closed_loop/run_loop5.py` exactly as used here, and its recorded run reached contact at chunk 5 with verdict PASS in 54.4 seconds.
- The two process design (body environment driver, brain environment worker, JSON lines contract) is how the existing driver already works; this pack changes none of it.
- The environment versions and install commands are the project's own record in `docs/environments.md`.
- The FlyBody model in the pinned FlyGym ships cameras, including one named "hero", and FlyGym ships a renderer with a save to video function. The API the capture code calls is real.

UNVERIFIED (never done anywhere yet):

- The full setup on a fresh laptop, start to finish. The environments were only ever built on the project machine.
- Rendering this body to pictures or video. The capture code is new, written for this pack, and has only been syntax checked.
- Windows laptops through WSL2 (see the Windows section at the top of this guide): every WSL2 step there is documented by Microsoft and Ubuntu, but nobody has run this project inside WSL2 yet, so the Windows route as a whole stays UNVERIFIED until the setup day practice run passes.
- Exact run timings on your hardware.
- Bit for bit identical numbers on a different processor.
