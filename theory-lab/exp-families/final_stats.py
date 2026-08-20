"""Consolidate run_*.out files into per-family totals for REPORT.md.

Handles resumed runs: a family's results are the concatenation of segments
(run file, id offset into the family shape file, count of ids to take).
The single overlap (cat25_p5 original id 481 searched twice) is resolved by
taking the resumed run's result for it (both were capped runs; result identical
status anyway) -- see SEGMENTS below.
"""
import json
import sys

# family -> (shape_file, [(run_file, take_from_run_start, n_take, family_id_offset)])
# For sorted spider files ids refer to the SORTED shape file also listed here.
SEGMENTS = {
    "cat25_spine<=4": ("shapes_cat25_p1_4.txt",
                       [("run_cat25_p1_4.out", 0, 903, 0)]),
    "cat25_spine=5": ("shapes_cat25_p5.txt",
                      [("run_cat25_p5_t20.out", 0, 481, 0),
                       ("run_cat25_p5_rest_t5.out", 0, None, 481)]),
    "diam4_25": ("shapes_diam4_25.txt",
                 [("run_diam4_25_t20.out", 0, 803, 0),
                  ("run_diam4_25_rest_t5.out", 0, None, 803)]),
    "spider_25(sorted)": ("spider25_concat.txt",
                          [("run_spider_25_t20.out", 0, 156, 0),
                           ("run_spider_25_rest_t20.out", 0, 131, 156),
                           ("run_spider_25_rest2_t5.out", 0, None, 287)]),
    "diam4_27": ("shapes_diam4_27.txt",
                 [("run_diam4_27_t5.out", 0, None, 0)]),
    "spider_27(sorted)": ("shapes_spider_27_sorted.txt",
                          [("run_spider_27_sorted_t5.out", 0, None, 0)]),
    "cat27_spine<=4": ("shapes_cat27_p1_4.txt",
                       [("run_cat27_p1_4_t5.out", 0, None, 0)]),
    "diam5_25": ("shapes_diam5_25.txt",
                 [("run_diam5_25_t5.out", 0, None, 0)]),
}


def parse_run(path):
    out = []
    wits = []
    try:
        fh = open(path)
    except FileNotFoundError:
        return out, wits
    for line in fh:
        if line.startswith("RES"):
            kv = dict(p.split("=") for p in line.split()[1:])
            out.append((int(kv["id"]), int(kv["nodes"]), int(kv.get("attempts", 0)),
                        int(kv["found"]), int(kv["capped"]),
                        float(kv.get("time", 0.0))))
        elif line.startswith("WITNESS"):
            wits.append(line.strip())
    return out, wits


def main():
    grand_wits = []
    rows = []
    detail = {}
    for fam, (shape_file, segs) in SEGMENTS.items():
        done = capped = found = 0
        nodes = attempts = 0
        maxnodes = 0
        tsum = 0.0
        capped_fids = []
        for run_file, start, ntake, off in segs:
            res, wits = parse_run(run_file)
            grand_wits += [(fam, w) for w in wits]
            res = res[start:start + ntake if ntake else None]
            for (i, nd, at, fo, ca, tm) in res:
                done += 1
                nodes += nd; attempts += at
                maxnodes = max(maxnodes, nd)
                tsum += tm
                found += fo
                if ca:
                    capped += 1
                    capped_fids.append(off + (i - (res[0][0] if res else 0)))
        try:
            total_shapes = sum(1 for _ in open(shape_file))
        except FileNotFoundError:
            total_shapes = None
        rows.append((fam, total_shapes, done, done - capped, capped, found,
                     nodes, maxnodes, tsum))
        detail[fam] = capped_fids
    hdr = f"{'family':22} {'#shapes':>8} {'attempted':>9} {'excluded':>9} {'capped':>7} {'found':>5} {'nodes':>15} {'cpu_s':>9}"
    print(hdr)
    for r in rows:
        fam, tot, done, excl, cap, fo, nd, mx, ts = r
        print(f"{fam:22} {str(tot):>8} {done:>9} {excl:>9} {cap:>7} {fo:>5} {nd:>15,} {ts:>9.0f}")
    if grand_wits:
        print("\n!!!!!!!!!!!! WITNESSES !!!!!!!!!!!!")
        for fam, w in grand_wits:
            print(fam, w)
    else:
        print("\nNo Leech labeling found anywhere (0 witnesses).")
    json.dump({fam: caps for fam, caps in detail.items()},
              open("capped_ids.json", "w"))
    print("capped family-ids -> capped_ids.json")


if __name__ == "__main__":
    main()
