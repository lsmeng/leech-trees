#!/usr/bin/env python3
"""Verify exact per-job agreement for the d1=20 Python/C++ forest searches."""

from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
from pathlib import Path


FIELDS = (
    "root_sets",
    "root_colorings",
    "root_edge_legal",
    "capacity_rejects",
    "weight_assignments",
    "parent_legal",
    "spectrum_survivors",
)
EXPECTED_COVERAGE = (
    (0, 200),
    (200, 400),
    (400, 600),
    (600, 800),
    (800, 1000),
    (1000, 1200),
    (1200, 1353),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary_shard_dir", type=Path)
    parser.add_argument("replay_jobs", type=Path)
    parser.add_argument("replay_summary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    shard_paths = sorted(
        (Path(p) for p in glob.glob(str(args.primary_shard_dir / "result_*.json"))),
        key=lambda p: int(p.stem.split("_")[1]),
    )
    primary: dict[tuple[int, str, int, str, int], tuple[int, ...]] = {}
    coverage: list[tuple[int, int]] = []
    for path in shard_paths:
        data = json.loads(path.read_text())
        coverage.append((int(data["signature_start"]), int(data["signature_stop"])))
        for row in data["results"]:
            for c_result in row["c_results"]:
                key = (
                    int(row["signature_index"]),
                    str(row["gate"]),
                    int(row["q"]),
                    str(row["class"]),
                    int(c_result["c"]),
                )
                if key in primary:
                    raise AssertionError(f"duplicate primary key: {key}")
                primary[key] = tuple(int(c_result[field]) for field in FIELDS)

    replay: dict[tuple[int, str, int, str, int], tuple[int, ...]] = {}
    with args.replay_jobs.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            key = (
                int(row["signature_index"]),
                str(row["gate"]),
                int(row["q"]),
                str(row["class"]),
                int(row["c"]),
            )
            if key in replay:
                raise AssertionError(f"duplicate replay key: {key}")
            replay[key] = tuple(int(row[field]) for field in FIELDS)

    summary = json.loads(args.replay_summary.read_text())
    mismatches = [
        key for key in sorted(set(primary) | set(replay))
        if primary.get(key) != replay.get(key)
    ]
    primary_totals = dict(zip(FIELDS, map(sum, zip(*primary.values()))))
    replay_totals = dict(zip(FIELDS, map(sum, zip(*replay.values()))))
    primary_signature_count = len({key[0] for key in primary})
    replay_signature_count = len({key[0] for key in replay})

    checks = {
        "coverage_exact": tuple(coverage) == EXPECTED_COVERAGE,
        "job_count_3716": len(primary) == len(replay) == 3716,
        "compatible_signature_count_592": primary_signature_count == replay_signature_count == 592,
        "job_keys_exact": set(primary) == set(replay),
        "per_job_counters_exact": not mismatches,
        "aggregate_counters_exact": primary_totals == replay_totals,
        "replay_summary_scope": (
            summary.get("signatures") == 1353
            and summary.get("gate_rows_tested") == 51414
            and summary.get("compatible_rows") == 929
            and summary.get("compatible_A") == 929
            and summary.get("compatible_B") == 0
            and summary.get("compatible_C") == 0
            and summary.get("row_c_jobs") == 3716
        ),
        "zero_full_spectrum_survivors": (
            primary_totals["spectrum_survivors"] == 0
            and replay_totals["spectrum_survivors"] == 0
            and summary.get("full_spectrum_survivors") == 0
        ),
    }
    status = "VERIFIED_EXACT_PER_JOB_MATCH" if all(checks.values()) else "MISMATCH"
    certificate = {
        "status": status,
        "checks": checks,
        "coverage": coverage,
        "primary_shards": [
            {"path": str(path), "sha256": sha256(path)} for path in shard_paths
        ],
        "replay_jobs": {"path": str(args.replay_jobs), "sha256": sha256(args.replay_jobs)},
        "replay_summary": {
            "path": str(args.replay_summary),
            "sha256": sha256(args.replay_summary),
        },
        "primary_job_count": len(primary),
        "replay_job_count": len(replay),
        "primary_compatible_signatures": primary_signature_count,
        "replay_compatible_signatures": replay_signature_count,
        "counter_fields": list(FIELDS),
        "primary_totals": primary_totals,
        "replay_totals": replay_totals,
        "mismatch_count": len(mismatches),
        "first_mismatch_keys": [list(key) for key in mismatches[:10]],
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    if status != "VERIFIED_EXACT_PER_JOB_MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
