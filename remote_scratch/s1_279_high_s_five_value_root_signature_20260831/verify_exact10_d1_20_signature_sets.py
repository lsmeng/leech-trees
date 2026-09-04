#!/usr/bin/env python3
"""Verify complete normalized d1=20 exact-10 signature-set agreement."""

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
    scalar_checks = {
        "params_total": primary["params_total"] == replay["params_total"] == 53,
        "params_valid": primary["params_valid"] == replay["params_valid"] == 52,
        "params_with_survivor": (
            primary["params_with_survivor"] == replay["params_with_survivor"] == 19
        ),
        "survivor_count": primary["survivor_count"] == replay["survivor_count"] == 1353,
        "extension_calls": (
            primary["full_high_coloring_calls"] == replay["extension_calls"] == 15536071
        ),
        "color_count_histogram": (
            primary["color_count_histogram"] == replay["color_count_histogram"]
        ),
    }
    checks = {
        **scalar_checks,
        "primary_saved_all": len(primary_raw) == primary["survivor_count"] == 1353,
        "primary_normalized_unique": len(set(primary_normalized)) == 1353,
        "replay_saved_all": len(replay_signatures) == replay["survivor_count"] == 1353,
        "replay_unique": len(set(replay_signatures)) == 1353,
        "signature_sets_exact": set(primary_normalized) == set(replay_signatures),
    }
    only_primary = sorted(set(primary_normalized) - set(replay_signatures))
    only_replay = sorted(set(replay_signatures) - set(primary_normalized))
    status = "VERIFIED_EXACT10_SIGNATURE_SET_MATCH" if all(checks.values()) else "MISMATCH"
    certificate = {
        "status": status,
        "checks": checks,
        "primary": {"path": str(args.primary), "sha256": sha256(args.primary)},
        "replay": {"path": str(args.replay), "sha256": sha256(args.replay)},
        "primary_saved": len(primary_raw),
        "primary_normalized_unique": len(set(primary_normalized)),
        "replay_saved": len(replay_signatures),
        "replay_unique": len(set(replay_signatures)),
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
