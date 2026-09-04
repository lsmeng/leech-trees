#!/usr/bin/env python3
"""Incremental relaxation for the right-tip-dominant LR region.

For an LR anchor N=A+Q+B, put C=A+Q.  If A>W and B-C>W, the values
N-k, k<=W, must join the distinguished B-tip leg to either a left mark near A
or a mark on another right leg near C.  This program enforces only necessary,
parameter-independent collisions among the corresponding offsets.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class DominantStats:
    W: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    max_marks: int = 2
    frontier_states: int = 0


def prove_dominant_lr(W: int) -> DominantStats:
    if W < 1:
        raise ValueError("W must be positive")
    stats = DominantStats(W=W)
    top = {0}
    left = [{0}]
    right: list[set[int]] = []
    high_sums = {0}
    differences: set[int] = set()
    left_cross_sums: set[int] = set()
    common_cross_sums: set[int] = set()

    def lower_values():
        return {x for side in (left, right) for leg in side for x in leg}

    def side_values(side):
        return {x for leg in side for x in leg}

    def state_key():
        first_left = tuple(sorted(left[0]))
        other_left = tuple(sorted(tuple(sorted(leg)) for leg in left[1:]))
        canonical_right = tuple(sorted(tuple(sorted(leg)) for leg in right))
        return tuple(sorted(top)), (first_left, *other_left), canonical_right

    def top_pieces(a: int):
        if not (1 <= a <= W) or a in top:
            return None
        lower = lower_values()
        new_high = {a + b for b in lower}
        if len(new_high) != len(lower) or new_high & high_sums:
            return None
        new_differences = {abs(a - old) for old in top}
        if len(new_differences) != len(top) or new_differences & differences:
            return None
        return new_high, new_differences

    def lower_pieces(side_name: str, leg_index: int, b: int):
        side = left if side_name == "L" else right
        other_side = right if side_name == "L" else left
        if not (1 <= b <= W) or b in lower_values():
            return None
        new_high = {a + b for a in top}
        if len(new_high) != len(top) or new_high & high_sums:
            return None
        same_leg = side[leg_index] if leg_index < len(side) else set()
        new_differences = {abs(b - old) for old in same_leg}
        if len(new_differences) != len(same_leg) or new_differences & differences:
            return None

        new_left_cross: set[int] = set()
        if side_name == "L":
            other_left = {x for i, leg in enumerate(left) if i != leg_index for x in leg}
            new_left_cross = {b + x for x in other_left}
            if len(new_left_cross) != len(other_left) or new_left_cross & left_cross_sums:
                return None

        if side_name == "L":
            common_partners = side_values(other_side)
        else:
            common_partners = side_values(left) | {
                x for i, leg in enumerate(right) if i != leg_index for x in leg
            }
        new_common = {b + x for x in common_partners}
        if len(new_common) != len(common_partners) or new_common & common_cross_sums:
            return None
        return new_high, new_differences, new_left_cross, new_common

    def apply_top(a: int, pieces):
        new_high, new_differences = pieces
        top.add(a)
        high_sums.update(new_high)
        differences.update(new_differences)
        return pieces

    def undo_top(a: int, token) -> None:
        new_high, new_differences = token
        top.remove(a)
        high_sums.difference_update(new_high)
        differences.difference_update(new_differences)

    def apply_lower(side_name: str, leg_index: int, b: int, pieces):
        side = left if side_name == "L" else right
        fresh = leg_index == len(side)
        if fresh:
            side.append(set())
        side[leg_index].add(b)
        new_high, new_differences, new_left_cross, new_common = pieces
        high_sums.update(new_high)
        differences.update(new_differences)
        left_cross_sums.update(new_left_cross)
        common_cross_sums.update(new_common)
        return (*pieces, fresh)

    def undo_lower(side_name: str, leg_index: int, b: int, token) -> None:
        side = left if side_name == "L" else right
        new_high, new_differences, new_left_cross, new_common, fresh = token
        side[leg_index].remove(b)
        high_sums.difference_update(new_high)
        differences.difference_update(new_differences)
        left_cross_sums.difference_update(new_left_cross)
        common_cross_sums.difference_update(new_common)
        if fresh:
            if side[leg_index]:
                raise RuntimeError("fresh dominant-regime leg not empty after undo")
            side.pop()

    def load_state(key) -> None:
        top.clear()
        top.update(key[0])
        left.clear()
        left.extend(set(leg) for leg in key[1])
        right.clear()
        right.extend(set(leg) for leg in key[2])
        high_sums.clear()
        differences.clear()
        left_cross_sums.clear()
        common_cross_sums.clear()

        lower = lower_values()
        high_sums.update(a + b for a in top for b in lower)
        for leg in [top, *left, *right]:
            seq = sorted(leg)
            differences.update(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        tagged_left = [(x, i) for i, leg in enumerate(left) for x in leg]
        left_cross_sums.update(
            x + y
            for j, (x, li) in enumerate(tagged_left)
            for y, lj in tagged_left[j + 1 :]
            if li != lj
        )
        left_values = side_values(left)
        right_values = side_values(right)
        common_cross_sums.update(x + y for x in left_values for y in right_values)
        tagged_right = [(x, i) for i, leg in enumerate(right) for x in leg]
        common_cross_sums.update(
            x + y
            for j, (x, li) in enumerate(tagged_right)
            for y, lj in tagged_right[j + 1 :]
            if li != lj
        )

    def candidates(k: int):
        out = set()
        lower = lower_values()

        for a in tuple(top):
            b = k - a
            for side_name, side in (("L", left), ("R", right)):
                for li in range(len(side) + 1):
                    pieces = lower_pieces(side_name, li, b)
                    if pieces is None:
                        continue
                    token = apply_lower(side_name, li, b, pieces)
                    out.add(state_key())
                    undo_lower(side_name, li, b, token)

        for b in tuple(lower):
            a = k - b
            pieces = top_pieces(a)
            if pieces is None:
                continue
            token = apply_top(a, pieces)
            out.add(state_key())
            undo_top(a, token)

        for a in range(1, k):
            b = k - a
            top_piece = top_pieces(a)
            if top_piece is None:
                continue
            top_token = apply_top(a, top_piece)
            for side_name, side in (("L", left), ("R", right)):
                for li in range(len(side) + 1):
                    lower_piece = lower_pieces(side_name, li, b)
                    if lower_piece is None:
                        continue
                    lower_token = apply_lower(side_name, li, b, lower_piece)
                    out.add(state_key())
                    undo_lower(side_name, li, b, lower_token)
            undo_top(a, top_token)
        return out

    stack = []

    def dfs(k: int) -> None:
        stats.nodes += 1
        stats.max_marks = max(
            stats.max_marks,
            len(top) + sum(len(leg) for side in (left, right) for leg in side),
        )
        while k in high_sums:
            k += 1
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, k)
        if k > W:
            stats.frontier_states += 1
            return
        parent = state_key()
        next_states = candidates(k)
        if not next_states:
            stats.dead_states += 1
            return
        for child in next_states:
            stats.accepted_children += 1
            stack.append(parent)
            load_state(child)
            dfs(k + 1)
            load_state(stack.pop())

    dfs(1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", type=int, default=15)
    args = parser.parse_args()
    print(json.dumps(asdict(prove_dominant_lr(args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
