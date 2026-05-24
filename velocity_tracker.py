from dataclasses import dataclass
import numpy as np

@dataclass
class VelocityEstimate:
    raw_vel: np.ndarray
    filtered_vel: np.ndarray
    speed: float

class VelocityTracker:
    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha
        self.prev_pos = None
        self.prev_t = None
        self.filtered_vel = np.zeros(3, dtype=np.float64)

    def update(self, pos: np.ndarray, t: float):
        if self.prev_pos is None:
            self.prev_pos = pos
            self.prev_t = t
            return None

        dt = t - self.prev_t
        if dt <= 1e-6:
            return None

        raw_vel = (pos - self.prev_pos) / dt
        self.filtered_vel = self.alpha * raw_vel + (1.0 - self.alpha) * self.filtered_vel

        self.prev_pos = pos
        self.prev_t = t

        return VelocityEstimate(
            raw_vel=raw_vel,
            filtered_vel=self.filtered_vel.copy(),
            speed=float(np.linalg.norm(self.filtered_vel)),
        )    