#!/usr/bin/env python3
"""Shared strict replay for frozen three-centre shard archives.

This module does not decide which finite order has been proved.  A small
order-specific verifier supplies the frozen hashes and aggregates, while this
file checks the archive topology, every shard summary, and every reported
witness.  A witness is counted only after both repository checkers accept it.
"""

from __future__ import annotations

import json
import re
import sys
import tarfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "src"))
from checker_a import is_leech as checker_a  # noqa: E402
from checker_b import is_leech as checker_b  # noqa: E402


MODES = ("AA", "BB", "AB", "AC")
SUM_FIELDS = (
    "anchors_generated",
    "anchors",
    "nodes",
    "candidate_marks",
    "candidate_pairs",
    "legal_children",
    "legal_single_children",
    "legal_pair_children",
    "frontier",
    "nsol",
)


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


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


def audit_archive(
    archive_path: Path,
    *,
    order: int,
    window: int,
    shards: int,
) -> dict[str, object]:
    """Replay one complete four-mode archive and return exact aggregates."""

    require(sys.flags.optimize == 0, "run without python -O/-OO")
    require(order >= 8 and window >= 1 and shards >= 1, (order, window, shards))
    expected_names = {"outputs"}
    for mode in MODES:
        for index in range(shards):
            expected_names.add(f"outputs/{mode}_{index}.out")
            expected_names.add(f"outputs/{mode}_{index}.err")

    by_mode: dict[str, list[dict[str, object]]] = {mode: [] for mode in MODES}
    witnesses = 0
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        require(len(members) == len(expected_names), "archive member count mismatch")
        require({member.name for member in members} == expected_names,
                "archive member set mismatch")
        require(len({member.name for member in members}) == len(members),
                "duplicate archive member")
        directory = archive.getmember("outputs")
        require(directory.isdir(), "outputs archive member is not a directory")

        for mode in MODES:
            for index in range(shards):
                error_member = archive.getmember(f"outputs/{mode}_{index}.err")
                output_member = archive.getmember(f"outputs/{mode}_{index}.out")
                require(error_member.isfile() and error_member.size == 0,
                        ("bad stderr member", error_member.name, error_member.size))
                require(output_member.isfile(), ("bad stdout member", output_member.name))
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
                    row["n"] == order
                    and row["N"] == order * (order - 1) // 2
                    and row["mode"] == mode,
                    (output_member.name, row),
                )
                require(row["window"] == window, (output_member.name, row))
                require(row["shard"] == [index, shards], (output_member.name, row))
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
                    witness_order, edges = parse_witness(line)
                    require(witness_order == order,
                            ("witness order", output_member.name, witness_order))
                    ok_a, why_a = checker_a(witness_order, edges)
                    ok_b, why_b = checker_b(witness_order, edges)
                    require(ok_a and ok_b,
                            ("witness rejected", output_member.name, why_a, why_b))
                    witnesses += 1
                by_mode[mode].append(row)

    summaries: dict[str, dict[str, int]] = {}
    for mode in MODES:
        rows = by_mode[mode]
        require(len(rows) == shards, (mode, len(rows)))
        summary = {field: sum(int(row[field]) for row in rows) for field in SUM_FIELDS}
        summary["deepest_missing_offset"] = max(
            int(row["deepest_missing_offset"]) for row in rows
        )
        summary["max_noncentre_marks"] = max(
            int(row["max_noncentre_marks"]) for row in rows
        )
        summaries[mode] = summary

    totals = {
        field: sum(summaries[mode][field] for mode in MODES)
        for field in SUM_FIELDS
    }
    totals["deepest_missing_offset"] = max(
        summaries[mode]["deepest_missing_offset"] for mode in MODES
    )
    totals["max_noncentre_marks"] = max(
        summaries[mode]["max_noncentre_marks"] for mode in MODES
    )
    require(totals["frontier"] == totals["nsol"] == witnesses == 0, totals)
    return {
        "modes": summaries,
        "totals": totals,
        "witnesses_checked_by_a_and_b": witnesses,
    }
