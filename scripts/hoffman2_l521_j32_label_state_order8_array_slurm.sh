#!/usr/bin/env bash
# Order-eight extension of the forced L(5,21)/J(32) label-state control.
# One task owns one of the 115 rooted order-eight skeletons.
#SBATCH --job-name=b27state8a
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --array=0-114%8
#SBATCH --output=logs/%x.%A_%a.out

set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
mkdir -p logs results
TASK=${SLURM_ARRAY_TASK_ID}
OUT="theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order8_shard${TASK}_${SLURM_ARRAY_JOB_ID}.json"
python theory-lab/topwindow/enumerate_pro_b27_l521_j32_label_state_cpsat.py \
  --min-order 8 --max-order 8 --skeleton-index "$TASK" --time-limit 0.20 > "$OUT"
echo "$OUT"
