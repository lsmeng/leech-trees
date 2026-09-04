#!/usr/bin/env python3
"""Verify the small-A, positive-r LR bi-spider certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict

from bispider_smalla_positive_cleanroom import check_positive_tail
from bispider_smalla_positive_prover import prove_positive_tail


W = 20
EXPECTED = {
    "regimes": 50,
    "nodes": 87_885,
    "accepted_children": 87_835,
    "dead_states": 53_581,
    "frontier_states": 0,
    "max_depth": 20,
    "max_selected_vertices": 11,
    "sha256": "baf3929973241ec3b1a24673083d1d9fd6cb998f51c7e4b8fbccc22bfa62d87e",
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def primary_row(A: int):
    return asdict(prove_positive_tail(A, W))


def cleanroom_row(A: int):
    raw = asdict(check_positive_tail(A, W))
    return {
        "A": raw["A"],
        "W": raw["W"],
        "nodes": raw["nodes"],
        "accepted_children": raw["children"],
        "dead_states": raw["dead"],
        "deepest_missing_offset": raw["deepest"],
        "max_selected_vertices": raw["max_selected_vertices"],
        "frontier_states": raw["frontier"],
    }


def parallel_map(function, items, jobs: int):
    if jobs == 1:
        return [function(item) for item in items]
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        return list(executor.map(function, items, chunksize=1))


def row_digest(rows) -> str:
    ordered = sorted(rows, key=lambda row: row["A"])
    blob = json.dumps(ordered, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def summary(rows):
    return {
        "regimes": len(rows),
        "nodes": sum(row["nodes"] for row in rows),
        "accepted_children": sum(row["accepted_children"] for row in rows),
        "dead_states": sum(row["dead_states"] for row in rows),
        "frontier_states": sum(row["frontier_states"] for row in rows),
        "max_depth": max(row["deepest_missing_offset"] for row in rows),
        "max_selected_vertices": max(row["max_selected_vertices"] for row in rows),
        "sha256": row_digest(rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    require(args.jobs >= 1, "jobs must be positive")

    regimes = list(range(1, 51))
    primary = parallel_map(primary_row, regimes, args.jobs)
    primary_summary = summary(primary)
    require(
        primary_summary == EXPECTED,
        ("primary summary mismatch", primary_summary, EXPECTED),
    )
    cleanroom = parallel_map(cleanroom_row, regimes, args.jobs)
    require(cleanroom == primary, "clean-room per-A table mismatch")

    print(
        json.dumps(
            {
                "theorem_region": {
                    "anchor": "LR: N=A+Q+B, A<B",
                    "conditions": ["1<=A<=50", "B>20", "Q-(B-A)>20"],
                    "conclusion": "no Leech bi-spider extends the anchor",
                },
                "primary": primary_summary,
                "cleanroom_regimes": len(cleanroom),
                "cleanroom_sha256": row_digest(cleanroom),
                "cleanroom_match": True,
                "status": "VERIFIED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
