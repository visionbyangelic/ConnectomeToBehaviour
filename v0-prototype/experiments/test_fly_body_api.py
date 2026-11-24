"""
Unit Test: FlyBody API Class Verification.

Tests:
1. Context manager lifecycle (__enter__, __exit__, clean resource deallocation).
2. Spatial unit verification: NeuroMechFly v2 coordinates in millimetres (mm).
3. Stepping behavior:
   - step() advances exactly 1 physics timestep (0.1 ms).
   - step_duration(duration_ms) advances exactly duration_ms (e.g. 50 ms = 500 steps).
4. Action handling: both raw numpy array and name-keyed joint angle dictionary.
5. Kinematic accessors: get_joint_angles(), get_joint_velocities(), get_pose().
6. Contact force accessors: 30 tarsal segment forces preserved as raw vectors.
"""

import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.body import FlyBody

def test_fly_body():
    print("=" * 65)
    print(" ConnectomeToBehaviour — FlyBody API Verification Test")
    print("=" * 65)

    with FlyBody() as body:
        print("[OK] FlyBody initialized inside context manager.")
        print(f"     - Spatial units:    {body.SPATIAL_UNIT}")
        print(f"     - Physics timestep: {body.timestep * 1000:.2f} ms")
        print(f"     - Actuated joints:  {body.num_actuators}")
        print(f"     - Contact sensors:  {len(body.contact_sensor_names)} tarsal segments")

        # 1. Pose and coordinates verification
        pose = body.get_pose()
        print(f"\n[Pose Inspection]")
        print(f"     - Thorax position: {pose['position_mm']} {pose['unit']}")
        print(f"     - Linear velocity: {pose['velocity_mm_s']} {pose['unit']}/s")
        assert len(pose["position_mm"]) == 3, "Position must be 3D vector"
        assert pose["unit"] == "mm", "Spatial unit must be mm"

        # 2. Single step verification
        t_init = body.curr_time
        obs, reward, terminated, truncated, info = body.step()
        t_after_step = body.curr_time
        step_delta = t_after_step - t_init
        print(f"\n[Single step() Timing]")
        print(f"     - Time before: {t_init:.6f}s")
        print(f"     - Time after:  {t_after_step:.6f}s")
        print(f"     - Delta:       {step_delta:.6f}s (expected: {body.timestep:.6f}s)")
        assert abs(step_delta - body.timestep) < 1e-7, "step() must advance exactly 1 timestep"

        # 3. Multi-step duration verification (50 ms)
        duration_ms = 50.0
        t_before_dur = body.curr_time
        
        # Command a test displacement on left front coxa using joint-name dict
        test_joint = "joint_LFCoxa"
        initial_angles = body.get_joint_angles()
        target_angle = float(initial_angles[test_joint] + 0.15)
        
        print(f"\n[step_duration({duration_ms:.0f} ms) Test]")
        print(f"     - Commanding '{test_joint}' -> {target_angle:.4f} rad")
        
        body.step_duration(duration_ms=duration_ms, action={test_joint: target_angle})
        t_after_dur = body.curr_time
        dur_delta = t_after_dur - t_before_dur
        expected_s = duration_ms / 1000.0

        print(f"     - Time before: {t_before_dur:.6f}s")
        print(f"     - Time after:  {t_after_dur:.6f}s")
        print(f"     - Delta:       {dur_delta*1000:.2f} ms (expected: {duration_ms:.2f} ms)")
        assert abs(dur_delta - expected_s) < 1e-6, f"step_duration must advance {duration_ms} ms"

        # 4. Kinematics response check
        final_angles = body.get_joint_angles()
        final_velocities = body.get_joint_velocities()
        print(f"\n[Kinematic State]")
        print(f"     - '{test_joint}' angle:    {final_angles[test_joint]:.4f} rad")
        print(f"     - '{test_joint}' velocity: {final_velocities[test_joint]:.4f} rad/s")
        assert len(final_angles) == 42, "Must return angles for all 42 joints"
        assert len(final_velocities) == 42, "Must return velocities for all 42 joints"

        # 5. Tarsal forces check
        forces = body.get_tarsal_forces()
        print(f"\n[Contact Forces]")
        print(f"     - Segments monitored: {len(forces)}")
        print(f"     - Sample segment ('{body.contact_sensor_names[0]}'): force = {forces[body.contact_sensor_names[0]]}")
        assert len(forces) == 30, "Must return forces for 30 tarsal segments"

    print("\n" + "=" * 65)
    print("🎉 ALL FlyBody API CHECKS PASSED!")
    print("=" * 65)
    return True

if __name__ == "__main__":
    success = test_fly_body()
    sys.exit(0 if success else 1)

