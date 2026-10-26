"""Closed-form two-link inverse kinematics and branch choice. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    l1, l2 = 0.3, 0.2
    x, y = p["target_x"], p["target_y"]
    cosine = (x * x + y * y - l1 * l1 - l2 * l2) / (2 * l1 * l2)
    reachable = abs(cosine) <= 1
    q2 = np.arccos(np.clip(cosine, -1, 1))
    q1 = np.arctan2(y, x) - np.arctan2(l2 * np.sin(q2), l1 + l2 * np.cos(q2))
    predicted = np.array(
        [
            l1 * np.cos(q1) + l2 * np.cos(q1 + q2),
            l1 * np.sin(q1) + l2 * np.sin(q1 + q2),
        ]
    )
    residual = np.linalg.norm(predicted - [x, y])
    metrics = dict(
        reachable=float(reachable),
        q1_rad=q1,
        q2_rad=q2,
        residual_m=residual,
        cosine_raw=cosine,
    )
    derivation = [
        f"Target is ({x:g},{y:g}) m with link lengths {l1:g},{l2:g} m.",
        f"Compute the raw elbow cosine {cosine:.8f}; reachability is {reachable}.",
        f"The positive-elbow candidate is q2={q2:.8f} rad.",
        f"Compute shoulder correction to obtain q1={q1:.8f} rad.",
        f"Forward kinematics returns {predicted.tolist()} m, with residual {residual:.8f} m.",
    ]
    notes = [
        (
            "The target is geometrically reachable; joint limits and collisions still require separate checks."
            if reachable
            else "The clipped candidate is only a nearest-boundary diagnostic. It must not be returned as a successful IK solution."
        ),
        "Negating q2 and recomputing q1 gives the other elbow branch when the target is not singular.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"target_x": 0.35, "target_y": 0.1}
    parameters["target_x"] = [0.05, 0.1, 0.2, 0.35, 0.48, 0.6][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
