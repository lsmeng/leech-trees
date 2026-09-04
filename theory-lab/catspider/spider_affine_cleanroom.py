"""Independent recomputation checker for the affine spider boundary proof.

This program intentionally imports no code from ``spider_affine_prover.py``.
The production prover maintains distance sets incrementally; this checker uses
immutable leg states and recomputes every centre and pair distance from scratch
after every proposed addition.  It also obtains the finite ranges for affine
marks directly from their value at the tail endpoint Pmin.

The two modes and their parameter P agree with the production prover.  Every
comparison must be constant for all real P>=Pmin; a changing comparison aborts
the run.  Thus a zero-frontier run independently checks the two infinite
boundary strips used in the uniform no-spider theorem.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True, order=True)
class Lin:
    q: int
    c: int

    def __add__(self, other: "Lin") -> "Lin":
        return Lin(self.q + other.q, self.c + other.c)

    def __sub__(self, other: "Lin") -> "Lin":
        return Lin(self.q - other.q, self.c - other.c)


@dataclass
class CheckStats:
    mode: str
    fixed: int
    pmin: int
    window: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    max_marks: int = 2
    frontier_states: int = 0
    comparisons: int = 0


def check_boundary(mode: str, fixed: int, *, pmin: int = 51, window: int = 25):
    if mode not in {"small-U", "small-delta"}:
        raise ValueError(mode)
    if not (fixed >= 1 and pmin >= 1 and window >= 1):
        raise ValueError("fixed, pmin and window must be positive")

    stats = CheckStats(mode, fixed, pmin, window)
    if mode == "small-U":
        U, T, N = Lin(0, fixed), Lin(1, fixed), Lin(1, 2 * fixed)
    else:
        U, T, N = Lin(1, 0), Lin(1, fixed), Lin(2, fixed)

    def at(x: Lin) -> int:
        return x.q * pmin + x.c

    def sign(x: Lin) -> int:
        """Uniform sign on [pmin,infinity), or abort if it can change."""

        stats.comparisons += 1
        here = at(x)
        if x.q == 0:
            return (x.c > 0) - (x.c < 0)
        if x.q > 0 and here > 0:
            return 1
        if x.q < 0 and here < 0:
            return -1
        raise AssertionError(f"non-uniform sign for P>={pmin}: {x}")

    def distinct(x: Lin, y: Lin) -> bool:
        d = x - y
        return sign(d) != 0

    def abs_tail(x: Lin) -> Lin:
        s = sign(x)
        if s == 0:
            return x
        return x if s > 0 else Lin(-x.q, -x.c)

    def cap(li: int) -> Lin:
        if li == 0:
            return T
        if li == 1:
            return U
        return U - Lin(0, 1)

    def within(x: Lin, upper: Lin) -> bool:
        return sign(x) > 0 and sign(upper - x) >= 0

    def canonical(legs) -> tuple[tuple[Lin, ...], ...]:
        first = tuple(sorted(legs[0]))
        second = tuple(sorted(legs[1]))
        rest = tuple(sorted(tuple(sorted(leg)) for leg in legs[2:]))
        return (first, second, *rest)

    def distance_set(state: tuple[tuple[Lin, ...], ...]):
        flat = [(x, li) for li, leg in enumerate(state) for x in leg]
        seen: list[Lin] = []
        for x, _ in flat:
            if not within(x, N):
                return None
            for y in seen:
                if not distinct(x, y):
                    return None
            seen.append(x)
        for i, (x, li) in enumerate(flat):
            for y, lj in flat[i + 1 :]:
                d = abs_tail(x - y) if li == lj else x + y
                if not within(d, N):
                    return None
                for old in seen:
                    if not distinct(d, old):
                        return None
                seen.append(d)
        return frozenset(seen)

    def coefficient_bounds(q: int, upper: Lin):
        """Constants c for 0 < q*P+c <= upper on the whole tail."""

        if q < 0 or q > upper.q:
            return None
        lo = 1 if q == 0 else 1 - q * pmin
        hi = upper.c if q == upper.q else (upper.q - q) * pmin + upper.c
        return lo, hi

    def sum_pairs(v: Lin, lx: int, ly: int):
        ux, uy = cap(lx), cap(ly)
        for qx in range(ux.q + 1):
            qy = v.q - qx
            bx, by = coefficient_bounds(qx, ux), coefficient_bounds(qy, uy)
            if bx is None or by is None:
                continue
            lo = max(bx[0], v.c - by[1])
            hi = min(bx[1], v.c - by[0])
            for cx in range(lo, hi + 1):
                yield Lin(qx, cx), Lin(qy, v.c - cx)

    def difference_pairs(v: Lin, li: int):
        upper = cap(li)
        for qx in range(upper.q + 1):
            qy = qx + v.q
            bx = coefficient_bounds(qx, upper)
            by = coefficient_bounds(qy, upper)
            if bx is None or by is None:
                continue
            lo = max(bx[0], by[0] - v.c)
            hi = min(bx[1], by[1] - v.c)
            for cx in range(lo, hi + 1):
                yield Lin(qx, cx), Lin(qy, cx + v.c)

    def add_state(state, placements):
        legs = [list(leg) for leg in state]
        fresh: dict[int, int] = {}
        for li, x in placements:
            if li < 0:
                if li not in fresh:
                    legs.append([])
                    fresh[li] = len(legs) - 1
                li = fresh[li]
            # The top and second tips are already pinned and may not be added
            # again.  Every later leg has strict cap U-1.
            upper = cap(li)
            if not within(x, upper):
                return None
            if li == 0 and sign(T - x) <= 0:
                return None
            if li == 1 and sign(U - x) <= 0:
                return None
            legs[li].append(x)
        child = canonical(legs)
        return child if distance_set(child) is not None else None

    def child_states(state, target: Lin):
        flat = [(x, li) for li, leg in enumerate(state) for x in leg]
        nlegs = len(state)
        options = set()

        def add(*placements):
            # Relabel fresh legs by first appearance after a deterministic sort.
            relabel: dict[int, int] = {}
            out = []
            for li, x in sorted(placements, key=lambda z: (z[1], z[0])):
                if li < 0:
                    if li not in relabel:
                        relabel[li] = -1 - len(relabel)
                    li = relabel[li]
                out.append((li, x))
            options.add(tuple(out))

        for y, yi in flat:
            x = target - y
            if sign(x) > 0:
                for li in range(nlegs):
                    if li != yi:
                        add((li, x))
                add((-1, x))
            add((yi, y + target))
            x = y - target
            if sign(x) > 0:
                add((yi, x))

        for li in range(nlegs):
            add((li, target))
        add((-1, target))

        placements = [*range(nlegs), -1]
        cross_placements = [
            (lx, ly)
            for lx in placements
            for ly in placements
            if lx != ly
        ]
        cross_placements.append((-1, -2))
        for lx, ly in cross_placements:
            for x, y in sum_pairs(target, lx, ly):
                if sign(y - x) > 0:
                    add((lx, x), (ly, y))
                elif sign(x - y) > 0:
                    add((ly, y), (lx, x))

        for li in placements:
            for x, y in difference_pairs(target, li):
                add((li, x), (li, y))

        children = set()
        for option in options:
            child = add_state(state, option)
            if child is not None:
                children.add(child)
        return children

    initial = canonical(((T,), (U,)))
    if distance_set(initial) != frozenset((T, U, N)):
        raise RuntimeError(f"invalid initial affine state: {initial}")

    def dfs(state, k: int) -> None:
        stats.nodes += 1
        stats.max_marks = max(stats.max_marks, sum(map(len, state)))
        values = distance_set(state)
        if values is None:
            raise RuntimeError(f"invalid affine state reached: {state}")
        target = N - Lin(0, k)
        while target in values:
            k += 1
            target = N - Lin(0, k)
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, k)
        if k > window:
            stats.frontier_states += 1
            return
        children = child_states(state, target)
        if not children:
            stats.dead_states += 1
            return
        stats.accepted_children += len(children)
        for child in children:
            dfs(child, k + 1)

    dfs(initial, 1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("small-U", "small-delta"))
    parser.add_argument("fixed", type=int, nargs="?")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--pmin", type=int, default=51)
    parser.add_argument("--window", type=int, default=25)
    args = parser.parse_args()
    if not args.all and args.fixed is None:
        parser.error("give fixed, or use --all")
    fixed_values = range(1, 11) if args.all else (args.fixed,)
    rows = [
        check_boundary(args.mode, fixed, pmin=args.pmin, window=args.window)
        for fixed in fixed_values
    ]
    print(
        json.dumps(
            {
                "mode": args.mode,
                "regimes": len(rows),
                "frontier_states": sum(row.frontier_states for row in rows),
                "max_depth": max(row.deepest_missing_offset for row in rows),
                "max_marks": max(row.max_marks for row in rows),
                "nodes": sum(row.nodes for row in rows),
            },
            sort_keys=True,
        )
    )
    for row in rows:
        print(json.dumps(asdict(row), sort_keys=True))


if __name__ == "__main__":
    main()
