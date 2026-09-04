#!/usr/bin/env python3
"""Verify complete normalized exact-10 signature-set agreement for one shard."""

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
    parser.add_argument("replay", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    primary = json.loads(args.primary.read_text())
    replay = json.loads(args.replay.read_text())
    primary_raw = [str(x) for x in primary["first_examples"]]
    primary_normalized = [normalize_primary(x) for x in primary_raw]
    replay_signatures = [str(x) for x in replay["canonical_root_signatures"]]

    scope = {
        "s": int(primary["s"]),
        "shape": str(primary["shape"]),
        "d1": int(primary["d1_shard"]),
    }
    checks = {
        "scope_exact": (
            scope["s"] == int(replay["s"])
            and scope["shape"] == str(replay["shape"])
            and scope["d1"] == int(replay["d1"])
        ),
        "params_total": primary["params_total"] == replay["params_total"],
        "params_valid": primary["params_valid"] == replay["params_valid"],
        "params_with_survivor": (
            primary["params_with_survivor"] == replay["params_with_survivor"]
        ),
        "survivor_count": primary["survivor_count"] == replay["survivor_count"],
        "extension_calls": (
            primary["full_high_coloring_calls"] == replay["extension_calls"]
        ),
        "color_count_histogram": (
            primary["color_count_histogram"] == replay["color_count_histogram"]
        ),
        "primary_saved_all": len(primary_raw) == primary["survivor_count"],
        "primary_normalized_unique": len(set(primary_normalized)) == len(primary_normalized),
        "replay_saved_all": len(replay_signatures) == replay["survivor_count"],
        "replay_unique": len(set(replay_signatures)) == len(replay_signatures),
        "signature_sets_exact": set(primary_normalized) == set(replay_signatures),
    }
    only_primary = sorted(set(primary_normalized) - set(replay_signatures))
    only_replay = sorted(set(replay_signatures) - set(primary_normalized))
    status = "VERIFIED_EXACT10_SIGNATURE_SET_MATCH" if all(checks.values()) else "MISMATCH"
    certificate = {
        "status": status,
        "scope": scope,
        "checks": checks,
        "primary": {"path": str(args.primary), "sha256": sha256(args.primary)},
        "replay": {"path": str(args.replay), "sha256": sha256(args.replay)},
        "params_total": int(primary["params_total"]),
        "params_valid": int(primary["params_valid"]),
        "params_with_survivor": int(primary["params_with_survivor"]),
        "extension_calls": int(primary["full_high_coloring_calls"]),
        "survivor_count": int(primary["survivor_count"]),
        "only_primary_count": len(only_primary),
        "only_replay_count": len(only_replay),
        "first_only_primary": only_primary[:10],
        "first_only_replay": only_replay[:10],
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    if status != "VERIFIED_EXACT10_SIGNATURE_SET_MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
