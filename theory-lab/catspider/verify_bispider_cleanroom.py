#!/usr/bin/env python3
"""Cross-check the production and clean-room bi-spider searches through n=10."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from dataclasses import asdict
from pathlib import Path

from bispider_cleanroom import solve


HERE = Path(__file__).resolve().parent

# Frozen production counts are also checked against a freshly compiled binary.
EXPECTED = {
    4: {"LR": (1, 1, 1), "LL": (1, 1, 1)},
    5: {"LR": (8, 8, 0), "LL": (5, 5, 0)},
    6: {"LR": (36, 87, 1), "LL": (19, 56, 0)},
    7: {"LR": (81, 387, 0), "LL": (42, 257, 0)},
    8: {"LR": (144, 1257, 0), "LL": (74, 732, 0)},
    9: {"LR": (257, 3894, 0), "LL": (131, 2262, 0)},
    10: {"LR": (441, 11655, 0), "LL": (224, 6444, 0)},
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def compile_production(output: Path) -> None:
    compiler = shutil.which("clang") or shutil.which("cc")
    require(compiler is not None, "no C compiler found")
    subprocess.run(
        [compiler, "-O3", "-o", str(output), str(HERE / "bispider.c")],
        check=True,
        capture_output=True,
        text=True,
    )


def run_production(binary: Path, n: int, mode: str) -> dict:
    completed = subprocess.run(
        [str(binary), str(n), mode],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [line for line in completed.stdout.splitlines() if line.startswith("{")]
    require(len(rows) == 1, (n, mode, completed.stdout, completed.stderr))
    return json.loads(rows[0])


def main() -> None:
    report = []
    with tempfile.TemporaryDirectory(prefix="bispider-verify-") as temp_dir:
        binary = Path(temp_dir) / "bispider"
        compile_production(binary)
        for n, expected_modes in EXPECTED.items():
            for mode, expected in expected_modes.items():
                prod = run_production(binary, n, mode)
                solutions, clean = solve(n, (mode,))
                clean_tuple = (clean.anchors, clean.nodes, len(solutions))
                prod_tuple = (prod["branches"], prod["nodes"], prod["nsol"])
                require(prod_tuple == expected, (n, mode, "production", prod_tuple, expected))
                require(clean_tuple == expected, (n, mode, "cleanroom", clean_tuple, expected))
                report.append(
                    {
                        "n": n,
                        "mode": mode,
                        "anchors": clean.anchors,
                        "nodes": clean.nodes,
                        "solutions": len(solutions),
                        "cleanroom_stats": asdict(clean),
                        "match": True,
                    }
                )
    print(
        json.dumps(
            {
                "orders": [min(EXPECTED), max(EXPECTED)],
                "regimes": len(report),
                "total_nodes_per_implementation": sum(row["nodes"] for row in report),
                "positive_controls": {
                    "n4": "two witnesses PASS checker_a + checker_b",
                    "n6": "one witness PASS checker_a + checker_b",
                },
                "rows": report,
                "status": "VERIFIED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
