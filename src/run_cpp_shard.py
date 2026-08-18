"""Cluster shard runner: python run_cpp_shard.py n shard nshards --time T [--ids results/theory_survivors_18.txt] [--order leaves]
Processes ids with (rank % nshards == shard-1) after ordering; resumable; output results/cpp_order_{n}_shard{shard}.jsonl.
Witnesses verified with both checkers."""
import json, sys, os, time, argparse, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import checker_a, checker_b
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "bin", "leech_search")
ap = argparse.ArgumentParser(); ap.add_argument("n", type=int); ap.add_argument("shard", type=int); ap.add_argument("nshards", type=int)
ap.add_argument("--time", type=float, default=600); ap.add_argument("--ids", default=None); ap.add_argument("--order", default="leaves")
ap.add_argument("--extra", default=""); ap.add_argument("--redo-unknown", action="store_true"); ap.add_argument("--min-time", type=float, default=0,
    help="only (re)run records whose previous time limit was < this (use with --redo-unknown)")
A = ap.parse_args(); n = A.n
recs = [json.loads(l) for l in open(os.path.join(ROOT, f"data/trees_{n}.jsonl"))]
if A.ids:
    keep = {int(x) for x in open(os.path.join(ROOT, A.ids)).read().split()}
    recs = [r for r in recs if r["id"] in keep]
def leaves(r):
    deg = {}
    for u, v in r["edges"]: deg[u] = deg.get(u, 0) + 1; deg[v] = deg.get(v, 0) + 1
    return sum(1 for d in deg.values() if d == 1)
if A.order == "leaves":  # many leaves = easy first
    recs.sort(key=lambda r: (-leaves(r), r["id"]))
mine = [r for i, r in enumerate(recs) if i % A.nshards == A.shard - 1]
out = os.path.join(ROOT, f"results/cpp_order_{n}_shard{A.shard}.jsonl")
done = {}
if os.path.exists(out):
    for l in open(out):
        if l.strip():
            r = json.loads(l); done[r["id"]] = r
todo = []
for r in mine:
    d = done.get(r["id"])
    if d is None or (A.redo_unknown and d["status"] == "UNKNOWN" and d.get("tl", 0) < A.time): todo.append(r)
print(f"n={n} shard {A.shard}/{A.nshards} mine={len(mine)} todo={len(todo)} time={A.time}", flush=True)
t0 = time.time()
with open(out, "a") as f:
    for r in todo:
        cmd = [BIN, "--time", str(A.time)] + A.extra.split()
        o = subprocess.run(cmd, input=json.dumps(r) + "\n", capture_output=True, text=True).stdout
        for line in o.splitlines():
            if not line.startswith("{"): continue
            res = json.loads(line); res["tl"] = A.time
            if res.get("witness"):
                e = [tuple(x) for x in res["witness"]]
                res["check_a"] = checker_a.is_leech(n, e)[0]; res["check_b"] = checker_b.is_leech(n, e)[0]
                print("!!! WITNESS", json.dumps(res), flush=True)
            f.write(json.dumps(res) + "\n"); f.flush()
print("done", round(time.time() - t0, 1), flush=True)
