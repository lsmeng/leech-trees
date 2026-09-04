#!/usr/bin/env python3
"""Audit the fixed-order calibration of the UNVERIFIED parametric probe."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "results" / "threebranch_parametric_n10_certificate.json"
PROBE = HERE / "threebranch_parametric_probe.py"
EXACT_SOURCE = HERE / "threebranch_exact.c"
sys.path.insert(0, str(ROOT / "src"))

import checker_a  # noqa: E402
import checker_b  # noqa: E402


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_witness(line: str) -> None:
    fields = dict(piece.split("=", 1) for piece in line.split()[1:])
    order = int(fields["n"])
    edges = [
        tuple(map(int, item.split(",")))
        for item in fields["edges"].rstrip(";").split(";")
    ]
    ok_a, reason_a = checker_a.is_leech(order, edges)
    ok_b, reason_b = checker_b.is_leech(order, edges)
    require(ok_a, ("checker_a rejected witness", reason_a, edges))
    require(ok_b, ("checker_b rejected witness", reason_b, edges))


def run_exact(binary: Path, mode: str, window: int) -> dict[str, object]:
    process = subprocess.run(
        [str(binary), "10", mode, "--no-pairs", "--diameter-intro",
         "--window", str(window)],
        capture_output=True, text=True, check=False,
    )
    require(process.returncode == 0, (mode, process.stdout, process.stderr))
    rows = []
    witness_count = 0
    for line in process.stdout.splitlines():
        if line.startswith("WITNESS "):
            verify_witness(line)
            witness_count += 1
        elif line.startswith("{"):
            rows.append(json.loads(line))
    require(len(rows) == 1, (mode, rows))
    require(rows[0]["nsol"] == witness_count, (mode, rows[0], witness_count))
    return rows[0]


def main() -> None:
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    certificate = json.loads(CERTIFICATE.read_text())
    require(certificate["claim_status"].startswith("OBSERVED calibration"),
            certificate)
    require(sha256(PROBE) == certificate["probe_sha256"], "probe hash mismatch")
    require(sha256(EXACT_SOURCE) == certificate["exact_source_sha256"],
            "exact source hash mismatch")

    expected_modes = certificate["modes"]
    require(set(expected_modes) == {"AA", "BB", "AB", "AC"}, expected_modes)
    with tempfile.TemporaryDirectory(prefix="leech-parametric-n10-") as temporary:
        binary = Path(temporary) / "threebranch_exact"
        build = subprocess.run(
            ["cc", "-O3", "-std=c11", "-Wall", "-Wextra", "-pedantic",
             "-o", str(binary), str(EXACT_SOURCE)],
            capture_output=True, text=True, check=False,
        )
        require(build.returncode == 0, (build.stdout, build.stderr))
        for mode, probe_row in expected_modes.items():
            require(probe_row["mode"] == mode, probe_row)
            require(probe_row["fixed_n"] == 10 and probe_row["nmin"] == 1,
                    probe_row)
            require(probe_row["status"] == "CLOSED", probe_row)
            require(not probe_row["capped"] and probe_row["solver_unknown"] == 0,
                    probe_row)
            require(probe_row["frontier_states"] == 0, probe_row)
            require(not probe_row["triangular_tail"]
                    and not probe_row["taylor_tail"]
                    and probe_row["taylor_residue_modulus"] == 0,
                    probe_row)
            exact = run_exact(binary, mode, int(probe_row["requested_window"]))
            require(exact["status"] == "DONE" and exact["frontier"] == 0,
                    (mode, exact))
            require(exact["nsol"] == 0, (mode, exact))
            require(exact["deepest_missing_offset"]
                    == probe_row["completed_offset"], (mode, exact, probe_row))
            require(exact["max_noncentre_marks"]
                    == probe_row["maximum_marks"], (mode, exact, probe_row))

    print(json.dumps({
        "status": "VERIFIED",
        "claim": "fixed-order n=10 parametric/exact closure calibration",
        "modes": sorted(expected_modes),
        "witness_policy": "every reported witness passes checker_a and checker_b",
        "trust_boundary": (
            "The parametric rows are frozen outputs, not recomputed here. "
            "Agreement at n=10 calibrates the implementation but does not "
            "certify a CLOSED all-order cell or an all-order theorem."
        ),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
