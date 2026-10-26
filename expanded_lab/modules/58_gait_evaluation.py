"""Gait phase metrics, contact slip and energy accounting. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    t = np.arange(0, 10, 0.01)
    dt = 0.01
    command = 0.2
    velocity = command + 0.02 * np.sin(2 * np.pi * 0.7 * t)
    position = np.cumsum(velocity) * dt
    phase = (t % 1.0) < 0.6
    foot_speed = np.where(phase, p["stance_slip"], 0.3 * np.sin(2 * np.pi * t))
    power = 12 + 8 * np.sin(2 * np.pi * t)
    distance = float(np.sum(abs(np.diff(position))))
    slip = np.sqrt(np.mean(foot_speed[phase] ** 2))
    metrics = dict(
        distance_m=distance,
        velocity_rmse_m_s=np.sqrt(np.mean((velocity - command) ** 2)),
        stance_slip_rms_m_s=slip,
        all_phase_foot_speed_rms_m_s=np.sqrt(np.mean(foot_speed**2)),
        positive_mechanical_work_J=np.trapezoid(np.maximum(power, 0), t),
        stance_fraction=np.mean(phase),
    )
    derivation = [
        "Create a ten-second synthetic trajectory commanded at 0.2 m/s.",
        f'Loaded-stance foot speed is {p["stance_slip"]:g} m/s; swing motion is excluded from the slip metric.',
        f'Distance is {distance:.6f} m and velocity RMSE is {metrics["velocity_rmse_m_s"]:.6f} m/s.',
        f'Stance-only slip RMS is {slip:.6f} m/s while all-phase RMS is {metrics["all_phase_foot_speed_rms_m_s"]:.6f} m/s.',
        f'Positive mechanical work is {metrics["positive_mechanical_work_J"]:.6f} J.',
    ]
    notes = [
        "These traces are synthetic metric fixtures, not walking results from the Asimov model.",
        "Mechanical work is not battery energy; physical electrical measurements require voltage/current timing and regeneration accounting.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"stance_slip": 0.01}
    parameters["stance_slip"] = [0.0, 0.002, 0.005, 0.01, 0.03, 0.1][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
