# Hop-diameter at most four

This directory contains the recovered, audited diameter-restricted forced-
forest engine and an independent Python implementation.

## Files

| file | purpose |
|---|---|
| `forest_search_d4.cpp` | exact shared-forest C++ search for hop-diameter at most four |
| `d4_cleanroom.py` | independent Python forced-forest search with separate state and pruning code |
| `verify_diameter4.py` | rebuilds the C++ engine, reproduces orders 2--18, runs the clean room through 13, verifies every positive witness twice, runs planted controls and the endgame ablation |
| `test_planted.py` | deterministic arbitrary-target positive controls |
| `verify_structure.py` | checks the top-window structural identities on the known trees and 300 random distinct-distance diameter-four trees |
| `run_diameter4_shards.py` | resumable parallel shard runner; writes a result only after a `DONE` process |
| `verify_diameter4_shards.py` | refuses missing/unfinished/wrong-key shards, sends every witness through both repository checkers, and freezes source/checker/executable plus complete-stdout digests |
| `results/diameter4_ladder_certificate.json` | frozen order-2--18 ladder and trust boundary |
| `results/diameter4_n25_shards_certificate.json` | frozen order-25 aggregate; the adjacent `n25_k512/` archive contains all 512 stdout/stderr pairs and the exact campaign executable |

## Reproduction

```text
nice -n 10 python3 theory-lab/diameter4/verify_diameter4.py \
  --max-order 18 --cleanroom-max 13 --jobs 3
```

The C++ ladder has 38,221,445 states in total and solution counts

```text
1,1,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0
```

for orders 2 through 18.  The five positive outputs are precisely the known
trees and pass both `src/checker_a.py` and `src/checker_b.py`.  The independent
Python engine has different node counts but the same solution counts through
order 13.  The strongest endgame feasibility prune can be disabled at compile
time with `-DD4_NO_ENDGAME`; order 17 then grows from 7,767,003 to 47,986,068
states and still has zero solutions.

**OBSERVED:** the five known trees are the only hop-diameter-at-most-four Leech
trees through order 18.  Together with Taylor's **LITERATURE** order condition,
and the completed **OBSERVED** order-25 sweep, this covers orders through 25.
All 512 order-25 shards are `DONE`; their aggregate has zero solutions over
322,189,234,739 reported nodes (including repeated pre-shard prefixes) and
3,403,240.387 reported CPU-seconds.

For a campaign certificate, pass the exact executable used by the runner:

```text
python3 theory-lab/diameter4/verify_diameter4_shards.py 25 \
  theory-lab/diameter4/results/n25_k512 \
  --shards 512 --shard-level 8 \
  --engine theory-lab/diameter4/results/n25_k512/campaign_engine_linux_x86_64 \
  --expected theory-lab/diameter4/results/diameter4_n25_shards_certificate.json
```

The aggregate records the audited C++ source and both checker hashes, the
campaign executable hash, a digest of every complete shard stdout, and the
reported CPU/node totals.  These provenance fields supplement rather than
replace the mathematical/source audit.
