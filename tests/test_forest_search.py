"""Regression for the forest engine (bin/forest_search): known Leech trees (n=4: 2, n=6: 1, else 0 for n<=13),
solution counts identical to the per-topology engine summed over all topologies on planted targets, and shard consistency.
Build: scripts/build.sh (also builds bin/forest_search).  Run: python -m pytest tests/test_forest_search.py"""
import json, os, random, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import checker_a, checker_b
ROOT = os.path.join(os.path.dirname(__file__), "..")
FBIN = os.environ.get("FOREST_BIN", os.path.join(ROOT, "bin", "forest_search"))
BIN8 = os.environ.get("LEECH_BIN8", os.path.join(ROOT, "bin", "leech_search_nw8"))

def forest(n, *flags):
    out = subprocess.run([FBIN, str(n), *flags], capture_output=True, text=True, check=True).stdout
    sols = [l for l in out.splitlines() if l.startswith("SOL:")]
    rec = json.loads([l for l in out.splitlines() if l.startswith("{")][-1])
    return rec, sols

def parse_sol(line):
    return [tuple(int(x) for x in tok.replace("-", ":").split(":")) for tok in line.split()[1:]]

def test_known_orders():
    r4, s4 = forest(4); assert r4["nsol"] == 2 and len(s4) == 2
    r6, s6 = forest(6); assert r6["nsol"] == 1
    for line in s4 + s6:
        e = parse_sol(line); n = len(e) + 1
        assert checker_a.is_leech(n, e)[0] and checker_b.is_leech(n, e)[0]
    for n in (5, 7, 8, 9, 10, 11):
        assert forest(n, "-q")[0]["nsol"] == 0

def test_shards_partition():
    full, _ = forest(11, "-q")
    parts = [forest(11, "-q", "--shard", str(i), "3", "--shard-level", "6")[0] for i in range(3)]
    assert sum(p["nsol"] for p in parts) == full["nsol"]
    # nodes: every shard visits the common prefix (levels <= 6) plus its own subtrees
    assert sum(p["nodes"] for p in parts) > full["nodes"]

def test_matches_per_topology_engine():
    if not os.path.exists(BIN8): return
    import networkx as nx
    random.seed(5)
    for n in (7, 8):
        trees = list(nx.nonisomorphic_trees(n))
        for _ in range(2):
            T = random.choice(trees); edges = list(T.edges())
            for _ in range(5000):
                ws = dict(zip(edges, random.sample(range(1, 30), len(edges))))
                G = nx.Graph(); G.add_weighted_edges_from([(u, v, ws[(u, v)]) for u, v in edges])
                d = dict(nx.all_pairs_dijkstra_path_length(G)); vals = sorted(d[u][v] for u in range(n) for v in range(u + 1, n))
                if len(set(vals)) == len(vals) and max(vals) <= 150: break
            recs = [{"id": i, "n": n, "edges": [list(e) for e in t.edges()], "target": vals} for i, t in enumerate(trees)]
            inp = "".join(json.dumps(r) + "\n" for r in recs)
            out = subprocess.run([BIN8, "--count"], input=inp, capture_output=True, text=True, check=True).stdout
            tot = sum(json.loads(l)["nsol"] for l in out.splitlines() if l.startswith("{"))
            assert tot >= 1
            r, _ = forest(n, "--target", ",".join(map(str, vals)), "-q")
            assert r["nsol"] == tot
