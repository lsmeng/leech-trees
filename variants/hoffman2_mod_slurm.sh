#!/bin/bash
#SBATCH --job-name=modleech
#SBATCH --partition=campus
#SBATCH --time=23:00:00
#SBATCH --cpus-per-task=7
#SBATCH --mem=2G
#SBATCH --output=logs/%x.%A.%a.out
# Modular Leech trees on Hoffman2: sbatch --array=1-NT variants/hoffman2_mod_slurm.sh <n> <NT>
# task t, worker p handles topologies with id % (NT*7) == (t-1)*7+p -> results/mod_{n}_part{i}.out
N=$1; NT=$2; P=${SLURM_CPUS_PER_TASK:-7}; K=$((NT*P))
cd $SCRATCH/leech-trees/variants; mkdir -p logs results
for ((p=0; p<P; p++)); do
  I=$(( (SLURM_ARRAY_TASK_ID-1)*P + p ))
  OUT=results/mod_${N}_part${I}.out
  python3 -c "
import sys,json
for l in open('data/trees_${N}.jsonl'):
    j=json.loads(l)
    if j['id'] % $K == $I: sys.stdout.write(l)" | ./mod_leech $N --print > $OUT 2> logs/mod_${N}_${I}.err &
done
wait
