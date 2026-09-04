#!/usr/bin/env python3
"""Independent brute-force checker for counting ADMISSIBLE abstract structures.

Object
------
* m "high" vertices labelled y = 0..m-1.
* A rooted "low tree" on r vertices labelled 0..r-1 given by lowpar[1..r-1]
  with lowpar[i] < i; low vertex 0 is the root.
* A *structure* is a parent function on the high vertices: parent(y) is either
  a low vertex i (0 <= i < r) or an earlier high vertex p with p < y.
  Hence r*(r+1)*...*(r+m-1) structures in total.

Admissibility
-------------
Build the rooted tree on r+m vertices.  High vertices split into components
under the induced high-high edges; the "low root" of a high vertex is the low
vertex at which its component attaches.  For each unordered pair {y, y'} of
distinct high vertices:
  * same component -> let q be the LCA (a high vertex) of y and y' inside the
    component; the pair's "within-value" is y + y' - 2q.
  * different components -> let i, i' be their low roots, l = LCA(i, i') in the
    low tree; the pair is in "class l" with "sum" y + y'.
The structure is ADMISSIBLE iff
  (a) all within-values (pooled over *all* components) are pairwise distinct,
  (b) for each low vertex l separately, the sums in class l are pairwise
      distinct.

This implementation is deliberately naive: full enumeration, explicit tree
build per structure, and LCA by walking explicit ancestor lists.
"""

import argparse
import itertools
import sys


def build_low_ancestor_lists(r, lowpar):
    """lowanc[i] = [i, lowpar[i], ..., 0]: explicit root-ward ancestor list."""
    lowanc = []
    for i in range(r):
        chain = [i]
        cur = i
        while cur != 0:
            cur = lowpar[cur]
            chain.append(cur)
        lowanc.append(chain)
    return lowanc


def low_lca_table(r, lowanc):
    """lca[i][j] found by walking up i's ancestor list until it meets j's."""
    tab = [[None] * r for _ in range(r)]
    for i in range(r):
        for j in range(r):
            j_anc = set(lowanc[j])
            for v in lowanc[i]:          # walk up from i toward the low root
                if v in j_anc:
                    tab[i][j] = v
                    break
            if tab[i][j] is None:
                raise RuntimeError("low tree is not connected: %d,%d" % (i, j))
    return tab


def run(m, lowpar_in, emit=False):
    r = len(lowpar_in) + 1
    lowpar = [-1] + list(lowpar_in)
    for i in range(1, r):
        if not (0 <= lowpar[i] < i):
            raise SystemExit("bad lowpar: lowpar[%d]=%d" % (i, lowpar[i]))

    lowanc = build_low_ancestor_lists(r, lowpar)
    llca = low_lca_table(r, lowanc)

    # choice code c for high vertex y ranges over 0..r+y-1:
    #   c <  r  ->  parent is low vertex c
    #   c >= r  ->  parent is high vertex c - r   (which is < y)
    choices = [range(r + y) for y in range(m)]
    pairs = [(a, b) for a in range(m) for b in range(a + 1, m)]

    total = 0
    admissible = 0

    for code in itertools.product(*choices):
        total += 1

        # ---- explicit tree build for this structure ----
        highanc = [None] * m     # high-only ancestor list, leaf-to-component-root
        lowroot = [0] * m        # low vertex the component attaches to
        comp = [0] * m           # component id = top high vertex of the component
        for y in range(m):
            c = code[y]
            if c < r:
                highanc[y] = [y]
                lowroot[y] = c
                comp[y] = y
            else:
                p = c - r
                highanc[y] = [y] + highanc[p]
                lowroot[y] = lowroot[p]
                comp[y] = comp[p]

        # ---- admissibility test ----
        ok = True
        within = set()
        class_sums = {}
        for a, b in pairs:
            if comp[a] == comp[b]:
                # explicit LCA: walk up a's ancestor list, first vertex also
                # on b's ancestor list.
                b_anc = set(highanc[b])
                q = None
                for v in highanc[a]:
                    if v in b_anc:
                        q = v
                        break
                if q is None:
                    raise RuntimeError("same component but no common ancestor")
                val = a + b - 2 * q
                if val in within:
                    ok = False
                    break
                within.add(val)
            else:
                l = llca[lowroot[a]][lowroot[b]]
                bucket = class_sums.get(l)
                if bucket is None:
                    bucket = set()
                    class_sums[l] = bucket
                s = a + b
                if s in bucket:
                    ok = False
                    break
                bucket.add(s)

        if ok:
            admissible += 1
            if emit:
                # same encoding as the C++ --emit: high parent p >= 0,
                # low vertex i encoded as -1-i.
                out = []
                for y in range(m):
                    c = code[y]
                    out.append(str(c - r) if c >= r else str(-1 - c))
                sys.stdout.write("STRUCT " + " ".join(out) + "\n")

    print("BRUTE m=%d lowpar=%s admissible=%d total=%d"
          % (m, ",".join(str(x) for x in lowpar_in), admissible, total))
    return admissible, total


def parse_lowpar(s):
    s = (s or "").strip()
    if not s:
        return []
    return [int(t) for t in s.split(",") if t.strip() != ""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--lowpar", type=str, default="")
    ap.add_argument("--emit", action="store_true")
    args = ap.parse_args()
    run(args.m, parse_lowpar(args.lowpar), emit=args.emit)


if __name__ == "__main__":
    main()
