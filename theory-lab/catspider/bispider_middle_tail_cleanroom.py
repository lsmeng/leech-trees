#!/usr/bin/env python3
"""Immutable full-recomputation search for the large-h middle LR tail."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Tuple


Side = Tuple[Tuple[int, ...], ...]
State = Tuple[Side, Tuple[int, ...], Side]


@dataclass
class Stats:
    A: int
    r: int
    W: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    frontier: int = 0
    max_vertices: int = 3


def flat(side: Side):
    return tuple(x for leg in side for x in leg)


def canon_side(side) -> Side:
    return (tuple(sorted(side[0])), *sorted(tuple(sorted(x)) for x in side[1:]))


def canonical(left, spine, right) -> State:
    return canon_side(left), tuple(sorted(spine)), canon_side(right)


def high_offsets(state: State, r: int):
    left, spine, right = state
    p_values = (*flat(left), *spine)
    right_values = flat(right)
    out = [p + b for p in p_values for b in right_values]
    tagged = [(b, leg) for leg, values in enumerate(right) for b in values]
    out.extend(
        r + b + c
        for i, (b, bi) in enumerate(tagged)
        for c, ci in tagged[i + 1 :]
        if bi != ci
    )
    return tuple(out)


@lru_cache(maxsize=None)
def valid(state: State, A: int, r: int, W: int) -> bool:
    left, spine, right = state
    left_values = flat(left)
    right_values = flat(right)
    p_values = (*left_values, *spine)
    cap = W - min(r, 0)
    if len(left_values) != len(set(left_values)):
        return False
    if len(right_values) != len(set(right_values)):
        return False
    if len(p_values) != len(set(p_values)):
        return False
    if any(a < 0 or a >= A for a in left_values):
        return False
    if A not in spine or any(p < A or (p != A and p > W) for p in spine):
        return False
    if any(b < 0 or b > cap for b in right_values):
        return False
    highs = high_offsets(state, r)
    if any(k < 0 for k in highs) or len(highs) != len(set(highs)):
        return False

    constants = []
    for leg in left:
        seq = sorted(leg)
        constants.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
    tagged_left = [(a, leg) for leg, values in enumerate(left) for a in values]
    constants.extend(
        2 * A - a - c
        for i, (a, ai) in enumerate(tagged_left)
        for c, ci in tagged_left[i + 1 :]
        if ai != ci
    )
    seq = sorted(spine)
    constants.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
    constants.extend(p - a for a in left_values for p in spine)
    for leg in right:
        seq = sorted(leg)
        constants.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
    if any(x <= 0 for x in constants) or len(constants) != len(set(constants)):
        return False

    tagged_right = [(b, leg) for leg, values in enumerate(right) for b in values]
    right_sums = [
        b + c
        for i, (b, bi) in enumerate(tagged_right)
        for c, ci in tagged_right[i + 1 :]
        if bi != ci
    ]
    return len(right_sums) == len(set(right_sums))


def add_side(side: Side, leg: int, value: int) -> Side:
    out = [list(values) for values in side]
    if leg == len(out):
        out.append([value])
    else:
        out[leg].append(value)
    return tuple(tuple(values) for values in out)


def location(side: Side, value: int):
    for leg, values in enumerate(side):
        if value in values:
            return leg
    return None


def extensions(state: State, kind: str, value: int):
    left, spine, right = state
    if kind == "L":
        old = location(left, value)
        if old is not None:
            return ((state, False, old),)
        return tuple(
            (canonical(add_side(left, leg, value), spine, right), True, leg)
            for leg in range(len(left) + 1)
        )
    if kind == "R":
        old = location(right, value)
        if old is not None:
            return ((state, False, old),)
        return tuple(
            (canonical(left, spine, add_side(right, leg, value)), True, leg)
            for leg in range(len(right) + 1)
        )
    if value in spine:
        return ((state, False, 0),)
    return ((canonical(left, (*spine, value), right), True, 0),)


def children(state: State, target: int, A: int, r: int, W: int):
    out = set()
    cap = W - min(r, 0)

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
            for first, added_first, _ in extensions(state, kind, p):
                for child, added_second, _ in extensions(first, "R", b):
                    if (added_first or added_second) and valid(child, A, r, W):
                        out.add(child)

    total = target - r
    if total >= 0:
        for b in range(total + 1):
            c = total - b
            if b > cap or c > cap:
                continue
            for first, added_first, leg_b in extensions(state, "R", b):
                for child, added_second, leg_c in extensions(first, "R", c):
                    if leg_b == leg_c:
                        continue
                    if (added_first or added_second) and valid(child, A, r, W):
                        out.add(child)
    return tuple(sorted(out))


def search(A: int, r: int, W: int = 35) -> Stats:
    if not (1 <= A <= 50 and -15 <= r <= 20 and W >= 1):
        raise ValueError((A, r, W))
    valid.cache_clear()
    stats = Stats(A=A, r=r, W=W)
    initial = canonical(((0,),), (A,), ((0,),))
    if not valid(initial, A, r, W):
        return stats
    seen = set()

    def dfs(state: State, target: int) -> None:
        if state in seen:
            return
        seen.add(state)
        stats.nodes += 1
        stats.max_vertices = max(
            stats.max_vertices,
            len(flat(state[0])) + len(state[1]) + len(flat(state[2])),
        )
        offsets = set(high_offsets(state, r))
        while target in offsets:
            target += 1
        stats.deepest = max(stats.deepest, target)
        if target > W:
            stats.frontier += 1
            return
        next_states = children(state, target, A, r, W)
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
    parser.add_argument("A", type=int)
    parser.add_argument("r", type=int)
    parser.add_argument("--window", type=int, default=35)
    args = parser.parse_args()
    print(json.dumps(asdict(search(args.A, args.r, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
