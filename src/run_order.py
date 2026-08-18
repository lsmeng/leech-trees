"""Run all topologies of order n through Taylor prefilter + CP-SAT, in parallel. Appends to results/order_{n}.jsonl (resumable)."""
import json, sys, os, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from solve_topology import solve
import checker_a, checker_b

TL = None
def _tl():
    v = os.environ.get("LEECH_TL", "None"); return None if v == "None" else float(v)
def work(rec):
    TL = _tl()
    n, edges = rec["n"], [tuple(e) for e in rec["edges"]]
    r = solve(n, edges, time_limit=TL); r["id"] = rec["id"]
    if r["witness"]:
        e = [tuple(x) for x in r["witness"]]
        r["check_a"] = checker_a.is_leech(n, e)[0]; r["check_b"] = checker_b.is_leech(n, e)[0]
    return r

if __name__ == "__main__":
    n = int(sys.argv[1]); TL = float(sys.argv[2]) if len(sys.argv) > 2 else None
    os.environ["LEECH_TL"] = str(TL)
    procs = int(sys.argv[3]) if len(sys.argv) > 3 else os.cpu_count()
    recs = [json.loads(l) for l in open(f"data/trees_{n}.jsonl")]
    out = f"results/order_{n}.jsonl"
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["id"] for l in open(out)}
    todo = [r for r in recs if r["id"] not in done]
    print(f"n={n} total={len(recs)} done={len(done)} todo={len(todo)} procs={procs} TL={TL}", flush=True)
    t0 = time.time(); k = 0
    with Pool(procs) as pool, open(out, "a") as f:
        for r in pool.imap_unordered(work, todo, chunksize=4):
            f.write(json.dumps(r) + "\n"); f.flush(); k += 1
            if r["status"] in ("OPTIMAL", "FEASIBLE"):
                print("!!! WITNESS", json.dumps(r), flush=True)
            if k % 500 == 0:
                print(f"{k}/{len(todo)} elapsed {time.time()-t0:.0f}s", flush=True)
    print("done", time.time() - t0)
