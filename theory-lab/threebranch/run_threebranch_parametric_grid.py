#!/usr/bin/env python3
"""Run a resumable bounded-concurrency grid of parametric probe cells.

This runner is diagnostic infrastructure.  It preserves every cell's final
``CLOSED``, ``FRONTIER`` or ``UNKNOWN`` status and never promotes a partial
grid to a theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def final_row(path: Path) -> dict[str, object]:
    rows = [json.loads(line) for line in path.read_text().splitlines()
            if line.startswith("{")]
    require(rows, ("no JSON row", path))
    return rows[-1]


def validate(
    path: Path,
    *,
    mode: str,
    window: int,
    fixed_order: int | None,
    nmin: int,
    cell: tuple[int, int, int],
    counts: tuple[int, int, int],
    taylor_residue_modulus: int,
) -> dict[str, object]:
    row = final_row(path)
    require(row["mode"] == mode and row["requested_window"] == window,
            (path, row))
    require(row["fixed_n"] == fixed_order and row["nmin"] == nmin, (path, row))
    expected_shards = [
        [axis, index, count]
        for axis, (index, count) in enumerate(zip(cell, counts), start=1)
        if count > 1
    ]
    require(row["scale_shards"] == expected_shards, (path, row, expected_shards))
    require(row["taylor_residue_modulus"] == taylor_residue_modulus, (path, row))
    require(not row["triangular_tail"] and not row["taylor_tail"], (path, row))
    require(row["status"] in {"CLOSED", "FRONTIER", "UNKNOWN"}, (path, row))
    require(row["solver_unknown"] == 0, (path, row))
    if row["status"] == "CLOSED":
        require(row["frontier_states"] == 0 and not row["capped"], (path, row))
    elif row["status"] == "FRONTIER":
        require(row["frontier_states"] > 0 and not row["capped"], (path, row))
    else:
        require(row["capped"], (path, row))
    return row


def run_cell(
    probe: Path,
    outdir: Path,
    *,
    mode: str,
    window: int,
    fixed_order: int | None,
    nmin: int,
    cell: tuple[int, int, int],
    counts: tuple[int, int, int],
    max_states: int,
    timeout_ms: int,
    memory_mb: int,
    taylor_residue_modulus: int,
) -> dict[str, object]:
    stem = f"{mode}_{cell[0]}_{cell[1]}_{cell[2]}"
    output = outdir / f"{stem}.out"
    error = outdir / f"{stem}.err"
    if output.exists() and error.exists() and error.stat().st_size == 0:
        try:
            return validate(
                output, mode=mode, window=window, fixed_order=fixed_order,
                nmin=nmin, cell=cell, counts=counts,
                taylor_residue_modulus=taylor_residue_modulus,
            )
        except (KeyError, RuntimeError, ValueError, json.JSONDecodeError):
            pass

    command = [
        sys.executable, str(probe), "--mode", mode,
        "--window", str(window), "--nmin", str(nmin),
        "--max-states", str(max_states), "--timeout-ms", str(timeout_ms),
    ]
    if fixed_order is not None:
        command.extend(("--fixed-order", str(fixed_order)))
    if taylor_residue_modulus:
        command.extend(("--taylor-residue-modulus", str(taylor_residue_modulus)))
    for axis, (index, count) in enumerate(zip(cell, counts), start=1):
        if count > 1:
            command.extend((f"--p{axis}-shard", str(index), str(count)))
    command = ["nice", "-n", "10", *command]
    if memory_mb:
        prlimit = shutil.which("prlimit")
        require(prlimit is not None, "--memory-mb requires prlimit")
        command = [prlimit, f"--as={memory_mb * 1024 * 1024}", "--", *command]

    with output.open("w") as stdout, error.open("w") as stderr:
        completed = subprocess.run(command, stdout=stdout, stderr=stderr, check=False)
    require(completed.returncode == 0, ("cell failed", cell, completed.returncode))
    require(error.stat().st_size == 0, ("nonempty stderr", error))
    return validate(
        output, mode=mode, window=window, fixed_order=fixed_order,
        nmin=nmin, cell=cell, counts=counts,
        taylor_residue_modulus=taylor_residue_modulus,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--mode", choices=("AA", "BB", "AB", "AC"), required=True)
    parser.add_argument("--window", type=int, required=True)
    parser.add_argument("--fixed-order", type=int)
    parser.add_argument("--nmin", type=int, default=153)
    parser.add_argument("--p1-count", type=int, default=1)
    parser.add_argument("--p2-count", type=int, default=1)
    parser.add_argument("--p3-count", type=int, default=1)
    parser.add_argument("--workers", type=int, default=32)
    parser.add_argument("--memory-mb", type=int, default=1024)
    parser.add_argument("--max-states", type=int, default=5000)
    parser.add_argument("--timeout-ms", type=int, default=10_000)
    parser.add_argument("--taylor-residue-modulus", type=int, default=0)
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    args.probe = args.probe.resolve()
    args.outdir = args.outdir.resolve()
    require(args.probe.is_file() and args.window >= 1 and args.nmin >= 1, args)
    counts = (args.p1_count, args.p2_count, args.p3_count)
    require(all(count >= 1 for count in counts), counts)
    total = counts[0] * counts[1] * counts[2]
    require(1 <= args.workers <= min(64, total), (args.workers, total))
    require(args.memory_mb >= 0 and args.max_states >= 1 and args.timeout_ms >= 0, args)
    args.outdir.mkdir(parents=True, exist_ok=True)
    z3_version = subprocess.check_output(
        [sys.executable, "-c", "import z3; print(z3.get_version_string())"],
        text=True,
    ).strip()
    manifest = {
        "schema": 1,
        "runner_sha256": sha256(Path(__file__).resolve()),
        "probe_sha256": sha256(args.probe),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "z3_version": z3_version,
        "mode": args.mode,
        "window": args.window,
        "fixed_order": args.fixed_order,
        "nmin": args.nmin,
        "grid": list(counts),
        "workers": args.workers,
        "memory_mb": args.memory_mb,
        "max_states": args.max_states,
        "timeout_ms": args.timeout_ms,
        "taylor_residue_modulus": args.taylor_residue_modulus,
    }
    manifest_path = args.outdir / "run_manifest.json"
    if manifest_path.exists():
        require(json.loads(manifest_path.read_text()) == manifest,
                ("run manifest mismatch", manifest_path))
    else:
        require(not any(args.outdir.glob("*.out"))
                and not any(args.outdir.glob("*.err")),
                ("refusing outputs without a run manifest", args.outdir))
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    cells = [
        (first, second, third)
        for first in range(counts[0])
        for second in range(counts[1])
        for third in range(counts[2])
    ]

    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                run_cell, args.probe, args.outdir,
                mode=args.mode, window=args.window, fixed_order=args.fixed_order,
                nmin=args.nmin, cell=cell, counts=counts,
                max_states=args.max_states, timeout_ms=args.timeout_ms,
                memory_mb=args.memory_mb,
                taylor_residue_modulus=args.taylor_residue_modulus,
            ): cell
            for cell in cells
        }
        for future in as_completed(futures):
            cell = futures[future]
            row = future.result()
            rows.append(row)
            print(json.dumps({
                "cell": cell,
                "status": row["status"],
                "states": row["frontier_states"],
                "offset": row["completed_offset"],
            }, sort_keys=True), flush=True)

    statuses = Counter(str(row["status"]) for row in rows)
    print(json.dumps({
        "status": "DONE",
        "mode": args.mode,
        "window": args.window,
        "fixed_order": args.fixed_order,
        "nmin": args.nmin,
        "grid": counts,
        "workers": args.workers,
        "completed": len(rows),
        "cell_statuses": dict(sorted(statuses.items())),
        "maximum_frontier_states": max(int(row["frontier_states"]) for row in rows),
        "maximum_marks": max(int(row["maximum_marks"]) for row in rows),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
