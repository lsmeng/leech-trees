"""Validation of forced_family.c:
1. Run the C engine on ALL nonisomorphic trees of order 2..11.  Expect: Leech
   labelings exist exactly for the 5 known trees (n=2; n=3; n=4 star; n=4 path;
   n=6 double star B_{2,2}) and for no tree of order 5, 7, 8, 9, 10, 11.
2. Every witness the engine prints is re-verified with src/checker_a.py AND
   src/checker_b.py.
3. Cross-check existence (found>0) per topology against the pure-Python reference
   src/filters.py::leech_labelings_of_topology for all trees of order <= 9.
"""
import json
import subprocess
import sys
import os

ROOT = "/Users/geoclaw/Documents/claude/projects/leech-trees"
HERE = os.path.join(ROOT, "theory-lab", "exp-families")
sys.path.insert(0, os.path.join(ROOT, "src"))
import checker_a, checker_b            # noqa: E402
from filters import leech_labelings_of_topology  # noqa: E402
sys.path.insert(0, HERE)
from gen_shapes import gen_all          # noqa: E402


def run_engine(shapes_lines, extra_args=()):
    proc = subprocess.run([os.path.join(HERE, "forced_family"), *extra_args],
                          input="".join(shapes_lines), capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    res, wits = {}, {}
    for line in proc.stdout.splitlines():
        if line.startswith("RES"):
            kv = dict(p.split("=") for p in line.split()[1:])
            res[int(kv["id"])] = (int(kv["nodes"]), int(kv["found"]), int(kv["capped"]))
        elif line.startswith("WITNESS"):
            kv = dict(p.split("=", 1) for p in line.split()[1:])
            edges = [tuple(map(int, t.split(","))) for t in kv["edges"].rstrip(";").split(";")]
            wits.setdefault(int(kv["id"]), []).append(edges)
    return res, wits


def main():
    all_shapes = []     # (n, edges)
    lines = []
    for n in range(2, 12):
        for edges, _tags in gen_all(n):
            all_shapes.append((n, edges))
            lines.append(f"{n} " + " ".join(f"{u} {v}" for u, v in edges) + "\n")
    res, wits = run_engine(lines)
    assert len(res) == len(all_shapes), (len(res), len(all_shapes))

    found_by_order = {}
    for i, (n, edges) in enumerate(all_shapes):
        nodes, found, capped = res[i]
        assert capped == 0
        if found:
            found_by_order.setdefault(n, 0)
            found_by_order[n] += 1
            for w_edges in wits.get(i, []):
                oka, ra = checker_a.is_leech(n, w_edges)
                okb, rb = checker_b.is_leech(n, w_edges)
                assert oka and okb, (n, w_edges, ra, rb)
    # counts of TOPOLOGIES admitting a labeling per order
    expect = {2: 1, 3: 1, 4: 2, 6: 1}
    assert found_by_order == expect, found_by_order
    print("PASS 1+2: engine on all trees n=2..11 finds Leech labelings exactly on the "
          f"5 known topologies {found_by_order}; all witnesses pass checker_a AND checker_b")
    ntrees = {}
    for n, _ in all_shapes:
        ntrees[n] = ntrees.get(n, 0) + 1
    print("   trees per order:", ntrees)
    tot_nodes = sum(r[0] for r in res.values())
    print(f"   total shapes {len(all_shapes)}, total DFS nodes {tot_nodes}")

    # 3. cross-check vs the pure-Python reference for n <= 9 (existence only)
    idx = 0
    mismatch = 0
    for i, (n, edges) in enumerate(all_shapes):
        if n > 9:
            continue
        ref = leech_labelings_of_topology(n, edges, limit=1)
        eng = res[i][1] > 0
        if bool(ref) != eng:
            mismatch += 1
            print("MISMATCH", n, edges, bool(ref), eng)
        idx += 1
    assert mismatch == 0
    print(f"PASS 3: existence agrees with src/filters.py reference on all {idx} trees n<=9")


def symmetry_test():
    """Machine-check the branch-symmetry breaking (G tags) via exact orbit counts.
    With S-slack the engine counts complete labelings that follow the least-missing
    rule with all distances distinct <= S+slack; the branch-permutation group (product
    of Sym(k_g) over groups g) acts FREELY on these labelings (weights are distinct),
    and the tagged run keeps exactly one representative per orbit, so
        found(untagged) == found(tagged) * prod_g k_g! .
    Checked on spiders and diam4/diam5 shapes with repeated branches."""
    from math import factorial
    from gen_shapes import gen_spider, gen_diam4, gen_diam5
    from collections import Counter
    cases = []
    for fam, n in (("spider", 7), ("spider", 8), ("diam4", 8), ("diam4", 9),
                   ("diam5", 8), ("diam5", 9)):
        gen = {"spider": gen_spider, "diam4": gen_diam4, "diam5": gen_diam5}[fam]
        for edges, tags in gen(n):
            groups = Counter(g for g, b in tags if g >= 0)
            sizes = Counter()
            for g, b in tags:
                if g >= 0:
                    sizes[(g, b)] = 1
            kg = Counter(g for g, b in {(g, b) for g, b in tags if g >= 0})
            if not kg:
                continue
            orbit = 1
            for g, k in kg.items():
                orbit *= factorial(k)
            if orbit == 1:
                continue
            cases.append((fam, n, edges, tags, orbit))
    assert cases
    checked = 0
    nonzero = 0
    for fam, n, edges, tags, orbit in cases:
        base = f"{n} " + " ".join(f"{u} {v}" for u, v in edges)
        tagline = " G " + " ".join(f"{g} {b}" for g, b in tags)
        slack = "25"
        r_un, _ = run_engine([base + "\n"], ("0", slack))
        r_tag, _ = run_engine([base + tagline + "\n"], ("0", slack))
        fu, ft = r_un[0][1], r_tag[0][1]
        assert fu == ft * orbit, (fam, n, edges, fu, ft, orbit)
        checked += 1
        if fu:
            nonzero += 1
    assert nonzero >= 5, nonzero
    print(f"PASS 4: branch-symmetry orbit identity found(untagged) = found(tagged) * prod k! "
          f"holds on {checked} shapes ({nonzero} with nonzero counts), slack=25")


if __name__ == "__main__":
    main()
    symmetry_test()
