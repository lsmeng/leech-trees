#!/usr/bin/env python3
"""Incremental prover for the small-A, positive-r LR bi-spider tail.

For ``N=A+Q+B``, ``1<=A<=50``, ``B>W`` and
``r=Q-(B-A)>W``, every value ``N-k`` with ``k<=W`` has offset ``p+b``.
Here ``b`` is a deficit from a right-leg extent B, while p is a deficit from
the left anchor (p<A), the left centre (p=A), or a spine point (p>A).

The search retains only parameter-independent necessary collision classes and
omits the exact long parameters and vertex budget.  Hence it is a supertree of
every exact continuation in the stated region.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class PositiveStats:
    A: int
    W: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    max_selected_vertices: int = 3
    frontier_states: int = 0


def prove_positive_tail(A: int, W: int = 20) -> PositiveStats:
    if A < 1 or W < 1:
        raise ValueError("A and W must be positive")
    stats = PositiveStats(A=A, W=W)
    left = [{0}]
    spine = {A}
    right = [{0}]
    p_values = {0, A}
    right_values = {0}
    high_sums = {0, A}
    constants = {A}
    right_cross_sums: set[int] = set()

    def side_values(side):
        return {x for leg in side for x in leg}

    def find(side, value: int):
        for i, leg in enumerate(side):
            if value in leg:
                return i
        return None

    def state_key():
        def canon(side):
            return (
                tuple(sorted(side[0])),
                *sorted(tuple(sorted(leg)) for leg in side[1:]),
            )

        return canon(left), tuple(sorted(spine)), canon(right)

    def unique_new(items, existing) -> set[int] | None:
        values = list(items)
        new = set(values)
        if any(x <= 0 for x in values):
            return None
        if len(new) != len(values) or new & existing:
            return None
        return new

    def left_pieces(leg_index: int, a: int):
        if not (1 <= a < A) or a in p_values:
            return None
        new_high = unique_new((a + b for b in right_values), high_sums)
        if new_high is None:
            return None
        own = left[leg_index] if leg_index < len(left) else set()
        constant_items = [abs(a - old) for old in own]
        constant_items.extend(
            2 * A - a - old
            for i, leg in enumerate(left)
            if i != leg_index
            for old in leg
        )
        constant_items.extend(d - a for d in spine)
        new_constants = unique_new(constant_items, constants)
        if new_constants is None:
            return None
        return new_high, new_constants

    def spine_pieces(d: int):
        if not (A < d <= W) or d in p_values:
            return None
        new_high = unique_new((d + b for b in right_values), high_sums)
        if new_high is None:
            return None
        constant_items = [abs(d - old) for old in spine]
        constant_items.extend(d - a for a in side_values(left))
        new_constants = unique_new(constant_items, constants)
        if new_constants is None:
            return None
        return new_high, new_constants

    def right_pieces(leg_index: int, b: int):
        if not (1 <= b <= W) or b in right_values:
            return None
        new_high = unique_new((p + b for p in p_values), high_sums)
        if new_high is None:
            return None
        own = right[leg_index] if leg_index < len(right) else set()
        new_constants = unique_new((abs(b - old) for old in own), constants)
        if new_constants is None:
            return None
        cross_items = [
            b + old
            for i, leg in enumerate(right)
            if i != leg_index
            for old in leg
        ]
        new_cross = unique_new(cross_items, right_cross_sums)
        if new_cross is None:
            return None
        return new_high, new_constants, new_cross

    def apply_left(leg_index: int, a: int, pieces):
        fresh = leg_index == len(left)
        if fresh:
            left.append(set())
        left[leg_index].add(a)
        p_values.add(a)
        high_sums.update(pieces[0])
        constants.update(pieces[1])
        return (*pieces, fresh)

    def undo_left(leg_index: int, a: int, token) -> None:
        new_high, new_constants, fresh = token
        left[leg_index].remove(a)
        p_values.remove(a)
        high_sums.difference_update(new_high)
        constants.difference_update(new_constants)
        if fresh:
            left.pop()

    def apply_spine(d: int, pieces):
        spine.add(d)
        p_values.add(d)
        high_sums.update(pieces[0])
        constants.update(pieces[1])
        return pieces

    def undo_spine(d: int, token) -> None:
        spine.remove(d)
        p_values.remove(d)
        high_sums.difference_update(token[0])
        constants.difference_update(token[1])

    def apply_right(leg_index: int, b: int, pieces):
        fresh = leg_index == len(right)
        if fresh:
            right.append(set())
        right[leg_index].add(b)
        right_values.add(b)
        high_sums.update(pieces[0])
        constants.update(pieces[1])
        right_cross_sums.update(pieces[2])
        return (*pieces, fresh)

    def undo_right(leg_index: int, b: int, token) -> None:
        new_high, new_constants, new_cross, fresh = token
        right[leg_index].remove(b)
        right_values.remove(b)
        high_sums.difference_update(new_high)
        constants.difference_update(new_constants)
        right_cross_sums.difference_update(new_cross)
        if fresh:
            right.pop()

    def load_state(key) -> None:
        left.clear()
        left.extend(set(leg) for leg in key[0])
        spine.clear()
        spine.update(key[1])
        right.clear()
        right.extend(set(leg) for leg in key[2])
        p_values.clear()
        p_values.update(side_values(left) | spine)
        right_values.clear()
        right_values.update(side_values(right))
        high_sums.clear()
        high_sums.update(p + b for p in p_values for b in right_values)
        constants.clear()
        for leg in left:
            seq = sorted(leg)
            constants.update(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        tagged_left = [(x, i) for i, leg in enumerate(left) for x in leg]
        constants.update(
            2 * A - x - y
            for j, (x, li) in enumerate(tagged_left)
            for y, lj in tagged_left[j + 1 :]
            if li != lj
        )
        seq = sorted(spine)
        constants.update(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        constants.update(d - a for a in side_values(left) for d in spine)
        for leg in right:
            seq = sorted(leg)
            constants.update(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        right_cross_sums.clear()
        tagged_right = [(x, i) for i, leg in enumerate(right) for x in leg]
        right_cross_sums.update(
            x + y
            for j, (x, li) in enumerate(tagged_right)
            for y, lj in tagged_right[j + 1 :]
            if li != lj
        )

    def p_variants(p: int):
        if p in p_values:
            return ((None, None),)
        if 1 <= p < A:
            return tuple(("L", i) for i in range(len(left) + 1))
        if A < p <= W:
            return (("S", None),)
        return ()

    def candidates(target: int):
        out = set()
        for p in range(target + 1):
            b = target - p
            if b < 0 or b > W:
                continue
            for p_kind, p_leg in p_variants(p):
                p_token = None
                if p_kind == "L":
                    pieces = left_pieces(p_leg, p)
                    if pieces is None:
                        continue
                    p_token = apply_left(p_leg, p, pieces)
                elif p_kind == "S":
                    pieces = spine_pieces(p)
                    if pieces is None:
                        continue
                    p_token = apply_spine(p, pieces)

                existing_b = find(right, b)
                right_options = (
                    (existing_b,)
                    if existing_b is not None
                    else tuple(range(len(right) + 1))
                )
                for b_leg in right_options:
                    if existing_b is not None:
                        if p_token is not None:
                            out.add(state_key())
                        continue
                    pieces = right_pieces(b_leg, b)
                    if pieces is None:
                        continue
                    b_token = apply_right(b_leg, b, pieces)
                    out.add(state_key())
                    undo_right(b_leg, b, b_token)

                if p_kind == "L":
                    undo_left(p_leg, p, p_token)
                elif p_kind == "S":
                    undo_spine(p, p_token)
        return out

    stack = []

    def dfs(target: int) -> None:
        stats.nodes += 1
        stats.max_selected_vertices = max(
            stats.max_selected_vertices,
            len(p_values) + len(right_values),
        )
        while target in high_sums:
            target += 1
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, target)
        if target > W:
            stats.frontier_states += 1
            return
        parent = state_key()
        next_states = candidates(target)
        if not next_states:
            stats.dead_states += 1
            return
        for child in next_states:
            stats.accepted_children += 1
            stack.append(parent)
            load_state(child)
            dfs(target + 1)
            load_state(stack.pop())

    dfs(1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--A", type=int)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--window", type=int, default=20)
    args = parser.parse_args()
    if args.all:
        rows = [prove_positive_tail(A, args.window) for A in range(1, 51)]
        print(
            json.dumps(
                {
                    "W": args.window,
                    "regimes": len(rows),
                    "nodes": sum(row.nodes for row in rows),
                    "frontier_states": sum(row.frontier_states for row in rows),
                    "max_depth": max(row.deepest_missing_offset for row in rows),
                    "max_selected_vertices": max(
                        row.max_selected_vertices for row in rows
                    ),
                },
                sort_keys=True,
            )
        )
        for row in rows:
            print(json.dumps(asdict(row), sort_keys=True))
        return
    if args.A is None:
        parser.error("give --A, or use --all")
    print(json.dumps(asdict(prove_positive_tail(args.A, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
