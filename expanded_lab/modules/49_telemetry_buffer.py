"""Ring buffers, bounded memory and time-window diagnostics. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    capacity = int(p["capacity"])
    rate = 500
    n = 5000
    buffer = np.zeros((capacity, 3))
    count = 0
    for i in range(n):
        t = i / rate
        buffer[count % capacity] = [t, np.sin(t), np.cos(t)]
        count += 1
    retained = min(count, capacity)
    if count <= capacity:
        snapshot = buffer[:retained].copy()
    else:
        start = count % capacity
        snapshot = np.concatenate([buffer[start:], buffer[:start]]).copy()
    assert np.all(np.diff(snapshot[:, 0]) > 0)
    expected_last = (n - 1) / rate
    assert np.isclose(snapshot[-1, 0], expected_last)
    horizon = snapshot[-1, 0] - snapshot[0, 0]
    metrics = dict(
        retained_samples=retained,
        horizon_s=horizon,
        allocated_bytes=buffer.nbytes,
        oldest_timestamp_s=snapshot[0, 0],
        latest_timestamp_s=snapshot[-1, 0],
    )
    derivation = [
        f"Write {n} samples at {rate} Hz into capacity {capacity}.",
        f"The allocated numerical storage is {buffer.nbytes} bytes.",
        f"After wrapping, retain {retained} most recent samples.",
        f"Chronological snapshot runs from {snapshot[0,0]:.6f} to {snapshot[-1,0]:.6f} s.",
        f"The retained diagnostic horizon is {horizon:.6f} s.",
    ]
    notes = [
        "Memory accounting covers the array payload, not interpreter, transport or rendering overhead.",
        "The example is single-threaded; concurrent producers/consumers require a reviewed synchronization or lock-free design.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"capacity": 1000}
    parameters["capacity"] = [100, 250, 500, 1000, 2000, 5000][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
