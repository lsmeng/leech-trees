"""Route 1: networkx nonisomorphic_trees (WROM). Route 2: nauty gentreeg (sparse6).
Both canonicalized with a certificate independent of either generator (AHU string from center),
then compared as sets. Output: data/trees_{n}.jsonl with canonical edge lists."""
import sys, json, subprocess, networkx as nx
from collections import Counter

def ahu_cert(G):
    n = G.number_of_nodes()
    centers = nx.center(G)
    def enc(v, p):
        return "(" + "".join(sorted(enc(c, v) for c in G[v] if c != p)) + ")"
    return min(enc(c, -1) for c in centers)

def route_nx(n):
    return {ahu_cert(T): sorted(map(tuple, map(sorted, T.edges()))) for T in nx.nonisomorphic_trees(n)}

def route_nauty(n):
    out = subprocess.run(["gentreeg", "-q", str(n)], capture_output=True, text=True, check=True).stdout
    d = {}
    for line in out.split("\n"):
        line = line.strip()
        if not line: continue
        G = nx.from_sparse6_bytes(line.encode())
        d[ahu_cert(G)] = sorted(map(tuple, map(sorted, G.edges())))
    return d

if __name__ == "__main__":
    n = int(sys.argv[1])
    a = route_nx(n); b = route_nauty(n)
    print(f"n={n}: networkx={len(a)} nauty={len(b)} same_set={set(a)==set(b)}")
    assert set(a) == set(b)
    with open(f"data/trees_{n}.jsonl", "w") as f:
        for i, cert in enumerate(sorted(a)):
            f.write(json.dumps({"id": i, "n": n, "edges": a[cert]}) + "\n")
    print("wrote", f"data/trees_{n}.jsonl")
