"""Streaming normalization, numerical stability and evaluation leakage. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def welford(samples):
    n = 0
    mean = 0.0
    M2 = 0.0
    for value in samples:
        n += 1
        delta = value - mean
        mean += delta / n
        M2 += delta * (value - mean)
    return mean, M2 / (n - 1)


def experiment(p):
    rng = np.random.default_rng(71)
    training = rng.normal(0, 1, 5000)
    testing = rng.normal(p["test_shift"], 1, 1000)
    mean, var = welford(training)
    frozen = (testing - mean) / np.sqrt(var + 1e-8)
    leaked_mean, leaked_var = welford(np.concatenate([training, testing]))
    leaked = (testing - leaked_mean) / np.sqrt(leaked_var + 1e-8)
    assert np.isclose(mean, training.mean())
    assert np.isclose(var, np.var(training, ddof=1))
    metrics = dict(
        training_mean=mean,
        training_variance=var,
        frozen_test_mean=np.mean(frozen),
        leaked_test_mean=np.mean(leaked),
        mean_normalized_disagreement=np.mean(abs(frozen - leaked)),
    )
    derivation = [
        "Estimate training statistics with 5,000 seeded samples using Welford updates.",
        f'The held-out distribution has mean shift {p["test_shift"]:g}.',
        f"Frozen normalizer produces test mean {np.mean(frozen):.6f}.",
        f"Updating statistics with evaluation data changes the test mean to {np.mean(leaked):.6f}.",
        f"Mean per-sample normalized disagreement is {np.mean(abs(frozen-leaked)):.6f}.",
    ]
    notes = [
        "A shifted test mean can be useful evidence of distribution shift; normalizing it away may hide the problem.",
        "Explicit online adaptation can be legitimate, but it is a different deployed algorithm requiring separate validation.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"test_shift": 1.0}
    parameters["test_shift"] = [0.0, 0.2, 0.5, 1.0, 2.0, 4.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
