#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
OUT="theory-lab/topwindow/results/pro_b27_j32_outward_deeper_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/enumerate_pro_b27_j32_outward_deeper.py \
  --max-order 1 --time-limit 0.20 > "$OUT"
echo "$OUT"
