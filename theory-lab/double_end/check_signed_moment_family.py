"""Independent check of (i) signed first moment = sum_e w_e q_e (S-q_e); (ii) charge identity; (iii) P'(zeta) = -N/(1-zeta) cut form for zeta=i."""
import json, random, cmath
d=json.load(open('/Users/geoclaw/Documents/claude/projects/leech-trees/theory-lab/double_end/ground_truth_small.json'))
def dm(n,edges):
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
def side(n,adj,u,v):  # vertices on u's side of edge (u,v)
    seen={u}; st=[u]
    while st:
        x=st.pop()
        for y,w in adj[x]:
            if (x,y)!=(u,v) and y not in seen: seen.add(y); st.append(y)
    return seen
def checks(n,edges):
    D,adj=dm(n,edges)
    sig=[(-1)**D[0][v] for v in range(n)]; S=sum(sig)
    lhs=sum(sig[u]*sig[v]*D[u][v] for u in range(n) for v in range(u+1,n))
    rhs=0
    for u,v,w in edges:
        A=side(n,adj,u,v); q=sum(sig[x] for x in A); rhs+=w*q*(S-q)
    ok1=(lhs==rhs)
    # zeta=i first-derivative cut identity: sum_{u<v} d z^{d} = sum_e w_e z^{w_e} (sum_{u in A} z^{d(u,x_e)}) (sum_{v notin A} z^{d(v,y_e)})
    z=1j
    lhs2=sum(D[u][v]*z**D[u][v] for u in range(n) for v in range(u+1,n))
    rhs2=0
    for u,v,w in edges:
        A=side(n,adj,u,v); B=set(range(n))-A
        rhs2+=w*z**w*sum(z**D[x][u] for x in A)*sum(z**D[y][v] for y in B)
    ok2=abs(lhs2-rhs2)<1e-9
    return ok1,ok2,lhs
random.seed(1)
allok=True
for T in d['leech_trees']:
    ok1,ok2,lhs=checks(T['n'],T['edges']); N=T['N']
    target = N//2 if N%2==0 else -(N+1)//2
    print(f"n={T['n']}: signed-moment cut identity {ok1}, zeta=i derivative cut identity {ok2}, signed sum={lhs} target={target}")
    allok &= ok1 and ok2 and lhs==target
for trial in range(300):
    n=random.randint(3,14); edges=[]
    for v in range(1,n): edges.append([random.randrange(v),v,random.randint(1,40)])
    ok1,ok2,_=checks(n,edges); allok &= ok1 and ok2
print("random trees (300, n<=14): all identities hold:", allok)
# charge identity on the n=6 tree analogue: classes by parity, charges +|Q| on P and -|P| on Q (zero-sum)
T=d['leech_trees'][-1]; n,edges=T['n'],T['edges']; D,adj=dm(n,edges)
par=[D[0][v]%2 for v in range(n)]; P=[v for v in range(n) if par[v]==0]; Q=[v for v in range(n) if par[v]==1]
cP,cQ=len(Q),-len(P); c=[cP if par[v]==0 else cQ for v in range(n)]
lhs=sum(c[u]*c[v]*D[u][v] for u in range(n) for v in range(u+1,n))
rhs=-sum(w*sum(c[x] for x in side(n,adj,u,v))**2 for u,v,w in edges)
print(f"n=6 charge identity (charges {cP}/{cQ}): {lhs} == {rhs} ->", lhs==rhs)
