"""Position and velocity estimation with intermittent measurements. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(37)
    dt = 0.02
    t = np.arange(0, 6, dt)
    true_position = 0.2 * t + 0.02 * np.sin(t)
    true_velocity = 0.2 + 0.02 * np.cos(t)
    measurements = true_position + rng.normal(0, 0.01, len(t))
    F = np.array([[1.0, dt], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])
    Q = 0.01 * np.array([[dt**4 / 4, dt**3 / 2], [dt**3 / 2, dt**2]])
    x = np.zeros(2)
    P = np.eye(2)
    errors = []
    drop_errors = []
    dropout = p["dropout_seconds"]
    end = 2 + dropout
    for i, z in enumerate(measurements):
        x = F @ x
        P = F @ P @ F.T + Q
        missing = 2 <= t[i] < end
        if not missing:
            S = float((H @ P @ H.T)[0, 0] + 0.0001)
            K = P @ H.T / S
            x += K[:, 0] * (z - float((H @ x)[0]))
            A = np.eye(2) - K @ H
            P = A @ P @ A.T + K * 0.0001 @ K.T
        error = x[1] - true_velocity[i]
        errors.append(error)
        if missing:
            drop_errors.append(error)
        assert np.linalg.eigvalsh(P).min() > -1e-10
    metrics = dict(
        velocity_rmse_m_s=np.sqrt(np.mean(np.array(errors) ** 2)),
        dropout_velocity_rmse_m_s=(
            np.sqrt(np.mean(np.array(drop_errors) ** 2)) if drop_errors else 0.0
        ),
        final_velocity_m_s=x[1],
        final_position_std_m=np.sqrt(P[0, 0]),
        final_velocity_std_m_s=np.sqrt(P[1, 1]),
    )
    derivation = [
        f"Use a two-state position/velocity model with dt={dt:g} s.",
        f"Drop measurements from t=2 s to t={end:g} s.",
        "Predict through missing samples without applying fabricated corrections.",
        f'Whole-run speed RMSE is {metrics["velocity_rmse_m_s"]:.6f} m/s.',
        f'Dropout speed RMSE is {metrics["dropout_velocity_rmse_m_s"]:.6f} m/s; final speed estimate is {x[1]:.6f} m/s.',
    ]
    notes = [
        "The true motion contains a small acceleration that is not exactly constant velocity.",
        "The filter state and covariance are expressed in one dimension; full robot base estimation requires orientation and contact models.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"dropout_seconds": 0.5}
    parameters["dropout_seconds"] = [0.0, 0.1, 0.25, 0.5, 1.0, 2.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
