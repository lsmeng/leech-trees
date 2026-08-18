#!/bin/bash
#SBATCH --job-name=forest18
#SBATCH --partition=campus
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=7
#SBATCH --mem=4G
#SBATCH --output=logs/%x.%A.%a.out
# Forest engine on Hoffman2 (SLURM): sbatch --array=1-NTASKS scripts/hoffman2_forest_slurm.sh <n> <NTASKS> [shard-level]
# Task t runs shards (t-1)*P .. t*P-1 of NSHARDS=NTASKS*P -> results/forest_order_{n}_shard{i}.jsonl (+ SOL lines inside)
N=$1; NTASKS=$2; L=${3:-8}; P=${SLURM_CPUS_PER_TASK:-7}; NSHARDS=$((NTASKS*P))
cd $SCRATCH/leech-trees; mkdir -p logs results
for ((p=0; p<P; p++)); do
  I=$(( (SLURM_ARRAY_TASK_ID-1)*P + p ))
  ./bin/forest_search $N --shard $I $NSHARDS --shard-level $L > results/forest_order_${N}_shard${I}.jsonl 2> logs/forest_${N}_${I}.err &
done
wait
