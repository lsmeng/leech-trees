#!/usr/bin/env bash
#SBATCH --job-name=b27state6
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%j.out

set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
mkdir -p logs results
OUT="theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order6_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/enumerate_pro_b27_l521_j32_label_state_cpsat.py \
  --max-order 6 --time-limit 0.20 > "$OUT"
echo "$OUT"
