#!/bin/bash
# usage: run_shards.sh n K L nworkers  -> results/cleanroom_forest_${n}_shard${w}.jsonl (worker w does shards i = w, w+W, ...)
# resumable: skips shards already recorded with status DONE.
n=$1; K=$2; L=$3; W=$4
here=$(cd "$(dirname "$0")" && pwd); res="$here/../results"
mkdir -p "$res"
for ((w=0; w<W; w++)); do
  (
    out="$res/cleanroom_forest_${n}_shard${w}.jsonl"
    for ((i=w; i<K; i+=W)); do
      if [ -f "$out" ] && grep -q "\"shard\":\[$i,$K,$L\].*\"status\":\"DONE\"" "$out"; then continue; fi
      nice -n 15 "$here/cr_forest" $n --shard $i $K --level $L >> "$out"
    done
  ) &
done
wait
