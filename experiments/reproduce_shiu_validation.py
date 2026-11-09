"""
Phase 1 Validation: Reproduce Shiu et al. (Nature 2024) Baseline Experiments.

Tests:
1. Sugar GRN excitation (150 Hz) -> Proboscis extension motor neuron (MN9) activation.
2. Bitter GRN excitation (150 Hz) -> No MN9 activation (aversive).
3. Sugar + Bitter co-activation -> Bitter-mediated circuit suppression of MN9.
4. Water GRN excitation (150 Hz) -> Distinct SEZ / MN9 response.
5. Ground-truth benchmark against published Shiu et al. sugar simulation.
"""

import sys
import json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# Add repo root to sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.brain import (
    FlyBrain,
    SUGAR_GRNS_RIGHT,
    BITTER_GRNS,
    WATER_GRNS,
    MN9_LEFT,
    MN9_RIGHT,
    compare_to_ground_truth,
)


def run_validation():
    results_dir = ROOT / "results" / "validation"
    results_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print(" ConnectomeToBehavior — Phase 1: Shiu et al. (2024) Validation")
    print("=" * 65)

    brain = FlyBrain()
    print(f"[Init] Connectome loaded: {brain.total_neurons} neurons ready.\n")

    sim_duration_ms = 100.0  # 100 ms biological time per condition
    results = {}

    # --------------------------------------------------------------------------
    # 1. Sugar GRN Activation
    # --------------------------------------------------------------------------
    print("--- Condition 1: Sugar GRNs Alone (150 Hz) ---")
    brain.reset_stimuli().activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)
    df_sugar = brain.simulate(duration_ms=sim_duration_ms, n_trials=1, exp_name="sugar_150hz")
    sugar_rates = brain.get_motor_neuron_rates()
    sugar_active = brain.get_active_neurons()

    results["sugar"] = {
        "stimulus": "Sugar GRNs (21 neurons, 150 Hz)",
        "duration_ms": sim_duration_ms,
        "total_spikes": len(df_sugar),
        "active_neurons": len(sugar_active),
        "mn9_left_hz": sugar_rates["MN9_left"],
        "mn9_right_hz": sugar_rates["MN9_right"],
    }
    print(f"-> MN9 Left: {sugar_rates['MN9_left']:.1f} Hz | MN9 Right: {sugar_rates['MN9_right']:.1f} Hz")
    print(f"-> Total Active Neurons: {len(sugar_active)}\n")

    # --------------------------------------------------------------------------
    # 2. Bitter GRN Activation
    # --------------------------------------------------------------------------
    print("--- Condition 2: Bitter GRNs Alone (150 Hz) ---")
    brain.reset_stimuli().activate(BITTER_GRNS, freq_hz=150.0)
    df_bitter = brain.simulate(duration_ms=sim_duration_ms, n_trials=1, exp_name="bitter_150hz")
    bitter_rates = brain.get_motor_neuron_rates()
    bitter_active = brain.get_active_neurons()

    results["bitter"] = {
        "stimulus": "Bitter GRNs (21 neurons, 150 Hz)",
        "duration_ms": sim_duration_ms,
        "total_spikes": len(df_bitter),
        "active_neurons": len(bitter_active),
        "mn9_left_hz": bitter_rates["MN9_left"],
        "mn9_right_hz": bitter_rates["MN9_right"],
    }
    print(f"-> MN9 Left: {bitter_rates['MN9_left']:.1f} Hz | MN9 Right: {bitter_rates['MN9_right']:.1f} Hz")
    print(f"-> Total Active Neurons: {len(bitter_active)}\n")

    # --------------------------------------------------------------------------
    # 3. Sugar + Bitter Co-activation (Inhibition Test)
    # --------------------------------------------------------------------------
    print("--- Condition 3: Sugar (150 Hz) + Bitter (150 Hz) Co-activation ---")
    brain.reset_stimuli()
    brain.activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)
    brain.activate_secondary(BITTER_GRNS, freq_hz=150.0)
    df_dual = brain.simulate(duration_ms=sim_duration_ms, n_trials=1, exp_name="sugar_plus_bitter")
    dual_rates = brain.get_motor_neuron_rates()
    dual_active = brain.get_active_neurons()

    results["sugar_plus_bitter"] = {
        "stimulus": "Sugar (150 Hz) + Bitter (150 Hz)",
        "duration_ms": sim_duration_ms,
        "total_spikes": len(df_dual),
        "active_neurons": len(dual_active),
        "mn9_left_hz": dual_rates["MN9_left"],
        "mn9_right_hz": dual_rates["MN9_right"],
    }
    print(f"-> MN9 Left: {dual_rates['MN9_left']:.1f} Hz | MN9 Right: {dual_rates['MN9_right']:.1f} Hz")
    print(f"-> Total Active Neurons: {len(dual_active)}\n")

    # --------------------------------------------------------------------------
    # 4. Water GRN Activation
    # --------------------------------------------------------------------------
    print("--- Condition 4: Water GRNs Alone (150 Hz) ---")
    brain.reset_stimuli().activate(WATER_GRNS, freq_hz=150.0)
    df_water = brain.simulate(duration_ms=sim_duration_ms, n_trials=1, exp_name="water_150hz")
    water_rates = brain.get_motor_neuron_rates()
    water_active = brain.get_active_neurons()

    results["water"] = {
        "stimulus": "Water GRNs (18 neurons, 150 Hz)",
        "duration_ms": sim_duration_ms,
        "total_spikes": len(df_water),
        "active_neurons": len(water_active),
        "mn9_left_hz": water_rates["MN9_left"],
        "mn9_right_hz": water_rates["MN9_right"],
    }
    print(f"-> MN9 Left: {water_rates['MN9_left']:.1f} Hz | MN9 Right: {water_rates['MN9_right']:.1f} Hz")
    print(f"-> Total Active Neurons: {len(water_active)}\n")

    # --------------------------------------------------------------------------
    # 5. Benchmark Against Published Ground Truth
    # --------------------------------------------------------------------------
    gt_file = ROOT / "Drosophila_brain_model-main" / "results" / "example" / "sugarR.parquet"
    if gt_file.exists():
        print("--- Ground Truth Comparison (vs. Shiu et al. published sugar run) ---")
        comparison = compare_to_ground_truth(df_sugar, gt_file, duration_s=1.0, n_trials=30)
        results["ground_truth_comparison"] = comparison
        print(f"-> Jaccard Overlap: {comparison['jaccard_overlap']:.3f}")
        print(f"-> Precision: {comparison['precision']:.3f} | Recall: {comparison['recall']:.3f}")
        print(f"-> Firing Rate Pearson Correlation: {comparison['firing_rate_correlation']:.3f}")
        print(f"-> Shared Active Neurons: {comparison['shared_active_neurons']}\n")

    # Save summary JSON
    json_path = results_dir / "validation_summary.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[Saved] Validation summary saved to: {json_path}")

    # --------------------------------------------------------------------------
    # Plot Comparative Bar Chart
    # --------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=150)
    fig.patch.set_facecolor("#0f172a")

    for ax in (ax1, ax2):
        ax.set_facecolor("#1e293b")
        ax.tick_params(colors="#94a3b8", labelsize=9)
        ax.spines["bottom"].set_color("#334155")
        ax.spines["top"].set_color("#334155")
        ax.spines["left"].set_color("#334155")
        ax.spines["right"].set_color("#334155")
        ax.grid(True, linestyle="--", alpha=0.15, color="#f8fafc")

    conditions = ["Sugar", "Bitter", "Sugar+Bitter", "Water"]
    colors = ["#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

    mn9_left_vals = [
        results["sugar"]["mn9_left_hz"],
        results["bitter"]["mn9_left_hz"],
        results["sugar_plus_bitter"]["mn9_left_hz"],
        results["water"]["mn9_left_hz"],
    ]

    active_counts = [
        results["sugar"]["active_neurons"],
        results["bitter"]["active_neurons"],
        results["sugar_plus_bitter"]["active_neurons"],
        results["water"]["active_neurons"],
    ]

    # Panel 1: Motor Neuron 9 (MN9) Output
    bars1 = ax1.bar(conditions, mn9_left_vals, color=colors, width=0.55, edgecolor="#ffffff", linewidth=0.5)
    ax1.set_title("Proboscis Extension Motor Neuron (MN9 Left)", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax1.set_ylabel("Firing Rate (Hz)", color="#94a3b8", fontsize=10)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.0, h + 1.5, f"{h:.0f} Hz", ha="center", va="bottom", color="#f8fafc", fontsize=9, fontweight="bold")

    # Panel 2: Whole-Brain Active Neuron Population
    bars2 = ax2.bar(conditions, active_counts, color=colors, width=0.55, edgecolor="#ffffff", linewidth=0.5)
    ax2.set_title("Whole-Brain Active Neuron Cascade", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax2.set_ylabel("Unique Active Neurons", color="#94a3b8", fontsize=10)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2.0, h + 4.0, f"{h}", ha="center", va="bottom", color="#f8fafc", fontsize=9, fontweight="bold")

    fig.suptitle("ConnectomeToBehavior: Phase 1 Validation (Shiu et al., Nature 2024)", color="#38bdf8", fontsize=12, fontweight="bold", y=1.02)
    plt.tight_layout()

    plot_path = results_dir / "mn9_response_comparison.png"
    plt.savefig(plot_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[Saved] Comparative graph saved to: {plot_path}")
    print("=" * 65)


if __name__ == "__main__":
    run_validation()
