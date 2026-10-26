"""Load paths, bolt-group screening and nominal stress. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    n = 4
    radius = p["radius"]
    F = p["axial_force"]
    moment = p["moment"]
    angles = np.arange(n) * 2 * np.pi / n
    y = radius * np.sin(angles)
    loads = F / n + moment * y / np.sum(y * y)
    area = 8e-6
    stress = loads.max() / area / 1e6
    metrics = dict(
        maximum_bolt_load_N=loads.max(),
        minimum_bolt_load_N=loads.min(),
        nominal_max_tensile_stress_MPa=stress,
        bolt_circle_radius_m=radius,
        recovered_total_force_N=loads.sum(),
    )
    assert np.isclose(loads.sum(), F)
    derivation = [
        f"Four ideal bolts lie on radius {radius:g} m with y coordinates {y.tolist()} m.",
        f"Apply direct axial force {F:g} N and bending moment {moment:g} Nm.",
        f"The simplified bolt loads are {loads.tolist()} N.",
        f"Maximum load {loads.max():.6f} N divided by assumed area 8 mm^2 gives {stress:.6f} MPa.",
        f"Summed axial force recovers {loads.sum():.6f} N as a consistency check.",
    ]
    notes = [
        "Negative calculated load indicates the simple tension-only interpretation needs joint contact/separation analysis.",
        "No allowable stress, bolt grade, preload or tightening torque is specified; this is not a structural approval.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"radius": 0.025, "axial_force": 400.0, "moment": 5.0}
    parameters["radius"] = [0.015, 0.02, 0.025, 0.03, 0.04, 0.05][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
