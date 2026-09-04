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

## 2026-08-20 — minimal distinct distance trees at n=12 (OBSERVED)
The Hoffman2 D=77 exhaustive run completed with 70/70 shards DONE, 1,020,925,849,186 nodes and exactly two solutions up to
isomorphism. Both witnesses independently pass `variants/checker_distinct.py` (BFS distances) and a separate rooted-depth/LCA
distance computation. Together with the completed UNSAT runs at D=69,...,76, this gives **M(12)=77**, with exactly two minimal
trees (improving Calhoun et al.'s literature bounds 69 <= M(12) <= 94). Witnesses and missing-distance sets are recorded in
`variants/RESULTS.md` and `paper/main.tex`.

## 2026-08-20 13:27 PDT — per-topology n=18 cross-check progress (OBSERVED)
The running Hoffman2 `redo18` campaign has raised independent-method coverage to **112,082 / 122,344 survivor topologies
(91.6%) UNSAT**, with 1,169 re-run cases still UNKNOWN at the 3600 s cap and 0 SAT. This is corroboration only; the complete
forest-engine result and its clean-room replication remain the basis of the n=18 theorem.

## 2026-08-20 — uniform spider theorem (OBSERVED; computer-assisted proof)

- OBSERVED — **No spider Leech tree exists at any order `n>=5`** (paths included).  The exact top-down search is reduced to three
  exhaustive regions: a relaxed, `n`-independent offset search closes every anchor with second tip `U>10` and tip gap `T-U>10`
  in 111 states; two affine searches close the 20 boundary strips `U<=10` or `T-U<=10` for unbounded parameter `P>=51` in
  1,123 states; and the original exact numeric search closes the finite base `n=5,...,15` in 16,153 states.  Full proof and trust
  boundary: `docs/spider-uniform-theorem.md`; one-command verifier:
  `nice -n 10 python3 theory-lab/catspider/verify_spider_uniform.py`; archived summary:
  `theory-lab/catspider/results/spider_uniform_certificate.json`.
- OBSERVED — independent adversarial audit verdict: **SOUND**.  The audit reproduced the complete verifier, checked every finite
  partition, compared 2,000 exact/affine boundary anchors and 2,500 exact/relaxed regular anchors, and found no missing regime,
  unsound relaxation, symmetry loss, or counterexample.  It did find that load-bearing Python `assert` statements disappeared
  under `python -O`; these are now explicit checks and the verifier refuses optimized mode.  Report:
  `docs/referee-spider-uniform.md`.
- LITERATURE — Varghese, Savithri, and Arumugam (AIP Conf. Proc. 2649, 2023, 020007;
  DOI `10.1063/5.0114834`) proved nonexistence for diameter-four tristars `T_{m,n,l}`.  Their special family `T_{1,r,1}` is a
  spider with two length-two legs and `r` unit legs; the theorem above strictly extends that overlap to every spider and every
  order `n>=5`.
- OBSERVED — corroboration not used in the proof: the cap-aware full numeric search at `n=100` closes 2,474 anchors in 273,133
  states, with deepest missing offset 25, at most 9 non-central marks, zero vertex-budget rejections, zero solutions and zero
  window frontier.  Raw summary: `theory-lab/catspider/results/spider_window_n100.json`.
- OBSERVED — this result is now the paper's second main theorem and has its own proof section in `paper/main.tex`.

## Next after spiders (UNVERIFIED roadmap)

- OBSERVED — the exact bi-spider engine (trees with at most two branching vertices) finds the known order-six double star, agrees
  between Python and C through `n=13`, and closes orders 25 and 27 with zero solutions.  A genuinely different immutable
  geometric search now agrees with the C engine separately on every `LR`/`LL` regime through `n=10` (27,046 nodes per
  implementation); all three positive controls pass `checker_a.py` and `checker_b.py`.  This independently audits the option
  enumeration but is not a second full run at orders 25 or 27.
- OBSERVED — six uniform `LR` regions are now proved by paired incremental/clean-room finite relaxations.  For
  `N=A+Q+B`, `A<B`, the first two exclude (a) `A>20` and `Q-(B-A)>20` (2,871 states, window 20), and
  (b) `A>15` and `B-(A+Q)>15` (1,881 states, window 15).  A third 1,956-regime certificate excludes
  `A>50` and `-15<=Q-(B-A)<=20` (2,402,716 states, window 50, zero frontier; full per-regime agreement between the
  two implementations).  Consequently **no `LR`-anchored bi-spider with `A>50` can be Leech**.  Those three regions cover
  16,500 / 21,905 legal `LR` anchors at order 25 and 23,926 / 30,276 at order 27.  Proof and trust boundary:
  `docs/bispider-progress.md`; verifier: `theory-lab/catspider/verify_bispider_strip.py`; archived summary:
  `theory-lab/catspider/results/bispider_strip_certificate.json`.
- OBSERVED — the fourth region handles the small-`A` cases omitted above: no `LR` anchor satisfies
  `1<=A<=50`, `B>20` and `Q-(B-A)>20`.  The paired W=20 searches agree on all 50 values of `A` (87,885 states,
  zero frontier), so together with the first region every surviving positive-imbalance anchor has `B<=20`.
  Total uniform coverage rises to 18,880 / 21,905 legal `LR` anchors at order 25 (86.2%) and
  26,826 / 30,276 at order 27 (88.6%).  Verifier:
  `theory-lab/catspider/verify_bispider_smalla_positive.py`; archived summary:
  `theory-lab/catspider/results/bispider_smalla_positive_certificate.json`.
- OBSERVED — the fifth region closes that final positive-imbalance boundary: no `LR` anchor satisfies
  `B<=20` and `Q-(B-A)>20`.  Its paired search checks 10,260 finite `(A,B,Q)` regimes (564,478 states,
  zero frontier), including a proved `Q>80` stable tail.  Consequently **no `LR`-anchored Leech bi-spider has
  positive imbalance greater than 20**.  Total uniform coverage is now 19,070 / 21,905 legal `LR` anchors at
  order 25 (87.1%) and 27,016 / 30,276 at order 27 (89.2%).  Verifier:
  `theory-lab/catspider/verify_bispider_smallb_positive.py`; archived summary:
  `theory-lab/catspider/results/bispider_smallb_positive_certificate.json`.
- OBSERVED — the sixth region closes the negative-imbalance tail: no `LR` anchor satisfies
  `1<=A<=15` and `Q-(B-A)<-15`.  Its paired W=15 search checks 570 finite `(A,C=A+Q)` regimes
  (78,835 states, zero frontier), with proved stable representatives for every dominance gap and for `C>45`.
  Together with the second region, **no `LR`-anchored Leech bi-spider has imbalance below -15**.  Uniform coverage
  is now 21,065 / 21,905 legal `LR` anchors at order 25 (96.2%) and 29,386 / 30,276 at order 27 (97.1%).
  Verifier: `theory-lab/catspider/verify_bispider_smalla_negative.py`; archived summary:
  `theory-lab/catspider/results/bispider_smalla_negative_certificate.json`.
- OBSERVED — the seventh region closes that fixed-width middle boundary at every target order.  For `W=35`, paired
  incremental/immutable searches agree on all 1,800 `(A,r)` regimes with `1<=A<=50`, `-15<=r<=20`
  (1,386,587 states, deepest missing offset 34, at most 12 selected vertices, zero frontier).  They prove the stable tail
  `h=N-2A>max(35,2(35-A)+abs(r))`.  Since `n>=18` gives `N>=153`, this inequality is automatic throughout the boundary.
  Combined with the first six regions, **no `LR`-anchored Leech bi-spider of order `n>=18` exists**.  Verifier:
  `theory-lab/catspider/verify_bispider_middle_tail.py`; archived summary:
  `theory-lab/catspider/results/bispider_middle_tail_certificate.json`; proof: `docs/bispider-progress.md`.
- OBSERVED — the complete `LL` classification closes the other half of the bi-spider problem at the target orders.  Three
  disjoint paired W=36 relaxations cover all `LL` anchors: `U>36,L<=36` (1,332 regimes), `U>36,L>36` (343), and
  `2<=U<=36` (630).  The two implementations agree per regime on 740,594 states and have zero frontier; the paranoid exact
  C engine independently closes all 2,825 order-18 `LL` anchors in 723,912 states.  Combined with the completed `LR` half,
  **no Leech tree of order `n>=18` has at most two branch vertices**.  Verifier:
  `theory-lab/catspider/verify_bispider_ll.py`; archived summary:
  `theory-lab/catspider/results/bispider_ll_certificate.json`; proof: `docs/bispider-progress.md`; adversarial audit:
  `docs/referee-bispider-n18.md`.  The stronger claim for every `n>=7` remains UNVERIFIED.
- OBSERVED — the exactly-three-branch normal form, topology generator and finite order-25 exclusion are now audited.  Such a tree is uniquely
  a three-centre path with positive core lengths and three leg partitions, modulo reversal.  Exact graph-isomorphism comparison
  covers every nonisomorphic tree through order 13; an independent Burnside count agrees through order 25, where there are
  1,437,739 such topologies; and the equal-leg symmetry tags pass the exact orbit test.  OBSERVED small-order progress: the full-recomputation geometric prototype has an
  independently checked four-way anchor partition, agrees with brute option generation, and agrees with the fixed-topology
  route at orders 8--10; its order-10 total is 12,289 valid anchors, 107,677 states and zero solutions.  Details:
  `docs/threebranch-engine.md`.  OBSERVED further calibration: the validated C/bitset port completes orders 8--15 with zero
  solutions; order 15 has 225,554 valid anchors and 25,379,164 states.  Its live two-new-mark positive probe has three children,
  while no legal anchored child through order 15 uses that branch.  OBSERVED theorem: this is forced in every tree metric by the
  anchored one-vertex lemma—after a distance-`N` pair and all values above the current gap are present, the tree four-point
  condition makes any two-new realization duplicate a larger distance.  Proof: `docs/anchored-one-vertex-lemma.md`; verifier:
  `theory-lab/threebranch/verify_one_vertex_lemma.py`.  The stronger OBSERVED diameter-endpoint introduction theorem says
  every new vertex first appears with one of the two diameter endpoints; its C-engine mode preserves all 40,704,104 nodes
  and 40,167,617 legal children through order 15 while cutting generated candidates by 58.2%.  Proof and verifier:
  `docs/diameter-endpoint-introduction.md` and `theory-lab/topwindow/verify_diameter_introduction.py`.  Its graph corollary
  says that the pairs at distances `N,N-1,...,N-q` form a connected far-pair graph in decreasing-distance order;
  proof: `docs/top-window-connectivity.md`.  With both reductions, the exact order-18 run over all four anchor classes is
  complete: 756,300 anchors, 273,479,949 states, zero solutions and zero frontier.  Hence OBSERVED computationally, no
  order-18 Leech tree has exactly three branch vertices.  A conservative audit also enumerates 29,931,056,264 two-new
  candidates with zero legal pair children and identical state invariants; verifier:
  `theory-lab/threebranch/verify_threebranch_n18.py`.  A second shape-independent OBSERVED theorem now controls the whole
  top window: if a matching has `k` pairs of distance at least `N-q`, then `k^2<=2q+1`; hence every such far pair meets a
  pole cover of at most `2 floor(sqrt(2q+1))` vertices.  The proof uses only the tree four-point property and distinct integer
  distances; its verifier audits 308,880 quartet pairings and 22,560 exact far-graph matching instances.  Proof:
  `docs/far-pair-crowding.md`; verifier: `theory-lab/topwindow/verify_far_pair_crowding.py`.  OBSERVED /
  UNVERIFIED window status: the exact numeric `W=25` cutoff
  leaves nonzero frontier in all four order-18 modes, proving that width 25 is too narrow.  The analogous order-25 survey is now
  OBSERVED complete as a diagnostic: 24/24 shards, 6,137,463 anchors, 14,148,916,526 states, zero solutions but
  166,321,078 frontier states.  Thus width 25 is again decisively insufficient and this is **not** an UNSAT result; audit:
  `theory-lab/threebranch/verify_threebranch_window_n25.py`.  The widened exact `W=60` campaign is now complete: all 384 paranoid
  shards are `DONE`, with 6,137,463 anchors, 14,164,880,449 states, zero frontier and zero solutions; the deepest missing offset
  is 51.  Therefore **OBSERVED computationally, no order-25 Leech tree has exactly three branch vertices**.  The 25 KB
  deterministic raw archive and frozen aggregate are checked by `theory-lab/threebranch/verify_threebranch_n25.py`; this finite
  theorem does not exclude trees with four or more branch vertices and is not an all-order theorem.  OBSERVED next-order
  stability: the order-27 `W=70` campaign also closes all 512 paranoid shards, covering 10,055,214 valid anchors and
  33,425,785,566 states with zero frontier and zero solutions.  Its deepest missing offset is 52 and no reached state uses
  more than 15 non-centre marks, essentially unchanged from order 25.  The deterministic raw archive is replayed by
  `theory-lab/threebranch/verify_threebranch_n27.py`.  Therefore **OBSERVED computationally, no order-27 Leech tree has
  exactly three branch vertices**.  This is a second finite theorem and stability check, not an all-order extrapolation and
  not an exclusion of order-27 trees with four or more branch vertices.  In parallel, the paper-readiness task is to finish the independent
  per-topology `n=18` rerun and obtain an external
  human review; neither is needed for the already complete two-implementation forest proof.
- OBSERVED calibration / UNVERIFIED route — an affine-integer three-centre probe reproduces the exact order-10 closing
  offsets and maximum mark counts separately in all four anchor modes; its frozen rows are compared against a freshly compiled
  exact C engine by `theory-lab/threebranch/verify_threebranch_parametric_n10.py`.  Its resumable grid runner binds all solver,
  resource and source/runtime fingerprints, so results from different settings cannot be silently mixed.  The first all-integer
  `N>=153`, `AB,W=8` 8-by-8 scale diagnostic was stopped by design after eight minutes: ten empty parameter cells closed at
  the base constraints, but none of the first 32 feasible cells completed.  This is an **UNVERIFIED negative scalability
  diagnostic**, not an all-order exclusion; it rules out spending a larger Hoffman2 allocation on the present vertex-budget-free
  relaxation and redirects the proof effort to a sound order/vertex-budget transition or the constant-deletion shallow core.
- OBSERVED — the recovered hop-diameter-at-most-four engine has now passed its repository audit.  It reproduces the five known
  trees and no others at orders 2--18 (38,221,445 C++ states), agrees in solution count with an independent Python engine through
  order 13, finds all 40 planted positive controls, and retains zero solutions at order 17 when its strongest prune is disabled
  (47,986,068 states).  All five positive outputs pass both checkers.  With Taylor's LITERATURE order restriction, this class is
  classified through order 25.  The order-25 campaign has all 512 shards `DONE`, zero solutions, 322,189,234,739 reported
  nodes including repeated pre-shard prefixes, and 3,403,240.387 reported CPU-seconds.  Proof: `docs/diameter4-engine.md`;
  audit: `docs/referee-diameter4.md`; verifiers: `theory-lab/diameter4/verify_diameter4.py` and
  `theory-lab/diameter4/verify_diameter4_shards.py`; frozen aggregate:
  `theory-lab/diameter4/results/diameter4_n25_shards_certificate.json`.  This is an **OBSERVED** restriction to hop-diameter at
  most four, not a claim about arbitrary order-25 trees.

## 2026-08-21 — general nonexistence programme (UNVERIFIED roadmap)

- OBSERVED — Phase I is complete for the requested range: the uniform spider theorem and paired `LR`/`LL` certificates prove
  that every hypothetical Leech tree of order `n>=18` has at least three branch vertices.  The separate stronger bi-spider
  conjecture for every `n>=7` remains UNVERIFIED.
- OBSERVED / UNVERIFIED — Phase II has recovered and audited the hop-diameter-four source and completed both finite order-25
  restrictions: hop-diameter at most four and exactly three branch vertices.  The latter exact C/bitset route additionally
  closes order 27 in all 512 `W=70` shards with zero frontier and zero solutions.  Arbitrary order-25/order-27 trees, and the
  parameter-independent three-centre theorem needed by Phase III, remain UNVERIFIED.
- UNVERIFIED — Phase III attempts a global thin-tip descent: bounded top-window configurations should either move a
  near-diameter pair into a proper branch or terminate at a thick tip, where pole-cover, weak-Sidon, vertex-budget and
  merge-profile waste constraints are intended to contradict one another.
- OBSERVED / UNVERIFIED — the far-pair crowding theorem and its pole-cover corollary are now proved for arbitrary tree shape:
  a `q`-far matching has size at most `floor(sqrt(2q+1))`, and all `q`-far pairs are covered by twice that many vertices.
  The complementary diameter-cap dichotomy is also OBSERVED: relative to a fixed diameter `(a,b)`, every `q`-far pair can
  be oriented so that each endpoint is either within weighted distance `3q` of the corresponding opposite endpoint or lies
  more than `q` deep in a proper off-diameter component.  This converts the abstract pole cover into the intended
  cap-versus-offshoot geometry.  The top-window connectivity theorem additionally supplies a canonical decreasing-value edge
  order rooted at the diameter.  Finally, for `2q<N`, all `q`-far neighbours of any fixed vertex share a common tree segment
  of length at least `N/2-q`; all incident far edges point into one local branch.  Combined with crowding, the connected
  far-pair graph is dominated by the diameter endpoints and has hop-diameter at most 3.  Thus every new top-window vertex
  enters through one of two diameter stars; there is no long handoff chain.  Proofs: `docs/diameter-endpoint-introduction.md`,
  `docs/diameter-cap-dichotomy.md` and `docs/far-neighbor-cone.md`.  Exhausting the remaining bounded-offset geometry of the
  two stars and their off-diameter common trunks, and forcing a terminal contradiction, remain UNVERIFIED.
- OBSERVED / UNVERIFIED — the central-edge sumset theorem now gives an exact global descent dichotomy.  The metric centre of
  every distinct-distance tree lies strictly inside an edge.  Cutting there produces integer radial-deficit sets `A,B` with
  injective cross sums and `d(x,y)=N-(alpha_x+beta_y)`.  If `D` is the larger within-half diameter and `M=N-D`, a Leech tree
  forces `A+B` to represent `0,...,M-1` exactly once.  Hence for every fixed `C`, either a proper half contains a pair of
  distance at least `N-C`, or `A+B` uniquely tiles the bounded prefix `0,...,C`.  Proof and audit:
  `docs/central-edge-sumset-descent.md`.  Iterating the proper-half case and excluding long tree-realised mixed-radix tilings
  remain UNVERIFIED.
- OBSERVED / UNVERIFIED — equality in the edge-cut containment bound is now rigid.  If deleting any edge of weight `w`
  leaves orders `a,b`, then `w<=N+1-ab`; exact equality forces a unique interval factorization by the two rooted
  distance sets.  An all-length mixed-radix reduction followed by an exact rooted-parent audit leaves only the known orders
  `2,3,4`.  Therefore every hypothetical Leech tree of order at least five satisfies the strict bound `w<=N-ab`.
  Proof and certificate: `docs/heaviest-edge-rigidity.md` and
  `theory-lab/topwindow/verify_heaviest_edge_rigidity.py`.  A uniform all-order lower bound on the positive excess
  `E=N+1-ab-w` that grows with the component orders remains UNVERIFIED.
- OBSERVED / UNVERIFIED — the same rooted-parent classification gives a uniform edge-cut handoff.  The two complete rooted
  distance sets on the sides of a globally distinct-distance tree cannot have unique cross sums covering `0,...,10`.
  Hence for every edge with cut product `ab>=11`, one of `w+1,...,w+10` is realised wholly inside a proper component of
  that cut.  In particular every edge of a target-order tree with sufficiently large cut product carries the same transition.
  Delaying the handoff until 10 is rigid: up to swapping sides, the shallow rooted core has depth sets `{0,1,4,5}` and
  `{0,2,8}`, with compatible edge weights `{1,3,5}` and `{2,8}`.
  Because the theorem applies independently to every edge, no Leech-window inheritance is needed; what remains UNVERIFIED
  is a directional nesting lemma, or a proof that repeated reverse handoffs force a thick branch contradiction.
- OBSERVED / UNVERIFIED — allowing a bounded number of holes gives an exact edgewise excess ladder in the cut product `ab`.
  Complete untruncated enumeration through `E=8` proves heaviest-edge excess at least 3 for orders 25/27, at least 7 for 36/38, and at least 9
  for 49/51.  The largest layer checks 104,249 compatible states and 69,721,840 rooted parent-search states; verifier:
  `theory-lab/topwindow/verify_heaviest_excess_ladder.py`.  The corresponding within-component distances occur by offsets
  22, 40 and 51, and improve the final merge-waste term by at least 24, 69 and 164 respectively.  A uniform asymptotic lower
  bound in `n` remains UNVERIFIED.
- OBSERVED / UNVERIFIED — the edge excesses also obey the exact weighted moment identity
  `sum_e (a_e b_e)E_e=(N+1)W_hop-sum_e(a_e b_e)^2-N(N+1)/2`.  It amplifies holes on balanced cuts and is
  independently checked on all five known witnesses (both checkers) and all 2,105,739 edge rows of the frozen order-18
  topology archive.  A complementary all-order rooted-span bound grows quadratically on unbalanced cuts; together the two
  lower bounds reduce the minimum order-18 moment margin from 27,523 to 12,784 but still kill 0/123,867 topologies, so a
  stronger thick-centre input is required; verifier: `theory-lab/topwindow/verify_edge_excess_moments.py`.
- OBSERVED / UNVERIFIED — orient every edge toward a side carrying its bounded handoff.  For `n>=12` every edge qualifies,
  every leaf edge points inward, and the oriented tree has a nonleaf sink.  At that sink, the complement of every incident
  branch contains a pair within 10 above the incident edge weight; at orders 25/27, 36/38 and 49/51 the guaranteed
  multiplicities are 2, 4 and 5 pairs by offsets 22, 40 and 51.  This reduces the global endgame to a degree-at-least-three
  thick centre or a degree-two bidirectional corridor.  Contracting all bidirectional handoff edges makes this terminal
  canonical.  A singleton degree-two terminal with incident weights `p<q=w_j` further forces either `q-p<=10` or
  `q<=binom(j-1,2)+2`; a nontrivial corridor has two opposite holes by offset 10 on every internal edge.  Proof:
  `docs/edge-handoff-orientation.md`.  Repeating the contraction with a 20-window reduces every nonfragmented singleton
  to 485 affine rows: `q=p+r`, `1<=r<=10`, with the two opposite rooted residual paths both of length at most 20.  All
  485 rows have explicit distance-injective local realisations, so the next filter must use global early-forest coverage
  or the weighted moment rather than another local parent-map test.  The Kruskal covering schedule now supplies that
  interface: if `p=w_i,q=w_j` and the fragmented bound fails, then either `p<=29,q<=39` or `j=i+1`.  An exact all-order
  forced-prefix relaxation reduces the former intersection to 9 rows and 7 forests; all 14 matches have zero right
  residual and extend one of the four known `L3/L4/L6` light cores, each rechecked by both independent checkers.  This is
  an OBSERVED prefix reduction, not yet an exclusion; verifier: `theory-lab/topwindow/verify_corridor_prefix.py`.  The
  consecutive large-rank branch now collapses all-order to `(q-p,delta)=(2,0),(3,0),(3,1)`, where
  `delta=binom(i,2)+1-p`; in a minimal counterexample the zero-defect rows are smaller Leech trees, leaving only a
  connected rooted core with distance set `{1,...,binom(i,2)-1,D}`, `D>=binom(i,2)+21`, and incident weight-1/weight-2
  edges at its root.  A parity square condition restricts its possible orders.  OBSERVED exact forced-prefix runs through
  core order 14 visit 3,690,761,100 terminal states and 162,845 connected cores with zero defect-one cores; this is a
  finite base, not the all-order exclusion.  The OBSERVED endpoint-strip theorem additionally forces both exceptional
  diameter pendant weights to be at least 22, preserves distances `1,...,21` and the rooted weight-1/weight-2 fork after
  deleting the diameter endpoints, and gives an exact three-part tiling of the remaining prefix.  It is an induction
  interface, not yet a decreasing induction.  Proof: `docs/prefix-defect-endpoint-strip.md`; verifier for the finite base:
  `theory-lab/topwindow/verify_prefix_defect_cores.py`.  A more selective OBSERVED order-16 diagnostic now completes all
  512 shards with 39,381,216,516 reported nodes and zero connected or target cores.  Its frozen raw-output hash, complete
  shard-key audit, local clang reproduction of shard zero and orders 8/11/12 regressions are checked by
  `theory-lab/topwindow/verify_prefix_defect_gap.py`; this remains a finite diagnostic, not an all-order induction.  More
  importantly, the OBSERVED full-window
  canonical contraction excludes every singleton degree-two terminal in a smallest `n>=18` counterexample.  A normalized cross-sum count first
  forces `p<=n-2`, then bounds its two outer orders by `a<=n/3` and `b<=n/2`, contradicting `a+b=n-1`.  Thus the only
  degree-two terminal left at that intermediate stage is a nontrivial full-bidirectional path, not a fragmented singleton or an unbounded family
  of isolated prefix-defect cores.  Proof: `docs/edge-handoff-orientation.md`; arithmetic audit:
  `theory-lab/topwindow/verify_full_window_singleton.py`.  In that last path case the globally heaviest edge is forced onto
  the bare corridor, and deleting it gives an exact unique-sum factorization of `0,...,N-q` with precisely the internal
  above-`q` distances removed.  If that heaviest edge is internal, both rooted eccentricities exceed it, so `N>=3q+2`;
  its reflected top prefix plus the separate far endpoint gives `ell*rho>=2q+2`; combining this with the forced quadratic excess makes the bare
  corridor linearly long (asymptotic fraction at least `1-sqrt(3)/2`, approximately `0.134`).  Arithmetic audit:
  `theory-lab/topwindow/verify_full_window_corridor.py`.  In the boundary-heaviest case the outer component count instead
  gives an asymptotic corridor fraction at least `1-sqrt(8/9)`, approximately `0.057`.  Hence both locations reduce to the
  same long-corridor task at this intermediate stage; the reflection-gap theorem below subsequently removes the internal
  location.  Counting the mutually disjoint
  internal distances in both outer components together with the other `c` chain-edge weights sharpens these fractions
  further to `1-1/sqrt(2)` (approximately `0.293`)
  for an internal maximum and `(5-3sqrt(2))/7` (approximately `0.108`) for a boundary maximum.  A multiscale count of all
  low contiguous corridor windows, strengthened by the joint rooted-span bound from the two globally disjoint outer
  distance sets, raises the rigorous internal constant to `329/1000=0.329`; exact target-order relaxation and frozen
  summary: `theory-lab/topwindow/verify_corridor_window_stability.py`.  In the boundary case those windows lie in one
  segment, and the same joint-span count raises its rigorous constant further to `29/250=0.116`; exact rational
  monotonicity and strong-concavity certificates plus the target-order relaxation are audited by
  `theory-lab/topwindow/verify_boundary_corridor_window_stability.py`.  At the top of either case,
  reflecting the two rooted depth sets at their eccentricities gives an exact no-hole unique-sum prefix of length
  `q+min(lambda,mu)` (at least `2q+1` for an internal maximum); reconciling this with the bottom finite-hole factorization
  was the remaining arithmetic interface before the reflection-gap dichotomy below.  In the other direction, the `c+2`
  cumulative positions on the bare chain form a Golomb ruler.  An exact Erdos--Turan difference count, applied after deleting the maximum edge to the
  one or two remaining chain segments, combines with the joint outer rooted span to give
  `c<=((3+sqrt(14))/10+o(1))n`, approximately `0.674n`; hence the two outer components together contain at least
  approximately `0.326n` vertices.  Consequently the corridor maximum also satisfies the uniform quadratic lower bound
  `q>=(0.02654199146...-o(1))n^2`.  This **OBSERVED** upper bound eliminates both the sublinear-outer and `q=o(n^2)`
  escape regimes; audit:
  `theory-lab/topwindow/verify_corridor_golomb_upper.py`.
- OBSERVED negative diagnostic / UNVERIFIED endgame — rooted realizability and a dense reflected top prefix alone do not
  force the missing corridor contradiction.  Two explicit rooted seven-vertex trees have disjoint internal distance
  spectra and injective cross-depth sums, while their reflected factors have 49 unique sums and cover `0,...,36`.
  This is deliberately not a Leech witness: joining the two displayed components at order 14 would require edge weight
  `91-36-64=-9`, and the positive bottom cross-depth sums begin only at 28.  The example therefore refutes only a
  top-density shortcut; a valid argument must retain the positive scale, the maximum-edge path geometry and, in the
  surviving boundary case, the exact bottom-hole/internal-spectrum correspondence in (FW10).  Audit:
  `theory-lab/topwindow/verify_reflected_prefix_barrier.py`.
- OBSERVED — the reflected-prefix gap dichotomy now excludes **every internal location of the maximum corridor edge at
  every order**.  If a unique-sum factor `U` of maximum `lambda` remains visible for `q` coefficients beyond its maximum,
  coefficient-block induction says that `U` is centrally symmetric or has a consecutive gap at least `q+1`.  Along a
  rooted component path all steps are edge weights below the global maximum `q`, so the gap case cannot connect the
  farthest vertex to the root.  In the symmetric case the first edge at the farthest vertex repeats as a root depth,
  contradicting distance uniqueness.  Thus a surviving bare corridor is necessarily boundary-heaviest.  The direct
  audit checks 584,442 oriented prefix factors through length 128 without using the all-order block normal form:
  `theory-lab/topwindow/verify_internal_corridor_reflection.py`.  At the next intermediate stage the degree-two endgame is only the
  boundary-heaviest factorization; its rigorous lower corridor fraction is `0.116` and the common upper fraction is
  approximately `0.674`.  The same dichotomy forces the boundary outer rooted-depth set to be centrally symmetric and
  its farthest vertex to be a root leaf.  An order-one outer side is impossible; an order-two side is the explicit
  `lambda--q` thin cap and forces the other reflected factor to contain `0,...,lambda-1`; every outer side of order at
  least three puts a degree-at-least-three vertex immediately across `q` and satisfies
  `q>=ceil(3lambda/2)+1`.  Hence the boundary problem itself splits into one thin-cap normal form and the common thick
  terminal profile.  The thin cap is now excluded at **every** order `n>=18`.  Its opposite boundary component creates
  a gap in the reflected factor; the exact alternating `lambda`-block pattern forces that component's boundary edge,
  eccentricity and diameter to be `lambda+1,lambda-1,lambda-1`.  The first occupied block then gives `b>=lambda`, while
  its internal distances give `binom(b,2)<=lambda-1`; hence `b=lambda=2`, making the whole tree a path, impossible for
  `n>=5`.  Thus every surviving terminal configuration either already contains a degree-at-least-three vertex or meets
  one immediately across its boundary maximum.  That boundary pole is now classified all-order: its complete
  mixed-radix rooted factor has order at most four, and after removing the thin case it is exactly
  `{0,s,2s}` or `{0,s,G,G+s}` with `G>2s`; in both cases the attachment root has global degree exactly three.
  If the opposite corridor endpoint entered the reflected top prefix, its complete gap would align with a pole digit
  block; the resulting nine finite local cases are all spiders, unrealizable rooted sets or direct distance collisions.
  Therefore every survivor satisfies `p+theta>=q+lambda`, has no corridor vertex in the top prefix, and forces opposite
  outer order at least `ceil((q+2s)/3)` or `ceil((q+G+s)/4)`.  This thick-opposite form is arithmetically fatal:
  `binom(b,2)<=p-1<=q-2` combines with those order bounds to give `q<=13` for the order-three pole and `q<=23` for the
  order-four pole.  The former contradicts `q>=n-1` at `n>=18`; the latter gives `n<=24`, where Taylor leaves only the
  fully certified order-18 exclusion.  Thus **no boundary-maximum corridor survives**, and the canonical sink component
  itself must contain a degree-at-least-three vertex.  Its general thick-centre contradiction remains **UNVERIFIED**.
  Audits:
  `theory-lab/topwindow/verify_boundary_thin_cap.py` and
  `theory-lab/topwindow/verify_boundary_pole_factor.py`,
  `theory-lab/topwindow/verify_boundary_pole_handoff.py`,
  `theory-lab/topwindow/verify_boundary_corridor_exclusion.py`.
- OBSERVED / UNVERIFIED — the first genuine thick case, a singleton canonical sink of degree at least three, now has an
  all-order normal form.  Every outer branch has diameter below its incident weight; hence the largest incident edge `q`
  is globally heaviest, `q>=sum_i binom(b_i,2)+d`, the diameter is the sum of the two largest arm heights, and
  `q>=ceil((N+4)/4)`.  Relative to the `q`-branch, an off-diameter or height-at-least-`q` third arm forces
  `N>=2q+3` and heaviest-edge excess at least three.  Otherwise the third height `h` leaves an exact reflected prefix
  with exact tail `Q=q-h`, because full support gives `mu+h>q`: either `q-h<lambda` (with a nested edge of weight at least `q-h+1` in the
  nonsymmetric case), or the branch is a complete mixed-radix pole of order at most four.  In the pole branch,
  `lambda<=2(n-4)`, `q>=ceil((N-2n+11)/3)` (respectively `q>=87` at order 25), and the third arm lies within
  `4 beta(q)<=4(n-1)` of the smaller diameter arm.  Full support also gives the two-sided thin scale
  `ceil((N-lambda+3)/3)<=q<=floor((2N-2lambda-2)/3)`; a leaf pole sharpens at order 25 to `101<=q<=161`.
  An exact low-spectrum balance `q=sum_i binom(b_i,2)+L_q+1` further gives an exact three-term mass-slack
  identity: unused low cross pairs, holes below the `mu`-arm incident weight, and rooted-eccentricity surplus.
  The distinct internal distances of that arm fit below twice its rooted eccentricity, so the last surplus is
  already quadratic in its order.  Consequently a pole cannot send all but boundedly many vertices into its
  `mu`-arm: the third-and-lower arms contain `(1-sqrt(2/5))n-O(1)` vertices (about `0.3675n`).  This is an
  **OBSERVED** all-order mass reduction, not an exclusion.  Combining the pole height scale with the exact identity
  further forces `max(X,delta,eta)>=n^2/54-O(n)`: every survivor has quadratically many extra low cross pairs,
  incident-spectrum holes, or rooted-eccentricity surplus.  The uniform exact mass-slack floors at
  `n=18,25,27,36,38,49,51` are `8,21,25,53,60,105,116`.  The pole cross-count also gives
  `h>=q+lambda-a(n-a)`, so every pole exposes either the third-height arm's incident edge with quadratic weight,
  or an edge beyond it of weight `n/12-O(1)` (and some lower-arm path edge has weight `n/6-O(1)`).  Splitting
  at `h=q/2` sharpens the finite interface: the short case is impossible for every `n>=48`; below that cutoff it
  makes the centre plus all lower arms a proper distance-injective core of order at least `3n/7-O(1)`, with every
  internal distance below `q`.  Finally the largest exact defect forces either a second, distinct heavy-arm
  interface or a vertex with `n/27-O(1)` extra low-cross neighbours.  In the incident-hole case those low pairs
  lie exactly in the complement of the `mu`-arm, while its high-pair count is the complementary edge excess.
  More strongly, the `mu`-arm incident edge is unconditionally at least
  `ceil((N-lambda+5)/6)=n^2/12-O(n)` and satisfies `4t>=q+4`; hence every pole has heavy interfaces in two
  different non-`q` arms.  In fact (FW48) makes the third-height arm stronger than the earlier path-average
  formulation: its *incident* edge is unconditionally `n^2/12-O(n)`, so no internal linear-edge fallback exists.
  A top-height layer count then forces more than
  `(sqrt(17/30)-sqrt(2/5))n-O(1)>0.12031n-O(1)` third-and-lower vertices to lie behind incident edges of weight
  `n^2/24-O(n)`.  The same layer argument absorbs the thick-third branch: every singleton thick terminal has
  `n/sqrt(6)-O(1)` vertices behind quadratic incident interfaces.  This is an OBSERVED thin/thick accumulation
  lemma, not yet a collision.  At every nonsymmetric reflected handoff, the exact-prefix gap now has a safe
  **OBSERVED** interpretation: an internal edge of the receiving arm either cuts off a proper component whose
  diameter is below that edge, or belongs to a nontrivial full-bidirectional edge-component contained in the arm.
  In the latter case, the first boundary edge of that component toward the centre is still heavier and cuts off a
  proper thin cap; this cap may be the whole receiving arm.  Thus singleton descent feeds directly into the
  thin-cap/non-singleton-core dichotomy.  This heavy closure need not shrink the receiving arm, and the core itself
  is not yet excluded.  Taking instead the first non-bidirectional boundary toward the farthest diameter
  endpoint gives a strict smaller cap.  Across that cap the reflected top prefix is exact again: either its rooted
  factor has order at most four, the next cap has strictly smaller order and boundary weight, or the complementary
  rooted tree has diameter surplus at least the cap boundary.  In the last case that complement contains both a
  new near-diameter pair whose deficit is strictly below the cap boundary and an off-diameter component at least
  that deep; four-point rigidity forces this pair to retain the old diameter endpoint and pivot only its other end.
  The three resulting tip heights have the exact affine form `k+r,k+q',k`, with `q'` below the old boundary;
  full-support orientation then forces the bidirectional component at their gate to be a canonical thick sink unless
  the `x`-ray contains a boundary edge above `2k+q'`.  Such an escape is possible only when `r>=n-1`, and its edge lies
  on the global diameter with deficit at least `n-2`.  Thus every `r<=n-2` pivot is now absorbed by the thick sink;
  in the original pole, the escape gate and new tip are moreover forced to remain inside the same `mu`-arm, with
  internal tip distance below `t`, short height `k<t/2`, and `r>=N-t+1`.  This explicit rooted-arm tail remains
  an **OBSERVED** reduction.  More exactly, every receiving-arm vertex whose reflected depth from the far endpoint
  is below `q'` lies inside the strict cap, while the pivot tip is the unique outside vertex at reflected depth
  exactly `q'`.  An absolute bound on this weighted endpoint strip, and hence exclusion of the tail, remains
  **UNVERIFIED**.  The original `t`-cut prefix also migrates exactly to the strict cap: it represents every deficit
  below `q'` once and first misses `q'`.  This yields an exact split.  Either the cap and one of the four order-at-most-four
  pole factors tile that prefix, forcing `q'<=4|C_z|`, or the third-and-lower-arm spectrum enters before the first hole;
  equality at the interface would repeat the pivot distance and is impossible.  This is an **OBSERVED** bridge between
  the inherited-cap and lower-core routes.  The second route actually forces `h>q/2` and returns to the established
  tall-third-arm heavy-edge handoff.  In the first route, cap-internal distance counting gives
  `q'<=a floor((1+sqrt(4t-15))/2)` with `a<=4`; if the cap is also a small terminal then `q'<=16`.
  Its coefficients below `q'` are now forced into four explicit mixed-radix digit strips, with `q'` a single deletion
  from the next cap-owned block.  The recurrence is independently replayed in 177 parameter rows by
  `theory-lab/topwindow/verify_endpoint_pole_first_hole.py`.  Comparing with the original three-arm cluster additionally
  gives `q'<min(H,mu)-h<=a beta(q)<=4(n-1)`, so the unknown deficit is now linear in order as well as square-root in `t`;
  moreover the entire receiving-arm band through `gamma-1`, for `gamma=min(H,mu)-h`, not merely the part below `q'`, has the same exact
  digit layers and satisfies `gamma<=a floor((1+sqrt(8t-7))/2)`.  An additional **OBSERVED** chain-pair count now
  shows that this band contains at least `gamma/(2a^2+a)>=gamma/36` rooted leaves.  Its induced rooted forest
  has at least `gamma/(4a^2+a)>=gamma/68` separate components and hence that many distinct terminal-subtree
  entrances (counting the attachment edge for the possible root component).  This is the requested all-order
  branch/hair accumulation inside the endpoint window.  Every such entrance either cuts out a proper thin cap or
  is a full-support bidirectional edge: consequently there are at least `gamma/136` pairwise disjoint thin caps,
  or the union of nontrivial full-bidirectional cores contains at least `gamma/136` entry edges.  This is an
  **OBSERVED** multiplicity bridge, but the window is not yet absolutely bounded and neither multiplicity has yet
  been converted into a distance collision.  On the bidirectional side, a branch-free maximal core is a path and
  can cross the band threshold at most twice; hence either one such core already contains a global branch vertex,
  or at least `gamma/272` different nontrivial bidirectional path cores occur.  Those cores are not yet proved to
  be complete canonical corridor sinks.  Finally, an **OBSERVED conditional fixed-window theorem** now shows that
  if the whole tree has at most `K` global branch vertices, then this endpoint terminal has
  `gamma<=64K+32`, independently of `n`; retaining the pole order gives `gamma<=224` for at most three branch
  vertices.  Conversely an unbounded window forces at least `gamma/64-O(1)` global branch vertices.  These statements apply inside
  the singleton-pole endpoint normal form, not to arbitrary rooted regions.  More sharply, the component roots
  and the cross-component pairs force `gamma/64-O(1)` connector branch vertices strictly outside the band, so the receiving arm
  must pay `b>=ceil(gamma/a)+gamma/64-O(1)` in disjoint band and branching-buffer mass.
  The ceiling arithmetic, including the whole-tree `K=3` caps `14,56,126,224`, is independently replayed by
  `theory-lab/topwindow/verify_endpoint_branch_capacity.py`; its frozen output is
  `theory-lab/topwindow/results/endpoint_branch_capacity_certificate.json`.  This finite replay is **OBSERVED** support for the
  constants, not a substitute for the all-order LCA proof in `docs/edge-handoff-orientation.md`.
  In that class the receiving arm itself has only `2,2,1,1` branch LCAs available at pole orders `1,2,3,4`: the singleton
  centre already uses one global branch vertex, and the order-3/4 pole root uses another.  The endpoint caps therefore
  sharpen to `10,40,54,96`.  They give an **OBSERVED finite local catalogue**: 10,597 truncated pole/mask rows reduce under
  the exact LCA capacity to 3,245, and their sharp first holes give 42,697 states with a frozen survivor hash.  Verifier:
  `theory-lab/topwindow/verify_endpoint_threebranch_catalogue.py`; certificate:
  `theory-lab/topwindow/results/endpoint_threebranch_catalogue_certificate.json`.  For pole orders three and four the
  receiving arm has at most one branch vertex, so a clean-room canonical ray-partition filter checks every possible
  band-internal topology.  It reduces 2,828 masks to 109 (maximum surviving `gamma` 13 and 20), and their 38,028
  sharp-hole states to 281.  For pole orders one and two, two receiving-arm branch vertices must be comparable, giving a
  nested two-splitter skeleton.  Its canonical topology filter reduces the other 417 masks to 64 and their 4,669 sharp-hole
  states to 238.  Thus the complete exact-three-branch endpoint catalogue now has only 173 masks and 519 sharp-hole states,
  with `gamma<=20`.  Since every genuine sharp hole has `q'<gamma`, this gives the conditional all-order fixed bound
  `q'<=19` for an exactly-three-branch singleton-pole endpoint terminal.  The pivot gate is then one of the three branch
  centres.  For pole orders three and four it is an end centre with two pendant legs whose lengths differ by `q'`, so the
  complete-tree anchor is `AC`; pole orders one and two reduce to the `AB/AC` classes, never `AA/BB`.  This **OBSERVED
  connector reduction and necessary topology filter** is reproduced by
  `theory-lab/topwindow/verify_endpoint_onebranch_topology.py` and its frozen certificate
  `theory-lab/topwindow/results/endpoint_onebranch_topology_certificate.json`, together with
  `theory-lab/topwindow/verify_endpoint_twobranch_topology.py` and its frozen certificate.  The one-branch results also
  agree with an optional independent Z3 diagnostic; the two-branch DFS agrees with an independent exhaustive reference on
  726 small splitter configurations.  In the high-pole `a=3,4` rows, the strict cap lies on the pendant `b`--`z` leg.
  Its pairwise deficit differences must be distinct and must avoid the fixed pole distances.  Combining this with the
  sharp-hole digit rule reduces the end-leg imbalance further to the **OBSERVED conditional all-order alphabets**
  `{1,2,3,6}` for `a=3` and `{1,2,4,5,8}` for `a=4`.  The 1,083-row tail-complete replay is
  `theory-lab/topwindow/verify_endpoint_pole_deficit_alphabet.py`, with frozen certificate in the adjacent `results/`
  directory.  For `a=4`, the connector lengths, pole tails and ray assignments can be retained symbolically while the
  triangular order equation and vertex budget are dropped.  The complete outside-band/common-trunk split has 418 relaxed
  integer-metric classes (284 outside and 134 branch-in-band), of which 27 have feasible planted metrics.  No seed saturates
  the top twenty distances.  Exactly one branch-in-band seed admits the first missing diameter-endpoint child; after adding
  it, neither top-eighty saturation nor a legal second child is possible.  This gives an **OBSERVED conditional all-order
  exclusion** of the complete order-four high-pole `AC` endpoint terminal.  Verifier:
  `theory-lab/topwindow/verify_endpoint_ep4_symbolic.py`; frozen full and outside-subterminal certificates:
  `theory-lab/topwindow/results/endpoint_ep4_symbolic_certificate.json` and
  `theory-lab/topwindow/results/endpoint_ep4_outside_symbolic_certificate.json`.  A separate exact C regression at orders 11
  and 18, including eight-shard recombination, is in `theory-lab/threebranch/threebranch_endpoint_exact.c` and
  `theory-lab/threebranch/verify_endpoint_exact.py`.  It is finite outside-band corroboration, not the all-order proof.
  The analogous `a=3` model has 218 outside-band/common-trunk classes (164+54), with 18 feasible planted metrics.  Successive
  top-window/diameter-introduction stages leave 10, 6 and 2 legal children; after the third child neither top-160 saturation
  nor a fourth child is possible, with zero solver unknowns.  This is an independently audited **OBSERVED conditional
  all-order exclusion** of the complete order-three high-pole `AC` endpoint terminal.  Full verifier and certificate:
  `theory-lab/topwindow/verify_endpoint_ep3_symbolic.py` and
  `theory-lab/topwindow/results/endpoint_ep3_symbolic_certificate.json`; Z3 4.15.4 replays all 218 classes on `geo-ws`, and
  Z3 4.16.0 agrees on the final two.  Thus both high-pole rows are closed.  In the low-pole rows, the additional exact
  split `mu<=H` versus `mu>H` closes the first half.  When `mu<=H`, the receiving eccentricity satisfies
  `theta<gamma`, so the FW108 band is the complete receiving arm.  Exact one/nested-two-splitter enumeration leaves no
  order-one state and only 13 order-two parameter states, comprising 29 canonical ray metrics.  All have the pivot as
  the attachment root.  In 19 metrics it is the only receiving-arm branch centre, so the third centre is in the lower
  part; its two possible placements relative to a height-`h` vertex give 38 symbolic seeds.  Four collide immediately,
  none of the other 34 saturates the top twenty values, and none admits the new vertex forced at its greatest missing
  value by diameter-endpoint introduction.  A direct-metric reference independently splits that last step into 136
  location queries, all infeasible.  In the other ten metrics the third centre lies below the pivot on one ray.  One
  seed collides; the other nine neither saturate the top twenty nor admit any of the 18 same-leg/new-leg introductions.
  A second direct-metric replay agrees exactly.  Z3 4.15.4 and 4.16.0 agree throughout with zero `unknown`.  Because the relaxation keeps only `N>=153`
  and drops the triangular-order equation and vertex budget, this is an **OBSERVED conditional all-order exclusion** of
  every `a=1,2`, `mu<=H` endpoint.  Verifiers and frozen certificates:
  `theory-lab/topwindow/verify_endpoint_lowpole_small_radius.py`,
  `theory-lab/topwindow/verify_endpoint_lowpole_small_radius_symbolic.py`, and
  `theory-lab/topwindow/verify_endpoint_lowpole_small_radius_reference.py`, together with the adjacent
  `verify_endpoint_lowpole_small_radius_upper_symbolic.py` and `_upper_reference.py`.  In the complementary `mu>H`
  branch, `h=q+lambda-gamma<t<q` gives the exact integer bound
  `1<=q-t<=gamma-lambda-1`.  Replaying all surviving digit/topology states sharpens this to `q-t<=5` at pole order one
  and `q-t<=10` at pole order two; the latter retains 48 of 59 masks and 193 of 223 sharp holes.  This **OBSERVED
  conditional all-order fixed-cluster reduction** is frozen by
  `theory-lab/topwindow/verify_endpoint_lowpole_high_gap.py` and its certificate.  Excluding the clustered `mu>H`
  endpoint remains **UNVERIFIED**.  At pole order one the cluster nevertheless has an exact doubled top block: the
  FW108 vertices of deficits `0,...,gamma-1`, paired first with the `q`-leaf and then with a lower height-`q-gamma`
  vertex, realise all deficits `0,...,2gamma-1`.  The remaining diameter-arm height difference must satisfy
  `mu-q>=gamma`, or the lower-height pair collides with the band translate.  This is an **OBSERVED conditional
  all-order top-block extension**, not the missing exclusion; consequently this is not yet an all-order
  three-branch theorem.  More generally, pairing every controlled receiving-band vertex with both the pole and a
  lower height vertex makes `S_gamma+(P union {gamma})` a direct sum.  At pole order two this is possible only when
  `gamma` is a multiple of `2lambda`; it removes 35 of the 48 remaining masks and 150 of 193 sharp holes, leaving 13
  masks and 43 holes.  Their direct cross-pair block covers every deficit through `gamma+lambda-1`, and the diameter-arm
  separation satisfies `mu-H>=gamma-lambda>q-t` (at order one, `mu-q>=gamma>q-t`).  This is an **OBSERVED conditional
  all-order factor-collision reduction**, replayed by
  `theory-lab/topwindow/verify_endpoint_lowpole_factor_collision.py` and its frozen certificate; it is not yet an
  exclusion of the surviving cluster.  The same direct-sum argument gives an exact two-sided empty layer: below the
  direct block's first absent coefficient, the `B` side contains only the controlled band and the complement contains only the
  pole plus the unique height-`h` vertex.  Hence the attachment-root deficit satisfies `theta>=2gamma` at order one
  and `theta>=gamma+lambda` at order two.  Equivalently,
  `mu-H>=2gamma-(q-t)` in the first row and `mu-H>=gamma-(q-t)` in the second.  At order one, root-pair directness also
  forces `theta<h` and `mu-h<t`.  These are **OBSERVED conditional all-order** consequences, not the missing
  endpoint exclusion.  Applying the exact `t`-cut coefficient dichotomy then removes the symmetric terminal at both
  pole orders.  FW144 leaves one order-one tail and two order-two tails among all FW76 small-pole forms; each has two
  different pairs of the same symbolic deficit `G+gamma`.  Hence every order-one/two `mu>H` endpoint strictly hands
  to an edge wholly inside `B` of weight at least `t-h+1`.  This **OBSERVED conditional all-order handoff** is replayed
  by `theory-lab/topwindow/verify_endpoint_lowpole_symmetric.py`; it still requires the global descent to absorb the
  proper-arm output.  Together with the order-three/four endpoint exclusions and the order-one/two `mu<=H` exclusion,
  this exhausts the exactly-three-branch singleton-pole endpoint: it is now either contradictory or returns to the
  FW85 internal-`B` handoff.  This is an **OBSERVED conditional all-order endpoint return theorem**, not the global
  three-branch theorem.  The FW77 two-small-factor output is no longer unbounded when the whole tree has
  at most three branch vertices: exact factorisation of every distance above `2h`, followed by the lower-band LCA
  capacity bound, leaves 66 ordered truncated pole-factor rows, bounds the difference of the two top/lower interfaces
  by 175, and gives `N-2h<=178`.  This is an **OBSERVED conditional all-order top-178 fixed-window theorem**, replayed
  by `theory-lab/topwindow/verify_endpoint_two_small_factor_window.py`; it is not yet an exclusion of the fixed
  catalogue.  Inside that box the full high spectrum determines the lower reflected band one coefficient at a time.
  Of 1,312,528 relaxed complete-pole parameter rows, 1,973 survive the exact binary recursion and 1,199 survive the
  whole-band LCA capacity test; every survivor has first interface at most 3, longer interface at most 112,
  `N-2h<=113` and at most 33 forced lower-band vertices.  This **OBSERVED conditional exact-high-spectrum reduction**
  is replayed by `theory-lab/topwindow/verify_endpoint_two_small_factor_spectrum.py`; the 1,199 rows are necessary
  parameter states, not witnesses.  When both pole orders are at least three, their roots leave `v` as the only
  lower-core branch vertex.  Exhaustive unlabeled-ray partitioning rejects all 25 such rows (23 band-internally and
  the last two against planted top-pole distances), leaving 1,174 rows with at least one order-one/two factor.  This
  **OBSERVED conditional subcase exclusion** is replayed by
  `theory-lab/topwindow/verify_endpoint_two_small_factor_root_topology.py`.  When exactly one pole has order at least
  three, only `v` and one additional lower splitter remain available.  The exhaustive relaxed one/nested-two-splitter
  topology filter reduces its 740 FW149 rows to 61.  Continuing the exact coefficient recursion through the first
  `T` distances at and below `2h` then reduces those 740 rows to exactly three planted affine rows; the certificate
  records all three explicitly.  These are independently audited **OBSERVED conditional all-order necessary-state
  reductions**.  A further exact continuation now assigns every newly forced prefix vertex to the one-splitter
  ray geometry and checks all represented pair distances; a separate branch inserts the splitter and its shared
  trunk explicitly if it becomes visible inside the prefix.  The three rows have empty frontiers after respectively
  33, 25 and 19 coefficients (maximum deficits 36, 33 and 24).  A three-regime height-stability argument maps every
  `h>=259` state to the replay height, so this is an independently audited **OBSERVED conditional all-order K=2
  subcase exclusion**, not merely a finite-order computation.  Replays:
  `theory-lab/topwindow/verify_endpoint_two_small_factor_nested_topology.py` and
  `theory-lab/topwindow/verify_endpoint_two_small_factor_boundary_continuation.py`, followed by the independent
  enumerator `theory-lab/topwindow/verify_endpoint_k2_prefix_pairs.py` and diagnostic SMT cross-check
  `theory-lab/topwindow/probe_endpoint_k2_tail_smt.py`.  The thick-surplus output, the both-small-factor `K=3` rows
  and the separate lower-core handoffs remain open.  For `K=3`, a
  topology-free LCA/ancestor-difference matching reduces 434 rows to 111; allowing every later internal
  `2h-k` pair count to be an independent free bit and continuing through the full first `T` block reduces those to
  61 rows.  These independently audited **OBSERVED conditional necessary-state reductions** are replayed by
  `theory-lab/topwindow/verify_endpoint_two_small_factor_lca_matching.py` and
  `theory-lab/topwindow/verify_endpoint_two_small_factor_free_internal_continuation.py`.  Coherent LCA-layer matching
  then forces all first-`T` internal bits to arise from the same at most three branch depths.  Its exact
  pair-resource replay rejects 9,197 of 12,514 relaxed extensions and reduces the 61 `K=3` rows to 34, by pole-order
  counts `9,1,23,1`; see `theory-lab/topwindow/verify_endpoint_two_small_factor_lca_layers.py`.  This is another
  **OBSERVED conditional necessary-state reduction**: deep LCA translates and the rooted hierarchy are still
  relaxed.  An exhaustive rooted-hierarchy placement then closes three complete `K=3` rows: the two singleton-factor
  rows with outer/receiving gaps `(9,1)` and `(10,1)`, and the `([0,6],[0])` row with gaps `(18,1)`.  All seven of
  their extensions finish below 74,935 states, with no cap hit; the root/one-splitter/chain/fork location predicates
  also agree with an explicit 300-case token-path audit.  This **OBSERVED conditional three-row exclusion** is
  replayed by `theory-lab/topwindow/verify_endpoint_two_small_factor_root_hierarchy.py`.  At that intermediate stage
  this terminal had 8 relaxed affine `K=3` rows, none a witness: the three former `K=2` rows are excluded by FW195, the
  first post-FW164 `K=3` row `P=U={0}, Q=2, R=1` is excluded by FW198, and seven further rows are excluded by
  the independently audited 13,874-configuration FW199 replay.  Four more expensive rows are excluded by the
  sharded 7,928-configuration FW200 replay, and eleven more by the 21,802-configuration FW201 replay.  A final mixed
  `H=40/50` replay partitions 30,346 configurations into 7,079 exact shards and excludes the last eight rows, with
  no frontier, unknown or cap hit and maximum one-layer state count 5,246.  Its row-specific three-regime height
  audit is stable for every `h>=259`.  Thus all 31 `K=3` rows are excluded; combined with FW195, this is an
  independently audited **OBSERVED conditional all-order exclusion of the present at-most-three-global-branch
  two-small-factor affine terminal**, not the global theorem.  Replay:
  `theory-lab/topwindow/verify_endpoint_k3_final_mixed_rows.py`.  The earlier
  affine terminal is not being reused as a proxy for the remaining thick cases.  Independently, every edge `q` on
  the unique global-diameter path now has an **OBSERVED all-order diameter-edge prefix/fork interface**: after
  orienting toward the side of larger internal diameter `D`, either the opposite rooted side is one of the FW76
  order-at-most-four poles, that proper side contains a path edge of weight at least `q+lambda-D+1`, or the dominant
  side contains a genuine branch vertex with two edge-disjoint tails of weight at least `q+ell` and
  `D>=2q+2ell+1`.  The exact reflected prefix and integer inequalities are independently replayed by
  `theory-lab/topwindow/verify_diameter_edge_prefix_fork.py`, with all five known witnesses passing both checkers.
  This is a routing theorem, not a thick--thick exclusion or global descent; absorbing the proper-side edge and
  double-deep fork outputs remains **UNVERIFIED**.  Applying the prefix lemma to both factors before accepting the
  fork strengthens its central-edge form.  The fully blocked fork has internal diameter `D>N/2`; with
  `C=N-D`, it either gives a genuinely `C`-deep off-diameter endpoint, or it forces `C>N/4`, `D<3N/4` and central
  cut product greater than `N/4`.  Hence both central sides then have at least
  `(n-sqrt(n(n+1)/2))/2=((1-1/sqrt(2))/2)n-O(1)` vertices.  This independently audited **OBSERVED all-order
  central offshoot/balanced-cut dichotomy** is replayed by
  `theory-lab/topwindow/verify_central_edge_prefix_offshoot.py`.  It routes arbitrary thick--thick geometry to an
  existing deep-offshoot terminal or a macroscopic balanced cut; neither output is yet excluded, so the global
  absorption remains **UNVERIFIED**.  The proper-side gap line now has its missing well-founded continuation:
  because every such gap edge lies strictly in one open half of the fixed global diameter, its centre side has full
  support.  Crossing the maximal bidirectional run toward the endpoint closes a thin diameter cap; every subsequent
  nonsymmetric prefix step strictly decreases cap order, while a nonpositive tail gives a deep offshoot whose deficit
  is strictly smaller than the cap boundary.  Thus the independently audited **OBSERVED all-order central-gap cap
  descent** terminates at an FW76 order-at-most-four cap or the existing deep-offshoot terminal, without assuming the
  cap is Leech; replay: `theory-lab/topwindow/verify_central_gap_cap_descent.py`.  This absorbs the gap output but does
  not exclude its two terminals or, by itself, the FW204 balanced cut.  In the fully blocked
  balanced branch, the first absent cross coefficient is exactly `C=N-D`: the internal `D`-pair has already occupied
  that distance.  If `m,k` count the two reflected factors below `C`, exact prefix coverage gives `mk>=C`, while
  both factors have an additional element above `C`.  Hence `C<=floor((n-2)^2/4)`,
  `D>=N-floor((n-2)^2/4)`, `m+k>=tau(C)>sqrt(N)`, and each central side has a distinct diameter-path edge crossing
  the missing level `C`, of weight at least two.  This independently audited **OBSERVED all-order central
  first-hole mass/shell bound** is replayed by `theory-lab/topwindow/verify_central_first_hole_mass.py`; `m+k` is a
  factor-vertex count, not an edge count, so this bound alone is not a balanced-cut contradiction.  The proof of
  FW205 in fact needs only a fixed-diameter edge strictly inside an open metric half, not an initial gap lower bound.
  Moreover the level-`C` shell exists in every fully blocked state, including FW204's generic `h>=C+1` offshoot:
  the internal `D=N-C` pair makes cross coefficient `C` zero, so both reflected factor maxima are strictly above
  `C`.  Applying FW207a at that open-half shell supplies the missing cap provenance.  Thus the previously implicit
  handoff is now an **OBSERVED all-order absorption of the generic C-deep output**, not an invocation of FW208 on a
  cap-free offshoot.
  Starting it at either FW206 level-`C` shell preserves endpoint radius `alpha<C`; finite cap-order descent therefore
  ends at an FW76 cap of order at most four or, by FW92--FW93, at a deep offshoot whose new deficit satisfies
  `q'<=alpha<C`.  This independently audited **OBSERVED all-order central-shell cap descent** is replayed by
  `theory-lab/topwindow/verify_central_shell_cap_descent.py`.  The balanced cut is consequently no longer an
  independent terminal.  The deep line has a further strict first-hole recurrence: its exact remainder cannot be
  zero, since the cap-root/opposite-endpoint cross pair would repeat the complement's internal diameter.  Thus its
  positive deficit satisfies `q'<alpha`; the cap contains a new level-`q'` shell, and another FW207 step either ends
  at an order-at-most-four pole or returns `1<=q''<q'`.  Positive-integer induction gives an independently audited
  **OBSERVED all-order deep-offshoot deficit descent** to a nested small cap; replay:
  `theory-lab/topwindow/verify_deep_offshoot_deficit_descent.py`.  This preserves rather than excludes the original
  pivot history.  The remaining **UNVERIFIED** object is a contextual order-at-most-four cap with that inherited
  history, not a free-standing assertion that small caps cannot occur.  That object now has an independently audited
  **OBSERVED all-order terminal-cap digit/pivot normal form**.  Its first-hole deficit `q_0=N-diam(D)` is at most
  `a(n-a)<=4(n-1)`; its complement band is exactly one of the four FW105 canonical mixed-radix indicators, with
  `chi_P(q_0)=1`; and the complement diameter keeps the old opposite global endpoint, giving
  `N=2k+r_0+q_0`, `r_0>=1`, `r_0!=q_0`.  Replay:
  `theory-lab/topwindow/verify_terminal_cap_digit_pivot.py`.  The first-hole count is now sharpened to
  `q_0<=a(n-a-1)<=4(n-5)`, and its missing level can be followed toward the opposite endpoint without making the
  invalid inference that every level below `N/2` lies in an open-half edge.  An explicit central-edge split through
  FW203--FW208 produces a disjoint opposite terminal cap `K`, of order at most four and radius below `q_0`.  If its
  first hole is `Q`, then `q_0!=Q` and every distance in the common top prefix crosses both cap cuts, so
  `min(q_0,Q)<=|J||K|<=16`.  In the nonreversal branch `q_0<Q`, both full FW76 factors are visible: 19 oriented
  mixed-radix rectangles reduce, after eight cap-internal collisions, to exactly 11 oriented rows with
  `q_0 in {1,2,3,4,6,8}`.  This independently audited **OBSERVED all-order opposite-cap overlap reduction** is
  replayed by `theory-lab/topwindow/verify_terminal_cap_opposite_overlap.py`.  The strict reversal `Q<q_0` is now
  **OBSERVED all-order absorbed**: reorienting at the smaller hole cuts either the old FW76 cap or its endpoint
  singleton, and at most one further endpoint cut reaches one of the same eleven nonreversal rows (FW212).  The
  endpoint-peeling identity is exact, and the constant-memory replay is
  `theory-lab/topwindow/verify_terminal_cap_reversal_absorption.py`.  Thus the reversal is no longer a separate
  output, although the contextual outer wrapper is not erased.  In the eleven nonreversal rows, the opposite
  complement is further identified **OBSERVED all-order** as the exact periodic radial lattice `P+q_0 Z_>=0`.
  Its capacity defect splits as
  `b(n-b-1)-Q=bu+delta`, where `u` is the number of unseen complement vertices besides the root and
  `0<=delta<=2`; its proper-complement excess is `C(b+1,2)+bu+delta`.  The first complete lattice blocks force
  rooted detour mass `a^4t^4/16-O(t^3)`, so bounded defect gives an order-`n-O(1)` core with
  `n^4/16-O(n^3)` radial detour.  Replay:
  `theory-lab/topwindow/verify_terminal_cap_periodic_lattice.py`.  The matching **OBSERVED all-order** LCA count
  (FW213) is global but gives a branch-rich alternative: if `B` is the number of global branch vertices, then
  `B>=1_{b>=3}+ceil([C(at,2)-D]_+/(2D-1))>at/(4b)-1`.  Thus a near-saturated periodic core forces
  `B>=n/16-O(1)`.  Under the additional, explicitly conditional hypothesis `B<=3`, the eleven exact inequalities
  sharpen to `t<=29`, at most 39 visible complement vertices, `Q<=154`, and `u>=n-44`; FW203--FW212 do not supply
  that hypothesis.  Replay: `theory-lab/topwindow/verify_terminal_cap_lattice_lca_bound.py`.  The
  **OBSERVED all-order visible/unseen LCA balance** (FW214), which needs no branch-count hypothesis, further gives
  `C(at,2)<=2(Q-1)+(u+1)(2D-1)`, hence `at<=4b(u+3)`,
  `u>=ceil((n-56)/17)`, and capacity defect `bu+delta>=ceil((n-56)/17)`.  Combining FW213/FW214 gives
  `16B+u>n-24`.  Replay: `theory-lab/topwindow/verify_terminal_cap_visible_unseen_balance.py`.  Thus the near-full
  periodic core is globally impossible at unbounded order.  Its high-coordinate part now has an independently
  audited **OBSERVED all-order heavy-spine alternative** (FW215): at a high LCA branch, the heavy child sheds at most
  `8b-1<=31` marked periodic vertices while at least half of the periodic lattice remains; a visible descendant cannot
  retain half once the lattice has order 80.  Hence `H>s/[2(8b-1)]`, and for `n>=160` either
  `u>=n/2-8` or the hop diameter is greater than `n/124`.  Replay:
  `theory-lab/topwindow/verify_terminal_cap_unseen_spine.py`.  This routes the remainder to a half-order unseen part
  or a linear bounded-shedding spine.  The latter now has an independently audited **OBSERVED all-order quadratic-span
  refinement** (FW216): its disjoint shed--retained pair families number at least
  `ceil(3s^2/8-(8b-1)s/4-(8b-1)^2/2)`, forcing
  `beta-Q>=ceil((C_sp-1)/2)-D=3s^2/16-O(bs)`.  Replay:
  `theory-lab/topwindow/verify_terminal_cap_spine_span.py`.  This is still compatible with the global quadratic
  diameter scale; the pendant bundles require a translate collision, a smaller span upper bound, or a decreasing
  transfer.  It is not yet a proper-core induction or the global exclusion.
  Taylor condition additionally gives an **OBSERVED all-order parity routing** (FW217) for four monochromatic periodic
  rows: all visible lattice vertices occupy one Taylor class, hence
  `u>=(n-k)/2-a-b>=(n-k)/2-6`, where `n=k^2` or `k^2+2`.  Replay:
  `theory-lab/topwindow/verify_terminal_cap_parity_routing.py`.  This sends those four rows asymptotically to a
  half-order unseen core, which remains unclassified.  A second independent Max direction review then exposed a
  shorter global entry that bypasses the other ten rows without excluding them.  If `x,z` are the global diameter
  endpoints, orient `z` to be absent from the unique distance-`N-1` pair.  Then `diam(T-z)=N-1`, the four-point
  identity forces that pair to contain `x`, and the endpoint gate gives `N=2k+r_0+1` with `r_0>=2`.  Thus the
  singleton `{z}` directly re-proves the FW209a--e/FW210 analytic package with first hole `q_0=1`; FW210's opposite
  terminal has radius below one and is the singleton `{x}`.  Hence every Leech tree of order `n>=3` lies in the
  unique FW210 rectangle `(1,{0},{0})`.  The only root-hit exceptions occur at `n<=4`; for every `n>=5`, and
  therefore every hypothetical G18 counterexample, the opposite root lies above its first hole and the full FW211
  `q=1` normal form applies.  This independently replayed **OBSERVED all-order universal endpoint-one singleton
  extension** is FW218; all five known witnesses pass both checkers, the four `n>=3` witnesses have endpoint deficit
  one, and L2 is the explicit `n=2` exception.  Replay:
  `theory-lab/topwindow/verify_universal_endpoint_one.py`.  FW218 is not the global exclusion: classification,
  collision or a decreasing transfer for the `q=1` unseen core remains **UNVERIFIED**.  The new
  **OBSERVED all-order exact q=1 threshold-core theorem** (FW219) now identifies that remainder precisely.  In
  `T-x`, reflected coordinates `0,...,Q-1` occur once, `Q` is absent, and the `u+1` vertices above `Q` form an
  ancestor-closed connected induced proper core `H_Q`.  Its vertices are in exact bijection with all holes of the
  internal spectrum:
  `Spec(T-x)=[1,N-Q] minus {d(x,v):v in H_Q}`.  The visible band is a pendant forest with component orders `s_i`
  satisfying `sum C(s_i,2)<=2Q-3`, at least `ceil(Q^2/(5Q-6))` components, and maximum component order at most
  `floor((1+sqrt(16Q-23))/2)`.  Different child branches at every LCA obey the exact cross-Sidon relation
  `Delta(A) intersect Delta(B)={0}`.  The q=1 balances sharpen to
  `n=Q+u+2`, `Q<=4u+7`, `u>=ceil((n-9)/5)`, and `4B+u>=n-4`.  Replay:
  `theory-lab/topwindow/verify_q1_threshold_core.py`.  This is not bounded-defect inheritance: there are exactly
  `u+1` holes, and a collision, finite return catalogue or decreasing contextual transfer remains **UNVERIFIED**.
  The proposed shortcut `sum_i(e_i-1)=O(1)` is now rejected at the level of the existing constraints by an
  **OBSERVED negative diagnostic**.  Repeatedly shedding the two endpoints of the current q=1 interval preserves
  cross-Sidon, keeps every FW216 modeled family distance distinct inside the quadratic `N` budget, and gives
  `sum_i(e_i-1)=floor(Q/4)`.  This abstract double peel is not a tree witness and leaves unmodeled pair classes
  unspecified; it shows only that A-prime needs genuinely new tree-realisation input and cannot be inferred from
  FW219/FW216 alone.  Replay: `theory-lab/topwindow/probe_q1_cross_sidon_double_peel.py`.
  The active boundary route has an independently replayed **OBSERVED all-order coordinate-zero smaller-cap bridge**
  (FW220).  For `Q>=4`, the visible component `W_0` containing coordinate zero has a first surviving top coefficient
  `q_*` with
  `1<=q_*<=|W_0|<=floor((1+sqrt(16Q-23))/2)<Q`.  Its entry is either already thin, or its first endpointward exit
  from the maximal bidirectional region cuts a nested open-half dominant thin cap with no larger first hole.  A
  direct thin entry is either open-half dominant or the central-thin branch.  Replay:
  `theory-lab/topwindow/verify_q1_coordinate_zero_cap.py`.  This gives a genuine local decrease `Q -> q_*`; although
  subsequent cap normalisation can return to the original endpoint-one side, the possible returns are no longer
  arbitrary.  The independently replayed **OBSERVED all-order q=1 small-return catalogue** (FW221) shows
  that normalising the FW220 cap stays inside it and ends with `q_0<=q_*<Q`; since the opposite endpoint edge obeys
  `g_x>=Q`, the new `q_0` shell still cuts exactly `{x}`.  The eleven FW210 rows then reduce to only
  `(1,{0},{0})`, `(2,{0,1},{0})`, and `(3,{0,1,2},{0})`: an endpoint singleton, rooted `L2`, or rooted `L3` with
  middle root.  `L6` realises the third row.  Replay: `theory-lab/topwindow/verify_q1_small_return_catalogue.py`.
  This finite return catalogue does not exclude its three entries, control the discarded wrapper, treat the
  original `Q=2,3` terminals, or prove G18; those steps remain **UNVERIFIED**.
  It does, however, give an exact proper-core spectrum.  The independently replayed **OBSERVED all-order q=1
  bounded-defect return-core interface** (FW222) writes a return cap of order `a=1,2,3` with boundary `g` as
  `I_N=F_D+I_C(a,2)+X^g(1+...+X^(a-1))R_D`, where `D=T-J` and `R_D` is its rooted-depth polynomial.  Consequently
  `Spec(D) intersect [1,g-1]={C(a,2)+1,...,g-1}`: the connected proper core has an exact prefix with only `0,1,3`
  fixed initial holes.  Replay: `theory-lab/topwindow/verify_q1_return_prefix_interface.py`.  This is the requested
  bounded-defect inheritance interface, but it is not yet an induction.  The independently replayed **OBSERVED
  all-order anchored q=1 return gap ladder** (FW223) now classifies the formerly free upper spectrum.  If
  `0=s_0<...<s_(d-1)` are the rooted depths of `D`, then
  `s_i-s_(i-1)=a+e_i`, the boundary-edge excess is exactly `sum e_i`, and the high internal spectrum is the disjoint
  union of the corresponding intervals
  `[g+s_(i-1)+a,g+s_i-1]`.  Retaining the old q=1 window pins the final interval to
  `[N-Q+1,N-a]`, so `e_(d-1)=Q-a` and the final rooted-depth gap is exactly `Q`.  The boundary root has original
  coordinate `g+a-1`: if it is visible then `g<=Q-a` and a wrapper remains; if it lies in `H_Q`, then the returned
  cap is exactly `W_0` and `g>=Q-a+2`.  Replay: `theory-lab/topwindow/verify_q1_return_gap_ladder.py`.  The remaining
  gap mass is still uncontrolled.  The next independently replayed **OBSERVED all-order exact q=1 double-peel
  tiling** (FW224) removes both `J` and the opposite endpoint `x`.  For `K=T-(J union {x})`, connected threshold
  core `H=H_Q`, opposite leaf edge `h`, and `M=N-Q`, it gives the exact coefficientwise state
  `I_M=F_K+I_C(a,2)+X^g A_a R_p(K)+X^h R_r(H)` and
  `X^hR_r(K)=X^hR_r(H)+I_[M+1,N-a]`.  Thus the old holes are exactly the rooted factor of connected `H`, while
  the other `Q-a` vertices form one consecutive rooted-depth block at the opposite root.  Replay:
  `theory-lab/topwindow/verify_q1_double_peel_tiling.py`.  This is a strict-size, smaller-ambient contextual state,
  but closure under another peel (or a forced collision) remains **UNVERIFIED**.  Its exact stability form is the
  **OBSERVED all-order q=1 linear-defect near-Leech reduction** (FW225).  If `k=|K|`, `C=C(k,2)` and `L=M-C`, then
  `L=a n+u+1-a(a+3)/2<=4n-14`; `Spec(K)` is `[1,C]` with exactly `delta<=L` low holes replaced by the same number
  of outliers in `[C+1,C+L]`.  Replay: `theory-lab/topwindow/verify_q1_double_peel_stability.py`.  Bounded `delta`
  is now a finite-hole/endpoint-strip target, while growing `delta` must be carried by the two rooted factors of
  FW224.  The independently replayed **OBSERVED all-order q=1 visible-return linear-defect theorem** (FW226) makes
  this split quantitative.  The disjoint width-`a` rooted blocks give
  `delta+ceil((delta-C(a,2))/a)>=k-ceil(g/a)`.  If the return root is visible, `g<=Q-a`; combining this with
  `u>=ceil((n-9)/5)` forces `delta>=n/10-O(1), 2n/5-O(1), 11n/20-O(1)` for `a=1,2,3`, respectively.  Replay:
  `theory-lab/topwindow/verify_q1_visible_return_defect.py`.  Hence bounded defect at unbounded order can occur only
  on the connected threshold-core side.  Excluding the resulting linear-defect visible rows or classifying the
  threshold-core bounded-defect rows remains **UNVERIFIED**; G18 is not inferred.  The next independently replayed
  **OBSERVED all-order q=1 bounded-defect giant-branch compression theorem** (FW227) gives the latter branch an
  explicit topology.  Cross-component shell pairs inject into only `2(L-a)+1=O(n)` values.  For a fixed cap
  `Delta>=delta`, put `c_0=Delta+ceil((Delta-C(a,2))/a)`; once `k` is at least
  `2c_0+17,2c_0+24,2c_0+32` for `a=1,2,3`, one component `B` of `K-p` satisfies
  `|T-B|<=c_0+5a+4` and has at most two boundary edges in `T`.  Replay:
  `theory-lab/topwindow/verify_q1_bounded_defect_giant_branch.py`.  This reduces fixed defect to a bounded wrapper,
  but a complete inherited spectrum for `B`, a wrapper catalogue/exclusion, and G18 remain **UNVERIFIED**.  The
  independently replayed **OBSERVED all-order q=1 double-peel Taylor-parity transfer theorem** (FW228), using the
  Taylor condition as **LITERATURE** input, further cuts the catalogue.  For `n=r^2`, it forces defect at least
  `r-2,floor((r-2)/2),r-2` in the `a=1,2,3` rows; for `n=r^2+2`, the bounds are
  `0,floor((r-1)/2),1`, strengthened at large core order to `delta>=C(a,2)+a`.  Hence uniformly bounded defect can
  survive only for `(n=r^2+2,a=1)` or `(n=r^2+2,a=3)`.  Replay:
  `theory-lab/topwindow/verify_q1_double_peel_parity.py`.  Those two rows and all growing-defect rows remain
  **UNVERIFIED** at that stage.  The next independently replayed **OBSERVED all-order q=1 shell-pair quadratic
  theorem** (FW229) removes the bounded alternative entirely.  The low rooted-depth vertices form an
  ancestor-closed ball of order at most `ell=ceil((delta-C(a,2))/a)`.  Partitioning every pair of the remaining
  shell vertices by whether its LCA is inside that ball gives
  `C(k-delta-ell,2)<=2(ell+1)(L-a)+ell`.  Hence
  `delta>=ceil((k-7)/12),ceil((k-11)/9),ceil((k-9)/8)` for `a=1,2,3`, with the sharper asymptotic constants
  `a(3-2sqrt(2))/(a+1)`.  Replay: `theory-lab/topwindow/verify_q1_shell_pair_quadratic.py`.  Every return now has
  linear defect; the remaining **UNVERIFIED** task is a collision/energy theorem for the two rooted factors carrying
  those holes.  The next independently replayed **OBSERVED all-order q=1 exact two-factor shell-allocation
  theorem** (FW230) uses the exact split `delta=C(a,2)+q+b`, where `q` is the number of low coefficients supplied by
  the return blocks and `b` is the number supplied by the connected `H` factor.  If
  `t=ceil(q/a)`, shell-pair counting at both roots gives
  `C(k-t,2)<=2(t+1)(L-a)+t` and
  `C(u+1-b,2)<=2(b+1)(L-1)+b`.  Adding the exact consecutive r-root block from `K-H` strengthens the latter to
  `C(k-b,2)<=2(b+1)((a+1)k+C(a,2)-1)+b`.  No `delta` subtraction is needed because the complete non-low factor
  supports already lie in narrow bands.  Exact real-algebra replay then improves the asymptotic floors for
  `delta/k` to `1/5,3/14,2/9` (the unrounded constants are approximately `0.20204,0.21539,0.22291`) for
  `a=1,2,3`.  Replay:
  `theory-lab/topwindow/verify_q1_two_factor_shell_allocation.py`.  This proves positive-density intrusion at the
  paired rooted interfaces, but the collision/energy closure and G18 remain **UNVERIFIED**.  The next independently
  replayed **OBSERVED all-order q=1 bi-root crown compression theorem** (FW231) intersects the two non-low shells.
  If their exact low-ball orders are `t,b`, then either `delta>=ceil(k/2)`, or, above core cutoffs `60,94,126`, all
  but an exact `O(1)` remainder of at least `k-t-b` crown vertices lies in one component off the p-r diameter path.
  The uniform remainder caps are `15,21,29`; on the minimum-defect boundary at core order `100000` they sharpen to
  `5,7,9`.  Replay: `theory-lab/topwindow/verify_q1_biroot_crown_compression.py`.  Making that giant central
  offshoot thin or giving it an inherited complete spectrum remains **UNVERIFIED**; G18 is not inferred.
  The next independently replayed **OBSERVED all-order q=1 giant-crown heavy branch-spine theorem** (FW232) uses
  the actual LCA hierarchy inside that one gate fibre.  If its selected shell has gate-depth width `W=L-a`, then a
  fixed LCA supports at most `2W+1` shell-pair distances.  Following the unique heavy child until only
  `O(sqrt(W))` marks remain gives at least
  `ceil((s_c^2-floor(sqrt(4(2W+1)))^2)/(3(2W+1)-1))` positive-loss vertices on one path.  Every such vertex is a
  global branch vertex unless it is itself a shell mark; shell marks on one path form a Golomb ruler in width `W`,
  so only `O(sqrt(W))` exceptions occur.  Consequently the low-defect rows contain branch spines of orders at
  least `k/48,k/72,k/96-O(sqrt(k))` for `a=1,2,3`; at the FW230 minimum-defect boundary for `k=100000`, the exact
  floors are `4673,3298,2394`.  Replay: `theory-lab/topwindow/verify_q1_crown_heavy_spine.py`.  Cross-level
  collision/descent on this spine and the separate `delta>=ceil(k/2)` energy branch remain **UNVERIFIED**; G18 is
  not inferred.
  The next independently replayed **OBSERVED all-order q=1 core-outlier pole-cone theorem** (FW233) localises the
  high-distance side of the defect.  The `delta` K-outliers lie in `[C+1,C+L]`, so their far-pair graph has matching
  number at most `floor(sqrt(2L-1))` and a pole cover of at most twice that order.  One pole is incident with at
  least `ceil(delta/(2 floor(sqrt(2L-1))))` outlier pairs; all of their paths share a common segment of length at
  least `(C-2L+3)/2`, which contains an edge of weight at least
  `ceil((C-2L+3)/(2(k-d_out)))`.  With the FW230 linear defect, this is an `Omega(sqrt(k))`-neighbour pole, a
  `k^2/4-O(k)` common cone and a located `k/4-O(sqrt(k))` edge in every return.  Replay:
  `theory-lab/topwindow/verify_q1_outlier_pole_cone.py`, with the underlying far-pair and common-cone verifiers
  hash-locked and separately replayed.  Identifying this cone with the FW232 crown spine, or forcing a collision
  when they separate, remains **UNVERIFIED**; G18 is not inferred.
  The next independently replayed **OBSERVED all-order q=1 crown-spine quadratic weighted-span theorem** (FW234)
  shows that the latter spine is also genuinely long in the weighted metric.  If `e_i` shell marks are shed and
  `m_(i+1)` retained at successive heavy LCAs, their cross-level pair families are disjoint and total exactly
  `(s_c^2-m_f^2-sum e_i^2)/2`.  The FW232 bounds make the two losses only `O(k^(3/2))`; packing all those distances
  into the moving shell interval forces `Gamma>=s_c^2/4-O(k^(3/2))`, uniformly
  `Gamma>=k^2/16-O(k^(3/2))`.  At the minimum-defect `k=100000` rows the exact span floors are
  `1578444539,1815868095,1952390823`.  Replay:
  `theory-lab/topwindow/verify_q1_crown_spine_quadratic_span.py`.  FW233 and FW234 now provide two located
  quadratic paths; proving that they nest into a strict contextual state or collide when separated remains
  **UNVERIFIED**, and G18 is not inferred.
  The next independently replayed **OBSERVED all-order q=1 crown--pole separated-side alignment theorem** (FW235)
  supplies the first relative-orientation bridge.  FW232 first selects the unique heavy child at the crown gate;
  if its `h_c` marks and the `d_out` pole neighbours lie in disjoint one-boundary sides, their cross distances are
  fixed-bridge sums of two rooted-depth sets and occupy at most `W+q_K+1<=W+L` integers.  Hence separated placement
  requires `h_c d_out<=W+L`; at a later heavy split, a wholly
  transverse pole side similarly requires `m d_out<=W+L`.  Exact finite bridging and all-order residue/parity
  tails exclude separated placement in the conservative low-defect envelopes from core orders
  `147464,279948,524298` for `a=1,2,3`.  Replay:
  `theory-lab/topwindow/verify_q1_crown_pole_alignment.py` (951,447 bridge rows, five inherited A/B witness passes,
  peak RSS about 65 MB).  The surviving containment/opposing-overlap orientations, the separate high-defect branch,
  strict contextual descent and G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 aligned proper-carrier absorption theorem** (FW236) shows that
  those surviving orientations cannot meet only accidentally.  Nested sides give a proper half-tree containing all
  crown marks and pole neighbours.  In opposing overlap, if `x` crown marks and `y` pole neighbours remain outside
  the other side, the exact two-gate identity gives `xy<=W+q_K+1<=C_*:=W+L`.  With
  `X=floor(sqrt(C_*h/d))` and `Y=floor(C_*/(X+1))`, either the pole side contains all `d` neighbours and at least
  `h-X` crown marks, or the crown side contains all `h` marks and at least `d-Y` pole neighbours.  Asymptotically
  the losses are `O(k^(3/4))` and `O(k^(1/4))`, respectively.  Replay:
  `theory-lab/topwindow/verify_q1_aligned_carrier_absorption.py`.  The carrier is a proper distinct-distance context,
  but consecutive-spectrum inheritance, repeatable descent, the high-defect closure and G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 anchored outlier diameter-endpoint cone theorem** (FW237)
  strengthens the pole itself.  If the `delta`-edge outlier graph has `s` active vertices, then
  `binom(s,2)>=delta`; fixed-diameter domination gives one endpoint outlier degree at least `ceil(s/2)`.  Its
  neighbours share a `K`-diameter prefix of length at least `(C-2L+3)/2`.  Because that endpoint is a leaf,
  deleting it produces the exact order-`k-1` carrier `K-{alpha}`, retaining every selected outlier neighbour and
  all but at most one crown mark.  The stronger degree lowers the permanent low-defect cone--crown alignment
  thresholds from `147464,279948,524298` to `1448,2496,3978`.  Replay:
  `theory-lab/topwindow/verify_q1_anchored_outlier_diameter_cone.py`.  What is still **UNVERIFIED** is the decisive
  spectral step: `K-{alpha}` has distinct distances, but no proved consecutive interval/q=1 inheritance; the
  repeatable descent, high-defect exclusion and G18 do not yet follow.
  The next independently replayed **OBSERVED q=1 old-threshold outlier endpoint-peeling theorem** (FW238) iterates
  that leaf step while keeping the original `C=binom(k,2)` fixed.  With `theta` remaining distances above `C`, a
  current diameter leaf removes at least `ceil(s(theta)/2)` of them, where `s(theta)` is the least integer with
  `binom(s(theta),2)>=theta`.  The potential `ceil(2 sqrt(2 theta))` drops every time, so at most
  `ceil(2 sqrt(2 delta))=O(sqrt(k))` leaves remove all original outliers.  The remaining connected induced tree
  `K_0` has order `k-O(sqrt(k))`, spectrum contained in `[1,C]`, and exactly
  `t k-binom(t+1,2)` holes there after `t` actual peels.  Moreover `F_K` splits exactly into `F_(K_0)` plus the
  `t` nested endpoint rooted factors.  Replay: `theory-lab/topwindow/verify_q1_outlier_endpoint_peeling.py`.
  The new interface is near-full and provenance-preserving, but its `O(k^(3/2))` old-threshold holes are not yet a
  smaller complete interval; rescaled closure and G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 one-leaf normalised shell/pole dichotomy** (FW239) avoids batching
  those holes.  Delete only the FW237 anchored leaf and reset the threshold to `C'=binom(k-1,2)`.  If `b_0` old holes
  and `r_0` deleted endpoint distances lie at most `C'`, the new defect is exactly `eta=b_0+r_0`.  Thus either
  `eta>=ceil(k/2)`, or at least `floor(k/2)` endpoint depths lie in a width-`k+L-2=O(k)` top shell.  Fixed-LCA
  capacity then prevents that shell's heavy path from leaving the pole child before only `O(sqrt(k))` marks remain;
  if the pole branches earlier, its common cone has already been traversed.  In either subcase the low-`eta` branch
  contains a located pole--shell common path of length `k^2/16-O(k^(3/2))`.  Replay:
  `theory-lab/topwindow/verify_q1_one_leaf_normalized_shell.py` (5 inherited A/B witness passes, about 58 MB peak RSS).
  This now routes the former high-defect geometry into a precise one-step dichotomy, but neither the linear new defect
  nor the shared quadratic path has yet been turned into a collision/closed recurrence; G18 remains **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 normalised four-factor prefix theorem** (FW240) keeps the coefficient
  provenance on that linear branch.  Restricting FW224 after the leaf decomposition gives exactly `I_(C')=F_(K')`
  plus the fixed cap interval, the truncated old `p`-root factor, the truncated old `H`-root factor, and the truncated
  deleted-leaf rooted factor.  Thus `eta=binom(a,2)+q'+b'+r_0`.  If `eta>=ceil(k/2)`, one of the three nonfixed
  suppliers contributes at least `ceil((eta-binom(a,2))/3)` holes and supports a connected ancestor ball in `K'`
  of order `k/(6a)-O(1)`, uniformly `k/18-O(1)`.  Replay:
  `theory-lab/topwindow/verify_q1_normalized_four_factor.py` (all three-way allocations through `k=60`, selected
  rows through `k=100000`, 5 inherited A/B passes, about 69 MB peak RSS).  This is genuine prefix inheritance, but
  the supplier ball still lacks an internal interval; collision/absorption, closed descent, and G18 remain
  **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 endpoint half-ball/half-shell normal form** (FW241) removes even
  the post-peel defect split from the geometry.  Of the `k-1` deleted-endpoint distances, at least
  `ceil((k-1)/2)` lie on one side of `C'`.  The low side is an ancestor-closed connected ball; distinct internal
  distances force its rooted radius to be at least `ceil(binom(t,2)/2)=k^2/16-O(k)`.  The high side is the
  FW239 shell and shares a pole-aligned path of length `k^2/16-O(k^(3/2))`.  Replay:
  `theory-lab/topwindow/verify_q1_endpoint_half_ball_shell.py` (endpoint partitions through `k=100000`, selected
  rows, 5 inherited A/B passes, about 58 MB peak RSS).  This produces a universal located quadratic object after
  one strict deletion, but a quadratic path alone is not a collision or closed recurrence; G18 remains
  **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 nested endpoint-prefix ledger theorem** (FW242) returns to the
  original FW219 threshold band and deletes its visible vertices in canonical coordinate order.  At stage `j` the
  coordinate-`j` vertex is a leaf, the current diameter is uniquely `N-j` from the opposite endpoint, and its
  remaining endpoint factor is supported in `1,...,N-Q`.  Telescoping all `Q` stages gives the exact disjoint
  identity `I_(N-Q)=F_H+X^g R_p(H)+sum_j L_j`, with each `L_j` a named translated rooted-depth factor.  Thus the
  connected threshold core now has a complete contextual prefix ledger, not just an unstructured hole set.
  Replay: `theory-lab/topwindow/verify_q1_threshold_endpoint_ledger.py` (19,984 arithmetic rows, the full L6
  geometry, 5 inherited A/B passes, about 54 MB peak RSS).  This also records the essential obstruction: deleting
  the first visible leaf deletes the unique internal owner of distance `N-Q`, so an intermediate tree is not itself
  Leech and the external ledger cannot be discarded.  Bounded compression/strict contextual recursion and G18
  remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 one-endpoint defect-ball theorem** (FW243) renormalises `T-x`
  itself.  If `m=n-1`, `C=binom(m,2)` and `h=|H_Q|`, then its ambient maximum is exactly `C+h`.  Its holes at most
  `C` are precisely the `x`-distances to the ancestor-closed ball `{v in H_Q:y(v)>=m}`; if that ball has order
  `delta`, `T-x` has exactly `delta` paired outliers above `C`.  Taylor parity (**LITERATURE** input) forces
  `delta>=floor((sqrt(n)-1)/2)` at square orders and `delta>=floor(sqrt(n-2)/2)` at square-plus-two orders.
  Replay: `theory-lab/topwindow/verify_q1_one_endpoint_defect_ball.py` (Taylor roots through 100,000, exact L6
  defect-ball control, 5 inherited A/B passes, about 71 MB peak RSS).  The hole carrier is now connected and the
  defect cannot stay zero, but outlier classification/high-defect closure and G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 one-endpoint shell/LCA compression theorem** (FW244) identifies
  every vertex outside that ball with a distinct offset in `1,...,m` except for the `delta` outlier offsets.  An
  exact LCA-capacity count gives
  `binom(m-delta,2)<=2m-2+delta(2m-1)`, hence
  `delta>=ceil((6m-3-sqrt(32m^2-16m-7))/2)=(3-2sqrt(2))m-O(1)` for `m=n-1`.
  The target floors at `n=18,25,27,36,38,49,51` are `3,4,4,6,6,8,8`.  Keeping the LCA translates also forces a
  quadratic coordinate span inside the same defect ball, and every high outlier has its LCA in that ball.
  Replay: `theory-lab/topwindow/verify_q1_one_endpoint_shell_lca.py` (all `m<=100000`, exact radical/integer
  agreement, L6 control, 5 inherited A/B passes, about 72 MB peak RSS).  Bounded/sublinear defect is now impossible,
  but the final shell--outlier collision and the `delta>m/2` branch remain **UNVERIFIED**, as does G18.
  The next independently replayed **OBSERVED q=1 two-endpoint ownership/overlap theorem** (FW245) applies the same
  defect ball to both diameter endpoints.  If `c_0` is the number of top-band values whose pair touches neither
  endpoint, then exactly `delta_x+delta_z=m-1+c_0`; hence one ball has order at least `ceil((m-1)/2)`.  Their rooted
  radii overlap continuously on the middle diameter path by the fixed length `binom(m,2)-m`.  If that overlap
  contains no common path vertex, its spanning edge exceeds `N-2m`; strict edge-cut rigidity forces the edge to cut
  off exactly one endpoint and its neighbour.  Replay:
  `theory-lab/topwindow/verify_q1_two_endpoint_defect_overlap.py` (all `m<=100000`, full two-end L6 control, 5
  inherited A/B passes, about 57 MB peak RSS).  Thus the formerly vague high-defect case is now a sharp alternative:
  shared linear defect carriers, or an explicit two-vertex endpoint wrapper.  The shared-vertex collision/wrapper
  exclusion and G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 shared-ball/top-cycle theorem** (FW246) excludes that wrapper for
  every `n>=12`: the wrapper would make its endpoint defect ball a singleton (`delta=1`), contradicting FW244.
  Therefore both balls share a diameter-path vertex `c`; its distances to both diameter endpoints lie in
  `[n-1,binom(n-1,2)]`, so `c` has no top-distance neighbour.  Yet the graph formed by the exactly `n-1` distances
  above `binom(n-1,2)` has `n` vertices and an isolated vertex, and therefore must contain a cycle.  Replay:
  `theory-lab/topwindow/verify_q1_shared_ball_top_cycle.py` (all remaining orders through 100,000, explicit L6
  isolated-vertex/triangle control, 5 inherited A/B passes, about 49 MB peak RSS).  The remaining high-defect
  geometry is now a shared central carrier plus a forced near-diameter cycle; cycle classification/thick-centre
  exclusion and G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 top-cycle normal-form theorem** (FW247) completes that
  classification.  Every hypothetical order-at-least-12 tree has either a top-distance triangle containing the
  diameter, or an induced top rectangle containing it.  In the rectangle, the three positive deficits satisfy the
  exact relation `c=a+b`; in the triangle the three median arms have the explicit half-sum form and are all greater
  than `(binom(n-1,2)-(n-1))/2`.  Replay:
  `theory-lab/topwindow/verify_q1_top_cycle_normal_form.py` (integer parameter identities through order 4,000,
  explicit L6 triangle control, 5 inherited A/B passes, about 58 MB peak RSS).  Locating the unique owners of the
  small deficits and excluding/descending from the triangle and rectangle gates remain **UNVERIFIED**, as does G18.
  The next independently replayed **OBSERVED q=1 triangle-or-Ferrers-factor theorem** (FW248) upgrades the
  rectangle branch globally.  If no vertex is at top distance from both diameter endpoints, the two endpoint
  top-neighbour coordinate sets `A,B` satisfy
  `#{(a,b):a+b=j}=1` for every `0<=j<n-1`; the entire top graph is their connected truncated Ferrers sum graph plus
  isolates, and its cycle rank equals the isolate count.  The first factor contains `0,...,Q-1` and omits `Q`, so
  the other factor has first positive digit exactly `Q` and enters the all-order mixed-radix prefix recursion.
  Replay: `theory-lab/topwindow/verify_q1_top_ferrers_factor.py` (7,994,001 first-digit rows through `m=4000`, L6
  triangle control, 5 inherited A/B passes, about 54 MB peak RSS).  Rooted realisation of the later digits and both
  the triangle and Ferrers exclusions remain **UNVERIFIED**, as does G18.
  A parallel independently replayed **OBSERVED q=1 popular-shell-sum theorem** (FW249) strengthens the one-endpoint
  defect estimate.  Exact multiplicities of the sums of two distinct elements of `1,...,m` give
  `delta>=ceil((2m-1-sqrt(16m-15))/8)=m/4-sqrt(m)/2+O(1)`, improving the FW244 density
  `3-2sqrt(2)` to asymptotic density `1/4` at each diameter endpoint.  Replay:
  `theory-lab/topwindow/verify_q1_shell_popular_sums.py` (16,639 direct sum-layer rows, exact minima through
  `m=100000`, L6 control, 5 inherited A/B passes, about 53 MB peak RSS).  This is a stronger carrier-size theorem,
  not a collision or an exclusion; both FW248 branches and G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 Ferrers common-gate theorem** (FW250) turns the nontriangle factor
  back into exact tree geometry.  Put `s=min(Q,n-1-Q)`.  If `v_j` has endpoint deficit `0<=j<s` and `r_Q` is the
  first opposite digit, then these `s` vertices have one common projection gate `g` on `x--r_Q`, and
  `d(g,v_j)=Z-j` with `Z>=(N+n-1-Q)/2`.  Hence this exact initial band is one consecutive quadratic crown; its
  paths share a trunk of length at least
  `ceil((2(n-1)-Q-2s+3)/2)>=ceil((ceil((n-1)/2)+3)/2)`.
  Replay: `theory-lab/topwindow/verify_q1_ferrers_common_gate.py` (23,970,006 exact gate/parity rows through
  `m=4000`, 5 inherited A/B passes, about 66 MB peak RSS).  Crown branching/later digits, the triangle branch and
  G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 quarter-core/uniform-trunk theorem** (FW251) transfers FW249 to the
  entire threshold core: `u+1=m-Q>=delta_min(m)`, hence
  `Q<=m-delta_min(m)=3m/4+sqrt(m)/2+O(1)`.  On the Ferrers side the corrected exact prefix
  `s=min(Q,m-Q)` makes the common trunk unconditional and gives
  `s>=min(Q,delta_min(m))`.
  Replay: `theory-lab/topwindow/verify_q1_core_density_trunk_window.py` (every `m<=100000`, 5 inherited A/B passes,
  about 59 MB peak RSS).  Converting the linear crown trunk into a collision/handoff and excluding it and the
  triangle branch remain **UNVERIFIED**, as does G18.
  The next independently replayed **OBSERVED q=1 Ferrers first-split theorem** (FW252) controls the first branch
  below that trunk.  For crown order `s>=7`, one child retains at least `s-2` crown marks.  Losing two is possible
  only for the two endpoint radii; the crown cross distances fill a linear interval with at most one hole (the
  one-mark case has the analogous exact one-hole interval).  Replay:
  `theory-lab/topwindow/verify_q1_ferrers_first_split.py` (142,407 nontrivial set partitions through `s=10`, 69
  cross-sum-injective survivors, all-order envelopes through `s=100000`, 5 inherited A/B passes, about 50 MB peak
  RSS).  Controlling unmarked vertices and the remaining hole owner is still **UNVERIFIED**; this is not yet the
  Ferrers exclusion or G18.
  The next independently replayed **OBSERVED q=1 triangle-gate/large-Ferrers theorem** (FW253) locates the other
  FW248 branch.  Every vertex top-adjacent to both diameter endpoints has a median gate inside both endpoint defect
  balls and three exact quadratic arms; vertices sharing a gate form a distinct-radius pole fibre of width at most
  `m-2` and order at most `m-1-|a-b|`.  On the Ferrers side, `delta_min(m)>=7` from `m=37`, so every `n>=38` case
  has either `Q<=6` or enters FW252 with crown order at least seven.  Replay:
  `theory-lab/topwindow/verify_q1_triangle_gate_and_large_ferrers.py` (11,988 extremal/parity rows through `m=4000`,
  exact large-order threshold, L6 triangle control, 5 inherited A/B passes, about 69 MB peak RSS).  The triangle
  fibres, small-`Q` core, giant carrier and G18 remain **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 small-Q 27-row theorem** (FW254) resolves the combinatorial width
  of the `Q<=6` label.  Its first crown LCA has exactly `1,4,7,7,8` possible cross-sum partitions for
  `Q=2,3,4,5,6`.  The remaining connected core has order `h=m-Q`, diameter at most
  `binom(h,2)+E_Q(m)` with `E_Q(m)=m(Q+1)-Q(Q+3)/2<=7m-27`, and the crown common trunk has length at least `m-7`.
  Replay: `theory-lab/topwindow/verify_q1_small_q_catalogue.py` (27 frozen rows, 499,945 exact arithmetic rows, 5
  inherited A/B passes, about 53 MB peak RSS).  The unmarked attachments of this fixed-width near-Leech core are
  still **UNVERIFIED**; no order or G18 is excluded by FW254 alone.
  The next independently replayed **OBSERVED q=1 crown-shell attachment theorem** (FW255) controls part of the
  unmarked geometry in the `s>=7` branch.  At the first crown LCA `h`, the crown uniquely owns the consecutive
  radii `H,H-1,...,H-s+1`.  A wholly crown-free extra child must have reflected shift at least
  `min(s+a,2s-2)` in the one-mark row and at least `2s-2` in the endpoint-pair row, so it is separated from the
  crown by another linear empty shell.  Replay: `theory-lab/topwindow/verify_q1_crown_shell_attachment_gap.py`
  (33,125 direct windows through `s=256`, all-order formulas through `s=100000`, 5 inherited A/B passes, about
  80 MB peak RSS).  Attachments inside the two marked sides and the one-hole owner remain **UNVERIFIED**; so does G18.
  The next independently replayed **OBSERVED q=1 opposing-tail theorem** (FW256) includes the parent direction at
  the first crown LCA.  A crown-free direction has shifts only in the two tails
  `t<=max(a,1)-s` or `t>=min(s+a,2s-2)` (one-mark row), and `t<=1-s` or `t>=2s-2`
  (endpoint-pair row).  Any unmarked cross owner of the single missing coefficient must satisfy the exact balance
  `t_left+t_right=2a` or `s-1`.  Replay: `theory-lab/topwindow/verify_q1_crown_opposing_tails.py` (2,117 direct tail
  rows, all-order formulas through `s=100000`, 5 inherited A/B passes, about 55 MB peak RSS).  Excluding this
  opposing balance and the marked-side attachments remains **UNVERIFIED**; G18 is still **UNVERIFIED**.
  The next independently replayed **OBSERVED q=1 opposing-owner fixed-diameter heavy-gateway theorem** (FW257)
  shows that an h-cross unmarked owner has one negative parent-side vertex and one positive descendant-side
  vertex; the positive direction need not be crown-free.  The reflected shift of `x` is negative, so one edge on
  the fixed diameter segment `x--h` jumps the forbidden window.  Its weight is at least `2s-1` in a
  one-outside-mark row and `3s-3` in the endpoint-pair row; deleting it separates `x` from `h` and the crown.
  Replay: `theory-lab/topwindow/verify_q1_crown_opposing_gateway.py` (33,125 direct gateway rows through `s=256`,
  all-order formulas through `s=100000`, 5 inherited A/B passes, about 61 MB peak RSS).  Converting the cut into
  a collision or strict contextual descent remains **UNVERIFIED**; no order and G18 are excluded by FW257 alone.
  The independently replayed **OBSERVED complete first-crown hole-owner interface theorem** (FW258) then proves
  `H>=s` and exhausts h-cross unmarked, mixed crown/unmarked, internal marked-side, rooted and outside-mark owners.
  Its positive descendant shift is a global FW219 coordinate, so `t_+!=Q`; this removes the `a=s-1` mixed row
  when `Q=2s-2` and at most one slack value from each opposing row.  Every remaining opposing owner has an exact
  slack `k>=0`: an admissible `k=0` tiles a complete consecutive block, while admissible `k>0` leaves exactly two
  symmetric k-gaps.  Replay: `theory-lab/topwindow/verify_q1_crown_hole_owner_interface.py` (mixed Q-conditioned
  rows through `s=64`, direct slack blocks through `s=32`, all-order formulas through `s=100000`, 5 inherited A/B
  passes).  These are local raw-coefficient gaps, not inherited
  subtree-spectrum holes; contextual descent and G18 remain **UNVERIFIED**.
  The independently replayed **OBSERVED crown gap-budget/long-trunk fork** (FW259) uses the first LCA inside the
  giant marked child.  On the coordinate-admissible rows, a gap placement requires `k>=s-2`, or `s-3` in the
  endpoint row; an admissible equality fills the whole gap and forces a singleton-versus-rest split.  Otherwise
  that LCA is beyond an explicit linear depth floor.  The `t_+!=Q` filter only narrows the premise; these bounds do
  not change.
  Replay: `theory-lab/topwindow/verify_q1_crown_gap_budget_trunk.py` (exact hierarchy arithmetic and 5 inherited
  A/B passes).  This is genuine slack consumption, but the long-trunk branch does not inherit the two-gap state;
  a closed iteration, any order exclusion and G18 remain **UNVERIFIED**.  This meets the route's stop-loss rule:
  further compatible span bounds are not being promoted as progress toward closure.
  The independently replayed **OBSERVED exact Q=2 visible-component/core tiling theorem** (FW260) classifies the
  visible forest as a rooted `L2` twig or two singleton components and gives the corresponding exact two/three-root
  polynomial partitions on an order-`n-3` connected core.  Their `X=-1` specialisation recovers Taylor's square
  order condition but does not strengthen it.  Replay: `theory-lab/topwindow/verify_q1_q2_core_tiling.py` (rows
  through order 100000, `L4`-path boundary control, 5 inherited A/B passes).  The unbounded rooted core and G18
  remain **UNVERIFIED**.
  A stronger scope bridge is the independently replayed **OBSERVED universal direct endpoint-singleton
  double-peel theorem** (FW261).  For every `n>=5` candidate and every opposite first hole `Q>=2`, deleting the two
  diameter endpoints leaves an order-`n-2` tree `K` with the exact disjoint tiling
  `I_(N-Q)=F_K+X^gR_p(K)+X^hR_r(H_Q)` and the exact opposite visible block.  Its paired low-hole/high-outlier defect
  lies in a band `L=2n-3-Q<=2n-5`, and `n-2<=2delta+g`; a visible endpoint neighbour gives
  `delta>=ceil((u+1)/2)`.  Replay: `theory-lab/topwindow/verify_q1_endpoint_singleton_double_peel.py` (bounded
  exhaustive arithmetic through order 1200, selected all-order rows through 100000, `L4`/`L6` controls, 5 inherited
  A/B passes, about 19 MB peak RSS).  This directly includes the original `Q=2,3` cases without claiming historical
  FW220--FW223 provenance.
  Finally, the independently replayed **OBSERVED universal direct two-root shell theorem** (FW262) allocates the
  low holes exactly between those two rooted factors and proves three LCA-shell inequalities.  An exact-real UNSAT
  certificate gives the sharp relaxed floor
  `delta/(n-2)>=10-4sqrt(6)-o(1)=0.202041...-o(1)`, so `Q=2,3` now enter the same linear-defect regime as the main return
  route.  Replay: `theory-lab/topwindow/verify_q1_endpoint_singleton_two_root_shell.py` (finite monotonicity, selected
  exact minima through core order 100000, Z3 QF_NRA UNSAT, 5 inherited A/B passes, about 49 MB peak RSS).  Locating
  the linear low-hole owners, preserving this state after another peel, excluding an order and G18 are still
  **UNVERIFIED**; FW261--FW262 are a unified exact interface, not a global descent theorem.
  The independently replayed **OBSERVED q=1 one/two-leaf terminal-annulus obstruction** (FW263) rules out the
  simplest proposed recursion.  If one or two non-root vertices are peeled from the FW261 core, their deleted
  polynomial has at most `2n-3` coefficients, but it contains a genuine leaf-edge weight at most
  `N-ceil(binomial(n-1,2)/2)`.  Any terminal interval of that size ending at `M=N-Q`, with `Q<=n-2`, begins at least
  at `N-3n+6`; the two bounds are disjoint for every `n>=14`.  Thus the deleted incident rooted factor cannot simply
  disappear into a high suffix.  Replay:
  `theory-lab/topwindow/verify_q1_two_leaf_terminal_annulus_obstruction.py` (999,870 arithmetic rows through order
  100,000, exact `L6` obstruction, 5 inherited A/B passes, about 19 MB peak RSS).  A valid next recurrence must retain
  or reroot that factor, or use a proper trunk cut with bounded boundary context.  Such a recurrence and G18 remain
  **UNVERIFIED**; FW263 excludes a proof route, not a tree order.
  The independently replayed **OBSERVED q=1 one-leaf three-owner retention obstruction** (FW264) concerns the
  fixed core `K'=K-{alpha}`, where `alpha` is a true `T`-leaf distinct from the two boundary roots, and a ledger whose
  external blocks are singleton-boundary classes labelled by original `T`-pairs.  With `C=binomial(n-2,2)`, the old
  endpoint edges and the peeled core-leaf edge are strictly below `C` for `n>=10`, while the stipulated next prefix
  reaches at least `C` (and `C+1` when the inherited second carrier is nonempty).  Thus the three labels
  `zp,xr,alpha-a` must remain active: actual-pair rerooting cannot relabel the low `h` or `w` coefficients.  These may
  be order-one ghosts; FW264 does not force three algebraic rooted factors or retention of the whole old rooted
  factors.  Multi-vertex/fragmented cap bundling, arbitrary nonactual translates and a core exchange which moves
  `x` or `alpha` into the new internal core are outside its scope.  Replay:
  `theory-lab/topwindow/verify_q1_one_leaf_three_owner_retention.py` (299,973 arithmetic rows through order 100,000,
  5 inherited A/B passes, about 19 MB peak RSS).  A proved label merger, bounded cap recurrence or core-exchange
  recurrence remains **UNVERIFIED**; FW264 is not an order exclusion.
  The independently replayed **OBSERVED universal trunk-cut owner ledger** (FW265) records what an arbitrary
  tree-edge cut
  actually carries.  If `e=ab` separates `K` into `A` and `B`, then
  `F_K=F_A+F_B+X^wR_a(A)R_b(B)`, and the cross product expands into exactly `|A|` named `B`-rooted shifts.  Under
  global distance uniqueness the refined family consisting of `F_A`, `F_B` and those shifts is pairwise
  support-disjoint.  Thus treating the unexpanded product as one boundary factor does not by itself certify a
  decreasing owner-expanded measure.  Replay: `theory-lab/topwindow/verify_q1_trunk_cut_ledger.py` (both orientations
  of every edge in the five known witnesses, fixed multiplicity/superincreasing controls, 5 inherited A/B passes,
  about 19 MB peak RSS).  FW265 does not show that `|A|` is large at the FW259 cut or that many shifts meet the
  retained prefix.  The first controlled attempt at the missing prefix-locality theorem gives only the
  **OBSERVED conditional occupancy bound** `N_r<=floor((2b-1)/r)` at a proposed FW261-type receiving prefix: at most
  one complete order-`b` shift fits, but this bound does not exclude linearly many one-coefficient grazing shifts.  FW259 does
  not yet bound the corresponding rooted ball or inherit the receiving prefix.  Bounded prefix locality and G18
  remain **UNVERIFIED**.
  The independently audited **OBSERVED q=1 core-exchange top-band obstruction** (FW266) quantifies and obstructs the
  bounded-cap same/lower-prefix escape.  In the FW261 orientation, if a proposed new internal set `C` contains `x`, its complete positive
  actual-pair term satisfies `supp(F_C) subset I_(M')`, and `E=T-C` contains `z` with `e=|E|<Q`, then `M'>=N-e`
  and the new deficit is at most `e`.  Hence `M'<=M=N-Q` forces `|T-C|>=Q`.  Replay:
  `theory-lab/topwindow/verify_q1_core_exchange_top_band.py` (333,374 `e`-form and 341,248 shifted-form rows,
  `L4`-path/`L6` controls, 5 inherited A/B passes, about 18 MB peak RSS).  The sharp canonical exchange is the old
  FW242 stage `T_e`; raising the prefix therefore gives an exact one-step ledger, not a new recurrence.
  The independently replayed **OBSERVED near-full-prefix external-owner conservation theorem** (FW267) explains why
  that raised-prefix ledger cannot simply forget its history.  For `n>=5`, strict heaviest-edge rigidity gives every
  edge `w<=N-a(n-a)<=N-(n-1)`.  If `E` has order `1<=e<=n-2`, every `y in E` is incident with a uniquely owned
  coefficient below `N-e`; an actual-pair ledger for `I_(N-e)` must therefore retain all `e` external vertices in
  its owner-label support.  This is a vertex-order statement, not `e` distinct coefficients or algebraic factors.
  Replay: `theory-lab/topwindow/verify_q1_near_full_external_owner_conservation.py` (all integer rows through order
  128, 79 external-subset and 312 incident-owner controls, all five witnesses through A/B, about 17 MB peak RSS).
  The independently audited **OBSERVED q=1 directed-hole exchange and normalization obstruction** (FW268) tests the
  last rolling-exchange escape exactly.  If `v_b` is a leaf of `T-z`, then `C_b=T-{z,v_b}` is connected and the actual
  pairs give `I_(N-1)=F_(C_b)+L_0+X^(N-b)+L_b`, with both low rooted classes supported in `I_(N-Q)`; hence the high
  band has the single named hole `N-b`.  However ambient deletion deficits are uniquely `0` off the diameter,
  `1` at `z` and `Q>=2` at `x`, so reorientation cannot reset the ambient state.  Moreover for every `n>=7` the
  exchange core is not an order-`n-2` Leech tree and cannot be fed back through FW218.  Replay:
  `theory-lab/topwindow/verify_q1_directed_hole_interface.py` (all five known witnesses through A/B, exact `L4`-path
  entry-only and `L6` rolling controls).  In `L6`, coordinates `b=1,3` give two actual-pair choices with
  equal core/external orders, prefix and band masses but holes `N-1,N-3`; they form an involution inside one fixed
  ambient ledger, not a certified contextual transition.  Numeric reorientation of the non-Leech
  cores changes the opposite deficit from four to eight.  Thus raw hole position, complementary height, diameter
  and the tested coarse counts are not a normalization-invariant no-return rank.  FW268 does not exclude a newly
  defined owner-aware contextual normalizer or an explicitly irreversible fully charged transition.
  None of the required closure mechanisms is currently available.  The q=1 bounded-cap/core-exchange/directed-hole
  programme is therefore stopped at FW268: further span, density, moment or heavy-edge constants are not being
  counted as closure progress, and no new order exclusion or G18 is claimed.  Full acceptance criteria and exact
  remaining triggers are recorded in `docs/q1-new-mechanism-sprint.md` and `docs/q1-directed-hole-sprint.md`.
  The subsequent **OBSERVED universal q=1 row-conditioned realization encoder** gives a completeness-preserving
  computational representation of every `n>=5` candidate: the FW219 reflected coordinates canonically order
  `T-x`, increasing parent labels determine all edge weights, a triangular recurrence determines every internal
  distance, and the `N` actual-pair variables form an exact permutation of `I_N`.  Order 25 would have exactly the
  rows `Q=2,...,19`.  Independent replay checks 2,944 rooted states, 294,400 BFS-versus-recurrence distances, 294,400
  hop recurrences, 81,880 distinct-edge hop bounds, the five known witnesses, fail-closed row summaries, and complete
  free sweeps through order 8, 38,272 subtree checks and all 19,894 ordered cut rows through order 200; all SAT
  controls pass checker A and checker B.  The released optional propagation
  includes value-to-owner inverse permutation, Taylor parity, exact structural/hop bounds, and an exact rooted-subtree
  implementation of the audited edgewise cut cap.  Implementation and trust boundary:
  `theory-lab/topwindow/q1_row_cpsat.py`, `theory-lab/topwindow/verify_q1_row_encoder.py`, and
  `docs/q1-row-encoder.md`.
  The same sprint has an **OBSERVED negative performance verdict**.  Generic forest closes all order-11 states in
  123,309 nodes and about 0.04 seconds, while the strongest useful tested one-worker owner/value/cut-cap pack leaves
  even the single row `n=11,Q=2` `UNKNOWN` after 60 seconds.  Across these recorded runs, the predeclared gate fails
  by more than three orders of magnitude before full row coverage.  No order-16 gate and no order-25 `Q=2,10,19`
  sentinel was run; no finite order exclusion or G18 is inferred.  CP-SAT `INFEASIBLE` still has no independently
  checkable proof log here.
  Further generic moments or solver redundancies are stopped; the computational route can reopen only after a proved
  low-owner localisation/bounded-interface theorem restores forest-like prefix forcing.
  The ensuing FW269 audit gives an **OBSERVED exact but nonclosing low-owner interface**.  Every actual owner of
  `1<=d<Q` lies in one of four explicit q=1 LCA cones: core--core, visible--core, one visible component, or two
  visible components.  In the last case
  `d=4+(Q-1-i)+(Q-1-j)+2(y(LCA)-Q-1)`; distinct visible coordinates sharpen this to `d>=5` and force both indices
  into the last `d-3` visible positions.  For the unique weight-1 edge, the two cut-side rooted-depth sets obey both
  cross-Sidon and the edge-domino rule; the visible indices below that edge contain no consecutive pair and hence
  number at most `ceil(Q/2)`.  These are genuine all-order Leech consequences, but a pure-`H` tail has an empty
  visible-index set and escapes them.
  A matching **OBSERVED negative metric diagnostic** preserves q=1 top geometry, global distance uniqueness and an
  arbitrary fixed interval `I_kappa`, while placing all `kappa` edge owners at `Theta(n)`-deep, separated pure-`H`
  anchors.  Its diameter is exponentially larger than `binom(n,2)`, so it is not Leech and does not satisfy the
  FW219c/FW261 tight-spectrum identities.  It shows only that top geometry, distinctness and fixed low coverage are
  insufficient; it does not show that full spectrum is the only possible missing condition.  The **OBSERVED exact**
  fifteen owner signatures through `I_6` therefore do not constitute a bounded attachment catalogue.  Even the
  stronger **OBSERVED external/non-replayed engine diagnostic** “weight 1 has a permanent true-leaf endpoint”
  visits 1,351 charged candidates by insertion
  depth six, above the predeclared order-11 100-fold gate of 1,233; this engine count is audited externally and is
  not part of the FW269 arithmetic replay.  No new engine or larger-order run is authorised.  A pure-core-tail
  elimination or full tight-spectrum owner-provenance bridge remains **UNVERIFIED**, and G18 is unchanged.  Full
  proofs and trust boundary: `docs/q1-low-owner-localization.md`.
  FW270 now closes that proposed successor audit.  Exact FW219c/FW261 coefficient coverage is **OBSERVED** to be
  equivalent, after restoring the proved q=1 top-owner class, to the full Leech spectrum; it is not a weaker bridge.
  Deleting the endpoints of the unit edge gives the **OBSERVED** domino identity
  `F_T=F^T_(T-{a,b})+X+(1+X)sum_v X^(s_v)`, where the first term retains ambient `T`-distances on the
  generally disconnected surviving label set.  In a pure-`H` tail, root-depth parity and spacing force
  `d(x,b)>=2Q+1` and `2|A|-1<=M-1-d(x,b)<=M-2Q-2`, but do not eliminate the tail.  A stronger **OBSERVED negative
  metric diagnostic** realizes formal diameter-`D` owner suppliers matching the `I_P`-projections of FW219c/FW261
  for every `P>=Q>=2`, has a nonpendant pure-`H` unit edge, and first misses `P+1`; it is not an
  FW219c/FW261 state, and its exponentially large diameter makes it non-Leech.  The proposed near-perfect nonpendant-unit bound
  `diam(S)>=binom(|S|,2)+|S|-4` remains **UNVERIFIED**.  The check through order 12 is only **OBSERVED
  external/non-replayed finite evidence**, and the order-13 attempts were `UNKNOWN`.  This route is stopped pending
  an **UNVERIFIED** rooted near-perfect realization theorem and a separate singleton-tail theorem.  No new engine or
  larger-order run is authorised; G18 remains **UNVERIFIED**.  Full proof and scope:
  `docs/q1-pure-tail-stop.md`.
  FW271 sharpens the surviving full-spectrum interface without claiming closure.  For a weight-one edge with a
  pure-`H` descendant side `A`, `s=|A|` and `q_b=d(x,b)`, the `Q(s+1)` actual pairs in the visible-rooted product
  occupy the named window `[M+1-q_b,M]`; alternating parity makes exact filling impossible.  This proves the
  **OBSERVED** bounds `q_b>=Q(s+1)+1`, `q_b>=2Q+rho+1`, `q_b<=M-rho-2`, and hence
  `4s<=N-3Q+1` and `s(Q+2)<=N-2Q-1`, with the stronger high/low branch inequalities recorded in the source note.
  The corresponding general visible-split formula is also **OBSERVED exact**, but its least mixed case gives only
  linear capacity and does not force the split to be pure.
  If the unit edge is pendant, FW271 gives the **OBSERVED exact self-complement**
  `I_N=F_(T-a) dot-union X R_b(T-a)` and the exact parity-halved `e x o` cross rectangle, where
  `eo=ceil(N/2)`.  In q=1 coordinates the leaf pair is either consecutive and visible or consecutive wholly inside
  the pure core.  The rectangle is a transformed actual-pair partition, not a smaller Leech state.  The related
  **LITERATURE** construction of Calhoun--Polhill gives perfect-distance forests `t K_(1,3)` for every `t`, so even
  a forest after parity halving does not imply componentwise Leech descent.
  An **OBSERVED negative mechanism audit** stops joint two-root/no-grazing, all-digit Ferrers, canonical
  triangle/triple-boundary, covariance-kernel, signed-derivative, positive-`q` Hosoya, finite-character and Ma--Yi
  path-packing arguments at explicit owner-localisation or lower-spectrum gaps.  No distance-matrix or parity
  cross-rectangle successor conclusion is frozen; those remain **UNVERIFIED**.  FW271 creates no verifier,
  certificate, SAT witness or order exclusion, and G18 remains **UNVERIFIED**.  Full theorem, controls and trust
  boundary: `docs/q1-full-spectrum-mechanism-audit.md`.
  FW272 freezes the first narrow successor to that parity rectangle.  Root a pendant unit edge `a--1--b` at `b`,
  let `R` and `S` be the half-scaled even and odd root-depth sets, and let `L` be the mixed-parity LCA-depth matrix.
  If `L` vanished identically, the exact odd-distance rectangle would give `R dot+ S=[0,eo-1]`.  An
  **OBSERVED all-order** local interval-block argument then forces `|E|<=3`: initial `R` blocks of length at least
  four collide immediately, and blocks of length two or three cannot have a later digit.  Taylor's
  **LITERATURE** parity sizes make both classes at least four for every candidate of order at least eleven.
  Hence every order-18 candidate whose unit edge is pendant has a positive mixed-LCA entry, whether that edge is
  visible or pure-core in q=1 coordinates.  Turning the resulting positive laminar block into a collision or a
  bounded-context smaller state remains **UNVERIFIED**; the nonpendant unit-edge branch is untouched.  FW272 has
  no verifier, certificate, SAT witness or order exclusion, and G18 remains **UNVERIFIED**.  Full proof and trust
  boundary: `docs/q1-pendant-mixed-lca.md`.
  FW273 freezes the first positive-entry successor.  For a pendant unit edge, let `tau` be the least transformed odd
  coordinate owned by a positive mixed LCA.  The raw root-depth convolution has coefficient one on
  `[0,tau-1]` and its first hole at `tau`.  An **OBSERVED all-order**, actual-owner-sensitive radix argument gives
  `tau<=3|O|+2`; its owner is exactly one odd edge not incident with the root, of weight
  `w=2tau+1<=6|O|+5`.  Hence the two order-eighteen orientations give `w<=47` and `w<=71`.
  The labelled cross matrix also completes every same-parity LCA whose descendant subtree contains the opposite
  parity.  At a deepest mixed vertex, the cross pairs form an exact direct block and every remaining free owner lies
  inside a pure monochromatic child, where all internal edges are even and may be halved.  This identifies, but does
  not remove, the obstruction: one pure child can retain `Theta(n^2)` owners and inherits neither an interval nor a
  q=1 state.  The q=1 order-eighteen visible row lies at half-indices at least 70 while `tau<=35`; no proved
  propagation joins them.  A small n=11 CP-SAT necessary-relaxation run is recorded only as **OBSERVED
  external/non-replayed diagnostic** evidence, without a frozen proof log; it is not a proof, certificate, or order
  exclusion.  The positive-block collision/bounded-state implication and G18 remain **UNVERIFIED**; the nonpendant
  unit-edge branch is untouched.  Full proof, exact completion identities, controls and stop boundary:
  `docs/q1-first-positive-lca.md`.
  FW274 sharpens only that first-positive localisation.  The exact raw prefix exhausts all root coordinates below
  the first hole (with the nonexistent next even coordinate defined as `+infinity`), so the two possible initial
  radices admit a finite rooted-ancestor analysis.  The resulting **OBSERVED all-order** bound is
  `tau<=10`; the first positive owner is therefore an odd edge not incident with the root, of weight
  `w=2tau+1<=21`.  FW272 supplies the positive-entry antecedent for every pendant-unit candidate of order at least
  eleven, including both order-eighteen orientations.  An eight-vertex globally distance-distinct pressure tree
  attains `tau=10,w=21` and fills the odd transformed sheet `I_[0,11]`, but its even half-sheet is not `I_16`, so
  it is not Leech and establishes sharpness only for the local interface.  Full even-sheet terminal absorption and
  the q=1 suffix handoff remain **UNVERIFIED**; the nonpendant unit-edge branch is untouched, no order is excluded,
  and G18 remains **UNVERIFIED**.  The frozen deterministic finite-kernel replay is
  `theory-lab/topwindow/verify_q1_absolute_first_odd_edge.py`, with byte-identical output in
  `theory-lab/topwindow/results/q1_absolute_first_odd_edge_certificate.json`; it supports the analytic proof but is
  not a Leech search or an independent all-order proof.  Full proof, collision ledger and trust boundary:
  `docs/q1-absolute-first-odd-edge.md`.
  FW275 returns to the hard nonpendant `2|b` unit-edge branch.  Its **OBSERVED exact** rooted wrapper has
  `m=b+2`, counterexample cap `D_0=binom(b,2)+3b-2`, `b-3` holes, and requires every residual coefficient
  to have an actual nonroot-pair LCA owner.  **OBSERVED analytic** scalable formal states survive all audited
  first-pivot/reflection/`2p`-chain tests inside the hard cap but are not trees and die at their second actual
  pivot.  **OBSERVED hand-checkable** equality trees at `(m,D)=(9,41)` and `(11,62)` exhibit a multi-gate owner
  triangle and long-chain/whole-row telescoping, but each lies at `D=D_0+1`; they test cap-blind local LCA claims,
  not implications that essentially use `D<=D_0`.  Thus only the cap-blind first-pivot / chain-boundary /
  single-virtual-row mechanism is at an **OBSERVED STOP**; this is not a disproof of the **UNVERIFIED**
  near-perfect bound.  Reopening requires an **UNVERIFIED** strict-cap global potential on labelled multi-gate
  owners or an exact terminal-suffix peeling theorem.  The earlier
  finite checks through order twelve remain only **OBSERVED external/non-replayed finite diagnostic** evidence; FW275
  has no verifier, SAT witness or order exclusion and leaves G18 **UNVERIFIED**.  Full rooted state, controls and
  reopening gate: `docs/nonpendant-unit-rooted-stability-stop.md`.
  FW276 returns to the FW274 first positive edge `f=pc`, `w=2tau+1<=21`, and freezes its **OBSERVED exact**
  cut algebra.  If `A` is the root side and `B` the descendant side, the internal odd/even owner polynomials and
  four rooted parity factors partition both complete parity sheets coefficientwise.  The root side owns the exact
  odd block below `tau`, the two internal sides own the exact even block through `tau+1`, and the Find-Next light
  component containing `c` has only even edges and order at most `tau+1<=11` after halving.  This does not bound
  the full side `B`: heavier attachments remain unbounded.  The whole light forest has at most `2tau` edges; its
  root component owns all `tau` low odd values, so at `tau=10`, order eighteen has `|A|>=7,|B|<=11`.  A formal
  `7|11` capacity split nevertheless passes every resulting inequality.  In q=1 coordinates a consecutive visible block across `f` would reflect to a rooted
  interval, but neither that block nor any relation `w>=Q` is proved.  An owner-labelled no-grazing/absorption lemma
  remains **UNVERIFIED**; FW276 has no computation or order exclusion and leaves G18 **UNVERIFIED**.  Full proof and
  stop boundary: `docs/q1-first-positive-edge-cut.md`.
  FW277 contracts the full forest below `w` and selects a leaf bag of the resulting heavy quotient on the
  descendant side of `f`.  Its **OBSERVED** nonroot light-bag excess is at most `tau-1` for `tau>=2`; for `tau=1`
  the light forest is exactly the root unit component, one nonroot edge-2 component and isolates.  Thus a selected
  quotient leaf is a genuine pendant all-even cap of order at most ten and diameter at most 108.  Its exact cut is
  `I_N=F_C+F_R+X^eR_t(C)R_r(R)`, and the four actual rows rooted at `t,r,b,a` forbid the six cap-depth differences
  `1,e,H,H+1,H+e,H+e+1`.  In q=1, an endpoint cap transports the complete visible suffix into disjoint shifted
  blocks.  If `x` is outside a cap containing no visible vertex, its `Qs` visible-by-cap owners give the new
  **OBSERVED owner-labelled area bound**
  `2e+rho+sQ+(s-1)(Q mod 2)<=N-Q-1`; at order eighteen a singleton in this branch has
  `e<=76-Q`.  A saturated cap halves to a Leech tree and, in the full light forest, can occur only at
  `tau=1,s=2`.  The remaining exact stop is already the singleton identity
  `I_N=F_R+X^eR_r(R)`: it retains a nonterminal order-`n-1` rooted row, while the proved invariants do not bound the
  number of heavy singleton bags independently of `n`.  No absorption, same-type descent or order exclusion follows; G18 remains
  **UNVERIFIED**.  Full proof and trust boundary: `docs/q1-light-quotient-cap.md`.
  FW278 audits the two exact successors of that singleton stop and the strict nonpendant cap.  Deleting the unit
  leaf and a singleton heavy leaf gives five named rooted supports with one same-owner overlap, fibrewise at most
  six distinct nonzero forbidden differences, and an **OBSERVED exact** rank-compression criterion: the common
  core becomes a same-topology Leech tree of order
  `n-2` exactly when the external-hole count is additive on every core path.  The known order-six tree shows this
  additivity can fail for a nonendpoint leaf.  In the FW275 hard `x=2` state, the filled virtual row has the exact
  cut flow `sum_f w_f(c_f-l_f)=2E`; combining it with `D<=D_0` prescribes both the number and sum of the outside
  holes.  This rejects the order-nine equality pattern after strict truncation, but no all-order subset-sum
  exclusion is proved.  Finally, the bordered additive distance matrix is integrally congruent to one hyperbolic
  plane plus `diag(-2w_e)`, so its Smith form, modular ranks and inverse sparsity read edge factors rather than
  cross-owner placement.  All three routes are at precise **OBSERVED mechanism-specific STOPs**; no order is
  excluded and G18 remains **UNVERIFIED**.  Full audit: `docs/unit-edge-owner-propagation-audit.md`.
  FW279 makes the requested architecture-level decision: the current pendant/nonpendant/small-`Q` A/B/C route is
  **OBSERVED not closed**.  On the canonical pendant deletion, transformed internal values form a strictly decreasing
  numeric owner forest.  Arbitrary-owner order-`n-2` descent is equivalent to injectivity plus placing its `G` sources
  in the exact top band; after injectivity the remaining displacement has the multiscale identity
  `Delta=sum_(h in H_0)(A_h-B_h)`.  Rank anti-coalescence and the opposite transport inequality are two independent
  **UNVERIFIED** lemmas.  On an arbitrary nonpendant `s|t` unit cut, the strict cap instead requires
  `|H_out|=E-((s-2)(t-2)+2)` with one exact signed cut-flow/subset-sum value.  Actual `D_0+1` and non-strict pressure
  trees show why the cap matters, while two formal `I_36` tilings reach the first and second rooted-LCA pivots and then
  fail; no actual strict counterexample was found.  In the restricted order-eighteen pure-`H` `2|15` wrapper, gate
  packing excludes exactly `Q=10,...,14`; `Q=5,...,9` remain **UNVERIFIED**, and one disclosed Q9 SMT sentinel ended
  `UNKNOWN` without a certificate.  FW279 adds no order exclusion, so G18 and global nonexistence remain
  **UNVERIFIED**.  Full decision and trust boundary: `docs/g18-closure-architecture-audit.md`.
  FW280 then isolates pendant rank anti-coalescence.  A first collision reduces to at most two edge-disjoint arms
  on each side, and the exact identities `def(P)-def(P')=|D intersect (d(P),d(P')]|` and
  `eta(s,w)=|M^+_(s,w)|-|M^-_(s,w)|` retain every internal/external actual owner.  Each mismatch is necessarily
  non-aligned with its prefix, but first-collision minimality cannot choose a common direction for the resulting
  LCA/gate/connector corrections.  A full-spectrum noncanonical `L6` orientation splits them among incompatible
  gates, while an infinite non-Leech exact-top family has a genuine transformed collision even after Taylor parity;
  a temporary 464-row order-six one-gap audit was `UNSAT` but is external/non-replayed and not proof input.  Thus
  canonical top ownership plus full low coverage remains an **UNVERIFIED** joint transport theorem, with the exact
  fallback retaining `Theta(n^2)` owner/LCA data.  FW280 excludes no order and leaves G18 **UNVERIFIED**.  Full stop:
  `docs/pendant-rank-anti-coalescence-stop.md`.
  FW281 tests that joint transport directly.  The exact threshold ledger writes a collision as zero total difference
  on internal ranks and positive old-length drift on external-owner thresholds; transformed Kruskal gives
  `K(j)>=j`, while full injectivity is exactly coefficientwise separation of its rooted merge convolutions.  Canonical
  full-spectrum `L6` has no collision but already has two shadow/lift cycles and AC-2 corrections of both signs, so
  least-threshold, same-root, uniform-sign and local-lift arguments all fail.  A noncanonical `L6` collision passes the
  entire scalar Kruskal schedule, and an odd-parameter non-Leech `Q=4` family passes Taylor parity while colliding.  A
  temporary 232-row `I_4` diagnostic was `UNSAT` but is external/non-replayed.  The 60k checkpoint therefore triggers
  **STOP**: reopening requires global rooted-merge convolution separation coupled to AC-1, not `Theta(n^2)` storage.
  FW281 excludes no order and leaves G18 **UNVERIFIED**.  Full stop:
  `docs/canonical-mismatch-gate-transport-stop.md`.
  FW282 returns to the separate full-window edgewise route and proves an **OBSERVED all-order exact reduction**.
  Contracting full-bidirectional edges does not merely produce some sink: every quotient node has outdegree at most
  one, so the quotient has a unique sink; boundary weights strictly increase toward it and every away basin is a
  strict thin cap.  A nontrivial branched sink has at least three first-level ports.  Its cap/core pair classes have
  an exact actual-owner polynomial partition, and a linear weighted skeleton preserves full-support geometry.  At
  any core leaf, the branch reduces to a one-port thin bouquet versus an arbitrary opposite side with the exact
  colored tiling `[0,N-p]=(U direct-sum V) dotunion H_S dotunion H_R`; both colors are nonempty and the first colored
  hole is at offset at most ten for `n>=18`.  The remaining **UNVERIFIED LPCT** theorem is to exclude this leaf-port
  state using complete coefficient coverage.  A six-vertex actual one-defect pressure tree has a two-vertex branched
  sink and misses exactly the load-bearing coefficient, so support geometry or a finite prefix alone is insufficient.
  The replay checks both independent witness checkers, 9,499 deterministic distance-injective support controls and
  the pressure tree.  FW282 excludes no order and does not prove global nonexistence.  Proof and trust boundary:
  `docs/full-window-quotient-arborescence.md` and
  `theory-lab/topwindow/verify_full_window_quotient_arborescence.py`.
  FW283 independently exhausts the bounded single-leaf-port continuation.  Up to swapping factors, there is exactly
  one first-cross-hole rooted-prefix row for every `eta<=10` except `eta=7`, which is impossible; the extremal
  `eta=10` bouquet is `{0,2,8}` against `{0,1,4,5}`.  A verified affine order-11 actual-tree family realizes this
  state with an owner edge `p+10` whose projection gate is arbitrarily remote, while retaining injective distances,
  thin caps, full support and the unique branched sink geometry.  The family is not Leech, so LPCT remains
  **UNVERIFIED**; it strictly stops only the mechanism that extends one bounded leaf-port prefix one owner at a time.
  The unique next target is a simultaneous two-port capped owner-return invariant using actual owners, projections
  and a common sink connector.  FW283 excludes no order and proves neither G18 nor global nonexistence.  Audit:
  `docs/leaf-port-colored-tiling-stop.md` and
  `theory-lab/topwindow/verify_leaf_port_colored_tiling_stop.py`.
  FW284 proves the requested two-port successor as an **OBSERVED all-order exact reduction**.  On the linear
  full-window skeleton (core edges plus first-level boundaries), the first compensated same-side owner at every edge
  either lies inside one named thin cap and strictly lifts to its heavier boundary, or crosses a uniquely selected
  maximum-weight skeleton edge and returns there as an actual cross owner.  This defines a fixed-point-free total map,
  hence an actual cap-lift/edge-lift/path-drop cycle, with exact balance
  `sum_D rho=sum_cycle eta+sum_cap sigma`.  Known L6 has the genuine positive cycle `5->8->5`, so neither bounded
  prefixes nor the scalar balance exclude cycles.  The remaining **UNVERIFIED NSSC** obligation is to use a
  nontrivial sink-core connector and compose returned endpoint projections around the cycle (endpoint monodromy).
  NSSC is a smaller state obligation, but after FW284 it is logically equivalent to excluding the nontrivial-sink
  branch; FW284 itself excludes no order and proves neither G18 nor global nonexistence.  Proof and audit:
  `docs/skeleton-first-owner-cycle.md` and
  `theory-lab/topwindow/verify_skeleton_first_owner_cycle.py`.
  FW285 then gives a **STRICT STOP** for composing endpoint monodromy from
  that compressed record alone.  An actual order-five distance-injective
  path has a nontrivial full-window sink and a total `8->9->8` FW284 cycle
  whose consecutive first-owner pairs are vertex-disjoint; an order-eight
  control adds a cap lift whose incoming and next owners are also disjoint.
  Neither control is Leech, so they do not refute NSSC.  They prove that the
  existing per-edge records—even with side-specific first owners—do not
  define owner transport.  The new **UNVERIFIED CCOO** successor must reuse
  discarded full-spectrum coefficients to force an immediate edge return,
  shared endpoint, or ordered overlapping core projection.  Audit:
  `docs/skeleton-endpoint-monodromy-stop.md` and
  `theory-lab/topwindow/verify_skeleton_endpoint_monodromy_stop.py`.
  FW286 recovers one exact full-spectrum consequence at every path drop.  In
  the ordered two-cut decomposition `A--q--B--r--C`, the returned owner's
  endpoint-edge lower bound promotes to `w_r>=eta_q+1`; hence every `AC` pair
  starts beyond the translated short band.  Complete coverage forces `AB`
  owners at offsets `0,...,eta_q-1` and the distinguished `BC` owner at
  `eta_q`.  The live path-drop obligation is now only an **UNVERIFIED
  Terminal AB-to-BC Connector** theorem for the last two adjacent owners.
  Cap-to-boundary transport and cycle-composition compatibility remain
  separate; NSSC and nonexistence are not proved.  Audit:
  `docs/two-cut-terminal-owner-switch.md` and
  `theory-lab/topwindow/verify_two_cut_terminal_owner_switch.py`.
  FW287 derives exact crossed-swap and four-point identities for the terminal
  `AB -> BC` owners.  Injectivity confines disjoint endpoints to four integer
  projection/height cones; the critical-path endpoint bound excludes the
  complete left-projection cone, including connector-root and `ell=0` cases.
  The three surviving `R,D,U` modes are all realized by actual non-Leech
  distance-injective trees with nontrivial sinks.  Complete-spectrum
  elimination or monotone transport of those modes, cap-to-boundary transport
  and cycle compatibility remain **UNVERIFIED**.  Audit:
  `docs/terminal-four-cone-reduction.md` and
  `theory-lab/topwindow/verify_terminal_four_cone_reduction.py`.
  FW288 proves the exhaustive local transport output for a single path drop:
  a direct shared endpoint, a `D`-mode earlier `AB` bridge, an `R`-mode
  oriented marked connector interval, or a `U`-mode sub-source-weight `BC`
  bridge.  The local TABC obligation is therefore complete.  Compatibility
  with the next FW284 arc (**UNVERIFIED PRCC**) and cap-to-boundary transport
  remain separate prerequisites for NSSC.  Audit:
  `docs/terminal-local-transport.md` and
  `theory-lab/topwindow/verify_terminal_local_transport.py`.
  FW289 proves the cap-lift endpoint-depth dichotomy and an exact
  four-cross-pair rectangle bound.  Shallow endpoints transport directly;
  equality at the target first offset collides; failure leaves a remote pair.
  An actual non-Leech control realizes that remote state with every rectangle
  cross distance inside `N`, so target-prefix cap transport is a **STRICT
  STOP** mechanism.  Full-spectrum **UNVERIFIED RCRT**, PRCC and cycle
  compatibility remain.  Audit: `docs/cap-endpoint-depth-stop.md` and
  `theory-lab/topwindow/verify_cap_endpoint_depth_stop.py`.
  FW290 proves the target first-owner fork at every path drop.  Equality with
  the old edge's returned offset forces the exact edge-lift return two-cycle;
  strict inequality puts the next owner below the dropped source.  An actual
  control then cap-lifts above that source, strictly stopping scalar
  skeleton-weight descent.  **UNVERIFIED ERTC/SBCC**, RCRT and the remaining
  cycle compatibility are now the live obligations.  Audit:
  `docs/pathdrop-target-owner-fork.md` and
  `theory-lab/topwindow/verify_pathdrop_target_owner_fork.py`.
  FW291 reduces the equality branch to the exact correlated two-root owner
  strip `BC^delta AB^eta BC`.  `L6` realizes complete coverage with a
  singleton sink; non-Leech controls realize nontrivial connectors and the
  complete local strip.  The bounded switchback mechanism is therefore a
  **STRICT STOP**.  **UNVERIFIED ERTC** must use coefficients outside the
  strip and nontrivial connector geometry simultaneously.  Audit:
  `docs/exact-return-switchback-stop.md` and
  `theory-lab/topwindow/verify_exact_return_switchback_stop.py`.
  FW292 combines the entire exact-return zero block with the FW283
  first-cross-hole table.  Of the 81 a priori `(delta,eta)` types, shallow
  convolution returns exclude 23 and rooted internal-distance compatibility
  excludes `(8,1)`, leaving exactly 57 one-root prefix types.  Actual
  shared-depth ownership and two-root triangle/parity then exclude
  `(6,8),(6,9),(6,10),(8,6)`.  Of the three rows forced to `ell=0`, `(8,9)`
  also dies because its depth-8 vertex is forbidden by the opposite first
  hole.  The final matched-shallow state has 50 explicit separated
  distinct-root witnesses and two forced-`ell=0` rows `(8,8),(8,10)`.  This
  is an exact finite reduction, not ERTC:
  complete coefficients beyond the return are still missing.  Audit:
  `docs/exact-return-prefix-classification.md` and
  `theory-lab/topwindow/verify_exact_return_prefix_classification.py`.
  FW293 closes the two forced-`ell=0` rows immediately.  For both `(8,8)` and
  `(8,10)`, FW283 forces rooted depth 2 in each of the disjoint outer parts
  `A,C`; the two distinct internal pairs therefore repeat global distance 2.
  Hence neither parameter type that was forced onto the zero-connector face
  survives.  The other 50 types have separated-root local witnesses, although
  FW293 does not exclude optional coincident-root signatures within them or
  their complete extensions.  Audit: `docs/exact-return-shared-root-collision.md` and
  `theory-lab/topwindow/verify_exact_return_shared_root_collision.py`.
  FW294 aligns the actual owners of distances 1 and 2 across the two cuts.
  If both first holes exceed one, the distance-1 owner forces both inner
  factors to contain depth 1 and restricts the connector to `ell=0` or `1`.
  If both holes are at least three, the distance-2 owner then excludes every
  type except `(3,3)`, which can remain only with `ell=0`.  This removes 20
  more types and leaves 30 necessary parameter pairs: those with
  `min(delta,eta)<=2`, plus `(3,3)`.  Audit:
  `docs/exact-return-unit-owner-alignment.md` and
  `theory-lab/topwindow/verify_exact_return_unit_owner_alignment.py`.
  FW295 shows why the isolated `(3,3),ell=0` row now needs genuinely global
  input.  Four order-seven weighted trees have all 21 distances distinct,
  the full exact-return strip and a two-vertex full-window sink, but are not
  Leech: all first fail coverage at distances 4 and 5.  Their two-vertex
  sinks extend independently through `B` or `C`, so local owner
  alignment plus nontrivial-sink status cannot close this row; a complete-
  coverage low-owner localization lemma is still required.  Audit:
  `docs/exact-return-33-nontrivial-stop.md` and
  `theory-lab/topwindow/verify_exact_return_33_nontrivial_stop.py`.
  FW296 proves `g>=7` in the `(3,3)` row: the exact return already gives an
  internal owner of distance 6, so every smaller target weight repeats that
  owner or one of distances 1--3.  Hence a complete extension must realize
  every `1,...,g-1` internally in `A,B,C`.  Stronger non-Leech controls with
  nontrivial sinks cover `[1,7]` (and a different three-centre topology covers
  `[1,6]`), showing that completing 4,5 and the return is still insufficient.
  The live global target is now the Pre-Target Internal-Gap Lemma.  Audit:
  `docs/exact-return-33-pretarget-gap-stop.md` and
  `theory-lab/topwindow/verify_exact_return_33_pretarget_gap_stop.py`.
  FW297 falsifies that proposed Pre-Target Internal-Gap Lemma.  An explicit
  order-17 tree has 136 distinct pair distances, a four-vertex sink, the exact
  `(3,3),ell=0` return state, and complete global coverage `[1,18]`; with
  `g=10`, all of `[1,g-1]` is internally covered.  It is not Leech (first gap
  19 and 58 outliers), but it proves that no bounded pre-target prefix can
  close the row.  The remaining successor must use the full-range three-part
  internal/cross-distance tiling identity.  Audit:
  `docs/exact-return-33-pretarget-countercontrol.md` and
  `theory-lab/topwindow/verify_exact_return_33_pretarget_countercontrol.py`.
  FW298 converts that full-range obligation into an exact event in the
  increasing-weight forest history.  The three internal parts own
  `[1,g-1]` and avoid the whole seven-value block `[g,g+6]`; the consecutive
  forced merges `r=g` and `q=g+3` then fill that block.  An explicit formal
  order-nine factor tiling satisfies the complete coefficient identity, all
  three top caps, rooted parity, the necessary radius/diameter inequality,
  the first-moment bounds and individually feasible pair triangles, but all
  720 coherent rooted parent maps fail.  The formal tiling is neither a tree
  nor a sink-geometry instance.  Thus cap/scalar/pairwise top data still do
  not close `(3,3)`;
  the smallest live successor is a coherent rooted-LCA obstruction across
  the two forced merges.  Audit: `docs/exact-return-33-forcing-macro.md` and
  `theory-lab/topwindow/verify_exact_return_33_forcing_macro.py`.
  FW299 resolves the smallest target `g=7` through the next forced edge.
  Coherent LCA data puts the depth-six return in `C`, hence it is the single
  edge six; below seven the forced forest is exactly the `1,2` rooted star
  plus isolated edges `4,5,6`.  The consecutive merges `r=7,q=10` then have
  spectrum `[1,15] union {17,23}`, so edge 16 is forced.  Exhausting 39
  join/attach/new representatives on the displayed prefix (unused isolated
  labels already quotiented) leaves 18 distance-injective representatives and
  ten canonical uncoloured forests: nine next force 18 and one next forces 20.
  These ten states are a complete necessary relaxation, not sufficient
  `A/B/C`-root-sink realizations; `g=7` remains open and the live successor is
  owner-aware descent on those states.  Audit:
  `docs/exact-return-33-g7-forcing.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_forcing.py`.
  FW300 restores the first owner data on those ten states.  Six weight-16
  placements force named `A/B/C` rooted depths and four retain one floating
  internal component; the exact local convolution windows remove none.  One
  further exhaustive forced edge gives 75 globally distinct canonical
  uncoloured successors,
  with next gaps `19:61,20:2,21:8,22:3,24:1`.  In the two states joining
  `d_6` to edge 4 or 5, edge 18 is forced to be a new isolated edge.  Two
  `q/r` cut-support witnesses show that all ten states make `q` or `r`
  bidirectional either immediately or after their already forced next edge, so
  none is removed by the local necessary bidirectional-support test for sink
  nontriviality.  Two connected non-Leech controls additionally
  realize different weight-16 states with the same exact return and nontrivial
  five-vertex sinks.  Owner lift plus sink nontriviality still does not close
  `g=7`; the next obligation is a coloured first-successor merge obstruction,
  not deeper uncoloured expansion.  Audit:
  `docs/exact-return-33-g7-owner-lift.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_owner_lift.py`.
  FW301 performs that exact necessary colouring.  Removing `q,r`, independently
  assigning every rootless internal component to `A/B/C`, and retaining the
  rooted components expands the 75 successors to 829 coloured states.  They
  have only five owner signatures below their next missing value
  (`19,20,21,22,24`): any future root connector has at least that weight, so
  those low coefficients are already frozen.  No signature is contradictory.
  A connected order-ten exact-return pressure tree gives the sharp obstruction:
  it forces new isolated edges 19 and 26, then has two weight-27 continuations,
  both next missing 29.  Therefore the live step is a first-root-activation
  packing lemma (the connector-crossing owner-overlap lemma) above the frozen
  threshold, not further colour-only refinement.  Audit:
  `docs/exact-return-33-g7-coloured-freeze.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_coloured_freeze.py`.
  FW302 falsifies the proposed immediate first-root-activation obstruction:
  both weight-27 pressure branches admit the same collision-free weight-29
  `C` activation, whose twenty new owners end at 121 below `N_18=153`; fresh
  edge 30 then survives and moves the hole to 39.  The correct all-order event
  is instead the globally heaviest edge, which is the final root activation.
  Its deletion gives the exact two-component identity
  `I_N=F_K+F_H+X^s R_{K,x}R_{H,y}` with no future repair.  The universal
  count has nonnegative capacity slack, and the established heaviest-edge
  rigidity theorem excludes equality, so the slack is at least one.  The live
  target is a coloured last-activation no-grazing lemma: a rooted
  difference-set overlap, an outlier, or strict inherited descent.  Audit:
  `docs/exact-return-33-g7-last-activation-stop.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_last_activation_stop.py`.
  FW303 combines that exact last cut with the independently verified
  all-order rooted-span bound and finite-hole ladder.  Every hypothetical
  `n>=18` completion now has final-cut slack at least nine, and its first nine
  internal holes above the heaviest edge occur by offsets
  `10,19,22,31,34,37,40,48,51`.  Side colouring forces respectively
  `9,9,8,6,3` of those first holes into the fixed-core side when the rootless
  final cap has order `1,2,3,4,5`.  The fixed edges `1,2,6,7,10` also lie in
  every rooted difference set on that side.  For a two-vertex final cap the
  full problem reduces exactly to the punctured tiling
  `I_N=F_K+X^t+X^sD(1+X^t)`, with `D` disjoint from `D+t`, cap
  `s+max(D)+t<=N`, slack at least 31, and all first nine located holes owned
  internally by `K`.  A connected order-12 pressure control shows that
  difference-set disjointness alone is insufficient.  The live successor is
  the Two-Vertex Final-Cap Punctured-Tiling Lemma; the singleton and `h>=3`
  branches remain separate.  Audit:
  `docs/exact-return-33-g7-final-cap-punctured-tiling-stop.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_final_cap_punctured_tiling_stop.py`.
  FW304 specializes the two-vertex cap all the way to three rooted rows.  The
  complete six-vertex core spectrum forces `t>=4`; the first cross hole is
  exactly one of `1,2,3`, with the attachment root respectively outside the
  weight-one endpoints, at `b_1`, or at `z`.  The only cap regimes are
  `t=4,5` or `t>=16` (the last two root rows also exclude 5).  A new
  missing-slot count strengthens the excess to at least 35 in every row and
  40 in the two fixed-root rows; late caps give 47 and 52.  Root-radius
  counting then locates at least 35 actual `K` owners by offset 66, with
  stronger row-specific windows.  Seven exact specialized first-nine-hole
  ladders and three order-12 pressure controls are independently replayed.
  The live successor is a Root-Localized 66-Window Owner Lemma converting
  that dense actual-owner window into a forbidden rooted difference, an
  outlier, or strict inherited return; the owner LCA/projection term remains
  unproved.  Audit:
  `docs/exact-return-33-g7-two-point-root-window-stop.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_two_point_root_window_stop.py`.
  FW305 fixes the smallest row `R2,t=4`.  An exhaustive rooted-parent replay
  shows that its first seven cross holes are uniquely
  `2,6,9,10,13,16,17`, with no branching through offset 18.  Each actual
  owner path now obeys an all-order endpoint-trim recursion: a small endpoint
  edge must expose one of the earlier forced owners, and the complete fixed
  core leaves only seven named nesting types.  The exact algebra then splits
  the row.  If `2s>N+2`, every such nesting is impossible and all seven paths
  are endpoint-heavy; otherwise at least 45 actual owners occur by offset 79.
  A distance-injective order-eight `t=4` pressure tree shows that the fixed
  root, coherent LCA geometry and first compensated hole alone still do not
  close the row.  The live successors are the Seven-Path Intersection Lemma
  in the high-bridge branch and the denser owner-to-projection lemma in the
  complementary branch.  Audit:
  `docs/exact-return-33-g7-r2-t4-owner-trim-stop.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_owner_trim_stop.py`.
  FW306 runs the exact `R2,t=4` rooted-support ladder with a 44-hole budget.
  All 51,833 peak live supports die while processing offset 70, with every
  compatible fixed-parent/LCA realization exhausted and no beam or state
  cutoff.  Since FW304 already places offset 70 inside every all-order deficit
  span, the row has `sigma>=45` and at least 45 actual internal `K` owners in
  `[s+1,s+70]`.  This improves both the universal 40-owner/73-window and the
  conditional 45-owner/79-window.  The live successor is the 70-Window
  Projection Lemma, retaining the first seven FW305 endpoint records while
  locating the remaining owner paths relative to `b_1--z`.  Audit:
  `docs/exact-return-33-g7-r2-t4-deep-hole-window.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_deep_hole_window.py`.
  FW307 replaces the single 44-hole layer by one exact global-budget replay.
  The induced deaths for budgets 44 through 54 are respectively
  `70,71,72,73,74,75,76,78,80,81,82`; self-consistency with the exact deficit
  span bootstraps every all-order `R2,t=4` state to `sigma>=55` and locates
  the fifty-fifth actual owner by offset 82.  The cold replay exhausts a peak
  536,697 rooted-depth supports.  Audit:
  `docs/exact-return-33-g7-r2-t4-sigma-bootstrap.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_sigma_bootstrap.py`.
  FW308 then retains actual endpoints of the first seven paths and projects
  every FW305 small trim to the fixed six-vertex core.  Six of eight trim
  types are impossible.  The surviving weight-six `d_6` fan and unit-edge
  `b_1` fan are rigid and mutually exclusive, so at least 13 of the 14
  endpoint incidences are heavy.  Actual controls realize all three unit-cut
  colours, each local fan, and a completely endpoint-heavy seven-path family;
  the low spectrum and global cap remain essential.  A remote owner avoiding
  the fixed core lies behind a full-bidirectional sink-core attachment.  The
  live target is the Three-Signature 82-Window Intersection Lemma: exclude
  signatures `N,D,B` by forcing remote thick carriers into a proper inherited
  exact-return descent.  The consultant's proposed historical boundary-thin
  transfer is explicitly not certified or used.  Audit:
  `docs/exact-return-33-g7-r2-t4-projection-signatures.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_projection_signatures.py`.
  FW309 classifies all 55 owner paths relative to the marked core.  A remote
  owner yields an exact simultaneous two-cut identity at a full-bidirectional
  carrier boundary, the edgewise product-45 nine-hole handoff, and named
  opposite-colour internal offsets `eta=s-w` and `eta+h`.  If no owner is
  remote, at least ten actual pairs share one of the six fixed core LCA
  depths and obey a common rooted-depth sum equation.  Three independently
  replayed controls realize one remote carrier, two split remote carriers,
  and a ten-pair common-LCA packet while failing the punctured low spectrum
  and their own caps.  The live target is the Marked-Core Packet Exclusion
  Lemma; a remote carrier is not yet an inherited state because the low
  interval is shared among carrier, complement, and cross classes.  Audit:
  `docs/exact-return-33-g7-r2-t4-marked-core-packets.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_marked_core_packets.py`.
  FW310 combines the two named same-side witnesses at every remote carrier
  with the FW282 full-window arborescence.  The carrier's maximal
  full-bidirectional component must be the unique sink; the nonpendant unit
  edge belongs to that same sink, so the complete marked path from `b_1` to
  the carrier lies inside it.  Every remote owner crosses two distinct
  sink-incidence atoms and its path meets the sink, because no first-level
  strict thin cap can contain a path longer than `s`.  This does not force
  two distinct external ports: an exact order-18 control realizes `P_2` with
  one endpoint in the sink and one behind a single thin cap, while the remote
  star uses two caps attached at one sink vertex.  The live remote target is
  therefore the Anchored Sink-Incidence Packet Exclusion Lemma, still coupled
  to the unchanged ten-fixed-LCA clause.  No inherited low interval or packet
  exclusion is claimed.  Audit:
  `docs/exact-return-33-g7-r2-t4-sink-incidence.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_sink_incidence.py`.
  FW311 chooses the least remote owner and proves that its actual path is
  critical: every proper subpath is below `s`.  Splitting at a rooted
  interior/LCA vertex gives two distinct positive carrier-root differences
  `alpha+beta=s+h_0`.  Directness at the FW309 carrier cut then forces four
  explicit holes in the opposite rooted factor `B`, with an exact finite
  forbidden-value table for all six possible fixed-core gates.  The missing
  step is now the Remote Complementary-Root Reception Lemma: low-spectrum
  ownership by arbitrary pairs does not yet turn either complementary length
  into one of those four rooted depths.  A deterministic order-119 control
  independently realizes all 55 owners in one sink-leaf bouquet while first
  missing five and violating its global cap.  Thus full-window sink geometry
  and the entire near-`s` packet alone do not supply reception.  Audit:
  `docs/exact-return-33-g7-r2-t4-complementary-root-holes.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_complementary_root_holes.py`.
  FW312 chooses the smaller FW311 complementary length and, for every
  `n>=36`, places the paired receiving distances `t,t+4` inside the
  punctured low window.  Their actual owners have nine carrier-cut colorings.
  If both owners cross the cut, rooted support uniqueness reduces the state
  exactly to a shared carrier endpoint, the exceptional `d_6/a` monotone
  row `(3,1)`, or a genuine opposite-direction switch rectangle.  Exact
  controls independently realize J-internal, L-internal, and cross-switch
  paired owners while failing the complete low spectrum and their own caps.
  The live target is Paired Reception Exclusion, using the other two corners
  of the cross rectangle, actual LCA projections, low coverage, and the cap;
  orders `18<=n<=35` remain a separate bounded audit.  No reception or
  remote-packet exclusion is claimed.  Audit:
  `docs/exact-return-33-g7-r2-t4-paired-reception.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_paired_reception.py`.
  FW313 removes FW312's unstructured `18<=n<=35` exception.  Taylor leaves
  only orders 18, 25, and 27 below 36, and the repository's replicated main
  computation already excludes 18.  Exhausting the two remaining orders
  leaves exactly 41 union rows: every gate is `a` or `d_6`, every least
  remote offset is in `{2,6,9,10}`, `24<=s<=33`, and
  `t in {s-4,...,s}`.  Therefore the second receiver `t+4` is one of the
  five exact named final-cap owners at `s,...,s+4`; 35 rows have a fixed
  L-side bridge/cap owner and six use the already named `P_2`.  The live
  bounded target is Top-Strip Reception Exclusion, not an arbitrary
  18-order interval.  No one of the 41 rows is yet excluded.  Audit:
  `docs/exact-return-33-g7-r2-t4-small-order-top-strip.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_small_order_top_strip.py`.
  FW314 makes the two complementary low owners fully explicit at the remote
  carrier cut.  Every non-cap owner is L-internal, J-internal, or cross; up
  to swapping the two values this gives six ordinary signatures plus the
  three cap-owned signatures `4L,4J,4X`.  Twelve independent exact controls
  realize all nine ordered L/J/X pairs and all three cap modes while
  preserving the FW311 four holes, directness, exact return, root shift-four
  exclusion, least remote owner, and canonical sink.  They first miss five
  and fail their own caps.  Thus owner colours and abstract LCA geometry
  alone cannot close reception.  The live all-order target is Evasive
  Complementary-Owner Exclusion, with X-containing modes the most structured
  first branch; the 41 FW313 top-strip rows remain a separate bounded target.
  Audit: `docs/exact-return-33-g7-r2-t4-all-owner-modes.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_all_owner_modes.py`.
  FW315 adds the first full-spectrum ownership layer beyond an X-owner.  If
  `c=w+b+r=s-delta` and `eta=s-w`, the reflected values
  `q_B=b+delta=eta-r` and `q_R=r+delta=eta-b` are positive and strictly below
  `s`.  A Leech tree must therefore give each a unique actual pair owner,
  while FW314 forbids `q_B` as a `B` depth and `q_R` as an `R` depth.  This is
  a **VERIFIED pressure refinement**, not an exclusion: an owner of a distance
  need not be a vertex at that rooted depth, and the FW311 complementary
  subpaths are `R` differences rather than necessarily `u`-rooted arms.  The
  successor is Reflected-Owner Reception; no X signature, remote packet,
  `g=7` state, ERTC, NSSC, order, or global nonexistence claim is closed.
  Audit: `docs/exact-return-33-g7-r2-t4-reflected-owner-pressure.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_reflected_owner_pressure.py`.
  FW316 keeps all six distances in the surviving branched monotone `(3,1)`
  rectangle.  With `D=A-ell` and `S=w+m+kappa`, distance injectivity leaves
  exactly three parameter regimes: `D>=4` off five explicit affine collision
  lines, `D=1,S>=2`, and `D<=-2`.  The middle regime's J pair owns `q+2`; the
  lower regime's L pair owns it exactly on `D=2S+1`; the upper regime has the
  rigid order `L<=q-3<q<q+1<q+3<q+4<J`.  A simultaneous reflected-X pattern
  sharing both original carrier endpoints is also impossible unless
  `delta=w`, when it collapses to the boundary pairs.  This is a **VERIFIED
  exact parameter refinement**, not a rectangle or owner-mode exclusion.
  The next target is Upper-Rectangle Cap-Slack Exclusion: compare the named
  J-pair excess `J-(q+4)=ell-A-1` with `N-(q+4)`.  Audit:
  `docs/exact-return-33-g7-r2-t4-six-distance-rectangle.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_six_distance_rectangle.py`.
  FW317 uses the actual fact that `a` and `d_6` are fixed-core leaf gates.
  Their named coreward depths contain `10,11,12` and `13,14,15`, while the
  two monotone-rectangle L endpoints have depths `b,b+1`.  If both endpoints
  were in non-coreward components of `L-g`, the two crossed endpoint pairs
  against a named consecutive core pair would repeat a distance.  Hence at
  least one endpoint is coreward; exactly one coreward is equivalent to
  `kappa=0`, and both coreward to `kappa>0`.  The boundary `b=0` is separately
  excluded by the fixed distance-one owner.  This is a **VERIFIED incidence
  reduction**, not a rectangle exclusion: abstract injective controls show
  that one-coreward survives consecutive-depth data alone.  The next target
  is the finite actual fixed-core attachment/LCA classification.  Audit:
  `docs/exact-return-33-g7-r2-t4-coreward-incidence.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_coreward_incidence.py`.
  FW318 performs that finite classification.  The actual fixed core has
  three LCA cells at gate `a` and four at gate `d_6`; including the two
  endpoint orientations gives fourteen affine rows.  The
  `d_6/(6,6,6)/O0` row is impossible because the distinct pairs
  `(z,P_0)` and `(d_6,P_1)` both have distance `b+1`.  Its reverse
  orientation survives but forces the five consecutive named owners
  `b,...,b+4`.  This is a **VERIFIED one-cell/orientation exclusion**, the
  first genuine subfamily exclusion after FW314; it is not a full rectangle
  exclusion.  Audit: `docs/exact-return-33-g7-r2-t4-attachment-cells.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_attachment_cells.py`.
  FW319 sharpens the surviving pre-`z` reverse cell.  Endpoint coincidence
  excludes `b=5`; avoidance of the fixed-core spectrum first leaves
  `b=18` or `b>=24`; and the carrier's rooted difference-three condition
  then excludes `b=18,25,26`.  Hence its exact current window is
  `b=24` or `b>=27`.  This is a **VERIFIED parameter-window theorem**, not a
  realization or cell exclusion.  The next target is Isolated-24 Reception:
  decide whether complete low ownership forces another carrier depth at
  rooted difference three from 24 or 25.  Audit:
  `docs/exact-return-33-g7-r2-t4-five-block.md` and
  `theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_five_block.py`.
  The separate `b=27` forced-`L(5,21)` / `J(32)` control then relaxed the
  remaining J32 endpoint leaf assumption: each endpoint was allowed `NONE`,
  a two-edge high path, or a two-leaf high fork.  Hoffman2 job `98806`
  covered 2,016 order-one attachment/port rows, all `INFEASIBLE`, with no
  `UNKNOWN`; the independent replay is
  `VERIFIED_J32_OUTWARD_DEEPER_ARTIFACT` plus
  `VERIFIED_INDEPENDENT_BFS_REPLAY` (artifact SHA-256
  `7849c9b68cfb9b7cd08bb792c3089dbe9360110a3fc4943c96bd4f27f401f754`).
  This is a finite nine-mode control only: arbitrary longer paths, larger
  forks, high Steiner skeletons, and the label-state completeness bridge
  remain **GAP**.  The order-two wrapper is present, but no order-two run is
  claimed until Hoffman2 access and quota are freshly verified.
  After that verification, the wrapper was submitted once as Hoffman2 job
  `98807` (`campus24`, one CPU, observed `RUNNING` on `n1183`).  Its artifact
  has the expected 14,688 rows (10,368 `EDGE`, 2,160 `FWD`, 2,160 `REV`) and
  passes the independent graph/BFS replay, with 13,608 `INFEASIBLE` and 1,080
  `UNKNOWN` (no `FEASIBLE`).  Targeted job `98808` reran exactly those 1,080
  rows at five seconds per row; its final artifact passes the same verifier
  with 14,688/14,688 `INFEASIBLE`, zero `UNKNOWN`/`FEASIBLE`.  This closes the
  displayed finite nine-mode order-two family only; arbitrary high topology
  and the label-state completeness bridge remain **GAP**.
  The next topology-only bridge is Hoffman2 job `98812`: all rooted residual
  trees through order ten with three labelled incidence locations `L5`, `L21`,
  and `J32`.  Its artifact
  `theory-lab/topwindow/results/pro_b27_marked_skeleton_3port_98812.json`
  (SHA-256
  `d80feac9332a3732037d1607f0904fd70bec06a3180a8e3ea5e7499141e2f834`)
  reports `VERIFIED_MARKED_SKELETON_CATALOGUE_3PORT`, with `601832` canonical
  marked rooted states.  This is only a finite topology catalogue; low
  component shapes, ordered high-edge tuples, admissible weights, full pair
  distances, and complete-spectrum closure remain **GAP**.
  Hoffman2 job `98813` then combined this with the low-component port
  extractor: all `1,809` rooted instances through order ten and all `680,961`
  low/high edge partitions round-tripped with every rootward port and every
  high-edge endpoint incidence retained.  The artifact
  `theory-lab/topwindow/results/pro_b27_low_component_port_skeleton_roundtrip_98813.json`
  (SHA-256
  `485640a1b630e95c05187c04fd85b66a46f22d9981824b939f23a8310cfc4d57`)
  reports `VERIFIED_LOW_COMPONENT_PORT_SKELETON_ROUNDTRIP`, with `3,657,039`
  component records and `2,976,078` high-edge incidences.  This is a finite
  structural bridge only; weights, complete spectra, and least-remote/descent
  completeness remain **GAP**.
  An independent Prüfer-tree implementation (without NetworkX or the primary
  generator) replayed the port and reconstruction invariants through order six:
  `1,441` labelled topologies, `8,476` rooted instances, and `259,384`
  low/high partitions, all passing.  It returns
  `VERIFIED_INDEPENDENT_LABELLED_PORT_REPLAY`; this remains finite and
  unweighted.
  The attempted order-seven exact label-state expansion (`98814`) timed out at
  30:13 with zero-byte output and is not evidence.  The order-six replacement
  (`98820`) covered 55,300 rows and passed independent graph/BFS replay, with
  53,137 `INFEASIBLE` and 2,163 `UNKNOWN`.  One-second targeted rerun `98823`
  resolved 365, leaving 1,798 UNKNOWN; five-second rerun `98826` targets only
  those remaining rows.  Its final artifact has SHA-256
  `b9d7e3dcc9f0401a3d2eb7c832e02b881d8c41b0c8668c1021647470807c382d` and
  passes independent verification with `55,300/55,300 INFEASIBLE`, zero
  UNKNOWN/FEASIBLE.  The two reruns changed only solver status/time fields;
  the exact order-six finite model is therefore closed, while global
  attachment/LCA and Label-State Completeness remain **GAP**.
  The earlier
  34-row relaxation (and the larger original set of 64) nevertheless has the same independently
  audited **OBSERVED conditional constant-deletion core output**: cutting the lower deficit band at `2T` leaves a
  proper connected induced subtree of order at least `n-23` and diameter at most `N-12` (the three `K=2` rows have
  the stronger diameter bound `N-24`).  The certificate freezes the extremal 23/12 constants over all passing
  `K=3` extensions.  This historical core statement was not by itself an exclusion or global descent theorem; that route
  would have needed an inheritance step preventing the omitted endpoint pieces from growing such a shallow core back
  into a Leech tree.  The same certificate also
  freezes `N-2q<=2` and `q-L_0<=30` over the 61 `K=3` rows; the three explicit `K=2` rows obey stronger/equal bounds.
  Recomputing the correlated constants after FW163--FW164 sharpens the earlier 34-row relaxation, and hence the
  now-excluded final 8 rows, to `q-L_0<=22` and
  `2L_0>=N-28`.  Their inherited core therefore misses at most 21 values below `q` and satisfies
  `w_{k+1}<=Pi_k+22`.  This **OBSERVED conditional refined mass/inheritance theorem** is replayed by
  `theory-lab/topwindow/verify_endpoint_terminal_mass_refined.py`; it is not yet the missing descent.
  Reusing the FW78 low-pair capacity count now forces a proper complete lower arm or connected all-low core of order
  `((3-sqrt(7))/2)n+O(1)=0.177124...n+O(1)`, improving the previous terminal constant `0.115562...` without widening
  the search.  Jointly packing the non-shallow vertices, rather than maximising the two capacity terms separately,
  sharpens the same conclusion to `((4+sqrt(2))/28)n+O(1)=0.1933647700...n+O(1)`, with exact structure-order bounds
  `7,8,10,11,13,14,16,17` before row correlation.  Keeping each row's actual pole orders and low-spectrum loss
  improves the target bounds to `8,9,11,11,14,14,17,17` at `n=36,38,49,51,64,66,81,83`.  This is an **OBSERVED conditional all-order terminal mass reduction** proved on the earlier relaxation, not its global absorption;
  the separate arithmetic replay is `theory-lab/topwindow/verify_endpoint_terminal_mass.py`.  In its complete-arm
  branch, the all-order rooted-span bound now gives an exact follow-up: either the complementary side contains at
  least `n^2/50-3n/10+1` internal pairs above the arm edge, or that edge has cut product greater than `4n^2/25`.
  This **OBSERVED conditional interface** reaches the thick-tip/weighted-edge-excess dichotomy but does not yet
  contradict either branch.  A balanced cut product is not necessarily a balanced Kruskal merge product; the exact
  singleton-centre decomposition instead forces a merge of at least half the cut size or an explicit reverse-order
  waste term.  Consequently the balanced-cut branch satisfies the **OBSERVED conditional** lower bound
  `TW>=n^4/625-O(n^3)` (exactly `3016,3364,8878,11704,25912,32108,71925,75624` at the first displayed targets).
  That historical route would additionally have needed a conflicting waste upper bound.  The alternative all-low connected core has a parameterised exact routing: for every fixed `d>=2`,
  either it contains a complete lower arm of order at least `ceil((Khat_n-1)/d)`, or its centre supports more than
  `(Khat_n-1)+(d-1)(Khat_n-1)^2/(2d)` distinct lower cross pairs below `q`.  Hence the earlier 34-row relaxation (indeed all
  64 rows before the sharper filters), and therefore the eight rows later excluded by FW202, feed a linear thin arm or a quadratic thick centre, an **OBSERVED conditional
  all-order routing theorem**; exclusion of those two global
  outputs remains **UNVERIFIED**.
  Independently of that large-structure routing, every one of those eight rows' full lower cores has order at least `n-5` and misses at most 21
  values from `1,...,q-1`.  Sorting its edges by weight therefore gives the inherited covering schedule
  `w_{k+1}<=Pi_k+22` at every rank.  This is an **OBSERVED conditional defect-21 inheritance theorem**, not a claim
  that the core is itself Leech; turning the constant-defect schedule into descent or contradiction remains
  **UNVERIFIED**.
  The exact FW78 pair partition is much sharper below the receiving edge `t`: no pole-to-core pair occurs below
  `t`, and the only possible non-core values are internal to the two pole factors.  Since FW77 gives `t>h`, every
  lower-core edge lies in this localized interval.  Consequently those 8 `K=3` rows have at most two holes
  below `t`; the three former `K=2` rows had respectively three, four and three, so the earlier 34-row relaxation satisfies the all-rank
  schedule `w_{k+1}<=Pi_k+5`.  This is an independently replayed **OBSERVED conditional defect-four
  prefix-inheritance theorem**, not yet a repair, descent or exclusion; see
  `theory-lab/topwindow/verify_endpoint_terminal_prefix_defect.py`.
  Composing these genuine missing values with the existing finite-hole rooted-sum ladder now gives an internal
  directional handoff at every lower-core edge `w`: either `t-w<=34`, or one component of `C_0-w` contains a pair
  of distance in `{w+1,...,w+34}`.  The bound is 22 on every `K=3` row and `31,34,31` on the three `K=2` rows.
  This **OBSERVED conditional bounded internal-handoff theorem** is replayed by
  `theory-lab/topwindow/verify_endpoint_terminal_core_handoff.py`.  It prevents the two poles from supplying the
  handoff, but does not yet force a heavier edge on its path or make successive choices nested; that final
  direction/thick-centre dichotomy remains **UNVERIFIED**.
  Nevertheless, contracting the at most 34 lower-core edges with `t-w<=34` and orienting every other edge by its
  internal handoff yields a sink component containing at most 35 vertices.  This elementary **OBSERVED conditional
  bounded-sink reduction** replaces an unbounded reversal corridor by a fixed-size lower-core centre.  Its incident
  branch complements remain unbounded, so combining this new sink with the thin-arm/quadratic-thick-centre output
  is the next step, not a finished exclusion.
  The hole-eight ladder row strengthens this edgewise to at least five distinct inward core pairs by offset 51
  (at least seven on `K=3`, and `6,5,6` on the three `K=2` rows), audited by
  `theory-lab/topwindow/verify_endpoint_terminal_core_handoff_multiplicity.py`.  Also, every edge in
  `[t-34,t-1]` must be incident with `v`; an internal arm edge there would make one `v`-depth exceed `h`.
  Hence the 35-point sink is only a star at `v` or a singleton.  Absorbing each near incident arm, which has order
  at most 34, gives an **OBSERVED conditional star-sink reduction** of order at most 1157 with every boundary
  handoff directed inward.  The unbounded far arms, rather than an unbounded centre, are now the remaining issue.
  Every edge `u` internal to one of those far arms satisfies `u<=floor((h-1)/2)`: its still heavier incident edge
  lies on the same `v`-path.  Since `h>=134`, it is more than 51 below `t`, so the fivefold FW169 handoff applies
  throughout every far-arm interior (sevenfold for `K=3`).  This **OBSERVED conditional internal-arm multiplicity
  theorem** leaves only the `v`-incident boundaries exceptional; the unresolved question is whether all interior
  handoffs can point back toward the fixed star without forcing the thick-centre contradiction.
  Phase I also removes the remaining branch-count slack.  The three now-excluded `K=2` rows had to contain exactly one hidden lower
  splitter besides `v` (the order-three pole root is the third branch vertex), while every `K=3` row must contain
  exactly two lower splitters besides `v`, in a chain or fork.  By the audited exactly-three-branch normal form, all
  off-skeleton components are bare paths.  This **OBSERVED conditional exact-skeleton reduction** does not delete a
  row—the splitters may be invisible below the forced band—but reduces the unbounded problem to weighted corridors
  on a fixed three-centre skeleton.
  The Kruskal waste now has the exact refinement
  `TW=(sum Delta_k^2-N)/2+sum Delta_k sigma_{k-1}`.  Hence every internal fivefold handoff either contains a heavier
  edge in the same proper side (strict nested descent), or forces covering surplus at least five at that edge.
  Internal merge products sum to `I_R`, so if every corridor handoff reverses toward the star then
  `TW>=(sum Delta_k^2-N)/2+5I_R` (`+7I_R` for `K=3`).  This **OBSERVED conditional
  nested-descent-versus-waste theorem** gives reverse handoffs a global additive cost; a matching thick-terminal
  waste upper bound is still **UNVERIFIED**.
  Direct cut capacity makes this grow with `n`: if an internal edge `u` cuts core orders `s,m-s`, it has at least
  `max(9-e,floor(h/2)+R-e-s(m-s))` same-side pairs above `u`, where `e<=4`.  Hence a bare leg of order at least
  `((1-1/sqrt(2))/2)n+O(1)=0.146446...n+O(1)` either yields nested descent or contributes at least
  `((sqrt(2)-1)/48)n^3+O(n^2)` weighted covering surplus.  The exact target-order leg thresholds are
  `6,6,8,8,10,10,12,13`, with uniform surplus totals `315,380,861,987,2013,2220,4191,4520`.
  This **OBSERVED conditional cut-capacity/cubic-waste theorem** is replayed by
  `theory-lab/topwindow/verify_endpoint_terminal_cut_capacity.py`; the complementary several-short-leg thick centre
  remains **UNVERIFIED**.
  On a bare branch-skeleton corridor the cut side orders are consecutive, so the same `kappa(s)` sums edge by edge.
  Since its growing term is positive outside
  `[alpha,1-alpha]`, `alpha=(1-1/sqrt(2))/2`, every fully reversing linear corridor either pays cubic surplus on its
  unbalanced tails or leaves two endpoint blocks each of order at least `alpha(n-O(1))`.  This **OBSERVED conditional
  corridor-to-two-thick-blocks reduction** makes the final uncharged geometry explicit; excluding those two blocks
  remains **UNVERIFIED**.
  Retaining the actual Kruskal merge products on a bare pendant leg strengthens the cubic charge: the first `r`
  leg cuts have cumulative merge product at least `binom(r+1,2)`, so Abel summation replaces `sum kappa(s)` by
  `sum s kappa(s)`.  The resulting **OBSERVED conditional merge-product amplification** is
  `((8sqrt(2)-11)/768)n^4+O(n^3)`; the exact target-order lower bounds are
  `675,850,2380,2800,6990,7860,17776,19656`.  It is audited by
  `theory-lab/topwindow/verify_endpoint_terminal_merge_amplification.py`.  Its coefficient is not alone a global
  contradiction, so aggregation across the fixed skeleton remains **UNVERIFIED**.
  For a complete bundle of short pendant arms at one non-root lower-core branch centre, that aggregation is now
  **OBSERVED conditional all-order**: every selected edge is internal to a lower arm rather than incident with `v`;
  if the bundle has total off-centre order `V`, maximum arm order `S<=m/2`, and no selected handoff contains a
  nested heavier edge, then
  `sum Delta_e sigma_e >= kappa(S) binom(V+1,2)`.  In particular a linear bundle mass `beta n` with maximum arm
  `gamma n`, `gamma<(1-1/sqrt(2))/2`, pays
  `beta^2(1/8-gamma(1-gamma))n^4/2+O(n^3)`.  This removes the former per-leg loss at a non-root diffuse centre;
  the exceptional bundle incident directly with `v`, combination with the long-corridor charge, and the matching
  terminal waste upper bound remain **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_star_bundle.py`; frozen summary:
  `theory-lab/topwindow/results/endpoint_terminal_star_bundle_certificate.json`.
  The exceptional root bundle is now quantitatively smaller.  One farthest vertex from each component of
  `C_0-v` has a distinct root depth, and its cross-arm distances are the restricted pair sums of those depths;
  they therefore form a weak Sidon set in `[0,h-1]`.  Kayll's Ruzsa bound
  `f(H)<=sqrt(H)+O(H^(1/4))` is **LITERATURE**, while the root-arm reduction and its exact finite difference
  replay are **OBSERVED conditional all-order**.  They give `d_v<=n/2+O(sqrt(n))` and hence at least
  `n/2-O(sqrt(n))` non-`v`-incident lower-core edges.  At the eight target orders the exact uniform root-arm
  upper bounds are `25,27,33,34,42,43,52,53`, leaving at least `5,6,10,12,16,18,23,25` nonincident edges.
  This is not an exclusion: many order-two arms can still send every interior handoff back toward `v`.
  Replay: `theory-lab/topwindow/verify_endpoint_terminal_root_arms.py`; literature/application boundary:
  `docs/literature-ledger.md` L21.
  Those root arms can nevertheless be aggregated through path slack.  If their incident weights are
  `p_1<...<p_d`, every prefix is weak Sidon and the exact FW178 inequality forces `p_i>=G(i)+1`; meanwhile the
  two-edge path between their first vertices has slack `min(p_i,p_j)`.  Hence
  `TW_root>=J(d)=sum_i(d-i)(G(i)+1)`; choosing `q=floor(sqrt(i))` in that exact inequality gives the
  **OBSERVED conditional all-order** consequence
  `d=beta n+O(1) => TW_root>=beta^4 n^4/12-O(n^(7/2))` without a literature input.  At the finite split
  `d>=ceil(n/4)`, the exact charges are `167,250,713,713,1707,2214,5544,5544`; below that split at least
  `22,24,31,34,43,45,55,58` core edges are non-`v`-incident.  This is a root-slack-versus-three-quarter-edge
  dichotomy, not an exclusion: the missing step is still a terminal waste upper bound or aggregation of the sparse
  branch.  Replay: `theory-lab/topwindow/verify_endpoint_terminal_root_slack.py`.
  The sparse-root edge mass now also aggregates componentwise.  Writing
  `s_i` for the orders of the components of `C_0-v`, connected-subtree merge
  mass and FW174 give
  `TW>=max(J(d_v),sum_i kappa(s_i)binom(s_i,2))` whenever `s_i<=m/2` and no
  nested heavier-edge descent occurs.  Hence if every `s_i<=m/8`, the exact
  FW179 span bound yields the **OBSERVED conditional all-order** consequence
  `TW=Omega(n^(16/5))`; otherwise a linear thick root component remains.
  This is an aggregation/reduction, not an exclusion: the fixed one-/two-
  splitter thick component and the missing terminal `TW` upper bound remain
  **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_component_aggregation.py`.
  The linear thick component has now been reduced without any topology
  enumeration.  Put `tau=floor(m/8)`: either an internal edge cuts off two
  blocks both of order at least `tau+1`, or all its smaller cut sides are at
  most `tau` and FW174 plus connected-subtree merge mass pays
  `kappa(tau)binom(tau+1,2)=Omega(n^4)`.  Together with FW180 this gives the
  **OBSERVED conditional all-order** alternative: nested heavier-edge
  descent, a linear two-thick-block cut, or `TW=Omega(n^(16/5))`.  It is not
  an exclusion; the thick-cut collision/waste argument and a terminal `TW`
  upper bound remain **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_thick_component.py`.
  For that thick cut, an edge of weight `u`, full cut product `c`, and
  Kruskal merge product `Delta` satisfies the exact cross-path bound
  `TW>=binom(Delta,2)+u(c-Delta)`.  Since `c=Omega(n^2)`, the FW181 balanced
  edge either has `u<m^(6/5)+1` or pays `TW=Omega(n^(16/5))`.  This is an
  **OBSERVED conditional all-order** scale reduction, not an exclusion: a
  subquadratic-weight linear separator and the missing terminal `TW` upper
  bound remain **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_balanced_edge_slack.py`.
  The defect-four core schedule adds a disjoint same-side slack term.  With
  `H=[t-u-1-e-r(m-r)]_+`, either one of those paths gives nested heavier-edge
  descent or `TW>=F(r(m-r),u)+H(H+3)/2`.  Combining this with FW182 makes
  every fixed outer balanced band quartic and forces any survivor below the
  `n^(16/5)` scale to have `|r-m/2|=O(n^(4/5))`.  This is an **OBSERVED
  conditional all-order** near-bisection reduction, not an exclusion; the
  low-weight near-bisection and terminal `TW` upper bound remain
  **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_balanced_edge_holes.py`.
  The FW172 fixed skeleton now absorbs the near-bisection outcome.  The side
  away from `v` consists, up to two splitter vertices, of at most two bare
  corridors and two complete non-root pendant bundles.  Any linear pendant
  bin is quartically charged by FW176/FW177; a linear corridor has only
  `O(n^(4/5))` near-bisection edges and its remaining linear tail is
  quartically charged by FW174 plus connected merge mass.  Thus the sparse-
  root milestone now gives the **OBSERVED conditional all-order** synthesis
  “strict nested heavier-edge descent or `TW=Omega(n^(16/5))`.”  It is not
  an exclusion: descent closure and a terminal `TW` upper bound remain
  **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_sparse_synthesis.py`.
  Retaining every vertex of each root component strengthens the root term to
  `sum_{i<j}s_i s_j(G(i)+1)`.  With `Q=sum s_i^2`, FW180 pays
  `Omega(n^2Q)` in the concentrated case, while Cauchy plus the quadratic
  weak-Sidon weight at index `Theta(n^2/Q)` pays `Omega(n^6/Q^2)` in the
  diffuse case.  Optimization upgrades the endpoint synthesis to the
  **OBSERVED conditional all-order** alternative “strict nested heavier-edge
  descent or `TW=Omega(n^(10/3))`.”  This is not an exclusion; descent
  closure and a terminal `TW` upper bound remain **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_weighted_root_slack.py`.
  The constant-window part of that descent is now well founded.  Every heavy
  FW167 handoff raises its edge weight by at most 34; every FW169 multiplicity
  handoff raises it by at most 51.  Since the lower core has only `m-1` edges
  but an internal arm edge is quadratically far below the near-`t` window,
  the **OBSERVED conditional all-order** bounded-ascent theorem forces, for
  `n>=271`, termination at a light handoff with `sigma>=1`; for `n>=407` it
  forces a fivefold light terminal with `sigma>=5` (`>=7` in `K=3`).  This is
  not an exclusion: different ascent chains may coalesce, and the larger-
  offset FW174/FW185 descent still requires closure.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_bounded_ascent.py`.
  The terminal waste ledger is now truncated at the globally heaviest edge
  `q`.  Exactly,
  `TW=binom(N-q+1,2)+RW_q`; on every current affine row the fixed first term
  is `n^4/32+O(n^3)`.  With final excess
  `E_q=N-a(n-a)-q+1=n^2/4-O(n)`, the residual is
  `RW_q=sum_{i<r}binom(Delta_i,2)-binom(E_q,2)+sum_{i<r}Delta_i sigma_{i-1}`.
  This **OBSERVED exact accounting theorem** identifies the real endgame as
  a quartic pre-`q` compensation problem.  It is not an exclusion or upper
  bound: in particular the truncated base may be negative, so the FW185
  lower bound cannot be added blindly to the fixed top triangle.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_truncated_waste.py`.
  The same residual identity now forces an **OBSERVED exact all-order
  concentration dichotomy**.  If `D` is the largest pre-`q` merge product,
  `Z` the largest pre-`q` covering surplus, `S` the pre-`q` pair mass and
  `E=E_q`, then
  `D+2Z>=1+ceil(E(E-1)/S)` and hence
  `max(D,Z)>=ceil((1+ceil(E(E-1)/S))/3)=n^2/24-O(n)` on every current affine
  row.  The `D` branch contains a light-edge cut with both sides linear in
  `n`; the `Z` branch contains a quadratically overfilled threshold.  This
  is not an exclusion or residual upper bound; the two branches still need
  separate geometric contradictions.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_compensation_concentration.py`.
  The concentration is now localised in the truncated ledger.  For a pre-`q`
  edge `w`, the large-merge paths contribute at least
  `sum_{j<Delta_w}min(j,q-w)`, while a surplus `sigma` contributes the future
  area `sum_{j=0}^{q-w}max(sigma-j,0)`.  If `M` is the FW188 threshold, this
  gives the **OBSERVED exact** alternative
  `RW_q>=binom(M,2)` or a witness of size at least `M` lies in
  `q-M+2,...,q-1`.  FW171 excludes all non-incident lower-arm edges from that
  band.  Uniformly for `n>=124`, a large-merge witness also cannot lie in a
  bounded outer factor, so it is a `v`-incident lower-arm edge; a high-surplus
  witness may additionally occupy one of at most seven pre-`q` outer edges.
  This is a localization theorem, not an exclusion or residual upper bound.
  Replay: `theory-lab/topwindow/verify_endpoint_terminal_top_localization.py`.
  A stronger **OBSERVED exact all-order transfer** now places the quadratic
  event at one named edge without assuming `RW_q=o(n^4)`.  Let `p` be the
  heaviest lower-core edge, `m=n-a-b`, and
  `O=binom(a,2)+binom(b,2)+bm`.  Then `p` is `v`-incident,
  `Delta_p=s(m-s)`, and the final excess telescopes to
  `sigma_p+Delta_p>=E_q-O`.  Consequently
  `max(sigma_p,Delta_p)>=ceil((E_q-O)/2)=n^2/8-O(n)`.  The merge branch is a
  root cut with smaller side at least `0.146446...n-O(1)`; in the surplus
  branch the already-connected root side has order `n/2-O(1)`.  This removes
  quadratic-scale basin coalescence, but is not yet an exclusion or an
  `RW_q` upper bound.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_core_boundary_transfer.py`.
  The large-merge half is now charged wholly inside `RW_q`.  If the last arm
  has order `s` and root eccentricity `theta`, its `binom(s,2)` distinct
  internal distances force `theta>=ceil(binomial(s,2)/2)`; hence
  `q-p>=Q+theta`.  Combining this runway with
  `Delta_p=s(m-s)>=n^2/8-O(n)` gives the **OBSERVED conditional all-order**
  bound
  `RW_q>=((7-4sqrt(2))/2048)n^4-O(n^3)`.  This safely resolves the merge
  branch for any future residual upper bound, but is not yet an exclusion;
  the high-surplus root-boundary branch remains.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_merge_runway.py`.
  The high-surplus half is now closed at the same residual scale by peeling
  lower arms in decreasing incident weight.  Peeled order `z` contributes at
  most `U(z)=z(m-z)+binom(z,2)` later merge mass, so while `z<n/16` every next
  incident edge has `max(Delta,sigma)>=n^2/16` for `n>=133`.  Large `Delta`
  invokes the FW191 runway charge; large `sigma` under a subquartic residual
  makes each peeled arm `o(n)` and its incident weight `q-o(n^2)`.  Once the
  peeled order reaches `n/16`, quadratically many cross-arm distances would
  occupy only `o(n^2)` top slots, contradicting uniqueness.  The resulting
  **OBSERVED conditional all-order** bound is the explicit
  `RW_q>=10^(-6)n^4` for all sufficiently large `n` in the current affine
  terminal.  This closes the lower-bound side, not the project: a conflicting
  upper bound for the same `RW_q` is still **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_surplus_peeling.py`.
  Retaining the exact quadratic suffix term and peeling to `n/7` strengthens
  this to the independently audited **OBSERVED conditional all-order** bound
  `RW_q>=n^4/25000` for all sufficiently large `n`; replay:
  `theory-lab/topwindow/verify_endpoint_terminal_surplus_peeling_sharp.py`.
  The exact identity `RW_q=sum_P(min(d(P),q)-maxedge(P))` then localizes all
  but `O(n^3)` of the residual inside the order-`n-O(1)` lower core `C_0`.
  Consequently **OBSERVED conditionally**, `RW_C>=n^4/50000`, and a positive
  density of core paths has quadratic capped slack.  FW165 also gives its
  exact defect-21 schedule formula.  This is not yet an exclusion: the
  stability/collision theorem for that near-full fixed-skeleton core remains
  **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_core_residual.py`.
  The threshold forest obtained by deleting every core edge above
  `q-ceil(n^2/100000)` now localizes this slack exactly.  One of its
  components has order at least `(1/2-1/50000)n-O(1)`; and, once FW194's
  pair-density conclusion is active, the exact three-branch skeleton gives
  either a low-edge ancestor chain of order `n/80000-O(1)` or one branch
  centre with `n/200-O(1)` low-edge descendants.  This is an independently
  audited **OBSERVED conditional all-order** localization, not yet the
  required collision or `RW_C` upper bound; those remain **UNVERIFIED**.
  Replay: `theory-lab/topwindow/verify_endpoint_terminal_slack_components.py`.
  In fact the surviving `K=3` rows have a sharper prefix core.  A core edge
  of weight exactly the root height `h` can only be the unique edge from the
  centre to a leaf; deleting that optional leaf preserves every distance
  below `h`.  Since the two pole orders are at most two, FW166 then leaves a
  connected induced core of order at least `n-5` containing all but at most
  two values of `[1,h-1]`, where `h=(N-E)/2` and `E<=26`.  This independently
  audited **OBSERVED conditional all-order** defect-two prefix stability is
  not yet a Leech subcore or collision; the fixed-three-centre defect-two
  theorem remains **UNVERIFIED**.  Replay:
  `theory-lab/topwindow/verify_endpoint_terminal_almost_prefix_core.py`.
  The first of those affine rows, `P=U={0}, Q=2, R=1`, now closes after 50
  exact coefficients.  A 5,552-configuration chain/fork replay explicitly
  covers both lower splitters when visible or shallow, safely relaxes deeper
  inactive LCAs, reaches no cap, and has no frontier; its all-height map
  separates low, root-depth and high distance bands uniformly for `h>=259`.
  This independently audited **OBSERVED conditional all-order** exclusion
  leaves 30 `K=3` rows and is not yet the full endpoint contradiction.
  Replay: `theory-lab/topwindow/verify_endpoint_k3_first_row.py`.
  Seven more affine rows close after only 30 coefficients.  Their exact
  chain/fork replay covers 13,874 configurations with no frontier, unknown or
  cap hit (maximum 2,933 states in a layer); its per-row recurrence and
  low/middle/high height-translation signatures are frozen in the certificate.
  This independently audited **OBSERVED conditional all-order seven-row
  exclusion** leaves 23 `K=3` rows, not a complete endpoint contradiction.
  Replay: `theory-lab/topwindow/verify_endpoint_k3_h30_rows.py`.
  Four more rows close under the same 30-coefficient relaxation after the two
  expensive chain-visible families are partitioned into exact marker shards.
  The 1,892-shard production replay covers 7,928 configurations with no
  frontier, unknown or cap hit and at most 13,572 states in a layer.  This
  independently audited **OBSERVED conditional all-order four-row exclusion**
  leaves 19 `K=3` rows; it is still not the endpoint contradiction.  Replay:
  `theory-lab/topwindow/verify_endpoint_k3_h30_split_rows.py`.
  Eleven more rows close in a persistent-worker sharded replay: 5,203 tasks
  partition 21,802 configurations exactly, with no frontier, unknown or cap
  hit and at most 5,320 states in one layer.  The independently audited
  **OBSERVED conditional all-order eleven-row exclusion** leaves eight `K=3`
  rows, each with a genuine relaxed H=30 frontier but still no witness.
  Replay: `theory-lab/topwindow/verify_endpoint_k3_h30_remaining_rows.py`.
  Raising the exact represented prefix to H=40 for seven rows and H=50 for
  the eighth closes every one of those frontiers.  The 7,079-shard replay
  partitions 30,346 configurations exactly, with no frontier/unknown/cap hit
  and at most 5,246 states in a layer.  Combined with the earlier K2 result,
  this independently audited **OBSERVED conditional all-order exclusion**
  closes the present at-most-three-global-branch two-small-factor affine
  terminal.  It is not the global theorem.  Replay:
  `theory-lab/topwindow/verify_endpoint_k3_final_mixed_rows.py`.
  Hence the inherited-cap route is now a genuinely well-founded **OBSERVED** descent into the existing
  thin/thick interface; the endpoint itself now returns internally and the three-branch two-small-factor branch is
  excluded at its affine terminal, while the thick-surplus and separate lower-core outputs remain
  **UNVERIFIED**.  The stronger shortcut “the original gap edge always cuts off a thin cap” is false without further
  hypotheses,
  as recorded by an OBSERVED negative diagnostic in
  `theory-lab/topwindow/verify_rooted_gap_transition.py`.  When the
  extra-low-cross defect is the large one, the vertices within `q/2` of the
  centre additionally induce a proper subtree of order at least `(1-sqrt(26/27))n-O(1)` (about `0.01869n`)
  whose entire internal spectrum is below `q`.  Cutting at `t` also inherits an exact reflected prefix of length
  `mu-h`; when `t>h`, the gap `R=t-h<=4(n-1)` either hands to an edge wholly inside the `mu`-arm (apart from an
  explicit symmetric factor) or makes that arm another pole of order at most four.  The finite-hole ladder removes
  most remaining directional ambiguity: for every `n>=36`, either `q-t<=40`, or the proper core consisting of the
  centre and all lower arms contains a pair at one of `t+1,...,t+40`.  Thus the large-order pole is now a bounded
  two-heavy-edge cluster or a strict handoff into a linearly large lower core.  The cluster itself also routes:
  if the third height exceeds `t`, that height is already a lower-core near-`t` pair; otherwise the reflected
  `t`-cut hands back into the `mu`-arm.  The apparent symmetric exception is not new: the complete digit-block
  structure plus the existing rooted collision classification forces every such factor to have order at most four.
  If both top factors are small, the remaining state has fixed width:
  `1<=t-h<=16`, `q-h<=56`, and the `q`-cut prefix has length at most 112; moreover one of the two top-side gaps is
  at most 16.  Exact low-spectrum counting then forces either one complete lower arm or the centre's `q/2`-shallow
  induced core to have at least `((9-sqrt(69))/6)n-O(1)` vertices (about `0.11556n`).  Thus even the fixed-width
  terminal descends to a linear proper structure.  Bringing these lower-core structures into the new cap recurrence,
  and excluding its deep-offshoot endpoint terminal, remains **UNVERIFIED**.
  Excluding these three
  interfaces and non-singleton thick components remains **UNVERIFIED**.  Audits:
  `theory-lab/topwindow/verify_singleton_thick_centre.py` and
  `theory-lab/topwindow/verify_rooted_gap_transition.py`.
- OBSERVED / UNVERIFIED — the small-weight side now has a matching global invariant.  In Kruskal weight order, if edge `k`
  merges component sizes `a_k,b_k`, then `Delta_k=a_k b_k`, `sum Delta_k=N`, and the next weight satisfies the exact covering
  schedule `w_{k+1}<=1+sum_{j<=k}Delta_j`.  The total path slack obeys the identity
  `TW=sum_P(d(P)-maxedge(P))=N(N+1)/2-sum_k w_k Delta_k` and the lower bound
  `TW>=(sum Delta_k^2-N)/2`.  Proof and audit: `docs/kruskal-covering-waste.md`.  A topology-uniform upper bound that
  contradicts this forced waste for thick terminal profiles remains UNVERIFIED.
- UNVERIFIED — fixed order-25 exhaustions help the global theorem only when their case trees are exported as
  parameter-independent transition lemmas; a zero solution count at one order is not itself an all-order induction step.
  Full staged plan, acceptance criteria and pivot conditions: `docs/nonexistence-roadmap.md`.  The two-Max-review
  synthesis and the specialised FW218 q=1 critical path are in `docs/post-max-review-q1-plan.md`.
- OBSERVED finite b=27 control — the forced `L(5,21)/J(32)` label-state model is now closed through rooted
  skeleton order eight: all `412,160` rows are `INFEASIBLE` and pass independent BFS replay.  This remains a
  finite state-class exclusion; attachment/LCA completeness, arbitrary low forests, and global nonexistence are
  still **GAP**.  The direct attachment/LCA extension is Hoffman2 job `99416`; its `--max-order 3` script covers
  rooted orders 1--3 (`41,088` rows total, including `34,560` order-three rows).  The complete initial artifact has
  `35,244 INFEASIBLE` and `5,844 UNKNOWN` (all `EDGE`) and passes the graph/BFS replay layer, but `UNKNOWN` is not
  a zero.  Hoffman2 job `99604` then reran exactly those `5,844` rows with a five-second limit.  The full rerun
  artifact has `41,088/41,088 INFEASIBLE`, zero `UNKNOWN` and zero `FEASIBLE`, and passes the independent graph/BFS
  replay.  Its SHA-256 is `12f9941bf7747e15867ba405dff9486705221d1dfa8aee35fe6df7ff68dfbbbc`.  A semantic comparison
  against the initial artifact found no changes outside solver status/time fields.  This closes the stated finite
  order-three attachment/LCA model; attachment-state completeness, richer high subtrees, arbitrary low forests,
  and global nonexistence remain **GAP**.  Detailed evidence is in
  `docs/pro-b27-l521-j32-label-state-control.md` and
  `docs/exact-return-33-g7-r2-t4-b27-residual-two-branch-frontier.md`.
  The next bounded relaxation replaces the J32 endpoint single-leaf assumption by `NONE`/`PATH2`/`FORK2` modes
  at both endpoints and covers rooted skeleton orders 1--3 (`92,448` rows).  Hoffman2 job `99744` completed
  this model at a 0.20-second per-row limit, and its complete artifact already passes the independent verifier;
  the finite relaxation is not closed until any resulting `UNKNOWN` rows are rerun.  The dedicated follow-up wrapper
  `scripts/hoffman2_j32_outward_deeper_order3_unknown_rerun_slurm.sh` is prepared for that exact targeted rerun.
  The initial artifact is now complete and hash-matched to Hoffman2 (`c8ff7915eb5f6e4a9fc46fa0706fa2bdfe7c5c124ee8667203e1642b660f05df`):
  `82,831 INFEASIBLE`, `9,617 UNKNOWN`, and zero `FEASIBLE`; all UNKNOWN rows are `EDGE`
  rows (1,080 at order 2 and 8,537 at order 3).  Targeted rerun job `100025` is active;
  its result must pass `theory-lab/topwindow/verify_pro_b27_j32_outward_deeper_rerun.py`
  and the independent graph/BFS verifier before this relaxation can be called closed.
  In parallel, Pro-guided job `100060` tested the complete isolated low-support control with both `L(21)` shapes
  (`stem<=80`, `h<=120`): `377,982` candidates, zero survivors, and normal completion in 17 seconds.  Its
  hash-matched artifact is `theory-lab/topwindow/results/pro_b27_j32_isolated_l521_minimal_stem80_h120_100060.json`
  (`14fc9ec1c4ba3c787559d098f39780a8d5065893d6738a124eead61c65e040cc`) and its independent audit is
  `theory-lab/topwindow/verify_pro_b27_j32_isolated_l521_minimal_result.py`.  This remains a bounded pressure
  control; remote attachment gates, other ownership patterns, arbitrary high subtrees, and global Label-State
  Completeness remain outside its scope.
