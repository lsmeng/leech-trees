#!/usr/bin/env bash
#SBATCH --job-name=b27unk6
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%j.out

set -euo pipefail

ROOT=/u/scratch/l/lsmeng/leech-trees
cd "$ROOT"
source env/bin/activate
mkdir -p logs results
INPUT=theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order6_98820.json
OUT="theory-lab/topwindow/results/pro_b27_l521_j32_label_state_order6_unknown_rerun_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/rerun_pro_b27_l521_j32_label_state_unknown.py \
  "$INPUT" "$OUT" --time-limit 1.0 > "$OUT.log"
cat "$OUT.log"
