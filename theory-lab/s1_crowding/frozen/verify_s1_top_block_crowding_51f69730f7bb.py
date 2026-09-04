#!/usr/bin/env python3
"""Independent verification of the singleton-final-cap top-block crowding theorem.

Setting (FW303.10 singleton branch, order 25, N=300): delete the heaviest edge
(weight s) whose detached side is a single leaf.  K is the remaining 24-vertex
tree rooted at the bridge endpoint x; D = rooted depths (24 distinct values,
0 in D), F = Spec(K), and F ⊔ (s+D) = [1,300].  With delta = max F = 276+r
the top-block lemma gives D = L ⊔ [B, A], |L| = r, A = 300-s, B = A-23+r,
i.e. m = 24-r "high" vertices at consecutive depths B..A and r "low" vertices.

Theorem (crowding).  Any two high vertices h_i,h_j (depths B+y_i, B+y_j,
0<=y<m, y_i != y_j) have distance
    y_i + y_j - 2q            if their LCA is high (depth B+q), and
    2B - 2l + y_i + y_j       if their LCA is a low vertex of depth l.
Hence, inside each of the r+1 classes (LCA high, or LCA = a given low
vertex), pairwise-distinct distances force pairwise-distinct sums
y_i+y_j in [1, 2m-3].  So at most (r+1)(2m-3) high-high pairs can have
distinct distances, while there are C(m,2) of them.
    r=3 (delta=279): 4*39 = 156 < 210 = C(21,2)   -> impossible
    r=4 (delta=280): 5*37 = 185 < 190 = C(20,2)   -> impossible
    r=5 (delta=281): 6*35 = 210 >= 171            -> not excluded by this count

This script checks (1) the parity lemma table for delta=277..281, (2) the
distance formulas against an independent BFS on random trees with the
required depth structure, (3) that the number of *distinct* high-high
distances never exceeds (r+1)(2m-3) on random and hill-climbed trees, and
(4) the arithmetic of the counting table.  It uses no project code.
"""
from __future__ import annotations

import itertools
import random
import sys
from collections import Counter, defaultdict


def parity_survivors(delta: int) -> list[tuple[str, tuple[int, ...]]]:
    """Return parity patterns (s parity, parities of l_1..l_{r-1}) that satisfy
    the exact parity equation.  E,O = numbers of even/odd depths in D."""
    r = delta - 276
    m = 24 - r
    out = []
    for s_par in (0, 1):
        for A_par in (0, 1):  # A = 300-s has parity of s (300 even)
            if A_par != s_par:
                continue
            B_par = (A_par + (m - 1)) % 2  # B = A - (m-1)
            # high block: m consecutive depths starting at parity B_par
            high_even = (m + (1 if B_par == 0 else 0)) // 2
            high_odd = m - high_even
            for lp in itertools.product((0, 1), repeat=r - 1):
                E = high_even + 1 + lp.count(0)  # +1 for depth 0
                O = high_odd + lp.count(1)
                assert E + O == 24
                ok = (O * (E + 1) == 150) if s_par == 0 else (E * (O + 1) == 150)
                if ok:
                    out.append(("s even" if s_par == 0 else "s odd", lp))
    return out


def random_low_tree(r: int, B: int, rng: random.Random, shape: str | None = None):
    """Rooted tree on r low vertices with distinct depths 0 = l0 < l1 < ... < B-1.
    Returns (depths, parent) with parent[0] = -1.  Vertex i has depth depths[i]
    and its parent is a vertex of smaller depth (so the low set is connected)."""
    while True:
        ls = sorted(rng.sample(range(1, B), r - 1)) if r > 1 else []
        depths = [0] + ls
        if r == 3 and shape == "chain":
            parent = [-1, 0, 1]
        elif r == 3 and shape == "star":
            parent = [-1, 0, 0]
        else:
            parent = [-1] + [rng.randrange(i) for i in range(1, r)]
        return depths, parent


def random_high_forest(m: int, r: int, rng: random.Random):
    """parent of high vertex y in {low 0..r-1 (encoded as -1-i)} ∪ {0..y-1}."""
    par = []
    for y in range(m):
        choices = [-1 - i for i in range(r)] + list(range(y))
        par.append(rng.choice(choices))
    return par


def build_tree(r: int, m: int, B: int, low_depths, low_parent, high_parent):
    """Vertices 0..r-1 low, r..r+m-1 high (high y -> index r+y).  Returns
    adjacency list with weights, and depth list."""
    n = r + m
    depth = list(low_depths) + [B + y for y in range(m)]
    adj = [[] for _ in range(n)]
    parent = [-1] * n
    for i in range(1, r):
        p = low_parent[i]
        parent[i] = p
    for y in range(m):
        hp = high_parent[y]
        parent[r + y] = (-1 - hp) if hp < 0 else r + hp
    for v in range(1, n):
        p = parent[v]
        w = depth[v] - depth[p]
        assert w > 0, (v, p, depth[v], depth[p])
        adj[v].append((p, w))
        adj[p].append((v, w))
    return adj, depth, parent


def bfs_dist(adj, src):
    n = len(adj)
    dist = [None] * n
    dist[src] = 0
    stack = [src]
    while stack:
        v = stack.pop()
        for u, w in adj[v]:
            if dist[u] is None:
                dist[u] = dist[v] + w
                stack.append(u)
    assert all(d is not None for d in dist)
    return dist


def lca(parent, depth, a, b):
    anc = set()
    v = a
    while v != -1:
        anc.add(v)
        v = parent[v]
    v = b
    while v not in anc:
        v = parent[v]
    return v


def check_formulas_and_capacity(r: int, trials: int, rng: random.Random, shape=None) -> int:
    """Return the maximum number of distinct high-high distances observed."""
    m = 24 - r
    cap = (r + 1) * (2 * m - 3)
    best = 0
    for _ in range(trials):
        s = rng.choice(range(24, 301 - m - r))  # keep B-1 >= r-1 so L fits
        A = 300 - s
        B = A - (m - 1)
        low_depths, low_parent = random_low_tree(r, B, rng, shape)
        hp = random_high_forest(m, r, rng)
        adj, depth, parent = build_tree(r, m, B, low_depths, low_parent, hp)
        n = r + m
        dist = [bfs_dist(adj, v) for v in range(n)]
        classes = defaultdict(list)
        for i in range(m):
            for j in range(i + 1, m):
                a, b = r + i, r + j
                w = lca(parent, depth, a, b)
                d = dist[a][b]
                if w >= r:  # high LCA
                    q = depth[w] - B
                    assert d == i + j - 2 * q, (d, i, j, q)
                    assert 1 <= d <= 2 * m - 3
                    classes["high"].append(d)
                else:
                    l = depth[w]
                    assert d == 2 * B - 2 * l + i + j, (d, i, j, l)
                    classes[("low", w)].append(d)
        # distinct pairs per class force distinct sums: check directly that
        # the number of distinct distances in each class is <= 2m-3
        total_distinct = 0
        for key, ds in classes.items():
            distinct = len(set(ds))
            assert distinct <= 2 * m - 3, (key, distinct)
            total_distinct += distinct
        # distinct high-high distances overall
        allhh = set()
        for ds in classes.values():
            allhh.update(ds)
        assert len(allhh) <= total_distinct <= cap
        best = max(best, len(allhh))
    return best


def hill_climb_max_distinct(r: int, iters: int, rng: random.Random) -> int:
    """Greedy local search trying to maximize distinct high-high distances;
    must never exceed (r+1)(2m-3)."""
    m = 24 - r
    cap = (r + 1) * (2 * m - 3)
    s = 24 + rng.randrange(0, 301 - m - r - 24)
    A = 300 - s
    B = A - (m - 1)
    low_depths, low_parent = random_low_tree(r, B, rng)
    hp = random_high_forest(m, r, rng)

    def score(hp_):
        adj, depth, parent = build_tree(r, m, B, low_depths, low_parent, hp_)
        vals = set()
        for i in range(m):
            di = bfs_dist(adj, r + i)
            for j in range(i + 1, m):
                vals.add(di[r + j])
        return len(vals)

    cur = score(hp)
    best = cur
    for _ in range(iters):
        y = rng.randrange(m)
        choices = [-1 - i for i in range(r)] + list(range(y))
        old = hp[y]
        hp[y] = rng.choice(choices)
        sc = score(hp)
        if sc >= cur:
            cur = sc
            best = max(best, sc)
        else:
            hp[y] = old
        assert best <= cap, (best, cap)
    return best


def main() -> None:
    rng = random.Random(20260901)
    print("== (1) exact parity equation, singleton cap, delta=277..281 ==")
    for delta in range(277, 282):
        surv = parity_survivors(delta)
        r = delta - 276
        print(f"delta={delta} r={r} m={24-r}: {len(surv)} surviving parity patterns")
        for tag, lp in surv:
            print(f"   {tag}, parities of l_1..l_{r-1} (0=even,1=odd): {lp}")
    print()
    print("== (4) counting table: capacity (r+1)(2m-3) vs C(m,2) ==")
    for r in range(1, 12):
        m = 24 - r
        cap = (r + 1) * (2 * m - 3)
        need = m * (m - 1) // 2
        print(f"delta={276+r} r={r:2d} m={m:2d}: capacity {cap:4d}  pairs {need:4d}  "
              f"{'IMPOSSIBLE' if cap < need else 'not excluded'}")
    print()
    print("== (2)+(3) formulas vs BFS, and distinct high-high distances <= capacity ==")
    for r, shape in ((3, "chain"), (3, "star"), (4, None), (5, None), (6, None)):
        best = check_formulas_and_capacity(r, 3000, rng, shape)
        m = 24 - r
        print(f"r={r} shape={shape or 'random'}: 3000 random trees OK; max distinct HH "
              f"distances seen = {best} (capacity {(r+1)*(2*m-3)}, pairs {m*(m-1)//2})")
    for r in (3, 4, 5):
        best = max(hill_climb_max_distinct(r, 4000, rng) for _ in range(5))
        m = 24 - r
        print(f"r={r}: hill-climb max distinct HH distances = {best} "
              f"(capacity {(r+1)*(2*m-3)}, pairs {m*(m-1)//2})")
    print()
    print("VERIFIED_S1_TOP_BLOCK_CROWDING_ARITHMETIC")


if __name__ == "__main__":
    main()
