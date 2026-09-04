#!/usr/bin/env python3
"""Verify the finite certificate for every LR anchor with r<-15."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict

from bispider_smalla_negative_cleanroom import search
from bispider_smalla_negative_prover import prove_negative_tail


W = 15
EXPECTED_CORE = {
    "regimes": 570,
    "nodes": 78_835,
    "accepted_children": 78_280,
    "dead_states": 43_776,
    "frontier_states": 0,
    "invalid_initial": 15,
    "max_depth": 15,
    "max_selected_vertices": 11,
    "sha256": "eed4b9ab8075fa09499a472c281d563629b4eb6c76fdf8c6f7dc48ca498f0308",
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def regimes():
    return [
        (A, C, W)
        for A in range(1, 16)
        for C in (*range(A + 1, 46), 46)
    ]


def primary_row(regime):
    return asdict(prove_negative_tail(*regime))


def cleanroom_row(regime):
    raw = asdict(search(*regime))
    return {
        "A": raw["A"],
        "C": raw["C"],
        "W": raw["W"],
        "nodes": raw["nodes"],
        "accepted_children": raw["children"],
        "dead_states": raw["dead"],
        "deepest_missing_offset": raw["deepest"],
        "frontier_states": raw["frontier"],
        "invalid_initial": raw["invalid_initial"],
        "max_selected_vertices": raw["max_vertices"],
    }


def parallel_map(function, items, jobs: int):
    if jobs == 1:
        return [function(item) for item in items]
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        return list(executor.map(function, items, chunksize=5))


def row_digest(rows) -> str:
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def summarize(rows):
    return {
        "regimes": len(rows),
        "nodes": sum(row["nodes"] for row in rows),
        "accepted_children": sum(row["accepted_children"] for row in rows),
        "dead_states": sum(row["dead_states"] for row in rows),
        "frontier_states": sum(row["frontier_states"] for row in rows),
        "invalid_initial": sum(row["invalid_initial"] for row in rows),
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

    table = regimes()
    primary = parallel_map(primary_row, table, args.jobs)
    primary_summary = summarize(primary)
    require(
        {key: primary_summary[key] for key in EXPECTED_CORE} == EXPECTED_CORE,
        ("primary aggregate mismatch", primary_summary, EXPECTED_CORE),
    )
    cleanroom = parallel_map(cleanroom_row, table, args.jobs)
    require(cleanroom == primary, "clean-room per-regime table mismatch")
    print(
        json.dumps(
            {
                "theorem_region": {
                    "anchor": "LR: N=A+Q+B, A<B",
                    "condition": "Q-(B-A)<-15",
                    "conclusion": "no Leech bi-spider extends the anchor",
                },
                "finite_partition": {
                    "exact_C": "A+1 <= C=A+Q <= 45",
                    "stable_tail": "C=46 represents every C>45",
                    "dominance": "B=C+16 represents every B-C>15",
                },
                "primary": primary_summary,
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
