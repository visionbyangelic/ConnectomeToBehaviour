"""
Benchmark Script: Measure Brian2 Build Time vs. Run Time Separately.

Isolates:
1. Parquet/CSV loading time
2. Brian2 network instantiation & synaptic connection time (_build_network)
3. Initial compilation & first simulation step (net.run(50 ms))
4. Subsequent simulation steps on the SAME pre-built network (net.run(50 ms) without rebuild)
5. Scaling to 100 ms and 1000 ms to determine real-time factor and closed-loop feasibility.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from brian2 import ms, second, prefs
prefs.codegen.target = "numpy"

from src.brain import FlyBrain, SUGAR_GRNS_RIGHT

def benchmark():
    print("=" * 70)
    print(" ConnectomeToBehaviour — Brian2 Build vs. Run Benchmark")
    print("=" * 70)

    # 1. Initialize FlyBrain (CSV metadata indexing)
    t0 = time.time()
    brain = FlyBrain(preload_connectome=True)
    t_metadata = time.time() - t0
    print(f"[Timing] 1. Metadata indexing ({brain.total_neurons} neurons): {t_metadata:.3f} s")

    # 2. Build Brian2 Network (Parquet load + Synapses connect + weight assignment)
    brain.activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)
    t0 = time.time()
    net, spk_mon = brain._build_network(duration_ms=50.0)
    t_build = time.time() - t0
    print(f"[Timing] 2. _build_network() (Parquet read + graph build): {t_build:.3f} s")

    # 3. First run (includes Brian2 code generation / overhead on first call)
    t0 = time.time()
    net.run(50.0 * ms)
    t_first_run_50ms = time.time() - t0
    spikes_1 = len(spk_mon.i)
    print(f"[Timing] 3. net.run(50 ms) [FIRST RUN - codegen + step]:   {t_first_run_50ms:.3f} s ({spikes_1} spikes)")

    # 4. Second run on the SAME network instance (pure ODE integration, zero rebuild)
    t0 = time.time()
    net.run(50.0 * ms)
    t_second_run_50ms = time.time() - t0
    spikes_2 = len(spk_mon.i) - spikes_1
    print(f"[Timing] 4. net.run(50 ms) [SECOND RUN - SAME network]:     {t_second_run_50ms:.3f} s ({spikes_2} spikes)")

    # 5. Third run on same network (100 ms step)
    t0 = time.time()
    net.run(100.0 * ms)
    t_third_run_100ms = time.time() - t0
    spikes_3 = len(spk_mon.i) - (spikes_1 + spikes_2)
    print(f"[Timing] 5. net.run(100 ms) [SAME network]:                  {t_third_run_100ms:.3f} s ({spikes_3} spikes)")

    # Calculate real-time factor
    # Real-time factor = compute time / biological time
    rtf_second = t_second_run_50ms / 0.050
    rtf_third = t_third_run_100ms / 0.100

    print("\n" + "=" * 70)
    print(" Performance Breakdown & Real-Time Factor (RTF)")
    print("=" * 70)
    print(f"Fixed Build Overhead (_build_network): {t_build:.2f} s")
    print(f"Incremental Run Rate (50 ms):          {t_second_run_50ms:.2f} s ({t_second_run_50ms/50.0*1000:.1f} ms compute per biological ms)")
    print(f"Incremental Run Rate (100 ms):         {t_third_run_100ms:.2f} s ({t_third_run_100ms/100.0*1000:.1f} ms compute per biological ms)")
    print(f"Real-Time Factor (steady-state):       {rtf_third:.1f}x slower than real time")
    print(f"Rebuild Overhead Ratio in 50 ms run:   {t_build / (t_build + t_first_run_50ms) * 100:.1f}% of total elapsed time")
    print("=" * 70)

if __name__ == "__main__":
    benchmark()

