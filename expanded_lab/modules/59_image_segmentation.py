"""Color segmentation, false positives and image-space evidence. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    rng = np.random.default_rng(79)
    h, w = 120, 160
    image = np.ones((h, w, 3)) * 40
    truth = np.zeros((h, w), bool)
    truth[40:70, 90:120] = True
    image[truth] = [30, 180, 30]
    image[10:30, 10:30] = [40, 100, 40]
    noisy = np.clip(image + rng.normal(0, p["noise_std"], image.shape), 0, 255)
    mask = (noisy[:, :, 1] - noisy[:, :, 0] > 70) & (
        noisy[:, :, 1] - noisy[:, :, 2] > 70
    )
    tp = np.count_nonzero(mask & truth)
    fp = np.count_nonzero(mask & ~truth)
    fn = np.count_nonzero(~mask & truth)
    ys, xs = np.where(mask)
    centroid_error = (
        np.hypot(xs.mean() - 104.5, ys.mean() - 54.5) if len(xs) else 1000.0
    )
    metrics = dict(
        precision=tp / max(1, tp + fp),
        recall=tp / max(1, tp + fn),
        centroid_error_px=centroid_error,
        predicted_area_px=mask.sum(),
        false_positive_pixels=fp,
    )
    derivation = [
        "Place a 30x30 pixel bright-green target and a dimmer green distractor in a 160x120 image.",
        f'Add pixel-channel noise sigma={p["noise_std"]:g}.',
        "Threshold green excess over red and blue by 70 intensity units.",
        f'Count TP={tp}, FP={fp}, FN={fn}; precision={metrics["precision"]:.6f}, recall={metrics["recall"]:.6f}.',
        f"The predicted-mask centroid differs from the target center by {centroid_error:.6f} pixels.",
    ]
    notes = [
        "All foreground pixels are pooled, so distractors can shift the centroid; connected-component selection is an important extension.",
        "No depth or metric reach target is inferred from this mask.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"noise_std": 10.0}
    parameters["noise_std"] = [0.0, 5.0, 10.0, 20.0, 30.0, 50.0][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
