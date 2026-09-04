"""Shard data/trees_{n}.jsonl over processes running bin/leech_search; append to results/cpp_order_{n}.jsonl (resumable).
Usage: python src/run_cpp.py n [--procs P] [--time T] [--sample K --seed S] [--extra "flags"] [--out path]
Every SAT witness is verified with checker_a and checker_b (fields check_a/check_b)."""
import json, sys, os, time, argparse, subprocess, random
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import checker_a, checker_b
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "bin", "leech_search")
ARGS = None

def work(job):
    batch, tl, extra = job
    cmd = [BIN] + (["--time", str(tl)] if tl else []) + extra.split()
    inp = "".join(json.dumps(r) + "\n" for r in batch)
    out = subprocess.run(cmd, input=inp, capture_output=True, text=True).stdout
    res = []
    for line in out.splitlines():
        if not line.startswith("{"): continue
        r = json.loads(line)
        if r.get("witness"):
            n = r["n"]; e = [tuple(x) for x in r["witness"]]
            r["check_a"] = checker_a.is_leech(n, e)[0]; r["check_b"] = checker_b.is_leech(n, e)[0]
        res.append(r)
    return res

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("n", type=int); ap.add_argument("--procs", type=int, default=os.cpu_count())
    ap.add_argument("--time", type=float, default=0); ap.add_argument("--sample", type=int, default=0); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--extra", default=""); ap.add_argument("--out", default=None); ap.add_argument("--chunk", type=int, default=1)
    ap.add_argument("--redo-unknown", action="store_true", help="re-run topologies whose recorded status is UNKNOWN (e.g. with a larger --time)")
    ARGS = ap.parse_args(); n = ARGS.n
    recs = [json.loads(l) for l in open(os.path.join(ROOT, f"data/trees_{n}.jsonl"))]
    if ARGS.sample:
        random.Random(ARGS.seed).shuffle(recs); recs = recs[:ARGS.sample]
    out = ARGS.out or os.path.join(ROOT, f"results/cpp_order_{n}.jsonl")
    done = set()
    if os.path.exists(out):
        for l in open(out):
            if not l.strip(): continue
            r = json.loads(l)
            if ARGS.redo_unknown and r["status"] == "UNKNOWN": continue
            done.add(r["id"])
    todo = [r for r in recs if r["id"] not in done]
    print(f"n={n} total={len(recs)} done={len(done)} todo={len(todo)} procs={ARGS.procs} time={ARGS.time} extra='{ARGS.extra}' out={out}", flush=True)
    batches = [(todo[i:i + ARGS.chunk], ARGS.time, ARGS.extra) for i in range(0, len(todo), ARGS.chunk)]
    t0 = time.time(); k = 0
    with Pool(ARGS.procs) as pool, open(out, "a") as f:
        for res in pool.imap_unordered(work, batches):
            for r in res:
                r["wall"] = round(time.time() - t0, 1)
                f.write(json.dumps(r) + "\n"); f.flush(); k += 1
                if r["status"] == "SAT":
                    print("!!! WITNESS", json.dumps(r), flush=True)
                if k % 200 == 0:
                    print(f"{k}/{len(todo)} elapsed {time.time()-t0:.0f}s", flush=True)
    print("done", round(time.time() - t0, 1), flush=True)
