# variants/ — neighbouring computational values (minimal distinct distance trees, modular Leech trees, leaf-Leech trees)

Started 2026-08-18/19 with the validated forest-engine family of this repo (own copies in `variants/`; nothing in
`src/` or `cleanroom/` modified).  Every claim below is labelled OBSERVED (computed here, with the cross-check named)
or LITERATURE (taken from a source, cited).  Witnesses are re-checked by `variants/checker_distinct.py`, an independent
BFS-based checker with no shared code with any engine.  Raw outputs: `variants/runs/` (local), Hoffman2
`$SCRATCH/leech-trees/variants/results/` (mirrored to `variants/results_h2/` when a run is closed).

## A. Minimal distinct distance trees M(n) (Calhoun, Ferland, Lister, Polhill, JCMCC 61 (2007) 33-57)

**Definition.** A distinct distance tree is a tree with positive-integer edge weights whose C(n,2) path sums are pairwise
distinct; M(n) = min over such trees on n vertices of the maximum distance.  LITERATURE (Calhoun Table 1, read from the
OCR `docs/sources/JCMCC2007_Calhoun_OCR.txt`, lines 171 ff.): exact values M(1..10) = 0,1,3,6,11,15,22,30,39,50
(n=7..10 by Theorem 2.2 + computer search; the minimal trees are drawn in their Figures 4-7); for 11 <= n <= 18 only
bounds: n=11: 59..77, 12: 69..94, 13: 80..119, 14: 93..142, 15: 107..165, 16: 121..214, 17: 139..254, 18: 153..294
(lower bounds "Theorem 2.2 + Computer Search", i.e. exclusion of few-gap targets; upper bounds by the tree of their Fig. 8
and its subtrees).  Calhoun: "it will take too long for the algorithm to check higher numbers of gaps and find the exact
value of M(n)" for n >= 11.

**Method** (`variants/mdd_forest.cpp`, adapted copy of `src/forest_search.cpp`).  Calhoun's forest DFS (Alg. 2.7) with the
complete isomorph rejection of the reference engine (parent = remove the max-weight edge; Aut = endpoint swaps of
single-edge components) plus a GAP branch: at value level t (all values < t decided) either t is already a distance, or t
is declared a gap (never a distance; at most g = D - C(n,2) gaps), or t is the weight of the next edge (join / attach /
new disjoint edge).  The forcing lemma is thereby replaced by "next weight = next undecided value or a gap"; the state
(forest, t) is reached by exactly one decision sequence, so the search tree has no redundant nodes and nsol at D = M(n)
is the number of minimal distinct distance trees up to isomorphism.  Prunes: distinctness/<= D by bitsets, gap budget,
w_max + (t + r - 1) <= D and 2t + 2r - 3 <= D (r = edges still to add; any two edges lie on a common path), vertex /
component budget, radius bound ceil(hi_X/2) + ceil(hi_Y/2) + t <= D.  Sharding by DFS index at level L (only forests
*entering* level L by an edge are assigned to shards, so their gap-chain descendants stay in the shard; identity
sum(shard nodes) = full + (K-1)*prefix verified at n=9,10).  Feasibility is decided for increasing D; the D = M(n)-1 run is
the UNSAT certificate (node counts recorded).  A translate look-ahead (`--look`) was implemented and measured: -20 % nodes,
~3x slower, off by default.  `--edge-first --maxsol 1` is the witness-hunting mode (n=11 witness in 3.6e7 nodes vs 5.9e8).

**Validation on Calhoun's known values** (OBSERVED, all reproduced, local M4, `variants/mdd_forest n D`):
| n | D=M(n)-1 nodes (UNSAT) | D=M(n) nodes | # minimal trees | Calhoun |
|---|---|---|---|---|
| 4 | (D<C(n,2)) | 6 | 2 | 2 (Leech) |
| 5 | 11 (D=10) | 54 | 6 | Fig. 2 ("two Golomb + found by hand", count not stated) |
| 6 | - | 47 | 1 | 1 (Leech) |
| 7 | 215 (D=21) | 1,411 | 2 | Fig. 4: 2 |
| 8 | 8,246 (D=29) | 38,139 | 2 | Fig. 5: 2 |
| 9 | 248,421 (D=38) | 929,453 | 1 | Fig. 6: 1 |
| 10 | 22,190,931 (D=49) | 63,559,820 | 1 | Fig. 7: 1 (same weights 1,2,3,4,5,11,14,18,28) |
Independent-method cross-check: `variants/mdd_topo.c` (per-topology DFS over networkx/nauty topologies, no forcing, no
forest, no isomorph rejection) gives n=9: D=38 0 labelings (28.3 M nodes), D=39 exactly one labeling on topology id 26 —
same tree.

**New exact values** (OBSERVED, Hoffman2 x86_64 gcc 11.5, K shards, all shards DONE):
| n | D | result | nodes | CPU-s |
|---|---|---|---|---|
| 11 | 59 | UNSAT | 1.80e8 (local) / 1.83e8 (Hoffman2, 7 shards) | 126 (local, loaded) / 33 |
| 11 | 60 | **SAT: 2 trees** | 5.86e8 | 111 |
| 11 | 61..65 | 2, 8, 11, 23, 55 trees with max <= D | 1.6e9 .. 4.0e10 | up to 5,636 |
=> **M(11) = 60**, exactly two minimal distinct distance trees:
`0-1:1 0-2:2 3-4:4 5-6:5 5-7:6 3-8:8 3-5:9 3-9:16 2-7:26 7-10:27` (missing 7,10,21,36,54) and
`0-1:1 0-2:2 3-4:4 5-6:5 5-7:6 3-8:8 3-5:9 3-9:16 7-10:26 0-7:27` (missing 7,10,21,36,56); both pass checker_distinct.
Distribution of the 55 trees with max <= 65 by max distance: 60:2, 61:0, 62:6, 63:3, 64:12, 65:32.
(cross-check per-topology engine: pending, see below)

n = 12: TBD

## B. Modular Leech trees (Leach & Walsh, JCMCC 78 (2011) 15-22 [not accessible]; Leach, Int. J. Combin. 2014, 218086)
TBD

## C. Leaf-Leech trees (Ozen, Wang, Yalman, Integers 16 (2016) #A21)
TBD
