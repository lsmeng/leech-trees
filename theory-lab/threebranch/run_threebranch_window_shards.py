#!/usr/bin/env python3
"""Run resumable exact three-branch window shards with bounded concurrency.

Every completed shard is checked immediately.  A reported witness is accepted
only after both repository witness checkers accept it.  Existing valid outputs
are reused, so an interrupted campaign can be resumed without rerunning them.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = next(
    (
        parent
        for parent in (HERE, *HERE.parents)
        if (parent / "src" / "checker_a.py").is_file()
        and (parent / "src" / "checker_b.py").is_file()
    ),
    None,
)
if REPO is None:
    raise RuntimeError("cannot locate repository witness checkers")
sys.path.insert(0, str(REPO / "src"))
from checker_a import is_leech as checker_a  # noqa: E402
from checker_b import is_leech as checker_b  # noqa: E402

MODES = ("AA", "BB", "AB", "AC")


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def parse_witness(line: str) -> tuple[int, list[tuple[int, int, int]]]:
    fields = dict(piece.split("=", 1) for piece in line.split()[1:])
    order = int(fields["n"])
    edges = [
        tuple(map(int, item.split(",")))
        for item in fields["edges"].rstrip(";").split(";")
        if item
    ]
    return order, edges


def validate_output(
    path: Path,
    *,
    order: int,
    mode: str,
    window: int,
    index: int,
    shards: int,
) -> dict[str, object]:
    lines = path.read_text().splitlines()
    summaries = [json.loads(line) for line in lines if line.startswith("{")]
    require(len(summaries) == 1, ("summary count", path, len(summaries)))
    row = summaries[0]
    require(row["n"] == order and row["mode"] == mode, (path, row))
    require(row["window"] == window, (path, row))
    require(row["shard"] == [index, shards], (path, row))
    require(row["status"] == "DONE", ("unfinished shard", path, row))
    require(row["paranoid"] == 1, ("nonparanoid shard", path, row))
    require(row["pair_mode"] == "one-vertex-lemma", (path, row))
    require(row["introduction_mode"] == "diameter-endpoints", (path, row))
    witness_lines = [line for line in lines if line.startswith("WITNESS ")]
    require(len(witness_lines) == row["nsol"], (path, witness_lines, row))
    for line in witness_lines:
        witness_order, edges = parse_witness(line)
        ok_a, why_a = checker_a(witness_order, edges)
        ok_b, why_b = checker_b(witness_order, edges)
        require(ok_a and ok_b, ("witness rejected", path, why_a, why_b, edges))
    return row


def run_one(
    engine: Path,
    outdir: Path,
    *,
    order: int,
    mode: str,
    window: int,
    index: int,
    shards: int,
    memory_mb: int,
) -> dict[str, object]:
    output = outdir / f"{mode}_{index}.out"
    error = outdir / f"{mode}_{index}.err"
    if output.exists() and error.exists() and error.stat().st_size == 0:
        try:
            return validate_output(
                output,
                order=order,
                mode=mode,
                window=window,
                index=index,
                shards=shards,
            )
        except (KeyError, RuntimeError, ValueError, json.JSONDecodeError):
            pass

    command = [
        "nice", "-n", "10", str(engine), str(order), mode,
        "--no-pairs", "--diameter-intro", "--window", str(window),
        "--shard", str(index), str(shards),
    ]
    if memory_mb:
        prlimit = shutil.which("prlimit")
        require(prlimit is not None, "--memory-mb requires prlimit")
        command = [prlimit, f"--as={memory_mb * 1024 * 1024}", "--", *command]
    with output.open("w") as stdout, error.open("w") as stderr:
        completed = subprocess.run(
            command,
            stdout=stdout,
            stderr=stderr,
            check=False,
        )
    require(completed.returncode == 0, ("shard failed", mode, index, completed.returncode))
    require(error.stat().st_size == 0, ("nonempty stderr", error))
    return validate_output(
        output,
        order=order,
        mode=mode,
        window=window,
        index=index,
        shards=shards,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--window", type=int, required=True)
    parser.add_argument("--shards", type=int, default=96)
    parser.add_argument("--workers", type=int, default=32)
    parser.add_argument("--memory-mb", type=int, default=0)
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    args.engine = args.engine.resolve()
    args.outdir = args.outdir.resolve()
    require(args.engine.is_file(), args.engine)
    require(args.order >= 2 and args.window >= 1, args)
    require(args.shards >= 1 and 1 <= args.workers <= args.shards, args)
    require(args.memory_mb >= 0, args)
    args.outdir.mkdir(parents=True, exist_ok=True)

    jobs = [(mode, index) for mode in MODES for index in range(args.shards)]
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                run_one,
                args.engine,
                args.outdir,
                order=args.order,
                mode=mode,
                window=args.window,
                index=index,
                shards=args.shards,
                memory_mb=args.memory_mb,
            ): (mode, index)
            for mode, index in jobs
        }
        for future in as_completed(futures):
            mode, index = futures[future]
            row = future.result()
            rows.append(row)
            print(json.dumps({
                "completed": [mode, index],
                "nodes": row["nodes"],
                "frontier": row["frontier"],
                "nsol": row["nsol"],
            }, sort_keys=True), flush=True)

    print(json.dumps({
        "status": "DONE",
        "order": args.order,
        "window": args.window,
        "shards": args.shards,
        "workers": args.workers,
        "completed": len(rows),
        "nodes": sum(int(row["nodes"]) for row in rows),
        "frontier": sum(int(row["frontier"]) for row in rows),
        "nsol": sum(int(row["nsol"]) for row in rows),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
