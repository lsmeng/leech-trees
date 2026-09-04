"""Instrument the high-value window of the exact Leech-spider search.

This is an experimental companion to ``spider_topdown.py``.  It uses the same
state and branching rules, but generates the two-new-mark options through
cap-aware intervals.  Near the top value N this makes the amount of work depend
on the offset k in N-k, rather than on N itself.

For a fixed anchor pair T > U with N = T+U, ``explore_anchor`` records:

* the greatest offset k for which a missing value N-k is examined;
* the greatest number of non-central marks in any accepted state;
* whether the vertex budget rejected an otherwise legal option; and
* whether any state survives beyond an optional window limit.

The probe is still numeric.  It does NOT prove that one window works for all
T,U; its purpose is to state and test the exact finite claim that a later
symbolic certificate must establish.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass
class AnchorStats:
    N: int
    T: int
    U: int
    nodes: int = 0
    options_generated: int = 0
    accepted_children: int = 0
    budget_rejects: int = 0
    deepest_missing_offset: int = 0
    max_marks: int = 2
    dead_states: int = 0
    solutions: int = 0
    frontier_states: int = 0


def explore_anchor(
    T: int,
    U: int,
    *,
    mark_budget: int | None = None,
    window_limit: int | None = None,
    paranoid: bool = False,
    trace_records: list[dict] | None = None,
) -> AnchorStats:
    """Run the exact top-down search for one numeric anchor pair.

    ``mark_budget`` is the maximum number of non-central spider marks.  Use
    n-1 for an order-n search, or ``None`` to test whether the high-window
    closure is independent of the order/vertex budget.

    If ``window_limit`` is W, a state whose next missing value is N-k with
    k>W is counted as a frontier state and is not expanded.
    """

    if not (T > U >= 1):
        raise ValueError(f"need T > U >= 1, got T={T}, U={U}")
    N = T + U
    stats = AnchorStats(N=N, T=T, U=U)

    # Leg 0 is the unique top leg.  Leg 1 has tip U.  Every later leg has
    # cap U-1.  Lists need not be sorted while the search is in progress.
    legs: list[list[int]] = [[T], [U]]
    marks: dict[int, int] = {T: 0, U: 1}
    values: set[int] = {T, U, N}

    def cap(li: int) -> int:
        return T if li == 0 else (U if li == 1 else U - 1)

    def placement_cap(li: int) -> int:
        return cap(li) if li >= 0 else U - 1

    def try_add(adds: list[tuple[int, int]]):
        """Apply an option, returning an undo token or ``None``."""

        for li, x in adds:
            if x < 1 or x in marks:
                return None
            if x > placement_cap(li):
                return None
            if li == 1 and x >= U:
                return None
            if li == 0 and x >= T:
                return None
        if len(adds) == 2 and adds[0][1] == adds[1][1]:
            return None
        if mark_budget is not None and len(marks) + len(adds) > mark_budget:
            stats.budget_rejects += 1
            return None

        undo_values: list[int] = []
        undo_marks: list[int] = []
        old_leg_count = len(legs)
        fresh_map: dict[int, int] = {}

        for li, x in adds:
            if li < 0:
                if li not in fresh_map:
                    legs.append([])
                    fresh_map[li] = len(legs) - 1
                li = fresh_map[li]

            new_values = [x]
            legal = True
            for m, mi in marks.items():
                w = abs(x - m) if mi == li else x + m
                if not (1 <= w <= N):
                    legal = False
                    break
                new_values.append(w)
            if legal and len(new_values) != len(set(new_values)):
                legal = False
            if legal and any(w in values for w in new_values):
                legal = False
            if not legal:
                for w in undo_values:
                    values.discard(w)
                for y in undo_marks:
                    legs[marks[y]].remove(y)
                    del marks[y]
                del legs[old_leg_count:]
                return None

            values.update(new_values)
            undo_values.extend(new_values)
            legs[li].append(x)
            marks[x] = li
            undo_marks.append(x)

        return undo_values, undo_marks, old_leg_count

    def undo(token) -> None:
        undo_values, undo_marks, old_leg_count = token
        for w in undo_values:
            values.discard(w)
        for x in undo_marks:
            legs[marks[x]].remove(x)
            del marks[x]
        del legs[old_leg_count:]

    def add_canonical(options: set[tuple[tuple[int, int], ...]], *placements):
        # Input placements are (mark, leg).  Relabel fresh legs by their first
        # appearance after sorting, exactly as in spider_topdown.py.
        relabel: dict[int, int] = {}
        out = []
        for x, li in sorted(placements):
            if li < 0:
                if li not in relabel:
                    relabel[li] = -1 - len(relabel)
                li = relabel[li]
            out.append((x, li))
        options.add(tuple(out))

    def cross_interval(v: int, lx: int, ly: int) -> Iterable[int]:
        """x values for x+y=v, x<y, at placements lx,ly."""

        lo = max(1, v - placement_cap(ly))
        hi = min((v - 1) // 2, placement_cap(lx))
        return range(lo, hi + 1)

    def options(v: int):
        opts: set[tuple[tuple[int, int], ...]] = set()
        nlegs = len(legs)

        # One new mark, paired with an existing mark.
        for y, yi in marks.items():
            x = v - y
            if x >= 1:
                for li in range(nlegs):
                    if li != yi:
                        add_canonical(opts, (x, li))
                add_canonical(opts, (x, -1))
            if y + v <= cap(yi):
                add_canonical(opts, (y + v, yi))
            if y - v >= 1:
                add_canonical(opts, (y - v, yi))

        # The centre is the partner.
        for li in range(nlegs):
            add_canonical(opts, (v, li))
        add_canonical(opts, (v, -1))

        # Two new marks on different legs.  Cap-aware intervals are equivalent
        # to the long x-loop in the reference prover, but near N contain only
        # O(N-v) candidates.
        for lx in range(nlegs):
            for ly in range(nlegs):
                if lx == ly:
                    continue
                for x in cross_interval(v, lx, ly):
                    add_canonical(opts, (x, lx), (v - x, ly))
            for x in cross_interval(v, lx, -1):
                add_canonical(opts, (x, lx), (v - x, -1))
            for x in cross_interval(v, -1, lx):
                add_canonical(opts, (x, -1), (v - x, lx))
        for x in cross_interval(v, -1, -2):
            add_canonical(opts, (x, -1), (v - x, -2))

        # Two new marks on one leg with difference v.
        for li in range(nlegs):
            for x1 in range(1, cap(li) - v + 1):
                add_canonical(opts, (x1, li), (x1 + v, li))
        for x1 in range(1, (U - 1) - v + 1):
            add_canonical(opts, (x1, -1), (x1 + v, -1))

        return opts

    def paranoid_check() -> None:
        all_values = []
        flat = [(x, li) for li, leg in enumerate(legs) for x in leg]
        for i, (x, lx) in enumerate(flat):
            all_values.append(x)
            for y, ly in flat[i + 1 :]:
                all_values.append(abs(x - y) if lx == ly else x + y)
        if len(all_values) != len(set(all_values)):
            raise RuntimeError("duplicate pair value in paranoid recomputation")
        if not all(1 <= w <= N for w in all_values):
            raise RuntimeError("out-of-range value in paranoid recomputation")
        if set(all_values) != values:
            raise RuntimeError("incremental value set mismatch in paranoid recomputation")

    next_state_id = 0

    def dfs(v: int, parent_id: int | None = None) -> None:
        nonlocal next_state_id
        state_id = next_state_id
        next_state_id += 1
        stats.nodes += 1
        stats.max_marks = max(stats.max_marks, len(marks))
        if paranoid:
            paranoid_check()
        while v >= 1 and v in values:
            v -= 1
        if trace_records is not None:
            top_offsets = sorted(T - x for x in legs[0])
            lower_legs = [sorted(U - x for x in leg) for leg in legs[1:]]
            trace_records.append(
                {
                    "id": state_id,
                    "parent": parent_id,
                    "next_missing_offset": None if v == 0 else N - v,
                    "top_offsets": top_offsets,
                    "lower_leg_offsets": lower_legs,
                    "high_offsets": sorted(N - w for w in values if N - 30 <= w <= N),
                    "low_values": sorted(w for w in values if w <= 30),
                    "marks": len(marks),
                }
            )
        if v == 0:
            stats.solutions += 1
            return

        offset = N - v
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, offset)
        if window_limit is not None and offset > window_limit:
            stats.frontier_states += 1
            return

        opts = options(v)
        stats.options_generated += len(opts)
        accepted_here = 0
        for key in opts:
            adds = [(li, x) for x, li in key]
            token = try_add(adds)
            if token is None:
                continue
            accepted_here += 1
            stats.accepted_children += 1
            dfs(v - 1, state_id)
            undo(token)
        if accepted_here == 0:
            stats.dead_states += 1

    dfs(N - 1)
    return stats


def explore_order(
    n: int, *, window_limit: int | None = None, ignore_budget: bool = False
):
    N = n * (n - 1) // 2
    rows = []
    for T in range(N // 2 + 1, N):
        U = N - T
        rows.append(
            explore_anchor(
                T,
                U,
                mark_budget=None if ignore_budget else n - 1,
                window_limit=window_limit,
            )
        )
    return rows


def summarize(rows: list[AnchorStats]):
    return {
        "anchors": len(rows),
        "nodes": sum(r.nodes for r in rows),
        "options_generated": sum(r.options_generated for r in rows),
        "accepted_children": sum(r.accepted_children for r in rows),
        "budget_rejects": sum(r.budget_rejects for r in rows),
        "deepest_missing_offset": max((r.deepest_missing_offset for r in rows), default=0),
        "max_marks": max((r.max_marks for r in rows), default=0),
        "dead_states": sum(r.dead_states for r in rows),
        "solutions": sum(r.solutions for r in rows),
        "frontier_states": sum(r.frontier_states for r in rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, nargs="?")
    parser.add_argument("--anchor", type=int)
    parser.add_argument("--U", type=int)
    parser.add_argument("--delta", type=int)
    parser.add_argument("--window", type=int)
    parser.add_argument("--ignore-budget", action="store_true")
    parser.add_argument("--rows", action="store_true")
    parser.add_argument("--paranoid", action="store_true")
    parser.add_argument("--states", action="store_true")
    args = parser.parse_args()

    if args.U is not None or args.delta is not None:
        if args.U is None or args.delta is None:
            parser.error("--U and --delta must be supplied together")
        records = [] if args.states else None
        row = explore_anchor(
            args.U + args.delta,
            args.U,
            mark_budget=None,
            window_limit=args.window,
            paranoid=args.paranoid,
            trace_records=records,
        )
        print(json.dumps(asdict(row), sort_keys=True))
        if records is not None:
            for record in records:
                print(json.dumps(record, sort_keys=True))
        return

    if args.n is None:
        parser.error("give n, or give --U and --delta")
    N = args.n * (args.n - 1) // 2
    if args.anchor is not None:
        records = [] if args.states else None
        rows = [
            explore_anchor(
                args.anchor,
                N - args.anchor,
                mark_budget=None if args.ignore_budget else args.n - 1,
                window_limit=args.window,
                paranoid=args.paranoid,
                trace_records=records,
            )
        ]
    else:
        rows = explore_order(
            args.n,
            window_limit=args.window,
            ignore_budget=args.ignore_budget,
        )
    print(json.dumps({"n": args.n, "N": N, **summarize(rows)}, sort_keys=True))
    if args.rows:
        for row in rows:
            print(json.dumps(asdict(row), sort_keys=True))
    if args.anchor is not None and records is not None:
        for record in records:
            print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
