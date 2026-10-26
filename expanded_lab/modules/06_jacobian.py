"""Finite-difference Jacobians and derivative verification. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def fk(q):
    a, b = q
    return np.array(
        [
            0.3 * np.cos(a) + 0.2 * np.cos(a + b),
            0.3 * np.sin(a) + 0.2 * np.sin(a + b),
        ]
    )


def experiment(p):
    q = np.array([0.4, -0.7])
    eps = p["epsilon"]
    a, b = q
    J = np.array(
        [
            [-0.3 * np.sin(a) - 0.2 * np.sin(a + b), -0.2 * np.sin(a + b)],
            [0.3 * np.cos(a) + 0.2 * np.cos(a + b), 0.2 * np.cos(a + b)],
        ]
    )
    estimated = np.zeros((2, 2))
    for j in range(2):
        delta = np.zeros(2)
        delta[j] = eps
        estimated[:, j] = (fk(q + delta) - fk(q - delta)) / (2 * eps)
    error = np.linalg.norm(estimated - J)
    velocity = J @ np.array([0.1, -0.2])
    metrics = dict(
        derivative_error=error,
        velocity_x_m_s=velocity[0],
        velocity_y_m_s=velocity[1],
        jacobian_condition=np.linalg.cond(J),
    )
    derivation = [
        f"At joint pose {q.tolist()} rad, endpoint is {fk(q).tolist()} m.",
        f"Use symmetric perturbations of {eps:.3e} rad for each joint.",
        f"The analytic first column is {J[:,0].tolist()} m/rad.",
        f"The estimated first column is {estimated[:,0].tolist()} m/rad.",
        f"Full matrix residual norm is {error:.3e}; predicted endpoint velocity is {velocity.tolist()} m/s.",
    ]
    notes = [
        "Reducing epsilon eventually makes floating-point cancellation important.",
        "Compare columns in the same frame and at the same configuration; otherwise the residual is not a derivative test.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"epsilon": 1e-05}
    parameters["epsilon"] = [0.1, 0.01, 0.001, 1e-05, 1e-07, 1e-09][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
