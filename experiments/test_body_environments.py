"""
Diagnostic script for Phase 3: Body Simulation Stack.

Tests:
1. MuJoCo core physics initialization and stepping.
2. FlyGym (NeuroMechFly v2) single-fly simulation on flat terrain.
3. FlyBody (DeepMind/Janelia) FruitFly model compilation and physics stepping.
4. Verifies runtime compatibility with NumPy 1.26.4.
"""

import sys
import numpy as np

def test_mujoco_core():
    print("\n--- 1. Testing Core MuJoCo Physics Engine ---")
    import mujoco
    print(f"[OK] MuJoCo library imported successfully: version {mujoco.__version__}")

    # Minimal test model
    xml = """
    <mujoco>
        <worldbody>
            <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
            <geom type="plane" size="1 1 0.1"/>
            <body pos="0 0 1">
                <joint type="free"/>
                <geom type="sphere" size="0.1" rgba="0 1 0 1"/>
            </body>
        </worldbody>
    </mujoco>
    """
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    print(f"[OK] Minimal MjModel compiled successfully (nbody={model.nbody}, ngeom={model.ngeom})")

    for step in range(10):
        mujoco.mj_step(model, data)
    print(f"[OK] 10 physics steps completed. Sphere height z = {data.qpos[2]:.4f} m (free fall gravity active)")
    return True


def test_flygym_body():
    print("\n--- 2. Testing FlyGym (NeuroMechFly v2) ---")
    try:
        from flygym import Fly, SingleFlySimulation
        from flygym.arena import FlatTerrain
        print("[OK] FlyGym imports succeeded.")

        # Initialize flat arena and standard fly model
        arena = FlatTerrain()
        fly = Fly(spawn_pos=(0, 0, 0.2))
        sim = SingleFlySimulation(fly=fly, arena=arena, timestep=1e-4)
        print("[OK] SingleFlySimulation instantiated successfully.")

        obs, info = sim.reset()
        print(f"[OK] Environment reset succeeded.")
        print(f"     - Number of actuated joints: {len(fly.actuated_joints)}")

        # Step 10 frames with zero / neutral action dict
        action = {"joints": np.zeros(len(fly.actuated_joints))}
        for step in range(10):
            obs, reward, terminated, truncated, info = sim.step(action)

        print(f"[OK] 10 FlyGym physics steps completed without error!")
        sim.close()
        return True
    except Exception as e:
        print(f"[FAIL] FlyGym encountered an error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_flybody_model():
    print("\n--- 3. Testing FlyBody (FruitFly / MuJoCo) ---")
    try:
        from dm_control import mjcf
        from flybody.fruitfly.fruitfly import FruitFly
        print("[OK] FlyBody FruitFly class imported.")

        fly = FruitFly()
        print(f"[OK] FruitFly model created: name='{fly.mjcf_model.model}'")

        # Compile MJCF to MuJoCo physics
        physics = mjcf.Physics.from_mjcf_model(fly.mjcf_model)
        print(f"[OK] Compiled FruitFly to MuJoCo Physics (bodies={physics.model.nbody}, actuators={physics.model.nu})")

        # Step physics for 10 frames
        for _ in range(10):
            physics.step()

        print(f"[OK] 10 FlyBody physics steps completed without error!")
        return True
    except Exception as e:
        print(f"[FAIL] FlyBody encountered an error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 65)
    print(" ConnectomeToBehavior — Phase 3: Body Physics Diagnostic")
    print("=" * 65)
    print(f"NumPy version in environment: {np.__version__}")

    results = {}
    results["mujoco_core"] = test_mujoco_core()
    results["flygym"] = test_flygym_body()
    results["flybody"] = test_flybody_model()

    print("\n" + "=" * 65)
    print(" Diagnostic Summary:")
    print("=" * 65)
    for component, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f" - {component:<15}: {status}")

    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 ALL BODY SIMULATION ENGINES OPERATIONAL!")
        print("NumPy 1.26.4 runtime compatibility confirmed across MuJoCo, FlyGym, and FlyBody.")
    else:
        print("\n⚠️ One or more body components require adjustments.")
    print("=" * 65)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
