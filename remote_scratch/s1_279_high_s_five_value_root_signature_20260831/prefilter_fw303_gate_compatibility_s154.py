#!/usr/bin/env python3
"""Sound FW303 gate-row compatibility prefilter for v4w exact-10 signatures.

This does not search the remaining high forest.  It only rejects a gate row
when the exact low depths do not contain its low core vertices, a selected
component root would be forced to have a high core parent, or a selected root
has the wrong low-parent color for a forced mixed-core attachment.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path


CORE_EDGES = (
    ("z", "b1", 1),
    ("z", "b2", 2),
    ("c", "d6", 6),
    ("c", "z", 7),
    ("z", "a", 10),
)
ALL_HIGH_Q = {
    "z": range(13, 21),
    "b1": range(14, 21),
    "b2": range(15, 21),
    "c": range(17, 21),
}
MIXED_Q = {
    "b2": (22,),
    "c": (22, 24, 26),
    "a": (24, 26, 28, 30),
    "d6": (24, 26, 28, 30, 32),
}


def adjacency() -> dict[str, list[tuple[str, int]]]:
    out: dict[str, list[tuple[str, int]]] = {}
    for a, b, w in CORE_EDGES:
        out.setdefault(a, []).append((b, w))
        out.setdefault(b, []).append((a, w))
    return out


ADJ = adjacency()


def rooted_profile(gate: str) -> tuple[dict[str, int], dict[str, str]]:
    offset = {gate: 0}
    parent: dict[str, str] = {}
    queue = deque([gate])
    while queue:
        v = queue.popleft()
        for u, w in ADJ[v]:
            if u in offset:
                continue
            offset[u] = offset[v] + w
            parent[u] = v
            queue.append(u)
    return offset, parent


def parse_group(text: str) -> list[int]:
    return [] if text == "" else [int(x) for x in text.split(",")]


def parse_signature(sig: str) -> dict[str, object]:
    parts = sig.split("|")
    if len(parts) < 7:
        raise ValueError(f"bad signature: {sig}")
    root_color: dict[int, int] = {}
    for color, field in enumerate(parts[4:7]):
        for y in parse_group(field):
            if y in root_color:
                raise ValueError("duplicate selected root")
            root_color[y] = color
    if len(root_color) != 10:
        raise ValueError("signature is not exact-10")
    return {
        "raw": sig,
        "s": int(parts[0]),
        "shape": parts[1],
        "d1": int(parts[2]),
        "d2": int(parts[3]),
        "root_color": root_color,
    }


def extract_signatures(source: dict[str, object]) -> tuple[list[str], str]:
    """Accept either the capped primary examples or the complete replay list."""
    complete = source.get("canonical_root_signatures")
    if isinstance(complete, list):
        return [str(sig) for sig in complete], "canonical_root_signatures"
    examples = source.get("first_examples")
    if isinstance(examples, list):
        return [str(sig) for sig in examples], "first_examples"
    raise ValueError("input has neither canonical_root_signatures nor first_examples")


def assess_row(
    parsed: dict[str, object], gate: str, q: int, row_kind: str
) -> dict[str, object]:
    s = int(parsed["s"])
    d1 = int(parsed["d1"])
    d2 = int(parsed["d2"])
    root_color = dict(parsed["root_color"])  # type: ignore[arg-type]
    B = 280 - s
    A = B + 20
    low_depth_to_color = {0: 0, d1: 1, d2: 2}
    offset, parent_vertex = rooted_profile(gate)
    t = A - q

    location: dict[str, tuple[str, int]] = {}
    bad_depths: list[dict[str, int]] = []
    for v, off in offset.items():
        depth = t + off
        if B <= depth <= A:
            location[v] = ("HIGH", depth - B)
        elif depth in low_depth_to_color:
            location[v] = ("LOW", low_depth_to_color[depth])
        else:
            bad_depths.append({"vertex": v, "depth": depth})
    base = {
        "kind": row_kind,
        "gate": gate,
        "q": q,
        "gate_depth": t,
    }
    if bad_depths:
        return {
            **base,
            "compatible": False,
            "reason": "core_depth_not_in_exact_D",
            "bad_depths": bad_depths,
        }

    fixed_high_children: dict[int, int] = {}
    forced_roots: dict[int, int] = {}
    for child, parent in parent_vertex.items():
        child_kind, child_id = location[child]
        parent_kind, parent_id = location[parent]
        if child_kind == "LOW":
            if parent_kind != "LOW":
                raise AssertionError("rooted core depth decreased")
            continue
        if parent_kind == "HIGH":
            fixed_high_children[child_id] = parent_id
        else:
            forced_roots[child_id] = parent_id

    selected_parent_conflicts = sorted(set(fixed_high_children).intersection(root_color))
    if selected_parent_conflicts:
        return {
            **base,
            "compatible": False,
            "reason": "selected_root_has_fixed_core_parent",
            "conflicting_selected_root_y": selected_parent_conflicts,
        }

    forced_color_conflicts = sorted(
        y for y, color in forced_roots.items()
        if y in root_color and root_color[y] != color
    )
    if forced_color_conflicts:
        return {
            **base,
            "compatible": False,
            "reason": "selected_root_wrong_forced_low_color",
            "conflicting_selected_root_y": forced_color_conflicts,
        }

    f_c = len(fixed_high_children)
    if row_kind == "A" and f_c != 5:
        raise AssertionError("bad all-high fixed-edge count")
    if row_kind == "B" and f_c != 4:
        raise AssertionError("bad Class B fixed-edge count")
    if row_kind == "C" and f_c != 3:
        raise AssertionError("bad Class C fixed-edge count")

    missing_forced = sorted(set(forced_roots) - set(root_color))
    class_min_c = {"A": 10, "B": 11, "C": 12}[row_kind]
    # For s=154, the high-component envelope permits c=14.  Keep the
    # endpoint inclusive here: range(..., 15) is the exact c=10..14 domain.
    possible_c = [
        c for c in range(class_min_c, 15)
        if c - 10 >= len(missing_forced)
    ]
    if not possible_c:
        return {
            **base,
            "compatible": False,
            "reason": "forced_roots_exceed_c14",
        }

    return {
        **base,
        "compatible": True,
        "class": row_kind,
        "f_C": f_c,
        "possible_c": possible_c,
        "core_location": {
            v: {"kind": kind, "id": ident}
            for v, (kind, ident) in sorted(location.items())
        },
        "fixed_high_parent": {
            str(y): p for y, p in sorted(fixed_high_children.items())
        },
        "forced_roots": {
            str(y): color for y, color in sorted(forced_roots.items())
        },
        "missing_forced_roots": missing_forced,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--compatible-only",
        action="store_true",
        help="omit rejected row records while retaining exact compatibility counts",
    )
    args = parser.parse_args()
    source = json.loads(args.input.read_text())
    signature_texts, signature_field = extract_signatures(source)
    signatures = [parse_signature(sig) for sig in signature_texts]

    results = []
    total_compatible = 0
    for parsed in signatures:
        rows = []
        for gate, qs in ALL_HIGH_Q.items():
            for q in qs:
                rows.append(assess_row(parsed, gate, q, "A"))
        for gate, qs in MIXED_Q.items():
            for q in qs:
                # f_C determines B versus C after exact embedding.
                row_kind = "B" if gate in {"b2", "a"} else "C"
                # d6 q=24,26 has f_C=4 (B); q>=28 has f_C=3 (C).
                if gate == "d6":
                    row_kind = "B" if q <= 26 else "C"
                rows.append(assess_row(parsed, gate, q, row_kind))
        compatible = [r for r in rows if r["compatible"]]
        total_compatible += len(compatible)
        results.append({
            "signature": parsed["raw"],
            "compatible_rows": len(compatible),
            "compatible_by_class": {
                cls: sum(1 for r in compatible if r["class"] == cls)
                for cls in ("A", "B", "C")
            },
            "rows": compatible if args.compatible_only else rows,
        })

    out = {
        "status": "FW303_GATE_COMPATIBILITY_PREFILTER_COMPLETE",
        "source_status": source.get("status"),
        "source_survivor_count": source.get("survivor_count"),
        "source_signature_field": signature_field,
        "source_signature_count": len(signature_texts),
        "compatible_only": args.compatible_only,
        "signatures_checked": len(signatures),
        "gate_rows_per_signature": 38,
        "total_compatible_signature_rows": total_compatible,
        "results": results,
    }
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
