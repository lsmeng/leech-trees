#!/usr/bin/env python3
"""Verify the fixed-d1 exact remainder batch without running the search."""
import hashlib
import json
import os
import sys


DS = list(range(38, 126, 2))
SEMANTIC = (
    "params_total",
    "params_valid",
    "params_with_survivor",
    "dfs_calls",
    "extension_invocations",
    "survivor_count",
)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def primary_signatures(obj):
    vals = []
    for raw in obj.get("first_examples", []):
        vals.append(raw.split("|C=", 1)[0])
    return vals


def digest(values):
    payload = "\n".join(sorted(values)).encode()
    return hashlib.sha256(payload).hexdigest()


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify_remainder_exact_batch.py BATCH_DIR OUTPUT_JSON")
    root, output = sys.argv[1:]
    records = []
    failures = []
    totals = {k: 0 for k in SEMANTIC}
    for d1 in DS:
        rd = os.path.join(root, "results", "d1_%d" % d1)
        pp = os.path.join(rd, "primary.json")
        rp = os.path.join(rd, "replay.json")
        cp = os.path.join(rd, "exact_v2_certificate.json")
        if not all(os.path.isfile(p) and os.path.getsize(p) > 0 for p in (pp, rp, cp)):
            failures.append({"d1": d1, "reason": "missing_artifact"})
            continue
        p, r, c = load(pp), load(rp), load(cp)
        expected_total = (126 - d1) // 2
        expected_valid = expected_total - (1 if d1 <= 62 else 0)
        checks = {
            "scope": p.get("s") == 152 and r.get("s") == 152 and p.get("shape") == "chain" and r.get("shape") == "chain",
            "d1": p.get("d1_shard") == d1 and r.get("d1") == d1,
            "params_total": p.get("params_total") == expected_total and r.get("params_total") == expected_total,
            "params_valid": p.get("params_valid") == expected_valid and r.get("params_valid") == expected_valid,
            "certificate": c.get("status") == "VERIFIED_EXACT10_SIGNATURE_SET_MATCH",
            "semantic_match": all(p.get(k) == r.get(k) for k in SEMANTIC if k != "extension_invocations"),
            "invocation_match": p.get("full_high_coloring_invocations") == r.get("extension_invocations"),
        }
        ps, rs = primary_signatures(p), r.get("canonical_root_signatures", [])
        checks.update({
            "primary_signature_count": len(ps) == p.get("survivor_count"),
            "replay_signature_count": len(rs) == r.get("survivor_count"),
            "primary_unique": len(ps) == len(set(ps)),
            "replay_unique": len(rs) == len(set(rs)),
            "signature_set_match": set(ps) == set(rs),
        })
        rec = {"d1": d1, "checks": checks, "primary_sha256": hashlib.sha256(open(pp, "rb").read()).hexdigest(), "replay_sha256": hashlib.sha256(open(rp, "rb").read()).hexdigest(), "certificate_sha256": hashlib.sha256(open(cp, "rb").read()).hexdigest(), "signature_sha256": digest(rs)}
        records.append(rec)
        if not all(checks.values()):
            failures.append({"d1": d1, "reason": "check_failed", "checks": checks})
        for k in SEMANTIC:
            key = "full_high_coloring_invocations" if k == "extension_invocations" else k
            totals[k] += p.get(key, 0)
    result = {
        "status": "VERIFIED_REMAINDER_EXACT_BATCH" if len(records) == len(DS) and not failures else "INCOMPLETE_REMAINDER_EXACT_BATCH",
        "d1_shards": DS,
        "shard_count": len(records),
        "expected_shard_count": len(DS),
        "params_total": sum((126 - d) // 2 for d in DS),
        "params_valid": sum((126 - d) // 2 - (1 if d <= 62 else 0) for d in DS),
        "totals_primary": totals,
        "failures": failures,
        "records": records,
    }
    with open(output, "w", encoding="utf-8") as fh:
        json.dump(result, fh, sort_keys=True, indent=2)
        fh.write("\n")
    print(result["status"], "records", len(records), "failures", len(failures))
    return 0 if result["status"].startswith("VERIFIED") else 2


if __name__ == "__main__":
    raise SystemExit(main())
