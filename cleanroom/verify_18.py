"""Aggregate results/cleanroom_forest_18_shard*.jsonl and compare with the reference per-level counts."""
import json, glob, os, sys
here = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1]) if len(sys.argv) > 1 else 18
recs = {}
for f in sorted(glob.glob(os.path.join(here, '..', 'results', f'cleanroom_forest_{n}_shard*.jsonl'))):
    for line in open(f):
        if line.startswith('{'):
            r = json.loads(line); recs[r['shard'][0]] = r
        elif line.startswith('SOL'):
            print("WITNESS LINE:", line.strip())
if not recs: print("no records"); sys.exit(1)
K, L = next(iter(recs.values()))['shard'][1:]
print(f"n={n} K={K} L={L}: {len(recs)}/{K} shards done")
assert all(r['shard'][1:] == [K, L] and r['status'] == 'DONE' for r in recs.values())
levels = [0] * n
for r in recs.values():
    for d, c in enumerate(r['levels']): levels[d] += c
prefix = [1,1,2,8,41,229,1384,8899,62843]
for r in recs.values(): assert r['levels'][:L+1] == prefix[:L+1], r
nodes = sum(r['nodes'] for r in recs.values()); nsol = sum(r['nsol'] for r in recs.values())
print("sum of levels (levels<=L counted K times):", levels)
if len(recs) == K:
    per = prefix + levels[L+1:]
    print("per-level counts:", per)
    print("nodes total (unique):", nodes - (K-1)*sum(prefix), " nsol:", nsol, " CPU-s:", round(sum(r['secs'] for r in recs.values())))
    ref = {18: [1,1,2,8,41,229,1384,8899,62843,480085,3984162,35540837,332597341,2896330052,17017193146,37669242243,1824413062,0],
           17: [1,1,2,8,41,229,1384,8899,62843,480084,3983102,35234962,303618177]}
    if n in ref:
        ok = per[:len(ref[n])] == ref[n]
        print("REFERENCE PER-LEVEL MATCH:", ok)
        if n == 18: print("unique nodes == 59,779,854,336:", nodes - (K-1)*sum(prefix) == 59779854336)
