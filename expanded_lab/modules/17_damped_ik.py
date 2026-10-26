"""Singular values and damped least-squares motion. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    q1 = 0.2
    q2 = p["elbow"]
    lam = p["damping"]
    J = np.array(
        [
            [-0.3 * np.sin(q1) - 0.2 * np.sin(q1 + q2), -0.2 * np.sin(q1 + q2)],
            [0.3 * np.cos(q1) + 0.2 * np.cos(q1 + q2), 0.2 * np.cos(q1 + q2)],
        ]
    )
    error = np.array([0.01, 0.0])
    singular = np.linalg.svd(J, compute_uv=False)
    dq = J.T @ np.linalg.solve(J @ J.T + lam * lam * np.eye(2), error)
    predicted = J @ dq
    metrics = dict(
        min_singular_value=singular[-1],
        joint_step_norm_rad=np.linalg.norm(dq),
        predicted_residual_m=np.linalg.norm(error - predicted),
        max_joint_step_rad=np.max(np.abs(dq)),
    )
    derivation = [
        f"Use pose q1={q1:g}, q2={q2:g} rad and Cartesian request {error.tolist()} m.",
        f"The Jacobian singular values are {singular.tolist()}.",
        f"Choose damping lambda={lam:g} and solve the regularized 2x2 system.",
        f"The joint update is {dq.tolist()} rad.",
        f"Linearized achieved displacement is {predicted.tolist()} m; residual is {np.linalg.norm(error-predicted):.8f} m.",
    ]
    notes = [
        "The linearized prediction is only valid for sufficiently small joint updates; recompute nonlinear FK after each iteration.",
        "A larger damping value can improve numerical behavior while deliberately leaving more task error.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"elbow": 0.03, "damping": 0.01}
    parameters["damping"] = [0.0001, 0.001, 0.005, 0.01, 0.03, 0.1][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
