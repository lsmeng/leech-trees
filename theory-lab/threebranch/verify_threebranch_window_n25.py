#!/usr/bin/env python3
"""Audit the completed order-25, width-25 three-branch diagnostic shards.

This is intentionally *not* an UNSAT verifier: a nonzero frontier means the
windowed search stopped before exact exhaustion.  The promoted conclusion is
only that width 25 is insufficient in every anchor class.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ARCHIVE = HERE / "results" / "window_n25_w25_intro_k6"
SOURCE = HERE / "threebranch_exact.c"
sys.path.insert(0, str(REPO / "src"))
from checker_a import is_leech as checker_a  # noqa: E402
from checker_b import is_leech as checker_b  # noqa: E402


EXPECTED_SOURCE_SHA256 = "2e796bf278634c302ffb9fe3510004379a2887b3d5af0e52f7edcfb5764172ac"
EXPECTED_ARCHIVE_SHA256 = "9e6d34ab3777b54d5370fcd4beaabbd9aa00db688b4efd8f109ee2644efcb420"
EXPECTED_MODES = {
    "AA": {
        "anchors_generated": 529_396,
        "anchors": 514_546,
        "nodes": 776_414_700,
        "candidate_marks": 6_636_765_470,
        "legal_children": 775_900_154,
        "frontier": 3_543_964,
        "deepest_missing_offset": 38,
    },
    "BB": {
        "anchors_generated": 529_396,
        "anchors": 512_875,
        "nodes": 331_342_935,
        "candidate_marks": 2_589_996_564,
        "legal_children": 330_830_060,
        "frontier": 700_550,
        "deepest_missing_offset": 33,
    },
    "AB": {
        "anchors_generated": 3_241_792,
        "anchors": 3_066_710,
        "nodes": 5_771_611_903,
        "candidate_marks": 46_765_267_602,
        "legal_children": 5_768_545_193,
        "frontier": 44_969_254,
        "deepest_missing_offset": 40,
    },
    "AC": {
        "anchors_generated": 2_150_218,
        "anchors": 2_043_332,
        "nodes": 7_269_546_988,
        "candidate_marks": 60_005_727_159,
        "legal_children": 7_267_503_656,
        "frontier": 117_107_310,
        "deepest_missing_offset": 40,
    },
}
EXPECTED_TOTALS = {
    "anchors_generated": 6_450_802,
    "anchors": 6_137_463,
    "nodes": 14_148_916_526,
    "candidate_marks": 115_997_756_795,
    "candidate_pairs": 0,
    "legal_children": 14_142_779_063,
    "legal_single_children": 14_142_779_063,
    "legal_pair_children": 0,
    "frontier": 166_321_078,
    "nsol": 0,
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def parse_witness(line: str) -> tuple[int, list[tuple[int, int, int]]]:
    match = re.fullmatch(r"WITNESS n=(\d+) mode=\S+ q1=\d+ q2=\d+ edges=(.*)", line)
    require(match is not None, ("bad witness line", line))
    edges = [tuple(map(int, token.split(",")))
             for token in match.group(2).split(";") if token]
    return int(match.group(1)), edges


def audit() -> dict:
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256,
            "threebranch source changed; rerun/review the diagnostic before promotion")
    output_paths = sorted(ARCHIVE.glob("*.out"))
    error_paths = sorted(ARCHIVE.glob("*.err"))
    require(len(output_paths) == 24 and len(error_paths) == 24,
            ("wrong shard file count", len(output_paths), len(error_paths)))
    require(sum(path.stat().st_size for path in error_paths) == 0,
            "nonempty stderr archive")
    archive_digest = hashlib.sha256(
        b"".join(path.read_bytes() for path in output_paths)
    ).hexdigest()
    require(archive_digest == EXPECTED_ARCHIVE_SHA256,
            ("archive hash mismatch", archive_digest, EXPECTED_ARCHIVE_SHA256))

    mode_rows = {mode: [] for mode in EXPECTED_MODES}
    witnesses = 0
    seen_shards = set()
    for path in output_paths:
        lines = path.read_text().splitlines()
        summaries = [json.loads(line) for line in lines if line.startswith("{")]
        require(len(summaries) == 1, ("wrong summary count", path, summaries))
        row = summaries[0]
        mode = row["mode"]
        require(mode in mode_rows, ("unknown mode", path, mode))
        require(row["n"] == 25 and row["N"] == 300 and row["window"] == 25,
                ("wrong target", path, row))
        require(row["status"] == "DONE" and row["paranoid"] == 1,
                ("unfinished/nonparanoid shard", path, row))
        require(row["pair_mode"] == "one-vertex-lemma",
                ("wrong pair mode", path, row))
        require(row["introduction_mode"] == "diameter-endpoints",
                ("wrong introduction mode", path, row))
        require(row["candidate_pairs"] == 0 and row["legal_pair_children"] == 0,
                ("unexpected two-new branch", path, row))
        require(row["legal_children"] == row["legal_single_children"],
                ("child accounting mismatch", path, row))
        require(row["nsol"] == 0 and row["frontier"] >= 0,
                ("diagnostic conclusion changed", path, row))
        shard = tuple(row["shard"])
        require(shard[1] == 6 and 0 <= shard[0] < 6,
                ("bad shard", path, shard))
        require((mode, shard[0]) not in seen_shards,
                ("duplicate shard", mode, shard))
        seen_shards.add((mode, shard[0]))
        require(path.name == f"{mode}_{shard[0]}.out",
                ("file/summary mismatch", path, mode, shard))

        witness_lines = [line for line in lines if line.startswith("WITNESS ")]
        require(len(witness_lines) == row["nsol"],
                ("witness count mismatch", path, witness_lines, row["nsol"]))
        for line in witness_lines:
            order, edges = parse_witness(line)
            ok_a, why_a = checker_a(order, edges)
            ok_b, why_b = checker_b(order, edges)
            require(ok_a and ok_b, ("witness rejected", path, why_a, why_b, edges))
            witnesses += 1
        mode_rows[mode].append(row)

    require(len(seen_shards) == 24, ("incomplete shard partition", seen_shards))
    fields = (
        "anchors_generated", "anchors", "nodes", "candidate_marks",
        "candidate_pairs", "legal_children", "legal_single_children",
        "legal_pair_children", "frontier", "nsol",
    )
    mode_summaries = {}
    totals = {field: 0 for field in fields}
    for mode, rows in mode_rows.items():
        require(len(rows) == 6, ("mode shard count", mode, len(rows)))
        summary = {field: sum(row[field] for row in rows) for field in fields}
        summary["deepest_missing_offset"] = max(
            row["deepest_missing_offset"] for row in rows
        )
        for field, expected in EXPECTED_MODES[mode].items():
            require(summary[field] == expected,
                    ("mode invariant mismatch", mode, field, summary[field], expected))
        require(summary["frontier"] > 0,
                ("mode unexpectedly closed", mode, summary))
        mode_summaries[mode] = summary
        for field in fields:
            totals[field] += summary[field]
    require(totals == EXPECTED_TOTALS, ("total mismatch", totals, EXPECTED_TOTALS))
    require(witnesses == 0, witnesses)

    return {
        "claim": "order-25 three-branch width-25 window is insufficient",
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "archive_sha256": archive_digest,
        "shards": len(output_paths),
        "modes": mode_summaries,
        "totals": totals,
        "witnesses_checked_by_a_and_b": witnesses,
        "status": "VERIFIED_DIAGNOSTIC_NOT_UNSAT",
    }


def main() -> None:
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
