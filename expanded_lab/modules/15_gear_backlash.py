"""Gear ratio, reflected inertia and backlash dead zones. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    ratio = p["ratio"]
    J = p["rotor_inertia"]
    gap = p["backlash"]
    t = np.linspace(0, 4, 1001)
    desired = 0.1 * np.sin(2 * np.pi * 0.5 * t)
    actual = np.zeros_like(desired)
    for i in range(1, len(t)):
        previous = actual[i - 1]
        actual[i] = np.clip(previous, desired[i] - gap / 2, desired[i] + gap / 2)
    error = desired - actual
    metrics = dict(
        reflected_inertia_kg_m2=J * ratio**2,
        tracking_rmse_rad=np.sqrt(np.mean(error**2)),
        peak_lost_motion_rad=np.max(np.abs(error)),
        transmitted_range_rad=np.ptp(actual),
    )
    derivation = [
        f"Rotor inertia {J:.3e} kg*m^2 is reflected through ratio {ratio:g}.",
        f"Output-equivalent inertia is {J*ratio**2:.8f} kg*m^2.",
        f"The commanded output trajectory has 0.1 rad amplitude and 0.5 Hz frequency.",
        f"Apply a total backlash gap of {gap:.6f} rad with a stateful play operator.",
        f"The resulting RMSE is {np.sqrt(np.mean(error**2)):.6f} rad; peak error is {np.max(np.abs(error)):.6f} rad.",
    ]
    notes = [
        "A stateful dead zone creates hysteresis; adding independent Gaussian noise would model a different phenomenon.",
        "The play model excludes stiffness, friction and load-dependent tooth contact.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"ratio": 36.0, "rotor_inertia": 2e-05, "backlash": 0.01}
    parameters["backlash"] = [0.0, 0.002, 0.005, 0.01, 0.02, 0.04][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
