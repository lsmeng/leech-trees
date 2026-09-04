#!/bin/bash
#SBATCH --job-name=leech
#SBATCH --partition=campus
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=7
#SBATCH --mem=4G
#SBATCH --output=logs/%x.%A.%a.out
# Usage: sbatch --array=1-NTASKS scripts/hoffman2_slurm_array.sh <n> <NTASKS> <time_per_topology> [ids-file] [extra flags]
# Hoffman2 = SLURM (2026). QOS campus24: MaxJobsPU=100, MaxSubmitPU=500, cpu=768 -> use 7 procs per array task.
N=$1; NTASKS=$2; TL=$3; IDS=${4:-}; EXTRA=${5:-}
P=${SLURM_CPUS_PER_TASK:-7}
NSHARDS=$((NTASKS * P))
cd $SCRATCH/leech-trees; mkdir -p logs results
IDSARG=""; [ -n "$IDS" ] && IDSARG="--ids $IDS"
for ((p=1; p<=P; p++)); do
  SHARD=$(( (SLURM_ARRAY_TASK_ID-1)*P + p ))
  ./env/bin/python src/run_cpp_shard.py $N $SHARD $NSHARDS --time $TL $IDSARG --extra "$EXTRA" > logs/shard_${N}_${SHARD}.log 2>&1 &
done
wait
