#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
OUT="theory-lab/topwindow/results/pro_b27_pure_high_chain_cpsat_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/enumerate_pro_b27_pure_high_chain_cpsat.py \
  --time-limit 120 > "$OUT"
echo "$OUT"
