#!/usr/bin/env python3
"""Double-end (two-anchor) gap-order search for Leech trees.  See THEORY.md.

Model.  N = C(n,2), V = n-2.  Each non-anchor vertex u carries (e,f) with
    e = N - d(a,u),  f = N - d(b,u),  p = (N+f-e)/2,  h = (N-e-f)/2.
Constraints: 1 <= e,f <= N-1; e+f <= N; e+f = N (mod 2); E, F disjoint V-sets;
    gap(u,v) = min(f_u+e_v, f_v+e_u) + 2 h_c,  h_c = 0 unless f_u-e_u = f_v-e_v,
    else 0 <= h_c <= min(h_u,h_v);
and {0} u E u F u {gap(u,v)} = [0, N-1] exactly.

Search: process gaps g = 1..N-1 in increasing order.  The smallest unrealised
gap must be an e- or f-coordinate (of a new or a half-known vertex), or the
resolution of a deferred tied pair.  Everything else is forced.

This is a SOUND RELAXATION of the tree problem: h_c is only constrained by
0 <= h_c <= min(h_u,h_v), not by the requirement that the branch hierarchy be
realisable.  Hence "no solution" is a genuine non-existence proof; any
solution found must be checked by verify_solution().
"""
from __future__ import annotations
import sys, time, json


def parity_splits(n):
    """Allowed (alpha, beta) = (#vertices with e even, #with e odd)."""
    N = n * (n - 1) // 2
    V = n - 2
    ev_needed = (N + 1) // 2          # #even values in [0, N-1]
    od_needed = N // 2
    out = []
    for al in range(V + 1):
        be = V - al
        if N % 2 == 0:
            ev = 1 + al + al + al * (al - 1) // 2 + be * (be - 1) // 2
            od = be + be + al * be
        else:
            ev = 1 + al + be + al * be
            od = al + be + al * (al - 1) // 2 + be * (be - 1) // 2
        if ev == ev_needed and od == od_needed:
            out.append((al, be))
    return out


class Search:
    def __init__(self, n, node_limit=None, max_solutions=5, verbose=0):
        self.n = n
        self.N = N = n * (n - 1) // 2
        self.V = V = n - 2
        self.node_limit = node_limit
        self.max_solutions = max_solutions
        self.verbose = verbose
        self.splits = parity_splits(n)
        self.alpha_ok = set(a for a, b in self.splits)
        self.beta_ok = set(b for a, b in self.splits)
        self.amax = max(self.alpha_ok) if self.splits else -1
        self.bmax = max(self.beta_ok) if self.splits else -1
        # mutable state
        self.e = [0] * V           # 0 = unknown
        self.f = [0] * V
        self.nv = 0
        self.alpha = 0
        self.beta = 0
        self.taken = bytearray(N)
        self.taken[0] = 1
        self.pv = [[0] * V for _ in range(V)]     # 0 = undetermined, else value
        self.deferred = []          # list of [i, j, base, hmax]
        self.nodes = 0
        self.solutions = []
        self.bailed = False
        self.no_hc = False
        self.no_attach = False
        self.no_hall = False
        self.no_lb = False
        self.no_ultra = False
        self.no_parity = False
        self.no_cover = False
        self.no_ub = False
        self.force_e_upto = 0   # gaps 1..force_e_upto must all be e-values;
                                # 0 disables (default, changes nothing)
        self.symmetry_break = True   # gap 1 is always a coordinate and a<->b
                                     # may be swapped, so assume 1 in E
        self.cov = [0] * (2 * N + 2)   # #representations w = e+f, e in E u {0}, f in F u {0}
        self.cov[0] = 1
        self.exempt = bytearray(N)     # gaps realised by a tied pair with h_c > 0

    # ---------- helpers ----------
    def h(self, i):
        return (self.N - self.e[i] - self.f[i]) // 2

    def partner_ok(self, i, g):
        """Does the half-known vertex i still admit a partner value > g?"""
        N = self.N
        if self.e[i] and self.f[i]:
            return True
        known = self.e[i] or self.f[i]
        par = (N - known) % 2
        hi = N - known
        for w in range(g, hi + 1):
            if w % 2 == par and not self.taken[w]:
                return True
        return False

    def attach_ok(self):
        """Attachment lemma R1: a vertex with h>0 hangs on a branch attached to
        P at a vertex of T with the same p and h=0; that vertex's coordinates
        are forced to be ((N-d)/2, (N+d)/2) with d = f-e."""
        N = self.N
        for i in range(self.nv):
            if not (self.e[i] and self.f[i]):
                continue
            if self.e[i] + self.f[i] == N:
                continue                      # h = 0, lies on P
            d = self.f[i] - self.e[i]
            if (N - d) % 2:
                return False
            ew = (N - d) // 2
            fw = (N + d) // 2
            if ew < 1 or fw < 1 or ew > N - 1 or fw > N - 1:
                return False
            we = wf = None
            for j in range(self.nv):
                if self.e[j] == ew:
                    we = j
                if self.f[j] == fw:
                    wf = j
            if we is not None and wf is not None:
                if we != wf:
                    return False
                continue
            if we is not None:
                if self.f[we] or self.taken[fw]:
                    return False
                continue
            if wf is not None:
                if self.e[wf] or self.taken[ew]:
                    return False
                continue
            if self.taken[ew] or self.taken[fw]:
                return False
        return True

    def feasible_partner_vals(self, i, g):
        N = self.N
        known = self.e[i] or self.f[i]
        par = (N - known) % 2
        return [w for w in range(g, N - known + 1)
                if w % 2 == par and not self.taken[w]]

    def hall_partners(self, g):
        """Half-known vertices need pairwise distinct partner values."""
        sets = []
        for i in range(self.nv):
            if not (self.e[i] and self.f[i]):
                fv = self.feasible_partner_vals(i, g)
                if not fv:
                    return False
                sets.append(set(fv))
        if len(sets) < 2:
            return True
        # exact bipartite matching (few vertices, so simple augmenting paths)
        match = {}
        for k, S in enumerate(sets):
            seen = set()
            if not self._aug(k, sets, match, seen):
                return False
        return True

    def _aug(self, k, sets, match, seen):
        for v in sets[k]:
            if v in seen:
                continue
            seen.add(v)
            if v not in match or self._aug(match[v], sets, match, seen):
                match[v] = k
                return True
        return False

    def lb_prune(self, g):
        """Hall condition on values: every untaken gap must be supplied either
        by one of the remaining coordinate assignments or by a pair whose value
        lower bound is small enough."""
        N, V = self.N, self.V
        lo = g          # coordinates still unassigned are >= g (one may equal g)
        assigned = 0
        for i in range(self.nv):
            assigned += (1 if self.e[i] else 0) + (1 if self.f[i] else 0)
        R = 2 * V - assigned
        LBs = []
        nv = self.nv
        for i in range(nv):
            for j in range(i + 1, nv):
                if self.pv[i][j] > 0:
                    continue
                if self.pv[i][j] == -1:
                    continue                      # deferred, handled below
                ei, fi, ej, fj = self.e[i], self.f[i], self.e[j], self.f[j]
                lb1 = (fi if fi else lo) + (ej if ej else lo)
                lb2 = (fj if fj else lo) + (ei if ei else lo)
                LBs.append(lb1 if lb1 < lb2 else lb2)
        for (i, j, base, hmax) in self.deferred:
            LBs.append(base if base > g else g)
        fut = V - nv
        if fut:
            for i in range(nv):
                ei, fi = self.e[i], self.f[i]
                c1 = (fi if fi else lo) + lo
                c2 = lo + (ei if ei else lo)
                lb = c1 if c1 < c2 else c2
                LBs.extend([lb] * fut)
            LBs.extend([2 * lo] * (fut * (fut - 1) // 2))
        LBs.sort()
        k = 0
        need = 0
        nlb = len(LBs)
        for t in range(g, N):
            if self.taken[t]:
                continue
            need += 1
            while k < nlb and LBs[k] <= t:
                k += 1
            if need > R + k:
                return False
        return True

    def hc_heights(self, i, j, hc):
        """The meeting point of u,v is a vertex of T.  If h_c > 0 it is a
        vertex w with the same p and height h_c, whose coordinates are then
        forced: e_w = N - p - h_c, f_w = p - h_c.  Either w already exists, or
        both of those values must still be free."""
        if hc == 0:
            return True
        N = self.N
        p = (N + self.f[i] - self.e[i]) // 2
        ew = N - p - hc
        fw = p - hc
        if ew < 1 or fw < 1 or ew > N - 1 or fw > N - 1:
            return False
        for w in range(self.nv):
            if self.e[w] == ew and self.f[w] == fw:
                return True
            if self.e[w] == ew or self.f[w] == fw:
                # a vertex already owns one of the two forced values
                if self.e[w] == ew and not self.f[w] and not self.taken[fw]:
                    return True
                if self.f[w] == fw and not self.e[w] and not self.taken[ew]:
                    return True
                return False
        return not (self.taken[ew] or self.taken[fw])

    def pair_hc(self, x, y):
        v = self.pv[x][y]
        if v <= 0:
            return None
        return (v - (self.f[x] + self.e[y])) // 2

    def ultrametric_ok(self, i, j):
        """LCA heights inside one p-class form a max-ultrametric: for any three
        vertices of the class the smallest of the three meeting heights occurs
        at least twice."""
        hij = self.pair_hc(i, j)
        if hij is None:
            return True
        d = self.f[i] - self.e[i]
        for k in range(self.nv):
            if k == i or k == j or not (self.e[k] and self.f[k]):
                continue
            if self.f[k] - self.e[k] != d:
                continue
            hik = self.pair_hc(i, k)
            hjk = self.pair_hc(j, k)
            if hik is None or hjk is None:
                continue
            m = min(hij, hik, hjk)
            if (hij == m) + (hik == m) + (hjk == m) < 2:
                return False
        # the meeting vertex of i,j is the class vertex w at height h_c(i,j);
        # it must be an ancestor of both, i.e. h_c(i,w) = h_c(j,w) = h_c(i,j)
        if hij > 0:
            for k in range(self.nv):
                if k == i or k == j or not (self.e[k] and self.f[k]):
                    continue
                if self.f[k] - self.e[k] != d:
                    continue
                if (self.N - self.e[k] - self.f[k]) // 2 != hij:
                    continue
                hik = self.pair_hc(i, k)
                hjk = self.pair_hc(j, k)
                if hik is not None and hik != hij:
                    return False
                if hjk is not None and hjk != hij:
                    return False
        return True

    def class_ok(self, i):
        """Run the ultrametric test on every determined pair involving i."""
        if not (self.e[i] and self.f[i]):
            return True
        d = self.f[i] - self.e[i]
        for j in range(self.nv):
            if j == i or not (self.e[j] and self.f[j]):
                continue
            if self.f[j] - self.e[j] != d:
                continue
            if not self.ultrametric_ok(i, j):
                return False
        return True

    def deferred_ok(self, g):
        for (i, j, base, hmax) in self.deferred:
            hit = False
            v = base
            while v <= base + 2 * hmax:
                if v >= g and not self.taken[v]:
                    hit = True
                    break
                v += 2
            if not hit:
                return False
        return True

    # ---------- assignment with propagation ----------
    def assign(self, i, is_e, g, trail):
        """Set coordinate; propagate.  trail collects undo records.
        Returns False on contradiction."""
        N, V = self.N, self.V
        if is_e:
            self.e[i] = g
        else:
            self.f[i] = g
        trail.append(("coord", i, is_e))
        self.cov[g] += 1                       # g + 0
        if is_e:
            for j in range(self.nv):
                if self.f[j]:
                    self.cov[g + self.f[j]] += 1
        else:
            for j in range(self.nv):
                if self.e[j]:
                    self.cov[g + self.e[j]] += 1
        self.taken[g] = 1
        trail.append(("take", g))
        if self.e[i] and self.f[i]:
            if self.e[i] + self.f[i] > N:
                return False
            if (self.e[i] + self.f[i]) % 2 != N % 2:
                return False
        for j in range(self.nv):
            if j == i or self.pv[i][j]:
                continue
            ei, fi, ej, fj = self.e[i], self.f[i], self.e[j], self.f[j]
            c1 = fi + ej if (fi and ej) else 0        # crossing f_i + e_j
            c2 = fj + ei if (fj and ei) else 0
            lo = g + 1
            lb1 = (fi if fi else lo) + (ej if ej else lo)
            lb2 = (fj if fj else lo) + (ei if ei else lo)
            val = 0
            if c1 and c2:
                if c1 != c2:
                    val = c1 if c1 < c2 else c2
                else:
                    hmax = min(self.h(i), self.h(j))
                    if hmax == 0:
                        val = c1
                    else:
                        self.deferred.append([i, j, c1, hmax])
                        self.pv[i][j] = self.pv[j][i] = -1     # deferred marker
                        trail.append(("defer", i, j))
                        continue
            elif c1 and c1 < lb2:
                val = c1
            elif c2 and c2 < lb1:
                val = c2
            if val:
                if val >= N or val <= 0 or self.taken[val]:
                    return False
                self.taken[val] = 1
                self.pv[i][j] = self.pv[j][i] = val
                trail.append(("pair", i, j, val))
        return True

    def undo(self, trail, mark):
        while len(trail) > mark:
            rec = trail.pop()
            k = rec[0]
            if k == "take":
                self.taken[rec[1]] = 0
            elif k == "coord":
                i, is_e = rec[1], rec[2]
                g = self.e[i] if is_e else self.f[i]
                self.cov[g] -= 1
                if is_e:
                    self.e[i] = 0
                    for j in range(self.nv):
                        if self.f[j]:
                            self.cov[g + self.f[j]] -= 1
                else:
                    self.f[i] = 0
                    for j in range(self.nv):
                        if self.e[j]:
                            self.cov[g + self.e[j]] -= 1
            elif k == "pair":
                i, j, val = rec[1], rec[2], rec[3]
                self.pv[i][j] = self.pv[j][i] = 0
                self.taken[val] = 0
            elif k == "defer":
                i, j = rec[1], rec[2]
                self.pv[i][j] = self.pv[j][i] = 0
                for t in range(len(self.deferred) - 1, -1, -1):
                    if self.deferred[t][0] == i and self.deferred[t][1] == j:
                        del self.deferred[t]
                        break
            elif k == "newv":
                self.nv -= 1
                self.e[self.nv] = 0
                self.f[self.nv] = 0
                if rec[1] == 0:
                    self.alpha -= 1
                else:
                    self.beta -= 1
            elif k == "resolve":
                i, j, val, base, hmax, idx = rec[1], rec[2], rec[3], rec[4], rec[5], rec[6]
                if val > base:
                    self.exempt[val] = 0
                self.taken[val] = 0
                self.pv[i][j] = self.pv[j][i] = -1
                # restore at the ORIGINAL index: rec() must be state-neutral,
                # otherwise the branch->shard assignment shifts under --split
                self.deferred.insert(idx, [i, j, base, hmax])

    # ---------- main recursion ----------
    def _dist_lb(self, i, j, g):
        """Lower bound on d(u_i,u_j) from |d(a,u)-d(a,v)| = |e_i-e_j| and the
        same on the b side; unknown coordinates are >= g."""
        lb = 1
        ei, fi, ej, fj = self.e[i], self.f[i], self.e[j], self.f[j]
        if ei and ej:
            v = ei - ej
            lb = max(lb, v if v > 0 else -v)
        elif ei:
            lb = max(lb, g - ei)
        elif ej:
            lb = max(lb, g - ej)
        if fi and fj:
            v = fi - fj
            lb = max(lb, v if v > 0 else -v)
        elif fi:
            lb = max(lb, g - fi)
        elif fj:
            lb = max(lb, g - fj)
        return lb

    def _h_ub(self, i, g):
        if self.e[i] and self.f[i]:
            return (self.N - self.e[i] - self.f[i]) // 2
        known = self.e[i] or self.f[i]
        return (self.N - known - g) // 2

    def ub_prune(self, g):
        """Dual Hall condition: every untaken gap must be supplied by a
        remaining coordinate or a pair whose value upper bound is large
        enough.  All remaining coordinates are <= N - g for a vertex not yet
        created (both of its coordinates are >= g and sum to <= N) and
        <= N - known for a half-known vertex."""
        N, V = self.N, self.V
        nv, fut = self.nv, V - self.nv
        UB = []
        for i in range(nv):
            if self.e[i] and self.f[i]:
                continue
            UB.append(N - (self.e[i] or self.f[i]))
        if fut:
            UB.extend([N - g] * (2 * fut))
        defwin = {}
        for (a_, b_, base, hmax) in self.deferred:
            defwin[(a_, b_)] = base + 2 * hmax
        for i in range(nv):
            for j in range(i + 1, nv):
                v = self.pv[i][j]
                if v > 0:
                    continue
                if v == -1:
                    UB.append(defwin.get((i, j), N - 1))
                    continue
                u = N - self._dist_lb(i, j, g)
                ei, fi, ej, fj = self.e[i], self.f[i], self.e[j], self.f[j]
                c1 = fi + ej if (fi and ej) else 0
                c2 = fj + ei if (fj and ei) else 0
                if c1 or c2:
                    c = c1 if c1 else c2
                    if c1 and c2:
                        c = c1 if c1 > c2 else c2
                    hh = self._h_ub(i, g)
                    hj = self._h_ub(j, g)
                    u = min(u, c + 2 * (hh if hh < hj else hj))
                UB.append(u if u < N - 1 else N - 1)
            if fut:
                m = self.e[i] or 0
                mf = self.f[i] or 0
                lo = m if (m and (not mf or m < mf)) else mf
                UB.extend([min(N - 1, N - max(1, g - lo))] * fut)
        if fut > 1:
            UB.extend([N - 1] * (fut * (fut - 1) // 2))
        UB.sort(reverse=True)
        k = 0
        need = 0
        m = len(UB)
        for t in range(N - 1, g - 1, -1):
            if self.taken[t]:
                continue
            need += 1
            while k < m and UB[k] >= t:
                k += 1
            if need > k:
                return False
        return True

    def cover_ok(self, g):
        """Covering lemma: every w in [0,N-1] is e+f for some e in E u {0},
        f in F u {0}, except gaps realised by a tied pair with h_c > 0.  For
        w < g every e,f that could represent w is already assigned, so the
        test is exact on that range."""
        cov = self.cov
        ex = self.exempt
        for w in range(g):
            if cov[w] == 0 and not ex[w]:
                return False
        return True

    def rescan(self, g, trail):
        """As g grows, the lower bound on every still-unknown coordinate rises,
        so pairs that were undetermined can become determined without any new
        assignment.  Re-derive them.  Returns True if anything was marked,
        None on contradiction."""
        changed = False
        lo = g
        for i in range(self.nv):
            for j in range(i + 1, self.nv):
                if self.pv[i][j]:
                    continue
                ei, fi, ej, fj = self.e[i], self.f[i], self.e[j], self.f[j]
                c1 = fi + ej if (fi and ej) else 0
                c2 = fj + ei if (fj and ei) else 0
                lb1 = (fi if fi else lo) + (ej if ej else lo)
                lb2 = (fj if fj else lo) + (ei if ei else lo)
                val = 0
                if c1 and c2:
                    if c1 != c2:
                        val = c1 if c1 < c2 else c2
                    else:
                        hmax = min(self.h(i), self.h(j))
                        if hmax == 0:
                            val = c1
                        else:
                            self.deferred.append([i, j, c1, hmax])
                            self.pv[i][j] = self.pv[j][i] = -1
                            trail.append(("defer", i, j))
                            changed = True
                            continue
                elif c1 and c1 < lb2:
                    val = c1
                elif c2 and c2 < lb1:
                    val = c2
                if val:
                    if val >= self.N or val <= 0 or self.taken[val]:
                        return None
                    self.taken[val] = 1
                    self.pv[i][j] = self.pv[j][i] = val
                    trail.append(("pair", i, j, val))
                    changed = True
        return changed

    def rec(self, g):
        self.nodes += 1
        if self.node_limit and self.nodes > self.node_limit:
            self.bailed = True
            return
        N, V = self.N, self.V
        trail0 = []
        try:
            return self._rec_body(g, trail0)
        finally:
            self.undo(trail0, 0)

    def _rec_body(self, g, trail0):
        N, V = self.N, self.V
        while True:
            while g < N and self.taken[g]:
                g += 1
            if g >= N:
                break
            ch = self.rescan(g, trail0)
            if ch is None:
                return
            if not ch:
                break
        if g >= N:
            if self.nv == V and all(self.e) and all(self.f) and not self.deferred:
                self.record()
            return
        # global prunes
        if not self.deferred_ok(g):
            return
        for i in range(self.nv):
            if not (self.e[i] and self.f[i]) and not self.partner_ok(i, g):
                return
        if not self.no_hall and not self.hall_partners(g):
            return
        if not self.no_lb and not self.lb_prune(g):
            return
        if not self.no_cover and not self.cover_ok(g):
            return
        if not self.no_ub and not self.ub_prune(g):
            return
        trail = []
        # ---- option 1: resolve a deferred tied pair at value g
        # NOTE: iterate over a snapshot -- undo() re-appends restored entries at
        # the end of self.deferred, so live indices are not stable.
        for (i, j, base, hmax) in ([] if g <= self.force_e_upto
                                   else [tuple(x) for x in self.deferred]):
            if base <= g <= base + 2 * hmax and (g - base) % 2 == 0 \
                    and (self.no_hc or self.hc_heights(i, j, (g - base) // 2)):
                mark = len(trail)
                idx = next(t for t, x in enumerate(self.deferred)
                           if x[0] == i and x[1] == j)
                del self.deferred[idx]
                self.pv[i][j] = self.pv[j][i] = g
                self.taken[g] = 1
                if g > base:
                    self.exempt[g] = 1
                trail.append(("resolve", i, j, g, base, hmax, idx))
                if self.no_ultra or self.ultrametric_ok(i, j):
                    self.rec(g + 1)
                self.undo(trail, mark)
                if len(self.solutions) >= self.max_solutions or self.bailed:
                    return
        # ---- option 2: g is a coordinate
        cands = []
        eonly = g <= self.force_e_upto
        for i in range(self.nv):
            if not self.e[i] and (self.f[i] + g) % 2 == N % 2 and self.f[i] + g <= N:
                cands.append((i, True))
            if not eonly and not self.f[i] and (self.e[i] + g) % 2 == N % 2 \
                    and self.e[i] + g <= N:
                cands.append((i, False))
        for (i, is_e) in cands:
            mark = len(trail)
            ok = self.assign(i, is_e, g, trail) and (self.no_attach or self.attach_ok()) and (self.no_ultra or self.class_ok(i))
            if ok:
                self.rec(g + 1)
            self.undo(trail, mark)
            if len(self.solutions) >= self.max_solutions or self.bailed:
                return
        if self.nv < V:
            sides = (True,) if (eonly or (self.symmetry_break and self.nv == 0)) \
                else (True, False)
            for is_e in sides:
                par = g % 2
                # new vertex: the known coordinate is g, the other is unknown
                al = self.alpha + (1 if (g % 2 == 0 if is_e else (N - g) % 2 == 0) else 0)
                be = self.nv + 1 - al
                if not self.no_parity and (al > self.amax or be > self.bmax):
                    continue
                mark = len(trail)
                i = self.nv
                self.nv += 1
                eps = 0 if ((g % 2) if is_e else ((N - g) % 2)) == 0 else 1
                if eps == 0:
                    self.alpha += 1
                else:
                    self.beta += 1
                trail.append(("newv", eps))
                ok = self.assign(i, is_e, g, trail) and (self.no_attach or self.attach_ok()) and (self.no_ultra or self.class_ok(i))
                if ok:
                    self.rec(g + 1)
                self.undo(trail, mark)
                if len(self.solutions) >= self.max_solutions or self.bailed:
                    return

    def record(self):
        sol = {"e": list(self.e), "f": list(self.f),
               "pairs": [[self.pv[i][j] for j in range(self.V)] for i in range(self.V)]}
        self.solutions.append(sol)
        if self.verbose:
            print("SOLUTION", sol["e"], sol["f"], flush=True)

    def run(self):
        t0 = time.time()
        if not self.splits:
            return {"n": self.n, "status": "PARITY_IMPOSSIBLE", "solutions": [],
                    "nodes": 0, "seconds": 0.0}
        self.rec(1)
        return {"n": self.n, "N": self.N, "V": self.V,
                "status": ("BAILED" if self.bailed else
                           ("SOLUTIONS" if self.solutions else "EMPTY_EXHAUSTED")),
                "parity_splits": self.splits,
                "solutions": self.solutions, "nodes": self.nodes,
                "seconds": round(time.time() - t0, 3)}


# ---------------- verification of a found solution ----------------
def verify_solution(n, e, f, pv):
    """Rebuild an explicit tree from (e,f,pair-gaps) and check by BFS that its
    distance set is exactly {1..N}.  Returns (ok, message)."""
    N = n * (n - 1) // 2
    V = n - 2
    P = [( (N + f[i] - e[i]) // 2, (N - e[i] - f[i]) // 2 ) for i in range(V)]
    # vertex ids: 0 = a, 1 = b, 2+i = i-th
    adj = {}
    def add(u, v, w):
        if w <= 0:
            raise ValueError("non-positive edge weight %d" % w)
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    # on-path vertices
    onp = sorted([(P[i][0], 2 + i) for i in range(V) if P[i][1] == 0])
    chain = [(0, 0)] + onp + [(N, 1)]
    for k in range(len(chain) - 1):
        add(chain[k][1], chain[k + 1][1], chain[k + 1][0] - chain[k][0])
    # branches, grouped by p
    byp = {}
    for i in range(V):
        if P[i][1] > 0:
            byp.setdefault(P[i][0], []).append(i)
    rootp = {p: v for p, v in onp}
    for p, mem in byp.items():
        if p not in rootp:
            return False, "no on-path attachment vertex at p=%d" % p
        # hc(u,v) from the recorded gap
        def hc(i, j):
            base = f[i] + e[j]
            return (pv[i][j] - base) // 2
        mem.sort(key=lambda i: P[i][1])
        for idx, i in enumerate(mem):
            best, bh = rootp[p], 0
            for j in mem[:idx]:
                hj = P[j][1]
                if hj < P[i][1] and hc(i, j) == hj and hj > bh:
                    best, bh = 2 + j, hj
            add(best, 2 + i, P[i][1] - bh)
    # BFS all-pairs
    import collections
    nodes = list(adj.keys())
    if len(nodes) != n:
        return False, "tree has %d vertices, expected %d" % (len(nodes), n)
    dists = []
    for s in nodes:
        dist = {s: 0}
        dq = collections.deque([s])
        while dq:
            u = dq.popleft()
            for (v, w) in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + w
                    dq.append(v)
        if len(dist) != n:
            return False, "not connected"
        for v in nodes:
            if v > s:
                dists.append(dist[v])
    dists.sort()
    if dists != list(range(1, N + 1)):
        return False, "distance multiset wrong: %s" % dists[:12]
    return True, "tree verified, edges=%s" % sorted(
        (min(u, v), max(u, v), w) for u in adj for (v, w) in adj[u] if u < v)


if __name__ == "__main__":
    n = int(sys.argv[1])
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else None
    s = Search(n, node_limit=lim, max_solutions=200, verbose=1)
    res = s.run()
    print(json.dumps({k: v for k, v in res.items() if k != "solutions"}, indent=1))
    print("solutions found:", len(res["solutions"]))
    for sol in res["solutions"]:
        ok, msg = verify_solution(n, sol["e"], sol["f"], sol["pairs"])
        print("  e=%s f=%s -> %s %s" % (sol["e"], sol["f"], "OK" if ok else "REJECT", msg[:160]))
