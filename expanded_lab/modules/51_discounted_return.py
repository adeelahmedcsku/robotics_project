"""Markov decision processes and discounted reward. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    gamma = p["gamma"]
    dt = 0.02
    immediate = np.zeros(100)
    delayed = np.zeros(100)
    immediate[0] = 1.0
    delayed[50] = 3.0
    weights = gamma ** np.arange(100)
    a = float(weights @ immediate)
    b = float(weights @ delayed)
    horizon = 1 / (1 - gamma)
    tau = -dt / np.log(gamma)
    metrics = dict(
        immediate_return=a,
        delayed_return=b,
        delayed_preference_margin=b - a,
        effective_horizon_steps=horizon,
        continuous_time_scale_s=tau,
    )
    derivation = [
        f"Choose gamma={gamma:g} at control period {dt:g} s.",
        "One candidate receives reward 1 now; the other receives reward 3 after 50 steps.",
        f"Immediate return is {a:.6f}; delayed return is 3*gamma^50={b:.6f}.",
        f"The geometric horizon scale is {horizon:.6f} steps.",
        f"The matching exponential time constant is {tau:.6f} s.",
    ]
    notes = [
        (
            "The delayed outcome is preferred under this discount."
            if b > a
            else "The immediate outcome is preferred despite the larger undiscounted delayed reward."
        ),
        "Episode termination, reward scaling and physical-time interpretation remain part of the task specification.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"gamma": 0.99}
    parameters["gamma"] = [0.9, 0.95, 0.97, 0.98, 0.99, 0.995][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
