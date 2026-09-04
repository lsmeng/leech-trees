#!/usr/bin/env python3
"""Immutable clean-room search for LL anchors with 2<=U<=W and N>=153.

In this range ``delta=N-2U>W``.  The long anchor leg has a stable cluster at
each end.  If ``a`` is a deficit from its tip, ``x`` a distance from the left
centre, and ``z`` a deficit from U on any other cL branch, the only high
offsets are ``a+z`` and ``U+a+x``.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Tuple


Side = Tuple[Tuple[int, ...], ...]
State = Tuple[Tuple[int, ...], Tuple[int, ...], Side, Tuple[int, ...], Side]


@dataclass
class Stats:
    U: int
    L: int
    W: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    frontier: int = 0
    max_vertices: int = 5
    peak_layer_states: int = 1


def flat(side: Side):
    return tuple(value for leg in side for value in leg)


def canon_fixed(side: Side) -> Side:
    return (tuple(sorted(side[0])), *sorted(tuple(sorted(leg)) for leg in side[1:]))


def canon_free(side: Side) -> Side:
    return tuple(sorted(tuple(sorted(leg)) for leg in side))


def canonical(top, bottom, short, spine, right) -> State:
    return (
        tuple(sorted(top)),
        tuple(sorted(bottom)),
        canon_fixed(short),
        tuple(sorted(spine)),
        canon_free(right),
    )


def z_values(state: State):
    return (*flat(state[2]), *state[3], *flat(state[4]))


def tagged_cleft(state: State):
    tagged = [(value, ("S", leg)) for leg, values in enumerate(state[2]) for value in values]
    tagged.extend((value, ("F", 0)) for value in state[3])
    tagged.extend((value, ("F", 0)) for value in flat(state[4]))
    return tuple(tagged)


def far_constants(state: State, L: int):
    far = [(value, "P", -1) for value in state[3]]
    far.extend((value, "R", leg) for leg, values in enumerate(state[4]) for value in values)
    result = []
    for index, (x, kind, leg) in enumerate(far):
        for y, other_kind, other_leg in far[index + 1 :]:
            if kind == other_kind == "R" and leg != other_leg:
                result.append(2 * L - x - y)
            else:
                result.append(abs(x - y))
    return result


def high_offsets(state: State, U: int):
    top, bottom = state[:2]
    zs = z_values(state)
    main = [a + z for a in top for z in zs]
    long_leg = [U + a + x for a in top for x in bottom]
    return tuple((*main, *long_leg))


def valid(state: State, U: int, L: int, W: int) -> bool:
    top, bottom, short, spine, right = state
    if 0 not in top or 0 not in bottom or 0 not in short[0] or L not in spine:
        return False
    if any(value < 0 or value > W for value in top):
        return False
    if any(value < 0 or value > W - U for value in bottom):
        return False
    zs = z_values(state)
    if len(zs) != len(set(zs)) or any(value < 0 or value >= U for value in zs):
        return False
    if any(value < L or value >= U for value in spine):
        return False
    if any(value <= 0 or value >= L for value in flat(right)):
        return False

    highs = high_offsets(state, U)
    if len(highs) != len(set(highs)):
        return False

    tagged = tagged_cleft(state)
    cross_sums = [
        z + other
        for index, (z, branch) in enumerate(tagged)
        for other, other_branch in tagged[index + 1 :]
        if branch != other_branch
    ]
    if len(cross_sums) != len(set(cross_sums)):
        return False

    constants = []
    for values in (top, bottom):
        seq = sorted(values)
        constants.extend(y - x for index, x in enumerate(seq) for y in seq[index + 1 :])
    for leg in short:
        seq = sorted(leg)
        constants.extend(y - x for index, x in enumerate(seq) for y in seq[index + 1 :])
    constants.extend(far_constants(state, L))
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


def search(U: int, L: int, W: int = 35, progress: bool = False) -> Stats:
    if not (2 <= U <= W and 1 <= L < U):
        raise ValueError((U, L, W))
    out = Stats(U=U, L=L, W=W)
    initial = canonical((0,), (0,), ((0,),), (L,), ())
    if not valid(initial, U, L, W):
        return out

    def top_extensions(state: State, value: int):
        if value in state[0]:
            return ((state, False),)
        if not 0 <= value <= W:
            return ()
        return ((canonical((*state[0], value), state[1], state[2], state[3], state[4]), True),)

    def bottom_extensions(state: State, value: int):
        if value in state[1]:
            return ((state, False),)
        if not 0 <= value <= W - U:
            return ()
        return ((canonical(state[0], (*state[1], value), state[2], state[3], state[4]), True),)

    def z_extensions(state: State, value: int):
        if value < 0 or value >= U:
            return ()
        if value in z_values(state):
            return ((state, False),)
        result = []
        for leg in range(len(state[2]) + 1):
            short = add_side(state[2], leg, value, fixed=True)
            result.append((canonical(state[0], state[1], short, state[3], state[4]), True))
        if 0 < value < L:
            for leg in range(len(state[4]) + 1):
                right = add_side(state[4], leg, value, fixed=False)
                result.append((canonical(state[0], state[1], state[2], state[3], right), True))
        elif L < value < U:
            result.append((canonical(state[0], state[1], state[2], (*state[3], value), state[4]), True))
        return tuple(result)

    def children(state: State, target: int):
        result = set()
        for a in range(target + 1):
            z = target - a
            for first, added_a in top_extensions(state, a):
                for child, added_z in z_extensions(first, z):
                    if (added_a or added_z) and valid(child, U, L, W):
                        result.add(child)
        total = target - U
        if total >= 0:
            for a in range(total + 1):
                x = total - a
                for first, added_a in top_extensions(state, a):
                    for child, added_x in bottom_extensions(first, x):
                        if (added_a or added_x) and valid(child, U, L, W):
                            result.add(child)
        return tuple(sorted(result))

    def vertex_count(state: State) -> int:
        # Both fixed centres occur as boundary coordinates in this relaxation.
        # Keeping that constant convention reproduces the original DFS stats.
        return len(state[0]) + len(state[1]) + len(z_values(state))

    buckets = {vertex_count(initial): {initial}}
    while buckets:
        count = min(buckets)
        states = buckets.pop(count)
        out.peak_layer_states = max(out.peak_layer_states, len(states))
        if progress:
            print(
                json.dumps(
                    {
                        "U": U,
                        "L": L,
                        "vertices": count,
                        "layer_states": len(states),
                        "nodes_before_layer": out.nodes,
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
                flush=True,
            )
        for state in states:
            out.nodes += 1
            out.max_vertices = max(out.max_vertices, count)
            offsets = set(high_offsets(state, U))
            target = next((value for value in range(1, W + 1) if value not in offsets), W + 1)
            out.deepest = max(out.deepest, target)
            if target > W:
                out.frontier += 1
                continue
            next_states = children(state, target)
            if not next_states:
                out.dead += 1
                continue
            out.children += len(next_states)
            for child in next_states:
                child_count = vertex_count(child)
                if child_count <= count:
                    raise RuntimeError("child did not add a selected endpoint")
                buckets.setdefault(child_count, set()).add(child)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("U", type=int)
    parser.add_argument("L", type=int)
    parser.add_argument("--window", type=int, default=35)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    print(json.dumps(asdict(search(args.U, args.L, args.window, args.progress)), sort_keys=True))


if __name__ == "__main__":
    main()
