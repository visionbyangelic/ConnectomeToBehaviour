import inspect
import numpy as np
from flygym import Fly, SingleFlySimulation
from flygym.arena import FlatTerrain

print("=== Fly init signature ===")
print(inspect.signature(Fly.__init__))

print("\n=== SingleFlySimulation init signature ===")
print(inspect.signature(SingleFlySimulation.__init__))

arena = FlatTerrain()
fly = Fly()
sim = SingleFlySimulation(fly=fly, arena=arena)
print("\n=== Default timestep ===")
print("sim.timestep:", sim.timestep)

obs, info = sim.reset()
print("\n=== Observation keys ===")
for k, v in obs.items():
    if isinstance(v, np.ndarray):
        print(f"obs['{k}']: shape={v.shape}, dtype={v.dtype}, min={v.min():.4f}, max={v.max():.4f}")
    else:
        print(f"obs['{k}']: {type(v)}")

print("\n=== Action space ===")
print("sim.action_space:", sim.action_space)

print("\n=== Actuated joints ===")
print("len(fly.actuated_joints):", len(fly.actuated_joints))
print("fly.actuated_joints[:6]:", fly.actuated_joints[:6])

print("\n=== Fly spawn_pos & units ===")
print("fly.spawn_pos:", getattr(fly, "spawn_pos", None))
print("fly.init_pose:", getattr(fly, "init_pose", None))

# Test stepping mechanism: does step advance sim.curr_time by sim.timestep?
t_before = sim.curr_time
action = {"joints": np.zeros(len(fly.actuated_joints))}
obs, reward, terminated, truncated, info = sim.step(action)
t_after = sim.curr_time
print("\n=== Step timing behavior ===")
print(f"sim.curr_time before: {t_before:.6f}s")
print(f"sim.curr_time after:  {t_after:.6f}s")
print(f"Delta: {t_after - t_before:.6f}s (sim.timestep: {sim.timestep:.6f}s)")
print(f"1 sim.step() advances exactly {((t_after - t_before)/sim.timestep):.1f} physics timesteps.")

sim.close()

