#!/usr/bin/env python3
"""Emit a frozen, auditable certificate for one abstract structure.

This is deliberately structure-only: it does not enumerate ``(s, L)`` and
does not claim that passing the emitted necessary data gives a Leech tree.
The certificate retains the additive information that a ``(W, P)`` summary
loses, especially the forbidden low-depth differences coming from
``S_i - S_j``.
"""
from __future__ import annotations

import argparse
import json

from colored_moment_hall_audit import audit, ints, parse_struct


def structure_certificate(
    lowpar_tail: list[int], hpar: list[int], delta: int, order_n: int = 25
) -> dict:
    base = audit(lowpar_tail, hpar, delta, order_n)
    if not base["partition_ok"]:
        raise ValueError("H/S pair partition is incomplete")
    if not base["H_unique"] or not all(base["S_unique"]):
        raise ValueError("structure has an internal H or S collision")

    # Exact equivalent of T_i ∩ T_j = ∅:
    # 2(l_i-l_j) must avoid every element of S_i-S_j.  Store the forbidden
    # *depth differences* (raw difference divided by two), not the raw sums.
    forbidden = {}
    S = base["S"]
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            forbidden[f"{i},{j}"] = sorted(
                {
                    d // 2
                    for d in base["raw_sum_difference_sets"][f"{i},{j}"]
                    if d % 2 == 0
                }
            )

    return {
        "status": "TRANSLATED_DIFFERENCE_STRUCTURE_CERTIFICATE",
        "m": base["m"],
        "r": base["r"],
        "delta": base["delta"],
        "order_n": base["order_n"],
        "H": base["H"],
        "S": base["S"],
        "W": base["W"],
        "P": base["P"],
        "pair_total": base["pair_total"],
        "partition_ok": base["partition_ok"],
        "H_unique": base["H_unique"],
        "S_unique": base["S_unique"],
        "S_sums": [sum(values) for values in S],
        "S_parity": base["S_parity"],
        "raw_sum_difference_sets": base["raw_sum_difference_sets"],
        "forbidden_even_2depth_differences": forbidden,
        "wiener_affine": base["wiener_affine"],
        "wiener_target": base["wiener_target"],
        "source_scope": (
            "structure-only; no (s,L) enumeration; necessary certificate, "
            "not an existence proof"
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lowpar", required=True)
    ap.add_argument("--struct", required=True)
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--order-n", type=int, default=25)
    args = ap.parse_args()
    result = structure_certificate(
        ints(args.lowpar), parse_struct(args.struct), args.delta, args.order_n
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
