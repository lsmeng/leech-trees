#!/bin/bash
#$ -cwd
#$ -o logs/$JOB_NAME.$JOB_ID.$TASK_ID.out
#$ -j y
#$ -l h_rt=24:00:00,h_data=1G
#$ -pe shared 1
# Usage: qsub -N leech18 -t 1-NSHARDS scripts/hoffman2_cpp_array.sh <n> <nshards> <time_per_topology> [ids-file] [extra flags]
N=$1; NSHARDS=$2; TL=$3; IDS=${4:-}; EXTRA=${5:-}
cd $SCRATCH/leech-trees; mkdir -p logs results
IDSARG=""; [ -n "$IDS" ] && IDSARG="--ids $IDS"
./env/bin/python src/run_cpp_shard.py $N $SGE_TASK_ID $NSHARDS --time $TL $IDSARG --extra "$EXTRA"
