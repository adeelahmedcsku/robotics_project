"""Commissioning evidence as a dependency graph. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    graph = {
        "inspection": [],
        "isolation": ["inspection"],
        "single_joint": ["isolation"],
        "calibration": ["single_joint"],
        "supported_limb": ["calibration"],
        "physical_skill": ["supported_limb"],
        "walking": ["physical_skill"],
    }
    stale_index = int(p["stale_gate_index"])
    keys = list(graph)
    records = {k: dict(status="PASS", revision="r1") for k in keys}
    if stale_index >= 0:
        records[keys[stale_index]]["revision"] = "r0"
    memo = {}

    def passes(name):
        if name in memo:
            return memo[name]
        own = (
            records[name]["status"] == "PASS"
            and records[name]["revision"] == "r1"
        )
        memo[name] = own and all(passes(dep) for dep in graph[name])
        return memo[name]

    results = {k: passes(k) for k in keys}
    metrics = dict(
        passing_gate_count=sum(results.values()),
        blocked_gate_count=sum(not v for v in results.values()),
        supported_limb_ready=float(results["supported_limb"]),
        physical_skill_ready=float(results["physical_skill"]),
        walking_ready=float(results["walking"]),
    )
    derivation = [
        f"The synthetic gate order is {keys}.",
        f"Stale gate index is {stale_index}; records must match revision r1.",
        "Evaluate each gate recursively, requiring all prerequisite evidence.",
        f"Results are {results}.",
        f"Total passing count is {sum(results.values())}; blocked count is {sum(not v for v in results.values())}.",
    ]
    notes = [
        "All PASS records here are artificial test fixtures, not physical commissioning evidence.",
        "A real record should include procedure, threshold rationale, instrument, raw artifact, date, reviewer and exact configuration.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"stale_gate_index": 2}
    parameters["stale_gate_index"] = [-1, 0, 1, 2, 4, 6][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
