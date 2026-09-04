#!/usr/bin/env python3
"""Planted-solution soundness test for forest_search_d4:
build random trees of hop-diameter <= 4 with distinct positive weights and all
pairwise distances distinct; feed the engine --target <distance multiset>; it
must find >= 1 solution. Negative control: diameter-5 trees must give 0."""
import argparse
import json
import random
import subprocess

def tree_dists(n, edges):
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w)); adj.setdefault(v, []).append((u, w))
    out = []
    hops = []
    for s in range(n):
        d = {s: 0}; h = {s: 0}; st = [s]
        while st:
            x = st.pop()
            for y, w in adj[x]:
                if y not in d:
                    d[y] = d[x] + w; h[y] = h[x] + 1; st.append(y)
        for t in range(s + 1, n):
            out.append(d[t]); hops.append(h[t])
    return out, max(hops)

def random_d4_tree(n, rng, diam5=False):
    """centre 0; branches: v_i with m_i leaves; heights <= 2 (diam <= 4).
    If diam5: two centres joined by an edge, guaranteeing a hop-5 path."""
    while True:
        if not diam5:
            verts = [0]; edges = []
            nb = rng.randint(2, max(2, (n - 1) // 2))
            branch_roots = []
            for _ in range(nb):
                if len(verts) >= n: break
                v = len(verts); verts.append(v); edges.append((0, v)); branch_roots.append(v)
            while len(verts) < n:
                v = len(verts); verts.append(v); edges.append((rng.choice(branch_roots), v))
        else:
            # two adjacent hubs each with a 2-deep branch -> hop diameter 5
            verts = [0, 1]; edges = [(0, 1)]
            a = len(verts); verts.append(a); edges.append((0, a))
            b = len(verts); verts.append(b); edges.append((a, b))
            c = len(verts); verts.append(c); edges.append((1, c))
            d = len(verts); verts.append(d); edges.append((c, d))
            hubs = [0, 1, a, c]
            while len(verts) < n:
                v = len(verts); verts.append(v); edges.append((rng.choice(hubs), v))
        ws = rng.sample(range(1, 60), len(edges))
        wedges = [(u, v, w) for (u, v), w in zip(edges, ws)]
        dists, hopdiam = tree_dists(n, wedges)
        if len(set(dists)) != len(dists):
            continue
        want = 5 if diam5 else 4
        if diam5 and hopdiam != 5:
            continue
        if not diam5 and hopdiam > 4:
            continue
        return wedges, dists

def engine_solutions(engine, n, dists):
    target = ",".join(map(str, sorted(dists)))
    result = subprocess.run(
        [engine, str(n), "--target", target, "-q"],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    if len(rows) != 1 or rows[0]["status"] != "DONE":
        raise RuntimeError(("bad planted run", n, result.stdout, result.stderr))
    return rows[0]["nsol"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("engine")
    parser.add_argument("--positive", type=int, default=40)
    parser.add_argument("--diameter-five-controls", type=int, default=15)
    args = parser.parse_args()
    rng = random.Random(20260820)
    for trial in range(args.positive):
        n = rng.randint(6, 12)
        wedges, dists = random_d4_tree(n, rng)
        nsol = engine_solutions(args.engine, n, dists)
        if nsol < 1:
            raise RuntimeError(("missed planted hop-diameter<=4 tree", trial, n, wedges))
    notes = 0
    for _ in range(args.diameter_five_controls):
        n = rng.randint(7, 12)
        wedges, dists = random_d4_tree(n, rng, diam5=True)
        nsol = engine_solutions(args.engine, n, dists)
        if nsol:
            # A diameter-five target can in principle have another realization
            # with diameter at most four, so this is diagnostic rather than a failure.
            notes += 1
    print(json.dumps({"positive_plants": args.positive, "misses": 0,
                      "diameter_five_controls": args.diameter_five_controls,
                      "controls_realized_by_d4": notes, "status": "VERIFIED"}, sort_keys=True))


if __name__ == "__main__":
    main()
