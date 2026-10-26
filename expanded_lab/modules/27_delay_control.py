"""Feedback delay, sample-and-hold and tracking degradation. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    dt = 0.001
    delay = p["delay"]
    d = max(0, round(delay / dt))
    q = v = 0.0
    states = [(0.0, 0.0)] * (d + 1)
    errors = []
    torques = []
    for k in range(3000):
        t = k * dt
        target = 0.1 * np.sin(2 * np.pi * 0.5 * t)
        oldq, oldv = states[max(0, len(states) - 1 - d)]
        u = np.clip(20 * (target - oldq) - 2 * oldv, -3, 3)
        v += dt * (u - 0.1 * v) / 0.08
        q += dt * v
        states.append((q, v))
        errors.append(target - q)
        torques.append(u)
    errors = np.array(errors)
    torques = np.array(torques)
    metrics = dict(
        actual_delay_s=d * dt,
        tracking_rmse_rad=np.sqrt(np.mean(errors**2)),
        peak_error_rad=np.max(abs(errors)),
        saturation_fraction=np.mean(abs(torques) >= 2.999),
    )
    derivation = [
        f"Request delay {delay:g} s; rounding to 1 ms samples gives {d} delayed samples.",
        "The reference is a 0.1 rad, 0.5 Hz sinusoid; gains remain Kp=20 and Kd=2.",
        "Use delayed position and velocity but the current reference to calculate torque.",
        f"After three seconds, RMSE is {np.sqrt(np.mean(errors**2)):.6f} rad.",
        f'Peak error is {np.max(abs(errors)):.6f} rad and saturation fraction is {metrics["saturation_fraction"]:.6f}.',
    ]
    notes = [
        "The chosen delay is deterministic; real transport also has jitter, dropouts and timestamp uncertainty.",
        "A simulator with immediate state access can substantially overestimate the usable gain margin.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"delay": 0.01}
    parameters["delay"] = [0.0, 0.002, 0.005, 0.01, 0.02, 0.05][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
