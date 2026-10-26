"""Integral action, saturation and anti-windup. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def simulate(cap, anti):
    q = v = integral = 0.0
    dt = 0.002
    history = []
    saturated = 0
    for k in range(2000):
        target = 0.5 if k < 500 else 0.0
        error = target - q
        raw = 12 * error + 10 * integral - 2 * v
        u = np.clip(raw, -cap, cap)
        if not anti or abs(raw) <= cap or error * (raw - u) <= 0:
            integral += dt * error
        v += dt * (u - 0.2 * v) / 0.2
        q += dt * v
        history.append(q)
        saturated += abs(raw) > cap
    return np.array(history), integral, saturated / 2000


def experiment(p):
    cap = p["torque_cap"]
    plain, ip, sp = simulate(cap, False)
    protected, ia, sa = simulate(cap, True)
    metrics = dict(
        plain_final_error_rad=abs(plain[-1]),
        protected_final_error_rad=abs(protected[-1]),
        plain_integral=ip,
        protected_integral=ia,
        plain_saturation_fraction=sp,
        protected_saturation_fraction=sa,
    )
    derivation = [
        f"Use symmetric actuator limit +/-{cap:g} Nm.",
        "Request 0.5 rad for one second, then return the target to zero.",
        f"Without anti-windup, saturation fraction is {sp:.6f} and final integral is {ip:.6f}.",
        f"Conditional integration gives saturation fraction {sa:.6f} and integral {ia:.6f}.",
        f"Final absolute errors are {abs(plain[-1]):.6f} and {abs(protected[-1]):.6f} rad respectively.",
    ]
    notes = [
        "Anti-windup improves consistency with actuator authority but does not guarantee every transient metric improves.",
        "Integral state must also be handled explicitly when changing modes, resetting faults or switching controllers.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"torque_cap": 1.0}
    parameters["torque_cap"] = [0.1, 0.25, 0.5, 1.0, 2.0, 5.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
