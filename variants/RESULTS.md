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
Independent-method cross-check (OBSERVED): `mdd_topo` per-topology DFS over all 235 topologies of order 11 —
D=59: 0 labelings, 1.2620879225e10 nodes; D=60: 18 raw labelings, 1.5106490676e10 nodes; run twice, locally
(arm64/clang) and on Hoffman2 (x86_64/gcc), with identical node counts and identical SOL lists.  The 18 raw labelings are
exactly the two trees above times their automorphisms (topology id 94: 6 labelings = 3! permutations of the pendant
weights 4,8,16 at one vertex; id 96: 12 = 3! x 2).  Cross-check n=10 the same way: D=49 0 / D=50 6 raw labelings
(1 tree x |Aut|=6), 7.5e8 / 9.1e8 nodes.

**n = 12** (OBSERVED, Hoffman2): D=69,70,71,72,73,74,75,76 all UNSAT with 3.7e8, 1.5e9, 5.2e9, 1.6e10, 4.2e10, 1.0e11,
2.4e11, 5.1e11 nodes (35-70 shards each, sum CPU 82 s ... 9.1e4 s); witness hunt (`--edge-first --maxsol 1`): D=78 SAT
`0-1:1 0-2:2 3-4:4 5-6:5 0-3:6 5-7:13 8-9:14 4-8:15 6-9:16 8-10:17 9-11:37` (missing 9,20,22,23,24,28,38,46,59,64,69,72;
checker OK; 3.1e10 nodes, 4601 s), also D=79,80,81,82 witnesses.  The exhaustive D=77 run completed in 70/70 DONE shards:
1,020,925,849,186 nodes, exactly two solutions up to isomorphism, both independently checked by BFS and depth/LCA distance
computations.  Their edge lists are `0-1:1 2-3:2 4-5:3 2-6:4 4-7:5 0-8:9 4-9:12 2-7:14 7-10:20 9-11:29 8-9:30`
and `0-1:1 2-3:2 4-5:3 2-6:4 4-7:5 0-8:9 4-9:12 3-7:14 7-10:18 9-11:29 8-9:30`.
Together with D<=76 UNSAT, this gives **M(12) = 77**, exactly two minimal trees (Calhoun: 69..94).

**n = 13**: not attempted exhaustively (M(13) >= 80 from Calhoun; extrapolated cost > 1e15 nodes at D ~ 90).  Upper bound
by leaf extension of the n=12 witnesses: **M(13) <= 105** (Calhoun 119): `... 4-12:62` appended to the D=79 tree
(checker OK, see agg script in this file's history).  Similarly M(12) <= 82 was first obtained by extending the n=11
trees with max <= 65 (`runs/agg_11_65.json`).

**Node/CPU cost summary (mdd_forest, Hoffman2 ~5e6 nodes/s/core):** growth ~x2.5-3.3 per unit of D and ~x10-30 per n at
fixed gap count; the search is dominated by the last two edge levels (r <= 2), where forests with small weights survive.

## B. Modular Leech trees (Leach & Walsh, JCMCC 78 (2011) 15-22 [not accessible]; Leach, Int. J. Combin. 2014, 218086)

**Definition** (Leach 2014, p.1, `variants/sources/Leach2014_IJC_modular_leech.txt`): T on n vertices, k = C(n,2)+1, an
edge weighting w: E(T) -> Z_k such that the C(n,2) path sums taken mod k are exactly {1,...,k-1} (a bijection paths ->
Z_k \ {0}).  LITERATURE: modular Leech trees exist for n = 2,3,4,6 (the Leech trees) and n = 8 (unique, over Z_29,
Fig. 3, labels 25,2,1,12,3,18,22 up to unit multiplication); Leach 2014 Thm 1/2: if n = 2,3 (mod 4) and n != m^2+2 then
none exist (so none for n = 7, 10, 14, 15, ...); "By Leach and Walsh [6] ... none exist for 5 or 7"; Thm 3: multiplying a
labeling by a unit of Z_k gives a labeling.  Leach's search: "for n = 8 there are 23 distinct unlabeled trees. By computer
search, we find that there is one modular Leech tree for n = 8 and the edge-weighting function is unique, up to group and
graph isomorphism."  Nothing is stated about n >= 9.

**Method.** `variants/mod_leech.c` (v1) and `variants/mod_leech2.c` (v2): per-topology DFS over networkx/nauty topologies
(`variants/data/trees_n.jsonl`; n=9,11 are the frozen files of the main repo, n=7,8,10,12,13 generated with networkx
nonisomorphic_trees).  Edges in BFS order from a max-degree root; a new edge attaches vertex c to placed p with label w in
[1,k-1]; the new residues d(p,u)+w mod k (all placed u) must be nonzero and unused (u128 bitset).  Symmetry: v1 restricts the
first edge to 1 (orbits with a unit there) or a non-unit, and reports orbits = A + B/phi(k) (the unit action is free
because the sum 1 is realised); v2 keeps the label vector lexicographically minimal in its U(k)-orbit (a label w on edge i
is allowed iff u*w >= w for every unit u fixing the earlier labels) and adds forward checking (every pending edge with a
placed parent must still admit some label).  Both count orbits under U(k) (graph automorphisms are NOT factored out; SOL
lines list all orbit representatives).  Validation (OBSERVED): brute force over all (k-1)^(n-1) labelings for n = 4,5,6
(`variants/test_mod_leech.py`) agrees with v1 on every topology; v1 and v2 give identical orbit counts for n = 4..9
(4, 4, 34, 0, 2, 0); every SOL passes `checker_distinct.py modular`; n = 8 reproduces Leach exactly: the unique topology
(id 4 of trees_8, the tree of Leach's Fig. 3) with orbit count 2 = one labeling up to the leaf swap, and 3 x our labeling
{1,4,18,6,10,17,20} = Leach's {3,12,25,18,1,22,2} (mod 29).

**Results (OBSERVED)**
| n | k | topologies | modular Leech trees (topologies / U(k)-orbits) | nodes (v1 / v2) | note |
|---|---|---|---|---|---|
| 4 | 7 | 2 | 2 / 4 | 18 / 16 | Leech's two trees |
| 5 | 11 | 3 | **2 / 4** | 127 / 58 | P5 with labels 5,1,2,7 (path sums mod 11 = 1..10) and the spider 0-1:1 1-2:5 0-3:3 0-4:7; **contradicts "none exist for 5" as reported in Leach 2014 for [6]** (both witnesses verified by checker_distinct and by brute force) |
| 6 | 16 | 6 | 2 / 34 | 21,837 / 1,700 | the double star (Leech tree, 16 orbits) and 1-0,1-2,1-3,0-4,4-5 (18 orbits) |
| 7 | 22 | 11 | 0 | 461,340 / 30,853 | agrees with Leach Thm 2 |
| 8 | 29 | 23 | 1 / 2 | 755,515 / 239,450 | = Leach 2014 |
| 9 | 37 | 47 | **0** | 1.81e7 / 6.5e6 | NEW: no modular Leech tree of order 9 |
| 10 | 46 | 106 | **0** | 1.42e10 (v1) / 3.6e8 (v2), Hoffman2 | consistent with Leach Thm 2 (10 = 2 mod 4, not m^2+2) |
| 11 | 56 | 235 | **0** | 1.28e10 (v2, Hoffman2, 42 procs) | NEW: no modular Leech tree of order 11 (11 = 3^2+2 is allowed by Thm 2) |
| 12 | 67 | 551 | not attempted (k prime, no unit symmetry gain; est. > 1e15 nodes) | | |

## C. Leaf-Leech trees (Ozen, Wang, Yalman, Integers 16 (2016) #A21)

**Definition** (Def. 1): an unweighted tree with L leaves whose leaf-leaf distances are exactly {3,...,C(L,2)+2}.
LITERATURE: Prop. 1 (Taylor analogue) L = m^2 or m^2+2; Thm 1: the expansion T^e of a Leech tree is leaf-Leech (so
L = 2,3,4,4,6 exist); Thm 2: a leaf-Leech tree without an *irreducible* vertex (degree >= 3 and no leaf neighbour) is the
expansion of a Leech tree; Prop. 2/3: no starlike / caterpillar leaf-Leech trees with > 4 leaves; **Question 3.1: does a
leaf-Leech tree with an irreducible vertex exist?** ("we have not been able to find a leaf-Leech tree that is not the
expansion of a Leech tree").  Largest L with a known leaf-Leech tree: 6.

**Method.** Contracting degree-2 vertices, a leaf-Leech tree = series-reduced tree (internal degrees >= 3) with L leaves and
positive integer edge weights, weighted leaf-leaf distances = {3..S+2}.  `variants/gen_leaf_topos.py` enumerates all such
topologies with nauty gentreeg (L+1 <= N <= 2L-2 vertices; cross-checked against networkx for N <= 14): L=9: 73
topologies, L=11: 488.  `variants/leaf_leech_cpsat.py`: per topology CP-SAT (weights in [1,S+2], AllDifferent over the S
leaf-pair distance variables in [3,S+2] = bijection), enumerate all solutions; every witness re-checked by
`checker_distinct.py leaf` (BFS distances; irreducible vertices reported); `variants/summarize_leaf.py` dedups modulo
isomorphism of the expanded unweighted tree.

**Results (OBSERVED)**
| L | topologies | leaf-Leech trees (distinct, expanded-tree isomorphism) | with irreducible vertex |
|---|---|---|---|
| 3 | 1 | 1 (= expansion of L3) | 0 |
| 4 | 2 | 2 (= expansions of L4_star, L4_path) | 0 |
| 5 | 3 | 0 (Taylor) | - |
| 6 | 7 | **6** = expansion of L6 + 5 new | **5** |
| 9 | 73 | INCONCLUSIVE: star (N=10) INFEASIBLE in 41 s; the N=11 topologies hit UNKNOWN at 3600 s (1 worker, enumerate-all); Hoffman2 jobs (7200 s) still running | |
| 11 | 488 | INCONCLUSIVE (same) | |
CP-SAT is not the right tool for L >= 9 (like the Leech case, README); a forcing/forest-style engine over leaf distances would be
needed — left open.  **Question 3.1 of OWY is answered YES already at L = 6**: e.g. `1-0:1 1-2:6 1-5:4 0-6:1 0-9:1 2-3:6 2-4:2 6-7:3 6-8:1`
(26 vertices after subdivision, leaves 3,4,5,7,8,9; vertices 1 and 2 have degree 3 and no leaf neighbour); leaf distances
{3..17}: checked.  The five new trees are listed by `summarize_leaf.py 6`.

## Summary table of new values (all OBSERVED; confidence label = how cross-checked)
| quantity | literature | new value | confidence |
|---|---|---|---|
| M(11) | 59..77 (Calhoun 2007) | **60**, exactly 2 minimal trees | forest engine (2 machines/compilers, sharded) + independent per-topology DFS over all 235 topologies (2 machines, identical node counts); witnesses by independent checker |
| M(12) | 69..94 | **77**, exactly 2 minimal trees | UNSAT D<=76; D=77 exhaustive forest run, 70/70 shards DONE, 1.021e12 nodes and 2 solutions; both witnesses verified independently by BFS and depth/LCA checkers |
| M(13) | 80..119 | 80 <= M(13) <= 105 | upper bound = verified witness; lower bound literature |
| modular Leech, order 5 | "none" (Leach-Walsh 2011 as quoted by Leach 2014) | **exist**: 2 topologies (P5; spider) / 4 U(11)-orbits | v1 + v2 + brute force over all labelings + checker |
| modular Leech, order 9 | open | **none** (47 topologies) | v1 and v2 (different symmetry breaking / pruning) agree, 1.8e7 / 6.5e6 nodes |
| modular Leech, order 10 | excluded by Leach Thm 2 | none (106 topologies) | v1 and v2 agree, Hoffman2 |
| modular Leech, order 11 | open (allowed by Thm 2) | **none** (235 topologies) | v2 only (1.28e10 nodes, Hoffman2); v1 too slow — single-implementation result |
| leaf-Leech, 6 leaves | only the expansion of L6 known; OWY Q3.1 open | **6 trees, 5 with irreducible vertices** (Q3.1: YES) | CP-SAT enumerate-all over all 7 series-reduced topologies + independent checker |
| leaf-Leech, 9 and 11 leaves | open | INCONCLUSIVE (CP-SAT UNKNOWN) | — |

Files: engines `mdd_forest.cpp`, `mdd_topo.c`, `mod_leech.c`, `mod_leech2.c`, `leaf_leech_cpsat.py`, `mdd_cpsat.py`, `mod_cpsat.py`
(the two CP-SAT cross-checks were too slow to be useful); checker `checker_distinct.py`; tests `test_mdd_forest.py`,
`test_mod_leech.py`; drivers `hoffman2_*_slurm.sh`, `agg_mdd.py`, `summarize_leaf.py`, `gen_leaf_topos.py`; raw outputs
`runs/` (local) and `results_h2/` (Hoffman2 mirror: mdd_11/12 shards, mddtopo, mod2, mddub), `results/leaf_L*.jsonl`.
