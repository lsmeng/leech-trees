#!/usr/bin/env python3
"""Leaf-Leech trees (Ozen-Wang-Yalman 2016, Integers 16 #A21, Def. 1): an unweighted tree with L leaves whose leaf-leaf
distances are exactly {3, 4, ..., C(L,2)+2}.  Contracting degree-2 vertices, this is a series-reduced tree (all internal
degrees >= 3) with L leaves and positive integer edge weights whose weighted leaf-leaf distances are {3..S+2}, S = C(L,2).
Method: enumerate all series-reduced topologies with L leaves (networkx nonisomorphic_trees(N) for L+1 <= N <= 2L-2,
filtered), then per topology CP-SAT (weights in [1, S+2], AllDifferent over the leaf-pair distance variables in [3, S+2] --
S pairs, S values, so a bijection), enumerate all solutions with a callback, and verify every witness with
checker_distinct.check_leaf.  Output: results/leaf_L{L}.jsonl (one record per topology) + SOL lines.
Usage: leaf_leech_cpsat.py L [--workers W] [--time T] [--limit-topologies K]"""
import sys, json, itertools, argparse, os, time
import networkx as nx
from ortools.sat.python import cp_model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checker_distinct import check_leaf

def series_reduced_trees(L):
    for N in range(L + 1, 2 * L - 1):
        for T in nx.nonisomorphic_trees(N):
            deg = dict(T.degree())
            if sum(1 for v in deg if deg[v] == 1) == L and all(deg[v] != 2 for v in deg):
                yield T

def solve(T, L, workers, tlimit, want_all=True):
    S = L * (L - 1) // 2; edges = list(T.edges()); m = cp_model.CpModel()
    w = {e: m.NewIntVar(1, S + 2, f"w{e}") for e in edges}
    leaves = [v for v in T if T.degree(v) == 1]
    dvars = []
    for a, b in itertools.combinations(leaves, 2):
        path = nx.shortest_path(T, a, b)
        pe = [tuple(sorted((path[i], path[i + 1]))) for i in range(len(path) - 1)]
        pe = [e if e in w else (e[1], e[0]) for e in pe]
        d = m.NewIntVar(3, S + 2, f"d{a}_{b}"); m.Add(d == sum(w[e] for e in pe)); dvars.append(d)
    m.AddAllDifferent(dvars)
    s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = tlimit
    sols = []
    if want_all:
        s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
        class CB(cp_model.CpSolverSolutionCallback):
            def __init__(self): super().__init__()
            def on_solution_callback(self): sols.append([(u, v, self.Value(w[(u, v)])) for (u, v) in edges])
        st = s.Solve(m, CB())
    else:
        st = s.Solve(m)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): sols.append([(u, v, s.Value(w[(u, v)])) for (u, v) in edges])
    return s.StatusName(st), sols, s.WallTime()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("L", type=int); ap.add_argument("--workers", type=int, default=1); ap.add_argument("--time", type=float, default=600); ap.add_argument("--all", action="store_true"); a = ap.parse_args()
    os.makedirs("results", exist_ok=True); out = open(f"results/leaf_L{a.L}.jsonl", "a")
    ntop = 0; nsol = 0; t0 = time.time(); statuses = {}
    for i, T in enumerate(series_reduced_trees(a.L)):
        ntop += 1
        st, sols, wt = solve(T, a.L, a.workers, a.time, want_all=a.all)
        statuses[st] = statuses.get(st, 0) + 1
        rec = {"id": i, "L": a.L, "N": T.number_of_nodes(), "edges": [list(e) for e in T.edges()], "status": st, "nsol": len(sols), "time": round(wt, 2)}
        for sol in sols:
            ok, msg = check_leaf(sol); assert ok, msg
            rec.setdefault("sols", []).append({"edges": sol, "check": msg}); nsol += 1
            print("SOL:", " ".join(f"{u}-{v}:{x}" for u, v, x in sol), "|", msg, flush=True)
        out.write(json.dumps(rec) + "\n"); out.flush()
    print(json.dumps({"L": a.L, "topologies": ntop, "statuses": statuses, "witnesses": nsol, "wall": round(time.time() - t0, 1)}))
