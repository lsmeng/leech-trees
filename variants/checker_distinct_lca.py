#!/usr/bin/env python3
"""Independent depth/LCA checker for distinct-distance-tree witnesses.

This intentionally shares no distance-computation code with checker_distinct.py,
which uses a graph search from every source vertex.
"""

import argparse
import itertools


def parse_edges(text):
    edges = []
    for token in text.replace("SOL:", "").split():
        endpoints, weight = token.split(":")
        left, right = endpoints.split("-")
        edges.append((int(left), int(right), int(weight)))
    return edges


def check_distinct_lca(edges, n, maximum=None):
    if len(edges) != n - 1:
        return False, "wrong edge count"
    adjacency = [[] for _ in range(n)]
    for left, right, weight in edges:
        if not (0 <= left < n and 0 <= right < n and left != right):
            return False, "bad endpoint"
        if type(weight) is not int or weight <= 0:
            return False, "bad weight"
        adjacency[left].append((right, weight))
        adjacency[right].append((left, weight))

    parent = [-1] * n
    depth = [None] * n
    depth[0] = 0
    order = [0]
    for vertex in order:
        for neighbour, weight in adjacency[vertex]:
            if neighbour == parent[vertex]:
                continue
            if depth[neighbour] is not None:
                return False, "cycle or parallel edge"
            parent[neighbour] = vertex
            depth[neighbour] = depth[vertex] + weight
            order.append(neighbour)
    if len(order) != n:
        return False, "disconnected"

    ancestors = []
    for vertex in range(n):
        chain = set()
        while vertex != -1:
            chain.add(vertex)
            vertex = parent[vertex]
        ancestors.append(chain)

    def lca(left, right):
        while left not in ancestors[right]:
            left = parent[left]
        return left

    distances = sorted(
        depth[left] + depth[right] - 2 * depth[lca(left, right)]
        for left, right in itertools.combinations(range(n), 2)
    )
    if len(set(distances)) != len(distances):
        return False, "repeated distance"
    observed_maximum = distances[-1]
    if maximum is not None and observed_maximum > maximum:
        return False, f"maximum {observed_maximum} exceeds {maximum}"
    missing = sorted(set(range(1, observed_maximum + 1)) - set(distances))
    return True, f"n={n}, distances={len(distances)}, max={observed_maximum}, missing={missing}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sol")
    parser.add_argument("--n", required=True, type=int)
    parser.add_argument("--D", type=int)
    args = parser.parse_args()
    valid, message = check_distinct_lca(parse_edges(args.sol), args.n, args.D)
    print(("OK: " if valid else "FAIL: ") + message)
    raise SystemExit(0 if valid else 1)
