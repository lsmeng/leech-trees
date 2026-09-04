#!/bin/bash
# Bounded topology-only incidence/partition catalogue on Hoffman2.
# Usage: sbatch scripts/hoffman2_incidence_partition_catalogue_slurm.sh
#SBATCH --job-name=b27inc8
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%j.out

set -euo pipefail

ROOT=${SCRATCH:?}/leech-trees
cd "$ROOT"
mkdir -p logs theory-lab/topwindow/results
./env/bin/python theory-lab/topwindow/verify_pro_b27_incidence_partition_catalogue.py \
  --max-order 8 \
  --output theory-lab/topwindow/results/pro_b27_incidence_partition_catalogue_order8.json
