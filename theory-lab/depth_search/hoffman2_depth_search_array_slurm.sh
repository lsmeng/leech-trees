#!/bin/bash
# depth_search pilot array.  One SLURM task per line of pilot_configs.txt.
# Usage: sbatch --array=0-21 hoffman2_depth_search_array_slurm.sh
#SBATCH --job-name=depthpilot
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%A.%a.out
set -euo pipefail
ROOT=${SCRATCH:?}/leech-trees/theory-lab/depth_search
cd "$ROOT"
mkdir -p logs out
K=${SLURM_ARRAY_TASK_ID}
LINE=$(sed -n "$((K+1))p" pilot_configs.txt)
TAG=$(echo "$LINE" | awk '{print $1}')
ARGS=$(echo "$LINE" | cut -d' ' -f2-)
echo "TASK $K TAG $TAG ARGS $ARGS"
/usr/bin/time -v ./depth_search $ARGS > out/${TAG}.txt.tmp 2> out/${TAG}.time || true
mv out/${TAG}.txt.tmp out/${TAG}.txt
echo DONE $TAG
