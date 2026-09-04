"""Exact affine high-window search for the two spider boundary strips.

The N-independent offset prover handles anchors T>U with U>10 and T-U>10.
This file treats the remaining infinite strips by keeping the unbounded
parameter symbolic:

``small-U``
    U is fixed and P=T-U varies.  Then
    T=P+U and N=P+2U.

``small-delta``
    delta=T-U is fixed and P=U varies.  Then
    T=P+delta and N=2P+delta.

Every mark and pair value is represented as q*P+c.  The search below is the
same complete top-down realizer search as spider_topdown.py.  Comparisons are
required to have one truth value for every integer P>=Pmin; an assertion fires
instead of silently choosing a branch if a comparison could change in that
range.  Thus a closed affine tree proves nonexistence simultaneously for the
whole tail P>=Pmin.  With the default Pmin=51, the finite prefix is contained
in orders n<=15 and is handled by the original exact numeric search.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True, order=True)
class Affine:
    q: int
    c: int

    def __add__(self, other: "Affine") -> "Affine":
        return Affine(self.q + other.q, self.c + other.c)

    def __sub__(self, other: "Affine") -> "Affine":
        return Affine(self.q - other.q, self.c - other.c)


ONE = Affine(0, 1)


@dataclass
class AffineStats:
    mode: str
    fixed: int
    Pmin: int
    window: int
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    max_marks: int = 2
    frontier_states: int = 0
    comparisons: int = 0


def prove_boundary(mode: str, fixed: int, *, Pmin: int = 51, window: int = 25):
    if mode not in {"small-U", "small-delta"}:
        raise ValueError(mode)
    if fixed < 1 or Pmin < 1 or window < 1:
        raise ValueError("fixed, Pmin and window must be positive")

    stats = AffineStats(mode, fixed, Pmin, window)
    if mode == "small-U":
        U = Affine(0, fixed)
        T = Affine(1, fixed)
        N = Affine(1, 2 * fixed)
    else:
        U = Affine(1, 0)
        T = Affine(1, fixed)
        N = Affine(2, fixed)

    def evaluate(x: Affine, P: int = Pmin) -> int:
        return x.q * P + x.c

    def stable_sign(x: Affine) -> int:
        """Sign of x for every real P>=Pmin; abort if it can change."""

        stats.comparisons += 1
        at_min = evaluate(x)
        if x.q == 0:
            return (x.c > 0) - (x.c < 0)
        if x.q > 0:
            if at_min > 0:
                return 1
            raise AssertionError(f"sign can change for P>=Pmin: {x}")
        if at_min < 0:
            return -1
        raise AssertionError(f"sign can change for P>=Pmin: {x}")

    def positive(x: Affine) -> bool:
        return stable_sign(x) > 0

    def leq(x: Affine, y: Affine) -> bool:
        return stable_sign(y - x) >= 0

    def affine_abs(x: Affine) -> Affine:
        sign = stable_sign(x)
        if sign == 0:
            return x
        return x if sign > 0 else Affine(-x.q, -x.c)

    def separated(x: Affine, y: Affine) -> bool:
        """True when x!=y for every P>=Pmin; abort on a future root."""

        d = x - y
        if d.q == 0:
            return d.c != 0
        at_min = evaluate(d)
        # The sign is stable exactly in these cases.
        if (d.q > 0 and at_min > 0) or (d.q < 0 and at_min < 0):
            return True
        raise AssertionError(f"equality/order can change for P>=Pmin: {x}, {y}")

    legs: list[list[Affine]] = [[T], [U]]
    marks: dict[Affine, int] = {T: 0, U: 1}
    values: set[Affine] = {T, U, N}

    def cap(li: int) -> Affine:
        if li == 0:
            return T
        if li == 1:
            return U
        return U - ONE

    def placement_cap(li: int) -> Affine:
        return cap(li) if li >= 0 else U - ONE

    def same_as_any(x: Affine, xs) -> bool:
        for y in xs:
            if x == y:
                return True
            if not separated(x, y):
                raise RuntimeError(f"unexpected affine collision: {x}, {y}")
        return False

    def try_add(adds: list[tuple[int, Affine]]):
        for li, x in adds:
            if not positive(x) or not leq(x, placement_cap(li)):
                return None
            if same_as_any(x, marks):
                return None
            if li == 1 and stable_sign(U - x) <= 0:
                return None
            if li == 0 and stable_sign(T - x) <= 0:
                return None
        if len(adds) == 2:
            if adds[0][1] == adds[1][1]:
                return None
            if not separated(adds[0][1], adds[1][1]):
                raise RuntimeError(f"unexpected affine collision: {adds}")

        undo_values: list[Affine] = []
        undo_marks: list[Affine] = []
        old_leg_count = len(legs)
        fresh_map: dict[int, int] = {}

        for li, x in adds:
            if li < 0:
                if li not in fresh_map:
                    legs.append([])
                    fresh_map[li] = len(legs) - 1
                li = fresh_map[li]
            new_values = [x]
            for m, mi in marks.items():
                w = affine_abs(x - m) if mi == li else x + m
                if not positive(w) or not leq(w, N):
                    break
                new_values.append(w)
            else:
                duplicate = False
                for i, w in enumerate(new_values):
                    if same_as_any(w, new_values[:i]) or same_as_any(w, values):
                        duplicate = True
                        break
                if not duplicate:
                    values.update(new_values)
                    undo_values.extend(new_values)
                    legs[li].append(x)
                    marks[x] = li
                    undo_marks.append(x)
                    continue

            for w in undo_values:
                values.discard(w)
            for y in undo_marks:
                legs[marks[y]].remove(y)
                del marks[y]
            del legs[old_leg_count:]
            return None
        return undo_values, undo_marks, old_leg_count

    def undo(token) -> None:
        undo_values, undo_marks, old_leg_count = token
        for w in undo_values:
            values.discard(w)
        for x in undo_marks:
            legs[marks[x]].remove(x)
            del marks[x]
        del legs[old_leg_count:]

    def canonical(options: set, *placements) -> None:
        relabel: dict[int, int] = {}
        out = []
        for x, li in sorted(placements):
            if li < 0:
                if li not in relabel:
                    relabel[li] = -1 - len(relabel)
                li = relabel[li]
            out.append((x, li))
        options.add(tuple(out))

    def const_bounds(q: int, ccap: Affine):
        if q < 0 or q > ccap.q:
            return None
        lo = 1 if q == 0 else None
        hi = ccap.c if q == ccap.q else None
        return lo, hi

    def bounded_range_for_sum(v: Affine, lx: int, ly: int):
        capx, capy = placement_cap(lx), placement_cap(ly)
        for qx in range(capx.q + 1):
            qy = v.q - qx
            by = const_bounds(qy, capy)
            bx = const_bounds(qx, capx)
            if bx is None or by is None:
                continue
            lox, hix = bx
            loy, hiy = by
            lows = [z for z in (lox, v.c - hiy if hiy is not None else None) if z is not None]
            highs = [z for z in (hix, v.c - loy if loy is not None else None) if z is not None]
            if not lows or not highs:
                raise AssertionError(f"unbounded sum decomposition: {mode}, {v}, {lx}, {ly}")
            lo, hi = max(lows), min(highs)
            for cx in range(lo, hi + 1):
                yield Affine(qx, cx), Affine(qy, v.c - cx)

    def bounded_range_for_difference(v: Affine, li: int):
        ccap = placement_cap(li)
        for qx in range(ccap.q + 1):
            qy = qx + v.q
            bx = const_bounds(qx, ccap)
            by = const_bounds(qy, ccap)
            if bx is None or by is None:
                continue
            lox, hix = bx
            loy, hiy = by
            lows = [z for z in (lox, loy - v.c if loy is not None else None) if z is not None]
            highs = [z for z in (hix, hiy - v.c if hiy is not None else None) if z is not None]
            if not lows or not highs:
                raise AssertionError(f"unbounded difference decomposition: {mode}, {v}, {li}")
            for cx in range(max(lows), min(highs) + 1):
                yield Affine(qx, cx), Affine(qy, cx + v.c)

    def options(v: Affine):
        opts = set()
        nlegs = len(legs)

        for y, yi in marks.items():
            x = v - y
            if positive(x):
                for li in range(nlegs):
                    if li != yi:
                        canonical(opts, (x, li))
                canonical(opts, (x, -1))
            plus = y + v
            if leq(plus, cap(yi)):
                canonical(opts, (plus, yi))
            minus = y - v
            if positive(minus):
                canonical(opts, (minus, yi))

        for li in range(nlegs):
            canonical(opts, (v, li))
        canonical(opts, (v, -1))

        pairs = []
        for lx in range(nlegs):
            for ly in range(nlegs):
                if lx != ly:
                    pairs.append((lx, ly))
            pairs.extend(((lx, -1), (-1, lx)))
        pairs.append((-1, -2))
        for lx, ly in pairs:
            for x, y in bounded_range_for_sum(v, lx, ly):
                if stable_sign(y - x) > 0:
                    canonical(opts, (x, lx), (y, ly))
                elif stable_sign(x - y) > 0:
                    canonical(opts, (y, ly), (x, lx))

        for li in [*range(nlegs), -1]:
            for x, y in bounded_range_for_difference(v, li):
                canonical(opts, (x, li), (y, li))
        return opts

    def dfs(k: int) -> None:
        stats.nodes += 1
        stats.max_marks = max(stats.max_marks, len(marks))
        target = N - Affine(0, k)
        while target in values:
            k += 1
            target = N - Affine(0, k)
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, k)
        if k > window:
            stats.frontier_states += 1
            return

        accepted = 0
        for key in options(target):
            adds = [(li, x) for x, li in key]
            token = try_add(adds)
            if token is None:
                continue
            accepted += 1
            stats.accepted_children += 1
            dfs(k + 1)
            undo(token)
        if not accepted:
            stats.dead_states += 1

    dfs(1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("small-U", "small-delta"))
    parser.add_argument("fixed", type=int, nargs="?")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--pmin", type=int, default=51)
    parser.add_argument("--window", type=int, default=25)
    args = parser.parse_args()

    fixed_values = range(1, 11) if args.all else [args.fixed]
    if not args.all and args.fixed is None:
        parser.error("give fixed, or use --all")
    rows = [
        prove_boundary(args.mode, fixed, Pmin=args.pmin, window=args.window)
        for fixed in fixed_values
    ]
    print(
        json.dumps(
            {
                "mode": args.mode,
                "regimes": len(rows),
                "frontier_states": sum(r.frontier_states for r in rows),
                "max_depth": max(r.deepest_missing_offset for r in rows),
                "max_marks": max(r.max_marks for r in rows),
                "nodes": sum(r.nodes for r in rows),
            },
            sort_keys=True,
        )
    )
    for row in rows:
        print(json.dumps(asdict(row), sort_keys=True))


if __name__ == "__main__":
    main()
