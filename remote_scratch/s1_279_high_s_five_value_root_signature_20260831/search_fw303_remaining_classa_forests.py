#!/usr/bin/env python3
"""Exact full-tree search for FW303-compatible Class-A v4w signatures.

Input is the sound 38-row compatibility prefilter.  For every surviving
all-high row and c=10..13, this enumerates all additional component roots,
their low parents, and all non-core HH parent edges.  It then compares the
complete 276-distance multiset of the resulting 24-vertex tree with F.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


W = (4, 5, 16, 18, 19, 20)
CORE_EDGE_WEIGHTS = (1, 2, 6, 7, 10)


def parse_group(text: str) -> list[int]:
    return [] if text == "" else [int(x) for x in text.split(",")]


def parse_signature(sig: str) -> tuple[int, str, int, int, dict[int, int]]:
    parts = sig.split("|")
    root_color: dict[int, int] = {}
    for color, field in enumerate(parts[4:7]):
        for y in parse_group(field):
            root_color[y] = color
    if len(root_color) != 10:
        raise ValueError("not an exact-10 signature")
    return int(parts[0]), parts[1], int(parts[2]), int(parts[3]), root_color


def attachment_weight(s: int, d1: int, d2: int, y: int, color: int) -> int:
    B = 280 - s
    return B + y - (0, d1, d2)[color]


def build_edges(
    s: int,
    d1: int,
    d2: int,
    root_color: dict[int, int],
    parent: dict[int, int],
) -> list[tuple[int, int, int]]:
    B = 280 - s
    edges = [(0, 1, d1), (1, 2, d2 - d1)]
    low_depth = (0, d1, d2)
    for y in range(21):
        child = 3 + y
        if y in root_color:
            color = root_color[y]
            edges.append((color, child, B + y - low_depth[color]))
        else:
            p = parent[y]
            edges.append((3 + p, child, y - p))
    if len(edges) != 23:
        raise AssertionError("wrong edge count")
    return edges


def distance_multiset(edges: list[tuple[int, int, int]]) -> tuple[int, ...]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(24)]
    for a, b, w in edges:
        if w <= 0:
            raise AssertionError("nonpositive edge")
        adj[a].append((b, w))
        adj[b].append((a, w))
    out: list[int] = []
    for src in range(24):
        dist: list[int | None] = [None] * 24
        dist[src] = 0
        stack = [src]
        while stack:
            v = stack.pop()
            for u, w in adj[v]:
                if dist[u] is not None:
                    continue
                dist[u] = int(dist[v]) + w
                stack.append(u)
        if any(x is None for x in dist):
            raise AssertionError("disconnected candidate")
        out.extend(int(dist[v]) for v in range(src + 1, 24))
    return tuple(sorted(out))


def search_row_c(
    signature: str,
    row: dict[str, object],
    c: int,
    max_examples: int,
) -> dict[str, object]:
    s, shape, d1, d2, selected = parse_signature(signature)
    if shape != "chain":
        raise ValueError("current bounded scanner is chain-only")
    fixed_parent = {
        int(y): int(p)
        for y, p in dict(row["fixed_high_parent"]).items()  # type: ignore[arg-type]
    }
    f_c = int(row["f_C"])
    extra_count = c - 10
    e = 21 - c - f_c
    if e < 0:
        raise AssertionError("negative non-core HH count")

    eligible_extra = sorted(set(range(21)) - set(selected) - set(fixed_parent))
    target = tuple(v for v in range(1, 280) if v not in {s, s + d1, s + d2})

    root_sets = 0
    root_colorings = 0
    root_edge_legal = 0
    weight_assignments = 0
    parent_legal = 0
    spectrum_survivors = 0
    examples: list[dict[str, object]] = []

    for extra_roots_tuple in itertools.combinations(eligible_extra, extra_count):
        root_sets += 1
        for colors in itertools.product(range(3), repeat=extra_count):
            root_colorings += 1
            roots = dict(selected)
            roots.update(zip(extra_roots_tuple, colors))

            edge_weights = [d1, d2 - d1, *CORE_EDGE_WEIGHTS]
            edge_weights.extend(
                attachment_weight(s, d1, d2, y, color)
                for y, color in sorted(roots.items())
            )
            if any(not (0 < w < s) for w in edge_weights):
                continue
            if len(edge_weights) != len(set(edge_weights)):
                continue
            root_edge_legal += 1

            unknown_children = sorted(set(range(21)) - set(roots) - set(fixed_parent))
            if len(unknown_children) != e:
                raise AssertionError("ledger mismatch")
            available_w = tuple(w for w in W if w not in set(edge_weights))
            if len(available_w) < e:
                continue

            for weights in itertools.permutations(available_w, e):
                weight_assignments += 1
                parent = dict(fixed_parent)
                ok = True
                for child, w in zip(unknown_children, weights):
                    p = child - w
                    if p < 0:
                        ok = False
                        break
                    parent[child] = p
                if not ok:
                    continue
                parent_legal += 1

                distances = distance_multiset(build_edges(s, d1, d2, roots, parent))
                if distances != target:
                    continue
                spectrum_survivors += 1
                if len(examples) < max_examples:
                    examples.append({
                        "extra_roots": {str(y): roots[y] for y in extra_roots_tuple},
                        "parent": {str(y): parent[y] for y in sorted(parent)},
                    })

    return {
        "c": c,
        "f_C": f_c,
        "e": e,
        "eligible_additional_roots": eligible_extra,
        "root_sets": root_sets,
        "root_colorings": root_colorings,
        "root_edge_legal": root_edge_legal,
        "weight_assignments": weight_assignments,
        "parent_legal": parent_legal,
        "spectrum_survivors": spectrum_survivors,
        "first_examples": examples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prefilter", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--max-examples", type=int, default=10)
    args = parser.parse_args()
    source = json.loads(args.prefilter.read_text())

    results = []
    total_survivors = 0
    compatible_rows = 0
    for signature_result in source["results"]:
        signature = signature_result["signature"]
        for row in signature_result["rows"]:
            if not row["compatible"] or row["class"] != "A":
                continue
            compatible_rows += 1
            c_results = []
            for c in (10, 11, 12, 13):
                result = search_row_c(signature, row, c, args.max_examples)
                total_survivors += int(result["spectrum_survivors"])
                c_results.append(result)
            results.append({
                "signature": signature,
                "gate": row["gate"],
                "q": row["q"],
                "fixed_high_parent": row["fixed_high_parent"],
                "c_results": c_results,
            })

    output = {
        "status": "FW303_REMAINING_CLASSA_FORESTS_EXHAUSTED",
        "source_status": source.get("status"),
        "compatible_rows": compatible_rows,
        "c_values": [10, 11, 12, 13],
        "total_full_spectrum_survivors": total_survivors,
        "results": results,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
