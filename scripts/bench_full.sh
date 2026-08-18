#!/bin/bash
# full runs, min user time of REPS: scripts/bench_full.sh BIN file REPS [flags]
BIN=$1; F=$2; REPS=$3; shift 3
best=999999; nodes=0
for r in $(seq 1 $REPS); do
  TMP=$(mktemp); { /usr/bin/time -p "$BIN" "$@" "$F" > "$TMP"; } 2> "$TMP.t"
  u=$(grep '^user' "$TMP.t" | awk '{print $2}')
  nodes=$(python3 -c "import json; print(sum(json.loads(l)['nodes'] for l in open('$TMP')))")
  best=$(python3 -c "print(min($best,$u))"); rm -f "$TMP" "$TMP.t"
done
python3 -c "print('flags: $*  nodes',$nodes,'min user',$best,'us/node',round($best/$nodes*1e6,3))"
