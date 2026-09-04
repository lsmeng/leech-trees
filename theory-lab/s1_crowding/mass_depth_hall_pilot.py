#!/usr/bin/env python3
"""Independent small pilot for mass -> low-depth Hall presolve.

The script is intentionally a toy-scale checker.  It enumerates local
component partitions, derives the necessary P_v counts, applies the relaxed
suffix-interval Hall test, and brute-forces the same basic low-depth
constraints.  A Hall rejection must never coexist with a brute-force depth
assignment.  This validates soundness of the presolve only; it is not a full
Leech-tree solver.
"""
from __future__ import annotations

import argparse
import itertools
import json
from math import ceil, comb
from typing import Iterator, List, Optional, Sequence, Tuple

Partition = Tuple[int, ...]


def integer_partitions(n: int, largest: Optional[int] = None) -> Iterator[Partition]:
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


def local_tuples(m: int, r: int) -> Iterator[Tuple[Partition, ...]]:
    parts = tuple(tuple(integer_partitions(a)) for a in range(m + 1))

    def rec(v: int, remaining: int, out: List[Partition]) -> Iterator[Tuple[Partition, ...]]:
        if v == r - 1:
            for p in parts[remaining]:
                yield tuple(out + [p])
            return
        for a in range(remaining + 1):
            for p in parts[a]:
                out.append(p)
                yield from rec(v + 1, remaining - a, out)
                out.pop()

    yield from rec(0, m, [])


def p_vector(lowpar: Sequence[int], masses: Tuple[Partition, ...], m: int) -> Tuple[int, ...]:
    r = len(lowpar)
    children = [[] for _ in range(r)]
    for v in range(1, r):
        children[lowpar[v]].append(v)
    subtree = [sum(masses[v]) for v in range(r)]
    local_w = [sum(comb(n, 2) for n in masses[v]) for v in range(r)]
    for v in range(r - 1, -1, -1):
        for u in children[v]:
            subtree[v] += subtree[u]
    out = []
    for v in range(r):
        p = comb(subtree[v], 2)
        p -= sum(comb(subtree[u], 2) for u in children[v])
        p -= local_w[v]
        out.append(p)
    return tuple(out)


def propagated_bounds(lowpar: Sequence[int], pvals: Sequence[int], delta: int, s: int) -> Tuple[int, ...]:
    b = delta + 1 - s
    lb = [max(1, ceil((delta + 2 - 2 * s + p) / 2)) for p in pvals]
    lb[0] = 0
    e = [0] * len(lowpar)
    for v in range(1, len(lowpar)):
        e[v] = max(lb[v], e[lowpar[v]] + 1)
    return tuple(e)


def suffix_hall(lowpar: Sequence[int], pvals: Sequence[int], delta: int, s: int) -> bool:
    b = delta + 1 - s
    e = propagated_bounds(lowpar, pvals, delta, s)
    if e[0] != 0 or b - 1 < 0:
        return False
    values = sorted(e[1:])
    used = 0
    for x in values:
        used = max(used + 1, x)
        if used > b - 1:
            return False
    return True


def brute_depth_exists(lowpar: Sequence[int], pvals: Sequence[int], delta: int, s: int) -> bool:
    b = delta + 1 - s
    if b <= 1:
        return False
    root_cap = 2 * s - delta - 2
    if pvals[0] > root_cap:
        return False
    slots = range(1, b)
    for choice in itertools.permutations(slots, len(lowpar) - 1):
        depths = (0,) + choice
        if len(set(depths)) != len(depths):
            continue
        ok = True
        for v in range(1, len(lowpar)):
            lb = max(1, ceil((delta + 2 - 2 * s + pvals[v]) / 2))
            if depths[v] < lb or depths[v] <= depths[lowpar[v]]:
                ok = False
                break
        if ok:
            return True
    return False


def run(lowpar: Sequence[int], m: int, delta: int, s_min: int, s_max: int) -> dict:
    total = hall_reject = false_reject = exact_possible = 0
    for masses in local_tuples(m, len(lowpar)):
        pvals = p_vector(lowpar, masses, m)
        for s in range(s_min, s_max + 1):
            total += 1
            hall_ok = suffix_hall(lowpar, pvals, delta, s)
            exact_ok = brute_depth_exists(lowpar, pvals, delta, s)
            if exact_ok:
                exact_possible += 1
            if not hall_ok:
                hall_reject += 1
                if exact_ok:
                    false_reject += 1
    return {
        "status": "MASS_DEPTH_HALL_PILOT",
        "lowpar": list(lowpar),
        "m": m,
        "delta": delta,
        "s_range": [s_min, s_max],
        "mass_s_pairs": total,
        "hall_reject": hall_reject,
        "exact_depth_possible": exact_possible,
        "false_rejects": false_reject,
        "soundness_ok": false_reject == 0,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--lowpar", required=True)
    ap.add_argument("--s-min", type=int, required=True)
    ap.add_argument("--s-max", type=int, required=True)
    args = ap.parse_args()
    lowpar = [int(x) for x in args.lowpar.split(",") if x.strip()]
    print(json.dumps(run(lowpar, args.m, args.delta, args.s_min, args.s_max), sort_keys=True))


if __name__ == "__main__":
    main()
