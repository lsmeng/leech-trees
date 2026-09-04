"""CP-SAT model v2: adds path-length lower bounds, per-edge parity/Taylor, automorphism symmetry breaking,
value-based decision strategy. Compare against v1 on slow n=11 instances."""
import json, sys, time, itertools
from math import comb
from ortools.sat.python import cp_model
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

def build(n, edges, symbreak=True, strategy=True):
    N = comb(n, 2)
    edges = [tuple(sorted(e)) for e in edges]
    G = nx.Graph(); G.add_edges_from(edges)
    m = cp_model.CpModel()
    w = {e: m.NewIntVar(1, N, f"w{e}") for e in edges}
    d = {}
    for s in range(n):
        for t in range(s + 1, n):
            p = nx.shortest_path(G, s, t); k = len(p) - 1
            pe = [tuple(sorted((p[i], p[i + 1]))) for i in range(k)]
            v = m.NewIntVar(k * (k + 1) // 2, N, f"d{s}_{t}")  # k distinct positive weights >= 1+..+k
            m.Add(v == sum(w[e] for e in pe)); d[(s, t)] = v
    m.AddAllDifferent(list(d.values()))
    m.Add(sum(d.values()) == N * (N + 1) // 2)
    # the two largest distances: N is realized; nothing else cheap here.
    # Taylor parity: count vertices at odd weighted depth from vertex 0 must be in taylor set
    sizes = [a for a in range(n + 1) if a * (n - a) == (N + 1) // 2]
    par = {e: m.NewBoolVar(f"p{e}") for e in edges}
    for e in edges:
        m.Add(w[e] == 2 * m.NewIntVar(0, N // 2, f"h{e}") + par[e])
    dp = {0: m.NewConstant(0)}
    for u, v in nx.bfs_edges(G, 0):
        x = m.NewBoolVar(f"dp{v}"); e = tuple(sorted((u, v)))
        m.AddBoolXOr([dp[u], par[e], x, True]); dp[v] = x
    tot = sum(dp[v] for v in range(1, n))
    b = [m.NewBoolVar(f"a{a}") for a in sizes]
    for a, bi in zip(sizes, b): m.Add(tot == a).OnlyEnforceIf(bi)
    m.AddExactlyOne(b)
    if symbreak:
        # automorphisms: for each generator-ish automorphism (all of them for small groups), impose lex order on edge weights
        auts = list(GraphMatcher(G, G).isomorphisms_iter())
        if len(auts) > 1 and len(auts) <= 5000:
            for phi in auts:
                if all(phi[v] == v for v in phi): continue
                img = [tuple(sorted((phi[u], phi[v]))) for u, v in edges]
                # find first edge moved; require w[e] <= w[phi(e)] as a weak lex-leader (sound: choose lex-min in orbit)
                # full lex-leader: (w[e1],...) <=lex (w[phi e1],...)
                pos = [(e, ie) for e, ie in zip(edges, img) if e != ie]
                if not pos: continue
                # lexicographic constraint via CP-SAT: implement with prefix-equal booleans (bounded depth 3 for size)
                depth = min(3, len(pos))
                eq_prev = None
                for i in range(depth):
                    e, ie = pos[i]
                    if eq_prev is None:
                        m.Add(w[e] <= w[ie])
                        eq = m.NewBoolVar(""); m.Add(w[e] == w[ie]).OnlyEnforceIf(eq); m.Add(w[e] != w[ie]).OnlyEnforceIf(eq.Not())
                        eq_prev = [eq]
                    else:
                        m.Add(w[e] <= w[ie]).OnlyEnforceIf(eq_prev)
                        eq = m.NewBoolVar(""); m.Add(w[e] == w[ie]).OnlyEnforceIf(eq); m.Add(w[e] != w[ie]).OnlyEnforceIf(eq.Not())
                        eq_prev = eq_prev + [eq]
    if strategy:
        # decide edge weights first, most central edges first, smallest values first
        cen = nx.edge_betweenness_centrality(G)
        order = sorted(edges, key=lambda e: -cen[e])
        m.AddDecisionStrategy([w[e] for e in order], cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.SELECT_MIN_VALUE)
    return m, w

def solve(n, edges, time_limit=None, workers=1, seed=0, **kw):
    m, w = build(n, edges, **kw)
    s = cp_model.CpSolver(); s.parameters.num_search_workers = workers; s.parameters.random_seed = seed
    if time_limit: s.parameters.max_time_in_seconds = time_limit
    t0 = time.time(); st = s.Solve(m); dt = time.time() - t0
    wit = [[e[0], e[1], s.Value(w[e])] for e in w] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    return {"status": s.StatusName(st), "time": round(dt, 2), "witness": wit, "conflicts": s.NumConflicts()}

if __name__ == "__main__":
    import solve_topology as v1
    n = 11
    recs = [json.loads(l) for l in open("data/trees_11.jsonl")]
    slow = [json.loads(l) for l in open("results/order_11.jsonl")]
    slow = sorted(slow, key=lambda r: -r["time"])[:6]
    for r in slow:
        e = [tuple(x) for x in recs[r["id"]]["edges"]]
        a = solve(n, e, time_limit=120, workers=1)
        b = solve(n, e, time_limit=120, workers=8, symbreak=True)
        print(r["id"], "v1", r["status"], r["time"], "| v2 1w", a["status"], a["time"], "| v2 8w", b["status"], b["time"], flush=True)
