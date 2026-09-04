#!/bin/bash
# Independent tuple-canonical regeneration of the order-eight catalogue.
# Usage: sbatch scripts/hoffman2_incidence_partition_catalogue_independent_slurm.sh
#SBATCH --job-name=b27inc8ind
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%j.out

set -euo pipefail
ROOT=${SCRATCH:?}/leech-trees
cd "$ROOT"
mkdir -p logs theory-lab/topwindow/results
./env/bin/python theory-lab/topwindow/replay_pro_b27_incidence_partition_catalogue_order8_independent.py \
  --max-order 8 \
  --output theory-lab/topwindow/results/pro_b27_incidence_partition_catalogue_order8_independent.json
