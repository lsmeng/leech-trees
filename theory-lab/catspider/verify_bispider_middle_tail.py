#!/usr/bin/env python3
"""Verify the large-h tail certificate for the bounded-imbalance LR strip."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict

from bispider_middle_tail_cleanroom import search
from bispider_middle_tail_prover import prove_tail


W = 35
EXPECTED = {
    "regimes": 1800,
    "nodes": 1_386_587,
    "accepted_children": 1_384_787,
    "dead_states": 810_109,
    "frontier_states": 0,
    "max_depth": 34,
    "max_selected_vertices": 12,
    "sha256": "0cf2bb93dea516b883d1756492c3253b947b5bbe3555df498dacda2c7ca3f997",
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def regimes():
    return [(A, r, W) for A in range(1, 51) for r in range(-15, 21)]


def primary_row(regime):
    return asdict(prove_tail(*regime))


def cleanroom_row(regime):
    raw = asdict(search(*regime))
    return {
        "A": raw["A"],
        "r": raw["r"],
        "W": raw["W"],
        "nodes": raw["nodes"],
        "accepted_children": raw["children"],
        "dead_states": raw["dead"],
        "deepest_missing_offset": raw["deepest"],
        "frontier_states": raw["frontier"],
        "max_selected_vertices": raw["max_vertices"],
    }


def parallel_map(function, items, jobs: int):
    if jobs == 1:
        return [function(item) for item in items]
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        return list(executor.map(function, items, chunksize=1))


def digest(rows) -> str:
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def summarize(rows):
    return {
        "regimes": len(rows),
        "nodes": sum(row["nodes"] for row in rows),
        "accepted_children": sum(row["accepted_children"] for row in rows),
        "dead_states": sum(row["dead_states"] for row in rows),
        "frontier_states": sum(row["frontier_states"] for row in rows),
        "max_depth": max(row["deepest_missing_offset"] for row in rows),
        "max_selected_vertices": max(row["max_selected_vertices"] for row in rows),
        "sha256": digest(rows),
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
    require(primary_summary == EXPECTED, (primary_summary, EXPECTED))
    print(json.dumps({"primary": primary_summary}, sort_keys=True), flush=True)
    cleanroom = parallel_map(cleanroom_row, table, args.jobs)
    require(cleanroom == primary, "clean-room per-(A,r) table mismatch")
    print(
        json.dumps(
            {
                "region": ["1<=A<=50", "-15<=r<=20", "large-h stable tail"],
                "primary": primary_summary,
                "cleanroom_sha256": digest(cleanroom),
                "cleanroom_match": True,
                "status": "VERIFIED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
