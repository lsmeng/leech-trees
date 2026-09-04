#!/usr/bin/env python3
"""Tiny independent differential for ``partial_depth_domain_audit``.

The oracle below directly checks each concrete depth tuple.  It is purposely
separate from the domain-union implementation: it does not import
``presolve`` and does not reuse the union Hall/moment code.
"""
from __future__ import annotations

import itertools
import json
import sys

from colored_moment_hall_audit import audit
from partial_depth_domain_audit import audit_domains


def concrete_ok(lowpar_tail, hpar, delta, s, depths, order_n=25, occupied=()):
    base = audit(lowpar_tail, hpar, delta, order_n)
    r, m = base["r"], base["m"]
    if not base["partition_ok"] or not base["H_unique"] or not all(base["S_unique"]):
        return False
    b = delta + 1 - s
    if len(depths) != r or depths[0] != 0 or b <= 0:
        return False
    if any(value < 0 or value >= b for value in depths):
        return False
    lowpar = [-1] + list(lowpar_tail)
    if len(set(depths)) != r:
        return False
    if any(depths[v] <= depths[lowpar[v]] for v in range(1, r)):
        return False
    if any(value < 1 or value > delta for value in base["H"]):
        return False
    classes = {"H": set(base["H"])}
    for v, raw in enumerate(base["S"]):
        classes[f"L{v}"] = {2 * b - 2 * depths[v] + x for x in raw}
    if any(any(value < 1 or value > delta for value in vals) for vals in classes.values()):
        return False
    if any(not classes[a].isdisjoint(classes[b])
           for a, b in itertools.combinations(classes, 2)):
        return False
    if any(classes[name] & set(occupied) for name in classes):
        return False
    affine = base["wiener_affine"]
    value = affine["const"] + affine["s"] * s + sum(
        affine[f"l{v}"] * depths[v] for v in range(1, r)
    )
    if value != base["wiener_target"]:
        return False
    odd_vertices = sum(value % 2 for value in depths)
    odd_vertices += sum((b + y) % 2 for y in range(m)) + s % 2
    target = (order_n * (order_n - 1) // 2 + 1) // 2
    return odd_vertices * (order_n - odd_vertices) == target


def run_case(name, lowpar, hpar, delta, s, domains, occupied=(), order_n=25):
    observed = audit_domains(
        lowpar, hpar, delta, s, domains, list(occupied), order_n=order_n
    )
    concrete = [
        depths for depths in itertools.product(*domains)
        if concrete_ok(
            lowpar, hpar, delta, s, depths, order_n=order_n, occupied=occupied
        )
    ]
    # Soundness gate: a concrete necessary-system survivor may never be
    # rejected by the domain-union audit.  The converse is intentionally not
    # required because the domain union forgets cross-depth correlations.
    sound = not concrete or observed["necessary_pass"]
    return {
        "name": name,
        "domain_assignments_checked": sum(1 for _ in itertools.product(*domains)),
        "concrete_survivors": len(concrete),
        "domain_failure_layers": observed["failure_layers"],
        "domain_interpretation": observed["interpretation"],
        "soundness_gate": sound,
    }


def main():
    cases = [
        run_case(
            "genuine_L6_positive",
            [], [-1, -1, 1, 1], 11, 8, [[0]],
            order_n=6,
        ),
        run_case(
            "r8_singleton",
            [0, 0, 1, 3, 4, 5, 6],
            [-1, -2, -4, -5, -6, -7, -8, -8, -8, 6, -7, -6, -5, -4, -2, -1],
            284, 158, [[0], [18], [40], [41], [51], [59], [88], [92]],
        ),
        run_case(
            "r9_three_value_box",
            [0, 0, 0, 0, 1, 5, 6, 7],
            [-1, -2, -6, -7, -8, -9, -9, 5, 5, 5, -8, -7, -6, -2, -1],
            285, 157,
            [[0], [12, 13, 14], [1, 2], [1, 2, 3], [2, 3, 4],
             [23, 24, 25], [32, 33, 34], [76, 77, 78], [100, 101, 102]],
        ),
    ]
    print(json.dumps({
        "status": "PARTIAL_DEPTH_DOMAIN_DIFFERENTIAL",
        "cases": cases,
        "soundness_ok": all(case["soundness_gate"] for case in cases),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
