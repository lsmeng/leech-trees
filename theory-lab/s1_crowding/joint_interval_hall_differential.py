#!/usr/bin/env python3
"""Remote-only tiny differential for joint_interval_hall_pilot."""
from __future__ import annotations

import itertools
import json
from math import ceil, comb

from joint_interval_hall_pilot import class_intervals, interval_hall


def parts(n, hi=None):
    if n == 0:
        yield ()
        return
    if hi is None or hi > n:
        hi = n
    for x in range(hi, 0, -1):
        for rest in parts(n - x, x):
            yield (x,) + rest


def local_tuples(m, r):
    all_parts = [tuple(parts(a)) for a in range(m + 1)]

    def rec(v, remaining, out):
        if v == r - 1:
            for p in all_parts[remaining]:
                yield tuple(out + [p])
            return
        for a in range(remaining + 1):
            for p in all_parts[a]:
                out.append(p)
                yield from rec(v + 1, remaining - a, out)
                out.pop()

    yield from rec(0, m, [])


def p_vector(lowpar, masses):
    r = len(lowpar)
    children = [[] for _ in range(r)]
    for v in range(1, r):
        children[lowpar[v]].append(v)
    subtree = [sum(masses[v]) for v in range(r)]
    local_w = [sum(comb(n, 2) for n in masses[v]) for v in range(r)]
    for v in range(r - 1, -1, -1):
        for u in children[v]:
            subtree[v] += subtree[u]
    return tuple(
        comb(subtree[v], 2)
        - sum(comb(subtree[u], 2) for u in children[v])
        - local_w[v]
        for v in range(r)
    )


def valid_depths(lowpar, pvals, delta, s):
    b = delta + 1 - s
    if b <= 1 or pvals[0] > 2 * s - delta - 2:
        return
    for tail in itertools.permutations(range(1, b), len(lowpar) - 1):
        depths = (0,) + tail
        if all(
            depths[v] >= max(1, ceil((delta + 2 - 2 * s + pvals[v]) / 2))
            and depths[v] > depths[lowpar[v]]
            for v in range(1, len(lowpar))
        ):
            yield depths


def brute_class_matching(m, delta, s, depths, W, pvals, occupied):
    """Independent tiny backtracking oracle for the interval class slots."""
    b = delta + 1 - s
    cap = 2 * m - 3
    used = set(occupied)
    options = [set(range(1, cap + 1))]
    for lv in depths:
        lo = max(1, 2 * b - 2 * lv + 1)
        hi = min(delta, 2 * b - 2 * lv + cap)
        options.append(set(range(lo, hi + 1)))
    options = [x - used for x in options]
    remaining = [W] + list(pvals)

    def rec(left, taken):
        if not any(left):
            return True
        choices = [
            (len(options[i] - taken), i)
            for i, count in enumerate(left)
            if count
        ]
        _, i = min(choices)
        for x in sorted(options[i] - taken):
            left[i] -= 1
            taken.add(x)
            if rec(left, taken):
                return True
            taken.remove(x)
            left[i] += 1
        return False

    return rec(remaining, set())


def main():
    report = []
    for name, lowpar in (
        ("chain3", [-1, 0, 1]),
        ("star3", [-1, 0, 0]),
        ("branch4", [-1, 0, 1, 1]),
    ):
        mass_s_pairs = exact_depth_assignments = hall_rejects = mismatches = 0
        max_subsets = 0
        for masses in local_tuples(5, len(lowpar)):
            pvals = p_vector(lowpar, masses)
            for s in range(5, 9):
                mass_s_pairs += 1
                for depths in valid_depths(lowpar, pvals, 10, s) or ():
                    exact_depth_assignments += 1
                    within = comb(5, 2) - sum(pvals)
                    result = interval_hall(5, 10, s, depths, within, pvals, lowpar=lowpar)
                    oracle = brute_class_matching(5, 10, s, depths, within, pvals, ())
                    max_subsets = max(max_subsets, result["subsets_checked"])
                    hall_rejects += int(not result["necessary_pass"])
                    mismatches += int(result["necessary_pass"] != oracle)
        report.append({
            "shape": name,
            "mass_s_pairs": mass_s_pairs,
            "exact_depth_assignments": exact_depth_assignments,
            "hall_rejects": hall_rejects,
            "matching_mismatches": mismatches,
            "max_subsets_checked": max_subsets,
        })
    print(json.dumps({
        "status": "JOINT_INTERVAL_HALL_DIFFERENTIAL",
        "results": report,
        "soundness_ok": all(x["matching_mismatches"] == 0 for x in report),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
