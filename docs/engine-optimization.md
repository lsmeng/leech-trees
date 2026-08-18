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
TABLE_HARD16
hard18 (5 survivors):
TABLE_HARD18
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
TABLE_FOREST
Level counts converge to universal values as n grows (L6=1384, L7=8899, L8=62.8k, L9~=4.7e5, L10~=3.3e6, ratio ~7.5x
per level); the last three levels dominate.
Projection: n=17 ~ 1e10 nodes (~5-10 CPU-h), n=18 ~ 1e11-1e12 nodes at 1.5-3 us/node = **50-800 CPU-hours total**,
trivially parallel (`--shard i K` at level 8: 62 814 subtrees), versus 1e4-1e5 CPU-hours projected for the per-topology
engine (v2 halves that).  Cross-check plan for n=18: forest engine (all topologies at once) + per-topology v2 on the
cluster as an independent method.
