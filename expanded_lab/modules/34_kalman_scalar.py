"""Scalar Kalman filtering and covariance interpretation. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(31)
    n = 500
    Q = 0.0001
    true_R = 0.01
    truth = np.cumsum(rng.normal(0, np.sqrt(Q), n))
    measurements = truth + rng.normal(0, np.sqrt(true_R), n)
    x = 0.0
    P = 1.0
    errors = []
    variances = []
    gains = []
    assumed_R = p["assumed_measurement_variance"]
    for z, actual in zip(measurements, truth):
        prediction = P + Q
        K = prediction / (prediction + assumed_R)
        x += K * (z - x)
        P = (1 - K) ** 2 * prediction + K * K * assumed_R
        errors.append(x - actual)
        variances.append(P)
        gains.append(K)
    errors = np.array(errors)
    variances = np.array(variances)
    metrics = dict(
        estimate_rmse=np.sqrt(np.mean(errors**2)),
        reported_std=np.sqrt(np.mean(variances)),
        final_gain=gains[-1],
        empirical_two_sigma_coverage=np.mean(
            abs(errors) <= 2 * np.sqrt(variances)
        ),
    )
    derivation = [
        f"True process variance per step is {Q:g}; true measurement variance is {true_R:g}.",
        f"The filter assumes measurement variance {assumed_R:g}.",
        "Predict variance, calculate gain, correct state, then use Joseph-form scalar covariance update.",
        f'Empirical RMSE is {metrics["estimate_rmse"]:.6f}; reported RMS standard deviation is {metrics["reported_std"]:.6f}.',
        f'Two-sigma empirical coverage is {metrics["empirical_two_sigma_coverage"]:.6f}.',
    ]
    notes = [
        "Coverage is a diagnostic under this synthetic model, not a universal confidence guarantee.",
        "Underestimating measurement variance can increase trust in noisy data and make the reported covariance overconfident.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"assumed_measurement_variance": 0.01}
    parameters["assumed_measurement_variance"] = [
        0.0001,
        0.001,
        0.005,
        0.01,
        0.05,
        0.1,
    ][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
