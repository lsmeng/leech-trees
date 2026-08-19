#!/bin/bash
#SBATCH --job-name=topo
#SBATCH --partition=campus
#SBATCH --time=23:00:00
#SBATCH --cpus-per-task=7
#SBATCH --mem=2G
#SBATCH --output=logs/%x.%A.%a.out
# Per-topology engines on Hoffman2: sbatch --array=1-NT variants/hoffman2_topo_slurm.sh <tag> <n> <NT> <cmd...>
# e.g. ... mdd11_59 11 4 ./mdd_topo 11 59 --print   or   ... mod11 11 4 ./mod_leech 11 --print
# task t, worker p handles topologies with id % (NT*7) == (t-1)*7+p -> results/<tag>_part{i}.out
TAG=$1; N=$2; NT=$3; shift 3; P=${SLURM_CPUS_PER_TASK:-7}; K=$((NT*P))
cd $SCRATCH/leech-trees/variants; mkdir -p logs results
for ((p=0; p<P; p++)); do
  I=$(( (SLURM_ARRAY_TASK_ID-1)*P + p ))
  OUT=results/${TAG}_part${I}.out
  python3 -c "
import sys,json
for l in open('data/trees_${N}.jsonl'):
    j=json.loads(l)
    if j['id'] % $K == $I: sys.stdout.write(l)" | "$@" > $OUT 2> logs/${TAG}_${I}.err &
done
wait
