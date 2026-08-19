#!/usr/bin/env python3
"""Independent-method cross-check for modular Leech trees: per-topology CP-SAT.  Labels w_e in [1,k-1], k=C(n,2)+1;
for each pair the path sum s_ij = q_ij*k + r_ij with r_ij in [1,k-1]; AllDifferent(r_ij) (a bijection onto Z_k*).
Symmetry: none (raw count when --all).  Usage: mod_cpsat.py n [--workers W] [--time T] [--all] [--ids ...] [--trees file]"""
import sys, json, itertools, argparse, os
import networkx as nx
from ortools.sat.python import cp_model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checker_distinct import check_modular

def solve(edges, n, workers, tlimit, want_all):
    k = n * (n - 1) // 2 + 1; m = cp_model.CpModel(); T = nx.Graph(edges)
    w = {tuple(e): m.NewIntVar(1, k - 1, f"w{e}") for e in edges}
    rv = []
    for a, b in itertools.combinations(range(n), 2):
        p = nx.shortest_path(T, a, b); pe = []
        for i in range(len(p) - 1):
            e = (p[i], p[i + 1]); pe.append(w[e] if e in w else w[(e[1], e[0])])
        r = m.NewIntVar(1, k - 1, f"r{a}_{b}"); q = m.NewIntVar(0, len(pe), f"q{a}_{b}"); m.Add(sum(pe) == q * k + r); rv.append(r)
    m.AddAllDifferent(rv)
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
    ap = argparse.ArgumentParser(); ap.add_argument("n", type=int); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--time", type=float, default=600); ap.add_argument("--all", action="store_true"); ap.add_argument("--ids"); ap.add_argument("--trees"); ap.add_argument("--part"); a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__)); tf = a.trees or os.path.join(here, "data", f"trees_{a.n}.jsonl")
    pi, pk = (int(x) for x in a.part.split("/")) if a.part else (0, 1)
    os.makedirs(os.path.join(here, "results"), exist_ok=True); of = os.path.join(here, "results", f"mod_cpsat_{a.n}" + (f"_part{pi}" if a.part else "") + ".jsonl")
    done = set()
    if os.path.exists(of):
        for l in open(of): done.add(json.loads(l)["id"])
    out = open(of, "a"); ids = set(int(x) for x in a.ids.split(",")) if a.ids else None; stat = {}
    for l in open(tf):
        t = json.loads(l)
        if t["id"] in done or (ids and t["id"] not in ids) or t["id"] % pk != pi: continue
        st, sols, wt = solve([tuple(e) for e in t["edges"]], a.n, a.workers, a.time, a.all)
        stat[st] = stat.get(st, 0) + 1
        rec = {"id": t["id"], "n": a.n, "status": st, "nsol": len(sols), "time": round(wt, 2), "sols": []}
        for sol in sols:
            ok, msg = check_modular(sol, a.n); assert ok, msg; rec["sols"].append(sol)
            print("SOL:", t["id"], " ".join(f"{u}-{v}:{x}" for u, v, x in sol), "|", msg, flush=True)
        out.write(json.dumps(rec) + "\n"); out.flush(); print(rec["id"], st, len(sols), rec["time"], flush=True)
    print(json.dumps({"n": a.n, "statuses": stat}))
