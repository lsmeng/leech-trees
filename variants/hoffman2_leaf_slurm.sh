#!/bin/bash
#SBATCH --job-name=leaf
#SBATCH --partition=campus
#SBATCH --time=23:00:00
#SBATCH --cpus-per-task=7
#SBATCH --mem=8G
#SBATCH --output=logs/%x.%A.%a.out
# leaf-Leech CP-SAT on Hoffman2: sbatch --array=1-NT variants/hoffman2_leaf_slurm.sh <L> <NT> [time]
L=$1; NT=$2; T=${3:-7200}; P=${SLURM_CPUS_PER_TASK:-7}; K=$((NT*P))
cd $SCRATCH/leech-trees/variants; mkdir -p logs results
for ((p=0; p<P; p++)); do
  I=$(( (SLURM_ARRAY_TASK_ID-1)*P + p ))
  ../env/bin/python leaf_leech_cpsat.py $L --all --time $T --topos data/leaf_topos_${L}.jsonl --part $I/$K > logs/leaf_${L}_${I}.log 2>&1 &
done
wait
