#!/usr/bin/env python3
"""E3 over ALL free-tree shapes of order n (data/trees_N.jsonl).

For a pair (x,y) in a tree: s_x = #vertices whose path to y passes through x
(= subtree size of x in the y-rooted tree), s_y symmetric. Containment bound:
d(x,y) <= N+1 - s_x*s_y. Hall condition for the top q values {N-q+1..N}:
  c(q) := #pairs with s_x*s_y <= q  must be >= q  for every q in 1..N.
slack(q) = c(q) - q; a shape with min_q slack(q) < 0 admits NO Leech weighting.

Note s_x*s_y is weight-free, so this is exact per shape (not sampled).
"""
import json, os, sys
from collections import Counter, deque
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
QMAX = 30


def slack_stats(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    # subtree sizes for every root
    sz = [[1] * n for _ in range(n)]
    for r in range(n):
        order = [r]
        par = [-1] * n
        par[r] = r
        for x in order:
            for y in adj[x]:
                if par[y] == -1:
                    par[y] = x
                    order.append(y)
        s = sz[r]
        for x in reversed(order[1:]):
            s[par[x]] += s[x]
        sz[r] = s
    cnt = Counter()
    for x in range(n):
        for y in range(x + 1, n):
            p = sz[y][x] * sz[x][y]
            if p <= QMAX:
                cnt[p] += 1
    c = 0
    slacks = []
    for q in range(1, QMAX + 1):
        c += cnt.get(q, 0)
        slacks.append(c - q)
    return slacks


def work(chunk):
    minslack_hist = Counter()
    argmin_hist = Counter()
    slack_at = Counter()   # sum of slack per q for mean
    nrec = 0
    worst = []
    for line in chunk:
        t = json.loads(line)
        sl = slack_stats(t['n'], t['edges'])
        ms = min(sl)
        am = 1 + sl.index(ms)
        minslack_hist[ms] += 1
        argmin_hist[am] += 1
        for q, s in enumerate(sl, 1):
            slack_at[q] += s
        nrec += 1
        if len(worst) < 5 or ms < worst[-1][0]:
            worst.append((ms, t['id']))
            worst.sort()
            worst = worst[:5]
    return minslack_hist, argmin_hist, slack_at, nrec, worst


def main():
    os.nice(10)
    out = {}
    for n in (11, 16, 18):
        path = os.path.join(ROOT, 'data', f'trees_{n}.jsonl')
        lines = open(path).read().splitlines()
        k = 3
        chunks = [lines[i::k] for i in range(k)]
        with Pool(k) as p:
            parts = p.map(work, chunks)
        mh, ah, sa, tot, worst = Counter(), Counter(), Counter(), 0, []
        for m, a, s, c, w in parts:
            mh += m; ah += a; sa += s; tot += c; worst += w
        worst.sort()
        out[n] = dict(ntrees=tot,
                      minslack_hist=sorted(mh.items()),
                      argmin_hist=sorted(ah.items()),
                      mean_slack={q: sa[q] / tot for q in range(1, QMAX + 1)},
                      worst5=worst[:5],
                      nviol=sum(v for m, v in mh.items() if m < 0))
        print(f"n={n}: {tot} shapes, min-slack range {min(mh)}..{max(mh)}, "
              f"violators(minslack<0)={out[n]['nviol']}, "
              f"minslack hist head={sorted(mh.items())[:6]}", flush=True)
    with open(os.path.join(HERE, 'e3_shapes.json'), 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
