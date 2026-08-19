#!/usr/bin/env python3
"""Independent-method cross-check for M(n): per-topology CP-SAT.  For every unlabeled tree on n vertices (data/trees_n.jsonl)
decide whether positive integer weights exist with all C(n,2) path sums distinct and <= D (AllDifferent over pair-distance
variables in [1, D]; redundant: edge weights distinct, w_i + w_j <= D for every edge pair, sum of the two largest ...).
With --all enumerates every solution (weight vectors) per topology.  Records -> results/mdd_cpsat_{n}_{D}.jsonl (resumable).
Usage: mdd_cpsat.py n D [--workers W] [--time T] [--all] [--ids i,j,...]"""
import sys, json, itertools, argparse, os, time
import networkx as nx
from ortools.sat.python import cp_model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checker_distinct import check_distinct

def solve(edges, n, D, workers, tlimit, want_all):
    m = cp_model.CpModel(); T = nx.Graph(edges)
    w = {tuple(e): m.NewIntVar(1, D, f"w{e}") for e in edges}
    m.AddAllDifferent(list(w.values()))
    dv = []
    for a, b in itertools.combinations(range(n), 2):
        p = nx.shortest_path(T, a, b); pe = []
        for i in range(len(p) - 1):
            e = (p[i], p[i + 1]); pe.append(w[e] if e in w else w[(e[1], e[0])])
        d = m.NewIntVar(1, D, f"d{a}_{b}"); m.Add(d == sum(pe)); dv.append(d)
    m.AddAllDifferent(dv)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlimit; sols = []
    if want_all:
        s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
        class CB(cp_model.CpSolverSolutionCallback):
            def __init__(self): super().__init__()
            def on_solution_callback(self): sols.append([(u, v, self.Value(w[(u, v)])) for (u, v) in w])
        st = s.Solve(m, CB())
    else:
        s.parameters.num_workers = workers; st = s.Solve(m)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): sols.append([(u, v, s.Value(w[(u, v)])) for (u, v) in w])
    return s.StatusName(st), sols, s.WallTime()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("n", type=int); ap.add_argument("D", type=int); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--time", type=float, default=600); ap.add_argument("--all", action="store_true"); ap.add_argument("--ids"); ap.add_argument("--trees", default=None); a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__)); tf = a.trees or os.path.join(here, "data", f"trees_{a.n}.jsonl")
    if not os.path.exists(tf): tf = os.path.join(here, "..", "data", f"trees_{a.n}.jsonl")
    os.makedirs(os.path.join(here, "results"), exist_ok=True); of = os.path.join(here, "results", f"mdd_cpsat_{a.n}_{a.D}{'_all' if a.all else ''}.jsonl")
    done = set()
    if os.path.exists(of):
        for l in open(of): done.add(json.loads(l)["id"])
    out = open(of, "a"); ids = set(int(x) for x in a.ids.split(",")) if a.ids else None; stat = {}
    for l in open(tf):
        t = json.loads(l)
        if t["id"] in done or (ids and t["id"] not in ids): continue
        st, sols, wt = solve([tuple(e) for e in t["edges"]], a.n, a.D, a.workers, a.time, a.all)
        stat[st] = stat.get(st, 0) + 1
        rec = {"id": t["id"], "n": a.n, "D": a.D, "status": st, "nsol": len(sols), "time": round(wt, 2), "sols": []}
        for sol in sols:
            ok, msg = check_distinct(sol, a.n, a.D); assert ok, msg; rec["sols"].append(sol)
            print("SOL:", t["id"], " ".join(f"{u}-{v}:{x}" for u, v, x in sol), "|", msg, flush=True)
        out.write(json.dumps(rec) + "\n"); out.flush(); print(rec["id"], st, len(sols), rec["time"], flush=True)
    print(json.dumps({"n": a.n, "D": a.D, "statuses": stat}))
