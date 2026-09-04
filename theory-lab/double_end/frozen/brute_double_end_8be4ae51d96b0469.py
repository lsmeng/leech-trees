#!/usr/bin/env python3
"""INDEPENDENT reference enumerator for the double-end normal form.

Completely different search order from double_end_search.py: it enumerates the
vertices themselves, in increasing order of e, and checks the defining
conditions directly.  Used as a differential test of the gap-order engine.

Conditions enforced (the DEFINITION only -- no attachment / ultrametric /
LCA-vertex conditions, so this is the pure relaxation):
    1 <= e,f <= N-1 ; e+f <= N ; e+f = N (mod 2) ; E, F disjoint, all distinct
    gap(u,v) = min(f_u+e_v, f_v+e_u) + 2 h_c , 0 <= h_c <= min(h_u,h_v),
        h_c = 0 unless f_u-e_u = f_v-e_v
    {0} u E u F u {gap(u,v)} = [0, N-1]
"""
import sys
from itertools import product


def enumerate_relaxation(n, node_limit=None):
    N = n * (n - 1) // 2
    V = n - 2
    sols = []
    nodes = [0]
    bailed = [False]
    E = []
    F = []
    taken = bytearray(N)
    taken[0] = 1
    hc_stack = []          # list of (i,j,gapvalue)

    def place(k, emin):
        if bailed[0]:
            return
        nodes[0] += 1
        if node_limit and nodes[0] > node_limit:
            bailed[0] = True
            return
        if k == V:
            if all(taken):
                sols.append((tuple(E), tuple(F), tuple(hc_stack)))
            return
        for e in range(emin, N):
            if taken[e]:
                continue
            for f in range(1, N - e + 1):
                if (e + f) % 2 != N % 2 or taken[f] or f == e:
                    continue
                # new coordinates
                taken[e] = 1
                taken[f] = 1
                E.append(e)
                F.append(f)
                # all pair gaps with previous vertices
                added = []
                ok = True
                choices = []
                for j in range(k):
                    c1 = F[j] + e
                    c2 = f + E[j]
                    if c1 != c2:
                        v = min(c1, c2)
                        if v <= 0 or v >= N or taken[v]:
                            ok = False
                            break
                        taken[v] = 1
                        added.append(v)
                        hc_stack.append((j, k, v))
                    else:
                        hmax = min((N - E[j] - F[j]) // 2, (N - e - f) // 2)
                        choices.append((j, c1, hmax))
                if ok:
                    if not choices:
                        place(k + 1, e + 1)
                    else:
                        def branch(t):
                            if t == len(choices):
                                place(k + 1, e + 1)
                                return
                            j, base, hmax = choices[t]
                            for hcv in range(hmax + 1):
                                v = base + 2 * hcv
                                if v <= 0 or v >= N or taken[v]:
                                    continue
                                taken[v] = 1
                                hc_stack.append((j, k, v))
                                branch(t + 1)
                                hc_stack.pop()
                                taken[v] = 0
                        branch(0)
                for v in added:
                    taken[v] = 0
                for _ in range(len(hc_stack) - 1, -1, -1):
                    if hc_stack and hc_stack[-1][1] == k:
                        hc_stack.pop()
                    else:
                        break
                E.pop()
                F.pop()
                taken[e] = 0
                taken[f] = 0
                if not ok:
                    continue
    place(0, 1)
    return sols, nodes[0], bailed[0]


if __name__ == "__main__":
    n = int(sys.argv[1])
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else None
    sols, nodes, bailed = enumerate_relaxation(n, lim)
    key = set()
    for (E, F, _) in sols:
        key.add((E, F))
    print("n=%d nodes=%d bailed=%s raw_solutions=%d distinct_(E,F)=%d"
          % (n, nodes, bailed, len(sols), len(key)))
    for k in sorted(key):
        print("  E=%s F=%s" % (list(k[0]), list(k[1])))
