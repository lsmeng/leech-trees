"""Sharded, resumable driver for the forest engine (bin/forest_search).
Usage: python src/run_forest.py n [--shards K] [--procs P] [--level L] [--out results/forest_order_{n}.jsonl] [--nice 10]
Each shard i (0..K-1) explores the common prefix (levels <= L) plus every L-level subtree with index % K == i; the
solution counts add up (tests/test_forest_search.py::test_shards_partition).  Every SOL line is re-checked with
checker_a/checker_b and appended to results/forest_order_{n}_solutions.jsonl."""
import argparse, json, os, subprocess, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import checker_a, checker_b
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "bin", "forest_search")

def work(job):
    n, i, K, L, nice = job
    cmd = (["nice", "-n", str(nice)] if nice else []) + [BIN, str(n), "--shard", str(i), str(K), "--shard-level", str(L)]
    t0 = time.time(); out = subprocess.run(cmd, capture_output=True, text=True).stdout
    sols = [l for l in out.splitlines() if l.startswith("SOL:")]
    rec = json.loads([l for l in out.splitlines() if l.startswith("{")][-1]); rec["wall"] = round(time.time() - t0, 1)
    checked = []
    for s in sols:
        e = [tuple(int(x) for x in tok.replace("-", ":").split(":")) for tok in s.split()[1:]]
        checked.append({"n": n, "shard": i, "edges": e, "check_a": checker_a.is_leech(n, e)[0], "check_b": checker_b.is_leech(n, e)[0]})
    return rec, checked

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("n", type=int); ap.add_argument("--shards", type=int, default=64)
    ap.add_argument("--procs", type=int, default=4); ap.add_argument("--level", type=int, default=8); ap.add_argument("--out", default=None)
    ap.add_argument("--nice", type=int, default=10)
    a = ap.parse_args(); n = a.n
    out = a.out or os.path.join(ROOT, f"results/forest_order_{n}.jsonl"); solf = out.replace(".jsonl", "_solutions.jsonl")
    done = set()
    if os.path.exists(out):
        for l in open(out):
            if l.strip(): r = json.loads(l); done.add(r["shard"][0])
    todo = [(n, i, a.shards, a.level, a.nice) for i in range(a.shards) if i not in done]
    print(f"n={n} shards={a.shards} done={len(done)} todo={len(todo)} procs={a.procs} level={a.level}", flush=True)
    t0 = time.time()
    with Pool(a.procs) as pool, open(out, "a") as f:
        for rec, checked in pool.imap_unordered(work, todo):
            f.write(json.dumps(rec) + "\n"); f.flush()
            if checked:
                with open(solf, "a") as g:
                    for c in checked: g.write(json.dumps(c) + "\n"); print("!!! WITNESS", json.dumps(c), flush=True)
            print(f"shard {rec['shard'][0]} nodes {rec['nodes']} nsol {rec['nsol']} time {rec['time']:.0f}s elapsed {time.time()-t0:.0f}s", flush=True)
    recs = [json.loads(l) for l in open(out) if l.strip()]
    print("done", len(recs), "shards; total nodes", sum(r["nodes"] for r in recs), "nsol", sum(r["nsol"] for r in recs), "status", set(r["status"] for r in recs), flush=True)
