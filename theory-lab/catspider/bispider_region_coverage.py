#!/usr/bin/env python3
"""Count exact LR anchors covered by the uniform bi-spider regions."""

from __future__ import annotations

import argparse
import json

from bispider_cleanroom import Geometry, State, distance_values


def count_order(n: int) -> dict:
    N = n * (n - 1) // 2
    valid = balanced = dominant = bounded_strip = positive_extension = 0
    small_b_positive = small_a_negative = 0
    covered = uncovered_large_A = 0
    for A in range(1, N // 2 + 1):
        for B in range(A + 1, N - A):
            Q = N - A - B
            geometry = Geometry(Q, (A,), A - 1, (B,), B - 1)
            initial = State(((A,),), (), ((B,),))
            if distance_values(initial, geometry, N) is None:
                continue
            valid += 1
            imbalance = Q - (B - A)
            in_balanced = A > 20 and imbalance > 20
            in_dominant = A > 15 and imbalance < -15
            in_strip = A > 50 and -15 <= imbalance <= 20
            in_positive_extension = A <= 50 and B > 20 and imbalance > 20
            in_small_b_positive = B <= 20 and imbalance > 20
            in_small_a_negative = A <= 15 and imbalance < -15
            balanced += in_balanced
            dominant += in_dominant
            bounded_strip += in_strip
            # Report only the genuinely new part of theorem D; its A>20 part
            # overlaps theorem A.
            positive_extension += in_positive_extension and not in_balanced
            small_b_positive += in_small_b_positive
            small_a_negative += in_small_a_negative
            in_union = (
                in_balanced
                or in_dominant
                or in_strip
                or in_positive_extension
                or in_small_b_positive
                or in_small_a_negative
            )
            covered += in_union
            uncovered_large_A += A > 50 and not in_union
    return {
        "n": n,
        "N": N,
        "valid_lr_anchors": valid,
        "balanced_region": balanced,
        "dominant_region": dominant,
        "bounded_strip_region": bounded_strip,
        "small_A_positive_new_region": positive_extension,
        "small_B_positive_region": small_b_positive,
        "small_A_negative_region": small_a_negative,
        "covered": covered,
        "uncovered": valid - covered,
        "uncovered_with_A_gt_50": uncovered_large_A,
        "covered_percent": round(100 * covered / valid, 3) if valid else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("orders", type=int, nargs="*", default=(18, 25, 27, 36, 51))
    args = parser.parse_args()
    print(json.dumps([count_order(n) for n in args.orders], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
