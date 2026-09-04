#!/usr/bin/env python3
"""Machine checks of the session's diameter-<=4 structural lemmas on
(a) the known Leech trees (L6 has diameter 3 -> applicable), and
(b) random distinct-distance diameter-<=4 trees (the lemmas only use
    distinctness of distances, so they must hold for these too).

Lemmas (T diam<=4, c a 2-centre, a_z = d(c,z), branches = children subtrees):
 W0: all a_z distinct (z != c).
 W1: for any interval J=(L,L+W], branch i: #{z in branch i: a_z in J} <= 2*sqrt(W)+2.
 W2: sum_{i<j} h_i h_j <= 2W  (h_i = count in branch i with a in J).
 W3: total count in J <= 4*sqrt(W)+2.
 W4: (i) a* >= N/2 (Leech only), (ii) z outside branch(a*): a_z <= N-a* (Leech only),
     (iii) delta = 2a*-N >= 1 (Leech only).
 M: master identity (any weighted tree, distances distinct or not):
    F(q)^2 - F(q^2) - sum_i (1-q^{-2x_i})(F_i(q)^2 - F_i(q^2)) = 2*sum_p q^{d_p}
    with F = sum_{v} q^{a_v} (a_c = 0), F_i over branch i only; checked as
    polynomial identity at random integer q (exact integer arithmetic).
"""
import random, math, json, sys
from itertools import combinations
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def build(n, edges):
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w)); adj.setdefault(v, []).append((u, w))
    def bfs(s):
        d = {s: (0, 0)}; st = [s]
        while st:
            x = st.pop()
            for y, w in adj[x]:
                if y not in d:
                    d[y] = (d[x][0] + w, d[x][1] + 1); st.append(y)
        return d
    return adj, bfs

def check_tree(n, edges, leech):
    adj, bfs = build(n, edges)
    # find 2-centre: vertex with hop-ecc <= 2
    centres = []
    for c in adj:
        d = bfs(c)
        if max(h for _, h in d.values()) <= 2:
            centres.append(c)
    require(centres, "no 2-centre (diameter > 4?)")
    c = centres[0]
    d = bfs(c)
    a = {z: d[z][0] for z in adj if z != c}
    N = n * (n - 1) // 2
    # branches
    branch = {}
    for v, w in adj[c]:
        branch[v] = v
        for y, w2 in adj[v]:
            if y != c:
                branch[y] = v
    # W0
    require(len(set(a.values())) == len(a), "W0 fail")
    verts = list(a)
    # windows: test every (L, W) with L in 0..max(a), W in 1..max(a)+1 (coarse grid for speed)
    amax = max(a.values())
    ws = sorted(set([1, 2, 3, 5, 8, 13, 21, 34, amax // 2 + 1, amax]))
    for W in ws:
        if W < 1: continue
        for L in range(0, amax + 1, max(1, W // 3)):
            J = lambda z: L < a[z] <= L + W
            hs = {}
            for z in verts:
                if J(z): hs[branch[z]] = hs.get(branch[z], 0) + 1
            hvals = list(hs.values())
            for h in hvals:
                require(h <= 2 * math.sqrt(W) + 2 + 1e-9, ("W1 fail", W, L, h))
            cross = sum(hs[i] * hs[j] for i, j in combinations(hs, 2))
            require(cross <= 2 * W, ("W2 fail", W, L, cross))
            require(sum(hvals) <= 4 * math.sqrt(W) + 2 + 1e-9, ("W3 fail", W, L))
    if leech:
        astar = max(a.values()); zstar = max(a, key=a.get)
        require(2 * astar >= N, "W4i fail")
        require(2 * astar - N >= 1, "W4iii fail")
        bs = branch[zstar]
        for z in verts:
            if branch[z] != bs:
                require(a[z] <= N - astar, "W4ii fail")
    # master identity at random q (exact; use Fraction to handle q^{-2x})
    from fractions import Fraction
    q = Fraction(random.randint(2, 7))
    F = 1 + sum(q ** av for av in a.values())
    lhs = F * F
    # F(q^2)
    F2 = 1 + sum((q * q) ** av for av in a.values())
    lhs -= F2
    for v, w in adj[c]:
        bverts = [z for z in verts if branch[z] == v]
        Fi = sum(q ** a[z] for z in bverts)
        Fi2 = sum((q * q) ** a[z] for z in bverts)
        lhs -= (1 - q ** (-2 * w)) * (Fi * Fi - Fi2)
    # rhs: 2 * sum over pairs q^{d}
    dall = []
    for s in adj:
        ds = bfs(s)
        for t2 in adj:
            if t2 > s: dall.append(ds[t2][0])
    rhs = 2 * sum(q ** dd for dd in dall)
    require(lhs == rhs, "master identity fail")
    return True

require(sys.flags.optimize == 0, "run without python -O/-OO")
repo = Path(__file__).resolve().parents[2]
known = json.loads((repo / "data" / "known_leech_trees.json").read_text())
for t in known["trees"]:
    if t["n"] >= 3:
        check_tree(t["n"], [tuple(e) for e in t["edges"]], leech=True)
        print("known", t["name"], "OK")

# random distinct-distance diam<=4 trees (weight range scaled with n so rejection sampling terminates)
rng = random.Random(7)
def rand_d4(n):
    while True:
        verts = [0]; edges = []
        nb = rng.randint(2, max(2, (n - 1) // 2)); roots = []
        for _ in range(nb):
            if len(verts) >= n: break
            v = len(verts); verts.append(v); edges.append((0, v)); roots.append(v)
        while len(verts) < n:
            v = len(verts); verts.append(v); edges.append((rng.choice(roots), v))
        ws = rng.sample(range(1, 40 * n * n), len(edges))
        wedges = [(u, v, w) for (u, v), w in zip(edges, ws)]
        adjx, bfsx = build(n, wedges)
        dd = []
        for s in range(n):
            d = bfsx(s)
            for t2 in range(s + 1, n): dd.append(d[t2][0])
        if len(set(dd)) == len(dd):
            return wedges
ok = 0
for _ in range(300):
    n = rng.randint(5, 14)
    wedges = rand_d4(n)
    check_tree(n, wedges, leech=False)
    ok += 1
print("random distinct-distance diam<=4 trees checked:", ok, "all OK")
