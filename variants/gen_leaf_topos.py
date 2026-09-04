#!/usr/bin/env python3
"""Enumerate series-reduced trees (all internal degrees >= 3) with exactly L leaves, L+1 <= N <= 2L-2 vertices, via nauty
gentreeg (-D? no: filter afterwards), cross-checked against networkx nonisomorphic_trees for N <= 14.  Output data/leaf_topos_{L}.jsonl"""
import sys, json, subprocess, networkx as nx
L = int(sys.argv[1]); out = open(f"data/leaf_topos_{L}.jsonl", "w"); c = 0; per_N = {}
for N in range(L + 1, 2 * L - 1):
    res = subprocess.run(["gentreeg", "-q", str(N)], capture_output=True, text=True, check=True).stdout
    cN = 0
    for line in res.split("\n"):
        line = line.strip()
        if not line: continue
        G = nx.from_sparse6_bytes(line.encode()); deg = dict(G.degree())
        if sum(1 for v in deg if deg[v] == 1) == L and all(deg[v] != 2 for v in deg):
            out.write(json.dumps({"id": c, "L": L, "N": N, "edges": [list(e) for e in G.edges()]}) + "\n"); c += 1; cN += 1
    per_N[N] = cN
    if N <= 14:
        cx = sum(1 for T in nx.nonisomorphic_trees(N) if sum(1 for v in T if T.degree(v) == 1) == L and all(T.degree(v) != 2 for v in T))
        assert cx == cN, (N, cx, cN)
print(json.dumps({"L": L, "total": c, "per_N": per_N, "nx_crosscheck_N<=14": True}))
