#!/bin/bash
# Depth-dependent phase, residual wave: same engine/flags as
# hoffman2_s1_depth_v7_array_slurm.sh, but each split K reads its own
# residual shapes file (produced by harvest_partial_splits.py) instead of
# the full shapes file, and skips cleanly if that split has nothing left.
# Usage: sbatch --array=0-$((NSPLIT-1)) hoffman2_s1_depth_v7_resid_slurm.sh <m> <split_level> <NSPLIT> <tag>
#SBATCH --job-name=s1dv7
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%A.%a.out
set -euo pipefail
M=$1; LVL=$2; NSPLIT=$3; TAG=$4
ROOT=${SCRATCH:?}/leech-trees/theory-lab/s1_crowding
cd "$ROOT"
mkdir -p logs depthv7_${TAG}
K=${SLURM_ARRAY_TASK_ID}
SHAPES=residual_wave2/shapes_split_${K}.txt
if [[ ! -s "$SHAPES" ]]; then
  exit 0
fi
./abstract_class_search7 --m $M --shapes-file $SHAPES --solve-depths --max-witness 50 --split $LVL $K $NSPLIT \
  > depthv7_${TAG}/split_${K}_of_${NSPLIT}.txt.tmp 2>&1 && mv depthv7_${TAG}/split_${K}_of_${NSPLIT}.txt.tmp depthv7_${TAG}/split_${K}_of_${NSPLIT}.txt
