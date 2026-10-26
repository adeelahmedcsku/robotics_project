"""First-order thermal models and duty-cycle limits. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    power, R, C = p["loss_power"], p["thermal_resistance"], p["thermal_capacity"]
    duration, ambient = p["duration"], 25.0
    rise = power * R * (1 - np.exp(-duration / (R * C)))
    final = ambient + rise
    threshold = 70.0
    steady = ambient + power * R
    if steady > threshold:
        crossing = -R * C * np.log(1 - (threshold - ambient) / (power * R))
    else:
        crossing = -1.0
    metrics = dict(
        final_temperature_C=final,
        steady_temperature_C=steady,
        time_constant_s=R * C,
        screening_margin_C=threshold - final,
        threshold_crossing_s=crossing,
    )
    derivation = [
        f"Assume loss power {power:g} W, Rth={R:g} K/W and Cth={C:g} J/K.",
        f"The thermal time constant is {R*C:.6f} s.",
        f"After {duration:g} s, temperature rise is {rise:.6f} K above 25 C ambient.",
        f"Predicted final temperature is {final:.6f} C and steady temperature is {steady:.6f} C.",
        f"The 70 C teaching threshold crossing time is {crossing:.6f} s; -1 means no crossing in the ideal constant-loss model.",
    ]
    notes = [
        "The 70 C threshold is an exercise parameter, not a motor or material rating.",
        "Actual winding, housing, drive and gearbox temperatures have different dynamics and measurement locations.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {
        "loss_power": 20.0,
        "thermal_resistance": 2.0,
        "thermal_capacity": 100.0,
        "duration": 300.0,
    }
    parameters["loss_power"] = [5.0, 10.0, 15.0, 20.0, 30.0, 40.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
