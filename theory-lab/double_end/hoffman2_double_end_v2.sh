#!/bin/bash
#SBATCH --job-name=dbl2
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --nice=10000
#SBATCH --time=02:00:00
#SBATCH --mem=2G
#SBATCH --cpus-per-task=1
#SBATCH --output=logs/dbl2.%A.%a.out
#
# sbatch --array=0-K hoffman2_double_end_v2.sh N LEVEL NSPLIT TAG [extra flags...]
# Output: doubleend_<TAG>/split_<k>_of_<NSPLIT>.txt   (renamed from .tmp only
# when the shard reports status=EXHAUSTED, so a bailed or killed shard is
# visible as a leftover .tmp and never mistaken for a completed one).
set -u
N=${1:?order n}; LVL=${2:?split level}; NSPLIT=${3:?nsplit}; TAG=${4:?tag}
shift 4
K=${SLURM_ARRAY_TASK_ID:-0}
cd "$(dirname "$0")" || exit 1
mkdir -p logs "doubleend_${TAG}"
OUT="doubleend_${TAG}/split_${K}_of_${NSPLIT}.txt"; TMP="${OUT}.tmp"
[ -f "$OUT" ] && { echo "already complete: $OUT"; exit 0; }
BIN=./double_end_search
[ -x "$BIN" ] || { echo "missing binary" >&2; exit 2; }
{ echo "# host $(hostname) start $(date -u +%FT%TZ)"
  echo "# binary sha256 $(sha256sum $BIN | cut -d' ' -f1)"
  echo "# args: $N --split $LVL $K $NSPLIT $*"; } > "$TMP"
nice -n 15 "$BIN" "$N" --split "$LVL" "$K" "$NSPLIT" --quiet "$@" >> "$TMP" 2>&1
rc=$?
echo "# rc $rc end $(date -u +%FT%TZ)" >> "$TMP"
if [ $rc -eq 0 ] && grep -q "^DOUBLE_END .*status=EXHAUSTED" "$TMP"; then
  mv "$TMP" "$OUT"; echo "complete: $OUT"
else
  echo "NOT complete (rc=$rc)" >&2; exit 3
fi
