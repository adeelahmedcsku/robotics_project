"""Temporal-difference residuals, GAE and episode boundaries. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    gamma = 0.99
    lam = p["gae_lambda"]
    rewards = np.array([0.2, 0.1, -0.1, 0.3, 1.0])
    values = np.array([0.4, 0.45, 0.3, 0.5, 0.6, 0.0])
    terminal = np.array([False, False, False, False, True])
    advantage = np.zeros(5)
    carry = 0.0
    residual = []
    for t in reversed(range(5)):
        continuation = 0.0 if terminal[t] else 1.0
        delta = rewards[t] + gamma * values[t + 1] * continuation - values[t]
        carry = delta + gamma * lam * continuation * carry
        advantage[t] = carry
        residual.append(delta)
    returns = advantage + values[:-1]
    metrics = dict(
        initial_advantage=advantage[0],
        final_advantage=advantage[-1],
        advantage_std=np.std(advantage),
        initial_value_target=returns[0],
        mean_advantage=np.mean(advantage),
    )
    derivation = [
        f"Use rewards {rewards.tolist()} and value predictions {values.tolist()}.",
        f"The last transition is truly terminal; gamma={gamma:g}, lambda={lam:g}.",
        f"Backward TD residuals in chronological order are {list(reversed(residual))}.",
        f"The resulting advantage vector is {advantage.tolist()}.",
        f"Value targets A+V are {returns.tolist()}.",
    ]
    notes = [
        "A time-limit truncation may retain a bootstrap value while still preventing recurrence into the next reset episode.",
        "Correct masking needs separate termination and rollout-boundary semantics; one generic done flag can hide a bug.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"gae_lambda": 0.95}
    parameters["gae_lambda"] = [0.0, 0.25, 0.5, 0.75, 0.95, 1.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
