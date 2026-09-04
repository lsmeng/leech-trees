#!/usr/bin/env python3
"""Verify the paired W=36 LL bi-spider certificate for every n>=18."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict

from bispider_ll_far_cleanroom import regimes as clean_far_regimes
from bispider_ll_far_cleanroom import search as clean_far
from bispider_ll_near_cleanroom import search as clean_near
from bispider_ll_prover import far_regimes, prove_far, prove_near, prove_small
from bispider_ll_small_cleanroom import search as clean_small


W = 36
EXPECTED = {
    "near": {
        "regimes": 1_332,
        "nodes": 433_069,
        "children": 431_737,
        "dead": 253_306,
        "frontier": 0,
        "max_depth": 28,
        "max_vertices": 12,
        "sha256": "94cd15d95cc0df434125c5e88af5fbb4b5c2089d397aeae186b6dfb7fab5c3f3",
    },
    "far": {
        "regimes": 343,
        "nodes": 89_723,
        "children": 89_380,
        "dead": 52_129,
        "frontier": 0,
        "max_depth": 36,
        "max_vertices": 12,
        "sha256": "db87ce9807221abb07c97c21aafc180086bcf6e69af1d3fe541f755bb847b584",
    },
    "small": {
        "regimes": 630,
        "nodes": 217_802,
        "children": 217_172,
        "dead": 131_397,
        "frontier": 0,
        "max_depth": 20,
        "max_vertices": 11,
        "sha256": "9d94098ed78c1100f8ae92c88a08afb70d198fbffc9e33b9ef4e8ea4b138d28b",
    },
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def near_regimes():
    return [(delta, L, W) for delta in range(1, W + 2) for L in range(1, W + 1)]


def small_regimes():
    return [(U, L, W) for U in range(2, W + 1) for L in range(1, U)]


def primary_near(row):
    return normalize_primary(prove_near(*row))


def primary_far(row):
    return normalize_primary(prove_far(*row))


def primary_small(row):
    return normalize_primary(prove_small(*row))


def cleanroom_near(row):
    return normalize_cleanroom(clean_near(*row), row)


def cleanroom_far(row):
    return normalize_cleanroom(clean_far(*row), row)


def cleanroom_small(row):
    return normalize_cleanroom(clean_small(*row), row)


def normalize_primary(stats):
    row = asdict(stats)
    return {
        "p1": row["p1"],
        "p2": row["p2"],
        "W": row["W"],
        "nodes": row["nodes"],
        "children": row["children"],
        "dead": row["dead"],
        "deepest": row["deepest"],
        "frontier": row["frontier"],
        "max_vertices": row["max_vertices"],
    }


def normalize_cleanroom(stats, regime):
    row = asdict(stats)
    return {
        "p1": regime[0],
        "p2": regime[1],
        "W": row["W"],
        "nodes": row["nodes"],
        "children": row["children"],
        "dead": row["dead"],
        "deepest": row["deepest"],
        "frontier": row["frontier"],
        "max_vertices": row["max_vertices"],
    }


def parallel_map(function, rows, jobs: int):
    if jobs == 1:
        return [function(row) for row in rows]
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        return list(executor.map(function, rows, chunksize=1))


def digest(rows) -> str:
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def summarize(rows):
    return {
        "regimes": len(rows),
        "nodes": sum(row["nodes"] for row in rows),
        "children": sum(row["children"] for row in rows),
        "dead": sum(row["dead"] for row in rows),
        "frontier": sum(row["frontier"] for row in rows),
        "max_depth": max(row["deepest"] for row in rows),
        "max_vertices": max(row["max_vertices"] for row in rows),
        "sha256": digest(rows),
    }


def partition_audit():
    """Check every actual LL anchor through n=40 maps to exactly one table."""

    near = set(near_regimes())
    far = set(far_regimes(W))
    small = set(small_regimes())
    counts = {"near": 0, "far": 0, "small": 0}
    for n in range(18, 41):
        N = n * (n - 1) // 2
        for U in range(2, (N - 1) // 2 + 1):
            delta = N - 2 * U
            for Q in range(1, U):
                L = U - Q
                if U <= W:
                    key = (U, L, W)
                    require(key in small, ("small partition", n, U, Q, key))
                    counts["small"] += 1
                elif L <= W:
                    key = (min(delta, W + 1), L, W)
                    require(key in near, ("near partition", n, U, Q, key))
                    counts["near"] += 1
                else:
                    rho = delta + 2 * Q
                    key = (min(delta, W + 1), min(rho, W + 1), W)
                    require(key in far, ("far partition", n, U, Q, key))
                    counts["far"] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    require(args.jobs >= 1, "jobs must be positive")
    require(
        far_regimes(W) == clean_far_regimes(W),
        "primary and clean-room far-region partitions differ",
    )
    audit_counts = partition_audit()
    print(json.dumps({"partition_audit_n18_through_n40": audit_counts}, sort_keys=True))

    regions = (
        ("near", near_regimes(), primary_near, cleanroom_near),
        ("far", list(far_regimes(W)), primary_far, cleanroom_far),
        ("small", small_regimes(), primary_small, cleanroom_small),
    )
    output = {}
    for name, table, primary_function, cleanroom_function in regions:
        primary = parallel_map(primary_function, table, args.jobs)
        summary = summarize(primary)
        require(summary == EXPECTED[name], (name, summary, EXPECTED[name]))
        cleanroom = parallel_map(cleanroom_function, table, args.jobs)
        require(cleanroom == primary, f"{name} clean-room per-regime mismatch")
        output[name] = {
            **summary,
            "cleanroom_sha256": digest(cleanroom),
            "cleanroom_match": True,
        }
        print(json.dumps({name: output[name]}, sort_keys=True), flush=True)

    print(
        json.dumps(
            {
                "order_range": "n>=18",
                "region": "all LL anchors",
                "window": W,
                "regions": output,
                "total_regimes": sum(row["regimes"] for row in output.values()),
                "total_nodes": sum(row["nodes"] for row in output.values()),
                "total_frontier": sum(row["frontier"] for row in output.values()),
                "partition_audit_n18_through_n40": audit_counts,
                "status": "VERIFIED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
