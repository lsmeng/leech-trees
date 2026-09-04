#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate

POOL=(43 44 45 46 47 48 49 51 52 53 56 58)
STAMP=${1:-pool12}
OUT="theory-lab/topwindow/results/pro_b27_pure_high_chain_${STAMP}_${SLURM_JOB_ID}.json"

python theory-lab/topwindow/enumerate_pro_b27_pure_high_chain_control.py \
  --pool "${POOL[@]}" \
  --witness-limit 20 > "$OUT"
echo "$OUT"
