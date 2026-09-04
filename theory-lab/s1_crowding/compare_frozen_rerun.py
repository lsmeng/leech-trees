#!/usr/bin/env python3
"""Accept or reject a frozen-source re-run against a recorded certificate.

The re-run is accepted only if, for every shape, the leaf count, the node count
and the survivor count agree exactly with the recorded certificate, and the
re-run's own status is VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY.  Leaf counts are
the acceptance quantity: they are what the search enumerates, and a divergence
there means the two sources explore different objects.

Usage: compare_frozen_rerun.py NEW_CERT.json OLD_CERT.json
"""
import hashlib, json, sys


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    new_p, old_p = sys.argv[1], sys.argv[2]
    new, old = json.load(open(new_p)), json.load(open(old_p))
    print("recorded certificate : %s  sha256 %s" % (old_p, sha256(old_p)[:16]))
    print("  status %s, survivors %d" % (old["status"], old["total_depth_survivors"]))
    print("re-run certificate   : %s  sha256 %s" % (new_p, sha256(new_p)[:16]))
    print("  status %s, survivors %d" % (new["status"], new["total_depth_survivors"]))
    print()
    problems = []
    if not new["status"].startswith("VERIFIED"):
        problems.append("re-run status is %s, not VERIFIED" % new["status"])
    if new["total_depth_survivors"] != 0:
        problems.append("re-run reports %d survivors" % new["total_depth_survivors"])
    shapes = sorted(set(old["per_shape"]) | set(new["per_shape"]))
    print("%-16s %16s %16s  %s" % ("shape", "leaves(recorded)", "leaves(re-run)", "verdict"))
    for sh in shapes:
        o, n = old["per_shape"].get(sh), new["per_shape"].get(sh)
        if o is None or n is None:
            problems.append("shape %s present in only one run" % sh)
            print("%-16s %16s %16s  MISSING" % (sh, o and o["leaves"], n and n["leaves"]))
            continue
        same = all(o[k] == n[k] for k in ("leaves", "nodes", "depth_survivors"))
        if not same:
            problems.append("shape %s differs: recorded %s, re-run %s"
                            % (sh, {k: o[k] for k in ("leaves", "nodes", "depth_survivors")},
                                   {k: n[k] for k in ("leaves", "nodes", "depth_survivors")}))
        print("%-16s %16d %16d  %s" % (sh, o["leaves"], n["leaves"], "match" if same else "DIFFER"))
    tot_o = sum(v["leaves"] for v in old["per_shape"].values())
    tot_n = sum(v["leaves"] for v in new["per_shape"].values())
    print("%-16s %16d %16d  %s" % ("TOTAL", tot_o, tot_n, "match" if tot_o == tot_n else "DIFFER"))
    print()
    if problems:
        print("REJECTED")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    print("ACCEPTED: the frozen source reproduces the recorded certificate exactly,")
    print("          shape by shape, with zero survivors.")


if __name__ == "__main__":
    main()
