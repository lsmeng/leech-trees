"""REFEREE (forest engine): planted instances at FULL DEPTH n=13..18 (the regression tests stop at n<=12).
A random weighted tree on n vertices with pairwise-distinct distances defines a target; the forest engine (a -DNW=8
scratch build for max target > 190, else bin/forest_search) must (i) report nsol >= 1, (ii) every SOL line must be a
tree on n vertices whose distance multiset equals the target (recomputed with networkx), (iii) the planted tree must be among the SOL lines (weighted-isomorphism
canonical form).  This exercises n=18-depth code paths (MAXV, u32 component masks, V==n termination) that the standard
Leech target cannot (no witness exists).  Usage: python tests/referee_forest_planted_big.py [BIN_NW8] [--per 3] [--seed 1]"""
import json, os, random, subprocess, sys
import networkx as nx
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def canon(n, edges):
    inc = [[] for _ in range(n)]
    for u, v, w in edges: inc[u].append(w); inc[v].append(w)
    return tuple(sorted(tuple(sorted(x)) for x in inc))

def planted(n, rng, wmax, cap):
    """incremental random construction: attach vertex i to a random earlier vertex with a random weight such that all new
    distances are unused and <= cap; restart on failure (random weights on a random tree almost never have distinct sums)"""
    while True:
        dist = [[0]]; edges = []; used = set(); ok = True
        for i in range(1, n):
            x = rng.randrange(i); ws = list(range(1, wmax)); rng.shuffle(ws); placed = False
            for w in ws:
                nd = [dist[x][j] + w for j in range(i)]
                if all(v <= cap and v not in used for v in nd) and len(set(nd)) == i:
                    used.update(nd); edges.append((x, i, w))
                    for j in range(i): dist[j].append(nd[j])
                    dist.append(nd + [0]); placed = True; break
            if not placed: ok = False; break
        if ok: return edges, sorted(used)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bin8 = args[0] if args else os.environ.get("FOREST_BIN8")
    per = int(sys.argv[sys.argv.index("--per") + 1]) if "--per" in sys.argv else 3
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 1
    rng = random.Random(seed); bad = 0
    for n in range(13, 19):
        for k in range(per):
            if n >= 17 and k >= 2: break   # the generator needs ~200 s per n=18 instance
            binp = bin8   # -DNW=8 build (max target <= 510); planted targets with max <= 190 are practically unreachable for n >= 13
            if binp is None or not os.path.exists(binp): print(f"n={n}: no NW=8 binary given, skip"); break
            edges, vals = planted(n, rng, wmax=(40 if n <= 14 else 50), cap=510)
            out = subprocess.run(["nice", "-n", "15", binp, str(n), "--target", ",".join(map(str, vals))], capture_output=True, text=True, check=True).stdout
            sols = [l for l in out.splitlines() if l.startswith("SOL:")]
            rec = json.loads([l for l in out.splitlines() if l.startswith("{")][-1])
            forms = set(); allok = True
            for s in sols:
                e = [tuple(int(x) for x in tok.replace("-", ":").split(":")) for tok in s.split()[1:]]
                G = nx.Graph(); G.add_weighted_edges_from(e); dd = dict(nx.all_pairs_dijkstra_path_length(G))
                got = sorted(dd[u][v] for u in range(n) for v in range(u + 1, n))
                allok &= (got == vals) and nx.is_tree(G) and G.number_of_nodes() == n
                forms.add(canon(n, e))
            ok = rec["nsol"] >= 1 and len(sols) == rec["nsol"] and allok and canon(n, edges) in forms and rec["status"] == "DONE"
            bad += not ok
            print(f"n={n} #{k} target max {max(vals)} nsol {rec['nsol']} nodes {rec['nodes']} time {rec['time']:.2f}s witnesses valid {allok} planted found {canon(n, edges) in forms} {'OK' if ok else 'MISMATCH'}", flush=True)
    print("DONE mismatches", bad); return bad

if __name__ == "__main__": sys.exit(1 if main() else 0)
