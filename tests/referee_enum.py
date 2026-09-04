"""REFEREE: independent enumerators of tree labelings with a prescribed distance set (no forcing lemma, no pruning
rules shared with leech_search.cpp).  Used as ground truth by tests/referee_diff.py.

count_dfs(n, edges, target)  : plain edge-by-edge backtracking (BFS edge order), domain = target values, incremental
                               distinctness of completed pair sums.  Only 'edge weight is itself a distance' is used
                               (an edge is a pair), so the domain restriction to `target` is trivially valid.
count_cpsat(n, edges, target): CP-SAT model (weights in target, pair sums = sum of weights, AllDifferent, pair values
                               in target); enumerate all solutions.  Second, fully independent oracle.
Both count LABELINGS (edge->weight maps), i.e. all symmetric copies are counted separately.
"""
import sys, itertools
from collections import deque

def bfs_edge_order(n, edges):
    adj = {i: [] for i in range(n)}
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    seen = {0}; order = []; dq = deque([0]); par = {0: None}
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if v not in seen: seen.add(v); par[v] = u; order.append((u, v)); dq.append(v)
    return order, par, adj

def all_pair_paths(n, edges):
    order, par, adj = bfs_edge_order(n, edges)
    eidx = {}
    for i, (u, v) in enumerate(order): eidx[(u, v)] = i; eidx[(v, u)] = i
    # depth / ancestors
    dep = {0: 0}
    for u, v in order: dep[v] = dep[u] + 1
    paths = {}
    for x in range(n):
        for y in range(x + 1, n):
            a, b, es = x, y, []
            while a != b:
                if dep[a] >= dep[b]: es.append(eidx[(a, par[a])]); a = par[a]
                else: es.append(eidx[(b, par[b])]); b = par[b]
            paths[(x, y)] = es
    return order, paths

def count_dfs(n, edges, target, limit=None):
    order, paths = all_pair_paths(n, edges)
    E = len(order); tset = set(target); tmax = max(target); vals = sorted(target)
    # pairs completed at each edge index (max edge index in path)
    completed = [[] for _ in range(E)]
    for p, es in paths.items(): completed[max(es)].append(es)
    w = [0] * E; used_vals = set(); cnt = 0
    sys.setrecursionlimit(10000)
    def rec(i):
        nonlocal cnt
        if i == E:
            cnt += 1; return limit is not None and cnt >= limit
        for v in vals:
            if v in used_vals: continue
            w[i] = v; added = []; ok = True
            for es in completed[i]:
                s = 0
                for e in es: s += w[e]
                if s in used_vals or s not in tset: ok = False; break
                used_vals.add(s); added.append(s)
            if ok:
                if rec(i + 1): return True
            for s in added: used_vals.discard(s)
        w[i] = 0
        return False
    rec(0)
    return cnt

def count_cpsat(n, edges, target, workers=1, limit=None):
    from ortools.sat.python import cp_model
    order, paths = all_pair_paths(n, edges)
    m = cp_model.CpModel(); dom = cp_model.Domain.FromValues(sorted(target))
    w = [m.NewIntVarFromDomain(dom, f"w{i}") for i in range(len(order))]
    d = []
    for p, es in paths.items():
        v = m.NewIntVarFromDomain(dom, f"d{p}"); m.Add(v == sum(w[e] for e in es)); d.append(v)
    m.AddAllDifferent(d)
    s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.enumerate_all_solutions = True
    class CB(cp_model.CpSolverSolutionCallback):
        def __init__(self): super().__init__(); self.k = 0
        def on_solution_callback(self):
            self.k += 1
            if limit is not None and self.k >= limit: self.StopSearch()
    cb = CB(); st = s.Solve(m, cb)
    assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.INFEASIBLE), s.StatusName(st)
    return cb.k

def leech_target(n): return list(range(1, n * (n - 1) // 2 + 1))

if __name__ == "__main__":
    # self-check on the known Leech trees (labelings counted with symmetry): star K_{1,3}: 3! = 6; P4: 2; L6 double star
    import json, os
    ROOT = os.path.join(os.path.dirname(__file__), "..")
    for n in (4, 5, 6):
        for r in map(json.loads, open(os.path.join(ROOT, f"data/trees_{n}.jsonl"))):
            a = count_dfs(n, [tuple(e) for e in r["edges"]], leech_target(n)); b = count_cpsat(n, [tuple(e) for e in r["edges"]], leech_target(n))
            print(n, r["id"], r["edges"], "dfs", a, "cpsat", b); assert a == b
