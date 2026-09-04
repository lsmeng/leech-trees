"""Checker A: BFS-from-every-vertex distance computation, pure Python, no libraries.
Input format: n, list of (u,v,w) edges with 0-based vertices. Returns (ok, reason)."""
from math import comb

def is_leech(n, edges):
    if len(edges) != n - 1:
        return False, "edge count"
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if not (isinstance(w, int) and w >= 1):
            return False, "non-positive-integer weight"
        adj[u].append((v, w)); adj[v].append((u, w))
    N = comb(n, 2)
    seen = [False] * (N + 1)
    count = 0
    for s in range(n):
        dist = [-1] * n; dist[s] = 0; stack = [s]
        while stack:
            u = stack.pop()
            for v, w in adj[u]:
                if dist[v] < 0:
                    dist[v] = dist[u] + w; stack.append(v)
        if any(d < 0 for d in dist):
            return False, "not connected"
        for t in range(s + 1, n):
            d = dist[t]
            if d > N or seen[d]:
                return False, f"distance {d} out of range or repeated"
            seen[d] = True; count += 1
    return count == N and all(seen[1:]), "ok"
