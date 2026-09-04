#!/usr/bin/env python3
"""Verify the finite certificate for all LR anchors with r>20 and B<=20."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict

from bispider_smallb_positive_cleanroom import search
from bispider_smallb_positive_prover import prove_tail


W = 20
EXPECTED_CORE = {
    "regimes": 10_260,
    "nodes": 564_478,
    "accepted_children": 554_218,
    "dead_states": 323_655,
    "frontier_states": 0,
    "invalid_initial": 0,
    "max_depth": 16,
    "max_selected_vertices": 9,
    "sha256": "621e3766337525fb13ecd4f2f20f490c501d1aa7b6fa18ac0d11e516cbdd16b7",
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def regimes():
    return [
        (A, B, Q, W)
        for A in range(1, 20)
        for B in range(A + 1, 21)
        for Q in (*range(21 + B - A, 81), 81)
    ]


def primary_row(regime):
    return asdict(prove_tail(*regime))


def cleanroom_row(regime):
    raw = asdict(search(*regime))
    return {
        "A": raw["A"],
        "B": raw["B"],
        "Q": raw["Q"],
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
        return list(executor.map(function, items, chunksize=10))


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
    print(json.dumps({"primary": primary_summary}, sort_keys=True), flush=True)

    cleanroom = parallel_map(cleanroom_row, table, args.jobs)
    require(cleanroom == primary, "clean-room per-regime table mismatch")
    print(
        json.dumps(
            {
                "theorem_region": {
                    "anchor": "LR: N=A+Q+B, A<B",
                    "conditions": ["Q-(B-A)>20", "B<=20"],
                    "conclusion": "no Leech bi-spider extends the anchor",
                },
                "finite_partition": {
                    "exact_Q": "21+B-A <= Q <= 80",
                    "stable_tail": "Q=81 represents every Q>80",
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
