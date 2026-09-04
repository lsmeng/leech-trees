#!/bin/bash
#$ -cwd
#$ -o logs/$JOB_NAME.$JOB_ID.$TASK_ID.out
#$ -j y
#$ -l h_rt=24:00:00,h_data=1G
#$ -pe shared 1
# Forest engine on the cluster: qsub -N forest18 -t 1-NSHARDS scripts/hoffman2_forest_array.sh <n> <nshards> [shard-level]
# Task i runs shard i-1 of NSHARDS (all level-L subtrees with index % NSHARDS == i-1) -> results/forest_order_{n}_shard{i}.jsonl
# Sum nsol over shards = number of Leech trees of order n (0 => none).  Build first: scripts/build.sh (bin/forest_search).
N=$1; NSHARDS=$2; L=${3:-8}
cd $SCRATCH/leech-trees; mkdir -p logs results
I=$((SGE_TASK_ID-1))
./bin/forest_search $N --shard $I $NSHARDS --shard-level $L > results/forest_order_${N}_shard${SGE_TASK_ID}.jsonl 2> logs/forest_${N}_${SGE_TASK_ID}.err
