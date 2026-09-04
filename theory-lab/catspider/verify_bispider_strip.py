#!/usr/bin/env python3
"""Verify the all-h bounded-imbalance LR offset certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict

from bispider_strip_cleanroom import (
    admissible_h_values as cleanroom_h_values,
    prove_strip_cleanroom,
)
from bispider_strip_prover import admissible_h_values, prove_strip


W = 50
EXPECTED = {
    "regimes": 1956,
    "nodes": 2_402_716,
    "frontier_states": 0,
    "max_depth": 46,
    "max_marks": 12,
    "sha256": "b445823ef3fc6541f4e7e260260376fdf4a76f0c0d54d577e56b39619458add8",
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def regimes():
    return [
        (r, h)
        for r in range(-15, 21)
        for h in admissible_h_values(W, r)
    ]


def primary_row(pair):
    r, h = pair
    return asdict(prove_strip(W, r, h))


def cleanroom_row(pair):
    r, h = pair
    raw = asdict(prove_strip_cleanroom(W, r, h))
    return {
        "W": raw["W"],
        "r": raw["r"],
        "h": raw["h"],
        "nodes": raw["nodes"],
        "accepted_children": raw["children"],
        "dead_states": raw["dead"],
        "deepest_missing_offset": raw["deepest"],
        "max_marks": raw["max_marks"],
        "frontier_states": raw["frontier"],
    }


def row_digest(rows) -> str:
    ordered = sorted(rows, key=lambda row: (row["r"], row["h"]))
    blob = json.dumps(ordered, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def invariant_signature(row):
    """Statistics that must be unchanged throughout the representative tail."""

    return {key: value for key, value in row.items() if key != "h"}


def selected_cleanroom_regimes(all_regimes):
    selected = set()
    for r in range(-15, 21):
        hs = list(admissible_h_values(W, r))
        selected.add((r, hs[0]))
        selected.add((r, hs[len(hs) // 2]))
        selected.add((r, hs[-1]))
    selected.add((-1, 15))  # unique maximum-depth primary regime
    return [pair for pair in all_regimes if pair in selected]


def parallel_map(function, items, jobs: int):
    if jobs == 1:
        return [function(item) for item in items]
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        return list(executor.map(function, items, chunksize=1))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--full-cleanroom", action="store_true")
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    require(args.jobs >= 1, "jobs must be positive")

    all_regimes = regimes()
    for r in range(-15, 21):
        require(
            admissible_h_values(W, r) == cleanroom_h_values(W, r),
            ("h partition mismatch", r),
        )
    primary = parallel_map(primary_row, all_regimes, args.jobs)
    summary = {
        "regimes": len(primary),
        "nodes": sum(row["nodes"] for row in primary),
        "frontier_states": sum(row["frontier_states"] for row in primary),
        "max_depth": max(row["deepest_missing_offset"] for row in primary),
        "max_marks": max(row["max_marks"] for row in primary),
        "sha256": row_digest(primary),
    }
    require(summary == EXPECTED, ("primary summary", summary, EXPECTED))

    clean_regimes = all_regimes if args.full_cleanroom else selected_cleanroom_regimes(all_regimes)
    cleanroom = parallel_map(cleanroom_row, clean_regimes, args.jobs)
    primary_by_key = {(row["r"], row["h"]): row for row in primary}
    for row in cleanroom:
        require(
            row == primary_by_key[(row["r"], row["h"])],
            ("cleanroom mismatch", row, primary_by_key[(row["r"], row["h"])]),
        )

    # The proof shows that the first admissible h above the critical bound
    # represents its entire parity tail.  Recompute the next h in both
    # implementations as a guard against retaining an accidental h-dependent
    # comparison in either program.
    tail_next = [
        (r, admissible_h_values(W, r)[-1] + 2)
        for r in range(-15, 21)
    ]
    tail_primary = parallel_map(primary_row, tail_next, args.jobs)
    tail_cleanroom = parallel_map(cleanroom_row, tail_next, args.jobs)
    for primary_row_next, cleanroom_row_next in zip(
        tail_primary, tail_cleanroom, strict=True
    ):
        r = primary_row_next["r"]
        tail = admissible_h_values(W, r)[-1]
        require(
            invariant_signature(primary_row_next)
            == invariant_signature(primary_by_key[(r, tail)]),
            ("primary tail instability", r, tail, primary_row_next),
        )
        require(
            cleanroom_row_next == primary_row_next,
            ("cleanroom tail mismatch", r, primary_row_next, cleanroom_row_next),
        )

    result = {
        "theorem_region": {
            "anchor": "LR: N=A+Q+B, A<B",
            "conditions": ["A>50", "-15<=Q-(B-A)<=20"],
            "conclusion": "no Leech bi-spider extends the anchor",
        },
        "primary": summary,
        "cleanroom_regimes": len(cleanroom),
        "cleanroom_scope": "full" if args.full_cleanroom else "boundary sample",
        "cleanroom_match": True,
        "tail_stability_regimes": len(tail_next),
        "tail_stability_match": True,
        "status": "VERIFIED",
    }
    if args.full_cleanroom:
        result["cleanroom_sha256"] = row_digest(cleanroom)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
