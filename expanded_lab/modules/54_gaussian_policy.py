"""Gaussian policies, action limits and saturation probability. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(67)
    mu = p["mean"]
    sigma = p["std"]
    raw = rng.normal(mu, sigma, 20000)
    bounded = np.clip(raw, -1, 1)
    entropy = 0.5 * np.log(2 * np.pi * np.e * sigma * sigma)
    metrics = dict(
        clipped_fraction=np.mean(abs(raw) > 1),
        raw_mean=np.mean(raw),
        bounded_mean=np.mean(bounded),
        raw_std=np.std(raw),
        bounded_std=np.std(bounded),
        gaussian_entropy_nats=entropy,
    )
    derivation = [
        f"Sample 20,000 actions from mean {mu:g} and standard deviation {sigma:g}.",
        f"Unbounded Gaussian entropy is {entropy:.6f} nats.",
        f'Clip to [-1,1]; clipped fraction is {metrics["clipped_fraction"]:.6f}.',
        f"Raw sample standard deviation is {np.std(raw):.6f}; bounded standard deviation is {np.std(bounded):.6f}.",
        f"Bounded mean is {np.mean(bounded):.6f}, which can shift when clipping is asymmetric around the policy mean.",
    ]
    notes = [
        "The entropy formula describes the unbounded Gaussian, not the clipped mixed distribution.",
        "A tanh-squashed policy requires a change-of-variables correction when computing log probabilities.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"mean": 0.2, "std": 0.5}
    parameters["std"] = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
