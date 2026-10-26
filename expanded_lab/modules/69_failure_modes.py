"""Fault injection, diagnostic coverage and remaining blind spots. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(97)
    n = 2000
    coverage = p["sensor_fault_detection"]
    categories = ["stale", "range", "sensor_bias", "power_loss"]
    weights = np.array([0.3, 0.2, 0.3, 0.2])
    detection = np.array([0.99, 0.99, coverage, 0.4])
    chosen = rng.choice(4, n, p=weights)
    detected = rng.random(n) < detection[chosen]
    observed = detected.mean()
    expected = float(weights @ detection)
    counts = {
        name: int(np.count_nonzero(chosen == i))
        for i, name in enumerate(categories)
    }
    metrics = dict(
        observed_detection_fraction=observed,
        expected_weighted_detection=expected,
        expected_undetected_fraction=1 - expected,
        undetected_fault_count=np.count_nonzero(~detected),
        sensor_bias_detection_assumption=coverage,
    )
    derivation = [
        f"Inject {n} synthetic faults with category counts {counts}.",
        f"Assumed category detection probabilities are {detection.tolist()}.",
        f"Weighted expected detection is {expected:.6f}.",
        f"The seeded campaign observes detection fraction {observed:.6f}.",
        f"Expected residual undetected fraction is {1-expected:.6f} under the chosen artificial mixture.",
    ]
    notes = [
        "The category mixture and detection probabilities are invented experiment inputs and cannot establish a physical safety integrity level.",
        "Detection alone is incomplete: the protective response, common-cause failures and consequences must also be evaluated.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"sensor_fault_detection": 0.5}
    parameters["sensor_fault_detection"] = [0.0, 0.25, 0.5, 0.75, 0.9, 0.99][
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
