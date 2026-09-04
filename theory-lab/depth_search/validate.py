#!/usr/bin/env python3
"""Validation driver for depth_search.

1. n = 2..11, all three symmetry modes: run the engine, canonicalise every witness up to
   isomorphism of weighted trees, and compare with data/known_leech_trees.json.
2. Print the node-count / CPU scaling table.
Run from theory-lab/depth_search/.
"""
import json, re, subprocess, sys, time, itertools, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ENG = os.path.join(HERE, "depth_search")

def canon(n, edges):
    """Canonical form of a weighted tree: sorted list over all vertex relabellings."""
    best = None
    for perm in itertools.permutations(range(n)):
        e = sorted(tuple(sorted((perm[u], perm[v]))) + (w,) for u, v, w in edges)
        if best is None or e < best:
            best = e
    return tuple(best)

def parse_sol(line, n):
    body = line.split("  depths:")[0][4:]
    edges = []
    for tok in body.split():
        pv, w = tok.split(":")
        p, v = pv.split("-")
        edges.append((int(p), int(v), int(w)))
    assert len(edges) == n - 1, line
    return edges

def run(n, sym):
    t0 = time.time()
    out = subprocess.run([ENG, "--order", str(n), "--sym", sym, "--verify", "--levels"],
                         capture_output=True, text=True).stdout
    dt = time.time() - t0
    sols = [parse_sol(l, n) for l in out.splitlines() if l.startswith("SOL ")]
    m = re.search(r"nodes=(\d+)", out)
    lv = [l for l in out.splitlines() if l.startswith("LEVELS")]
    return sols, int(m.group(1)), dt, (lv[0][7:] if lv else "")

known = json.load(open(os.path.join(ROOT, "data", "known_leech_trees.json")))["trees"]
kc = {}
for t in known:
    kc.setdefault(t["n"], set()).add(canon(t["n"], [tuple(e) for e in t["edges"]]))

print("== validation against data/known_leech_trees.json ==")
print(f"{'n':>3} {'sym':>5} {'raw':>5} {'up to iso':>9} {'expected':>8}  verdict")
ok = True
for n in range(2, 12):
    for sym in ("none", "w1", "diam"):
        sols, nodes, dt, lv = run(n, sym)
        cs = {canon(n, s) for s in sols} if n <= 6 else set()
        exp = kc.get(n, set())
        good = (cs == exp) if n <= 6 else (len(sols) == 0)
        ok &= good
        print(f"{n:>3} {sym:>5} {len(sols):>5} {len(cs):>9} {len(exp):>8}  {'OK' if good else 'MISMATCH'}")
print("ALL VALIDATION PASSED" if ok else "VALIDATION FAILED")

print()
print("== scaling, general mode, --sym w1 ==")
print(f"{'n':>3} {'N':>4} {'nodes':>14} {'CPU(s)':>9}  levels")
for n in range(7, 12):
    sols, nodes, dt, lv = run(n, "w1")
    print(f"{n:>3} {n*(n-1)//2:>4} {nodes:>14,} {dt:>9.2f}  {lv.strip()}")
