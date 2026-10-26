"""Offline command-gate exercise. Not a certified hardware safety system."""
from dataclasses import dataclass
import numpy as np

@dataclass
class Gate:
    lower: np.ndarray
    upper: np.ndarray
    max_speed: float = .2
    timeout: float = .1
    last_sequence: int = -1
    fault: str = ''

    def validate(self, now, sent, sequence, target, measured, dt):
        target, measured = np.asarray(target), np.asarray(measured)
        checks = [
            (not np.isfinite([now, sent, dt]).all() or dt <= 0, 'invalid time'),
            (now-sent < 0 or now-sent > self.timeout, 'stale or future command'),
            (sequence <= self.last_sequence, 'replayed sequence'),
            (target.shape != self.lower.shape or measured.shape != target.shape,
             'shape mismatch')]
        for invalid, reason in checks:
            if invalid: self.fault = reason
        if not self.fault:
            if not np.isfinite(target).all() or not np.isfinite(measured).all():
                self.fault = 'nonfinite state'
            elif np.any(target < self.lower) or np.any(target > self.upper):
                self.fault = 'position limit'
            elif np.any(np.abs(target-measured) > self.max_speed*dt):
                self.fault = 'step envelope'
        if self.fault:
            raise RuntimeError(self.fault)
        self.last_sequence = sequence
        return target.copy()

if __name__ == '__main__':
    g = Gate(np.array([-1.]), np.array([1.]))
    print(g.validate(1., .99, 1, [.001], [0.], .01))
    try:
        g.validate(2., .99, 2, [.001], [0.], .01)
    except RuntimeError as e:
        print('Latched expected fault:', e)
