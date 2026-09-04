#!/usr/bin/env bash
# Official independent sweep of the whole delta=279 (r=3) singleton normal form:
# every s in [13,160], both low shapes, every 0<d1<d2<B of any parity.
# Four nice -n 15 workers, each a single process over a contiguous s-range.
set -u
cd "$(dirname "$0")"
out=r3_full_sweep
mkdir -p "$out"
run_range() {
  lo=$1; hi=$2
  f="$out/sweep_s${lo}_${hi}.txt"
  test -s "$f" && return 0
  ( for s in $(seq "$lo" "$hi"); do for sh in chain star; do
      nice -n 15 ./s1_direct_search --r 3 --s "$s" --shape "$sh" --all-d-any --nodes-limit 200000000
    done; done ) > "$f.tmp" 2>&1 && mv "$f.tmp" "$f"
}
# small s has large B and many (d1,d2) pairs: balance ranges by C(279-s,2)
run_range 13 40 &
run_range 41 70 &
run_range 71 105 &
run_range 106 160 &
wait
cat "$out"/sweep_s*.txt | grep -c EXHAUSTED_EMPTY
cat "$out"/sweep_s*.txt | grep -v EXHAUSTED_EMPTY | head
echo R3_FULL_SWEEP_DONE
