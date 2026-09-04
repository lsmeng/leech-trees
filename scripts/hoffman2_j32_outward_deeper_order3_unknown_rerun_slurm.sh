#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
INPUT=theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order3_99744.json
OUT="theory-lab/topwindow/results/pro_b27_j32_outward_deeper_order3_unknown_rerun_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/rerun_pro_b27_j32_outward_deeper_unknown.py \
  "$INPUT" "$OUT" --time-limit 5.0 > "$OUT.log"
cat "$OUT.log"
