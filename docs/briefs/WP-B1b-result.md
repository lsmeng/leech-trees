# WP-B1b result — n=20 rebuild validation + relaunch

**(1) Diff/build check.** `diff` of Hoffman2 `src/forest_search.cpp` vs laptop copy: **empty**
(both `MAXV=21`, line 106 guard `n > MAXV-1`). `bin/forest_search` mtime (epoch 1788596052) is
7s newer than `src/forest_search.cpp` (1788596045) — binary already reflects the patched source;
no rebuild performed.

**(2) Positive control, n=17.** Job **217848** (30 tasks x 7 cpus, K=210, `campus`/`campus24`,
23:50 wall) — 30/30 COMPLETED, 0 failed. `verify_forest_run.py 17 <merged results+logs> 210 8`:
1680->210 DONE records, Sigma nsol=0, Sigma nodes=7,890,649,165 (raw shard sum), prefix_ok=True,
level 9-12 histograms match the independent oracle exactly, engine sha256 `966438bffb510690`.

Raw shard sums over-count the shared top-8-level trunk (size Sigma(PREFIX[0..8])=73,408 nodes,
replayed once per shard). Correcting `raw - (K-1)*73408`: K=210 gives 7,890,649,165 -
209*73408 = **7,875,306,893**; a pre-existing local K=32 run of the same n=17
(`results/forest_order_17.jsonl`, raw 7,877,582,541) gives the identical 7,875,306,893 after the
same correction. **Control matches exactly** -> control_ok = true.

**(3) n=20 relaunch.** Job **217897** submitted 2026-09-06T04:29:05Z, same layout as n=19:
240 tasks x 7 cpus, NSHARDS=1680, `campus`/`campus24`, 23:50 wall,
`sbatch ... --array=1-240 src/hoffman2_forest_slurm.sh 20 240 8`.

**(4) n=20 outcome (within 2h budget).** All 240/240 tasks COMPLETED by 05:49:23Z (~80 min
elapsed), 0 failed. `verify_forest_run.py 20 <merged> 1680 8`: 1680/1680 DONE, Sigma nsol=0
(0 survivors), Sigma nodes=3,883,156,913,714 raw (-> 3,883,033,661,682 trunk-corrected), prefix_ok=True,
engine sha256 `966438bffb510690` (same binary as control). CPU-h (Elapsed x AllocCPUS) = 510.31.
No queue conflicts introduced; no other jobs touched.

```json
{"status": "completed", "control_nodes17": 7875306893, "control_ok": true, "job20": 217897, "blocking": null}
```
