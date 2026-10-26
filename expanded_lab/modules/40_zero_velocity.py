"""Zero-velocity updates, foot constraints and slip bias. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(43)
    dt = 0.01
    t = np.arange(0, 6, dt)
    slip = p["slip_speed"]
    truth = np.where(t < 2, 0.0, np.where(t < 4, slip, 0.0))
    acceleration = np.gradient(truth, dt)
    measured = acceleration + 0.02 + rng.normal(0, 0.01, len(t))
    estimate = 0.0
    raw = 0.0
    errors = []
    raw_errors = []
    for i, a in enumerate(measured):
        raw += a * dt
        estimate += a * dt
        assumed_contact = (i % 20) == 0
        if assumed_contact:
            estimate = 0.2 * estimate
        errors.append(estimate - truth[i])
        raw_errors.append(raw - truth[i])
    metrics = dict(
        constrained_rmse_m_s=np.sqrt(np.mean(np.array(errors) ** 2)),
        unconstrained_rmse_m_s=np.sqrt(np.mean(np.array(raw_errors) ** 2)),
        slip_interval_bias_m_s=np.mean(np.array(errors)[(t >= 2) & (t < 4)]),
        final_constrained_error_m_s=errors[-1],
    )
    derivation = [
        f"The synthetic foot/body velocity is {slip:g} m/s during a two-second slip interval.",
        "Acceleration measurement includes +0.02 m/s^2 bias and 0.01 m/s^2 noise.",
        "Every 0.2 s, impose a strong zero-velocity pseudo-measurement regardless of actual slip.",
        f'Constrained RMSE is {metrics["constrained_rmse_m_s"]:.6f} m/s; unconstrained RMSE is {metrics["unconstrained_rmse_m_s"]:.6f} m/s.',
        f'Mean bias during slip is {metrics["slip_interval_bias_m_s"]:.6f} m/s.',
    ]
    notes = [
        "Zero-velocity constraints can reduce drift in valid stationary intervals and create systematic error during slip.",
        "Use contact confidence, slip indicators and innovation checks rather than permanently enforcing the constraint.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"slip_speed": 0.05}
    parameters["slip_speed"] = [0.0, 0.01, 0.03, 0.05, 0.1, 0.2][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
