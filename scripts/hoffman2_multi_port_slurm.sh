#!/usr/bin/env bash
set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate

H_MAX=${1:-150}
EDGE_MAX=${2:-180}
STAMP=${3:-h${H_MAX}_e${EDGE_MAX}}
OUT="theory-lab/topwindow/results/pro_b27_multi_port_${STAMP}_${SLURM_JOB_ID}.json"

python theory-lab/topwindow/enumerate_pro_b27_multi_port_control.py \
  --h-max "$H_MAX" \
  --edge-max "$EDGE_MAX" \
  --witness-limit 20 > "$OUT"
echo "$OUT"
