"""Reach-curve calibration (pre-gate calibration, NOT a gate step),
24 Nov 2026 -- Reviewer 1's Pass 6 condition 1.

Kinematics only, no food geom, no verdicts. The body (Demo C FlyBody
construction, as in Q3) is settled per SS2.3, then the extension command
e is swept 0 -> 1 in 41 equal steps through the SS4.3 chain exactly as
registered (feedforward inverse from the compiled artefact's parameters,
Amendment Pass 5; yaw and neck held at rest; at e = 0 the chain writes
ctrl = 0 to the five proboscis DoFs). Each e is held 0.4 s and the final
state recorded: the five achieved joint angles, E (SS4.4 two-segment
pitch sum), and the labrum lowest surface height.

Two surface-height series are recorded per point, because they differ
materially for these geoms and the difference matters:

- z_surf (centre-minus-rbound, as prescribed for this calibration):
  per labrum geom, geom_xpos[gid].z - geom_rbound[gid]; z_surf is the
  smaller of the two. NOTE: geom_rbound is the bounding-SPHERE radius
  (0.1822 mm); the labrum geoms are elongated, extending only ~0.097 mm
  below their centres in this pose, so this series is a conservative
  LOWER BOUND on the surface height, ~0.086 mm below the true surface.
  It is not the lowest surface point.
- z_true (the method execution #3's q5_diagnostic.py used):
  mj_geomDistance from each labrum geom to the ground plane geom --
  the true lowest-surface height above the ground; z_true is the
  smaller of the two. This is the physically meaningful reach.

f_c and the sensitivity tables are computed for BOTH series.
"""

import csv
import json
import time
from pathlib import Path

import mujoco as mj
import numpy as np

from flygym.compose import ActuatorType

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import (PITCH_JOINTS, PROBOSCIS, build_sim, dof_index,  # noqa: E402
                         settle)
from gate_common3 import (LABRUM_GEOM_NAMES, RESULTS, chain_ctrl,  # noqa: E402
                          compiled_params, extension_E)

HOLD_STEPS = 4000          # 0.4 s at dt = 1e-4 s
N_POINTS = 41              # e = 0, 0.025, ..., 1.0
SAT_TOL = 1e-4             # rad; "angle stops changing" band


def labrum_surface(sim):
    """Lowest labrum surface height: geom centre z minus bounding radius."""
    m, d = sim.mj_model, sim.mj_data
    per_geom = {}
    for name in LABRUM_GEOM_NAMES:
        gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, name)
        per_geom[name] = {
            "centre_z_mm": float(d.geom_xpos[gid][2]),
            "rbound_mm": float(m.geom_rbound[gid]),
            "surface_z_mm": float(d.geom_xpos[gid][2] - m.geom_rbound[gid]),
        }
    z = min(v["surface_z_mm"] for v in per_geom.values())
    return z, per_geom


def ground_distance_check(sim):
    """Cross-check: mj_geomDistance from each labrum geom to the ground
    plane geom = true lowest-surface height above the ground plane."""
    m, d = sim.mj_model, sim.mj_data
    planes = [g for g in range(m.ngeom)
              if m.geom_type[g] == mj.mjtGeom.mjGEOM_PLANE]
    if not planes:
        return None
    out = {}
    for name in LABRUM_GEOM_NAMES:
        gid = mj.mj_name2id(m, mj.mjtObj.mjOBJ_GEOM, name)
        out[name] = float(mj.mj_geomDistance(m, d, gid, planes[0], 10.0, None))
    return out


def interp_crossing(xs, ys, level):
    """Smallest x where y (sampled at xs) falls to <= level, linear in x.
    Returns None if y never reaches level."""
    if ys[0] <= level:
        return float(xs[0])
    for i in range(1, len(xs)):
        if ys[i] <= level:
            x0, x1, y0, y1 = xs[i - 1], xs[i], ys[i - 1], ys[i]
            if y1 == y0:
                return float(x1)
            return float(x0 + (level - y0) * (x1 - x0) / (y1 - y0))
    return None


def interp_value(xs, ys, x):
    """Linear interpolation of y at x (xs increasing)."""
    return float(np.interp(x, xs, ys))


def main():
    t0 = time.time()
    q2 = json.loads((RESULTS / "q2_rerun3.json").read_text())
    signs = {j: q2["joints"][j]["extension_sign_s"] for j in PITCH_JOINTS}
    theta_ext = {j: q2["joints"][j]["theta_ext_rad"] for j in PITCH_JOINTS}
    assert signs == {"c_head-c_rostrum-pitch": -1,
                     "c_rostrum-c_haustellum-pitch": -1}, signs
    assert theta_ext == {"c_head-c_rostrum-pitch": -1.19,
                         "c_rostrum-c_haustellum-pitch": -1.54}, theta_ext

    fly, world, sim = build_sim(with_adhesion=True)
    idx, order = dof_index(fly)
    params = compiled_params(sim)
    st = settle(sim, fly, np.zeros(len(order)))
    assert st["settled"], "settle did not complete within the SS2.3 cap"
    rest = {j: st["rest_angles"][j] for j in PROBOSCIS}
    z_rest, _ = labrum_surface(sim)

    base_ctrl = np.zeros(len(order))
    curve = []
    for k in range(N_POINTS):
        e = k / (N_POINTS - 1)
        ctrl = chain_ctrl(base_ctrl, idx, params, e, rest, signs, theta_ext)
        sim.set_actuator_inputs(fly.name, ActuatorType.POSITION, ctrl)
        for _ in range(HOLD_STEPS):
            sim.step()
        angles_all = sim.get_joint_angles(fly.name)
        by_joint = {j: float(angles_all[idx[j]]) for j in PROBOSCIS}
        z_surf, per_geom = labrum_surface(sim)
        gd = ground_distance_check(sim)
        curve.append({
            "e": float(e),
            "angles_rad": by_joint,
            "E_rad": extension_E(by_joint, rest, signs),
            "z_surf_mm": z_surf,
            "z_surf_per_geom": per_geom,
            "ground_distance_check_mm": gd,
            "z_true_mm": float(min(gd.values())) if gd else None,
        })
    sim.close()

    e_max = curve[-1]["E_rad"]
    for pt in curve:
        pt["E_fraction"] = float(pt["E_rad"] / e_max)
    R = curve[-1]["z_surf_mm"]
    fracs = [pt["E_fraction"] for pt in curve]
    zs = [pt["z_surf_mm"] for pt in curve]
    zt = [pt["z_true_mm"] for pt in curve]

    # Saturation: smallest sweep e from which the achieved angle stays
    # within SAT_TOL of its e = 1 value for all larger e.
    saturation = {}
    for j in PITCH_JOINTS:
        a_end = curve[-1]["angles_rad"][j]
        sat_e = None
        for k, pt in enumerate(curve):
            if all(abs(q["angles_rad"][j] - a_end) <= SAT_TOL
                   for q in curve[k:]):
                sat_e = pt["e"]
                break
        saturation[j] = {"saturation_e": sat_e,
                         "achieved_angle_at_e1_rad": a_end}

    fc = {f"{T:.3f}": interp_crossing(fracs, zs, T)
          for T in (0.296, 0.306, 0.316, 0.326, 0.336, 0.346)}
    inv = {f"{f:.2f}": interp_value(fracs, zs, f) for f in (0.60, 0.80, 0.95)}
    fc_true = {f"{T:.3f}": interp_crossing(fracs, zt, T)
               for T in (0.296, 0.306, 0.316, 0.326, 0.336, 0.346)}
    inv_true = {f"{f:.2f}": interp_value(fracs, zt, f)
                for f in (0.60, 0.80, 0.95)}

    def analysis(series, label):
        return {
            "series": label,
            "reach_at_e1_mm": float(series[-1]),
            "surface_at_rest_mm": float(series[0]),
            "f_c_of_T": {f"{T:.3f}": interp_crossing(fracs, series, T)
                         for T in (0.296, 0.306, 0.316, 0.326, 0.336, 0.346)},
            "f_c_at_0.330": interp_crossing(fracs, series, 0.330),
            "f_c_at_0.346": interp_crossing(fracs, series, 0.346),
            "T_at_onset_fraction": {
                f"{f:.2f}": interp_value(fracs, series, f)
                for f in (0.60, 0.80, 0.95)},
        }

    result = {
        "artefact": "reach_curve calibration (pre-gate, NOT a gate step)",
        "date": "24 Nov 2026",
        "spec": "PART4-SENSORY-SPECS.md SS4.3-SS4.4; Reviewer 1 Pass 6 cond. 1",
        "construction": "Demo C FlyBody via gate_common.build_sim "
                        "(with_adhesion=True, adhesion never commanded)",
        "settle": {"n_chunks": st["n_chunks"], "theta_rest_rad": rest},
        "signs": signs, "theta_ext_rad": theta_ext,
        "hold_per_point_s": HOLD_STEPS * 1e-4,
        "n_points": N_POINTS,
        "z_surf_method": ("per labrum geom (l_labrum_lower, r_labrum_lower): "
                          "geom_xpos.z - geom_rbound (centre height minus "
                          "bounding-sphere radius); z_surf = min over the "
                          "two geoms."),
        "method_warning": ("geom_rbound (0.1822 mm) is the bounding-SPHERE "
                           "radius of an elongated geom; the labrum geoms "
                           "extend only ~0.097 mm below their centres here, "
                           "so the centre-minus-rbound series UNDERSTATES "
                           "the true surface height by ~0.086 mm. The "
                           "z_true series (mj_geomDistance to the ground "
                           "plane, execution #3's diagnostic method) is "
                           "the physical surface height. Both analyses "
                           "are recorded; they give different f_c values "
                           "and must not be mixed."),
        "z_surf_at_rest_mm": float(z_rest),
        "E_max_rad": float(e_max),
        "R_labrum_surface_reach_at_e1_mm": float(R),
        "analysis_centre_minus_rbound": analysis(zs, "z_surf (centre - rbound)"),
        "analysis_true_surface": analysis(zt, "z_true (geomDistance to ground)"),
        "achieved_angles_at_e1_rad": curve[-1]["angles_rad"],
        "saturation": saturation,
        "f_c_of_T": fc,
        "f_c_at_0.330": interp_crossing(fracs, zs, 0.330),
        "f_c_at_0.346": interp_crossing(fracs, zs, 0.346),
        "T_at_onset_fraction": inv,
        "curve": curve,
        "wall_clock_s": time.time() - t0,
    }
    out_json = RESULTS / "reach_curve.json"
    out_json.write_text(json.dumps(result, indent=2))
    out_csv = RESULTS / "reach_curve.csv"
    with out_csv.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["e", "E_rad", "E_fraction", "z_surf_mm", "z_true_mm"] +
                   [f"angle_{j}_rad" for j in PROBOSCIS])
        for pt in curve:
            w.writerow([pt["e"], pt["E_rad"], pt["E_fraction"],
                        pt["z_surf_mm"], pt["z_true_mm"]] +
                       [pt["angles_rad"][j] for j in PROBOSCIS])

    print("theta_rest:", {j: round(rest[j], 5) for j in PROBOSCIS})
    print("z_surf at rest (e=0):", round(curve[0]["z_surf_mm"], 4), "mm",
          "| z_true at rest:", round(zt[0], 4), "mm")
    print("E_max:", round(e_max, 4), "rad | R (z_surf at e=1):", round(R, 4),
          "mm | R_true:", round(zt[-1], 4), "mm")
    print("achieved at e=1:", {j: round(curve[-1]["angles_rad"][j], 4)
                               for j in PROBOSCIS})
    for j, s in saturation.items():
        print("saturation", j, "e =", s["saturation_e"])
    print("[centre-rbound] f_c(0.330) =", result["f_c_at_0.330"],
          "| f_c(0.346) =", result["f_c_at_0.346"])
    print("[centre-rbound] f_c table:", {k: (None if v is None else round(v, 4))
                                        for k, v in fc.items()})
    print("[centre-rbound] T at onset fractions:",
          {k: round(v, 4) for k, v in inv.items()})
    print("[true surface] f_c(0.330) =", result["analysis_true_surface"]["f_c_at_0.330"],
          "| f_c(0.346) =", result["analysis_true_surface"]["f_c_at_0.346"])
    print("[true surface] f_c table:",
          {k: (None if v is None else round(v, 4))
           for k, v in fc_true.items()})
    print("[true surface] T at onset fractions:",
          {k: round(v, 4) for k, v in inv_true.items()})
    print("wrote", out_json, "and", out_csv,
          "| wall", round(result["wall_clock_s"], 1), "s")


if __name__ == "__main__":
    main()
