#!/usr/bin/env python3
"""Immutable full-recomputation checker for the dominant LR relaxation.

Put C=A+Q.  Under ``A>W`` and ``B-C>W``, every value N-k (k<=W) joins the
dominant right tip branch to either a near-A left mark or a near-C mark on
another right leg.  The immutable state below recomputes every retained
parameter-independent collision class from scratch.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


State = tuple[
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]


@dataclass
class CleanroomStats:
    W: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    max_marks: int = 2
    frontier: int = 0


def canon_legs(legs, anchored: bool):
    normalized = [tuple(sorted(leg)) for leg in legs]
    if anchored:
        return (normalized[0], *sorted(normalized[1:]))
    return tuple(sorted(normalized))


def canonical(top, left, right) -> State:
    return tuple(sorted(top)), canon_legs(left, True), canon_legs(right, False)


def valid(state: State, W: int) -> bool:
    top, left, right = state
    lower_l = [x for leg in left for x in leg]
    lower_r = [x for leg in right for x in leg]
    lower = lower_l + lower_r
    if len(top) != len(set(top)) or len(lower) != len(set(lower)):
        return False
    if any(x < 0 or x > W for x in (*top, *lower)):
        return False

    high = [a + b for a in top for b in lower]
    if len(high) != len(set(high)):
        return False

    differences = []
    for leg in (top, *left, *right):
        seq = sorted(leg)
        differences.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
    if len(differences) != len(set(differences)):
        return False

    tagged_l = [(x, i) for i, leg in enumerate(left) for x in leg]
    left_sums = [
        x + y
        for j, (x, li) in enumerate(tagged_l)
        for y, lj in tagged_l[j + 1 :]
        if li != lj
    ]
    if len(left_sums) != len(set(left_sums)):
        return False

    tagged_r = [(x, i) for i, leg in enumerate(right) for x in leg]
    common_base_sums = [x + y for x in lower_l for y in lower_r]
    common_base_sums.extend(
        x + y
        for j, (x, li) in enumerate(tagged_r)
        for y, lj in tagged_r[j + 1 :]
        if li != lj
    )
    return len(common_base_sums) == len(set(common_base_sums))


def add_to_legs(legs, leg_index: int, value: int):
    out = [list(leg) for leg in legs]
    if leg_index == len(out):
        out.append([value])
    else:
        out[leg_index].append(value)
    return tuple(tuple(leg) for leg in out)


def children(state: State, k: int, W: int):
    top, left, right = state
    lower_location = {
        x: ("L", i)
        for i, leg in enumerate(left)
        for x in leg
    }
    lower_location.update(
        {x: ("R", i) for i, leg in enumerate(right) for x in leg}
    )
    out = set()
    for a in range(k + 1):
        b = k - a
        if a > W or b > W:
            continue
        top_variants = [(top, False)] if a in top else [(tuple(top) + (a,), True)]
        if b in lower_location:
            lower_variants = [(left, right, False)]
        else:
            lower_variants = []
            lower_variants.extend(
                (add_to_legs(left, i, b), right, True)
                for i in range(len(left) + 1)
            )
            lower_variants.extend(
                (left, add_to_legs(right, i, b), True)
                for i in range(len(right) + 1)
            )
        for new_top, top_added in top_variants:
            for new_left, new_right, lower_added in lower_variants:
                if not top_added and not lower_added:
                    continue
                child = canonical(new_top, new_left, new_right)
                if valid(child, W):
                    out.add(child)
    return tuple(sorted(out))


def check_dominant_lr(W: int) -> CleanroomStats:
    stats = CleanroomStats(W=W)

    def dfs(state: State, k: int):
        stats.nodes += 1
        stats.max_marks = max(
            stats.max_marks,
            len(state[0]) + sum(len(leg) for side in state[1:] for leg in side),
        )
        high = {a + b for a in state[0] for side in state[1:] for leg in side for b in leg}
        while k in high:
            k += 1
        stats.deepest = max(stats.deepest, k)
        if k > W:
            stats.frontier += 1
            return
        next_states = children(state, k, W)
        if not next_states:
            stats.dead += 1
            return
        for child in next_states:
            stats.children += 1
            dfs(child, k + 1)

    initial = ((0,), ((0,),), ())
    if not valid(initial, W):
        raise RuntimeError("invalid dominant-regime initial state")
    dfs(initial, 1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", type=int, default=30)
    args = parser.parse_args()
    print(json.dumps(asdict(check_dominant_lr(args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
