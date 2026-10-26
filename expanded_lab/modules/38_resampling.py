"""Timestamps, interpolation and asynchronous sensor streams. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    offset = p["offset"]
    fs = p["sample_rate"]
    frequency = 2.0
    reference_t = np.arange(0.2, 2.8, 0.005)
    sensor_t = np.arange(0, 3, 1 / fs)
    measured = np.sin(2 * np.pi * frequency * (sensor_t + offset))
    truth = np.sin(2 * np.pi * frequency * reference_t)
    naive = np.interp(reference_t, sensor_t, measured)
    corrected = np.interp(reference_t, sensor_t + offset, measured)
    metrics = dict(
        naive_alignment_rmse=np.sqrt(np.mean((naive - truth) ** 2)),
        corrected_alignment_rmse=np.sqrt(np.mean((corrected - truth) ** 2)),
        nominal_phase_error_rad=2 * np.pi * frequency * offset,
        sensor_interval_s=1 / fs,
    )
    derivation = [
        f"The signal is a 2 Hz sinusoid sampled at {fs:g} Hz.",
        f"Sensor timestamp offset is {offset:g} s, equivalent to phase {2*np.pi*frequency*offset:.6f} rad.",
        "Naive interpolation treats nominal sensor times as correct.",
        f'Naive RMSE is {metrics["naive_alignment_rmse"]:.6f}.',
        f'Adding the known offset before interpolation reduces RMSE to {metrics["corrected_alignment_rmse"]:.6f}.',
    ]
    notes = [
        "Residual after offset correction includes interpolation error from finite sampling.",
        "An unknown or drifting clock offset requires estimation and validity limits; arrival time is not a substitute for sample time.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"offset": 0.01, "sample_rate": 100.0}
    parameters["offset"] = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
