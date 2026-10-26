"""Observation ordering, normalization and schema hashes. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np

import hashlib
import json


def experiment(p):
    raw = np.array([0.2, -0.1, 0.5])
    mean = np.array([0.0, 0.0, 0.1])
    std = np.array([0.5, 0.5, 0.2])
    names = ["elbow_rad", "knee_rad", "gyro_rad_s"]
    normalized = (raw - mean) / std
    weights = np.array([0.4, -0.2, 0.1])
    baseline = float(weights @ normalized)
    shifted = raw.copy()
    shifted[2] += p["gyro_offset"]
    correct = float(weights @ ((shifted - mean) / std))
    wrong = float(weights @ ((shifted[[2, 1, 0]] - mean) / std))
    schema = dict(
        names=names, mean=mean.tolist(), std=std.tolist(), dtype="float32"
    )
    encoded = json.dumps(schema, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    metrics = dict(
        reference_action=baseline,
        correct_action=correct,
        reordered_action=wrong,
        reordering_action_error=abs(correct - wrong),
        normalized_gyro=(shifted[2] - mean[2]) / std[2],
    )
    derivation = [
        f"Ordered fields are {names}.",
        f"Means are {mean.tolist()} and standard deviations are {std.tolist()}.",
        f'Apply gyro offset {p["gyro_offset"]:g} rad/s and normalize in the declared order.',
        f"Correct action is {correct:.6f}; a silent field swap produces {wrong:.6f}.",
        f"Canonical schema SHA256 is {digest}.",
    ]
    notes = [
        "A schema hash detects version mismatch only when both producer and consumer actually enforce it.",
        "Include clipping, frame conventions, history stacking and action scaling in a real deployment contract.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"gyro_offset": 0.0}
    parameters["gyro_offset"] = [-0.2, -0.1, 0.0, 0.1, 0.2, 0.5][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
