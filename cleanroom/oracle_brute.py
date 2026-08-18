"""Independent brute-force oracle for the forced-forest search tree (clean-room).
Generates ALL labeled children (no symmetry rule at all), validates each by recomputing the
full distance multiset from scratch (BFS), and de-duplicates every level by a complete
canonical form of a distinct-weight forest without isolated vertices:
   canon(F) = sorted tuple over vertices of the sorted tuple of incident edge weights.
(Complete: vertices are recovered as the tuples, edge w joins the two tuples containing w.)
Prints per-level counts of abstract forced forests; compare with cr_forest --no-sumrule.
usage: python oracle_brute.py n [--sumrule]
"""
import sys
from collections import deque

def distances(n_used, edges):
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w)); adj.setdefault(v, []).append((u, w))
    dl = []
    verts = sorted(adj)
    for s in verts:
        d = {s: 0}; q = deque([s])
        while q:
            u = q.popleft()
            for v, w in adj[u]:
                if v not in d: d[v] = d[u] + w; q.append(v)
        dl += [d[t] for t in d if t > s]
    return dl

def comps(edges):
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x: x = parent[x]
        return x
    for u, v, w in edges:
        parent[find(u)] = find(v)
    c = {}
    for x in list(parent): c.setdefault(find(x), []).append(x)
    return list(c.values())

def canon(edges):
    inc = {}
    for u, v, w in edges:
        inc.setdefault(u, []).append(w); inc.setdefault(v, []).append(w)
    return tuple(sorted(tuple(sorted(x)) for x in inc.values()))

def main():
    n = int(sys.argv[1]); sumrule = '--sumrule' in sys.argv
    N = n * (n - 1) // 2
    level = {(): []}  # canon -> edges ; root = empty forest
    counts = [1]; nsol = 0
    lev = 0
    while level and lev < n - 1:
        nxt = {}
        for key, edges in level.items():
            V = len({x for e in edges for x in e[:2]})
            dl = distances(V, edges)
            ds = set(dl)
            assert len(dl) == len(ds)
            if len(edges) == n - 1:
                continue
            t = 1
            while t in ds: t += 1
            if sumrule and edges and t + max(e[2] for e in edges) > N:
                continue
            cs = comps(edges)
            cands = []
            for i in range(len(cs)):
                for j in range(i + 1, len(cs)):
                    for x in cs[i]:
                        for y in cs[j]:
                            cands.append(edges + [(x, y, t)])
            if V + 1 <= n:
                for c in cs:
                    for x in c:
                        cands.append(edges + [(x, V, t)])
            if V + 2 <= n:
                cands.append(edges + [(V, V + 1, t)])
            for ch in cands:
                dl2 = distances(0, ch)
                if len(dl2) != len(set(dl2)) or max(dl2) > N:
                    continue
                k = canon(ch)
                nxt.setdefault(k, ch)
        lev += 1
        counts.append(len(nxt))
        for k, ch in nxt.items():
            if len(ch) == n - 1:
                nsol += 1
        level = nxt
    while len(counts) < n: counts.append(0)
    print({"n": n, "sumrule": sumrule, "levels": counts, "nodes": sum(counts), "nsol": nsol})

main()
