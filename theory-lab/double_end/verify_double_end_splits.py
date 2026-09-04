#!/usr/bin/env python3
"""Merge and certify sharded double-end runs.

Usage: verify_double_end_splits.py DIR NSPLIT --n N [--out cert.json]

Checks that every shard 0..NSPLIT-1 produced a final (non-.tmp) file whose
summary line reports the expected n and split and status=EXHAUSTED, that no
shard reported a solution, and records the SHA-256 of every shard file.
"""
import argparse, hashlib, json, os, re, sys

SUM = re.compile(r"^DOUBLE_END n=(\d+) N=(\d+) V=(\d+) split=(-?\d+):(\d+)/(\d+) "
                 r"nodes=(\d+) solutions=(\d+) status=(\w+)")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("nsplit", type=int)
    ap.add_argument("--n", type=int, required=True); ap.add_argument("--out")
    a = ap.parse_args()
    errors, files = [], {}
    total_nodes = total_sols = 0
    tmps = [f for f in os.listdir(a.dir) if f.endswith(".tmp")]
    if tmps:
        errors.append("%d unfinished .tmp shards: %s" % (len(tmps), sorted(tmps)[:5]))
    for k in range(a.nsplit):
        p = os.path.join(a.dir, "split_%d_of_%d.txt" % (k, a.nsplit))
        if not os.path.isfile(p):
            errors.append("missing shard %d" % k); continue
        lines = open(p).read().splitlines()
        summ = [l for l in lines if l.startswith("DOUBLE_END ")]
        if len(summ) != 1:
            errors.append("shard %d: %d summary lines" % (k, len(summ))); continue
        m = SUM.match(summ[0])
        if not m:
            errors.append("shard %d: unparsable summary %r" % (k, summ[0][:100])); continue
        n, _N, _V, _lvl, sk, sn, nodes, sols, status = m.groups()
        if int(n) != a.n or int(sk) != k or int(sn) != a.nsplit:
            errors.append("shard %d: scope mismatch %r" % (k, summ[0][:100]))
        if status != "EXHAUSTED":
            errors.append("shard %d: status %s" % (k, status))
        if int(sols):
            errors.append("shard %d: %s SOLUTIONS reported" % (k, sols))
        total_nodes += int(nodes); total_sols += int(sols)
        files["split_%d_of_%d.txt" % (k, a.nsplit)] = sha256(p)
    status = ("CERTIFIED_FINITE_IMPOSSIBLE_ORDER_%d" % a.n) if (not errors and total_sols == 0) \
             else ("SOLUTIONS" if total_sols else "GAP")
    cert = {"status": status, "n": a.n, "dir": os.path.abspath(a.dir),
            "nsplit": a.nsplit, "total_nodes": total_nodes,
            "total_solutions": total_sols, "errors": errors, "file_sha256": files}
    print(json.dumps({k: v for k, v in cert.items() if k != "file_sha256"}, indent=1))
    if a.out:
        json.dump(cert, open(a.out, "w"), indent=1, sort_keys=True)
        print("certificate sha256", sha256(a.out))
    sys.exit(0 if status.startswith("CERTIFIED") else 1)


if __name__ == "__main__":
    main()
