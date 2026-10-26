"""Gravity compensation and model-mismatch torque. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    true_mass = 2.0
    model_mass = p["model_mass"]
    length = 0.25
    angles = np.linspace(-1.0, 1.0, 41)
    basis = np.cos(angles)
    true = true_mass * 9.81 * length * basis
    assumed = model_mass * 9.81 * length * basis
    rng = np.random.default_rng(3)
    measured = true + rng.normal(0, 0.03, len(angles))
    coefficient = float(basis @ measured / (basis @ basis))
    fitted = coefficient * basis
    metrics = dict(
        feedforward_rmse_Nm=np.sqrt(np.mean((true - assumed) ** 2)),
        peak_residual_Nm=np.max(abs(true - assumed)),
        identified_mass_kg=coefficient / (9.81 * length),
        fit_residual_rmse_Nm=np.sqrt(np.mean((measured - fitted) ** 2)),
    )
    derivation = [
        f"The true static gravity coefficient is {true_mass*9.81*length:.6f} Nm.",
        f"The assumed model uses mass {model_mass:g} kg and coefficient {model_mass*9.81*length:.6f} Nm.",
        "Generate static samples over -1 to +1 rad with 0.03 Nm standard-deviation noise.",
        f"Project measurements onto cos(q), obtaining A_hat={coefficient:.6f} Nm.",
        f'The inferred mass is {metrics["identified_mass_kg"]:.6f} kg; feedforward mismatch RMSE is {metrics["feedforward_rmse_Nm"]:.6f} Nm.',
    ]
    notes = [
        "The cosine model assumes a known angle convention, lever and negligible dynamic/friction torque during the measurement.",
        "A good gravity fit does not identify inertia, backlash or transient motor limits.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"model_mass": 1.8}
    parameters["model_mass"] = [1.0, 1.5, 1.8, 2.0, 2.2, 2.5][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
