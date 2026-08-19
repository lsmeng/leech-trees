#!/usr/bin/env python3
"""Regression tests for variants/mdd_forest: (1) Calhoun's M(n) for n<=9 reproduced with the published number of minimal trees,
(2) every SOL passes checker_distinct, (3) shard identity sum(nodes_i) = full + (K-1)*prefix and sum(nsol_i) = nsol,
(4) agreement with the independent per-topology engine mdd_topo (raw labeling counts modulo automorphisms ignored; here only
SAT/UNSAT and n=9 uniqueness)."""
import subprocess, json, os, sys
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from checker_distinct import check_distinct, parse
def run(args):
    out = subprocess.run([os.path.join(here, "mdd_forest")] + [str(a) for a in args], capture_output=True, text=True).stdout
    sols = [l for l in out.splitlines() if l.startswith("SOL:")]; rec = json.loads([l for l in out.splitlines() if l.startswith("{")][0]); return rec, sols
known = {4: (6, 2), 5: (11, 6), 6: (15, 1), 7: (22, 2), 8: (30, 2), 9: (39, 1)}
for n, (M, cnt) in known.items():
    if M - 1 >= n * (n - 1) // 2:
        r, _ = run([n, M - 1]); assert r["nsol"] == 0, (n, r)
    r, sols = run([n, M]); assert r["nsol"] == cnt == len(sols), (n, r)
    for s in sols:
        ok, msg = check_distinct(parse(s), n, M); assert ok, msg
    print(f"n={n}: M={M} UNSAT below, {cnt} minimal trees, witnesses OK")
for n, D, K, L in ((9, 39, 5, 4), (8, 30, 3, 3)):
    full, fs = run([n, D, "-q"]); pre, _ = run([n, D, "-q", "--nodes", 10**9, "--shard", 0, 1, "--shard-level", L])
    tot = 0; ns = 0
    for i in range(K):
        r, s = run([n, D, "--shard", i, K, "--shard-level", L]); tot += r["nodes"]; ns += r["nsol"]
    print(f"shards n={n} D={D} K={K} L={L}: sum nodes {tot}, full {full['nodes']}, nsol {ns}/{full['nsol']}")
    assert ns == full["nsol"] and (tot - full["nodes"]) % (K - 1) == 0
out = subprocess.run([os.path.join(here, "mdd_topo"), "9", "39"], input=open(os.path.join(here, "data", "trees_9.jsonl")).read(), capture_output=True, text=True).stdout
raw = sum(json.loads(l)["raw_sols"] for l in out.splitlines() if l.startswith("{")); assert raw == 1, raw
print("mdd_topo n=9 D=39: exactly one labeling over all 47 topologies; all tests passed")
