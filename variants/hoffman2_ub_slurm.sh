#!/bin/bash
#SBATCH --job-name=mddub
#SBATCH --partition=campus
#SBATCH --time=23:00:00
#SBATCH --cpus-per-task=7
#SBATCH --mem=2G
#SBATCH --output=logs/%x.%A.out
# upper-bound hunt: sbatch variants/hoffman2_ub_slurm.sh <n> <D1> <D2> ... (<=7 values): edge-first DFS, stop at first witness
N=$1; shift; cd $SCRATCH/leech-trees/variants; mkdir -p logs results
for D in "$@"; do ./mdd_forest $N $D --edge-first --maxsol 1 > results/mddub_${N}_${D}.out 2> logs/mddub_${N}_${D}.err & done
wait
