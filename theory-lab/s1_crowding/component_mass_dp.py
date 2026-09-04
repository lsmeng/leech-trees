#!/usr/bin/env python3
"""Sound component-mass / low-LCA necessary-condition prefilter.

This module deliberately does not enumerate high labels or depths.  For a
fixed rooted low tree, it enumerates every distribution of the m high
vertices into components attached directly to low vertices (each local
component is represented only by its positive integer mass).  It rejects a
mass pattern only when the high-high LCA capacity inequalities fail:

    W = sum_{v,j} C(n[v,j], 2) <= 2*m-3
    P_v = C(M_v,2) - sum_{u child of v} C(M_u,2) - W_v <= 2*m-3

where M_v is high mass in the low subtree rooted at v and W_v is the local
contribution to W.  These are necessary conditions, never sufficient ones.
No existing search result is read or overwritten; the JSON output is a
standalone planning/census artifact.
"""
from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Iterator, Optional, Sequence, Tuple, List

Partition = Tuple[int, ...]


def integer_partitions(n: int, largest: Optional[int] = None) -> Iterator[Partition]:
    """Yield every partition of n in non-increasing order, including ()."""
    if n == 0:
        yield ()
        return
    if n < 0:
        return
    if largest is None or largest > n:
        largest = n
    for first in range(largest, 0, -1):
        for rest in integer_partitions(n - first, first):
            yield (first,) + rest


def local_partition_tuples(m: int, r: int) -> Iterator[Tuple[Partition, ...]]:
    """Yield all r-tuples of local partitions with total mass m."""
    parts = tuple(tuple(integer_partitions(n)) for n in range(m + 1))

    def rec(v: int, remaining: int, out: List[Partition]) -> Iterator[Tuple[Partition, ...]]:
        if v == r - 1:
            for p in parts[remaining]:
                yield tuple(out + [p])
            return
        for mass in range(remaining + 1):
            for p in parts[mass]:
                out.append(p)
                yield from rec(v + 1, remaining - mass, out)
                out.pop()

    yield from rec(0, m, [])


def validate_lowpar(lowpar: Sequence[int]) -> None:
    if not lowpar or lowpar[0] != -1:
        raise ValueError("lowpar must start with -1 for the root")
    for i, p in enumerate(lowpar[1:], 1):
        if not (0 <= p < i):
            raise ValueError(f"lowpar[{i}]={p} is not a rooted depth-order parent")


def capacity_record(lowpar: Sequence[int], masses: Tuple[Partition, ...], m: int) -> dict:
    r = len(lowpar)
    children = [[] for _ in range(r)]
    for v in range(1, r):
        children[lowpar[v]].append(v)
    local_w = [sum(comb(n, 2) for n in masses[v]) for v in range(r)]
    subtree_mass = [sum(masses[v]) for v in range(r)]
    for v in range(r - 1, -1, -1):
        for u in children[v]:
            subtree_mass[v] += subtree_mass[u]
    p_values = []
    for v in range(r):
        p = comb(subtree_mass[v], 2)
        p -= sum(comb(subtree_mass[u], 2) for u in children[v])
        p -= local_w[v]
        p_values.append(p)
    cap = 2 * m - 3
    return {
        "m": m,
        "r": r,
        "capacity": cap,
        "masses": [list(p) for p in masses],
        "subtree_mass": subtree_mass,
        "W": sum(local_w),
        "P": p_values,
        "necessary_pass": sum(local_w) <= cap and all(p <= cap for p in p_values),
    }


def census(lowpar: Sequence[int], m: int, emit: Optional[Path] = None) -> dict:
    validate_lowpar(lowpar)
    if m < 1:
        raise ValueError("m must be positive")
    total = passed = 0
    max_w = max_p = 0
    out = emit.open("w", encoding="utf-8") if emit else None
    try:
        for masses in local_partition_tuples(m, len(lowpar)):
            rec = capacity_record(lowpar, masses, m)
            total += 1
            max_w = max(max_w, rec["W"])
            max_p = max(max_p, max(rec["P"]))
            if rec["necessary_pass"]:
                passed += 1
                if out:
                    out.write(json.dumps(rec, sort_keys=True) + "\n")
    finally:
        if out:
            out.close()
    return {
        "status": "COMPONENT_MASS_DP_CENSUS",
        "lowpar": list(lowpar),
        "m": m,
        "total_mass_patterns": total,
        "necessary_pass_patterns": passed,
        "max_W_seen": max_w,
        "max_P_seen": max_p,
        "emitted_jsonl": str(emit) if emit else None,
    }


def parse_lowpar(text: str) -> list[int]:
    return [int(x) for x in text.split(",") if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--lowpar", required=True, help="comma-separated, starting -1")
    ap.add_argument("--emit", type=Path, default=None, help="optional JSONL of passing patterns")
    args = ap.parse_args()
    print(json.dumps(census(parse_lowpar(args.lowpar), args.m, args.emit), sort_keys=True))


if __name__ == "__main__":
    main()
