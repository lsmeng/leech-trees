#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate

POOL=(43 44 45 46 47 48 49 51 52 53)
STAMP=${1:-pool10}
OUT="theory-lab/topwindow/results/pro_b27_shared_multiport_${STAMP}_${SLURM_JOB_ID}.json"

python theory-lab/topwindow/enumerate_pro_b27_shared_multiport_control.py \
  --pool "${POOL[@]}" \
  --witness-limit 20 > "$OUT"
echo "$OUT"
