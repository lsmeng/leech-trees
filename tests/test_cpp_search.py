"""Regression for the C++ engine (bin/leech_search).  Run: source .venv/bin/activate; python -m pytest tests/test_cpp_search.py
Checks: n=4 (2 SAT), n=6 (exactly the known double-star SAT, 5 UNSAT), n=5,9 all UNSAT, witnesses pass both checkers,
solution counts identical across prune subsets and modes on planted (random-weight) instances with a custom target set
(binary built with -DNW=8), and complete symmetry breaking (count with sym == count without sym / |Aut|)."""
import json, os, random, subprocess, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import checker_a, checker_b
ROOT = os.path.join(os.path.dirname(__file__), "..")
BIN = os.environ.get("LEECH_BIN", os.path.join(ROOT, "bin", "leech_search"))          # e.g. LEECH_BIN=bin/leech_search_v2
BIN8 = os.environ.get("LEECH_BIN8", os.path.join(ROOT, "bin", "leech_search_nw8"))   # -DNW=8 build of the same source

def run(binary, recs, flags=()):
    inp = "".join(json.dumps(r) + "\n" for r in recs)
    out = subprocess.run([binary, *flags], input=inp, capture_output=True, text=True, check=True).stdout
    return [json.loads(l) for l in out.splitlines() if l.startswith("{")]

def load(n): return [json.loads(l) for l in open(os.path.join(ROOT, f"data/trees_{n}.jsonl"))]

def test_small_orders():
    r4 = run(BIN, load(4)); assert [x["status"] for x in r4] == ["SAT", "SAT"]
    r6 = run(BIN, load(6)); assert sum(x["status"] == "SAT" for x in r6) == 1 and len(r6) == 6
    for r in r4 + r6:
        if r["witness"]:
            e = [tuple(x) for x in r["witness"]]
            assert checker_a.is_leech(r["n"], e)[0] and checker_b.is_leech(r["n"], e)[0]
    for n in (5, 9):
        assert all(x["status"] == "UNSAT" for x in run(BIN, load(n)))
        assert all(x["status"] == "UNSAT" for x in run(BIN, load(n), ["--no-parity"]))

def planted(seed=7, per_n=4):
    import networkx as nx
    random.seed(seed); recs = []; i = 0
    for n in (7, 8, 9, 10):
        trees = list(nx.nonisomorphic_trees(n)); random.shuffle(trees)
        for T in trees[:per_n]:
            edges = list(T.edges())
            for _ in range(2000):
                ws = dict(zip(edges, random.sample(range(1, 60), len(edges))))
                G = nx.Graph(); G.add_weighted_edges_from([(u, v, ws[(u, v)]) for u, v in edges])
                d = dict(nx.all_pairs_dijkstra_path_length(G)); vals = sorted(d[u][v] for u in range(n) for v in range(u + 1, n))
                if len(set(vals)) == len(vals) and max(vals) <= 500: break
            else: continue
            recs.append({"id": i, "n": n, "edges": [list(e) for e in edges], "target": vals}); i += 1
    return recs

def test_planted_prune_consistency():
    if not os.path.exists(BIN8): return
    recs = planted()
    base = [r["nsol"] for r in run(BIN8, recs, ["--count", "--no-sym"])]
    assert all(c >= 1 for c in base)
    for flags in (["--no-fc"], ["--no-hall"], ["--no-grp"], ["--no-sum"], ["--no-parity"], ["--no-top"], ["--no-grp2"], ["--cover"],
                  ["--no-fc", "--no-hall", "--no-grp", "--no-sum", "--no-parity", "--no-top"], ["--mode", "edge"], ["--mode", "ff"],
                  ["--legacy"], ["--legacy", "--no-fc"], ["--wcover", "0"], ["--wcover", "5"], ["--wcover", "100000"], ["--no-look"],
                  ["--no-look", "--wcover", "0"], ["--hallw", "8"], ["--hallw", "78"]):
        assert [r["nsol"] for r in run(BIN8, recs, ["--count", "--no-sym", *flags])] == base, flags
    import networkx as nx
    from networkx.algorithms.isomorphism import GraphMatcher
    sym = [r["nsol"] for r in run(BIN8, recs, ["--count"])]
    for rec, a, b in zip(recs, base, sym):
        G = nx.Graph(rec["edges"]); aut = sum(1 for _ in GraphMatcher(G, G).isomorphisms_iter())
        assert b * aut == a
