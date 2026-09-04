#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
OUT="theory-lab/topwindow/results/pro_b27_ordered_arc_spectrum_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/verify_pro_b27_ordered_arc_spectrum.py --max-order 5 > "$OUT"
echo "$OUT"
