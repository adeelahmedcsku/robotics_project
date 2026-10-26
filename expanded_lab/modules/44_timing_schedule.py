"""Multi-rate controllers, policy decimation and sample age. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    dt = 0.001
    n = 5000
    decimation = int(p["policy_decimation"])
    last_policy = 0
    ages = []
    counts = dict(physics=0, control=0, policy=0, telemetry=0)
    for tick in range(n):
        counts["physics"] += 1
        if tick % 2 == 0:
            counts["control"] += 1
        if tick % decimation == 0:
            last_policy = tick
            counts["policy"] += 1
        if tick % 100 == 0:
            counts["telemetry"] += 1
        ages.append((tick - last_policy) * dt)
    metrics = dict(
        policy_rate_Hz=1 / (dt * decimation),
        maximum_held_action_age_s=max(ages),
        mean_held_action_age_s=np.mean(ages),
        control_updates=counts["control"],
        policy_updates=counts["policy"],
        telemetry_updates=counts["telemetry"],
    )
    derivation = [
        f"Use {n} base ticks at {dt:g} s per tick.",
        f"Control runs every two ticks; policy runs every {decimation} ticks; telemetry every 100.",
        f"The policy rate is {1/(dt*decimation):.6f} Hz.",
        f"The oldest held policy action reaches {max(ages):.6f} s before replacement.",
        f"Event counts are {counts}.",
    ]
    notes = [
        "This schedule is logical simulation time and assumes every computation completes before its deadline.",
        "Wall-time execution still needs measured compute/transport budgets and an overrun response.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"policy_decimation": 20}
    parameters["policy_decimation"] = [2, 5, 10, 20, 50, 100][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
