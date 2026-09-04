#!/usr/bin/env python3
"""Verify one completed depthv7 shard without claiming corpus coverage."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ABSTRACT = re.compile(
    r"^ABSTRACT m=(?P<m>\d+) r=(?P<r>\d+) lowpar=(?P<lowpar>[0-9,]*) "
    r"xcap=\d+ split=5:(?P<k>\d+)/(?P<n>\d+) leaves=(?P<leaves>\d+) "
    r"nodes=(?P<nodes>\d+) (?P<status>\w+) depth_survivors=(?P<surv>\d+) "
    r"structures_with_survivor=(?P<struct_surv>\d+)"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("shard", type=Path)
    ap.add_argument("shapes", type=Path)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--r", type=int, required=True)
    ap.add_argument("--split", type=int, required=True)
    ap.add_argument("--nsplit", type=int, required=True)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    expected = {
        line.strip() for line in args.shapes.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    errors: list[str] = []
    lines = args.shard.read_text().splitlines()
    seen: set[str] = set()
    total_survivors = 0
    total_struct_survivors = 0
    abstract_count = 0
    for line in lines:
        match = ABSTRACT.match(line)
        if not match:
            continue
        abstract_count += 1
        data = match.groupdict()
        lowpar = data["lowpar"]
        seen.add(lowpar)
        if int(data["m"]) != args.m or int(data["r"]) != args.r:
            errors.append(f"scope mismatch: {line}")
        if int(data["k"]) != args.split or int(data["n"]) != args.nsplit:
            errors.append(f"split mismatch: {line}")
        if data["status"] != "EXHAUSTED":
            errors.append(f"non-exhausted shape: {line}")
        total_survivors += int(data["surv"])
        total_struct_survivors += int(data["struct_surv"])
    if abstract_count == 0:
        errors.append("no ABSTRACT lines")
    if seen != expected:
        errors.append(f"shape mismatch: expected={sorted(expected)} seen={sorted(seen)}")
    if not lines or not lines[-1].startswith("SHAPES_FILE_SUMMARY") or not lines[-1].endswith("COMPLETE"):
        errors.append("missing final COMPLETE summary")
    if total_survivors or total_struct_survivors:
        errors.append("survivor count is nonzero")

    status = "VERIFIED_PARTIAL_SHARD_EMPTY" if not errors else "PARTIAL_SHARD_GAP"
    result = {
        "status": status,
        "scope": {
            "m": args.m,
            "r": args.r,
            "split": args.split,
            "nsplit": args.nsplit,
            "shapes": sorted(expected),
        },
        "abstract_lines": abstract_count,
        "total_depth_survivors": total_survivors,
        "total_structure_survivors": total_struct_survivors,
        "errors": errors,
        "shard_sha256": sha256(args.shard),
        "shapes_sha256": sha256(args.shapes),
        "source_scope": "one completed shard only; not corpus coverage or a global proof",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.out:
        args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
