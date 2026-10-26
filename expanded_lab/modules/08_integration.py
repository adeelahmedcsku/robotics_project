"""Discrete integration and numerical stability. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    dt, k, T = p["dt"], p["decay_rate"], p["duration"]
    n = max(1, round(T / dt))
    actual = n * dt
    explicit = 1.0
    implicit = 1.0
    for _ in range(n):
        explicit *= 1 - k * dt
        implicit /= 1 + k * dt
    exact = np.exp(-k * actual)
    factor = abs(1 - k * dt)
    metrics = dict(
        explicit_final=explicit,
        implicit_final=implicit,
        exact_final=exact,
        explicit_abs_error=abs(explicit - exact),
        implicit_abs_error=abs(implicit - exact),
        explicit_amplification=factor,
    )
    derivation = [
        f"Choose dt={dt:g} s and decay rate k={k:g} per second.",
        f"Advance {n} steps to actual time {actual:.6f} s.",
        f"Explicit one-step multiplier is {1-k*dt:.6f}; its magnitude is {factor:.6f}.",
        f"Exact final value is {exact:.8f}; explicit gives {explicit:.8f}.",
        f"Implicit final value is {implicit:.8f}; compare absolute errors in the table.",
    ]
    notes = [
        (
            "The explicit recurrence is stable for this scalar decay."
            if factor < 1
            else "The explicit recurrence is on or outside its stability boundary; reducing dt changes the numerical problem."
        ),
        "Implicit stability does not mean high accuracy; a heavily damped numerical result can still be wrong.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"dt": 0.02, "decay_rate": 10.0, "duration": 1.0}
    parameters["dt"] = [0.005, 0.01, 0.02, 0.05, 0.1, 0.25][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
