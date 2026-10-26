"""Inertia tensors and the parallel-axis theorem. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    m = p["mass"]
    a, b, c = 0.2, 0.1, 0.08
    r = np.array([p["offset"], 0.02, 0.0])
    Ic = m / 12 * np.diag([b * b + c * c, a * a + c * c, a * a + b * b])
    shift = m * ((r @ r) * np.eye(3) - np.outer(r, r))
    Io = Ic + shift
    principal = np.linalg.eigvalsh(Io)
    alpha = np.array([0.0, 0.0, p["acceleration"]])
    tau = Io @ alpha
    assert np.all(principal > 0) and np.allclose(Io, Io.T)
    metrics = dict(
        Izz_kg_m2=Io[2, 2],
        minimum_principal_kg_m2=principal[0],
        torque_z_Nm=tau[2],
        offset_contribution_kg_m2=shift[2, 2],
    )
    derivation = [
        f"A uniform {m:g} kg box has COM Izz={Ic[2,2]:.8f} kg*m^2.",
        f"Shift the reference by {r.tolist()} m.",
        f"The parallel-axis contribution to Izz is {shift[2,2]:.8f} kg*m^2.",
        f"Total Izz is {Io[2,2]:.8f}; requested z acceleration is {alpha[2]:g} rad/s^2.",
        f"Ignoring other dynamics, required z torque is {tau[2]:.8f} Nm.",
    ]
    notes = [
        "This acceleration-only torque excludes gravity, Coriolis terms, friction and transmission effects.",
        "An inertia tensor attached to the wrong origin can make a controller consistently wrong even when total mass is correct.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"mass": 2.0, "offset": 0.1, "acceleration": 3.0}
    parameters["offset"] = [0.0, 0.02, 0.05, 0.1, 0.2, 0.3][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
