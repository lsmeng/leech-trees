#!/usr/bin/env bash
#SBATCH --job-name=b27unk7a
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --array=0-47%8
#SBATCH --output=logs/%x.%A_%a.out

set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
mkdir -p logs results
TASK=${SLURM_ARRAY_TASK_ID}
INPUT=$(find theory-lab/topwindow/results -maxdepth 1 \
  -name "pro_b27_l521_j32_label_state_order7_shard${TASK}_*.json" -size +1c \
  | sort | tail -n 1)
if [[ -z "$INPUT" ]]; then
  echo "missing non-empty input shard ${TASK}" >&2
  exit 2
fi
OUT="theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order7_unknown_rerun5_shard${TASK}_${SLURM_ARRAY_JOB_ID}.json"
python theory-lab/topwindow/rerun_pro_b27_l521_j32_label_state_unknown.py \
  "$INPUT" "$OUT" --time-limit 5.0 > "$OUT.log"
cat "$OUT.log"
