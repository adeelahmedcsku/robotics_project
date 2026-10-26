"""Landed cost, VAT, contingency and scope decisions. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np


def experiment(p):
    motors = int(p["motor_count"])
    unit = p["motor_allowance"]
    eu_gross = 350.0
    import_net = motors * unit
    shipping = 120.0
    tax = 0.19
    fabrication = 600.0
    protection = 700.0
    contingency = 0.15
    import_landed = (import_net + shipping) * (1 + tax)
    subtotal = eu_gross + import_landed + fabrication + protection
    reserve = subtotal * contingency
    total = subtotal + reserve
    metrics = dict(
        import_landed_EUR=import_landed,
        subtotal_EUR=subtotal,
        reserve_EUR=reserve,
        total_stage_EUR=total,
        budget_margin_EUR=6000 - total,
    )
    derivation = [
        f"This hypothetical stage contains {motors} motors at an internal allowance of EUR {unit:g} each.",
        f"Net import allowance EUR {import_net:g} plus EUR 120 shipping is taxed at an assumed 19%.",
        f"Import landed cost is EUR {import_landed:.2f}; EU gross, fabrication and protection give subtotal EUR {subtotal:.2f}.",
        f"Reserve 15% contingency: EUR {reserve:.2f}.",
        f"Total is EUR {total:.2f}; margin against EUR 6,000 is EUR {6000-total:.2f}.",
    ]
    notes = [
        "Every amount here is a teaching allowance. Actual VAT jurisdiction, customs treatment, supplier terms and compatibility must be checked.",
        "A negative margin means reduce scope or increase funding; essential protection is not the balancing item.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"motor_count": 3, "motor_allowance": 400.0}
    parameters["motor_count"] = [1, 2, 3, 4, 6, 12][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
