#!/usr/bin/env python3
"""Clean-room exact search for Leech bi-spiders.

This is intentionally not a port of ``bispider_topdown.py``.  A state is an
immutable collection of geometric vertex positions.  Every distance is
recomputed from scratch.  When the greatest missing value ``v`` is processed,
the program

* tries every legal single new position; and
* for two new endpoints, iterates the first position and solves the metric
  equation ``d(x, y) = v`` uniformly over every existing/fresh position slot.

Thus the production program's hand-written centre/same-leg/cross-leg option
list is not reused.  The only shared ingredients are the mathematical LR/LL
normalisation and the descending greatest-missing-value principle.

Any solution is converted to a weighted edge list and must pass both
``src/checker_a.py`` and ``src/checker_b.py`` before it is printed.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from time import monotonic


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import checker_a  # noqa: E402
import checker_b  # noqa: E402


@dataclass(frozen=True, order=True)
class Vertex:
    side: str
    leg: int
    x: int


@dataclass(frozen=True)
class Geometry:
    Q: int
    fixed_caps_l: tuple[int, ...]
    fresh_cap_l: int
    fixed_caps_r: tuple[int, ...]
    fresh_cap_r: int


@dataclass(frozen=True)
class State:
    legs_l: tuple[tuple[int, ...], ...]
    spine: tuple[int, ...]
    legs_r: tuple[tuple[int, ...], ...]


@dataclass
class Stats:
    anchors: int = 0
    nodes: int = 0
    candidate_marks: int = 0
    candidate_pairs: int = 0
    legal_children: int = 0
    memo_hits: int = 0
    max_noncentre_marks: int = 0
    deepest_missing_offset: int = 0


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def cap(geometry: Geometry, side: str, leg: int) -> int:
    fixed = geometry.fixed_caps_l if side == "L" else geometry.fixed_caps_r
    fresh = geometry.fresh_cap_l if side == "L" else geometry.fresh_cap_r
    return fixed[leg] if leg < len(fixed) else fresh


def canonical(state: State, geometry: Geometry) -> State:
    """Sort interchangeable non-anchor legs without merging anchor legs."""

    def canon_side(legs: tuple[tuple[int, ...], ...], fixed_count: int):
        fixed = tuple(tuple(sorted(leg)) for leg in legs[:fixed_count])
        free = tuple(sorted(tuple(sorted(leg)) for leg in legs[fixed_count:]))
        return fixed + free

    return State(
        canon_side(state.legs_l, len(geometry.fixed_caps_l)),
        tuple(sorted(state.spine)),
        canon_side(state.legs_r, len(geometry.fixed_caps_r)),
    )


def vertices(state: State) -> tuple[Vertex, ...]:
    out: list[Vertex] = []
    for i, leg in enumerate(state.legs_l):
        out.extend(Vertex("L", i, x) for x in leg)
    out.extend(Vertex("S", -1, x) for x in state.spine)
    for i, leg in enumerate(state.legs_r):
        out.extend(Vertex("R", i, x) for x in leg)
    return tuple(out)


def distance_to_left(v: Vertex, Q: int) -> int:
    if v.side == "L":
        return v.x
    if v.side == "S":
        return v.x
    return Q + v.x


def distance_to_right(v: Vertex, Q: int) -> int:
    if v.side == "L":
        return Q + v.x
    if v.side == "S":
        return Q - v.x
    return v.x


def pair_distance(a: Vertex, b: Vertex, Q: int) -> int:
    if a.side == "S" and b.side == "S":
        return abs(a.x - b.x)
    if a.side == "S":
        return a.x + b.x if b.side == "L" else Q - a.x + b.x
    if b.side == "S":
        return b.x + a.x if a.side == "L" else Q - b.x + a.x
    if a.side != b.side:
        return a.x + Q + b.x
    if a.leg == b.leg:
        return abs(a.x - b.x)
    return a.x + b.x


def distance_values(state: State, geometry: Geometry, N: int) -> frozenset[int] | None:
    vs = vertices(state)
    raw = [geometry.Q]
    for i, v in enumerate(vs):
        raw.append(distance_to_left(v, geometry.Q))
        raw.append(distance_to_right(v, geometry.Q))
        for w in vs[i + 1 :]:
            raw.append(pair_distance(v, w, geometry.Q))
    if any(x < 1 or x > N for x in raw):
        return None
    if len(raw) != len(set(raw)):
        return None
    return frozenset(raw)


def slots(state: State) -> tuple[tuple[str, int], ...]:
    return (
        tuple(("L", i) for i in range(len(state.legs_l) + 1))
        + (("S", -1),)
        + tuple(("R", i) for i in range(len(state.legs_r) + 1))
    )


def coordinates(state: State, geometry: Geometry, slot: tuple[str, int]):
    side, leg = slot
    if side == "S":
        return range(1, geometry.Q)
    return range(1, cap(geometry, side, leg) + 1)


def all_positions(state: State, geometry: Geometry):
    for side, leg in slots(state):
        for x in coordinates(state, geometry, (side, leg)):
            yield Vertex(side, leg, x)


def add_raw(state: State, vertex: Vertex) -> State | None:
    """Add a vertex, preserving fresh-leg identity until the child is complete."""

    if vertex.side == "S":
        return State(state.legs_l, state.spine + (vertex.x,), state.legs_r)
    legs = list(state.legs_l if vertex.side == "L" else state.legs_r)
    if vertex.leg > len(legs):
        return None
    if vertex.leg == len(legs):
        legs.append((vertex.x,))
    else:
        legs[vertex.leg] = legs[vertex.leg] + (vertex.x,)
    if vertex.side == "L":
        return State(tuple(legs), state.spine, state.legs_r)
    return State(state.legs_l, state.spine, tuple(legs))


def partner_coordinates(
    first: Vertex, slot: tuple[str, int], target: int, Q: int
) -> tuple[int, ...]:
    """Solve d(first, second)=target in the chosen geometric slot."""

    side, leg = slot
    if first.side == "S":
        if side == "S":
            return (first.x - target, first.x + target)
        if side == "L":
            return (target - first.x,)
        return (target - (Q - first.x),)
    if first.side == "L":
        if side == "S":
            return (target - first.x,)
        if side == "R":
            return (target - Q - first.x,)
        if leg == first.leg:
            return (first.x - target, first.x + target)
        return (target - first.x,)
    if side == "S":
        return (Q + first.x - target,)
    if side == "L":
        return (target - Q - first.x,)
    if leg == first.leg:
        return (first.x - target, first.x + target)
    return (target - first.x,)


def child_states(
    state: State,
    geometry: Geometry,
    target: int,
    n: int,
    N: int,
    stats: Stats,
) -> tuple[State, ...]:
    old_count = len(vertices(state))
    out: set[State] = set()
    first_positions = tuple(all_positions(state, geometry))

    if old_count + 1 <= n - 2:
        for first in first_positions:
            stats.candidate_marks += 1
            state1 = add_raw(state, first)
            if state1 is None:
                continue
            values1 = distance_values(state1, geometry, N)
            if values1 is not None and target in values1:
                out.add(canonical(state1, geometry))

    if old_count + 2 <= n - 2:
        for first in first_positions:
            state1 = add_raw(state, first)
            if state1 is None:
                continue
            values1 = distance_values(state1, geometry, N)
            if values1 is None or target in values1:
                continue
            for slot in slots(state1):
                allowed = range(
                    1,
                    (geometry.Q - 1 if slot[0] == "S" else cap(geometry, slot[0], slot[1]))
                    + 1,
                )
                allowed_lo = allowed.start
                allowed_hi = allowed.stop - 1
                for x in set(partner_coordinates(first, slot, target, geometry.Q)):
                    if x < allowed_lo or x > allowed_hi:
                        continue
                    second = Vertex(slot[0], slot[1], x)
                    stats.candidate_pairs += 1
                    if second == first:
                        continue
                    state2 = add_raw(state1, second)
                    if state2 is None:
                        continue
                    values2 = distance_values(state2, geometry, N)
                    if values2 is None or target not in values2:
                        continue
                    out.add(canonical(state2, geometry))

    stats.legal_children += len(out)
    return tuple(sorted(out, key=repr))


def state_to_edges(state: State, geometry: Geometry) -> tuple[int, list[tuple[int, int, int]]]:
    edges: list[tuple[int, int, int]] = []
    next_vertex = 2

    previous_vertex = 0
    previous_x = 0
    for s in sorted(state.spine):
        edges.append((previous_vertex, next_vertex, s - previous_x))
        previous_vertex = next_vertex
        previous_x = s
        next_vertex += 1
    edges.append((previous_vertex, 1, geometry.Q - previous_x))

    for centre, legs in ((0, state.legs_l), (1, state.legs_r)):
        for leg in legs:
            previous_vertex = centre
            previous_x = 0
            for x in sorted(leg):
                edges.append((previous_vertex, next_vertex, x - previous_x))
                previous_vertex = next_vertex
                previous_x = x
                next_vertex += 1
    return next_vertex, edges


def verify_witness(state: State, geometry: Geometry, n: int) -> list[tuple[int, int, int]]:
    actual_n, edges = state_to_edges(state, geometry)
    require(actual_n == n, f"witness has {actual_n} vertices, expected {n}")
    ok_a, reason_a = checker_a.is_leech(n, edges)
    ok_b, reason_b = checker_b.is_leech(n, edges)
    require(ok_a, f"checker_a rejected witness: {reason_a}")
    require(ok_b, f"checker_b rejected witness: {reason_b}")
    return edges


def solve(n: int, modes: tuple[str, ...]) -> tuple[list[dict], Stats]:
    N = n * (n - 1) // 2
    stats = Stats()
    solutions: list[dict] = []
    solved_states: dict[tuple[Geometry, State], bool] = {}

    def run_anchor(geometry: Geometry, initial: State, anchor: dict) -> None:
        initial = canonical(initial, geometry)
        initial_values = distance_values(initial, geometry, N)
        if initial_values is None:
            return
        stats.anchors += 1
        seen: set[State] = set()

        def dfs(state: State) -> bool:
            key = (geometry, state)
            if key in solved_states:
                stats.memo_hits += 1
                return solved_states[key]
            if state in seen:
                stats.memo_hits += 1
                return False
            seen.add(state)
            stats.nodes += 1
            mark_count = len(vertices(state))
            stats.max_noncentre_marks = max(stats.max_noncentre_marks, mark_count)
            values = distance_values(state, geometry, N)
            require(values is not None, f"invalid state reached: {state}")
            missing = next((v for v in range(N, 0, -1) if v not in values), 0)
            stats.deepest_missing_offset = max(stats.deepest_missing_offset, N - missing)
            if missing == 0:
                edges = verify_witness(state, geometry, n)
                solutions.append(
                    {
                        **anchor,
                        "Q": geometry.Q,
                        "legs_l": state.legs_l,
                        "spine": state.spine,
                        "legs_r": state.legs_r,
                        "edges": edges,
                        "checker_a": "PASS",
                        "checker_b": "PASS",
                    }
                )
                solved_states[key] = True
                return True
            found = False
            for child in child_states(state, geometry, missing, n, N, stats):
                found = dfs(child) or found
            solved_states[key] = found
            return found

        dfs(initial)

    if "LR" in modes:
        for tip_l in range(1, N // 2 + 1):
            for tip_r in range(tip_l + 1, N - tip_l):
                Q = N - tip_l - tip_r
                if Q < 1:
                    break
                geometry = Geometry(Q, (tip_l,), tip_l - 1, (tip_r,), tip_r - 1)
                initial = State(((tip_l,),), (), ((tip_r,),))
                run_anchor(geometry, initial, {"mode": "LR", "tip_l": tip_l, "tip_r": tip_r})

    if "LL" in modes:
        for tip_1 in range(N // 2 + 1, N):
            tip_2 = N - tip_1
            if tip_2 < 1:
                break
            for Q in range(1, tip_2):
                geometry = Geometry(
                    Q,
                    (tip_1, tip_2),
                    tip_2 - 1,
                    (),
                    max(tip_2 - Q - 1, 0),
                )
                initial = State(((tip_1,), (tip_2,)), (), ())
                run_anchor(geometry, initial, {"mode": "LL", "tip_1": tip_1, "tip_2": tip_2})

    return solutions, stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("mode", choices=("LR", "LL", "both"), nargs="?", default="both")
    args = parser.parse_args()
    require(args.n >= 4, "clean-room bi-spider search currently requires n >= 4")
    modes = ("LR", "LL") if args.mode == "both" else (args.mode,)
    started = monotonic()
    solutions, stats = solve(args.n, modes)
    summary = {
        "n": args.n,
        "N": args.n * (args.n - 1) // 2,
        "modes": modes,
        "solutions": len(solutions),
        **stats.__dict__,
        "seconds": round(monotonic() - started, 3),
        "status": "DONE",
    }
    print(json.dumps(summary, sort_keys=True))
    for solution in solutions:
        print(json.dumps(solution, sort_keys=True))


if __name__ == "__main__":
    main()
