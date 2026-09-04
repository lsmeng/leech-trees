#!/usr/bin/env python3
"""Immutable full-recomputation search for r<-15 and A<=15.

Put ``C=A+Q`` and ``d=B-C=-r>15``.  A top-window pair with deficit at most
15 has one endpoint within 15 of the distinguished B-tip.  The other endpoint
is a left mark, a spine point, another right leg, or (when C<=15) a mark near
the centre on the distinguished leg.  All other pair distances are below the
window.

The retained relaxation has two independently unique collision classes:
offsets of pairs incident with the B-tip cluster, and actual distances internal
to the complementary cluster (plus differences inside the tip cluster).
Parameter-dependent collisions between these classes are omitted.  B=C+16
therefore represents every d>15.  Exact C values through 45 are checked; for
C>45, coefficient-0 distances are at most 30, coefficient-1 distances are at
least C-15, and the coefficient-2 class is separated as well.  Thus C=46
represents the stable tail.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


Side = tuple[tuple[int, ...], ...]
State = tuple[Side, tuple[int, ...], Side]
Vertex = tuple[str, int, int]


@dataclass
class Stats:
    A: int
    C: int
    W: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    frontier: int = 0
    memo_hits: int = 0
    invalid_initial: int = 0
    max_vertices: int = 4


def canon_side(side) -> Side:
    return (tuple(sorted(side[0])), *sorted(tuple(sorted(x)) for x in side[1:]))


def canonical(left, spine, right) -> State:
    return canon_side(left), tuple(sorted(spine)), canon_side(right)


def parameters(A: int, C: int):
    Q = C - A
    B = C + 16
    N = B + C
    return B, Q, N


def chosen_vertices(state: State, A: int, C: int):
    left, spine, right = state
    _, Q, _ = parameters(A, C)
    out: list[Vertex] = []
    for leg, depths in enumerate(left):
        out.extend(("L", leg, depth) for depth in depths)
    out.extend(("S", 0, s) for s in (0, *spine, Q))
    for leg, depths in enumerate(right):
        out.extend(("R", leg, depth) for depth in depths)
    return tuple(out)


def distance(x: Vertex, y: Vertex, Q: int) -> int:
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


def collision_classes(state: State, A: int, C: int):
    B, Q, N = parameters(A, C)
    selected = chosen_vertices(state, A, C)
    offsets: list[int] = []
    internal: list[int] = []

    def near_tip(vertex: Vertex) -> bool:
        return vertex[0] == "R" and vertex[1] == 0 and vertex[2] >= B - 15

    for i, x in enumerate(selected):
        for y in selected[i + 1 :]:
            value = distance(x, y, Q)
            x_tip = near_tip(x)
            y_tip = near_tip(y)
            if x_tip ^ y_tip:
                offsets.append(N - value)
            else:
                internal.append(value)
    if any(value < 0 for value in offsets):
        return None
    if any(value <= 0 for value in internal):
        return None
    if len(offsets) != len(set(offsets)):
        return None
    if len(internal) != len(set(internal)):
        return None
    return frozenset(offsets), frozenset(internal)


def options_for_depth(side: Side, depth: int, first_leg_only: bool = False):
    found = [(leg, False) for leg, values in enumerate(side) if depth in values]
    if found:
        return tuple(found)
    if first_leg_only:
        return ((0, True),)
    return tuple((leg, True) for leg in range(len(side) + 1))


def add_side(side: Side, depth: int, option) -> Side:
    leg, is_new = option
    if not is_new:
        return side
    out = [list(values) for values in side]
    if leg == len(out):
        out.append([depth])
    else:
        out[leg].append(depth)
    return tuple(tuple(values) for values in out)


def endpoint_options(state: State, A: int, C: int, W: int):
    left, spine, right = state
    B, Q, _ = parameters(A, C)
    out = []

    for a in range(A):
        depth = A - a
        for leg, fresh in options_for_depth(left, depth):
            out.append(("L", leg, depth, fresh))

    legal_spine = {0, Q}
    legal_spine.update(range(1, min(Q, W - A) + 1))
    present_spine = {0, *spine, Q}
    out.extend(("S", 0, s, s not in present_spine) for s in sorted(legal_spine))

    long_depths = {B - x for x in range(W + 1)}
    long_depths.update(range(1, max(1, W - C + 1)))
    for depth in sorted(long_depths):
        fresh = depth not in right[0]
        out.append(("R", 0, depth, fresh))

    other_depths = {C - p for p in range(1, min(W, C - 1) + 1)}
    for depth in sorted(other_depths):
        found = [leg for leg in range(1, len(right)) if depth in right[leg]]
        if found:
            out.extend(("R", leg, depth, False) for leg in found)
        else:
            out.extend(
                ("R", leg, depth, True) for leg in range(1, len(right) + 1)
            )
    return tuple(out)


def option_vertex(option) -> Vertex:
    kind, leg, depth, _ = option
    return kind, leg, depth


def apply_option(state: State, option) -> State:
    left, spine, right = state
    kind, leg, value, fresh = option
    if not fresh:
        return state
    if kind == "L":
        left = add_side(left, value, (leg, True))
    elif kind == "R":
        right = add_side(right, value, (leg, True))
    elif kind == "S":
        spine = (*spine, value)
    else:
        raise RuntimeError(kind)
    return canonical(left, spine, right)


def children(state: State, target: int, A: int, C: int, W: int):
    _, Q, _ = parameters(A, C)
    options = endpoint_options(state, A, C, W)
    out = set()
    for i, first in enumerate(options):
        x = option_vertex(first)
        for second in options[i + 1 :]:
            y = option_vertex(second)
            if x == y or distance(x, y, Q) != target:
                continue
            child = apply_option(state, first)
            child = apply_option(child, second)
            if child == state:
                continue
            if collision_classes(child, A, C) is not None:
                out.add(child)
    return tuple(sorted(out))


def search(A: int, C: int, W: int = 15) -> Stats:
    if not (1 <= A <= W and C >= A + 1):
        raise ValueError((A, C, W))
    stats = Stats(A=A, C=C, W=W)
    B, _, N = parameters(A, C)
    initial = canonical(((A,),), (), ((B,),))
    if collision_classes(initial, A, C) is None:
        stats.invalid_initial = 1
        return stats
    seen = set()

    def dfs(state: State, k: int) -> None:
        if state in seen:
            stats.memo_hits += 1
            return
        seen.add(state)
        stats.nodes += 1
        stats.max_vertices = max(
            stats.max_vertices,
            sum(len(leg) for leg in state[0]) + len(state[1])
            + sum(len(leg) for leg in state[2]) + 2,
        )
        classes = collision_classes(state, A, C)
        if classes is None:
            raise RuntimeError("invalid state reached")
        offsets, _ = classes
        while k in offsets:
            k += 1
        stats.deepest = max(stats.deepest, k)
        if k > W:
            stats.frontier += 1
            return
        next_states = children(state, N - k, A, C, W)
        if not next_states:
            stats.dead += 1
            return
        for child in next_states:
            stats.children += 1
            dfs(child, k + 1)

    dfs(initial, 1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("A", type=int)
    parser.add_argument("C", type=int)
    parser.add_argument("--window", type=int, default=15)
    args = parser.parse_args()
    print(json.dumps(asdict(search(args.A, args.C, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
