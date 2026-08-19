#!/usr/bin/env python3
"""Summarize leaf-Leech results: results/leaf_L{L}*.jsonl -> distinct leaf-Leech trees up to isomorphism (of the expanded,
unweighted tree), with irreducible-vertex flag; re-verifies every witness with checker_distinct.check_leaf."""
import sys, json, glob, os
import networkx as nx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checker_distinct import check_leaf
L = int(sys.argv[1]); recs = []
for f in sorted(glob.glob(f"results/leaf_L{L}*.jsonl")):
    for l in open(f): recs.append(json.loads(l))
def expand(sol):
    G = nx.Graph(); c = 0
    for u, v, w in sol:
        prev = ("v", u)
        for i in range(w - 1): c += 1; G.add_edge(prev, ("s", c)); prev = ("s", c)
        G.add_edge(prev, ("v", v))
    return G
distinct = []; stat = {}; ntop = 0; unk = []
for r in recs:
    ntop += 1; stat[r["status"]] = stat.get(r["status"], 0) + 1
    if r["status"] not in ("OPTIMAL", "INFEASIBLE"): unk.append(r["id"])
    for s in r.get("sols", []):
        sol = [tuple(e) for e in s["edges"]]; ok, msg = check_leaf(sol); assert ok, msg
        G = expand(sol)
        if not any(nx.is_isomorphic(G, H) for H, _, _ in distinct): distinct.append((G, sol, msg))
print(json.dumps({"L": L, "topologies": ntop, "statuses": stat, "unknown_ids": unk, "distinct_leaf_leech_trees": len(distinct),
                  "with_irreducible_vertex": sum(1 for _, _, m in distinct if "irreducible: []" not in m)}))
for G, sol, msg in distinct: print(" ".join(f"{u}-{v}:{w}" for u, v, w in sol), "|", G.number_of_nodes(), "vertices |", msg)
