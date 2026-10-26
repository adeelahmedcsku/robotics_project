"""Complementary attitude filtering and acceleration contamination. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(29)
    dt = 0.01
    t = np.arange(0, 8, dt)
    truth = 0.15 * np.sin(2 * np.pi * 0.3 * t)
    rate = 0.15 * 2 * np.pi * 0.3 * np.cos(2 * np.pi * 0.3 * t)
    gyro = rate + 0.01 + rng.normal(0, 0.005, len(t))
    accel_angle = truth + rng.normal(0, 0.02, len(t))
    accel_angle[(t > 3) & (t < 4)] += 0.15
    tau = p["time_constant"]
    alpha = tau / (tau + dt)
    estimate = 0.0
    history = []
    for g, a in zip(gyro, accel_angle):
        estimate = alpha * (estimate + g * dt) + (1 - alpha) * a
        history.append(estimate)
    error = np.array(history) - truth
    clean = (t < 3) | (t > 5)
    metrics = dict(
        alpha=alpha,
        total_rmse_rad=np.sqrt(np.mean(error**2)),
        clean_rmse_rad=np.sqrt(np.mean(error[clean] ** 2)),
        contamination_peak_error_rad=np.max(abs(error[(t > 3) & (t < 4)])),
        final_error_rad=error[-1],
    )
    derivation = [
        f"Time constant {tau:g} s with dt=0.01 s gives alpha={alpha:.8f}.",
        "True roll is a 0.15 rad, 0.3 Hz sinusoid; gyro bias is 0.01 rad/s.",
        "Contaminate the accelerometer roll proxy by +0.15 rad between three and four seconds.",
        f'Whole-record RMSE is {metrics["total_rmse_rad"]:.6f} rad; clean-segment RMSE is {metrics["clean_rmse_rad"]:.6f} rad.',
        f'Peak error during contamination is {metrics["contamination_peak_error_rad"]:.6f} rad.',
    ]
    notes = [
        "The synthetic accelerometer-angle disturbance represents a limitation of gravity-based attitude correction during motion.",
        "A production estimator needs measurement validity checks and a consistent three-dimensional orientation representation.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"time_constant": 0.5}
    parameters["time_constant"] = [0.05, 0.1, 0.25, 0.5, 1.0, 2.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
