#!/usr/bin/env python3
"""Immutable full-recomputation checker for the regular-LR offset search."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class OffsetStats:
    W: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    max_marks: int = 2
    frontier_states: int = 0


State = tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]


def canonical_side(legs) -> tuple[tuple[int, ...], ...]:
    first = tuple(sorted(legs[0]))
    rest = tuple(sorted(tuple(sorted(leg)) for leg in legs[1:]))
    return (first, *rest)


def canonical(left, right) -> State:
    return canonical_side(left), canonical_side(right)


def offsets(side) -> set[int]:
    return {x for leg in side for x in leg}


def high_sums(state: State) -> set[int]:
    left, right = state
    return {a + b for a in offsets(left) for b in offsets(right)}


def valid(state: State, W: int) -> bool:
    left, right = state
    for side in (left, right):
        flat = [x for leg in side for x in leg]
        if len(flat) != len(set(flat)):
            return False
        if any(x < 0 or x > W for x in flat):
            return False

    cross = [a + b for a in offsets(left) for b in offsets(right)]
    if len(cross) != len(set(cross)):
        return False

    differences = []
    for side in (left, right):
        for leg in side:
            seq = sorted(leg)
            differences.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
    if len(differences) != len(set(differences)):
        return False

    for side in (left, right):
        tagged = [(x, i) for i, leg in enumerate(side) for x in leg]
        sums = [
            x + y
            for j, (x, li) in enumerate(tagged)
            for y, lj in tagged[j + 1 :]
            if li != lj
        ]
        if len(sums) != len(set(sums)):
            return False
    return True


def placements(side, value: int):
    found = [(i, False) for i, leg in enumerate(side) if value in leg]
    if found:
        return found
    return [(i, True) for i in range(len(side) + 1)]


def add(side, leg_index: int, value: int, is_new: bool):
    if not is_new:
        return tuple(tuple(leg) for leg in side)
    legs = [list(leg) for leg in side]
    if leg_index == len(legs):
        legs.append([value])
    else:
        legs[leg_index].append(value)
    return tuple(tuple(leg) for leg in legs)


def children(state: State, target: int, W: int) -> tuple[State, ...]:
    left, right = state
    out: set[State] = set()
    for a in range(target + 1):
        b = target - a
        if a > W or b > W:
            continue
        for li, add_left in placements(left, a):
            for ri, add_right in placements(right, b):
                if not add_left and not add_right:
                    continue
                child = canonical(
                    add(left, li, a, add_left),
                    add(right, ri, b, add_right),
                )
                if valid(child, W):
                    out.add(child)
    return tuple(sorted(out))


def check_regular_lr(W: int) -> OffsetStats:
    if W < 1:
        raise ValueError("W must be positive")
    stats = OffsetStats(W=W)

    def dfs(state: State, target: int) -> None:
        stats.nodes += 1
        stats.max_marks = max(
            stats.max_marks,
            sum(len(leg) for side in state for leg in side),
        )
        values = high_sums(state)
        while target in values:
            target += 1
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, target)
        if target > W:
            stats.frontier_states += 1
            return
        next_states = children(state, target, W)
        if not next_states:
            stats.dead_states += 1
            return
        for child in next_states:
            stats.accepted_children += 1
            dfs(child, target + 1)

    initial = (((0,),), ((0,),))
    if not valid(initial, W):
        raise RuntimeError("invalid initial regular-LR offset state")
    dfs(initial, 1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(asdict(check_regular_lr(args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
