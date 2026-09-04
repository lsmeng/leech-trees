#!/usr/bin/env python3
"""Prototype Presburger top-window search for three-centre trees.

This is an UNVERIFIED research probe, not a certificate.  It replaces the
numeric diameter ``N`` and the three free anchor parameters by integer
variables.  For a fixed window, every candidate introduced by a diameter
endpoint has an affine coordinate.  Tree distances are therefore piecewise
affine, and Z3 checks the resulting quantifier-free integer constraints.

The search deliberately omits the finite-order remaining-vertex prune.  This
is a relaxation: closing it for every integer ``N >= Nmin`` would be stronger
than closing only triangular ``N=n(n-1)/2`` at each order.  A surviving model
is merely a top-window partial geometry, never a Leech-tree witness.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Iterable

import z3


NCOEFF = 5  # N, p1, p2, p3, constant


@dataclass(frozen=True, order=True)
class Affine:
    coefficients: tuple[int, int, int, int, int]

    def __add__(self, other: "Affine") -> "Affine":
        return Affine(tuple(a + b for a, b in zip(
            self.coefficients, other.coefficients
        )))

    def __sub__(self, other: "Affine") -> "Affine":
        return Affine(tuple(a - b for a, b in zip(
            self.coefficients, other.coefficients
        )))

    def __neg__(self) -> "Affine":
        return Affine(tuple(-a for a in self.coefficients))

    def scale(self, multiplier: int) -> "Affine":
        return Affine(tuple(multiplier * a for a in self.coefficients))

    def z3(self, variables: tuple[z3.IntNumRef, ...]):
        return sum(
            coefficient * variable
            for coefficient, variable in zip(
                self.coefficients[:-1], variables
            )
        ) + self.coefficients[-1]


def basis(index: int) -> Affine:
    coefficients = [0] * NCOEFF
    coefficients[index] = 1
    return Affine(tuple(coefficients))


N_FORM = basis(0)
P1 = basis(1)
P2 = basis(2)
P3 = basis(3)
ONE = basis(4)
ZERO = ONE.scale(0)
REQUIRED_LEGS = (2, 1, 2)


@dataclass(frozen=True, order=True)
class Vertex:
    kind: str  # L for leg, S for core spine
    centre: int
    leg: int
    x: Affine


@dataclass(frozen=True)
class Geometry:
    mode: str
    q1: Affine
    q2: Affine
    fixed_caps: tuple[tuple[Affine, ...], tuple[Affine, ...], tuple[Affine, ...]]
    # A fresh cap can be a minimum; x is legal iff it is below every entry.
    fresh_cap_bounds: tuple[
        tuple[Affine, ...], tuple[Affine, ...], tuple[Affine, ...]
    ]
    endpoints: tuple[Vertex, Vertex]

    @property
    def positions(self) -> tuple[Affine, Affine, Affine]:
        return (ZERO, self.q1, self.q1 + self.q2)

    @property
    def core_total(self) -> Affine:
        return self.q1 + self.q2


@dataclass(frozen=True)
class State:
    legs: tuple[
        tuple[tuple[Affine, ...], ...],
        tuple[tuple[Affine, ...], ...],
        tuple[tuple[Affine, ...], ...],
    ]
    spine: tuple[Affine, ...]


@dataclass
class Stats:
    mode: str
    nmin: int
    fixed_n: int | None
    requested_window: int
    triangular_tail: bool = False
    taylor_tail: bool = False
    taylor_residue_modulus: int = 0
    scale_shards: tuple[tuple[int, int, int], ...] = ()
    solver_calls: int = 0
    candidates: int = 0
    feasible_children: int = 0
    maximum_states: int = 1
    maximum_marks: int = 2
    completed_offset: int = 0
    solver_unknown: int = 0
    capped: bool = False


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def affine_abs(expression):
    return z3.If(expression >= 0, expression, -expression)


def canonical(state: State, geometry: Geometry) -> State:
    centres = []
    for centre in range(3):
        fixed_count = len(geometry.fixed_caps[centre])
        legs = state.legs[centre]
        fixed = tuple(tuple(sorted(leg)) for leg in legs[:fixed_count])
        free = tuple(sorted(tuple(sorted(leg)) for leg in legs[fixed_count:]))
        centres.append(fixed + free)
    return State(tuple(centres), tuple(sorted(state.spine)))


def vertices(state: State) -> tuple[Vertex, ...]:
    selected = []
    for centre, legs in enumerate(state.legs):
        for leg, marks in enumerate(legs):
            selected.extend(Vertex("L", centre, leg, x) for x in marks)
    selected.extend(Vertex("S", -1, -1, x) for x in state.spine)
    return tuple(selected)


def finite_order_branch_feasible(state: State, fixed_n: int | None) -> bool:
    """Mirror the exact engine's discrete vertex-budget prune when requested."""

    if fixed_n is None:
        return True
    missing_legs = sum(
        max(0, required - len(state.legs[centre]))
        for centre, required in enumerate(REQUIRED_LEGS)
    )
    remaining_vertices = fixed_n - 3 - len(vertices(state))
    return missing_legs <= remaining_vertices


def distance_to_centre(vertex: Vertex, centre: int, geometry: Geometry, variables):
    position = geometry.positions[centre]
    if vertex.kind == "S":
        return affine_abs((vertex.x - position).z3(variables))
    left, right = sorted((vertex.centre, centre))
    core = geometry.positions[right] - geometry.positions[left]
    return (vertex.x + core).z3(variables)


def pair_distance(first: Vertex, second: Vertex, geometry: Geometry, variables):
    if first.kind == "S" and second.kind == "S":
        return affine_abs((first.x - second.x).z3(variables))
    if first.kind == "S":
        position = geometry.positions[second.centre]
        return second.x.z3(variables) + affine_abs(
            (first.x - position).z3(variables)
        )
    if second.kind == "S":
        position = geometry.positions[first.centre]
        return first.x.z3(variables) + affine_abs(
            (second.x - position).z3(variables)
        )
    if first.centre == second.centre and first.leg == second.leg:
        return affine_abs((first.x - second.x).z3(variables))
    left, right = sorted((first.centre, second.centre))
    core = geometry.positions[right] - geometry.positions[left]
    return (first.x + second.x + core).z3(variables)


def distance_values(state: State, geometry: Geometry, variables):
    selected = vertices(state)
    values = [
        geometry.q1.z3(variables),
        geometry.q2.z3(variables),
        geometry.core_total.z3(variables),
    ]
    for index, vertex in enumerate(selected):
        values.extend(
            distance_to_centre(vertex, centre, geometry, variables)
            for centre in range(3)
        )
        values.extend(
            pair_distance(vertex, other, geometry, variables)
            for other in selected[index + 1:]
        )
    return tuple(values)


def extension_values(vertex: Vertex, state: State, geometry: Geometry, variables):
    """Distances created by adding ``vertex`` to the old symbolic state."""

    values = [
        distance_to_centre(vertex, centre, geometry, variables)
        for centre in range(3)
    ]
    values.extend(
        pair_distance(vertex, old, geometry, variables)
        for old in vertices(state)
    )
    return tuple(values)


def state_constraints(state: State, geometry: Geometry, variables):
    values = distance_values(state, geometry, variables)
    maximum = variables[0]
    return z3.And(
        *(value >= 1 for value in values),
        *(value <= maximum for value in values),
        z3.Distinct(*values),
    )


def extension_constraints(vertex: Vertex, state: State, geometry: Geometry, variables):
    """Incremental form of the full range/distinct-distance test."""

    old_values = distance_values(state, geometry, variables)
    new_values = extension_values(vertex, state, geometry, variables)
    maximum = variables[0]
    return (
        *(value >= 1 for value in new_values),
        *(value <= maximum for value in new_values),
        z3.Distinct(*new_values),
        *(new != old for new in new_values for old in old_values),
    )


def slots(state: State) -> tuple[tuple[str, int, int], ...]:
    result = []
    for centre in range(3):
        result.extend(
            ("L", centre, leg)
            for leg in range(len(state.legs[centre]) + 1)
        )
    result.append(("S", -1, -1))
    return tuple(result)


def cap_bounds(geometry: Geometry, centre: int, leg: int) -> tuple[Affine, ...]:
    fixed = geometry.fixed_caps[centre]
    if leg < len(fixed):
        return (fixed[leg],)
    return geometry.fresh_cap_bounds[centre]


def legal_position(vertex: Vertex, geometry: Geometry, variables):
    x = vertex.x.z3(variables)
    if vertex.kind == "S":
        return z3.And(
            x > 0,
            x < geometry.core_total.z3(variables),
            x != geometry.q1.z3(variables),
        )
    return z3.And(
        x >= 1,
        *(x <= bound.z3(variables) for bound in cap_bounds(
            geometry, vertex.centre, vertex.leg
        )),
    )


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


def candidate_vertices(
    state: State,
    geometry: Geometry,
    target: Affine,
) -> tuple[Vertex, ...]:
    candidates = set()
    positions = geometry.positions
    for old in geometry.endpoints:
        require(old.kind == "L", old)
        old_position = positions[old.centre]
        for kind, centre, leg in slots(state):
            if kind == "S":
                delta = target - old.x
                candidates.add(Vertex("S", -1, -1, old_position - delta))
                candidates.add(Vertex("S", -1, -1, old_position + delta))
            elif centre == old.centre and leg == old.leg:
                candidates.add(Vertex("L", centre, leg, old.x - target))
                candidates.add(Vertex("L", centre, leg, old.x + target))
            else:
                left, right = sorted((old.centre, centre))
                core = positions[right] - positions[left]
                candidates.add(Vertex("L", centre, leg, target - old.x - core))
    return tuple(sorted(candidates))


def merge_region(regions: dict[State, z3.BoolRef], state: State, formula) -> None:
    if state in regions:
        regions[state] = z3.Or(regions[state], formula)
    else:
        regions[state] = formula


def build_mode(mode: str, variables, nmin: int, fixed_n: int | None):
    fixed_maximum = fixed_n * (fixed_n - 1) // 2 if fixed_n is not None else None
    maximum = ONE.scale(fixed_maximum) if fixed_maximum is not None else N_FORM
    p1, p2, p3 = (basis(i) for i in range(1, 4))
    constraints = [variables[0] >= nmin]
    if fixed_n is not None:
        constraints.append(variables[0] == fixed_n * (fixed_n - 1) // 2)
    empty: tuple[Affine, ...] = ()

    if mode in {"AA", "BB"}:
        long_tip, q1, q2 = p1, p2, p3
        short_tip = maximum - long_tip
        constraints.extend([
            long_tip.z3(variables) < maximum.z3(variables),
            long_tip.scale(2).z3(variables) > maximum.z3(variables),
            q1.z3(variables) >= 1,
            q1.z3(variables) < (short_tip - ONE).z3(variables),
            q2.z3(variables) >= 1,
        ])
        if mode == "AA":
            constraints.extend([
                q2.z3(variables) < (short_tip - q1).z3(variables),
                (short_tip - q1 - ONE).z3(variables) >= 1,
                (short_tip - q1 - q2 - ONE).z3(variables) >= 1,
            ])
            geometry = Geometry(
                mode, q1, q2,
                ((long_tip, short_tip), empty, empty),
                ((short_tip - ONE,),
                 (short_tip - q1 - ONE,),
                 (short_tip - q1 - q2 - ONE,)),
                (Vertex("L", 0, 0, long_tip), Vertex("L", 0, 1, short_tip)),
            )
            state = State((((long_tip,), (short_tip,)), empty, empty), empty)
        else:
            constraints.extend([
                q2.z3(variables) > q1.z3(variables),
                q2.z3(variables) < short_tip.z3(variables),
                (short_tip - q1 - ONE).z3(variables) >= 1,
                (short_tip - q2 - ONE).z3(variables) >= 1,
            ])
            geometry = Geometry(
                mode, q1, q2,
                (empty, (long_tip, short_tip), empty),
                ((short_tip - q1 - ONE,),
                 (short_tip - ONE,),
                 (short_tip - q2 - ONE,)),
                (Vertex("L", 1, 0, long_tip), Vertex("L", 1, 1, short_tip)),
            )
            state = State((empty, ((long_tip,), (short_tip,)), empty), empty)
    elif mode == "AB":
        end_tip, middle_tip, q2 = p1, p2, p3
        q1 = maximum - end_tip - middle_tip
        constraints.extend([
            end_tip.z3(variables) >= 1,
            middle_tip.z3(variables) >= 2,
            q1.z3(variables) >= 1,
            q2.z3(variables) >= 1,
            q2.z3(variables) < middle_tip.z3(variables),
            (end_tip - ONE).z3(variables) >= 1,
            (q1 + middle_tip - ONE).z3(variables) >= 1,
            (middle_tip - q2 - ONE).z3(variables) >= 1,
            (end_tip + q1 - q2 - ONE).z3(variables) >= 1,
        ])
        geometry = Geometry(
            mode, q1, q2,
            ((end_tip,), (middle_tip,), empty),
            ((end_tip - ONE, q1 + middle_tip - ONE),
             (middle_tip - ONE, end_tip + q1 - ONE),
             (middle_tip - q2 - ONE, end_tip + q1 - q2 - ONE)),
            (Vertex("L", 0, 0, end_tip), Vertex("L", 1, 0, middle_tip)),
        )
        state = State((((end_tip,),), ((middle_tip,),), empty), empty)
    elif mode == "AC":
        left_tip, right_tip, q1 = p1, p2, p3
        total = maximum - left_tip - right_tip
        q2 = total - q1
        constraints.extend([
            left_tip.z3(variables) >= 1,
            right_tip.z3(variables) > left_tip.z3(variables),
            right_tip.z3(variables) < (maximum - left_tip).z3(variables),
            total.z3(variables) >= 2,
            q1.z3(variables) >= 1,
            q1.z3(variables) < total.z3(variables),
            (left_tip - ONE).z3(variables) >= 1,
            (q2 + right_tip - ONE).z3(variables) >= 1,
            (left_tip + q1 - ONE).z3(variables) >= 1,
            (right_tip - ONE).z3(variables) >= 1,
            (left_tip + total - ONE).z3(variables) >= 1,
        ])
        geometry = Geometry(
            mode, q1, q2,
            ((left_tip,), empty, (right_tip,)),
            ((left_tip - ONE,),
             (q2 + right_tip - ONE, left_tip + q1 - ONE),
             (right_tip - ONE, left_tip + total - ONE)),
            (Vertex("L", 0, 0, left_tip), Vertex("L", 2, 0, right_tip)),
        )
        state = State((((left_tip,),), empty, ((right_tip,),)), empty)
    else:
        raise ValueError(mode)

    state = canonical(state, geometry)
    require(finite_order_branch_feasible(state, fixed_n), (mode, fixed_n, state))
    constraints.append(state_constraints(state, geometry, variables))
    return geometry, state, z3.And(*constraints)


def prove_mode(
    mode: str,
    *,
    nmin: int,
    fixed_n: int | None,
    window: int,
    timeout_ms: int,
    max_states: int,
    progress: bool,
    triangular_tail: bool,
    taylor_tail: bool,
    taylor_residue_modulus: int,
    scale_shards: tuple[tuple[int, int, int], ...],
):
    require(not taylor_tail or triangular_tail, "Taylor tail requires triangular tail")
    variables = tuple(z3.Int(name) for name in ("N", "p1", "p2", "p3"))
    geometry, initial, base = build_mode(mode, variables, nmin, fixed_n)
    order_variable = z3.Int("n") if triangular_tail else None
    taylor_root = z3.Int("m") if taylor_tail else None
    if order_variable is not None:
        base = z3.And(
            base,
            order_variable >= 18,
            2 * variables[0] == order_variable * (order_variable - 1),
        )
    if taylor_root is not None:
        base = z3.And(
            base,
            taylor_root >= 1,
            z3.Or(
                order_variable == taylor_root * taylor_root,
                order_variable == taylor_root * taylor_root + 2,
            ),
        )
    if taylor_residue_modulus:
        modulus = taylor_residue_modulus
        allowed_residues = sorted({
            (order * (order - 1) // 2) % modulus
            for root in range(2 * modulus)
            for order in (root * root, root * root + 2)
        })
        base = z3.And(
            base,
            z3.Or(*(
                variables[0] % modulus == residue
                for residue in allowed_residues
            )),
        )
    for axis, index, count in scale_shards:
        parameter = variables[axis]
        base = z3.And(
            base,
            count * parameter >= index * variables[0],
            count * parameter < (index + 1) * variables[0],
        )
    stats = Stats(
        mode, nmin, fixed_n, window,
        triangular_tail=triangular_tail,
        taylor_tail=taylor_tail,
        taylor_residue_modulus=taylor_residue_modulus,
        scale_shards=scale_shards,
    )

    def feasible(formula):
        stats.solver_calls += 1
        solver = z3.Solver()
        if timeout_ms:
            solver.set(timeout=timeout_ms)
        solver.add(formula)
        status = solver.check()
        if status == z3.unknown:
            stats.solver_unknown += 1
            raise RuntimeError(("solver unknown", solver.reason_unknown()))
        return status == z3.sat, solver.model() if status == z3.sat else None

    def check_solver(solver: z3.Solver, *extra):
        stats.solver_calls += 1
        solver.push()
        solver.add(*extra)
        status = solver.check()
        model = solver.model() if status == z3.sat else None
        solver.pop()
        if status == z3.unknown:
            stats.solver_unknown += 1
            raise RuntimeError(("solver unknown", solver.reason_unknown()))
        return status == z3.sat, model

    ok, model = feasible(base)
    if not ok:
        return stats, {}, None
    regions: dict[State, z3.BoolRef] = {initial: base}
    last_model = model
    maximum_form = (
        ONE.scale(fixed_n * (fixed_n - 1) // 2)
        if fixed_n is not None else N_FORM
    )
    for offset in range(1, window + 1):
        target = maximum_form - ONE.scale(offset)
        target_z3 = target.z3(variables)
        next_regions: dict[State, z3.BoolRef] = {}
        for state, region in regions.items():
            values = distance_values(state, geometry, variables)
            present = z3.Or(*(value == target_z3 for value in values))
            present_region = z3.And(region, present)
            solver = z3.Solver()
            if timeout_ms:
                solver.set(timeout=timeout_ms)
            solver.add(region)
            ok, model = check_solver(solver, present)
            if ok:
                merge_region(next_regions, state, present_region)
                last_model = model
                if max_states and len(next_regions) > max_states:
                    stats.capped = True
                    break

            missing_region = z3.And(region, z3.Not(present))
            solver.add(z3.Not(present))
            stats.solver_calls += 1
            missing_status = solver.check()
            if missing_status == z3.unknown:
                stats.solver_unknown += 1
                raise RuntimeError(("solver unknown", solver.reason_unknown()))
            missing_ok = missing_status == z3.sat
            if not missing_ok:
                continue
            for candidate in candidate_vertices(state, geometry, target):
                stats.candidates += 1
                raw_child = add_raw(state, candidate)
                require(raw_child is not None, candidate)
                child = canonical(raw_child, geometry)
                if not finite_order_branch_feasible(child, fixed_n):
                    continue
                created = extension_values(candidate, state, geometry, variables)
                extension = (
                    legal_position(candidate, geometry, variables),
                    *extension_constraints(candidate, state, geometry, variables),
                    z3.Or(*(value == target_z3 for value in created)),
                )
                ok, model = check_solver(solver, *extension)
                if ok:
                    stats.feasible_children += 1
                    child_region = z3.And(missing_region, *extension)
                    merge_region(next_regions, child, child_region)
                    last_model = model
                    if max_states and len(next_regions) > max_states:
                        stats.capped = True
                        break

            if stats.capped:
                break

        regions = next_regions
        stats.completed_offset = offset
        stats.maximum_states = max(stats.maximum_states, len(regions))
        if regions:
            stats.maximum_marks = max(
                stats.maximum_marks,
                max(len(vertices(state)) for state in regions),
            )
        if progress:
            print(json.dumps({
                "mode": mode,
                "offset": offset,
                "states": len(regions),
                "maximum_marks": stats.maximum_marks,
                "solver_calls": stats.solver_calls,
            }, sort_keys=True), flush=True)
        if stats.capped:
            break
        if not regions:
            break

    model_row = None
    if regions and last_model is not None:
        model_row = {
            str(variable): last_model.eval(variable, model_completion=True).as_long()
            for variable in variables
        }
        if order_variable is not None:
            model_row["n"] = last_model.eval(
                order_variable, model_completion=True
            ).as_long()
        if taylor_root is not None:
            model_row["m"] = last_model.eval(
                taylor_root, model_completion=True
            ).as_long()
    return stats, regions, model_row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("AA", "BB", "AB", "AC", "all"),
                        default="all")
    parser.add_argument("--window", type=int, default=8)
    parser.add_argument("--nmin", type=int, default=153,
                        help="minimum numeric diameter N for the relaxed tail")
    parser.add_argument("--fixed-order", type=int)
    parser.add_argument("--timeout-ms", type=int, default=10_000)
    parser.add_argument("--max-states", type=int, default=20_000)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--triangular-tail", action="store_true",
                        help="require N=n(n-1)/2 for an integer n>=18")
    parser.add_argument("--taylor-tail", action="store_true",
                        help="also require the literature order form n=m^2 or m^2+2")
    parser.add_argument("--taylor-residue-modulus", type=int, default=0,
                        help="cheap necessary Taylor filter on N modulo this integer")
    parser.add_argument("--p1-shard", type=int, nargs=2, metavar=("INDEX", "COUNT"))
    parser.add_argument("--p2-shard", type=int, nargs=2, metavar=("INDEX", "COUNT"))
    parser.add_argument("--p3-shard", type=int, nargs=2, metavar=("INDEX", "COUNT"))
    args = parser.parse_args()
    require(args.window >= 1 and args.nmin >= 1, args)
    require(args.fixed_order is None or args.fixed_order >= 8, args.fixed_order)
    require(not args.triangular_tail or args.fixed_order is None,
            "do not combine --fixed-order and --triangular-tail")
    require(not args.taylor_tail or args.triangular_tail,
            "--taylor-tail requires --triangular-tail")
    require(args.taylor_residue_modulus >= 0, args.taylor_residue_modulus)
    scale_shards = []
    for axis, shard in enumerate(
        (args.p1_shard, args.p2_shard, args.p3_shard), start=1
    ):
        if shard is None:
            continue
        index, count = shard
        require(count >= 1 and 0 <= index < count, (axis, shard))
        scale_shards.append((axis, index, count))
    require(args.timeout_ms >= 0 and args.max_states >= 0, args)

    modes: Iterable[str] = ("AA", "BB", "AB", "AC") \
        if args.mode == "all" else (args.mode,)
    output = []
    for mode in modes:
        stats, regions, model = prove_mode(
            mode,
            nmin=args.nmin,
            fixed_n=args.fixed_order,
            window=args.window,
            timeout_ms=args.timeout_ms,
            max_states=args.max_states,
            progress=args.progress,
            triangular_tail=args.triangular_tail,
            taylor_tail=args.taylor_tail,
            taylor_residue_modulus=args.taylor_residue_modulus,
            scale_shards=tuple(scale_shards),
        )
        row = {
            **stats.__dict__,
            "frontier_states": len(regions),
            "example_model": model,
            "status": (
                "UNKNOWN" if stats.capped or stats.solver_unknown
                else "CLOSED" if not regions
                else "FRONTIER"
            ),
            "claim_boundary": (
                "UNVERIFIED relaxed parametric top-window probe; a frontier is "
                "not a Leech witness and CLOSED needs an independent checker"
            ),
        }
        output.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
