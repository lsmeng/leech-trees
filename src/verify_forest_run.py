"""Verdict script for a sharded forest-engine run (referee-forest.md §8).
Usage: python src/verify_forest_run.py <n> <dir with forest_order_{n}_shard{i}.jsonl and forest_{n}_{i}.err> <K> <L>
Checks: exactly K DONE records with indices 0..K-1 once, consistent [K,L]; per-level histograms: levels<=L identical to
prefix in every shard; sums over shards for levels L+1.. compared to reference exact counts (n=18 L9..L12 from the
independent Python oracle in referee-forest.md); reports Σnsol, unique nodes."""
import sys, json, glob, os, re, hashlib
n, d, K, L = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
REF = {18: {9: 480085, 10: 3984162, 11: 35540837, 12: 332597341}, 17: {9: 480084, 10: 3983102, 11: 35234962, 12: 303618177}}
PREFIX = [1, 1, 2, 8, 41, 229, 1384, 8899, 62843]
recs = {}
for f in glob.glob(os.path.join(d, f"forest_order_{n}_shard*.jsonl")):
    js = [l for l in open(f).read().splitlines() if l.startswith("{")]
    if not js: print("NO RECORD", f); continue
    r = json.loads(js[-1]); i = r["shard"][0]
    assert r["shard"][1] == K and r["shard"][2] == L, (f, r["shard"])
    assert i not in recs, ("dup", i); recs[i] = r
assert sorted(recs) == list(range(K)), ("missing shards", sorted(set(range(K)) - set(recs))[:10])
assert all(r["status"] == "DONE" for r in recs.values())
nsol = sum(r["nsol"] for r in recs.values()); nodes = sum(r["nodes"] for r in recs.values())
hist = {}
prefix_ok = True; got = 0
for i in range(K):
    ef = os.path.join(d, f"forest_{n}_{i}.err")
    if not os.path.exists(ef): continue
    m = re.search(r"depth:\s*(.*)", open(ef).read())
    if not m: continue
    got += 1
    h = {int(a): int(b) for a, b in (tok.split(":") for tok in m.group(1).split())}
    for lev in range(min(L, len(PREFIX) - 1) + 1):
        if h.get(lev, 0) != PREFIX[lev]: prefix_ok = False; print("prefix mismatch shard", i, lev, h.get(lev))
    for lev, c in h.items():
        if lev > L: hist[lev] = hist.get(lev, 0) + c
print(f"n={n} K={K} L={L}: {len(recs)} DONE records, Σnsol={nsol}, Σnodes={nodes}, histograms found={got}/{K}, prefix_ok={prefix_ok}")
for lev in sorted(hist):
    ref = REF.get(n, {}).get(lev)
    print(f"  level {lev}: {hist[lev]}" + (f"  ref {ref}  {'OK' if ref == hist[lev] else 'MISMATCH'}" if ref else ""))
print("engine sha256", hashlib.sha256(open(os.path.join(os.path.dirname(__file__), "forest_search.cpp"), "rb").read()).hexdigest()[:16])
