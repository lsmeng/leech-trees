#!/bin/bash
# Depth-dependent phase: enumerate all depth-free structures of the labeled
# low shapes listed in a shapes file and run the (s,L) CSP on each.
# Usage: sbatch --array=0-$((NSPLIT-1)) hoffman2_s1_depth_array_slurm.sh <m> <shapesfile> <split_level> <NSPLIT> <tag>
#SBATCH --job-name=s1dv7
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%A.%a.out
set -euo pipefail
M=$1; SHAPES=$2; LVL=$3; NSPLIT=$4; TAG=$5
ROOT=${SCRATCH:?}/leech-trees/theory-lab/s1_crowding
cd "$ROOT"
mkdir -p logs depthv7_${TAG}
K=${SLURM_ARRAY_TASK_ID}
./abstract_class_search7 --m $M --shapes-file $SHAPES --solve-depths --max-witness 50 --split $LVL $K $NSPLIT \
  > depthv7_${TAG}/split_${K}_of_${NSPLIT}.txt.tmp 2>&1 && mv depthv7_${TAG}/split_${K}_of_${NSPLIT}.txt.tmp depthv7_${TAG}/split_${K}_of_${NSPLIT}.txt
