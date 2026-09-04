#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate

H_MAX=${1:-150}
STAMP=${2:-h${H_MAX}}
OUT="theory-lab/topwindow/results/pro_b27_ordered_arc_${STAMP}_${SLURM_JOB_ID}.json"

python theory-lab/topwindow/enumerate_pro_b27_ordered_arc_control.py \
  --h-max "$H_MAX" \
  --witness-limit 20 > "$OUT"
echo "$OUT"
