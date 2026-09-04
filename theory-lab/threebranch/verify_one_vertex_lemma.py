#!/usr/bin/env python3
"""Audit the anchored one-vertex completion lemma and its C prune."""
from __future__ import annotations

import json
import random
import subprocess
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "threebranch_exact.c"
BINARY = HERE / "threebranch_exact"
CERTIFICATE = HERE / "results" / "threebranch_exact_certificate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def build() -> None:
    process = subprocess.run(
        ["cc", "-O3", "-std=c11", "-Wall", "-Wextra", "-pedantic",
         "-o", str(BINARY), str(SOURCE)],
        capture_output=True, text=True, check=False,
    )
    require(process.returncode == 0, f"build failed:\n{process.stdout}\n{process.stderr}")


def tree_distances(n: int, edges):
    adjacency = [[] for _ in range(n)]
    for u, v, weight in edges:
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))
    distances = [[0] * n for _ in range(n)]
    for source in range(n):
        stack = [(source, -1, 0)]
        while stack:
            vertex, parent, value = stack.pop()
            distances[source][vertex] = value
            for neighbour, weight in adjacency[vertex]:
                if neighbour != parent:
                    stack.append((neighbour, vertex, value + weight))
    return distances


def audit_tree_metrics() -> int:
    rng = random.Random(20260821)
    checked = 0
    for n in range(4, 13):
        for _ in range(120):
            edges = [(vertex, rng.randrange(vertex), rng.randrange(1, 31))
                     for vertex in range(1, n)]
            distances = tree_distances(n, edges)
            diameter = max((distances[u][v], u, v)
                           for u in range(n) for v in range(u + 1, n))
            maximum, a, b = diameter
            for x, y in combinations((vertex for vertex in range(n)
                                      if vertex not in (a, b)), 2):
                value = distances[x][y]
                sums = sorted((
                    maximum + value,
                    distances[a][x] + distances[b][y],
                    distances[a][y] + distances[b][x],
                ))
                require(sums[1] == sums[2],
                        f"four-point failure n={n} edges={edges} quartet={(a,b,x,y)}")
                cross = max(distances[a][x], distances[a][y],
                            distances[b][x], distances[b][y])
                require(cross > value,
                        f"strict-cross failure N={maximum} v={value} quartet={(a,b,x,y)}")
                checked += 1
    require(checked > 10000, f"too few metric checks: {checked}")
    return checked


def run_engine(order: int, *extra: str):
    process = subprocess.run([str(BINARY), str(order), "all", *extra],
                             capture_output=True, text=True, check=False)
    require(process.returncode == 0,
            f"engine failed n={order} {extra}:\n{process.stdout}\n{process.stderr}")
    summaries = [json.loads(line) for line in process.stdout.splitlines()
                 if line.startswith("{")]
    require(len(summaries) == 1, f"unexpected output n={order}: {process.stdout}")
    return summaries[0]


def audit_prune() -> dict:
    frozen = json.loads(CERTIFICATE.read_text())["exact_runs"]
    rows = {}
    for order in range(8, 16):
        summary = run_engine(order, "--no-pairs")
        expected = frozen[str(order)]
        require(summary["status"] == "DONE", f"unfinished lemma run n={order}")
        require(summary["pair_mode"] == "one-vertex-lemma", f"wrong mode n={order}")
        for field in ("anchors", "nodes", "legal_children"):
            require(summary[field] == expected[field],
                    f"pair-prune mismatch n={order} {field}: "
                    f"{summary[field]} != {expected[field]}")
        require(summary["nsol"] == expected["solutions"] == 0,
                f"solution mismatch n={order}")
        require(summary["legal_pair_children"] == expected["legal_pair_children"] == 0,
                f"pair-child mismatch n={order}")
        rows[order] = {
            "anchors": summary["anchors"],
            "nodes": summary["nodes"],
            "solutions": summary["nsol"],
        }

    process = subprocess.run([str(BINARY), "--pair-probe"], capture_output=True,
                             text=True, check=False)
    require(process.returncode == 0, f"pair probe failed: {process.stderr}")
    probe = json.loads(process.stdout)
    require(probe["legal_pair_children"] == 3 and probe["status"] == "PASS",
            f"pair probe changed: {probe}")
    return rows


def main() -> None:
    build()
    metric_checks = audit_tree_metrics()
    rows = audit_prune()
    print(f"PASS four-point/strict-cross audit: {metric_checks} weighted quartets")
    print("PASS lemma-pruned C invariants equal conservative runs n=8..15:", rows)
    print("PASS non-anchored two-new positive probe: 3 children")
    print("PASS anchored one-vertex completion lemma audit")


if __name__ == "__main__":
    main()
