"""Control deadlines, jitter and tail-latency budgets. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(19)
    n = 10000
    period = p["period_ms"]
    sensing = rng.uniform(0.1, 0.3, n)
    transport = rng.uniform(0.1, 0.4, n)
    compute = np.maximum(0.05, rng.normal(0.7, 0.12, n))
    jitter = rng.exponential(p["jitter_mean_ms"], n)
    rare = rng.random(n) < 0.005
    jitter[rare] += 3.0
    elapsed = sensing + transport + compute + jitter
    metrics = dict(
        mean_completion_ms=np.mean(elapsed),
        p99_completion_ms=np.quantile(elapsed, 0.99),
        max_completion_ms=np.max(elapsed),
        deadline_miss_fraction=np.mean(elapsed > period),
        minimum_observed_margin_ms=period - np.max(elapsed),
    )
    derivation = [
        f"Generate {n} synthetic cycles with period {period:g} ms.",
        f'Exponential jitter mean is {p["jitter_mean_ms"]:g} ms, plus a 0.5% long-delay mechanism.',
        f"Mean completion is {np.mean(elapsed):.6f} ms.",
        f"The 99th percentile is {np.quantile(elapsed,.99):.6f} ms and worst observed is {np.max(elapsed):.6f} ms.",
        f"Missed-deadline fraction is {np.mean(elapsed>period):.6f}.",
    ]
    notes = [
        "Worst observed latency is not a proven worst-case bound; finite sampling can miss rarer events.",
        "The random workload is pedagogical. Real timing claims require instrumented measurements under declared stress conditions.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"period_ms": 2.0, "jitter_mean_ms": 0.1}
    parameters["jitter_mean_ms"] = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
