#!/usr/bin/env python3
"""Audit one fixed ``(structure, s, L)`` against necessary conditions.

This is a bounded, structure-aware presolver, not a depth enumerator and not
an existence solver.  A failed layer is a sound rejection of this candidate;
passing every layer is reported only as ``NOT_EXCLUDED`` because LL/LH and
other owners are intentionally outside this module.
"""
from __future__ import annotations

import argparse
import itertools
import json

from colored_moment_hall_audit import audit, ints, parse_struct


def _sets_for_candidate(base: dict, delta: int, s: int, depths: list[int]):
    b = delta + 1 - s
    classes = {"H": set(base["H"])}
    for v, vals in enumerate(base["S"]):
        classes[f"L{v}"] = {2 * b - 2 * depths[v] + a for a in vals}
    return classes


def _allowed_sets(m: int, delta: int, s: int, depths: list[int], occupied: set[int]):
    b = delta + 1 - s
    cap = 2 * m - 3
    out = {"H": set(range(1, cap + 1))}
    for v, lv in enumerate(depths):
        lo = 2 * b - 2 * lv + 1
        hi = lo + cap - 1
        out[f"L{v}"] = set(range(max(1, lo), min(delta, hi) + 1))
    for values in out.values():
        values.difference_update(occupied)
    return out


def _sum_extrema(values: set[int], demand: int):
    ordered = sorted(values)
    if demand < 0 or demand > len(ordered):
        return None
    return sum(ordered[:demand]), sum(ordered[-demand:]) if demand else 0


def presolve(
    lowpar_tail: list[int],
    hpar: list[int],
    delta: int,
    s: int,
    depths: list[int],
    occupied: list[int] | None = None,
    order_n: int = 25,
) -> dict:
    occupied_list = [] if occupied is None else list(occupied)
    if len(set(occupied_list)) != len(occupied_list):
        raise ValueError("duplicate occupied owners")
    if any(x < 1 or x > delta for x in occupied_list):
        raise ValueError("occupied owner outside [1,delta]")

    base = audit(lowpar_tail, hpar, delta, order_n)
    r, m = base["r"], base["m"]
    if r + m + 1 != order_n:
        raise ValueError("structure order r+m+1 does not match order_n")
    if len(depths) != r or depths[0] != 0:
        raise ValueError("depth vector must have length r and start at zero")
    b = delta + 1 - s
    if b <= 0 or any(l < 0 or l >= b for l in depths):
        raise ValueError("depth outside [0,B)")
    if len(set(depths)) != r:
        raise ValueError("low depths must be distinct")
    lowpar = [-1] + list(lowpar_tail)
    if len(lowpar) != r:
        raise ValueError("lowpar/depth length mismatch")
    if any(not (0 <= lowpar[v] < v and depths[v] > depths[lowpar[v]]) for v in range(1, r)):
        raise ValueError("low parent/depth order invalid")

    classes = _sets_for_candidate(base, delta, s, depths)
    exact = {
        "within_range": all(all(1 <= z <= delta for z in vals) for vals in classes.values()),
    }
    # Keep H and each low class aligned explicitly; a positional comprehension
    # here is easy to get wrong because classes contains H first.
    exact["H_internal_unique"] = len(classes["H"]) == len(base["H"])
    exact["T_internal_unique"] = all(
        len(classes[f"L{v}"]) == len(base["S"][v]) for v in range(r)
    )
    exact["internal_unique"] = exact["H_internal_unique"] and exact["T_internal_unique"]
    exact["pairwise_disjoint"] = all(
        classes[a].isdisjoint(classes[b])
        for a, b in itertools.combinations(classes, 2)
    )
    if occupied_list:
        occ = set(occupied_list)
        exact["occupied_disjoint"] = all(not vals & occ for vals in classes.values())
    else:
        exact["occupied_disjoint"] = True
    exact["necessary_pass"] = all(exact.values())

    allowed = _allowed_sets(m, delta, s, depths, set(occupied_list))
    names = ["H"] + [f"L{v}" for v in range(r)]
    demands = {"H": len(base["H"])}
    demands.update({f"L{v}": len(base["S"][v]) for v in range(r)})
    class_sums = {"H": sum(base["H"])}
    class_sums.update({
        f"L{v}": len(base["S"][v]) * (2 * b - 2 * depths[v]) + sum(base["S"][v])
        for v in range(r)
    })
    class_parity = {
        "H": (sum(x % 2 == 0 for x in base["H"]), sum(x % 2 for x in base["H"]))
    }
    class_parity.update({
        f"L{v}": (
            sum(x % 2 == 0 for x in base["S"][v]),
            sum(x % 2 for x in base["S"][v]),
        ) for v in range(r)
    })

    hall_failures = []
    parity_failures = []
    moment_failures = []
    for mask in range(1, 1 << len(names)):
        q = [names[i] for i in range(len(names)) if mask & (1 << i)]
        demand = sum(demands[name] for name in q)
        union = set().union(*(allowed[name] for name in q))
        if demand > len(union):
            hall_failures.append({"classes": q, "demand": demand, "capacity": len(union)})
        even_demand = sum(class_parity[name][0] for name in q)
        odd_demand = sum(class_parity[name][1] for name in q)
        even_capacity = sum(x % 2 == 0 for x in union)
        odd_capacity = sum(x % 2 for x in union)
        if even_demand > even_capacity or odd_demand > odd_capacity:
            parity_failures.append({
                "classes": q,
                "demand_even": even_demand,
                "capacity_even": even_capacity,
                "demand_odd": odd_demand,
                "capacity_odd": odd_capacity,
            })
        lo_hi = _sum_extrema(union, demand)
        if lo_hi is None or not (lo_hi[0] <= sum(class_sums[name] for name in q) <= lo_hi[1]):
            moment_failures.append({
                "classes": q,
                "demand": demand,
                "capacity": len(union),
                "sum": sum(class_sums[name] for name in q),
                "bounds": lo_hi,
            })

    affine = base["wiener_affine"]
    wiener_value = affine["const"] + affine["s"] * s + sum(
        affine[f"l{v}"] * depths[v] for v in range(1, r)
    )
    vertex_depths = list(depths) + [b + y for y in range(m)] + [s]
    odd_vertices = sum(d % 2 for d in vertex_depths)
    pair_count = order_n * (order_n - 1) // 2
    target_odd_pairs = (pair_count + 1) // 2
    parity_ok = odd_vertices * (order_n - odd_vertices) == target_odd_pairs
    checks = {
        "exact_translation": exact,
        "hall": {"checked": (1 << len(names)) - 1, "failures": hall_failures},
        "parity_hall": {"failures": parity_failures},
        "moment_hall": {"failures": moment_failures},
        "global_parity": {
            "odd_vertices": odd_vertices,
            "odd_pairs": odd_vertices * (order_n - odd_vertices),
            "target_odd_pairs": target_odd_pairs,
            "ok": parity_ok,
        },
        "wiener": {"value": wiener_value, "target": base["wiener_target"], "ok": wiener_value == base["wiener_target"]},
    }
    necessary_pass = (
        exact["necessary_pass"]
        and not hall_failures
        and not parity_failures
        and not moment_failures
        and parity_ok
        and checks["wiener"]["ok"]
    )
    failure_layers = []
    if not exact["necessary_pass"]:
        failure_layers.append("exact_translation")
    if hall_failures:
        failure_layers.append("hall")
    if parity_failures:
        failure_layers.append("parity_hall")
    if moment_failures:
        failure_layers.append("moment_hall")
    if not parity_ok:
        failure_layers.append("global_parity")
    if not checks["wiener"]["ok"]:
        failure_layers.append("wiener")
    return {
        "status": "COLORED_MOMENT_HALL_PRESOLVE",
        "m": m,
        "r": r,
        "delta": delta,
        "s": s,
        "depths": depths,
        "occupied": sorted(occupied_list),
        "checks": checks,
        "necessary_pass": necessary_pass,
        "failure_layers": failure_layers,
        "interpretation": "NOT-EXCLUDED" if necessary_pass else "UNSAT_FOR_THIS_CANDIDATE",
        "source_scope": "one fixed (structure,s,L); necessary system only, not existence proof",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lowpar", required=True)
    ap.add_argument("--struct", required=True)
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--depths", required=True)
    ap.add_argument("--occupied", default="")
    ap.add_argument("--order-n", type=int, default=25)
    args = ap.parse_args()
    out = presolve(
        ints(args.lowpar), parse_struct(args.struct), args.delta, args.s,
        ints(args.depths), ints(args.occupied) if args.occupied else [], args.order_n,
    )
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
