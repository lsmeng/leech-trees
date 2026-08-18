"""Checker B: independent algorithm — root the tree, compute depth of every vertex and LCA
by naive ancestor-walk; d(u,v)=depth[u]+depth[v]-2*depth[lca]. Uses a sorted list compare
instead of a boolean seen-array. Shares no code with checker A."""
def is_leech(n, edges):
    if len(edges) != n - 1: return False, "edge count"
    for u, v, w in edges:
        if type(w) is not int or w < 1: return False, "bad weight"
    nbr = {i: {} for i in range(n)}
    for u, v, w in edges:
        if v in nbr[u]: return False, "multi-edge"
        nbr[u][v] = w; nbr[v][u] = w
    parent = [-1] * n; depth = [None] * n; depth[0] = 0
    order = [0]
    for u in order:
        for v, w in nbr[u].items():
            if depth[v] is None:
                depth[v] = depth[u] + w; parent[v] = u; order.append(v)
    if len(order) != n: return False, "disconnected/cyclic"
    def anc(x):
        s = set()
        while x != -1: s.add(x); x = parent[x]
        return s
    ancs = [anc(i) for i in range(n)]
    def lca(u, v):
        x = u
        while x not in ancs[v]: x = parent[x]
        return x
    ds = sorted(depth[u] + depth[v] - 2 * depth[lca(u, v)] for u in range(n) for v in range(u + 1, n))
    return ds == list(range(1, n * (n - 1) // 2 + 1)), "ok"
