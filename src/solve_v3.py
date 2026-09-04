"""v3 = v2 + explicit dual channeling: boolean x[p][v] (pair p realizes value v), each value exactly once,
each pair exactly one value, linked to d_p. Redundant with AllDifferent but gives value-side propagation."""
import sys, time, json
from math import comb
from ortools.sat.python import cp_model
import networkx as nx
sys.path.insert(0, 'src')
from solve_v2 import build

def solve(n, edges, time_limit=None, workers=1, seed=0):
    N = comb(n, 2)
    m, w = build(n, edges)
    # recover d vars by name
    proto = m.Proto()
    pairs = [(m.GetIntVarFromProtoIndex(i), pv.domain[0], pv.domain[-1]) for i, pv in enumerate(proto.variables) if pv.name.startswith("d") and not pv.name.startswith("dp")]
    x = [[m.NewBoolVar("") for v in range(N + 1)] for p in pairs]
    for i, (dp, lb, ub) in enumerate(pairs):
        m.Add(x[i][0] == 0)
        m.Add(dp == sum(v * x[i][v] for v in range(N + 1)))
        m.AddExactlyOne(x[i])
    for v in range(1, N + 1):
        m.AddExactlyOne([x[i][v] for i in range(len(pairs))])
    s = cp_model.CpSolver(); s.parameters.num_search_workers = workers; s.parameters.random_seed = seed
    if time_limit: s.parameters.max_time_in_seconds = time_limit
    t0 = time.time(); st = s.Solve(m); dt = time.time() - t0
    wit = [[e[0], e[1], s.Value(w[e])] for e in w] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    return {"status": s.StatusName(st), "time": round(dt, 2), "witness": wit, "conflicts": s.NumConflicts()}

if __name__ == "__main__":
    recs = [json.loads(l) for l in open("data/trees_11.jsonl")]
    for i in [56, 58, 48]:
        e = [tuple(x) for x in recs[i]["edges"]]
        b = solve(11, e, time_limit=120, workers=8)
        print(i, "v3 8w", b["status"], b["time"], flush=True)
