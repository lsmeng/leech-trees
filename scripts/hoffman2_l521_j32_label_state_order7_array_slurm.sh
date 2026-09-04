#!/usr/bin/env bash
#SBATCH --job-name=b27state7a
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=00:30:00
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
OUT="theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order7_shard${TASK}_${SLURM_ARRAY_JOB_ID}.json"
python theory-lab/topwindow/enumerate_pro_b27_l521_j32_label_state_cpsat.py \
  --min-order 7 --max-order 7 --skeleton-index "$TASK" --time-limit 0.20 > "$OUT"
echo "$OUT"
