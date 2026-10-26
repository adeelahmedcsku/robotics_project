"""CAN bandwidth screening without invented motor commands. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    joints = int(p["joints"])
    rate = p["cycle_rate"]
    bits = p["frame_bits"]
    baud = p["bitrate"]
    frames = joints * p["frames_per_joint"] * rate
    demand = frames * bits
    utilization = demand / baud
    frame_time = bits / baud
    cycle_wire = joints * p["frames_per_joint"] * frame_time
    metrics = dict(
        frames_per_second=frames,
        required_bits_per_second=demand,
        utilization_fraction=utilization,
        one_frame_wire_time_us=frame_time * 1e6,
        minimum_cycle_wire_time_ms=cycle_wire * 1000,
    )
    derivation = [
        f'Plan {joints} joints at {rate:g} cycles/s with {p["frames_per_joint"]:g} frames per joint per cycle.',
        f"Frame demand is {frames:.6f} per second.",
        f"Assume {bits:g} total wire bits per frame at {baud:g} bit/s.",
        f"Required wire throughput is {demand:.6f} bit/s and utilization is {utilization:.6f}.",
        f"The minimum cycle wire time is {cycle_wire*1000:.6f} ms before additional contention or error handling.",
    ]
    notes = [
        (
            "The budget exceeds nominal bus capacity and is infeasible under these assumptions."
            if utilization > 1
            else "Nominal capacity is not exceeded, but margin and worst-case latency still need analysis."
        ),
        "The assumed frame length is a teaching budget input; confirm the actual bus generation, protocol and traffic pattern.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {
        "joints": 6,
        "cycle_rate": 500.0,
        "frame_bits": 135.0,
        "bitrate": 1000000.0,
        "frames_per_joint": 2.0,
    }
    parameters["cycle_rate"] = [50.0, 100.0, 200.0, 300.0, 500.0, 1000.0][
        args.case
    ]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
