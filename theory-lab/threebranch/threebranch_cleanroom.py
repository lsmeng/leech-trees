#!/usr/bin/env python3
"""Exact full-recomputation search for Leech trees with three branch vertices.

The three branch centres lie at weighted coordinates 0, Q1 and Q1+Q2 on one
core path.  Every other vertex is either an interior core mark or a mark on a
path leg based at one of the three centres.  A state is immutable and every
pair distance is recomputed from the geometry; there is no incremental
distance cache.

The unique distance-N leaf pair has, up to reflection, one of four centre
types: AA (same end), BB (same middle), AB (end-middle), or AC (opposite
ends).  For every legal numeric anchor, the search repeatedly realizes the
greatest missing distance by adding one or two marks.  The run is a proof only
when it reports status DONE.  Any solution is converted to weighted edges and
must pass both repository witness checkers before it is printed.
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


REQUIRED_LEGS = (2, 1, 2)


@dataclass(frozen=True, order=True)
class Vertex:
    kind: str                 # "L" for a leg mark, "S" for a core-spine mark
    centre: int               # 0,1,2 for L; -1 for S
    leg: int                  # leg index for L; -1 for S
    x: int                    # depth from centre for L; coordinate from c0 for S


@dataclass(frozen=True)
class Geometry:
    q1: int
    q2: int
    fixed_caps: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]
    fresh_caps: tuple[int, int, int]

    @property
    def positions(self) -> tuple[int, int, int]:
        return (0, self.q1, self.q1 + self.q2)

    @property
    def total_core(self) -> int:
        return self.q1 + self.q2


@dataclass(frozen=True)
class State:
    legs: tuple[
        tuple[tuple[int, ...], ...],
        tuple[tuple[int, ...], ...],
        tuple[tuple[int, ...], ...],
    ]
    spine: tuple[int, ...]


@dataclass
class Stats:
    anchors_generated: int = 0
    anchors: int = 0
    nodes: int = 0
    candidate_marks: int = 0
    candidate_pairs: int = 0
    legal_children: int = 0
    memo_hits: int = 0
    max_noncentre_marks: int = 0
    deepest_missing_offset: int = 0
    capped: bool = False


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(state: State, geometry: Geometry) -> State:
    """Sort interchangeable free legs without permuting fixed anchor legs."""
    centres = []
    for centre in range(3):
        fixed_count = len(geometry.fixed_caps[centre])
        legs = state.legs[centre]
        fixed = tuple(tuple(sorted(leg)) for leg in legs[:fixed_count])
        free = tuple(sorted(tuple(sorted(leg)) for leg in legs[fixed_count:]))
        centres.append(fixed + free)
    return State(tuple(centres), tuple(sorted(state.spine)))


def vertices(state: State) -> tuple[Vertex, ...]:
    out = []
    for centre, legs in enumerate(state.legs):
        for leg, marks in enumerate(legs):
            out.extend(Vertex("L", centre, leg, x) for x in marks)
    out.extend(Vertex("S", -1, -1, x) for x in state.spine)
    return tuple(out)


def distance_to_centre(vertex: Vertex, centre: int, geometry: Geometry) -> int:
    position = geometry.positions[centre]
    if vertex.kind == "S":
        return abs(vertex.x - position)
    return vertex.x + abs(geometry.positions[vertex.centre] - position)


def pair_distance(first: Vertex, second: Vertex, geometry: Geometry) -> int:
    if first.kind == "S" and second.kind == "S":
        return abs(first.x - second.x)
    if first.kind == "S":
        return second.x + abs(first.x - geometry.positions[second.centre])
    if second.kind == "S":
        return first.x + abs(second.x - geometry.positions[first.centre])
    if first.centre == second.centre and first.leg == second.leg:
        return abs(first.x - second.x)
    core = abs(geometry.positions[first.centre] - geometry.positions[second.centre])
    return first.x + core + second.x


def distance_values(state: State, geometry: Geometry, maximum: int) -> frozenset[int] | None:
    selected = vertices(state)
    raw = [geometry.q1, geometry.q2, geometry.total_core]
    for index, vertex in enumerate(selected):
        raw.extend(distance_to_centre(vertex, centre, geometry) for centre in range(3))
        raw.extend(pair_distance(vertex, other, geometry)
                   for other in selected[index + 1 :])
    if any(value < 1 or value > maximum for value in raw):
        return None
    if len(raw) != len(set(raw)):
        return None
    return frozenset(raw)


def leg_cap(geometry: Geometry, centre: int, leg: int) -> int:
    fixed = geometry.fixed_caps[centre]
    return fixed[leg] if leg < len(fixed) else geometry.fresh_caps[centre]


def slots(state: State) -> tuple[tuple[str, int, int], ...]:
    result = []
    for centre in range(3):
        result.extend(("L", centre, leg) for leg in range(len(state.legs[centre]) + 1))
    result.append(("S", -1, -1))
    return tuple(result)


def coordinates(state: State, geometry: Geometry, slot: tuple[str, int, int]):
    kind, centre, leg = slot
    if kind == "S":
        return (x for x in range(1, geometry.total_core)
                if x != geometry.q1)
    return range(1, leg_cap(geometry, centre, leg) + 1)


def all_positions(state: State, geometry: Geometry):
    for kind, centre, leg in slots(state):
        for x in coordinates(state, geometry, (kind, centre, leg)):
            yield Vertex(kind, centre, leg, x)


def add_raw(state: State, vertex: Vertex) -> State | None:
    if vertex.kind == "S":
        return State(state.legs, state.spine + (vertex.x,))
    all_legs = [list(centre_legs) for centre_legs in state.legs]
    centre_legs = all_legs[vertex.centre]
    if vertex.leg > len(centre_legs):
        return None
    if vertex.leg == len(centre_legs):
        centre_legs.append((vertex.x,))
    else:
        centre_legs[vertex.leg] = centre_legs[vertex.leg] + (vertex.x,)
    return State(tuple(tuple(legs) for legs in all_legs), state.spine)


def partner_coordinates(
    first: Vertex,
    slot: tuple[str, int, int],
    target: int,
    geometry: Geometry,
) -> tuple[int, ...]:
    """Solve d(first, second)=target for the coordinate in ``slot``."""
    kind, centre, leg = slot
    if first.kind == "S":
        if kind == "S":
            return (first.x - target, first.x + target)
        offset = abs(first.x - geometry.positions[centre])
        return (target - offset,)

    first_position = geometry.positions[first.centre]
    if kind == "S":
        delta = target - first.x
        return (first_position - delta, first_position + delta)
    if centre == first.centre and leg == first.leg:
        return (first.x - target, first.x + target)
    core = abs(first_position - geometry.positions[centre])
    return (target - first.x - core,)


def position_is_legal(vertex: Vertex, geometry: Geometry) -> bool:
    if vertex.kind == "S":
        return 0 < vertex.x < geometry.total_core and vertex.x != geometry.q1
    return 1 <= vertex.x <= leg_cap(geometry, vertex.centre, vertex.leg)


def branch_feasible(state: State, n: int) -> bool:
    missing_legs = sum(max(0, required - len(state.legs[centre]))
                       for centre, required in enumerate(REQUIRED_LEGS))
    remaining_vertices = n - 3 - len(vertices(state))
    return missing_legs <= remaining_vertices


def child_states(
    state: State,
    geometry: Geometry,
    target: int,
    n: int,
    maximum: int,
    stats: Stats,
) -> tuple[State, ...]:
    old_count = len(vertices(state))
    out = set()
    first_positions = tuple(all_positions(state, geometry))

    if old_count + 1 <= n - 3:
        for first in first_positions:
            stats.candidate_marks += 1
            state1 = add_raw(state, first)
            if state1 is None:
                continue
            child = canonical(state1, geometry)
            values1 = distance_values(child, geometry, maximum)
            if values1 is not None and target in values1 and branch_feasible(child, n):
                out.add(child)

    if old_count + 2 <= n - 3:
        for first in first_positions:
            state1 = add_raw(state, first)
            if state1 is None:
                continue
            values1 = distance_values(state1, geometry, maximum)
            if values1 is None or target in values1:
                continue
            for slot in slots(state1):
                for x in set(partner_coordinates(first, slot, target, geometry)):
                    second = Vertex(slot[0], slot[1], slot[2], x)
                    stats.candidate_pairs += 1
                    if not position_is_legal(second, geometry) or second == first:
                        continue
                    state2 = add_raw(state1, second)
                    if state2 is None:
                        continue
                    child = canonical(state2, geometry)
                    values2 = distance_values(child, geometry, maximum)
                    if values2 is None or target not in values2 or not branch_feasible(child, n):
                        continue
                    out.add(child)

    stats.legal_children += len(out)
    return tuple(sorted(out, key=repr))


def state_to_edges(state: State, geometry: Geometry) -> tuple[int, list[tuple[int, int, int]]]:
    edges = []
    next_vertex = 3
    spine_vertices = {}
    for coordinate in sorted(state.spine):
        spine_vertices[coordinate] = next_vertex
        next_vertex += 1
    core_points = [(0, 0), (geometry.q1, 1), (geometry.total_core, 2)]
    core_points.extend((coordinate, vertex) for coordinate, vertex in spine_vertices.items())
    core_points.sort()
    for (left_x, left_vertex), (right_x, right_vertex) in zip(core_points, core_points[1:]):
        edges.append((left_vertex, right_vertex, right_x - left_x))

    for centre, legs in enumerate(state.legs):
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


def anchor_geometries(n: int, modes: tuple[str, ...]):
    """Yield the four exhaustive distance-N anchor classes, modulo reflection."""
    maximum = n * (n - 1) // 2
    empty = ()

    if "AA" in modes:
        for long_tip in range(maximum // 2 + 1, maximum):
            short_tip = maximum - long_tip
            for q1 in range(1, short_tip - 1):
                for q2 in range(1, short_tip - q1):
                    total = q1 + q2
                    fresh = (short_tip - 1, short_tip - q1 - 1,
                             short_tip - total - 1)
                    if min(fresh[1:]) < 1:
                        continue
                    geometry = Geometry(q1, q2, ((long_tip, short_tip), empty, empty), fresh)
                    initial = State((((long_tip,), (short_tip,)), empty, empty), empty)
                    yield geometry, initial, {
                        "mode": "AA", "long_tip": long_tip, "short_tip": short_tip,
                    }

    if "BB" in modes:
        for long_tip in range(maximum // 2 + 1, maximum):
            short_tip = maximum - long_tip
            for q1 in range(1, short_tip - 1):
                for q2 in range(q1 + 1, short_tip):
                    fresh = (short_tip - q1 - 1, short_tip - 1,
                             short_tip - q2 - 1)
                    if min(fresh[0], fresh[2]) < 1:
                        continue
                    geometry = Geometry(q1, q2, (empty, (long_tip, short_tip), empty), fresh)
                    initial = State((empty, ((long_tip,), (short_tip,)), empty), empty)
                    yield geometry, initial, {
                        "mode": "BB", "long_tip": long_tip, "short_tip": short_tip,
                    }

    if "AB" in modes:
        for end_tip in range(1, maximum - 2):
            for middle_tip in range(2, maximum - end_tip):
                q1 = maximum - end_tip - middle_tip
                if q1 < 1:
                    continue
                for q2 in range(1, middle_tip):
                    fresh = (
                        min(end_tip - 1, q1 + middle_tip - 1),
                        min(middle_tip - 1, end_tip + q1 - 1),
                        min(middle_tip - q2 - 1, end_tip + q1 - q2 - 1),
                    )
                    if min(fresh[0], fresh[2]) < 1:
                        continue
                    geometry = Geometry(q1, q2, ((end_tip,), (middle_tip,), empty), fresh)
                    initial = State((((end_tip,),), ((middle_tip,),), empty), empty)
                    yield geometry, initial, {
                        "mode": "AB", "end_tip": end_tip, "middle_tip": middle_tip,
                    }

    if "AC" in modes:
        for left_tip in range(1, maximum):
            for right_tip in range(left_tip + 1, maximum - left_tip):
                total = maximum - left_tip - right_tip
                if total < 2:
                    continue
                for q1 in range(1, total):
                    q2 = total - q1
                    fresh = (
                        left_tip - 1,
                        min(q2 + right_tip - 1, left_tip + q1 - 1),
                        min(right_tip - 1, left_tip + total - 1),
                    )
                    if min(fresh) < 1:
                        continue
                    geometry = Geometry(q1, q2, ((left_tip,), empty, (right_tip,)), fresh)
                    initial = State((((left_tip,),), empty, ((right_tip,),)), empty)
                    yield geometry, initial, {
                        "mode": "AC", "left_tip": left_tip, "right_tip": right_tip,
                    }


def solve(
    n: int,
    modes: tuple[str, ...],
    max_nodes: int = 0,
) -> tuple[list[dict], Stats]:
    maximum = n * (n - 1) // 2
    stats = Stats()
    solutions = []
    solved_states = {}

    for geometry, initial, anchor in anchor_geometries(n, modes):
        if stats.capped:
            break
        stats.anchors_generated += 1
        initial = canonical(initial, geometry)
        initial_values = distance_values(initial, geometry, maximum)
        if initial_values is None or not branch_feasible(initial, n):
            continue
        require(maximum in initial_values, f"anchor does not realize N: {anchor}")
        stats.anchors += 1

        def dfs(state: State) -> bool:
            key = (geometry, state)
            if key in solved_states:
                stats.memo_hits += 1
                return solved_states[key]
            if max_nodes and stats.nodes >= max_nodes:
                stats.capped = True
                return False
            stats.nodes += 1
            mark_count = len(vertices(state))
            stats.max_noncentre_marks = max(stats.max_noncentre_marks, mark_count)
            values = distance_values(state, geometry, maximum)
            require(values is not None, f"invalid state reached: {state}")
            missing = next((value for value in range(maximum, 0, -1)
                            if value not in values), 0)
            stats.deepest_missing_offset = max(stats.deepest_missing_offset,
                                               maximum - missing)
            if missing == 0:
                require(all(len(state.legs[c]) >= REQUIRED_LEGS[c] for c in range(3)),
                        "complete state does not have exactly three branch centres")
                edges = verify_witness(state, geometry, n)
                solutions.append({
                    **anchor,
                    "q1": geometry.q1,
                    "q2": geometry.q2,
                    "legs": state.legs,
                    "spine": state.spine,
                    "edges": edges,
                    "checker_a": "PASS",
                    "checker_b": "PASS",
                })
                solved_states[key] = True
                return True
            found = False
            for child in child_states(state, geometry, missing, n, maximum, stats):
                found = dfs(child) or found
                if stats.capped:
                    break
            if not stats.capped:
                solved_states[key] = found
            return found

        dfs(initial)

    return solutions, stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("mode", choices=("AA", "BB", "AB", "AC", "all"),
                        nargs="?", default="all")
    parser.add_argument("--max-nodes", type=int, default=0,
                        help="diagnostic global cap; a capped run is UNKNOWN")
    args = parser.parse_args()
    require(args.n >= 8, "an exactly-three-branch tree needs at least eight vertices")
    require(args.max_nodes >= 0, "--max-nodes must be nonnegative")
    modes = ("AA", "BB", "AB", "AC") if args.mode == "all" else (args.mode,)
    started = monotonic()
    solutions, stats = solve(args.n, modes, args.max_nodes)
    summary = {
        "n": args.n,
        "N": args.n * (args.n - 1) // 2,
        "modes": modes,
        "solutions": len(solutions),
        **stats.__dict__,
        "seconds": round(monotonic() - started, 3),
        "status": "UNKNOWN" if stats.capped else "DONE",
    }
    print(json.dumps(summary, sort_keys=True))
    for solution in solutions:
        print(json.dumps(solution, sort_keys=True))


if __name__ == "__main__":
    main()
