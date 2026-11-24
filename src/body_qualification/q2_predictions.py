"""Pre-registered Q2 prediction table (SS7.3, Amendment Pass 5).

Computed AFTER Q0 and BEFORE the Q2 sweep runs: the predicted steady
state for all nine targets on all five proboscis joints under the frozen
SS4.3 clamped map, using the compiled values recorded at Q0 (kp from
gainprm, ks from jnt_stiffness, ref from qpos_spring). The sweep tests
this recorded prediction; the 0.05 rad tolerance is unchanged.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent))
from gate_common import PROBOSCIS  # noqa: E402
from gate_common3 import RESULTS  # noqa: E402


def main():
    t0 = time.time()
    q0 = json.loads((RESULTS / "q0_rerun3.json").read_text())
    assert q0["verdict"] == "PASS", "Q0 did not pass; no prediction table"
    premise = q0["premise_checks"]

    table = {}
    for joint in PROBOSCIS:
        p = premise[joint]
        kp, ks, ref = p["kp_gainprm0"], p["jnt_stiffness"], p["qpos_spring"]
        lo, hi = p["yaml_range"]
        points = []
        for k in range(9):
            target = lo + k * (hi - lo) / 8
            q = (kp * target + ks * ref) / (kp + ks)
            q_eff = min(max(q, lo), hi)
            points.append({
                "k": k, "target_ctrl_rad": float(target),
                "qhat_unclamped_rad": float(q),
                "predicted_steady_state_rad": float(q_eff),
                "clamp_bound": bool(q < lo or q > hi),
            })
        table[joint] = {"kp": kp, "ks": ks, "ref_qpos_spring": ref,
                        "range": [lo, hi], "points": points}

    now = datetime.now(timezone.utc)
    result = {
        "artefact": "q2_predictions_prereg",
        "spec": "PART4-SENSORY-SPECS SS7.3 (Amendment Pass 5)",
        "computed_at_utc": now.isoformat(),
        "computed_at_wat": now.astimezone().isoformat(),
        "source": "compiled values recorded in results/q0_rerun3.json "
                  "(premise_checks); map qhat_eff(ctrl) = clamp((kp*ctrl + "
                  "ks*ref)/(kp + ks), range) with ref = qpos_spring",
        "tolerance_rad": 0.05,
        "table": table,
        "wall_clock_s": time.time() - t0,
    }
    out = RESULTS / "q2_predictions_prereg.json"
    out.write_text(json.dumps(result, indent=2))
    print("wrote", out, "at", result["computed_at_utc"])
    for j, t in table.items():
        print(j, "kp", t["kp"], "ks", t["ks"], "ref", t["ref_qpos_spring"],
              "pred range", round(t["points"][0]["predicted_steady_state_rad"], 4),
              "->", round(t["points"][-1]["predicted_steady_state_rad"], 4),
              "clamp_bound points:", [p["k"] for p in t["points"] if p["clamp_bound"]])


if __name__ == "__main__":
    main()
