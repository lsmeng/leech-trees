"""Shape generators for structured families of trees, order n.

Families (each shape emitted once up to isomorphism, as an edge list on 0..n-1):
  all        - all nonisomorphic trees (networkx), for validation at small n
  caterpillar- trees whose non-leaf vertices induce a path
  spider     - one vertex of degree >= 3, all others degree <= 2 (legs = partition
               of n-1 into >= 3 parts)
  diam4      - trees of diameter exactly 4: center c with k >= 0 pendant leaves and
               m >= 2 attached stars of sizes a_1 >= ... >= a_m >= 1
  diam5      - trees of diameter exactly 5: central edge (u,v); each side has
               pendant leaves + attached stars, with >= 1 star (depth-2 branch)
               on each side; canonical up to swapping the two sides

Output: one line per shape: "n u1 v1 u2 v2 ..." for forced_family.c.
Usage: gen_shapes.py FAMILY N [--count-only] [--maxdiam D]
"""
import sys
from itertools import product


def emit(edges, n, out, tags=None):
    """tags: optional per-edge list of (group, branch) with group=-1 for untagged.
    Groups collect pairwise-identical rooted branches at a common vertex (equal-length
    spider legs, equal-size star branches); the engine breaks that symmetry."""
    line = str(n) + " " + " ".join(f"{u} {v}" for u, v in edges)
    if tags is not None:
        line += " G " + " ".join(f"{g} {b}" for g, b in tags)
    out.write(line + "\n")


# ---------------------------------------------------------------- caterpillars
def caterpillar_seqs(n):
    """Yield leaf-count sequences (c_1..c_p) on the internal path u_1..u_p:
    c_1, c_p >= 1 (p >= 2), sum c_i = n - p; canonical under reversal.
    p = 1 is the star K_{1,n-1} (c_1 = n-1)."""
    if n >= 2:
        yield (n - 1,)                       # star (p=1); n=2 gives single edge
    for p in range(2, n - 1):
        rem = n - p                          # total leaves, >= 2 needed
        if rem < 2:
            continue

        def rec(prefix, left, slots):
            if slots == 1:
                if left >= 1:
                    yield prefix + (left,)
                return
            lo = 1 if len(prefix) == 0 else 0
            hi = left - 1                    # last slot needs >= 1
            for c in range(lo, hi + 1):
                yield from rec(prefix + (c,), left - c, slots - 1)

        for seq in rec((), rem, p):
            if seq <= seq[::-1]:
                yield seq


def caterpillar_edges(seq):
    p = len(seq)
    n = p + sum(seq)
    edges = []
    for i in range(p - 1):
        edges.append((i, i + 1))
    nxt = p
    for i, c in enumerate(seq):
        for _ in range(c):
            edges.append((i, nxt)); nxt += 1
    return edges, n


def gen_caterpillar(n, maxdiam=None, mindiam=None):
    for seq in caterpillar_seqs(n):
        p = len(seq)
        diam = 2 if p == 1 else p + 1        # edges on longest path
        if n <= 3:
            diam = n - 1
        if maxdiam is not None and diam > maxdiam:
            continue
        if mindiam is not None and diam < mindiam:
            continue
        yield caterpillar_edges(seq)[0], None


# ---------------------------------------------------------------- spiders
def partitions(total, maxpart=None, minparts=1):
    """Partitions of total into parts (descending)."""
    maxpart = maxpart or total

    def rec(left, mx, acc):
        if left == 0:
            yield tuple(acc)
            return
        for part in range(min(mx, left), 0, -1):
            acc.append(part)
            yield from rec(left - part, part, acc)
            acc.pop()

    yield from rec(total, maxpart, [])


def gen_spider(n, maxdiam=None):
    """Center 0; legs = partition of n-1 into k >= 3 parts.  Tags: equal-length legs
    (length >= 2, multiplicity >= 2) form a symmetry group; length-1 legs are pendant
    edges at the center and are already handled by the engine's pendant classes."""
    for legs in partitions(n - 1):
        if len(legs) < 3:
            continue
        if maxdiam is not None and legs[0] + legs[1] > maxdiam:
            continue
        edges = []
        tags = []
        nxt = 1
        # group ids per leg length (only lengths >= 2 with multiplicity >= 2)
        from collections import Counter
        cnt = Counter(legs)
        glen = {L: gi for gi, L in enumerate(sorted(set(L for L in legs
                                                        if L >= 2 and cnt[L] >= 2)))}
        seen_branch = {L: 0 for L in glen}
        for L in legs:
            prev = 0
            g, b = -1, 0
            if L in glen:
                g, b = glen[L], seen_branch[L]
                seen_branch[L] += 1
            for _ in range(L):
                edges.append((prev, nxt)); tags.append((g, b))
                prev = nxt; nxt += 1
        yield edges, tags


# ---------------------------------------------------------------- diameter 4
def _center_branches_shape(n, sides, base_edges):
    """sides: list of (center_vertex, k_leaves, star_sizes).  Builds edges + tags;
    equal-size star branches at the SAME center (multiplicity >= 2) share a symmetry
    group; pendant leaves are covered by the engine's pendant classes."""
    from collections import Counter
    edges = list(base_edges)
    tags = [(-1, 0)] * len(base_edges)
    nxt = max(c for c, _, _ in sides) + 1
    gid = 0
    for center, k, stars in sides:
        for _ in range(k):
            edges.append((center, nxt)); tags.append((-1, 0)); nxt += 1
        cnt = Counter(stars)
        gmap, seen = {}, {}
        for s in sorted(set(stars)):
            if cnt[s] >= 2:
                gmap[s] = gid; seen[s] = 0; gid += 1
        for ai in stars:
            g, b = -1, 0
            if ai in gmap:
                g, b = gmap[ai], seen[ai]; seen[ai] += 1
            hub = nxt; edges.append((center, hub)); tags.append((g, b)); nxt += 1
            for _ in range(ai):
                edges.append((hub, nxt)); tags.append((g, b)); nxt += 1
    assert nxt == n, (nxt, n, sides)
    return edges, tags


def gen_diam4(n):
    """Center 0, k pendant leaves, m >= 2 stars with a_1 >= ... >= a_m >= 1.
    n = 1 + k + m + sum(a_i)."""
    for m in range(2, n):
        for k in range(0, n - 1 - 2 * m + 1):
            tot = n - 1 - k - m              # sum of a_i
            if tot < m:
                continue
            for a in partitions(tot):
                if len(a) != m:
                    continue
                yield _center_branches_shape(n, [(0, k, a)], [])


# ---------------------------------------------------------------- diameter 5
def side_configs(size):
    """All (k, stars) with k >= 0 pendant leaves and stars a_1>=..>=a_m>=1, m >= 1,
    total vertices used on this side (excluding the center) = k + m + sum(a) = size."""
    out = []
    for m in range(1, size):
        for k in range(0, size - 2 * m + 1):
            tot = size - k - m
            if tot < m:
                continue
            for a in partitions(tot):
                if len(a) == m:
                    out.append((k, a))
    return out


def gen_diam5(n):
    """Central edge (0,1); side sizes s0 + s1 = n - 2, each side >= 2 (needs a star).
    Canonical: (s0, config0) <= (s1, config1) lexicographically."""
    seen = set()
    for s0 in range(2, n - 3):
        s1 = n - 2 - s0
        if s1 < 2:
            continue
        for c0 in side_configs(s0):
            for c1 in side_configs(s1):
                key = tuple(sorted([(s0, c0), (s1, c1)]))
                if key in seen:
                    continue
                seen.add(key)
                (k0, a0), (k1, a1) = c0, c1
                yield _center_branches_shape(
                    n, [(0, k0, a0), (1, k1, a1)], [(0, 1)])


# ---------------------------------------------------------------- all trees
def gen_all(n):
    import networkx as nx
    for T in nx.nonisomorphic_trees(n):
        mapping = {v: i for i, v in enumerate(T.nodes())}
        yield [(mapping[u], mapping[v]) for u, v in T.edges()], None


FAMILIES = {"all": gen_all, "caterpillar": gen_caterpillar, "spider": gen_spider,
            "diam4": gen_diam4, "diam5": gen_diam5}


def main():
    fam = sys.argv[1]
    n = int(sys.argv[2])
    count_only = "--count-only" in sys.argv
    maxdiam = None
    if "--maxdiam" in sys.argv:
        maxdiam = int(sys.argv[sys.argv.index("--maxdiam") + 1])
    gen = FAMILIES[fam]
    kwargs = {}
    if maxdiam is not None and fam in ("caterpillar", "spider"):
        kwargs["maxdiam"] = maxdiam
    if "--mindiam" in sys.argv and fam == "caterpillar":
        kwargs["mindiam"] = int(sys.argv[sys.argv.index("--mindiam") + 1])
    notags = "--notags" in sys.argv
    cnt = 0
    out = sys.stdout
    for edges, tags in gen(n, **kwargs):
        cnt += 1
        if not count_only:
            emit(edges, n, out, None if notags else tags)
    if count_only:
        print(cnt)


if __name__ == "__main__":
    main()
