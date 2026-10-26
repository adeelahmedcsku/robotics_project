"""Vectors, projections and joint-axis torque. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    length, force = p["length"], p["force"]
    angle = np.deg2rad(p["angle_deg"])
    r = np.array([length, 0.0, 0.0])
    F = force * np.array([np.cos(angle), np.sin(angle), 0.0])
    axis = np.array([0.0, 0.0, 1.0])
    moment = np.cross(r, F)
    torque = float(axis @ moment)
    perpendicular = force * np.sin(angle)
    assert np.isclose(torque, length * perpendicular)
    metrics = dict(
        axis_torque_Nm=torque,
        force_perpendicular_N=perpendicular,
        force_magnitude_N=float(np.linalg.norm(F)),
        lever_m=length,
    )
    derivation = [
        f"Force components in the chosen frame: Fx={F[0]:.6f} N, Fy={F[1]:.6f} N.",
        f"The lever is ({length:.6f}, 0, 0) m, so only Fy contributes to the z moment.",
        f"r cross F gives Mz={moment[2]:.6f} Nm.",
        f"Projection onto the unit z axis gives torque {torque:.6f} Nm.",
    ]
    notes = [
        f"The effective perpendicular force is {perpendicular:.6f} N, rather than the full {force:g} N.",
        "Changing origin changes moment; changing coordinates consistently does not change its physical meaning.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"length": 0.2, "force": 50.0, "angle_deg": 60.0}
    parameters["angle_deg"] = [0.0, 15.0, 30.0, 45.0, 60.0, 90.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
