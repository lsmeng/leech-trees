"""Top-down exact prover / enumerator for Leech BI-SPIDERS of order n.

A bi-spider = tree with at most TWO vertices of degree >= 3.  Structure: two
centers cL, cR joined by a spine path of weighted length Q >= 1 (interior spine
vertices have degree 2), plus "legs" (paths) hanging at cL (L-legs, marks =
distance from cL) and at cR (R-legs, marks from cR).  This class contains all
double stars and double brooms; trees with <= 1 branch vertex (spiders, paths)
are covered by spider_topdown.py, and this search's family overlaps them
harmlessly (a side may end up with 0 or 1 legs).

Distances (all pairs):
  centers:      (cL,cR)=Q; (cL,x): b | s | Q+c ; (cR,x): b+Q | Q-s | c
                for x an L-mark b, spine mark s in (0,Q), R-mark c.
  L-L:  same leg |b-b'| ; different legs b+b'
  L-S:  b+s          L-R:  b+Q+c        S-S: |s-s'|
  S-R:  (Q-s)+c      R-R:  same leg |c-c'| ; different c+c'
Leech <=> multiset of all C(n,2) values = {1..N}.  Facts used (proved):
  * all values distinct; the value-N pair is leaf-leaf; leaves = leg tips;
  * so N is realised by a tip pair of type LR (T_L + Q + T_R = N) or, up to
    mirror, LL (T_1 + T_2 = N, the two largest L-tips, different L-legs).
Search: numeric branch on the anchors -- case LR over (T_L < T_R), Q = N-T_L-T_R;
case LL over (T_1 > N/2, Q <= N - T_1 - 1), T_2 = N - T_1 -- then descend
v = N-1..1 exactly as in spider_topdown.py, branching over all ways to realise
an unrealised v by adding 1 or 2 new marks.  Vertex budget: #marks <= n-2.
usage: python bispider_topdown.py n {LR|LL|both} [--paranoid] [--verbose]
"""
import sys
from time import time

PARANOID = False

def solve(n, cases=('LR','LL'), verbose=False):
    N = n*(n-1)//2
    sols = []
    stats = {"nodes":0, "opts":0, "branches":0}

    # state (closures): legsL/legsR: list of lists of marks; spine: list of s
    # marks maps mark-key -> ('L',i)/('R',i)/('S',) ... we keep typed containers
    # and a global `values` set; caps set per branch.

    def run_branch(Q, capsL, capsR, initL, initR):
        """capsL/capsR: list of caps for pre-created legs, plus default cap for
        fresh legs as capsL[-1] convention handled via capL(i).  initL/initR:
        list of initial tip marks per pre-created leg."""
        legsL = [list(x) for x in initL]
        legsR = [list(x) for x in initR]
        spine = []
        values = set()
        capfL, capfR = capsL[-1], capsR[-1]   # caps for fresh legs
        def capL(i): return capsL[i] if i < len(capsL)-1 else capfL
        def capR(i): return capsR[i] if i < len(capsR)-1 else capfR

        def pairvals_of(kind, x):
            """values created by new mark x of kind ('L',i)/('R',i)/('S',)
            against current state, including its two center distances."""
            out = []
            if kind[0]=='L':
                li = kind[1]
                out.append(x); out.append(x+Q)
                for j,leg in enumerate(legsL):
                    for b in leg: out.append(abs(x-b) if j==li else x+b)
                for s in spine: out.append(x+s)
                for leg in legsR:
                    for c in leg: out.append(x+Q+c)
            elif kind[0]=='R':
                li = kind[1]
                out.append(x+Q); out.append(x)
                for j,leg in enumerate(legsR):
                    for c in leg: out.append(abs(x-c) if j==li else x+c)
                for s in spine: out.append((Q-s)+x)
                for leg in legsL:
                    for b in leg: out.append(x+Q+b)
            else:  # spine mark
                out.append(x); out.append(Q-x)
                for s in spine: out.append(abs(x-s))
                for leg in legsL:
                    for b in leg: out.append(b+x)
                for leg in legsR:
                    for c in leg: out.append((Q-x)+c)
            return out

        def nmarks():
            return sum(len(l) for l in legsL)+sum(len(l) for l in legsR)+len(spine)

        def legal(kind, x):
            if x < 1: return False
            if kind[0]=='L':
                li=kind[1]
                if x > (capL(li) if li < len(legsL) else capfL): return False
            elif kind[0]=='R':
                li=kind[1]
                if x > (capR(li) if li < len(legsR) else capfR): return False
            else:
                if x >= Q: return False
            return True

        def try_add(adds):
            """adds: list of (kind, x); kind ('L',i)with i==len(legsL) meaning a
            fresh leg (i==len+1 second fresh), similarly R.  Returns undo or None."""
            for kind,x in adds:
                if not legal(kind,x): return None
            if len(adds)==2 and adds[0]==adds[1]: return None
            if nmarks()+len(adds) > n-2: return None
            undo_vals=[]; undo=[]
            okall=True
            for kind,x in adds:
                nv = pairvals_of(kind,x)
                ok = True
                for w in nv:
                    if w<1 or w>N or w in values: ok=False; break
                    values.add(w); undo_vals.append(w)
                if ok and len(nv)!=len(set(nv)): ok=False
                if not ok: okall=False; break
                if kind[0]=='L':
                    while kind[1] >= len(legsL): legsL.append([])
                    legsL[kind[1]].append(x); undo.append(('L',kind[1]))
                elif kind[0]=='R':
                    while kind[1] >= len(legsR): legsR.append([])
                    legsR[kind[1]].append(x); undo.append(('R',kind[1]))
                else:
                    spine.append(x); undo.append(('S',))
            if not okall:
                for w in undo_vals: values.discard(w)
                for u in undo:
                    if u[0]=='L': legsL[u[1]].pop()
                    elif u[0]=='R': legsR[u[1]].pop()
                    else: spine.pop()
                while legsL and not legsL[-1]: legsL.pop()
                while legsR and not legsR[-1]: legsR.pop()
                return None
            return (undo_vals, undo)

        def undo_tok(tok):
            uv, ud = tok
            for w in uv: values.discard(w)
            for u in ud:
                if u[0]=='L': legsL[u[1]].pop()
                elif u[0]=='R': legsR[u[1]].pop()
                else: spine.pop()
            while legsL and not legsL[-1]: legsL.pop()
            while legsR and not legsR[-1]: legsR.pop()

        def options(v):
            opts=set()
            def add(*pl):
                # canonicalise fresh-leg indices per side (sorted placements)
                nl, nr = len(legsL), len(legsR)
                relabL={}; relabR={}; out=[]
                for kind,x in sorted(pl):
                    if kind[0]=='L' and kind[1]>=nl:
                        if kind[1] not in relabL: relabL[kind[1]]=nl+len(relabL)
                        kind=('L',relabL[kind[1]])
                    elif kind[0]=='R' and kind[1]>=nr:
                        if kind[1] not in relabR: relabR[kind[1]]=nr+len(relabR)
                        kind=('R',relabR[kind[1]])
                    out.append((kind,x))
                opts.add(tuple(out))
            nl, nr = len(legsL), len(legsR)
            maxcapL = max([capL(i) for i in range(nl)]+[capfL])
            maxcapR = max([capR(i) for i in range(nr)]+[capfR])
            # ---- center pairs ----
            for i in range(nl+1): add((('L',i), v))          # (cL, L-mark v)
            if v-Q >= 1:
                for i in range(nr+1): add((('R',i), v-Q))    # (cL, R-mark), Q+c=v
                for i in range(nl+1): add((('L',i), v-Q))    # (cR, L-mark), b+Q=v
            if 0 < v < Q: add((('S',), v))                   # (cL, spine)
            for i in range(nr+1): add((('R',i), v))          # (cR, R-mark)
            if 0 < Q-v < Q: add((('S',), Q-v))               # (cR, spine), Q-s=v
            # ---- one new mark, one pinned partner ----
            for j,leg in enumerate(legsL):
                for b in leg:
                    x=v-b
                    if x>=1:                                  # L-L sum
                        for i in range(nl+1):
                            if i!=j: add((('L',i), x))
                    add((('L',j), b+v))                       # L-L diff same leg
                    if b-v>=1: add((('L',j), b-v))
                    if 0 < v-b < Q: add((('S',), v-b))        # L-S
                    if v-Q-b>=1:                              # L-R
                        for i in range(nr+1): add((('R',i), v-Q-b))
            for j,leg in enumerate(legsR):
                for c in leg:
                    x=v-c
                    if x>=1:                                  # R-R sum
                        for i in range(nr+1):
                            if i!=j: add((('R',i), x))
                    add((('R',j), c+v))                       # R-R diff same leg
                    if c-v>=1: add((('R',j), c-v))
                    if 0 < Q-(v-c) < Q: add((('S',), Q-(v-c)))  # S-R
                    if v-Q-c>=1:                              # L-R
                        for i in range(nl+1): add((('L',i), v-Q-c))
            for s in spine:
                if 0 < s+v < Q: add((('S',), s+v))            # S-S diff
                if 0 < s-v < Q: add((('S',), s-v))
                if v-s>=1:                                    # L-S
                    for i in range(nl+1): add((('L',i), v-s))
                if v-(Q-s)>=1:                                # S-R
                    for i in range(nr+1): add((('R',i), v-(Q-s)))
            # ---- both marks new ----
            # L-L sum x+y=v, different legs (incl. one or two fresh)
            for x in range(1,(v-1)//2+1):
                y=v-x
                if y > maxcapL: continue
                for i in range(nl+1):
                    for j in range(nl+2):
                        if i!=j: add((('L',i), x),(('L',j), y))
            # R-R sum
            for x in range(1,(v-1)//2+1):
                y=v-x
                if y > maxcapR: continue
                for i in range(nr+1):
                    for j in range(nr+2):
                        if i!=j: add((('R',i), x),(('R',j), y))
            # same-leg diff both new: (x, x+v)
            for x in range(1, maxcapL-v+1):
                for i in range(nl+1): add((('L',i), x),(('L',i), x+v))
            for x in range(1, maxcapR-v+1):
                for i in range(nr+1): add((('R',i), x),(('R',i), x+v))
            # S-S both new
            for s in range(1, Q-v):
                add((('S',), s),(('S',), s+v))
            # L-S both new: b+s=v
            for s in range(1, min(Q, v)):
                b=v-s
                if b>=1:
                    for i in range(nl+1): add((('L',i), b),(('S',), s))
            # S-R both new: (Q-s)+c=v
            for s in range(1, Q):
                c=v-(Q-s)
                if c>=1:
                    for i in range(nr+1): add((('R',i), c),(('S',), s))
            # L-R both new: b+Q+c=v
            for b in range(1, v-Q):
                c=v-Q-b
                if c>=1:
                    for i in range(nl+1):
                        for j in range(nr+1):
                            add((('L',i), b),(('R',j), c))
            return opts

        def paranoid_check():
            flat=[]
            for i,leg in enumerate(legsL):
                for b in leg: flat.append((('L',i),b))
            for i,leg in enumerate(legsR):
                for c in leg: flat.append((('R',i),c))
            for s in spine: flat.append((('S',),s))
            allv=[Q]
            def dL(k,x): return x if k[0]=='L' else (Q+x if k[0]=='R' else x)
            def dR(k,x): return x+Q if k[0]=='L' else (x if k[0]=='R' else Q-x)
            for i,(k,x) in enumerate(flat):
                allv.append(dL(k,x)); allv.append(dR(k,x))
                for (k2,y) in flat[i+1:]:
                    if k[0]==k2[0]=='S': allv.append(abs(x-y))
                    elif k[0]=='S': allv.append((x if k2[0]=='L' else Q-x)+y)
                    elif k2[0]=='S': allv.append((y if k[0]=='L' else Q-y)+x)
                    elif k[0]!=k2[0]: allv.append(x+Q+y)
                    elif k==k2 or (k[0]==k2[0] and k[1]==k2[1]): allv.append(abs(x-y))
                    else: allv.append(x+y)
            assert len(allv)==len(set(allv)), "duplicate value"
            assert all(1<=w<=N for w in allv), "range"
            assert set(allv)==values, "mismatch"

        def dfs(v):
            stats["nodes"] += 1
            if PARANOID: paranoid_check()
            while v>=1 and v in values: v-=1
            if v==0:
                assert nmarks()==n-2
                sols.append((Q, tuple(tuple(sorted(l)) for l in legsL),
                                tuple(sorted(spine)),
                                tuple(tuple(sorted(l)) for l in legsR)))
                return
            opts=options(v)
            stats["opts"]+=len(opts)
            for key in opts:
                tok=try_add(list(key))
                if tok is None: continue
                dfs(v-1)
                undo_tok(tok)

        # init values: centers + initial tips
        init_marks=[]
        for i,leg in enumerate(legsL):
            for b in leg: init_marks.append((('L',i),b))
        for i,leg in enumerate(legsR):
            for c in leg: init_marks.append((('R',i),c))
        legsL2=[[] for _ in legsL]; legsR2=[[] for _ in legsR]
        legsLsave, legsRsave = legsL, legsR
        legsL, legsR = legsL2, legsR2  # rebuild via try_add for value bookkeeping
        values.add(Q)
        ok=True; toks=[]
        for kind,x in init_marks:
            tok=try_add([(kind,x)])
            if tok is None: ok=False; break
            toks.append(tok)
        if ok:
            stats["branches"]+=1
            dfs(N-1)
        return

    if 'LR' in cases:
        # T_L < T_R, Q = N - T_L - T_R >= 1
        for TL in range(1, N//2+1):
            for TR in range(TL+1, N-TL):
                Q = N-TL-TR
                if Q < 1: break
                run_branch(Q, [TL,TL-1], [TR,TR-1], [[TL]], [[TR]])
        # note: capsL=[TL, TL-1]: leg 0 cap TL; fresh legs cap TL-1 (their tips
        # are smaller than the largest L-tip; marks<TL enforced by distinctness
        # anyway, cap TL-1 is safe).  Same on the right.
    if 'LL' in cases:
        # N = T1 + T2, T1 > T2; Q in [1, T2-1]; right side free with cap T2-Q-1
        for T1 in range(N//2+1, N):
            T2 = N-T1
            if T2 < 1: break
            for Q in range(1, T2):
                run_branch(Q, [T1,T2,T2-1], [max(T2-Q-1,0)], [[T1],[T2]], [])
    return sols, stats

def main():
    n=int(sys.argv[1])
    case=sys.argv[2] if len(sys.argv)>2 and not sys.argv[2].startswith('--') else 'both'
    global PARANOID
    PARANOID='--paranoid' in sys.argv
    cases=('LR','LL') if case=='both' else (case,)
    t0=time()
    sols,stats=solve(n,cases)
    print({"n":n,"N":n*(n-1)//2,"cases":cases,"raw_solutions":len(sols),
           "branches":stats["branches"],"nodes":stats["nodes"],
           "options":stats["opts"],"secs":round(time()-t0,2)}, flush=True)
    for s in sols:
        print("BISPIDER SOL: Q=%d legsL=%s spine=%s legsR=%s"%s, flush=True)

main()
