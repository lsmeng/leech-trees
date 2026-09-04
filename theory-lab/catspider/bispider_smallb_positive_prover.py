#!/usr/bin/env python3
"""Incremental finite prover for the LR tail r>20, B<=20.

The top-window reduction and Q=81 stable-tail representative are described in
``bispider_smallb_positive_cleanroom.py``.  This implementation uses mutable
leg states and validates a new vertex only against the current distance set.
It imports no search code from the immutable full-recomputation checker.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


SideKey = tuple[tuple[int, ...], ...]
StateKey = tuple[SideKey, tuple[int, ...], SideKey]
Vertex = tuple[str, int, int]


@dataclass
class TailStats:
    A: int
    B: int
    Q: int
    W: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    frontier_states: int = 0
    invalid_initial: int = 0
    max_selected_vertices: int = 4


def prove_tail(A: int, B: int, Q: int, W: int = 20) -> TailStats:
    if not (1 <= A < B <= W and Q > 20 + B - A):
        raise ValueError((A, B, Q, W))
    stats = TailStats(A=A, B=B, Q=Q, W=W)
    N = A + Q + B
    left = [{0}]
    spine: set[int] = set()
    right = [{0}]
    distances: set[int] = set()

    def canon_side(side) -> SideKey:
        return (
            tuple(sorted(side[0])),
            *sorted(tuple(sorted(leg)) for leg in side[1:]),
        )

    def state_key() -> StateKey:
        return canon_side(left), tuple(sorted(spine)), canon_side(right)

    def vertices() -> tuple[Vertex, ...]:
        out: list[Vertex] = []
        for leg, offsets in enumerate(left):
            out.extend(("L", leg, A - a) for a in offsets)
        out.extend(("S", 0, s) for s in (0, *sorted(spine), Q))
        for leg, offsets in enumerate(right):
            out.extend(("R", leg, B - b) for b in offsets)
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

    def fresh_distances(vertex: Vertex):
        values = [metric(vertex, old) for old in vertices()]
        new = set(values)
        if any(value <= 0 for value in values):
            return None
        if len(new) != len(values) or new & distances:
            return None
        return new

    def rebuild(key: StateKey) -> None:
        left.clear()
        left.extend(set(leg) for leg in key[0])
        spine.clear()
        spine.update(key[1])
        right.clear()
        right.extend(set(leg) for leg in key[2])
        values = []
        chosen = vertices()
        for i, x in enumerate(chosen):
            values.extend(metric(x, y) for y in chosen[i + 1 :])
        if any(value <= 0 for value in values) or len(values) != len(set(values)):
            raise RuntimeError("invalid saved state")
        distances.clear()
        distances.update(values)

    def find(side, value: int):
        for leg, values in enumerate(side):
            if value in values:
                return leg
        return None

    def variants(side, value: int):
        existing = find(side, value)
        if existing is not None:
            return ((existing, False),)
        return tuple((leg, True) for leg in range(len(side) + 1))

    def add_left(a: int, option):
        leg, is_new = option
        if not is_new:
            return None
        vertex = ("L", leg, A - a)
        new_values = fresh_distances(vertex)
        if new_values is None:
            return False
        fresh_leg = leg == len(left)
        if fresh_leg:
            left.append(set())
        left[leg].add(a)
        distances.update(new_values)
        return new_values, fresh_leg

    def undo_left(a: int, option, token) -> None:
        if token is None:
            return
        new_values, fresh_leg = token
        leg, _ = option
        distances.difference_update(new_values)
        left[leg].remove(a)
        if fresh_leg:
            left.pop()

    def add_right(b: int, option):
        leg, is_new = option
        if not is_new:
            return None
        vertex = ("R", leg, B - b)
        new_values = fresh_distances(vertex)
        if new_values is None:
            return False
        fresh_leg = leg == len(right)
        if fresh_leg:
            right.append(set())
        right[leg].add(b)
        distances.update(new_values)
        return new_values, fresh_leg

    def undo_right(b: int, option, token) -> None:
        if token is None:
            return
        new_values, fresh_leg = token
        leg, _ = option
        distances.difference_update(new_values)
        right[leg].remove(b)
        if fresh_leg:
            right.pop()

    def add_spine(s: int):
        if s in spine or s in (0, Q):
            return None
        vertex = ("S", 0, s)
        new_values = fresh_distances(vertex)
        if new_values is None:
            return False
        spine.add(s)
        distances.update(new_values)
        return new_values

    def undo_spine(s: int, token) -> None:
        if token is None:
            return
        distances.difference_update(token)
        spine.remove(s)

    initial = state_key()
    try:
        rebuild(initial)
    except RuntimeError:
        stats.invalid_initial = 1
        return stats

    def candidate_states(k: int) -> set[StateKey]:
        out: set[StateKey] = set()

        def emit_lr(a: int, b: int) -> None:
            for left_option in variants(left, a):
                left_token = add_left(a, left_option)
                if left_token is False:
                    continue
                for right_option in variants(right, b):
                    right_token = add_right(b, right_option)
                    if right_token is False:
                        continue
                    if left_token is not None or right_token is not None:
                        out.add(state_key())
                    undo_right(b, right_option, right_token)
                undo_left(a, left_option, left_token)

        def emit_left_spine(a: int, s: int) -> None:
            for left_option in variants(left, a):
                left_token = add_left(a, left_option)
                if left_token is False:
                    continue
                spine_token = add_spine(s)
                if spine_token is not False:
                    if left_token is not None or spine_token is not None:
                        out.add(state_key())
                    undo_spine(s, spine_token)
                undo_left(a, left_option, left_token)

        def emit_spine_right(s: int, b: int) -> None:
            spine_token = add_spine(s)
            if spine_token is False:
                return
            for right_option in variants(right, b):
                right_token = add_right(b, right_option)
                if right_token is False:
                    continue
                if spine_token is not None or right_token is not None:
                    out.add(state_key())
                undo_right(b, right_option, right_token)
            undo_spine(s, spine_token)

        for a in range(A):
            b = k - a
            if 0 <= b < B:
                emit_lr(a, b)

            t = k - B - a
            if 0 <= t <= W - B:
                emit_left_spine(a, Q - t)

        for b in range(B):
            s = k - A - b
            if 0 <= s <= W - A:
                emit_spine_right(s, b)

        legal_spine = {0, Q}
        legal_spine.update(range(1, min(Q, W - A) + 1))
        legal_spine.update(Q - t for t in range(1, min(Q, W - B) + 1))
        target = N - k
        ordered = sorted(legal_spine)
        for i, s in enumerate(ordered):
            for t in ordered[i + 1 :]:
                if t - s != target:
                    continue
                first = add_spine(s)
                if first is False:
                    continue
                second = add_spine(t)
                if second is not False:
                    if first is not None or second is not None:
                        out.add(state_key())
                    undo_spine(t, second)
                undo_spine(s, first)
        return out

    stack: list[StateKey] = []

    def dfs(k: int) -> None:
        stats.nodes += 1
        stats.max_selected_vertices = max(
            stats.max_selected_vertices,
            sum(len(leg) for leg in left) + len(spine)
            + sum(len(leg) for leg in right) + 2,
        )
        while N - k in distances:
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
    parser.add_argument("B", type=int)
    parser.add_argument("Q", type=int)
    parser.add_argument("--window", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(asdict(prove_tail(args.A, args.B, args.Q, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
