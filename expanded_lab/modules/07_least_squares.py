"""Least-squares identification and residual diagnosis. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    n = int(p["samples"])
    sigma = p["noise"]
    span = p["span"]
    rng = np.random.default_rng(11)
    x = np.linspace(-span, span, n)
    X = np.column_stack([x, np.ones(n)])
    truth = np.array([1.04, 0.025])
    y = X @ truth + rng.normal(0, sigma, n)
    estimate, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    residual = y - X @ estimate
    variance = float(residual @ residual / (n - 2))
    covariance = variance * np.linalg.inv(X.T @ X)
    metrics = dict(
        scale_error=estimate[0] - truth[0],
        offset_error_rad=estimate[1] - truth[1],
        residual_rmse_rad=np.sqrt(np.mean(residual**2)),
        design_condition=np.linalg.cond(X),
        scale_std_estimate=np.sqrt(covariance[0, 0]),
    )
    derivation = [
        f"Collect {n} reference positions spanning [-{span:g},{span:g}] rad.",
        f"True scale and offset are {truth.tolist()}; inject noise sigma={sigma:g} rad.",
        f"Least-squares estimate is {estimate.tolist()}.",
        f"Residual degrees of freedom are {n-2}; variance estimate is {variance:.6e}.",
        f"The design matrix condition is {np.linalg.cond(X):.6f}; estimated scale uncertainty is {np.sqrt(covariance[0,0]):.6f}.",
    ]
    notes = [
        f"The identification range is {2*span:g} rad; narrowing it weakens scale estimation even if the offset remains observable.",
        "Covariance assumes the linear noise model and does not account for backlash, systematic reference error or temperature drift.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"samples": 40, "noise": 0.005, "span": 0.5}
    parameters["span"] = [0.01, 0.025, 0.05, 0.1, 0.5, 1.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
