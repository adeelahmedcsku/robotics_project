"""Angular momentum, kinetic energy and off-axis motion. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    I = np.diag([0.08, 0.12, 0.2])
    omega = np.array([p["speed"], 0.7, 0.2])
    alpha = np.array([0.0, 0.3, 0.0])
    momentum = I @ omega
    energy = 0.5 * omega @ momentum
    gyroscopic = np.cross(omega, momentum)
    torque = I @ alpha + gyroscopic
    cosine = (omega @ momentum) / (
        np.linalg.norm(omega) * np.linalg.norm(momentum)
    )
    angle = np.arccos(np.clip(cosine, -1, 1))
    metrics = dict(
        kinetic_energy_J=energy,
        momentum_norm_kg_m2_s=np.linalg.norm(momentum),
        misalignment_rad=angle,
        gyroscopic_torque_Nm=np.linalg.norm(gyroscopic),
        required_torque_Nm=np.linalg.norm(torque),
    )
    derivation = [
        f"Angular velocity is {omega.tolist()} rad/s.",
        f"Multiply by diagonal inertia to obtain L={momentum.tolist()} kg*m^2/s.",
        f"The quadratic energy is {energy:.6f} J.",
        f"Compute omega cross L: {gyroscopic.tolist()} Nm.",
        f"Include the acceleration term to obtain torque {torque.tolist()} Nm.",
    ]
    notes = [
        f"L and omega differ in direction by {angle:.6f} rad in this non-spherical body.",
        "The calculation assumes a rigid body about its COM with a consistently expressed inertia tensor.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"speed": 1.0}
    parameters["speed"] = [0.1, 0.3, 0.7, 1.0, 2.0, 4.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
