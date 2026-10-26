"""Cable resistance, voltage drop and heat screening. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rho = 1.72e-8
    length = p["one_way_length"]
    area = p["area_mm2"] * 1e-6
    current = p["current"]
    R = rho * 2 * length / area
    drop = current * R
    heat = current * current * R
    metrics = dict(
        loop_resistance_ohm=R,
        voltage_drop_V=drop,
        conductor_heat_W=heat,
        drop_fraction_of_48V=drop / 48.0,
        heat_per_one_way_meter_W_m=heat / length,
    )
    derivation = [
        f'Assume rho={rho:.3e} ohm*m, one-way length {length:g} m and area {p["area_mm2"]:g} mm^2.',
        f"Include outgoing and return conductors: loop resistance is {R:.8f} ohm.",
        f"At current {current:g} A, voltage drop is {drop:.6f} V.",
        f"Joule heating is I^2*R={heat:.6f} W across the loop.",
        f"Drop is {drop/48*100:.6f}% of an illustrative 48 V bus.",
    ]
    notes = [
        "The 48 V reference and resistivity are declared arithmetic assumptions, not an approved operating voltage or wire rating.",
        "Connector contact resistance, flex life, thermal environment and protective-device coordination are excluded.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"one_way_length": 1.0, "area_mm2": 1.5, "current": 5.0}
    parameters["current"] = [1.0, 2.0, 5.0, 10.0, 15.0, 20.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
