"""Reproduce the computer-assisted proof that no Leech spider has n>=5.

The verifier checks four logically separate pieces:

1. the exact numeric base cases n=5,...,15;
2. the relaxed offset closure for U>10 and T-U>10;
3. both affine boundary strips for parameter P>=51; and
4. agreement of the affine prover with an independent from-scratch checker
   and with exact numeric instances.

No SAT witness is involved in this nonexistence proof.  A nonzero exit means
the certificate did not verify.  Optimized Python execution is rejected.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from spider_affine_cleanroom import check_boundary
from spider_affine_prover import prove_boundary
from spider_offset_prover import prove_regular
from spider_window_probe import explore_order, explore_anchor, summarize


BASE_NODE_COUNTS = {
    5: 13,
    6: 50,
    7: 132,
    8: 254,
    9: 507,
    10: 971,
    11: 1511,
    12: 2050,
    13: 2736,
    14: 3562,
    15: 4367,
}
STAT_FIELDS = (
    "nodes",
    "accepted_children",
    "dead_states",
    "deepest_missing_offset",
    "max_marks",
    "frontier_states",
)
AFFINE_EXPECTED = {
    "small-U": (
        (3, 2, 1, 5, 4, 0),
        (4, 3, 2, 5, 4, 0),
        (4, 3, 3, 2, 3, 0),
        (10, 9, 6, 6, 4, 0),
        (13, 12, 8, 8, 5, 0),
        (17, 16, 9, 7, 5, 0),
        (30, 29, 18, 6, 5, 0),
        (37, 36, 17, 9, 6, 0),
        (42, 41, 21, 8, 6, 0),
        (49, 48, 26, 8, 6, 0),
    ),
    "small-delta": (
        (129, 128, 63, 25, 9, 0),
        (122, 121, 63, 25, 9, 0),
        (105, 104, 68, 18, 8, 0),
        (62, 61, 32, 17, 8, 0),
        (90, 89, 49, 18, 8, 0),
        (72, 71, 39, 19, 9, 0),
        (97, 96, 53, 18, 8, 0),
        (66, 65, 31, 15, 8, 0),
        (79, 78, 38, 11, 7, 0),
        (92, 91, 47, 10, 7, 0),
    ),
}


def require(condition: bool, message) -> None:
    """Raise on a failed certificate invariant, even under ``python -O``."""

    if not condition:
        raise RuntimeError(message)


def stat_tuple(row):
    return tuple(getattr(row, field) for field in STAT_FIELDS)


def verify(*, numeric_spots: bool = True):
    require(
        sys.flags.optimize == 0,
        "the spider verifier must be run without Python optimization (-O/-OO)",
    )
    base_rows = []
    for n, expected_nodes in BASE_NODE_COUNTS.items():
        rows = explore_order(n)
        summary = summarize(rows)
        require(summary["nodes"] == expected_nodes, (n, summary, expected_nodes))
        require(summary["solutions"] == 0, (n, summary))
        require(summary["frontier_states"] == 0, (n, summary))
        base_rows.append(summary)

    regular = prove_regular(10, None)
    require(regular.nodes == 111, asdict(regular))
    require(regular.accepted_children == 110, asdict(regular))
    require(regular.dead_states == 57, asdict(regular))
    require(regular.deepest_missing_offset == 10, asdict(regular))
    require(regular.max_marks == 7, asdict(regular))
    require(regular.frontier_states == 0, asdict(regular))

    affine_rows = []
    cleanroom_rows = []
    numeric_checks = 0
    for mode in ("small-U", "small-delta"):
        for fixed in range(1, 11):
            primary = prove_boundary(mode, fixed, Pmin=51, window=25)
            clean = check_boundary(mode, fixed, pmin=51, window=25)
            require(primary.frontier_states == 0, asdict(primary))
            require(clean.frontier_states == 0, asdict(clean))
            require(
                stat_tuple(primary) == AFFINE_EXPECTED[mode][fixed - 1],
                (asdict(primary), AFFINE_EXPECTED[mode][fixed - 1]),
            )
            require(
                stat_tuple(primary) == stat_tuple(clean),
                (asdict(primary), asdict(clean)),
            )
            affine_rows.append(primary)
            cleanroom_rows.append(clean)

            if numeric_spots:
                for P in (51, 52, 137):
                    if mode == "small-U":
                        T, U = P + fixed, fixed
                    else:
                        T, U = P + fixed, P
                    numeric = explore_anchor(
                        T,
                        U,
                        mark_budget=None,
                        window_limit=25,
                    )
                    require(
                        stat_tuple(numeric) == stat_tuple(primary),
                        (mode, fixed, P, stat_tuple(numeric), stat_tuple(primary)),
                    )
                    numeric_checks += 1

    return {
        "certificate": "no Leech spider of order n >= 5",
        "status": "VERIFIED",
        "parameters": {"regular_window": 10, "boundary_window": 25, "pmin": 51},
        "base": {
            "orders": [5, 15],
            "nodes": sum(row["nodes"] for row in base_rows),
            "solutions": sum(row["solutions"] for row in base_rows),
            "reference_node_counts": BASE_NODE_COUNTS,
        },
        "regular_relaxation": asdict(regular),
        "affine_primary": {
            "regimes": len(affine_rows),
            "nodes": sum(row.nodes for row in affine_rows),
            "frontier_states": sum(row.frontier_states for row in affine_rows),
            "max_depth": max(row.deepest_missing_offset for row in affine_rows),
            "max_marks": max(row.max_marks for row in affine_rows),
            "invariant_fields": STAT_FIELDS,
            "regime_invariants": AFFINE_EXPECTED,
        },
        "affine_cleanroom": {
            "regimes": len(cleanroom_rows),
            "nodes": sum(row.nodes for row in cleanroom_rows),
            "frontier_states": sum(row.frontier_states for row in cleanroom_rows),
            "fieldwise_matches": len(cleanroom_rows),
        },
        "numeric_affine_spot_checks": numeric_checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-numeric-spots",
        action="store_true",
        help="skip the 60 extra affine-vs-numeric regression instances",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            verify(numeric_spots=not args.skip_numeric_spots),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
