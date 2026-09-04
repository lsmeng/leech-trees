#!/usr/bin/env python3
"""Theory branch: machine checks for docs/theory-notes.md and topology filters for n=18.

Usage:
  .venv/bin/python src/theory_checks.py test            # brute-force checks of every lemma (n<=8 + random)
  .venv/bin/python src/theory_checks.py filter18 [-j J] # apply topology filters to data/trees_18.jsonl,
                                                        # write results/theory_survivors_18.txt
  .venv/bin/python src/theory_checks.py filter N        # same for data/trees_N.jsonl (report only)

Everything here is pure necessary-condition logic; a topology is "killed" only if a proven lemma
(see docs/theory-notes.md, same numbering) shows no Leech weighting exists on it.
"""
import sys, os, json, math, random, itertools, time
from math import comb
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# ----------------------------------------------------------------------------------------------
# Optimal Golomb ruler lengths G[m] for m marks (m=1..27).  Values 1..8 are re-derived below by
# brute force (test_ogr); the rest are the standard published table (Shearer / distributed.net).
# ----------------------------------------------------------------------------------------------
OGR = {1: 0, 2: 1, 3: 3, 4: 6, 5: 11, 6: 17, 7: 25, 8: 34, 9: 44, 10: 55, 11: 72, 12: 85, 13: 106,
       14: 127, 15: 151, 16: 177, 17: 199, 18: 216, 19: 246, 20: 283, 21: 333, 22: 356, 23: 372,
       24: 425, 25: 480, 26: 492, 27: 553}


def ogr_bruteforce(m):
    """Length of the optimal Golomb ruler with m marks by branch-and-bound (m<=8 in seconds)."""
    best = [None]
    L = OGR[m] - 1 if m in OGR else 10 * m * m
    # search rulers of length <= L; increase L until found -> optimum. Start from a safe lower bound.
    lo = comb(m, 2)  # need C(m,2) distinct positive differences
    for length in range(lo, 10 * m * m):
        # DFS marks 0 = a0 < a1 < ... < a_{m-1} = length
        marks = [0]
        used = set()

        def dfs():
            if len(marks) == m - 1:
                # last mark = length
                diffs = [length - a for a in marks]
                if len(set(diffs)) == len(diffs) and not (set(diffs) & used):
                    return True
                return False
            k = len(marks)
            for a in range(marks[-1] + 1, length):
                # remaining marks must fit: need (m-1-k) more marks strictly increasing before length
                if a + (m - 1 - k) > length:
                    break
                diffs = [a - b for b in marks]
                if len(set(diffs)) != len(diffs) or (set(diffs) & used):
                    continue
                marks.append(a); used.update(diffs)
                if dfs():
                    return True
                marks.pop(); used.difference_update(diffs)
            return False
        if m == 2:
            return 1
        if dfs():
            return length
    return None


# ----------------------------------------------------------------------------------------------
# tree utilities
# ----------------------------------------------------------------------------------------------
class Tree:
    def __init__(self, n, edges):
        self.n = n
        self.edges = [tuple(e) for e in edges]
        assert len(self.edges) == n - 1
        self.adj = [[] for _ in range(n)]
        for i, (u, v) in enumerate(self.edges):
            self.adj[u].append((v, i)); self.adj[v].append((u, i))
        self.deg = [len(a) for a in self.adj]
        # root at 0, parent edge, order
        self.parent = [-1] * n; self.pedge = [-1] * n; self.depth = [0] * n
        order = [0]; seen = [False] * n; seen[0] = True
        for u in order:
            for v, i in self.adj[u]:
                if not seen[v]:
                    seen[v] = True; self.parent[v] = u; self.pedge[v] = i; self.depth[v] = self.depth[u] + 1
                    order.append(v)
        self.order = order
        # subtree sizes -> cut sizes s_e (size of the side not containing root)
        sub = [1] * n
        for v in reversed(order[1:]):
            sub[self.parent[v]] += sub[v]
        self.sub = sub
        self.s = [0] * (n - 1)
        for v in order[1:]:
            self.s[self.pedge[v]] = sub[v]
        self.c = [se * (n - se) for se in self.s]          # c_e = number of pairs whose path uses e
        # pairs and path-edge incidence
        self.pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        self.N = len(self.pairs)
        self.pathedges = {}
        for (u, v) in self.pairs:
            self.pathedges[(u, v)] = self.path_edges(u, v)
        self.hop = {p: len(es) for p, es in self.pathedges.items()}
        self.side_of = None

    def path_edges(self, u, v):
        es = []
        a, b = u, v
        while a != b:
            if self.depth[a] < self.depth[b]:
                a, b = b, a
            es.append(self.pedge[a]); a = self.parent[a]
        return es

    def lca(self, u, v):
        a, b = u, v
        while a != b:
            if self.depth[a] < self.depth[b]:
                a, b = b, a
            a = self.parent[a]
        return a

    def dist(self, w, u, v):
        return sum(w[e] for e in self.pathedges[(u, v)] if True) if u < v else self.dist(w, v, u)

    def all_dists(self, w):
        return {p: sum(w[e] for e in es) for p, es in self.pathedges.items()}

    def cef(self):
        """c_ef = number of pairs whose path contains both e and f (e != f) = a*b where a,b are the
        sizes of the two 'outer' components after deleting e and f."""
        m = self.n - 1
        C = [[0] * m for _ in range(m)]
        for es in self.pathedges.values():
            for i in range(len(es)):
                for j in range(i + 1, len(es)):
                    C[es[i]][es[j]] += 1; C[es[j]][es[i]] += 1
        return C

    def cef_formula(self, e, f):
        """a*b via component sizes: delete e and f -> three components; the two not between them."""
        # component sizes: for edge e = parent edge of x_e (root side / subtree side)
        xe = next(v for v in range(self.n) if self.pedge[v] == e)
        xf = next(v for v in range(self.n) if self.pedge[v] == f)
        # is xf inside subtree(xe)?
        def inside(a, b):  # b in subtree of a
            while b != -1:
                if b == a:
                    return True
                b = self.parent[b]
            return False
        if inside(xe, xf):
            return (self.n - self.sub[xe]) * self.sub[xf]
        if inside(xf, xe):
            return (self.n - self.sub[xf]) * self.sub[xe]
        return self.sub[xe] * self.sub[xf]

    def hop_diameter(self):
        return max(self.hop.values())

    def leaves(self):
        return [v for v in range(self.n) if self.deg[v] == 1]


def load_trees(n, limit=None):
    path = os.path.join(ROOT, 'data', f'trees_{n}.jsonl')
    out = []
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                r = json.loads(line); out.append((r['id'], r['edges']))
                if limit and len(out) >= limit:
                    break
    else:
        import networkx as nx
        for i, g in enumerate(nx.nonisomorphic_trees(n)):
            out.append((i, [list(e) for e in g.edges()]))
    return out


# ----------------------------------------------------------------------------------------------
# exhaustive Leech / distinct-distance enumeration (small n)
# ----------------------------------------------------------------------------------------------
def enumerate_leech(T, maxw=None):
    """All weightings (weights distinct positive integers <= N) with distances exactly {1..N}."""
    n, N = T.n, T.N
    maxw = maxw or N
    order = T.order
    w = [0] * (n - 1)
    dist = [[0] * n for _ in range(n)]
    used = 0
    results = []
    placed = [order[0]]

    def rec(k):
        nonlocal used
        if k == n:
            if used == (1 << (N + 1)) - 2:
                results.append(list(w))
            return
        v = order[k]; p = T.parent[v]; e = T.pedge[v]
        for wt in range(1, maxw + 1):
            new = []
            ok = True
            m = used
            for x in placed:
                d = dist[p][x] + wt
                if d > N or (m >> d) & 1:
                    ok = False; break
                m |= 1 << d; new.append((x, d))
            if not ok:
                continue
            w[e] = wt; used = m
            for x, d in new:
                dist[v][x] = dist[x][v] = d
            placed.append(v)
            rec(k + 1)
            placed.pop()
            used = m
            for x, d in new:
                used &= ~(1 << d)
        return
    rec(1)
    return results


def random_weighted_tree(n, rng, wmax=None, distinct_dists=False):
    import networkx as nx
    while True:
        g = nx.random_labeled_tree(n, seed=rng.randrange(1 << 30)) if hasattr(nx, 'random_labeled_tree') \
            else nx.random_tree(n, seed=rng.randrange(1 << 30))
        T = Tree(n, list(g.edges()))
        wmax_ = wmax or 4 * n * n
        w = [rng.randint(1, wmax_) for _ in range(n - 1)]
        if distinct_dists:
            D = T.all_dists(w)
            if len(set(D.values())) != T.N:
                continue
        return T, w


# ----------------------------------------------------------------------------------------------
# Lemma implementations (numbering as in docs/theory-notes.md)
# ----------------------------------------------------------------------------------------------
def moment_sums(T, w):
    """(sum d, sum d^2, sum d^3) over pairs, computed from the distances directly."""
    D = list(T.all_dists(w).values())
    return sum(D), sum(x * x for x in D), sum(x ** 3 for x in D)


def moment_sums_cut(T, w):
    """Lemma 1/2: same via cut structure: S1 = sum c_e w_e ; S2 = sum c_e w_e^2 + 2 sum_{e<f} c_ef w_e w_f."""
    m = T.n - 1
    S1 = sum(T.c[e] * w[e] for e in range(m))
    C = T.cef()
    S2 = sum(T.c[e] * w[e] ** 2 for e in range(m)) + 2 * sum(C[e][f] * w[e] * w[f] for e in range(m) for f in range(e + 1, m))
    return S1, S2


def bfs_parents(T, root):
    par = [-1] * T.n; par[root] = root
    stack = [root]
    while stack:
        u = stack.pop()
        for x, _ in T.adj[u]:
            if par[x] == -1:
                par[x] = u; stack.append(x)
    return par


def sidon_ok(vals):
    sums = [a + b for a, b in itertools.combinations(vals, 2)]
    return len(set(sums)) == len(sums)


def max_sidon_in(N):
    """Largest k such that a Sidon set of size k fits in [1,N] (k marks Golomb ruler of length <= N-1)."""
    k = 1
    while (k + 1) in OGR and OGR[k + 1] <= N - 1:
        k += 1
    return k


def mod4_label_counts(T, w):
    """Lemma 6: residues of d(u,v) mod 4 from phi(v)=depth mod 4 and parity of phi(lca)."""
    n = T.n
    phi = [0] * n
    for v in T.order[1:]:
        phi[v] = (phi[T.parent[v]] + w[T.pedge[v]]) % 4
    cnt = [0] * 4
    for (u, v) in T.pairs:
        m = T.lca(u, v)
        r = (phi[u] + phi[v] - 2 * (phi[m] % 2)) % 4
        cnt[r] += 1
    return cnt


def residue_counts_target(N, mod):
    return [len([k for k in range(1, N + 1) if k % mod == r]) for r in range(mod)]


# ---- Filter F1: Golomb hop bound ---------------------------------------------------------------
def filter_golomb(T):
    """Every path with k edges is a Golomb ruler with k+1 marks and length <= N. Kill if OGR(k+1) > N."""
    D = T.hop_diameter()
    return OGR.get(D + 1, 10 ** 9) <= T.N


# ---- Filter F2: Sidon degree bound --------------------------------------------------------------
# STAR_MIN[d] = minimum possible a_{d-1}+a_d over sets {a_1<...<a_d} of positive integers whose C(d,2)
# pairwise sums are distinct and avoid the set ("star-Sidon", the exact structure of the incident weights at
# a vertex).  Values d<=9 re-derived by star_min_bruteforce in test_sidon; d=10..12 from the referee's
# exact search (also reproduced by the same routine, slower).  NOTE: NOT the Golomb/OGR bound (a weak
# Sidon set may contain 3-term APs, e.g. {1,2,4,8,14,19,24}).
STAR_MIN = {2: 3, 3: 6, 4: 11, 5: 19, 6: 31, 7: 43, 8: 63, 9: 80, 10: 110, 11: 138, 12: 169}


def star_min_bruteforce(d):
    """Exact minimum of a_{d-1}+a_d over star-Sidon sets of size d (branch and bound)."""
    best = [10 ** 9]

    def dfs(A, sums):
        k = len(A)
        if k == d:
            best[0] = min(best[0], A[-1] + A[-2]); return
        a = A[-1] + 1 if A else 1
        while True:
            if k <= d - 2 and 2 * a + 2 * d - 3 - 2 * k >= best[0]:
                break
            if k == d - 1 and a + A[-1] >= best[0]:
                break
            ns = [a + b for b in A]
            ok = len(set(ns)) == len(ns) and not (set(ns) & sums)
            ok = ok and not (set(ns) & set(A)) and a not in sums
            if ok:
                dfs(A + [a], sums | set(ns))
            a += 1
    dfs([], set())
    return best[0]


def max_degree_bound(N):
    """Lemma 5(b): a vertex of degree d has incident weights forming a star-Sidon set whose top-two sum is
    a distance <= N, so STAR_MIN[d] <= N.  Largest d passing (d beyond the table: unbounded/unknown)."""
    d = 2
    while (d + 1) in STAR_MIN and STAR_MIN[d + 1] <= N:
        d += 1
    return d if d < max(STAR_MIN) else 10 ** 9


def filter_degree(T):
    """Lemma 5(b) with the containment refinement: at a vertex v of degree d with branch sizes b_i,
    STAR_MIN[d] <= N+1-b_(1)*b_(2) (two smallest branch sizes)."""
    n, N = T.n, T.N
    for v in range(n):
        d = T.deg[v]
        if d < 3:
            continue
        d = min(d, max(STAR_MIN))   # S(d) is non-decreasing (drop the largest element), so S(d) >= S(12) for d > 12
        sizes = []
        for x, e in T.adj[v]:
            sizes.append(T.sub[x] if T.parent[x] == v else n - T.sub[v])
        sizes.sort()
        if STAR_MIN[d] > N + 1 - sizes[0] * sizes[1]:
            return False
    return True


# ---- Filter F3: projection (real second-moment) bound -----------------------------------------
def incidence(T):
    import numpy as np
    A = np.zeros((T.N, T.n - 1))
    for i, p in enumerate(T.pairs):
        for e in T.pathedges[p]:
            A[i, e] = 1.0
    return A


def filter_projection(T):
    """min over real w with 1'Aw = M1 of ||Aw||^2  =  M1^2 / ||P_A 1||^2 ; kill if > M2."""
    import numpy as np
    A = incidence(T)
    N = T.N
    M1 = N * (N + 1) / 2; M2 = N * (N + 1) * (2 * N + 1) / 6
    one = np.ones(N)
    coef, *_ = np.linalg.lstsq(A, one, rcond=None)
    proj = A @ coef
    val = M1 ** 2 / float(proj @ proj)
    return val <= M2 * (1 + 1e-9), val / M2


# ---- Filter F4: majorization QP/LP (permutahedron + Golomb + containment bounds) ---------------
def containment_upper(T):
    """Lemma 4(d): d(x,y) <= N + 1 - s_x*s_y where s_x (s_y) is the number of vertices on x's (y's)
    side of the first (last) edge of the x-y path; s_x*s_y = #pairs whose path contains path(x,y)."""
    n = T.n
    ub = []
    for (u, v) in T.pairs:
        es = T.pathedges[(u, v)]
        # side sizes: for edge e = pedge[z] with s[e]=sub[z]; u's side is sub-side iff u is in subtree(z)
        def side(vertex, e):
            z = next(q for q in range(n) if T.pedge[q] == e)
            # is vertex inside subtree(z)?
            q = vertex
            while q != -1 and q != z:
                q = T.parent[q]
            return T.sub[z] if q == z else n - T.sub[z]
        # first edge on u's end: the edge incident to u on the path
        eu = next(e for e in es if u in T.edges[e]); ev = next(e for e in es if v in T.edges[e])
        su, sv = side(u, eu), side(v, ev)
        ub.append(T.N + 1 - su * sv)
    return ub


def lp_constraint_data(T):
    """Common data for the relaxation: A (pairs x edges), per-pair lower bounds (Golomb) and upper
    bounds (containment), sum M1, top-s bounds."""
    import numpy as np
    A = incidence(T)
    N = T.N
    hop = np.array([T.hop[p] for p in T.pairs])
    lb = np.array([OGR[h + 1] for h in hop], dtype=float)
    ub = np.array(containment_upper(T), dtype=float)
    top = np.array([sum(range(N, N - s, -1)) for s in range(N + 1)], dtype=float)
    return A, hop, lb, ub, top


def filter_lp(T, tol=1e-7, max_iter=300):
    """scipy/HiGHS LP cutting planes on the same constraint set (independent solver; used in tests)."""
    import numpy as np
    from scipy.optimize import linprog
    A, hop, lb, ub, top = lp_constraint_data(T)
    N, m = T.N, T.n - 1
    A_eq = np.ones((1, N)) @ A; b_eq = [N * (N + 1) / 2]
    A_ub = [-A, A]; b_ub = [-lb, ub]
    for k in range(1, int(hop.max()) + 1):
        S = (hop >= k).astype(float); s = int(S.sum())
        if 0 < s < N:
            A_ub.append((S @ A)[None, :]); b_ub.append(np.array([top[s]]))
        S = (hop <= k).astype(float); s = int(S.sum())
        if 0 < s < N:
            A_ub.append((-S @ A)[None, :]); b_ub.append(np.array([-s * (s + 1) / 2]))
    cuts = 0
    for it in range(max_iter):
        res = linprog(np.zeros(m), A_ub=np.vstack(A_ub), b_ub=np.concatenate(b_ub), A_eq=A_eq, b_eq=b_eq,
                      bounds=[(1, N)] * m, method='highs')
        if res.status == 2:
            return False, it, cuts
        if res.status != 0:
            return True, it, cuts
        d = A @ res.x
        idx = np.argsort(-d); cs = np.cumsum(d[idx])
        viol = [s for s in range(1, N) if cs[s - 1] > top[s] + tol]
        if not viol:
            return True, it, cuts
        for s in viol:
            row = np.zeros(N); row[idx[:s]] = 1.0
            A_ub.append((row @ A)[None, :]); b_ub.append(np.array([top[s]])); cuts += 1
    return True, max_iter, cuts


def filter_qp(T, tol=1e-6, max_iter=100, extra_rows=None, return_w=False):
    """Feasibility of the convex relaxation
         w in [1,N]^m,  d = A w,  OGR(hop_P+1) <= d_P <= N+1-s_x s_y,  sum d = M1,  d majorized by (1..N)
    solved by minimising sum d_P^2 (HiGHS QP) with cutting planes for the majorization constraints.
    Early exit: min sum d^2 > M2 => infeasible (Karamata: any majorized d has sum d^2 <= M2).
    Returns (survives, iterations, cuts, status[, w])."""
    import numpy as np, highspy
    A, hop, lb, ub, top = lp_constraint_data(T)
    N, m = T.N, T.n - 1
    M1 = N * (N + 1) / 2; M2 = N * (N + 1) * (2 * N + 1) / 6
    Q = A.T @ A
    h = highspy.Highs(); h.silent()
    inf = highspy.kHighsInf
    h.addVars(m, np.ones(m), np.full(m, float(N)))
    Qh = 2 * Q
    rows, cols, vals = [], [], []
    for j in range(m):
        for i in range(j, m):
            rows.append(i); vals.append(Qh[i, j])
    start = np.zeros(m + 1, dtype=np.int32)
    for j in range(m):
        start[j + 1] = start[j] + (m - j)
    h.passHessian(m, len(vals), highspy.HessianFormat.kTriangular, start, np.array(rows, dtype=np.int32),
                  np.array(vals))
    h.changeObjectiveSense(highspy.ObjSense.kMinimize)

    def addrow(coef, lo, hi):
        idx = np.nonzero(np.abs(coef) > 1e-12)[0]
        h.addRow(lo, hi, len(idx), idx.astype(np.int32), coef[idx])
    addrow(np.ones(N) @ A, M1, M1)
    for i in range(N):
        addrow(A[i], lb[i], ub[i])
    for k in range(1, int(hop.max()) + 1):
        S = (hop >= k).astype(float); s = int(S.sum())
        if 0 < s < N:
            addrow(S @ A, -inf, top[s])
        S = (hop <= k).astype(float); s = int(S.sum())
        if 0 < s < N:
            addrow(S @ A, s * (s + 1) / 2, inf)
    if extra_rows:
        for coef, lo, hi in extra_rows:
            addrow(coef, lo, hi)
    cuts = 0
    for it in range(max_iter):
        h.run()
        st = h.getModelStatus()
        if st == highspy.HighsModelStatus.kInfeasible:
            return (False, it, cuts, 'infeasible') + ((None,) if return_w else ())
        if st != highspy.HighsModelStatus.kOptimal:
            ok = filter_lp(T)[0]      # solver trouble: fall back to the independent LP formulation
            return (ok, it, cuts, 'status:' + str(st) + '->lp:' + str(ok)) + ((None,) if return_w else ())
        val = h.getInfo().objective_function_value
        if val > M2 * (1 + 1e-9):
            return (False, it, cuts, 'obj>M2') + ((None,) if return_w else ())
        w = np.array(h.getSolution().col_value)
        d = A @ w
        idx = np.argsort(-d); cs = np.cumsum(d[idx])
        viol = [s for s in range(1, N) if cs[s - 1] > top[s] + tol]
        if not viol:
            return (True, it, cuts, 'feasible') + ((w,) if return_w else ())
        for s in viol:
            row = np.zeros(N); row[idx[:s]] = 1.0
            addrow(row @ A, -inf, top[s]); cuts += 1
    return (True, max_iter, cuts, 'maxiter') + ((None,) if return_w else ())


def filter_qp_diam(T):
    """Disjunctive strengthening (Lemma 4): some leaf pair (u,v) has d=N; then every pair disjoint
    from {u,v} has d <= N-3.  Topology survives iff the QP is feasible for at least one leaf pair."""
    import numpy as np
    A, hop, lb, ub, top = lp_constraint_data(T)
    N = T.N
    leaves = T.leaves()
    pidx = {p: i for i, p in enumerate(T.pairs)}
    for i in range(len(leaves)):
        for j in range(i + 1, len(leaves)):
            u, v = leaves[i], leaves[j]
            if OGR[T.hop[(u, v)] + 1] > N:
                continue
            rows = []
            r = np.zeros(N); r[pidx[(u, v)]] = 1.0
            rows.append((r @ A, float(N), float(N)))
            far = np.array([1.0 if (u not in p and v not in p) else 0.0 for p in T.pairs])
            for k, p in enumerate(T.pairs):
                if far[k]:
                    r = np.zeros(N); r[k] = 1.0
                    rows.append((r @ A, -np.inf, float(N - 3)))
            ok = filter_qp(T, extra_rows=rows)[0]
            if ok:
                return True
    return False


# ---- Filter F5: top-value / low-degree pair count -----------------------------------------
def filter_topvalues(T):
    """Lemma 4(c): for every m>=1, #{pairs {x,y}: deg x <= m and deg y <= m} >= m."""
    n = T.n
    for mdeg in range(1, n):
        low = [v for v in range(n) if T.deg[v] <= mdeg]
        if comb(len(low), 2) < mdeg:
            return False
        if len(low) == n:
            break
    return True


FILTERS = [('F1_golomb_diam', filter_golomb), ('F2_sidon_degree', filter_degree),
           ('F5_topvalue_pairs', filter_topvalues),
           ('F3_projection', lambda T: filter_projection(T)[0]), ('F4_relaxation_QP', lambda T: filter_qp(T)[0]),
           ('F6_diam_disjunction', filter_qp_diam)]


# ----------------------------------------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------------------------------------
def known_trees():
    data = json.load(open(os.path.join(ROOT, 'data', 'known_leech_trees.json')))
    out = []
    for t in data['trees']:
        edges = [(u, v) for u, v, w in t['edges']]
        T = Tree(t['n'], edges)
        w = [w for u, v, w in t['edges']]
        out.append((t['name'], T, w))
    return out


def test_ogr():
    for mk in range(2, 9):
        got = ogr_bruteforce(mk)
        assert got == OGR[mk], (mk, got, OGR[mk])
    print("PASS OGR table re-derived by brute force for 2..8 marks:", {k: OGR[k] for k in range(2, 9)})


def test_moments(rng):
    for name, T, w in known_trees():
        S1, S2, S3 = moment_sums(T, w)
        N = T.N
        assert S1 == N * (N + 1) // 2 and S2 == N * (N + 1) * (2 * N + 1) // 6 and S3 == (N * (N + 1) // 2) ** 2
        c1, c2 = moment_sums_cut(T, w)
        assert (c1, c2) == (S1, S2), name
    for _ in range(300):
        n = rng.randint(3, 12)
        T, w = random_weighted_tree(n, rng)
        S1, S2, _ = moment_sums(T, w)
        assert moment_sums_cut(T, w) == (S1, S2)
        C = T.cef()
        for e in range(n - 1):
            for f in range(e + 1, n - 1):
                assert C[e][f] == T.cef_formula(e, f), (n, e, f)
    print("PASS Lemma 1-2 (cut identities, c_ef = a*b) on known trees + 300 random weighted trees")


def test_exhaustive_small():
    """n<=7 exhaustive: recover exactly the five known Leech trees; none at n=5,7. n=8 with cap."""
    found = {}
    for n in range(2, 8):
        cnt = 0
        for tid, edges in load_trees(n):
            T = Tree(n, edges)
            sols = enumerate_leech(T)
            if sols:
                found[(n, tid)] = (T, sols); cnt += len(sols)
        print(f"  n={n}: Leech weightings found (labeled, over frozen topologies): {cnt}")
    ns = sorted(set(k[0] for k in found))
    assert ns == [2, 3, 4, 6], ns
    assert len([k for k in found if k[0] == 4]) == 2
    print("PASS exhaustive n<=7 reproduces Leech's classification (n in {2,3,4,4,6}), none at 5,7")
    return found


def test_golomb_lemma(found, rng):
    # every path in every Leech tree is a Golomb ruler; hop-diameter bound holds
    for (n, tid), (T, sols) in found.items():
        for w in sols:
            D = T.all_dists(w)
            for (u, v) in T.pairs:
                es = T.pathedges[(u, v)]
                # sub-path sums along the path are all distinct (they are distances of distinct pairs)
                assert filter_golomb(T)
    # random distinct-distance trees: every path is a Golomb ruler with length >= OGR(k+1)
    for _ in range(300):
        T, w = random_weighted_tree(rng.randint(3, 9), rng, distinct_dists=True)
        D = T.all_dists(w)
        for p, es in T.pathedges.items():
            assert D[p] >= OGR[len(es) + 1]
    print("PASS Lemma 3 (Golomb): sub-path sums distinct, d_P >= OGR(hop+1) on Leech + 300 random distinct-distance trees")


def test_topvalues(found, rng):
    def check(T, w):
        D = T.all_dists(w)
        ranked = sorted(D.items(), key=lambda kv: -kv[1])
        (p0, d0), (p1, d1) = ranked[0], ranked[1]
        assert T.deg[p0[0]] == 1 and T.deg[p0[1]] == 1          # (a) max is leaf-leaf
        assert set(p0) & set(p1)                                # (b) top two share an endpoint
        for j, (p, d) in enumerate(ranked):
            assert T.deg[p[0]] <= j + 1 and T.deg[p[1]] <= j + 1  # (c) rank-j pair has degrees <= j+1
            if j > 6:
                break
        # (b') second largest: other endpoint is a leaf, or has degree 2 and is adjacent to the far
        # leaf of p0 through an edge of weight d0-d1
        common = (set(p0) & set(p1)).pop()
        y = [x for x in p1 if x != common][0]; v = [x for x in p0 if x != common][0]
        if T.deg[y] != 1:
            assert T.deg[y] == 2 and (min(y, v), max(y, v)) in T.pathedges and T.hop[(min(y, v), max(y, v))] == 1
            assert D[(min(y, v), max(y, v))] == d0 - d1
        assert filter_topvalues(T)
    for (n, tid), (T, sols) in found.items():
        for w in sols:
            if n >= 3:
                check(T, w)
    for _ in range(500):
        T, w = random_weighted_tree(rng.randint(3, 10), rng, distinct_dists=True)
        check(T, w)
    print("PASS Lemma 4 (top values): max is leaf-leaf, top-2 share endpoint, rank-j degree bound, deg-2 case; 500 random")


def test_sidon(found, rng):
    def check(T, w):
        D = T.all_dists(w)
        for v in range(T.n):
            # distances from v, one representative per branch (any choice) form a Sidon set
            branches = defaultdict(list)
            par = bfs_parents(T, v)
            for x in range(T.n):
                if x == v:
                    continue
                y = x
                while par[y] != v:
                    y = par[y]
                branches[y].append(D[(min(v, x), max(v, x))])
            for _ in range(3):
                reps = [rng.choice(b) for b in branches.values()]
                assert sidon_ok(reps), (v, reps)
                assert not (set(reps) & set(a + b for a, b in itertools.combinations(reps, 2)))
        assert max(T.deg) <= max_sidon_in(max(D.values()))
        assert max(T.deg) <= max_degree_bound(max(D.values()))
        # Lemma 5(b) inequality directly: incident weights Sidon, top-two sum is a distance <= max distance
        for v in range(T.n):
            if T.deg[v] >= 2:
                a = sorted(w[e] for _, e in T.adj[v])
                assert sidon_ok(a) and a[-1] + a[-2] <= max(D.values())
                assert not (set(a) & set(x + y for x, y in itertools.combinations(a, 2)))
                assert len(a) not in STAR_MIN or a[-1] + a[-2] >= STAR_MIN[len(a)]
    for (n, tid), (T, sols) in found.items():
        for w in sols:
            check(T, w)
    for _ in range(300):
        T, w = random_weighted_tree(rng.randint(3, 10), rng, distinct_dists=True)
        check(T, w)
    for d_ in range(2, 9):
        assert star_min_bruteforce(d_) == STAR_MIN[d_], d_
    # the referee's counterexample to the (withdrawn) OGR form: weak Sidon, contains a 3-term AP
    assert sidon_ok([1, 2, 4, 8, 14, 19, 24]) and 19 + 24 < OGR[7] + OGR[6] + 2
    print("PASS star-Sidon minima re-derived for d=2..8:", {d_: STAR_MIN[d_] for d_ in range(2, 9)})
    print("PASS Lemma 5 (branch Sidon): per-vertex cross-branch representatives Sidon & sum-free; deg <= maxSidon(N)")


def test_mod4(found, rng):
    for (n, tid), (T, sols) in found.items():
        for w in sols:
            assert mod4_label_counts(T, w) == residue_counts_target(T.N, 4)
    for _ in range(300):
        T, w = random_weighted_tree(rng.randint(3, 10), rng)
        D = T.all_dists(w)
        direct = [0] * 4
        for d in D.values():
            direct[d % 4] += 1
        assert mod4_label_counts(T, w) == direct
        # Taylor parity as corollary: #odd = a(n-a)
        a = sum(1 for v in range(1, T.n) if sum(w[e] for e in T.pathedges[(0, v)]) % 2 == 1)
        assert direct[1] + direct[3] == a * (T.n - a)
    print("PASS Lemma 6 (mod 4 residue formula; Taylor parity as corollary) on Leech + 300 random")


def test_lp_and_projection(found, rng):
    import numpy as np
    # (i) exact Leech weights satisfy every row of the relaxation (Golomb lb, containment ub, sum, top-s)
    for (n, tid), (T, sols) in found.items():
        A, hop, lb, ub, top = lp_constraint_data(T)
        N = T.N
        for w in sols:
            d = A @ np.array(w, float)
            assert np.all(d >= lb - 1e-9) and np.all(d <= ub + 1e-9), (n, tid, w)
            assert abs(d.sum() - N * (N + 1) / 2) < 1e-9
            ds = np.sort(d)[::-1]
            assert all(ds[:s_].sum() <= top[s_] + 1e-9 for s_ in range(1, N + 1))
        assert filter_projection(T)[0], (n, tid)
        assert filter_lp(T)[0], (n, tid)
        assert filter_qp(T)[0], (n, tid)
        assert filter_qp_diam(T), (n, tid)
    # (ii) containment bound & Golomb bound on random distinct-distance trees (weight-level statement)
    for _ in range(300):
        T, w = random_weighted_tree(rng.randint(3, 10), rng, distinct_dists=True)
        D = T.all_dists(w)
        vals = sorted(D.values())
        rank = {v: i + 1 for i, v in enumerate(vals)}   # rank within the distinct multiset
        ub = containment_upper(T)
        for i, p in enumerate(T.pairs):
            assert rank[D[p]] <= ub[i]                    # rank <= N+1 - s_x s_y
            assert rank[D[p]] >= comb(T.hop[p] + 1, 2)     # poset lower bound (weaker than Golomb)
    # (iii) majorization separation oracle vs brute-force definition
    for _ in range(200):
        N = rng.randint(3, 15)
        v = np.arange(1, N + 1, dtype=float)
        d = np.random.default_rng(rng.randrange(1 << 30)).random(N) * N
        d *= v.sum() / d.sum()
        ds = np.sort(d)[::-1]
        maj = all(ds[:s].sum() <= v[::-1][:s].sum() + 1e-9 for s in range(1, N + 1))
        maj2 = True
        for r in range(1, N + 1):
            if not maj2:
                break
            for S in itertools.combinations(range(N), r):
                if sum(d[i] for i in S) > sum(range(N, N - r, -1)) + 1e-9:
                    maj2 = False; break
        assert maj == maj2
    # (iv) two independent solvers (scipy LP cutting planes vs HiGHS QP) agree; F4 => F3
    for n in (7, 8, 9, 10):
        for tid, edges in load_trees(n):
            T = Tree(n, edges)
            p = filter_projection(T)[0]; l = filter_lp(T)[0]; q = filter_qp(T)[0]
            assert l == q, (n, tid, l, q)
            assert (not p) <= (not q), (n, tid, p, q)
    print("PASS Lemma 7-8 (relaxation): Leech weights feasible; containment/Golomb ranks on 300 random; oracle==definition; LP==QP on n<=10; F4=>F3")


def small_filter_table():
    print("\nFilter survivors by order (n: total -> F1 F2 F5 F3 F4 F6 cumulative):")
    for n in range(4, 12):
        trees = load_trees(n)
        counts = []
        alive = list(range(len(trees)))
        Ts = {tid: Tree(n, e) for tid, e in trees}
        for name, fn in FILTERS:
            alive = [i for i in alive if fn(Ts[trees[i][0]])]
            counts.append(len(alive))
        print(f"  n={n}: {len(trees)} -> {counts}")


def run_tests():
    rng = random.Random(20260818)
    test_ogr()
    test_moments(rng)
    found = test_exhaustive_small()
    test_golomb_lemma(found, rng)
    test_topvalues(found, rng)
    test_sidon(found, rng)
    test_mod4(found, rng)
    test_lp_and_projection(found, rng)
    small_filter_table()
    print("\nALL TESTS PASSED")


# ----------------------------------------------------------------------------------------------
# n=18 filtering
# ----------------------------------------------------------------------------------------------
def _work(args):
    tid, n, edges = args
    T = Tree(n, edges)
    r = {'id': tid}
    r['F1'] = filter_golomb(T)
    r['F2'] = filter_degree(T)
    r['F5'] = filter_topvalues(T)
    ok, ratio = filter_projection(T)
    r['F3'] = bool(ok); r['F3_ratio'] = round(float(ratio), 4)
    if r['F1'] and r['F2'] and r['F3'] and r['F5']:
        ok, it, cuts, st = filter_qp(T)
        if not ok:   # independent cross-check of every kill with the scipy LP; keep if solvers disagree
            ok2 = filter_lp(T)[0]
            if ok2:
                st += '(LP disagrees: kept)'; ok = True
        r['F4'] = bool(ok); r['F4_status'] = st
    else:
        r['F4'] = False; r['F4_status'] = 'skipped(dead)'
    r['F6'] = bool(filter_qp_diam(T)) if r['F4'] else False
    r['diam'] = T.hop_diameter(); r['maxdeg'] = max(T.deg); r['leaves'] = len(T.leaves())
    return r


def run_filter(n, jobs=1, write=False, limit=None):
    from multiprocessing import Pool
    trees = load_trees(n, limit)
    t0 = time.time()
    tasks = [(tid, n, e) for tid, e in trees]
    if jobs > 1:
        with Pool(jobs) as pool:
            rows = pool.map(_work, tasks, chunksize=64)
    else:
        rows = [_work(t) for t in tasks]
    dt = time.time() - t0
    tot = len(rows)
    ind = {k: sum(1 for r in rows if r[k]) for k in ('F1', 'F2', 'F5', 'F3')}
    cum = {}
    alive = rows
    for k in ('F1', 'F2', 'F5', 'F3', 'F4', 'F6'):
        alive = [r for r in alive if r[k]]
        cum[k] = len(alive)
    print(f"n={n}: {tot} topologies, {dt:.1f}s")
    print("  individual survivors:", ind, "(F4 only evaluated on F1&F2&F3&F5 survivors; F6 on F4 survivors)")
    print("  cumulative survivors F1,F2,F5,F3,F4,F6:", cum)
    diam_hist = defaultdict(int); deg_hist = defaultdict(int)
    for r in alive:
        diam_hist[r['diam']] += 1; deg_hist[r['maxdeg']] += 1
    print("  survivors by hop-diameter:", dict(sorted(diam_hist.items())))
    print("  survivors by max degree:", dict(sorted(deg_hist.items())))
    if write:
        os.makedirs(os.path.join(ROOT, 'results'), exist_ok=True)
        with open(os.path.join(ROOT, 'results', f'theory_survivors_{n}.txt'), 'w') as f:
            for r in alive:
                f.write(f"{r['id']}\n")
        with open(os.path.join(ROOT, 'results', f'theory_filters_{n}.jsonl'), 'w') as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print("  wrote results/theory_survivors_%d.txt and results/theory_filters_%d.jsonl" % (n, n))
    return rows


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'test':
        run_tests()
    elif sys.argv[1] == 'filter18':
        jobs = int(sys.argv[sys.argv.index('-j') + 1]) if '-j' in sys.argv else 1
        limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None
        run_filter(18, jobs=jobs, write=(limit is None), limit=limit)
    elif sys.argv[1] == 'filter':
        n = int(sys.argv[2])
        jobs = int(sys.argv[sys.argv.index('-j') + 1]) if '-j' in sys.argv else 1
        run_filter(n, jobs=jobs)
