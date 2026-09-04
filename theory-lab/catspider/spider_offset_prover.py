"""N-independent high-window relaxation for regular spider anchors.

Write the two largest tips as T > U and N=T+U.  While processing values
N-k with k <= W, assume

    U > W  and  T-U > W.

Then every mark introduced by a realizer of N-k is necessarily

    T-a on the top leg, or U-b on a non-top leg,  0 <= a,b <= W.

The proof is elementary: centre and same-leg realizers require U<=k, while
two lower-leg marks could sum to N-k only if T-U<=k.  Hence a cross-leg
realizer consists of exactly one top and one lower mark, with offsets summing
to k.

Every real spider must satisfy the following three bounded collision tests:

* top/lower cross distances: the sums a+b must be unique;
* same-leg distances: the differences |a-a'| and |b-b'| must be unique;
* cross distances between two lower legs: the sums b+b' must be unique;
The search deliberately ignores every cross-category collision, including a
possible equality between T-a and 2U-(b+b').  It is therefore a relaxation,
not an exact model: every real spider branch survives, and possibly some
spurious branches survive too.  Closure of the relaxation is consequently a
sound nonexistence proof for every numeric anchor with U>W and T-U>W.

The optional ``r`` argument adds one diagnostically useful collision class;
the uniform theorem uses only the weaker ``r=None`` search.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class OffsetStats:
    W: int
    r: int | None
    nodes: int = 0
    accepted_children: int = 0
    dead_states: int = 0
    deepest_missing_offset: int = 0
    max_marks: int = 2
    frontier_states: int = 0


def canonical_lower(lower: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    """Keep the U-tip leg first; sort all otherwise interchangeable legs."""

    first = tuple(sorted(lower[0]))
    rest = tuple(sorted(tuple(sorted(leg)) for leg in lower[1:]))
    return (first, *rest)


def prove_regular(W: int, r: int | None) -> OffsetStats:
    if W < 1:
        raise ValueError("W must be positive")
    if r is not None and not (-W <= r <= 2 * W):
        raise ValueError("use r=None outside the only relevant interval [-W,2W]")

    stats = OffsetStats(W=W, r=r)

    # A: offsets on the unique top leg (0 is its tip).
    # lower[0]: offsets on the second-tip leg (0 is its tip).
    # lower[1:]: offsets on interchangeable further legs.
    # The three value sets store the offset normal forms described above.
    A = {0}
    lower = [{0}]
    high_sums = {0}
    low_differences: set[int] = set()
    lower_cross_sums: set[int] = set()

    def all_B() -> set[int]:
        return {b for leg in lower for b in leg}

    def valid_top_add(a: int):
        if not (1 <= a <= W) or a in A:
            return None
        new_high = {a + b for b in all_B()}
        if len(new_high) != len(all_B()) or new_high & high_sums:
            return None
        new_diffs = {abs(a - old) for old in A}
        if 0 in new_diffs or len(new_diffs) != len(A):
            return None
        if new_diffs & low_differences:
            return None
        if r is not None and any(s - a == r for s in lower_cross_sums):
            return None
        return new_high, new_diffs

    def valid_lower_add(li: int, b: int):
        B = all_B()
        if not (1 <= b <= W) or b in B:
            return None
        new_high = {a + b for a in A}
        if len(new_high) != len(A) or new_high & high_sums:
            return None
        same_leg = lower[li] if li < len(lower) else set()
        new_diffs = {abs(b - old) for old in same_leg}
        if 0 in new_diffs or len(new_diffs) != len(same_leg):
            return None
        if new_diffs & low_differences:
            return None
        other_B = {old for j, leg in enumerate(lower) if j != li for old in leg}
        new_lower_sums = {b + old for old in other_B}
        if len(new_lower_sums) != len(other_B):
            return None
        if new_lower_sums & lower_cross_sums:
            return None
        if r is not None:
            if any(s - a == r for s in new_lower_sums for a in A):
                return None
        return new_high, new_diffs, new_lower_sums

    def apply_top(a: int, pieces):
        new_high, new_diffs = pieces
        A.add(a)
        high_sums.update(new_high)
        low_differences.update(new_diffs)
        return new_high, new_diffs

    def undo_top(a: int, token) -> None:
        new_high, new_diffs = token
        A.remove(a)
        high_sums.difference_update(new_high)
        low_differences.difference_update(new_diffs)

    def apply_lower(li: int, b: int, pieces):
        new_high, new_diffs, new_lower_sums = pieces
        fresh = li == len(lower)
        if fresh:
            lower.append(set())
        lower[li].add(b)
        high_sums.update(new_high)
        low_differences.update(new_diffs)
        lower_cross_sums.update(new_lower_sums)
        return new_high, new_diffs, new_lower_sums, fresh

    def undo_lower(li: int, b: int, token) -> None:
        new_high, new_diffs, new_lower_sums, fresh = token
        lower[li].remove(b)
        high_sums.difference_update(new_high)
        low_differences.difference_update(new_diffs)
        lower_cross_sums.difference_update(new_lower_sums)
        if fresh:
            if lower[li]:
                raise RuntimeError("fresh lower leg was not empty after undo")
            lower.pop()

    def state_key():
        return tuple(sorted(A)), canonical_lower([tuple(leg) for leg in lower])

    def candidate_states(k: int):
        """All canonical child states that newly realize high offset k."""

        children = set()
        B = all_B()

        # Existing top endpoint plus one new lower endpoint.
        for a in tuple(A):
            b = k - a
            for li in range(len(lower) + 1):
                pieces = valid_lower_add(li, b)
                if pieces is None:
                    continue
                token = apply_lower(li, b, pieces)
                children.add(state_key())
                undo_lower(li, b, token)

        # Existing lower endpoint plus one new top endpoint.
        for b in tuple(B):
            a = k - b
            pieces = valid_top_add(a)
            if pieces is None:
                continue
            token = apply_top(a, pieces)
            children.add(state_key())
            undo_top(a, token)

        # Two new endpoints.  Applying the top endpoint first also checks all
        # values involving old marks; the lower addition then checks their
        # mutual high sum k.
        for a in range(1, k):
            b = k - a
            top_pieces = valid_top_add(a)
            if top_pieces is None:
                continue
            top_token = apply_top(a, top_pieces)
            for li in range(len(lower) + 1):
                lower_pieces = valid_lower_add(li, b)
                if lower_pieces is None:
                    continue
                lower_token = apply_lower(li, b, lower_pieces)
                children.add(state_key())
                undo_lower(li, b, lower_token)
            undo_top(a, top_token)
        return children

    def load_state(key) -> None:
        """Recompute all derived value sets from a canonical offset state."""

        A.clear()
        A.update(key[0])
        lower.clear()
        lower.extend(set(leg) for leg in key[1])
        high_sums.clear()
        low_differences.clear()
        lower_cross_sums.clear()

        B_with_leg = [(b, li) for li, leg in enumerate(lower) for b in leg]
        for a in A:
            for b, _ in B_with_leg:
                high_sums.add(a + b)
        for offsets in [A, *lower]:
            seq = sorted(offsets)
            for i, x in enumerate(seq):
                for y in seq[i + 1 :]:
                    low_differences.add(y - x)
        for i, (b, li) in enumerate(B_with_leg):
            for c, lj in B_with_leg[i + 1 :]:
                if li != lj:
                    lower_cross_sums.add(b + c)

    seen_stack: list[tuple] = []

    def dfs(k: int) -> None:
        stats.nodes += 1
        stats.max_marks = max(stats.max_marks, len(A) + sum(map(len, lower)))
        while k in high_sums:
            k += 1
        stats.deepest_missing_offset = max(stats.deepest_missing_offset, k)
        if k > W:
            stats.frontier_states += 1
            return

        parent = state_key()
        children = candidate_states(k)
        if not children:
            stats.dead_states += 1
            return
        for child in children:
            stats.accepted_children += 1
            seen_stack.append(parent)
            load_state(child)
            dfs(k + 1)
            load_state(seen_stack.pop())

    dfs(1)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", type=int, default=25)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--r", type=int)
    group.add_argument("--generic", action="store_true")
    parser.add_argument("--all-r", action="store_true")
    args = parser.parse_args()

    if args.all_r:
        rows = [prove_regular(args.window, r) for r in range(-args.window, 2 * args.window + 1)]
        rows.append(prove_regular(args.window, None))
        print(
            json.dumps(
                {
                    "window": args.window,
                    "regimes": len(rows),
                    "frontier_states": sum(row.frontier_states for row in rows),
                    "max_depth": max(row.deepest_missing_offset for row in rows),
                    "max_marks": max(row.max_marks for row in rows),
                    "nodes": sum(row.nodes for row in rows),
                },
                sort_keys=True,
            )
        )
        for row in rows:
            print(json.dumps(asdict(row), sort_keys=True))
        return

    r = None if args.generic else args.r
    print(json.dumps(asdict(prove_regular(args.window, r)), sort_keys=True))


if __name__ == "__main__":
    main()
