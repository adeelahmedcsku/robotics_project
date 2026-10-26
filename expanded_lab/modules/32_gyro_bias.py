"""Gyroscope bias calibration and attitude drift. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(23)
    dt = 0.01
    T = 10.0
    n = int(T / dt)
    calibration = int(p["calibration_seconds"] / dt)
    calibration = max(2, calibration)
    bias = 0.015
    sigma = 0.01
    stationary = bias + rng.normal(0, sigma, calibration)
    estimated = stationary.mean()
    truth = 0.2 * np.ones(n)
    measured = truth + bias + rng.normal(0, sigma, n)
    raw = np.cumsum(measured) * dt
    corrected = np.cumsum(measured - estimated) * dt
    expected = np.cumsum(truth) * dt
    metrics = dict(
        estimated_bias_rad_s=estimated,
        bias_error_rad_s=estimated - bias,
        raw_final_angle_error_rad=raw[-1] - expected[-1],
        corrected_final_angle_error_rad=corrected[-1] - expected[-1],
        corrected_angle_rmse_rad=np.sqrt(np.mean((corrected - expected) ** 2)),
    )
    derivation = [
        f"Collect {calibration} stationary samples at 100 Hz.",
        f"True injected bias is {bias:g} rad/s; estimated bias is {estimated:.8f} rad/s.",
        f"Integrate a 0.2 rad/s motion for {T:g} s.",
        f"Raw final attitude error is {raw[-1]-expected[-1]:.8f} rad.",
        f"After bias correction, final error is {corrected[-1]-expected[-1]:.8f} rad.",
    ]
    notes = [
        "This calibration assumes zero true angular velocity and constant bias during both intervals.",
        "Longer averaging reduces random estimation error but cannot remove a temperature-dependent bias change.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"calibration_seconds": 2.0}
    parameters["calibration_seconds"] = [0.1, 0.25, 0.5, 1.0, 2.0, 5.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
