"""Contact detection, thresholds and hysteresis. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(41)
    t = np.arange(0, 4, 0.01)
    truth = (t >= 1) & (t < 3)
    signal = np.where(truth, 30.0, 0.0)
    signal = signal + rng.normal(0, p["noise_std"], len(t))
    enter, exit = 15.0, 5.0
    state = False
    predicted = []
    for value in signal:
        if not state and value >= enter:
            state = True
        elif state and value <= exit:
            state = False
        predicted.append(state)
    predicted = np.array(predicted)
    false_positive = np.mean(predicted[~truth])
    false_negative = np.mean(~predicted[truth])
    switches = np.count_nonzero(predicted[1:] != predicted[:-1])
    metrics = dict(
        false_positive_fraction=false_positive,
        false_negative_fraction=false_negative,
        transition_count=switches,
        accuracy=np.mean(predicted == truth),
        signal_noise_std_N=p["noise_std"],
    )
    derivation = [
        "The labeled contact interval is one to three seconds with mean load 30 N.",
        f'Add Gaussian noise with sigma={p["noise_std"]:g} N.',
        "Enter contact at 15 N and leave at 5 N using a stateful threshold.",
        f"False-positive fraction is {false_positive:.6f}; false-negative fraction is {false_negative:.6f}.",
        f"The detector made {switches} state transitions instead of the ideal two.",
    ]
    notes = [
        "Thresholds are teaching values; a real detector must be calibrated for sensor range, preload, bias and contact dynamics.",
        "A stable contact flag does not prove no slip or a known contact wrench.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"noise_std": 5.0}
    parameters["noise_std"] = [0.5, 2.0, 5.0, 8.0, 12.0, 20.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
