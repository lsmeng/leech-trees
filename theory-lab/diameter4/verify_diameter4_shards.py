#!/usr/bin/env python3
"""Aggregate a complete diameter-four shard sweep and verify any witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ENGINE_SOURCE = HERE / "forest_search_d4.cpp"
sys.path.insert(0, str(REPO / "src"))
from checker_a import is_leech as checker_a  # noqa: E402
from checker_b import is_leech as checker_b  # noqa: E402


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parse_witness(line: str):
    edges = []
    for token in line[len("SOL:") :].split():
        match = re.fullmatch(r"(\d+)-(\d+):(\d+)", token)
        require(match is not None, ("bad witness token", token))
        edges.append(tuple(map(int, match.groups())))
    return edges


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    require(path.is_file(), ("missing hashed artifact", path))
    return sha256_bytes(path.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--shards", type=int, default=512)
    parser.add_argument("--shard-level", type=int, default=8)
    parser.add_argument(
        "--engine",
        type=Path,
        help="optional exact campaign executable to include in the frozen digest",
    )
    parser.add_argument(
        "--expected",
        type=Path,
        help="optional frozen aggregate JSON that the replay must match exactly",
    )
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")

    summaries = []
    witnesses = []
    digest_rows = []
    stdout_digest_rows = []
    for index in range(args.shards):
        path = args.outdir / f"shard_{index:04d}.out"
        require(path.is_file(), ("missing shard", index, path))
        text = path.read_text()
        rows = [json.loads(line) for line in text.splitlines() if line.startswith("{")]
        require(len(rows) == 1, ("bad shard summary", index, path))
        row = rows[0]
        require(row["n"] == args.n, ("wrong order", index, row))
        require(row["status"] == "DONE", ("unfinished shard", index, row))
        require(row["shard"] == [index, args.shards, args.shard_level], ("wrong shard key", index, row))
        found = [parse_witness(line) for line in text.splitlines() if line.startswith("SOL:")]
        require(len(found) == row["nsol"], ("witness count mismatch", index, row, len(found)))
        for edges in found:
            ok_a, why_a = checker_a(args.n, edges)
            ok_b, why_b = checker_b(args.n, edges)
            require(ok_a and ok_b, ("witness rejected", index, why_a, why_b, edges))
            witnesses.append(edges)
        summaries.append(row)
        digest_rows.append({key: row[key] for key in ("n", "status", "nsol", "nodes", "shard")})
        stdout_digest_rows.append({"index": index, "sha256": sha256_bytes(text.encode())})

    blob = json.dumps(digest_rows, sort_keys=True, separators=(",", ":")).encode()
    stdout_blob = json.dumps(stdout_digest_rows, sort_keys=True, separators=(",", ":")).encode()
    output = {
        "n": args.n,
        "family": "hop-diameter<=4",
        "shards": args.shards,
        "shard_level": args.shard_level,
        "all_done": True,
        "sum_reported_nodes_including_repeated_prefixes": sum(row["nodes"] for row in summaries),
        "min_shard_nodes": min(row["nodes"] for row in summaries),
        "max_shard_nodes": max(row["nodes"] for row in summaries),
        "sum_reported_cpu_seconds": sum(row["time"] for row in summaries),
        "nsol": sum(row["nsol"] for row in summaries),
        "witnesses_checked_by_a_and_b": len(witnesses),
        "per_shard_sha256": hashlib.sha256(blob).hexdigest(),
        "per_shard_stdout_sha256": sha256_bytes(stdout_blob),
        "engine_source_sha256": sha256_file(ENGINE_SOURCE),
        "checker_a_sha256": sha256_file(REPO / "src" / "checker_a.py"),
        "checker_b_sha256": sha256_file(REPO / "src" / "checker_b.py"),
        "status": "VERIFIED",
    }
    if args.engine is not None:
        output["campaign_engine_sha256"] = sha256_file(args.engine)
    if args.expected is not None:
        require(args.expected.is_file(), ("missing frozen aggregate", args.expected))
        expected = json.loads(args.expected.read_text())
        require(output == expected, ("frozen aggregate mismatch", output, expected))
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
