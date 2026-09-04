"""Independent cross-check of brute_leech_small.py -- shares no code with it.

  * trees from Prufer-sequence decoding (not leaf addition), deduplicated by
    bucketing on the multiset of vertex distance-vectors and then confirming
    with an explicit brute-force search over all n! vertex bijections;
  * Method A: full numpy scan of the whole cube [1..N]^(n-1), using only the
    DEFINITION (distances distinct and <= N).  No sum identity, no bounds;
  * Method B: DFS with the distinctness prune only.  No sum identity, no
    rearrangement bound, no monotone cutoff.
"""
import heapq, itertools, sys, time
import numpy as np

def prufer_decode(seq, n):
    if n == 1: return []
    if n == 2: return [(0, 1)]
    deg = [1] * n
    for x in seq: deg[x] += 1
    leaves = [i for i in range(n) if deg[i] == 1]
    heapq.heapify(leaves)
    edges = []
    for x in seq:
        leaf = heapq.heappop(leaves)
        edges.append((leaf, x))
        deg[x] -= 1
        if deg[x] == 1: heapq.heappush(leaves, x)
    u = heapq.heappop(leaves); v = heapq.heappop(leaves)
    edges.append((u, v))
    return edges

def hop_matrix(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    D = [[0] * n for _ in range(n)]
    for s in range(n):
        seen = {s}; q = [(s, 0)]
        while q:
            x, d = q.pop(0)
            D[s][x] = d
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); q.append((y, d + 1))
    return D

def shape_key(n, edges):
    D = hop_matrix(n, edges)
    return tuple(sorted(tuple(sorted(r)) for r in D))

def iso_shapes(n, A, B):
    tb = frozenset((min(u, v), max(u, v)) for u, v in B)
    for p in itertools.permutations(range(n)):
        if frozenset((min(p[u], p[v]), max(p[u], p[v])) for u, v in A) == tb:
            return True
    return False

def iso_weighted(n, A, B):
    tb = frozenset((min(u, v), max(u, v), w) for u, v, w in B)
    for p in itertools.permutations(range(n)):
        if frozenset((min(p[u], p[v]), max(p[u], p[v]), w) for u, v, w in A) == tb:
            return True
    return False

_shape_cache = {}
def shapes_via_prufer(n):
    if n in _shape_cache: return _shape_cache[n]
    if n == 2:
        _shape_cache[n] = [[(0, 1)]]; return _shape_cache[n]
    buckets = {}
    for seq in itertools.product(range(n), repeat=n - 2):
        e = prufer_decode(list(seq), n)
        buckets.setdefault(shape_key(n, e), []).append(e)
    # One representative per bucket. The invariant (multiset of vertex
    # distance-vectors) is not proven complete, so spot-confirm each bucket by
    # an explicit n! bijection search on up to CAP of its members.
    CAP = 25
    reps = []
    collisions = 0
    confirmed = 0
    for key, group in buckets.items():
        rep = group[0]
        reps.append(rep)
        for e in group[1:CAP]:
            confirmed += 1
            if not iso_shapes(n, e, rep):
                collisions += 1
                reps.append(e)
    _shape_cache[n] = reps
    print("      (%d distance-vector buckets; %d members spot-confirmed "
          "isomorphic to their bucket rep by n! search; %d counterexamples)"
          % (len(buckets), confirmed, collisions), flush=True)
    return reps

def path_matrix(n, edges):
    m = len(edges)
    adj = [[] for _ in range(n)]
    for k, (u, v) in enumerate(edges):
        adj[u].append((v, k)); adj[v].append((u, k))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    M = np.zeros((len(pairs), m), dtype=np.int64)
    for pi, (s, t) in enumerate(pairs):
        par = {s: (None, None)}; st = [s]
        while st:
            x = st.pop()
            for (y, k) in adj[x]:
                if y not in par:
                    par[y] = (x, k); st.append(y)
        x = t
        while x != s:
            px, pk = par[x]; M[pi, pk] = 1; x = px
    return M

def method_A(n):
    N = n * (n - 1) // 2
    sols = []
    scanned = 0
    for edges in shapes_via_prufer(n):
        m = len(edges)
        Mt = path_matrix(n, edges).T.copy()
        total = N ** m
        scanned += total
        CH = 300_000
        base = np.arange(1, N + 1, dtype=np.int64)
        for start in range(0, total, CH):
            stop = min(start + CH, total)
            idx = np.arange(start, stop, dtype=np.int64)
            W = np.empty((stop - start, m), dtype=np.int64)
            tmp = idx.copy()
            for k in range(m - 1, -1, -1):
                W[:, k] = base[tmp % N]; tmp //= N
            D = W @ Mt
            good = D.max(axis=1) <= N
            if not good.any(): continue
            Ds = np.sort(D[good], axis=1)
            ok = np.all(np.diff(Ds, axis=1) > 0, axis=1)
            for row in W[good][ok]:
                sols.append([(edges[k][0], edges[k][1], int(row[k]))
                             for k in range(m)])
    reps = []
    for s in sols:
        if not any(iso_weighted(n, s, r) for r in reps):
            reps.append(s)
    return len(reps), reps, scanned

def method_B(n, deadline):
    N = n * (n - 1) // 2
    sols = []; nodes = [0]; hit = [False]
    for edges in shapes_via_prufer(n):
        m = len(edges)
        adj = [[] for _ in range(n)]
        for k, (u, v) in enumerate(edges):
            adj[u].append((v, k)); adj[v].append((u, k))
        order = []; seen = {0}; q = [0]
        while q:
            x = q.pop(0)
            for (y, k) in adj[x]:
                if y not in seen:
                    seen.add(y); order.append((x, y, k)); q.append(y)
        D = [[0] * n for _ in range(n)]
        placed = [0]; used = bytearray(N + 2); wl = [0] * m
        def rec(i):
            nodes[0] += 1
            if (nodes[0] & 0xFFFF) == 0 and time.time() > deadline:
                hit[0] = True; raise KeyboardInterrupt
            if i == m:
                sols.append([(edges[k][0], edges[k][1], wl[k]) for k in range(m)]); return
            p, t, k = order[i]
            for w in range(1, N + 1):
                nd = []; bad = False
                for s in placed:
                    v = D[s][p] + w
                    if v > N or used[v] or v in nd:
                        bad = True; break
                    nd.append(v)
                if bad: continue
                for v in nd: used[v] = 1
                for a, s in enumerate(placed):
                    D[s][t] = D[t][s] = nd[a]
                placed.append(t); wl[k] = w
                rec(i + 1)
                placed.pop()
                for v in nd: used[v] = 0
        try:
            rec(0)
        except KeyboardInterrupt:
            break
    reps = []
    for s in sols:
        if not any(iso_weighted(n, s, r) for r in reps):
            reps.append(s)
    return len(reps), nodes[0], hit[0]

if __name__ == "__main__":
    NM = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print("== shape counts via Prufer + distance-vector buckets + n! iso confirm ==",
          flush=True)
    for n in range(2, NM + 1):
        t0 = time.time()
        c = len(shapes_via_prufer(n))
        print("  n=%d shapes=%d (%.1fs)" % (n, c, time.time() - t0), flush=True)
    print("\n== Method A: full cube scan [1..N]^(n-1), definition only ==", flush=True)
    for n in range(2, 7):
        t0 = time.time()
        c, reps, scanned = method_A(n)
        print("  n=%d  leech=%d  tuples_scanned=%d  (%.1fs)"
              % (n, c, scanned, time.time() - t0), flush=True)
        for r in reps: print("      ", r, flush=True)
    print("\n== Method B: distinctness-only DFS ==", flush=True)
    for n in range(2, NM + 2):
        t0 = time.time()
        c, nodes, hit = method_B(n, time.time() + 120)
        print("  n=%d  leech=%d  nodes=%d  %.1fs  %s"
              % (n, c, nodes, time.time() - t0,
                 "TIMEOUT (INCOMPLETE)" if hit else "exhaustive"), flush=True)
