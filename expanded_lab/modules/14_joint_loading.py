"""Gravity, acceleration and joint-load budgeting. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    l, mp, mr = p["length"], p["payload"], p["rod_mass"]
    q = np.deg2rad(p["angle_deg"])
    alpha = p["acceleration"]
    gravity = (mp * 9.81 * l + mr * 9.81 * l / 2) * np.cos(q)
    inertia = mp * l * l + mr * l * l / 3
    dynamic = inertia * alpha
    friction = 0.3
    total = gravity + dynamic + friction
    metrics = dict(
        gravity_Nm=gravity,
        inertia_kg_m2=inertia,
        acceleration_Nm=dynamic,
        total_required_Nm=total,
        gravity_fraction=gravity / total,
    )
    derivation = [
        f"Payload mass {mp:g} kg acts at {l:g} m; rod COM acts at {l/2:g} m.",
        f'At angle {p["angle_deg"]:g} degrees, gravity torque is {gravity:.6f} Nm.',
        f"Total modeled rotational inertia is {inertia:.6f} kg*m^2.",
        f"Acceleration {alpha:g} rad/s^2 adds {dynamic:.6f} Nm.",
        f"Add 0.3 Nm illustrative friction: total demand is {total:.6f} Nm.",
    ]
    notes = [
        "The load budget separates assumptions so the dominant contribution can be identified.",
        "This one-axis model excludes impact, gear reflected inertia, cable forces and multi-link coupling.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {
        "length": 0.25,
        "payload": 2.0,
        "rod_mass": 1.0,
        "angle_deg": 20.0,
        "acceleration": 3.0,
    }
    parameters["acceleration"] = [0.0, 1.0, 2.0, 3.0, 6.0, 12.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
