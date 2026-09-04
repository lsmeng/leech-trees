#!/usr/bin/env bash
set -euo pipefail

base=${1:?base directory required}
out="$base/star_independent_py_s152"
primary="$base/exact10_shards_s152_star"
checker="$base/check_exact10_root_signature.py"
mkdir -p "$out"

run_one() {
  local d1=$1
  local dst="$out/d1_${d1}.json"
  local tmp="$dst.tmp.$$"
  if [[ -s "$dst" ]] && grep -q '"expected_json_verified": true' "$dst"; then
    return 0
  fi
  rm -f "$tmp"
  if /usr/bin/time -p timeout 20m nice -n 15 python3 "$checker" \
      --s 152 --shape star --d1 "$d1" \
      --expect-json "$primary/d1_${d1}.json" > "$tmp" 2> "$out/d1_${d1}.time"; then
    mv "$tmp" "$dst"
  else
    rc=$?
    rm -f "$tmp"
    echo "FAILED d1=$d1 rc=$rc" >&2
    return "$rc"
  fi
}
export base out primary checker
export -f run_one
seq 2 2 126 | xargs -P 4 -n 1 bash -c 'run_one "$1"' _
echo "STAR_INDEPENDENT_PY_COMPLETE count=$(find "$out" -maxdepth 1 -name "d1_*.json" -type f | wc -l)"
