"""
Canonical 1.0-Second Multi-Trial Validation Suite (N=10 Trials).

Matches Shiu et al. (Nature 2024) full 1.0-second trial protocol:
1. Sugar GRN excitation (150 Hz) -> Proboscis extension motor neuron (MN9) activation.
2. Bitter GRN excitation (150 Hz) -> Aversive baseline (no MN9 activation).
3. Sugar + Bitter co-activation (150 Hz each) -> Statistical test of lateral inhibition.
4. Water GRN excitation (150 Hz) -> Distinct SEZ circuit.
5. Reference Model Comparison (vs. Shiu et al. 1.0 s sugar simulation):
   - Jaccard overlap, precision, recall, Pearson correlation.
   - Rigorous statistics: Mean, Standard Deviation, 95% Confidence Interval, Welch's t-test.
6. Execution: Parallelized across CPU cores using joblib.
"""

import sys
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from brian2 import ms, second, Hz, prefs
prefs.codegen.target = "numpy"

from src.brain import (
    FlyBrain,
    SUGAR_GRNS_RIGHT,
    BITTER_GRNS,
    WATER_GRNS,
    MN9_LEFT,
    MN9_RIGHT,
    compare_to_ground_truth,
)


def run_single_trial(
    trial_idx: int,
    duration_s: float,
    stim_primary: list,
    freq_primary: float,
    stim_secondary: list,
    freq_secondary: float,
    exp_name: str,
):
    """Worker function for a single parallel trial."""
    # Set unique seed per trial for stochastic Poisson inputs
    np.random.seed(42 + trial_idx * 17)

    brain = FlyBrain(preload_connectome=True)
    brain.reset_stimuli()
    if stim_primary and freq_primary > 0:
        brain.activate(stim_primary, freq_hz=freq_primary)
    if stim_secondary and freq_secondary > 0:
        brain.activate_secondary(stim_secondary, freq_hz=freq_secondary)

    duration_ms = duration_s * 1000.0
    net, spk_mon = brain._build_network(duration_ms=duration_ms)
    net.run(duration_s * second)

    spike_trains = spk_mon.spike_trains()
    all_ts = []
    all_ids = []

    for brian_idx, times in spike_trains.items():
        if len(times) > 0:
            fly_id = brain.i2flyid[brian_idx]
            for t in times:
                all_ts.append(float(t / second))
                all_ids.append(fly_id)

    df_trial = pd.DataFrame({
        "t": all_ts,
        "trial": trial_idx,
        "flywire_id": all_ids,
        "exp_name": exp_name,
    })

    mn9_l_spikes = len(df_trial[df_trial["flywire_id"] == MN9_LEFT])
    mn9_r_spikes = len(df_trial[df_trial["flywire_id"] == MN9_RIGHT])

    active_neurons = len(df_trial["flywire_id"].unique()) if len(df_trial) > 0 else 0
    total_spikes = len(df_trial)

    return {
        "trial": trial_idx,
        "spikes_df": df_trial,
        "mn9_left_hz": mn9_l_spikes / duration_s,
        "mn9_right_hz": mn9_r_spikes / duration_s,
        "total_spikes": total_spikes,
        "active_neurons": active_neurons,
    }


def run_condition_parallel(
    exp_name: str,
    stim_primary: list,
    freq_primary: float,
    stim_secondary: list,
    freq_secondary: float,
    duration_s: float = 1.0,
    n_trials: int = 10,
    n_jobs: int = 3,
):
    print(f"\n>>> Running '{exp_name}' (N={n_trials} trials, {duration_s}s duration, {n_jobs} parallel workers)...")
    t0 = time.time()

    results = Parallel(n_jobs=n_jobs, verbose=5)(
        delayed(run_single_trial)(
            tr,
            duration_s,
            stim_primary,
            freq_primary,
            stim_secondary,
            freq_secondary,
            exp_name,
        )
        for tr in range(n_trials)
    )

    elapsed = time.time() - t0
    print(f"[Done] {exp_name} completed in {elapsed:.1f}s ({elapsed/60.0:.1f} min)")

    dfs = [r["spikes_df"] for r in results]
    df_all = pd.concat(dfs, ignore_index=True)

    mn9_l = [r["mn9_left_hz"] for r in results]
    mn9_r = [r["mn9_right_hz"] for r in results]
    spikes = [r["total_spikes"] for r in results]
    active = [r["active_neurons"] for r in results]

    def calc_ci(data):
        mean = float(np.mean(data))
        sem = float(stats.sem(data)) if len(data) > 1 else 0.0
        ci95 = float(sem * stats.t.ppf((1 + 0.95) / 2.0, len(data) - 1)) if len(data) > 1 else 0.0
        return mean, float(np.std(data, ddof=1)), ci95

    l_m, l_s, l_ci = calc_ci(mn9_l)
    r_m, r_s, r_ci = calc_ci(mn9_r)
    spk_m, spk_s, spk_ci = calc_ci(spikes)
    act_m, act_s, act_ci = calc_ci(active)

    summary = {
        "exp_name": exp_name,
        "duration_s": duration_s,
        "n_trials": n_trials,
        "mn9_left": {"mean": l_m, "std": l_s, "ci95": l_ci, "trials": mn9_l},
        "mn9_right": {"mean": r_m, "std": r_s, "ci95": r_ci, "trials": mn9_r},
        "total_spikes": {"mean": spk_m, "std": spk_s, "ci95": spk_ci},
        "active_neurons": {"mean": act_m, "std": act_s, "ci95": act_ci},
        "cumulative_active_neurons": len(df_all["flywire_id"].unique()),
        "elapsed_s": elapsed,
    }

    print(f" -> MN9 Left:  {l_m:.1f} ± {l_s:.1f} Hz (95% CI: [{l_m - l_ci:.1f}, {l_m + l_ci:.1f}])")
    print(f" -> MN9 Right: {r_m:.1f} ± {r_s:.1f} Hz (95% CI: [{r_m - r_ci:.1f}, {r_m + r_ci:.1f}])")
    print(f" -> Active Neurons / trial: {act_m:.1f} ± {act_s:.1f} (cumulative: {summary['cumulative_active_neurons']})")

    return df_all, summary


def main():
    duration_s = 1.0
    n_trials = 10
    n_jobs = 3

    out_dir = ROOT / "results" / "validation"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print(f" ConnectomeToBehaviour — Canonical Multi-Trial Validation Suite")
    print(f" Protocol: 1.0 s duration x N={n_trials} trials per condition")
    print(f" Reference Model Benchmark: Shiu et al. (Nature 2024) sugarR.parquet (1.0 s)")
    print("=" * 70)

    t_suite_start = time.time()
    results = {
        "metadata": {
            "duration_s": duration_s,
            "n_trials": n_trials,
            "n_jobs": n_jobs,
            "connectome": "FlyWire v630 (2023_03_23)",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    }

    # 1. Sugar alone (150 Hz)
    df_sugar, sum_sugar = run_condition_parallel(
        "sugar_150hz", SUGAR_GRNS_RIGHT, 150.0, [], 0.0, duration_s, n_trials, n_jobs
    )
    results["sugar"] = sum_sugar

    # 2. Bitter alone (150 Hz)
    df_bitter, sum_bitter = run_condition_parallel(
        "bitter_150hz", BITTER_GRNS, 150.0, [], 0.0, duration_s, n_trials, n_jobs
    )
    results["bitter"] = sum_bitter

    # 3. Sugar + Bitter co-activation (150 Hz each)
    df_dual, sum_dual = run_condition_parallel(
        "sugar_plus_bitter_150hz", SUGAR_GRNS_RIGHT, 150.0, BITTER_GRNS, 150.0, duration_s, n_trials, n_jobs
    )
    results["sugar_plus_bitter"] = sum_dual

    # 4. Water alone (150 Hz)
    df_water, sum_water = run_condition_parallel(
        "water_150hz", WATER_GRNS, 150.0, [], 0.0, duration_s, n_trials, n_jobs
    )
    results["water"] = sum_water

    # 5. Statistical Hypothesis Testing: Does Bitter suppress MN9 firing?
    sugar_l_rates = sum_sugar["mn9_left"]["trials"]
    dual_l_rates = sum_dual["mn9_left"]["trials"]
    t_stat_l, p_val_l = stats.ttest_ind(sugar_l_rates, dual_l_rates, equal_var=False)

    sugar_r_rates = sum_sugar["mn9_right"]["trials"]
    dual_r_rates = sum_dual["mn9_right"]["trials"]
    t_stat_r, p_val_r = stats.ttest_ind(sugar_r_rates, dual_r_rates, equal_var=False)

    pct_inhibition_l = (1.0 - sum_dual["mn9_left"]["mean"] / sum_sugar["mn9_left"]["mean"]) * 100.0
    pct_inhibition_r = (1.0 - sum_dual["mn9_right"]["mean"] / sum_sugar["mn9_right"]["mean"]) * 100.0

    stats_test = {
        "mn9_left": {
            "welch_t_statistic": float(t_stat_l),
            "p_value": float(p_val_l),
            "percent_inhibition": float(pct_inhibition_l),
            "significant_at_0_05": bool(p_val_l < 0.05),
            "significant_at_0_01": bool(p_val_l < 0.01),
        },
        "mn9_right": {
            "welch_t_statistic": float(t_stat_r),
            "p_value": float(p_val_r),
            "percent_inhibition": float(pct_inhibition_r),
            "significant_at_0_05": bool(p_val_r < 0.05),
            "significant_at_0_01": bool(p_val_r < 0.01),
        },
    }
    results["statistical_tests"] = stats_test

    print("\n" + "=" * 70)
    print(" Statistical Hypothesis Test: Lateral Inhibition")
    print("=" * 70)
    print(f"MN9 Left:  {sum_sugar['mn9_left']['mean']:.1f} Hz -> {sum_dual['mn9_left']['mean']:.1f} Hz ({pct_inhibition_l:.1f}% suppression)")
    print(f"           Welch's t = {t_stat_l:.3f}, p = {p_val_l:.4e} {'(STATISTICALLY SIGNIFICANT p < 0.01)' if p_val_l < 0.01 else ''}")
    print(f"MN9 Right: {sum_sugar['mn9_right']['mean']:.1f} Hz -> {sum_dual['mn9_right']['mean']:.1f} Hz ({pct_inhibition_r:.1f}% suppression)")
    print(f"           Welch's t = {t_stat_r:.3f}, p = {p_val_r:.4e} {'(STATISTICALLY SIGNIFICANT p < 0.01)' if p_val_r < 0.01 else ''}")

    # 6. Reference Model Comparison (against Shiu et al. sugarR.parquet)
    gt_path = ROOT / "Drosophila_brain_model-main" / "results" / "example" / "sugarR.parquet"
    if gt_path.exists():
        print("\n" + "=" * 70)
        print(" Reference Model Reproduction Benchmark (vs. Shiu et al. 1.0 s simulation)")
        print("=" * 70)
        benchmark_results = compare_to_ground_truth(
            df_sugar,
            gt_path,
            duration_s=1.0,
            n_trials=30,
            sim_duration_s=1.0,
            sim_n_trials=n_trials,
        )
        results["reference_model_benchmark_1s"] = benchmark_results
        print(f"-> Pearson Firing-Rate Correlation: {benchmark_results['firing_rate_correlation']:.4f}")
        print(f"-> Jaccard Overlap:                {benchmark_results['jaccard_overlap']:.4f}")
        print(f"-> Precision:                      {benchmark_results['precision']:.4f}")
        print(f"-> Recall:                         {benchmark_results['recall']:.4f}")
        print(f"-> Shared Active Neurons:          {benchmark_results['shared_active_neurons']}")
        print(f"-> Sim Active Neurons:             {benchmark_results['sim_active_neurons']}")
        print(f"-> Reference Active Neurons:       {benchmark_results['gt_active_neurons']}")

    total_suite_time = time.time() - t_suite_start
    results["metadata"]["total_suite_elapsed_s"] = total_suite_time
    print(f"\n[Complete] Entire 4-condition N=10 validation finished in {total_suite_time/60.0:.1f} min.")

    # Save summary JSON
    json_path = out_dir / "validation_summary_1s_n10.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[Saved] Canonical JSON results: {json_path}")

    # 7. Generate Publication-Quality Figure with 95% Confidence Intervals
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=150)
    fig.patch.set_facecolor("#0f172a")

    for ax in (ax1, ax2):
        ax.set_facecolor("#1e293b")
        ax.tick_params(colors="#94a3b8", labelsize=9)
        ax.spines["bottom"].set_color("#334155")
        ax.spines["top"].set_color("#334155")
        ax.spines["left"].set_color("#334155")
        ax.spines["right"].set_color("#334155")
        ax.grid(True, linestyle="--", alpha=0.15, color="#f8fafc")

    cond_labels = ["Sugar", "Bitter", "Sugar+Bitter", "Water"]
    cond_colors = ["#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

    mn9_left_means = [results[k]["mn9_left"]["mean"] for k in ["sugar", "bitter", "sugar_plus_bitter", "water"]]
    mn9_left_cis = [results[k]["mn9_left"]["ci95"] for k in ["sugar", "bitter", "sugar_plus_bitter", "water"]]

    active_means = [results[k]["active_neurons"]["mean"] for k in ["sugar", "bitter", "sugar_plus_bitter", "water"]]
    active_cis = [results[k]["active_neurons"]["ci95"] for k in ["sugar", "bitter", "sugar_plus_bitter", "water"]]

    # Panel 1: MN9 Left
    bars1 = ax1.bar(
        cond_labels,
        mn9_left_means,
        yerr=mn9_left_cis,
        capsize=5,
        error_kw={"elinewidth": 1.4, "ecolor": "#ffffff"},
        color=cond_colors,
        width=0.55,
        edgecolor="#ffffff",
        linewidth=0.5,
    )
    ax1.set_title("MN9 Left Firing Rate (Mean ± 95% CI, N=10 Trials)", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax1.set_ylabel("Firing Rate (Hz)", color="#94a3b8", fontsize=10)
    for bar, m, ci in zip(bars1, mn9_left_means, mn9_left_cis):
        h = bar.get_height()
        label = f"{m:.1f}±{ci:.1f}" if ci > 0 else f"{m:.1f}"
        ax1.text(bar.get_x() + bar.get_width() / 2.0, h + max(ci, 2.0) + 2.0, label, ha="center", va="bottom", color="#f8fafc", fontsize=8.5, fontweight="bold")

    # Panel 2: Active Neurons
    bars2 = ax2.bar(
        cond_labels,
        active_means,
        yerr=active_cis,
        capsize=5,
        error_kw={"elinewidth": 1.4, "ecolor": "#ffffff"},
        color=cond_colors,
        width=0.55,
        edgecolor="#ffffff",
        linewidth=0.5,
    )
    ax2.set_title("Active Neurons per Trial (Mean ± 95% CI, N=10 Trials)", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax2.set_ylabel("Active Neurons Count", color="#94a3b8", fontsize=10)
    for bar, m, ci in zip(bars2, active_means, active_cis):
        h = bar.get_height()
        label = f"{m:.0f}±{ci:.0f}" if ci > 0 else f"{m:.0f}"
        ax2.text(bar.get_x() + bar.get_width() / 2.0, h + max(ci, 5.0) + 4.0, label, ha="center", va="bottom", color="#f8fafc", fontsize=8.5, fontweight="bold")

    fig.suptitle("ConnectomeToBehaviour — Canonical Validation (1.0 s biological time, N=10 trials)", color="#38bdf8", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()

    plot_path = out_dir / "mn9_response_1s_n10.png"
    plt.savefig(plot_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[Saved] Publication chart with 95% CI: {plot_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()

