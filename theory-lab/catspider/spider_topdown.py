"""Top-down exact prover / enumerator for Leech SPIDERS (incl. paths) of order n.

Model. A spider (tree with at most one vertex of degree >= 3) with a chosen
center w (for a path: any interior vertex) is a set of k >= 2 legs; leg = strictly
increasing marks 0 < m_1 < ... < m_h = tip (weighted distances from w).
Tree distances = {marks} (center pairs) u {|m-m'| same leg} u {m+m' cross legs}.
Leech <=> this multiset is exactly {1..N}, N = C(n,2).  Facts used (all proved):
  * all C(n,2) distances are distinct, so in particular ALL marks are distinct
    across legs (center distances), and every pinned pair value is unique;
  * N = T + T' where T > T' are the two largest tips (max distance);
  * marks on any leg other than the top-two are < T'; marks on the second leg
    are <= T'; marks on the top leg are <= T.
Search. Branch on T (numeric).  Descend v = N-1 .. 1; maintain pinned marks and
the set of realised values; if v is unrealised, branch over ALL ways to realise
it by adding one or two new marks (with a pinned partner, with the center, or
both new; same-leg differences included); the vertex budget (#marks <= n-1)
makes the search finite.  Completeness: any Leech spider S consistent with the
current state realises v by some pair; each of its endpoints is either already
pinned or is added by exactly one enumerated option, so S survives in some
branch; hence "all branches die" proves nonexistence for that T, and looping T
over (N/2, N) proves it for order n.  If a branch reaches v=0 all N values are
covered by C(#marks+1,2) <= C(n,2) distinct pinned pairs, forcing #marks = n-1:
the state IS a Leech spider and is reported.
usage: python spider_topdown.py n [Tmin Tmax] [--verbose]
"""
import sys
from time import time

PARANOID = False

def solve(n, Tlist=None, verbose=False):
    N = n*(n-1)//2
    sols = []
    stats = {"nodes":0, "opts":0}

    def run_T(T):
        Tp = N - T
        # legs: list of lists of marks; index 0 = top leg (cap T), 1 = second (cap Tp),
        # others cap Tp-1
        legs = [[T],[Tp]]
        marks = {T:0, Tp:1}            # mark value -> leg index
        values = {T, Tp, N}
        def cap(idx):
            return T if idx==0 else (Tp if idx==1 else Tp-1)

        def try_add(adds):
            """adds: list of (legid, x); legid >= 0 is an existing leg index,
            legid < 0 is a fresh-leg group id (-1, -2: equal ids = same fresh leg).
            Apply with checks. Returns undo token or None if illegal."""
            # legality pre-checks
            for li, x in adds:
                if x < 1 or x in marks: return None
                if li >= 0 and (x > cap(li) or (li==1 and x >= Tp) or (li==0 and x >= T)): return None
                if li < 0 and x > Tp-1: return None
            if len(adds)==2 and adds[0][1]==adds[1][1]: return None
            if len(marks) + len(adds) > n-1: return None
            undo_vals = []; undo_marks = []; undo_leglen = len(legs)
            negmap = {}
            ok = True
            for li, x in adds:
                if li < 0:
                    if li not in negmap:
                        legs.append([]); negmap[li] = len(legs)-1
                    li = negmap[li]
                nv = [x]  # center distance
                for m, mi in marks.items():
                    if mi == li: nv.append(abs(x-m))
                    else:
                        s = x+m
                        if s > N: ok=False; break
                        nv.append(s)
                if not ok: break
                for w in nv:
                    if w in values or w < 1: ok=False; break
                    values.add(w); undo_vals.append(w)
                if not ok: break
                if len(nv) != len(set(nv)): ok=False; break
                legs[li].append(x); marks[x]=li; undo_marks.append(x)
            if not ok:
                for w in undo_vals: values.discard(w)
                for x in undo_marks: legs[marks[x]].remove(x); del marks[x]
                del legs[undo_leglen:]
                return None
            return (undo_vals, undo_marks, undo_leglen)

        def undo(tok):
            uv, um, ul = tok
            for w in uv: values.discard(w)
            for x in um: legs[marks[x]].remove(x); del marks[x]
            del legs[ul:]

        def options(v):
            """all candidate add-lists realising v (may still fail try_add checks)"""
            opts = set()
            def addopt(*placements):
                # canonical: sort by (x, li); relabel fresh-leg ids (-1,-2,..) in
                # first-appearance order so equivalent options collapse
                pl = sorted(placements)
                relab = {}; out = []
                for x, li in pl:
                    if li < 0:
                        if li not in relab: relab[li] = -1 - len(relab)
                        li = relab[li]
                    out.append((x, li))
                opts.add(tuple(out))
            nlegs = len(legs)
            # --- one new mark with pinned partner y (cross-leg sum) ---
            for y, yi in marks.items():
                x = v - y
                if x >= 1:
                    for li in range(nlegs):
                        if li != yi: addopt((x, li))
                    addopt((x, -1))
                # same-leg difference with pinned y: new = y+v or y-v on leg yi
                if y + v <= cap(yi): addopt((y+v, yi))
                if y - v >= 1: addopt((y-v, yi))
            # --- center partner: new mark at v ---
            for li in range(nlegs): addopt((v, li))
            addopt((v, -1))
            # --- two new marks, cross-leg sum x+y=v, x<y ---
            for x in range(max(1, v-T), (v-1)//2 + 1):
                y = v - x
                if x == y: continue
                for lx in range(nlegs):
                    for ly in range(nlegs):
                        if lx != ly: addopt((x,lx),(y,ly))
                    addopt((x,lx),(y,-1))
                    addopt((y,lx),(x,-1))
                addopt((x,-1),(y,-2))
                # two new same-leg (difference y-x = v-2x... no: y-x, only if y-x==v impossible here)
            # --- two new marks same leg, difference: x2 - x1 = v ---
            for x1 in range(1, T - v + 1):
                x2 = x1 + v
                for li in range(nlegs):
                    if x2 <= cap(li): addopt((x1,li),(x2,li))
                # on a fresh leg: x2 <= Tp-1 needed
                if x2 <= Tp-1: addopt((x1,-1),(x2,-1))
            return opts

        def paranoid_check():
            """recompute the full pair-value multiset from scratch; assert it
            equals the incremental `values` set and is duplicate-free in [1,N]."""
            allv = []
            flat = [(x, li) for li, leg in enumerate(legs) for x in leg]
            for i, (x, lx) in enumerate(flat):
                allv.append(x)                       # center pair
                for (y, ly) in flat[i+1:]:
                    allv.append(abs(x-y) if lx == ly else x+y)
            assert len(allv) == len(set(allv)), "duplicate pair value!"
            assert all(1 <= w <= N for w in allv), "value out of range!"
            assert set(allv) == values, "incremental value set mismatch!"

        def dfs(v):
            stats["nodes"] += 1
            if PARANOID: paranoid_check()
            while v >= 1 and v in values: v -= 1
            if v == 0:
                assert len(marks) == n-1, "tiling with too few marks?!"
                sols.append((T, tuple(tuple(sorted(l)) for l in legs)))
                return
            opts = options(v)
            stats["opts"] += len(opts)
            for key in opts:
                adds = [(li, x) for (x, li) in key]
                tok = try_add(adds)
                if tok is None: continue
                dfs(v-1)
                undo(tok)

        dfs(N-1)

    if Tlist is None:
        Tlist = range(N//2 + 1, N)
    for T in Tlist:
        if T <= N - T: continue
        if N - T < 1: continue
        t0 = time()
        n0 = stats["nodes"]
        run_T(T)
        if verbose:
            print(f"  T={T} done nodes={stats['nodes']-n0} ({time()-t0:.2f}s)", flush=True)
    return sols, stats

def main():
    n = int(sys.argv[1])
    args = [a for a in sys.argv[2:] if not a.startswith('--')]
    verbose = '--verbose' in sys.argv
    global PARANOID
    PARANOID = '--paranoid' in sys.argv
    Tlist = None
    if len(args) == 2:
        Tlist = range(int(args[0]), int(args[1])+1)
    t0 = time()
    sols, stats = solve(n, Tlist, verbose)
    # dedup by edge multiset (paths appear once per interior-vertex representation)
    def edges_of(sol):
        T, legs = sol
        es = []
        for leg in legs:
            prev = 0
            for m in leg:
                es.append(m - prev); prev = m
        return tuple(sorted(es))
    uniq = {}
    for s in sols: uniq.setdefault(edges_of(s), s)
    print({"n": n, "N": n*(n-1)//2, "raw_solutions": len(sols),
           "unique_by_edge_multiset": len(uniq), "nodes": stats["nodes"],
           "options_generated": stats["opts"], "secs": round(time()-t0, 2)})
    for k, s in uniq.items():
        print("SPIDER SOL: T=%d legs=%s edges=%s" % (s[0], s[1], k))

main()
