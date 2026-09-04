#!/usr/bin/env python3
"""Immutable clean-room search for LL anchors with U>W, L<=W, N>=153.

Let the two LL anchor tips have depths T>U, put ``delta=T-U`` and
``L=U-Q``.  This file covers ``1<=L<=W``.  For target orders and U>W, all
top-window endpoint coordinates are deficits from the two anchor tips;
``delta=W+1`` is the stable sentinel for values greater than W.  The separate
far-side probe handles ``L>W``, where right-leg marks remain visible.

This is deliberately a relaxation.  It keeps the exact high-offset classes
and several parameter-free internal collision classes, but omits collisions
between classes and all distances involving vertices outside the window.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Tuple


Side = Tuple[Tuple[int, ...], ...]
State = Tuple[Tuple[int, ...], Side, Tuple[int, ...], Side]


@dataclass
class Stats:
    delta: int
    L: int
    W: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    frontier: int = 0
    max_vertices: int = 4


def flat(side: Side):
    return tuple(value for leg in side for value in leg)


def canon_fixed(side: Side) -> Side:
    return (tuple(sorted(side[0])), *sorted(tuple(sorted(leg)) for leg in side[1:]))


def canon_free(side: Side) -> Side:
    return tuple(sorted(tuple(sorted(leg)) for leg in side))


def canonical(top, short, spine, right) -> State:
    return tuple(sorted(top)), canon_fixed(short), tuple(sorted(spine)), canon_free(right)


def z_values(state: State):
    return (*flat(state[1]), *state[2], *flat(state[3]))


def tagged_cleft(state: State):
    tagged = [(value, ("S", leg)) for leg, values in enumerate(state[1]) for value in values]
    tagged.extend((value, ("F", 0)) for value in state[2])
    tagged.extend((value, ("F", 0)) for value in flat(state[3]))
    return tuple(tagged)


def high_classes(state: State, delta: int, W: int):
    top = state[0]
    tagged = tagged_cleft(state)
    main = [a + z for a in top for z, _ in tagged]
    cross = [
        z + other
        for index, (z, branch) in enumerate(tagged)
        for other, other_branch in tagged[index + 1 :]
        if branch != other_branch
    ]
    offsets = list(main)
    if delta <= W:
        offsets.extend(delta + value for value in cross)
    return tuple(main), tuple(cross), tuple(offsets)


@lru_cache(maxsize=None)
def valid(state: State, delta: int, L: int, W: int) -> bool:
    top, short, spine, right = state
    if 0 not in top or 0 not in short[0]:
        return False
    if any(value < 0 or value > W for value in top):
        return False
    zs = z_values(state)
    if len(zs) != len(set(zs)) or any(value < 0 or value > W for value in zs):
        return False
    if L not in spine or any(value < L or value > W for value in spine):
        return False
    if any(value <= 0 or value >= L for value in flat(right)):
        return False

    main, cross, offsets = high_classes(state, delta, W)
    if len(main) != len(set(main)) or len(cross) != len(set(cross)):
        return False
    if delta <= W and len(offsets) != len(set(offsets)):
        return False

    constants = []
    seq = sorted(top)
    constants.extend(y - x for index, x in enumerate(seq) for y in seq[index + 1 :])
    for leg in short:
        seq = sorted(leg)
        constants.extend(y - x for index, x in enumerate(seq) for y in seq[index + 1 :])

    far = [(value, "P", -1) for value in spine]
    far.extend((value, "R", leg) for leg, values in enumerate(right) for value in values)
    for index, (x, kind, leg) in enumerate(far):
        for y, other_kind, other_leg in far[index + 1 :]:
            if kind == other_kind == "R" and leg != other_leg:
                constants.append(2 * L - x - y)
            else:
                constants.append(abs(x - y))
    if any(value <= 0 for value in constants):
        return False
    return len(constants) == len(set(constants))


def add_side(side: Side, leg: int, value: int, *, fixed: bool) -> Side:
    out = [list(values) for values in side]
    if leg == len(out):
        out.append([value])
    else:
        out[leg].append(value)
    raw = tuple(tuple(values) for values in out)
    return canon_fixed(raw) if fixed else canon_free(raw)


def z_branch(state: State, value: int):
    for leg, values in enumerate(state[1]):
        if value in values:
            return "S", leg
    if value in state[2] or any(value in values for values in state[3]):
        return "F", 0
    return None


def search(delta: int, L: int, W: int = 35) -> Stats:
    if W < 1 or not (1 <= delta <= W + 1 and 1 <= L <= W):
        raise ValueError((delta, L, W))
    valid.cache_clear()
    out = Stats(delta=delta, L=L, W=W)
    initial = canonical((0,), ((0,),), (L,), ())
    if not valid(initial, delta, L, W):
        return out

    def top_extensions(state: State, value: int):
        if value in state[0]:
            return ((state, False),)
        if not 0 <= value <= W:
            return ()
        return ((canonical((*state[0], value), state[1], state[2], state[3]), True),)

    def z_extensions(state: State, value: int):
        if value < 0 or value > W:
            return ()
        if value in z_values(state):
            return ((state, False),)
        result = []
        for leg in range(len(state[1]) + 1):
            short = add_side(state[1], leg, value, fixed=True)
            result.append((canonical(state[0], short, state[2], state[3]), True))
        if 0 < value < L:
            for leg in range(len(state[3]) + 1):
                right = add_side(state[3], leg, value, fixed=False)
                result.append((canonical(state[0], state[1], state[2], right), True))
        elif L < value <= W:
            result.append((canonical(state[0], state[1], (*state[2], value), state[3]), True))
        return tuple(result)

    def children(state: State, target: int):
        result = set()
        for a in range(target + 1):
            z = target - a
            for first, added_a in top_extensions(state, a):
                for child, added_z in z_extensions(first, z):
                    if (added_a or added_z) and valid(child, delta, L, W):
                        result.add(child)

        total = target - delta
        if delta <= W and total >= 0:
            for z in range(total + 1):
                other = total - z
                if z == other:
                    continue
                for first, added_z in z_extensions(state, z):
                    for child, added_other in z_extensions(first, other):
                        if not (added_z or added_other):
                            continue
                        if z_branch(child, z) == z_branch(child, other):
                            continue
                        if valid(child, delta, L, W):
                            result.add(child)
        return tuple(sorted(result))

    seen = set()

    def dfs(state: State, target: int) -> None:
        if state in seen:
            return
        seen.add(state)
        out.nodes += 1
        out.max_vertices = max(out.max_vertices, len(state[0]) + len(z_values(state)))
        offsets = set(high_classes(state, delta, W)[2])
        while target in offsets:
            target += 1
        out.deepest = max(out.deepest, target)
        if target > W:
            out.frontier += 1
            return
        next_states = children(state, target)
        if not next_states:
            out.dead += 1
            return
        for child in next_states:
            out.children += 1
            dfs(child, target + 1)

    dfs(initial, 1)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("delta", type=int)
    parser.add_argument("L", type=int)
    parser.add_argument("--window", type=int, default=35)
    args = parser.parse_args()
    print(json.dumps(asdict(search(args.delta, args.L, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
