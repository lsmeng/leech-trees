# Exactly three branch vertices: normal form and search boundary

**OBSERVED normal form, generator audit and exact exclusions at orders 18, 25
and 27; UNVERIFIED uniform Leech exclusion.** This note records the completed
finite parts of Phase II-B. It does not claim an all-order three-branch theorem
or exclude order-25/order-27 trees with four or more branch vertices.

## 1. Normal form

A branch vertex means a vertex of unweighted degree at least three. If a tree
has exactly three branch vertices, call them `c0,c1,c2`. Their minimal
connecting subtree is a path with one of the three branch vertices in the
middle. Indeed, if the median of the three were a fourth vertex, its three
internally disjoint incident paths would give it degree at least three, a
contradiction.

After ordering the endpoints, the branch skeleton is therefore

```text
c0 ----(p edges)---- c1 ----(q edges)---- c2,       p,q >= 1.
```

No off-skeleton path can attach to an internal vertex of either segment: that
would make the attachment vertex a fourth branch vertex. Every remaining
component is a path attached at one of `c0,c1,c2`; otherwise it would itself
contain a branch vertex. Thus the whole topology is specified by

```text
(p, left-leg partition, middle-leg partition, q, right-leg partition),
```

where the end partitions have at least two parts and the middle partition has
at least one. The only residual skeleton symmetry is simultaneous reversal

```text
(p,left,q,right) <-> (q,right,p,left).
```

This proves that `gen_shapes.py threebranch n` is exhaustive once one
representative of that reversal is retained.

## 2. Independent topology audits

`theory-lab/exp-families/verify_threebranch_shapes.py` performs two checks.

1. For every order `2<=n<=13`, NetworkX independently enumerates all
   nonisomorphic trees. Filtering for exactly three branch vertices and
   matching by exact graph isomorphism gives a bijection with the constructive
   generator. The nonzero counts are

   ```text
   n:      8   9   10   11   12   13
   count:  1   5   22   74   219  576
   ```

2. A separate partition-number/Burnside calculation checks the generator
   counts through order 25. If `C` marks a positive core-segment length, `E`
   an end-leg partition with at least two parts, and `M` a nonempty middle-leg
   partition, the oriented series is `x*C^2*E^2*M`. Reflection fixes exactly
   `p=q` and `left=right`; averaging the oriented and fixed coefficients gives
   the unoriented count. The order-25 coefficient and generator count agree:

   ```text
   three-branch topologies at n=25: 1,437,739
   ```

Reproduce both checks with

```text
.venv/bin/python theory-lab/exp-families/verify_threebranch_shapes.py 13 25
```

## 3. Fixed-topology calibration route

The generator emits sound automorphism tags for equal-length legs at a fixed
centre. `validate.py` checks the exact orbit identity

```text
untagged count = tagged count * product_g (# equal branches in g)!
```

including a three-branch example. The same validation run checks the generic
fixed-topology engine on every nonisomorphic tree through order 11, compares
it with the pure-Python reference through order 9, and sends every positive
witness through both `src/checker_a.py` and `src/checker_b.py`.

```text
.venv/bin/python theory-lab/exp-families/validate.py
```

The fixed-topology engine is exact only when `capped=0`. It is useful as an
independent calibration oracle and for small skeletons, but 1,437,739 order-25
topologies make a blind topology-by-topology exhaustion a poor primary route.
In particular, `found=0,capped=1` is `UNKNOWN`, not `UNSAT`.

## 4. Exact three-centre prototype

`theory-lab/threebranch/threebranch_cleanroom.py` now works with the three
weighted centres directly. Relative to the unique distance-`N` pair, mirror
symmetry leaves four anchor types: `AA` (same end), `BB` (same middle), `AB`
(end--middle), and `AC` (opposite ends). Core-spine marks and leg marks share
one explicit tree-metric formula. The search descends through the greatest
missing distance and adds the one or two absent endpoints that realize it.

The first validation ladder is **OBSERVED**:

- independent brute anchor loops and the universal fresh-leg cap agree for
  every valid anchor at orders 8 and 9;
- a separate adjacency traversal agrees with the geometric distance formula
  on 48 anchors;
- solved one/two-mark options equal brute enumeration on 12 anchors;
- the geometric and fixed-topology engines both find zero solutions at orders
  8 and 9;
- all four geometric modes complete at order 10 with 12,289 valid anchors,
  107,677 states and zero solutions; the fixed-topology engine independently
  closes all 22 topologies with zero solutions.

Verifier and frozen summary:

```text
nice -n 10 python3 theory-lab/threebranch/verify_threebranch_cleanroom.py --max-order 10
theory-lab/threebranch/results/threebranch_cleanroom_certificate.json
```

The prototype recomputes all distances and scans all legal coordinates. Its
order-10 `AB` mode alone takes about 110 seconds in the calibration run, so it
is an audit oracle rather than a plausible order-25 engine.

The C/bitset implementation `threebranch_exact.c` now reproduces all Python
anchor, node and legal-child invariants through order 10, including each of the
four modes separately. Its explicit two-new-mark generator agrees with a
three-child brute positive probe. Paranoid full-distance recomputation and the
fast incremental mode agree through order 12, and the independent fixed-
topology engine agrees at order 11. The exact C ladder has continued through
order 15 with zero solutions; the order-15 total is 225,554 valid anchors and
25,379,164 states.

The finite one-mark pattern has now been promoted for a mathematical reason,
not from extrapolation. The shape-independent **OBSERVED anchored one-vertex
lemma** applies the tree four-point condition to the selected diameter pair and
proves that a greatest missing value can never first occur between two absent
vertices. The two-mark code is not dead—the synthetic non-anchored metric probe
has exactly three legal pair children—but it can soundly be disabled after the
distance-`N` pair is fixed. Proof and verifier:
`docs/anchored-one-vertex-lemma.md` and
`theory-lab/threebranch/verify_one_vertex_lemma.py`.

The stronger **OBSERVED diameter-endpoint introduction theorem** shows that a
new vertex need not be paired with an arbitrary selected vertex: its first
descending-distance occurrence must meet one of the two diameter tips. The C
option `--diameter-intro` applies this exact rule. Through orders 8--15 it
preserves all 40,704,104 nodes and 40,167,617 legal children while reducing
generated one-mark candidates from 705,215,286 to 294,821,373. Proof and
verifier: `docs/diameter-endpoint-introduction.md` and
`theory-lab/topwindow/verify_diameter_introduction.py`.

With both proved reductions enabled, the four exact order-18 anchor classes
are now complete: 756,300 valid anchors, 273,479,949 states, zero solutions and
zero frontier; the deepest missing offset is 43. The `geo-ws` rows are archived
under `theory-lab/threebranch/results/exact_n18_intro/`, and the verifier
rebuilds and reproduces all per-mode invariants locally:
`theory-lab/threebranch/verify_threebranch_n18.py`. Therefore **no order-18
Leech tree has exactly three branch vertices (OBSERVED computational
theorem)**. This finite result does not imply the same exclusion at order 25
by itself, and neither finite order implies a uniform theorem. A separate conservative run explicitly generated
29,931,056,264 two-new-mark candidates in the same four modes; none was legal,
and all node/child invariants agree with the theorem-reduced run. Its rows are
archived under `theory-lab/threebranch/results/exact_n18_conservative/`.

The C engine also supports an exact numeric top-window cutoff and a modulo
partition of the outer anchor parameter. A `K=3` audit at order 10 reproduces
every additive invariant and the maxima of the unsharded run. At order 18,
the first `W=25` survey has nonzero frontiers in all four modes (11,886 `AA`,
2,798 `BB`, 48,076 `AB`, 36,816 `AC`), so a 25-value window is demonstrably
too narrow for a uniform certificate. This is an **OBSERVED diagnostic**, not
a negative result. The completed order-25 `W=25` survey has the same status;
its nonzero frontier is recorded below.

## 5. Completed order-25 exact exclusion and remaining uniform task

Widening the same exact search to `W=60` closes every order-25 shard before the
cutoff. All 384 paranoid shards are `DONE`; their exact aggregate is

```text
anchors              6,137,463
nodes            14,164,880,449
candidate marks 117,889,380,986
solutions                     0
frontier                      0
deepest missing offset       51
```

The source hash is unchanged from the audited order-18 and `W=25` runs. A
bounded-concurrency resumable runner checks every completed summary and sends
any reported witness through both repository checkers. Its `n=10` sharded
aggregate agrees exactly with the unsharded invariant. The order-25 raw shard
archive is deterministic, contains all 384 stdout and 384 empty stderr files,
and is replayed by
`theory-lab/threebranch/verify_threebranch_n25.py`; frozen summary:
`theory-lab/threebranch/results/threebranch_n25_w60_certificate.json`.

Therefore **no order-25 Leech tree has exactly three branch vertices
(OBSERVED computational theorem)**. Together with the uniform no-bi-spider
theorem, any hypothetical order-25 Leech tree has at least four branch
vertices; together with the diameter-four campaign, it has hop-diameter at
least five. These are finite restrictions, not arbitrary order-25 or all-order
nonexistence.

The next Taylor order supplies an independent width/stability point. At
order 27, `W=70` closes all four anchor modes in 128 shards each. All 512
paranoid shards are `DONE`; their aggregate is

```text
anchors              10,055,214
nodes             33,425,785,566
candidate marks  283,606,352,230
solutions                       0
frontier                        0
deepest missing offset         52
maximum non-centre marks       15
```

The source and runner hashes are unchanged. The deterministic archive has
512 stdout and 512 empty stderr members and is replayed, including the double
witness-checker gate, by `theory-lab/threebranch/verify_threebranch_n27.py`;
frozen summary:
`theory-lab/threebranch/results/threebranch_n27_w70_certificate.json`.
Therefore **no order-27 Leech tree has exactly three branch vertices
(OBSERVED computational theorem)**. The near-identical order-25/order-27
depth and mark bounds motivate a parameter-independent affine window, but do
not prove one. Trees with four or more branch vertices and the all-order
three-centre claim remain **UNVERIFIED**.

The remaining scalable implementation must convert the exact high-value case
tree into bounded offset states independent of `n`. The uniform acceptance
ladder still requires:

1. add broader planted positive distinct-distance controls;
2. build a bounded top-window implementation independent of the exact C
   engine;
3. obtain paired per-regime invariants for stable parameter tails;
4. extract and independently audit stable affine regimes covering all orders.

Until that uniform ladder is complete, exclusion of exactly-three-branch Leech
trees at all orders remains **UNVERIFIED**.

## Completed order-25 width-25 diagnostic

**OBSERVED diagnostic; not an UNSAT result.** The diameter-endpoint,
one-new-vertex C engine has completed all four anchor modes in six exact shards
each at `n=25` with cutoff `W=25`. The aggregate is

```text
anchors              6,137,463
nodes            14,148,916,526
candidate marks 115,997,756,795
solutions                     0
frontier            166,321,078
```

Every mode has nonzero aggregate frontier (`AA 3,543,964`, `BB 700,550`,
`AB 44,969,254`, `AC 117,107,310`). Therefore the only promoted conclusion is
that width 25 is insufficient; zero solutions among the closed states does not
exclude the frontier. The 24 archived outputs have empty stderr, an exact
mode/shard partition and source/archive hashes checked by
`theory-lab/threebranch/verify_threebranch_window_n25.py`; frozen summary:
`theory-lab/threebranch/results/threebranch_window_n25_certificate.json`.
