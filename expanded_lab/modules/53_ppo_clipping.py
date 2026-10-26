"""PPO clipping, advantage signs and surrogate objectives. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    epsilon = p["clip_epsilon"]
    ratios = np.array([0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 1.5])
    advantage = np.array([-1.0, -0.5, 1.0, -0.2, 0.5, 1.0, -1.0])
    raw = ratios * advantage
    clipped = np.clip(ratios, 1 - epsilon, 1 + epsilon) * advantage
    objective = np.minimum(raw, clipped)
    active = np.abs(raw - objective) > 1e-12
    metrics = dict(
        policy_loss=-np.mean(objective),
        unclipped_loss=-np.mean(raw),
        objective_changed_fraction=np.mean(active),
        ratio_outside_clip_fraction=np.mean(
            (ratios < 1 - epsilon) | (ratios > 1 + epsilon)
        ),
        minimum_sample_objective=np.min(objective),
    )
    derivation = [
        f"Probability ratios are {ratios.tolist()}.",
        f"Advantages are {advantage.tolist()}; clipping epsilon is {epsilon:g}.",
        f"Unclipped sample objectives are {raw.tolist()}.",
        f"Apply the minimum with the clipped branch to obtain {objective.tolist()}.",
        f'Negative mean objective gives policy loss {metrics["policy_loss"]:.6f}.',
    ]
    notes = [
        "Ratio outside the clip interval is not identical to a changed surrogate contribution; advantage sign matters.",
        "This calculation omits value loss, entropy bonus, optimizer behavior and rollout collection.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"clip_epsilon": 0.2}
    parameters["clip_epsilon"] = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
