#!/usr/bin/env python3
"""Exact full-tree search for all FW303 gate classes A/B/C.

The input is the sound 38-row compatibility prefilter.  For every compatible
signature/row and every possible c<=13, this enumerates every missing forced
root, every free additional root and color, and every remaining non-core HH
parent edge.  Each terminal candidate is a complete 24-vertex tree whose 276
pair-distance multiset is compared exactly with F.

The implementation deliberately uses only row descriptors emitted by the
prefilter: fixed_high_parent describes core HH edges, while forced_roots
describes fixed low-high core edges.  Low-low core edges are already the two
edges of the chain and must not be inserted a second time.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


W = (4, 5, 16, 18, 19, 20)


def parse_group(text: str) -> list[int]:
    return [] if text == "" else [int(x) for x in text.split(",")]


def parse_signature(sig: str) -> tuple[int, str, int, int, dict[int, int]]:
    parts = sig.split("|")
    if len(parts) < 7:
        raise ValueError(f"bad signature: {sig}")
    root_color: dict[int, int] = {}
    for color, field in enumerate(parts[4:7]):
        for y in parse_group(field):
            if y in root_color:
                raise ValueError("duplicate selected root")
            root_color[y] = color
    if len(root_color) != 10:
        raise ValueError("not an exact-10 signature")
    return int(parts[0]), parts[1], int(parts[2]), int(parts[3]), root_color


def attachment_weight(s: int, d1: int, d2: int, y: int, color: int) -> int:
    b = 280 - s
    return b + y - (0, d1, d2)[color]


def build_edges(
    s: int,
    d1: int,
    d2: int,
    root_color: dict[int, int],
    parent: dict[int, int],
) -> list[tuple[int, int, int]]:
    b = 280 - s
    low_depth = (0, d1, d2)
    edges = [(0, 1, d1), (1, 2, d2 - d1)]
    for y in range(21):
        child = 3 + y
        if y in root_color:
            color = root_color[y]
            edges.append((color, child, b + y - low_depth[color]))
        else:
            p = parent[y]
            edges.append((3 + p, child, y - p))
    if len(edges) != 23:
        raise AssertionError("wrong edge count")
    if len({(min(a, b), max(a, b)) for a, b, _ in edges}) != 23:
        raise AssertionError("duplicate tree edge")
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


def legal_parent_vectors(
    children: list[int], available_w: tuple[int, ...]
):
    """Yield only injections whose induced parent p=child-w is nonnegative."""
    chosen_parent = [0] * len(children)
    used = [False] * len(available_w)

    def rec(index: int):
        if index == len(children):
            yield tuple(chosen_parent)
            return
        child = children[index]
        for weight_index, weight in enumerate(available_w):
            if used[weight_index] or weight > child:
                continue
            used[weight_index] = True
            chosen_parent[index] = child - weight
            yield from rec(index + 1)
            used[weight_index] = False

    yield from rec(0)


def search_row_c(
    signature: str,
    row: dict[str, object],
    c: int,
    max_examples: int,
) -> dict[str, object]:
    s, shape, d1, d2, selected = parse_signature(signature)
    if shape != "chain":
        raise ValueError("current scanner is chain-only")
    fixed_parent = {
        int(y): int(p)
        for y, p in dict(row["fixed_high_parent"]).items()  # type: ignore[arg-type]
    }
    forced = {
        int(y): int(color)
        for y, color in dict(row["forced_roots"]).items()  # type: ignore[arg-type]
    }
    if set(fixed_parent).intersection(forced):
        raise AssertionError("a core child cannot also be a forced root")
    if set(fixed_parent).intersection(selected):
        raise AssertionError("prefilter admitted selected fixed child")
    for y, color in forced.items():
        if y in selected and selected[y] != color:
            raise AssertionError("prefilter admitted forced-color conflict")

    base_roots = dict(selected)
    base_roots.update(forced)
    free_root_count = c - len(base_roots)
    f_c = len(fixed_parent)
    e = 21 - c - f_c
    if free_root_count < 0 or e < 0:
        return {
            "c": c,
            "f_C": f_c,
            "e": e,
            "reason": "root_or_edge_ledger_negative",
            "spectrum_survivors": 0,
            "first_examples": [],
        }

    eligible_free = sorted(set(range(21)) - set(base_roots) - set(fixed_parent))
    if free_root_count > len(eligible_free):
        return {
            "c": c,
            "f_C": f_c,
            "e": e,
            "reason": "insufficient_free_root_positions",
            "eligible_free_roots": eligible_free,
            "spectrum_survivors": 0,
            "first_examples": [],
        }

    target = tuple(v for v in range(1, 280) if v not in {s, s + d1, s + d2})
    fixed_weights = [y - p for y, p in sorted(fixed_parent.items())]
    if any(w <= 0 for w in fixed_weights):
        raise AssertionError("fixed high parent is not shallower")

    root_sets = 0
    root_colorings = 0
    root_edge_legal = 0
    capacity_rejects = 0
    weight_assignments = 0
    parent_legal = 0
    spectrum_survivors = 0
    examples: list[dict[str, object]] = []

    for free_roots in itertools.combinations(eligible_free, free_root_count):
        root_sets += 1
        for colors in itertools.product(range(3), repeat=free_root_count):
            root_colorings += 1
            roots = dict(base_roots)
            roots.update(zip(free_roots, colors))

            # Exactly the already installed tree edges: the two low-tree edges,
            # fixed core HH edges, and one low attachment for every complete root.
            edge_weights = [d1, d2 - d1, *fixed_weights]
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
                raise AssertionError("high-edge ledger mismatch")
            available_w = tuple(w for w in W if w not in set(edge_weights))
            if len(available_w) < e:
                capacity_rejects += 1
                continue

            weight_assignments += math.factorial(len(available_w)) // math.factorial(
                len(available_w) - e
            )
            for parent_vector in legal_parent_vectors(unknown_children, available_w):
                parent = dict(fixed_parent)
                parent.update(zip(unknown_children, parent_vector))
                parent_legal += 1

                edges = build_edges(s, d1, d2, roots, parent)
                weights_in_tree = [w for _, _, w in edges]
                if len(weights_in_tree) != len(set(weights_in_tree)):
                    raise AssertionError("edge uniqueness ledger failed")
                if distance_multiset(edges) != target:
                    continue
                spectrum_survivors += 1
                if len(examples) < max_examples:
                    examples.append({
                        "free_roots": {str(y): roots[y] for y in free_roots},
                        "all_roots": {str(y): roots[y] for y in sorted(roots)},
                        "parent": {str(y): parent[y] for y in sorted(parent)},
                    })

    return {
        "c": c,
        "f_C": f_c,
        "e": e,
        "forced_roots": {str(y): forced[y] for y in sorted(forced)},
        "missing_forced_roots": sorted(set(forced) - set(selected)),
        "eligible_free_roots": eligible_free,
        "free_root_count": free_root_count,
        "root_sets": root_sets,
        "root_colorings": root_colorings,
        "root_edge_legal": root_edge_legal,
        "capacity_rejects": capacity_rejects,
        "weight_assignments": weight_assignments,
        "parent_legal": parent_legal,
        "spectrum_survivors": spectrum_survivors,
        "first_examples": examples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prefilter", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int)
    parser.add_argument("--max-examples", type=int, default=10)
    args = parser.parse_args()
    source = json.loads(args.prefilter.read_text())
    source_results = source["results"]
    stop = len(source_results) if args.stop is None else min(args.stop, len(source_results))
    if not (0 <= args.start <= stop):
        raise ValueError("bad signature slice")

    results = []
    total_survivors = 0
    compatible_rows = 0
    rows_by_class = {"A": 0, "B": 0, "C": 0}
    row_c_jobs = 0
    for signature_index, signature_result in enumerate(
        source_results[args.start:stop], start=args.start
    ):
        signature = str(signature_result["signature"])
        for row in signature_result["rows"]:
            if not row["compatible"]:
                continue
            compatible_rows += 1
            row_class = str(row["class"])
            rows_by_class[row_class] += 1
            c_results = []
            for c in row["possible_c"]:
                result = search_row_c(signature, row, int(c), args.max_examples)
                total_survivors += int(result["spectrum_survivors"])
                row_c_jobs += 1
                c_results.append(result)
            results.append({
                "signature_index": signature_index,
                "signature": signature,
                "class": row_class,
                "gate": row["gate"],
                "q": row["q"],
                "f_C": row["f_C"],
                "fixed_high_parent": row["fixed_high_parent"],
                "forced_roots": row["forced_roots"],
                "c_results": c_results,
            })

    output = {
        "status": "FW303_ALL_CLASS_FORESTS_EXHAUSTED",
        "source_status": source.get("status"),
        "source_signature_count": source.get("source_signature_count"),
        "signature_start": args.start,
        "signature_stop": stop,
        "signatures_processed": stop - args.start,
        "compatible_rows": compatible_rows,
        "compatible_rows_by_class": rows_by_class,
        "row_c_jobs": row_c_jobs,
        "total_full_spectrum_survivors": total_survivors,
        "results": results,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
