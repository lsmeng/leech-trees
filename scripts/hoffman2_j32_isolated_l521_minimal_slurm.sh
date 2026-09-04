#!/usr/bin/env bash
#SBATCH --job-name=b27iso
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=08:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%j.out

# Bounded Pro-guided control search; this is not a global proof.
set -euo pipefail
MAX_STEM=${1:-80}
MAX_H=${2:-120}
ROOT=${SCRATCH:-$HOME/scratch}/leech-trees
cd "$ROOT"
mkdir -p logs results
OUT="results/pro_b27_j32_isolated_l521_minimal_stem${MAX_STEM}_h${MAX_H}_${SLURM_JOB_ID}.json"
./env/bin/python theory-lab/topwindow/run_pro_b27_j32_isolated_l521_minimal.py \
  --max-stem "$MAX_STEM" --max-h "$MAX_H" --output "$OUT"
