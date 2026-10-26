"""Support polygons, center of pressure and load transfer. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    left = p["left_load"]
    right = 1 - left
    weight = p["mass"] * 9.81
    assert 0 <= left <= 1
    positions = np.array([-0.1, 0.1])
    forces = weight * np.array([left, right])
    cop = float(forces @ positions / forces.sum())
    com = p["com_x"]
    margin = min(com + 0.14, 0.14 - com)
    moment = weight * (com - cop)
    metrics = dict(
        cop_x_m=cop,
        com_margin_m=margin,
        left_force_N=forces[0],
        right_force_N=forces[1],
        unbalanced_pitch_moment_Nm=moment,
    )
    derivation = [
        f"Total vertical load is {weight:.6f} N.",
        f"Left fraction {left:g} gives forces {forces.tolist()} N at x=-0.1,+0.1 m.",
        f"The weighted contact location is COP x={cop:.6f} m.",
        f"COM x={com:g} m has signed margin {margin:.6f} m inside the illustrative outer edges.",
        f"The gravity/COP moment difference is {moment:.6f} Nm.",
    ]
    notes = [
        (
            "One contact resultant has zero load; do not treat both point contacts as equally active support."
            if min(left, right) == 0
            else "Both contact resultants are compressive in this static illustration."
        ),
        "The .14 m outer edges are teaching geometry; real support requires measured foot patches and contact state.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"left_load": 0.5, "mass": 10.0, "com_x": 0.02}
    parameters["left_load"] = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
