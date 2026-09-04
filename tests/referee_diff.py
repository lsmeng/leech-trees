"""REFEREE differential test for the C++ engine (adversarial soundness audit; see docs/referee-report.md).
Usage: .venv/bin/python tests/referee_diff.py [--quick] [--nmax 10] [--per 3] [--seed 11] [--symn 12]
Builds referee binaries from src/leech_search.cpp (HEAD, fast path) into a scratch dir (never touches bin/), also tests the
production binary bin/leech_search (cluster build, 78d940c) read-only.  Ground truth = tests/referee_enum.py (plain DFS + CP-SAT).
Checks, for every topology n=7..nmax and several planted distinct-distance targets (max <= 190 so NW=3 binaries apply):
  (1) HEAD --count --no-sym  == independent DFS count            (any pruning rule unsound => mismatch, esp. 0 vs >0)
  (2) HEAD --count           * |Aut(T)| == (1)                    (symmetry breaking complete & non-redundant)
  (3) every flag subset / mode / legacy path gives the same count (rules individually sound)
  (4) bin/leech_search (cluster binary) same counts
  (5) status SAT/UNSAT of the default (first-solution) run agrees with count>0
  (6) symmetry stress: trees with the largest |Aut| for n=8..symn (planted), (1)-(4) again
  (7) the standard Leech target n=7..9 (all UNSAT), CP-SAT cross-check on a random subset
Exit code 1 on any discrepancy; details printed with the instance JSON so it can be replayed.
"""
import json, os, sys, random, subprocess, argparse, time, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from referee_enum import count_dfs, count_cpsat, leech_target
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCR = os.environ.get("REFEREE_SCRATCH", os.path.join(ROOT, "results", "referee_bin"))
os.makedirs(SCR, exist_ok=True)
SRC = os.path.join(ROOT, "src", "leech_search.cpp")
PROD = os.path.join(ROOT, "bin", "leech_search")

def build(name, src, extra=()):
    out = os.path.join(SCR, name)
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        subprocess.run(["clang++", "-O3", "-march=native", "-std=c++17", *extra, "-o", out, src], check=True)
    return out

def run(binary, recs, flags=()):
    inp = "".join(json.dumps(r) + "\n" for r in recs)
    p = subprocess.run([binary, *flags], input=inp, capture_output=True, text=True)
    if p.returncode != 0: raise RuntimeError(f"{binary} {flags} rc={p.returncode} stderr={p.stderr[-500:]}")
    out = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
    if len(out) != len(recs): raise RuntimeError(f"{binary} {flags}: {len(out)} outputs for {len(recs)} records; stderr={p.stderr[-500:]}")
    return out

def aut_size(edges, cap=None):
    """|Aut(T)| by explicit enumeration (independent of the engine); with cap, stops at cap+1 (returns cap+1)"""
    G = nx.Graph(edges); k = 0
    for _ in GraphMatcher(G, G).isomorphisms_iter():
        k += 1
        if cap is not None and k > cap: break
    return k

def plant(n, edges, rng, lo=1, hi=60, maxv=190, tries=300):
    for _ in range(tries):
        ws = dict(zip(edges, rng.sample(range(lo, hi), len(edges))))
        G = nx.Graph(); G.add_weighted_edges_from([(u, v, ws[(u, v)]) for u, v in edges])
        d = dict(nx.all_pairs_dijkstra_path_length(G)); vals = sorted(d[u][v] for u in range(n) for v in range(u + 1, n))
        if len(set(vals)) == len(vals) and max(vals) <= maxv: return vals
    return None

def plant_par(n, edges, rng, nodd, maxv=190, tries=2000):
    """planted target with exactly `nodd` odd edge weights (Taylor a small) -> parity DP gets exercised (esp. with --no-fc)"""
    for _ in range(tries):
        ws = rng.sample(range(2, 60, 2), len(edges) - nodd) + rng.sample(range(1, 60, 2), nodd); rng.shuffle(ws); ws = dict(zip(edges, ws))
        G = nx.Graph(); G.add_weighted_edges_from([(u, v, ws[(u, v)]) for u, v in edges])
        d = dict(nx.all_pairs_dijkstra_path_length(G)); vals = sorted(d[u][v] for u in range(n) for v in range(u + 1, n))
        if len(set(vals)) == len(vals) and max(vals) <= maxv: return vals
    return None

FLAGSETS = [[], ["--no-grp"], ["--no-hall"], ["--no-parity"], ["--no-top"], ["--no-sum"], ["--no-fc"], ["--no-grp2"],
            ["--legacy"], ["--legacy", "--no-fc"], ["--legacy", "--no-grp"], ["--legacy", "--no-hall"], ["--legacy", "--no-grp2"],
            ["--legacy", "--no-fc", "--no-hall", "--no-grp", "--no-sum", "--no-parity", "--no-top", "--no-grp2"],
            ["--legacy", "--no-fc", "--no-hall"], ["--legacy", "--no-fc", "--no-grp", "--no-hall", "--no-sum", "--no-top"],   # parity (+grp2) nearly alone
            ["--legacy", "--cover"], ["--legacy", "--match"], ["--wcover", "200"], ["--wcover", "50", "--no-grp"],
            ["--mode", "edge"], ["--mode", "edge", "--order", "bfs"], ["--mode", "edge", "--order", "rev"], ["--mode", "ff"],
            # v2 (4785a43+) options: window cover / lookahead / windowed Hall
            ["--no-look"], ["--wcover", "0"], ["--wcover", "0", "--no-look"], ["--wcover", "500"], ["--hallw", "78"], ["--hallw", "3"], ["--hallw", "0"],
            ["--no-look", "--wcover", "0", "--no-grp", "--no-hall", "--no-parity", "--no-top", "--no-sum"]]
PROD_FLAGSETS = [[], ["--no-grp"], ["--no-hall"], ["--no-parity"], ["--no-top"], ["--no-sum"], ["--no-fc"], ["--no-grp2"], ["--cover"], ["--match"],
                 ["--no-fc", "--no-hall"], ["--no-fc", "--no-grp", "--no-hall", "--no-sum", "--no-top"], ["--no-fc", "--no-grp"], ["--no-hall", "--no-grp"],
                 ["--no-fc", "--no-hall", "--no-grp", "--no-sum", "--no-parity", "--no-top", "--no-grp2"], ["--mode", "edge"], ["--mode", "ff"]]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--quick", action="store_true"); ap.add_argument("--nmax", type=int, default=10)
    ap.add_argument("--per", type=int, default=3); ap.add_argument("--seed", type=int, default=11); ap.add_argument("--symn", type=int, default=12)
    ap.add_argument("--cpsat", type=int, default=25, help="number of random instances cross-checked with CP-SAT")
    ap.add_argument("--src", action="append", default=None, help="engine source(s) to audit (repeatable; default src/leech_search.cpp; frozen copies are safer)")
    ap.add_argument("--maxaut", type=int, default=20000, help="skip symmetry-stress trees with |Aut| above this (DFS enumerates all symmetric copies)")
    ap.add_argument("--no-prod", action="store_true", help="skip bin/leech_search")
    A = ap.parse_args(); rng = random.Random(A.seed)
    bins = {}
    for src in (A.src or [SRC]):
        src_sha = hashlib.sha256(open(src, "rb").read()).hexdigest()[:16]
        bins[f"SRC[{os.path.basename(src)}:{src_sha}]"] = build(f"ref_nw3_{src_sha}", src)
    if os.path.exists(PROD) and not A.no_prod: bins["PROD[bin/leech_search]"] = PROD
    for k, v in bins.items(): print("binary", k, "->", v, "md5", hashlib.md5(open(v, "rb").read()).hexdigest(), flush=True)
    bad = 0; ninst = 0; t0 = time.time()
    def report(msg, rec):
        nonlocal bad; bad += 1; print("DISCREPANCY:", msg, "\n  instance:", json.dumps(rec), flush=True)
    # ---- instances ----
    insts = []
    ranges = [(1, 60), (1, 30), (1, 20)] if not A.quick else [(1, 60)]
    for n in range(7, A.nmax + 1):
        trees = list(nx.nonisomorphic_trees(n))
        for T in trees:
            edges = [tuple(e) for e in T.edges()]
            for j, (lo, hi) in enumerate(ranges[:A.per]):
                tgt = plant(n, edges, rng, lo, hi)
                if tgt is None: continue
                insts.append({"id": len(insts), "n": n, "edges": [list(e) for e in edges], "target": tgt, "kind": f"planted{lo}-{hi}"})
        # standard target (all UNSAT for 7<=n<=9 by literature; we do not assume it, DFS decides)
        if n <= 9:
            for T in trees:
                edges = [tuple(e) for e in T.edges()]
                insts.append({"id": len(insts), "n": n, "edges": [list(e) for e in edges], "target": leech_target(n), "kind": "leech"})
    # parity-skewed planted targets (0/1/2 odd weights): Taylor a in {0,1,2}, parity DP actually fires (with --no-fc / legacy)
    for n in range(7, A.nmax + 1):
        trees = list(nx.nonisomorphic_trees(n))
        for T in trees[::3]:
            edges = [tuple(e) for e in T.edges()]
            for nodd in (0, 1, 2):
                tgt = plant_par(n, edges, rng, nodd)
                if tgt is None: continue
                insts.append({"id": len(insts), "n": n, "edges": [list(e) for e in edges], "target": tgt, "kind": f"par{nodd}"})
    # symmetry stress: top-|Aut| trees for n=8..symn
    for n in range(8, A.symn + 1):
        trees = list(nx.nonisomorphic_trees(n))
        scored = sorted(((a, i) for a, i in ((aut_size(list(T.edges()), A.maxaut), i) for i, T in enumerate(trees)) if a <= A.maxaut), reverse=True)
        pick = [i for _, i in scored[:8]] + rng.sample(range(len(trees)), min(6, len(trees)))
        for i in pick:
            edges = [tuple(e) for e in trees[i].edges()]
            for (lo, hi) in [(1, 60), (1, 30)]:
                tgt = plant(n, edges, rng, lo, hi)
                if tgt is None: continue
                insts.append({"id": len(insts), "n": n, "edges": [list(e) for e in edges], "target": tgt, "kind": f"sym{lo}-{hi}"})
    print(f"{len(insts)} instances", flush=True)
    # ---- ground truth (cached per instance set) ----
    cache = os.path.join(SCR, f"truth_s{A.seed}_n{A.nmax}_p{A.per}_sym{A.symn}_q{int(A.quick)}.json")
    key = hashlib.sha256(json.dumps(insts, sort_keys=True).encode()).hexdigest()
    truth = {}
    if os.path.exists(cache):
        c = json.load(open(cache))
        if c.get("key") == key: truth = {int(k): v for k, v in c["truth"].items()}; print("ground truth loaded from", cache)
    if not truth:
        for r in insts:
            truth[r["id"]] = count_dfs(r["n"], [tuple(e) for e in r["edges"]], r["target"])
        json.dump({"key": key, "truth": truth}, open(cache, "w"))
    print("DFS ground truth done", round(time.time() - t0, 1), "s; SAT instances:", sum(1 for v in truth.values() if v > 0), flush=True)
    for r in rng.sample(insts, min(A.cpsat, len(insts))):
        c = count_cpsat(r["n"], [tuple(e) for e in r["edges"]], r["target"])
        if c != truth[r["id"]]: report(f"CP-SAT {c} != DFS {truth[r['id']]}", r)
    print("CP-SAT cross-check done", round(time.time() - t0, 1), flush=True)
    # ---- engine runs ----
    stripped = [{k: r[k] for k in ("id", "n", "edges", "target")} for r in insts]
    auts = {r["id"]: aut_size([tuple(e) for e in r["edges"]]) for r in insts}
    for name, b in bins.items():
        if b is None: continue
        base = run(b, stripped, ["--count", "--no-sym"])
        for r, o in zip(insts, base):
            if o["nsol"] != truth[r["id"]]: report(f"{name} --count --no-sym nsol={o['nsol']} != truth {truth[r['id']]}", r)
        sym = run(b, stripped, ["--count"])
        for r, o in zip(insts, sym):
            if o["nsol"] * auts[r["id"]] != truth[r["id"]]: report(f"{name} --count nsol={o['nsol']} * |Aut|={auts[r['id']]} != truth {truth[r['id']]}", r)
        first = run(b, stripped, [])
        for r, o in zip(insts, first):
            if (o["status"] == "SAT") != (truth[r["id"]] > 0): report(f"{name} default status {o['status']} vs truth count {truth[r['id']]}", r)
            if o["status"] == "SAT":
                # verify witness realizes target
                G = nx.Graph(); G.add_weighted_edges_from([(u, v, w) for u, v, w in o["witness"]])
                d = dict(nx.all_pairs_dijkstra_path_length(G)); vals = sorted(d[u][v] for u in range(r["n"]) for v in range(u + 1, r["n"]))
                if vals != r["target"]: report(f"{name} witness does not realize target", r)
        for fl in (FLAGSETS if name.startswith("SRC") else PROD_FLAGSETS):
            probe = subprocess.run([b, *fl], input=json.dumps(stripped[0]) + "\n", capture_output=True, text=True)
            if probe.returncode != 0 and "cannot open" in probe.stderr: print(f"  {name}: flags {fl} not supported by this build, skipped"); continue
            try: res = run(b, stripped, ["--count", "--no-sym", *fl])
            except RuntimeError as ex: report(f"{name} {fl} crashed: {ex}", {}); continue
            for r, o in zip(insts, res):
                if o["nsol"] != truth[r["id"]]: report(f"{name} {fl} --count --no-sym nsol={o['nsol']} != truth {truth[r['id']]}", r)
            res = run(b, stripped, ["--count", *fl])
            for r, o in zip(insts, res):
                if o["nsol"] * auts[r["id"]] != truth[r["id"]]: report(f"{name} {fl} --count nsol*aut={o['nsol']}*{auts[r['id']]} != truth {truth[r['id']]}", r)
        print(name, "done", round(time.time() - t0, 1), flush=True)
    kinds = {}
    for r in insts: kinds.setdefault(r["kind"], [0, 0]); kinds[r["kind"]][0] += 1; kinds[r["kind"]][1] += truth[r["id"]] > 0
    print("instances by kind (total, SAT):", kinds)
    print("DISCREPANCIES:", bad); sys.exit(1 if bad else 0)

if __name__ == "__main__": main()
