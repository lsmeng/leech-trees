"""REFEREE (forest engine) differential harness.  Read-only w.r.t. src/ and bin/.
Checks (all on bin/forest_search unless FOREST_BIN is set):
  A. per-level node counts of the engine == independent Python enumerator (tests/referee_forest_enum.py) on planted
     (custom-target) instances n=6..NA (exercises the FULL != [1..N] code paths: RnotF holes, custom N) and nsol equal;
  B. nsol(forest engine, --target) == sum over ALL topologies of the per-topology engine `--count` (bin/leech_search v1
     production and bin/leech_search_v2), n=6..NB, planted targets (>=1 solution) and the standard Leech target;
  C. sharding: for several (K, L) incl. K not dividing #level-L nodes: per-depth histograms satisfy
     hist_shard[d] == hist_full[d] for d <= L and sum_shards hist[d] == hist_full[d] for d > L; sum nsol == nsol.
Usage: .venv/bin/python tests/referee_forest_diff.py [--na 9] [--nb 11] [--per 3] [--seed 7] [--procs 2]
Never uses more than --procs concurrent engine processes (an n=18 production run shares this machine)."""
import argparse, json, os, random, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from referee_forest_enum import enumerate_tree, engine_depth_hist, leech_target
import networkx as nx
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FBIN = os.environ.get("FOREST_BIN", os.path.join(ROOT, "bin", "forest_search"))
PT_BINS = [os.path.join(ROOT, "bin", b) for b in ("leech_search", "leech_search_v2") if os.path.exists(os.path.join(ROOT, "bin", b))]
NICE = ["nice", "-n", "15"]

def planted(n, rng, wmax, cap=190):
    trees = list(nx.nonisomorphic_trees(n))
    while True:
        T = rng.choice(trees); edges = list(T.edges())
        ws = dict(zip(edges, rng.sample(range(1, wmax), len(edges))))
        G = nx.Graph(); G.add_weighted_edges_from([(u, v, ws[(u, v)]) for u, v in edges])
        d = dict(nx.all_pairs_dijkstra_path_length(G)); vals = sorted(d[u][v] for u in range(n) for v in range(u + 1, n))
        if len(set(vals)) == len(vals) and max(vals) <= cap: return edges, ws, vals

def forest_run(n, target=None, extra=()):
    args = NICE + [FBIN, str(n), "-q", *extra]
    if target: args += ["--target", ",".join(map(str, sorted(target)))]
    p = subprocess.run(args, capture_output=True, text=True, check=True)
    hist = {}
    for line in p.stderr.splitlines():
        if line.startswith("depth:"):
            for tok in line.split()[1:]:
                dd, c = tok.split(":"); hist[int(dd)] = int(c)
    rec = json.loads([l for l in p.stdout.splitlines() if l.startswith("{")][-1])
    return hist, rec

def per_topology_sum(binp, n, target):
    trees = list(nx.nonisomorphic_trees(n))
    recs = [{"id": i, "n": n, "edges": [list(e) for e in t.edges()], "target": sorted(target)} for i, t in enumerate(trees)]
    inp = "".join(json.dumps(r) + "\n" for r in recs)
    out = subprocess.run(NICE + [binp, "--count"], input=inp, capture_output=True, text=True, check=True).stdout
    rs = [json.loads(l) for l in out.splitlines() if l.startswith("{")]
    assert len(rs) == len(trees), (binp, n, len(rs), len(trees))
    assert all(r.get("status") != "UNKNOWN" for r in rs)
    return sum(r["nsol"] for r in rs), len(trees)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--na", type=int, default=9); ap.add_argument("--nb", type=int, default=11)
    ap.add_argument("--per", type=int, default=3); ap.add_argument("--seed", type=int, default=7); ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--skip", default=""); ap.add_argument("--nd", type=int, default=8)
    a = ap.parse_args(); rng = random.Random(a.seed); bad = 0; t0 = time.time()
    # ---------------- A: planted per-level counts vs Python enumerator ----------------
    if "A" not in a.skip:
        for n in range(6, a.na + 1):
            for k in range(a.per):
                edges, ws, vals = planted(n, rng, wmax={6: 20, 7: 25, 8: 30, 9: 35, 10: 40}.get(n, 45))
                T = frozenset(vals)
                st = enumerate_tree(n, T, sumprune=True, rule="brute")
                se = enumerate_tree(n, T, sumprune=True, rule="enginerule")
                hist, rec = forest_run(n, T)
                py = [st[l]["abstract"] for l in sorted(st)]; en = [hist[l] for l in sorted(hist) if hist[l]]
                pysol = sum(v["sols"] for v in st.values()); dups = sum(v["dups"] for v in se.values())
                ok = py == en and pysol == rec["nsol"] and dups == 0 and [se[l]["generated"] for l in sorted(se)] == py
                bad += not ok
                print(f"A n={n} #{k} target max {max(vals)} py levels {py} sols {pysol} | engine {en} nsol {rec['nsol']} | enginerule dups {dups} {'OK' if ok else 'MISMATCH'}", flush=True)
    # ---------------- B: forest nsol == sum over topologies of per-topology --count ----------------
    if "B" not in a.skip:
        for n in range(6, a.nb + 1):
            targets = [("planted", planted(n, rng, wmax={6: 20, 7: 25, 8: 30, 9: 35, 10: 40, 11: 45}.get(n, 50))[2]) for _ in range(a.per)]
            targets.append(("leech", sorted(leech_target(n))))
            if n <= 9:   # hunt for planted targets with >= 2 non-isomorphic solutions (rare): the count identity is then non-trivial
                found = 0
                for _ in range(400):
                    vals = planted(n, rng, 2 * n + 2)[2]
                    if forest_run(n, vals)[1]["nsol"] >= 2:
                        targets.append(("multi", vals)); found += 1
                        if found >= 3: break
            for kind, vals in targets:
                _, rec = forest_run(n, vals)
                res = {}
                with ThreadPoolExecutor(max_workers=max(1, a.procs - 1)) as ex:
                    futs = {ex.submit(per_topology_sum, b, n, vals): b for b in PT_BINS}
                    for f, b in futs.items(): res[os.path.basename(b)] = f.result()
                ok = all(v[0] == rec["nsol"] for v in res.values()) and (kind == "leech" or rec["nsol"] >= 1)
                bad += not ok
                print(f"B n={n} {kind:7s} forest nsol {rec['nsol']} nodes {rec['nodes']} | per-topology " +
                      ", ".join(f"{k}: {v[0]} over {v[1]} topologies" for k, v in res.items()) + f" {'OK' if ok else 'MISMATCH'}", flush=True)
    # ---------------- C: sharding partition ----------------
    if "C" not in a.skip:
        cases = []
        for n in (10, 11, 12):
            cases.append((n, None))
            cases.append((n, planted(n, rng, wmax=40 if n < 12 else 50)[2]))
        for n, vals in cases:
            full_h, full = forest_run(n, vals)
            for K, L in ((3, 6), (7, 5), (5, 4), (13, 8), (4, 9), (1000, 7)):
                if L > n - 1: continue
                nL = full_h.get(L, 0)
                def one(i): return forest_run(n, vals, ("--shard", str(i), str(K), "--shard-level", str(L)))
                with ThreadPoolExecutor(max_workers=a.procs) as ex: parts = list(ex.map(one, range(K)))
                ok = sum(p[1]["nsol"] for p in parts) == full["nsol"]
                for d in full_h:
                    if d <= L: ok &= all(p[0].get(d, 0) == full_h[d] for p in parts)
                    else: ok &= sum(p[0].get(d, 0) for p in parts) == full_h[d]
                # nodes identity: sum = K * prefix(<=L) + rest
                pre = sum(full_h[d] for d in full_h if d <= L)
                ok &= sum(p[1]["nodes"] for p in parts) == K * pre + (full["nodes"] - pre)
                # every shard done, none empty beyond prefix unless K > nL
                nonempty = sum(1 for p in parts if p[1]["nodes"] > pre)
                ok &= nonempty <= min(K, nL)   # a level-L subtree may be empty (the node dies), so only an upper bound
                bad += not ok
                print(f"C n={n} {'leech' if vals is None else 'planted'} K={K} L={L} level-L nodes {nL} (nL%K={nL % K}) full nsol {full['nsol']} nodes {full['nodes']} shards-sum nodes {sum(p[1]['nodes'] for p in parts)} nonempty {nonempty} {'OK' if ok else 'MISMATCH'}", flush=True)
    # ---------------- D: forest nsol == sum over topologies of (#labelings by a NO-FORCING plain DFS) / |Aut| ----------------
    if "D" not in a.skip:
        from referee_enum import count_dfs
        from networkx.algorithms.isomorphism import GraphMatcher
        for n in range(5, min(a.nd, 9) + 1):
            targets = [planted(n, rng, wmax=2 * n + 4)[2] for _ in range(a.per)] + [sorted(leech_target(n))]
            for vals in targets:
                trees = list(nx.nonisomorphic_trees(n)); tot = 0
                for T in trees:
                    edges = [tuple(e) for e in T.edges()]
                    lab = count_dfs(n, edges, vals)
                    aut = sum(1 for _ in GraphMatcher(T, T).isomorphisms_iter())
                    assert lab % aut == 0, (n, edges, lab, aut)
                    tot += lab // aut
                _, rec = forest_run(n, vals)
                ok = tot == rec["nsol"]; bad += not ok
                print(f"D n={n} target max {max(vals)} forest nsol {rec['nsol']} | no-forcing DFS sum(labelings/|Aut|) {tot} {'OK' if ok else 'MISMATCH'}", flush=True)
    print(f"DONE mismatches={bad} in {time.time() - t0:.0f}s")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
