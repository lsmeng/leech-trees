#!/usr/bin/env python3
"""N-independent relaxation for regular LR bi-spider anchors.

Let ``A`` and ``B`` be the largest left and right leg tips and let the two
branch centres be separated by weighted length ``Q``.  The LR anchor is

    N = A + Q + B.

If, for a chosen window W,

    A > W,  B > W,  Q + B - A > W,  Q + A - B > W,

then a value N-k with k<=W cannot be a centre/leg, spine/leg, same-side, or
same-leg distance.  It must join a left mark A-a to a right mark B-b, where
``a+b=k``.  The inequalities are deliberately strict and slightly stronger
than necessary; that is harmless for the regular region.

This program retains only necessary collision constraints on the bounded
offsets:

* every left-right offset sum is unique;
* same-leg offset differences are unique globally; and
* different-leg offset sums are unique on each side.

It omits cross-category and parameter-dependent collisions, all spine
vertices, and the vertex budget.  It is therefore a relaxation (supertree) of
every exact LR search satisfying the four inequalities.  Zero frontier is a
sound uniform nonexistence certificate for that regular LR region.
"""

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


def canonical_side(legs: list[set[int]]) -> tuple[tuple[int, ...], ...]:
    first = tuple(sorted(legs[0]))
    rest = tuple(sorted(tuple(sorted(leg)) for leg in legs[1:]))
    return (first, *rest)


def prove_regular_lr(W: int) -> OffsetStats:
    if W < 1:
        raise ValueError("W must be positive")
    stats = OffsetStats(W=W)
    left = [{0}]
    right = [{0}]
    high_sums = {0}
    small_differences: set[int] = set()
    left_cross_sums: set[int] = set()
    right_cross_sums: set[int] = set()

    def all_offsets(legs: list[set[int]]) -> set[int]:
        return {x for leg in legs for x in leg}

    def state_key():
        return canonical_side(left), canonical_side(right)

    def pieces_for(side: str, leg_index: int, value: int):
        own = left if side == "L" else right
        other = right if side == "L" else left
        own_cross = left_cross_sums if side == "L" else right_cross_sums
        own_values = all_offsets(own)
        other_values = all_offsets(other)
        if not (1 <= value <= W) or value in own_values:
            return None

        new_high = {value + x for x in other_values}
        if len(new_high) != len(other_values) or new_high & high_sums:
            return None

        same_leg = own[leg_index] if leg_index < len(own) else set()
        new_differences = {abs(value - x) for x in same_leg}
        if 0 in new_differences or len(new_differences) != len(same_leg):
            return None
        if new_differences & small_differences:
            return None

        other_own = {x for i, leg in enumerate(own) if i != leg_index for x in leg}
        new_cross = {value + x for x in other_own}
        if len(new_cross) != len(other_own) or new_cross & own_cross:
            return None
        return new_high, new_differences, new_cross

    def apply(side: str, leg_index: int, value: int, pieces):
        own = left if side == "L" else right
        own_cross = left_cross_sums if side == "L" else right_cross_sums
        fresh = leg_index == len(own)
        if fresh:
            own.append(set())
        own[leg_index].add(value)
        new_high, new_differences, new_cross = pieces
        high_sums.update(new_high)
        small_differences.update(new_differences)
        own_cross.update(new_cross)
        return new_high, new_differences, new_cross, fresh

    def undo(side: str, leg_index: int, value: int, token) -> None:
        own = left if side == "L" else right
        own_cross = left_cross_sums if side == "L" else right_cross_sums
        new_high, new_differences, new_cross, fresh = token
        own[leg_index].remove(value)
        high_sums.difference_update(new_high)
        small_differences.difference_update(new_differences)
        own_cross.difference_update(new_cross)
        if fresh:
            if own[leg_index]:
                raise RuntimeError("fresh leg was not empty after undo")
            own.pop()

    def load_state(key) -> None:
        left.clear()
        left.extend(set(leg) for leg in key[0])
        right.clear()
        right.extend(set(leg) for leg in key[1])
        high_sums.clear()
        small_differences.clear()
        left_cross_sums.clear()
        right_cross_sums.clear()

        for a in all_offsets(left):
            for b in all_offsets(right):
                high_sums.add(a + b)
        for legs in (left, right):
            for leg in legs:
                seq = sorted(leg)
                for i, x in enumerate(seq):
                    for y in seq[i + 1 :]:
                        small_differences.add(y - x)
        for legs, cross in ((left, left_cross_sums), (right, right_cross_sums)):
            tagged = [(x, i) for i, leg in enumerate(legs) for x in leg]
            for j, (x, li) in enumerate(tagged):
                for y, lj in tagged[j + 1 :]:
                    if li != lj:
                        cross.add(x + y)

    def candidate_states(k: int):
        children = set()
        left_values = all_offsets(left)
        right_values = all_offsets(right)

        for a in tuple(left_values):
            b = k - a
            for ri in range(len(right) + 1):
                pieces = pieces_for("R", ri, b)
                if pieces is None:
                    continue
                token = apply("R", ri, b, pieces)
                children.add(state_key())
                undo("R", ri, b, token)

        for b in tuple(right_values):
            a = k - b
            for li in range(len(left) + 1):
                pieces = pieces_for("L", li, a)
                if pieces is None:
                    continue
                token = apply("L", li, a, pieces)
                children.add(state_key())
                undo("L", li, a, token)

        for a in range(1, k):
            b = k - a
            for li in range(len(left) + 1):
                left_pieces = pieces_for("L", li, a)
                if left_pieces is None:
                    continue
                left_token = apply("L", li, a, left_pieces)
                for ri in range(len(right) + 1):
                    right_pieces = pieces_for("R", ri, b)
                    if right_pieces is None:
                        continue
                    right_token = apply("R", ri, b, right_pieces)
                    children.add(state_key())
                    undo("R", ri, b, right_token)
                undo("L", li, a, left_token)
        return children

    stack: list[tuple] = []

    def dfs(k: int) -> None:
        stats.nodes += 1
        stats.max_marks = max(
            stats.max_marks,
            sum(map(len, left)) + sum(map(len, right)),
        )
        while k in high_sums:
            k += 1
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, k)
        if k > W:
            stats.frontier_states += 1
            return
        parent = state_key()
        children = candidate_states(k)
        if not children:
            stats.dead_states += 1
            return
        for child in children:
            stats.accepted_children += 1
            stack.append(parent)
            load_state(child)
            dfs(k + 1)
            load_state(stack.pop())

    dfs(1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", type=int, default=40)
    args = parser.parse_args()
    print(json.dumps(asdict(prove_regular_lr(args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
