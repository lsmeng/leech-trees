#!/usr/bin/env python3
"""Verify the exact order-27 three-branch-vertex shard archive."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from audit_threebranch_archive import audit_archive, require


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "threebranch_exact.c"
RUNNER = HERE / "run_threebranch_window_shards.py"
SHARED_AUDIT = HERE / "audit_threebranch_archive.py"
ARCHIVE = HERE / "results" / "threebranch_n27_w70_outputs.tar.gz"
RESULT = HERE / "results" / "threebranch_n27_w70_certificate.json"

ORDER = 27
WINDOW = 70
SHARDS = 128
EXPECTED_SOURCE_SHA256 = (
    "2e796bf278634c302ffb9fe3510004379a2887b3d5af0e52f7edcfb5764172ac"
)
EXPECTED_RUNNER_SHA256 = (
    "7f1ae1b5aef569008052b25f2dd598ac69547c3f487b304ab56bfb2bfff5c9f0"
)
EXPECTED_SHARED_AUDIT_SHA256 = (
    "1df189791209daffc554d6fced7bed0a1197be52b202f865c4fd48032d98b378"
)
EXPECTED_ARCHIVE_SHA256 = (
    "d351b0d564b1ed42878010d703a32b72996c9c97daaf72e232aa8d46f8362faa"
)
EXPECTED = {
    "AA": {
        "anchors_generated": 862_924,
        "anchors": 842_172,
        "nodes": 1_794_114_175,
        "candidate_marks": 15_795_485_677,
        "candidate_pairs": 0,
        "legal_children": 1_793_272_003,
        "legal_single_children": 1_793_272_003,
        "legal_pair_children": 0,
        "frontier": 0,
        "nsol": 0,
        "deepest_missing_offset": 45,
        "max_noncentre_marks": 14,
    },
    "BB": {
        "anchors_generated": 862_924,
        "anchors": 839_861,
        "nodes": 674_240_372,
        "candidate_marks": 5_388_117_120,
        "candidate_pairs": 0,
        "legal_children": 673_400_511,
        "legal_single_children": 673_400_511,
        "legal_pair_children": 0,
        "frontier": 0,
        "nsol": 0,
        "deepest_missing_offset": 36,
        "max_noncentre_marks": 12,
    },
    "AB": {
        "anchors_generated": 5_222_697,
        "anchors": 5_024_858,
        "nodes": 13_138_936_602,
        "candidate_marks": 109_765_064_990,
        "candidate_pairs": 0,
        "legal_children": 13_133_911_744,
        "legal_single_children": 13_133_911_744,
        "legal_pair_children": 0,
        "frontier": 0,
        "nsol": 0,
        "deepest_missing_offset": 52,
        "max_noncentre_marks": 15,
    },
    "AC": {
        "anchors_generated": 3_466_747,
        "anchors": 3_348_323,
        "nodes": 17_818_494_417,
        "candidate_marks": 152_657_684_443,
        "candidate_pairs": 0,
        "legal_children": 17_815_146_094,
        "legal_single_children": 17_815_146_094,
        "legal_pair_children": 0,
        "frontier": 0,
        "nsol": 0,
        "deepest_missing_offset": 51,
        "max_noncentre_marks": 15,
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit() -> dict[str, object]:
    require(sha256(SOURCE) == EXPECTED_SOURCE_SHA256, "source hash mismatch")
    require(sha256(RUNNER) == EXPECTED_RUNNER_SHA256, "runner hash mismatch")
    require(sha256(SHARED_AUDIT) == EXPECTED_SHARED_AUDIT_SHA256,
            "shared audit hash mismatch")
    require(sha256(ARCHIVE) == EXPECTED_ARCHIVE_SHA256, "archive hash mismatch")
    replay = audit_archive(
        ARCHIVE,
        order=ORDER,
        window=WINDOW,
        shards=SHARDS,
    )
    require(replay["modes"] == EXPECTED,
            ("mode aggregate mismatch", replay["modes"]))
    totals = replay["totals"]
    require(totals["nodes"] == 33_425_785_566, totals)
    require(totals["frontier"] == totals["nsol"] == 0, totals)

    output = {
        "claim": "no order-27 Leech tree has exactly three branch vertices",
        "order": ORDER,
        "window": WINDOW,
        "shards_per_mode": SHARDS,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "runner_sha256": EXPECTED_RUNNER_SHA256,
        "shared_audit_sha256": EXPECTED_SHARED_AUDIT_SHA256,
        "archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "verifier_sha256": sha256(Path(__file__)),
        "modes": replay["modes"],
        "totals": totals,
        "witnesses_checked_by_a_and_b": replay[
            "witnesses_checked_by_a_and_b"
        ],
        "status": "VERIFIED",
        "trust_boundary": (
            "Exact finite order-27 exclusion for the proved exactly-three-branch "
            "normal form, using the previously audited diameter-endpoint and "
            "one-new-vertex theorems. All 512 paranoid shards are DONE with zero "
            "frontier and zero solutions. This does not exclude order-27 trees "
            "with four or more branch vertices and is not an all-order theorem."
        ),
    }
    if RESULT.exists():
        require(output == json.loads(RESULT.read_text()), RESULT)
    return output


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
