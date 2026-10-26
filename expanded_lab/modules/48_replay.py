"""Offline replay, action parity and fault localization. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(61)
    obs = rng.normal(0, 1, (1000, 4))
    W = np.array([[0.2, -0.1, 0.3, 0.4], [-0.3, 0.2, 0.1, -0.2]])
    bias = np.array([0.05, -0.02])
    reference = np.tanh(obs @ W.T + bias)
    migrated = obs.copy()
    migrated[:, 2] *= p["scale_error_factor"]
    candidate = np.tanh(migrated @ W.T + bias)
    difference = candidate - reference
    per_sample = np.max(abs(difference), axis=1)
    metrics = dict(
        action_rmse=np.sqrt(np.mean(difference**2)),
        maximum_absolute_action_error=np.max(abs(difference)),
        mismatch_fraction=np.mean(per_sample > 1e-5),
        mean_action_magnitude=np.mean(abs(reference)),
    )
    derivation = [
        "Generate 1000 four-dimensional observations from a fixed seeded distribution.",
        f'The candidate preprocessing multiplies field 2 by {p["scale_error_factor"]:g}.',
        "Run the same tanh actor for reference and candidate pipelines.",
        f'Action RMSE is {metrics["action_rmse"]:.8f}; maximum disagreement is {metrics["maximum_absolute_action_error"]:.8f}.',
        f'Fraction exceeding 1e-5 action error is {metrics["mismatch_fraction"]:.6f}.',
    ]
    notes = [
        "The replay distribution is synthetic; physical logs and edge cases must be included before deployment.",
        "Exact inference parity does not validate the policy behavior or the physical actuator mapping.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"scale_error_factor": 1.0}
    parameters["scale_error_factor"] = [0.5, 0.9, 0.99, 1.0, 1.01, 1.1][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
