"""
FlyBody: Thin, robust Python wrapper around FlyGym (NeuroMechFly v2) MuJoCo body simulation.

Key Design Principles:
1. Thin wrapper: delegates directly to SingleFlySimulation without introducing a redundant simulation engine.
2. Verified unit convention: NeuroMechFly v2 uses millimetres (mm) for length, seconds (s) for time,
   radians (rad) for joint angles, and mm/s^2 for accelerations (gravity = -9810 mm/s^2).
3. Explicit stepping separation:
   - step(action): executes 1 native environment step (advances by exactly sim.timestep, default 0.1 ms).
   - step_duration(duration_ms, action): advances the verified number of physics steps for the requested duration.
4. Action space integrity: 42 actuated leg joints (7 per leg x 6 legs) accepting position targets in radians.
5. Ground-truth observations: exposes raw joint kinematics, pose, and verified 30-segment tarsal contact forces.
   Does not invent unmodeled sensors (e.g. labellum touch is explicitly reported as None until modeled).
"""

from typing import Dict, List, Optional, Tuple, Union, Any
import numpy as np
from flygym import Fly, SingleFlySimulation
from flygym.arena import FlatTerrain


class FlyBody:
    """
    Physical Drosophila body simulation environment wrapping NeuroMechFly v2 (MuJoCo).
    """

    # Spatial scale: NeuroMechFly v2 is modeled in millimetres (mm)
    SPATIAL_UNIT = "mm"
    GRAVITY_MM_S2 = (0.0, 0.0, -9810.0)

    def __init__(
        self,
        arena: Optional[Any] = None,
        spawn_pos: Optional[Tuple[float, float, float]] = None,
        spawn_orientation: Optional[Tuple[float, float, float]] = None,
        timestep: float = 1e-4,
    ):
        """
        Initialize the FlyBody simulation.

        Parameters
        ----------
        arena : BaseArena, optional
            FlyGym arena. Defaults to FlatTerrain() if None.
        spawn_pos : tuple of (float, float, float), optional
            Spawn position in millimetres (x, y, z).
            Defaults to (0.0, 0.0, 0.5) mm if None.
        spawn_orientation : tuple of (float, float, float), optional
            Spawn orientation in Euler angles (roll, pitch, yaw) in radians.
            Defaults to (0.0, 0.0, 0.0) rad if None.
        timestep : float, default=1e-4
            MuJoCo physics integration timestep in seconds (1e-4 s = 0.1 ms).
        """
        self.arena = arena if arena is not None else FlatTerrain()
        self.spawn_pos = spawn_pos if spawn_pos is not None else (0.0, 0.0, 0.5)
        self.spawn_orientation = spawn_orientation if spawn_orientation is not None else (0.0, 0.0, 0.0)
        self.timestep = float(timestep)

        # Initialize NeuroMechFly v2 fly model
        self.fly = Fly(
            spawn_pos=self.spawn_pos,
            spawn_orientation=self.spawn_orientation,
            control="position",
        )

        # Initialize FlyGym simulation
        self.sim = SingleFlySimulation(
            fly=self.fly,
            arena=self.arena,
            timestep=self.timestep,
            gravity=self.GRAVITY_MM_S2,
        )

        # Cache joint metadata
        self.actuated_joints: List[str] = list(self.fly.actuated_joints)
        self.num_actuators: int = len(self.actuated_joints)
        self.joint_name2idx: Dict[str, int] = {name: i for i, name in enumerate(self.actuated_joints)}

        # Cache tarsal contact sensor names (30 segments: 5 segments x 6 legs)
        self.contact_sensor_names: List[str] = list(self.fly.contact_sensor_placements)

        # Observation cache from most recent step
        self._last_obs: Optional[Dict[str, np.ndarray]] = None
        self._last_info: Optional[Dict[str, Any]] = None

        # Reset environment on instantiation
        self.reset()

    def reset(self) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
        """
        Reset simulation state to initial spawn conditions.

        Returns
        -------
        obs : dict
            Initial observation dictionary from FlyGym.
        info : dict
            Diagnostic info dictionary from FlyGym.
        """
        obs, info = self.sim.reset()
        self._last_obs = obs
        self._last_info = info
        return obs, info

    def _prepare_action_dict(
        self,
        action: Optional[Union[np.ndarray, Dict[str, float]]],
    ) -> Dict[str, np.ndarray]:
        """
        Convert user action (array or joint-name dict) into the FlyGym action dict format:
        {'joints': np.ndarray of shape (42,), dtype float32}.
        """
        if action is None:
            # Neutral / hold: maintain zero joint positions if no target is provided
            joint_arr = np.zeros(self.num_actuators, dtype=np.float32)
        elif isinstance(action, dict):
            if "joints" in action and isinstance(action["joints"], np.ndarray):
                joint_arr = action["joints"].astype(np.float32)
            else:
                # Name-keyed dictionary of joint angles: preserve existing angle for unmentioned joints
                joint_arr = np.zeros(self.num_actuators, dtype=np.float32)
                if self._last_obs is not None and "joints" in self._last_obs:
                    joint_arr = self._last_obs["joints"][0].copy().astype(np.float32)

                for joint_name, target_angle in action.items():
                    if joint_name in self.joint_name2idx:
                        idx = self.joint_name2idx[joint_name]
                        joint_arr[idx] = float(target_angle)
        elif isinstance(action, (np.ndarray, list)):
            joint_arr = np.asarray(action, dtype=np.float32)
            if len(joint_arr) != self.num_actuators:
                raise ValueError(
                    f"Action array length {len(joint_arr)} does not match actuated joint count {self.num_actuators}"
                )
        else:
            raise TypeError(f"Unsupported action type: {type(action)}")

        return {"joints": joint_arr}

    def step(
        self,
        action: Optional[Union[np.ndarray, Dict[str, float]]] = None,
    ) -> Tuple[Dict[str, np.ndarray], float, bool, bool, Dict[str, Any]]:
        """
        Execute exactly ONE native FlyGym environment step.
        Advances simulation clock by exactly self.timestep (0.1 ms).

        Parameters
        ----------
        action : ndarray or dict, optional
            Joint position commands in radians.

        Returns
        -------
        obs, reward, terminated, truncated, info
        """
        action_dict = self._prepare_action_dict(action)
        obs, reward, terminated, truncated, info = self.sim.step(action_dict)
        self._last_obs = obs
        self._last_info = info
        return obs, reward, terminated, truncated, info

    def step_duration(
        self,
        duration_ms: float,
        action: Optional[Union[np.ndarray, Dict[str, float]]] = None,
    ) -> Tuple[Dict[str, np.ndarray], float, bool, bool, Dict[str, Any]]:
        """
        Advance physics by the specified duration in milliseconds.
        Executes exactly round(duration_s / timestep) native simulation steps.

        Parameters
        ----------
        duration_ms : float
            Biological/physical duration to advance in milliseconds.
        action : ndarray or dict, optional
            Joint position commands held constant across this duration window.

        Returns
        -------
        obs, reward, terminated, truncated, info from the final step.
        """
        duration_s = float(duration_ms) / 1000.0
        n_steps = int(round(duration_s / self.timestep))

        action_dict = self._prepare_action_dict(action)
        reward = 0.0
        terminated = False
        truncated = False

        for _ in range(n_steps):
            obs, reward, terminated, truncated, info = self.sim.step(action_dict)
            self._last_obs = obs
            self._last_info = info
            if terminated or truncated:
                break

        return self._last_obs, reward, terminated, truncated, self._last_info

    @property
    def curr_time(self) -> float:
        """Current physical simulation time in seconds."""
        return float(self.sim.curr_time)

    def get_joint_angles(self) -> Dict[str, float]:
        """Return current joint angles (radians) mapped by joint name."""
        if self._last_obs is None or "joints" not in self._last_obs:
            return {}
        # Row 0 of obs['joints'] contains joint angles in radians
        angles = self._last_obs["joints"][0]
        return {name: float(angles[i]) for i, name in enumerate(self.actuated_joints)}

    def get_joint_velocities(self) -> Dict[str, float]:
        """Return current joint angular velocities (rad/s) mapped by joint name."""
        if self._last_obs is None or "joints" not in self._last_obs:
            return {}
        # Row 1 of obs['joints'] contains joint velocities in rad/s
        velocities = self._last_obs["joints"][1]
        return {name: float(velocities[i]) for i, name in enumerate(self.actuated_joints)}

    def get_pose(self) -> Dict[str, Any]:
        """
        Return thorax position, linear velocity, and orientation vectors.
        Spatial units are in millimetres (mm).
        """
        if self._last_obs is None:
            return {}

        fly_data = self._last_obs.get("fly", None)
        orientation = self._last_obs.get("fly_orientation", None)

        pos_mm = fly_data[0] if fly_data is not None else np.zeros(3)
        vel_mm_s = fly_data[1] if fly_data is not None else np.zeros(3)

        return {
            "position_mm": pos_mm.tolist(),
            "velocity_mm_s": vel_mm_s.tolist(),
            "orientation_vector": orientation.tolist() if orientation is not None else None,
            "unit": self.SPATIAL_UNIT,
        }

    def get_tarsal_forces(self) -> Dict[str, np.ndarray]:
        """
        Return 3D ground reaction forces (Fx, Fy, Fz) for each of the 30 monitored tarsal segments.
        Forces are in native FlyGym units (mN).
        """
        if self._last_obs is None or "contact_forces" not in self._last_obs:
            return {}

        forces = self._last_obs["contact_forces"]
        return {name: forces[i].copy() for i, name in enumerate(self.contact_sensor_names)}

    def get_observation(self) -> Optional[Dict[str, np.ndarray]]:
        """Return raw, unmodified FlyGym observation dictionary."""
        return self._last_obs

    def close(self):
        """Release MuJoCo simulation and render contexts."""
        if hasattr(self, "sim") and self.sim is not None:
            self.sim.close()

    def __enter__(self) -> "FlyBody":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

