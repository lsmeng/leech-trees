# WP-A3 result

Status: submitted (wave 2 of depth phase for delta=285, m=15, r=9). Not waited on.

## Confirmed inputs (via `sacct -j 118376 --format=JobID,SubmitLine -X` on Hoffman2, not guessed)
- Prior run's exact submit line: `sbatch --array=0-255 hoffman2_s1_depth_v7_array_slurm.sh 15 shapes_r9_exists.txt 5 256 r9`
- shapes file: `$SCRATCH/leech-trees/theory-lab/s1_crowding/shapes_r9_exists.txt` (95 lines, sha256 `8c2e6a724d5ac504e93f3f3b7e3060e019df0f1778e6e95c4aeeeac01f09d0bc`)
- LVL (split level): `5`
- NSPLIT: `256`, m: `15`
- engine: `abstract_class_search7`, sha256 `29fe1fd705feaf31c21d478c02ab16a064dec3223281ed3482323c87f6c0dfe7` (unchanged from 2026-09-02 run; abstract_class_search_moment not used anywhere)

## Step 1 — harvest (login node, `depthv7_r9_partial_20260902/`, 824K, ran directly)
`python3 harvest_partial_splits.py depthv7_r9_partial_20260902 256 --m 15 --shapes shapes_r9_exists.txt --resid-dir residual_wave2 --out harvest_wave2.json`
- shapes_total=95, missing_split_shape_pairs=**21124** (matches the brief's prior figure exactly), done=3196, survivors=0, shapes_complete_across_all_splits=0
- residual_wave2/: 256 files named `shapes_split_<K>.txt`, all non-empty, total lines = 21124 (checksum against harvest total OK)

## Step 2 — resid script
Wrote `theory-lab/s1_crowding/hoffman2_s1_depth_v7_resid_slurm.sh` (same as `hoffman2_s1_depth_v7_array_slurm.sh`: partition campus, qos campus24, 23:50:00, --nice=10000, 1 cpu, 2G). Only changes: per-split `SHAPES=residual_wave2/shapes_split_${K}.txt` (actual harvest-script output name, not the guessed `split_${K}...`), skip via `[[ ! -s "$SHAPES" ]] && exit 0`, output dir tag `r9_wave2`. Copied to Hoffman2 at `$SCRATCH/leech-trees/theory-lab/s1_crowding/`, sha256 `c33d5436fe8a26d30b77231eec7be356ef426bf7d96496ca83c60a12f653d05d`.

## Step 3 — submitted
`squeue -u $USER` was 0 jobs before submit (0+256=256<500, OK). Job 217897 (other run) untouched — not visible in this user's queue, left alone.
`sbatch --array=0-255 hoffman2_s1_depth_v7_resid_slurm.sh 15 5 256 r9_wave2` → **job 218157**, submitted 2026-09-05 22:48 PDT, PENDING at submit time. Output: `depthv7_r9_wave2/split_<K>_of_256.txt`, logs `logs/s1dv7.218157.<K>.out`.

## Next wave (copy verbatim once job 218157's splits are done/cancelled)
```
cd $SCRATCH/leech-trees/theory-lab/s1_crowding
python3 harvest_partial_splits.py depthv7_r9_wave2 256 --m 15 --shapes shapes_r9_exists.txt --resid-dir residual_wave3 --out harvest_wave3.json
```
Repeat steps 2-3 (bump tag to `r9_wave3`, resid dir to `residual_wave3`) until missing_split_shape_pairs=0, then run `verify_depth_splits.py` for the VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY certificate.
