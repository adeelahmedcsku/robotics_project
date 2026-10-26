"""A synthetic packet codec and corruption tests. Numerical teaching experiment only."""

import math
import json
import argparse
import numpy as np

import struct


def crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = (
                ((crc << 1) ^ 0x1021) & 0xFFFF
                if crc & 0x8000
                else (crc << 1) & 0xFFFF
            )
    return crc


def encode(sequence, target):
    payload = struct.pack("<2sBIf", b"ED", 1, sequence, target)
    return payload + struct.pack("<H", crc16(payload))


def decode(packet):
    if len(packet) != 13:
        raise ValueError("length")
    payload, check = packet[:-2], struct.unpack("<H", packet[-2:])[0]
    if crc16(payload) != check:
        raise ValueError("crc")
    magic, version, sequence, target = struct.unpack("<2sBIf", payload)
    if magic != b"ED" or version != 1:
        raise ValueError("schema")
    if not np.isfinite(target) or abs(target) > 0.5:
        raise ValueError("target")
    return sequence, target


def experiment(p):
    rng = np.random.default_rng(59)
    rejected = 0
    n = 500
    target = p["target"]
    base = encode(7, target)
    seq, recovered = decode(base)
    for _ in range(n):
        damaged = bytearray(base)
        index = int(rng.integers(0, len(base)))
        damaged[index] ^= 1 << int(rng.integers(0, 8))
        try:
            decode(damaged)
        except ValueError:
            rejected += 1
    assert seq == 7 and rejected == n
    metrics = dict(
        packet_bytes=len(base),
        target_roundtrip_error_rad=abs(recovered - target),
        single_bit_faults_rejected=rejected,
        rejection_fraction=rejected / n,
    )
    derivation = [
        f"Encode sequence 7 and target {target:g} rad with explicit little-endian fields.",
        f"The complete fictional packet occupies {len(base)} bytes.",
        f"Float32 round-trip error is {abs(recovered-target):.9e} rad.",
        f"Inject {n} random single-bit corruptions across payload and checksum.",
        f"Reject {rejected} corrupted packets; no physical transport exists.",
    ]
    notes = [
        "CRC detects accidental corruption; it is not authentication or a defense against a deliberate sender.",
        "This CRC and packet layout are teaching choices, not the CAN wire format or Asimov motor protocol.",
    ]
    return metrics, derivation, notes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0, choices=range(6))
    args = parser.parse_args()
    parameters = {"target": 0.1}
    parameters["target"] = [-0.4, -0.1, 0.0, 0.1, 0.25, 0.4][args.case]
    metrics, derivation, notes = experiment(parameters)
    result = dict(
        parameters=parameters,
        metrics={k: float(v) for k, v in metrics.items()},
        derivation=derivation,
        notes=notes,
    )
    print(json.dumps(result, indent=2))
