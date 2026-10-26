"""Minimum-jerk trajectories and duration constraints. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    T, delta = p["duration"], p["excursion"]
    r = np.linspace(0, 1, 1001)
    s = 10 * r**3 - 15 * r**4 + 6 * r**5
    ds = 30 * r**2 - 60 * r**3 + 30 * r**4
    dds = 60 * r - 180 * r**2 + 120 * r**3
    ddds = 60 - 360 * r + 360 * r**2
    q = delta * s
    v = delta * ds / T
    a = delta * dds / T**2
    j = delta * ddds / T**3
    assert np.isclose(q[0], 0) and np.isclose(q[-1], delta)
    assert np.allclose(v[[0, -1]], 0) and np.allclose(a[[0, -1]], 0)
    metrics = dict(
        peak_speed_rad_s=np.max(abs(v)),
        peak_acceleration_rad_s2=np.max(abs(a)),
        peak_jerk_rad_s3=np.max(abs(j)),
        final_position_rad=q[-1],
        speed_limit_margin_rad_s=0.5 - np.max(abs(v)),
    )
    derivation = [
        f"Move through delta={delta:g} rad over duration T={T:g} s.",
        "Evaluate the polynomial and its first three derivatives at 1001 normalized positions.",
        f"Peak speed is {np.max(abs(v)):.6f} rad/s.",
        f"Peak acceleration is {np.max(abs(a)):.6f} rad/s^2; peak jerk is {np.max(abs(j)):.6f} rad/s^3.",
        f'Against an illustrative 0.5 rad/s speed envelope, margin is {metrics["speed_limit_margin_rad_s"]:.6f} rad/s.',
    ]
    notes = [
        "The speed envelope is a teaching assumption and must not be substituted for a released actuator limit.",
        "Zero endpoint velocity and acceleration do not ensure the controller can supply the required intermediate torque.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"duration": 2.0, "excursion": 0.4}
    parameters["duration"] = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
