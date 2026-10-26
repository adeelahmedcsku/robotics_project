"""Sampling, aliasing and the difference between signal and display rate. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    fs, frequency, T = p["sample_rate"], p["signal_frequency"], p["duration"]
    n = max(4, int(fs * T))
    t = np.arange(n) / fs
    x = np.sin(2 * np.pi * frequency * t)
    alias = abs((frequency + fs / 2) % fs - fs / 2)
    spectrum = np.abs(np.fft.rfft(x))
    frequencies = np.fft.rfftfreq(n, 1 / fs)
    peak = float(frequencies[np.argmax(spectrum)])
    metrics = dict(
        nyquist_Hz=fs / 2,
        alias_Hz=alias,
        fft_peak_Hz=peak,
        samples=n,
        sampled_rms=float(np.sqrt(np.mean(x * x))),
    )
    derivation = [
        f"Sample a {frequency:g} Hz sinusoid at {fs:g} samples per second.",
        f"The sample interval is {1/fs:.6f} s and Nyquist frequency is {fs/2:.6f} Hz.",
        f"The analytical alias frequency is {alias:.6f} Hz.",
        f"An {n}-sample FFT resolves bins spaced {fs/n:.6f} Hz; peak bin is {peak:.6f} Hz.",
        f"Sampled RMS is {np.sqrt(np.mean(x*x)):.6f}; exact coincidences can produce misleading zeros.",
    ]
    notes = [
        (
            "Signal lies below Nyquist, but practical reconstruction still needs filtering assumptions."
            if frequency < fs / 2
            else "The original signal cannot be uniquely recovered from these samples without extra information."
        ),
        "FFT leakage depends on record duration and windowing; a peak bin alone is not a precision frequency estimate.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"sample_rate": 100.0, "signal_frequency": 35.0, "duration": 2.0}
    parameters["sample_rate"] = [20.0, 40.0, 60.0, 80.0, 100.0, 200.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
