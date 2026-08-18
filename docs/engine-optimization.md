# Engine optimization log (2026-08-18)

Goal: cut the cost of the hard n=16/n=18 topologies (few leaves, long spine) by >= 10x while staying exact.
Two outcomes: (A) the per-topology engine `src/leech_search.cpp` was rewritten around incremental component groups
(v2, ~2x on the hard set, exact); (B) a topology-free **forest engine** `src/forest_search.cpp` (Calhoun Alg. 2.7 with
complete isomorph rejection and bitset distance sets) shares the whole search tree across all topologies and is
2-3 orders of magnitude cheaper in total; it is the recommended route to n=18.  All numbers below were measured on a
heavily loaded M4 (10 background `leech_search` + cadical jobs), so wall times are noisy; node counts are exact.

## Benchmark sets
- `results/bench/quick16.jsonl` (8 topologies, 8 leaves, 3-11 M base nodes), `q3.jsonl` = first three (iteration set).
- `results/bench/hard16.jsonl` (20 topologies, <=7 leaves, diameter 8-11; the 10 slowest UNSAT + 10 UNKNOWN(200 s) of the sample).
- `results/bench/hard18.jsonl` (5 n=18 survivors: 3 with 10 leaves, 2 with 9 leaves, diameter 8-10).
- `results/bench/planted.json`, `planted_big.json`: random-weight instances (custom target sets) with known solution counts.
Scripts: `scripts/bench.sh BIN file [flags]`, `scripts/bench_full.sh BIN file REPS [flags]` (min user-CPU of REPS full runs),
`scripts/bench_cost.sh BIN file NODECAP REPS [flags]` (us/node under a node cap).

## A. Per-topology engine v2 (`bin/leech_search_v2`, `--legacy` gives the old prune path)
### What was measured first (base engine, q3 set, node counts)
| variant | nodes (3 topologies) | note |
|---|---|---|
| base (all prunes) | 7.08 M | 2.0 us/node user time |
| --no-fc | 26.0 M | domains/forbids/Hall-lo are the useful part |
| --no-grp2 | 11.4 M | one-edge-difference forbids: 1.6x |
| --no-hall | 10.5 M | Hall lower bound: 1.5x |
| --no-parity, --no-sum, pairUB in Hall, pairLB in Hall, Hall upper side, hi_e in Hall | identical | never kill at n=16 |
| --cover | 6.84 M | -4% |
| --match | identical | exact matching adds nothing beyond counting |
Kill anatomy (hard16 id 4360, 29.7 M nodes): Hall-L kills at v = t (no edge can take t): 5.9 M, v-t <= 3: 3.3 M,
v-t > 40: 6.5 k; lb > N: 12 M.  Domains are large (~50 values at k=7), so unit propagation is useless; the search dies
at depth 8-10, t = 12-17, from local collisions/counting in the low window.

### v2 changes (all exact; identical solution counts on planted sets in every flag combination, ladder n=4/6/5/9/11 unchanged)
1. **Component groups**: comp[]/cmask[] of the assigned forest; `G[a][b]` = bitset of partial sums of the pairs
   (x in a, y in b).  All pairs of a group share the unassigned-edge set (their path in the quotient tree), so
   `assign(e,w)` = shift every group whose quotient path crosses e by w, merge the two endpoint groups (dup => dead),
   with a save/restore undo stack.  This replaces the O(P) hashing passes: same-set duplicates (grp), singleton lists,
   and the general one-edge-difference rule (grp2) become: for unassigned e=(B,C) and every other component A,
   `w_e not in near_A - far_A` (near = G[A][B], far = G[A][C]).  Per node: O(k * #components) group ops.
2. **64-bit windows**: everything is evaluated in [t, t+63] (domain, forbidden set via the smaller side of near/far with
   `bitreverse`, Hall counting over [t, t+40] with per-group skip); full range only as a fallback.  hi_e / pairUB / Hall
   upper side / sum prune dropped from the fast path (measured zero effect).
3. **Child filter (--look, default on)**: before assigning (e,t), check that the next missing value t' can be placed on some
   other edge f (t' in dom_f and translates S_f+t', S_e+t disjoint) - a superset of the child's own test; kills the
   ~60% of leaves that die at "no edge can take t" without paying assign+prunes for them (-25% nodes).
4. **Window cover (--wcover B, default 50)**: values below the smallest lower bound of any multi-edge pair must be
   covered by disjoint translates S_e + w_e (w_e in dom_e); a budgeted 64-bit DFS with warm start from the parent's
   cover; give-up = alive.  Halves the nodes; the DFS costs ~0.4 us/node, net ~1.3x.
5. Distinctness-adjusted lower bounds for multi-edge pairs (sorted lo_e with +1 steps, max with pms[r]).

### v2 results
q3 (3 quick topologies, user CPU): base 14.6 s / 7.08 M nodes -> v2 7.6 s / 3.67 M nodes (1.9x).
hard16 (wall, both under load; base run first):
| id | base nodes | base s | v2 nodes | v2 s | node ratio | time ratio |
|---|---|---|---|---|---|---|
| 11198 | 38.2 M | 95 | 17.2 M | 60 | 2.22 | 1.57 |
| 10710 | 30.4 M | 83 | 14.9 M | 50 | 2.03 | 1.65 |
| 4360 | 29.8 M | 79 | 13.8 M | 47 | 2.16 | 1.67 |
| 5569 | 28.5 M | 76 | 13.4 M | 46 | 2.13 | 1.66 |
| 5020 | 28.9 M | 75 | 13.4 M | 48 | 2.15 | 1.55 |
| 3517 | 31.2 M | 90 | 13.5 M | 44 | 2.32 | 2.05 |
| 4301 | 28.9 M | 76 | 13.3 M | 43 | 2.18 | 1.75 |
| 14084 | 28.6 M | 72 | 13.5 M | 47 | 2.11 | 1.54 |
| 1388 | 30.8 M | 76 | 14.3 M | 48 | 2.16 | 1.58 |
| 9671 | 30.6 M | 79 | 13.3 M | 46 | 2.30 | 1.69 |
| 4924 | 140.8 M | 367 | 59.6 M | 200 | 2.36 | 1.84 |
| 4437 | 66.1 M | 168 | 28.0 M | 91 | 2.36 | 1.84 |
| 302 | 56.0 M | 148 | 27.7 M | 84 | 2.02 | 1.76 |
| 1890 | 57.7 M | 143 | 25.0 M | 70 | 2.31 | 2.03 |
| 156 | 48.8 M | 136 | 24.9 M | 64 | 1.96 | 2.12 |
| 12155 | 57.5 M | 160 | 26.2 M | 72 | 2.19 | 2.23 |
| 4779 | 134.4 M | 454 | 56.8 M | 156 | 2.37 | 2.90 |
| 4391 | 65.3 M | 215 | 27.8 M | 78 | 2.35 | 2.78 |
| 379 | 126.9 M | 414 | 57.5 M | 147 | 2.21 | 2.83 |
| 702 | 144.8 M | 482 | 57.6 M | 150 | 2.51 | 3.21 |
| **total (20, all UNSAT)** | 1204 M | 3488 | 532 M | 1593 | **2.26** | **2.19** |
hard18 (5 survivors):
| id (leaves) | base nodes | base s | v2 nodes | v2 s | node ratio | time ratio |
|---|---|---|---|---|---|---|
| 84692 (10) | 11.5 M | 58 | 6.0 M | 28 | 1.91 | 2.09 |
| 15758 (10) | 4.9 M | 22 | 2.6 M | 12 | 1.90 | 1.89 |
| 86493 (10) | 23.7 M | 111 | 12.8 M | 60 | 1.85 | 1.85 |
| 27764 (9) | 23.0 M | 108 | 11.4 M | 49 | 2.02 | 2.21 |
| 28295 (9) | 61.9 M | 295 | 30.0 M | 127 | 2.06 | 2.32 |
Honest summary: v2 = ~2.2x fewer nodes and ~1.6-2x wall on the hard set.  Every further prune tried
(lazy vs. materialised forbids, Hall window, exact hi_e, wcover budgets 3-1000, forbidden memo, hallw 8-78) was
time-neutral within noise: the per-topology search is dominated by re-deriving the same small-weight forests.

## B. Forest engine (`src/forest_search.cpp`, `bin/forest_search`)
Search over weighted forests with the forced next weight (Calhoun Alg 2.7): the next edge joins two components,
attaches a new vertex, or is a new disjoint edge.  New: (i) every abstract forest is generated exactly once
(parent = remove the max-weight edge; Aut of a distinct-weight forest = endpoint swaps of its single-edge components,
so only the smaller endpoint of a single-edge component is used as an attachment) - this alone cut nodes 10x at n=12-13;
(ii) per-vertex distance bitsets D0[x] with sumset-by-shift tests, incremental undo; (iii) w_i + w_j <= N.
Note: the vertex/component "budget" is an invariant (every edge type reduces (#comp-1)+(n-|V|) by exactly 1), so the
only prunes are value-based; the tree dies at the last two levels.
Validation: n=4 -> 2 trees, n=6 -> 1, n=5,7..16 -> 0 (matches Leech/Taylor/SWZ/Calhoun; witnesses pass both checkers);
solution counts equal the per-topology engine summed over all topologies on planted targets (tests/test_forest_search.py);
shards partition the count.
Node counts (single core, `-q`):
| n | nodes | user CPU (loaded M4) | Leech trees | level counts (last four) |
|---|---|---|---|---|
| 11 | 123 309 | 0.05 s | 0 | |
| 12 | 704 494 | 0.14 s | 0 | L8 58.9k, L9 279k, L10 356k |
| 13 | 4 178 290 | 0.9 s | 0 | L9 425k, L10 1.86M, L11 1.82M |
| 14 | 25 486 327 | 6.4 s | 0 | L10 3.25M, L11 13.0M, L12 8.66M |
| 15 | 162 497 458 | 44 s | 0 | L11 26.2M, L12 93.5M, L13 38.4M |
| 16 | 1 096 039 152 | 321 s | **0** (Calhoun 2007 reproduced) | L12 220M, L13 684M, L14 155M |
Growth ~6.5x per n; per node 0.25-0.3 us.
Level counts converge to universal values as n grows (L6=1384, L7=8899, L8=62.8k, L9~=4.7e5, L10~=3.3e6, ratio ~7.5x
per level); the last three levels dominate.
Measured on the first 44 of 512 n=18 shards: 117 M nodes and 79 s per shard (nice 15 on the loaded machine) =>
n=18 ~ 6e10 nodes, **~11 CPU-hours total** (~5-6 h unloaded; wall ~2.5 h with 5 processes), trivially parallel (`src/run_forest.py 18 --shards 512 --procs P`, or the SGE array
`scripts/hoffman2_forest_array.sh`), versus 1e4-1e5 CPU-hours projected for the per-topology engine (v2 halves that).
For n=16 the forest engine needed 321 CPU-s against ~500-700 CPU-hours for the per-topology run: ~5000x.
Runs launched 2026-08-18: `results/forest_order_17.jsonl` (32 shards) and `results/forest_order_18.jsonl` (512 shards),
logs `results/forest_order_1{7,8}.log`; every SOL line is re-checked with checker_a/checker_b.  Cross-check plan for n=18: forest engine (all topologies at once) + per-topology v2 on the
cluster as an independent method.
