#!/bin/bash
#SBATCH --job-name=b27port
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%j.out
#
# Run the port-first J32 profile scan on Hoffman2, not on the workstation.
# Usage from the project checkout:
#   sbatch scripts/hoffman2_port_profile_slurm.sh [max_edges] [h_max]
# The scan is an OBSERVED pressure test; it is not a proof by itself.

set -euo pipefail
MAX_EDGES=${1:-3}
H_MAX=${2:-220}
ROOT=${SCRATCH:-$HOME/scratch}/leech-trees
cd "$ROOT"
mkdir -p logs results
./env/bin/python theory-lab/topwindow/scan_pro_b27_j32_port_profiles.py \
  --max-edges "$MAX_EDGES" --h-max "$H_MAX" --carrier J --profile-limit 1000 \
  > "results/pro_b27_j32_port_profiles_e${MAX_EDGES}_h${H_MAX}_${SLURM_JOB_ID}.json"
