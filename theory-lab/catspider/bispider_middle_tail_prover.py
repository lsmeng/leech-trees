#!/usr/bin/env python3
"""Incremental prover for the large-h bounded-imbalance LR tail.

For fixed ``1<=A<=50`` and ``-15<=r<=20``, a sufficiently large
``h=N-2A`` removes the LL, right-boundary-spine and parameter-dependent
classes from a top window of width W.  The retained high offsets are

    p+b,                 r+b+b' (different right legs),

where p is a left-leg deficit, the left centre, or a short spine position.
This implementation maintains every retained collision class incrementally.
It imports no code from the immutable full-recomputation probe.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Tuple


SideKey = Tuple[Tuple[int, ...], ...]
StateKey = Tuple[SideKey, Tuple[int, ...], SideKey]


@dataclass
class TailStats:
    A: int
    r: int
    W: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    frontier_states: int = 0
    max_selected_vertices: int = 3


def prove_tail(A: int, r: int, W: int = 35) -> TailStats:
    if not (1 <= A <= 50 and -15 <= r <= 20 and W >= 1):
        raise ValueError((A, r, W))
    stats = TailStats(A=A, r=r, W=W)
    cap = W - min(r, 0)
    left = [{0}]
    spine = {A}
    right = [{0}]
    p_values = {0, A}
    right_values = {0}
    high_offsets = {0, A}
    constants = {A}
    right_sums: set[int] = set()

    def side_values(side):
        return {value for leg in side for value in leg}

    def canon_side(side) -> SideKey:
        return (
            tuple(sorted(side[0])),
            *sorted(tuple(sorted(leg)) for leg in side[1:]),
        )

    def state_key() -> StateKey:
        return canon_side(left), tuple(sorted(spine)), canon_side(right)

    def find(side, value: int):
        for leg, values in enumerate(side):
            if value in values:
                return leg
        return None

    def unique_new(items, existing, *, positive: bool):
        values = list(items)
        fresh = set(values)
        if positive and any(value <= 0 for value in values):
            return None
        if not positive and any(value < 0 for value in values):
            return None
        if len(fresh) != len(values) or fresh & existing:
            return None
        return fresh

    def left_pieces(leg: int, a: int):
        if not (0 <= a < A) or a in p_values:
            return None
        new_high = unique_new((a + b for b in right_values), high_offsets, positive=False)
        if new_high is None:
            return None
        own = left[leg] if leg < len(left) else set()
        constant_items = [abs(a - old) for old in own]
        constant_items.extend(
            2 * A - a - old
            for other_leg, values in enumerate(left)
            if other_leg != leg
            for old in values
        )
        constant_items.extend(p - a for p in spine)
        new_constants = unique_new(constant_items, constants, positive=True)
        if new_constants is None:
            return None
        return new_high, new_constants

    def spine_pieces(p: int):
        if not (A <= p <= W) or p in p_values:
            return None
        new_high = unique_new((p + b for b in right_values), high_offsets, positive=False)
        if new_high is None:
            return None
        constant_items = [abs(p - old) for old in spine]
        constant_items.extend(p - a for a in side_values(left))
        new_constants = unique_new(constant_items, constants, positive=True)
        if new_constants is None:
            return None
        return new_high, new_constants

    def right_pieces(leg: int, b: int):
        if not (0 <= b <= cap) or b in right_values:
            return None
        high_items = [p + b for p in p_values]
        high_items.extend(
            r + b + old
            for other_leg, values in enumerate(right)
            if other_leg != leg
            for old in values
        )
        new_high = unique_new(high_items, high_offsets, positive=False)
        if new_high is None:
            return None
        own = right[leg] if leg < len(right) else set()
        new_constants = unique_new(
            (abs(b - old) for old in own), constants, positive=True
        )
        if new_constants is None:
            return None
        new_sums = unique_new(
            (
                b + old
                for other_leg, values in enumerate(right)
                if other_leg != leg
                for old in values
            ),
            right_sums,
            positive=False,
        )
        if new_sums is None:
            return None
        return new_high, new_constants, new_sums

    def add_left(leg: int, a: int, pieces):
        fresh_leg = leg == len(left)
        if fresh_leg:
            left.append(set())
        left[leg].add(a)
        p_values.add(a)
        high_offsets.update(pieces[0])
        constants.update(pieces[1])
        return (*pieces, fresh_leg)

    def undo_left(leg: int, a: int, token) -> None:
        new_high, new_constants, fresh_leg = token
        high_offsets.difference_update(new_high)
        constants.difference_update(new_constants)
        p_values.remove(a)
        left[leg].remove(a)
        if fresh_leg:
            left.pop()

    def add_spine(p: int, pieces):
        spine.add(p)
        p_values.add(p)
        high_offsets.update(pieces[0])
        constants.update(pieces[1])
        return pieces

    def undo_spine(p: int, token) -> None:
        high_offsets.difference_update(token[0])
        constants.difference_update(token[1])
        p_values.remove(p)
        spine.remove(p)

    def add_right(leg: int, b: int, pieces):
        fresh_leg = leg == len(right)
        if fresh_leg:
            right.append(set())
        right[leg].add(b)
        right_values.add(b)
        high_offsets.update(pieces[0])
        constants.update(pieces[1])
        right_sums.update(pieces[2])
        return (*pieces, fresh_leg)

    def undo_right(leg: int, b: int, token) -> None:
        new_high, new_constants, new_sums, fresh_leg = token
        high_offsets.difference_update(new_high)
        constants.difference_update(new_constants)
        right_sums.difference_update(new_sums)
        right_values.remove(b)
        right[leg].remove(b)
        if fresh_leg:
            right.pop()

    def rebuild(key: StateKey) -> None:
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
        high_offsets.clear()
        high_offsets.update(p + b for p in p_values for b in right_values)
        tagged_right = [(b, leg) for leg, values in enumerate(right) for b in values]
        high_offsets.update(
            r + b + c
            for i, (b, bi) in enumerate(tagged_right)
            for c, ci in tagged_right[i + 1 :]
            if bi != ci
        )
        constants.clear()
        for leg in left:
            seq = sorted(leg)
            constants.update(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        tagged_left = [(a, leg) for leg, values in enumerate(left) for a in values]
        constants.update(
            2 * A - a - c
            for i, (a, ai) in enumerate(tagged_left)
            for c, ci in tagged_left[i + 1 :]
            if ai != ci
        )
        seq = sorted(spine)
        constants.update(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        constants.update(p - a for a in side_values(left) for p in spine)
        for leg in right:
            seq = sorted(leg)
            constants.update(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        right_sums.clear()
        right_sums.update(
            b + c
            for i, (b, bi) in enumerate(tagged_right)
            for c, ci in tagged_right[i + 1 :]
            if bi != ci
        )

    def add_p(kind: str, value: int):
        if value in p_values:
            return ((None, None, None),)
        if kind == "L":
            out = []
            for leg in range(len(left) + 1):
                pieces = left_pieces(leg, value)
                if pieces is not None:
                    out.append(("L", leg, pieces))
            return tuple(out)
        pieces = spine_pieces(value)
        return () if pieces is None else (("S", 0, pieces),)

    def candidate_states(target: int) -> set[StateKey]:
        out: set[StateKey] = set()
        for p in range(target + 1):
            b = target - p
            if b > cap:
                continue
            kinds = []
            if p < A:
                kinds.append("L")
            if A <= p <= W:
                kinds.append("S")
            for kind in kinds:
                for p_kind, p_leg, p_pieces in add_p(kind, p):
                    p_token = None
                    if p_kind == "L":
                        p_token = add_left(p_leg, p, p_pieces)
                    elif p_kind == "S":
                        p_token = add_spine(p, p_pieces)
                    old_b = find(right, b)
                    options = (old_b,) if old_b is not None else range(len(right) + 1)
                    for b_leg in options:
                        if old_b is not None:
                            if p_token is not None:
                                out.add(state_key())
                            continue
                        pieces = right_pieces(b_leg, b)
                        if pieces is None:
                            continue
                        b_token = add_right(b_leg, b, pieces)
                        out.add(state_key())
                        undo_right(b_leg, b, b_token)
                    if p_kind == "L":
                        undo_left(p_leg, p, p_token)
                    elif p_kind == "S":
                        undo_spine(p, p_token)

        total = target - r
        if total >= 0:
            for b in range(total + 1):
                c = total - b
                if b > cap or c > cap:
                    continue
                old_b = find(right, b)
                first_options = (old_b,) if old_b is not None else range(len(right) + 1)
                for b_leg in first_options:
                    b_token = None
                    if old_b is None:
                        pieces = right_pieces(b_leg, b)
                        if pieces is None:
                            continue
                        b_token = add_right(b_leg, b, pieces)
                    old_c = find(right, c)
                    second_options = (old_c,) if old_c is not None else range(len(right) + 1)
                    for c_leg in second_options:
                        if b_leg == c_leg:
                            continue
                        if old_c is not None:
                            if b_token is not None:
                                out.add(state_key())
                            continue
                        pieces = right_pieces(c_leg, c)
                        if pieces is None:
                            continue
                        c_token = add_right(c_leg, c, pieces)
                        out.add(state_key())
                        undo_right(c_leg, c, c_token)
                    if old_b is None:
                        undo_right(b_leg, b, b_token)
        return out

    seen: set[StateKey] = set()
    stack: list[StateKey] = []

    def dfs(target: int) -> None:
        key = state_key()
        if key in seen:
            return
        seen.add(key)
        stats.nodes += 1
        stats.max_selected_vertices = max(
            stats.max_selected_vertices, len(p_values) + len(right_values)
        )
        while target in high_offsets:
            target += 1
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, target)
        if target > W:
            stats.frontier_states += 1
            return
        parent = key
        children = candidate_states(target)
        if not children:
            stats.dead_states += 1
            return
        for child in children:
            stats.accepted_children += 1
            stack.append(parent)
            rebuild(child)
            dfs(target + 1)
            rebuild(stack.pop())

    dfs(1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("A", type=int)
    parser.add_argument("r", type=int)
    parser.add_argument("--window", type=int, default=35)
    args = parser.parse_args()
    print(json.dumps(asdict(prove_tail(args.A, args.r, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
