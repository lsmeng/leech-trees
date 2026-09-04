#!/usr/bin/env python3
"""Relaxed global distance-slot Hall/flow necessary test.

For fixed mass counts and low depths, each LCA class is assigned a demand
(``W`` for high-LCA pairs and ``P_v`` for low-LCA pairs).  The class-to-slot
edges are deliberately relaxed supersets of the true distance options.  Thus
max-flow failure is sound necessary exclusion; max-flow success says nothing
about existence.  This file is a small, dependency-free pilot, not the full
Leech-tree solver.
"""
from __future__ import annotations

import argparse
import json
from collections import deque
from math import comb
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


class Dinic:
    def __init__(self, n: int) -> None:
        self.g: List[List[List[int]]] = [[] for _ in range(n)]

    def add(self, u: int, v: int, cap: int) -> None:
        self.g[u].append([v, cap, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def flow(self, s: int, t: int) -> int:
        ans = 0
        n = len(self.g)
        while True:
            level = [-1] * n
            level[s] = 0
            q: deque[int] = deque([s])
            while q:
                u = q.popleft()
                for v, cap, _ in self.g[u]:
                    if cap and level[v] < 0:
                        level[v] = level[u] + 1
                        q.append(v)
            if level[t] < 0:
                return ans
            it = [0] * n

            def dfs(u: int, pushed: int) -> int:
                if u == t:
                    return pushed
                while it[u] < len(self.g[u]):
                    e = self.g[u][it[u]]
                    v, cap, rev = e
                    if cap and level[v] == level[u] + 1:
                        got = dfs(v, min(pushed, cap))
                        if got:
                            e[1] -= got
                            self.g[v][rev][1] += got
                            return got
                    it[u] += 1
                return 0

            while True:
                got = dfs(s, 10**9)
                if not got:
                    break
                ans += got


def allowed_slots(m: int, delta: int, s: int, low_depths: Sequence[int], occupied: Iterable[int]) -> Dict[str, Set[int]]:
    b = delta + 1 - s
    cap = 2 * m - 3
    used = set(occupied)
    out: Dict[str, Set[int]] = {"H": set(range(1, cap + 1)) - used}
    for v, lv in enumerate(low_depths):
        vals = {2 * b - 2 * lv + t for t in range(1, cap + 1)}
        out["L%d" % v] = {x for x in vals if 1 <= x <= delta and x not in used}
    return out


def validate_inputs(m: int, delta: int, s: int, low_depths: Sequence[int], W: int, pvals: Sequence[int], occupied: Sequence[int], lowpar: Optional[Sequence[int]]) -> None:
    if not low_depths or low_depths[0] != 0:
        raise ValueError("low_depths must start with root depth 0")
    if len(set(low_depths)) != len(low_depths):
        raise ValueError("low depths must be pairwise distinct")
    b = delta + 1 - s
    if any(l < 0 or l >= b for l in low_depths):
        raise ValueError("low depth outside [0,B)")
    if W < 0 or any(p < 0 for p in pvals):
        raise ValueError("class demands must be nonnegative")
    if W + sum(pvals) != comb(m, 2):
        raise ValueError("W + sum(P) must equal C(m,2)")
    if len(set(occupied)) != len(occupied):
        raise ValueError("duplicate occupied slots indicate an upstream owner collision")
    if any(x < 1 or x > delta for x in occupied):
        raise ValueError("occupied slot outside [1,delta]")
    if lowpar is not None:
        if len(lowpar) != len(low_depths) or (lowpar and lowpar[0] != -1):
            raise ValueError("lowpar must align with low_depths and start with -1")
        for v in range(1, len(lowpar)):
            if not (0 <= lowpar[v] < v):
                raise ValueError("lowpar is not depth-order indexed")
            if low_depths[v] <= low_depths[lowpar[v]]:
                raise ValueError("child low depth must exceed parent depth")


def relaxed_flow(m: int, delta: int, s: int, low_depths: Sequence[int], W: int, pvals: Sequence[int], occupied: Iterable[int] = (), lowpar: Optional[Sequence[int]] = None) -> dict:
    if len(low_depths) != len(pvals):
        raise ValueError("low_depths and pvals must have same length")
    occupied_list = list(occupied)
    validate_inputs(m, delta, s, low_depths, W, pvals, occupied_list, lowpar)
    demands = [("H", W)] + [("L%d" % v, p) for v, p in enumerate(pvals)]
    slots = allowed_slots(m, delta, s, low_depths, occupied_list)
    slot_values = sorted({x for vals in slots.values() for x in vals})
    source = 0
    class0 = 1
    slot0 = class0 + len(demands)
    sink = slot0 + len(slot_values)
    dinic = Dinic(sink + 1)
    slot_id = {x: slot0 + i for i, x in enumerate(slot_values)}
    demand = 0
    for i, (name, d) in enumerate(demands):
        if d < 0:
            raise ValueError("negative class demand")
        demand += d
        node = class0 + i
        dinic.add(source, node, d)
        for x in sorted(slots[name]):
            dinic.add(node, slot_id[x], 1)
    for x in slot_values:
        dinic.add(slot_id[x], sink, 1)
    value = dinic.flow(source, sink)
    return {
        "status": "GLOBAL_DISTANCE_SLOT_FLOW",
        "m": m,
        "delta": delta,
        "s": s,
        "low_depths": list(low_depths),
        "W": W,
        "P": list(pvals),
        "demand": demand,
        "max_flow": value,
        "necessary_pass": value == demand,
        "slot_count": len(slot_values),
        "occupied": sorted(occupied_list),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--depths", required=True, help="comma-separated low depths, root first")
    ap.add_argument("--W", type=int, required=True)
    ap.add_argument("--P", required=True, help="comma-separated P_v, root first")
    ap.add_argument("--occupied", default="", help="optional comma-separated occupied distance slots")
    ap.add_argument("--lowpar", default=None, help="optional comma-separated low parents, starting -1")
    args = ap.parse_args()
    depths = [int(x) for x in args.depths.split(",") if x.strip()]
    pvals = [int(x) for x in args.P.split(",") if x.strip()]
    occupied = [int(x) for x in args.occupied.split(",") if x.strip()]
    lowpar = None if args.lowpar is None else [int(x) for x in args.lowpar.split(",") if x.strip()]
    print(json.dumps(relaxed_flow(args.m, args.delta, args.s, depths, args.W, pvals, occupied, lowpar), sort_keys=True))


if __name__ == "__main__":
    main()
