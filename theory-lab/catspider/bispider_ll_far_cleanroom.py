#!/usr/bin/env python3
"""Immutable clean-room search for LL anchors with U>W and L=U-Q>W.

The visible endpoints are long-leg deficits ``a``, short-left deficits ``z``,
and right-leg deficits ``c``.  Put ``delta=T-U`` and ``rho=delta+2Q=N-2L``.
The high offsets are

    a+z,                 delta+z+z' across cL branches,
    rho+c+c'             across different right legs.

Values W+1 are stable sentinels for delta>W or rho>W.  The program retains
necessary within-class collisions and omits parameter-dependent cross-class
collisions, so it is a relaxation of every exact anchor in this region.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Tuple


Side = Tuple[Tuple[int, ...], ...]
State = Tuple[Tuple[int, ...], Side, Side]


@dataclass
class Stats:
    delta: int
    rho: int
    W: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    frontier: int = 0
    max_vertices: int = 2


def flat(side: Side):
    return tuple(value for leg in side for value in leg)


def canon_fixed(side: Side) -> Side:
    return (tuple(sorted(side[0])), *sorted(tuple(sorted(leg)) for leg in side[1:]))


def canon_free(side: Side) -> Side:
    return tuple(sorted(tuple(sorted(leg)) for leg in side))


def canonical(top, short, right) -> State:
    return tuple(sorted(top)), canon_fixed(short), canon_free(right)


def z_values(state: State):
    return (*flat(state[1]), *flat(state[2]))


def tagged_cleft(state: State):
    tagged = [(value, ("S", leg)) for leg, values in enumerate(state[1]) for value in values]
    tagged.extend((value, ("F", 0)) for value in flat(state[2]))
    return tuple(tagged)


def classes(state: State, delta: int, rho: int, W: int):
    tagged = tagged_cleft(state)
    main = [a + z for a in state[0] for z, _ in tagged]
    cross = [
        z + other
        for index, (z, branch) in enumerate(tagged)
        for other, other_branch in tagged[index + 1 :]
        if branch != other_branch
    ]
    tagged_right = [(value, leg) for leg, values in enumerate(state[2]) for value in values]
    rr = [
        value + other
        for index, (value, leg) in enumerate(tagged_right)
        for other, other_leg in tagged_right[index + 1 :]
        if leg != other_leg
    ]
    offsets = list(main)
    if delta <= W:
        offsets.extend(delta + value for value in cross)
    if rho <= W:
        offsets.extend(rho + value for value in rr)
    return tuple(main), tuple(cross), tuple(rr), tuple(offsets)


@lru_cache(maxsize=None)
def valid(state: State, delta: int, rho: int, W: int) -> bool:
    top, short, right = state
    if 0 not in top or 0 not in short[0]:
        return False
    if any(value < 0 or value > W for value in top):
        return False
    zs = z_values(state)
    if len(zs) != len(set(zs)) or any(value < 0 or value > W for value in zs):
        return False
    if any(value <= 0 for value in flat(right)):
        return False

    main, cross, rr, offsets = classes(state, delta, rho, W)
    if any(len(values) != len(set(values)) for values in (main, cross, rr)):
        return False
    if len(offsets) != len(set(offsets)):
        return False

    constants = []
    if delta <= W and rho <= W:
        Q = (rho - delta) // 2
        constants.append(Q)
        centre_offsets = []
        for a in top:
            centre_offsets.extend((Q + delta - a, 2 * Q + delta - a))
        for z in flat(short):
            centre_offsets.extend((Q - z, 2 * Q - z))
        for c in flat(right):
            centre_offsets.extend((Q - c, -c))
        if len(centre_offsets) != len(set(centre_offsets)):
            return False
    seq = sorted(top)
    constants.extend(y - x for index, x in enumerate(seq) for y in seq[index + 1 :])
    for side in (short, right):
        for leg in side:
            seq = sorted(leg)
            constants.extend(y - x for index, x in enumerate(seq) for y in seq[index + 1 :])
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


def branch(state: State, value: int):
    for leg, values in enumerate(state[1]):
        if value in values:
            return "S", leg
    if any(value in values for values in state[2]):
        return "F", 0
    return None


def right_leg(state: State, value: int):
    for leg, values in enumerate(state[2]):
        if value in values:
            return leg
    return None


def search(delta: int, rho: int, W: int = 35, dump_frontier: bool = False) -> Stats:
    if W < 1 or not (1 <= delta <= W + 1 and 1 <= rho <= W + 1):
        raise ValueError((delta, rho, W))
    if delta == W + 1 and rho != W + 1:
        raise ValueError("rho>W whenever delta>W")
    if delta <= W and rho <= W and (rho < delta + 2 or (rho - delta) % 2):
        raise ValueError("rho=delta+2Q with integral Q>=1")
    valid.cache_clear()
    out = Stats(delta=delta, rho=rho, W=W)
    initial = canonical((0,), ((0,),), ())
    if not valid(initial, delta, rho, W):
        out.nodes = 1
        out.dead = 1
        return out

    def top_extensions(state: State, value: int):
        if value in state[0]:
            return ((state, False),)
        if not 0 <= value <= W:
            return ()
        return ((canonical((*state[0], value), state[1], state[2]), True),)

    def z_extensions(state: State, value: int):
        if value < 0 or value > W:
            return ()
        if value in z_values(state):
            return ((state, False),)
        result = []
        for leg in range(len(state[1]) + 1):
            short = add_side(state[1], leg, value, fixed=True)
            result.append((canonical(state[0], short, state[2]), True))
        if value > 0:
            for leg in range(len(state[2]) + 1):
                right = add_side(state[2], leg, value, fixed=False)
                result.append((canonical(state[0], state[1], right), True))
        return tuple(result)

    def right_extensions(state: State, value: int):
        if value <= 0 or value > W:
            return ()
        old = right_leg(state, value)
        if old is not None:
            return ((state, False),)
        if value in z_values(state):
            return ()
        result = []
        for leg in range(len(state[2]) + 1):
            right = add_side(state[2], leg, value, fixed=False)
            result.append((canonical(state[0], state[1], right), True))
        return tuple(result)

    def children(state: State, target: int):
        result = set()
        for a in range(target + 1):
            z = target - a
            for first, added_a in top_extensions(state, a):
                for child, added_z in z_extensions(first, z):
                    if (added_a or added_z) and valid(child, delta, rho, W):
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
                        if branch(child, z) == branch(child, other):
                            continue
                        if valid(child, delta, rho, W):
                            result.add(child)

        total = target - rho
        if rho <= W and total >= 0:
            for value in range(1, total):
                other = total - value
                if value == other:
                    continue
                for first, added_value in right_extensions(state, value):
                    for child, added_other in right_extensions(first, other):
                        if not (added_value or added_other):
                            continue
                        if right_leg(child, value) == right_leg(child, other):
                            continue
                        if valid(child, delta, rho, W):
                            result.add(child)
        return tuple(sorted(result))

    seen = set()

    def dfs(state: State, target: int) -> None:
        if state in seen:
            return
        seen.add(state)
        out.nodes += 1
        out.max_vertices = max(out.max_vertices, len(state[0]) + len(z_values(state)))
        offsets = set(classes(state, delta, rho, W)[3])
        while target in offsets:
            target += 1
        out.deepest = max(out.deepest, target)
        if target > W:
            out.frontier += 1
            if dump_frontier:
                print(repr(state), file=sys.stderr, flush=True)
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


def regimes(W: int = 35):
    result = []
    for delta in range(1, W + 1):
        result.extend((delta, rho, W) for rho in range(delta + 2, W + 1, 2))
        result.append((delta, W + 1, W))
    result.append((W + 1, W + 1, W))
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("delta", type=int)
    parser.add_argument("rho", type=int)
    parser.add_argument("--window", type=int, default=35)
    parser.add_argument("--dump-frontier", action="store_true")
    args = parser.parse_args()
    print(
        json.dumps(
            asdict(search(args.delta, args.rho, args.window, args.dump_frontier)),
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
