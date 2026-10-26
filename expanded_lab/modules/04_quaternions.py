"""Unit quaternions, sign equivalence and incremental attitude. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def multiply(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.array(
        [
            aw * bw - ax * bx - ay * by - az * bz,
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
        ]
    )


def experiment(p):
    dt, duration, rate = p["dt"], p["duration"], p["rate"]
    n = round(duration / dt)
    actual = n * dt
    inc = np.array([np.cos(rate * dt / 2), 0.0, 0.0, np.sin(rate * dt / 2)])
    q = np.array([1.0, 0.0, 0.0, 0.0])
    for _ in range(n):
        q = multiply(q, inc)
        q /= np.linalg.norm(q)
    exact = np.array(
        [np.cos(rate * actual / 2), 0.0, 0.0, np.sin(rate * actual / 2)]
    )
    error = 2 * np.arccos(np.clip(abs(q @ exact), 0, 1))
    same = 2 * np.arccos(np.clip(abs(q @ (-q)), 0, 1))
    assert np.isclose(np.linalg.norm(q), 1)
    metrics = dict(
        final_w=q[0],
        final_z=q[3],
        angle_error_rad=error,
        sign_equivalence_error_rad=same,
        actual_duration_s=actual,
    )
    derivation = [
        f"One increment rotates {rate*dt:.6f} rad about local z.",
        f"Apply {n} increments, giving actual duration {actual:.6f} s.",
        f"The final scalar-first quaternion is {q.tolist()}.",
        f"Use the absolute dot product for sign-invariant error: {error:.9f} rad.",
        f"Compare q with -q using the same metric: {same:.9f} rad.",
    ]
    notes = [
        "Constant-axis exact increments are a reference case, not a full noisy IMU estimator.",
        "Changing the multiplication side changes whether increments are interpreted in body or world coordinates.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"dt": 0.01, "duration": 2.0, "rate": 0.7}
    parameters["dt"] = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
