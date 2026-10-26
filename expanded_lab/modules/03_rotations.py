"""Rotation matrices and the Rodrigues formula. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    theta = np.deg2rad(p["angle_deg"])
    axis = np.array([1.0, 2.0, 3.0])
    axis /= np.linalg.norm(axis)
    x, y, z = axis
    K = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
    R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
    v = np.array([0.3, -0.2, 0.5])
    rotated = R @ v
    ortho = np.linalg.norm(R.T @ R - np.eye(3))
    det = np.linalg.det(R)
    roundtrip = np.linalg.norm(R.T @ rotated - v)
    assert ortho < 1e-12 and abs(det - 1) < 1e-12
    metrics = dict(
        rotated_x_m=rotated[0],
        rotated_y_m=rotated[1],
        rotated_z_m=rotated[2],
        orthogonality_error=ortho,
        roundtrip_error_m=roundtrip,
    )
    derivation = [
        f"Normalize axis (1,2,3) to {axis.tolist()}.",
        f'Convert {p["angle_deg"]:g} degrees to {theta:.6f} radians.',
        f"Assemble the skew matrix and evaluate Rodrigues; determinant is {det:.12f}.",
        f"R times (0.3,-0.2,0.5) gives {rotated.tolist()} meters.",
        f"Transpose the rotation to recover the original vector; residual is {roundtrip:.3e} m.",
    ]
    notes = [
        "A determinant near one does not alone guarantee orthogonality; both tests are retained.",
        "The chosen axis and vector are teaching geometry, unrelated to an unverified motor mounting.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"angle_deg": 45.0}
    parameters["angle_deg"] = [0.0, 15.0, 45.0, 90.0, 135.0, 180.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
