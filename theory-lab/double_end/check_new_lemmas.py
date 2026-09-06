"""Positive controls for new order-25 route lemmas on the five known Leech trees."""
import json, cmath, itertools
d=json.load(open('/Users/geoclaw/Documents/claude/projects/leech-trees/theory-lab/double_end/ground_truth_small.json'))
trees=d['leech_trees']
def dist_matrix(n,edges):
    adj={i:[] for i in range(n)}
    for u,v,w in edges: adj[u].append((v,w)); adj[v].append((u,w))
    D=[[None]*n for _ in range(n)]
    for s in range(n):
        st=[(s,0)]; D[s][s]=0
        while st:
            x,dx=st.pop()
            for y,w in adj[x]:
                if D[s][y] is None: D[s][y]=dx+w; st.append((y,dx+w))
    return D,adj
def is_chordal(n,E):
    # maximum cardinality search + perfect elimination check
    adj={i:set() for i in range(n)}
    for u,v in E: adj[u].add(v); adj[v].add(u)
    weight={i:0 for i in range(n)}; order=[]; left=set(range(n))
    while left:
        x=max(left,key=lambda i:weight[i]); order.append(x); left.remove(x)
        for y in adj[x]:
            if y in left: weight[y]+=1
    pos={x:i for i,x in enumerate(order)}
    for x in order:  # earlier-numbered neighbours must form a clique
        prev=[y for y in adj[x] if pos[y]<pos[x]]
        if not prev: continue
        p=max(prev,key=lambda y:pos[y])
        for y in prev:
            if y!=p and y not in adj[p]: return False
    return True
for T in trees:
    n,N,edges=T['n'],T['N'],T['edges']
    D,adj=dist_matrix(n,edges)
    pairs={D[u][v]:(u,v) for u in range(n) for v in range(u+1,n)}
    assert sorted(pairs)==list(range(1,N+1))
    print(f"\n== n={n} N={N} edges={edges}")
    if n>=3:
        a,b=pairs[N]; 
        # name a so that d(a,w)=N-1
        u,v=pairs[N-1]
        if b in (u,v): a,b=b,a
        assert a in pairs[N-1]
        others=[x for x in range(n) if x not in (a,b)]
        # claim 1: pair attaining delta=diam(T-a) contains b; delta = N - min F
        delta=max(D[x][y] for x in range(n) for y in range(n) if a not in (x,y))
        px,py=pairs[delta]
        F={N-D[b][u] for u in others}; E={N-D[a][u] for u in others}
        ok1 = (b in (px,py)) and (not others or delta==N-min(F))
        print(f" claim1 contains-b: delta={delta} pair={pairs[delta]} b={b}  minF={min(F) if F else None}  ->", ok1)
        # claim: T-{a,b} distances; g2 = N - diam(T-{a,b})
        if len(others)>=2:
            d2=max(D[x][y] for x in others for y in others)
            g2=N-d2
            rest=sorted(D[x][y] for i,x in enumerate(others) for y in others[i+1:])
            print(f" diam(T-a-b)={d2}, g2={g2}, distances of T-a-b = {rest}")
    # claim 2: chordal filtration
    ch=all(is_chordal(n,[pairs[t] for t in range(1,T0+1)]) for T0 in range(1,N+1))
    print(" claim2 every near-graph N_t chordal:", ch)
    # claim 3: roots of unity subtree identity, every root vertex, every nontrivial N-th root of unity
    okall=True
    for root in range(n):
        par={root:None}; h={root:0}; order=[root]; st=[root]
        while st:
            x=st.pop()
            for y,w in adj[x]:
                if y not in h: h[y]=h[x]+w; par[y]=x; order.append(y); st.append(y)
        for k in range(1,N):
            z=cmath.exp(2j*cmath.pi*k/N)
            sig={}
            for x in reversed(order):
                sg=z**h[x]
                for y,w in adj[x]:
                    if par.get(y)==x: sg+=sig[y]
                sig[x]=sg
            tot=0
            for x in order:
                sg=sig[x]**2
                for y,w in adj[x]:
                    if par.get(y)==x: sg-=sig[y]**2
                tot+=z**(-2*h[x])*sg
            direct=sum(z**D[u][v] for u in range(n) for v in range(n))
            if abs(tot-n)>1e-7 or abs(direct-n)>1e-7: okall=False
    print(" claim3 roots-of-unity subtree identity = n:", okall)
