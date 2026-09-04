#!/usr/bin/env python3
"""Build a canonical-signature union from completed independent replay shards."""
import hashlib
import json
import os
import sys


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_remainder_exact_union.py BATCH_DIR OUTPUT_JSON")
    batch, output = sys.argv[1:]
    d1_values = list(range(38, 126, 2))
    signatures = []
    per_d1 = []
    for d1 in d1_values:
        path = os.path.join(batch, "results", "d1_%d" % d1, "replay.json")
        with open(path, encoding="utf-8") as fh:
            obj = json.load(fh)
        if obj.get("s") != 152 or obj.get("shape") != "chain" or obj.get("d1") != d1:
            raise SystemExit("scope mismatch for d1=%d" % d1)
        shard = [str(s) for s in obj.get("canonical_root_signatures", [])]
        if len(shard) != len(set(shard)):
            raise SystemExit("duplicate signature in d1=%d" % d1)
        signatures.extend(shard)
        per_d1.append({"d1": d1, "signature_count": len(shard), "sha256": hashlib.sha256(("\n".join(sorted(shard))).encode()).hexdigest()})
    if len(signatures) != len(set(signatures)):
        raise SystemExit("duplicate signature across d1 shards")
    signatures.sort()
    result = {
        "status": "REMAINDER_EXACT_CANONICAL_UNION_BUILT",
        "s": 152,
        "shape": "chain",
        "d1_min": 38,
        "d1_max": 124,
        "d1_shards": d1_values,
        "shard_count": len(d1_values),
        "survivor_count": len(signatures),
        "canonical_root_signatures": signatures,
        "per_d1": per_d1,
    }
    with open(output, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(result["status"], "signatures", len(signatures), "shards", len(d1_values))


if __name__ == "__main__":
    main()
