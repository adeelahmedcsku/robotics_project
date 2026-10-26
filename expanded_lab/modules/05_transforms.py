"""Homogeneous transforms and frame-chain round trips. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def transform(angle, translation):
    c, s = np.cos(angle), np.sin(angle)
    T = np.eye(4)
    T[:3, :3] = [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    T[:3, 3] = translation
    return T


def experiment(p):
    a = np.deg2rad(p["angle_deg"])
    T_ab = transform(a, [0.1, 0.2, 0.3])
    T_bc = transform(-0.3, [p["offset"], 0.0, 0.05])
    T_ac = T_ab @ T_bc
    point = np.array([0.2, 0.1, 0.0, 1.0])
    world = T_ac @ point
    R, t = T_ac[:3, :3], T_ac[:3, 3]
    inverse = np.eye(4)
    inverse[:3, :3] = R.T
    inverse[:3, 3] = -R.T @ t
    recovered = inverse @ world
    error = np.linalg.norm(recovered - point)
    direct = T_ab @ (T_bc @ point)
    assert np.allclose(world, direct) and error < 1e-12
    metrics = dict(
        point_x_m=world[0],
        point_y_m=world[1],
        point_z_m=world[2],
        roundtrip_error_m=error,
        translation_norm_m=np.linalg.norm(t),
    )
    derivation = [
        f'T_BC translation is ({p["offset"]:.6f},0,0.05) m.',
        f"T_AB rotates by {a:.6f} rad before adding its translation.",
        f"Compose T_AC; the resulting translation is {t.tolist()} m.",
        f"Point (0.2,0.1,0) in C becomes {world[:3].tolist()} in A.",
        f"Apply the analytic inverse; recovery error is {error:.3e} m.",
    ]
    notes = [
        "The point result includes both translations in the correct rotated directions.",
        "A direction encoded with homogeneous last element zero would ignore translation.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"angle_deg": 45.0, "offset": 0.15}
    parameters["angle_deg"] = [0.0, 15.0, 30.0, 45.0, 60.0, 90.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
