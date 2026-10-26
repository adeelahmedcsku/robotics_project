"""Second-order joint dynamics and PD tuning. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    I, kp, kd = p["inertia"], p["kp"], p["kd"]
    b = 0.1
    dt = 0.001
    target = 0.1
    q = 0.0
    v = 0.0
    positions = []
    for _ in range(3000):
        torque = kp * (target - q) - kd * v
        acceleration = (torque - b * v) / I
        v += dt * acceleration
        q += dt * v
        positions.append(q)
    positions = np.array(positions)
    wn = np.sqrt(kp / I)
    zeta = (b + kd) / (2 * np.sqrt(kp * I))
    overshoot = max(0.0, positions.max() - target) / target
    metrics = dict(
        natural_frequency_rad_s=wn,
        damping_ratio=zeta,
        overshoot_fraction=overshoot,
        final_error_rad=target - q,
        trajectory_rmse_rad=np.sqrt(np.mean((positions - target) ** 2)),
    )
    derivation = [
        f"Joint inertia is {I:g} kg*m^2; Kp={kp:g} Nm/rad; Kd={kd:g} Nm*s/rad.",
        f"The implied natural frequency is {wn:.6f} rad/s and damping ratio is {zeta:.6f}.",
        "Apply a 0.1 rad target and integrate semi-implicitly at 1 ms for three seconds.",
        f"Peak position is {positions.max():.6f} rad, producing overshoot fraction {overshoot:.6f}.",
        f'Final tracking error is {target-q:.8f} rad; trajectory RMSE is {metrics["trajectory_rmse_rad"]:.6f} rad.',
    ]
    notes = [
        (
            "This model is underdamped."
            if zeta < 1
            else "This model is critically damped or overdamped."
        ),
        "There is no torque saturation, delay, gravity or contact in this identification-friendly reference.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"inertia": 0.08, "kp": 20.0, "kd": 2.0}
    parameters["kd"] = [0.1, 0.5, 1.0, 2.0, 4.0, 8.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
