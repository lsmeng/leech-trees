#!/usr/bin/env python3
"""Brute-force cross-check of mod_leech for n <= 6: enumerate ALL labelings (Z_k minus 0)^{n-1} of every topology, count
raw modular Leech labelings, and compare with mod_leech's raw_unit*1 + raw_nonunit (engine restricts the first BFS edge to
1 or a non-unit; brute count = raw_unit*phi(k) + raw_nonunit).  Also checks every engine SOL with checker_distinct.check_modular."""
import itertools, json, subprocess, sys, math, os
sys.path.insert(0, os.path.dirname(__file__))
from checker_distinct import check_modular, parse
here = os.path.dirname(os.path.abspath(__file__))
def brute(n, edges):
    k = n * (n - 1) // 2 + 1; cnt = 0
    for w in itertools.product(range(1, k), repeat=n - 1):
        adj = {v: [] for v in range(n)}
        for (u, v), x in zip(edges, w): adj[u].append((v, x)); adj[v].append((u, x))
        seen = set(); ok = True
        for s in range(n):
            d = {s: 0}; st = [s]
            while st:
                x = st.pop()
                for y, x2 in adj[x]:
                    if y not in d: d[y] = d[x] + x2; st.append(y)
            for t2 in range(s + 1, n):
                r = d[t2] % k
                if r == 0 or r in seen: ok = False; break
                seen.add(r)
            if not ok: break
        if ok: cnt += 1
    return cnt
import networkx as nx
for n in (4, 5, 6):
    k = n * (n - 1) // 2 + 1; phi = sum(1 for w in range(1, k) if math.gcd(w, k) == 1)
    tops = [{"id": i, "n": n, "edges": [list(e) for e in t.edges()]} for i, t in enumerate(nx.nonisomorphic_trees(n))]
    out = subprocess.run([os.path.join(here, "mod_leech"), str(n), "--print"], input="\n".join(json.dumps(t) for t in tops) + "\n", capture_output=True, text=True).stdout
    recs = [json.loads(l) for l in out.splitlines() if l.startswith("{")]
    sols = [l for l in out.splitlines() if l.startswith("SOL:")]
    for s in sols:
        ok, msg = check_modular(parse(s), n); assert ok, (s, msg)
    for t, r in zip(tops, recs):
        b = brute(n, [tuple(e) for e in t["edges"]])
        eng = r["raw_unit"] * phi + r["raw_nonunit"]
        print(f"n={n} id={t['id']} brute={b} engine={eng} orbits={r['orbits']}", "OK" if b == eng else "MISMATCH")
        assert b == eng
print("all SOL lines pass check_modular; brute force agrees for n=4,5,6")
