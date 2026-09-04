"""CP-SAT model for one topology. Positive integer edge weights, all C(n,2) path sums distinct
and in [1,N] (=> bijection onto {1..N}). Returns status and witness if any."""
import json, sys, time
from math import comb
from ortools.sat.python import cp_model
import networkx as nx

def paths(n, edges):
    G = nx.Graph(); G.add_edges_from(edges)
    P = {}
    for s in range(n):
        for t in range(s + 1, n):
            p = nx.shortest_path(G, s, t)
            P[(s, t)] = [tuple(sorted((p[i], p[i + 1]))) for i in range(len(p) - 1)]
    return P

def taylor_sizes(n):
    """Taylor (1977): color vertices by parity of weighted depth; #odd distances = a(n-a) must equal
    ceil(N/2). Returns admissible a values. NOTE: depends on weights, so it is a constraint, not a topology filter."""
    N = comb(n, 2)
    return [a for a in range(n + 1) if a * (n - a) == (N + 1) // 2]

def solve(n, edges, time_limit=None, workers=1, seed=0):
    N = comb(n, 2)
    edges = [tuple(sorted(e)) for e in edges]
    m = cp_model.CpModel()
    w = {e: m.NewIntVar(1, N, f"w{e}") for e in edges}
    P = paths(n, edges)
    d = {}
    for (s, t), pe in P.items():
        v = m.NewIntVar(1, N, f"d{s}_{t}")
        m.Add(v == sum(w[e] for e in pe)); d[(s, t)] = v
    m.AddAllDifferent(list(d.values()))
    # Taylor parity constraint (redundant but strong): parity of weighted depth from vertex 0
    par = {e: m.NewBoolVar(f"p{e}") for e in edges}
    for e in edges:
        m.Add(w[e] == 2 * m.NewIntVar(0, N // 2, f"h{e}") + par[e])
    depth_par = {0: 0}
    G = nx.Graph(); G.add_edges_from(edges)
    order = list(nx.bfs_edges(G, 0))
    dp = {0: m.NewConstant(0)}
    for u, v in order:
        x = m.NewBoolVar(f"dp{v}"); e = tuple(sorted((u, v)))
        m.AddBoolXOr([dp[u], par[e], x, True])  # x = dp[u] xor par[e]
        dp[v] = x
    sizes = taylor_sizes(n)
    tot = sum(dp[v] for v in range(1, n))
    m.AddAllowedAssignments([tot], [[a] for a in sizes]) if False else None
    b = [m.NewBoolVar(f"a{a}") for a in sizes]
    for a, bi in zip(sizes, b): m.Add(tot == a).OnlyEnforceIf(bi)
    m.AddExactlyOne(b)
    # redundant: sum of all distances = N(N+1)/2 (cut-size identity)
    m.Add(sum(d.values()) == N * (N + 1) // 2)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.random_seed = seed
    if time_limit: s.parameters.max_time_in_seconds = time_limit
    t0 = time.time(); st = s.Solve(m); dt = time.time() - t0
    name = s.StatusName(st)
    wit = [[e[0], e[1], s.Value(w[e])] for e in edges] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    return {"status": name, "time": round(dt, 3), "witness": wit, "conflicts": s.NumConflicts(), "branches": s.NumBranches()}

if __name__ == "__main__":
    n = int(sys.argv[1]); edges = json.loads(sys.argv[2])
    print(json.dumps(solve(n, edges, time_limit=float(sys.argv[3]) if len(sys.argv) > 3 else None)))
