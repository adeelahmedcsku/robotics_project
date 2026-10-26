"""Camera intrinsics, projection and pixel-error sensitivity. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    Z = p["depth"]
    fx, fy, cx, cy = 400.0, 410.0, 320.0, 240.0
    X, Y = 0.1, -0.05
    sigma = p["pixel_noise"]
    assert Z > 0
    u = fx * X / Z + cx
    v = fy * Y / Z + cy
    reconstructed = np.array([(u - cx) * Z / fx, (v - cy) * Z / fy, Z])
    error = np.linalg.norm(reconstructed - [X, Y, Z])
    lateral = Z * sigma / fx
    metrics = dict(
        pixel_u=u,
        pixel_v=v,
        lateral_uncertainty_m=lateral,
        roundtrip_error_m=error,
        projection_scale_px_per_m=fx / Z,
    )
    derivation = [
        f"Use fx={fx:g}, fy={fy:g}, cx={cx:g}, cy={cy:g} pixels.",
        f"Project point (0.1,-0.05,{Z:g}) m.",
        f"Pixel result is u={u:.6f}, v={v:.6f}.",
        f"Assuming exact known depth, inverse projection returns {reconstructed.tolist()} m.",
        f"Pixel noise sigma={sigma:g} px maps to lateral sigma approximately {lateral:.6f} m.",
    ]
    notes = [
        "The inverse result requires known depth; a monocular pixel alone does not identify a metric 3-D point.",
        "Distortion, rolling shutter, calibration uncertainty and camera-to-body extrinsics are excluded here.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"depth": 1.0, "pixel_noise": 1.0}
    parameters["depth"] = [0.2, 0.5, 1.0, 2.0, 3.0, 5.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
