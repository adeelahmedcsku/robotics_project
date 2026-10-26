"""Mechanical energy, electrical demand and regeneration. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    eta = p["efficiency"]
    regen = p["regen_efficiency"]
    T = 4.0
    t = np.linspace(0, T, 2001)
    speed = 2 * np.sin(2 * np.pi * t / T)
    torque = 1.5 * np.cos(2 * np.pi * t / T) + 0.5
    mechanical = torque * speed
    electrical = np.where(mechanical >= 0, mechanical / eta, mechanical * regen)
    positive = np.trapezoid(np.maximum(electrical, 0), t)
    returned = -np.trapezoid(np.minimum(electrical, 0), t)
    metrics = dict(
        energy_drawn_J=positive,
        energy_returned_J=returned,
        net_energy_J=positive - returned,
        peak_draw_W=max(electrical),
        peak_return_W=-min(electrical),
    )
    derivation = [
        "Generate a four-second signed torque and speed cycle.",
        f"Motoring efficiency is {eta:g}; regenerative efficiency is {regen:g}.",
        f"Convert positive and negative mechanical power using their respective efficiencies.",
        f"Integrate positive electrical power: {positive:.6f} J drawn.",
        f"Integrate negative electrical power: {returned:.6f} J returned; net is {positive-returned:.6f} J.",
    ]
    notes = [
        "Negative mechanical power represents energy leaving the mechanical system; the electrical destination depends on the actual drive and power topology.",
        "A low net-energy cycle can still impose large instantaneous source and sink requirements.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"efficiency": 0.8, "regen_efficiency": 0.5}
    parameters["regen_efficiency"] = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
