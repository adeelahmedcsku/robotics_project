"""Message queues, delivery policy and stale-command risk. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    producer_dt = 0.01
    consumer_dt = p["consumer_period"]
    production = np.arange(0, 5, producer_dt)
    consumption = np.arange(0, 5, consumer_dt)
    fifo = []
    latest = []
    queue = []
    index = 0
    dropped = 0
    for now in consumption:
        arrivals = []
        while index < len(production) and production[index] <= now + 1e-12:
            arrivals.append(production[index])
            index += 1
        queue.extend(arrivals)
        if queue:
            fifo.append(now - queue.pop(0))
        available = production[production <= now + 1e-12]
        if len(available):
            latest.append(now - available[-1])
        dropped += max(0, len(arrivals) - 1)
    metrics = dict(
        fifo_mean_age_s=np.mean(fifo),
        fifo_max_age_s=np.max(fifo),
        latest_mean_age_s=np.mean(latest),
        latest_max_age_s=np.max(latest),
        fifo_backlog_count=len(queue),
        replaced_arrivals_count=dropped,
    )
    derivation = [
        f"The producer emits state every {producer_dt:g} s.",
        f"The consumer processes one item every {consumer_dt:g} s.",
        f"FIFO retains {len(queue)} pending messages after the five-second run.",
        f"FIFO maximum age is {np.max(fifo):.6f} s; latest-value maximum age is {np.max(latest):.6f} s.",
        f"Latest-value replacement intentionally skips at least {dropped} intermediate arrivals in this schedule.",
    ]
    notes = [
        "A trajectory is not always replaceable by its last point; choose semantics appropriate to the command type.",
        "The simulation concerns queue policy only and does not reproduce packet loss, DDS discovery or actual ROS middleware timing.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"consumer_period": 0.02}
    parameters["consumer_period"] = [0.005, 0.01, 0.015, 0.02, 0.05, 0.1][
        args.case
    ]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
