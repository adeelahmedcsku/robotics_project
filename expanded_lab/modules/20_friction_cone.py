"""Friction cones, slip feasibility and contact margins. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    mass, mu, acc = p["mass"], p["mu"], p["acceleration"]
    normal = mass * 9.81 * p["supported_fraction"]
    required = mass * acc
    capacity = mu * normal
    margin = capacity - abs(required)
    angle = np.arctan(mu)
    utilization = abs(required) / capacity
    metrics = dict(
        normal_force_N=normal,
        tangential_required_N=required,
        friction_capacity_N=capacity,
        force_margin_N=margin,
        utilization=utilization,
        cone_half_angle_rad=angle,
    )
    derivation = [
        f"The modeled normal force is {normal:.6f} N.",
        f"Acceleration {acc:g} m/s^2 requires horizontal force {required:.6f} N.",
        f"At mu={mu:g}, Coulomb capacity is {capacity:.6f} N.",
        f"Margin is {margin:.6f} N and utilization is {utilization:.6f}.",
        f"The friction-cone half angle is atan(mu)={angle:.6f} rad.",
    ]
    notes = [
        (
            "The requested force is inside the modeled friction bound."
            if margin >= 0
            else "The requested force exceeds the modeled friction capacity; a controller must reduce demand or change support."
        ),
        "This static feasibility check excludes torsional friction, impact, compliance and changing normal force.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {
        "mass": 10.0,
        "mu": 0.6,
        "acceleration": 2.0,
        "supported_fraction": 1.0,
    }
    parameters["mu"] = [0.1, 0.2, 0.3, 0.4, 0.6, 0.8][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
