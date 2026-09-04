#!/usr/bin/env python3
"""Differential test: gap-order engine (all optional prunes OFF) vs the
independent vertex-order reference enumerator.  They must agree exactly on the
set of relaxation solutions, described as the set of (e,f) vertex pairs."""
import importlib.util, sys

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

de = load("de", "double_end_search.py")
bd = load("bd", "brute_double_end.py")

for n in [int(x) for x in sys.argv[1:]] or [3, 4, 6]:
    s = de.Search(n, node_limit=2_000_000_000, max_solutions=10**9, verbose=0)
    s.no_hc = s.no_attach = s.no_ultra = s.no_parity = True
    s.no_hall = s.no_lb = s.no_cover = s.no_ub = True
    s.symmetry_break = False
    r = s.run()
    eng = set(frozenset((sol["e"][i], sol["f"][i]) for i in range(n - 2))
              for sol in r["solutions"])
    sols, nodes, bailed = bd.enumerate_relaxation(n, 2_000_000_000)
    ref = set(frozenset((E[i], F[i]) for i in range(n - 2)) for (E, F, _) in sols)
    ok = (eng == ref) and not bailed and r["status"] != "BAILED"
    print("n=%-3d engine=%-5d reference=%-5d  %s" %
          (n, len(eng), len(ref), "AGREE" if ok else "MISMATCH"))
    if not ok:
        print("   only in engine:   ", sorted(map(sorted, eng - ref))[:6])
        print("   only in reference:", sorted(map(sorted, ref - eng))[:6])

    # now with all prunes on: solutions must be a subset, and must contain all
    # configurations that verify as genuine trees
    s2 = de.Search(n, node_limit=2_000_000_000, max_solutions=10**9, verbose=0)
    s2.symmetry_break = False
    r2 = s2.run()
    eng2 = set(frozenset((sol["e"][i], sol["f"][i]) for i in range(n - 2))
               for sol in r2["solutions"])
    trees_ref = set()
    for (E, F, _) in sols:
        pv = [[0] * (n - 2) for _ in range(n - 2)]
        okv = False
        for sol in r["solutions"]:
            if frozenset((sol["e"][i], sol["f"][i]) for i in range(n - 2)) == \
               frozenset((E[i], F[i]) for i in range(n - 2)):
                v, _msg = de.verify_solution(n, sol["e"], sol["f"], sol["pairs"])
                if v:
                    okv = True
        if okv:
            trees_ref.add(frozenset((E[i], F[i]) for i in range(n - 2)))
    print("     with prunes on: %d solutions; genuine trees among unpruned: %d; "
          "all trees kept: %s; pruned set is subset: %s"
          % (len(eng2), len(trees_ref), trees_ref <= eng2, eng2 <= eng))
