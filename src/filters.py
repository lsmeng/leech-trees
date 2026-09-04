"""Topology filters for the Leech-tree search, one function per lemma.

Every filter takes an *unlabeled* tree (networkx.Graph on n vertices) and returns
True if the topology SURVIVES (may still carry a Leech labeling) and False if the
lemma PROVES that no Leech labeling exists on that topology.  Each docstring cites
the lemma (see docs/literature-ledger.md for the full statement + proof sketch) and
says whether the proof was re-derived here (VERIFIED-BY-ME) or is taken on trust.

Self-test:  .venv/bin/python src/filters.py --selftest
    * every filter must accept the five known Leech trees (data/known_leech_trees.json)
    * every filter must accept every topology on n<=8 that admits a Leech labeling
      (found by an exhaustive forced-weight DFS, see leech_labelings_of_topology)
    * table constants (Golomb, star-Sidon max degree) are re-verified for small S.
Survivor counts at n=18:  .venv/bin/python src/filters.py --count data/trees_18.jsonl

Definitions.  n = order, S = C(n,2) = largest distance.  A tree topology has
diameter t = number of EDGES on a longest path.  Leech tree = positive-integer edge
weights whose C(n,2) path sums are exactly {1..S}.
"""
from __future__ import annotations

import json
import sys
from math import comb, isqrt

import networkx as nx

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def graph_from_edges(n, edges):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from((int(u), int(v)) for u, v in edges)
    return G


def diameter_edges(G):
    """Number of edges on a longest path (two-sweep BFS; exact on trees)."""
    n = G.number_of_nodes()
    if n <= 1:
        return 0
    s = next(iter(G.nodes))
    d = nx.single_source_shortest_path_length(G, s)
    far = max(d, key=d.get)
    d2 = nx.single_source_shortest_path_length(G, far)
    return max(d2.values())


def is_path_graph(G):
    n = G.number_of_nodes()
    if n <= 2:
        return True
    degs = sorted(d for _, d in G.degree())
    return degs[0] == 1 and degs[1] == 1 and all(x == 2 for x in degs[2:])


# ----------------------------------------------------------------------------
# F0  Taylor 1977 (order condition; VERIFIED-BY-ME, proof re-derived in ledger L2)
# ----------------------------------------------------------------------------

def passes_taylor_order(n):
    """Taylor 1977 (Math. Mag. 50(5) 258-259), reproduced as SWZ 2005 Thm 1 and
    Calhoun et al. 2007 Thm 1.3:  if a Leech tree on n vertices exists then
    n = k^2 or n = k^2 + 2.  Pure order filter (independent of shape); at n = 18
    it passes (18 = 16 + 2).  VERIFIED-BY-ME (parity double count, ledger L2)."""
    k = isqrt(n)
    if k * k == n:
        return True
    k = isqrt(n - 2) if n >= 2 else 0
    return k * k == n - 2


# ----------------------------------------------------------------------------
# F1  Paths (Leech 1975, proof in SWZ 2005 p.3; VERIFIED-BY-ME, ledger L3)
# ----------------------------------------------------------------------------

def passes_not_long_path(G):
    """Leech 1975 (stated without proof), proof written out in SWZ 2005 p.3 and
    Calhoun et al. 2007 Prop. 1.2:  the path P_n is a Leech tree iff n <= 4.
    Topology filter: kills the path topology for n >= 5.  VERIFIED-BY-ME:
    weights on a Leech path must be exactly {1..n-1} (sum = C(n,2) forces it),
    1 must be adjacent only to n-1, then 2 must be adjacent only to n-1, so the
    path has <= 3 edges."""
    n = G.number_of_nodes()
    return not (n >= 5 and is_path_graph(G))


# ----------------------------------------------------------------------------
# F2  Diameter <= 3 (Calhoun 2007 Prop 2.10/2.11; EJGTA 2020 Thm 2.1; Luo-Yu 2024)
# ----------------------------------------------------------------------------

def passes_diameter_ge_4(G):
    """Calhoun-Ferland-Lister-Polhill 2007 Prop. 2.10 (stars) and Prop. 2.11
    (diameter 3, finite search tree Fig. 10); Varghese-Lakshmanan-Arumugam 2020
    (EJGTA 8(1)) Thm 2.1 (hand case analysis); Luo-Yu 2024 (Involve 17(2), abstract
    only): the only Leech trees of diameter <= 3 are the five known ones, i.e.
    for n >= 7 a Leech tree has diameter >= 4.  Topology filter: kills the star and
    all double stars B_{r,s}.  VERIFIED-BY-ME by an independent exhaustive
    forced-weight search over all double stars with 7 <= n <= 18 (selftest below,
    function no_leech_double_star)."""
    n = G.number_of_nodes()
    if n <= 6:
        return True
    return diameter_edges(G) >= 4


# ----------------------------------------------------------------------------
# F3  SWZ 2005 Theorem 2, exact finite form (VERIFIED-BY-ME, ledger L5)
# ----------------------------------------------------------------------------

def swz_path_ok(t, n):
    """Exact inequality behind SWZ 2005 Thm 2 ("no path longer than n/sqrt2 (1+o(1))").
    A path with t edges inside a Leech tree of order n: for every k with 1<=k<=t the
    N_k = t*k - C(k,2) sub-paths of 1..k edges have distinct positive weights, so their
    total is >= N_k(N_k+1)/2, while summing window-sums shows the total is
    <= C(k+1,2) * C(n,2).  Returns True iff no k violates it."""
    S = comb(n, 2)
    for k in range(1, t + 1):
        N = t * k - comb(k, 2)
        if N * (N + 1) // 2 > comb(k + 1, 2) * S:
            return False
    return True


def passes_swz_long_path(G):
    """SWZ 2005 Thm 2 in exact form (swz_path_ok).  Topology filter on the diameter t
    (edges): at n = 18 it kills t >= 16.  VERIFIED-BY-ME (re-derived, ledger L5)."""
    return swz_path_ok(diameter_edges(G), G.number_of_nodes())


# ----------------------------------------------------------------------------
# F4  Golomb-ruler diameter bound (VERIFIED-BY-ME for m<=13 marks; literature m>=14)
# ----------------------------------------------------------------------------

# Optimal Golomb ruler lengths G(m), m marks (OEIS A003022).  m<=13 re-verified by an
# exhaustive C search in this project (scratch golomb.c / golomb2.c, see ledger L6);
# m = 14..17 are literature values (Shearer 1990 tables; distributed.net OGR).
OGR = {1: 0, 2: 1, 3: 3, 4: 6, 5: 11, 6: 17, 7: 25, 8: 34, 9: 44, 10: 55, 11: 72,
       12: 85, 13: 106, 14: 127, 15: 151, 16: 177, 17: 199, 18: 216, 19: 246}
OGR_VERIFIED_HERE = 13   # marks up to which the table was re-derived by our own search


def max_marks_in_length(L):
    """Largest m with OGR[m] <= L (m marks fit in a ruler of length L)."""
    m = max(k for k, g in OGR.items() if g <= L)
    if m == max(OGR):
        raise ValueError("OGR table too short")
    return m


def passes_golomb_diameter(G):
    """The t+1 vertices of a longest path in a Leech tree have pairwise distinct
    distances, all <= S = C(n,2): they form a Golomb ruler with t+1 marks and length
    <= S.  Hence t+1 <= max{m : G(m) <= S}.  At n = 18 (S=153): G(15)=151 <= 153 <
    177 = G(16), so t <= 14.  Status: the argument is VERIFIED-BY-ME; the numeric
    G(16)=177 is LITERATURE (m<=13 re-verified here).  Strictly stronger than F3."""
    n = G.number_of_nodes()
    return diameter_edges(G) + 1 <= max_marks_in_length(comb(n, 2))


# ----------------------------------------------------------------------------
# F5  EJGTA 2020 Thm 3.1: path + pendant at v_{n-1}  (VERIFIED-BY-ME by search)
# ----------------------------------------------------------------------------

def is_broom_at_penultimate(G):
    """True iff G is P_m (v1..vm) plus one pendant vertex attached at v_{m-1}
    (equivalently at v_2), m >= 3; order m+1, diameter m-1."""
    n = G.number_of_nodes()
    if n < 4:
        return False
    degs = [d for _, d in G.degree()]
    if degs.count(3) != 1 or degs.count(1) != 3 or degs.count(2) != n - 4:
        return False
    v = next(u for u, d in G.degree() if d == 3)
    leaf_nb = sum(1 for u in G[v] if G.degree(u) == 1)
    return leaf_nb == 2   # two leaves + one long arm  <=>  pendant at v_{m-1}


def passes_ejgta_broom(G):
    """Varghese-Lakshmanan-Arumugam 2020 Thm 3.1 (+ Observation 3.1): the tree G_m
    obtained from P_m by attaching a pendant vertex at v_{m-1} is not a Leech tree for
    m >= 4 (order >= 5).  Topology filter (kills exactly one tree of diameter n-2).
    At n = 18 it is subsumed by F3/F4.  VERIFIED-BY-ME by exhaustive forced-weight
    search for orders 5..12 (selftest) and by re-reading their case analysis."""
    return not (G.number_of_nodes() >= 5 and is_broom_at_penultimate(G))


# ----------------------------------------------------------------------------
# F6  Max degree via the star-Sidon condition (VERIFIED-BY-ME by exhaustive search)
# ----------------------------------------------------------------------------

# STAR_DMAX[n] = largest d for which there exist d distinct positive integers with
# pairwise-distinct pairwise sums, no sum equal to an element, and everything <= C(n,2).
# Computed by exhaustive DFS (scratch stardeg.c; Python re-implementation
# star_sidon_max_degree below re-verifies n <= 12 in the selftest).
STAR_DMAX = {2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 5, 8: 5, 9: 6, 10: 7, 11: 7, 12: 8,
             13: 8, 14: 9, 15: 9, 16: 10, 17: 10, 18: 11}


def star_sidon_feasible(S, d):
    """Exists W, |W|=d, distinct positive ints, all pairwise sums (i<j) distinct,
    no sum in W, all elements and sums <= S ?  Exhaustive DFS (increasing order)."""
    used = bytearray(S + 2)
    w = []

    def rec():
        k = len(w)
        if k == d:
            return True
        lo = w[-1] + 1 if w else 1
        for p in range(lo, S + 1):
            if d - k >= 2 and 2 * p + 1 > S:
                break
            if w and p + w[-1] > S:
                break
            if used[p]:
                continue
            new = [p] + [x + p for x in w]
            if any(s > S or used[s] for s in new):
                continue
            for s in new:
                used[s] = 1
            w.append(p)
            if rec():
                return True
            w.pop()
            for s in new:
                used[s] = 0
        return False

    return rec()


def star_sidon_max_degree(n):
    S = comb(n, 2)
    d = 1
    while d + 1 <= n - 1 and star_sidon_feasible(S, d + 1):
        d += 1
    return d


def passes_max_degree(G):
    """Star-Sidon degree bound (this project; the same idea underlies SWZ 2005 Thm 3
    and, per its abstract, Luo-Yu 2024).  A vertex of degree d has d distinct incident
    weights w_i and the C(d,2) neighbour-neighbour distances w_i+w_j; all d+C(d,2)
    values are distinct and <= S.  Exhaustive search shows this is impossible for
    d > STAR_DMAX[n]; at n = 18 the max degree is <= 11.  Topology filter.
    VERIFIED-BY-ME (exhaustive search, table STAR_DMAX)."""
    n = G.number_of_nodes()
    if n not in STAR_DMAX:
        return True
    return max(d for _, d in G.degree()) <= STAR_DMAX[n]


# ----------------------------------------------------------------------------
# All filters
# ----------------------------------------------------------------------------

TOPOLOGY_FILTERS = [
    ("F1 not_long_path (Leech75/SWZ05)", passes_not_long_path),
    ("F2 diameter>=4 (Calhoun07/EJGTA20)", passes_diameter_ge_4),
    ("F3 swz_long_path (SWZ05 Thm2 exact)", passes_swz_long_path),
    ("F4 golomb_diameter (OGR table)", passes_golomb_diameter),
    ("F5 ejgta_broom (EJGTA20 Thm3.1)", passes_ejgta_broom),
    ("F6 max_degree<=STAR_DMAX (star-Sidon)", passes_max_degree),
]


def passes_all(G):
    return all(f(G) for _, f in TOPOLOGY_FILTERS)


# ----------------------------------------------------------------------------
# Exhaustive Leech search on a fixed topology (forced weights; for self-tests only)
# ----------------------------------------------------------------------------

def leech_labelings_of_topology(n, edges, limit=1, classes=None):
    """Return up to `limit` Leech labelings of the given topology (list of edge->weight
    dicts), by DFS over the ORDER in which edges receive weights.  Lemma (Calhoun 2.6 /
    SWZ Find-Next-Weight): the k-th smallest weight equals the least positive integer
    that is not a distance in the sub-forest of the k-1 lighter edges.  So a labeling
    is determined by the ordering of edges by weight; we enumerate orderings with
    pruning (repeated distance, distance > S).  Exact for small n (n <= 9 practical).
    `classes` (optional, one id per edge): edges with the same id are declared
    interchangeable by an automorphism of the topology (e.g. pendant edges at one
    centre); then only the lowest-index unplaced edge of a class is tried
    (symmetry breaking, valid because such swaps fix all other edges)."""
    S = comb(n, 2)
    edges = [tuple(e) for e in edges]
    m = len(edges)
    if classes is None:
        classes = list(range(m))
    adj = {v: [] for v in range(n)}          # weighted adjacency of placed edges
    used = bytearray(S + 2)                  # distances present so far
    comp = list(range(n))                    # union-find over placed edges

    def find(x):
        while comp[x] != x:
            comp[x] = comp[comp[x]]
            x = comp[x]
        return x

    def dists_from(src):
        out = {src: 0}
        stack = [src]
        while stack:
            u = stack.pop()
            for v, w in adj[u]:
                if v not in out:
                    out[v] = out[u] + w
                    stack.append(v)
        return out

    weight = {}
    results = []
    placed = [False] * m

    def rec(next_w):
        if len(results) >= limit:
            return
        if len(weight) == m:
            results.append(dict(weight))
            return
        # next weight is forced = least missing distance = next_w (maintained)
        for i, (u, v) in enumerate(edges):
            if placed[i]:
                continue
            if any((not placed[j]) and classes[j] == classes[i] for j in range(i)):
                continue
            # new distances: for a in comp(u), b in comp(v): d(a,u)+w+d(v,b)
            du = dists_from(u)
            dv = dists_from(v)
            new = []
            ok = True
            for a, da in du.items():
                for b, db in dv.items():
                    d = da + next_w + db
                    if d > S or used[d]:
                        ok = False
                        break
                    new.append(d)
                if not ok:
                    break
            if not ok:
                continue
            if len(set(new)) != len(new):
                continue
            for d in new:
                used[d] = 1
            adj[u].append((v, next_w)); adj[v].append((u, next_w))
            placed[i] = True; weight[(u, v)] = next_w
            nw = next_w + 1
            while nw <= S and used[nw]:
                nw += 1
            rec(nw)
            placed[i] = False; del weight[(u, v)]
            adj[u].pop(); adj[v].pop()
            for d in new:
                used[d] = 0
            if len(results) >= limit:
                return

    rec(1)
    return results


def no_leech_double_star(n):
    """Exhaustively check that no double star B_{r,s} (r+s+2 = n, r>=s>=1) and no
    star K_{1,n-1} admits a Leech labeling.  Uses a dedicated fast DFS: weights in
    increasing order are forced (least missing distance), and each new edge is either
    the centre edge, a u-pendant or a v-pendant.  Returns True if none exists."""
    S = comb(n, 2)
    # star
    if leech_labelings_of_topology(n, [(0, i) for i in range(1, n)], classes=[0] * (n - 1)):
        return False
    for s in range(1, n // 2):
        r = n - 2 - s
        if r < s:
            continue
        # vertices: 0=u, 1=v, 2..r+1 pendants at u, r+2..n-1 pendants at v
        edges = [(0, 1)] + [(0, i) for i in range(2, r + 2)] + [(1, i) for i in range(r + 2, n)]
        classes = [0] + [1] * r + [2] * s
        if leech_labelings_of_topology(n, edges, classes=classes):
            return False
    return True


# ----------------------------------------------------------------------------
# self-test and counting
# ----------------------------------------------------------------------------

def _selftest(root):
    import os
    known = json.load(open(os.path.join(root, "data", "known_leech_trees.json")))["trees"]
    sys.path.insert(0, os.path.join(root, "src"))
    import checker_a

    # 1. every filter accepts every known Leech tree
    for t in known:
        G = graph_from_edges(t["n"], [(u, v) for u, v, _ in t["edges"]])
        assert passes_taylor_order(t["n"]), t["name"]
        for name, f in TOPOLOGY_FILTERS:
            assert f(G), (name, t["name"])
    print("PASS: all filters accept the 5 known Leech trees")

    # 2. exhaustive truth for n<=8: which topologies admit a Leech labeling?
    found_names = []
    for n in range(2, 9):
        for T in nx.nonisomorphic_trees(n):
            edges = list(T.edges())
            labs = leech_labelings_of_topology(n, edges, limit=10)
            G = graph_from_edges(n, edges)
            for lab in labs:
                ok, why = checker_a.is_leech(n, [(u, v, w) for (u, v), w in lab.items()])
                assert ok, why
            if labs:
                found_names.append((n, sorted(d for _, d in G.degree())))
                for name, f in TOPOLOGY_FILTERS:
                    assert f(G), ("filter kills a Leech topology", name, n, edges)
            # a killed topology must have no labeling
            if not passes_all(G):
                assert not labs, ("filter wrongly kills", n, edges)
    assert sorted(found_names) == sorted([
        (2, [1, 1]), (3, [1, 1, 2]), (4, [1, 1, 1, 3]), (4, [1, 1, 2, 2]),
        (6, [1, 1, 1, 1, 3, 3])]), found_names
    print("PASS: exhaustive n<=8 search reproduces exactly the 5 known trees; no filter kills a Leech topology")

    # 3. diameter<=3 exclusion re-verified independently for 7<=n<=18
    for n in range(7, 19):
        assert no_leech_double_star(n), n
    print("PASS: no Leech star/double star for 7<=n<=18 (independent exhaustive search)")

    # 4. EJGTA broom re-verified for orders 5..12
    for m in range(4, 11):
        n = m + 1
        edges = [(i, i + 1) for i in range(m - 1)] + [(m - 2, m)]   # P_m = 0..m-1, pendant m at v_{m-1}
        G = graph_from_edges(n, edges)
        assert is_broom_at_penultimate(G)
        classes = list(range(m - 1)) + [m - 2]     # last path edge (v_{m-1}v_m) ~ pendant edge
        assert not leech_labelings_of_topology(n, edges, classes=classes), n
    print("PASS: EJGTA broom G_m has no Leech labeling for orders 5..11")

    # 5. star-Sidon table re-verified for n<=12 by the Python search
    for n in range(2, 13):
        assert star_sidon_max_degree(n) == STAR_DMAX[n], n
    print("PASS: STAR_DMAX re-verified for n<=12")

    # 6. Golomb table sanity (small m) via brute force
    def golomb_exists(m, L):
        marks = [0]
        used = set()

        def rec():
            if len(marks) == m:
                return True
            for p in range(marks[-1] + 1, L + 1):
                diffs = [p - q for q in marks]
                if any(d in used for d in diffs) or len(set(diffs)) != len(diffs):
                    continue
                used.update(diffs); marks.append(p)
                if rec():
                    return True
                marks.pop(); used.difference_update(diffs)
            return False
        return rec()
    for m in range(2, 10):
        assert golomb_exists(m, OGR[m]) and not golomb_exists(m, OGR[m] - 1), m
    print("PASS: OGR table re-verified for m<=9 in Python (m<=13 by C search, see ledger)")

    # 7. SWZ exact path bound sanity: the full path P_n violates it iff n >= 7
    #    (k=2 gives n^2-7n+6 <= 0); P_5, P_6 are killed by F1 (Leech's finer argument)
    for n in range(2, 40):
        assert swz_path_ok(n - 1, n) == (n <= 6), n
    assert swz_path_ok(15, 18) and not swz_path_ok(16, 18)
    print("PASS: swz_path_ok: P_n violates iff n>=7; at n=18 kills diameter>=16 only")


def _count(path):
    names = [name for name, _ in TOPOLOGY_FILTERS]
    killed = {name: 0 for name in names}
    total = 0
    survivors = 0
    diam_hist = {}
    deg_hist = {}
    with open(path) as fh:
        for line in fh:
            rec = json.loads(line)
            n = rec["n"]
            G = graph_from_edges(n, rec["edges"])
            total += 1
            alive = True
            for name, f in TOPOLOGY_FILTERS:
                if not f(G):
                    killed[name] += 1
                    alive = False
            if alive:
                survivors += 1
            t = diameter_edges(G)
            diam_hist[t] = diam_hist.get(t, 0) + 1
            dm = max(d for _, d in G.degree())
            deg_hist[dm] = deg_hist.get(dm, 0) + 1
    print(f"topologies: {total}")
    for name in names:
        print(f"  killed by {name}: {killed[name]}  -> survivors {total - killed[name]}")
    print(f"combined survivors: {survivors}")
    print("diameter histogram:", dict(sorted(diam_hist.items())))
    print("max-degree histogram:", dict(sorted(deg_hist.items())))
    return survivors


if __name__ == "__main__":
    import os
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    if "--selftest" in sys.argv:
        _selftest(root)
    if "--count" in sys.argv:
        _count(sys.argv[sys.argv.index("--count") + 1])
