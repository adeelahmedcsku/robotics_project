"""Monte Carlo uncertainty propagation and repeatability. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(int(p["seed"]))
    n = int(p["samples"])
    sigma = p["angle_noise"]
    mass = rng.normal(2.0, 0.04, n)
    length = rng.normal(0.25, 0.002, n)
    angle = rng.normal(0.6, sigma, n)
    torque = mass * 9.81 * length * np.cos(angle)
    nominal = 2 * 9.81 * 0.25 * np.cos(0.6)
    low, high = np.quantile(torque, [0.025, 0.975])
    metrics = dict(
        mean_torque_Nm=np.mean(torque),
        std_torque_Nm=np.std(torque, ddof=1),
        lower_quantile_Nm=low,
        upper_quantile_Nm=high,
        nominal_torque_Nm=nominal,
    )
    derivation = [
        f'Draw {n} samples with generator seed {int(p["seed"])}.',
        f"Mass sigma is 0.04 kg, lever sigma is 0.002 m, angle sigma is {sigma:g} rad.",
        f"Evaluate gravity torque for each sample; nominal value is {nominal:.6f} Nm.",
        f"Sample mean is {np.mean(torque):.6f} Nm and sample standard deviation is {np.std(torque,ddof=1):.6f} Nm.",
        f"Central empirical 95% interval is [{low:.6f},{high:.6f}] Nm.",
    ]
    notes = [
        "These quantiles describe the assumed population, not a confidence interval for the sample mean.",
        "Independent Gaussian inputs are a declared teaching assumption; shared calibration errors can create correlations.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"seed": 17, "samples": 5000, "angle_noise": 0.02}
    parameters["angle_noise"] = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
