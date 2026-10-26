"""Allowlisted skills, bounded parameters and behavior outcomes. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def approve(request, ready, now):
    if not ready:
        return False, "not_ready"
    if request.get("skill") not in ("observe", "supported_wave"):
        return False, "unknown_skill"
    if not 0 <= now - request.get("sent", -100) <= 0.5:
        return False, "stale"
    if request["skill"] == "supported_wave":
        amplitude = request.get("amplitude")
        if not isinstance(amplitude, (int, float)) or not np.isfinite(amplitude):
            return False, "type"
        if not 0 <= amplitude <= 0.1:
            return False, "amplitude"
    return True, "approved"


def experiment(p):
    amplitude = p["amplitude"]
    now = 1.0
    requests = [
        dict(skill="supported_wave", amplitude=amplitude, sent=0.9),
        dict(skill="arbitrary_motor_code", amplitude=0.01, sent=0.9),
        dict(skill="supported_wave", amplitude=0.05, sent=0.0),
        dict(skill="observe", sent=0.9),
    ]
    decisions = [approve(r, True, now) for r in requests]
    approved = sum(x[0] for x in decisions)
    not_ready = approve(requests[0], False, now)
    assert not not_ready[0]
    metrics = dict(
        approved_requests=approved,
        rejected_requests=len(requests) - approved,
        requested_amplitude_rad=amplitude,
        primary_request_approved=float(decisions[0][0]),
        inactive_request_approved=float(not_ready[0]),
    )
    derivation = [
        f"The planner requests supported_wave amplitude {amplitude:g} rad.",
        "The allowlist contains observe and supported_wave only.",
        f"Decisions for normal, unknown, stale and observation requests are {decisions}.",
        f"Approved {approved} requests and rejected {len(requests)-approved}.",
        f"The same request with readiness false is rejected as {not_ready[1]}.",
    ]
    notes = [
        "Approval is permission to start a bounded skill; it is not proof the physical task completed.",
        "The executor still needs cancellation, tracking checks, timeout and a reviewed stop response.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"amplitude": 0.05}
    parameters["amplitude"] = [-0.05, 0.0, 0.025, 0.05, 0.1, 0.2][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
