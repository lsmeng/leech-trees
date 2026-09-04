#!/usr/bin/env python3
"""Enumerate the possible "top window skeletons" of an order-25 Leech tree.

Setting (proved in checkpoint §3.10).  (a,b) is the unique pair at distance
N=300; for u not in {a,b} put e(u) = N - d(a,u) >= 1, f(u) = N - d(b,u) >= 2
(after renaming so that d(a,w) = N-1 for some w), p(u) = (N + f - e)/2 the
position of u's foot on the a-b path, h(u) = (N - e - f)/2 its height; e and
f have the same parity; for u,v not in {a,b} with p(u) <= p(v),
    d(u,v) = N - f(u) - e(v) - 2 h_c,
with h_c = 0 unless p(u) = p(v) and u,v hang in the same branch (then
1 <= h_c <= min(h(u),h(v))).  All e-values are distinct, all f-values are
distinct, and no e-value equals an f-value (the values N-e, N-f are distances
from a resp. b of different pairs).

The top window is the set of distances N-t, 0 <= t <= W.  Level t = 0 is
(a,b).  Every level 1 <= t <= W is realised by exactly one pair, which is an
A-step (a,v) with e(v)=t, a B-step (u,b) with f(u)=t, or a cross pair (u,v)
with f(u) + e(v) + 2h_c = t (u before v in the p-order, or tied and same
branch).  Conversely every pair whose value lies in the window must be the
unique realiser of its level.

Model.  A vertex is relevant to the window iff e <= W or f <= W.  Its other
coordinate is either an explicit value in [1, WX] (WX = W + 14 covers every
value that can affect the p-order relative to a double-far vertex) or "big"
(> WX), in which case only its parity and side matter.  Relevant vertices with
f <= W ("A-side") precede those with e <= W and f big ("B-side"), so cross
pairs between them have h_c = 0; ties in p only occur between vertices with
both coordinates explicit.

The enumeration is a DFS over the levels t = 1..W deciding the realiser of
each level, creating vertices lazily.  It counts the skeletons and prints
statistics.  It is a NECESSARY-condition enumerator: a skeleton says nothing
about the rest of the tree.  Usage: top_window_skeletons.py W [--emit]
"""
from __future__ import annotations

import sys
from collections import Counter

N = 300


def run(W: int, emit: bool = False):
    WX = W + 14
    # vertex: dict(e=int or None(big), f=int or None(big), epar, fpar)
    verts: list[dict] = []
    used_e: set[int] = {0}          # b has e=0
    used_f: set[int] = {0}          # a has f=0
    level_real: list[str] = [""] * (W + 1)
    count = 0
    stats = Counter()
    shapes = Counter()
    smallsets = set()   # distinct (pattern, small e-values, small f-values, cross assignments)

    def coord_ok(val, side_used, other_used):
        return val not in side_used and val not in other_used

    def p_of(v):
        # position; None if depends on a big coordinate (then only side matters)
        if v["e"] is None or v["f"] is None:
            return None
        return (N + v["f"] - v["e"]) / 2

    def side(v):
        # 'A' if f small and e big/large, 'B' if e small and f big, 'D' double
        if v["f"] is not None and v["f"] <= W and (v["e"] is None or v["e"] > W):
            return "A"
        if v["e"] is not None and v["e"] <= W and (v["f"] is None or v["f"] > W):
            return "B"
        return "D"

    def before(u, v):
        """True if u strictly precedes v in p-order, False if v precedes u,
        None if tied (both explicit and equal p)."""
        pu, pv = p_of(u), p_of(v)
        if pu is not None and pv is not None:
            if pu < pv:
                return True
            if pu > pv:
                return False
            return None
        # at least one big coordinate: order by side
        su, sv = side(u), side(v)
        order = {"A": 0, "D": 1, "B": 2}
        if order[su] != order[sv]:
            return order[su] < order[sv]
        # same side with a big coordinate: their cross value is > W anyway; pick arbitrary
        return True

    def window_pairs_ok():
        """Check that every pair of existing vertices whose value could lie in
        the window is the registered realiser of exactly its level, and that no
        level has two realisers.  Returns the set of levels realised by cross
        pairs (with the pair identity) or None if inconsistent."""
        found: dict[int, tuple] = {}
        n = len(verts)
        for i in range(n):
            for j in range(i + 1, n):
                u, v = verts[i], verts[j]
                b = before(u, v)
                cands = []
                if b is None:
                    # tied: different branches (h_c=0) or same branch with h_c>=1
                    # f_u + e_v == f_v + e_u when tied
                    base = (u["f"] + v["e"]) if (u["f"] is not None and v["e"] is not None) else None
                    if base is None:
                        continue
                    hmax = min((N - u["e"] - u["f"]) // 2, (N - v["e"] - v["f"]) // 2)
                    for hc in range(0, hmax + 1):
                        t = base + 2 * hc
                        if t <= W:
                            cands.append((t, hc))
                    # exactly one of these is the actual value; recorded in pair_choice
                    key = (i, j)
                    if key not in pair_choice:
                        continue  # will be decided when needed
                    hc = pair_choice[key]
                    t = base + 2 * hc
                    if t > W:
                        continue
                    if t in found:
                        return None
                    found[t] = (i, j)
                else:
                    if not b:
                        u, v = v, u
                    if u["f"] is None or v["e"] is None:
                        continue
                    t = u["f"] + v["e"]
                    if t > W:
                        continue
                    if t in found:
                        return None
                    found[t] = (i, j)
        return found

    pair_choice: dict[tuple, int] = {}

    def consistent():
        found = window_pairs_ok()
        if found is None:
            return False
        for t, pair in found.items():
            if level_real[t] == "":
                return False          # a cross pair produces a level not yet assigned -> only ok if it is assigned to it later; treat as pending
            if level_real[t] != ("X", pair):
                return False
        for t in range(1, W + 1):
            lr = level_real[t]
            if isinstance(lr, tuple) and lr[0] == "X" and found.get(t) != lr[1]:
                return False
        return True

    def new_vertex(e, f):
        verts.append({"e": e, "f": f})

    def dfs(t):
        nonlocal count
        if t > W:
            if consistent():
                count += 1
                nA = sum(1 for v in verts if side(v) == "A")
                nB = sum(1 for v in verts if side(v) == "B")
                nD = sum(1 for v in verts if side(v) == "D")
                stats[(nA, nB, nD)] += 1
                pat = tuple(("A" if isinstance(x, str) and x == "A" else "B" if x == "B" else "X") for x in level_real[1:])
                shapes[pat] += 1
                Es = tuple(sorted(v["e"] for v in verts if v["e"] is not None and v["e"] <= W))
                Fs = tuple(sorted(v["f"] for v in verts if v["f"] is not None and v["f"] <= W))
                Xs = tuple(sorted((lv, verts[pr[0]]["f"] if verts[pr[0]]["f"] is not None else -1, verts[pr[1]]["e"] if verts[pr[1]]["e"] is not None else -1)
                                  for lv, x in enumerate(level_real) if isinstance(x, tuple) for pr in [x[1]]))
                smallsets.add((pat, Es, Fs, Xs))
                if emit:
                    print("SKEL", level_real[1:], [(v["e"], v["f"]) for v in verts])
            return
        # option X: the level is realised by a cross pair of existing vertices
        n = len(verts)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                u, v = verts[i], verts[j]
                b = before(u, v)
                if b is None:
                    # tied pair (i<j canonical)
                    if i > j:
                        continue
                    base = u["f"] + v["e"]
                    hmax = min((N - u["e"] - u["f"]) // 2, (N - v["e"] - v["f"]) // 2)
                    for hc in range(0, hmax + 1):
                        if base + 2 * hc == t and (i, j) not in pair_choice:
                            pair_choice[(i, j)] = hc
                            level_real[t] = ("X", (i, j))
                            dfs(t + 1)
                            level_real[t] = ""
                            del pair_choice[(i, j)]
                elif b:
                    if u["f"] is None or v["e"] is None:
                        continue
                    if u["f"] + v["e"] == t:
                        level_real[t] = ("X", (min(i, j), max(i, j)) if i < j else (j, i))
                        # canonical key: (min,max) but realiser identity is the unordered pair
                        level_real[t] = ("X", (min(i, j), max(i, j)))
                        dfs(t + 1)
                        level_real[t] = ""
        # option A: new vertex v with e = t (t must be unused as e and as f)
        if t not in used_e and t not in used_f:
            # its f: explicit value in [2, WX] with same parity, unused, or big
            for fval in list(range(2, WX + 1)) + [None]:
                if fval is not None and (fval % 2 != t % 2 or fval in used_f or fval in used_e):
                    continue
                if fval is not None and fval + t > N:
                    continue
                new_vertex(t, fval)
                used_e.add(t)
                if fval is not None:
                    used_f.add(fval)
                level_real[t] = "A"
                if partial_ok():
                    dfs(t + 1)
                level_real[t] = ""
                used_e.discard(t)
                if fval is not None:
                    used_f.discard(fval)
                verts.pop()
        # option B: new vertex u with f = t (t >= 2)
        if t >= 2 and t not in used_f and t not in used_e:
            for eval_ in list(range(1, WX + 1)) + [None]:
                if eval_ is not None and (eval_ % 2 != t % 2 or eval_ in used_e or eval_ in used_f):
                    continue
                if eval_ is not None and eval_ + t > N:
                    continue
                new_vertex(eval_, t)
                used_f.add(t)
                if eval_ is not None:
                    used_e.add(eval_)
                level_real[t] = "B"
                if partial_ok():
                    dfs(t + 1)
                level_real[t] = ""
                used_f.discard(t)
                if eval_ is not None:
                    used_e.discard(eval_)
                verts.pop()

    def partial_ok():
        """No two existing pairs may claim the same window level, and no
        existing cross pair may claim a level already realised by a step or by
        a different pair, except levels not yet reached (which must then be
        realised by that pair later — enforced when the level is reached since
        option X requires the pair to exist; but a pair could also be forced
        onto a level < current t already assigned to a step: reject)."""
        found = window_pairs_ok()
        if found is None:
            return False
        for lv, pair in found.items():
            lr = level_real[lv]
            if lr == "":
                continue
            if lr in ("A", "B"):
                return False
            if lr[1] != pair:
                return False
        return True

    dfs(1)
    print(f"W={W} WX={WX} skeletons={count} distinct_small_structures={len(smallsets)} distinct_patterns={len(shapes)}")
    print("  (nA, nB, nD) counts:", sorted(stats.items()))
    top = shapes.most_common(8)
    print("  most common level patterns (A=a-step, B=b-step, X=cross):")
    for pat, c in top:
        print("   ", "".join(pat), c)
    return count


if __name__ == "__main__":
    W = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    run(W, emit="--emit" in sys.argv)
