#!/usr/bin/env python3
"""Joint interval-Hall necessary filter for low-LCA distance classes.

For fixed ``(m, delta, s, low_depths, W, P_v)``, every high-LCA pair lies in
the interval ``[1, 2m-3]`` and every low-LCA class ``v`` lies in
``[2B-2*l_v+1, 2B-2*l_v+(2m-3)]`` intersected with ``[1, delta]``.

The test enumerates all subsets of these at most ten classes.  If the sum of
their demands exceeds the number of distance slots in the union of their
intervals (after removing only explicitly supplied, distinct occupied slots),
global distance injectivity is impossible.  This is a necessary filter only:
passing the test is not an existence certificate.
"""
from __future__ import annotations

import argparse
import itertools
import json
from math import comb
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


Interval = Tuple[int, int]


def validate_inputs(
    m: int,
    delta: int,
    s: int,
    low_depths: Sequence[int],
    W: int,
    pvals: Sequence[int],
    occupied: Sequence[int],
    lowpar: Optional[Sequence[int]],
) -> None:
    if len(low_depths) != len(pvals) or not low_depths:
        raise ValueError("low_depths and P must be nonempty and aligned")
    if low_depths[0] != 0:
        raise ValueError("root low depth must be 0")
    if len(set(low_depths)) != len(low_depths):
        raise ValueError("low depths must be pairwise distinct")
    b = delta + 1 - s
    if b <= 0 or any(l < 0 or l >= b for l in low_depths):
        raise ValueError("low depth outside [0,B)")
    if W < 0 or any(p < 0 for p in pvals):
        raise ValueError("class demands must be nonnegative")
    if W + sum(pvals) != comb(m, 2):
        raise ValueError("W + sum(P) must equal C(m,2)")
    if len(set(occupied)) != len(occupied):
        raise ValueError("duplicate occupied slots indicate an upstream collision")
    if any(x < 1 or x > delta for x in occupied):
        raise ValueError("occupied slot outside [1,delta]")
    if lowpar is not None:
        if len(lowpar) != len(low_depths) or lowpar[0] != -1:
            raise ValueError("lowpar must align and start with -1")
        for v in range(1, len(lowpar)):
            if not (0 <= lowpar[v] < v):
                raise ValueError("lowpar must be depth-order indexed")
            if low_depths[v] <= low_depths[lowpar[v]]:
                raise ValueError("child low depth must exceed parent depth")


def class_intervals(
    m: int,
    delta: int,
    s: int,
    low_depths: Sequence[int],
    occupied: Iterable[int] = (),
) -> Dict[str, Set[int]]:
    """Return exact integer interval supersets after clipping/removing slots."""
    b = delta + 1 - s
    cap = 2 * m - 3
    used = set(occupied)
    out: Dict[str, Set[int]] = {"H": set(range(1, cap + 1))}
    for v, lv in enumerate(low_depths):
        lo = 2 * b - 2 * lv + 1
        hi = lo + cap - 1
        out["L%d" % v] = set(range(max(1, lo), min(delta, hi) + 1))
    for name in out:
        out[name].difference_update(used)
    return out


def interval_hall(
    m: int,
    delta: int,
    s: int,
    low_depths: Sequence[int],
    W: int,
    pvals: Sequence[int],
    occupied: Sequence[int] = (),
    lowpar: Optional[Sequence[int]] = None,
) -> dict:
    """Check all class-subset Hall inequalities and return a witness on fail."""
    validate_inputs(m, delta, s, low_depths, W, pvals, occupied, lowpar)
    names = ["H"] + ["L%d" % v for v in range(len(pvals))]
    demands = [W] + list(pvals)
    slots = class_intervals(m, delta, s, low_depths, occupied)
    failed: Optional[dict] = None
    checked = 0
    for mask in range(1, 1 << len(names)):
        subset = [i for i in range(len(names)) if mask & (1 << i)]
        demand = sum(demands[i] for i in subset)
        union: Set[int] = set()
        for i in subset:
            union.update(slots[names[i]])
        checked += 1
        if demand > len(union):
            failed = {
                "classes": [names[i] for i in subset],
                "demand": demand,
                "union_slots": len(union),
                "deficit": demand - len(union),
            }
            break
    return {
        "status": "JOINT_INTERVAL_HALL",
        "m": m,
        "delta": delta,
        "s": s,
        "low_depths": list(low_depths),
        "W": W,
        "P": list(pvals),
        "occupied": sorted(occupied),
        "subsets_checked": checked,
        "necessary_pass": failed is None,
        "failure": failed,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--delta", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--depths", required=True, help="comma-separated low depths")
    ap.add_argument("--W", type=int, required=True)
    ap.add_argument("--P", required=True, help="comma-separated P_v")
    ap.add_argument("--occupied", default="", help="comma-separated known slots")
    ap.add_argument("--lowpar", default=None, help="comma-separated parents")
    args = ap.parse_args()
    depths = [int(x) for x in args.depths.split(",") if x.strip()]
    pvals = [int(x) for x in args.P.split(",") if x.strip()]
    occupied = [int(x) for x in args.occupied.split(",") if x.strip()]
    lowpar = None if args.lowpar is None else [int(x) for x in args.lowpar.split(",") if x.strip()]
    print(json.dumps(interval_hall(args.m, args.delta, args.s, depths, args.W, pvals, occupied, lowpar), sort_keys=True))


if __name__ == "__main__":
    main()
