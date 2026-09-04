#!/usr/bin/env python3
"""Incremental offset prover for bounded-imbalance LR bi-spider anchors."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class StripStats:
    W: int
    r: int
    h: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    max_marks: int = 2
    frontier_states: int = 0


def admissible_h_values(W: int, r: int) -> tuple[int, ...]:
    q_min = max(1, r + 1)
    h_min = 2 * q_min - r
    max_offset = W - min(r, 0)
    critical = max(W, 2 * max_offset + abs(r))
    values = list(range(h_min, critical + 1, 2))
    tail = max(critical + 1, h_min)
    if (tail + r) % 2:
        tail += 1
    return tuple(values + [tail])


def prove_strip(W: int, r: int, h: int) -> StripStats:
    if W < 1 or h < 1 or (h + r) % 2 or h + r < 2:
        raise ValueError("invalid W,r,h")
    stats = StripStats(W=W, r=r, h=h)
    Q = (h + r) // 2
    mark_cap = W - min(r, 0)
    left = [{0}]
    right = [{0}]
    high_offsets = {0}
    differences: set[int] = set()

    def values(side):
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
        return canon(left), canon(right)

    def pieces_for(side_name: str, leg_index: int, value: int):
        own = left if side_name == "L" else right
        other = right if side_name == "L" else left
        if not (1 <= value <= mark_cap) or value in values(own):
            return None
        other_values = values(other)
        if side_name == "L":
            if any(value - b == r or b - value == h for b in other_values):
                return None
        else:
            if any(a - value == r or value - a == h for a in other_values):
                return None

        same_leg = own[leg_index] if leg_index < len(own) else set()
        new_differences = {abs(value - old) for old in same_leg}
        if (
            len(new_differences) != len(same_leg)
            or new_differences & differences
            or Q in new_differences
        ):
            return None

        new_high = []
        if side_name == "L":
            new_high.extend(value + b for b in other_values)
            new_high.extend(
                h + value + old
                for i, leg in enumerate(left)
                if i != leg_index
                for old in leg
            )
        else:
            new_high.extend(a + value for a in other_values)
            new_high.extend(
                r + value + old
                for i, leg in enumerate(right)
                if i != leg_index
                for old in leg
            )
        if any(x < 0 for x in new_high):
            return None
        if len(new_high) != len(set(new_high)) or set(new_high) & high_offsets:
            return None
        return set(new_high), new_differences

    def apply(side_name: str, leg_index: int, value: int, pieces):
        side = left if side_name == "L" else right
        fresh = leg_index == len(side)
        if fresh:
            side.append(set())
        side[leg_index].add(value)
        new_high, new_differences = pieces
        high_offsets.update(new_high)
        differences.update(new_differences)
        return new_high, new_differences, fresh

    def undo(side_name: str, leg_index: int, value: int, token) -> None:
        side = left if side_name == "L" else right
        new_high, new_differences, fresh = token
        side[leg_index].remove(value)
        high_offsets.difference_update(new_high)
        differences.difference_update(new_differences)
        if fresh:
            if side[leg_index]:
                raise RuntimeError("fresh strip leg was not empty after undo")
            side.pop()

    def load_state(key) -> None:
        left.clear()
        left.extend(set(leg) for leg in key[0])
        right.clear()
        right.extend(set(leg) for leg in key[1])
        high_offsets.clear()
        differences.clear()
        L = values(left)
        R = values(right)
        high_offsets.update(a + b for a in L for b in R)
        for shift, side in ((h, left), (r, right)):
            tagged = [(x, i) for i, leg in enumerate(side) for x in leg]
            high_offsets.update(
                shift + x + y
                for j, (x, li) in enumerate(tagged)
                for y, lj in tagged[j + 1 :]
                if li != lj
            )
        for side in (left, right):
            for leg in side:
                seq = sorted(leg)
                differences.update(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])

    def pair_children(
        side_1: str,
        value_1: int,
        side_2: str,
        value_2: int,
        different_legs: bool,
    ):
        out = set()
        first_side = left if side_1 == "L" else right
        existing_1 = find(first_side, value_1)

        def with_second(leg_1, added_1, token_1):
            second_side = left if side_2 == "L" else right
            existing_2 = find(second_side, value_2)
            options_2 = [existing_2] if existing_2 is not None else range(len(second_side) + 1)
            for leg_2 in options_2:
                if different_legs and side_1 == side_2 and leg_1 == leg_2:
                    continue
                if existing_2 is not None:
                    if added_1:
                        out.add(state_key())
                    continue
                pieces_2 = pieces_for(side_2, leg_2, value_2)
                if pieces_2 is None:
                    continue
                token_2 = apply(side_2, leg_2, value_2, pieces_2)
                out.add(state_key())
                undo(side_2, leg_2, value_2, token_2)

        if existing_1 is not None:
            with_second(existing_1, False, None)
        else:
            for leg_1 in range(len(first_side) + 1):
                pieces_1 = pieces_for(side_1, leg_1, value_1)
                if pieces_1 is None:
                    continue
                token_1 = apply(side_1, leg_1, value_1, pieces_1)
                with_second(leg_1, True, token_1)
                undo(side_1, leg_1, value_1, token_1)
        return out

    def candidates(target: int):
        out = set()
        for a in range(target + 1):
            out.update(pair_children("L", a, "R", target - a, False))
        rr_sum = target - r
        if rr_sum >= 0:
            for b in range(rr_sum + 1):
                out.update(pair_children("R", b, "R", rr_sum - b, True))
        ll_sum = target - h
        if ll_sum >= 0:
            for a in range(ll_sum + 1):
                out.update(pair_children("L", a, "L", ll_sum - a, True))
        return out

    # r=0 makes the two anchor tips equidistant from cR.
    if r == 0:
        stats.dead_states = 1
        return stats

    stack = []

    def dfs(target: int) -> None:
        stats.nodes += 1
        stats.max_marks = max(stats.max_marks, len(values(left)) + len(values(right)))
        while target in high_offsets:
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
    parser.add_argument("--window", type=int, default=50)
    parser.add_argument("--r", type=int)
    parser.add_argument("--h", type=int)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--r-lo", type=int, default=-15)
    parser.add_argument("--r-hi", type=int, default=20)
    args = parser.parse_args()
    if args.all:
        rows = [
            prove_strip(args.window, r, h)
            for r in range(args.r_lo, args.r_hi + 1)
            for h in admissible_h_values(args.window, r)
        ]
        print(
            json.dumps(
                {
                    "W": args.window,
                    "regimes": len(rows),
                    "nodes": sum(row.nodes for row in rows),
                    "frontier_states": sum(row.frontier_states for row in rows),
                    "max_depth": max(row.deepest_missing_offset for row in rows),
                    "max_marks": max(row.max_marks for row in rows),
                },
                sort_keys=True,
            )
        )
        for row in rows:
            print(json.dumps(asdict(row), sort_keys=True))
        return
    if args.r is None or args.h is None:
        parser.error("provide --r and --h, or use --all")
    print(json.dumps(asdict(prove_strip(args.window, args.r, args.h)), sort_keys=True))


if __name__ == "__main__":
    main()
