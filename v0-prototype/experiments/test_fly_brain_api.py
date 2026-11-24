"""
Test script for the FlyBrain API class in src/brain.
Runs a short 50 ms simulation activating sugar GRNs and prints MN9 and active neuron stats.
"""

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.brain import FlyBrain, SUGAR_GRNS_RIGHT, MN9_LEFT, MN9_RIGHT

def main():
    print("=== Testing FlyBrain Class Initialization ===")
    brain = FlyBrain()
    print(f"Loaded connectome metadata: {brain.total_neurons} neurons indexed.")

    print("\n=== Setting Stimulus: Sugar GRNs (150 Hz) ===")
    brain.activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)

    print("\n=== Simulating 50 ms ===")
    df_spikes = brain.simulate(duration_ms=50.0, n_trials=1, exp_name="test_sugar_50ms")

    rates = brain.get_firing_rates()
    active_neurons = brain.get_active_neurons()
    mn_rates = brain.get_motor_neuron_rates()

    print(f"\nResults:")
    print(f"- Total spikes: {len(df_spikes)}")
    print(f"- Active neurons: {len(active_neurons)}")
    print(f"- MN9 Left rate: {mn_rates['MN9_left']} Hz")
    print(f"- MN9 Right rate: {mn_rates['MN9_right']} Hz")

    print("\n=== FlyBrain API test PASSED ===")

if __name__ == "__main__":
    main()
