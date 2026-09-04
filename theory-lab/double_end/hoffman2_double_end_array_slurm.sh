#!/bin/bash
#$ -N doubleend
#SBATCH --job-name=dbl
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --nice=10000
#SBATCH --time=23:50:00
#SBATCH --mem=2G
#SBATCH --cpus-per-task=1
#SBATCH --output=logs/dbl.%A.%a.out
#SBATCH --error=logs/dbl.%A.%a.err
#
# Sharded run of the double-end gap-order engine.
#   sbatch --array=0-255 hoffman2_double_end_array_slurm.sh N LEVEL NSPLIT
# Each task writes  doubleend_n<N>/split_<k>_of_<NSPLIT>.txt  atomically
# (written to .tmp and renamed only on clean completion), so a task killed by
# the wall clock leaves no file and is easy to detect and re-run.
set -u
N=${1:?order n}
LVL=${2:-4}
NSPLIT=${3:-256}
K=${SLURM_ARRAY_TASK_ID:-0}
cd "$(dirname "$0")" || exit 1
mkdir -p logs "doubleend_n${N}"
OUT="doubleend_n${N}/split_${K}_of_${NSPLIT}.txt"
TMP="${OUT}.tmp"
if [ -f "$OUT" ]; then echo "already complete: $OUT"; exit 0; fi
BIN=./double_end_search
if [ ! -x "$BIN" ]; then echo "missing binary $BIN" >&2; exit 2; fi
echo "# host $(hostname) start $(date -u +%FT%TZ)" > "$TMP"
echo "# binary sha256 $(sha256sum $BIN | cut -d' ' -f1)" >> "$TMP"
nice -n 15 "$BIN" "$N" --split "$LVL" "$K" "$NSPLIT" --max-solutions 50 --quiet >> "$TMP" 2>&1
rc=$?
echo "# rc $rc end $(date -u +%FT%TZ)" >> "$TMP"
if [ $rc -eq 0 ] && grep -q "^DOUBLE_END .*status=EXHAUSTED" "$TMP"; then
  mv "$TMP" "$OUT"
  echo "complete: $OUT"
else
  echo "NOT complete (rc=$rc); leaving $TMP for inspection" >&2
  exit 3
fi
