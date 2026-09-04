#!/bin/bash
# First-pass rooted attachment/LCA expansion through order five.
# UNKNOWN rows must be rerun and independently audited before any promotion.
#SBATCH --job-name=b27att5
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=6G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%j.out

set -euo pipefail
ROOT=${SCRATCH:?}/leech-trees
cd "$ROOT"
mkdir -p logs theory-lab/topwindow/results
./env/bin/python theory-lab/topwindow/enumerate_pro_b27_attachment_lca_falsification.py \
  --max-order 5 --time-limit 0.20 \
  > "theory-lab/topwindow/results/pro_b27_attachment_lca_falsification_order5_${SLURM_JOB_ID}.json"
