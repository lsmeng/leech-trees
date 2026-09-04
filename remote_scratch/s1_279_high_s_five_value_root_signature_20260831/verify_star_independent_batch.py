#!/usr/bin/env python3
"""Strict read-only verifier for the s=152 star independent exact10 batch."""

import argparse
import json
from pathlib import Path


def load(path: Path):
    with path.open() as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primary", type=Path, required=True)
    ap.add_argument("--independent", type=Path, required=True)
    ap.add_argument("--allow-missing-sentinel", action="store_true")
    args = ap.parse_args()

    expected_d1 = list(range(2, 126, 2))
    optional = 126
    compare = (
        "s", "B", "shape", "params_total", "params_valid",
        "params_with_survivor", "survivor_count", "survivor_xor_fnv1a64",
        "survivor_sum_fnv1a64", "color_count_histogram",
    )
    total = {k: 0 for k in ("params_total", "params_valid",
                            "params_with_survivor", "survivor_count")}
    checked = []
    errors = []

    for d1 in expected_d1 + [optional]:
        pp = args.primary / f"d1_{d1}.json"
        ip = args.independent / f"d1_{d1}.json"
        if not pp.exists():
            errors.append(f"missing primary d1={d1}")
            continue
        if not ip.exists():
            if d1 == optional and args.allow_missing_sentinel:
                continue
            errors.append(f"missing independent d1={d1}")
            continue
        p, i = load(pp), load(ip)
        if d1 == optional:
            if p.get("params_total") != 0 or p.get("params_valid") != 0:
                errors.append("d1=126 is not the expected empty sentinel")
            if i.get("params_total") != 0 or i.get("params_valid") != 0:
                errors.append("independent d1=126 is not empty")
        for key in compare:
            if key == "shape" and (p.get(key), i.get(key)) != ("star", "star"):
                errors.append(f"d1={d1} shape mismatch: {p.get(key)!r}/{i.get(key)!r}")
            elif key != "shape" and p.get(key) != i.get(key):
                errors.append(f"d1={d1} field {key} mismatch: {p.get(key)!r}/{i.get(key)!r}")
        if p.get("d1_shard", d1) != d1 or i.get("d1", d1) != d1:
            errors.append(f"d1={d1} shard identity mismatch")
        if p.get("status") != "EXACT10_ROOT_SUBSYSTEM_EXHAUSTED":
            errors.append(f"d1={d1} unexpected primary status {p.get('status')!r}")
        if i.get("status") != "INDEPENDENT_EXACT10_ROOT_SUBSYSTEM_EXHAUSTED":
            errors.append(f"d1={d1} unexpected independent status {i.get('status')!r}")
        if i.get("expected_json_verified") is not True:
            errors.append(f"d1={d1} expected_json_verified is not true")
        for key in total:
            total[key] += int(i.get(key, 0))
        checked.append(d1)

    if checked and optional in checked:
        checked_nonempty = [d for d in checked if d != optional]
    else:
        checked_nonempty = checked
    if checked_nonempty != expected_d1:
        errors.append(f"nonempty d1 coverage mismatch: {checked_nonempty}")
    if total["params_total"] != 1953:
        errors.append(f"params_total aggregate {total['params_total']} != 1953")
    if total["params_valid"] != 1612:
        errors.append(f"params_valid aggregate {total['params_valid']} != 1612")
    if total["params_with_survivor"] != 0 or total["survivor_count"] != 0:
        errors.append(f"nonzero survivors: {total}")

    result = {"status": "VERIFIED_STAR_INDEPENDENT_EXACT_BATCH" if not errors else "GAP",
              "checked_d1": checked, "aggregate": total, "errors": errors}
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
