#!/usr/bin/env python3
"""E1/E2/E3 numerical experiments: forced-forest random sampler + additive-combinatorics
measurements (difference-set occupation, death-point histogram, containment-bound slack).

Model (Calhoun forcing lemma, as used in the repo's exhaustive search):
  - build a forest, edges added in increasing weight order;
  - the next edge weight is FORCED: m = least positive integer not realised as a distance;
  - a placement is legal iff every newly created pairwise distance is fresh (not yet realised),
    all distances stay <= N = n(n-1)/2, vertex count stays <= n, and the vertex deficit
    n - V remains coverable by the remaining edges (each edge adds <= 2 new vertices);
  - placements: NEW (fresh 2-vertex component), ATTACH (new leaf at existing vertex),
    JOIN (edge between two existing vertices in different components).
  - a run dies when the forced value m has no legal placement (or m > N); a run that places
    n-1 edges has, by construction, distances exactly {1..N} on n vertices => a Leech tree.

Sampling: uniform over legal placements (shuffle all candidates, take first legal -- the
first legal element of a uniformly shuffled list is uniform over the legal subset).
"""
import sys, os, json, random, time
from collections import defaultdict
from math import comb
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------------------------------
# core sampler
# --------------------------------------------------------------------------------------
def run_once(n, rng):
    """One forced random run. Returns (depth, edges, tstar, completed).
    edges: list of (u, v, w). tstar = forced value at death (None if completed)."""
    N = n * (n - 1) // 2
    V = 0
    comp = {}                       # vertex -> component id
    comps = defaultdict(list)      # cid -> [vertices]
    dist = {}                       # (u,v) u<v -> d   (within components)
    used = set()                    # realised distances
    edges = []
    next_cid = 0

    while len(edges) < n - 1:
        # forced value
        m = 1
        while m in used:
            m += 1
        if m > N:
            return len(edges), edges, m, False
        rem_after = (n - 1) - (len(edges) + 1)

        # enumerate candidates
        cands = [('new',)]
        verts = list(comp.keys())
        for x in verts:
            cands.append(('attach', x))
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                x, y = verts[i], verts[j]
                if comp[x] != comp[y]:
                    cands.append(('join', x, y))
        rng.shuffle(cands)

        placed = False
        for c in cands:
            if c[0] == 'new':
                if V + 2 > n:
                    continue
                if n - (V + 2) > 2 * rem_after:
                    continue
                # distance m is fresh by construction of m
                u, v = V, V + 1
                comp[u] = comp[v] = next_cid
                comps[next_cid] = [u, v]
                next_cid += 1
                dist[(u, v)] = m
                used.add(m)
                edges.append((u, v, m))
                V += 2
                placed = True
                break
            elif c[0] == 'attach':
                if V + 1 > n or n - (V + 1) > 2 * rem_after:
                    continue
                x = c[1]
                cid = comp[x]
                nd = []
                ok = True
                for z in comps[cid]:
                    d = m if z == x else m + dist[(min(x, z), max(x, z))]
                    if d > N or d in used:
                        ok = False
                        break
                    nd.append((z, d))
                if not ok:
                    continue
                u = V
                comp[u] = cid
                for z, d in nd:
                    dist[(min(u, z), max(u, z))] = d
                    used.add(d)
                comps[cid].append(u)
                edges.append((x, u, m))
                V += 1
                placed = True
                break
            else:  # join
                x, y = c[1], c[2]
                if n - V > 2 * rem_after:
                    continue
                ca, cb = comp[x], comp[y]
                nd = []
                fresh = set()
                ok = True
                for a in comps[ca]:
                    da = 0 if a == x else dist[(min(a, x), max(a, x))]
                    for b in comps[cb]:
                        db = 0 if b == y else dist[(min(y, b), max(y, b))]
                        d = da + m + db
                        if d > N or d in used or d in fresh:
                            ok = False
                            break
                        fresh.add(d)
                        nd.append((a, b, d))
                    if not ok:
                        break
                if not ok:
                    continue
                for a, b, d in nd:
                    dist[(min(a, b), max(a, b))] = d
                    used.add(d)
                merged = comps[ca] + comps[cb]
                for z in comps[cb]:
                    comp[z] = ca
                comps[ca] = merged
                del comps[cb]
                edges.append((x, y, m))
                placed = True
                break

        if not placed:
            return len(edges), edges, m, False

    return len(edges), edges, None, True


def worker(args):
    n, nruns, seed, topk = args
    rng = random.Random(seed)
    deaths = []          # (depth, tstar, ncomp)
    best = []            # (depth, edges) top-k by depth, any shape
    best_tree = []       # (depth, edges) top-k by depth among single-component deaths
    completed = 0
    for _ in range(nruns):
        depth, edges, tstar, done = run_once(n, rng)
        if done:
            completed += 1
            best.append((depth, edges))
            continue
        vs = set()
        for u, v, w in edges:
            vs.add(u); vs.add(v)
        ncomp = len(vs) - len(edges)
        deaths.append((depth, tstar, ncomp))
        for lst, cond in ((best, True), (best_tree, ncomp == 1)):
            if not cond:
                continue
            if len(lst) < topk:
                lst.append((depth, edges))
                lst.sort(key=lambda t: -t[0])
            elif depth > lst[-1][0]:
                lst[-1] = (depth, edges)
                lst.sort(key=lambda t: -t[0])
    return deaths, best, best_tree, completed


def sample_n(n, nruns, topk=150, nproc=3, seed0=1):
    per = nruns // nproc
    args = [(n, per, seed0 + 1000 * i + n, topk) for i in range(nproc)]
    with Pool(nproc) as p:
        parts = p.map(worker, args)
    deaths = []
    best = []
    best_tree = []
    completed = 0
    for d, b, bt, c in parts:
        deaths.extend(d)
        best.extend(b)
        best_tree.extend(bt)
        completed += c
    best.sort(key=lambda t: -t[0])
    best_tree.sort(key=lambda t: -t[0])
    return deaths, best[:topk], best_tree[:topk], completed


# --------------------------------------------------------------------------------------
# tree analysis
# --------------------------------------------------------------------------------------
def components(edges):
    adj = defaultdict(list)
    vs = set()
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
        vs.add(u); vs.add(v)
    seen = set()
    comps = []
    for s in vs:
        if s in seen:
            continue
        stack = [s]
        seen.add(s)
        cc = [s]
        while stack:
            x = stack.pop()
            for y, w in adj[x]:
                if y not in seen:
                    seen.add(y)
                    cc.append(y)
                    stack.append(y)
        comps.append(cc)
    return comps, adj


def all_dists_from(v, adj, verts):
    d = {v: 0}
    stack = [v]
    while stack:
        x = stack.pop()
        for y, w in adj[x]:
            if y not in d:
                d[y] = d[x] + w
                stack.append(y)
    return d


def analyze_component(cc, adj, N):
    """A/B occupation analysis on tree component cc. Returns per-vertex records + centroid."""
    nv = len(cc)
    dfrom = {v: all_dists_from(v, adj, cc) for v in cc}
    deg = {v: len(adj[v]) for v in cc}

    # centroid: minimise max branch size
    def max_branch(v):
        best = 0
        seen = {v}
        for y, w in adj[v]:
            # size of branch through y
            stack = [y]
            seen2 = {v, y}
            sz = 1
            while stack:
                x = stack.pop()
                for z, w2 in adj[x]:
                    if z not in seen2:
                        seen2.add(z)
                        sz += 1
                        stack.append(z)
            best = max(best, sz)
        return best
    centroid = min(cc, key=max_branch)

    recs = {}
    for v in cc:
        leaves = [(y, w) for y, w in adj[v] if deg[y] == 1]
        B = sorted(w for y, w in leaves)
        leafset = set(y for y, w in leaves)
        A = sorted([0] + [dfrom[v][x] for x in cc if x != v and x not in leafset])
        # A distinctness (should hold in any legal state)
        a_distinct = len(A) == len(set(A))
        D = set()
        for i in range(len(A)):
            for j in range(len(A)):
                D.add(A[i] - A[j])
        BB = set()
        for i in range(len(B)):
            for j in range(len(B)):
                BB.add(B[i] - B[j])
        inter = (D & BB) - {0}
        maxA = max(A) if A else 0
        occ_maxA = len(D) / (2 * maxA + 1) if maxA > 0 else 1.0
        occ_N = len(D) / (2 * N + 1)
        # cross-branch sum-distinctness at v
        branches = []
        for y, w in adj[v]:
            stack = [y]
            seen2 = {v, y}
            br = [y]
            while stack:
                x = stack.pop()
                for z, w2 in adj[x]:
                    if z not in seen2:
                        seen2.add(z)
                        br.append(z)
                        stack.append(z)
            branches.append(br)
        sums = []
        for bi in range(len(branches)):
            for bj in range(bi + 1, len(branches)):
                for x in branches[bi]:
                    for y in branches[bj]:
                        sums.append(dfrom[v][x] + dfrom[v][y])
        cross_ok = len(sums) == len(set(sums))
        recs[v] = dict(k=len(B), lenA=len(A), maxA=maxA, sizeD=len(D),
                       occ_maxA=occ_maxA, occ_N=occ_N,
                       AB_disjoint=(len(inter) == 0), n_AB_violations=len(inter),
                       A_distinct=a_distinct, cross_ok=cross_ok)
    return recs, centroid, nv


def pair_products(cc, adj):
    """For every pair (x,y) in tree cc: s_x*s_y with s_x = size of x's side component
    when deleting edge (x, first-step-toward-y)."""
    # subtree sizes: for each directed edge (u->y), size of component containing y in T-(u,y)
    sz = {}
    def size_dir(u, y):
        if (u, y) in sz:
            return sz[(u, y)]
        stack = [y]
        seen = {u, y}
        s = 1
        while stack:
            x = stack.pop()
            for z, w in adj[x]:
                if z not in seen:
                    seen.add(z)
                    s += 1
                    stack.append(z)
        sz[(u, y)] = s
        return s
    # first step toward y from x
    nxt = {}
    for v in cc:
        # BFS recording parents
        par = {v: None}
        stack = [v]
        order = []
        while stack:
            x = stack.pop()
            order.append(x)
            for z, w in adj[x]:
                if z not in par:
                    par[z] = x
                    stack.append(z)
        for y in cc:
            if y == v:
                continue
            # walk from y up to v, first step from v is last hop
            x = y
            while par[x] != v:
                x = par[x]
            nxt[(v, y)] = x
    nv = len(cc)
    prods = []
    for i in range(nv):
        for j in range(i + 1, nv):
            x, y = cc[i], cc[j]
            a = nxt[(x, y)]
            b = nxt[(y, x)]
            s_x = nv - size_dir(x, a)
            s_y = nv - size_dir(y, b)
            prods.append(s_x * s_y)
    return prods


def analyze_state(edges, n):
    N = n * (n - 1) // 2
    comps, adj = components(edges)
    comps.sort(key=len, reverse=True)
    cc = comps[0]
    recs, centroid, nv = analyze_component(cc, adj, N)
    best_v = max(recs, key=lambda v: recs[v]['occ_maxA'])
    prods = pair_products(cc, adj)
    return dict(n=n, N=N, ncomp=len(comps), main_size=nv,
                depth=len(edges),
                centroid=recs[centroid], best=recs[best_v],
                all_AB_ok=all(r['AB_disjoint'] for r in recs.values()),
                all_cross_ok=all(r['cross_ok'] for r in recs.values()),
                all_A_distinct=all(r['A_distinct'] for r in recs.values()),
                prods=sorted(prods))


# --------------------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------------------
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    os.nice(10)
    t0 = time.time()

    if mode == 'sanity':
        # n=6 should complete sometimes and reproduce a Leech tree
        deaths, best, best_tree, completed = sample_n(6, 30000, topk=5, nproc=3)
        print(f"n=6: {completed} completions / 30000 runs")
        for depth, edges in best[:3]:
            print(depth, edges)
        return

    plan = {11: 300000, 16: 300000, 18: 300000}
    if mode == 'quick':
        plan = {11: 3000, 16: 3000, 18: 3000}
    out = {}
    for n, nruns in plan.items():
        t1 = time.time()
        deaths, best, best_tree, completed = sample_n(n, nruns, topk=300, nproc=3)
        out[n] = dict(nruns=nruns, completed=completed,
                      deaths=deaths, best=[(d, e) for d, e in best],
                      best_tree=[(d, e) for d, e in best_tree])
        depths = [d for d, t, c in deaths]
        td = [d for d, e in best_tree] or [0]
        print(f"n={n}: {nruns} runs in {time.time()-t1:.0f}s, completed={completed}, "
              f"max depth={max(depths)}, deepest kept={best[0][0]}..{best[-1][0]}, "
              f"tree-deaths kept depth {max(td)}..{min(td)} ({len(best_tree)})",
              flush=True)
    with open(os.path.join(HERE, 'samples.json'), 'w') as f:
        json.dump({str(k): dict(nruns=v['nruns'], completed=v['completed'],
                                deaths=v['deaths'],
                                best=v['best'], best_tree=v['best_tree'])
                   for k, v in out.items()}, f)
    print(f"total {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
