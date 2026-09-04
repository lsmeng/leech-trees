#!/usr/bin/env python3
"""Structure-only audit for the colored moment--Hall necessary system.

This intentionally does not enumerate bridge weights or low depths.  It
reconstructs the high/low LCA classes from one frozen STRUCT, checks the exact
pair partition, records raw-sum difference information, and derives the
symbolic affine Wiener first-moment equation for the full order-n tree.
"""
from __future__ import annotations

import argparse
import json
from math import comb


def ints(s: str) -> list[int]:
    return [int(x) for x in s.split(",") if x.strip()]


def parse_struct(s: str) -> list[int]:
    t = s.strip()
    if t.startswith("STRUCT"):
        return [int(x) for x in t.split()[1:]]
    return ints(t)


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
    r, m = len(lowpar), len(hpar)
    hroot = [-1] * m
    parent: list[int | None] = [None] * m
    for y, hp in enumerate(hpar):
        if hp < 0:
            root = -hp - 1
            if not 0 <= root < r:
                raise ValueError(f"bad high root {root}")
            hroot[y] = root
        else:
            if not 0 <= hp < y:
                raise ValueError(f"bad high parent {y},{hp}")
            parent[y] = hp
            hroot[y] = hroot[hp]

    def high_lca(a: int, b: int) -> int:
        seen = set()
        while True:
            seen.add(a)
            if parent[a] is None:
                break
            a = parent[a]  # type: ignore[assignment]
        while b not in seen:
            if parent[b] is None:
                raise ValueError("different components passed to high_lca")
            b = parent[b]  # type: ignore[assignment]
        return b

    comp = []
    for y in range(m):
        q = y
        while parent[q] is not None:
            q = parent[q]  # type: ignore[assignment]
        comp.append(q)

    H: list[int] = []
    S = [[] for _ in range(r)]
    for y in range(m):
        for yy in range(y):
            if comp[y] == comp[yy]:
                q = high_lca(y, yy)
                H.append(y + yy - 2 * q)
            else:
                S[low_lca(lowpar, hroot[y], hroot[yy])].append(y + yy)
    return lowpar, hroot, parent, H, S


def affine_wiener(lowpar, hpar, hroot, hparent, delta: int, order_n: int):
    """Return coefficients of the cut first moment in s,l_i and constant."""
    r, m = len(lowpar), len(hpar)
    cap = r + m
    n = order_n
    parent: list[int | None] = [None] * (cap + 1)
    # edge weight is represented as (constant, coefficient map).
    weights: list[tuple[int, dict[str, int]]] = [(0, {}) for _ in range(cap + 1)]
    for i in range(1, r):
        p = lowpar[i]
        parent[i] = p
        c = {f"l{i}": 1, f"l{p}": -1}
        weights[i] = (0, c)
    B_const = delta + 1
    for y, hp in enumerate(hpar):
        v = r + y
        if hp < 0:
            root = -hp - 1
            parent[v] = root
            weights[v] = (B_const + y, {"s": -1, f"l{root}": -1})
        else:
            parent[v] = r + hp
            weights[v] = (y - hp, {})
    parent[cap] = 0
    weights[cap] = (0, {"s": 1})

    children = [[] for _ in range(cap + 1)]
    for v in range(1, cap + 1):
        if parent[v] is None:
            raise ValueError("disconnected symbolic tree")
        children[parent[v]].append(v)
    sub = [1] * (cap + 1)
    for v in range(cap, 0, -1):
        sub[parent[v]] += sub[v]  # type: ignore[index]

    out = {"const": 0, "s": 0}
    for i in range(1, r):
        out[f"l{i}"] = 0
    for v in range(1, cap + 1):
        cut = sub[v] * (n - sub[v])
        const, coeff = weights[v]
        out["const"] += cut * const
        for key, value in coeff.items():
            out[key] = out.get(key, 0) + cut * value
    return out


def audit(lowpar_tail, hpar, delta: int, order_n: int):
    lowpar, hroot, hparent, H, S = reconstruct(lowpar_tail, hpar)
    m = len(hpar)
    pair_total = comb(m, 2)
    h_unique = len(set(H)) == len(H)
    s_unique = [len(set(x)) == len(x) for x in S]
    partition_ok = len(H) + sum(len(x) for x in S) == pair_total
    diffs = {}
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            diffs[f"{i},{j}"] = sorted({a - b for a in S[i] for b in S[j]})
    affine = affine_wiener(lowpar, hpar, hroot, hparent, delta, order_n)
    return {
        "status": "COLORED_MOMENT_HALL_STRUCTURE_AUDIT",
        "m": m,
        "r": len(lowpar),
        "delta": delta,
        "order_n": order_n,
        "H": sorted(H),
        "S": [sorted(x) for x in S],
        "W": len(H),
        "P": [len(x) for x in S],
        "pair_total": pair_total,
        "partition_ok": partition_ok,
        "H_unique": h_unique,
        "S_unique": s_unique,
        "raw_sum_difference_sets": diffs,
        "H_parity": {"even": sum(x % 2 == 0 for x in H), "odd": sum(x % 2 for x in H)},
        "S_parity": [
            {"even": sum(x % 2 == 0 for x in vals), "odd": sum(x % 2 for x in vals)}
            for vals in S
        ],
        "wiener_affine": affine,
        "wiener_target": comb(order_n, 2) * (comb(order_n, 2) + 1) // 2,
        "source_scope": "structure-only; no (s,L) enumeration; necessary-system audit, not existence proof",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lowpar", required=True)
    ap.add_argument("--struct", required=True)
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--order-n", type=int, default=25)
    args = ap.parse_args()
    print(json.dumps(audit(ints(args.lowpar), parse_struct(args.struct), args.delta, args.order_n), sort_keys=True))


if __name__ == "__main__":
    main()
