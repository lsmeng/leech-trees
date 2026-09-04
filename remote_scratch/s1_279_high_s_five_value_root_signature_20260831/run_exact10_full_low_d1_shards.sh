#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 S SHAPE" >&2
  exit 2
fi

s=$1
shape=$2
case "$s" in
  152|154|156|158|160) ;;
  *) echo "bad s: $s" >&2; exit 2 ;;
esac
case "$shape" in
  star|chain) ;;
  *) echo "bad shape: $shape" >&2; exit 2 ;;
esac

B=$((280-s))
outdir="exact10_v4_shards_s${s}_${shape}"
mkdir -p "$outdir"

for ((d1=2; d1<B; d1+=2)); do
  out="$outdir/d1_${d1}.json"
  timing="$outdir/d1_${d1}.time"
  tmp="$out.tmp.$$"
  ttmp="$timing.tmp.$$"

  if [[ -s "$out" ]]; then
    continue
  fi

  rm -f "$tmp" "$ttmp"
  if /usr/bin/time -f 'ELAPSED=%e MAXRSS_KB=%M' -o "$ttmp" \
       nice -n 15 timeout "${EXACT10_TIMEOUT:-300}" \
       ./exact10_full_low_root_signature \
       --s "$s" --shape "$shape" --d1 "$d1" > "$tmp"; then
    mv "$tmp" "$out"
    mv "$ttmp" "$timing"
    if ! python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1]))["survivor_count"] == 0 else 1)' "$out"; then
      echo "SURVIVOR s=$s shape=$shape d1=$d1" >&2
      exit 4
    fi
  else
    rc=$?
    rm -f "$tmp"
    mv "$ttmp" "$timing" 2>/dev/null || true
    echo "FAILED s=$s shape=$shape d1=$d1 rc=$rc" >&2
    exit "$rc"
  fi
done

sha256sum "$outdir"/d1_*.json > "$outdir/SHA256SUMS"
echo "COMPLETE s=$s shape=$shape shards=$(find "$outdir" -name 'd1_*.json' -type f | wc -l)"
