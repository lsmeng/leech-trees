#!/usr/bin/env python3
"""Validation ladder for the exact three-centre clean-room prototype."""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "theory-lab" / "exp-families"))

from gen_shapes import gen_threebranch  # noqa: E402
from threebranch_cleanroom import (  # noqa: E402
    REQUIRED_LEGS,
    Geometry,
    State,
    Stats,
    Vertex,
    add_raw,
    all_positions,
    anchor_geometries,
    branch_feasible,
    canonical,
    child_states,
    distance_values,
    pair_distance,
    solve,
    state_to_edges,
)


MODES = ("AA", "BB", "AB", "AC")
EMPTY = ()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def anchor_key(geometry: Geometry, anchor: dict):
    parameters = tuple(anchor[key] for key in sorted(anchor) if key != "mode")
    return anchor["mode"], geometry.q1, geometry.q2, parameters, geometry.fresh_caps


def independent_initial_values(
    q1: int,
    q2: int,
    endpoints: tuple[tuple[int, int], tuple[int, int]],
) -> list[int]:
    """Distances on the three centres plus two anchor tips, without search code."""
    positions = (0, q1, q1 + q2)
    raw = [q1, q2, q1 + q2]
    for centre, depth in endpoints:
        raw.extend(depth + abs(positions[centre] - position) for position in positions)
    (c0, d0), (c1, d1) = endpoints
    raw.append(d0 + d1 + abs(positions[c0] - positions[c1]))
    return raw


def independent_anchor_set(n: int, mode: str):
    """Brute parameter loops plus the universal fresh-leg cap formula."""
    maximum = n * (n - 1) // 2
    out = set()

    def add(q1, q2, endpoints, fixed_caps, initial_counts, parameters):
        positions = (0, q1, q1 + q2)
        fresh_caps = tuple(
            min(maximum - 1 - depth - abs(positions[centre] - positions[anchor_centre])
                for anchor_centre, depth in endpoints)
            for centre in range(3)
        )
        for centre, required in enumerate(REQUIRED_LEGS):
            if initial_counts[centre] < required and fresh_caps[centre] < 1:
                return
        missing_legs = sum(max(0, required - initial_counts[centre])
                           for centre, required in enumerate(REQUIRED_LEGS))
        if missing_legs > n - 5:  # two anchor tips already use two of n-3 marks
            return
        raw = independent_initial_values(q1, q2, endpoints)
        if any(value < 1 or value > maximum for value in raw):
            return
        if len(raw) != len(set(raw)) or maximum not in raw:
            return
        geometry = Geometry(q1, q2, fixed_caps, fresh_caps)
        out.add(anchor_key(geometry, {"mode": mode, **parameters}))

    if mode in ("AA", "BB"):
        centre = 0 if mode == "AA" else 1
        for long_tip in range(maximum // 2 + 1, maximum):
            short_tip = maximum - long_tip
            for q1 in range(1, maximum):
                q2_start = q1 + 1 if mode == "BB" else 1
                for q2 in range(q2_start, maximum):
                    fixed = ((long_tip, short_tip), EMPTY, EMPTY) if mode == "AA" \
                        else (EMPTY, (long_tip, short_tip), EMPTY)
                    counts = (2, 0, 0) if mode == "AA" else (0, 2, 0)
                    add(q1, q2, ((centre, long_tip), (centre, short_tip)),
                        fixed, counts,
                        {"long_tip": long_tip, "short_tip": short_tip})

    elif mode == "AB":
        for end_tip in range(1, maximum):
            for middle_tip in range(1, maximum):
                q1 = maximum - end_tip - middle_tip
                if q1 < 1:
                    continue
                for q2 in range(1, maximum):
                    add(q1, q2, ((0, end_tip), (1, middle_tip)),
                        ((end_tip,), (middle_tip,), EMPTY), (1, 1, 0),
                        {"end_tip": end_tip, "middle_tip": middle_tip})

    elif mode == "AC":
        for left_tip in range(1, maximum):
            for right_tip in range(left_tip + 1, maximum):
                total = maximum - left_tip - right_tip
                for q1 in range(1, total):
                    add(q1, total - q1, ((0, left_tip), (2, right_tip)),
                        ((left_tip,), EMPTY, (right_tip,)), (1, 0, 1),
                        {"left_tip": left_tip, "right_tip": right_tip})
    else:
        raise RuntimeError(f"unknown mode {mode}")
    return out


def generated_anchor_set(n: int, mode: str):
    maximum = n * (n - 1) // 2
    out = set()
    for geometry, initial, anchor in anchor_geometries(n, (mode,)):
        if distance_values(initial, geometry, maximum) is None:
            continue
        if not branch_feasible(initial, n):
            continue
        out.add(anchor_key(geometry, anchor))
    return out


def verify_anchor_partition() -> None:
    counts = {}
    for n in (8, 9):
        for mode in MODES:
            expected = independent_anchor_set(n, mode)
            generated = generated_anchor_set(n, mode)
            require(generated == expected,
                    f"anchor mismatch n={n} mode={mode}: "
                    f"generated-only={len(generated - expected)} "
                    f"expected-only={len(expected - generated)}")
            counts[(n, mode)] = len(generated)
    print("PASS anchor partition and fresh caps:", counts)


def independent_tree_distances(vertex_count: int, edges):
    adjacency = [[] for _ in range(vertex_count)]
    for u, v, weight in edges:
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))
    values = []
    for source in range(vertex_count):
        stack = [(source, -1, 0)]
        distances = {}
        while stack:
            vertex, parent, distance = stack.pop()
            distances[vertex] = distance
            for neighbour, weight in adjacency[vertex]:
                if neighbour != parent:
                    stack.append((neighbour, vertex, distance + weight))
        require(len(distances) == vertex_count, "edge conversion is disconnected")
        values.extend(distances[target] for target in range(source + 1, vertex_count))
    return values


def verify_metric_conversion() -> None:
    n = 9
    maximum = 36
    checked = 0
    per_mode = defaultdict(int)
    for geometry, initial, anchor in anchor_geometries(n, MODES):
        if per_mode[anchor["mode"]] >= 12:
            continue
        values = distance_values(initial, geometry, maximum)
        if values is None or not branch_feasible(initial, n):
            continue
        actual_n, edges = state_to_edges(initial, geometry)
        independent = independent_tree_distances(actual_n, edges)
        require(len(independent) == len(set(independent)), "converted anchor has duplicate")
        require(frozenset(independent) == values,
                f"metric conversion mismatch: {anchor} {geometry}")
        per_mode[anchor["mode"]] += 1
        checked += 1
    require(all(per_mode[mode] == 12 for mode in MODES),
            f"insufficient metric samples: {dict(per_mode)}")
    print(f"PASS independent weighted-tree metric conversion: {checked} anchors")


def brute_children(state: State, geometry: Geometry, target: int, n: int, maximum: int):
    out = set()
    old_count = sum(len(leg) for centre in state.legs for leg in centre) + len(state.spine)
    first_positions = tuple(all_positions(state, geometry))
    if old_count + 1 <= n - 3:
        for first in first_positions:
            state1 = add_raw(state, first)
            if state1 is None:
                continue
            child = canonical(state1, geometry)
            values = distance_values(child, geometry, maximum)
            if values is not None and target in values and branch_feasible(child, n):
                out.add(child)
    if old_count + 2 <= n - 3:
        for first in first_positions:
            state1 = add_raw(state, first)
            if state1 is None:
                continue
            values1 = distance_values(state1, geometry, maximum)
            if values1 is None or target in values1:
                continue
            for second in all_positions(state1, geometry):
                if pair_distance(first, second, geometry) != target:
                    continue
                state2 = add_raw(state1, second)
                if state2 is None:
                    continue
                child = canonical(state2, geometry)
                values2 = distance_values(child, geometry, maximum)
                if values2 is not None and target in values2 and branch_feasible(child, n):
                    out.add(child)
    return out


def verify_child_options() -> None:
    n = 9
    maximum = 36
    checked = 0
    per_mode = defaultdict(int)
    for geometry, initial, anchor in anchor_geometries(n, MODES):
        mode = anchor["mode"]
        if per_mode[mode] >= 3:
            continue
        values = distance_values(initial, geometry, maximum)
        if values is None or not branch_feasible(initial, n):
            continue
        target = next(value for value in range(maximum, 0, -1) if value not in values)
        optimized = set(child_states(initial, geometry, target, n, maximum, Stats()))
        brute = brute_children(initial, geometry, target, n, maximum)
        require(optimized == brute,
                f"child mismatch {anchor} {geometry}: "
                f"optimized-only={len(optimized - brute)} brute-only={len(brute - optimized)}")
        per_mode[mode] += 1
        checked += 1
    require(all(per_mode[mode] == 3 for mode in MODES),
            f"insufficient child samples: {dict(per_mode)}")
    print(f"PASS solved-partner options equal brute one/two-mark enumeration: {checked} anchors")


def fixed_topology_solution_count(n: int) -> int:
    lines = []
    shape_count = 0
    for edges, tags in gen_threebranch(n):
        line = str(n) + " " + " ".join(f"{u} {v}" for u, v in edges)
        line += " G " + " ".join(f"{group} {branch}" for group, branch in tags)
        lines.append(line + "\n")
        shape_count += 1
    binary = ROOT / "theory-lab" / "exp-families" / "forced_family"
    process = subprocess.run([str(binary), "0"], input="".join(lines),
                             capture_output=True, text=True, check=False)
    require(process.returncode == 0, f"fixed-topology engine failed: {process.stderr}")
    results = []
    for line in process.stdout.splitlines():
        if not line.startswith("RES "):
            continue
        fields = dict(piece.split("=") for piece in line.split()[1:])
        require(int(fields["capped"]) == 0, f"fixed topology capped: {line}")
        results.append(int(fields["found"]))
    require(len(results) == shape_count,
            f"fixed topology returned {len(results)} of {shape_count} shapes")
    return sum(results)


def verify_small_orders(max_order: int) -> None:
    rows = {}
    for n in range(8, max_order + 1):
        solutions, stats = solve(n, MODES)
        require(not stats.capped, f"clean-room run capped at n={n}")
        fixed_count = fixed_topology_solution_count(n)
        require(len(solutions) == fixed_count,
                f"solution-count mismatch n={n}: clean={len(solutions)} fixed={fixed_count}")
        require(len(solutions) == 0, f"unexpected three-branch Leech tree at n={n}")
        rows[n] = {
            "anchors": stats.anchors,
            "nodes": stats.nodes,
            "solutions": len(solutions),
            "fixed_solutions": fixed_count,
        }
    print("PASS exact small-order differential:", rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, choices=(9, 10), default=9,
                        help="10 reproduces the slower four-mode calibration")
    args = parser.parse_args()
    verify_anchor_partition()
    verify_metric_conversion()
    verify_child_options()
    verify_small_orders(args.max_order)
    print("PASS complete three-branch clean-room validation ladder")


if __name__ == "__main__":
    main()
