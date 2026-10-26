"""Stereo depth, disparity uncertainty and range limits. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    Z = p["true_depth"]
    f, B = 400.0, 0.06
    sigma = p["disparity_noise"]
    disparity = f * B / Z
    std = f * B * sigma / disparity**2
    noisy_depth = f * B / (disparity + sigma)
    metrics = dict(
        disparity_px=disparity,
        depth_std_m=std,
        relative_depth_std=std / Z,
        one_sigma_positive_disparity_depth_m=noisy_depth,
        linearization_error_m=abs((Z - std) - noisy_depth),
    )
    derivation = [
        f"Use focal length {f:g} px and calibrated baseline {B:g} m.",
        f"At true depth {Z:g} m, expected disparity is {disparity:.6f} px.",
        f"Disparity sigma={sigma:g} px propagates to sigma_Z={std:.6f} m.",
        f"A +1 sigma disparity perturbation gives exact depth {noisy_depth:.6f} m.",
        f'Compare the first-order prediction Z-sigma_Z; linearization discrepancy is {metrics["linearization_error_m"]:.6f} m.',
    ]
    notes = [
        "Depth uncertainty grows quadratically with range in this fixed-camera approximation.",
        "When disparity approaches its uncertainty scale, Gaussian linearization and naive depth estimates become unreliable.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"true_depth": 1.0, "disparity_noise": 0.5}
    parameters["true_depth"] = [0.3, 0.5, 1.0, 2.0, 3.0, 5.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
