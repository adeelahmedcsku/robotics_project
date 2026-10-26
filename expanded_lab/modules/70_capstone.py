"""An integrated synthetic joint with perception, gating and fault recovery. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    dt = 0.002
    duration = 4.0
    n = round(duration / dt)
    timeout = 0.1
    q = v = 0.0
    state = "OBSERVE"
    last_sent = 0.0
    fault_time = None
    errors = []
    max_torque = 0.0
    object_visible = True
    drop_at = p["dropout_start"]
    for k in range(n):
        t = k * dt
        if state == "OBSERVE" and object_visible:
            state = "EXECUTE"
        if t < drop_at:
            last_sent = t
        if t - last_sent > timeout and state == "EXECUTE":
            state = "FAULT"
            fault_time = t
        target = 0.05 * (1 - np.cos(2 * np.pi * min(t, 3.0) / 3.0))
        torque = (
            np.clip(8 * (target - q) - 1.2 * v, -0.5, 0.5)
            if state == "EXECUTE"
            else 0.0
        )
        v += dt * (torque - 0.2 * v) / 0.05
        q += dt * v
        errors.append(target - q)
        max_torque = max(max_torque, abs(torque))
    metrics = dict(
        final_position_rad=q,
        peak_applied_torque_Nm=max_torque,
        tracking_rmse_rad=np.sqrt(np.mean(np.array(errors) ** 2)),
        fault_latched=float(state == "FAULT"),
        fault_time_s=-1 if fault_time is None else fault_time,
    )
    derivation = [
        "The synthetic object observation enables only a predefined 0.1 rad peak supported-style gesture.",
        f"Command refresh stops at t={drop_at:g} s; timeout is {timeout:g} s.",
        "A stale command latches FAULT and removes torque authority in this unloaded numerical plant.",
        f"Final state is {state}; fault time is {fault_time}.",
        f'Peak torque is {max_torque:.6f} Nm; final position is {q:.6f} rad and RMSE is {metrics["tracking_rmse_rad"]:.6f} rad.',
    ]
    notes = [
        "Zero torque after a fault is suitable only for this explicitly unloaded damped synthetic plant; a loaded physical robot needs a reviewed support/stop strategy.",
        "No automatic healthy-message transition leaves the fault state, and no physical bus is opened.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"dropout_start": 2.0}
    parameters["dropout_start"] = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
