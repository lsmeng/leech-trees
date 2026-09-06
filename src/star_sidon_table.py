#!/usr/bin/env python3
"""Recompute the star-Sidon table S(d) of Lemma 2.5 by exhaustive search.

A set W of d distinct positive integers is *star-Sidon* if the pairwise sums
w_i+w_j (i<j) are distinct from each other and from the elements.  S(d) is the
minimum of a_{d-1}+a_d over star-Sidon sets of size d.  Because a_{d-1}+a_d is
the largest sum, a star-Sidon set of size d with a_{d-1}+a_d <= T is the same
thing as a star-Sidon set of size d all of whose elements and sums are <= T.
Hence S(d) is the least T for which such a set exists, and the search below --
an exhaustive DFS in increasing order, identical in logic to the C scratch
program docs/sources/stardeg.c -- decides that for each T.

Usage:  python3 src/star_sidon_table.py [dmax]        (default dmax = 12)
Prints one line per d with S(d), a witness attaining it, and the number of
DFS nodes spent proving T = S(d)-1 infeasible.
"""
import sys

def search(T, d):
    """Return a star-Sidon set of size d with all elements and sums <= T, or None."""
    used = bytearray(T + 2)
    w = []
    nodes = 0
    def rec():
        nonlocal nodes
        k = len(w)
        if k == d:
            return True
        lo = w[-1] + 1 if w else 1
        for p in range(lo, T + 1):
            nodes += 1
            if d - k >= 2 and 2 * p + 1 > T:
                break
            if w and p + w[-1] > T:
                break
            if used[p]:
                continue
            new = [p] + [x + p for x in w]
            if any(s > T or used[s] for s in new):
                continue
            for s in new:
                used[s] = 1
            w.append(p)
            if rec():
                return True
            w.pop()
            for s in new:
                used[s] = 0
        return False
    ok = rec()
    return (list(w) if ok else None), nodes

def main():
    dmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    T = 1
    rows = []
    for d in range(2, dmax + 1):
        last_nodes = 0
        while True:
            wit, nodes = search(T, d)
            if wit is not None:
                rows.append((d, T, wit))
                print(f"S({d:2d}) = {T:4d}   witness {wit}   "
                      f"(nodes to refute {T-1}: {last_nodes})", flush=True)
                break
            last_nodes = nodes
            T += 1
    print("TABLE", " ".join(str(t) for _, t, _ in rows))
    print("VERIFIED_STAR_SIDON_TABLE")

if __name__ == "__main__":
    main()
