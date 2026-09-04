#!/usr/bin/env python3
"""Exact fixed-shard S1-279 realization check.

Scope is deliberately narrow and fully existential:
  s=152, chain, d1=18, d2=100;
  the first exact-10 root signature from the v4w scan;
  c=10, hence the selected roots are all high-component roots;
  all 25 all-high FW303 core-gate rows (Class A).

For each compatible gate row, the five non-gate core vertices have their
literal FW303 parent.  The remaining six non-root high vertices use the six
distinct non-core HH weights {4,5,16,18,19,20}.  Every resulting 24-vertex
tree is checked against the complete 276-entry distance multiset.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


S = 152
B = 128
D1 = 18
D2 = 100
LOW_DEPTH = (0, D1, D2)
ROOT_COLOR = {
    5: 0,
    0: 1,
    8: 1,
    16: 1,
    2: 2,
    3: 2,
    4: 2,
    6: 2,
    9: 2,
    15: 2,
}
W = (4, 5, 16, 18, 19, 20)
HOLES = (S, S + D1, S + D2)
TARGET = tuple(v for v in range(1, 280) if v not in HOLES)

CORE_EDGES = (
    ("z", "b1", 1),
    ("z", "b2", 2),
    ("c", "d6", 6),
    ("c", "z", 7),
    ("z", "a", 10),
)
GATE_Q = {
    "z": tuple(range(13, 21)),
    "b1": tuple(range(14, 21)),
    "b2": tuple(range(15, 21)),
    "c": tuple(range(17, 21)),
}


def core_adjacency() -> dict[str, list[tuple[str, int]]]:
    adj: dict[str, list[tuple[str, int]]] = {}
    for a, b, w in CORE_EDGES:
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))
    return adj


CORE_ADJ = core_adjacency()


def oriented_core(gate: str, q: int) -> tuple[dict[str, int], dict[int, int]]:
    """Return core vertex -> high y and fixed child-y -> parent-y."""
    offset = {gate: 0}
    parent_vertex: dict[str, str] = {}
    queue = deque([gate])
    while queue:
        v = queue.popleft()
        for u, w in CORE_ADJ[v]:
            if u in offset:
                continue
            offset[u] = offset[v] + w
            parent_vertex[u] = v
            queue.append(u)

    gate_y = 20 - q
    vertex_y = {v: gate_y + off for v, off in offset.items()}
    if len(set(vertex_y.values())) != 6:
        raise AssertionError("core rooted profile is not injective")
    if not all(0 <= y <= 20 for y in vertex_y.values()):
        raise AssertionError("all-high gate row escaped high block")

    fixed_parent = {
        vertex_y[v]: vertex_y[p]
        for v, p in parent_vertex.items()
    }
    if not all(p < y for y, p in fixed_parent.items()):
        raise AssertionError("core orientation is not rootward")
    return vertex_y, fixed_parent


def build_edges(parent: dict[int, int]) -> list[tuple[int, int, int]]:
    # Low vertices: 0=x, 1=u1, 2=u2.  High v_y is node 3+y.
    edges = [(0, 1, D1), (1, 2, D2 - D1)]
    for y in range(21):
        child = 3 + y
        if y in ROOT_COLOR:
            low = ROOT_COLOR[y]
            edges.append((low, child, B + y - LOW_DEPTH[low]))
        else:
            p = parent[y]
            edges.append((3 + p, child, y - p))
    if len(edges) != 23:
        raise AssertionError("wrong edge count")
    return edges


def all_pair_distances(edges: list[tuple[int, int, int]]) -> tuple[int, ...]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(24)]
    for a, b, w in edges:
        if w <= 0:
            raise AssertionError("nonpositive edge")
        adj[a].append((b, w))
        adj[b].append((a, w))

    distances: list[int] = []
    for src in range(24):
        dist: list[int | None] = [None] * 24
        dist[src] = 0
        stack = [src]
        while stack:
            v = stack.pop()
            for u, w in adj[v]:
                if dist[u] is not None:
                    continue
                dist[u] = dist[v] + w  # type: ignore[operator]
                stack.append(u)
        if any(d is None for d in dist):
            raise AssertionError("disconnected candidate")
        distances.extend(int(dist[v]) for v in range(src + 1, 24))
    if len(distances) != 276:
        raise AssertionError("wrong pair count")
    return tuple(sorted(distances))


def run(max_examples: int) -> dict[str, object]:
    rows_total = 0
    rows_compatible = 0
    assignments_tested = 0
    assignments_parent_legal = 0
    spectrum_survivors = 0
    examples: list[dict[str, object]] = []
    row_stats: list[dict[str, object]] = []

    for gate, qs in GATE_Q.items():
        for q in qs:
            rows_total += 1
            vertex_y, fixed_parent = oriented_core(gate, q)
            non_gate_core_y = set(fixed_parent)

            # A selected component root cannot simultaneously have a fixed
            # high parent.  The core gate itself is intentionally not forced
            # to be a root.
            root_conflicts = sorted(non_gate_core_y.intersection(ROOT_COLOR))
            if root_conflicts:
                row_stats.append({
                    "gate": gate,
                    "q": q,
                    "compatible": False,
                    "reason": "selected_root_has_fixed_core_parent",
                    "conflicting_selected_root_y": root_conflicts,
                    "core_vertex_y": vertex_y,
                })
                continue

            rows_compatible += 1
            unknown_children = sorted(
                set(range(21)) - set(ROOT_COLOR) - non_gate_core_y
            )
            if len(unknown_children) != 6:
                raise AssertionError("c=10 Class A must have six non-core children")

            row_tested = 0
            row_legal = 0
            row_survivors = 0
            for perm in itertools.permutations(W):
                assignments_tested += 1
                row_tested += 1
                parent = dict(fixed_parent)
                legal = True
                for child_y, weight in zip(unknown_children, perm):
                    p = child_y - weight
                    if p < 0:
                        legal = False
                        break
                    parent[child_y] = p
                if not legal:
                    continue
                assignments_parent_legal += 1
                row_legal += 1

                distances = all_pair_distances(build_edges(parent))
                if distances != TARGET:
                    continue

                spectrum_survivors += 1
                row_survivors += 1
                if len(examples) < max_examples:
                    examples.append({
                        "gate": gate,
                        "q": q,
                        "core_vertex_y": vertex_y,
                        "parent": {str(y): parent[y] for y in sorted(parent)},
                        "distance_sha256": hashlib.sha256(
                            ",".join(map(str, distances)).encode()
                        ).hexdigest(),
                    })

            row_stats.append({
                "gate": gate,
                "q": q,
                "compatible": True,
                "unknown_children": unknown_children,
                "assignments_tested": row_tested,
                "assignments_parent_legal": row_legal,
                "spectrum_survivors": row_survivors,
            })

    return {
        "status": "C10_CLASSA_FW303_FIXED_SIGNATURE_EXHAUSTED",
        "scope": {
            "s": S,
            "shape": "chain",
            "d1": D1,
            "d2": D2,
            "B": B,
            "c": 10,
            "class": "A_all_high",
            "root_color": {str(y): ROOT_COLOR[y] for y in sorted(ROOT_COLOR)},
            "noncore_hh_weights": list(W),
            "holes": list(HOLES),
        },
        "coverage": {
            "rows_total": rows_total,
            "rows_compatible": rows_compatible,
            "assignments_tested": assignments_tested,
            "assignments_parent_legal": assignments_parent_legal,
        },
        "spectrum_survivors": spectrum_survivors,
        "first_examples": examples,
        "row_stats": row_stats,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-examples", type=int, default=10)
    args = parser.parse_args()
    result = run(args.max_examples)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
