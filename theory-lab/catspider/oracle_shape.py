"""Independent brute-force oracle for the SHAPE-RESTRICTED forced-forest search.
Same idea as cleanroom/oracle_brute.py (all labeled children, validity by BFS
recomputation, dedup by canonical form), plus shape filters implemented
*independently* of cs_forest.c:
  cat    : every component, after literally deleting its leaves, is a path
           (checked by degree count in the induced subgraph), and
           #{v: deg>=2} <= Dmax(n)-1;
  spider : #{v: deg>=3} <= 1 over the whole forest, and every component's hop
           diameter (BFS, unweighted) <= Dmax(n).
Dmax(n) = max D with OGR(D+1) <= N, OGR table as in the repo.
usage: python oracle_shape.py n {all|cat|spider} [--sumrule]
"""
import sys
from collections import deque

OGR = [0,0,1,3,6,11,17,25,34,44,55,72,85,106,127,151,177,199,216,246,283,333,356,372,425,480,492,553,585]

def dmax(N):
    m = 1
    while m+1 < len(OGR) and OGR[m+1] <= N:
        m += 1
    return m-1

def adjacency(edges):
    adj = {}
    for u,v,w in edges:
        adj.setdefault(u,set()).add(v); adj.setdefault(v,set()).add(u)
    return adj

def components(adj):
    seen, out = set(), []
    for s in adj:
        if s in seen: continue
        comp = set([s]); q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in comp: comp.add(v); q.append(v)
        seen |= comp; out.append(comp)
    return out

def hop_diam(adj, comp):
    def bfs(s):
        d = {s:0}; q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in d: d[v]=d[u]+1; q.append(v)
        far = max(d, key=lambda k: d[k]); return far, d[far]
    a,_ = bfs(next(iter(comp))); _,e = bfs(a); return e

def is_cat_component(adj, comp):
    # literally delete leaves, check remainder is a path (or empty/single vertex)
    core = {v for v in comp if len(adj[v]) >= 2}
    if len(core) <= 1: return True
    degs = [len(adj[v] & core) for v in core]
    # remainder of a tree is a tree; it is a path iff no vertex has >2 core-neighbours
    return max(degs) <= 2

def shape_ok(edges, shape, Dm):
    adj = adjacency(edges)
    if shape == 'all': return True
    if shape == 'spider':
        if sum(1 for v in adj if len(adj[v]) >= 3) > 1: return False
        return all(hop_diam(adj, c) <= Dm for c in components(adj))
    # cat
    if sum(1 for v in adj if len(adj[v]) >= 2) > Dm - 1: return False
    return all(is_cat_component(adj, c) for c in components(adj))

def distances(edges):
    adj = {}
    for u,v,w in edges:
        adj.setdefault(u,[]).append((v,w)); adj.setdefault(v,[]).append((u,w))
    dl = []
    for s in sorted(adj):
        d = {s:0}; q = deque([s])
        while q:
            u = q.popleft()
            for v,w in adj[u]:
                if v not in d: d[v]=d[u]+w; q.append(v)
        dl += [d[t] for t in d if t > s]
    return dl

def comps_verts(edges):
    adj = adjacency(edges)
    return [sorted(c) for c in components(adj)]

def canon(edges):
    inc = {}
    for u,v,w in edges:
        inc.setdefault(u,[]).append(w); inc.setdefault(v,[]).append(w)
    return tuple(sorted(tuple(sorted(x)) for x in inc.values()))

def main():
    n = int(sys.argv[1]); shape = sys.argv[2]; sumrule = '--sumrule' in sys.argv
    N = n*(n-1)//2; Dm = dmax(N)
    level = {(): []}
    counts = [1]; nsol = 0; lev = 0
    while level and lev < n-1:
        nxt = {}
        for key, edges in level.items():
            V = len({x for e in edges for x in e[:2]})
            dl = distances(edges); ds = set(dl)
            assert len(dl) == len(ds)
            if len(edges) == n-1: continue
            t = 1
            while t in ds: t += 1
            if sumrule and edges and t + max(e[2] for e in edges) > N: continue
            cs = comps_verts(edges)
            cands = []
            for i in range(len(cs)):
                for j in range(i+1, len(cs)):
                    for x in cs[i]:
                        for y in cs[j]:
                            cands.append(edges + [(x,y,t)])
            if V+1 <= n:
                for c in cs:
                    for x in c:
                        cands.append(edges + [(x, V, t)])
            if V+2 <= n:
                cands.append(edges + [(V, V+1, t)])
            for ch in cands:
                dl2 = distances(ch)
                if len(dl2) != len(set(dl2)) or max(dl2) > N: continue
                if not shape_ok(ch, shape, Dm): continue
                nxt.setdefault(canon(ch), ch)
        lev += 1
        counts.append(len(nxt))
        for k,ch in nxt.items():
            if len(ch) == n-1: nsol += 1
        level = nxt
    while len(counts) < n: counts.append(0)
    print({"n":n,"shape":shape,"sumrule":sumrule,"Dmax":Dm,
           "levels":counts,"nodes":sum(counts),"nsol":nsol})

main()
