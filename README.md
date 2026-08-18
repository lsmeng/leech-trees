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
- LITERATURE (unverified copies): 9,11 ruled out computationally by Székely–Wang–Zhang 2005; all perfect-distance trees n<18 determined by Calhoun et al. 2007 (so 16 done); diameter-3 excluded n>=7 and finitely many diameter-4 (Luo–Yu 2024).
- CORRECTION: Taylor's parity condition constrains the parity pattern of *weights* (count of odd-depth vertices must be 7 or 11 at n=18); it is NOT a topology filter (bipartition of the unweighted tree is irrelevant). Implemented as a redundant constraint in solve_v2.

## Layout
src/checker_a.py, checker_b.py   independent witness checkers
src/enumerate_trees.py           two-route topology enumeration + AHU certificate cross-check
src/solve_topology.py (v1), solve_v2.py (bounds+Taylor+symbreak+strategy), solve_v3.py (dual channel; slower)
src/run_order.py                 parallel resumable driver -> results/order_{n}.jsonl
data/trees_{n}.jsonl             frozen topologies; results/                per-topology outcomes

## Next (research core)
1. Read SWZ 2005 / Calhoun 2007 for their pruning (max degree, no long path, leaf-edge structure) and re-prove what we use.
2. Purpose-built search: branch on values (small-first or diameter-first) with bitset incremental distinctness; C/Rust; benchmark on n=16 (known UNSAT) as calibration.
3. Only then n=18 on Hoffman2; certificates: enumeration logs + per-topology proof (DRAT/VeriPB via SAT encoding) for the final claim.
