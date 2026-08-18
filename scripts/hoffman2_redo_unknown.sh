#!/bin/bash
#SBATCH --job-name=redo
#SBATCH --partition=campus
#SBATCH --time=23:50:00
#SBATCH --cpus-per-task=7
#SBATCH --mem=4G
#SBATCH --output=logs/%x.%A.%a.out
# Rerun UNKNOWN topologies with the v2 engine and a larger cap.
# sbatch --array=1-NTASKS scripts/hoffman2_redo_unknown.sh <n> <NTASKS> <cap_seconds> [ids-file]
N=$1; NTASKS=$2; TL=$3; IDS=${4:-}; P=${SLURM_CPUS_PER_TASK:-7}; NSHARDS=$((NTASKS*P))
cd $SCRATCH/leech-trees; mkdir -p logs results/redo
IDSARG=""; [ -n "$IDS" ] && IDSARG="--ids $IDS"
for ((p=1; p<=P; p++)); do
  SHARD=$(( (SLURM_ARRAY_TASK_ID-1)*P + p ))
  ./env/bin/python src/run_cpp_shard.py $N $SHARD $NSHARDS --time $TL $IDSARG --bin bin/leech_search_v2 --redo-unknown \
     --merge-from "results/cpp_order_${N}_shard*.jsonl" --out-prefix results/redo/cpp_redo --extra "--wcover 50 --look" > logs/redo_${N}_${SHARD}.log 2>&1 &
done
wait
