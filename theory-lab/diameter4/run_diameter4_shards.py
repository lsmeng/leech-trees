#!/usr/bin/env python3
"""Run resumable independent shards of the diameter-four forest search."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parse_summary(text: str):
    rows = [json.loads(line) for line in text.splitlines() if line.startswith("{")]
    require(len(rows) == 1, ("expected one summary", text[-2000:]))
    return rows[0]


def completed(path: Path, n: int, index: int, shards: int, level: int):
    if not path.exists():
        return None
    row = parse_summary(path.read_text())
    expected = [index, shards, level]
    require(row["n"] == n and row["shard"] == expected, ("stale shard file", path, row, expected))
    return row if row["status"] == "DONE" else None


def run_one(engine: Path, n: int, index: int, shards: int, level: int, outdir: Path):
    output_path = outdir / f"shard_{index:04d}.out"
    error_path = outdir / f"shard_{index:04d}.err"
    old = completed(output_path, n, index, shards, level)
    if old is not None:
        return {"index": index, "skipped": True, **old}
    result = subprocess.run(
        [str(engine), str(n), "--shard", str(index), str(shards), "--shard-level", str(level)],
        capture_output=True,
        text=True,
    )
    require(result.returncode == 0, ("engine failed", index, result.returncode, result.stderr[-2000:]))
    row = parse_summary(result.stdout)
    require(row["status"] == "DONE", ("incomplete shard", index, row))
    require(row["n"] == n and row["shard"] == [index, shards, level], ("wrong shard", index, row))
    temporary_output = outdir / f".shard_{index:04d}.{os.getpid()}.out.tmp"
    temporary_error = outdir / f".shard_{index:04d}.{os.getpid()}.err.tmp"
    temporary_output.write_text(result.stdout)
    temporary_error.write_text(result.stderr)
    os.replace(temporary_output, output_path)
    os.replace(temporary_error, error_path)
    return {"index": index, "skipped": False, **row}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("engine", type=Path)
    parser.add_argument("n", type=int)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--shards", type=int, default=512)
    parser.add_argument("--shard-level", type=int, default=8)
    parser.add_argument("--jobs", type=int, default=64)
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    require(args.engine.is_file(), ("missing engine", args.engine))
    require(2 <= args.n <= 27, "n must be in 2..27 for this source")
    require(args.shards >= 1 and args.jobs >= 1, "shards and jobs must be positive")
    require(0 <= args.shard_level < args.n, "invalid shard level")
    args.outdir.mkdir(parents=True, exist_ok=True)

    done = 0
    total_nodes = 0
    total_solutions = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                run_one,
                args.engine.resolve(),
                args.n,
                index,
                args.shards,
                args.shard_level,
                args.outdir.resolve(),
            ): index
            for index in range(args.shards)
        }
        for future in as_completed(futures):
            row = future.result()
            done += 1
            total_nodes += row["nodes"]
            total_solutions += row["nsol"]
            print(
                json.dumps(
                    {
                        "completed": done,
                        "index": row["index"],
                        "nodes": row["nodes"],
                        "solutions_so_far": total_solutions,
                        "sum_reported_nodes_so_far": total_nodes,
                        "total": args.shards,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    print(json.dumps({"n": args.n, "completed": done, "shards": args.shards,
                      "sum_reported_nodes": total_nodes, "nsol": total_solutions,
                      "status": "DONE"}, sort_keys=True))


if __name__ == "__main__":
    main()
