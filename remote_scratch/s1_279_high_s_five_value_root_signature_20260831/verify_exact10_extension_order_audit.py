#!/usr/bin/env python3
"""Certify that the d1=28 extension-call mismatch is traversal-order only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_primary(signature: str) -> str:
    marker = "|C="
    if marker not in signature:
        raise ValueError("primary signature lacks full-color witness marker")
    return signature.split(marker, 1)[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary", type=Path)
    parser.add_argument("original_replay", type=Path)
    parser.add_argument("aligned_replay", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    primary = json.loads(args.primary.read_text())
    original = json.loads(args.original_replay.read_text())
    aligned = json.loads(args.aligned_replay.read_text())

    primary_signatures = sorted(
        normalize_primary(str(value)) for value in primary["first_examples"]
    )
    original_signatures = sorted(
        str(value) for value in original["canonical_root_signatures"]
    )
    aligned_signatures = sorted(
        str(value) for value in aligned["canonical_root_signatures"]
    )

    invariant_fields = (
        "s",
        "B",
        "shape",
        "params_total",
        "params_valid",
        "params_with_survivor",
        "dfs_calls",
        "survivor_count",
        "color_count_histogram",
    )
    checks = {
        "scope_d1_28": (
            int(primary["d1_shard"]) == 28
            and int(original["d1"]) == 28
            and int(aligned["d1"]) == 28
        ),
        "original_and_aligned_invariants_exact": all(
            original[field] == aligned[field] for field in invariant_fields
        ),
        "primary_and_aligned_invariants_exact": all(
            primary[field] == aligned[field]
            for field in invariant_fields
            if field not in {"d1"}
        ),
        "all_signature_sets_exact": (
            primary_signatures == original_signatures == aligned_signatures
        ),
        "all_signatures_saved_and_unique": (
            len(primary_signatures) == int(primary["survivor_count"])
            and len(original_signatures) == int(original["survivor_count"])
            and len(aligned_signatures) == int(aligned["survivor_count"])
            and len(set(primary_signatures)) == len(primary_signatures)
            and len(set(original_signatures)) == len(original_signatures)
            and len(set(aligned_signatures)) == len(aligned_signatures)
        ),
        "original_counter_diff_is_1649": (
            int(original["extension_calls"])
            - int(primary["full_high_coloring_calls"])
            == 1649
        ),
        "aligned_counter_matches_primary": (
            int(aligned["extension_calls"])
            == int(primary["full_high_coloring_calls"])
        ),
    }

    status = (
        "VERIFIED_EXTENSION_COUNTER_TRAVERSAL_ORDER_DIAGNOSTIC"
        if all(checks.values())
        else "MISMATCH"
    )
    certificate = {
        "status": status,
        "scope": {"s": int(primary["s"]), "shape": primary["shape"], "d1": 28},
        "interpretation": (
            "Changing only the replay extension color traversal from 1,2,0 to "
            "0,1,2 preserves every semantic result and makes the short-circuit "
            "recursion counter equal to the primary counter."
        ),
        "checks": checks,
        "primary": {"path": str(args.primary), "sha256": sha256(args.primary)},
        "original_replay": {
            "path": str(args.original_replay),
            "sha256": sha256(args.original_replay),
            "extension_calls": int(original["extension_calls"]),
        },
        "aligned_replay": {
            "path": str(args.aligned_replay),
            "sha256": sha256(args.aligned_replay),
            "extension_calls": int(aligned["extension_calls"]),
        },
        "primary_extension_calls": int(primary["full_high_coloring_calls"]),
        "survivor_count": int(primary["survivor_count"]),
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    if status == "MISMATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
