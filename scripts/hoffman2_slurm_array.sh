#!/bin/bash
#SBATCH --job-name=leech
#SBATCH --partition=campus
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --output=logs/%x.%A.%a.out
# Usage: sbatch --array=1-NSHARDS scripts/hoffman2_slurm_array.sh <n> <nshards> <time_per_topology> [ids-file] [extra flags]
# Hoffman2 moved from SGE to SLURM (2026); campus partition: 24h max, ~3.9k CPUs.
N=$1; NSHARDS=$2; TL=$3; IDS=${4:-}; EXTRA=${5:-}
cd $SCRATCH/leech-trees; mkdir -p logs results
IDSARG=""; [ -n "$IDS" ] && IDSARG="--ids $IDS"
./env/bin/python src/run_cpp_shard.py $N $SLURM_ARRAY_TASK_ID $NSHARDS --time $TL $IDSARG --extra "$EXTRA"
