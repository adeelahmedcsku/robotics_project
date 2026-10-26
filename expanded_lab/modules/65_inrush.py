"""Capacitor charging, stored energy and inrush screening. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    V, R, C = p["voltage"], p["resistance"], p["capacitance"]
    tau = R * C
    initial = V / R
    energy = 0.5 * C * V * V
    t95 = -tau * np.log(0.05)
    power0 = V * V / R
    metrics = dict(
        initial_current_A=initial,
        time_constant_s=tau,
        charge_95_percent_time_s=t95,
        stored_energy_J=energy,
        initial_resistor_power_W=power0,
    )
    derivation = [
        f"Use illustrative source V={V:g} V, R={R:g} ohm and C={C:g} F.",
        f"Initial ideal charging current is {initial:.6f} A.",
        f"The RC time constant is {tau:.6f} s and 95% charge time is {t95:.6f} s.",
        f"Capacitor stored energy at full voltage is {energy:.6f} J.",
        f"Initial resistor power is {power0:.6f} W and decays with charging.",
    ]
    notes = [
        "Stored energy can remain after source disconnection; a physical discharge/isolation procedure must verify it.",
        "Resistor pulse energy, switching ratings, failure modes and supply behavior are not established by the ideal RC equation.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"voltage": 24.0, "resistance": 10.0, "capacitance": 0.002}
    parameters["resistance"] = [1.0, 2.0, 5.0, 10.0, 20.0, 50.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
