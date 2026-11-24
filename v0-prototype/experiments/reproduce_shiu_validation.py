"""
Phase 1 Validation: Reproduce Shiu et al. (Nature 2024) Baseline Experiments.

Rigorous Multi-Trial Validation Suite:
1. Sugar GRN excitation (150 Hz) -> Proboscis extension motor neuron (MN9) activation.
2. Bitter GRN excitation (150 Hz) -> No MN9 activation (aversive circuit).
3. Sugar + Bitter co-activation -> Lateral circuit inhibition of MN9 firing.
4. Water GRN excitation (150 Hz) -> Distinct SEZ / MN9 response.
5. Dual Ground-Truth Benchmark against published Shiu et al. sugar simulation:
   - Time-matched slice: First 100 ms of simulation vs first 100 ms of reference.
   - Cumulative slice: First 100 ms of simulation vs full 1.0 s reference (with explicit documentation of trial/duration differences).
"""

import sys
import json
import argparse
from pathlib import Path
import numpy as np
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


def run_condition_multi_trial(brain: FlyBrain, duration_ms: float, n_trials: int, exp_name: str):
    """Run simulation over multiple trials and return DataFrame plus per-trial statistics."""
    df_spikes = brain.simulate(duration_ms=duration_ms, n_trials=n_trials, exp_name=exp_name, verbose=True)

    trial_s = duration_ms / 1000.0
    mn_stats = brain.get_motor_neuron_stats(duration_ms=duration_ms, n_trials=n_trials)

    # Per-trial spike counts and active neuron counts
    trial_spike_counts = []
    trial_active_counts = []
    for tr in range(n_trials):
        tr_df = df_spikes[df_spikes['trial'] == tr]
        trial_spike_counts.append(len(tr_df))
        trial_active_counts.append(len(tr_df['flywire_id'].unique()) if len(tr_df) > 0 else 0)

    summary = {
        "duration_ms": duration_ms,
        "n_trials": n_trials,
        "mn9_left_mean_hz": float(mn_stats["MN9_left"]["mean_hz"]),
        "mn9_left_std_hz": float(mn_stats["MN9_left"]["std_hz"]),
        "mn9_left_trials_hz": mn_stats["MN9_left"]["trials_hz"],
        "mn9_right_mean_hz": float(mn_stats["MN9_right"]["mean_hz"]),
        "mn9_right_std_hz": float(mn_stats["MN9_right"]["std_hz"]),
        "mn9_right_trials_hz": mn_stats["MN9_right"]["trials_hz"],
        "total_spikes_mean": float(np.mean(trial_spike_counts)),
        "total_spikes_std": float(np.std(trial_spike_counts, ddof=1)) if n_trials > 1 else 0.0,
        "active_neurons_mean": float(np.mean(trial_active_counts)),
        "active_neurons_std": float(np.std(trial_active_counts, ddof=1)) if n_trials > 1 else 0.0,
        "cumulative_active_neurons": len(df_spikes['flywire_id'].unique()) if len(df_spikes) > 0 else 0,
    }

    return df_spikes, summary


def run_validation(n_trials: int = 3, sim_duration_ms: float = 100.0):
    results_dir = ROOT / "results" / "validation"
    results_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 68)
    print(" ConnectomeToBehaviour — Phase 1: Shiu et al. (2024) Multi-Trial Validation")
    print(f" (Trials per condition: N={n_trials}, Duration per trial: {sim_duration_ms} ms)")
    print("=" * 68)

    brain = FlyBrain()
    print(f"[Init] Connectome loaded: {brain.total_neurons} neurons ready.\n")

    results = {
        "metadata": {
            "n_trials": n_trials,
            "duration_ms": sim_duration_ms,
            "units": "Hz for rates, count for spikes/neurons",
        }
    }

    # --------------------------------------------------------------------------
    # 1. Sugar GRN Activation
    # --------------------------------------------------------------------------
    print("--- Condition 1: Sugar GRNs Alone (150 Hz) ---")
    brain.reset_stimuli().activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)
    df_sugar, sugar_summary = run_condition_multi_trial(brain, sim_duration_ms, n_trials, "sugar_150hz")
    sugar_summary["stimulus"] = "Sugar GRNs (21 Right SEZ neurons, 150 Hz)"
    results["sugar"] = sugar_summary
    print(f"-> MN9 Left: {sugar_summary['mn9_left_mean_hz']:.1f} ± {sugar_summary['mn9_left_std_hz']:.1f} Hz (trials: {sugar_summary['mn9_left_trials_hz']})")
    print(f"-> MN9 Right: {sugar_summary['mn9_right_mean_hz']:.1f} ± {sugar_summary['mn9_right_std_hz']:.1f} Hz (trials: {sugar_summary['mn9_right_trials_hz']})")
    print(f"-> Active Neurons (mean per trial): {sugar_summary['active_neurons_mean']:.1f} ± {sugar_summary['active_neurons_std']:.1f} (cumulative: {sugar_summary['cumulative_active_neurons']})\n")

    # --------------------------------------------------------------------------
    # 2. Bitter GRN Activation
    # --------------------------------------------------------------------------
    print("--- Condition 2: Bitter GRNs Alone (150 Hz) ---")
    brain.reset_stimuli().activate(BITTER_GRNS, freq_hz=150.0)
    df_bitter, bitter_summary = run_condition_multi_trial(brain, sim_duration_ms, n_trials, "bitter_150hz")
    bitter_summary["stimulus"] = "Bitter GRNs (21 SEZ neurons, 150 Hz)"
    results["bitter"] = bitter_summary
    print(f"-> MN9 Left: {bitter_summary['mn9_left_mean_hz']:.1f} ± {bitter_summary['mn9_left_std_hz']:.1f} Hz")
    print(f"-> MN9 Right: {bitter_summary['mn9_right_mean_hz']:.1f} ± {bitter_summary['mn9_right_std_hz']:.1f} Hz")
    print(f"-> Active Neurons (mean per trial): {bitter_summary['active_neurons_mean']:.1f} ± {bitter_summary['active_neurons_std']:.1f}\n")

    # --------------------------------------------------------------------------
    # 3. Sugar + Bitter Co-activation (Inhibition Test)
    # --------------------------------------------------------------------------
    print("--- Condition 3: Sugar (150 Hz) + Bitter (150 Hz) Co-activation ---")
    brain.reset_stimuli()
    brain.activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)
    brain.activate_secondary(BITTER_GRNS, freq_hz=150.0)
    df_dual, dual_summary = run_condition_multi_trial(brain, sim_duration_ms, n_trials, "sugar_plus_bitter")
    dual_summary["stimulus"] = "Sugar (150 Hz) + Bitter (150 Hz)"
    results["sugar_plus_bitter"] = dual_summary
    print(f"-> MN9 Left: {dual_summary['mn9_left_mean_hz']:.1f} ± {dual_summary['mn9_left_std_hz']:.1f} Hz (trials: {dual_summary['mn9_left_trials_hz']})")
    print(f"-> MN9 Right: {dual_summary['mn9_right_mean_hz']:.1f} ± {dual_summary['mn9_right_std_hz']:.1f} Hz (trials: {dual_summary['mn9_right_trials_hz']})")
    print(f"-> Active Neurons (mean per trial): {dual_summary['active_neurons_mean']:.1f} ± {dual_summary['active_neurons_std']:.1f}\n")

    # --------------------------------------------------------------------------
    # 4. Water GRN Activation
    # --------------------------------------------------------------------------
    print("--- Condition 4: Water GRNs Alone (150 Hz) ---")
    brain.reset_stimuli().activate(WATER_GRNS, freq_hz=150.0)
    df_water, water_summary = run_condition_multi_trial(brain, sim_duration_ms, n_trials, "water_150hz")
    water_summary["stimulus"] = "Water GRNs (18 SEZ neurons, 150 Hz)"
    results["water"] = water_summary
    print(f"-> MN9 Left: {water_summary['mn9_left_mean_hz']:.1f} ± {water_summary['mn9_left_std_hz']:.1f} Hz")
    print(f"-> MN9 Right: {water_summary['mn9_right_mean_hz']:.1f} ± {water_summary['mn9_right_std_hz']:.1f} Hz")
    print(f"-> Active Neurons (mean per trial): {water_summary['active_neurons_mean']:.1f} ± {water_summary['active_neurons_std']:.1f}\n")

    # --------------------------------------------------------------------------
    # 5. Dual Ground-Truth Benchmark Against Published Shiu et al. (2024) Data
    # --------------------------------------------------------------------------
    gt_file = ROOT / "Drosophila_brain_model-main" / "results" / "example" / "sugarR.parquet"
    if gt_file.exists():
        print("--- Ground Truth Comparison (vs. Shiu et al. Nature 2024 sugarR.parquet) ---")

        # Benchmark A: Time-matched window (first 100 ms of reference vs first 100 ms of simulation)
        time_matched = compare_to_ground_truth(
            df_sugar,
            gt_file,
            duration_s=1.0,
            n_trials=30,
            time_window_s=(0.0, sim_duration_ms / 1000.0),
            sim_duration_s=sim_duration_ms / 1000.0,
            sim_n_trials=n_trials,
        )
        time_matched["description"] = "Time-matched comparison: first 100 ms of simulation vs first 100 ms of reference"
        results["ground_truth_time_matched_100ms"] = time_matched

        print(f"A. Time-Matched Window (First {sim_duration_ms:.0f} ms):")
        print(f"   -> Jaccard Overlap: {time_matched['jaccard_overlap']:.3f}")
        print(f"   -> Precision: {time_matched['precision']:.3f} | Recall: {time_matched['recall']:.3f}")
        print(f"   -> Pearson Correlation: {time_matched['firing_rate_correlation']:.3f}")
        print(f"   -> Sim Active: {time_matched['sim_active_neurons']} | GT Active in window: {time_matched['gt_active_neurons']} | Shared: {time_matched['shared_active_neurons']}")

        # Benchmark B: Full reference (100 ms simulation vs full 1.0 s cumulative reference)
        cumulative = compare_to_ground_truth(
            df_sugar,
            gt_file,
            duration_s=1.0,
            n_trials=30,
            time_window_s=None,
            sim_duration_s=sim_duration_ms / 1000.0,
            sim_n_trials=n_trials,
        )
        cumulative["description"] = "Cumulative comparison: 100 ms simulation vs full 1.0 s 30-trial reference (methodological mismatch explicitly noted)"
        results["ground_truth_cumulative_1s"] = cumulative

        print(f"\nB. Cumulative 1.0 s Reference Benchmark:")
        print(f"   -> Jaccard Overlap: {cumulative['jaccard_overlap']:.3f}")
        print(f"   -> Precision: {cumulative['precision']:.3f} | Recall: {cumulative['recall']:.3f}")
        print(f"   -> Pearson Correlation: {cumulative['firing_rate_correlation']:.3f}")
        print(f"   -> Shared Active Neurons: {cumulative['shared_active_neurons']}\n")

    # Save summary JSON
    json_path = results_dir / "validation_summary.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[Saved] Multi-trial validation summary saved to: {json_path}")

    # --------------------------------------------------------------------------
    # Plot Publication-Quality Comparative Bar Chart with Error Bars (Mean ± SD)
    # --------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8), dpi=150)
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

    mn9_left_means = [
        results["sugar"]["mn9_left_mean_hz"],
        results["bitter"]["mn9_left_mean_hz"],
        results["sugar_plus_bitter"]["mn9_left_mean_hz"],
        results["water"]["mn9_left_mean_hz"],
    ]
    mn9_left_stds = [
        results["sugar"]["mn9_left_std_hz"],
        results["bitter"]["mn9_left_std_hz"],
        results["sugar_plus_bitter"]["mn9_left_std_hz"],
        results["water"]["mn9_left_std_hz"],
    ]

    active_means = [
        results["sugar"]["active_neurons_mean"],
        results["bitter"]["active_neurons_mean"],
        results["sugar_plus_bitter"]["active_neurons_mean"],
        results["water"]["active_neurons_mean"],
    ]
    active_stds = [
        results["sugar"]["active_neurons_std"],
        results["bitter"]["active_neurons_std"],
        results["sugar_plus_bitter"]["active_neurons_std"],
        results["water"]["active_neurons_std"],
    ]

    # Panel 1: Motor Neuron 9 (MN9 Left) Output with Error Bars
    bars1 = ax1.bar(
        conditions,
        mn9_left_means,
        yerr=mn9_left_stds,
        capsize=4,
        error_kw={"elinewidth": 1.2, "ecolor": "#ffffff"},
        color=colors,
        width=0.55,
        edgecolor="#ffffff",
        linewidth=0.5,
    )
    ax1.set_title("Proboscis Extension Motor Neuron (MN9 Left)", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax1.set_ylabel("Firing Rate (Hz, Mean ± SD)", color="#94a3b8", fontsize=10)
    for bar, m, s in zip(bars1, mn9_left_means, mn9_left_stds):
        h = bar.get_height()
        label = f"{m:.0f}±{s:.0f}" if s > 0 else f"{m:.0f}"
        ax1.text(bar.get_x() + bar.get_width() / 2.0, h + max(s, 2.0) + 1.5, label, ha="center", va="bottom", color="#f8fafc", fontsize=8.5, fontweight="bold")

    # Panel 2: Whole-Brain Active Neuron Population with Error Bars
    bars2 = ax2.bar(
        conditions,
        active_means,
        yerr=active_stds,
        capsize=4,
        error_kw={"elinewidth": 1.2, "ecolor": "#ffffff"},
        color=colors,
        width=0.55,
        edgecolor="#ffffff",
        linewidth=0.5,
    )
    ax2.set_title("Active Neuron Cascade (Mean ± SD per trial)", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax2.set_ylabel("Active Neurons per Trial", color="#94a3b8", fontsize=10)
    for bar, m, s in zip(bars2, active_means, active_stds):
        h = bar.get_height()
        label = f"{m:.0f}±{s:.0f}" if s > 0 else f"{m:.0f}"
        ax2.text(bar.get_x() + bar.get_width() / 2.0, h + max(s, 5.0) + 3.0, label, ha="center", va="bottom", color="#f8fafc", fontsize=8.5, fontweight="bold")

    fig.suptitle(f"ConnectomeToBehaviour: Multi-Trial Validation (N={n_trials} trials, 100 ms biological time)", color="#38bdf8", fontsize=12, fontweight="bold", y=1.02)
    plt.tight_layout()

    plot_path = results_dir / "mn9_response_comparison.png"
    plt.savefig(plot_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[Saved] Comparative graph with error bars saved to: {plot_path}")
    print("=" * 68)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-trial validation of FlyBrain LIF model.")
    parser.add_argument("--n-trials", type=int, default=3, help="Number of stochastic Poisson trials per condition (default: 3)")
    parser.add_argument("--duration-ms", type=float, default=100.0, help="Biological duration per trial in ms (default: 100.0)")
    args = parser.parse_args()

    run_validation(n_trials=args.n_trials, sim_duration_ms=args.duration_ms)
