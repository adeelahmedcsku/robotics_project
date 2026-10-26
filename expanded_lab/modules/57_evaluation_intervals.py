"""Fall rates, confidence intervals and finite evidence. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    n = int(p["trials"])
    failures = int(round(n * p["observed_fraction"]))
    phat = failures / n
    z = 1.959963984540054
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    half = z * np.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / denom
    zero_upper = 1 - 0.05 ** (1 / n)
    metrics = dict(
        observed_failure_fraction=phat,
        wilson_lower=max(0, center - half),
        wilson_upper=min(1, center + half),
        zero_failure_upper_if_applicable=zero_upper,
        observed_failures=failures,
    )
    derivation = [
        f"Use {n} trials and {failures} observed failures.",
        f"Observed fraction is {phat:.8f}.",
        f"The 95% Wilson interval is [{max(0,center-half):.8f},{min(1,center+half):.8f}].",
        f"If all {n} trials had zero failures, a one-sided 95% upper bound would be {zero_upper:.8f}.",
        "The zero-failure formula solves (1-p)^n=0.05 under the binomial independent-trial assumption.",
    ]
    notes = [
        "Changing the terrain, disturbance distribution or controller release changes the population to which these intervals apply.",
        "Repeated trials with shared initialization or correlated faults may provide less information than the independent model assumes.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"trials": 100, "observed_fraction": 0.02}
    parameters["trials"] = [10, 20, 50, 100, 500, 1000][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
