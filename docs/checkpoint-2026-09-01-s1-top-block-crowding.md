# Checkpoint — 2026-09-01 — S1-279..S1-284 closed by top-block crowding

Author: Fable (independent take-over audit, see
`docs/handoff-fable-leech-tree-audit-2026-09-01.md`).
Status of this note: `delta = 279, 280`: **THEOREM** (elementary, conditional
only on the already verified singleton-final-cap identity
`F ⊔ (s+D) = [1,300]` and its top-block lemma), plus two independent
computational confirmations.  `delta = 281, 282`: **CERTIFIED FINITE
IMPOSSIBLE** by an exhaustive depth-free search over every low-tree shape
(section 3.3); the search is independent of `s` and of the low depths.
`delta = 283`: **CERTIFIED FINITE IMPOSSIBLE** by the depth-free search
(47 of 48 shapes) plus the depth phase on the chain shape (section 3.7),
with two independent runs agreeing.  `delta = 284`: **CERTIFIED FINITE
IMPOSSIBLE** (section 3.9, Hoffman2 array, verifier certificate).

## 1. Scope

Order-25 target, `N = 300`.  Singleton final cap: the heaviest edge (weight
`s`) is pendant; `K` is the 24-vertex remainder rooted at the bridge endpoint
`x`; `D = R_{K,x}` (24 distinct depths, `0 ∈ D`), `F = Spec(K)`,
`F ⊔ (s+D) = [1,300]`, `delta = max F = 276 + r`.  The top-block lemma of
`docs/exact-return-33-g7-singleton-final-cap-sharpening.md` gives

```text
A = 300 - s,   m = 24 - r,   B = A - m + 1,
D = L ⊔ [B, A],   |L| = r,   0 ∈ L,   L ⊂ [0, B-1].
```

I re-derived the identity, the top-block lemma and the parity table
(`delta = 277, 278` impossible; `delta = 279` forces `s, d1, d2` even;
`delta = 280` forces `s, d1, d2, d3` even) and confirmed them with
`theory-lab/s1_crowding/verify_s1_top_block_crowding.py` (section (1) of its
output).  Nothing else from the FW303 chain is used below: no core gate, no
component-count bound, no weight alphabet.

## 2. Theorem (top-block crowding)

Call the `m` vertices with depths in `[B, A]` *high* (`h_y` has depth `B+y`,
`0 <= y <= m-1`) and the `r` vertices with depths in `L` *low*.  Low vertices
form a connected rooted subtree containing `x` (every ancestor of a low
vertex is low).  Two high vertices lie in the same component of the high
induced forest iff their LCA is high.

For high `h_y, h_{y'}` (`y != y'`):

```text
LCA high, depth B+q :   d = y + y' - 2q            in [1, 2m-3]
LCA low,  depth l   :   d = 2B - 2l + (y + y')
```

Partition the `C(m,2)` high-high pairs into `r+1` classes: "LCA high" and
"LCA = the low vertex of depth l" for each `l ∈ L`.  For the high-LCA class,
the distance is `y+y'-2q` and therefore itself lies in `[1,2m-3]` (the
high-LCA depth `q` need not be determined by `y+y'`).  For the class with
LCA equal to a fixed low vertex of depth `l`, the distance is
`2B-2l+y+y'`, with `y+y' ∈ [1,2m-3]`.  Thus, under global distance
injectivity, every one of the `r+1` classes contains at most `2m-3` pairs.
Hence a distance-injective `K` needs

```text
C(m,2) <= (r+1)(2m-3).
```

```text
delta=279  r=3  m=21 :  210 > 4*39 = 156   IMPOSSIBLE
delta=280  r=4  m=20 :  190 > 5*37 = 185   IMPOSSIBLE
delta=281  r=5  m=19 :  171 <= 6*35 = 210  not excluded by this count
```

Therefore **no S1-279 candidate exists**: for every `s`, both low-tree
shapes (chain and star), and every `d1 < d2`.  Likewise **no S1-280
candidate exists** for every `s`, every low-tree shape on four vertices and
every `d1 < d2 < d3`.  The argument does not use parity, the FW303 core, the
`c` range, or the alphabet `{4,5,16,18,19,20}`.

Consequence for the existing programme: the certified `s=152` and `s=154`
star/chain shards, the 555,397-signature `s=154` chain union, the 38-row
prefilter and the planned 1286-shard forest are all subsumed.  Their zero
results are consistent with the theorem but no further forest shard is
needed.  The singleton branch now starts at `delta >= 281`
(`A >= 141`, `s <= 159`).

## 3. Independent computational confirmations

All code is new, in `theory-lab/s1_crowding/`, and shares nothing with the
`remote_scratch` pipeline.

### 3.1 `verify_s1_top_block_crowding.py`

Pure-Python, no project imports.  Checks (1) the parity table for
`delta = 277..281`, (2) the two distance formulas against BFS on random trees
with the required depth structure (`r = 3` chain/star, `r = 4, 5, 6` random
low shapes, 3000 trees each), (3) that the number of distinct high-high
distances never exceeds `(r+1)(2m-3)` on random and hill-climbed trees, and
(4) the counting table.  Output ends with
`VERIFIED_S1_TOP_BLOCK_CROWDING_ARITHMETIC`.

### 3.2 `s1_direct_search.cpp` — direct exhaustive search of the normal form

Vertices are placed in depth order; each high vertex chooses its parent among
the low vertices and all shallower high vertices; every new pair distance is
checked incrementally against `F = [1,delta] \ (s+L)` and against the
distances already used.  Positive controls: the known order-6 Leech tree
(heaviest edge 8 pendant, `r = 1`) is recovered (`survivors = 1`), and
planted random distance-injective trees at orders 9, 10, 12 with `r = 2, 3, 4`
are recovered in every trial (`FOUND_PLANTED`).

Sweep of the whole `delta = 279` normal form for the five values of `s`
handled by the previous pipeline, both shapes, all even `0 < d1 < d2 < B`
(local run, 0.07 s CPU in total; repeated on Geo Workstation with identical
output):

```text
s=152 chain instances=1953 low_prefail=31 survivors=0 nodes=3344909 EXHAUSTED_EMPTY
s=152 star  instances=1953 low_prefail=25 survivors=0 nodes=1378767 EXHAUSTED_EMPTY
s=154 chain instances=1891 low_prefail=31 survivors=0 nodes=3226030 EXHAUSTED_EMPTY
s=154 star  instances=1891 low_prefail=24 survivors=0 nodes=1332943 EXHAUSTED_EMPTY
s=156 chain instances=1830 low_prefail=30 survivors=0 nodes=3040083 EXHAUSTED_EMPTY
s=156 star  instances=1830 low_prefail=22 survivors=0 nodes=1278394 EXHAUSTED_EMPTY
s=158 chain instances=1770 low_prefail=30 survivors=0 nodes=2899510 EXHAUSTED_EMPTY
s=158 star  instances=1770 low_prefail=21 survivors=0 nodes=1231799 EXHAUSTED_EMPTY
s=160 chain instances=1711 low_prefail=29 survivors=0 nodes=2811873 EXHAUSTED_EMPTY
s=160 star  instances=1711 low_prefail=19 survivors=0 nodes=1191305 EXHAUSTED_EMPTY
```

(`low_prefail` counts parameter pairs whose three low-low distances already
collide or leave `F`, e.g. chain `d2 = 2 d1`; they match the pipeline's
`params_total - params_valid`.)

Official full sweep on Geo Workstation (`run_r3_full_sweep.sh`, four
`nice -n 15` workers, 4 minutes wall): every `s ∈ [13,160]` (148 values),
both shapes, every `0 < d1 < d2 < B` of **any** parity:

```text
summaries            296   (148 s-values x 2 shapes), all EXHAUSTED_EMPTY
instances      5,725,972
low_prefail      789,154
nodes        571,781,366
survivors              0   aborted 0
all_summaries.txt SHA-256 d130f57d25aefc9b5097c6eb57e27731c06496e8ae51f7621ea911dc8318e3ed
s1_direct_search.cpp SHA-256 433e9a8884a04a5bb068c063df1d6c246d3e74f919ecf911512836906262c3d7
```

(`s < 13` is impossible because the diameter path has at most 24 edges of
weight `<= s`; `s > 160` is excluded by `delta <= 2A`.)  Per instance the search dies after at most
ten placed high vertices (`LEVELS 1 3 12 42 147 374 850 1151 548 5 0 ...` for
`s=154`, chain, `d1=20, d2=60`), which is the crowding theorem observed
in the search tree.

### 3.3 `abstract_class_search.cpp` — depth-free class search

Enumerates every parent structure on the high block for a given low-tree
shape (parent of `h_y` = a low vertex or an earlier `h_p`) and rejects only
violations of the class-injectivity conditions of the theorem: all
within-component distances `y+y'-2q` pairwise distinct, and for every low
vertex `l` the sums `y+y'` of the pairs whose LCA is `l` pairwise distinct.
These conditions involve neither `L` nor `s`; low-tree shapes are taken up to
rooted isomorphism (AHU canonical form), since only the LCA structure enters.
A complete structure is a necessary condition for any tree of the normal
form, so an empty search closes the whole `delta` for every `s` and every
choice of low depths.

```text
delta=279  m=21 r=3 : 2 shapes            leaves=0  (<0.1 s)
delta=280  m=20 r=4 : 6 shapes            leaves=0  (<0.1 s)
delta=281  m=19 r=5 : 9 classes / 24 lab. leaves=0  (0.3 s, max 1,697,398 nodes for the chain)
delta=282  m=18 r=6 : 20 classes / 120    leaves=0  (9 s,  max 37,868,410 nodes for the chain)
```

Local run (single process, seconds); repeated on Geo Workstation with the
same source (the run record reports SHA-256
`3a7a58beed9e02a9c97aae9db84e5425989871f7dc351d40921b0a0f17ebcae3`).
The current checked-out/remote source file now hashes to
`e72d39e673671f0a7fe6a9a66986d3075277a9dd4e7e6ce2a4d7e63d53ab987c`;
the historical run source and the current source/binary must be reconciled
before this computational result is promoted beyond Fable-reported finite
evidence.
For `delta = 279, 280` this is a second, independent mechanisation of the
theorem; for `delta = 281, 282` it is the certificate.  `delta = 283`
(`m = 17`, `r = 7`, 48 rooted shapes) is running on Geo Workstation in four
`nice -n 15` shards; no claim is made for it here.

### 3.5 `brute_abstract_check.py` — independent brute force of the class semantics

Written by a subagent from the written specification only (it did not read
the C++).  It enumerates every parent structure explicitly, rebuilds the tree,
finds every LCA by walking ancestor lists, and counts admissible structures.
Eight cases (`m = 4..7`, `r = 1..4`, totals up to 604,800 structures) match
the C++ `leaves=` counts exactly, and the emitted structure sets are
identical after sorting:

```text
m=4 r=1 : 9/24        m=5 r=1 : 7/120       m=5 r=2 : 99/720
m=6 r=2 : 117/5040    m=6 r=3 chain : 1207/20160   m=6 r=3 star : 504/20160
m=7 r=3 chain : 1593/181440          m=7 r=4 lowpar=0,0,1 : 3476/604800
```

### 3.6 Depth phase (`--solve-depths`) and its validation

For a complete abstract structure the program searches every bridge weight
`s` and every low-depth vector `L` (each low vertex strictly deeper than its
parent, all depths distinct, all below `B`) such that the full multiset of
`C(24,2)` pair values is a set of distinct values inside `[1,delta] \ (s+L)`;
a survivor would be a genuine tree of the normal form.  Two validations:

* the order-6 Leech tree is recovered (`DEPTH_SURVIVOR s=8`, `r=1`);
* differential test against `s1_direct_search` on a relaxed target (all
  values in `[1,60]` allowed, no holes; order 9, `m=5`, `r=3`, both low
  shapes, `s ∈ {10,12,14,16}`, every increasing `L`): the abstract+CSP
  survivor counts equal the direct-search counts exactly for the chain
  (`1385, 501, 190, 34`) and exactly twice them for the star
  (`5182, 2232, 714, 126` vs `2591, 1116, 357, 63`), the factor two being
  the `u1 <-> u2` automorphism that the depth-order-free CSP counts twice.
  This exercises the low-low, low-high and class-value bookkeeping of the CSP
  on thousands of genuine survivors.

### 3.7 `delta = 283` (`m = 17`, `r = 7`): certified finite impossible

Depth-free phase (Geo Workstation, 4 shards over the 48 rooted low-tree
shapes, `--stop-first`, source SHA-256
`3a7a58beed9e02a9c97aae9db84e5425989871f7dc351d40921b0a0f17ebcae3`):
47 shapes are exhausted with zero structures, no shard aborted; only the
chain `lowpar = 0,1,2,3,4,5` has structures (first one after 11,571 nodes).
Merged output SHA-256
`5e9b40afaa05bd9551d27f473314abb05f0e6faa10b38255a07c4f27ff350b09`.

Depth phase on the chain, two independent runs:

```text
Geo Workstation, one process (v2 source 7a32ba54...):
  leaves=14730 nodes=932540226 EXHAUSTED depth_survivors=0 csp_nodes=16302184
  output SHA-256 fc360372265552ae0dc5db057cdda80d506d0009b2927541676e42f847407cec
Hoffman2, 64 prefix-split array tasks (v3 source 6a5315dd...), all COMPLETE:
  leaves=14730 nodes=934428210 depth_survivors=0 csp_nodes=16302184
  merged output SHA-256 b1bce6b547ac84acf94aaa63a901f51472ea06569e82f32d8dac54e62de18c97
  verify_depth_splits.py -> VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY, certificate SHA-256
  32603c95154113d2354fd6f53a7d0026ecb86b5cc5ff0c4e54e33eb7316fb3fe (depth_r7chain/certificate.json)
```

(The node totals differ only by the prefix nodes that every split task
re-traverses; leaves and CSP nodes coincide exactly.)  A third run with the
memoized rho-level CSP (`abstract_class_search7`, local, 108 s CPU) again
gives `leaves=14730`, `depth_survivors=0`; only 2,045 distinct fibre
assignments `rho` occur among the 14,730 structures, and every one of them
is already dead at the rho level (`leaf_rho_dead=14730`).  Every one of the
14,730 depth-free structures fails the `(s, L)` search, so **no S1-283
candidate exists** for any `s` and any low depths.  The first structure
found is the "nested extreme" pattern `h_0, h_16` at `x`, `h_1, h_15` at
`u_1`, ..., with every low class full; for it the root class forces
`s = 158`.

### 3.8 Soundness notes for the depth phase

* *One labeled representative per rooted-isomorphism class suffices.*  The
  CSP requires only that every low vertex is strictly deeper than its parent
  and that all depths are distinct; it never assumes `l_i < l_j` for `i < j`.
  Any actual tree whose low subtree is isomorphic to the representative can be
  relabeled to the representative's labels, and every parent function on the
  high block is enumerated under that labeling.  (Automorphisms of the low
  tree only cause duplicate counting of survivors, never omission; the
  relaxed differential test shows the factor 2 for the star.)
* *Memoized rho-level CSP and prefix pruning (`--rho-check`).*  With
  `rho(y)` the low vertex carrying `h_y`'s component, all pair values except
  the same-fibre ones are functions of `(s, L, rho)`.  Running the CSP on the
  values of the first `y` placed high vertices is a relaxation of every
  extension, so a prefix with no `(s, L)` survivor can be cut, and the result
  depends only on the prefix of `rho`, which is memoized.  At a leaf the full
  `rho`-level CSP is run once per distinct `rho`; its survivors are then
  checked against the leaf-specific within-component and same-fibre class
  values.  The relaxed differential test returns identical counts with and
  without prefix checks.

### 3.9 `delta = 284` (`m = 16`, `r = 8`): certified finite impossible; `delta = 285` running

Hoffman2 arrays over rooted shapes (`--stop-first`, no aborts):

```text
delta=284  m=16 r=8 : 115 shapes,   7 with structures  (merged SHA-256 18082a3a9062f712b36d58c229c1a1cb875c2a1ca07e0f04cd6146a1de46787b)
delta=285  m=15 r=9 : 286 shapes,  95 with structures  (merged SHA-256 ac29908f71d1d20f8688278daeeb7fc7149b4fee5d8f5a7ec06da1a0df6019f1)
delta=286  m=14 r=10: 719 shapes,  317 with structures  (Hoffman2 array 115949; merged SHA-256 2f91a166a5ca9adfbbac0445782358c0ec7b9149e49e3d30aacef40ffac21723)
delta=287  m=13 r=11: 1842 shapes, 1523 with structures (Hoffman2 array 115950; merged SHA-256 048883d27554d51113576fe2a7dfbf27c946f4f4c7461f4e7e886c28c4a83aa3)
```

The depth phase for the 7 (`delta = 284`) and 95 (`delta = 285`) shapes
with structures is running on Hoffman2 as prefix-split arrays of
`abstract_class_search7` (one labeled representative per
rooted-isomorphism class; the CSP only requires each low vertex to be deeper
than its parent, so a representative suffices).  Status at 2026-09-02
00:30 PDT: for `delta = 284` all 64 tasks have finished the six non-chain
shapes (partial per-task sums over 36 tasks: leaves 1.6M–4.2M per shape,
`depth_survivors = 0` everywhere, and the per-task leaf counts coincide with
the independently run per-leaf implementation `abstract_class_search_v4` on
the same splits) and are working on the chain `0,1,2,3,4,5,6`, whose
1/64 slice has 366,635,322 abstract nodes and 22,547,805 leaves (local
probe), i.e. about 2.3e10 nodes and 1.4e9 leaves in total; the memoized
rho-level CSP is the bottleneck.  The first finished task (split 10) shows
the actual cost: chain slice `leaves=21496630 nodes=366044262
rho_csp_runs=653421` (memo ratio 33) `csp_nodes=3417469778
depth_survivors=0`, about two hours per task including the six other
shapes.  Collect with

```bash
python3 verify_depth_splits.py depthv7_r8 64 --m 16 --shapes shapes_r8_exists.txt --out depthv7_r8/certificate.json
python3 verify_depth_splits.py depthv7_r9 256 --m 15 --shapes shapes_r9_exists.txt --out depthv7_r9/certificate.json
```

(`VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY` with `errors=[]` is the acceptance
criterion; any `.tmp` left by a task that hit the 24 h limit is reported as
an error and that split must be rerun with a finer `--split`.)

**Result for `delta = 284` (2026-09-02 07:05 EDT).**  All 64 tasks of
Hoffman2 array `118375` (`abstract_class_search7`, prefix split at level 5,
one representative per rooted low-tree class, tasks 2h02–3h52 each)
finished; `verify_depth_splits.py` returned
`VERIFIED_DEPTH_SPLITS_EXHAUSTED_EMPTY`, `errors=[]`:

```text
shape            leaves        nodes          distinct rho   csp_nodes       survivors
0,0,1,3,4,5,6    3,018,576     1,905,844,936     219,758     6,060,630,718   0
0,1,1,2,4,5,6    3,094,884     1,925,488,408     226,254       777,654,870   0
0,1,2,2,3,5,6    3,180,114     1,953,706,332     233,464       742,211,809   0
0,1,2,3,3,4,6    3,281,182     2,007,391,240     242,116       847,594,294   0
0,1,2,3,4,4,5    3,428,058     2,229,724,050     256,082       899,376,730   0
0,1,2,3,4,5,5    7,329,832     4,285,409,714     567,932     2,006,443,404   0
0,1,2,3,4,5,6 1,618,164,436   25,005,269,686  47,467,069   244,492,129,704   0
TOTAL         1,641,497,082   39,312,834,366  49,212,675   255,826,041,529   0
certificate depthv7_r8/certificate.json SHA-256 b5769434011afa56dcc3d124f0bacfb831052b7fe3e39a699d837589248ca6be
merged split outputs all_splits_sorted.txt SHA-256 bccd6ab737e1a5aff30944bf82d3bd4506b9edc5c49721f6166e8a335ddd7b55
```

(The 108 other rooted low-tree classes have no depth-free structure, array
115734, merged SHA-256 18082a3a… in §3.8.)  For the six non-chain shapes the
per-split leaf counts also agree with the independent per-leaf implementation
`abstract_class_search_v4` (array 115848, cancelled before finishing the
chain).  Hence **no S1-284 candidate exists** for any `s` and any low
structure.  The singleton branch, and by §3.10 the whole order-25 problem,
now starts at `delta = 285` (running, array 118376).

### 3.9 Controller provenance audit (2026-09-02)

The mathematical crowding argument in §2 is sound after correcting its
wording: the high-LCA class is bounded because its *distances* lie in
`[1,2m-3]`; it is not true that `q` is determined by `y+y'`.  The current
source/binary provenance is not yet closed: the historical hash recorded for
`abstract_class_search.cpp` (`3a7a...`) differs from the current source hash
(`e72d...`) on all three visible copies, and the running
`abstract_class_search_v4` binary has a separate hash.  Therefore the
numerical zero counts for `delta=281..283` remain useful finite evidence,
but their certification label is provisional until an exact source hash,
binary hash, command line, and output hash are linked for each run.  The
`delta=284,285` depth arrays remain `RUNNING/UNKNOWN` while their files are
still `.tmp`.

### 3.10 Ordinary Chat advisor audit (2026-09-02)

The ordinary Chat advisor independently reviewed §2 and found no
low-connectivity or LCA-class coverage gap. It agrees that the crowding
inequality is valid after the proof repair in §2, and that the `delta=281,282`
depth-free searches have complete parent-choice quantifiers. It also clarifies
that the `delta=283` Geo/Hoffman2 agreement is independent execution/partition
evidence, not a second algorithm; a separate depth checker would be the
minimal stronger cross-check if a two-implementation standard is required.

For `delta >= 284`, the advisor's highest-value structural proposal is a
sound component-mass / low-LCA capacity prefilter. If high components attached
at low vertex `v` have sizes `n_{v,j}` and `M_v` is the total high mass below
`v`, then

```text
W   = sum_{v,j} C(n_{v,j},2) <= 2m-3
P_v = C(M_v,2) - sum_{u child of v} C(M_u,2) - sum_j C(n_{v,j},2) <= 2m-3
W + sum_v P_v = C(m,2)
```

These are necessary conditions independent of high labels, `s`, and low
depths. They can be followed by depth-interval/Hall propagation before the
full `(s,L)` CSP. No safe monotone implication from `delta=284` to larger
`delta` was found.

### 3.4 `hh_capacity.cpp`

Exact maxima `Cap(m)` (cross-branch pairs with distinct sums) and `W(m)`
(within-forest pairs with distinct distances).  Both equal or nearly equal the
trivial bound `2m-3` for `m <= 14` (`Cap(m) = 2m-3` is attained by the block
pattern `{0}, {m-1}, {1..m-2}`), so the crude per-class capacity cannot be
improved by a better single-class bound; `delta >= 281` needs the joint
search of 3.3 with `L`-dependent constraints.

## 3.10 Diametral-endpoint reduction (2026-09-02, theorem)

Let `(a,b)` be the unique pair at distance `300` (unique since distances are
distinct; both are leaves), `P` the `a`–`b` path.  For `u ∉ {a,b}` let
`p(u)` be the position on `P` of the vertex of `P` closest to `u`, `h(u)` its
distance to `P`, and put `e(u) = 300 − d(a,u) = 300 − p − h ≥ 1`,
`f(u) = 300 − d(b,u) = p − h ≥ 1`.  For `u,v ∉ {a,b}` with `p(u) ≤ p(v)`
one has `d(u,v) = 300 − f(u) − e(v) − 2h_c` with `h_c ≥ 0` (the height above
`P` of their last common vertex when they hang in the same branch, else 0).
Hence every pair avoiding `a` and `b` has distance `≤ 298`, so `299` is
`d(a,w)` or `d(b,w)`; renaming, `d(a,w) = 299`, `diam(T−b) = 299`, and
`diam(T−a) ≤ 298`.  With §2–3.7 (`diam(T−ℓ) ≥ 284` for every leaf `ℓ`),

```text
284 <= diam(T − a) <= 298,   i.e.  r = diam(T−a) − 276 ∈ [8,22],  m = 24 − r ∈ [2,16].
```

Independent adversarial check (subagent, 2026-09-02, random-tree brute force
on all identities plus the known Leech trees): claims verified; two
degenerate-case caveats — the per-class bound is `max(0,2m−3)` (only `m ≥ 2`
is ever used), and "the low vertices form a connected subtree containing `x`"
needs `r ≥ 1`, i.e. `s ≤ δ`; side condition `s ≤ δ+1−r` since the `r` low
depths must fit below `B`.  Free strengthening: after the renaming,
`f(u) ≥ 2` for every `u ∉ {a,b}` (the unique `299`-pair is `(a,w)`), so pairs
avoiding `a` and `b` have distance `≤ 297`, and if `diam(T−a) = 298` the
attaining pair contains `b`.

**Consequence.**  The order-25 problem is reduced to the singleton normal
form of §1 for the leaf `a` alone: if no tree of the normal form exists for
any `δ ∈ [284,298]`, any `s` and any low structure, then no order-25 Leech
tree exists.  The reduction uses only the spectrum identity for the leaf `a`;
the "heaviest edge is pendant" hypothesis of the earlier S1 notes is not
needed, and the two-vertex/larger final-cap branches of the earlier programme
become unnecessary.  The other endpoint `b` has `diam(T−b) = 299` and carries
no top-block information.  `δ = 284` is certified (§3.9), `δ = 285` is being computed; `δ ≥ 286`
(`m ≤ 14`) is where depth-free structures become generic and a second anchor
(the forcing lemma on the smallest edge weights of `K`) will be needed.

## 3.11 Second implementations queued (2026-09-02 07:20 EDT)

* Provenance re-run of `δ = 281, 282, 283` from the frozen source
  `frozen/abstract_class_search_d83323870704.cpp` on Geo Workstation
  (`rerun_frozen/results.txt`, one `nice -n 15` process, done 08:20 EDT,
  SHA-256 `4d9ec4985f45d24fce96b54bec3c580535dd657b8341118d2f9af9195fd88511`):
  `δ = 281` (9 classes) and `δ = 282` (20 classes) `NO_STRUCTURE`;
  `δ = 283`: 48 classes, only the chain has structures, chain depth phase
  `leaves=14730 nodes=932540226 depth_survivors=0 rho_csp_runs=2045
  csp_nodes=3665441` — all identical to the original runs.  So the
  certificates for `δ = 281, 282, 283` are now reproduced from the single
  frozen source (only `δ = 284`, about 130 CPU-hours, has not been re-run
  from it).
* Unmemoised second pass of the `δ = 284` chain shape with the per-leaf
  implementation `abstract_class_search_v4` (Hoffman2 array `118830`, 64 prefix
  splits, output `depth_r8chain_v4/`): queued behind the `δ = 285` array.
  Acceptance: same per-split leaf counts as `depthv7_r8` and zero survivors.

## 3.12 Source snapshots

The search sources were edited during the day (memoisation, sharding,
progress output); each run records the SHA-256 of the source it used.  The
final sources are frozen with hash-tagged names in
`theory-lab/s1_crowding/frozen/` (e.g. `abstract_class_search_d83323870704.cpp`).
The enumeration logic of `abstract_class_search.cpp` (depth-free DFS, class
bitsets) is unchanged since the first version; the third δ=283 run with the
final source reproduced `leaves=14730`, `depth_survivors=0`.

## 4. What remains open

By §3.10 the whole order-25 problem is the singleton normal form for
`δ ∈ [285, 298]`; `δ = 285` is running (§3.9), `δ ∈ [286, 298]` are open.
Nothing here claims global nonexistence.  For the first `delta`
at which depth-free structures exist, the next tool is the depth-dependent
search of 3.2 generalised to `r` low vertices with the low depths `L` chosen
inside the search.
