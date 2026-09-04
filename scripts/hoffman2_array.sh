#!/bin/bash
#$ -cwd
#$ -o logs/$JOB_NAME.$JOB_ID.$TASK_ID.out
#$ -j y
#$ -l h_rt=23:00:00,h_data=2G
#$ -pe shared 1
#$ -t 1-100
# Usage: qsub -N leech18 scripts/hoffman2_array.sh <n> <engine: cpsat|cpp> <nshards>
# Each task processes shard $SGE_TASK_ID of NSHARDS over data/trees_$n.jsonl, resumable.
N=${1:-18}; ENGINE=${2:-cpp}; NSHARDS=${3:-100}
cd $SCRATCH/leech-trees; mkdir -p logs results
if [ "$ENGINE" = "cpsat" ]; then
  ./env/bin/python src/run_shard_cpsat.py $N $SGE_TASK_ID $NSHARDS
else
  ./env/bin/python src/run_cpp.py $N --shard $SGE_TASK_ID --nshards $NSHARDS
fi
