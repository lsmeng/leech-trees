#!/usr/bin/env python3
"""Rebuild and verify the hop-diameter-at-most-four search certificate."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "src"))
from checker_a import is_leech as checker_a  # noqa: E402
from checker_b import is_leech as checker_b  # noqa: E402
from d4_cleanroom import search as cleanroom_search  # noqa: E402


C_LADDER = {
    2: (2, 1),
    3: (3, 1),
    4: (6, 2),
    5: (11, 0),
    6: (47, 1),
    7: (178, 0),
    8: (497, 0),
    9: (1_289, 0),
    10: (3_311, 0),
    11: (8_778, 0),
    12: (24_264, 0),
    13: (70_639, 0),
    14: (216_040, 0),
    15: (690_247, 0),
    16: (2_282_083, 0),
    17: (7_767_003, 0),
    18: (27_157_047, 0),
}

CLEANROOM_LADDER = {
    2: (2, 1),
    3: (3, 1),
    4: (8, 2),
    5: (18, 0),
    6: (78, 1),
    7: (309, 0),
    8: (1_086, 0),
    9: (3_976, 0),
    10: (14_446, 0),
    11: (54_546, 0),
    12: (199_009, 0),
    13: (723_070, 0),
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def parse_witness(line: str):
    edges = []
    require(line.startswith("SOL:"), ("bad witness line", line))
    for token in line[len("SOL:") :].split():
        match = re.fullmatch(r"(\d+)-(\d+):(\d+)", token)
        require(match is not None, ("bad witness token", token))
        edges.append(tuple(map(int, match.groups())))
    return edges


def check_witness(n: int, edges) -> None:
    ok_a, why_a = checker_a(n, edges)
    ok_b, why_b = checker_b(n, edges)
    require(ok_a and ok_b, ("witness rejected", n, why_a, why_b, edges))


def compile_engine(build_dir: Path, *, ablate_endgame: bool = False) -> Path:
    requested = os.environ.get("CXX")
    compiler = requested or next(
        (candidate for candidate in ("c++", "g++", "clang++") if shutil.which(candidate)),
        None,
    )
    require(compiler is not None, "no C++17 compiler found; set CXX")
    binary = build_dir / ("forest_search_d4_ablate" if ablate_endgame else "forest_search_d4")
    command = [
        compiler,
        "-O3",
        "-std=c++17",
        "-DNW=5",
    ]
    if ablate_endgame:
        command.append("-DD4_NO_ENDGAME")
    command.extend([str(HERE / "forest_search_d4.cpp"), "-o", str(binary)])
    subprocess.run(command, check=True)
    return binary


def run_c_order(binary: Path, n: int):
    expected_nodes, expected_solutions = C_LADDER[n]
    command = [str(binary), str(n)]
    if expected_solutions == 0:
        command.append("-q")
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    witnesses = [parse_witness(line) for line in result.stdout.splitlines() if line.startswith("SOL:")]
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    require(len(rows) == 1, ("expected one C summary", n, result.stdout))
    row = rows[0]
    require(row["status"] == "DONE", ("incomplete C order", n, row))
    require(row["nodes"] == expected_nodes, ("C node mismatch", n, row, expected_nodes))
    require(row["nsol"] == expected_solutions, ("C solution mismatch", n, row, expected_solutions))
    require(len(witnesses) == expected_solutions, ("C witness count", n, len(witnesses), expected_solutions))
    for edges in witnesses:
        check_witness(n, edges)
    return {
        "n": n,
        "nodes": row["nodes"],
        "solutions": row["nsol"],
        "witnesses_checked_twice": len(witnesses),
    }


def run_cleanroom_order(n: int):
    expected_nodes, expected_solutions = CLEANROOM_LADDER[n]
    solutions, stats = cleanroom_search(n)
    require(not stats["timeout"], ("clean-room timeout", n))
    require(stats["nodes"] == expected_nodes, ("clean-room node mismatch", n, stats, expected_nodes))
    require(len(solutions) == expected_solutions, ("clean-room solution mismatch", n, len(solutions), expected_solutions))
    for edges in solutions:
        check_witness(n, edges)
    return {
        "n": n,
        "nodes": stats["nodes"],
        "solutions": len(solutions),
        "witnesses_checked_twice": len(solutions),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=18)
    parser.add_argument("--cleanroom-max", type=int, default=13)
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--skip-planted", action="store_true")
    parser.add_argument("--skip-ablation", action="store_true")
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    require(2 <= args.max_order <= 18, "max-order must be in 2..18")
    require(1 <= args.cleanroom_max <= 13, "cleanroom-max must be in 1..13")
    require(1 <= args.jobs <= 3, "jobs must be in 1..3")

    with tempfile.TemporaryDirectory(prefix="leech-d4-") as tmp:
        binary = compile_engine(Path(tmp))
        c_orders = list(range(2, args.max_order + 1))
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            c_rows = list(pool.map(lambda n: run_c_order(binary, n), c_orders))
        planted = None
        if not args.skip_planted:
            result = subprocess.run(
                [sys.executable, str(HERE / "test_planted.py"), str(binary)],
                check=True,
                capture_output=True,
                text=True,
            )
            planted = json.loads(result.stdout.splitlines()[-1])
            require(planted["status"] == "VERIFIED" and planted["misses"] == 0, planted)
        ablation = None
        if not args.skip_ablation:
            ablated_binary = compile_engine(Path(tmp), ablate_endgame=True)
            result = subprocess.run(
                [str(ablated_binary), "17", "-q"],
                check=True,
                capture_output=True,
                text=True,
            )
            rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
            require(len(rows) == 1, ("bad ablation output", result.stdout, result.stderr))
            ablation = rows[0]
            require(
                ablation["status"] == "DONE"
                and ablation["nsol"] == 0
                and ablation["nodes"] == 47_986_068,
                ("endgame ablation mismatch", ablation),
            )

    clean_orders = list(range(2, args.cleanroom_max + 1))
    clean_rows = [run_cleanroom_order(n) for n in clean_orders]
    for n in range(2, min(args.max_order, args.cleanroom_max) + 1):
        require(
            c_rows[n - 2]["solutions"] == clean_rows[n - 2]["solutions"],
            ("implementation solution mismatch", n),
        )

    output = {
        "family": "hop-diameter<=4",
        "c_orders": c_rows,
        "c_total_nodes": sum(row["nodes"] for row in c_rows),
        "cleanroom_orders": clean_rows,
        "cleanroom_total_nodes": sum(row["nodes"] for row in clean_rows),
        "positive_witnesses_checked_by_a_and_b": sum(row["witnesses_checked_twice"] for row in c_rows),
        "planted_controls": planted,
        "endgame_ablation_n17": ablation,
        "status": "VERIFIED",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
