"""Fault persistence, debounce and explicit re-arming. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    dt = 0.01
    t = np.arange(0, 5, dt)
    signal = np.ones(len(t)) * 30.0
    signal[50] = 90.0
    signal[100:102] = 90.0
    signal[t >= 3] = 90.0
    required = max(1, round(p["debounce_seconds"] / dt))
    count = 0
    latched = False
    first = None
    false_before = 0
    for i, value in enumerate(signal):
        count = count + 1 if value > 70 else 0
        if count >= required and not latched:
            latched = True
            first = t[i]
            false_before += t[i] < 3
    latency = -1.0 if first is None else first - 3.0
    metrics = dict(
        required_bad_samples=required,
        first_latch_time_s=-1 if first is None else first,
        detection_latency_from_sustained_fault_s=latency,
        false_latch_before_fault=false_before,
        latched_final=float(latched),
    )
    derivation = [
        f'At 100 Hz, debounce duration {p["debounce_seconds"]:g} s becomes {required} consecutive samples.',
        "Inject a one-sample spike at 0.5 s and a two-sample spike at 1 s.",
        "At 3 s, begin a sustained threshold violation.",
        f"First latched fault occurs at {first} s; early false-latch count is {false_before}.",
        f"Relative to sustained-fault onset, reported latency is {latency:.6f} s; a negative value means an earlier spike already latched.",
    ]
    notes = [
        "The temperature values and threshold are synthetic and do not specify a physical motor limit.",
        "Detection delay must be included in the reviewed response envelope; debouncing every fault category identically is inappropriate.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"debounce_seconds": 0.05}
    parameters["debounce_seconds"] = [0.01, 0.02, 0.03, 0.05, 0.1, 0.2][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
