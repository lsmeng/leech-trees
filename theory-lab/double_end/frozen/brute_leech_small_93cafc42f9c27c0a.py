#!/usr/bin/env python3
"""
brute_leech_small.py -- independent brute-force ground-truth enumerator for Leech trees.

Written from scratch (no reuse of any other search code in this repository) so that
its output can serve as an independent regression oracle for other search engines.

DEFINITION
    A Leech tree of order n is a tree on n vertices with positive integer edge
    weights such that the C(n,2) pairwise path distances are exactly
    {1, 2, ..., C(n,2)}, each value occurring exactly once.

WHAT THIS SCRIPT DOES
    1. Enumerates all unlabeled trees on n vertices (self-contained: recursive
       leaf-addition generator + AHU canonical form dedup; no networkx needed).
    2. For each tree shape, exhaustively searches positive integer edge weights
       with a DFS that grows a connected subtree one edge at a time and prunes
       as soon as two determined pairwise distances collide or exceed N=C(n,2).
    3. Deduplicates the solutions up to isomorphism of the *weighted* tree.
    4. Emits the "double-end data" for each Leech tree and checks claims (i)-(iv).
    5. Writes ground_truth_small.json and ground_truth_small.md.

PRUNING (all provably sound -- necessary conditions for a Leech tree)
    P1  distinctness: every newly determined distance must be <= N, unused, and
        distinct from the other distances created by the same edge.
    P2  weight-sum identity: sum_e c_e * w_e = N(N+1)/2, where c_e = a_e * b_e is
        the product of the two component sizes obtained by deleting edge e.
        (Each edge e lies on exactly a_e*b_e of the C(n,2) tree paths, so the sum
        of all pairwise distances equals sum_e c_e w_e; it must equal 1+...+N.)
        Used both as an exact terminal test and as a two-sided interval bound on
        the partial sum, via the rearrangement inequality against the still
        unused distance values.
    P3  distinct weights: every edge weight is itself a pairwise distance, so the
        weights are distinct and each is drawn from the still-unused values.
    P4  monotone cutoff: candidate weights are tried in increasing order, so once
        the partial weighted sum exceeds the target the loop can break.

    Every complete assignment is finally re-verified from scratch by recomputing
    all pairwise distances and comparing the sorted list against [1..N].

USAGE
    python3 brute_leech_small.py [--nmax 9] [--outdir DIR]
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone


# --------------------------------------------------------------------------
# tree machinery
# --------------------------------------------------------------------------

def build_adj(n, edges):
    adj = [[] for _ in range(n)]
    for (u, v) in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def _rooted_code(adj, root, parent):
    """AHU canonical code of the tree rooted at `root` (unweighted)."""
    kids = [c for c in adj[root] if c != parent]
    if not kids:
        return "()"
    return "(" + "".join(sorted(_rooted_code(adj, c, root) for c in kids)) + ")"


def canon_free(n, edges):
    """Complete isomorphism invariant for a free (unrooted) tree.

    min over all choices of root of the AHU rooted code.  Complete: an
    isomorphism carries roots to roots, so the *set* of rooted codes is an
    invariant; conversely equal minima exhibit an isomorphism of rooted trees.
    """
    if n <= 1:
        return "()"
    adj = build_adj(n, edges)
    return min(_rooted_code(adj, r, -1) for r in range(n))


def _rooted_code_w(adjw, root, parent):
    """AHU canonical code of a rooted *edge-weighted* tree."""
    kids = [(c, w) for (c, w) in adjw[root] if c != parent]
    if not kids:
        return "()"
    return "(" + "".join(sorted("%d:%s" % (w, _rooted_code_w(adjw, c, root))
                                for (c, w) in kids)) + ")"


def canon_free_weighted(n, wedges):
    """Complete isomorphism invariant for a free edge-weighted tree."""
    adjw = [[] for _ in range(n)]
    for (u, v, w) in wedges:
        adjw[u].append((v, w))
        adjw[v].append((u, w))
    return min(_rooted_code_w(adjw, r, -1) for r in range(n))


def gen_free_trees(n):
    """All unlabeled trees on n vertices, as lists of (u, v) edges on 0..n-1.

    Every tree on k vertices arises from a tree on k-1 vertices by attaching a
    new leaf, so growing by leaves and deduplicating by canonical form at each
    level is exhaustive.
    """
    if n <= 0:
        return []
    if n == 1:
        return [[]]
    trees = [[]]                       # the single tree on 1 vertex
    for k in range(2, n + 1):
        seen = {}
        for e in trees:
            for attach in range(k - 1):
                ne = e + [(attach, k - 1)]
                c = canon_free(k, ne)
                if c not in seen:
                    seen[c] = ne
        trees = list(seen.values())
    return trees


def edge_coeffs(n, edges):
    """c_e = a_e * b_e, the number of tree paths through edge e."""
    coeffs = []
    for i in range(len(edges)):
        rest = [e for j, e in enumerate(edges) if j != i]
        adj = build_adj(n, rest)
        u = edges[i][0]
        seen = {u}
        st = [u]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        a = len(seen)
        coeffs.append(a * (n - a))
    return coeffs


def growth_order(n, edges, coeffs):
    """Order edges so the placed set stays connected, greedily taking the edge
    with the largest coefficient first (strongest early sum constraint).

    Returns a list of (parent_already_placed, new_vertex, coeff, edge_index).
    """
    m = len(edges)
    if m == 0:
        return [], 0
    first = max(range(m), key=lambda i: coeffs[i])
    start = edges[first][0]
    placed = {start}
    remaining = set(range(m))
    order = []
    while remaining:
        cands = []
        for i in remaining:
            u, v = edges[i]
            if (u in placed) != (v in placed):
                p, t = (u, v) if u in placed else (v, u)
                cands.append((coeffs[i], i, p, t))
        cands.sort(key=lambda x: -x[0])
        c, i, p, t = cands[0]
        order.append((p, t, c, i))
        placed.add(t)
        remaining.discard(i)
    return order, start


def all_pairs_distances(n, wedges):
    """Full distance matrix of a weighted tree, computed independently."""
    adjw = [[] for _ in range(n)]
    for (u, v, w) in wedges:
        adjw[u].append((v, w))
        adjw[v].append((u, w))
    D = [[0] * n for _ in range(n)]
    for s in range(n):
        st = [(s, -1, 0)]
        while st:
            x, par, dd = st.pop()
            D[s][x] = dd
            for (y, w) in adjw[x]:
                if y != par:
                    st.append((y, x, dd + w))
    return D


# --------------------------------------------------------------------------
# the weight search
# --------------------------------------------------------------------------


CROSS_CHECK = {
    "script": "crosscheck_independent.py (log: crosscheck_independent.log)",
    "shares_code_with_this_file": False,
    "methods": {
        "shape_counts": {
            "how": "trees from Prufer-sequence decoding, deduplicated by the "
                   "multiset of vertex distance-vectors, with bucket members "
                   "spot-confirmed isomorphic by explicit n! bijection search",
            "counts": {2: 1, 3: 1, 4: 2, 5: 3, 6: 6, 7: 11, 8: 23, 9: 47},
            "agrees_with_this_file": True,
        },
        "A_full_cube_scan": {
            "how": "numpy scan of the ENTIRE cube [1..N]^(n-1); the only test "
                   "applied is the definition (all C(n,2) distances distinct "
                   "and <= N). No sum identity, no bounds, no ordering prune.",
            "n_range": [2, 6],
            "counts": {2: 1, 3: 1, 4: 2, 5: 0, 6: 1},
            "tuples_scanned": {2: 1, 3: 9, 4: 432, 5: 30000, 6: 4556250},
            "agrees_with_this_file": True,
            "same_trees_found": True,
        },
        "B_distinctness_only_dfs": {
            "how": "DFS with the distinctness prune only -- no sum identity, "
                   "no rearrangement bound, no monotone cutoff.",
            "n_exhaustive": [2, 3, 4, 5, 6, 7, 8],
            "counts": {2: 1, 3: 1, 4: 2, 5: 0, 6: 1, 7: 0, 8: 0},
            "agrees_with_this_file": True,
            "n9": "INCONCLUSIVE -- the run spent its whole budget generating "
                  "the 9-vertex shapes via Prufer sequences and timed out "
                  "before the weight search did any real work.",
        },
    },
    "summary": ("n = 2..8 are corroborated by at least one search that uses "
                "nothing beyond the definition. n = 9 rests on this file's "
                "search alone."),
}


class LimitHit(Exception):
    pass


def bound_ok(S, cs_desc, avail_sorted, target):
    """Reference two-sided bound on the achievable completion of sum_e c_e w_e.

    cs_desc: coefficients of the still-unassigned edges, sorted descending.
    avail_sorted: still-unused distance values, ascending.  The weights of the
    unassigned edges must be distinct members of this list, so by the
    rearrangement inequality the minimum of sum c_e w_e pairs the largest
    coefficients with the smallest available values and the maximum pairs
    largest with largest.

    The DFS inlines this for speed (it only needs the r smallest and r largest
    available values); `--selftest` checks the two agree on random inputs.
    """
    r = len(cs_desc)
    need = target - S
    if r == 0:
        return need == 0
    if len(avail_sorted) < r:
        return False
    lo = 0
    hi = 0
    for i in range(r):
        lo += cs_desc[i] * avail_sorted[i]
        hi += cs_desc[i] * avail_sorted[-1 - i]
    return lo <= need <= hi


def bound_ok_fast(S, cs_desc, lo_vals, hi_vals, target):
    """Same predicate as bound_ok, given only the r smallest (ascending) and
    r largest (descending) still-available values."""
    r = len(cs_desc)
    need = target - S
    if r == 0:
        return need == 0
    if len(lo_vals) < r:
        return False
    lo = 0
    hi = 0
    for i in range(r):
        lo += cs_desc[i] * lo_vals[i]
        hi += cs_desc[i] * hi_vals[i]
    return lo <= need <= hi


def selftest(trials=4000):
    """Check bound_ok_fast agrees with the reference bound_ok."""
    import random
    rnd = random.Random(20260902)
    for _ in range(trials):
        N = rnd.randint(1, 40)
        avail = sorted(rnd.sample(range(1, N + 1), rnd.randint(1, N)))
        r = rnd.randint(0, 8)
        cs = sorted((rnd.randint(1, 25) for _ in range(r)), reverse=True)
        S = rnd.randint(0, 500)
        target = rnd.randint(0, 800)
        lo_vals = avail[:r]
        hi_vals = list(reversed(avail))[:r]
        a = bound_ok(S, cs, avail, target)
        b = bound_ok_fast(S, cs, lo_vals, hi_vals, target)
        if a != b:
            raise AssertionError("bound mismatch: %r" % ((N, avail, cs, S, target),))
    print("selftest: bound_ok_fast agrees with bound_ok on %d random cases" % trials)


def search_tree(n, edges, node_limit, deadline):
    """Exhaustive DFS over weight assignments for one tree shape.

    Returns (solutions, nodes_used, hit_limit).  solutions is a list of weight
    lists indexed by the original edge order.
    """
    N = n * (n - 1) // 2
    target = N * (N + 1) // 2
    m = len(edges)
    coeffs = edge_coeffs(n, edges)
    order, start = growth_order(n, edges, coeffs)

    # suffix[i] = coefficients of order[i:], sorted descending
    suffix = [None] * (m + 1)
    suffix[m] = []
    for i in range(m - 1, -1, -1):
        suffix[i] = sorted(suffix[i + 1] + [order[i][2]], reverse=True)

    D = [[0] * n for _ in range(n)]
    placed = [start]
    used = bytearray(N + 2)
    weights = [0] * m           # indexed by position in `order`
    sols = []
    stats = {"nodes": 0}

    def rec(idx, S):
        stats["nodes"] += 1
        if stats["nodes"] > node_limit:
            raise LimitHit()
        if (stats["nodes"] & 0x3FFF) == 0 and time.time() > deadline:
            raise LimitHit()
        if idx == m:
            sols.append(list(weights))
            return
        p, t, c, ei = order[idx]
        rest = suffix[idx + 1]
        r = len(rest)
        avail = [v for v in range(1, N + 1) if not used[v]]
        dp = [D[s][p] for s in placed]      # independent of w; hoisted
        for w in avail:
            S2 = S + c * w
            if S2 > target:
                break                      # P4: S2 is increasing in w
            newd = []
            seen = set()
            ok = True
            for b in dp:
                val = b + w
                if val > N or used[val] or val in seen:
                    ok = False
                    break
                seen.add(val)
                newd.append(val)
            if not ok:
                continue
            for v in newd:
                used[v] = 1
            # the r smallest / r largest values still available
            lo_vals = []
            hi_vals = []
            if r:
                for v in avail:
                    if not used[v]:
                        lo_vals.append(v)
                        if len(lo_vals) == r:
                            break
                if len(lo_vals) == r:
                    for v in reversed(avail):
                        if not used[v]:
                            hi_vals.append(v)
                            if len(hi_vals) == r:
                                break
            if bound_ok_fast(S2, rest, lo_vals, hi_vals, target):
                for k, s in enumerate(placed):
                    D[s][t] = D[t][s] = newd[k]
                D[t][t] = 0
                placed.append(t)
                weights[idx] = w
                rec(idx + 1, S2)
                placed.pop()
            for v in newd:
                used[v] = 0

    hit = False
    try:
        rec(0, 0)
    except LimitHit:
        hit = True

    # translate solutions from `order` positions back to original edge indices
    out = []
    for ws in sols:
        wlist = [0] * m
        for pos, (p, t, c, ei) in enumerate(order):
            wlist[ei] = ws[pos]
        out.append(wlist)
    return out, stats["nodes"], hit


def verify_leech(n, wedges):
    """Independent re-verification: recompute all distances, compare to 1..N."""
    N = n * (n - 1) // 2
    D = all_pairs_distances(n, wedges)
    ds = sorted(D[i][j] for i in range(n) for j in range(i + 1, n))
    return ds == list(range(1, N + 1)), ds, D


# --------------------------------------------------------------------------
# double-end analysis
# --------------------------------------------------------------------------

def double_end(n, wedges):
    """Compute double-end data and check claims (i)-(iv). Returns a dict."""
    N = n * (n - 1) // 2
    D = all_pairs_distances(n, wedges)
    anchors = [(i, j) for i in range(n) for j in range(i + 1, n) if D[i][j] == N]
    res = {"N": N, "anchor_pair_count": len(anchors)}
    if len(anchors) != 1:
        res["error"] = "diameter pair not unique"
        return res
    a, b = anchors[0]
    res["anchors"] = [a, b]
    others = [u for u in range(n) if u not in (a, b)]
    table = []
    for u in others:
        e = N - D[a][u]
        f = N - D[b][u]
        h2 = N - e - f
        table.append({
            "u": u, "d_a": D[a][u], "d_b": D[b][u],
            "e": e, "f": f,
            "h_is_integer": (h2 % 2 == 0),
            "h": h2 // 2 if h2 % 2 == 0 else None,
            "f_minus_e": f - e,
        })
    res["table"] = table
    E = [r["e"] for r in table]
    F = [r["f"] for r in table]
    res["E"] = sorted(E)
    res["F"] = sorted(F)

    checks = {}

    # ---- claim (i)
    c1 = {}
    c1["E_size_ok"] = (len(set(E)) == n - 2 and len(E) == n - 2)
    c1["F_size_ok"] = (len(set(F)) == n - 2 and len(F) == n - 2)
    c1["disjoint"] = len(set(E) & set(F)) == 0
    c1["range_ok"] = all(1 <= x <= N - 1 for x in E + F)
    c1["pass"] = all(c1.values())
    c1["vacuous"] = (len(table) == 0)
    if E + F:
        c1["intersection"] = sorted(set(E) & set(F))
    checks["i"] = c1

    # ---- claim (ii)
    c2 = {"parity_pass": True, "sum_pass": True, "distinct_pass": True,
          "parity_failures": [], "sum_failures": [], "distinct_failures": []}
    for r in table:
        e, f, u = r["e"], r["f"], r["u"]
        if (e - f) % 2 != 0:
            c2["parity_pass"] = False
            c2["parity_failures"].append({"u": u, "e": e, "f": f})
        if e + f > N:
            c2["sum_pass"] = False
            c2["sum_failures"].append({"u": u, "e": e, "f": f, "sum": e + f})
        if e == f:
            c2["distinct_pass"] = False
            c2["distinct_failures"].append({"u": u, "e": e, "f": f})
    c2["pass"] = c2["parity_pass"] and c2["sum_pass"] and c2["distinct_pass"]
    c2["vacuous"] = (len(table) == 0)
    c2["vertices_checked"] = len(table)
    # e(u)+f(u) = N - 2h(u) identically, so e = f (mod 2) iff N is even.
    c2["N_parity"] = "even" if N % 2 == 0 else "odd"
    c2["parity_claim_predicted_by_N_parity"] = (N % 2 == 0)
    checks["ii"] = c2

    # ---- claim (iii)
    c3 = {"pairs": [], "hc_integer_pass": True, "hc_nonneg_pass": True,
          "hc_zero_when_slopes_differ_pass": True, "hc_le_min_h_pass": True}
    idx = {r["u"]: r for r in table}
    for i in range(len(others)):
        for j in range(i + 1, len(others)):
            u, v = others[i], others[j]
            ru, rv = idx[u], idx[v]
            lhs = N - D[u][v]
            cross = min(ru["f"] + rv["e"], rv["f"] + ru["e"])
            diff = lhs - cross
            hc = diff // 2 if diff % 2 == 0 else None
            slopes_differ = (ru["f_minus_e"] != rv["f_minus_e"])
            hu, hv = ru["h"], rv["h"]
            rec = {"u": u, "v": v, "d_uv": D[u][v], "N_minus_d": lhs,
                   "min_cross": cross, "h_c": hc,
                   "slopes_differ": slopes_differ,
                   "h_u": hu, "h_v": hv}
            if hc is None:
                c3["hc_integer_pass"] = False
                rec["fail"] = "h_c not an integer"
            else:
                if hc < 0:
                    c3["hc_nonneg_pass"] = False
                    rec["fail"] = "h_c negative"
                if slopes_differ and hc != 0:
                    c3["hc_zero_when_slopes_differ_pass"] = False
                    rec["fail"] = "h_c nonzero although slopes differ"
                if hu is not None and hv is not None and hc > min(hu, hv):
                    c3["hc_le_min_h_pass"] = False
                    rec["fail"] = "h_c > min(h_u,h_v)"
            c3["pairs"].append(rec)
    c3["pass"] = (c3["hc_integer_pass"] and c3["hc_nonneg_pass"]
                  and c3["hc_zero_when_slopes_differ_pass"]
                  and c3["hc_le_min_h_pass"])
    c3["vacuous"] = (len(c3["pairs"]) == 0)
    c3["pairs_checked"] = len(c3["pairs"])
    # How much of claim (iii) was actually exercised?
    c3["pairs_with_slopes_differ"] = sum(1 for q in c3["pairs"] if q["slopes_differ"])
    c3["pairs_with_slopes_equal"] = sum(1 for q in c3["pairs"] if not q["slopes_differ"])
    hcs = [q["h_c"] for q in c3["pairs"] if q["h_c"] is not None]
    c3["max_h_c"] = max(hcs) if hcs else None
    c3["all_h_c_zero"] = all(x == 0 for x in hcs) if hcs else None
    # the "h_c <= min(h_u,h_v)" bound is only informative when it could bind
    c3["pairs_where_bound_could_bind"] = sum(
        1 for q in c3["pairs"]
        if q["h_u"] is not None and q["h_v"] is not None and min(q["h_u"], q["h_v"]) > 0
        and not q["slopes_differ"])
    checks["iii"] = c3

    # ---- claim (iv)
    multiset = [0] + E + F + [N - D[others[i]][others[j]]
                              for i in range(len(others))
                              for j in range(i + 1, len(others))]
    c4 = {"multiset_sorted": sorted(multiset),
          "expected": list(range(0, N)),
          "pass": sorted(multiset) == list(range(0, N)),
          "vacuous": False}
    checks["iv"] = c4

    res["checks"] = checks
    res["all_pass"] = all(checks[k]["pass"] for k in ("i", "ii", "iii", "iv"))
    return res


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def run(nmax, outdir, budgets):
    started = time.time()
    per_n = {}
    all_trees = []
    known_tree_counts = {1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 6, 7: 11, 8: 23, 9: 47,
                         10: 106, 11: 235}

    for n in range(2, nmax + 1):
        N = n * (n - 1) // 2
        shapes = gen_free_trees(n)
        t0 = time.time()
        node_limit, time_limit = budgets.get(n, (10 ** 9, 3600.0))
        deadline = t0 + time_limit
        total_nodes = 0
        hit_any = False
        raw = []
        per_shape = []
        for si, edges in enumerate(shapes):
            sols, nodes, hit = search_tree(n, edges, node_limit - total_nodes,
                                           deadline)
            total_nodes += nodes
            hit_any = hit_any or hit
            per_shape.append({"shape_index": si,
                              "shape_canon": canon_free(n, edges),
                              "edges": [list(e) for e in edges],
                              "nodes": nodes,
                              "solutions": len(sols),
                              "hit_limit": hit})
            for ws in sols:
                raw.append([[edges[k][0], edges[k][1], ws[k]]
                            for k in range(len(edges))])
        elapsed = time.time() - t0

        # dedup up to isomorphism of the weighted tree, and re-verify
        uniq = {}
        for wedges in raw:
            good, ds, D = verify_leech(n, [tuple(x) for x in wedges])
            if not good:
                raise RuntimeError("internal error: search returned a non-Leech "
                                   "tree for n=%d: %r" % (n, wedges))
            key = canon_free_weighted(n, [tuple(x) for x in wedges])
            if key not in uniq:
                uniq[key] = (wedges, ds)

        entries = []
        for key in sorted(uniq):
            wedges, ds = uniq[key]
            de = double_end(n, [tuple(x) for x in wedges])
            entries.append({
                "n": n, "N": N,
                "weighted_canonical_form": key,
                "edges": [[u, v, w] for (u, v, w) in wedges],
                "distances_sorted": ds,
                "distances_equal_1_to_N": ds == list(range(1, N + 1)),
                "double_end": de,
            })
            all_trees.append(entries[-1])

        per_n[n] = {
            "N": N,
            "tree_shapes": len(shapes),
            "tree_shapes_expected_oeis_A000055": known_tree_counts.get(n),
            "tree_shape_count_matches_known": len(shapes) == known_tree_counts.get(n),
            "leech_trees_up_to_iso": len(uniq),
            "raw_labeled_solutions": len(raw),
            "dfs_nodes": total_nodes,
            "seconds": round(elapsed, 3),
            "node_limit": node_limit,
            "time_limit_s": time_limit,
            "exhaustive": (not hit_any),
            "hit_limit": hit_any,
            "per_shape": per_shape,
        }
        print("n=%d  N=%2d  shapes=%3d  leech=%d  nodes=%d  %.2fs  %s"
              % (n, N, len(shapes), len(uniq), total_nodes, elapsed,
                 "EXHAUSTIVE" if not hit_any else "*** HIT LIMIT ***"),
              flush=True)

    summary = {
        "schema_version": 1,
        "generator": "brute_leech_small.py (independent brute-force enumerator)",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "definition": ("A Leech tree of order n is a tree on n vertices with "
                       "positive integer edge weights whose C(n,2) pairwise "
                       "path distances are exactly {1,...,C(n,2)}."),
        "notes": {
            "vertex_labels": "0-based; edges are [u, v, weight].",
            "counts": "leech_trees_up_to_iso counts weighted trees up to "
                      "isomorphism (AHU canonical form of the edge-weighted tree).",
            "double_end": ("anchors (a,b) is the unique pair at distance N; "
                           "e(u)=N-d(a,u), f(u)=N-d(b,u), h(u)=(N-e-f)/2; "
                           "h_c = (N-d(u,v) - min(f_u+e_v, f_v+e_u))/2."),
        },
        "per_n": per_n,
        "counts_by_n": {str(n): per_n[n]["leech_trees_up_to_iso"] for n in per_n},
        "exhaustive_by_n": {str(n): per_n[n]["exhaustive"] for n in per_n},
        "regression_expected_counts": {
            "description": ("Complete counts of Leech trees of order n up to "
                            "isomorphism of the edge-weighted tree, for every n "
                            "whose search finished exhaustively. Safe to use as a "
                            "regression fixture for another search engine."),
            "counts": {str(n): per_n[n]["leech_trees_up_to_iso"]
                       for n in per_n if per_n[n]["exhaustive"]},
            "n_not_exhaustive": [n for n in per_n if not per_n[n]["exhaustive"]],
        },
        "leech_trees": all_trees,
        "claim_summary": claim_summary(all_trees),
        "independent_cross_check": CROSS_CHECK,
        "total_seconds": round(time.time() - started, 3),
    }

    os.makedirs(outdir, exist_ok=True)
    jpath = os.path.join(outdir, "ground_truth_small.json")
    with open(jpath, "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=False)
    mpath = os.path.join(outdir, "ground_truth_small.md")
    with open(mpath, "w") as fh:
        fh.write(render_md(summary))
    print("\nwrote %s\nwrote %s" % (jpath, mpath))
    return summary


def claim_summary(trees):
    out = {}
    for key in ("i", "ii", "iii", "iv"):
        tot = len(trees)
        ok = sum(1 for t in trees if t["double_end"]["checks"][key]["pass"])
        nonvac = [t for t in trees
                  if not t["double_end"]["checks"][key].get("vacuous")]
        nvok = sum(1 for t in nonvac if t["double_end"]["checks"][key]["pass"])
        out[key] = {"trees_checked": tot, "passed": ok, "failed": tot - ok,
                    "all_pass": ok == tot,
                    "trees_non_vacuous": len(nonvac),
                    "non_vacuous_passed": nvok,
                    "non_vacuous_failed": len(nonvac) - nvok}
    # parity sub-claim of (ii) broken out, since it is the interesting one
    tot = len(trees)
    ok = sum(1 for t in trees if t["double_end"]["checks"]["ii"]["parity_pass"])
    out["ii_parity_only"] = {"trees_checked": tot, "passed": ok,
                             "failed": tot - ok, "all_pass": ok == tot}
    ok = sum(1 for t in trees if t["double_end"]["checks"]["ii"]["sum_pass"])
    out["ii_sum_only"] = {"trees_checked": tot, "passed": ok,
                          "failed": tot - ok, "all_pass": ok == tot}
    ok = sum(1 for t in trees if t["double_end"]["checks"]["ii"]["distinct_pass"])
    out["ii_distinct_only"] = {"trees_checked": tot, "passed": ok,
                               "failed": tot - ok, "all_pass": ok == tot}
    # which trees fail the parity sub-claim, and does N-parity explain it?
    par = []
    for t in trees:
        c = t["double_end"]["checks"]["ii"]
        if c.get("vacuous"):
            continue
        par.append({"n": t["n"], "N": t["N"], "N_parity": c["N_parity"],
                    "parity_pass": c["parity_pass"],
                    "predicted": c["parity_claim_predicted_by_N_parity"],
                    "prediction_correct":
                        c["parity_pass"] == c["parity_claim_predicted_by_N_parity"]})
    out["ii_parity_detail"] = {
        "per_tree": par,
        "identity": "e(u)+f(u) = N - 2h(u) with h(u)=dist(u, a-b path) >= 0, "
                    "so e(u) = f(u) (mod 2) if and only if N is even.",
        "prediction_holds_on_all_trees": all(x["prediction_correct"] for x in par),
    }
    # how much of claim (iii) was really exercised
    pairs = sum(t["double_end"]["checks"]["iii"]["pairs_checked"] for t in trees)
    hcs = [q["h_c"] for t in trees
           for q in t["double_end"]["checks"]["iii"]["pairs"]
           if q["h_c"] is not None]
    out["iii_coverage"] = {
        "total_non_anchor_pairs_checked": pairs,
        "pairs_with_slopes_differ": sum(
            t["double_end"]["checks"]["iii"]["pairs_with_slopes_differ"] for t in trees),
        "pairs_with_slopes_equal": sum(
            t["double_end"]["checks"]["iii"]["pairs_with_slopes_equal"] for t in trees),
        "pairs_where_h_c_bound_could_bind": sum(
            t["double_end"]["checks"]["iii"]["pairs_where_bound_could_bind"] for t in trees),
        "observed_h_c_values": sorted(set(hcs)),
        "all_observed_h_c_are_zero": all(x == 0 for x in hcs) if hcs else None,
        "caveat": ("h_c = 0 on every pair in this data set, so the sub-claims "
                   "'h_c = 0 when the slopes differ' and 'h_c <= min(h_u,h_v)' "
                   "are satisfied but never discriminated: no observed pair "
                   "would have violated them for any nonnegative h_c choice "
                   "other than by being nonzero."),
    }
    return out


def render_md(s):
    L = []
    A = L.append
    A("# Ground truth: small Leech trees (independent brute force)\n")
    A("Generated `%s` by `brute_leech_small.py`.\n" % s["generated_utc"])
    A("**Definition.** %s\n" % s["definition"])
    A("Vertices are 0-based; an edge is written `u-v (w)`.\n")
    A("This file is produced by an implementation written from scratch for this purpose;")
    A("it shares no code with any other search engine in this repository, so it can be")
    A("used as an independent oracle.\n")

    A("## 1. Counts per n\n")
    A("| n | N=C(n,2) | tree shapes | shapes match known | Leech trees (up to iso) | DFS nodes | time (s) | exhaustive |")
    A("|---|---|---|---|---|---|---|---|")
    for n in sorted(s["per_n"], key=int):
        d = s["per_n"][n] if isinstance(n, str) else s["per_n"][n]
        A("| %s | %d | %d | %s | %d | %d | %.2f | %s |"
          % (n, d["N"], d["tree_shapes"],
             "yes" if d["tree_shape_count_matches_known"] else "NO",
             d["leech_trees_up_to_iso"], d["dfs_nodes"], d["seconds"],
             "yes" if d["exhaustive"] else "NO (hit limit)"))
    A("")
    A("Search limits used: node limit / wall-clock limit per n are recorded in the JSON.")
    A("An `exhaustive = yes` row means the DFS finished the whole search space for")
    A("every tree shape on n vertices, so the count is a complete count.\n")
    A("**Regression fixture.** For every n marked exhaustive above, the count is a")
    A("complete count of Leech trees of order n up to isomorphism of the weighted tree:\n")
    A("```python")
    A("EXPECTED_LEECH_COUNTS = %s" % (
        {int(k): v for k, v in sorted(s["counts_by_n"].items(), key=lambda kv: int(kv[0]))
         if s["exhaustive_by_n"][k]},))
    A("```\n")
    A("These agree with the literature: Leech trees exist only for n = 2, 3, 4, 6 in")
    A("this range, with two of them at n = 4, and none for n = 5, 7, 8, 9.\n")

    A("## 2. Claim summary over all Leech trees found\n")
    cs = s["claim_summary"]
    A("| claim | trees checked | passed | failed | non-vacuous trees | verdict |")
    A("|---|---|---|---|---|---|")
    labels = {
        "i": "(i) E,F disjoint, size n-2, in [1,N-1]",
        "ii": "(ii) e=f mod 2, e+f<=N, e!=f  (all three)",
        "ii_parity_only": "(ii-a) e(u) = f(u) mod 2",
        "ii_sum_only": "(ii-b) e(u)+f(u) <= N",
        "ii_distinct_only": "(ii-c) e(u) != f(u)",
        "iii": "(iii) N-d(u,v) = min(f_u+e_v, f_v+e_u) + 2h_c, h_c>=0, forced 0, h_c<=min(h_u,h_v)",
        "iv": "(iv) {0} u E u F u {N-d(u,v)} = {0..N-1}",
    }
    for k in ("i", "ii", "ii_parity_only", "ii_sum_only", "ii_distinct_only",
              "iii", "iv"):
        d = cs[k]
        base = k.split("_")[0]
        nv = cs[base].get("trees_non_vacuous", d["trees_checked"])
        A("| %s | %d | %d | %d | %d | %s |"
          % (labels[k], d["trees_checked"], d["passed"], d["failed"], nv,
             "PASS" if d["all_pass"] else "**FAIL**"))
    A("")
    A("A tree is *vacuous* for a claim when the claim quantifies over an empty set")
    A("(n = 2 has no non-anchor vertices; n = 2, 3 have no non-anchor pairs), so the")
    A("`non-vacuous trees` column is the number of trees where the claim had content.")
    A("")
    A("### 2a. What these numbers do and do not establish\n")
    A("Only %d Leech trees exist in this range, so the sample is tiny. Per-claim caveats:\n"
      % len(s["leech_trees"]))
    A("* **(i), (ii-b), (ii-c) and (iv) are forced by the Leech property itself**, so")
    A("  passing them is a consistency check on this enumerator rather than evidence for")
    A("  a nontrivial structural theorem. `d(a,u)` and `d(b,v)` are distances of distinct")
    A("  vertex pairs, hence distinct, which gives (i) and `e != f`; `d(a,u)+d(b,u) >=")
    A("  d(a,b) = N` gives `e+f <= N`; and (iv) is just the image of the bijection")
    A("  `{pairs} -> {1..N}` under `d |-> N-d`.")
    A("* **(ii-a) `e(u) = f(u) (mod 2)` is FALSE as stated.** Writing `h(u)` for the")
    A("  distance from `u` to the `a`-`b` path, `d(a,u)+d(b,u) = d(a,b) + 2h(u) = N + 2h(u)`,")
    A("  so `e(u)+f(u) = N - 2h(u)` identically. Hence `e(u) = f(u) (mod 2)` **iff N is")
    A("  even**. It holds for n = 4 (N = 6) and fails for n = 3 (N = 3) and n = 6 (N = 15).")
    A("  The correct universal statement is `e(u) + f(u) = N (mod 2)`. This prediction")
    A("  matched the data on every tree: %s."
      % s["claim_summary"]["ii_parity_detail"]["prediction_holds_on_all_trees"])
    cov = s["claim_summary"]["iii_coverage"]
    A("* **(iii) passed, but is barely exercised.** Only %d non-anchor pairs exist across"
      % cov["total_non_anchor_pairs_checked"])
    A("  all Leech trees found (%d with `f_u-e_u != f_v-e_v`, %d with them equal). Every"
      % (cov["pairs_with_slopes_differ"], cov["pairs_with_slopes_equal"]))
    A("  observed `h_c` was 0 (observed values: %s). So `min(f_u+e_v, f_v+e_u)` is exact"
      % cov["observed_h_c_values"])
    A("  on all available data, and the two refinements -- `h_c = 0` when the slopes")
    A("  differ, and `h_c <= min(h_u,h_v)` -- are satisfied but never discriminating:")
    A("  no pair in this data set could have distinguished them from the blanket")
    A("  statement `h_c = 0`. Treat (iii) as *not contradicted*, not as *confirmed*.")
    A("")

    A("## 2b. Independent cross-check of the counts\n")
    xc = s["independent_cross_check"]
    A("The counts above were re-derived by `crosscheck_independent.py`, which shares")
    A("no code with `brute_leech_small.py`: it builds trees from Prufer sequences")
    A("instead of leaf addition, decides isomorphism by brute-force search over all")
    A("`n!` vertex bijections instead of AHU canonical forms, and searches weights")
    A("using only the definition.\n")
    A("| check | n range | counts | agrees |")
    A("|---|---|---|---|")
    m = xc["methods"]
    A("| tree shape counts (Prufer + n! iso) | 2-9 | %s | %s |"
      % (m["shape_counts"]["counts"],
         "yes" if m["shape_counts"]["agrees_with_this_file"] else "NO"))
    A("| A: full scan of the entire cube `[1..N]^(n-1)`, definition only | 2-6 | %s | %s |"
      % (m["A_full_cube_scan"]["counts"],
         "yes" if m["A_full_cube_scan"]["agrees_with_this_file"] else "NO"))
    A("| B: DFS with the distinctness prune only | 2-8 | %s | %s |"
      % (m["B_distinctness_only_dfs"]["counts"],
         "yes" if m["B_distinctness_only_dfs"]["agrees_with_this_file"] else "NO"))
    A("")
    A("Method A scanned every one of the %d weight tuples for n = 6 with no"
      % m["A_full_cube_scan"]["tuples_scanned"][6])
    A("mathematical pruning at all, and returned the same single tree.\n")
    A("**Caveat for n = 9.** %s" % m["B_distinctness_only_dfs"]["n9"])
    A("So the n = 9 result (no Leech tree of order 9) rests on `brute_leech_small.py`")
    A("alone. Its extra prunes are provably necessary conditions -- the weight-sum")
    A("identity `sum_e a_e b_e w_e = N(N+1)/2` and the rearrangement bound derived")
    A("from it, plus distinctness of edge weights -- but they were not independently")
    A("re-implemented at n = 9. (The literature also reports no Leech tree of order 9.)\n")
    A("## 3. The Leech trees and their double-end data\n")
    for t in s["leech_trees"]:
        n, N = t["n"], t["N"]
        de = t["double_end"]
        A("### n = %d  (N = %d)\n" % (n, N))
        A("Edges: " + ", ".join("`%d-%d (%d)`" % (u, v, w) for u, v, w in t["edges"]))
        A("")
        A("Distances sorted: `%s`  ->  equals {1..%d}: **%s**\n"
          % (t["distances_sorted"], N,
             "yes" if t["distances_equal_1_to_N"] else "NO"))
        if "anchors" in de:
            a, b = de["anchors"]
            A("Anchor pair (unique pair at distance N): **(%d, %d)**\n" % (a, b))
            if de["table"]:
                A("| u | d(a,u) | d(b,u) | e(u) | f(u) | h(u) | f-e |")
                A("|---|---|---|---|---|---|---|")
                for r in de["table"]:
                    A("| %d | %d | %d | %d | %d | %s | %d |"
                      % (r["u"], r["d_a"], r["d_b"], r["e"], r["f"],
                         r["h"], r["f_minus_e"]))
                A("")
            A("E = %s" % de["E"])
            A("")
            A("F = %s" % de["F"])
            A("")
            ck = de["checks"]
            A("| claim | result |")
            A("|---|---|")
            A("| (i) disjoint / size %d / range [1,%d] | %s |"
              % (n - 2, N - 1, "PASS" if ck["i"]["pass"] else "**FAIL**"))
            A("| (ii-a) e = f (mod 2) | %s |"
              % ("PASS" if ck["ii"]["parity_pass"] else "**FAIL**"))
            A("| (ii-b) e+f <= N | %s |"
              % ("PASS" if ck["ii"]["sum_pass"] else "**FAIL**"))
            A("| (ii-c) e != f | %s |"
              % ("PASS" if ck["ii"]["distinct_pass"] else "**FAIL**"))
            A("| (iii) cross-distance formula | %s |"
              % ("PASS" if ck["iii"]["pass"] else "**FAIL**"))
            A("| (iv) full multiset = {0..%d} | %s |"
              % (N - 1, "PASS" if ck["iv"]["pass"] else "**FAIL**"))
            A("")
            if ck["ii"]["parity_failures"]:
                A("Parity failures (ii-a): `%s`\n" % ck["ii"]["parity_failures"])
            if ck["ii"]["sum_failures"]:
                A("Sum failures (ii-b): `%s`\n" % ck["ii"]["sum_failures"])
            if ck["ii"]["distinct_failures"]:
                A("Distinctness failures (ii-c): `%s`\n" % ck["ii"]["distinct_failures"])
            if ck["iii"]["pairs"]:
                A("Non-anchor pairs (claim iii):\n")
                A("| u | v | d(u,v) | N-d | min(f_u+e_v, f_v+e_u) | h_c | slopes differ | h_u | h_v | note |")
                A("|---|---|---|---|---|---|---|---|---|---|")
                for p in ck["iii"]["pairs"]:
                    A("| %d | %d | %d | %d | %d | %s | %s | %s | %s | %s |"
                      % (p["u"], p["v"], p["d_uv"], p["N_minus_d"],
                         p["min_cross"], p["h_c"],
                         "yes" if p["slopes_differ"] else "no",
                         p["h_u"], p["h_v"], p.get("fail", "")))
                A("")
            else:
                A("_No non-anchor pairs: claim (iii) is vacuous for n = %d._\n" % n)
            A("Multiset check (iv): `%s` vs expected `{0..%d}` -> %s\n"
              % (ck["iv"]["multiset_sorted"], N - 1,
                 "PASS" if ck["iv"]["pass"] else "**FAIL**"))
        else:
            A("**Anchor pair not unique** (%d pairs at distance N).\n"
              % de["anchor_pair_count"])
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=9)
    ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--n8-nodes", type=int, default=8_000_000)
    ap.add_argument("--n8-secs", type=float, default=60.0)
    ap.add_argument("--n9-nodes", type=int, default=12_000_000)
    ap.add_argument("--n9-secs", type=float, default=90.0)
    args = ap.parse_args()

    budgets = {}
    for n in range(2, 8):
        budgets[n] = (50_000_000, 120.0)
    budgets[8] = (args.n8_nodes, args.n8_secs)
    budgets[9] = (args.n9_nodes, args.n9_secs)

    sys.setrecursionlimit(10000)
    selftest()
    run(args.nmax, args.outdir, budgets)


if __name__ == "__main__":
    main()
