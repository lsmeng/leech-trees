#!/usr/bin/env bash
#SBATCH --job-name=b27portrt
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
OUT="theory-lab/topwindow/results/pro_b27_low_component_port_skeleton_roundtrip_${SLURM_JOB_ID}.json"
python theory-lab/topwindow/verify_pro_b27_low_component_port_skeleton_roundtrip.py \
  --max-order 10 --output "$OUT"
echo "$OUT"
