#!/usr/bin/env python3
"""Aggregate sharded mdd_forest outputs: agg_mdd.py results_dir n D  -> summary JSON (shards done, sum nodes, nsol, distinct SOL lines)"""
import sys, glob, json
d, n, D = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
files = sorted(glob.glob(f"{d}/mdd_{n}_{D}_shard*.jsonl"))
tot = 0; ns = 0; done = 0; K = None; sols = []; times = []
for f in files:
    for l in open(f):
        if l.startswith("SOL:"): sols.append(l.strip()[4:].strip())
        elif l.startswith("{"):
            j = json.loads(l); tot += j["nodes"]; ns += j["nsol"]; done += j["status"] == "DONE"; K = j["shard"][1]; times.append(j["time"])
print(json.dumps({"n": n, "D": D, "shards": len(files), "K": K, "done": done, "sum_nodes": tot, "nsol": ns, "distinct_sols": len(set(sols)), "cpu_s": round(sum(times), 1), "max_shard_s": round(max(times), 1) if times else None, "sols": sorted(set(sols))}))
