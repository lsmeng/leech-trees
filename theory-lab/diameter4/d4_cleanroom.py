#!/usr/bin/env python3
"""Exhaustive forced-forest search for Leech trees of hop-diameter <= 4, fixed order n.

Soundness/completeness basis (all proved in repo docs/theory-notes.md or below):
  * Forcing lemma (Calhoun 2007 Lem 2.6): in a Leech tree with sorted weights
    w_1 < ... < w_{n-1}, w_k = least positive integer not realised as a distance
    in the forest formed by the edges of weights w_1..w_{k-1}.
    => enumerate forests by adding, at step k, an edge of exactly that forced
    weight, in every inequivalent position.
  * All distances in any subforest of a Leech tree are distinct and <= N.
  * Diameter invariant (proved in the report): in a subforest of a tree of hop
    diameter <= 4, every component has hop diameter <= 4 and at most one
    component has hop diameter >= 3.  Conversely any forest satisfying this is
    completable to a hop-diameter-<=4 tree (attach star centres to a 2-centre).
  * Final acceptance: k = n-1 edges, one component (then #vertices = n
    automatically), all C(n,2) distances distinct and <= N  =>  they are
    exactly {1..N}  => Leech.
Automorphism note: with all edge weights distinct, the only automorphism of any
reachable forest is the endpoint swap of a single-edge component; we kill it by
designating the smaller-id endpoint of single-edge components as the unique
attachment point.  Forests determine their own history (edges sorted by weight),
so no cross-branch duplication is possible; the search tree has no repeats.
"""
import sys, time, json

def search(n, time_limit=None, verbose=False):
    N = n * (n - 1) // 2
    E_target = n - 1
    # state ------------------------------------------------------------------
    comp_of = {}        # vertex -> component id
    comp_verts = {}     # cid -> list of vertices (in creation order)
    cdiam = {}          # cid -> hop diameter
    wd = {}             # (u,v) sorted -> weighted distance   (within components)
    hd = {}             # (u,v) sorted -> hop distance
    realized = set()    # set of weighted distances present
    edges = []          # (u,v,w) placement log
    single_edge = {}    # cid -> True if component is a single edge (for symmetry)
    solutions = []
    stats = {"nodes": 0, "maxk": 0, "t0": time.time(), "timeout": False}

    def pk(a, b):
        return (a, b) if a < b else (b, a)

    def check_time():
        if time_limit is not None and time.time() - stats["t0"] > time_limit:
            stats["timeout"] = True
            return True
        return False

    def forced_weight():
        m = 1
        while m in realized:
            m += 1
        return m

    def n_big():
        return sum(1 for d in cdiam.values() if d >= 3)

    def rec(k, next_vid, next_cid):
        if stats["timeout"] or check_time():
            return
        stats["nodes"] += 1
        stats["maxk"] = max(stats["maxk"], k)
        if k == E_target:
            if len(comp_verts) == 1:
                # all distances distinct (enforced) and <= N (enforced); count = C(n,2)
                if len(realized) != N:
                    raise RuntimeError(("terminal distance count", n, len(realized), N))
                solutions.append(list(edges))
            return
        C = len(comp_verts)
        if C - 1 > E_target - k:      # cannot connect any more
            return
        m = forced_weight()
        if m > N:
            return
        # containment bound (Lemma 4c): every final edge has c_e >= n-1, so every
        # future weight (in particular m) is <= N + 1 - (n-1).
        if m > N - n + 2:
            return
        nbig = n_big()

        # cross-assembly prune: each component attaches to the final 2-centre c by
        # an edge from its attach vertex (star centre / big-comp centre); at most
        # one component contains c.  Future join weights are distinct, >= m.
        # For comps A,B the eventual leaf-leaf cross distance is >=
        #   ecc(A) + ecc(B) + m           (if c in A or B; one join)
        #   ecc(A) + ecc(B) + 2m+1        (c elsewhere; two distinct joins)
        # where ecc = max weighted distance from the attach vertex (= max over
        # centre candidates when the comp is big).  All distances <= N.
        if C >= 2:
            eccs = []
            for cid0, verts in comp_verts.items():
                if cdiam[cid0] <= 2:
                    # star: attach/centre vertex has ecc = max incident..., for a
                    # single edge or star the centre's weighted ecc = max edge wt =
                    # max leaf distance; compute via min over vertices of max wd
                    best = None
                    for z in verts:
                        e = max((wd[pk(z, u)] for u in verts if u != z), default=0)
                        best = e if best is None else min(best, e)
                    eccs.append(best)
                else:
                    # big comp: centre candidates = vertices with hop ecc <= 2
                    best = None
                    for z in verts:
                        if max((hd[pk(z, u)] for u in verts if u != z), default=0) <= 2:
                            e = max((wd[pk(z, u)] for u in verts if u != z), default=0)
                            best = e if best is None else min(best, e)
                    if best is None:
                        return  # no valid centre: dead (should not happen)
                    eccs.append(best)
            eccs.sort(reverse=True)
            if eccs[0] + eccs[1] + m > N:
                return
            # at most one component contains c; any two c-free comps need two
            # distinct future joins with weights >= m, m+1:
            if C >= 3 and eccs[1] + eccs[2] + 2 * m + 1 > N:
                return

        # move (a): fresh single-edge component --------------------------------
        # needs room: after move, C+1 comps, k+1 edges: (C+1)-1 <= E_target-(k+1)
        if C <= E_target - k - 1:
            u, v = next_vid, next_vid + 1
            cid = next_cid
            comp_of[u] = comp_of[v] = cid
            comp_verts[cid] = [u, v]
            cdiam[cid] = 1
            wd[(u, v)] = m; hd[(u, v)] = 1
            realized.add(m)
            edges.append((u, v, m))
            single_edge[cid] = True
            rec(k + 1, next_vid + 2, next_cid + 1)
            del single_edge[cid]
            edges.pop()
            realized.discard(m)
            del wd[(u, v)], hd[(u, v)]
            del comp_verts[cid], cdiam[cid], comp_of[u], comp_of[v]
            if stats["timeout"]: return

        # move (b): pendant vertex at existing vertex z ------------------------
        for cid0 in list(comp_verts.keys()):
            verts = comp_verts[cid0]
            zs = [verts[0]] if single_edge.get(cid0) else verts
            for z in zs:
                # new hop ecc of z + 1 <= 4 ; diameter update
                ecc = max((hd[pk(z, u)] for u in verts if u != z), default=0)
                ndiam = max(cdiam[cid0], ecc + 1)
                if ndiam > 4:
                    continue
                if ndiam >= 3 and cdiam[cid0] < 3 and nbig >= 1:
                    continue  # would create a second big component
                # weighted collision checks
                newvals = [m]
                ok = m not in realized
                if ok:
                    for u in verts:
                        if u == z: continue
                        val = m + wd[pk(z, u)]
                        if val > N or val in realized:
                            ok = False; break
                        newvals.append(val)
                # internal dups impossible: wd[z,u] distinct over u
                if not ok:
                    continue
                t = next_vid
                comp_of[t] = cid0
                verts.append(t)
                olddiam = cdiam[cid0]; cdiam[cid0] = ndiam
                wassingle = single_edge.pop(cid0, False)
                for u in verts[:-1]:
                    if u == z: continue
                    wd[pk(t, u)] = m + wd[pk(z, u)]
                    hd[pk(t, u)] = 1 + hd[pk(z, u)]
                wd[pk(t, z)] = m; hd[pk(t, z)] = 1
                realized.update(newvals)
                edges.append((z, t, m))
                rec(k + 1, next_vid + 1, next_cid)
                edges.pop()
                realized.difference_update(newvals)
                for u in verts[:-1]:
                    if u == z: continue
                    del wd[pk(t, u)], hd[pk(t, u)]
                del wd[pk(t, z)], hd[pk(t, z)]
                if wassingle: single_edge[cid0] = True
                cdiam[cid0] = olddiam
                verts.pop()
                del comp_of[t]
                if stats["timeout"]: return

        # move (c): join two components with edge (u in A, v in B) -------------
        cids = list(comp_verts.keys())
        for ia in range(len(cids)):
            for ib in range(ia + 1, len(cids)):
                A, B = cids[ia], cids[ib]
                va, vb = comp_verts[A], comp_verts[B]
                ua_list = [va[0]] if single_edge.get(A) else va
                ub_list = [vb[0]] if single_edge.get(B) else vb
                for u in ua_list:
                    ecc_u = max((hd[pk(u, x)] for x in va if x != u), default=0)
                    for v in ub_list:
                        ecc_v = max((hd[pk(v, y)] for y in vb if y != v), default=0)
                        ndiam = max(cdiam[A], cdiam[B], ecc_u + 1 + ecc_v)
                        if ndiam > 4:
                            continue
                        extra_big = (1 if cdiam[A] >= 3 else 0) + (1 if cdiam[B] >= 3 else 0)
                        if ndiam >= 3 and nbig - extra_big >= 1:
                            continue  # another big component elsewhere
                        # weighted collision checks over the |A|x|B| new pairs
                        newvals = []
                        seen_ok = True
                        for x in va:
                            dxu = wd[pk(x, u)] if x != u else 0
                            base = dxu + m
                            if base > N: seen_ok = False; break
                            for y in vb:
                                val = base + (wd[pk(v, y)] if y != v else 0)
                                if val > N or val in realized:
                                    seen_ok = False; break
                                newvals.append(val)
                            if not seen_ok: break
                        if seen_ok and len(set(newvals)) != len(newvals):
                            seen_ok = False
                        if not seen_ok:
                            continue
                        # apply: merge B into A
                        for x in va:
                            dxu = wd[pk(x, u)] if x != u else 0
                            hxu = hd[pk(x, u)] if x != u else 0
                            for y in vb:
                                wd[pk(x, y)] = dxu + m + (wd[pk(v, y)] if y != v else 0)
                                hd[pk(x, y)] = hxu + 1 + (hd[pk(v, y)] if y != v else 0)
                        for y in vb:
                            comp_of[y] = A
                        old_va_len = len(va)
                        va.extend(vb)
                        oldA_diam = cdiam[A]
                        cdiam[A] = ndiam
                        saveB = comp_verts.pop(B); saveBdiam = cdiam.pop(B)
                        wasA = single_edge.pop(A, False); wasB = single_edge.pop(B, False)
                        realized.update(newvals)
                        edges.append((u, v, m))
                        rec(k + 1, next_vid, next_cid)
                        edges.pop()
                        realized.difference_update(newvals)
                        if wasA: single_edge[A] = True
                        if wasB: single_edge[B] = True
                        comp_verts[B] = saveB; cdiam[B] = saveBdiam
                        cdiam[A] = oldA_diam
                        del va[old_va_len:]
                        for y in vb:
                            comp_of[y] = B
                        for x in va:
                            for y in vb:
                                del wd[pk(x, y)], hd[pk(x, y)]
                        if stats["timeout"]: return

    rec(0, 0, 0)
    stats["time"] = time.time() - stats["t0"]
    return solutions, stats


def verify_leech(n, edges):
    """independent check: rebuild distances by Floyd-style BFS on the tree"""
    import itertools
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w)); adj.setdefault(v, []).append((u, w))
    vs = sorted(adj)
    if len(vs) != n or len(edges) != n - 1:
        return False
    dists = []
    for s in vs:
        # BFS
        d = {s: 0}; st = [s]
        while st:
            x = st.pop()
            for y, w in adj[x]:
                if y not in d:
                    d[y] = d[x] + w; st.append(y)
        for t in vs:
            if t > s: dists.append(d[t])
    N = n * (n - 1) // 2
    return sorted(dists) == list(range(1, N + 1))


if __name__ == "__main__":
    if sys.flags.optimize:
        raise RuntimeError("run without python -O/-OO")
    ns = [int(a) for a in sys.argv[1].split(",")]
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else None
    for n in ns:
        sols, st = search(n, time_limit=tl)
        for s in sols:
            if not verify_leech(n, s):
                raise RuntimeError(("invalid clean-room solution", n, s))
        status = "TIMEOUT" if st["timeout"] else "complete"
        print(f"n={n:3d} N={n*(n-1)//2:5d}  solutions={len(sols)}  nodes={st['nodes']:>12,}  "
              f"maxdepth={st['maxk']}  time={st['time']:.2f}s  [{status}]", flush=True)
        for s in sols:
            print("   ", s, flush=True)
