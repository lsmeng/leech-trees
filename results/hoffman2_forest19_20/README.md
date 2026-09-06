# Completed forest-engine runs at n = 19 and n = 20

Produced on the UCLA Hoffman2 cluster on 2026-09-05/06 to measure the growth of
the forced-forest search, for the extrapolation quoted in the Discussion.
They are not used by any theorem.

| n | SLURM array | shards (K, L) | raw nodes | unique nodes | survivors | CPU-h |
|---|---|---|---|---|---|---|
| 19 | 214065 | 1680, 8 | 474,060,441,097 | 473,937,189,065 | 0 | 60.7 |
| 20 | 217897 | 1680, 8 | 3,883,156,913,714 | 3,883,033,661,682 | 0 | 510.3 |

Unique counts subtract the (K-1) repeated copies of the 73,408-node prefix of
levels 0..8, exactly as for n = 17 in Table 3.  Growth factors, against the
n = 18 unique total 59,779,854,336: g(19) = 7.928, g(20) = 8.193.

Acceptance, for both n, by `src/verify_forest_run.py <n> <dir> 1680 8`:

    n=19 K=1680 L=8: 1680 DONE records, Snsol=0, Snodes=474060441097, histograms found=1680/1680, prefix_ok=True
    n=20 K=1680 L=8: 1680 DONE records, Snsol=0, Snodes=3883156913714, histograms found=1680/1680, prefix_ok=True

`forest19_20_shards.tar.gz` (MD5 377e316106b89aa7086919bf9c4ad659, SHA-256
prefix 6d986e9de3b3f061) holds the 3,360 per-shard JSONL records.

## Provenance of the engine

The n = 19 and n = 20 runs required `MAXV = 21` in `src/forest_search.cpp`;
the value in the v1.0 deposit was 20, which caps the engine at n <= 19 and
made a first n = 20 attempt (array 214066) exit immediately on every shard.
The constant is a pure array-size cap and the `n > MAXV-1` guard is unchanged
in meaning; the patched build was validated by rerunning n = 17 to the
published total (array 217848: raw 7,890,649,165 = 7,875,306,893 + 209 x 73,408
at K = 210, survivors 0).

* patched source `src/forest_search.cpp`, SHA-256 prefix `966438bffb510690`
* cluster binary `bin/forest_search`, SHA-256 prefix `e8b108ec8f366624`,
  built 2026-09-05T01:14 from that source; it produced the n = 17 control and
  the n = 20 run
* the n = 19 run (array 214065, 2026-09-05 00:56) predates the rebuild and was
  produced by the `MAXV = 20` binary compiled from the otherwise identical
  v1.0 source; that binary was overwritten and its hash was not recorded

Note that the "engine sha256" line printed by `verify_forest_run.py` is the
hash of the source sitting beside the script at verification time, not of the
binary that produced the data.
