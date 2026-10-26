"""Encoder counts, quantization, wrapping and velocity estimates. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    resolution = int(p["counts"])
    dt = 0.002
    t = np.arange(0, 2, dt)
    truth = 3.1 + 0.4 * np.sin(2 * np.pi * 0.5 * t)
    wrapped = (truth + np.pi) % (2 * np.pi) - np.pi
    counts = np.round(wrapped / (2 * np.pi) * resolution)
    measured = counts * 2 * np.pi / resolution
    unwrapped = np.unwrap(measured)
    unwrapped += truth[0] - unwrapped[0]
    velocity = np.gradient(unwrapped, dt)
    exact = 0.4 * np.pi * np.cos(np.pi * t)
    metrics = dict(
        quantization_step_rad=2 * np.pi / resolution,
        position_rmse_rad=np.sqrt(np.mean((unwrapped - truth) ** 2)),
        velocity_rmse_rad_s=np.sqrt(np.mean((velocity - exact) ** 2)),
        raw_wrap_jump_rad=np.max(abs(np.diff(measured))),
    )
    derivation = [
        f"Encoder resolution is {resolution} counts per revolution.",
        f"One count represents {2*np.pi/resolution:.8f} rad.",
        "Generate a trajectory crossing the +/-pi wrapping boundary and quantize it.",
        f'After unwrap and initial alignment, position RMSE is {metrics["position_rmse_rad"]:.8f} rad.',
        f'Differentiating at 2 ms gives velocity RMSE {metrics["velocity_rmse_rad_s"]:.6f} rad/s.',
    ]
    notes = [
        "The initial alignment removes an arbitrary integer-turn offset but is not an absolute-zero calibration.",
        "Higher numerical differentiation rate does not create additional encoder position information.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"counts": 4096}
    parameters["counts"] = [256, 512, 1024, 4096, 16384, 65536][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
