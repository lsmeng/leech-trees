#!/usr/bin/env python3
"""Compressed component-mass / low-LCA necessary-condition DP.

This is a state-compressed companion to component_mass_dp.py.  Local component
partitions are quotient-ed by the only two quantities used by the capacity
test: their total mass ``a`` and ``w=sum(C(n,2))``.  For each low subtree it
keeps reachable ``(M,W)`` states, where M is subtree high mass and W is total
within-component pair count.  The parent transition recomputes the exact
low-LCA class count from child masses.  Passing a state is still only a
necessary condition, never a sufficient construction.
"""
from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple

Partition = Tuple[int, ...]
State = Tuple[int, int]


def integer_partitions(n: int, largest: Optional[int] = None) -> Iterator[Partition]:
    if n == 0:
        yield ()
        return
    if n < 0:
        return
    if largest is None or largest > n:
        largest = n
    for first in range(largest, 0, -1):
        for rest in integer_partitions(n - first, first):
            yield (first,) + rest


def validate_lowpar(lowpar: Sequence[int]) -> None:
    if not lowpar or lowpar[0] != -1:
        raise ValueError("lowpar must start with -1 for the root")
    for i, p in enumerate(lowpar[1:], 1):
        if not (0 <= p < i):
            raise ValueError(f"lowpar[{i}]={p}={i}")


def local_options(m: int) -> Dict[int, Tuple[int, ...]]:
    """Return attainable local ``w`` values for every local mass ``a``."""
    out: Dict[int, Set[int]] = {}
    for a in range(m + 1):
        vals: Set[int] = set()
        for part in integer_partitions(a):
            vals.add(sum(comb(n, 2) for n in part))
        out[a] = vals
    return {a: tuple(sorted(vals)) for a, vals in out.items()}


def compressed_states(lowpar: Sequence[int], m: int) -> Tuple[List[Set[State]], dict]:
    validate_lowpar(lowpar)
    if m < 1:
        raise ValueError("m must be positive")
    r = len(lowpar)
    cap = 2 * m - 3
    children: List[List[int]] = [[] for _ in range(r)]
    for v in range(1, r):
        children[lowpar[v]].append(v)
    opts = local_options(m)
    states: List[Set[State]] = [set() for _ in range(r)]
    state_counts: List[int] = [0] * r
    transition_counts: List[int] = [0] * r

    for v in range(r - 1, -1, -1):
        # (sum child masses, sum child W, sum C(child mass,2))
        acc: Set[Tuple[int, int, int]] = {(0, 0, 0)}
        for u in children[v]:
            nxt: Set[Tuple[int, int, int]] = set()
            for s, w, q in acc:
                for child_m, child_w in states[u]:
                    ns = s + child_m
                    nw = w + child_w
                    if ns <= m and nw <= cap:
                        nxt.add((ns, nw, q + comb(child_m, 2)))
            acc = nxt

        accepted: Set[State] = set()
        attempted = 0
        for s, w, q in acc:
            for a in range(m - s + 1):
                for w0 in opts[a]:
                    attempted += 1
                    mass = s + a
                    total_w = w + w0
                    if total_w > cap:
                        continue
                    p = comb(mass, 2) - q - w0
                    if 0 <= p <= cap:
                        accepted.add((mass, total_w))
        states[v] = accepted
        state_counts[v] = len(accepted)
        transition_counts[v] = attempted

    root_m = sorted(w for mass, w in states[0] if mass == m)
    summary = {
        "status": "COMPONENT_MASS_DP_COMPRESSED",
        "lowpar": list(lowpar),
        "m": m,
        "capacity": cap,
        "root_possible": bool(root_m),
        "root_W_states": root_m,
        "states_per_vertex": state_counts,
        "transition_attempts_per_vertex": transition_counts,
        "total_reachable_states": sum(state_counts),
    }
    return states, summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--lowpar", required=True, help="comma-separated, starting -1")
    ap.add_argument("--emit", type=Path, default=None, help="optional JSONL of reachable states")
    args = ap.parse_args()
    lowpar = [int(x) for x in args.lowpar.split(",") if x.strip()]
    states, summary = compressed_states(lowpar, args.m)
    if args.emit:
        with args.emit.open("w", encoding="utf-8") as fh:
            for v, vertex_states in enumerate(states):
                for mass, within in sorted(vertex_states):
                    fh.write(json.dumps({"vertex": v, "M": mass, "W": within}, sort_keys=True) + "\n")
        summary["emitted_jsonl"] = str(args.emit)
    else:
        summary["emitted_jsonl"] = None
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
