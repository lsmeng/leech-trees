#!/bin/bash
#SBATCH --job-name=mdd
#SBATCH --partition=campus
#SBATCH --time=23:00:00
#SBATCH --cpus-per-task=7
#SBATCH --mem=2G
#SBATCH --output=logs/%x.%A.%a.out
# Minimal distinct distance trees on Hoffman2: sbatch --array=1-NT variants/hoffman2_mdd_slurm.sh <n> <D> <NT> [shard-level L]
# task t runs shards (t-1)*7 .. t*7-1 of K = NT*7 -> results/mdd_{n}_{D}_shard{i}.jsonl
N=$1; D=$2; NT=$3; L=${4:-7}; P=${SLURM_CPUS_PER_TASK:-7}; K=$((NT*P))
cd $SCRATCH/leech-trees/variants; mkdir -p logs results
for ((p=0; p<P; p++)); do
  I=$(( (SLURM_ARRAY_TASK_ID-1)*P + p ))
  OUT=results/mdd_${N}_${D}_shard${I}.jsonl
  if grep -q '"status": "DONE"' $OUT 2>/dev/null; then continue; fi
  ./mdd_forest $N $D --shard $I $K --shard-level $L > $OUT 2> logs/mdd_${N}_${D}_${I}.err &
done
wait
