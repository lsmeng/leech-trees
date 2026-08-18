# Clean-room re-implementation of the forest search (`cleanroom/cr_forest.c`)

Date 2026-08-18. Purpose: item 4 of the certificate scheme in `docs/referee-forest.md` §8 — a *second,
independent* implementation of the forced-forest DFS written only from the algorithm description
(referee-forest.md §1–5, Calhoun 2007 Lemma 2.6 / Alg. 2.7, literature ledger L4), reproducing the
per-level node counts (a mathematical invariant: number of abstract forced forests per level).
`src/forest_search.cpp`, `src/leech_search.cpp` and `bin/` were **not read**. `cargo` is not installed
on this Mac, so the implementation is C (clang -O3), single file, no dependencies.

## Files
| file | what |
|---|---|
| `cleanroom/cr_forest.c` | the engine. `cr_forest n [--shard i K --level L] [--maxlevel M] [--no-sumrule]`; prints `SOL:` lines + one JSON record with the per-level histogram |
| `cleanroom/oracle_brute.py` | independent Python oracle: ALL labeled children, validity by BFS recomputation of the full distance multiset, dedup per level by the canonical form "sorted multiset of per-vertex sorted incident-weight tuples" |
| `cleanroom/check_solutions.py` | runs the engine, feeds every witness to `src/checker_a.py` and `src/checker_b.py` |
| `cleanroom/check_sharding.py` | shard partition identities for 11 (n,K,L) cases |
| `cleanroom/run_shards.sh` | `run_shards.sh n K L W`: W workers at nice 15, resumable, JSON lines to `results/cleanroom_forest_{n}_shard{w}.jsonl` |
| `cleanroom/verify_18.py` | aggregates the shard files, checks prefix identity, sums per-level counts, compares with the README reference |

## Design (own choices, not copied)
* State (copied per DFS level, ~1 KB): vertex count V, labels in appearance order, component id = smallest
  label in the component, per-component vertex bitmask, full within-component distance matrix (u8),
  per-vertex distance bitset `D[v]` (3×64 bits, bit d = distance d from v), per-vertex max distance,
  global realised set `R` (bit 0 set so `t = ctz(~R)`), edge list.
* Next weight `t` = least positive integer not in `R` (forcing lemma). Children in this order:
  joins over unordered pairs `x<y` of *eligible* vertices in different components, attachments at eligible
  `x` (needs V+1 ≤ n), one new isolated edge (needs V+2 ≤ n).
* Eligibility of `x` for weight `t`: (i) isomorph rejection — if the component of `x` has exactly two
  vertices, only the smaller label is eligible; (ii) necessary distance test — `t + maxD[x] ≤ N` and
  `((D[x] ∪ {0}) << t) ∩ R = ∅` (these are exactly the new distances of an attachment at `x`, and a
  subset of the new distances of any join at `x`).
* Join test: iterate `a` over the smaller of the two components, translate `(D[y] ∪ {0})` by
  `dist(a,x)+t`, reject if any translate exceeds N, meets `R`, or meets the union of previous translates
  (repeated distance); the union `U` becomes the new part of `R`.
* Leaf: `ne = n−1` (then necessarily V = n, one component); the code asserts `|R| = N` (all N pair
  distances distinct and ≤ N ⇒ exactly {1..N}); the witness is printed, not expanded.
* `--sumrule` (default ON, `--no-sumrule` to disable): do not expand a node when `t + w_max > N`
  (the new edge and the heaviest edge lie on a common path of any completing tree). Necessary condition,
  never removes a solution; it does change node counts (see below), and the reference engine has it, so
  it is on by default for count comparison.
* Sharding: level-L nodes are numbered in DFS order; shard `i` of `K` expands only those with index
  ≡ i (mod K); levels ≤ L are visited (and counted) by every shard. `--maxlevel M` stops expansion at
  level M (used to obtain exact whole-tree prefix counts cheaply).

## Validation (all OBSERVED 2026-08-18)
* n=4: 2 solutions (`0-1:1 0-2:2 0-3:4` star, `0-1:1 2-3:2 0-2:3` path); n=6: 1 (double star, = L6 of
  `data/known_leech_trees.json` up to relabeling); n=5,7,8,…,16: 0. All witnesses pass checker_a and checker_b.
* Isomorph rejection / exactly-once: `oracle_brute.py` per-level counts == engine (`--no-sumrule`) for
  n=4..12 at every level (n=11: 1,1,2,8,41,229,1383,8645,43855,69144; n=12 without sum rule:
  …,278539,356480 / 704,495 nodes; oracle with `--sumrule`: 356,479 / 704,494 — both variants agree with the engine).
* Sharding identities (`check_sharding.py`): 11 cases n∈{6,10,11,12}, (K,L)∈{(3,2),(4,3),(3,6),(7,5),
  (13,8),(5,4),(4,9),(1000,7),(13,8),(7,5),(3,9)}: for d ≤ L each shard equals the full run, for d > L
  the shard entries sum to the full run, Σnsol = nsol, Σnodes = K·prefix + rest, and each shard sees
  exactly `levels[L]` level-L nodes.
* Per-level agreement with the reference engine (referee-forest.md §1 table, README):
  n=4..11 identical at every level (totals 6/11/47/215/961/4750/23451/123309).
  n=12: identical **with** the sum rule (…,278539,356479; 704,494 nodes). **Without** the sum rule the
  clean-room engine and the brute oracle both give level 10 = 356,480 (704,495 nodes): the sum rule fires
  exactly once at n=12 (level-9 node `0-1:1 2-3:2 2-4:3 5-6:4 0-7:6 2-5:8 5-8:9 3-7:16 3-9:29`, t=38,
  38+29 > 66, whose only child `10-11:38` is then not generated). So the referee's remark "the sum rule
  never fires for n ≤ 12" is off by one node at n=12; harmless (necessary condition), but the referee's
  Python `brute` count 356,479 must have had the sum prune on.
  n=13: 1,1,2,8,41,229,1384,8898,62402,424878,1864968,1815478 (4,178,290 nodes; identical with/without sum rule).
  n=16 full: 1,1,2,8,41,229,1384,8899,62843,480048,3968025,33269745,220001476,683511193,154735257,0 —
  **1,096,039,152 nodes, identical to `results/forest_order_16.out` at every level**, 0 trees; 492 s (loaded machine)
  vs 449 s reference.
  n=17 levels 0–12 (`--maxlevel 12`): 1,1,2,8,41,229,1384,8899,62843,**480084,3983102,35234962,303618177** — matches.
  n=18 levels 0–12: 1,1,2,8,41,229,1384,8899,62843,**480085,3984162,35540837,332597341** — matches (56 s).
* Speed: ~2.4–3.7 M nodes/s single core unloaded (n=13–15), ~1.6 M nodes/s per process with 5 concurrent
  nice-15 processes at n=18 (memcpy-per-node design; ~0.7× the reference engine).

## n=18 full run
`cleanroom/run_shards.sh 18 100 8 5` (K=100 shards, L=8, 5 workers, nice 15) → `results/cleanroom_forest_18_shard{0..4}.jsonl`.
Aggregation / verdict: `python3 cleanroom/verify_18.py`.
Status at commit time: 100 shards launched 2026-08-18 (~6 min CPU per shard, ~2 h wall with 5 workers), 57/100 done, all
`nsol 0`, prefix histogram identical in every shard.  Partial results are in the shard files (resumable: re-running
`run_shards.sh 18 100 8 5` skips DONE shards).

How to verify once all 100 shards are DONE:
```
cd ~/Documents/claude/projects/leech-trees && python3 cleanroom/verify_18.py 18
```
`verify_18.py` (a) parses every JSON record in `results/cleanroom_forest_18_shard*.jsonl` (and prints any `SOL:` witness
line), (b) asserts all records are `DONE` with the same `[K,L]` and that every shard's levels 0..8 equal the prefix
1,1,2,8,41,229,1384,8899,62843, (c) sums levels 9..17 over shards, and — when all K=100 are present — prints
`per-level counts`, `nodes total (unique)` = Σnodes − (K−1)·73,408, `nsol`, and the two verdict lines
`REFERENCE PER-LEVEL MATCH: True/False` (levels 0–17 vs README/referee: …,480085,3984162,35540837,332597341,
2896330052,17017193146,37669242243,1824413062,0) and `unique nodes == 59,779,854,336: True/False`.
Expected if the clean-room engine agrees with the reference: both True and nsol = 0.
For n=17 the same script (`verify_18.py 17`) compares levels 0–12 against the referee prefix.
