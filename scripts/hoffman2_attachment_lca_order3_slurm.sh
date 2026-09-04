#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
OUT="theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order3_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/enumerate_pro_b27_attachment_lca_falsification.py \
  --max-order 3 --time-limit 0.20 > "$OUT"
echo "$OUT"
