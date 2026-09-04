#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
OUT="theory-lab/topwindow/results/pro_b27_two_port_skeleton_cpsat_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/enumerate_pro_b27_two_port_skeleton_cpsat.py \
  --max-order 4 --time-limit 30 > "$OUT"
echo "$OUT"
