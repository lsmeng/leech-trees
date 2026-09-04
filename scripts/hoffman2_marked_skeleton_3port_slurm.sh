#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
OUT="theory-lab/topwindow/results/pro_b27_marked_skeleton_3port_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/verify_pro_b27_marked_skeleton_catalogue_3port.py \
  --max-order 10 --output "$OUT"
echo "$OUT"
