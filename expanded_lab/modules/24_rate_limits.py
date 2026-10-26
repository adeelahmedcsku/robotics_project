"""Position envelopes, slew limits and stopping distance. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    vmax, dt, delay = p["speed"], p["dt"], p["delay"]
    brake = p["deceleration"]
    q = 0.0
    request = 0.5
    trace = []
    for _ in range(500):
        q += np.clip(request - q, -vmax * dt, vmax * dt)
        trace.append(q)
    stopping = vmax * delay + vmax * vmax / (2 * brake)
    margin = 0.12 - stopping
    metrics = dict(
        final_target_rad=q,
        ideal_stopping_distance_rad=stopping,
        remaining_travel_margin_rad=margin,
        per_update_step_rad=vmax * dt,
        time_to_target_s=request / vmax,
    )
    derivation = [
        f"At vmax={vmax:g} rad/s and dt={dt:g} s, each target increment is capped at {vmax*dt:.6f} rad.",
        f"Reaction delay contributes {vmax*delay:.6f} rad of travel.",
        f"Ideal constant deceleration {brake:g} rad/s^2 contributes {vmax*vmax/(2*brake):.6f} rad.",
        f"Total screened stopping distance is {stopping:.6f} rad.",
        f"With 0.12 rad assumed remaining travel, margin is {margin:.6f} rad.",
    ]
    notes = [
        (
            "The ideal calculation leaves positive travel margin."
            if margin >= 0
            else "The ideal calculation already exceeds available travel; reduce speed or increase clearance before considering uncertainty."
        ),
        "Load, control delay, brake authority and power-loss behavior must be measured for a physical stopping claim.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"speed": 0.4, "dt": 0.01, "delay": 0.05, "deceleration": 2.0}
    parameters["speed"] = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
