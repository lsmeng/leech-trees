#!/usr/bin/env python3
"""Reproduce and verify the exact three-branch-vertex order-18 exclusion."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = HERE / "threebranch_exact.c"
ARCHIVE = HERE / "results" / "exact_n18_intro"
CONSERVATIVE_ARCHIVE = HERE / "results" / "exact_n18_conservative"
sys.path.insert(0, str(REPO / "src"))
from checker_a import is_leech as checker_a  # noqa: E402
from checker_b import is_leech as checker_b  # noqa: E402


EXPECTED = {
    "AA": {
        "anchors_generated": 67_525,
        "anchors": 63_736,
        "nodes": 17_644_207,
        "candidate_marks": 145_254_033,
        "legal_children": 17_580_471,
        "deepest_missing_offset": 38,
        "max_noncentre_marks": 11,
    },
    "BB": {
        "anchors_generated": 67_525,
        "anchors": 63_358,
        "nodes": 12_152_789,
        "candidate_marks": 96_759_109,
        "legal_children": 12_089_431,
        "deepest_missing_offset": 33,
        "max_noncentre_marks": 11,
    },
    "AB": {
        "anchors_generated": 413_475,
        "anchors": 377_686,
        "nodes": 128_532_966,
        "candidate_marks": 1_000_774_086,
        "legal_children": 128_155_280,
        "deepest_missing_offset": 43,
        "max_noncentre_marks": 11,
    },
    "AC": {
        "anchors_generated": 272_875,
        "anchors": 251_520,
        "nodes": 115_149_987,
        "candidate_marks": 891_856_548,
        "legal_children": 114_898_467,
        "deepest_missing_offset": 41,
        "max_noncentre_marks": 11,
    },
}

CONSERVATIVE_CANDIDATES = {
    "AA": (330_366_238, 1_351_900_378),
    "BB": (224_050_521, 908_629_597),
    "AB": (2_781_309_845, 13_531_924_324),
    "AC": (2_686_552_501, 14_138_601_965),
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def parse_summary(output: str) -> dict:
    rows = [json.loads(line) for line in output.splitlines() if line.startswith("{")]
    require(len(rows) == 1, ("expected one summary", output))
    return rows[0]


def parse_witness(line: str) -> tuple[int, list[tuple[int, int, int]]]:
    match = re.fullmatch(r"WITNESS n=(\d+) mode=\S+ q1=\d+ q2=\d+ edges=(.*)", line)
    require(match is not None, ("bad witness line", line))
    edges = []
    for token in match.group(2).split(";"):
        if token:
            edges.append(tuple(map(int, token.split(","))))
    return int(match.group(1)), edges


def check_row(mode: str, row: dict, output: str) -> dict:
    require(row["n"] == 18 and row["N"] == 153 and row["mode"] == mode,
            ("wrong order/mode", mode, row))
    require(row["status"] == "DONE" and row["frontier"] == 0,
            ("unfinished exact run", mode, row))
    require(row["nsol"] == 0 and row["legal_pair_children"] == 0,
            ("unexpected solution/pair child", mode, row))
    require(row["pair_mode"] == "one-vertex-lemma",
            ("wrong pair mode", mode, row))
    require(row["introduction_mode"] == "diameter-endpoints",
            ("wrong introduction mode", mode, row))
    for field, expected in EXPECTED[mode].items():
        require(row[field] == expected,
                ("frozen invariant mismatch", mode, field, row[field], expected))

    witness_lines = [line for line in output.splitlines() if line.startswith("WITNESS ")]
    require(len(witness_lines) == row["nsol"],
            ("witness count mismatch", mode, len(witness_lines), row["nsol"]))
    for line in witness_lines:
        order, edges = parse_witness(line)
        ok_a, why_a = checker_a(order, edges)
        ok_b, why_b = checker_b(order, edges)
        require(ok_a and ok_b, ("witness rejected", mode, why_a, why_b, edges))
    return {
        "mode": mode,
        **EXPECTED[mode],
        "solutions": row["nsol"],
        "frontier": row["frontier"],
        "witnesses_checked_by_a_and_b": len(witness_lines),
    }


def archive_row(mode: str) -> dict:
    path = ARCHIVE / f"{mode}.out"
    require(path.exists(), ("missing archived output", path))
    output = path.read_text()
    return check_row(mode, parse_summary(output), output)


def conservative_archive_row(mode: str) -> dict:
    path = CONSERVATIVE_ARCHIVE / f"{mode}.out"
    require(path.exists(), ("missing conservative output", path))
    output = path.read_text()
    row = parse_summary(output)
    require(row["n"] == 18 and row["N"] == 153 and row["mode"] == mode,
            ("wrong conservative order/mode", mode, row))
    require(row["status"] == "DONE" and row["nsol"] == 0,
            ("unfinished conservative run", mode, row))
    require(row["legal_pair_children"] == 0,
            ("unexpected conservative pair child", mode, row))
    for field in (
        "anchors_generated", "anchors", "nodes", "legal_children",
        "deepest_missing_offset", "max_noncentre_marks",
    ):
        require(row[field] == EXPECTED[mode][field],
                ("conservative/reduced mismatch", mode, field,
                 row[field], EXPECTED[mode][field]))
    expected_marks, expected_pairs = CONSERVATIVE_CANDIDATES[mode]
    require(row["candidate_marks"] == expected_marks,
            ("conservative mark count", mode, row["candidate_marks"], expected_marks))
    require(row["candidate_pairs"] == expected_pairs,
            ("conservative pair count", mode, row["candidate_pairs"], expected_pairs))
    witness_lines = [line for line in output.splitlines() if line.startswith("WITNESS ")]
    require(not witness_lines, ("unexpected conservative witness", mode, witness_lines))
    return {
        "mode": mode,
        "candidate_marks": row["candidate_marks"],
        "candidate_pairs": row["candidate_pairs"],
        "legal_pair_children": row["legal_pair_children"],
        "nodes": row["nodes"],
        "solutions": row["nsol"],
    }


def build(binary: Path) -> None:
    process = subprocess.run(
        ["cc", "-O3", "-std=c11", "-Wall", "-Wextra", "-pedantic",
         "-o", str(binary), str(SOURCE)],
        capture_output=True, text=True, check=False,
    )
    require(process.returncode == 0, ("build failure", process.stdout, process.stderr))


def reproduce(binary: Path, mode: str) -> dict:
    process = subprocess.run(
        [str(binary), "18", mode, "--no-pairs", "--diameter-intro"],
        capture_output=True, text=True, check=False,
    )
    require(process.returncode == 0,
            ("local reproduction failure", mode, process.stdout, process.stderr))
    return check_row(mode, parse_summary(process.stdout), process.stdout)


def totals(rows: list[dict]) -> dict:
    return {
        "anchors_generated": sum(row["anchors_generated"] for row in rows),
        "anchors": sum(row["anchors"] for row in rows),
        "nodes": sum(row["nodes"] for row in rows),
        "candidate_marks": sum(row["candidate_marks"] for row in rows),
        "legal_children": sum(row["legal_children"] for row in rows),
        "solutions": sum(row["solutions"] for row in rows),
        "frontier": sum(row["frontier"] for row in rows),
        "deepest_missing_offset": max(row["deepest_missing_offset"] for row in rows),
        "max_noncentre_marks": max(row["max_noncentre_marks"] for row in rows),
        "witnesses_checked_by_a_and_b": sum(
            row["witnesses_checked_by_a_and_b"] for row in rows
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-only", action="store_true",
                        help="check frozen geo-ws rows without recomputing")
    args = parser.parse_args()
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    modes = ["AA", "BB", "AB", "AC"]
    archived = [archive_row(mode) for mode in modes]
    conservative = [conservative_archive_row(mode) for mode in modes]
    reproduced = None
    if not args.archive_only:
        with tempfile.TemporaryDirectory(prefix="leech-threebranch-n18-") as temporary:
            binary = Path(temporary) / "threebranch_exact"
            build(binary)
            with ThreadPoolExecutor(max_workers=4) as pool:
                reproduced = list(pool.map(lambda mode: reproduce(binary, mode), modes))
        require(reproduced == archived,
                ("local/geo-ws invariant mismatch", reproduced, archived))

    output = {
        "claim": "no order-18 Leech tree has exactly three branch vertices",
        "geo_ws_modes": archived,
        "geo_ws_totals": totals(archived),
        "conservative_pair_enumeration": {
            "modes": conservative,
            "candidate_marks": sum(row["candidate_marks"] for row in conservative),
            "candidate_pairs": sum(row["candidate_pairs"] for row in conservative),
            "legal_pair_children": sum(row["legal_pair_children"] for row in conservative),
            "nodes": sum(row["nodes"] for row in conservative),
            "solutions": sum(row["solutions"] for row in conservative),
        },
        "local_reproduction": None if reproduced is None else totals(reproduced),
        "status": "VERIFIED",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
