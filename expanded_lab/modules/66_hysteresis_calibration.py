"""Bidirectional calibration and hidden hysteresis. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(89)
    x = np.linspace(-0.5, 0.5, 100)
    h = p["hysteresis"]
    a, b = 1.02, 0.01
    forward = a * x + b + h + rng.normal(0, 0.001, len(x))
    reverse = a * x + b - h + rng.normal(0, 0.001, len(x))
    X = np.column_stack([np.tile(x, 2), np.ones(200)])
    y = np.concatenate([forward, reverse])
    theta = np.linalg.lstsq(X, y, rcond=None)[0]
    residual = y - X @ theta
    f_bias = residual[:100].mean()
    r_bias = residual[100:].mean()
    metrics = dict(
        fitted_scale=theta[0],
        fitted_offset_rad=theta[1],
        pooled_residual_rmse_rad=np.sqrt(np.mean(residual**2)),
        forward_bias_rad=f_bias,
        reverse_bias_rad=r_bias,
        directional_separation_rad=f_bias - r_bias,
    )
    derivation = [
        f"True scale is {a:g} and offset {b:g} rad.",
        f"Add directional offset +/-{h:g} rad and 0.001 rad noise.",
        f"Fit one shared scale/offset to both directions: {theta.tolist()}.",
        f"Forward residual mean is {f_bias:.6f} rad; reverse mean is {r_bias:.6f} rad.",
        f"Directional separation is {f_bias-r_bias:.6f} rad, revealing structure hidden by a pooled fit.",
    ]
    notes = [
        "A low aggregate fit error can still conceal a consistent direction-dependent error relevant to reaching or balance.",
        "A calibration model should match the phenomenon and be validated on independent bidirectional trajectories.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"hysteresis": 0.005}
    parameters["hysteresis"] = [0.0, 0.001, 0.002, 0.005, 0.01, 0.02][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
