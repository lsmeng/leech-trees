#!/usr/bin/env python3
"""Build and regression-check the high-pole endpoint AC engine."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = HERE / "threebranch_endpoint_exact.c"
BASE_SOURCE = HERE / "threebranch_exact.c"
RESULT = HERE / "results" / "endpoint_exact_certificate.json"
sys.path.insert(0, str(REPO / "src"))
import checker_a  # noqa: E402
import checker_b  # noqa: E402


EXPECTED = {
    "n11_EP3": [2621, 2, 4, 19, 2, 0, 0, 17, 6, 318, 3580, 984],
    "n11_EP4": [696, 0, 0, 0, 0, 0, 0, 0, 0, 443, 1491, 490],
    "n18_EP3": [2793454, 4908, 7628, 40216, 2720, 0, 0, 18, 9, 1078, 140535, 15820],
    "n18_EP4": [3413707, 1279, 1279, 6663, 0, 0, 0, 18, 9, 2837, 299523, 42005],
}

FIELDS = (
    "anchors_generated",
    "anchors",
    "nodes",
    "candidate_marks",
    "legal_children",
    "frontier",
    "nsol",
    "deepest_missing_offset",
    "max_noncentre_marks",
    "band_masks",
    "band_partition_nodes",
    "band_partitions",
)


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(row: dict[str, object]) -> list[int]:
    return [int(row[field]) for field in FIELDS]


def parse_witness(line: str):
    prefix, payload = line.split("edges=", 1)
    order = int(prefix.split("n=", 1)[1].split()[0])
    edges = []
    for token in payload.strip().split(";"):
        if token:
            edges.append(tuple(map(int, token.split(","))))
    return order, edges


def run(executable: Path, order: int, mode: str, *options: str):
    process = subprocess.run(
        [str(executable), str(order), mode, "--window", "25", *options],
        check=True,
        capture_output=True,
        text=True,
    )
    witnesses = []
    rows = []
    for line in process.stdout.splitlines():
        if line.startswith("WITNESS "):
            witness_order, edges = parse_witness(line)
            ok_a, why_a = checker_a.is_leech(witness_order, edges)
            ok_b, why_b = checker_b.is_leech(witness_order, edges)
            require(ok_a and ok_b, (line, why_a, why_b))
            witnesses.append(edges)
        elif line.startswith("{"):
            rows.append(json.loads(line))
    require(len(rows) == 1, (order, mode, options, process.stdout, process.stderr))
    row = rows[0]
    require(row["status"] == "DONE", row)
    require(row["nsol"] == len(witnesses), (row, witnesses))
    require(row["candidate_pairs"] == 0 and row["legal_pair_children"] == 0, row)
    return row, witnesses


def audit() -> dict[str, object]:
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    with tempfile.TemporaryDirectory(prefix="leech-endpoint-") as directory:
        executable = Path(directory) / "endpoint_exact"
        subprocess.run([
            "cc", "-O3", "-Wall", "-Wextra", "-std=c11",
            str(SOURCE), "-o", str(executable),
        ], check=True, cwd=HERE)

        rows = {}
        witness_count = 0
        for order, mode in ((11, "EP3"), (11, "EP4"), (18, "EP3"), (18, "EP4")):
            key = f"n{order}_{mode}"
            row, witnesses = run(executable, order, mode)
            rows[key] = row
            witness_count += len(witnesses)
            require(compact(row) == EXPECTED[key], (key, compact(row), EXPECTED[key]))

        fast, witnesses = run(executable, 18, "EP3", "--fast")
        witness_count += len(witnesses)
        require(compact(fast) == EXPECTED["n18_EP3"], fast)
        require(fast["paranoid"] == 0, fast)

        shards = []
        for index in range(8):
            row, witnesses = run(
                executable, 18, "EP3", "--shard", str(index), "8"
            )
            witness_count += len(witnesses)
            require(row["shard"] == [index, 8], row)
            shards.append(row)
        summed = [
            sum(int(row[field]) for row in shards)
            for field in FIELDS[:7]
        ]
        require(summed == EXPECTED["n18_EP3"][:7], (summed, EXPECTED["n18_EP3"][:7]))
        require(max(int(row["deepest_missing_offset"]) for row in shards) == 18, shards)
        require(max(int(row["max_noncentre_marks"]) for row in shards) == 9, shards)
        for field, expected in zip(FIELDS[9:], EXPECTED["n18_EP3"][9:]):
            require(all(int(row[field]) == expected for row in shards), (field, shards))

    output = {
        "claim": "outside-band high-pole a=3,4 AC endpoint engine regression",
        "expected_rows": EXPECTED,
        "n18_ep3_shards": 8,
        "n18_ep3_shard_partition": "exact anchor-key partition; band enumeration repeated",
        "witnesses_checked_by_a_and_b": witness_count,
        "endpoint_source_sha256": sha256(SOURCE),
        "verifier_sha256": sha256(Path(__file__)),
        "base_source_sha256": sha256(BASE_SOURCE),
        "checker_a_sha256": sha256(REPO / "src" / "checker_a.py"),
        "checker_b_sha256": sha256(REPO / "src" / "checker_b.py"),
        "status": "VERIFIED",
        "trust_boundary": (
            "Finite outside-band engine regression and sharding audit only. The "
            "all-order outside-band EP4 claim requires the separate symbolic "
            "relaxation; branch-in-band EP4, EP3 and low-pole AB/AC cases are "
            "not covered by this finite certificate."
        ),
    }
    if RESULT.exists():
        require(output == json.loads(RESULT.read_text()), (output, RESULT))
    return output


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
