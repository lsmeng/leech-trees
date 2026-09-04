#!/usr/bin/env python3
"""Conservative audit for *domains* of low depths.

This is intentionally not a depth enumerator or an existence solver.  For
each low class it takes the union of translated slots over its current depth
domain.  All reported rejections are necessary-condition rejections for the
whole domain box; a pass means only ``NOT-EXCLUDED``.  The union loses
correlations between depths, so it is safe but deliberately incomplete.
"""
from __future__ import annotations

import argparse
import itertools
import json
from math import gcd
from typing import Iterable

from colored_moment_hall_audit import audit, ints, parse_struct


def parse_domains(text: str) -> list[list[int]]:
    """Parse ``0;1,2,3;4`` into sorted finite domains."""
    if not text:
        raise ValueError("--domains must contain one domain per low vertex")
    out: list[list[int]] = []
    for raw in text.split(";"):
        vals = sorted(set(int(x.strip()) for x in raw.split(",") if x.strip()))
        if not vals:
            raise ValueError("empty low-depth domain")
        out.append(vals)
    return out


def _matching_exists(domains: list[list[int]]) -> bool:
    """Small bipartite matching check for pairwise distinct low depths."""
    owner: dict[int, int] = {}

    def visit(i: int, seen: set[int]) -> bool:
        for value in domains[i]:
            if value in seen:
                continue
            seen.add(value)
            if value not in owner or visit(owner[value], seen):
                owner[value] = i
                return True
        return False

    for i in sorted(range(len(domains)), key=lambda k: len(domains[k])):
        if not visit(i, set()):
            return False
    return True


def _possible_parity_counts(domains: list[list[int]]) -> list[int]:
    counts = {0}
    for domain in domains:
        counts = {old + (value % 2) for old in counts for value in domain}
    return sorted(counts)


def _affine_range_and_gcd(
    const: int, terms: Iterable[tuple[int, list[int]]]
) -> tuple[int, int, int]:
    """Return an interval and a safe congruence gcd for an affine image."""
    lo = hi = const
    gcd_value = 0
    for coeff, domain in terms:
        values = [coeff * value for value in domain]
        lo += min(values)
        hi += max(values)
        base = values[0]
        for value in values[1:]:
            # gcd of all attainable increments is a necessary, not sufficient,
            # description when a domain is non-arithmetic.
            gcd_value = gcd(gcd_value, abs(value - base))
    return lo, hi, gcd_value


def _range_sum(values: set[int], demand: int) -> tuple[int, int] | None:
    ordered = sorted(values)
    if demand < 0 or demand > len(ordered):
        return None
    return (
        sum(ordered[:demand]),
        sum(ordered[-demand:]) if demand else 0,
    )


def audit_domains(
    lowpar_tail: list[int],
    hpar: list[int],
    delta: int,
    s: int,
    domains: list[list[int]],
    occupied: list[int] | None = None,
    order_n: int = 25,
    subset_cap: int = 1 << 16,
) -> dict:
    occupied_set = set(occupied or [])
    if len(occupied_set) != len(occupied or []):
        raise ValueError("duplicate occupied owner")
    if any(value < 1 or value > delta for value in occupied_set):
        raise ValueError("occupied owner outside [1,delta]")

    base = audit(lowpar_tail, hpar, delta, order_n)
    r, m = base["r"], base["m"]
    if r + m + 1 != order_n:
        raise ValueError("structure order r+m+1 does not match order_n")
    if len(domains) != r:
        raise ValueError(f"need {r} low-depth domains, got {len(domains)}")
    b = delta + 1 - s
    if b <= 0 or any(value < 0 or value >= b for d in domains for value in d):
        raise ValueError("depth domain contains a value outside [0,B)")
    if domains[0] != [0]:
        raise ValueError("root low-depth domain must be exactly 0")
    lowpar = [-1] + list(lowpar_tail)
    if len(lowpar) != r:
        raise ValueError("low parent/domain length mismatch")
    if any(not (0 <= lowpar[v] < v) for v in range(1, r)):
        raise ValueError("low parent must be an earlier low vertex")

    failures: list[dict] = []
    if not base["partition_ok"]:
        failures.append({"layer": "structure", "reason": "H/S pair partition incomplete"})
    if not base["H_unique"] or not all(base["S_unique"]):
        failures.append({"layer": "structure", "reason": "raw H/S collision"})
    if any(value < 1 or value > delta for value in base["H"]):
        failures.append({"layer": "exact_translation", "reason": "fixed H outside [1,delta]"})
    if not set(base["H"]).isdisjoint(occupied_set):
        failures.append({"layer": "occupied", "reason": "occupied slot lies in fixed H"})
    if not _matching_exists(domains):
        failures.append({"layer": "distinct_depths", "reason": "no injective depth assignment"})
    for v in range(1, r):
        if not any(child > parent for parent in domains[lowpar[v]] for child in domains[v]):
            failures.append({
                "layer": "parent_depth",
                "vertex": v,
                "parent": lowpar[v],
                "reason": "no allowed child depth above parent",
            })

    # Fixed H and a union over every depth in each low domain.  Removing H and
    # occupied slots is essential: those owners are present in every
    # realization, so they cannot be used by a low class.
    classes = {"H": set(base["H"])}
    possible = {"H": set(base["H"])}
    for v, vals in enumerate(base["S"]):
        slots = {
            2 * b - 2 * depth + raw
            for depth in domains[v]
            for raw in vals
        }
        possible[f"L{v}"] = slots - occupied_set - set(base["H"])
        classes[f"L{v}"] = possible[f"L{v}"]

    for name, values in possible.items():
        if any(value < 1 or value > delta for value in values):
            # Out-of-range values are simply unavailable in the actual slot
            # domain; retain only legal slots and report the domain as broad.
            possible[name] = {value for value in values if 1 <= value <= delta}

    names = ["H"] + [f"L{v}" for v in range(r)]
    demands = {"H": len(base["H"])}
    demands.update({f"L{v}": len(base["S"][v]) for v in range(r)})
    cap = 2 * m - 3
    component_failures = []
    if demands["H"] > cap:
        component_failures.append({"class": "H", "demand": demands["H"], "capacity": cap})
    for v in range(r):
        if demands[f"L{v}"] > cap:
            component_failures.append({
                "class": f"L{v}", "demand": demands[f"L{v}"] , "capacity": cap,
            })
    parity = {
        "H": (
            sum(value % 2 == 0 for value in base["H"]),
            sum(value % 2 for value in base["H"]),
        )
    }
    parity.update({
        f"L{v}": (
            sum(value % 2 == 0 for value in base["S"][v]),
            sum(value % 2 for value in base["S"][v]),
        )
        for v in range(r)
    })

    subset_total = (1 << len(names)) - 1
    subset_masks = range(1, min(subset_total, subset_cap) + 1)
    subset_complete = subset_total <= subset_cap
    hall_failures: list[dict] = []
    parity_failures: list[dict] = []
    moment_failures: list[dict] = []
    demand_span_failures: list[dict] = []
    for mask in subset_masks:
        selected = [names[i] for i in range(len(names)) if mask & (1 << i)]
        demand = sum(demands[name] for name in selected)
        union = set().union(*(possible[name] for name in selected))
        if demand > len(union):
            hall_failures.append({
                "classes": selected,
                "demand": demand,
                "capacity": len(union),
            })
        even_demand = sum(parity[name][0] for name in selected)
        odd_demand = sum(parity[name][1] for name in selected)
        even_capacity = sum(value % 2 == 0 for value in union)
        odd_capacity = sum(value % 2 for value in union)
        if even_demand > even_capacity or odd_demand > odd_capacity:
            parity_failures.append({
                "classes": selected,
                "demand_even": even_demand,
                "capacity_even": even_capacity,
                "demand_odd": odd_demand,
                "capacity_odd": odd_capacity,
            })

        # The exact class sum is affine in each depth.  Use its broadest
        # interval over the domain box; disjointness from the slot-sum bounds
        # is therefore a sound rejection, while overlap is only unknown.
        fixed_sum = sum(base["H"]) if "H" in selected else 0
        min_sum = max_sum = fixed_sum
        for name in selected:
            if name == "H":
                continue
            v = int(name[1:])
            p = len(base["S"][v])
            raw_sum = sum(base["S"][v])
            values = [p * (2 * b - 2 * depth) + raw_sum for depth in domains[v]]
            min_sum += min(values)
            max_sum += max(values)
        bounds = _range_sum(union, demand)
        if bounds is None or max_sum < bounds[0] or min_sum > bounds[1]:
            moment_failures.append({
                "classes": selected,
                "demand": demand,
                "capacity": len(union),
                "possible_sum_interval": [min_sum, max_sum],
                "slot_sum_bounds": bounds,
            })

        low_selected = [name for name in selected if name != "H"]
        if low_selected:
            low_demand = sum(demands[name] for name in low_selected)
            max_depth = max(max(domains[int(name[1:])]) for name in low_selected)
            min_depth = min(min(domains[int(name[1:])]) for name in low_selected)
            span_capacity = cap + 2 * (max_depth - min_depth)
            if low_demand > span_capacity:
                demand_span_failures.append({
                    "classes": low_selected,
                    "demand": low_demand,
                    "capacity_upper_bound": span_capacity,
                    "depth_bounds": [min_depth, max_depth],
                })

    # The H+single-low form has a separate endpoint bound because H is fixed
    # in [1,C0] while a low interval moves with its depth.
    for v in range(r):
        max_h_low_capacity = cap + min(cap, 2 * (b - min(domains[v])))
        demand = demands["H"] + demands[f"L{v}"]
        if demand > max_h_low_capacity:
            demand_span_failures.append({
                "classes": ["H", f"L{v}"],
                "demand": demand,
                "capacity_upper_bound": max_h_low_capacity,
                "minimum_depth": min(domains[v]),
            })

    # Pairwise forbidden differences are a cheap, sound domain filter.  It
    # does not claim that independently compatible pairs glue globally.
    difference_failures = []
    forbidden = base["raw_sum_difference_sets"]
    for i in range(r):
        for j in range(i + 1, r):
            forbidden_depth_diffs = {
                raw // 2 for raw in forbidden[f"{i},{j}"] if raw % 2 == 0
            }
            if not any(
                (left - right) not in forbidden_depth_diffs
                for left in domains[i]
                for right in domains[j]
            ):
                difference_failures.append({
                    "pair": [i, j],
                    "forbidden_differences": sorted(forbidden_depth_diffs),
                })

    # Global odd-pair condition: parity of translated low classes is depth
    # independent, but vertex-depth parity varies over the current domains.
    high_odd = sum((b + y) % 2 for y in range(m)) + (s % 2)
    possible_odd_vertices = {
        high_odd + count for count in _possible_parity_counts(domains)
    }
    pair_total = order_n * (order_n - 1) // 2
    target_odd_pairs = (pair_total + 1) // 2
    parity_targets = sorted({
        odd for odd in possible_odd_vertices
        if odd * (order_n - odd) == target_odd_pairs
    })
    global_parity_failure = not parity_targets

    affine = base["wiener_affine"]
    affine_terms = [
        (affine[f"l{v}"], domains[v]) for v in range(1, r)
    ]
    affine_const = affine["const"] + affine["s"] * s
    wiener_lo, wiener_hi, wiener_gcd = _affine_range_and_gcd(
        affine_const, affine_terms
    )
    target = base["wiener_target"]
    wiener_ok = wiener_lo <= target <= wiener_hi and (
        wiener_gcd == 0 or (target - wiener_lo) % wiener_gcd == 0
    )

    if hall_failures:
        failures.append({"layer": "hall", "witness": hall_failures[0]})
    if component_failures:
        failures.append({"layer": "component_capacity", "witness": component_failures[0]})
    if parity_failures:
        failures.append({"layer": "parity_hall", "witness": parity_failures[0]})
    if moment_failures:
        failures.append({"layer": "moment_hall", "witness": moment_failures[0]})
    if demand_span_failures:
        failures.append({"layer": "demand_span", "witness": demand_span_failures[0]})
    if difference_failures:
        failures.append({"layer": "difference_domain", "witness": difference_failures[0]})
    if global_parity_failure:
        failures.append({
            "layer": "global_parity",
            "possible_odd_vertices": sorted(possible_odd_vertices),
            "target_odd_pairs": target_odd_pairs,
        })
    if not wiener_ok:
        failures.append({
            "layer": "wiener",
            "interval": [wiener_lo, wiener_hi],
            "gcd": wiener_gcd,
            "target": target,
        })

    failure_layers = []
    for item in failures:
        if item["layer"] not in failure_layers:
            failure_layers.append(item["layer"])
    return {
        "status": "PARTIAL_DEPTH_DOMAIN_AUDIT",
        "delta": delta,
        "s": s,
        "B": b,
        "r": r,
        "m": m,
        "domains": domains,
        "occupied": sorted(occupied_set),
        "subset_check": {
            "checked": min(subset_total, subset_cap),
            "total": subset_total,
            "complete": subset_complete,
        },
        "checks": {
            "component_capacity": {"failures": component_failures, "capacity": cap},
            "hall": {"failures": hall_failures},
            "parity_hall": {"failures": parity_failures},
            "moment_hall": {"failures": moment_failures},
            "demand_span": {"failures": demand_span_failures},
            "difference_domain": {"failures": difference_failures},
            "global_parity": {
                "possible_odd_vertices": sorted(possible_odd_vertices),
                "target_odd_pairs": target_odd_pairs,
                "satisfying_odd_vertices": parity_targets,
            },
            "wiener": {
                "interval": [wiener_lo, wiener_hi],
                "gcd": wiener_gcd,
                "target": target,
                "necessary_pass": wiener_ok,
            },
        },
        "failure_layers": failure_layers,
        "necessary_pass": not failures,
        "interpretation": (
            "NOT-EXCLUDED_BY_PARTIAL_DOMAIN_AUDIT"
            if not failures else "UNSAT_FOR_ALL_ASSIGNMENTS_IN_DOMAIN_BOX"
        ),
        "source_scope": (
            "domain-union necessary conditions; no depth assignment enumeration; "
            "pass is not an existence proof"
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lowpar", required=True)
    ap.add_argument("--struct", required=True)
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--domains", required=True)
    ap.add_argument("--occupied", default="")
    ap.add_argument("--order-n", type=int, default=25)
    args = ap.parse_args()
    result = audit_domains(
        ints(args.lowpar), parse_struct(args.struct), args.delta, args.s,
        parse_domains(args.domains), ints(args.occupied) if args.occupied else [],
        args.order_n,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
