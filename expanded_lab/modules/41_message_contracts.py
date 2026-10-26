"""Typed joint-command contracts and rejection accounting. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def valid(message, now, last_sequence):
    names = ["joint_a", "joint_b"]
    if message.get("names") != names:
        return False, "names"
    q = np.asarray(message.get("position", []), dtype=float)
    if q.shape != (2,):
        return False, "shape"
    if not np.isfinite(q).all():
        return False, "nonfinite"
    if np.any(abs(q) > 0.5):
        return False, "range"
    if message["sequence"] <= last_sequence:
        return False, "sequence"
    age = now - message["sent"]
    if not 0 <= age <= 0.1:
        return False, "age"
    return True, "accepted"


def experiment(p):
    rng = np.random.default_rng(47)
    n = 1000
    last = -1
    counts = {}
    corrupt = p["invalid_fraction"]
    for i in range(n):
        now = i * 0.02
        msg = dict(
            names=["joint_a", "joint_b"],
            position=[0.1, -0.1],
            sequence=i,
            sent=now - 0.01,
        )
        if rng.random() < corrupt:
            kind = i % 4
            if kind == 0:
                msg["names"] = ["joint_b", "joint_a"]
            if kind == 1:
                msg["position"] = [float("nan"), 0.0]
            if kind == 2:
                msg["sent"] = now - 0.2
            if kind == 3:
                msg["position"] = [2.0, 0.0]
        ok, reason = valid(msg, now, last)
        counts[reason] = counts.get(reason, 0) + 1
        if ok:
            last = i
    accepted = counts.get("accepted", 0)
    metrics = dict(
        accepted_count=accepted,
        rejected_count=n - accepted,
        rejection_fraction=(n - accepted) / n,
        last_accepted_sequence=last,
    )
    derivation = [
        f"Generate {n} commands at 50 Hz with corruption probability {corrupt:g}.",
        "Corrupt name order, numeric finiteness, age or range in alternating injected cases.",
        "Validate the entire candidate before updating last accepted sequence.",
        f"Accepted {accepted} messages; rejected {n-accepted}.",
        f"Rejection reasons are {counts}.",
    ]
    notes = [
        "Rejected messages do not update the accepted sequence or active target in this contract example.",
        "A production parser must also handle missing keys, malicious payload sizes, schema versions and transport authentication.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"invalid_fraction": 0.1}
    parameters["invalid_fraction"] = [0.0, 0.01, 0.05, 0.1, 0.25, 0.5][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
