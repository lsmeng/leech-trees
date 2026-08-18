"""Shard runner for CP-SAT v2 (fallback engine): python run_shard_cpsat.py n shard nshards [timelimit]. Resumable."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from solve_v2 import solve
import checker_a, checker_b
n, shard, nsh = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
TL = float(sys.argv[4]) if len(sys.argv) > 4 else 3600
recs = [json.loads(l) for l in open(f"data/trees_{n}.jsonl")]
mine = [r for r in recs if r["id"] % nsh == (shard - 1)]
out = f"results/cpsat_order_{n}_shard{shard}.jsonl"
done = {json.loads(l)["id"] for l in open(out)} if os.path.exists(out) else set()
with open(out, "a") as f:
    for r in mine:
        if r["id"] in done: continue
        e = [tuple(x) for x in r["edges"]]
        res = solve(n, e, time_limit=TL, workers=1); res["id"] = r["id"]
        if res["witness"]:
            w = [tuple(x) for x in res["witness"]]
            res["check_a"] = checker_a.is_leech(n, w)[0]; res["check_b"] = checker_b.is_leech(n, w)[0]
        f.write(json.dumps(res) + "\n"); f.flush()
