"""REFEREE (forest engine): independent Python enumerators of the forced-weight forest search tree
(Calhoun et al. 2007 Alg. 2.7) used to audit src/forest_search.cpp.  Nothing here shares code with the engine.

Objects: weighted forests F (edge list (u,v,w), no isolated vertices) that are candidate sub-forests of a Leech tree of
order n with target distance set T (default 1..N, N=n(n-1)/2).  Forcing rule: the next edge weight is
t = min(T minus D(F)) where D(F) = set of within-component distances; the edge is added by JOIN (two vertices in different
components), ATTACH (existing vertex + new vertex) or NEW (disjoint edge).  A child is kept iff every new distance is in T,
not already in D(F), and the new distances are pairwise distinct.  Vertex bound: |V| <= n always.

Three enumerators of the same tree:
  brute(n, T)      : ALL labeled children of every node, deduplicated per level by a canonical form (complete invariant for
                     distinct-weight forests: sorted multiset of per-vertex incident-weight sets).  Ground truth for
                     'how many abstract forests are there per level'.
  enginerule(n, T) : the engine's generation rule re-implemented independently (vertex labels by order of appearance, for a
                     single-edge component only its smaller endpoint is used, join pairs x<y) but WITHOUT any dedup; the
                     canonical forms of all generated forests are collected in a list.  Test: no duplicates AND the set
                     equals brute's set  ->  the rule generates every abstract forest exactly once.
  Both accept sumprune=True to also apply the engine's parent-level rule w_next + w_max <= N (needed to reproduce the
  engine's per-depth node counts exactly; the rule is a trivial necessary condition and does not affect leaves).

count_labelings_by_topology(n, T): (used by referee_forest_diff.py) is NOT here; see tests/referee_enum.py::count_dfs.

Run:  python tests/referee_forest_enum.py [nmax]   (prints per-level counts, compares with the binary if present)
"""
import sys, os, json, subprocess, itertools
from collections import defaultdict

def leech_target(n): return frozenset(range(1, n * (n - 1) // 2 + 1))

class Forest:
    __slots__ = ("edges", "V", "adj")
    def __init__(self, edges, V):
        self.edges = edges; self.V = V
        adj = [[] for _ in range(V)]
        for u, v, w in edges: adj[u].append((v, w)); adj[v].append((u, w))
        self.adj = adj
    def dist_from(self, s):
        d = {s: 0}; st = [s]
        while st:
            u = st.pop()
            for v, w in self.adj[u]:
                if v not in d: d[v] = d[u] + w; st.append(v)
        return d
    def comps(self):
        seen = [-1] * self.V; cs = []
        for s in range(self.V):
            if seen[s] < 0:
                d = self.dist_from(s); c = sorted(d)
                for x in c: seen[x] = len(cs)
                cs.append(c)
        return seen, cs
    def dists(self):
        """all within-component distances as a list (with multiplicity)"""
        out = []
        for s in range(self.V):
            for x, d in self.dist_from(s).items():
                if x > s: out.append(d)
        return out
    def canon(self):
        inc = [tuple(sorted(w for _, w in self.adj[u])) for u in range(self.V)]
        return tuple(sorted(inc))
    def wmax(self): return max((w for _, _, w in self.edges), default=0)

def check_child(F, Dset, T, N):
    """recompute all distances of F from scratch; valid iff all distinct and all in T (subset of 1..N)"""
    ds = F.dists()
    if len(ds) != len(set(ds)): return False
    return all(d in T for d in ds)

def children_all(F, t, n, T, N):
    """every labeled child by join/attach/new (no symmetry restriction)"""
    seen, cs = F.comps(); V = F.V; out = []
    for x in range(V):
        for y in range(x + 1, V):
            if seen[x] != seen[y]: out.append(Forest(F.edges + [(x, y, t)], V))
    if V < n:
        for x in range(V): out.append(Forest(F.edges + [(x, V, t)], V + 1))
    if V + 2 <= n: out.append(Forest(F.edges + [(V, V + 1, t)], V + 2))
    return out

def children_enginerule(F, t, n, T, N):
    """engine's rule: for a single-edge component only the smaller endpoint; join x<y; attach; new"""
    seen, cs = F.comps(); V = F.V; out = []
    elig = [x for x in range(V) if not (len(cs[seen[x]]) == 2 and x != min(cs[seen[x]]))]
    for i, x in enumerate(elig):
        for y in elig[i + 1:]:
            if seen[x] != seen[y]: out.append(Forest(F.edges + [(x, y, t)], V))
    if V < n:
        for x in elig: out.append(Forest(F.edges + [(x, V, t)], V + 1))
    if V + 2 <= n: out.append(Forest(F.edges + [(V, V + 1, t)], V + 2))
    return out

def enumerate_tree(n, T=None, sumprune=True, rule="brute", nmax_level=None, keep=False):
    """returns per-level dict: {level: (#abstract forests, #labeled generated, #solutions)}; with rule='enginerule' the
    'labeled generated' count is what the engine would visit and 'dups' records canonical-form collisions."""
    T = T or leech_target(n); N = max(T); E = n - 1
    gen = children_all if rule == "brute" else children_enginerule
    level = {(): Forest([], 0)}; stats = {0: dict(abstract=1, generated=1, sols=0, dups=0)}
    levels = [dict(level)] if keep else None
    L = 0
    while level:
        if nmax_level is not None and L >= nmax_level: break
        nxt = {}; ngen = 0; ndup = 0; nsol = 0
        for F in level.values():
            Dset = set(F.dists()); missing = sorted(T - Dset)
            if not missing:
                if len(F.edges) == E and F.V == n: nsol += 1
                continue
            t = missing[0]
            if len(F.edges) >= E: continue
            if sumprune and F.edges and t + F.wmax() > N: continue
            for C in gen(F, t, n, T, N):
                if not check_child(C, Dset, T, N): continue
                ngen += 1; c = C.canon()
                if c in nxt: ndup += 1
                else: nxt[c] = C
        stats[L]["sols"] = nsol
        if not nxt: break
        L += 1; stats[L] = dict(abstract=len(nxt), generated=ngen, sols=0, dups=ndup)
        level = nxt
        if keep: levels.append(dict(level))
    # solutions at the last level
    nsol = 0
    for F in level.values():
        Dset = set(F.dists())
        if not (T - Dset) and len(F.edges) == E and F.V == n: nsol += 1
    stats[L]["sols"] = nsol
    return (stats, levels) if keep else stats

def engine_depth_hist(bin_path, n, target=None, extra=()):
    args = [bin_path, str(n), "-q", *extra]
    if target: args += ["--target", ",".join(map(str, sorted(target)))]
    p = subprocess.run(args, capture_output=True, text=True, check=True)
    hist = {}
    for line in p.stderr.splitlines():
        if line.startswith("depth:"):
            for tok in line.split()[1:]:
                d, c = tok.split(":"); hist[int(d)] = int(c)
    rec = json.loads([l for l in p.stdout.splitlines() if l.startswith("{")][-1])
    return hist, rec

if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    BIN = os.environ.get("FOREST_BIN", os.path.join(ROOT, "bin", "forest_search"))
    for n in range(4, nmax + 1):
        sb = enumerate_tree(n, sumprune=True, rule="brute")
        se = enumerate_tree(n, sumprune=True, rule="enginerule")
        s0 = enumerate_tree(n, sumprune=False, rule="brute")
        eh, rec = engine_depth_hist(BIN, n) if os.path.exists(BIN) else ({}, {})
        print(f"n={n}: brute abstract per level {[sb[l]['abstract'] for l in sorted(sb)]} sols {sum(v['sols'] for v in sb.values())}")
        print(f"      brute labeled generated   {[sb[l]['generated'] for l in sorted(sb)]}")
        print(f"      enginerule generated      {[se[l]['generated'] for l in sorted(se)]} dups {[se[l]['dups'] for l in sorted(se)]}")
        print(f"      no-sumprune abstract      {[s0[l]['abstract'] for l in sorted(s0)]} sols {sum(v['sols'] for v in s0.values())}")
        print(f"      engine depth hist         {[eh[l] for l in sorted(eh) if eh[l]]} nsol {rec.get('nsol')}")
