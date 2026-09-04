#!/usr/bin/env python3
"""Immutable clean-room search for the small-A, positive-r LR tail.

For an LR anchor ``N=A+Q+B`` put ``r=Q-(B-A)=N-2B``.  Assume

    1 <= A <= 50,   B > W,   r > W.

Then ``h=N-2A=2(B-A)+r>W``.  For ``k<=W`` the only possible realisers of
``N-k`` join a right-leg mark ``B-b`` to one of

* a left mark ``A-a`` (deficit ``p=a``);
* the left centre (deficit ``p=A``); or
* a spine mark at coordinate ``s`` from the left centre (deficit ``p=A+s``).

In every case ``k=p+b``.  The state below retains only parameter-independent
necessary collisions among these bounded deficits.  It deliberately omits
all comparisons involving the exact values of B,Q,r and the vertex budget,
so it is a relaxation rather than an exact bi-spider search.

This implementation recomputes every retained collision class from scratch.
It imports no code from the paired incremental prover.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from functools import lru_cache


Side = tuple[tuple[int, ...], ...]
State = tuple[Side, tuple[int, ...], Side]


@dataclass
class CleanroomStats:
    A: int
    W: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    max_selected_vertices: int = 3
    frontier: int = 0
    memo_hits: int = 0


def canonical_side(side) -> Side:
    anchor = tuple(sorted(side[0]))
    fresh = tuple(sorted(tuple(sorted(leg)) for leg in side[1:]))
    return (anchor, *fresh)


def canonical(left, spine, right) -> State:
    return canonical_side(left), tuple(sorted(spine)), canonical_side(right)


def flat(side: Side) -> tuple[int, ...]:
    return tuple(x for leg in side for x in leg)


def high_offsets(state: State) -> tuple[int, ...]:
    left, spine, right = state
    p_values = (*flat(left), *spine)
    return tuple(p + b for p in p_values for b in flat(right))


@lru_cache(maxsize=None)
def valid(state: State, A: int, W: int) -> bool:
    left, spine, right = state
    left_values = flat(left)
    right_values = flat(right)
    p_values = (*left_values, *spine)

    if len(left_values) != len(set(left_values)):
        return False
    if len(right_values) != len(set(right_values)):
        return False
    if len(p_values) != len(set(p_values)):
        return False
    if any(a < 0 or a >= A for a in left_values):
        return False
    if A not in spine or any(d < A or (d != A and d > W) for d in spine):
        return False
    if any(b < 0 or b > W for b in right_values):
        return False

    highs = high_offsets(state)
    if len(highs) != len(set(highs)):
        return False

    # All distances wholly inside the left/spine branch, together with all
    # same-right-leg distances, are bounded constants.  They belong to one
    # global distance set and hence must be positive and pairwise distinct.
    constants: list[int] = []
    for leg in left:
        seq = sorted(leg)
        constants.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
    tagged_left = [(x, i) for i, leg in enumerate(left) for x in leg]
    constants.extend(
        2 * A - x - y
        for j, (x, li) in enumerate(tagged_left)
        for y, lj in tagged_left[j + 1 :]
        if li != lj
    )
    spine_seq = sorted(spine)
    constants.extend(
        y - x for i, x in enumerate(spine_seq) for y in spine_seq[i + 1 :]
    )
    constants.extend(d - a for a in left_values for d in spine)
    for leg in right:
        seq = sorted(leg)
        constants.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
    if any(x <= 0 for x in constants) or len(constants) != len(set(constants)):
        return False

    # Different right legs have distances 2B-(b+b'), so their offset sums are
    # unique even though this whole class lies below the selected top window.
    tagged_right = [(x, i) for i, leg in enumerate(right) for x in leg]
    right_sums = [
        x + y
        for j, (x, li) in enumerate(tagged_right)
        for y, lj in tagged_right[j + 1 :]
        if li != lj
    ]
    return len(right_sums) == len(set(right_sums))


def add_to_side(side: Side, leg_index: int, value: int) -> Side:
    out = [list(leg) for leg in side]
    if leg_index == len(out):
        out.append([value])
    else:
        out[leg_index].append(value)
    return tuple(tuple(leg) for leg in out)


def children(state: State, target: int, A: int, W: int) -> tuple[State, ...]:
    left, spine, right = state
    left_values = flat(left)
    p_values = set((*left_values, *spine))
    right_values = flat(right)
    out: set[State] = set()

    for p in range(target + 1):
        b = target - p
        if b > W:
            continue

        if p in p_values:
            p_variants = [(left, spine, False)]
        elif 0 <= p < A:
            p_variants = [
                (add_to_side(left, i, p), spine, True)
                for i in range(len(left) + 1)
            ]
        elif A < p <= W:
            p_variants = [(left, (*spine, p), True)]
        else:
            p_variants = []

        if b in right_values:
            b_variants = [(right, False)]
        else:
            b_variants = [
                (add_to_side(right, i, b), True)
                for i in range(len(right) + 1)
            ]

        for new_left, new_spine, p_added in p_variants:
            for new_right, b_added in b_variants:
                if not p_added and not b_added:
                    continue
                child = canonical(new_left, new_spine, new_right)
                if valid(child, A, W):
                    out.add(child)
    return tuple(sorted(out))


def check_positive_tail(A: int, W: int = 20) -> CleanroomStats:
    if A < 1 or W < 1:
        raise ValueError("A and W must be positive")
    valid.cache_clear()
    stats = CleanroomStats(A=A, W=W)
    initial = canonical(((0,),), (A,), ((0,),))
    if not valid(initial, A, W):
        raise RuntimeError(f"invalid initial state for A={A}, W={W}")
    seen: set[State] = set()

    def dfs(state: State, target: int) -> None:
        if state in seen:
            stats.memo_hits += 1
            return
        seen.add(state)
        stats.nodes += 1
        stats.max_selected_vertices = max(
            stats.max_selected_vertices,
            len(flat(state[0])) + len(state[1]) + len(flat(state[2])),
        )
        offsets = set(high_offsets(state))
        while target in offsets:
            target += 1
        stats.deepest = max(stats.deepest, target)
        if target > W:
            stats.frontier += 1
            return
        next_states = children(state, target, A, W)
        if not next_states:
            stats.dead += 1
            return
        for child in next_states:
            stats.children += 1
            dfs(child, target + 1)

    dfs(initial, 1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--A", type=int)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--window", type=int, default=20)
    args = parser.parse_args()
    if args.all:
        rows = [check_positive_tail(A, args.window) for A in range(1, 51)]
        print(
            json.dumps(
                {
                    "W": args.window,
                    "regimes": len(rows),
                    "nodes": sum(row.nodes for row in rows),
                    "frontier": sum(row.frontier for row in rows),
                    "max_depth": max(row.deepest for row in rows),
                    "max_selected_vertices": max(
                        row.max_selected_vertices for row in rows
                    ),
                    "memo_hits": sum(row.memo_hits for row in rows),
                },
                sort_keys=True,
            )
        )
        for row in rows:
            print(json.dumps(asdict(row), sort_keys=True))
        return
    if args.A is None:
        parser.error("give --A, or use --all")
    print(json.dumps(asdict(check_positive_tail(args.A, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
