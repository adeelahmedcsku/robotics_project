"""Link masses, payload shifts and center of mass. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    masses = np.array([4.0, 2.0, 1.0, p["payload_mass"]])
    positions = np.array(
        [
            [0.0, 0.0, 0.4],
            [0.1, 0.0, 0.3],
            [-0.1, 0.0, 0.2],
            [p["payload_x"], 0.0, 0.5],
        ]
    )
    total = masses.sum()
    com = (masses[:, None] * positions).sum(axis=0) / total
    forces = masses[:, None] * np.array([0.0, 0.0, -9.81])
    moment = np.cross(positions, forces).sum(axis=0)
    expected = np.cross(com, total * np.array([0.0, 0.0, -9.81]))
    assert np.allclose(moment, expected)
    metrics = dict(
        total_mass_kg=total,
        com_x_m=com[0],
        com_z_m=com[2],
        gravity_pitch_moment_Nm=moment[1],
        weight_N=total * 9.81,
    )
    derivation = [
        f'Total mass is 4+2+1+{p["payload_mass"]:g} = {total:.6f} kg.',
        f'The payload lies at x={p["payload_x"]:g} m in the shared frame.',
        f"Sum mass times position, then divide by total: COM={com.tolist()} m.",
        f"Sum each gravity moment to obtain pitch moment {moment[1]:.6f} Nm.",
        "Applying total weight at the COM reproduces the same moment, providing an independent check.",
    ]
    notes = [
        "This static point-mass model does not represent distributed inertia or dynamic contact stability.",
        f"The horizontal COM displacement from the origin is {com[0]:.6f} m; compare it with a measured support margin.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"payload_mass": 1.0, "payload_x": 0.3}
    parameters["payload_mass"] = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
