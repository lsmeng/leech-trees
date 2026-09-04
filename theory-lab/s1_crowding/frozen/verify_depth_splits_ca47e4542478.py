#!/usr/bin/env python3
"""Merge and verify prefix-split depth-phase outputs of abstract_class_search.

Usage: verify_depth_splits.py DIR NSPLIT --m M --shapes SHAPESFILE [--out CERT.json]

Checks:
  * exactly one final file split_k_of_NSPLIT.txt for every k in [0,NSPLIT)
    (no .tmp leftovers, no missing splits);
  * every file ends with SHAPES_FILE_SUMMARY ... COMPLETE and contains one
    ABSTRACT line per shape of SHAPESFILE, each EXHAUSTED with the expected
    m and split=5:k/NSPLIT;
  * per-shape totals of leaves, nodes, depth_survivors, rho_csp_runs;
  * total depth_survivors == 0  (otherwise the certificate status is SURVIVORS).
Writes a JSON certificate with SHA-256 of every split file.
"""
import argparse, hashlib, json, os, re, sys

LINE = re.compile(r"^ABSTRACT m=(\d+) r=(\d+) lowpar=([0-9,]*) xcap=\d+ split=(-?\d+):(\d+)/(\d+) leaves=(\d+) nodes=(\d+) (\w+)"
                  r"(?: depth_survivors=(\d+) structures_with_survivor=(\d+) csp_nodes=(\d+)(?: rho_csp_runs=(\d+) rho_memo_hits=(\d+) rho_prefix_prunes=(\d+) leaf_rho_dead=(\d+) leaf_checks=(\d+))?)?")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("nsplit", type=int)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--shapes", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    shapes = [l.strip() for l in open(a.shapes) if l.strip() and not l.startswith("#")]
    errors = []
    per_shape = {s: {"tasks": 0, "leaves": 0, "nodes": 0, "depth_survivors": 0, "rho_csp_runs": 0, "csp_nodes": 0} for s in shapes}
    files = {}
    tmps = [f for f in os.listdir(a.dir) if f.endswith(".tmp")]
    if tmps:
        errors.append(f"{len(tmps)} unfinished .tmp files: {sorted(tmps)[:5]}")
    for k in range(a.nsplit):
        p = os.path.join(a.dir, f"split_{k}_of_{a.nsplit}.txt")
        if not os.path.isfile(p):
            errors.append(f"missing split {k}")
            continue
        text = open(p).read().splitlines()
        if not text or not text[-1].startswith("SHAPES_FILE_SUMMARY") or not text[-1].endswith("COMPLETE"):
            errors.append(f"split {k}: no COMPLETE summary")
        seen = set()
        for line in text:
            if line.startswith("DEPTH_SURVIVOR"):
                errors.append(f"split {k}: survivor line: {line[:120]}")
            mm = LINE.match(line)
            if not mm:
                continue
            m, r, lowpar, lvl, sk, sn, leaves, nodes, status = mm.group(1, 2, 3, 4, 5, 6, 7, 8, 9)
            if int(m) != a.m or int(sk) != k or int(sn) != a.nsplit:
                errors.append(f"split {k}: scope mismatch in line {line[:80]}")
            if status != "EXHAUSTED":
                errors.append(f"split {k}: shape {lowpar} status {status}")
            if lowpar not in per_shape:
                errors.append(f"split {k}: unexpected shape {lowpar}")
                continue
            if lowpar in seen:
                errors.append(f"split {k}: duplicate shape {lowpar}")
            seen.add(lowpar)
            ps = per_shape[lowpar]
            ps["tasks"] += 1
            ps["leaves"] += int(leaves)
            ps["nodes"] += int(nodes)
            if mm.group(10) is None:
                errors.append(f"split {k}: shape {lowpar} has no depth fields")
            else:
                ps["depth_survivors"] += int(mm.group(10))
                ps["csp_nodes"] += int(mm.group(12))
                if mm.group(13) is not None:
                    ps["rho_csp_runs"] += int(mm.group(13))
        missing = set(shapes) - seen
        if missing:
            errors.append(f"split {k}: shapes not run: {sorted(missing)}")
        files[f"split_{k}_of_{a.nsplit}.txt"] = sha256(p)
    total_surv = sum(v["depth_survivors"] for v in per_shape.values())
    status = "VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY" if not errors and total_surv == 0 else ("SURVIVORS" if total_surv else "GAP")
    cert = {"status": status, "dir": os.path.abspath(a.dir), "nsplit": a.nsplit, "m": a.m, "shapes": shapes,
            "per_shape": per_shape, "total_depth_survivors": total_surv, "errors": errors, "file_sha256": files}
    print(json.dumps({k: v for k, v in cert.items() if k != "file_sha256"}, indent=1))
    if a.out:
        with open(a.out, "w") as f:
            json.dump(cert, f, indent=1, sort_keys=True)
        print("certificate sha256", sha256(a.out))
    sys.exit(0 if status.startswith("VERIFIED") else 1)


if __name__ == "__main__":
    main()
