"""
Ground-truth comparison and evaluation metrics for Drosophila connectome LIF simulations.

Implements the standard validation methodology from:
- Shiu et al. (Nature 2024)
- eonsystemspbc/fly-brain (code/compare_ground_truth.py)
"""

from pathlib import Path
from typing import Dict, Union, Optional
import numpy as np
import pandas as pd


def compute_firing_rates(df_spikes: pd.DataFrame, duration_s: float, n_trials: int = 1) -> pd.Series:
    """
    Calculate per-neuron average firing rate (Hz) from a spike DataFrame.

    Parameters
    ----------
    df_spikes : pd.DataFrame
        DataFrame with at least 'flywire_id' column.
    duration_s : float
        Trial duration in seconds.
    n_trials : int, default=1
        Number of trials in the dataset.

    Returns
    -------
    pd.Series
        Firing rates indexed by flywire_id.
    """
    if len(df_spikes) == 0:
        return pd.Series(dtype=float)
    counts = df_spikes.groupby('flywire_id').size()
    total_time = duration_s * n_trials
    return counts / total_time


def compare_to_ground_truth(
    sim_rates_or_spikes: Union[pd.Series, pd.DataFrame],
    gt_path_or_df: Union[str, Path, pd.DataFrame],
    duration_s: float = 1.0,
    n_trials: int = 30,
    time_window_s: Optional[tuple] = None,
    sim_duration_s: float = 0.1,
    sim_n_trials: int = 1,
) -> Dict[str, float]:
    """
    Compare simulated firing rates against published ground-truth data.

    Parameters
    ----------
    sim_rates_or_spikes : pd.Series or pd.DataFrame
        Simulated firing rates Series or raw spikes DataFrame.
    gt_path_or_df : Path, str, or pd.DataFrame
        Ground-truth reference parquet path or loaded DataFrame.
    duration_s : float, default=1.0
        Biological duration per trial for ground-truth reference.
    n_trials : int, default=30
        Number of trials in the ground-truth reference dataset.
    time_window_s : tuple of (float, float), optional
        Optional (t_start, t_end) window in seconds to perform a time-matched slice
        (e.g., (0.0, 0.1) for matching the first 100 ms).
    sim_duration_s : float, default=0.1
        Biological duration per trial for simulated data.
    sim_n_trials : int, default=1
        Number of trials in simulated data.

    Returns
    -------
    dict
        Dictionary containing Jaccard index, precision, recall, Pearson correlation,
        and counts of active and shared neurons.
    """
    if isinstance(gt_path_or_df, (str, Path)):
        df_gt = pd.read_parquet(gt_path_or_df)
    else:
        df_gt = gt_path_or_df.copy()

    # Apply time-window slice if requested
    gt_effective_duration = duration_s
    if time_window_s is not None and 't' in df_gt.columns:
        t0, t1 = time_window_s
        df_gt = df_gt[(df_gt['t'] >= t0) & (df_gt['t'] <= t1)]
        gt_effective_duration = t1 - t0

    gt_rates = compute_firing_rates(df_gt, duration_s=gt_effective_duration, n_trials=n_trials)

    if isinstance(sim_rates_or_spikes, pd.DataFrame):
        df_sim = sim_rates_or_spikes.copy()
        sim_effective_duration = sim_duration_s
        if time_window_s is not None and 't' in df_sim.columns:
            t0, t1 = time_window_s
            df_sim = df_sim[(df_sim['t'] >= t0) & (df_sim['t'] <= t1)]
            sim_effective_duration = t1 - t0
        sim_rates = compute_firing_rates(df_sim, duration_s=sim_effective_duration, n_trials=sim_n_trials)
    else:
        sim_rates = sim_rates_or_spikes

    gt_neurons = set(gt_rates[gt_rates > 0].index)
    sim_neurons = set(sim_rates[sim_rates > 0].index)

    all_neurons = gt_neurons | sim_neurons
    shared = gt_neurons & sim_neurons

    jaccard = len(shared) / len(all_neurons) if all_neurons else 0.0
    precision = len(shared) / len(sim_neurons) if sim_neurons else 0.0
    recall = len(shared) / len(gt_neurons) if gt_neurons else 0.0

    # Pearson correlation across shared active neurons
    correlation = 0.0
    if len(shared) >= 2:
        shared_list = sorted(shared)
        gt_vec = np.array([gt_rates[n] for n in shared_list])
        sim_vec = np.array([sim_rates[n] for n in shared_list])
        corr_matrix = np.corrcoef(gt_vec, sim_vec)
        if not np.isnan(corr_matrix[0, 1]):
            correlation = float(corr_matrix[0, 1])

    return {
        'jaccard_overlap': float(jaccard),
        'precision': float(precision),
        'recall': float(recall),
        'firing_rate_correlation': float(correlation),
        'sim_active_neurons': int(len(sim_neurons)),
        'gt_active_neurons': int(len(gt_neurons)),
        'shared_active_neurons': int(len(shared)),
        'time_window_matched': bool(time_window_s is not None),
    }
