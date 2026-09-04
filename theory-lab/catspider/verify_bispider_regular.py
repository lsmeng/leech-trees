#!/usr/bin/env python3
"""Verify the uniform regular-LR bi-spider certificate."""

from __future__ import annotations

import json
from dataclasses import asdict

from bispider_dominant_cleanroom import check_dominant_lr
from bispider_dominant_prover import prove_dominant_lr
from bispider_offset_cleanroom import check_regular_lr
from bispider_offset_prover import prove_regular_lr


EXPECTED = {
    "W": 20,
    "nodes": 2871,
    "accepted_children": 2870,
    "dead_states": 1754,
    "deepest_missing_offset": 20,
    "max_marks": 10,
    "frontier_states": 0,
}

DOMINANT_EXPECTED = {
    "W": 15,
    "nodes": 1881,
    "accepted_children": 1880,
    "dead_states": 1057,
    "deepest_missing_offset": 15,
    "max_marks": 10,
    "frontier_states": 0,
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    primary = asdict(prove_regular_lr(20))
    cleanroom = asdict(check_regular_lr(20))
    require(primary == EXPECTED, ("primary", primary, EXPECTED))
    require(cleanroom == EXPECTED, ("cleanroom", cleanroom, EXPECTED))
    dominant_primary = asdict(prove_dominant_lr(15))
    dominant_raw = asdict(check_dominant_lr(15))
    dominant_cleanroom = {
        "W": dominant_raw["W"],
        "nodes": dominant_raw["nodes"],
        "accepted_children": dominant_raw["children"],
        "dead_states": dominant_raw["dead"],
        "deepest_missing_offset": dominant_raw["deepest"],
        "max_marks": dominant_raw["max_marks"],
        "frontier_states": dominant_raw["frontier"],
    }
    require(
        dominant_primary == DOMINANT_EXPECTED,
        ("dominant primary", dominant_primary, DOMINANT_EXPECTED),
    )
    require(
        dominant_cleanroom == DOMINANT_EXPECTED,
        ("dominant cleanroom", dominant_cleanroom, DOMINANT_EXPECTED),
    )
    print(
        json.dumps(
            {
                "theorem_region": {
                    "anchor": "LR: N=A+Q+B with A<B",
                    "conditions": ["A>20", "Q-(B-A)>20"],
                    "conclusion": "no Leech bi-spider extends the anchor",
                },
                "dominant_theorem_region": {
                    "anchor": "LR: N=A+Q+B with A<B and C=A+Q",
                    "conditions": ["A>15", "B-C>15"],
                    "conclusion": "no Leech bi-spider extends the anchor",
                },
                "primary": primary,
                "cleanroom": cleanroom,
                "dominant_primary": dominant_primary,
                "dominant_cleanroom": dominant_cleanroom,
                "status": "VERIFIED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
