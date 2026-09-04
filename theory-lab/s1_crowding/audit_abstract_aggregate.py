#!/usr/bin/env python3
"""Lightweight, independent audit of an abstract-search aggregate.

This parser checks only textual consistency and shard coverage.  It does not
enumerate trees and cannot turn an aggregate into a mathematical theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


def parse_kv(tokens: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for token in tokens:
        if "=" in token:
            key, value = token.split("=", 1)
            out[key] = value
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("aggregate", type=Path)
    ap.add_argument("--expected-shards", type=int, default=32)
    args = ap.parse_args()

    text = args.aggregate.read_text(encoding="utf-8")
    records: list[tuple[str, dict[str, str]]] = []
    summaries: list[dict[str, str]] = []
    errors: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "ABSTRACT":
            if len(fields) < 3:
                errors.append(f"line {lineno}: short ABSTRACT record")
                continue
            records.append((fields[-1], parse_kv(fields[1:-1])))
        elif fields[0] == "ABSTRACT_SUMMARY":
            summaries.append(parse_kv(fields[1:]))
        else:
            errors.append(f"line {lineno}: unknown record kind {fields[0]!r}")

    statuses = {status: sum(1 for st, _ in records if st == status) for status in {st for st, _ in records}}
    lowpars = [data.get("lowpar", "") for _, data in records]
    unique_lowpars = len(set(lowpars)) == len(lowpars)
    record_count = len(records)
    summary_shards: list[int] = []
    summary_checks: list[bool] = []
    raw_count_checks: list[bool] = []
    for summary in summaries:
        try:
            shard = int(summary["shard"].split("/", 1)[0])
            summary_shards.append(shard)
            shape_run = int(summary["shapes_run"])
            skipped_other = int(summary["skipped_other_shards"])
            skipped_iso = int(summary["skipped_iso"])
            summary_checks.append(
                int(summary["iso_classes"]) == record_count
                and shape_run + skipped_other == record_count
            )
            low_count = len(lowpars[0].split(",")) if lowpars and lowpars[0] else None
            raw_count_checks.append(
                low_count is not None
                and shape_run + skipped_other + skipped_iso == math.factorial(low_count)
            )
        except (KeyError, ValueError):
            summary_checks.append(False)
            raw_count_checks.append(False)

    exists_count = statuses.get("EXISTS", 0)
    exhausted_count = statuses.get("EXHAUSTED", 0)
    leaf_sum = 0
    leaf_status_ok = True
    for status, data in records:
        try:
            leaves = int(data["leaves"])
        except (KeyError, ValueError):
            leaf_status_ok = False
            continue
        leaf_sum += leaves
        leaf_status_ok &= (status == "EXISTS" and leaves > 0) or (status == "EXHAUSTED" and leaves == 0)

    expected_shards = list(range(args.expected_shards))
    checks = {
        "no_parse_errors": not errors,
        "records_nonempty": record_count > 0,
        "unique_lowpar": unique_lowpars,
        "status_partition": exists_count + exhausted_count == record_count,
        "summary_count": len(summaries) == args.expected_shards,
        "summary_shards_exact": sorted(summary_shards) == expected_shards,
        "summary_coverage": bool(summary_checks) and all(summary_checks),
        "raw_factorial_coverage": bool(raw_count_checks) and all(raw_count_checks),
        "leaf_status_consistent": leaf_status_ok,
        "leaf_sum_matches_exists": leaf_sum == exists_count,
    }
    result = {
        "aggregate": str(args.aggregate),
        "aggregate_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "records": record_count,
        "statuses": statuses,
        "summaries": len(summaries),
        "summary_shards": sorted(summary_shards),
        "leaf_sum": leaf_sum,
        "checks": checks,
        "all_checks_ok": all(checks.values()),
        "errors": errors,
        "scope": "textual aggregate consistency only; not a theorem or depth certificate",
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["all_checks_ok"] else 1)


if __name__ == "__main__":
    main()
