#!/usr/bin/env python3
"""Verify the exact order-25 three-branch-vertex shard archive."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = HERE / "threebranch_exact.c"
RUNNER = HERE / "run_threebranch_window_shards.py"
ARCHIVE = HERE / "results" / "threebranch_n25_w60_outputs.tar.gz"
RESULT = HERE / "results" / "threebranch_n25_w60_certificate.json"
sys.path.insert(0, str(REPO / "src"))
from checker_a import is_leech as checker_a  # noqa: E402
from checker_b import is_leech as checker_b  # noqa: E402

MODES = ("AA", "BB", "AB", "AC")
SHARDS = 96
EXPECTED_SOURCE_SHA256 = (
    "2e796bf278634c302ffb9fe3510004379a2887b3d5af0e52f7edcfb5764172ac"
)
EXPECTED_RUNNER_SHA256 = (
    "7f1ae1b5aef569008052b25f2dd598ac69547c3f487b304ab56bfb2bfff5c9f0"
)
EXPECTED_ARCHIVE_SHA256 = (
    "499da6e3350bed329502c94a85d32c86f740633a01a426b111fabde0255c675a"
)
EXPECTED = {
    "AA": {
        "anchors_generated": 529_396,
        "anchors": 514_546,
        "nodes": 777_725_356,
        "candidate_marks": 6_717_376_997,
        "candidate_pairs": 0,
        "legal_children": 777_210_810,
        "legal_single_children": 777_210_810,
        "legal_pair_children": 0,
        "frontier": 0,
        "nsol": 0,
        "deepest_missing_offset": 47,
        "max_noncentre_marks": 13,
    },
    "BB": {
        "anchors_generated": 529_396,
        "anchors": 512_875,
        "nodes": 331_552_855,
        "candidate_marks": 2_604_245_256,
        "candidate_pairs": 0,
        "legal_children": 331_039_980,
        "legal_single_children": 331_039_980,
        "legal_pair_children": 0,
        "frontier": 0,
        "nsol": 0,
        "deepest_missing_offset": 38,
        "max_noncentre_marks": 12,
    },
    "AB": {
        "anchors_generated": 3_241_792,
        "anchors": 3_066_710,
        "nodes": 5_778_080_789,
        "candidate_marks": 47_341_809_497,
        "candidate_pairs": 0,
        "legal_children": 5_775_014_079,
        "legal_single_children": 5_775_014_079,
        "legal_pair_children": 0,
        "frontier": 0,
        "nsol": 0,
        "deepest_missing_offset": 49,
        "max_noncentre_marks": 15,
    },
    "AC": {
        "anchors_generated": 2_150_218,
        "anchors": 2_043_332,
        "nodes": 7_277_521_449,
        "candidate_marks": 61_225_949_236,
        "candidate_pairs": 0,
        "legal_children": 7_275_478_117,
        "legal_single_children": 7_275_478_117,
        "legal_pair_children": 0,
        "frontier": 0,
        "nsol": 0,
        "deepest_missing_offset": 51,
        "max_noncentre_marks": 14,
    },
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_witness(line: str) -> tuple[int, list[tuple[int, int, int]]]:
    match = re.fullmatch(
        r"WITNESS n=(\d+) mode=\S+ q1=\d+ q2=\d+ edges=(.*)", line
    )
    require(match is not None, ("bad witness line", line))
    edges = [
        tuple(map(int, token.split(",")))
        for token in match.group(2).split(";")
        if token
    ]
    return int(match.group(1)), edges


def audit() -> dict[str, object]:
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    require(sha256(SOURCE) == EXPECTED_SOURCE_SHA256, "source hash mismatch")
    require(sha256(RUNNER) == EXPECTED_RUNNER_SHA256, "runner hash mismatch")
    require(sha256(ARCHIVE) == EXPECTED_ARCHIVE_SHA256, "archive hash mismatch")

    expected_names = {"outputs"}
    for mode in MODES:
        for index in range(SHARDS):
            expected_names.add(f"outputs/{mode}_{index}.out")
            expected_names.add(f"outputs/{mode}_{index}.err")

    by_mode: dict[str, list[dict[str, object]]] = {mode: [] for mode in MODES}
    witnesses = 0
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        members = archive.getmembers()
        require({member.name for member in members} == expected_names,
                "archive member set mismatch")
        require(len(members) == len(expected_names), "duplicate archive member")
        for mode in MODES:
            for index in range(SHARDS):
                error_member = archive.getmember(f"outputs/{mode}_{index}.err")
                require(error_member.size == 0, ("nonempty stderr", error_member.name))
                output_member = archive.getmember(f"outputs/{mode}_{index}.out")
                stream = archive.extractfile(output_member)
                require(stream is not None, output_member.name)
                text = stream.read().decode("utf-8")
                rows = [
                    json.loads(line)
                    for line in text.splitlines()
                    if line.startswith("{")
                ]
                require(len(rows) == 1, ("summary count", output_member.name, rows))
                row = rows[0]
                require(
                    row["n"] == 25 and row["N"] == 300 and row["mode"] == mode,
                    (output_member.name, row),
                )
                require(row["window"] == 60, (output_member.name, row))
                require(row["shard"] == [index, SHARDS], (output_member.name, row))
                require(row["status"] == "DONE" and row["paranoid"] == 1,
                        (output_member.name, row))
                require(row["pair_mode"] == "one-vertex-lemma",
                        (output_member.name, row))
                require(row["introduction_mode"] == "diameter-endpoints",
                        (output_member.name, row))
                require(row["candidate_pairs"] == row["legal_pair_children"] == 0,
                        (output_member.name, row))
                require(row["legal_children"] == row["legal_single_children"],
                        (output_member.name, row))
                require(row["frontier"] == row["nsol"] == 0,
                        (output_member.name, row))

                witness_lines = [
                    line for line in text.splitlines() if line.startswith("WITNESS ")
                ]
                require(len(witness_lines) == row["nsol"],
                        (output_member.name, witness_lines, row))
                for line in witness_lines:
                    order, edges = parse_witness(line)
                    ok_a, why_a = checker_a(order, edges)
                    ok_b, why_b = checker_b(order, edges)
                    require(ok_a and ok_b,
                            ("witness rejected", output_member.name, why_a, why_b))
                    witnesses += 1
                by_mode[mode].append(row)

    sum_fields = (
        "anchors_generated", "anchors", "nodes", "candidate_marks",
        "candidate_pairs", "legal_children", "legal_single_children",
        "legal_pair_children", "frontier", "nsol",
    )
    summaries = {}
    for mode in MODES:
        rows = by_mode[mode]
        require(len(rows) == SHARDS, (mode, len(rows)))
        summary = {field: sum(int(row[field]) for row in rows) for field in sum_fields}
        summary["deepest_missing_offset"] = max(
            int(row["deepest_missing_offset"]) for row in rows
        )
        summary["max_noncentre_marks"] = max(
            int(row["max_noncentre_marks"]) for row in rows
        )
        require(summary == EXPECTED[mode], ("mode aggregate mismatch", mode, summary))
        summaries[mode] = summary

    totals = {
        field: sum(int(summaries[mode][field]) for mode in MODES)
        for field in sum_fields
    }
    totals["deepest_missing_offset"] = max(
        int(summaries[mode]["deepest_missing_offset"]) for mode in MODES
    )
    totals["max_noncentre_marks"] = max(
        int(summaries[mode]["max_noncentre_marks"]) for mode in MODES
    )
    require(totals["nodes"] == 14_164_880_449, totals)
    require(totals["frontier"] == totals["nsol"] == witnesses == 0, totals)

    output = {
        "claim": "no order-25 Leech tree has exactly three branch vertices",
        "order": 25,
        "window": 60,
        "shards_per_mode": SHARDS,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "runner_sha256": EXPECTED_RUNNER_SHA256,
        "archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "verifier_sha256": sha256(Path(__file__)),
        "modes": summaries,
        "totals": totals,
        "witnesses_checked_by_a_and_b": witnesses,
        "status": "VERIFIED",
        "trust_boundary": (
            "Exact finite order-25 exclusion for the proved exactly-three-branch "
            "normal form, using the previously audited diameter-endpoint and "
            "one-new-vertex theorems. All 384 paranoid shards are DONE with zero "
            "frontier and zero solutions. This does not exclude order-25 trees "
            "with four or more branch vertices and is not an all-order theorem."
        ),
    }
    if RESULT.exists():
        require(output == json.loads(RESULT.read_text()), RESULT)
    return output


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
