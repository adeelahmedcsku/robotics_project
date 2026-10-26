"""Units, dimensional reasoning and motor-speed conversion. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rpm, ratio = p["rpm"], p["ratio"]
    torque, efficiency = p["motor_torque"], p["efficiency"]
    assert rpm > 0 and ratio > 0 and 0 < efficiency <= 1
    motor_speed = rpm * 2 * np.pi / 60
    joint_speed = motor_speed / ratio
    joint_torque = torque * ratio * efficiency
    input_power = torque * motor_speed
    output_power = joint_torque * joint_speed
    recovered_rpm = joint_speed * ratio * 60 / (2 * np.pi)
    assert abs(recovered_rpm - rpm) < 1e-9
    metrics = dict(
        joint_speed_rad_s=joint_speed,
        joint_torque_Nm=joint_torque,
        input_power_W=input_power,
        output_power_W=output_power,
        loss_W=input_power - output_power,
    )
    derivation = [
        f"Motor speed: {rpm:g} rev/min times 2*pi/60 = {motor_speed:.6f} rad/s.",
        f"Divide by ratio {ratio:g}: output speed = {joint_speed:.6f} rad/s.",
        f"Multiply input torque {torque:g} Nm by ratio and efficiency: {joint_torque:.6f} Nm.",
        f"Input mechanical power = {input_power:.6f} W; output = {output_power:.6f} W.",
        f"The difference, {input_power-output_power:.6f} W, is modeled mechanical loss.",
    ]
    notes = [
        f"The ideal power ratio is reduced to {efficiency:.3f}; a torque increase does not imply a power increase.",
        "This constant-efficiency model excludes speed-dependent loss, driver current and thermal limits.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {
        "rpm": 1200.0,
        "ratio": 36.0,
        "motor_torque": 0.3,
        "efficiency": 0.8,
    }
    parameters["ratio"] = [6.0, 12.0, 25.0, 36.0, 50.0, 100.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
