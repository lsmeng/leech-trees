#!/usr/bin/env python3
"""Independent witness checker for the three tree-labelling variants (no shared code with the search engines).

  checker_distinct.py distinct  "0-1:1 2-3:2 ..." [--n N] [--D D]
      distinct-distance tree: tree on N vertices, positive weights, all C(N,2) path sums distinct; prints max distance
      (Calhoun et al. 2007 M(n) witness if max == D).
  checker_distinct.py modular  "0-1:1 2-3:2 ..." --n N
      modular Leech tree (Leach-Walsh): edge labels in Z_k, k = C(N,2)+1, the C(N,2) path sums mod k are exactly {1..k-1}.
  checker_distinct.py leaf  "0-1:1 2-3:2 ..."
      leaf-Leech tree (Ozen-Wang-Yalman 2016): a weighted tree = subdivided tree; the leaf-leaf distances are exactly
      {3, ..., C(L,2)+2} where L = number of leaves.
Distances are computed by a plain BFS/DFS over the adjacency lists (path sums), independent of the search engines' bitsets.
Exit code 0 = valid, 1 = invalid.  Also importable: check_distinct(edges, n), check_modular(edges, n), check_leaf(edges).
"""
import sys, itertools, argparse
from collections import deque

def parse(s):
    edges = []
    for tok in s.replace("SOL:", "").split():
        uv, w = tok.split(":"); u, v = uv.split("-"); edges.append((int(u), int(v), int(w)))
    return edges

def all_dist(edges, verts):
    adj = {v: [] for v in verts}
    for u, v, w in edges: adj[u].append((v, w)); adj[v].append((u, w))
    dist = {}
    for s in verts:
        d = {s: 0}; q = deque([s])
        while q:
            x = q.popleft()
            for y, w in adj[x]:
                if y not in d: d[y] = d[x] + w; q.append(y)
        if len(d) != len(verts): return None
        dist[s] = d
    return dist

def is_tree(edges, n):
    verts = set(); [verts.update((u, v)) for u, v, w in edges]
    if len(edges) != n - 1 or len(verts) != n: return False, verts
    if any(w <= 0 for _, _, w in edges): return False, verts
    return all_dist(edges, sorted(verts)) is not None, verts

def check_distinct(edges, n=None, D=None):
    if n is None: n = len(edges) + 1
    ok, verts = is_tree(edges, n)
    if not ok: return False, "not a tree on %d vertices" % n
    verts = sorted(verts); dist = all_dist(edges, verts)
    vals = [dist[u][v] for u, v in itertools.combinations(verts, 2)]
    if len(set(vals)) != len(vals): return False, "repeated distance"
    mx = max(vals)
    if D is not None and mx > D: return False, "max distance %d > D=%d" % (mx, D)
    return True, "distinct-distance tree n=%d, %d distances, max=%d, missing=%s" % (n, len(vals), mx, sorted(set(range(1, mx + 1)) - set(vals)))

def check_modular(edges, n):
    ok, verts = is_tree(edges, n)
    if not ok: return False, "not a tree on %d vertices" % n
    k = n * (n - 1) // 2 + 1
    verts = sorted(verts); dist = all_dist(edges, verts)
    vals = sorted(dist[u][v] % k for u, v in itertools.combinations(verts, 2))
    if vals != list(range(1, k)): return False, "path sums mod %d are not {1..%d}: %s" % (k, k - 1, vals)
    return True, "modular Leech tree n=%d over Z_%d" % (n, k)

def check_leaf(edges):
    verts = set(); [verts.update((u, v)) for u, v, w in edges]
    n = len(verts)
    ok, _ = is_tree(edges, n)
    if not ok: return False, "not a tree"
    deg = {}
    for u, v, w in edges: deg[u] = deg.get(u, 0) + 1; deg[v] = deg.get(v, 0) + 1
    leaves = sorted(v for v in verts if deg[v] == 1); L = len(leaves)
    dist = all_dist(edges, sorted(verts))
    vals = sorted(dist[u][v] for u, v in itertools.combinations(leaves, 2))
    S = L * (L - 1) // 2
    if vals != list(range(3, S + 3)): return False, "leaf distances are not {3..%d}: %s" % (S + 2, vals)
    # irreducible vertex: degree >= 3 (in the subdivided tree, i.e. after expanding weights) with no leaf neighbour
    adj = {v: [] for v in verts}
    for u, v, w in edges: adj[u].append((v, w)); adj[v].append((u, w))
    irr = [v for v in verts if deg[v] >= 3 and not any(deg[y] == 1 and w == 1 for y, w in adj[v])]
    return True, "leaf-Leech tree with %d leaves (%d internal vertices of degree>=3, irreducible: %s)" % (L, sum(1 for v in verts if deg[v] >= 3), irr)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("kind", choices=["distinct", "modular", "leaf"]); ap.add_argument("sol"); ap.add_argument("--n", type=int); ap.add_argument("--D", type=int)
    a = ap.parse_args(); e = parse(a.sol)
    if a.kind == "distinct": ok, msg = check_distinct(e, a.n, a.D)
    elif a.kind == "modular": ok, msg = check_modular(e, a.n or len(e) + 1)
    else: ok, msg = check_leaf(e)
    print(("OK: " if ok else "FAIL: ") + msg); sys.exit(0 if ok else 1)
