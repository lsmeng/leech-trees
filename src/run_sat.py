"""Sharded, resumable SAT driver.  For each topology in data/trees_{n}.jsonl:
encode (sat_encode.Encoding) -> DIMACS -> CDCL solver (cadical|kissat) with a DRAT proof ->
SAT: decode + both checkers;  UNSAT: drat-trim verifies the proof.  Appends one JSON record per
topology to results/sat_order_{n}{tag}.jsonl and skips ids already present.

usage: python src/run_sat.py N [--procs 8] [--timeout 600] [--solver cadical] [--variant onehot]
          [--dirs 3] [--no-sym] [--parity] [--ids 1,2,3 | --sample 30 --seed 0] [--tag _x]
          [--keep-proofs] [--check-timeout 20000] [--no-check]
"""
import argparse, json, os, sys, time, subprocess, random, tempfile, shutil
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sat_encode import Encoding
import checker_a, checker_b

DRAT_TRIM = os.path.join(ROOT, "tools", "drat-trim", "drat-trim")
CFG = {}


def _init(cfg):
    CFG.update(cfg)


def solve_one(rec):
    n, edges, tid = rec["n"], rec["edges"], rec["id"]
    cfg = CFG
    out = {"id": tid, "n": n, "solver": cfg["solver"], "variant": cfg["variant"], "dirs": cfg["dirs"]}
    t0 = time.time()
    E = Encoding(n, edges, variant=cfg["variant"], dirs=cfg["dirs"], symbreak=not cfg["no_sym"],
                 parity=cfg["parity"], amo=cfg["amo"])
    wd = tempfile.mkdtemp(prefix=f"leech{n}_{tid}_", dir=cfg["tmpdir"])
    cnf = os.path.join(wd, "f.cnf"); proof = os.path.join(wd, "f.drat")
    E.write_dimacs(cnf)
    out.update(E.stats()); out["encode_time"] = round(time.time() - t0, 3)
    out["cnf_bytes"] = os.path.getsize(cnf)
    T = cfg["timeout"]
    if cfg["solver"] == "cadical":
        cmd = ["cadical", "-q", "-t", str(int(T)), cnf, proof]
    else:
        cmd = ["kissat", "-q", f"--time={int(T)}", cnf, proof]
    t1 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=T + 30)
        rc, so = r.returncode, r.stdout
    except subprocess.TimeoutExpired:
        rc, so = -1, ""
    out["solve_time"] = round(time.time() - t1, 3)
    out["proof_bytes"] = os.path.getsize(proof) if os.path.exists(proof) else 0
    if rc == 10:
        model = [int(t) for line in so.splitlines() if line.startswith("v") for t in line.split()[1:]]
        w = E.decode(model)
        out["status"] = "SAT"; out["witness"] = w
        out["check_a"] = checker_a.is_leech(n, w)[0]; out["check_b"] = checker_b.is_leech(n, w)[0]
    elif rc == 20:
        out["status"] = "UNSAT"
        if not cfg["no_check"]:
            t2 = time.time()
            try:
                d = subprocess.run([DRAT_TRIM, cnf, proof, "-t", str(cfg["check_timeout"])],
                                   capture_output=True, text=True, timeout=cfg["check_timeout"] + 60)
                s = [l for l in d.stdout.splitlines() if l.startswith("s ")]
                out["drat"] = s[-1][2:] if s else "NO-RESULT rc=%d" % d.returncode
            except subprocess.TimeoutExpired:
                out["drat"] = "CHECK-TIMEOUT"
            out["drat_time"] = round(time.time() - t2, 3)
    else:
        out["status"] = "TIMEOUT" if rc in (0, -1) else f"ERR{rc}"
    if cfg["keep_proofs"] and out.get("status") == "UNSAT":
        dst = os.path.join(ROOT, "results", "proofs", f"n{n}")
        os.makedirs(dst, exist_ok=True)
        shutil.copy(cnf, os.path.join(dst, f"{tid}.cnf")); shutil.copy(proof, os.path.join(dst, f"{tid}.drat"))
    shutil.rmtree(wd, ignore_errors=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--solver", default="cadical", choices=["cadical", "kissat"])
    ap.add_argument("--variant", default="order", choices=["onehot", "order", "hybrid"])
    ap.add_argument("--dirs", type=int, default=3)
    ap.add_argument("--amo", default="seqcounter")
    ap.add_argument("--no-sym", action="store_true"); ap.add_argument("--parity", action="store_true")
    ap.add_argument("--ids", default=None); ap.add_argument("--sample", type=int, default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="")
    ap.add_argument("--keep-proofs", action="store_true")
    ap.add_argument("--no-check", action="store_true")
    ap.add_argument("--check-timeout", type=int, default=20000)
    ap.add_argument("--tmpdir", default=os.environ.get("LEECH_TMP", None))
    a = ap.parse_args()
    CFG.update(vars(a))
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "data", f"trees_{a.n}.jsonl"))]
    if a.ids:
        want = set(int(x) for x in a.ids.split(","))
        recs = [r for r in recs if r["id"] in want]
    elif a.sample:
        recs = random.Random(a.seed).sample(recs, a.sample)
    outp = os.path.join(ROOT, "results", f"sat_order_{a.n}{a.tag}.jsonl")
    done = set()
    if os.path.exists(outp):
        done = {json.loads(l)["id"] for l in open(outp)}
    todo = [r for r in recs if r["id"] not in done]
    print(f"n={a.n} selected={len(recs)} done={len(done)} todo={len(todo)} procs={a.procs} "
          f"solver={a.solver} variant={a.variant} dirs={a.dirs} T={a.timeout}", flush=True)
    t0 = time.time(); k = 0; counts = {}
    with Pool(a.procs, initializer=_init, initargs=(dict(CFG),)) as pool, open(outp, "a") as f:
        for r in pool.imap_unordered(solve_one, todo, chunksize=1):
            f.write(json.dumps(r) + "\n"); f.flush(); k += 1
            counts[r["status"]] = counts.get(r["status"], 0) + 1
            if r["status"] == "SAT":
                print("!!! WITNESS", json.dumps(r), flush=True)
            print(f"[{k}/{len(todo)}] id={r['id']} {r['status']} solve={r['solve_time']}s "
                  f"proof={r['proof_bytes']/1e6:.1f}MB drat={r.get('drat','-')} "
                  f"({r.get('drat_time','-')}s) ncl={r['ncl']}", flush=True)
    print("done", round(time.time() - t0, 1), "s", counts, flush=True)


if __name__ == "__main__":
    main()
