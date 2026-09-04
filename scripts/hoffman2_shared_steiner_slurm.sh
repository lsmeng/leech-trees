#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate

MAX_EDGES=${1:-1}
H_MAX=${2:-120}
STEINER_MIN=${3:-38}
STAMP=${4:-e${MAX_EDGES}_h${H_MAX}_s${STEINER_MIN}}
OUT="theory-lab/topwindow/results/pro_b27_shared_steiner_${STAMP}_${SLURM_JOB_ID}.json"

python theory-lab/topwindow/enumerate_pro_b27_shared_steiner.py \
  --max-edges "$MAX_EDGES" \
  --h-max "$H_MAX" \
  --steiner-min "$STEINER_MIN" \
  --witness-limit 20 > "$OUT"
echo "$OUT"
