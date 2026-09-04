#!/usr/bin/env python3
"""Incremental finite prover for the LR tail r<-15 and A<=15.

This independently implements the collision-class relaxation documented in
``bispider_smalla_negative_cleanroom.py``.  New vertices are checked only
against the mutable retained offset and internal-distance sets.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


SideKey = tuple[tuple[int, ...], ...]
StateKey = tuple[SideKey, tuple[int, ...], SideKey]
Vertex = tuple[str, int, int]


@dataclass
class NegativeStats:
    A: int
    C: int
    W: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    frontier_states: int = 0
    invalid_initial: int = 0
    max_selected_vertices: int = 4


def prove_negative_tail(A: int, C: int, W: int = 15) -> NegativeStats:
    if not (1 <= A <= W and C >= A + 1):
        raise ValueError((A, C, W))
    stats = NegativeStats(A=A, C=C, W=W)
    Q = C - A
    B = C + 16
    N = B + C
    left = [{A}]
    spine: set[int] = set()
    right = [{B}]
    offsets: set[int] = set()
    internal: set[int] = set()

    def canon_side(side) -> SideKey:
        return (
            tuple(sorted(side[0])),
            *sorted(tuple(sorted(leg)) for leg in side[1:]),
        )

    def state_key() -> StateKey:
        return canon_side(left), tuple(sorted(spine)), canon_side(right)

    def vertices() -> tuple[Vertex, ...]:
        out: list[Vertex] = []
        for leg, depths in enumerate(left):
            out.extend(("L", leg, depth) for depth in depths)
        out.extend(("S", 0, s) for s in (0, *sorted(spine), Q))
        for leg, depths in enumerate(right):
            out.extend(("R", leg, depth) for depth in depths)
        return tuple(out)

    def metric(x: Vertex, y: Vertex) -> int:
        tx, lx, vx = x
        ty, ly, vy = y
        if tx == ty == "L":
            return abs(vx - vy) if lx == ly else vx + vy
        if tx == ty == "R":
            return abs(vx - vy) if lx == ly else vx + vy
        if tx == ty == "S":
            return abs(vx - vy)
        if tx == "L" and ty == "S":
            return vx + vy
        if tx == "S" and ty == "L":
            return vy + vx
        if tx == "S" and ty == "R":
            return Q - vx + vy
        if tx == "R" and ty == "S":
            return Q - vy + vx
        if tx == "L" and ty == "R":
            return vx + Q + vy
        if tx == "R" and ty == "L":
            return vy + Q + vx
        raise RuntimeError((x, y))

    def near_tip(vertex: Vertex) -> bool:
        return vertex[0] == "R" and vertex[1] == 0 and vertex[2] >= B - W

    def fresh_classes(vertex: Vertex):
        new_offsets = []
        new_internal = []
        vertex_tip = near_tip(vertex)
        for old in vertices():
            value = metric(vertex, old)
            if vertex_tip ^ near_tip(old):
                new_offsets.append(N - value)
            else:
                new_internal.append(value)
        offset_set = set(new_offsets)
        internal_set = set(new_internal)
        if any(value < 0 for value in new_offsets):
            return None
        if any(value <= 0 for value in new_internal):
            return None
        if len(offset_set) != len(new_offsets) or offset_set & offsets:
            return None
        if len(internal_set) != len(new_internal) or internal_set & internal:
            return None
        return offset_set, internal_set

    def rebuild(key: StateKey) -> None:
        left.clear()
        left.extend(set(leg) for leg in key[0])
        spine.clear()
        spine.update(key[1])
        right.clear()
        right.extend(set(leg) for leg in key[2])
        offset_values = []
        internal_values = []
        selected = vertices()
        for i, x in enumerate(selected):
            for y in selected[i + 1 :]:
                value = metric(x, y)
                if near_tip(x) ^ near_tip(y):
                    offset_values.append(N - value)
                else:
                    internal_values.append(value)
        if any(value < 0 for value in offset_values):
            raise RuntimeError("negative offset in saved state")
        if any(value <= 0 for value in internal_values):
            raise RuntimeError("nonpositive internal distance in saved state")
        if len(offset_values) != len(set(offset_values)):
            raise RuntimeError("offset collision in saved state")
        if len(internal_values) != len(set(internal_values)):
            raise RuntimeError("internal collision in saved state")
        offsets.clear()
        offsets.update(offset_values)
        internal.clear()
        internal.update(internal_values)

    def find(side, value: int, first: int = 0):
        for leg in range(first, len(side)):
            if value in side[leg]:
                return leg
        return None

    def variants(side, value: int, first: int = 0):
        existing = find(side, value, first)
        if existing is not None:
            return ((existing, False),)
        return tuple((leg, True) for leg in range(first, len(side) + 1))

    def add_left(depth: int, option):
        leg, is_new = option
        if not is_new:
            return None
        new_classes = fresh_classes(("L", leg, depth))
        if new_classes is None:
            return False
        fresh_leg = leg == len(left)
        if fresh_leg:
            left.append(set())
        left[leg].add(depth)
        offsets.update(new_classes[0])
        internal.update(new_classes[1])
        return new_classes, fresh_leg

    def undo_left(depth: int, option, token) -> None:
        if token is None:
            return
        new_classes, fresh_leg = token
        leg, _ = option
        offsets.difference_update(new_classes[0])
        internal.difference_update(new_classes[1])
        left[leg].remove(depth)
        if fresh_leg:
            left.pop()

    def add_right(depth: int, option):
        leg, is_new = option
        if not is_new:
            return None
        new_classes = fresh_classes(("R", leg, depth))
        if new_classes is None:
            return False
        fresh_leg = leg == len(right)
        if fresh_leg:
            right.append(set())
        right[leg].add(depth)
        offsets.update(new_classes[0])
        internal.update(new_classes[1])
        return new_classes, fresh_leg

    def undo_right(depth: int, option, token) -> None:
        if token is None:
            return
        new_classes, fresh_leg = token
        leg, _ = option
        offsets.difference_update(new_classes[0])
        internal.difference_update(new_classes[1])
        right[leg].remove(depth)
        if fresh_leg:
            right.pop()

    def add_spine(s: int):
        if s in spine or s in (0, Q):
            return None
        new_classes = fresh_classes(("S", 0, s))
        if new_classes is None:
            return False
        spine.add(s)
        offsets.update(new_classes[0])
        internal.update(new_classes[1])
        return new_classes

    def undo_spine(s: int, token) -> None:
        if token is None:
            return
        offsets.difference_update(token[0])
        internal.difference_update(token[1])
        spine.remove(s)

    initial = state_key()
    try:
        rebuild(initial)
    except RuntimeError:
        stats.invalid_initial = 1
        return stats

    def candidate_states(k: int) -> set[StateKey]:
        out: set[StateKey] = set()

        def with_long(x: int, add_other, undo_other) -> None:
            long_depth = B - x
            long_option = (0, long_depth not in right[0])
            long_token = add_right(long_depth, long_option)
            if long_token is False:
                return
            other_token = add_other()
            if other_token is not False:
                if long_token is not None or other_token is not None:
                    out.add(state_key())
                undo_other(other_token)
            undo_right(long_depth, long_option, long_token)

        for x in range(W + 1):
            p = k - x
            if 0 <= p < A:
                depth = A - p
                for option in variants(left, depth):
                    with_long(
                        x,
                        lambda depth=depth, option=option: add_left(depth, option),
                        lambda token, depth=depth, option=option: undo_left(
                            depth, option, token
                        ),
                    )

            if A <= p <= C:
                s = p - A
                if s <= W - A or s == Q:
                    with_long(
                        x,
                        lambda s=s: add_spine(s),
                        lambda token, s=s: undo_spine(s, token),
                    )

            if 1 <= p < C:
                depth = C - p
                for option in variants(right, depth, first=1):
                    with_long(
                        x,
                        lambda depth=depth, option=option: add_right(depth, option),
                        lambda token, depth=depth, option=option: undo_right(
                            depth, option, token
                        ),
                    )

            y = k - C - x
            if 1 <= y <= W - C:
                option = (0, y not in right[0])
                with_long(
                    x,
                    lambda y=y, option=option: add_right(y, option),
                    lambda token, y=y, option=option: undo_right(y, option, token),
                )
        return out

    stack: list[StateKey] = []

    def dfs(k: int) -> None:
        stats.nodes += 1
        stats.max_selected_vertices = max(
            stats.max_selected_vertices,
            sum(len(leg) for leg in left) + len(spine)
            + sum(len(leg) for leg in right) + 2,
        )
        while k in offsets:
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
            rebuild(child)
            dfs(k + 1)
            rebuild(stack.pop())

    dfs(1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("A", type=int)
    parser.add_argument("C", type=int)
    parser.add_argument("--window", type=int, default=15)
    args = parser.parse_args()
    print(
        json.dumps(
            asdict(prove_negative_tail(args.A, args.C, args.window)),
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
