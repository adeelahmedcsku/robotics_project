"""Immutable experiment manifests and configuration identity. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np

import hashlib
import json


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def experiment(p):
    base = dict(
        model="sha256:model_example",
        policy="sha256:policy_example",
        calibration="calibration_r1",
        seed=7,
        control_period=0.02,
        action_scale=0.15,
    )
    modified = dict(base)
    modified["action_scale"] = p["action_scale"]
    h0 = digest(base)
    h1 = digest(modified)
    reordered = {k: modified[k] for k in reversed(list(modified))}
    assert digest(reordered) == h1
    changed = [k for k in base if base[k] != modified[k]]
    metrics = dict(
        content_identity_changed=float(h0 != h1),
        changed_field_count=len(changed),
        action_scale=p["action_scale"],
        scale_ratio_to_baseline=p["action_scale"] / 0.15,
    )
    derivation = [
        f"Baseline fields are {base}.",
        f'Change action_scale to {p["action_scale"]:g}; changed fields are {changed}.',
        f"Baseline canonical manifest hash is {h0}.",
        f"Candidate canonical manifest hash is {h1}.",
        "Reordering dictionary insertion order preserves the canonical hash, verified by assertion.",
    ]
    notes = [
        "The model/policy hash strings are explicit fictional labels in this unit exercise; a real manifest must hash actual file bytes.",
        "A hash detects content changes but does not prove provenance, authenticity, compatibility or safety.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"action_scale": 0.15}
    parameters["action_scale"] = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
