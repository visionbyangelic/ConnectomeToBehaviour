"""Gate summary, fifth execution: assembles Q0-Q6 (rerun5), computes
epsilon_res and theta_off, applies the SS4.4 band guard, compares the
mesh cache against Q0's before-listing (SS7.1: no download during the
gate), and records the Part 5 freeze outputs on a full pass.
"""

import json
import time
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common3 import RESULTS  # noqa: E402
from q0_rerun5 import cache_listing  # noqa: E402

STEPS = ["q0", "q1", "q2", "q3", "q4", "q5", "q6"]


def load(name):
    p = RESULTS / f"{name}_rerun5.json"
    return json.loads(p.read_text()) if p.exists() else None


def main():
    t0 = time.time()
    res = {s: load(s) for s in STEPS}
    verdicts = {s: (None if res[s] is None else res[s]["verdict"])
                for s in STEPS}

    eps_res = None
    theta_off = None
    band_guard = None
    if res["q2"] and res["q3"]:
        q2_err = max(j["max_steady_state_error_rad"]
                     for j in res["q2"]["joints"].values())
        q3_res = max(res["q3"]["post_retraction_residuals_rad"])
        eps_res = max(q2_err, q3_res)
        theta_off = 3 * eps_res
        band_guard = {"eps_res_rad": eps_res,
                      "q2_term_rad": q2_err, "q3_term_rad": q3_res,
                      "theta_off_rad": theta_off,
                      "guard": "theta_off < 0.10 rad",
                      "passes": bool(theta_off < 0.10)}

    cache_after = cache_listing()
    cache_before = (res["q0"] or {}).get("mesh_cache_before")
    no_download = (cache_before is not None
                   and cache_before["files"] == cache_after["files"])

    all_pass = all(v == "PASS" for v in verdicts.values())
    gate_pass = bool(all_pass and band_guard and band_guard["passes"])
    summary = {
        "gate": "feeding-body qualification gate, fifth execution",
        "spec": ("PART4-SENSORY-SPECS.md SS7 as amended by Passes 1-3, "
                 "5 and 6 (revised)"),
        "step_verdicts": verdicts,
        "band_guard": band_guard,
        "mesh_cache_no_download_during_gate": no_download,
        "gate_verdict": "PASS" if gate_pass else "FAIL",
        "wall_clock_s": time.time() - t0,
    }
    if gate_pass:
        q2, q3, q5, q6 = res["q2"], res["q3"], res["q5"], res["q6"]
        summary["freeze_outputs"] = {
            "pinned_hashes": {n: h["sha256"] for n, h in
                              res["q0"]["hashes"].items()},
            "compiled_premise_values": res["q0"]["premise_checks"],
            "construction": res["q0"]["construction"],
            "prediction_table_artefact": "results/q2_predictions_prereg5.json",
            "prediction_table_computed_at_utc":
                q2["predictions_computed_at_utc"],
            "extension_signs": {j: q2["joints"][j]["extension_sign_s"]
                                for j in
                                ("c_head-c_rostrum-pitch",
                                 "c_rostrum-c_haustellum-pitch")},
            "theta_ext_rad": q3["theta_ext_rad"],
            "empirical_map": {j: [{"target_ctrl": p["target_ctrl"],
                                   "steady_state_rad":
                                       p["steady_state_rad"]}
                                  for p in q2["joints"][j]["points"]]
                              for j in q2["joints"]},
            "eps_res_rad": eps_res,
            "theta_off_rad": theta_off,
            "band_guard_passes": band_guard["passes"],
            "E_max_rad": q3["E_max_measured_hold_mean_rad"],
            "E_raw_extremes_rad": q3["E_raw_extremes_rad"],
            "E_max_fraction_of_raw_extremes":
                q3["E_max_fraction_of_raw_extremes"],
            "final_arena_offset_mm":
                q5["final_offset_in_front_of_tip_projection_mm"],
            "arena_offset_adjusted_once": q5["offset_adjusted_once"],
            "q5_measured_onset_fraction":
                q5["attempts"][-1].get("onset_fraction_measured"),
            "q6_calibration_curve":
                "results/q6_rerun5.json + "
                "results/q6_calibration_curve_rerun5.csv",
            "q6_r_hi_status": "155 Hz PROVISIONAL (SS7.6)",
        }
    out = RESULTS / "gate_summary_rerun5.json"
    out.write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: summary[k] for k in
                      ("step_verdicts", "band_guard",
                       "mesh_cache_no_download_during_gate",
                       "gate_verdict")}, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
