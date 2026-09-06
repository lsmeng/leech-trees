# WP-B1 result — forest engine n=19, n=20 growth factors

Checkout: `/u/scratch/l/lsmeng/leech-trees` on Hoffman2 (not a git repo; synced by `src/hoffman2_sync.sh`).
Arrays: 214065 (forest19, 240 SLURM array tasks) and 214066 (forest20, 240 tasks), both COMPLETED
(480/480 tasks report State=COMPLETED via `sacct`). Per task fans out to 7 shards (`--cpus-per-task=7`
in `src/hoffman2_forest_slurm.sh`), so NSHARDS=1680=210×8 for each n — the "8x scale-up from n=18
(K=210)" the brief calls for.

**n=19: clean.** 1680/1680 `forest_order_19_shard*.jsonl` present, all `status:"DONE"`.
`src/verify_forest_run.py` was missing from the Hoffman2 checkout (not part of the last sync); copied
it over (single 2.4 KB file, no compute) and ran it against a symlink dir merging `results/*.jsonl`
with `logs/forest_19_*.err`:
`n=19 K=1680 L=8: 1680 DONE records, Σnsol=0, Σnodes=474060441097, histograms found=1680/1680, prefix_ok=True` / `engine sha256 966438bffb510690`.
Direct jsonl sum agrees: nodes=474,060,441,097, survivors(nsol)=0.

**n=20: FAILED, all 1680 shards empty.** Every `logs/forest_20_*.err` reads `n too large for this
build`; every `results/forest_order_20_shard*.jsonl` is 0 bytes. `verify_forest_run.py 20 ... 1680 8`
raises `AssertionError: ('missing shards', [0, 1, ..., 9])` (all 1680 shards, output token above the
traceback). Root cause: `src/forest_search.cpp` line 106 guards `n > MAXV-1`; the array job (submitted
00:56, done ~01:00) ran a binary built with `MAXV=20` (n≤19 only). At 01:14 — **after** the job had
already finished — the source was patched to `MAXV=21` (comment: "bumped by 1 ... to allow n=20") and
`bin/forest_search` rebuilt, but per instructions no new compute job was submitted, so this fix is
untested and n=20 has zero valid search data. nodes20=0, survivors20=N/A (not a real result).

CPU time (`sacct -j <id> -X -n -o JobID,Elapsed,TotalCPU,AllocCPUS`, summed over 240 tasks each):
`TotalCPU` reports `00:00:00` for every task in both arrays (accounting gap — the shard workers are
backgrounded `&`/`wait` children of the batch step, apparently not captured by this cluster's
sacct/cgroup polling). Used `Elapsed×AllocCPUS` (AllocCPUS=7 constant) instead: n=19 elapsed
Σ=31240s → 60.74 CPU-h; n=20 elapsed Σ=125s → 0.24 CPU-h (consistent with instant failure).

g19 = nodes19/nodes18 = 474060441097 / 59795196608 (exact n=18 total, summed from the 210 local
`results/hoffman2/forest_order_18_shard*.jsonl`, not the brief's 6.0e10 placeholder) = **7.928**.
g20 = 0/474060441097 = 0 — **not a real growth factor**, purely an artifact of the n=20 failure.

SHA-256 of sorted-concatenated shard lines: n=19 `7db368ae819af53ef6d47705b6860720f13d1a79744410bb98ad7ab32dd578f`;
n=20 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85` (= sha256("") since all shards are empty).

Copied both shard sets to laptop `results/hoffman2_forest19_20/` (tar-over-ssh, scp was too slow for
3360 tiny files; n=19 ≈6.6 MB / 1680 files, n=20 0 bytes / 1680 files); sha256 of sorted-concatenated
content matches the Hoffman2 originals exactly for both.

**Recommendation (not executed — no new compute jobs per brief):** rebuild+resubmit n=20 with the
already-patched `MAXV=21` binary now sitting on Hoffman2; everything else for n=19 is solid.

```json
{"status": "blocked", "nodes19": 474060441097, "nodes20": 0, "cpuh19": 60.74, "cpuh20": 0.24, "g19": 7.928, "g20": 0.0, "blocking": "n=20 array (214066) ran with a stale binary (MAXV=20 cap) and produced 0 valid shards ('n too large for this build' in all 1680 logs/forest_20_*.err); source/binary were patched to MAXV=21 post-hoc but not rerun -- g20 and cpuh20 are not meaningful, n=20 needs a resubmit under the fixed binary"}
```
