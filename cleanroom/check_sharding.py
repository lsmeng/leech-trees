"""Sharding partition identities: for (n,K,L) run all K shards and compare with the full run."""
import subprocess, sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
def run(args):
    out = subprocess.run([os.path.join(here, 'cr_forest')] + [str(a) for a in args], capture_output=True, text=True).stdout
    return json.loads([l for l in out.splitlines() if l.startswith('{')][0])
cases = [(6,3,2),(6,4,3),(10,3,6),(10,7,5),(10,13,8),(11,5,4),(11,4,9),(11,1000,7),(12,13,8),(12,7,5),(12,3,9)]
bad = 0
for n, K, L in cases:
    full = run([n])
    shards = [run([n, '--shard', i, K, '--level', L]) for i in range(K)]
    lv = full['levels']
    prefix = sum(lv[:L+1])
    ok = True
    for d in range(len(lv)):
        if d <= L:
            ok &= all(s['levels'][d] == lv[d] for s in shards)
        else:
            ok &= sum(s['levels'][d] for s in shards) == lv[d]
    ok &= sum(s['nsol'] for s in shards) == full['nsol']
    ok &= sum(s['nodes'] for s in shards) == K * prefix + (full['nodes'] - prefix)
    ok &= all(s['level_L_nodes'] == lv[L] for s in shards)
    print(f"n={n} K={K} L={L}: {'OK' if ok else 'MISMATCH'}  (level-{L} nodes {lv[L]}, nsol {full['nsol']})")
    bad += not ok
print("ALL SHARDING IDENTITIES HOLD" if not bad else f"{bad} FAILURES")
