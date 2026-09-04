#!/usr/bin/env python3
"""Independent canonical-state prover for all LL top-window regions.

The three clean-room programs keep region-specific immutable searches.  This
file independently expresses the same necessary collision systems through one
canonical graph walker and separately written placement routines.  It imports
no code from the clean-room implementations.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Callable, Tuple


Side = Tuple[Tuple[int, ...], ...]


@dataclass
class Stats:
    region: str
    p1: int
    p2: int
    W: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    frontier: int = 0
    max_vertices: int = 0


def flat(side: Side):
    return tuple(value for leg in side for value in leg)


def fixed_side(side) -> Side:
    return (tuple(sorted(side[0])), *sorted(tuple(sorted(leg)) for leg in side[1:]))


def free_side(side) -> Side:
    return tuple(sorted(tuple(sorted(leg)) for leg in side))


def add_to_side(side: Side, leg: int, value: int, fixed: bool) -> Side:
    work = [list(values) for values in side]
    if leg == len(work):
        work.append([value])
    else:
        work[leg].append(value)
    raw = tuple(tuple(values) for values in work)
    return fixed_side(raw) if fixed else free_side(raw)


def unique(values) -> bool:
    values = tuple(values)
    return len(values) == len(set(values))


def walk(
    stats: Stats,
    initial,
    valid: Callable,
    offsets: Callable,
    children: Callable,
    size: Callable,
) -> Stats:
    seen = set()

    def dfs(state) -> None:
        if state in seen:
            return
        seen.add(state)
        stats.nodes += 1
        stats.max_vertices = max(stats.max_vertices, size(state))
        present = set(offsets(state))
        target = next((value for value in range(1, stats.W + 1) if value not in present), stats.W + 1)
        stats.deepest = max(stats.deepest, target)
        if target > stats.W:
            stats.frontier += 1
            return
        next_states = children(state, target)
        if not next_states:
            stats.dead += 1
            return
        stats.children += len(next_states)
        for child in next_states:
            if not valid(child):
                raise RuntimeError("child placement bypassed validity")
            dfs(child)

    if not valid(initial):
        raise RuntimeError("invalid initial state")
    dfs(initial)
    return stats


def prove_near(delta: int, L: int, W: int = 36) -> Stats:
    """U>W, 1<=L=U-Q<=W; delta=W+1 means delta>W."""

    if not (1 <= delta <= W + 1 and 1 <= L <= W):
        raise ValueError((delta, L, W))
    # state = top, short-left legs, spine-deficits, right-leg deficits
    def canon(top, short, spine, right):
        return tuple(sorted(top)), fixed_side(short), tuple(sorted(spine)), free_side(right)

    initial = canon((0,), ((0,),), (L,), ())

    def zitems(state):
        return (*flat(state[1]), *state[2], *flat(state[3]))

    def tagged(state):
        out = [(z, ("S", leg)) for leg, values in enumerate(state[1]) for z in values]
        out.extend((z, ("F", 0)) for z in state[2])
        out.extend((z, ("F", 0)) for z in flat(state[3]))
        return tuple(out)

    def class_values(state):
        tags = tagged(state)
        main = [a + z for a in state[0] for z, _ in tags]
        cross = [
            z + other
            for index, (z, branch) in enumerate(tags)
            for other, other_branch in tags[index + 1 :]
            if branch != other_branch
        ]
        high = list(main)
        if delta <= W:
            high.extend(delta + value for value in cross)
        return main, cross, high

    def constants(state):
        out = []
        seq = sorted(state[0])
        out.extend(y - x for index, x in enumerate(seq) for y in seq[index + 1 :])
        for leg in state[1]:
            seq = sorted(leg)
            out.extend(y - x for index, x in enumerate(seq) for y in seq[index + 1 :])
        far = [(z, "P", -1) for z in state[2]]
        far.extend((z, "R", leg) for leg, values in enumerate(state[3]) for z in values)
        for index, (z, kind, leg) in enumerate(far):
            for other, other_kind, other_leg in far[index + 1 :]:
                out.append(
                    2 * L - z - other
                    if kind == other_kind == "R" and leg != other_leg
                    else abs(z - other)
                )
        return out

    def valid(state):
        top, short, spine, right = state
        zs = zitems(state)
        if 0 not in top or 0 not in short[0] or L not in spine:
            return False
        if any(not 0 <= value <= W for value in top):
            return False
        if not unique(zs) or any(not 0 <= value <= W for value in zs):
            return False
        if any(not L <= value <= W for value in spine):
            return False
        if any(not 0 < value < L for value in flat(right)):
            return False
        main, cross, high = class_values(state)
        low = constants(state)
        return unique(main) and unique(cross) and unique(high) and all(x > 0 for x in low) and unique(low)

    def top_places(state, value):
        if value in state[0]:
            return ((state, False),)
        if not 0 <= value <= W:
            return ()
        return ((canon((*state[0], value), state[1], state[2], state[3]), True),)

    def z_places(state, value):
        if not 0 <= value <= W:
            return ()
        if value in zitems(state):
            return ((state, False),)
        out = []
        for leg in range(len(state[1]) + 1):
            out.append((canon(state[0], add_to_side(state[1], leg, value, True), state[2], state[3]), True))
        if 0 < value < L:
            for leg in range(len(state[3]) + 1):
                out.append((canon(state[0], state[1], state[2], add_to_side(state[3], leg, value, False)), True))
        elif L < value <= W:
            out.append((canon(state[0], state[1], (*state[2], value), state[3]), True))
        return tuple(out)

    def branch(state, value):
        for leg, values in enumerate(state[1]):
            if value in values:
                return "S", leg
        if value in state[2] or any(value in values for values in state[3]):
            return "F", 0
        return None

    def children(state, target):
        out = set()
        for a in range(target + 1):
            z = target - a
            for first, add_a in top_places(state, a):
                for child, add_z in z_places(first, z):
                    if (add_a or add_z) and valid(child):
                        out.add(child)
        if delta <= W and target >= delta:
            total = target - delta
            for z in range(total + 1):
                other = total - z
                if z == other:
                    continue
                for first, add_z in z_places(state, z):
                    for child, add_other in z_places(first, other):
                        if (add_z or add_other) and branch(child, z) != branch(child, other) and valid(child):
                            out.add(child)
        return out

    stats = Stats("near", delta, L, W)
    return walk(stats, initial, valid, lambda state: class_values(state)[2], children, lambda state: len(state[0]) + len(zitems(state)))


def prove_far(delta: int, rho: int, W: int = 36) -> Stats:
    """U>W, L>W; sentinels W+1 denote the corresponding large tails."""

    if not (1 <= delta <= W + 1 and 1 <= rho <= W + 1):
        raise ValueError((delta, rho, W))
    if delta == W + 1 and rho != W + 1:
        raise ValueError((delta, rho))
    if delta <= W and rho <= W and (rho < delta + 2 or (rho - delta) % 2):
        raise ValueError((delta, rho))

    def canon(top, short, right):
        return tuple(sorted(top)), fixed_side(short), free_side(right)

    initial = canon((0,), ((0,),), ())

    def zitems(state):
        return (*flat(state[1]), *flat(state[2]))

    def tagged(state):
        out = [(z, ("S", leg)) for leg, values in enumerate(state[1]) for z in values]
        out.extend((z, ("F", 0)) for z in flat(state[2]))
        return tuple(out)

    def class_values(state):
        tags = tagged(state)
        main = [a + z for a in state[0] for z, _ in tags]
        cross = [z + other for i, (z, b) in enumerate(tags) for other, c in tags[i + 1 :] if b != c]
        rr_tags = [(z, leg) for leg, values in enumerate(state[2]) for z in values]
        rr = [z + other for i, (z, leg) in enumerate(rr_tags) for other, other_leg in rr_tags[i + 1 :] if leg != other_leg]
        high = list(main)
        if delta <= W:
            high.extend(delta + value for value in cross)
        if rho <= W:
            high.extend(rho + value for value in rr)
        return main, cross, rr, high

    def valid(state):
        top, short, right = state
        zs = zitems(state)
        if 0 not in top or 0 not in short[0]:
            return False
        if any(not 0 <= value <= W for value in top):
            return False
        if not unique(zs) or any(not 0 <= value <= W for value in zs):
            return False
        if any(value <= 0 for value in flat(right)):
            return False
        main, cross, rr, high = class_values(state)
        if not all(unique(values) for values in (main, cross, rr, high)):
            return False
        low = []
        if delta <= W and rho <= W:
            Q = (rho - delta) // 2
            low.append(Q)
            centre = []
            for a in top:
                centre.extend((Q + delta - a, 2 * Q + delta - a))
            for z in flat(short):
                centre.extend((Q - z, 2 * Q - z))
            for c in flat(right):
                centre.extend((Q - c, -c))
            if not unique(centre):
                return False
        for values in (top,):
            seq = sorted(values)
            low.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        for side in (short, right):
            for leg in side:
                seq = sorted(leg)
                low.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        return all(value > 0 for value in low) and unique(low)

    def top_places(state, value):
        if value in state[0]:
            return ((state, False),)
        if not 0 <= value <= W:
            return ()
        return ((canon((*state[0], value), state[1], state[2]), True),)

    def z_places(state, value):
        if not 0 <= value <= W:
            return ()
        if value in zitems(state):
            return ((state, False),)
        out = []
        for leg in range(len(state[1]) + 1):
            out.append((canon(state[0], add_to_side(state[1], leg, value, True), state[2]), True))
        if value > 0:
            for leg in range(len(state[2]) + 1):
                out.append((canon(state[0], state[1], add_to_side(state[2], leg, value, False)), True))
        return tuple(out)

    def right_places(state, value):
        if not 0 < value <= W:
            return ()
        for values in state[2]:
            if value in values:
                return ((state, False),)
        if value in zitems(state):
            return ()
        return tuple(
            (canon(state[0], state[1], add_to_side(state[2], leg, value, False)), True)
            for leg in range(len(state[2]) + 1)
        )

    def cleft_branch(state, value):
        for leg, values in enumerate(state[1]):
            if value in values:
                return "S", leg
        if any(value in values for values in state[2]):
            return "F", 0
        return None

    def rleg(state, value):
        for leg, values in enumerate(state[2]):
            if value in values:
                return leg
        return None

    def children(state, target):
        out = set()
        for a in range(target + 1):
            z = target - a
            for first, add_a in top_places(state, a):
                for child, add_z in z_places(first, z):
                    if (add_a or add_z) and valid(child):
                        out.add(child)
        if delta <= W and target >= delta:
            total = target - delta
            for z in range(total + 1):
                other = total - z
                if z == other:
                    continue
                for first, add_z in z_places(state, z):
                    for child, add_other in z_places(first, other):
                        if (add_z or add_other) and cleft_branch(child, z) != cleft_branch(child, other) and valid(child):
                            out.add(child)
        if rho <= W and target >= rho:
            total = target - rho
            for z in range(1, total):
                other = total - z
                if z == other:
                    continue
                for first, add_z in right_places(state, z):
                    for child, add_other in right_places(first, other):
                        if (add_z or add_other) and rleg(child, z) != rleg(child, other) and valid(child):
                            out.add(child)
        return out

    stats = Stats("far", delta, rho, W)
    if not valid(initial):
        stats.nodes = 1
        stats.dead = 1
        stats.max_vertices = 2
        return stats
    return walk(stats, initial, valid, lambda state: class_values(state)[3], children, lambda state: len(state[0]) + len(zitems(state)))


def prove_small(U: int, L: int, W: int = 36) -> Stats:
    """2<=U<=W and 1<=L<U; N>=153 forces delta>W."""

    if not (2 <= U <= W and 1 <= L < U):
        raise ValueError((U, L, W))
    # state = top deficits, long-leg bottom depths, short legs, spine, right
    def canon(top, bottom, short, spine, right):
        return tuple(sorted(top)), tuple(sorted(bottom)), fixed_side(short), tuple(sorted(spine)), free_side(right)

    initial = canon((0,), (0,), ((0,),), (L,), ())

    def zitems(state):
        return (*flat(state[2]), *state[3], *flat(state[4]))

    def tagged(state):
        out = [(z, ("S", leg)) for leg, values in enumerate(state[2]) for z in values]
        out.extend((z, ("F", 0)) for z in state[3])
        out.extend((z, ("F", 0)) for z in flat(state[4]))
        return tuple(out)

    def offsets(state):
        return tuple(
            [a + z for a in state[0] for z in zitems(state)]
            + [U + a + x for a in state[0] for x in state[1]]
        )

    def valid(state):
        top, bottom, short, spine, right = state
        zs = zitems(state)
        if 0 not in top or 0 not in bottom or 0 not in short[0] or L not in spine:
            return False
        if any(not 0 <= value <= W for value in top):
            return False
        if any(not 0 <= value <= W - U for value in bottom):
            return False
        if not unique(zs) or any(not 0 <= value < U for value in zs):
            return False
        if any(not L <= value < U for value in spine):
            return False
        if any(not 0 < value < L for value in flat(right)):
            return False
        if not unique(offsets(state)):
            return False
        tags = tagged(state)
        cross = [z + other for i, (z, b) in enumerate(tags) for other, c in tags[i + 1 :] if b != c]
        if not unique(cross):
            return False
        low = []
        for values in (top, bottom):
            seq = sorted(values)
            low.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        for leg in short:
            seq = sorted(leg)
            low.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
        far = [(z, "P", -1) for z in spine]
        far.extend((z, "R", leg) for leg, values in enumerate(right) for z in values)
        for i, (z, kind, leg) in enumerate(far):
            for other, other_kind, other_leg in far[i + 1 :]:
                low.append(2 * L - z - other if kind == other_kind == "R" and leg != other_leg else abs(z - other))
        return all(value > 0 for value in low) and unique(low)

    def one(state, index, value, cap):
        values = state[index]
        if value in values:
            return ((state, False),)
        if not 0 <= value <= cap:
            return ()
        pieces = list(state)
        pieces[index] = tuple((*values, value))
        return ((canon(*pieces), True),)

    def z_places(state, value):
        if not 0 <= value < U:
            return ()
        if value in zitems(state):
            return ((state, False),)
        out = []
        for leg in range(len(state[2]) + 1):
            out.append((canon(state[0], state[1], add_to_side(state[2], leg, value, True), state[3], state[4]), True))
        if 0 < value < L:
            for leg in range(len(state[4]) + 1):
                out.append((canon(state[0], state[1], state[2], state[3], add_to_side(state[4], leg, value, False)), True))
        elif L < value < U:
            out.append((canon(state[0], state[1], state[2], (*state[3], value), state[4]), True))
        return tuple(out)

    def children(state, target):
        out = set()
        for a in range(target + 1):
            z = target - a
            for first, add_a in one(state, 0, a, W):
                for child, add_z in z_places(first, z):
                    if (add_a or add_z) and valid(child):
                        out.add(child)
        if target >= U:
            total = target - U
            for a in range(total + 1):
                x = total - a
                for first, add_a in one(state, 0, a, W):
                    for child, add_x in one(first, 1, x, W - U):
                        if (add_a or add_x) and valid(child):
                            out.add(child)
        return out

    stats = Stats("small", U, L, W)
    return walk(stats, initial, valid, offsets, children, lambda state: len(state[0]) + len(state[1]) + len(zitems(state)))


def far_regimes(W: int = 36):
    rows = []
    for delta in range(1, W + 1):
        rows.extend((delta, rho, W) for rho in range(delta + 2, W + 1, 2))
        rows.append((delta, W + 1, W))
    rows.append((W + 1, W + 1, W))
    return tuple(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("region", choices=("near", "far", "small"))
    parser.add_argument("p1", type=int)
    parser.add_argument("p2", type=int)
    parser.add_argument("--window", type=int, default=36)
    args = parser.parse_args()
    function = {"near": prove_near, "far": prove_far, "small": prove_small}[args.region]
    print(json.dumps(asdict(function(args.p1, args.p2, args.window)), sort_keys=True))


if __name__ == "__main__":
    main()
