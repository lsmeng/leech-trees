#!/usr/bin/env python3
"""
Independent exact-10 component-root checker/replay.

This implementation is intentionally structurally different from the C++:
- Python sets, not bitsets;
- actual numerical tree distances are computed directly for every root pair;
- no raw-y-sum collision tables are used;
- no C++ local-color-mask or available-position pruning is reused;
- parameter order is d1 shard -> d2;
- color trial order is deliberately 2, 0, 1.

Supported:
    --s {152,154,156,158,160}
    --shape {star,chain}
    --d1 EVEN_INTEGER          optional; restrict to one d1 shard

With --d1 omitted, params_total/params_valid and survivor aggregates are
directly comparable to a full C++ (s,shape) run.

With --d1 supplied, the same fields refer only to that d1 shard and can be
summed/XORed over d1 shards:
- params_total, params_valid, params_with_survivor, survivor_count: sum
- color_count_histogram: componentwise sum
- survivor_xor_fnv1a64: XOR
- survivor_sum_fnv1a64: sum modulo 2^64
"""

import argparse
import json
from collections import Counter

ALLOWED_S = {152, 154, 156, 158, 160}
MAX_VALUE = 279
Y_MIN = 0
Y_MAX = 20
EXACT_ROOTS = 10

FNV_OFFSET = 1469598103934665603
FNV_PRIME = 1099511628211
MASK64 = (1 << 64) - 1


def fnv1a64(text: str) -> int:
    h = FNV_OFFSET
    for byte in text.encode("utf-8"):
        h ^= byte
        h = (h * FNV_PRIME) & MASK64
    return h


def hex64(value: int) -> str:
    return f"{value & MASK64:016x}"


class Exact10Checker:
    def __init__(self, s: int, shape: str, d1_shard=None):
        if s not in ALLOWED_S:
            raise ValueError("s must be one of 152,154,156,158,160")
        if shape not in ("star", "chain"):
            raise ValueError("shape must be star or chain")

        self.s = s
        self.B = 280 - s
        self.shape = shape
        self.d1_shard = d1_shard

        self.d1 = None
        self.d2 = None

        # Current owner-value set.  Each value in this set is already owned by
        # one concrete unordered pair represented by the current subsystem.
        self.owner_values = set()

        # Selected component roots as (y, color), in increasing y order.
        self.roots = []

        self.params_total = 0
        self.params_valid = 0
        self.params_with_survivor = 0

        self.dfs_calls = 0
        self.candidate_attempts = 0
        self.survivor_count = 0

        self.survivor_xor = 0
        self.survivor_sum = 0

        self.color_histogram = Counter()
        self.first_examples = []
        self.max_examples = 50

    # ------------------------------------------------------------------
    # Fixed S1-279 value domain
    # ------------------------------------------------------------------

    def is_hole(self, value: int) -> bool:
        return value in (
            self.s,
            self.s + self.d1,
            self.s + self.d2,
        )

    def pair_value_allowed(self, value: int) -> bool:
        return (
            1 <= value <= MAX_VALUE
            and not self.is_hole(value)
        )

    def low_parent_depth(self, color: int) -> int:
        if color == 0:
            return 0
        if color == 1:
            return self.d1
        if color == 2:
            return self.d2
        raise ValueError(f"bad color {color}")

    # ------------------------------------------------------------------
    # Exact low-subtree LCA table
    # ------------------------------------------------------------------

    def lca_depth(self, color_a: int, color_b: int) -> int:
        if self.shape == "star":
            # STAR:
            #   (1,1) -> u1
            #   (2,2) -> u2
            #   every pair involving color0, and (1,2), -> x
            if color_a == 1 and color_b == 1:
                return self.d1
            if color_a == 2 and color_b == 2:
                return self.d2
            return 0

        # CHAIN x--u1--u2:
        #   any pair involving color0 -> x
        #   (1,1),(1,2) -> u1
        #   (2,2) -> u2
        if color_a == 0 or color_b == 0:
            return 0
        if color_a == 2 and color_b == 2:
            return self.d2
        return self.d1

    # ------------------------------------------------------------------
    # Parameter setup
    # ------------------------------------------------------------------

    def add_background_owner(self, value: int) -> bool:
        if not self.pair_value_allowed(value):
            return False
        if value in self.owner_values:
            return False
        self.owner_values.add(value)
        return True

    def setup_parameter(self, d1: int, d2: int) -> bool:
        self.d1 = d1
        self.d2 = d2
        self.owner_values = set()
        self.roots = []

        if not (0 < d1 < d2 < self.B):
            return False
        if d1 % 2 != 0 or d2 % 2 != 0:
            return False

        if self.shape == "star":
            # Literal low edges x-u1 and x-u2.
            if not (d1 < self.s and d2 < self.s):
                return False

            # Pair u1-u2 has LCA x.
            low_low_distance = d1 + d2

        else:
            # Literal low edges x-u1 and u1-u2.
            gap = d2 - d1
            if not (d1 < self.s and gap < self.s):
                return False

            # d1 and gap are two different K edges, hence two different
            # globally owned pair distances.
            if d1 == gap:
                return False

            low_low_distance = gap

        # D\{0}: rooted pairs (x,u1),(x,u2).
        if not self.add_background_owner(d1):
            return False
        if not self.add_background_owner(d2):
            return False

        # Complete 21-term rooted owner block:
        # (x,v_y), y=0,...,20.
        for y in range(Y_MIN, Y_MAX + 1):
            if not self.add_background_owner(self.B + y):
                return False

        # Pair (u1,u2).  In chain this is also the literal u1-u2 edge.
        if not self.add_background_owner(low_low_distance):
            return False

        return True

    # ------------------------------------------------------------------
    # Attachment / root candidate checks
    # ------------------------------------------------------------------

    def attachment_value(self, y: int, color: int) -> int:
        return self.B + y - self.low_parent_depth(color)

    def local_attachment_legal(self, y: int, color: int) -> bool:
        """
        Check only the attachment against the current immutable/dynamic owner
        set.  Unlike the C++ implementation, no precomputed color mask exists.
        """
        value = self.attachment_value(y, color)

        if not (0 < value < self.s):
            return False

        if color == 0:
            # Same unordered pair:
            # attachment edge (x,h_y) IS the rooted D owner (x,h_y).
            return (
                value == self.B + y
                and value in self.owner_values
            )

        # Colors 1 and 2 are genuinely new unordered owner pairs.
        return (
            self.pair_value_allowed(value)
            and value not in self.owner_values
        )

    def actual_root_distance(
        self,
        y_a: int,
        color_a: int,
        y_b: int,
        color_b: int,
    ) -> int:
        ell = self.lca_depth(color_a, color_b)
        return 2 * self.B + y_a + y_b - 2 * ell

    def try_add_root(self, y: int, color: int):
        """
        Return the set of newly inserted owner values on success.
        Return None on rejection.

        Every root-root comparison is performed on the ACTUAL tree distance.
        No raw y-sum is compared across LCA classes.
        """
        self.candidate_attempts += 1

        if not self.local_attachment_legal(y, color):
            return None

        pending = set()

        # Attachment owner.
        att = self.attachment_value(y, color)

        if color == 0:
            # Same-owner exception only.  Do not insert a second copy.
            if att != self.B + y:
                return None
            if att not in self.owner_values:
                return None
        else:
            if not self.pair_value_allowed(att):
                return None
            if att in self.owner_values:
                return None
            pending.add(att)

        # Root-root owner against each previously selected component root.
        for old_y, old_color in self.roots:
            dist = self.actual_root_distance(
                y,
                color,
                old_y,
                old_color,
            )

            if not self.pair_value_allowed(dist):
                return None

            if dist in self.owner_values:
                return None

            # Two distinct new unordered pairs in this same insertion may not
            # acquire the same owner value.
            if dist in pending:
                return None

            pending.add(dist)

        # Commit all genuinely new owner values.
        self.owner_values.update(pending)
        self.roots.append((y, color))

        return pending

    def undo_root(self, newly_added):
        self.roots.pop()
        for value in newly_added:
            self.owner_values.remove(value)

    # ------------------------------------------------------------------
    # Survivor canonicalization / aggregation
    # ------------------------------------------------------------------

    def canonical_signature(self) -> str:
        by_color = [[], [], []]

        # DFS selects y increasingly, so these lists are already sorted.
        for y, color in self.roots:
            by_color[color].append(y)

        fields = [
            str(self.s),
            self.shape,
            str(self.d1),
            str(self.d2),
        ]

        for values in by_color:
            fields.append(",".join(str(v) for v in values))

        return "|".join(fields)

    def record_survivor(self):
        self.survivor_count += 1

        counts = [0, 0, 0]
        for _, color in self.roots:
            counts[color] += 1

        self.color_histogram[tuple(counts)] += 1

        signature = self.canonical_signature()
        digest = fnv1a64(signature)

        self.survivor_xor ^= digest
        self.survivor_sum = (
            self.survivor_sum + digest
        ) & MASK64

        if len(self.first_examples) < self.max_examples:
            self.first_examples.append(signature)

    # ------------------------------------------------------------------
    # Independent DFS
    # ------------------------------------------------------------------

    def dfs(self, next_y: int, need: int):
        self.dfs_calls += 1

        if need == 0:
            self.record_survivor()
            return

        if next_y > Y_MAX:
            return

        # Only elementary combinatorial remaining-position bound.
        # No C++ local-color-mask availability pruning is reused.
        remaining_positions = Y_MAX - next_y + 1
        if remaining_positions < need:
            return

        last_possible_y = Y_MAX - need + 1

        # Deliberately different color order from C++.
        color_order = (2, 0, 1)

        for y in range(next_y, last_possible_y + 1):
            for color in color_order:
                newly_added = self.try_add_root(y, color)

                if newly_added is None:
                    continue

                self.dfs(y + 1, need - 1)
                self.undo_root(newly_added)

    # ------------------------------------------------------------------
    # Full parameter / shard loop
    # ------------------------------------------------------------------

    def d1_values(self):
        if self.d1_shard is None:
            return range(2, self.B, 2)

        d1 = self.d1_shard

        if d1 <= 0 or d1 >= self.B or d1 % 2 != 0:
            return ()

        return (d1,)

    def run(self):
        for d1 in self.d1_values():
            for d2 in range(d1 + 2, self.B, 2):
                self.params_total += 1

                if not self.setup_parameter(d1, d2):
                    continue

                self.params_valid += 1

                before = self.survivor_count

                # setup_parameter resets roots.
                self.dfs(Y_MIN, EXACT_ROOTS)

                if self.survivor_count != before:
                    self.params_with_survivor += 1

    # ------------------------------------------------------------------
    # JSON output
    # ------------------------------------------------------------------

    def result(self):
        histogram = {
            ",".join(str(x) for x in key): value
            for key, value in sorted(self.color_histogram.items())
        }

        result = {
            "status": "INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED",
            "s": self.s,
            "B": self.B,
            "shape": self.shape,
            "params_total": self.params_total,
            "params_valid": self.params_valid,
            "params_with_survivor": self.params_with_survivor,
            "dfs_calls": self.dfs_calls,
            "candidate_attempts": self.candidate_attempts,
            "survivor_count": self.survivor_count,
            "survivor_xor_fnv1a64": hex64(self.survivor_xor),
            "survivor_sum_fnv1a64": hex64(self.survivor_sum),
            "color_count_histogram": histogram,
            "first_examples": self.first_examples,
        }

        if self.d1_shard is not None:
            result["d1"] = self.d1_shard

        return result


def compare_expected(actual, expected):
    """
    Compare exactly the fields intended for C++/Python replay agreement.

    If --d1 is used, expected should be the corresponding C++ d1 shard result.
    Without --d1 it may be a full (s,shape) result.
    """
    scalar_fields = (
        "s",
        "B",
        "shape",
        "params_total",
        "params_valid",
        "params_with_survivor",
        "survivor_count",
        "survivor_xor_fnv1a64",
        "survivor_sum_fnv1a64",
    )

    for key in scalar_fields:
        if key not in expected:
            raise AssertionError(f"expected JSON missing field {key!r}")

        if actual[key] != expected[key]:
            raise AssertionError(
                f"{key}: checker={actual[key]!r}, "
                f"expected={expected[key]!r}"
            )

    if (
        actual["color_count_histogram"]
        != expected.get("color_count_histogram")
    ):
        raise AssertionError(
            "color_count_histogram mismatch:\n"
            f"checker={actual['color_count_histogram']!r}\n"
            f"expected={expected.get('color_count_histogram')!r}"
        )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--s",
        required=True,
        type=int,
        choices=sorted(ALLOWED_S),
    )

    parser.add_argument(
        "--shape",
        required=True,
        choices=("star", "chain"),
    )

    parser.add_argument(
        "--d1",
        type=int,
        default=None,
        help=(
            "Optional even d1 shard.  When omitted, exhaust all legal d1."
        ),
    )

    parser.add_argument(
        "--expect-json",
        default=None,
        help=(
            "Optional C++ result JSON for exact aggregate comparison."
        ),
    )

    args = parser.parse_args()

    if args.d1 is not None and args.d1 % 2 != 0:
        raise SystemExit("--d1 must be even")

    checker = Exact10Checker(
        s=args.s,
        shape=args.shape,
        d1_shard=args.d1,
    )

    checker.run()
    result = checker.result()

    if args.expect_json is not None:
        with open(args.expect_json, "r", encoding="utf-8") as handle:
            expected = json.load(handle)

        compare_expected(result, expected)
        result["expected_json_verified"] = True

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
