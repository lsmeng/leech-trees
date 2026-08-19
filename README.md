# Leech trees, order 18 — Phase 2 workspace

Question: does a tree on 18 vertices with positive-integer edge weights exist whose 153 pairwise
path sums are exactly {1,…,153}? (Leech 1975; smallest open order per FrontierMath / EJGTA 2020 / Integers 2016.)
Started 2026-08-18 from Codex Phase-1 handoff `~/Documents/Codex-Handoffs/mathematical-problem-discovery_*.md`.

## Status ledger (label every claim)
- OBSERVED 2026-08-18: five known Leech trees reproduced by brute force for n<=6 (n=2,3,4 star,4 path,6 double-star). data/known_leech_trees.json
- OBSERVED: two independent checkers (src/checker_a.py BFS; src/checker_b.py depth+LCA) agree on 5 known + 1000 perturbations. tests/test_checkers.py
- OBSERVED: unlabeled tree counts by two generators (networkx WROM vs nauty gentreeg) agree: n=5:3, 9:47, 11:235, 16:19320, 18:123867. data/trees_18.jsonl frozen.
- OBSERVED: CP-SAT (v1/v2/v3) proves n=5, n=9 infeasible for all topologies (results/order_5,9.jsonl); n=6 finds the known tree; n=11 partial (v2 solves the slow ones in 10-60 s).
- OBSERVED: generic CP-SAT does NOT scale: random n=16 topologies UNKNOWN after 240 s x 10 workers. => n=18 needs a purpose-built search (this is the actual research core, not done).
- OBSERVED 2026-08-18 (C++ engine, bin/leech_search): n=4 both known trees SAT (witnesses pass checker_a+b), n=6 exactly the known
  double-star SAT + 5 UNSAT, n=5 (3), n=9 (47), n=11 (235) all UNSAT (n=9 agrees id-by-id with CP-SAT results/order_9.jsonl);
  n=11 total 3.2M nodes / ~5 s single core (CP-SAT needed 10-60 s per slow topology).
- OBSERVED 2026-08-18: n=16 random 200-topology sample (results/cpp_bench16_sample.jsonl, 200 s cap, loaded machine ~0.3 M nodes/s):
  time quantiles 10/25/50/75/90% = 0.6/2.5/19/100/>200 s; 30/200 hit the 200 s cap; nodes median 6M, mean 18M (capped);
  hardness is set by leaf count / diameter: >=9 leaves ~1 s, 7 leaves ~75 s, <=6 leaves & diameter >=10 typically 150-900 s
  (Golomb-ruler-like spines). Full n=16 run launched: `nohup python src/run_cpp.py 16 --procs 10 --time 3600` ->
  results/cpp_order_16.jsonl (+ .log); projected 2-3 days on this Mac; re-run UNKNOWNs with --redo-unknown --time larger.
- OBSERVED 2026-08-18: n=18 spot checks (survivor topologies): 12 leaves ~0.2-1 s, 10 leaves 17-61 s, 9 leaves 126 s / >240 s,
  i.e. ~30-60x harder than the same leaf class at n=16.  Extrapolation for all 122k n=18 topologies: mean ~1-3 h/topology
  => ~10^4-10^5 CPU-hours (Hoffman2-scale, not a laptop job).  Bottleneck: path-like / few-leaf topologies where the small
  weights form long Golomb-ruler segments; the bottom-up forcing search has ~10^8-10^9 nodes there.
- OBSERVED 2026-08-18 (engine v2, docs/engine-optimization.md): rewrite of the per-topology engine around incremental
  component groups + 64-bit windows + window-cover lookahead: exact (identical solution counts on planted sets in every
  flag combination, ladder unchanged), 2.26x fewer nodes and 2.2x faster on 20 hard n=16 topologies, ~2x on 5 n=18
  survivors.  Binary bin/leech_search_v2 (bin/leech_search = old build kept for the running n=16 job; `--legacy` = old prunes).
- OBSERVED 2026-08-18 (FOREST ENGINE, src/forest_search.cpp): Calhoun's forest DFS (forced weights, edge added by join /
  attach / new) with complete isomorph rejection (parent = remove max edge; Aut = endpoint swaps of single-edge
  components) and bitset distance sets: n=4 -> 2 trees, n=6 -> 1, n=5,7..16 -> 0; **n=16: 1.10e9 nodes, 321 CPU-s**
  (vs ~500-700 CPU-h for the per-topology run) and **n=17: 7.9e9 nodes, 1.7 CPU-h, 0 trees**, both reproducing Calhoun 2007; agrees with the per-topology engine summed
  over all topologies on planted targets (tests/test_forest_search.py).  Growth ~6.5x per n => n=18 ~ 5e10 nodes,
  ~5-10 CPU-hours: launched locally (results/forest_order_17.jsonl, forest_order_18.jsonl; src/run_forest.py).
- LITERATURE (unverified copies): 9,11 ruled out computationally by Székely–Wang–Zhang 2005; all perfect-distance trees n<18 determined by Calhoun et al. 2007 (so 16 done); diameter-3 excluded n>=7 and finitely many diameter-4 (Luo–Yu 2024).
- LITERATURE LEDGER 2026-08-18: docs/literature-ledger.md (SWZ05 preprint + code recovered via Wayback, Calhoun07 OCR, EJGTA20, Integers16 read; Luo-Yu24 abstract only). Verified topology filters in src/filters.py kill only 152/123867 topologies at n=18 (diameter<=14 via Golomb rulers, max degree<=11 via exhaustive star-Sidon search, diameter>=4, no path/broom): 123,715 survive. Real pruning is weight-side: forcing lemma (k-th smallest weight = least missing distance), Taylor 11/7 parity, m1<=105, m2<=76.
- CORRECTION: Taylor's parity condition constrains the parity pattern of *weights* (count of odd-depth vertices must be 7 or 11 at n=18); it is NOT a topology filter (bipartition of the unweighted tree is irrelevant). Implemented as a redundant constraint in solve_v2.

## C++ exact engine (src/leech_search.cpp, 2026-08-18)
Build: `scripts/build.sh` -> `bin/leech_search` (clang++ -O3, no deps).  Driver: `python src/run_cpp.py n [--procs P] [--time T]
[--sample K --seed S] [--redo-unknown]` -> `results/cpp_order_{n}.jsonl` (resumable; every SAT witness re-checked by checker_a+b).
Primary branching = FORCING LEMMA (Calhoun Lemma 2.6 / SWZ "Find-Next-Weight"): at level t all values < t are realized, so t is either
already realized (skip) or must be the weight of an unassigned edge -> branch over <= n-1-k edges.  Alternatives kept as options:
`--mode edge` (edge-driven, dynamic min-domain / bfs / leaf-first order) and `--mode ff` (fail-first value choice); both lose to
value mode (edge mode ~20x more nodes at n=9, ff ~2x at n=11).
Pruning (all switchable, all verified sound on planted instances, see tests/test_cpp_search.py): bitset distinctness; grp
(pairs with identical unassigned-edge set need distinct partial sums; the biggest single win, 2x nodes) and its 2-crossing
domain-forbid form; sum identity Σ c_e w_e = N(N+1)/2 (min/max + per-edge UB); forward check of per-edge domains via shift-AND;
Hall prefix/suffix counting on pair windows [LB,UB] (LB = partial + smallest missing / Golomb OGR(hop+1); UB = containment
N+1-s_x s_y, Calhoun m1 <= (4n-1)^2/48, w_i+w_j <= N); Taylor parity DP over forest components; top-value structure (N-1,N-2
pairs meet the N pair); root filters (Golomb/containment windows, degree bound OGR(d)+OGR(d-1)+2 <= N+1-b1 b2); complete
symmetry breaking (iso sibling subtrees + bicentral swap; verified count = total/|Aut|).  Optional: `--grp2` (general
superset-forbid; -35% nodes, ~neutral in time), `--cover`, `--match` (exact interval matching; no gain).
OBSERVED: the theory-branch weight bounds (containment/Golomb/top/degree) change node counts by <1% in this bottom-up search
(the search dies at small values long before large values are reached); the useful ones are the small-value structure prunes.
Node rate ~0.7-1.5 M nodes/s single core; prunes() is 90% of the time.

- OBSERVED 2026-08-18: SAT route (src/sat_encode.py order-encoding + cadical + drat-trim): n=4 both SAT, n=6 exactly the known tree SAT, n=9 all 47 UNSAT and n=11 all 235 UNSAT with drat-trim-VERIFIED DRAT proofs (results/sat_order_{n}.jsonl); n=16 random 30: 0/30 within 600 s. Certificates up to n=11 only; not a route to n=18 by itself. docs/sat-route.md

## Layout
src/checker_a.py, checker_b.py   independent witness checkers
src/enumerate_trees.py           two-route topology enumeration + AHU certificate cross-check
src/solve_topology.py (v1), solve_v2.py (bounds+Taylor+symbreak+strategy), solve_v3.py (dual channel; slower)
src/run_order.py                 parallel resumable driver -> results/order_{n}.jsonl
src/leech_search.cpp, scripts/build.sh, src/run_cpp.py   C++ exact engine + driver -> results/cpp_order_{n}.jsonl
tests/test_cpp_search.py         engine regression (known trees, UNSAT orders, planted-instance prune consistency, symmetry completeness)
src/filters.py                   one function per proven lemma (topology filters) + self-tests; docs/literature-ledger.md, docs/sources/
data/trees_{n}.jsonl             frozen topologies; results/                per-topology outcomes

## Forest engine (src/forest_search.cpp, 2026-08-18) -- recommended route to n=18
`bin/forest_search n [--target ...] [--shard i K] [--shard-level L] [-q]`; sharded resumable driver `python src/run_forest.py n
--shards K --procs P` (witnesses re-checked by both checkers); cluster array `scripts/hoffman2_forest_array.sh`.
Details, benchmarks and the v2 per-topology results: docs/engine-optimization.md.

## Next (research core)
1. DONE (docs/literature-ledger.md): literature gives ~no topology pruning; build the search around the weight-forcing lemma.
2. Purpose-built search: branch on values (small-first or diameter-first) with bitset incremental distinctness; C/Rust; benchmark on n=16 (known UNSAT) as calibration.
3. Only then n=18 on Hoffman2; certificates: enumeration logs + per-topology proof (DRAT/VeriPB via SAT encoding) for the final claim.

## 2026-08-18 evening — first complete n=18 verdict (OBSERVED, pending referee)
- Hoffman2 (SLURM job 83703, 30 tasks × 7 procs, gcc 11.5 x86_64) forest engine `bin/forest_search 18 --shard i 210 --shard-level 8`: **210/210 shards DONE, 5.98e10 nodes, nsol = 0, depth-17 count = 0** — i.e. no 18-vertex Leech tree found by the forest engine. Raw shard outputs archived in results/hoffman2/. Wall ~1.5 min per task.
- Status label: COMPUTATIONAL EVIDENCE. Becomes a claim only after (a) docs/referee-forest.md verdict on isomorph rejection/sharding/forcing completeness, (b) independent local re-run (clang, arm64, 512 shards; results/forest_order_18.jsonl in progress), (c) cross-check with the per-topology engine leech18 on Hoffman2 (independent method; UNKNOWNs to be rerun with v2 + larger caps).
- n=16 per-topology run on Hoffman2 finished: 19,308 UNSAT + 12 UNKNOWN (cap 1800 s) → rerun UNKNOWNs; forest engine already reproduces Calhoun's n=16 result.

## 2026-08-18 ~18:00 — n=18 forest-engine verdict replicated three ways (OBSERVED)
| run | machine/compiler | shards (K,L) | Σnodes | unique nodes (Σ − (K−1)·prefix) | levels 9–16 sums | level 17 | nsol |
|---|---|---|---|---|---|---|---|
| Hoffman2 job 83703 | x86_64 gcc 11.5 | 210, 8 | 59,795,196,608 | 59,779,854,336 | == oracle (9–12), 2.896e9/1.702e10/3.767e10/1.824e9 (13–16) | 0 | 0 |
| Hoffman2 job 83752 | x86_64 gcc 11.5 | 175, 9 | 59,876,162,118 | 59,779,854,336 | identical | 0 | 0 |
| local | arm64 clang | 512, 8 | 59,817,365,824 | 59,779,854,336 | (stderr not kept) | — | 0 |
Verdict script: src/verify_forest_run.py. Referee: docs/referee-forest.md (no BUG; isomorph rejection, forcing completeness, prefilters, sharding all VERIFIED). Remaining for a paper-grade claim: independent-method cross-check (per-topology engine on Hoffman2: first pass at ~73k/122k, UNKNOWNs rerun with v2 queued) and ideally a second implementation of the forest search from the algorithm description reproducing the per-level counts.

## 2026-08-18 ~20:20 — fourth replication: CLEAN-ROOM implementation (OBSERVED)
`cleanroom/cr_forest.c` (written by an agent that never opened forest_search.cpp; own labeling/canonical scheme; C/clang, arm64, K=100, L=8, 34,207 CPU-s):
all 18 per-level forced-forest counts identical to the reference engine (1,1,2,8,41,229,1384,8899,62843,480085,3984162,35540837,332597341,2896330052,17017193146,37669242243,1824413062,0), unique nodes 59,779,854,336, nsol = 0. `python3 cleanroom/verify_18.py 18` → REFERENCE PER-LEVEL MATCH: True. Details docs/cleanroom-forest.md.
Status: the per-level count sequence — a mathematical invariant of the forced-forest tree — is now reproduced by two independent implementations on two architectures/compilers. The remaining independent-METHOD check is the per-topology engine (Hoffman2 leech18, ~88k/122k first pass).

## 2026-08-19 00:00 — per-topology engine: n=16 COMPLETE (OBSERVED)
Hoffman2 per-topology run: 19,308 UNSAT (v1, cap 1800 s) + 12 UNKNOWN rerun with v2 (cap 6 h) → all 12 UNSAT in 673–1317 s ⇒ **19,320/19,320 topologies UNSAT** — independent-method reproduction of Calhoun 2007 (n=16). n=18 first pass at ~111k/122k with ~34% UNKNOWN at the 300 s cap; UNKNOWN rerun with v2 (cap 3600 s) to be queued after the first pass; this cross-check will outlive the 24-h window and is not on the critical path (forest engine ×2 implementations is the primary evidence).

## 2026-08-19 03:30 — per-topology n=18 first pass COMPLETE (OBSERVED)
Hoffman2 job 83594 (v1 engine, cap 300 s, easy-first): 122,344/122,344 survivor topologies processed: **73,021 UNSAT, 49,323 UNKNOWN, 0 SAT**. UNKNOWN rerun with v2 (cap 3600 s) queued as job `redo18` (60×7 procs, resumable, results/redo/). Independent-method cross-check therefore currently covers 59.7% of survivor topologies (plus the 1,523 non-survivors killed by proven filters); the forest-engine verdict (2 implementations, 4 runs) remains the primary evidence.

## 2026-08-19 (later) — per-topology cross-check progress
`redo18` (v2 engine, cap 3600 s) has re-decided 17,273 of the 49,323 first-pass UNKNOWNs: **17,272 UNSAT, 1 still UNKNOWN at 1 h, 0 SAT**. Independent-method coverage now 90,293 / 122,344 survivor topologies (73.8%); remaining shards queued on Hoffman2 (no Claude budget needed).
