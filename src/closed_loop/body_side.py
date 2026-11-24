"""Part 5 body side: the pinned FlyBody in the SS4.6 feeding arena.

Runs in the BODY environment (FlyGym 2.1.1 / MuJoCo 3.16.0 / numpy
2.5.5), inside the driver process -- the bridge's body half, as in
Part 2b and the SS6 slice (only the brain crosses a process boundary).
Construction and measurement reuse the qualification gate's own
machinery (repo/src/body_qualification/), so the loop's body is built exactly
as the gate qualified it:

  pilot    -- a no-arena settle reads the labrum tip's settled ground
              projection; the arena centre is placed 0.6 mm in front of
              it (SS4.6's frozen offset; gate Q5: unadjusted);
  arena    -- body_qualification.q5_rerun5.build_arena: pedestal (r 0.5 mm x
              h 0.28 mm) + food disc (r 0.5 mm x h 0.05 mm) with its
              top at ground + 0.33 mm, WITH the six proboscis contact
              pairs of the gate's Q5 defect fix -- without them the
              labrum is contact-invisible and the SS4.5 event cannot
              exist;
  settle   -- SS2.3, under zero command, food geom present; any
              labrum/tarsus food contact during warmup marks the
              episode INVALID (SS2.3 feeding addition) and the caller
              records it as such;
  chunks   -- per 100 ms chunk: the five proboscis ctrls from the
              registered chain (chain.py) are written as a zero-order
              hold (all other position actuators stay at ctrl 0, as at
              the gate), the body steps 1000 physics steps, and the
              SS4.5 taste event is tracked per physics step from the
              body's own contact reporting -- food-geom-filtered
              forces on the labrum segments and the front-leg tarsus
              segments (gate_common3.food_contact_forces), debounced
              per SS2.4 (ON after >= 10 consecutive steps with force
              > 0, OFF after >= 50 without), state sampled at the chunk
              boundary. Labrum adhesion follows SS4.3's chunk-level
              rule: engages in the first chunk after the event turns
              ON; releases after the event has been OFF for 2
              consecutive chunks.
"""

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QUALGATE = HERE.parent / "body_qualification"
sys.path.insert(0, str(QUALGATE))

import mujoco as mj  # noqa: E402
from flygym.compose import ActuatorType  # noqa: E402

from gate_common import CHUNK_STEPS, PROBOSCIS, build_sim, dof_index, settle  # noqa: E402
from gate_common3 import (FRONT_TARSUS_BODIES, NECK, compiled_params,  # noqa: E402
                          food_contact_forces, geom_ids_for_bodies,
                          labrum_tip_pos)
from q5_rerun5 import build_arena  # noqa: E402

ARENA_OFFSET_MM = 0.6         # SS4.6 final offset (gate Q5: unadjusted)
THORAX_BODY = "flybody/c_thorax"
RECORDED_JOINTS = tuple(PROBOSCIS) + tuple(NECK)


class FeedingBody:
    """One episode's body: pilot, arena, settle, then chunk stepping."""

    def __init__(self):
        # --- pilot settle: arena placement from the tip projection --
        fly, world, sim = build_sim(with_adhesion=True)
        idx0, order0 = dof_index(fly)
        st0 = settle(sim, fly, np.zeros(len(order0)))
        if not st0["settled"]:
            sim.close()
            raise RuntimeError("pilot settle failed; cannot place "
                               "the arena")
        tip = labrum_tip_pos(sim)
        head_id = mj.mj_name2id(sim.mj_model, mj.mjtObj.mjOBJ_BODY,
                                "flybody/c_head")
        head = sim.mj_data.xpos[head_id]
        forward = np.array([tip[0] - head[0], tip[1] - head[1]],
                           dtype=float)
        forward /= np.linalg.norm(forward)
        tip_proj = np.array([tip[0], tip[1]], dtype=float)
        sim.close()
        centre = tip_proj + ARENA_OFFSET_MM * forward
        self.pilot = {
            "tip_settled_xyz_mm": [float(x) for x in tip],
            "arena_centre_xy_mm": [float(x) for x in centre],
            "offset_in_front_of_tip_projection_mm": ARENA_OFFSET_MM}

        # --- episode arena + settle (SS2.3) --------------------------
        self.fly, self.world, self.sim = build_arena(centre)
        sim = self.sim
        m = sim.mj_model
        self.idx, self.order = dof_index(self.fly)
        self.params = compiled_params(sim)
        self.food_gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, "food")
        self.labrum_gids = {
            mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, n) for n in
            ("flybody/l_labrum_lower", "flybody/r_labrum_lower")}
        self.tarsus_gids = geom_ids_for_bodies(sim, FRONT_TARSUS_BODIES)
        self.adh_ids = [mj.mj_name2id(m, mj.mjtObj.mjOBJ_ACTUATOR,
                                      f"flybody/{s}_labrum-adhesion")
                        for s in ("l", "r")]
        self.thorax_id = mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY,
                                       THORAX_BODY)

        def food_check():
            lf, tf = food_contact_forces(sim, self.food_gid,
                                         self.labrum_gids,
                                         self.tarsus_gids)
            return (lf + tf) > 0

        st = settle(sim, self.fly, np.zeros(len(self.order)),
                    food_check=food_check)
        self.settle_record = {
            "settled": bool(st["settled"]),
            "n_chunks": st["n_chunks"],
            "chunks": st["chunks"],
            "food_contact_during_warmup":
                bool(st["food_contact_during_warmup"])}
        self.valid = bool(st["settled"]
                          and not st["food_contact_during_warmup"])
        self.theta_rest = {j: float(st["rest_angles"][j])
                           for j in PROBOSCIS}

        # --- SS4.5 event + SS4.3 adhesion state ----------------------
        self.event_on = False
        self._on_streak = 0
        self._off_streak = 0
        self.adhesion = False
        self._adhesion_off_chunks = 0
        self.chunk_index = 0

    def thorax_xyz(self):
        return np.asarray(self.sim.mj_data.xpos[self.thorax_id],
                          dtype=float)

    def step_chunk(self, ctrls):
        """Step one 100 ms chunk under the chain's proboscis ctrls.

        `ctrls` maps the five proboscis joint names to ctrl values;
        every other position actuator is held at ctrl 0 (the gate's
        construction). Returns the per-chunk body record; the SS4.5
        event state it reports is the state at the chunk's end -- the
        state that gates brain chunk k+1 (SS2.1 / SS4.5).
        """
        sim = self.sim
        ctrl = np.zeros(len(self.order))
        for j in PROBOSCIS:
            ctrl[self.idx[j]] = float(ctrls[j])
        sim.set_actuator_inputs(self.fly.name, ActuatorType.POSITION,
                                ctrl)
        for aid in self.adh_ids:
            sim.mj_data.ctrl[aid] = 1.0 if self.adhesion else 0.0
        adhesion_during = bool(self.adhesion)
        max_labrum_force = 0.0
        max_tarsus_force = 0.0
        forces_finite = True
        for _ in range(CHUNK_STEPS):
            sim.step()
            lf, tf = food_contact_forces(sim, self.food_gid,
                                         self.labrum_gids,
                                         self.tarsus_gids)
            forces_finite = (forces_finite and math.isfinite(lf)
                             and math.isfinite(tf))
            max_labrum_force = max(max_labrum_force, lf)
            max_tarsus_force = max(max_tarsus_force, tf)
            if (lf + tf) > 0:
                self._on_streak += 1
                self._off_streak = 0
                if self._on_streak >= 10 and not self.event_on:
                    self.event_on = True
            else:
                self._off_streak += 1
                self._on_streak = 0
                if self._off_streak >= 50 and self.event_on:
                    self.event_on = False
        angles_all = sim.get_joint_angles(self.fly.name)
        angles = {j: float(angles_all[self.idx[j]])
                  for j in RECORDED_JOINTS}
        thorax = self.thorax_xyz()
        record = {
            "chunk": self.chunk_index,
            "angles_rad": angles,
            "max_labrum_food_force_N": max_labrum_force,
            "max_front_tarsus_food_force_N": max_tarsus_force,
            "taste_event_at_chunk_end": bool(self.event_on),
            "adhesion_during_chunk": adhesion_during,
            "thorax_xyz_mm": [float(x) for x in thorax],
            "finite": bool(forces_finite
                           and np.all(np.isfinite(sim.mj_data.qpos))
                           and np.all(np.isfinite(sim.mj_data.qvel))
                           and all(math.isfinite(v)
                                   for v in angles.values())),
        }
        # SS4.3 adhesion rule, decided at the chunk boundary: engages
        # in the first chunk after the event turns ON; releases after
        # the event has been OFF for 2 consecutive chunks.
        if self.event_on:
            self._adhesion_off_chunks = 0
            self.adhesion = True
        else:
            self._adhesion_off_chunks += 1
            if self.adhesion and self._adhesion_off_chunks >= 2:
                self.adhesion = False
        self.chunk_index += 1
        return record

    def close(self):
        self.sim.close()
