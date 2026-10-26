"""Domain randomization, correlations and feasible parameter sets. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(73)
    n = 5000
    width = p["range_fraction"]
    density = rng.uniform(1 - width, 1 + width, n)
    length_scale = rng.uniform(1 - width, 1 + width, n)
    mass = 2 * density * length_scale
    length = 0.3 * length_scale
    consistent = mass * length**2 / 3
    independent = 0.06 * rng.uniform(1 - width, 1 + width, n)
    implied_length = np.sqrt(3 * independent / mass)
    metrics = dict(
        mass_std_kg=np.std(mass),
        consistent_inertia_std_kg_m2=np.std(consistent),
        mass_inertia_correlation=np.corrcoef(mass, consistent)[0, 1],
        independent_implied_length_rmse_m=np.sqrt(
            np.mean((implied_length - length) ** 2)
        ),
        maximum_consistent_inertia_kg_m2=np.max(consistent),
    )
    derivation = [
        f"Sample density and length scales within +/-{width*100:g} percent.",
        "Derive mass and inertia from the same physical dimensions rather than unrelated ranges.",
        f"Mass standard deviation is {np.std(mass):.6f} kg and inertia standard deviation is {np.std(consistent):.6f} kg*m^2.",
        f'Mass/inertia sample correlation is {metrics["mass_inertia_correlation"]:.6f}.',
        f'Independent inertia sampling implies a rod-length RMSE of {metrics["independent_implied_length_rmse_m"]:.6f} m relative to the actual sampled length.',
    ]
    notes = [
        "The chosen manufacturing model is still simplified; real uncertainty may arise from payload, assembly and calibration rather than density changes.",
        "Randomization ranges need identification evidence and held-out evaluation, not just an intuition that more variation is safer.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"range_fraction": 0.1}
    parameters["range_fraction"] = [0.01, 0.025, 0.05, 0.1, 0.2, 0.3][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
