#!/usr/bin/env python3
"""Verify exact coverage and per-job agreement for Python/C++ forest searches."""

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


def normalized_signature(text: str) -> str:
    """Drop the primary search's optional full-color witness suffix."""
    return text.rsplit("|C=", 1)[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary_shard_dir", type=Path)
    parser.add_argument("replay_jobs", type=Path)
    parser.add_argument("replay_summary", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--replay-signatures",
        type=Path,
        help=(
            "independent exact-search JSON containing canonical_root_signatures; "
            "when supplied, compare jobs by canonical signature text rather than "
            "implementation-specific signature_index"
        ),
    )
    args = parser.parse_args()
    summary = json.loads(args.replay_summary.read_text())
    expected_signatures = int(summary["signatures"])
    replay_signature_texts: list[str] | None = None
    if args.replay_signatures is not None:
        signature_data = json.loads(args.replay_signatures.read_text())
        replay_signature_texts = [
            normalized_signature(str(text))
            for text in signature_data["canonical_root_signatures"]
        ]
        if len(replay_signature_texts) != expected_signatures:
            raise AssertionError("replay signature count does not match replay summary")
        if len(set(replay_signature_texts)) != len(replay_signature_texts):
            raise AssertionError("duplicate canonical replay signature")

    shard_paths = sorted(
        (Path(p) for p in glob.glob(str(args.primary_shard_dir / "result_*.json"))),
        key=lambda p: int(p.stem.split("_")[1]),
    )
    primary: dict[tuple[int | str, str, int, str, int], tuple[int, ...]] = {}
    coverage: list[tuple[int, int]] = []
    primary_classes = {"A": 0, "B": 0, "C": 0}
    shard_integrity: list[dict[str, object]] = []
    for path in shard_paths:
        data = json.loads(path.read_text())
        start = int(data["signature_start"])
        stop = int(data["signature_stop"])
        coverage.append((start, stop))
        stem_parts = path.stem.split("_")
        filename_range_ok = (
            len(stem_parts) == 3
            and stem_parts[0] == "result"
            and int(stem_parts[1]) == start
            and int(stem_parts[2]) == stop
        )
        shard_integrity.append({
            "path": str(path),
            "status": data.get("status"),
            "signature_start": start,
            "signature_stop": stop,
            "source_signature_count": int(data.get("source_signature_count", -1)),
            "signatures_processed": int(data.get("signatures_processed", -1)),
            "filename_range_ok": filename_range_ok,
        })
        for row_class, count in data["compatible_rows_by_class"].items():
            primary_classes[str(row_class)] += int(count)
        for row in data["results"]:
            signature_key: int | str = int(row["signature_index"])
            if replay_signature_texts is not None:
                signature_key = normalized_signature(str(row["signature"]))
            for c_result in row["c_results"]:
                key = (
                    signature_key, str(row["gate"]), int(row["q"]),
                    str(row["class"]), int(c_result["c"]),
                )
                if key in primary:
                    raise AssertionError(f"duplicate primary key: {key}")
                primary[key] = tuple(int(c_result[field]) for field in FIELDS)

    replay: dict[tuple[int | str, str, int, str, int], tuple[int, ...]] = {}
    with args.replay_jobs.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            signature_index = int(row["signature_index"])
            signature_key: int | str = signature_index
            if replay_signature_texts is not None:
                if not 0 <= signature_index < len(replay_signature_texts):
                    raise AssertionError(f"bad replay signature index: {signature_index}")
                signature_key = replay_signature_texts[signature_index]
            key = (
                signature_key, str(row["gate"]), int(row["q"]),
                str(row["class"]), int(row["c"]),
            )
            if key in replay:
                raise AssertionError(f"duplicate replay key: {key}")
            replay[key] = tuple(int(row[field]) for field in FIELDS)

    contiguous = bool(coverage) and coverage[0][0] == 0
    contiguous = contiguous and all(a[1] == b[0] for a, b in zip(coverage, coverage[1:]))
    contiguous = contiguous and coverage[-1][1] == expected_signatures
    mismatches = [
        key for key in sorted(set(primary) | set(replay))
        if primary.get(key) != replay.get(key)
    ]
    primary_totals = dict(zip(FIELDS, map(sum, zip(*primary.values()))))
    replay_totals = dict(zip(FIELDS, map(sum, zip(*replay.values()))))
    primary_signature_count = len({key[0] for key in primary})
    replay_signature_count = len({key[0] for key in replay})
    replay_classes = {
        cls: int(summary[f"compatible_{cls}"]) for cls in ("A", "B", "C")
    }
    expected_shard_count = (expected_signatures + 199) // 200
    checks = {
        "shard_count_exact": len(shard_paths) == expected_shard_count,
        "shard_status_all_exhausted": all(
            item["status"] == "FW303_ALL_CLASS_FORESTS_EXHAUSTED"
            for item in shard_integrity
        ),
        "shard_filename_ranges_exact": all(
            bool(item["filename_range_ok"]) for item in shard_integrity
        ),
        "shard_source_signature_count_exact": all(
            item["source_signature_count"] == expected_signatures
            for item in shard_integrity
        ),
        "shard_processed_count_exact": all(
            item["signatures_processed"] == item["signature_stop"] - item["signature_start"]
            for item in shard_integrity
        ),
        "coverage_contiguous": contiguous,
        "job_count_exact": len(primary) == len(replay) == int(summary["row_c_jobs"]),
        "compatible_signature_count_exact": primary_signature_count == replay_signature_count,
        "class_histogram_exact": primary_classes == replay_classes,
        "job_keys_exact": set(primary) == set(replay),
        "per_job_counters_exact": not mismatches,
        "aggregate_counters_exact": primary_totals == replay_totals,
        "aggregate_matches_summary": all(
            replay_totals[field] == int(summary[
                "full_spectrum_survivors" if field == "spectrum_survivors" else field
            ]) for field in FIELDS
        ),
        "zero_full_spectrum_survivors": (
            primary_totals["spectrum_survivors"] == 0
            and replay_totals["spectrum_survivors"] == 0
        ),
    }
    status = "VERIFIED_EXACT_PER_JOB_MATCH" if all(checks.values()) else "MISMATCH"
    d1_scope = (
        {"d1": int(summary["d1"])}
        if "d1" in summary
        else {
            "d1_min": int(summary["d1_min"]),
            "d1_max": int(summary["d1_max"]),
        }
    )
    certificate = {
        "status": status,
        "d1": int(summary["d1"]) if "d1" in summary else None,
        "d1_scope": d1_scope,
        "checks": checks,
        "coverage": coverage,
        "expected_shard_count": expected_shard_count,
        "shard_integrity": shard_integrity,
        "primary_shards": [
            {"path": str(path), "sha256": sha256(path)} for path in shard_paths
        ],
        "replay_jobs": {"path": str(args.replay_jobs), "sha256": sha256(args.replay_jobs)},
        "replay_summary": {
            "path": str(args.replay_summary), "sha256": sha256(args.replay_summary)
        },
        "job_key_mode": (
            "canonical_signature" if replay_signature_texts is not None
            else "implementation_specific_index"
        ),
        "primary_job_count": len(primary),
        "replay_job_count": len(replay),
        "primary_compatible_signatures": primary_signature_count,
        "replay_compatible_signatures": replay_signature_count,
        "primary_classes": primary_classes,
        "replay_classes": replay_classes,
        "counter_fields": list(FIELDS),
        "primary_totals": primary_totals,
        "replay_totals": replay_totals,
        "mismatch_count": len(mismatches),
        "first_mismatch_keys": [list(key) for key in mismatches[:10]],
    }
    if args.replay_signatures is not None:
        certificate["replay_signatures"] = {
            "path": str(args.replay_signatures),
            "sha256": sha256(args.replay_signatures),
        }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    if status != "VERIFIED_EXACT_PER_JOB_MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
