"""Linear inverted pendulum prediction and capture-point intuition. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    h, T = p["height"], p["horizon"]
    w = np.sqrt(9.81 / h)
    x0, v0, zmp = 0.02, 0.05, 0.0
    x = zmp + (x0 - zmp) * np.cosh(w * T) + v0 / w * np.sinh(w * T)
    v = (x0 - zmp) * w * np.sinh(w * T) + v0 * np.cosh(w * T)
    capture = x0 + v0 / w
    metrics = dict(
        natural_rate_per_s=w,
        final_com_x_m=x,
        final_speed_m_s=v,
        initial_capture_point_m=capture,
        divergent_growth_factor=np.exp(w * T),
    )
    derivation = [
        f"At height {h:g} m, omega=sqrt(9.81/h)={w:.6f} per second.",
        f"Start at x0={x0:g} m and v0={v0:g} m/s with ZMP zero.",
        f"Over {T:g} s, the hyperbolic solution predicts x={x:.6f} m and v={v:.6f} m/s.",
        f"The initial capture-point coordinate is {capture:.6f} m.",
        f"The divergent mode multiplies by exp(omega*T)={np.exp(w*T):.6f}.",
    ]
    notes = [
        "A fixed support point does not recover the displaced state in this open-loop model.",
        "A predicted capture point outside reachable/contact-feasible support is a warning, not an invitation to command an impossible step.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"height": 0.6, "horizon": 0.3}
    parameters["height"] = [0.3, 0.4, 0.5, 0.6, 0.8, 1.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
