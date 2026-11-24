"""SS2.4 resting acceptance test (Part 4 specs, pre-registered).

N = 10 resting episodes per configuration -- (A) feeding arena (pinned
FlyBody, SS4.6 arena as qualified at gate execution #5, proboscis
contact pairs included) and (B) walk/halt arena (Part 2b loop
configuration: NeuroMechFly legs-only body, HybridTurningController
pathway, SS5.3 JON channel). Each episode: settle per SS2.3 (zero
command; 3 consecutive chunks with leg-contact transitions <= 2 and
thorax height change <= 0.01 mm; 30-chunk cap, else INVALID), then
3.0 s (30 chunks) with no command and no stimulus pulse, feedback
detectors armed from t = 0.

Pass rule (SS2.4, pre-registered): zero false ignitions across all 10
episodes per configuration. A false ignition is (a) the constructed
channel (SS4.5 taste event / SS5.3 JON channel) switching ON at any
point in the episode, or (b) any single chunk exceeding its channel's
on-threshold whether or not the state machine switches -- JON: >= 8
transitions in a chunk; taste: the SS4.5 contact condition (qualifying
contact force > 0 against the food geom) sustained >= 10 consecutive
physics steps within the chunk.

Invalid episodes are never silently replaced: attempts continue until
10 valid episodes exist or 13 attempts are used, and every attempt is
recorded either way.

Runs in the body environment (FlyGym 2.1.1 / MuJoCo). Usage:
  python acceptance_test.py [--config A|B] [--episodes N]
Writes results/acceptance_test.json (merged across configs).
"""

import argparse
import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

import sys

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "part2b"))

from flygym.compose import ActuatorType  # noqa: E402

from gate_common import (CHUNK_STEPS, PROBOSCIS, build_sim, dof_index,  # noqa: E402
                         settle)
from gate_common3 import (FRONT_TARSUS_BODIES, RESULTS,  # noqa: E402
                          food_contact_forces, geom_ids_for_bodies,
                          labrum_tip_pos)
from q5_rerun5 import build_arena  # noqa: E402

N_EPISODES = 10
MAX_ATTEMPTS = 13
REST_CHUNKS = 30          # 3.0 s at 100 ms chunks
ON_STEPS = 10             # SS2.4/SS4.5 debounce: contact ON >= 10 steps
OFF_STEPS = 50            # contact OFF >= 50 steps
JON_ON = 8                # SS5.3: chunk transitions >= 8 -> ON
JON_OFF = 2               # SS5.3: chunk transitions <= 2 -> OFF


# ----------------------------------------------------------------------
# Configuration A -- feeding arena (FlyBody, SS4.6 as qualified)
# ----------------------------------------------------------------------

def feeding_episode(ep_idx):
    rec = {"episode": ep_idx, "config": "A_feeding"}

    # Pilot settle on plain ground -> arena centre (SS4.6 placement,
    # frozen offset 0.6 mm; same construction as Q5 execution #5).
    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    st = settle(sim, fly, np.zeros(len(order)))
    assert st["settled"], "pilot settle failed"
    tip = labrum_tip_pos(sim)
    head_id = mj.mj_name2id(sim.mj_model, mj.mjtObj.mjOBJ_BODY,
                            "flybody/c_head")
    head = sim.mj_data.xpos[head_id]
    forward = np.array([tip[0] - head[0], tip[1] - head[1]])
    forward = forward / np.linalg.norm(forward)
    tip_proj = np.array([tip[0], tip[1]])
    sim.close()
    centre = tip_proj + 0.6 * forward
    rec["arena_centre_xy_mm"] = [float(x) for x in centre]

    fly, world, sim = build_arena(centre)
    m = sim.mj_model
    idx, order = dof_index(fly)
    food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
    labrum_gids = {mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n) for n in
                   ("flybody/l_labrum_lower", "flybody/r_labrum_lower")}
    tarsus_gids = geom_ids_for_bodies(sim, FRONT_TARSUS_BODIES)
    adh_ids = [mj.mj_name2id(m, mj.mjtObj.mjOBJ_ACTUATOR,
                             f"flybody/{s}_labrum-adhesion")
               for s in ("l", "r")]

    warm = {"run": 0, "max_run": 0}

    def food_check():
        lf, tf = food_contact_forces(sim, food_gid, labrum_gids,
                                     tarsus_gids)
        if (lf + tf) > 0:
            warm["run"] += 1
            warm["max_run"] = max(warm["max_run"], warm["run"])
            return True
        warm["run"] = 0
        return False

    st = settle(sim, fly, np.zeros(len(order)), food_check=food_check)
    rec["settle_chunks"] = st["n_chunks"]
    rec["settle_chunk_details"] = st["chunks"]
    rec["settled"] = st["settled"]
    rec["food_contact_during_warmup"] = st["food_contact_during_warmup"]
    rec["warmup_max_qualifying_run_steps"] = warm["max_run"]
    if not st["settled"] or st["food_contact_during_warmup"]:
        rec["status"] = "INVALID"
        rec["invalid_reason"] = (
            "settle cap reached (SS2.3)" if not st["settled"]
            else "food contact during warmup (SS2.3 feeding addition)")
        rec["false_ignition"] = None
        sim.close()
        return rec
    rec["status"] = "VALID"

    # Resting phase: 30 chunks, e = 0 (ctrl 0 on the proboscis DoFs;
    # the zero vector is also the legs'/held joints' command, exactly
    # as in the gate's settle), labrum adhesion held off (the SS4.3
    # adhesion rule engages only on a taste event; the event detector
    # is what this test judges). Taste event per SS4.5/SS2.4.
    zero_ctrl = np.zeros(len(order))
    state = {"on_streak": 0, "off_streak": 0, "event_on": False}
    chunks = []
    false_ignition = False
    fi_detail = None
    for c in range(REST_CHUNKS):
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, zero_ctrl)
        for aid in adh_ids:
            sim.mj_data.ctrl[aid] = 0.0
        run = 0
        max_run = 0
        max_lf = 0.0
        max_tf = 0.0
        event_on_any = False
        for _ in range(CHUNK_STEPS):
            sim.step()
            lf, tf = food_contact_forces(sim, food_gid, labrum_gids,
                                         tarsus_gids)
            max_lf = max(max_lf, lf)
            max_tf = max(max_tf, tf)
            if (lf + tf) > 0:
                run += 1
                max_run = max(max_run, run)
                state["on_streak"] += 1
                state["off_streak"] = 0
                if state["on_streak"] >= ON_STEPS and not state["event_on"]:
                    state["event_on"] = True
            else:
                run = 0
                state["off_streak"] += 1
                state["on_streak"] = 0
                if state["off_streak"] >= OFF_STEPS and state["event_on"]:
                    state["event_on"] = False
            if state["event_on"]:
                event_on_any = True
        chunks.append({
            "chunk": c,
            "max_qualifying_run_steps": max_run,
            "event_on_at_chunk_end": bool(state["event_on"]),
            "event_on_any_step": event_on_any,
            "max_labrum_food_force_N": max_lf,
            "max_front_tarsus_food_force_N": max_tf,
        })
        if (event_on_any or max_run >= ON_STEPS) and not false_ignition:
            false_ignition = True
            fi_detail = {
                "chunk": c,
                "kind": ("channel_on" if event_on_any
                         else "chunk_threshold_exceeded"),
                "max_qualifying_run_steps": max_run}
    rec["chunks"] = chunks
    rec["false_ignition"] = false_ignition
    rec["false_ignition_detail"] = fi_detail
    sim.close()
    return rec


# ----------------------------------------------------------------------
# Configuration B -- walk/halt arena (Part 2b loop configuration)
# ----------------------------------------------------------------------

def walkhalt_episode(ep_idx):
    from flygym.compose.world.flat_ground import FlatGroundWorld
    from flygym.simulation import Simulation
    from flygym.utils.math import Rotation3D
    from flygym_demo.complex_terrain import (
        HybridControllerObservation, HybridTurningController,
        apply_locomotion_action, make_locomotion_fly)
    from sensory import ContactTransitions

    rec = {"episode": ep_idx, "config": "B_walkhalt"}
    fly_name = "nmf"
    fly = make_locomotion_fly(name=fly_name)
    world = FlatGroundWorld()
    world.add_fly(fly, (0, 0, 0.8), Rotation3D("quat", (1, 0, 0, 0)))
    sim = Simulation(world)
    sim.reset()
    controller = HybridTurningController(timestep=sim.timestep)
    thorax_idx = [s.name for s in fly.get_bodysegs_order()].index("c_thorax")
    steps_per_chunk = int(round(0.1 / sim.timestep))
    rec["timestep_s"] = float(sim.timestep)
    rec["steps_per_chunk"] = steps_per_chunk
    signal = np.array([0.0, 0.0])   # zero descending command throughout

    def contact_flags():
        contact, *_ = sim.get_ground_contact_info(fly_name)
        flags = np.asarray(contact).reshape(-1)
        if len(flags) != 6:
            raise RuntimeError(f"expected 6 leg contact flags, "
                               f"got {len(flags)}")
        return [bool(f) for f in flags]

    def thorax_z():
        return float(np.asarray(
            sim.get_body_positions(fly_name)[thorax_idx], dtype=float)[2])

    transitions = ContactTransitions(n_legs=6)
    transitions.set_baseline(contact_flags())

    def run_chunk():
        """One 100 ms chunk at zero command; returns (transitions, dh)."""
        n_trans = 0
        heights = []
        for _ in range(steps_per_chunk):
            obs = HybridControllerObservation.from_sim(sim, fly_name)
            action = controller.step(signal, obs)
            apply_locomotion_action(sim, fly_name, action)
            sim.step()
            n_trans += transitions.update(contact_flags())
            heights.append(thorax_z())
        heights = np.array(heights)
        return n_trans, float(heights.max() - heights.min())

    # Warmup / settle per SS2.3: transitions counted, never converted.
    settle_chunks = []
    good_streak = 0
    settled = False
    for c in range(30):
        n_trans, dh = run_chunk()
        ok = n_trans <= 2 and dh <= 0.01
        settle_chunks.append({"chunk": c, "transitions": n_trans,
                              "thorax_dh_mm": dh, "ok": bool(ok)})
        good_streak = good_streak + 1 if ok else 0
        if good_streak >= 3:
            settled = True
            break
    rec["settle_chunks"] = len(settle_chunks)
    rec["settle_chunk_details"] = settle_chunks
    rec["settled"] = settled
    if not settled:
        rec["status"] = "INVALID"
        rec["invalid_reason"] = "settle cap reached (SS2.3)"
        rec["false_ignition"] = None
        sim.close()
        return rec
    rec["status"] = "VALID"

    # Resting phase: JON channel armed from t = 0 (SS5.3 hysteresis:
    # ON at chunk count >= 8, OFF at <= 2, hold between).
    jon_on = False
    chunks = []
    false_ignition = False
    fi_detail = None
    for c in range(REST_CHUNKS):
        n_trans, dh = run_chunk()
        state_start = jon_on
        if not jon_on and n_trans >= JON_ON:
            jon_on = True
        elif jon_on and n_trans <= JON_OFF:
            jon_on = False
        chunks.append({"chunk": c, "transitions": n_trans,
                       "thorax_dh_mm": dh,
                       "jon_on_at_chunk_start": state_start,
                       "jon_on_at_chunk_end": jon_on})
        if (jon_on or n_trans >= JON_ON) and not false_ignition:
            false_ignition = True
            fi_detail = {"chunk": c,
                         "kind": ("channel_on" if jon_on
                                  else "chunk_threshold_exceeded"),
                         "transitions": n_trans}
    rec["chunks"] = chunks
    rec["false_ignition"] = false_ignition
    rec["false_ignition_detail"] = fi_detail
    sim.close()
    return rec


# ----------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------

def run_config(key, episode_fn):
    t0 = time.time()
    episodes = []
    valid = 0
    attempts = 0
    while valid < N_EPISODES and attempts < MAX_ATTEMPTS:
        rec = episode_fn(attempts)
        episodes.append(rec)
        attempts += 1
        if rec["status"] == "VALID":
            valid += 1
        print(f"[{key}] attempt {attempts}: status={rec['status']} "
              f"settle_chunks={rec.get('settle_chunks')} "
              f"false_ignition={rec.get('false_ignition')}", flush=True)
    n_invalid = sum(1 for e in episodes if e["status"] == "INVALID")
    valid_eps = [e for e in episodes if e["status"] == "VALID"]
    ignitions = [{"episode": e["episode"], **(e["false_ignition_detail"]
                                              or {})}
                 for e in valid_eps if e["false_ignition"]]
    verdict = ("PASS" if len(valid_eps) == N_EPISODES and not ignitions
               else "FAIL")
    return {
        "episodes_attempted": attempts,
        "episodes_valid": len(valid_eps),
        "episodes_invalid": n_invalid,
        "false_ignitions": ignitions,
        "verdict": verdict,
        "episodes": episodes,
        "wall_clock_s": time.time() - t0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", choices=("A", "B", "both"), default="both")
    args = ap.parse_args()

    out_path = RESULTS / "acceptance_test.json"
    result = {}
    if out_path.exists():
        result = json.loads(out_path.read_text())
    result.update({
        "test": "SS2.4 resting acceptance test",
        "spec": "PART4-SENSORY-SPECS.md SS2.4 (Amendment Pass 1 "
                "operational definition); SS2.3 settle; SS4.5 taste "
                "event; SS5.3 JON channel",
        "pass_rule": "zero false ignitions across N=10 resting "
                     "episodes per configuration",
        "n_episodes_per_configuration": N_EPISODES,
        "rest_chunks_per_episode": REST_CHUNKS,
    })
    wall0 = time.time()
    if args.config in ("A", "both"):
        result["config_A_feeding"] = run_config("A", feeding_episode)
    if args.config in ("B", "both"):
        result["config_B_walkhalt"] = run_config("B", walkhalt_episode)
    if "config_A_feeding" in result and "config_B_walkhalt" in result:
        result["overall_verdict"] = (
            "PASS" if result["config_A_feeding"]["verdict"] == "PASS"
            and result["config_B_walkhalt"]["verdict"] == "PASS"
            else "FAIL")
    result["wall_clock_total_s"] = time.time() - wall0
    out_path.write_text(json.dumps(result, indent=2))
    for key in ("config_A_feeding", "config_B_walkhalt"):
        if key in result:
            r = result[key]
            print(key, "->", r["verdict"],
                  f"(valid {r['episodes_valid']}, "
                  f"invalid {r['episodes_invalid']}, "
                  f"ignitions {len(r['false_ignitions'])}, "
                  f"wall {r['wall_clock_s']:.1f} s)")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
