#!/usr/bin/env python3
"""Immutable clean-room prover for the bounded-imbalance LR strip.

For an LR anchor N=A+Q+B with A<B, set

    r = Q-(B-A),       h = N-2A = 2Q-r.

When A>W, a distance N-k, k<=W, can only have one of the offset forms

    LR: a+b,      RR: r+b+b',      LL: h+a+a',

where the same-side forms use different legs.  This implementation keeps the union of
those high-offset values unique and all same-leg differences unique.  Every
other collision class and the vertex budget are omitted, making it a
relaxation of the exact search for fixed r,h.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from functools import lru_cache


Side = tuple[tuple[int, ...], ...]
State = tuple[Side, Side]


@dataclass
class StripStats:
    W: int
    r: int
    h: int
    nodes: int = 0
    children: int = 0
    dead: int = 0
    deepest: int = 0
    max_marks: int = 2
    frontier: int = 0
    memo_hits: int = 0


def canonical_side(side) -> Side:
    first = tuple(sorted(side[0]))
    rest = tuple(sorted(tuple(sorted(leg)) for leg in side[1:]))
    return (first, *rest)


def canonical(left, right) -> State:
    return canonical_side(left), canonical_side(right)


def flat(side: Side) -> tuple[int, ...]:
    return tuple(x for leg in side for x in leg)


def high_offset_list(state: State, W: int, r: int, h: int) -> list[int]:
    left, right = state
    out = [a + b for a in flat(left) for b in flat(right)]
    for shift, side in ((h, left), (r, right)):
        tagged = [(x, i) for i, leg in enumerate(side) for x in leg]
        out.extend(
            shift + x + y
            for j, (x, li) in enumerate(tagged)
            for y, lj in tagged[j + 1 :]
            if li != lj
        )
    return out


@lru_cache(maxsize=None)
def valid(state: State, W: int, r: int, h: int) -> bool:
    if (h + r) % 2 or h + r < 2:
        return False
    for side in state:
        values = flat(side)
        if len(values) != len(set(values)):
            return False
        if any(x < 0 or x > W - min(r, 0) for x in values):
            return False

    highs = high_offset_list(state, W, r, h)
    if any(x < 0 for x in highs) or len(highs) != len(set(highs)):
        return False

    differences = []
    for side in state:
        for leg in side:
            seq = sorted(leg)
            differences.extend(y - x for i, x in enumerate(seq) for y in seq[i + 1 :])
    if len(differences) != len(set(differences)):
        return False
    Q = (h + r) // 2
    if Q in differences:
        return False

    # Centre-to-mark distances also form one global distance set.  At cR,
    # depths C-a and B-b coincide exactly when a-b=r; at cL, depths A-a and
    # Q+B-b=A+h-b coincide exactly when b-a=h.
    left_values = flat(state[0])
    right_values = flat(state[1])
    if any(a - b == r or b - a == h for a in left_values for b in right_values):
        return False

    # On either side, different-leg distances have a fixed base minus the
    # offset sum.  Their sums remain unique even when that distance class lies
    # below the selected high window and is omitted from ``highs``.
    for side in state:
        tagged = [(x, i) for i, leg in enumerate(side) for x in leg]
        sums = [
            x + y
            for j, (x, li) in enumerate(tagged)
            for y, lj in tagged[j + 1 :]
            if li != lj
        ]
        if len(sums) != len(set(sums)):
            return False
    return True


def add_raw(state: State, side_name: str, leg_index: int, value: int) -> State:
    selected = 0 if side_name == "L" else 1
    sides = [[list(leg) for leg in side] for side in state]
    side = sides[selected]
    if leg_index == len(side):
        side.append([value])
    else:
        side[leg_index].append(value)
    return (
        tuple(tuple(leg) for leg in sides[0]),
        tuple(tuple(leg) for leg in sides[1]),
    )


def location(side: Side, value: int):
    for i, leg in enumerate(side):
        if value in leg:
            return i
    return None


def pair_extensions(
    state: State,
    side_1: str,
    value_1: int,
    side_2: str,
    value_2: int,
    *,
    different_legs: bool,
):
    index_1 = 0 if side_1 == "L" else 1
    old_location_1 = location(state[index_1], value_1)
    first_options = (
        [(state, old_location_1, False)]
        if old_location_1 is not None
        else [
            (add_raw(state, side_1, leg, value_1), leg, True)
            for leg in range(len(state[index_1]) + 1)
        ]
    )
    for state_1, leg_1, added_1 in first_options:
        index_2 = 0 if side_2 == "L" else 1
        old_location_2 = location(state_1[index_2], value_2)
        second_options = (
            [(state_1, old_location_2, False)]
            if old_location_2 is not None
            else [
                (add_raw(state_1, side_2, leg, value_2), leg, True)
                for leg in range(len(state_1[index_2]) + 1)
            ]
        )
        for state_2, leg_2, added_2 in second_options:
            if not added_1 and not added_2:
                continue
            if different_legs and side_1 == side_2 and leg_1 == leg_2:
                continue
            yield canonical(*state_2)


def child_states(state: State, target: int, W: int, r: int, h: int) -> tuple[State, ...]:
    out: set[State] = set()

    # LR: a+b=target.
    for a in range(target + 1):
        b = target - a
        for child in pair_extensions(state, "L", a, "R", b, different_legs=False):
            if valid(child, W, r, h):
                out.add(child)

    # RR: r+b+b'=target, endpoints on different right legs.
    rr_sum = target - r
    if rr_sum >= 0:
        for b in range(rr_sum + 1):
            other = rr_sum - b
            for child in pair_extensions(state, "R", b, "R", other, different_legs=True):
                if valid(child, W, r, h):
                    out.add(child)

    # LL: h+a+a'=target, endpoints on different left legs.
    ll_sum = target - h
    if ll_sum >= 0:
        for a in range(ll_sum + 1):
            other = ll_sum - a
            for child in pair_extensions(state, "L", a, "L", other, different_legs=True):
                if valid(child, W, r, h):
                    out.add(child)
    return tuple(sorted(out))


def prove_strip_cleanroom(W: int, r: int, h: int) -> StripStats:
    if W < 1 or h < 1:
        raise ValueError("require W>=1 and h>=1")
    if (h + r) % 2 or h + r < 2:
        raise ValueError("r,h do not define an integral positive Q")
    valid.cache_clear()
    stats = StripStats(W=W, r=r, h=h)
    initial: State = (((0,),), ((0,),))
    if not valid(initial, W, r, h):
        # For example r=0 makes the two anchor tips equidistant from cR, so
        # the anchor already repeats a distance and the regime is empty.
        stats.dead = 1
        return stats
    seen: set[State] = set()

    def dfs(state: State, target: int) -> None:
        if state in seen:
            stats.memo_hits += 1
            return
        seen.add(state)
        stats.nodes += 1
        stats.max_marks = max(stats.max_marks, len(flat(state[0])) + len(flat(state[1])))
        values = set(high_offset_list(state, W, r, h))
        while target in values:
            target += 1
        stats.deepest = max(stats.deepest, target)
        if target > W:
            stats.frontier += 1
            return
        children = child_states(state, target, W, r, h)
        if not children:
            stats.dead += 1
            return
        for child in children:
            stats.children += 1
            dfs(child, target + 1)

    dfs(initial, 1)
    return stats


def admissible_h_values(W: int, r: int) -> tuple[int, ...]:
    """All h that affect the window, plus one representative infinite tail."""

    q_min = max(1, r + 1)
    h_min = 2 * q_min - r
    max_offset = W - min(r, 0)
    # For h>W the LL class leaves the high window.  Once h exceeds every
    # possible b-a and Q=(h+r)/2 exceeds every same-leg offset difference,
    # no retained comparison depends on h.  One further admissible value then
    # represents the entire infinite tail.
    critical = max(W, 2 * max_offset + abs(r))
    values = list(range(h_min, critical + 1, 2))
    tail = max(critical + 1, h_min)
    if (tail + r) % 2:
        tail += 1
    return tuple(values + [tail])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", type=int, default=20)
    parser.add_argument("--r", type=int)
    parser.add_argument("--h", type=int)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--r-lo", type=int, default=-15)
    parser.add_argument("--r-hi", type=int, default=20)
    args = parser.parse_args()
    if args.all:
        rows = [
            prove_strip_cleanroom(args.window, r, h)
            for r in range(args.r_lo, args.r_hi + 1)
            for h in admissible_h_values(args.window, r)
        ]
        print(
            json.dumps(
                {
                    "W": args.window,
                    "regimes": len(rows),
                    "nodes": sum(row.nodes for row in rows),
                    "frontier": sum(row.frontier for row in rows),
                    "max_deepest": max(row.deepest for row in rows),
                    "max_marks": max(row.max_marks for row in rows),
                },
                sort_keys=True,
            )
        )
        for row in rows:
            print(json.dumps(asdict(row), sort_keys=True))
        return
    if args.r is None or args.h is None:
        parser.error("provide --r and --h, or use --all")
    print(json.dumps(asdict(prove_strip_cleanroom(args.window, args.r, args.h)), sort_keys=True))


if __name__ == "__main__":
    main()
