#!/usr/bin/env bash
set -e
base=/home/geo/codex-work/leech-trees/remote_scratch/s1_279_high_s_five_value_root_signature_20260831
batch=$base/exact10_batch_s152_chain_20260901
prefilter=$batch/remainder_fw303_prefilter.json
sharddir=$batch/remainder_forest_shards_v2
mkdir -p "$sharddir"
cd "$base"
run_one() {
  start=$1
  stop=$2
  out="$sharddir/result_${start}_${stop}.json"
  tim="$sharddir/result_${start}_${stop}.time"
  test -s "$out" && return 0
  /usr/bin/time -p timeout 20m nice -n 15 python3 "$base/search_fw303_all_class_forests.py" "$prefilter" "$out" --start "$start" --stop "$stop" --max-examples 1000000 2> "$tim"
}
starts=()
for start in $(seq 0 200 24000); do starts+=( "$start" ); done
n=${#starts[@]}
for ((i=0; i<n; i+=4)); do
  pids=()
  for ((j=i; j<i+4 && j<n; j++)); do
    start=${starts[j]}
    stop=$((start+200))
    if (( stop > 24077 )); then stop=24077; fi
    run_one "$start" "$stop" &
    pids+=( "$!" )
  done
  for pid in "${pids[@]}"; do wait "$pid"; done
done
echo FOREST_BATCH_COMPLETE
