"""
Experiment: Test MN9 Bilateral Symmetry and Asymmetry.

Tests whether MN9 Left vs. Right firing asymmetry is driven by unilateral sensory stimulation:
1. Right sugar GRNs alone (21 neurons, 150 Hz) -> expect Left > Right or asymmetric
2. Left sugar GRNs alone (10 neurons, 150 Hz)  -> expect Right > Left (mirror-image)
3. Bilateral sugar GRNs (31 neurons, 150 Hz)   -> expect symmetric activation
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.brain import (
    FlyBrain,
    SUGAR_GRNS_RIGHT,
    SUGAR_GRNS_LEFT,
    MN9_LEFT,
    MN9_RIGHT,
)

def run_symmetry_test():
    print("=" * 70)
    print(" ConnectomeToBehaviour — MN9 Lateralization & Symmetry Test")
    print("=" * 70)

    brain = FlyBrain()
    duration_ms = 100.0

    # 1. Right GRNs alone
    print("\n--- Condition 1: Right Sugar GRNs Alone (21 neurons, 150 Hz) ---")
    brain.reset_stimuli().activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)
    df_r = brain.simulate(duration_ms=duration_ms, n_trials=1, exp_name="sugar_right", verbose=False)
    r_rates = brain.get_motor_neuron_rates()
    r_left_spikes = len(df_r[df_r['flywire_id'] == MN9_LEFT])
    r_right_spikes = len(df_r[df_r['flywire_id'] == MN9_RIGHT])
    print(f"Right-only Input -> MN9 Left: {r_left_spikes} spikes ({r_rates['MN9_left']} Hz) | MN9 Right: {r_right_spikes} spikes ({r_rates['MN9_right']} Hz)")

    # 2. Left GRNs alone
    print("\n--- Condition 2: Left Sugar GRNs Alone (10 neurons, 150 Hz) ---")
    brain.reset_stimuli().activate(SUGAR_GRNS_LEFT, freq_hz=150.0)
    df_l = brain.simulate(duration_ms=duration_ms, n_trials=1, exp_name="sugar_left", verbose=False)
    l_rates = brain.get_motor_neuron_rates()
    l_left_spikes = len(df_l[df_l['flywire_id'] == MN9_LEFT])
    l_right_spikes = len(df_l[df_l['flywire_id'] == MN9_RIGHT])
    print(f"Left-only Input  -> MN9 Left: {l_left_spikes} spikes ({l_rates['MN9_left']} Hz) | MN9 Right: {l_right_spikes} spikes ({l_rates['MN9_right']} Hz)")

    # 3. Bilateral GRNs
    print("\n--- Condition 3: Bilateral Sugar GRNs (31 neurons, 150 Hz) ---")
    bilateral_grns = SUGAR_GRNS_RIGHT + SUGAR_GRNS_LEFT
    brain.reset_stimuli().activate(bilateral_grns, freq_hz=150.0)
    df_bi = brain.simulate(duration_ms=duration_ms, n_trials=1, exp_name="sugar_bilateral", verbose=False)
    bi_rates = brain.get_motor_neuron_rates()
    bi_left_spikes = len(df_bi[df_bi['flywire_id'] == MN9_LEFT])
    bi_right_spikes = len(df_bi[df_bi['flywire_id'] == MN9_RIGHT])
    print(f"Bilateral Input  -> MN9 Left: {bi_left_spikes} spikes ({bi_rates['MN9_left']} Hz) | MN9 Right: {bi_right_spikes} spikes ({bi_rates['MN9_right']} Hz)")

    print("\n" + "=" * 70)
    print(" Symmetry Analysis Summary")
    print("=" * 70)
    print(f"Right Input Asymmetry Ratio (Left/Right): {r_rates['MN9_left'] / max(r_rates['MN9_right'], 1e-5):.2f}")
    print(f"Left Input Asymmetry Ratio  (Right/Left): {l_rates['MN9_right'] / max(l_rates['MN9_left'], 1e-5):.2f}")
    diff_bi = abs(bi_rates['MN9_left'] - bi_rates['MN9_right'])
    print(f"Bilateral Difference: |Left - Right| = {diff_bi:.1f} Hz")
    print("=" * 70)

if __name__ == "__main__":
    run_symmetry_test()

