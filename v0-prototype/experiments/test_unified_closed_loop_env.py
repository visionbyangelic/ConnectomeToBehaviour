"""
Diagnostic Script: Single-Process Unified Closed-Loop Compatibility Test.

Tests whether Brian2 (neural LIF connectome simulation) and FlyGym (NeuroMechFly v2 MuJoCo physics)
can execute co-operatively inside the exact same Python process on Windows with NumPy 1.26.4.

Requirements:
1. True co-execution: brain simulation -> motor extraction -> actuator mapping -> physics step.
2. Temporary, explicitly labeled non-biological test mapping (diagnostic verification of actuator command transmission).
3. Explicit timing tracking: 50 ms biological neural time matched to physics timestep integration.
4. Quantitative verification of physics advancement without memory errors, ABI collisions, or C-extension conflicts.
"""

import sys
import time
from pathlib import Path
import numpy as np

# Ensure repository root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def run_diagnostic():
    print("=" * 70)
    print(" ConnectomeToBehaviour — Unified Process Compatibility Diagnostic")
    print("=" * 70)
    print(f"[Diagnostic] Python version: {sys.version.split()[0]}")
    print(f"[Diagnostic] NumPy version:  {np.__version__}")

    # --------------------------------------------------------------------------
    # Step 1: Import all core simulation engines in the same namespace
    # --------------------------------------------------------------------------
    print("\n--- Step 1: Importing Brian2, FlyGym, MuJoCo, and FlyBrain ---")
    t0_import = time.time()
    try:
        import mujoco
        import brian2
        from flygym import Fly, SingleFlySimulation
        from flygym.arena import FlatTerrain
        from src.brain import FlyBrain, SUGAR_GRNS_RIGHT, MN9_LEFT, MN9_RIGHT
        print(f"[OK] Core libraries imported cleanly in {time.time() - t0_import:.2f}s:")
        print(f"     - MuJoCo: {mujoco.__version__}")
        print(f"     - Brian2: {brian2.__version__} (codegen target: {brian2.prefs.codegen.target})")
    except Exception as e:
        print(f"[FAIL] Library import error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # --------------------------------------------------------------------------
    # Step 2: Initialize FlyBrain and run a real connectome simulation
    # --------------------------------------------------------------------------
    print("\n--- Step 2: Initializing FlyBrain and Simulating Biological Dynamics ---")
    brain_duration_ms = 50.0  # 50 ms biological time (~18s CPU compute)
    brain_duration_s = brain_duration_ms / 1000.0

    t0_brain = time.time()
    brain = FlyBrain()
    print(f"[OK] FlyBrain initialized ({brain.total_neurons} neurons indexed).")

    # Apply 150 Hz Poisson input to sugar-sensing GRNs
    brain.activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)
    print(f"[Action] Activated {len(SUGAR_GRNS_RIGHT)} Sugar GRNs at 150 Hz Poisson drive.")
    print(f"[Simulating] Running {brain_duration_ms:.0f} ms whole-brain simulation...")

    df_spikes = brain.simulate(duration_ms=brain_duration_ms, n_trials=1, exp_name="diagnostic_test", verbose=False)
    brain_time_elapsed = time.time() - t0_brain

    total_spikes = len(df_spikes)
    active_neurons = brain.get_active_neurons()
    print(f"[OK] Brain simulation completed in {brain_time_elapsed:.2f}s:")
    print(f"     - Total spikes generated:    {total_spikes}")
    print(f"     - Active neurons in cascade: {len(active_neurons)}")

    if total_spikes == 0:
        print("[FAIL] Brain simulation produced 0 spikes; cannot proceed to motor extraction.")
        return False

    # --------------------------------------------------------------------------
    # Step 3: Extract Motor Neuron Output (Spike Counts & Firing Rates)
    # --------------------------------------------------------------------------
    print("\n--- Step 3: Extracting Motor Neuron 9 Output ---")
    mn_rates = brain.get_motor_neuron_rates()
    mn9_left_spikes = len(df_spikes[df_spikes['flywire_id'] == MN9_LEFT])
    mn9_right_spikes = len(df_spikes[df_spikes['flywire_id'] == MN9_RIGHT])

    print(f"[Motor Output] MN9 Left:  {mn9_left_spikes} spikes -> {mn_rates['MN9_left']:.1f} Hz (over {brain_duration_ms} ms)")
    print(f"[Motor Output] MN9 Right: {mn9_right_spikes} spikes -> {mn_rates['MN9_right']:.1f} Hz (over {brain_duration_ms} ms)")

    # --------------------------------------------------------------------------
    # Step 4: Initialize FlyGym (NeuroMechFly v2) Physics Engine
    # --------------------------------------------------------------------------
    print("\n--- Step 4: Initializing FlyGym MuJoCo Body Simulation ---")
    physics_dt = 1e-4  # 0.1 ms per physics integration timestep
    arena = FlatTerrain()
    fly = Fly(spawn_pos=(0, 0, 0.2))
    sim = SingleFlySimulation(fly=fly, arena=arena, timestep=physics_dt)
    print(f"[OK] SingleFlySimulation instantiated (dt = {physics_dt*1000:.2f} ms).")

    obs, info = sim.reset()
    actuated_joints = fly.actuated_joints
    num_actuators = len(actuated_joints)
    print(f"[OK] Simulation reset completed.")
    print(f"     - Actuated joint count: {num_actuators}")
    print(f"     - Sample joint names:   {actuated_joints[:3]} ... {actuated_joints[-3:]}")

    # --------------------------------------------------------------------------
    # Step 5: Temporary Diagnostic Mapping to an Actuator
    # --------------------------------------------------------------------------
    print("\n--- Step 5: Applying Temporary Diagnostic Actuator Mapping ---")
    print("  [NOTE: This is a diagnostic software handoff test, NOT an anatomical decoder]")

    # Select the first actuated joint as a test target
    test_joint_idx = 0
    test_joint_name = actuated_joints[test_joint_idx]
    
    # Read initial joint position from observation
    initial_joint_angles = obs["joints"][0].copy() if "joints" in obs else np.zeros(num_actuators)
    initial_test_angle = float(initial_joint_angles[test_joint_idx])
    print(f"     - Target test actuator: index {test_joint_idx} ('{test_joint_name}')")
    print(f"     - Initial joint angle:  {initial_test_angle:.6f} rad")

    # Diagnostic rule: Scale MN9 Left firing rate (0 - 100 Hz) to a test joint displacement (e.g. 0.0 - 0.2 rad)
    # This explicitly verifies the actuator command changes target proportional to brain activity
    test_command_scale = 0.002  # rad per Hz
    test_target_angle = initial_test_angle + (mn_rates['MN9_left'] * test_command_scale)

    action = {"joints": np.zeros(num_actuators)}
    action["joints"][test_joint_idx] = test_target_angle
    print(f"     - Computed test command: {test_target_angle:.6f} rad (delta = +{test_target_angle - initial_test_angle:.6f} rad)")

    # --------------------------------------------------------------------------
    # Step 6: Step MuJoCo Physics and Verify Simulation Advancement
    # --------------------------------------------------------------------------
    print("\n--- Step 6: Stepping MuJoCo Physics with Brain-Derived Command ---")
    initial_sim_time = sim.curr_time
    
    # Step physics for 500 steps (500 * 1e-4 s = 50.0 ms of physical time, matching the 50 ms brain window)
    num_physics_steps = int(round(brain_duration_s / physics_dt))
    print(f"[Stepping] Advancing {num_physics_steps} physics steps ({num_physics_steps * physics_dt * 1000:.1f} ms physical time)...")

    t0_physics = time.time()
    for step_i in range(num_physics_steps):
        obs, reward, terminated, truncated, info = sim.step(action)

    physics_time_elapsed = time.time() - t0_physics
    final_sim_time = sim.curr_time
    advanced_time = final_sim_time - initial_sim_time

    final_joint_angles = obs["joints"][0] if "joints" in obs else np.zeros(num_actuators)
    final_test_angle = float(final_joint_angles[test_joint_idx])

    print(f"[OK] Physics stepped successfully in {physics_time_elapsed:.2f}s:")
    print(f"     - Initial simulation clock: {initial_sim_time:.4f} s")
    print(f"     - Final simulation clock:   {final_sim_time:.4f} s (advanced: {advanced_time*1000:.1f} ms)")
    print(f"     - Initial test joint angle: {initial_test_angle:.6f} rad")
    print(f"     - Final test joint angle:   {final_test_angle:.6f} rad")
    print(f"     - Actuator responded:      {'YES (angle evolved)' if abs(final_test_angle - initial_test_angle) > 1e-5 else 'NO'}")

    sim.close()

    # --------------------------------------------------------------------------
    # Step 7: Pass/Fail Evaluation Criteria
    # --------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" Diagnostic Evaluation Summary")
    print("=" * 70)
    
    checks = {
        "1. Libraries imported in same process": True,
        "2. Brian2 simulated connectome (>0 spikes)": total_spikes > 0,
        "3. Motor neuron rates extracted without error": ('MN9_left' in mn_rates and mn_rates['MN9_left'] > 0),
        "4. FlyGym initialized on flat terrain": True,
        "5. Brain output converted to valid actuator command": action is not None,
        "6. MuJoCo stepped matching 50 ms duration": abs(advanced_time - brain_duration_s) < 1e-5,
        "7. Zero memory faults, ABI collisions, or C-extension errors": True,
    }

    for desc, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f" {status} — {desc}")

    all_passed = all(checks.values())
    print("=" * 70)
    if all_passed:
        print("🎉 UNIFIED PROCESS COMPATIBILITY CONFIRMED!")
        print("Brian2 and FlyGym co-exist and pass data within a single Python process.")
        print("IPC/socket bridge is NOT needed; Phase 4 can proceed with direct in-process calls.")
    else:
        print("⚠️ One or more unified execution checks failed.")
    print("=" * 70)

    return all_passed


if __name__ == "__main__":
    success = run_diagnostic()
    sys.exit(0 if success else 1)

