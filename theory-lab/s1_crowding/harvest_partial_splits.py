#!/usr/bin/env python3
"""Harvest completed (split, shape) pairs from a depth-phase run that was cut
short by the wall clock, and emit the residual work.

The array script writes one ABSTRACT line per shape as it finishes and only
renames the .tmp to .txt when the whole shapes file is done.  A task killed at
the wall therefore leaves a .tmp whose ABSTRACT lines are still valid evidence
for the shapes it did complete.  This script collects those, checks them for
survivors and scope, and writes one residual shapes file per split so the
remaining work can be resubmitted without redoing anything.

Usage:
  harvest_partial_splits.py DIR NSPLIT --m M --shapes SHAPESFILE
                            [--resid-dir residual] [--out harvest.json]
"""
import argparse, hashlib, json, os, re, sys

LINE = re.compile(r"^ABSTRACT m=(\d+) r=(\d+) lowpar=([0-9,]*) xcap=\d+ "
                  r"split=(-?\d+):(\d+)/(\d+) leaves=(\d+) nodes=(\d+) (\w+)"
                  r"(?: depth_survivors=(\d+))?")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("nsplit", type=int)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--shapes", required=True)
    ap.add_argument("--resid-dir"); ap.add_argument("--out")
    a = ap.parse_args()
    shapes = [l.strip() for l in open(a.shapes) if l.strip() and not l.startswith("#")]
    done = {}        # split -> set of shapes completed
    survivors, errors, files = [], [], {}
    agg = {s: {"splits_done": 0, "leaves": 0, "nodes": 0, "survivors": 0} for s in shapes}
    for k in range(a.nsplit):
        base = os.path.join(a.dir, "split_%d_of_%d.txt" % (k, a.nsplit))
        path = base if os.path.isfile(base) else base + ".tmp"
        if not os.path.isfile(path):
            errors.append("split %d: no output at all" % k)
            done[k] = set()
            continue
        files[os.path.basename(path)] = sha256(path)
        seen = set()
        for line in open(path).read().splitlines():
            if line.startswith("DEPTH_SURVIVOR"):
                survivors.append("split %d: %s" % (k, line[:160]))
            mm = LINE.match(line)
            if not mm:
                continue
            m, _r, lowpar, _lvl, sk, sn, leaves, nodes, status = mm.group(1,2,3,4,5,6,7,8,9)
            if int(m) != a.m or int(sk) != k or int(sn) != a.nsplit:
                errors.append("split %d: scope mismatch %r" % (k, line[:90])); continue
            if status != "EXHAUSTED":
                errors.append("split %d shape %s: status %s" % (k, lowpar, status)); continue
            if lowpar not in agg:
                errors.append("split %d: unexpected shape %s" % (k, lowpar)); continue
            seen.add(lowpar)
            agg[lowpar]["splits_done"] += 1
            agg[lowpar]["leaves"] += int(leaves); agg[lowpar]["nodes"] += int(nodes)
            if mm.group(10) is not None:
                agg[lowpar]["survivors"] += int(mm.group(10))
        done[k] = seen
    missing = {k: [s for s in shapes if s not in done[k]] for k in range(a.nsplit)}
    n_missing = sum(len(v) for v in missing.values())
    complete_shapes = [s for s in shapes if agg[s]["splits_done"] == a.nsplit]
    if a.resid_dir and n_missing:
        os.makedirs(a.resid_dir, exist_ok=True)
        for k, ms in missing.items():
            if ms:
                with open(os.path.join(a.resid_dir, "shapes_split_%d.txt" % k), "w") as f:
                    f.write("\n".join(ms) + "\n")
    rep = {"dir": os.path.abspath(a.dir), "nsplit": a.nsplit, "m": a.m,
           "shapes_total": len(shapes),
           "shapes_complete_across_all_splits": len(complete_shapes),
           "missing_split_shape_pairs": n_missing,
           "total_survivors_seen": len(survivors), "survivor_lines": survivors[:20],
           "errors": errors[:40], "per_shape": agg}
    print(json.dumps({k: v for k, v in rep.items() if k != "per_shape"}, indent=1))
    print("shapes finished in ALL %d splits: %d / %d"
          % (a.nsplit, len(complete_shapes), len(shapes)))
    if a.out:
        rep["file_sha256"] = files
        json.dump(rep, open(a.out, "w"), indent=1, sort_keys=True)
        print("harvest report sha256", sha256(a.out))
    sys.exit(0 if not survivors else 2)


if __name__ == "__main__":
    main()
