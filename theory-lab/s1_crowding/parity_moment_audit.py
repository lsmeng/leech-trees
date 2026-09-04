#!/usr/bin/env python3
"""Independent parity and first-Wiener-moment audit for one (s,L) candidate.

This is a read-only presolver/audit, not a Leech-tree solver.  The rooted low
vertex 0 is the bridge endpoint x; the singleton cap leaf is an extra vertex
of depth s.  Given lowpar, STRUCT hpar, and low depths L, it builds the full
weighted tree, checks the parity count, and compares the cut identity with a
direct all-pairs distance sum.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from math import comb


def ints(text: str) -> list[int]:
    return [int(x) for x in text.split(",") if x != ""]


def parse_struct(text: str) -> list[int]:
    if text.lstrip().startswith("STRUCT"):
        return [int(x) for x in text.split()[1:]]
    return ints(text)


def low_lca(lowpar: list[int], a: int, b: int) -> int:
    ancestors = set()
    while a >= 0:
        ancestors.add(a)
        a = lowpar[a]
    while b not in ancestors:
        b = lowpar[b]
    return b


def build_candidate(lowpar_tail: list[int], hpar: list[int], delta: int, s: int, depths: list[int]):
    lowpar = [-1] + lowpar_tail
    r, m = len(lowpar), len(hpar)
    if len(depths) != r or depths[0] != 0:
        raise ValueError("depth vector must have length r and start at 0")
    B = delta + 1 - s
    n = r + m + 1
    cap = n - 1
    parent: list[int | None] = [None] * n
    weight: list[int] = [0] * n
    vertex_depth = list(depths) + [B + y for y in range(m)] + [s]

    for i in range(1, r):
        p = lowpar[i]
        if not (0 <= p < i):
            raise ValueError(f"low parent must be earlier: i={i}, p={p}")
        parent[i] = p
        weight[i] = depths[i] - depths[p]
    for y, hp in enumerate(hpar):
        v = r + y
        if hp < 0:
            p = -hp - 1
            if not (0 <= p < r):
                raise ValueError(f"bad high root: y={y}, p={p}")
            parent[v] = p
            weight[v] = B + y - depths[p]
        else:
            if not (0 <= hp < y):
                raise ValueError(f"high parent must be earlier: y={y}, hp={hp}")
            parent[v] = r + hp
            weight[v] = y - hp
    parent[cap] = 0
    weight[cap] = s
    if any(weight[v] <= 0 for v in range(1, n)):
        raise ValueError("non-positive edge weight")

    children = [[] for _ in range(n)]
    for v in range(1, n):
        assert parent[v] is not None
        children[parent[v]].append(v)
    subtree = [1] * n
    for v in range(n - 1, 0, -1):
        assert parent[v] is not None
        subtree[parent[v]] += subtree[v]

    adjacency = [[] for _ in range(n)]
    cut_sum = 0
    for v in range(1, n):
        p = parent[v]
        assert p is not None
        w = weight[v]
        adjacency[v].append((p, w))
        adjacency[p].append((v, w))
        cut_sum += subtree[v] * (n - subtree[v]) * w
    return n, vertex_depth, adjacency, cut_sum


def all_pair_sum(adjacency: list[list[tuple[int, int]]]) -> tuple[int, int, int]:
    n = len(adjacency)
    total = 0
    distinct = set()
    for src in range(n):
        distance = [None] * n
        distance[src] = 0
        queue = deque([src])
        while queue:
            v = queue.popleft()
            for u, w in adjacency[v]:
                if distance[u] is None:
                    distance[u] = distance[v] + w
                    queue.append(u)
        for dst in range(src + 1, n):
            d = distance[dst]
            assert d is not None
            total += d
            distinct.add(d)
    return total, len(distinct), n * (n - 1) // 2


def audit(lowpar_tail: list[int], hpar: list[int], delta: int, s: int, depths: list[int]) -> dict:
    n, vertex_depth, adjacency, cut_sum = build_candidate(lowpar_tail, hpar, delta, s, depths)
    pair_sum, distinct_count, pair_count = all_pair_sum(adjacency)
    target_sum = pair_count * (pair_count + 1) // 2
    odd_vertices = sum(d % 2 for d in vertex_depth)
    target_odd_pairs = (pair_count + 1) // 2
    odd_pairs = odd_vertices * (n - odd_vertices)
    return {
        "status": "PARITY_MOMENT_AUDIT",
        "n": n,
        "delta": delta,
        "s": s,
        "depths": depths,
        "odd_vertices": odd_vertices,
        "odd_pairs": odd_pairs,
        "target_odd_pairs": target_odd_pairs,
        "parity_ok": odd_pairs == target_odd_pairs,
        "pair_count": pair_count,
        "distinct_distance_count": distinct_count,
        "cut_first_moment": cut_sum,
        "direct_first_moment": pair_sum,
        "target_first_moment": target_sum,
        "cut_identity_ok": cut_sum == pair_sum,
        "moment_target_ok": pair_sum == target_sum,
        "all_checks_ok": odd_pairs == target_odd_pairs and cut_sum == pair_sum and pair_sum == target_sum,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lowpar", required=True, help="comma-separated lowpar[1..r-1]")
    ap.add_argument("--struct", required=True, help="STRUCT line or comma-separated hpar")
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--depths", required=True, help="comma-separated low depths L[0..r-1]")
    args = ap.parse_args()
    out = audit(ints(args.lowpar), parse_struct(args.struct), args.delta, args.s, ints(args.depths))
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
