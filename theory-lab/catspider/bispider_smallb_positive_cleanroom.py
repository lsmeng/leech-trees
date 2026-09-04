#!/usr/bin/env python3
"""Immutable full-distance search for the LR tail r>20, B<=20.

For ``N=A+Q+B``, assume ``1<=A<B<=20`` and
``r=Q-(B-A)>20``.  With ``W=20``, an endpoint of a distance in the top
window must be a leg mark or a spine point within the two finite boundary
zones.  The search retains all pair distances among the selected boundary
vertices, but omits all other vertices and the vertex budget.  It is therefore
a relaxation of every exact continuation.

For ``Q>80`` the two boundary clusters are separated: every internal distance
is at most 40, while every cross-cluster distance is ``Q+c`` and exceeds 40.
Thus collision relations in the tail are independent of Q; Q=81 represents
the entire tail.  Smaller admissible Q values are checked individually.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass


Side = tuple[tuple[int, ...], ...]
State = tuple[Side, tuple[int, ...], Side]


@dataclass
class Stats:
    A: int
    B: int
    Q: int
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


def selected_vertices(state: State, A: int, B: int, Q: int):
    left, spine, right = state
    out = []
    for leg, offsets in enumerate(left):
        out.extend(("L", leg, A - a) for a in offsets)
    out.extend(("S", 0, s) for s in (0, *spine, Q))
    for leg, offsets in enumerate(right):
        out.extend(("R", leg, B - b) for b in offsets)
    return tuple(out)


def distance(x, y, Q: int) -> int:
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


def distance_values(state: State, A: int, B: int, Q: int):
    vertices = selected_vertices(state, A, B, Q)
    values = []
    for i, x in enumerate(vertices):
        values.extend(distance(x, y, Q) for y in vertices[i + 1 :])
    if any(v <= 0 for v in values) or len(values) != len(set(values)):
        return None
    return frozenset(values)


def side_options(side: Side, cap: int):
    positions = {a: leg for leg, values in enumerate(side) for a in values}
    out = []
    for a in range(cap):
        if a in positions:
            out.append((a, positions[a], False))
        else:
            out.extend((a, leg, True) for leg in range(len(side) + 1))
    return tuple(out)


def add_side(side: Side, option) -> Side:
    value, leg, is_new = option
    if not is_new:
        return side
    out = [list(values) for values in side]
    if leg == len(out):
        out.append([value])
    else:
        out[leg].append(value)
    return tuple(tuple(values) for values in out)


def spine_options(spine: tuple[int, ...], A: int, B: int, Q: int, W: int):
    legal = {0, Q}
    legal.update(range(1, min(Q, W - A) + 1))
    legal.update(Q - t for t in range(1, min(Q, W - B) + 1))
    present = {0, *spine, Q}
    return tuple((s, s not in present) for s in sorted(legal))


def option_vertex(kind: str, option, A: int, B: int):
    value, leg, _ = option
    if kind == "L":
        return (kind, leg, A - value)
    if kind == "R":
        return (kind, leg, B - value)
    raise RuntimeError(kind)


def children(state: State, target: int, A: int, B: int, Q: int, W: int):
    left, spine, right = state
    left_opts = side_options(left, A)
    right_opts = side_options(right, B)
    spine_opts = spine_options(spine, A, B, Q, W)
    out = set()

    def retain(new_left, new_spine, new_right, changed):
        if not changed:
            return
        child = canonical(new_left, new_spine, new_right)
        if distance_values(child, A, B, Q) is not None:
            out.add(child)

    for lo in left_opts:
        lv = option_vertex("L", lo, A, B)
        for ro in right_opts:
            rv = option_vertex("R", ro, A, B)
            if distance(lv, rv, Q) == target:
                retain(
                    add_side(left, lo),
                    spine,
                    add_side(right, ro),
                    lo[2] or ro[2],
                )

    for lo in left_opts:
        lv = option_vertex("L", lo, A, B)
        for s, s_new in spine_opts:
            if distance(lv, ("S", 0, s), Q) == target:
                retain(
                    add_side(left, lo),
                    (*spine, s) if s_new else spine,
                    right,
                    lo[2] or s_new,
                )

    for s, s_new in spine_opts:
        sv = ("S", 0, s)
        for ro in right_opts:
            rv = option_vertex("R", ro, A, B)
            if distance(sv, rv, Q) == target:
                retain(
                    left,
                    (*spine, s) if s_new else spine,
                    add_side(right, ro),
                    s_new or ro[2],
                )

    for i, (s, s_new) in enumerate(spine_opts):
        for t, t_new in spine_opts[i + 1 :]:
            if t - s == target:
                additions = tuple(x for x, fresh in ((s, s_new), (t, t_new)) if fresh)
                retain(left, (*spine, *additions), right, bool(additions))

    return tuple(sorted(out))


def search(A: int, B: int, Q: int, W: int = 20) -> Stats:
    if not (1 <= A < B <= W and Q > 20 + B - A):
        raise ValueError((A, B, Q, W))
    stats = Stats(A=A, B=B, Q=Q, W=W)
    N = A + Q + B
    initial = canonical(((0,),), (), ((0,),))
    initial_values = distance_values(initial, A, B, Q)
    if initial_values is None:
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
        values = distance_values(state, A, B, Q)
        if values is None:
            raise RuntimeError("invalid state reached")
        while N - k in values:
            k += 1
        stats.deepest = max(stats.deepest, k)
        if k > W:
            stats.frontier += 1
            return
        next_states = children(state, N - k, A, B, Q, W)
        if not next_states:
            stats.dead += 1
            return
        for child in next_states:
            stats.children += 1
            dfs(child, k + 1)

    dfs(initial, 1)
    return stats


def run_regime(regime) -> Stats:
    return search(*regime)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("A", type=int, nargs="?")
    parser.add_argument("B", type=int, nargs="?")
    parser.add_argument("Q", type=int, nargs="?")
    parser.add_argument("--window", type=int, default=20)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if args.all:
        regimes = [
            (A, B, Q, args.window)
            for A in range(1, 20)
            for B in range(A + 1, 21)
            for Q in (*range(21 + B - A, 81), 81)
        ]
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            rows = list(executor.map(run_regime, regimes, chunksize=10))
        print(
            json.dumps(
                {
                    "regimes": len(rows),
                    "nodes": sum(row.nodes for row in rows),
                    "children": sum(row.children for row in rows),
                    "dead": sum(row.dead for row in rows),
                    "frontier": sum(row.frontier for row in rows),
                    "invalid_initial": sum(row.invalid_initial for row in rows),
                    "max_depth": max(row.deepest for row in rows),
                    "max_vertices": max(row.max_vertices for row in rows),
                    "memo_hits": sum(row.memo_hits for row in rows),
                },
                sort_keys=True,
            )
        )
        return
    if None in (args.A, args.B, args.Q):
        parser.error("give A B Q, or use --all")
    print(json.dumps(asdict(search(args.A, args.B, args.Q, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
