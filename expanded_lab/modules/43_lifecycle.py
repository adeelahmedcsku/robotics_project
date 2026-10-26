"""Lifecycle activation, preconditions and fault latching. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def transition(state, event, ready):
    if event == "shutdown":
        return "finalized"
    if event == "fault" and state == "active":
        return "fault"
    if state == "unconfigured" and event == "configure":
        return "inactive"
    if state == "inactive" and event == "activate" and all(ready.values()):
        return "active"
    if state == "active" and event == "deactivate":
        return "inactive"
    if state == "fault" and event == "reset":
        return "inactive"
    return state


def experiment(p):
    rng = np.random.default_rng(53)
    trials = 200
    activations = 0
    blocked = 0
    faults = 0
    unsafe_resume = 0
    for _ in range(trials):
        ready = {
            k: rng.random() >= p["failed_readiness_probability"]
            for k in ["calibration", "limits", "feedback", "support"]
        }
        state = transition("unconfigured", "configure", ready)
        state = transition(state, "activate", ready)
        if state == "active":
            activations += 1
            state = transition(state, "fault", ready)
            faults += 1
            state = transition(state, "healthy_packet", ready)
            unsafe_resume += state == "active"
        else:
            blocked += 1
    assert unsafe_resume == 0
    metrics = dict(
        activation_count=activations,
        blocked_count=blocked,
        fault_count=faults,
        automatic_resume_count=unsafe_resume,
        activation_fraction=activations / trials,
    )
    derivation = [
        f'Run {trials} readiness trials with per-flag failure probability {p["failed_readiness_probability"]:g}.',
        "Configuration moves the supervisor to inactive; activation checks all four readiness flags.",
        f"Activate {activations} trials and block {blocked}.",
        f"Inject a fault into every active trial, then deliver a healthy packet.",
        f"Automatic active resumption count is {unsafe_resume}; the assertion requires zero.",
    ]
    notes = [
        "Readiness flags represent evidence that must exist outside this synthetic state machine.",
        "A reset returns to inactive; a new reviewed activation is required before motion can resume.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"failed_readiness_probability": 0.1}
    parameters["failed_readiness_probability"] = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5][
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
