#!/usr/bin/env python3
"""Independent high-high translated-sumset filter for STRUCT records.

This is a necessary filter only.  It reconstructs the high forest from the
low-tree parent list and a STRUCT hpar record, then searches (s,L) for which
the exact high-high sets H and 2B-2*l_v+S_v are mutually disjoint and inside
[1, delta].  LL/LH/holes are deliberately omitted in this pilot.
"""

from __future__ import annotations

import argparse
import json
import re
from functools import lru_cache


def parse_ints(text: str) -> list[int]:
    return [int(x) for x in text.split(",") if x != ""]


def low_lca(lowpar: list[int], a: int, b: int) -> int:
    anc = set()
    while a >= 0:
        anc.add(a)
        a = lowpar[a]
    while b not in anc:
        b = lowpar[b]
    return b


def reconstruct(lowpar_tail: list[int], hpar: list[int]):
    lowpar = [-1] + list(lowpar_tail)
    r = len(lowpar)
    m = len(hpar)
    hroot: list[int] = [-1] * m
    parent: list[int | None] = [None] * m
    for y, hp in enumerate(hpar):
        if hp < 0:
            root = -hp - 1
            if not (0 <= root < r):
                raise ValueError(f"bad low root {root} at high vertex {y}")
            hroot[y] = root
        else:
            if not (0 <= hp < y):
                raise ValueError(f"high parent must be earlier: y={y} hp={hp}")
            parent[y] = hp
            hroot[y] = hroot[hp]

    def high_lca(a: int, b: int) -> int:
        seen = set()
        while a is not None:
            seen.add(a)
            a = parent[a] if parent[a] is not None else None
        while b not in seen:
            if parent[b] is None:
                raise ValueError("different high components passed to high_lca")
            b = parent[b]
        return b

    hcomp = []
    for y in range(m):
        q = y
        while parent[q] is not None:
            q = parent[q]
        hcomp.append(q)

    H: list[int] = []
    S = [[] for _ in range(r)]
    for y in range(m):
        for yy in range(y):
            if hcomp[y] == hcomp[yy]:
                q = high_lca(y, yy)
                H.append(y + yy - 2 * q)
            else:
                a = low_lca(lowpar, hroot[y], hroot[yy])
                S[a].append(y + yy)
    return lowpar, hroot, H, S


def run(lowpar_tail: list[int], hpar: list[int], delta: int, node_limit: int):
    lowpar, hroot, H, S = reconstruct(lowpar_tail, hpar)
    if len(set(H)) != len(H):
        return {"status": "UPSTREAM_H_COLLISION", "H_size": len(H)}
    if any(v < 1 or v > delta for v in H):
        return {"status": "H_OUT_OF_RANGE", "H_size": len(H)}
    hset = set(H)
    # In the Leech-tree parameterization, B=delta+1-s and B>=r leaves room
    # for r distinct low depths in [0,B).
    s_max = delta + 1 - len(lowpar)
    nodes = 0
    complete = True
    witnesses = []
    pass_count = 0
    tested_s = 0

    for s in range(1, s_max + 1):
        B = delta + 1 - s
        tested_s += 1
        # Root class is fixed at l_0=0.
        root_t = {2 * B + z for z in S[0]}
        if any(z < 1 or z > delta for z in root_t) or root_t & hset:
            continue
        if len(root_t) != len(S[0]):
            continue
        used = hset | root_t
        L = [0] + [None] * (len(lowpar) - 1)

        def dfs(i: int, used_now: set[int]):
            nonlocal nodes, complete, pass_count
            nodes += 1
            if nodes > node_limit:
                complete = False
                return
            if i == len(lowpar):
                pass_count += 1
                if len(witnesses) < 3:
                    witnesses.append({"s": s, "L": list(L)})
                return
            lo = L[lowpar[i]] + 1
            for l in range(lo, B):
                if l in L[:i]:
                    continue
                vals = {2 * B - 2 * l + z for z in S[i]}
                if len(vals) != len(S[i]):
                    continue
                if any(z < 1 or z > delta for z in vals):
                    continue
                if vals & used_now:
                    continue
                L[i] = l
                dfs(i + 1, used_now | vals)
                L[i] = None
                if nodes > node_limit:
                    return

        dfs(1, used)
        if nodes > node_limit:
            break
    return {
        "status": "COMPLETE" if complete else "NODE_LIMIT",
        "m": len(hpar),
        "r": len(lowpar),
        "delta": delta,
        "H_size": len(H),
        "S_sizes": [len(x) for x in S],
        "tested_s": tested_s,
        "nodes": nodes,
        "high_high_passes": pass_count,
        "witnesses": witnesses,
        "hroot": hroot,
        "H": sorted(H),
        "S": [sorted(x) for x in S],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lowpar", required=True, help="comma-separated lowpar[1..r-1]")
    ap.add_argument("--struct", required=True, help="STRUCT line or hpar integer list")
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--node-limit", type=int, default=2_000_000)
    args = ap.parse_args()
    m = re.search(r"\bhpar=((?:-?\d+,)*-?\d+)", args.struct)
    if m:
        hpar = parse_ints(m.group(1))
    elif args.struct.lstrip().startswith("STRUCT"):
        # Current C++ --emit format is: STRUCT <hpar[0]> ... <hpar[M-1]>.
        hpar = [int(x) for x in args.struct.split()[1:]]
    else:
        hpar = parse_ints(args.struct)
    out = run(parse_ints(args.lowpar), hpar, args.delta, args.node_limit)
    print(json.dumps(out, sort_keys=True))
    return 0 if out["status"] in {"COMPLETE", "NODE_LIMIT"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
