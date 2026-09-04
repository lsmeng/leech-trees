#!/usr/bin/env python3
"""Audit the Kruskal covering schedule and merge-waste inequality."""

from __future__ import annotations

import hashlib
import json
import random
import sys
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "src"))
from checker_a import is_leech as checker_a  # noqa: E402
from checker_b import is_leech as checker_b  # noqa: E402


EXPECTED = {
    "random_distinct_distance_trees": 900,
    "random_pair_maximum_checks": 28_200,
    "known_leech_witnesses": 5,
    "known_schedule_steps": 14,
    "known_total_waste": 52,
    "checker_a_passes": 5,
    "checker_b_passes": 5,
    "sha256": "94c619aa2b33abd483a7f00ee792708385190c00f2c9335db7686bc0083f0757",
}


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def pair_data(n: int, edges: list[tuple[int, int, int]]):
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for left, right, weight in edges:
        adjacency[left].append((right, weight))
        adjacency[right].append((left, weight))
    rows = []
    for source in range(n):
        stack = [(source, -1, 0, 0)]
        while stack:
            vertex, parent, distance, maximum = stack.pop()
            if source < vertex:
                rows.append((source, vertex, distance, maximum))
            for neighbour, weight in adjacency[vertex]:
                if neighbour != parent:
                    stack.append((neighbour, vertex, distance + weight, max(maximum, weight)))
    require(len(rows) == comb(n, 2), ("pair count", n, rows))
    return rows


def merge_profile(n: int, edges: list[tuple[int, int, int]]):
    ordered = sorted(edges, key=lambda edge: edge[2])
    require(len({weight for _, _, weight in ordered}) == len(ordered),
            ("edge-weight collision", n, edges))
    parent = list(range(n))
    size = [1] * n

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    rows = []
    cumulative = 0
    for left, right, weight in ordered:
        first, second = root(left), root(right)
        require(first != second, ("cycle in merge profile", n, edges, left, right))
        product = size[first] * size[second]
        cumulative += product
        rows.append((weight, size[first], size[second], product, cumulative))
        if size[first] < size[second]:
            first, second = second, first
        parent[second] = first
        size[first] += size[second]
    require(cumulative == comb(n, 2), ("merge products do not sum to pairs", n, rows))
    return rows


def component_labels(n: int, edges: list[tuple[int, int, int]], threshold: int):
    adjacency = [[] for _ in range(n)]
    for left, right, weight in edges:
        if weight <= threshold:
            adjacency[left].append(right)
            adjacency[right].append(left)
    labels = [-1] * n
    for start in range(n):
        if labels[start] != -1:
            continue
        label = start
        stack = [start]
        while stack:
            vertex = stack.pop()
            if labels[vertex] != -1:
                continue
            labels[vertex] = label
            stack.extend(adjacency[vertex])
    return labels


def check_general(n: int, edges: list[tuple[int, int, int]]):
    pairs = pair_data(n, edges)
    profile = merge_profile(n, edges)
    maximum_sum = sum(maximum for _, _, _, maximum in pairs)
    merge_sum = sum(weight * product for weight, _, _, product, _ in profile)
    require(maximum_sum == merge_sum,
            ("path-maximum/merge identity", n, maximum_sum, merge_sum, edges))
    slack = sum(distance - maximum for _, _, distance, maximum in pairs)
    require(slack >= 0, ("negative path slack", n, slack, pairs))
    return pairs, profile, slack


def check_leech(witness: dict):
    n = witness["n"]
    edges = [tuple(edge) for edge in witness["edges"]]
    ok_a, why_a = checker_a(n, edges)
    ok_b, why_b = checker_b(n, edges)
    require(ok_a, ("checker A rejection", witness["name"], why_a))
    require(ok_b, ("checker B rejection", witness["name"], why_b))
    pairs, profile, slack = check_general(n, edges)
    total_pairs = comb(n, 2)
    require(sorted(distance for _, _, distance, _ in pairs) == list(range(1, total_pairs + 1)),
            ("non-Leech witness", witness["name"], pairs))

    schedule = []
    pi_previous = 0
    for index, (weight, _, _, product, cumulative) in enumerate(profile):
        require(weight <= 1 + pi_previous,
                ("covering schedule failure", witness["name"], index, weight, pi_previous))
        sigma = pi_previous - (weight - 1)
        labels = component_labels(n, edges, weight - 1)
        large_inside = sum(
            1 for left, right, distance, _ in pairs
            if labels[left] == labels[right] and distance > weight
        )
        require(sigma == large_inside,
                ("schedule deficit mismatch", witness["name"], index, sigma, large_inside))
        schedule.append((weight, product, pi_previous, sigma))
        pi_previous = cumulative

    pi_by_threshold = []
    for threshold in range(1, total_pairs + 1):
        pi = sum(product for weight, _, _, product, _ in profile if weight <= threshold)
        require(pi >= threshold, ("cover deficit", witness["name"], threshold, pi))
        pi_by_threshold.append(pi)
    total_waste = sum(pi - threshold for threshold, pi in enumerate(pi_by_threshold, start=1))
    moment_form = total_pairs * (total_pairs + 1) // 2 - sum(
        weight * product for weight, _, _, product, _ in profile
    )
    lower_numerator = sum(product * product for _, _, _, product, _ in profile) - total_pairs
    require(lower_numerator % 2 == 0,
            ("nonintegral quadratic base", witness["name"], lower_numerator))
    quadratic_base = lower_numerator // 2
    weighted_covering_surplus = sum(
        product * sigma
        for (_, product, _, sigma) in schedule
    )
    require(2 * total_waste >= lower_numerator,
            ("merge-waste lower bound", witness["name"], total_waste, lower_numerator))
    require(total_waste == quadratic_base + weighted_covering_surplus,
            ("covering-surplus decomposition", witness["name"], total_waste,
             quadratic_base, weighted_covering_surplus))
    require(total_waste == moment_form == slack,
            ("waste identity", witness["name"], total_waste, moment_form, slack))
    return {
        "name": witness["name"],
        "schedule": schedule,
        "total_waste": total_waste,
        "lower_bound_numerator": lower_numerator,
        "weighted_covering_surplus": weighted_covering_surplus,
    }


def audit() -> dict[str, int | str]:
    rng = random.Random(2026082107)
    transcript = []
    totals = {
        "random_distinct_distance_trees": 0,
        "random_pair_maximum_checks": 0,
        "known_leech_witnesses": 0,
        "known_schedule_steps": 0,
        "known_total_waste": 0,
        "checker_a_passes": 0,
        "checker_b_passes": 0,
    }
    for n in range(4, 13):
        for sample in range(100):
            parents = [rng.randrange(vertex) for vertex in range(1, n)]
            weights = [1 << index for index in range(n - 1)]
            rng.shuffle(weights)
            edges = [(vertex, parents[vertex - 1], weights[vertex - 1])
                     for vertex in range(1, n)]
            pairs, profile, slack = check_general(n, edges)
            totals["random_distinct_distance_trees"] += 1
            totals["random_pair_maximum_checks"] += len(pairs)
            transcript.append(("random", n, sample, tuple(profile), slack))

    witnesses = json.loads((REPO / "data" / "known_leech_trees.json").read_text())["trees"]
    for witness in witnesses:
        row = check_leech(witness)
        totals["known_leech_witnesses"] += 1
        totals["known_schedule_steps"] += len(row["schedule"])
        totals["known_total_waste"] += row["total_waste"]
        totals["checker_a_passes"] += 1
        totals["checker_b_passes"] += 1
        transcript.append(("leech", row))

    totals["sha256"] = hashlib.sha256(
        json.dumps(transcript, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return totals


def main() -> None:
    require(sys.flags.optimize == 0, "run without python -O/-OO")
    summary = audit()
    require(summary == EXPECTED, ("frozen invariant mismatch", summary, EXPECTED))
    print(json.dumps({
        "claim": "Kruskal covering schedule and merge-waste inequality",
        "status": "VERIFIED",
        **summary,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
