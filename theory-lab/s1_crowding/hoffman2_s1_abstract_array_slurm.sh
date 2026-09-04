#!/bin/bash
# Depth-free class search (abstract_class_search) for the singleton final cap,
# sharded over rooted low-tree isomorphism classes.
# Usage: sbatch --array=0-$((NSHARDS-1)) hoffman2_s1_abstract_array_slurm.sh <r> <NSHARDS> [extra args]
#SBATCH --job-name=s1abs
#SBATCH --partition=campus
#SBATCH --qos=campus24
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --nice=10000
#SBATCH --output=logs/%x.%A.%a.out
set -euo pipefail
R=$1; NSH=$2; shift 2
ROOT=${SCRATCH:?}/leech-trees/theory-lab/s1_crowding
cd "$ROOT"
mkdir -p logs abstract_r${R}
M=$((24-R))
K=${SLURM_ARRAY_TASK_ID}
./abstract_class_search --m $M --r $R --all-shapes --stop-first --shard $K $NSH --nodes-limit 100000000000 "$@" \
  > abstract_r${R}/shard_${K}_of_${NSH}.txt.tmp 2>&1 && mv abstract_r${R}/shard_${K}_of_${NSH}.txt.tmp abstract_r${R}/shard_${K}_of_${NSH}.txt
