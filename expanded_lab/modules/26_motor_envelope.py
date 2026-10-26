"""Torque-speed envelopes and trajectory feasibility. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    omega = p["speed"]
    stall = p["stall_torque"]
    free = p["no_load_speed"]
    required = p["required_torque"]
    available = stall * max(0.0, 1 - abs(omega) / free)
    reserve = available - abs(required)
    metrics = dict(
        available_torque_Nm=available,
        reserve_Nm=reserve,
        required_mechanical_power_W=required * omega,
        envelope_power_W=available * abs(omega),
        feasible=float(reserve >= 0),
    )
    derivation = [
        f"The teaching envelope has zero-speed torque {stall:g} Nm and no-load speed {free:g} rad/s.",
        f"At speed {omega:g} rad/s the linear speed factor is {max(0,1-abs(omega)/free):.6f}.",
        f"Available torque is {available:.6f} Nm while demand is {required:g} Nm.",
        f"Reserve is {reserve:.6f} Nm; feasibility flag is {reserve>=0}.",
        f"Demanded mechanical power is {required*omega:.6f} W.",
    ]
    notes = [
        "The illustrative envelope is instantaneous and excludes continuous thermal derating and regenerative quadrants.",
        "A positive reserve is only one constraint; position, load path, current and thermal checks remain separate.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {
        "speed": 2.0,
        "stall_torque": 10.0,
        "no_load_speed": 8.0,
        "required_torque": 4.0,
    }
    parameters["speed"] = [0.0, 1.0, 2.0, 4.0, 6.0, 8.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
