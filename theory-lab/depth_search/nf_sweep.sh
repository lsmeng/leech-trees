#!/bin/bash
# Full normal-form sweep for one order: all r (1..k-2), all s.  Prints per-order totals.
# Usage: nf_sweep.sh <order> [extra depth_search args...]
cd "$(dirname "$0")"
N=$1; shift
K=$((N-1))
TOT=0; SOLS=0; INST=0
T0=$(python3 -c 'import time;print(time.time())')
for ((r=1; r<=K-2; r++)); do
  ./depth_search --order $N --nf --r $r --all-s --no-witness "$@"
done > /tmp/nfsweep_$N.txt 2>&1
T1=$(python3 -c 'import time;print(time.time())')
python3 - "$N" "$T0" "$T1" <<'PY'
import sys,re
n,t0,t1=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
tot=0;sols=0;inst=0;ab=0
for line in open(f"/tmp/nfsweep_{n}.txt"):
    m=re.search(r"sols=(\d+) nodes=(\d+)",line)
    if m:
        inst+=1; sols+=int(m.group(1)); tot+=int(m.group(2))
        if "ABORTED" in line: ab+=1
print(f"NFSWEEP order={n} instances={inst} nodes={tot} sols={sols} aborted={ab} wall={t1-t0:.2f}s")
PY
