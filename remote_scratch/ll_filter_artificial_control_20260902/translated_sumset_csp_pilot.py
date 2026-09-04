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
    return lowpar, hroot, H, S, hcomp, parent


def bfs_distance_check(lowpar, hpar, hroot, hcomp, parent, depths, B):
    """Recompute every high-high distance on one weighted unified tree."""
    r, m = len(lowpar), len(hpar)
    global_parent: dict[int, int | None] = {}
    edge_weight: dict[int, int] = {}
    for i in range(r):
        global_parent[i] = None if i == 0 else lowpar[i]
        edge_weight[i] = 0 if i == 0 else depths[i] - depths[lowpar[i]]
    for y, hp in enumerate(hpar):
        gid = r + y
        if hp < 0:
            global_parent[gid] = -hp - 1
            edge_weight[gid] = B + y - depths[hroot[y]]
        else:
            global_parent[gid] = r + hp
            edge_weight[gid] = y - hp

    def pair_distance(a: int, b: int):
        pa = {}
        d = 0
        while a is not None:
            pa[a] = d
            p = global_parent[a]
            if p is None:
                break
            d += edge_weight[a]
            a = p
        d = 0
        while b not in pa:
            p = global_parent[b]
            if p is None:
                raise ValueError("unconnected unified tree")
            d += edge_weight[b]
            b = p
        return pa[b] + d, b

    H = []
    S = [[] for _ in range(r)]
    bad = []
    for y in range(m):
        for yy in range(y):
            d, lca = pair_distance(r + y, r + yy)
            if lca >= r:
                q = lca - r
                expected = y + yy - 2 * q
                H.append(d)
            else:
                v = lca
                expected = 2 * B - 2 * depths[v] + y + yy
                # Normalize the weighted distance back to the raw y+yy sum.
                S[v].append(d - 2 * B + 2 * depths[v])
            if d != expected:
                bad.append({"pair": [yy, y], "distance": d, "expected": expected})
    return {
        "ok": not bad,
        "pair_count": m * (m - 1) // 2,
        "bad": bad[:5],
        "H": sorted(H),
        "S": [sorted(x) for x in S],
    }


def run(
    lowpar_tail: list[int],
    hpar: list[int],
    delta: int,
    node_limit: int,
    include_known_occupied: bool = False,
    include_low_low: bool = False,
):
    lowpar, hroot, H, S, hcomp, parent = reconstruct(lowpar_tail, hpar)
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
    occupied_rejects = 0
    occupied_prune_rejects = 0
    xhigh_out_of_range_rejects = 0
    low_low_prune_rejects = 0

    for s in range(1, s_max + 1):
        B = delta + 1 - s
        tested_s += 1
        if include_known_occupied:
            xhigh = [B + y for y in range(len(hpar))]
            if any(z < 1 or z > delta for z in xhigh):
                xhigh_out_of_range_rejects += 1
                continue
        # Root class is fixed at l_0=0.
        root_t = {2 * B + z for z in S[0]}
        if any(z < 1 or z > delta for z in root_t) or root_t & hset:
            continue
        if len(root_t) != len(S[0]):
            continue
        used = hset | root_t
        if include_known_occupied:
            known_xhigh = {B + y for y in range(len(hpar))}
            # Root's hole is s+l_0=s; all these owners are already fixed.
            known_root_hole = {s} if s <= delta else set()
            known = known_xhigh | known_root_hole
            if len(known) != len(known_xhigh) + len(known_root_hole) or known & used:
                occupied_prune_rejects += 1
                continue
            used |= known
        L = [0] + [None] * (len(lowpar) - 1)

        def dfs(i: int, used_now: set[int]):
            nonlocal nodes, complete, pass_count, occupied_rejects
            nonlocal occupied_prune_rejects, low_low_prune_rejects
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
                next_used = used_now | vals
                if include_low_low:
                    # Every low-low distance involving the newly assigned low
                    # vertex is now determined.  Reject immediately if it is
                    # out of range, collides with an already occupied distance,
                    # or duplicates another newly determined low-low distance.
                    new_ll: set[int] = set()
                    bad_ll = False
                    for j in range(i):
                        if L[j] is None:
                            bad_ll = True
                            break
                        a = low_lca(lowpar, i, j)
                        if L[a] is None:
                            bad_ll = True
                            break
                        d_ll = l + L[j] - 2 * L[a]
                        if (
                            d_ll < 1
                            or d_ll > delta
                            or d_ll in next_used
                            or d_ll in new_ll
                        ):
                            bad_ll = True
                            break
                        new_ll.add(d_ll)
                    if bad_ll:
                        low_low_prune_rejects += 1
                        L[i] = None
                        continue
                    next_used = next_used | new_ll
                if include_known_occupied and s + l <= delta:
                    hole = s + l
                    if hole in next_used:
                        occupied_prune_rejects += 1
                        L[i] = None
                        continue
                    next_used = next_used | {hole}
                dfs(i + 1, next_used)
                L[i] = None
                if nodes > node_limit:
                    return

        dfs(1, used)
        if nodes > node_limit:
            break
    result = {
        "status": "COMPLETE" if complete else "NODE_LIMIT",
        "m": len(hpar),
        "r": len(lowpar),
        "delta": delta,
        "H_size": len(H),
        "S_sizes": [len(x) for x in S],
        "tested_s": tested_s,
        "nodes": nodes,
        "high_high_passes": pass_count,
        "include_known_occupied": include_known_occupied,
        "occupied_rejects": occupied_rejects,
        "occupied_prune_rejects": occupied_prune_rejects,
        "xhigh_out_of_range_rejects": xhigh_out_of_range_rejects,
        "include_low_low": include_low_low,
        "low_low_prune_rejects": low_low_prune_rejects,
        "witnesses": witnesses,
        "hroot": hroot,
        "H": sorted(H),
        "S": [sorted(x) for x in S],
    }
    if witnesses:
        w = witnesses[0]
        result["bfs_check"] = bfs_distance_check(
            lowpar, hpar, hroot, hcomp, parent, w["L"], delta + 1 - w["s"]
        )
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lowpar", required=True, help="comma-separated lowpar[1..r-1]")
    ap.add_argument("--struct", required=True, help="STRUCT line or hpar integer list")
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--node-limit", type=int, default=2_000_000)
    ap.add_argument(
        "--include-known-occupied",
        action="store_true",
        help="also reserve fixed x-high slots and holes s+l_v",
    )
    ap.add_argument(
        "--include-low-low",
        action="store_true",
        help="also reserve exact low-low distances during depth DFS",
    )
    args = ap.parse_args()
    m = re.search(r"\bhpar=((?:-?\d+,)*-?\d+)", args.struct)
    if m:
        hpar = parse_ints(m.group(1))
    elif args.struct.lstrip().startswith("STRUCT"):
        # Current C++ --emit format is: STRUCT <hpar[0]> ... <hpar[M-1]>.
        hpar = [int(x) for x in args.struct.split()[1:]]
    else:
        hpar = parse_ints(args.struct)
    out = run(
        parse_ints(args.lowpar),
        hpar,
        args.delta,
        args.node_limit,
        include_known_occupied=args.include_known_occupied,
        include_low_low=args.include_low_low,
    )
    print(json.dumps(out, sort_keys=True))
    return 0 if out["status"] in {"COMPLETE", "NODE_LIMIT"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
