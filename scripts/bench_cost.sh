#!/bin/bash
# per-node cost under load: run BIN with a node cap R times, report min user-CPU seconds per node.
# usage: scripts/bench_cost.sh BIN file.jsonl NODECAP REPS [flags]
BIN=$1; F=$2; CAP=$3; REPS=$4; shift 4
best=999999; nodes=0
for r in $(seq 1 $REPS); do
  TMP=$(mktemp); { /usr/bin/time -p "$BIN" --nodes $CAP "$@" "$F" > "$TMP"; } 2> "$TMP.t"
  u=$(grep '^user' "$TMP.t" | awk '{print $2}')
  nodes=$(python3 -c "import json,sys; print(sum(json.loads(l)['nodes'] for l in open('$TMP')))")
  best=$(python3 -c "print(min($best,$u))"); rm -f "$TMP" "$TMP.t"
done
python3 -c "print('nodes',$nodes,'min user',$best,'us/node',round($best/$nodes*1e6,3))"
