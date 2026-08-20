"""Machine checks for the caterpillar/spider theory lemmas of this lab.

L-A (reformulation): caterpillar with spine v_1..v_m (non-leaf vertices),
    p_i = d(v_1,v_i); leaf u at v_{i(u)} weight b_u; rho(u)=p_{i(u)}+b_u,
    lam(u)=p_{i(u)}-b_u; rho(v_i)=lam(v_i)=p_i.  Then for i(x)<=i(y), x!=y:
    d(x,y) = rho(y) - lam(x).
L-B (coordinate distinctness): if all pairwise distances of the caterpillar are
    distinct then the n values rho are distinct and the n values lam are distinct.
L-C (pendant disjointness, any distinct-distance tree): at any vertex v with
    pendant weights b_1..b_k and A = {0} u {d(v,x): x not a pendant leaf at v}:
    b_j - b_i (i!=j) is never a difference of two elements of A.
L-D (window tiling): Leech caterpillar, A1 = max rho, G1 = min lam,
    E = A1-G1-N >= 0; every s in {0..N-1} has EXACTLY one admissible pair
    (i(x)<=i(y), x!=y) with (lam(x)-G1) + (A1-rho(y)) = s+E, counting each
    unordered pair once (tie i(x)=i(y): either orientation, same value).
Checks: the five known Leech trees + 3000 random caterpillars with distinct
distances (random weights, retry until distinct) + 3000 random trees for L-C.
"""
import random
from itertools import combinations
from collections import deque

def dists(n, edges):
    adj = {}
    for u,v,w in edges:
        adj.setdefault(u,[]).append((v,w)); adj.setdefault(v,[]).append((u,w))
    D = {}
    for s in adj:
        d = {s:0}; q = deque([s])
        while q:
            u = q.popleft()
            for v,w in adj[u]:
                if v not in d: d[v]=d[u]+w; q.append(v)
        D[s]=d
    return D

def caterpillar_coords(n, edges):
    """return None if not a caterpillar, else (index, rho, lam) dicts."""
    adj = {}
    for u,v,w in edges:
        adj.setdefault(u,[]).append((v,w)); adj.setdefault(v,[]).append((u,w))
    deg = {v:len(adj[v]) for v in adj}
    spine = [v for v in adj if deg[v]>=2]
    if not spine:   # single edge
        return None
    core = set(spine)
    # spine must induce a path: find an end
    coreN = {v:sum(1 for x,_ in adj[v] if x in core) for v in core}
    if any(c>2 for c in coreN.values()): return None
    ends = [v for v in core if coreN[v]<=1]
    start = ends[0] if ends else None
    order = [start]; prev=None
    while True:
        nxt=[x for x,_ in adj[order[-1]] if x in core and x!=prev]
        if not nxt: break
        prev=order[-1]; order.append(nxt[0])
    if len(order)!=len(core): return None
    D = dists(n, edges)
    p = {v: D[order[0]][v] for v in order}
    idx = {v:i for i,v in enumerate(order)}
    rho={}; lam={}; index={}
    for v in order:
        rho[v]=lam[v]=p[v]; index[v]=idx[v]
    for v in adj:
        if v in core: continue
        (att,w), = [(x,w) for x,w in adj[v]]
        rho[v]=p[att]+w; lam[v]=p[att]-w; index[v]=idx[att]
    return index, rho, lam, D

def check_LA_LB(n, edges, require_distinct):
    got = caterpillar_coords(n, edges)
    if got is None: return None
    index, rho, lam, D = got
    verts = list(rho)
    for x,y in combinations(verts,2):
        if index[x] > index[y]: x,y = y,x
        d = D[x][y]
        if index[x] < index[y]:
            assert d == rho[y]-lam[x], (edges,x,y)
        else:
            assert d in (rho[y]-lam[x], rho[x]-lam[y]), (edges,x,y)
    if require_distinct:
        assert len(set(rho.values()))==len(verts), edges
        assert len(set(lam.values()))==len(verts), edges
    return True

def check_LC(n, edges):
    D = dists(n, edges)
    adj = {}
    for u,v,w in edges:
        adj.setdefault(u,[]).append((v,w)); adj.setdefault(v,[]).append((u,w))
    for v in adj:
        pend = [(x,w) for x,w in adj[v] if len(adj[x])==1]
        B = [w for _,w in pend]
        pendset = {x for x,_ in pend}
        A = [0]+[D[v][x] for x in adj if x!=v and x not in pendset]
        Adiff = {a-a2 for a in A for a2 in A}
        for i,j in combinations(range(len(B)),2):
            assert B[j]-B[i] not in Adiff and B[i]-B[j] not in Adiff, (edges,v)

def check_LD(n, edges):
    got = caterpillar_coords(n, edges)
    if got is None: return None
    index, rho, lam, D = got
    verts = list(rho); N = n*(n-1)//2
    A1 = max(rho.values()); G1 = min(lam.values()); E = A1-G1-N
    assert E >= 0, edges
    from collections import Counter
    cnt = Counter()
    for x,y in combinations(verts,2):
        if index[x] > index[y]: x,y = y,x
        cnt[(lam[x]-G1)+(A1-rho[y])] += 1   # equals A1-G1-d(x,y) = E+s
    for s in range(N):
        assert cnt[s+E] == 1, (edges, s, E)
    return E

def rand_caterpillar(rng):
    m = rng.randint(2,5); L = rng.randint(1,4)
    n = m+L
    for _ in range(400):
        edges=[]
        for i in range(1,m): edges.append((i-1,i,rng.randint(1,40)))
        for j in range(L):
            att = rng.randint(0,m-1) if 0<rng.random() else 0
            edges.append((att, m+j, rng.randint(1,40)))
        # ends of spine must carry a leg to make v_0,v_{m-1} non-leaves
        if not any(u==0 or v==0 for u,v,w in edges[m-1:]): continue
        if not any(u==m-1 or v==m-1 for u,v,w in edges[m-1:]): continue
        D = dists(n, edges)
        dl = [D[x][y] for x,y in combinations(sorted(D),2)]
        if len(dl)==len(set(dl)): return n, edges
    return None

def rand_tree(rng):
    n = rng.randint(3,9)
    for _ in range(400):
        edges=[(rng.randint(0,i-1), i, rng.randint(1,60)) for i in range(1,n)]
        D = dists(n, edges)
        dl=[D[x][y] for x,y in combinations(sorted(D),2)]
        if len(dl)==len(set(dl)): return n, edges
    return None

KNOWN = {
 2:[ [(0,1,1)] ],
 3:[ [(0,1,1),(0,2,2)] ],
 4:[ [(0,1,1),(0,2,2),(0,3,4)], [(0,1,1),(2,3,2),(0,2,3)] ],
 6:[ [(0,1,1),(0,2,2),(3,4,4),(0,3,5),(3,5,8)] ],
}

def main():
    rng = random.Random(20260820)
    for n, trees in KNOWN.items():
        for edges in trees:
            check_LC(n, edges)
            r = check_LA_LB(n, edges, True)
            e = check_LD(n, edges)
            print(f"known n={n}: L-A/B {'ok' if r else 'n/a (not caterpillar-decomposable)'}, "
                  f"L-C ok, L-D E={e}")
    na=nc=0
    for _ in range(3000):
        t = rand_caterpillar(rng)
        if not t: continue
        n, edges = t
        if check_LA_LB(n, edges, True): na+=1
    for _ in range(3000):
        t = rand_tree(rng)
        if not t: continue
        n, edges = t
        check_LC(n, edges); nc+=1
    print(f"random caterpillars L-A/L-B checked: {na}; random trees L-C checked: {nc}; all OK")

main()
