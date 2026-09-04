#!/usr/bin/env python3
"""Build and audit the C/bitset exact three-centre engine."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "threebranch_exact.c"
BINARY = HERE / "threebranch_exact"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "theory-lab" / "exp-families"))

import checker_a  # noqa: E402
import checker_b  # noqa: E402
from gen_shapes import gen_threebranch  # noqa: E402
from threebranch_cleanroom import (  # noqa: E402
    Geometry,
    State,
    Stats,
    child_states,
    vertices,
)


EXPECTED_ALL = {
    8: {"anchors_generated": 3246, "anchors": 1473, "nodes": 2663,
        "legal_children": 1190, "nsol": 0, "deepest_missing_offset": 10,
        "max_noncentre_marks": 4},
    9: {"anchors_generated": 7816, "anchors": 4804, "nodes": 21350,
        "legal_children": 16546, "nsol": 0, "deepest_missing_offset": 18,
        "max_noncentre_marks": 5},
    10: {"anchors_generated": 16800, "anchors": 12289, "nodes": 107677,
         "legal_children": 95388, "nsol": 0, "deepest_missing_offset": 20,
         "max_noncentre_marks": 6},
}

EXPECTED_N10_MODES = {
    "AA": {"anchors_generated": 1330, "anchors": 1056, "nodes": 10076,
           "legal_children": 9020, "nsol": 0, "deepest_missing_offset": 17,
           "max_noncentre_marks": 6},
    "BB": {"anchors_generated": 1330, "anchors": 1042, "nodes": 6708,
           "legal_children": 5666, "nsol": 0, "deepest_missing_offset": 17,
           "max_noncentre_marks": 5},
    "AB": {"anchors_generated": 8610, "anchors": 6123, "nodes": 54140,
           "legal_children": 48017, "nsol": 0, "deepest_missing_offset": 20,
           "max_noncentre_marks": 6},
    "AC": {"anchors_generated": 5530, "anchors": 4068, "nodes": 36753,
           "legal_children": 32685, "nsol": 0, "deepest_missing_offset": 20,
           "max_noncentre_marks": 6},
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def build() -> None:
    process = subprocess.run(
        ["cc", "-O3", "-std=c11", "-Wall", "-Wextra", "-pedantic",
         "-o", str(BINARY), str(SOURCE)],
        capture_output=True, text=True, check=False,
    )
    require(process.returncode == 0, f"C build failed:\n{process.stdout}\n{process.stderr}")


def verify_witness_line(line: str) -> None:
    fields = dict(piece.split("=", 1) for piece in line.split()[1:])
    witness_n = int(fields["n"])
    edges = [tuple(map(int, item.split(",")))
             for item in fields["edges"].rstrip(";").split(";")]
    ok_a, reason_a = checker_a.is_leech(witness_n, edges)
    ok_b, reason_b = checker_b.is_leech(witness_n, edges)
    require(ok_a, f"checker_a rejected C witness: {reason_a} {edges}")
    require(ok_b, f"checker_b rejected C witness: {reason_b} {edges}")


def run_engine(*arguments: str):
    process = subprocess.run([str(BINARY), *arguments], capture_output=True,
                             text=True, check=False)
    require(process.returncode == 0,
            f"C engine failed {arguments}:\n{process.stdout}\n{process.stderr}")
    summary = None
    witness_count = 0
    for line in process.stdout.splitlines():
        if line.startswith("WITNESS "):
            verify_witness_line(line)
            witness_count += 1
        elif line.startswith("{"):
            summary = json.loads(line)
    require(summary is not None, f"missing JSON summary for {arguments}")
    if "nsol" in summary:
        require(summary["nsol"] == witness_count,
                f"witness count mismatch {arguments}: {summary['nsol']} != {witness_count}")
    return summary


def relevant(summary):
    fields = ("anchors_generated", "anchors", "nodes", "legal_children", "nsol",
              "deepest_missing_offset", "max_noncentre_marks", "status")
    return {field: summary[field] for field in fields}


def verify_python_invariants() -> None:
    rows = {}
    for order, expected in EXPECTED_ALL.items():
        paranoid = run_engine(str(order), "all")
        fast = run_engine(str(order), "all", "--fast")
        require(paranoid["status"] == "DONE" and fast["status"] == "DONE",
                f"unfinished C calibration n={order}")
        for field, value in expected.items():
            require(paranoid[field] == value,
                    f"Python invariant mismatch n={order} {field}: "
                    f"C={paranoid[field]} Python={value}")
        require(relevant(paranoid) == relevant(fast),
                f"paranoid/fast mismatch n={order}: {relevant(paranoid)} {relevant(fast)}")
        rows[order] = relevant(paranoid)
    print("PASS C equals Python per-level invariants n=8..10:", rows)

    mode_rows = {}
    for mode, expected in EXPECTED_N10_MODES.items():
        summary = run_engine("10", mode)
        for field, value in expected.items():
            require(summary[field] == value,
                    f"mode mismatch n=10 {mode} {field}: {summary[field]} != {value}")
        mode_rows[mode] = relevant(summary)
    print("PASS C equals Python per-mode invariants at n=10:", mode_rows)


def verify_pair_probe() -> None:
    state = State(((), (), ()), ())
    geometry = Geometry(2, 3, ((), (), ()), (10, 10, 10))
    children = child_states(state, geometry, 20, 8, 28, Stats())
    expected = sum(len(vertices(child)) == 2 for child in children)
    require(expected == 3, f"independent brute pair count changed: {expected}")
    summary = run_engine("--pair-probe")
    require(summary["status"] == "PASS", f"C pair probe failed: {summary}")
    require(summary["legal_pair_children"] == expected,
            f"C/brute pair mismatch: {summary['legal_pair_children']} != {expected}")
    print("PASS two-new-mark C probe equals brute enumeration: 3 children")


def fixed_topology_n11() -> int:
    lines = []
    shape_count = 0
    for edges, tags in gen_threebranch(11):
        line = "11 " + " ".join(f"{u} {v}" for u, v in edges)
        line += " G " + " ".join(f"{group} {branch}" for group, branch in tags)
        lines.append(line + "\n")
        shape_count += 1
    binary = ROOT / "theory-lab" / "exp-families" / "forced_family"
    process = subprocess.run([str(binary), "0"], input="".join(lines),
                             capture_output=True, text=True, check=False)
    require(process.returncode == 0, f"fixed topology n=11 failed: {process.stderr}")
    results = []
    for line in process.stdout.splitlines():
        if line.startswith("WITNESS "):
            # forced_family uses the same edge triple encoding after edges=.
            verify_witness_line(line)
        elif line.startswith("RES "):
            fields = dict(piece.split("=") for piece in line.split()[1:])
            require(int(fields["capped"]) == 0, f"fixed topology capped: {line}")
            results.append(int(fields["found"]))
    require(len(results) == shape_count == 74,
            f"unexpected n=11 shape/result count {shape_count}/{len(results)}")
    return sum(results)


def verify_extended_ladder() -> None:
    fixed = fixed_topology_n11()
    require(fixed == 0, f"unexpected fixed-topology n=11 solutions: {fixed}")
    rows = {}
    for order in (11, 12):
        paranoid = run_engine(str(order), "all")
        fast = run_engine(str(order), "all", "--fast")
        require(paranoid["status"] == "DONE" and paranoid["nsol"] == 0,
                f"unexpected C result n={order}: {paranoid}")
        require(relevant(paranoid) == relevant(fast),
                f"extended paranoid/fast mismatch n={order}")
        rows[order] = relevant(paranoid)
    require(rows[11]["nsol"] == fixed,
            f"independent n=11 solution mismatch C={rows[11]['nsol']} fixed={fixed}")
    print("PASS extended C ladder n=11,12 and independent fixed-topology n=11:", rows)


def verify_window_sharding() -> None:
    full = run_engine("10", "all", "--no-pairs", "--window", "20")
    shards = [run_engine("10", "all", "--no-pairs", "--window", "20",
                         "--shard", str(index), "3") for index in range(3)]
    additive = (
        "anchors_generated", "anchors", "nodes", "candidate_marks",
        "candidate_pairs", "legal_children", "legal_single_children",
        "legal_pair_children", "frontier", "nsol",
    )
    for field in additive:
        total = sum(row[field] for row in shards)
        require(total == full[field],
                f"shard sum mismatch {field}: {total} != {full[field]}")
    for field in ("deepest_missing_offset", "max_noncentre_marks"):
        value = max(row[field] for row in shards)
        require(value == full[field],
                f"shard max mismatch {field}: {value} != {full[field]}")
    require(all(row["status"] == "DONE" for row in shards), "unfinished shard audit")
    print("PASS window/shard partition: K=3 sums to unsharded n=10 W=20 invariants")


def main() -> None:
    build()
    verify_pair_probe()
    verify_python_invariants()
    verify_extended_ladder()
    verify_window_sharding()
    print("PASS complete C/bitset three-centre validation ladder")


if __name__ == "__main__":
    main()
