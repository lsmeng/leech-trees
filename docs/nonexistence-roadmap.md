# General nonexistence roadmap

**UNVERIFIED PROGRAMME — 2026-08-21.**  This document is a research plan, not
a proof that the five known Leech trees are the only ones.  It separates the
proved computational baseline from the remaining proposed stages: attack
three branch vertices and short hop-diameter, then extract a global descent
theorem.  The no-bi-spider theorem is complete for `n>=18`, but the stronger
range `n>=7` is not.  Every promoted theorem
must still satisfy the verification rules in Section 8.

## 1. Objective and terminology

A *branch vertex* has unweighted degree at least three.  In this programme:

- a `spider` has at most one branch vertex;
- a `bi-spider` has at most two branch vertices;
- a *three-branch tree* has exactly three branch vertices (the informal name
  `tri-spider` is avoided until a precise normal form is fixed);
- *hop-diameter* is the number of edges, ignoring weights, on a longest path.

The ultimate target is

> **UNVERIFIED target G.** No Leech tree has order `n>=7`.

By Taylor's necessary condition, the only orders to consider are `n=m^2` and
`n=m^2+2`.  The first open orders after the completed order-18 theorem are
`25,27,36,38,49,51,...`.  Consequently target G is an infinite structural
problem, not a feasible order-by-order extension of the order-18 forest run.

## 2. Proved and observed baseline

| Scope | status | current boundary |
|---|---|---|
| all trees through order 24 | **OBSERVED / LITERATURE** | the repository proves order 18; Taylor excludes 19--24; the five known trees are the only ones through 24 |
| spiders, every order | **OBSERVED** | no spider Leech tree exists for `n>=5`; complete verifier and independent adversarial audit |
| bi-spiders at orders 25 and 27 | **OBSERVED** | exact searches close both orders with zero solutions; small-order production/clean-room checks agree |
| uniform `LR` bi-spiders | **OBSERVED for `n>=18`** | seven paired finite relaxations; the last stable-tail certificate and `N>=153` bridge close the bounded middle strip |
| uniform `LL` bi-spiders | **OBSERVED for `n>=18`** | three paired W=36 relaxations cover all 2,305 finite regimes and have zero frontier |
| all bi-spiders | **OBSERVED for `n>=18`** | the `LR` and `LL` partitions are exhaustive; every target-order tree has at least three branch vertices |
| exactly-three-branch topology normal form | **OBSERVED** | constructive generator is bijective against all nonisomorphic trees through 13; independent Burnside counts agree through 25 |
| exactly-three-branch trees at order 18 | **OBSERVED** | four exact anchor classes close 756,300 anchors and 273,479,949 states with zero solutions/frontier; local and `geo-ws` invariants agree |
| exactly-three-branch `n=25,W=25` diagnostic | **OBSERVED / UNVERIFIED** | all 24 shards finish 14,148,916,526 states with zero solutions but 166,321,078 frontier states; the width is insufficient, so no UNSAT verdict |
| exactly-three-branch trees at order 25 | **OBSERVED** | all 384 paranoid `W=60` shards finish 14,164,880,449 states with zero solutions and zero frontier; deterministic raw archive and aggregate verifier |
| exactly-three-branch trees at order 27 | **OBSERVED** | all 512 paranoid `W=70` shards finish 33,425,785,566 states with zero solutions and zero frontier; deepest offset 52 and at most 15 non-centre marks; deterministic raw archive and aggregate verifier |
| order-four high-pole `AC` endpoint | **OBSERVED conditional all-order exclusion** | all 418 outside-band/common-trunk symbolic classes: 27 feasible seeds, one legal first child, then zero top-80 saturations, zero legal second children and zero solver unknowns |
| order-three high-pole `AC` endpoint | **OBSERVED conditional all-order exclusion** | all 218 outside-band/common-trunk symbolic classes: 18 feasible seeds; child counts 10,6,2,0 across four introductions; every intervening saturation count and every solver-unknown count is zero |
| order-one/two low-pole endpoint | **OBSERVED conditional handoff / UNVERIFIED global absorption** | `mu<=H` is excluded; for `mu>H`, factor collisions and exact empty layers eliminate every symmetric/small-factor terminal, so all five order-one and 13 order-two band states hand strictly to an internal `B` edge of weight at least `t-h+1` |
| at-most-three-branch two-small-factor terminal | **OBSERVED conditional all-order exclusion** | full high-spectrum recursion gives 1,199 top-113 rows; coherent LCA layers plus rooted hierarchy leave 34 rows (`31 K=3`, `3 K=2`); FW195 excludes all three `K=2` rows and FW198--FW202 exclude all 31 `K=3` rows, the last eight through a 30,346-configuration mixed-H replay with no frontier/unknown/cap hit; this closes the present affine terminal, not the other thick-centre or higher-global-branch cases |
| anchored one-vertex completion | **OBSERVED** | tree four-point lemma eliminates every two-new-vertex branch after the diameter pair is selected; conservative/pruned searches agree through 15 |
| diameter-endpoint introduction | **OBSERVED** | every new vertex in descending distance order first appears with a diameter endpoint; exact C invariants agree through 15 with 58.2% fewer generated candidates |
| top-window connectivity | **OBSERVED** | the pairs at distances `N,N-1,...,N-q` form a connected far-pair graph in that edge order and use at most `q+2` vertices |
| far-pair crowding and pole cover | **OBSERVED** | every matching of pairs at distance at least `N-q` has `k^2<=2q+1`; all such pairs meet at most `2 floor(sqrt(2q+1))` vertices |
| diameter-cap/deep-offshoot dichotomy | **OBSERVED** | every `q`-far pair is oppositely oriented relative to a fixed diameter; each endpoint lies in a weighted `3q` endpoint cap or more than `q` deep off the diameter |
| far-neighbour common cone | **OBSERVED** | for `2q<N`, all far edges incident with one vertex share a tree direction for at least `N/2-q`; diameter domination gives far-graph hop-diameter at most 3 |
| central-edge sumset descent | **OBSERVED** | cutting the metric-centre edge gives injective radial-deficit sumsets; above the larger half-diameter they exactly tile an initial deficit interval |
| edge-cut equality rigidity | **OBSERVED** | at any edge, equality in `w<=N+1-ab` occurs only in the known orders 2,3,4; every order at least 5 has strict excess |
| edge-cut bounded handoff | **OBSERVED** | every edge with `ab>=11` has some distance in `w+1,...,w+10` wholly in a proper side; compatible rooted cross sums cannot cover `0,...,10` |
| edge-cut finite excess ladder | **OBSERVED / UNVERIFIED** | exact cut-product budgets through `E=8` force heaviest-edge `E>=3,7,9` at target pairs 25/27, 36/38, 49/51; asymptotic continuation is unproved |
| rooted-span and weighted excess bounds | **OBSERVED / UNVERIFIED** | exact moment weights each excess by its cut product; an all-order rooted-span bound is quadratic on unbalanced cuts, but the combination still kills 0/123,867 order-18 topologies |
| handoff orientation sink | **OBSERVED / UNVERIFIED** | every degree-two sink is excluded; in a singleton thin pole an exact three-defect identity forces at least `(1-sqrt(2/5))n-O(1)` vertices into third-and-lower arms, while exclusion of the thick-third/scale/pole interfaces and non-singleton thick cores remains open |
| Kruskal covering and merge waste | **OBSERVED** | the light-edge merge profile gives an exact covering schedule and `TW>=(sum Delta_k^2-N)/2`; the missing piece is a terminal-profile upper bound |
| arbitrary order-25 trees | **UNVERIFIED** | every hypothetical survivor has at least four branch vertices and hop-diameter at least five |
| arbitrary order-27 trees | **UNVERIFIED** | the exactly-three-branch class is excluded, but trees with four or more branch vertices are not |
| hop-diameter at most four | **OBSERVED / LITERATURE through order 25** | paired engines reproduce the five known trees through 18; Taylor covers 19--24; all 512 order-25 shards are `DONE` with zero solutions and a frozen aggregate |

The current generic forest engine is not the route to order 25: extrapolation
is `10^16`--`10^17` states.  The caterpillar-restricted run exhibits the same
barrier, reaching 3.3 billion states already at level 13.  These are
**OBSERVED decision outputs**: do not launch a full bottom-up order-25 run
without a new prune or a different decomposition.

## 3. Dependency chain

The intended chain is

```text
uniform spider theorem                         [done]
        |
uniform bi-spider theorem                      [done for n>=18]
        |
order-25 three-branch + short-diameter cases   [Phase II]
        |
local thin/thick transition lemmas
        |
global descent + thick-tip contradiction       [Phase III]
        |
finite candidate bound, then finite base runs
```

The arrows are not automatic logical implications.  Each phase must export
parameter-independent lemmas and a complete catalogue of its surviving local
states.  A fixed order-25 exhaustion by itself is evidence and a useful test,
but it is not a lemma about all orders.

## 4. Phase I — uniform bi-spider theorem

### I-A. Close the fixed-width `LR` boundary

**OBSERVED — complete for every `n>=18`.**  Paired W=20 searches close both
`1<=A<=50`, `B>20`, `r=Q-(B-A)>20` and the complementary `B<=20`, `r>20`
strip.  A paired W=15 search closes `1<=A<=15`, `r<-15`; together with the
earlier dominant-tip region this eliminates the whole negative tail.  The only
remaining `LR` space was

```text
-15 <= r <= 20:     A <= 50
```

Here `r` has 36 values and `h=N-2A`.  The completed W=35 verifier proves the
stable tail

```text
h > max(35, 2(35-A)+abs(r))
```

for every one of the `50*36=1,800` `(A,r)` regimes.  Its incremental and
immutable full-recomputation implementations agree per regime on 1,386,587
states and zero frontier.  If `n>=18`, then `N>=153`, so
`h>=153-2A` is strictly above both threshold terms throughout the displayed
boundary.  Thus all LR anchors at the target orders are excluded.  Proof and
trust boundary: `docs/bispider-progress.md`; frozen certificate:
`theory-lab/catspider/results/bispider_middle_tail_certificate.json`.

### I-B. Classify and close `LL` anchors

**OBSERVED — complete for every `n>=18`.**  Write the two same-side tip depths
as `T>U`, put `delta=T-U` and `L=U-Q`, and use the W=36 top window.  The
classification has three disjoint and exhaustive cases:

```text
2<=U<=36;             U>36 and 1<=L<=36;             U>36 and L>36.
```

Their exact high-offset forms are respectively

```text
a+z, U+a+x;
a+z, delta+z+z';
a+z, delta+z+z', rho+c+c',       rho=delta+2Q=N-2L.
```

The last line is essential: even when the far centre lies outside the window,
right-leg marks near its tips remain visible.  Exact parameters through 36
and stable sentinel 37 reduce the three cases to 630, 1,332 and 343 regimes.
A canonical-state prover and three separately written immutable searches agree
per regime on 740,594 states and zero frontier.  The verifier also audits
624,389 actual anchors at orders 18--40, and the paranoid exact C engine closes
all 2,825 order-18 LL anchors independently.  Proof and trust boundary:
`docs/bispider-progress.md`; frozen certificate:
`theory-lab/catspider/results/bispider_ll_certificate.json`; adversarial audit:
`docs/referee-bispider-n18.md`.

### I-C. The Phase-I deliverable

The immediate deliverable for the requested global range is complete:

> **OBSERVED target B18.** No bi-spider Leech tree exists for `n>=18`.

The stronger historical target remains separate:

> **UNVERIFIED target B.** The order-six double star is the only bi-spider
> Leech tree with two branch vertices; in particular no bi-spider exists for
> `n>=7`.

The completed B18 theorem has a one-command verifier, frozen per-regime
invariants, clean-room comparisons and an adversarial proof review.  It
establishes the branching-complexity lower bound for the requested range:
every hypothetical Leech tree of order at least 18 has at least three branch
vertices.  Extending that statement down to order seven requires a new finite
base/boundary analysis and is still UNVERIFIED.

## 5. Phase II — order 25 with three branch vertices and short diameter

This phase contains two complementary searches.  They should not be conflated:
three branch vertices is a branching-complexity restriction, whereas
hop-diameter at most four allows many branch vertices but restricts their
layout.

### II-A. Recover and audit the hop-diameter-four engine

**OBSERVED recovery, audit, and order-25 restricted exclusion complete.**  The final
scratch source, its independent Python implementation and validation helpers
are now in `theory-lab/diameter4/`.  The C++ order-2--18 ladder, independent
solution counts through 13, planted positives, strongest-prune ablation and
two-architecture builds have been reproduced.  The five known outputs pass
both witness checkers.  Full proof and adversarial review are
`docs/diameter4-engine.md` and `docs/referee-diameter4.md`.

The original pre-run requirements are now satisfied:

1. Copy the final fixed source and its validation scripts into a dedicated
   repository directory; do not use stale instrumented binaries.
2. Re-derive and document the subforest invariant and every additional prune.
3. Differentially test planted diameter-four instances and reproduce the full
   order-2--18 count ladder locally.
4. Obtain an adversarial review of sharding, the shape invariant and all caps.
5. Run order 25 in 512 resumable shards, publishing shard counts, node totals
   and completion status.  The completed sweep used the offered `geo-ws` resource;
   any later Hoffman2 run must use `sbatch`.  A capped shard is `UNKNOWN`, never
   `UNSAT`.

The completed campaign reports 3,403,240.387 CPU-seconds (about 945.3 CPU-hours)
and 322,189,234,739 nodes including repeated pre-shard prefixes.  All 512
shards are `DONE` and the frozen aggregate verifier succeeds.

Acceptance criterion: zero solutions and zero unfinished shards, with a
reproducible aggregate verifier.  Any SAT witness must pass both
`src/checker_a.py` and `src/checker_b.py`.

The criterion is met: the aggregate has zero solutions and freezes every shard
stdout, the audited source, the exact campaign executable, and both checker
hashes in `theory-lab/diameter4/results/diameter4_n25_shards_certificate.json`.
This promotes only the hop-diameter-at-most-four order-25 exclusion to
**OBSERVED**; arbitrary order-25 trees remain **UNVERIFIED**.

### II-B. Build an exact three-branch-vertex search

**OBSERVED topology reduction and finite order-25 exclusion; UNVERIFIED uniform theorem.**  The normal form
is now fixed: the three branch vertices form a path, its two core segments have
positive hop lengths, the endpoint centres carry at least two path legs, and
the middle centre carries at least one.  A constructive generator is bijective
against all nonisomorphic trees through order 13.  A separate Burnside series
agrees with its counts through order 25, where the class contains 1,437,739
topologies.  Equal-leg symmetry tags pass the fixed-topology engine's exact
orbit test.  Proof and verifier: `docs/threebranch-engine.md` and
`theory-lab/exp-families/verify_threebranch_shapes.py`.

The exact full-recomputation prototype now partitions the unique distance-`N`
pair into four anchor types (`AA`, `BB`, `AB`, `AC`).  Independent brute anchor
and option enumerations audit the construction; the geometric and fixed-
topology routes agree through order 10, where 12,289 valid anchors and 107,677
geometric states give zero solutions.  This is **OBSERVED calibration**, not an
order-25 result.  The fixed-topology generator and Python geometric engine are
now independent small-order oracles, not intended order-25 primary engines.

The C/bitset implementation now agrees with the Python invariants through
order 10, has paired paranoid/fast checks through 12, agrees with the
fixed-topology route at 11, and completes the exact ladder through 15 with zero
solutions.  Order 15 has 225,554 anchors and 25,379,164 states.  The remaining
task is the zero-slack/top-window reduction from two centres to three; finite
exact runs are calibration only.  Proof and verifiers:
`docs/threebranch-engine.md`,
`theory-lab/threebranch/verify_threebranch_cleanroom.py`, and
`theory-lab/threebranch/verify_threebranch_exact.py`.

The shape-independent anchored one-vertex lemma is also complete: once the
diameter-`N` pair and all values above the current greatest gap are present,
the tree four-point property makes a two-new-vertex realization duplicate a
larger distance. This removes the dominant pair-option family from every later
top-down search. It is an **OBSERVED branching lemma**, not yet the local
thin-tip transition required by Phase III. Proof and audit:
`docs/anchored-one-vertex-lemma.md` and
`theory-lab/threebranch/verify_one_vertex_lemma.py`.

The stronger diameter-endpoint introduction theorem is implemented by
`--diameter-intro`. Combined with `--no-pairs`, it completes all four
order-18 anchor classes in 273,479,949 states with zero solutions and zero
frontier. The `geo-ws` archive and a local rebuild agree per mode. This is an
**OBSERVED finite-order exclusion** for exactly three branch vertices, not an
order-25 or all-order result. Verifier:
`theory-lab/threebranch/verify_threebranch_n18.py`.

The exact numeric window/shard mode is validated at order 10. A width-25 probe
at order 18 leaves frontier in every anchor class, and the completed order-25
`W=25` survey likewise leaves 166,321,078 frontier states. These are
**OBSERVED / UNVERIFIED diagnostics** showing that width 25 is too narrow.
The widened order-25 `W=60` campaign closes all four anchor classes in 384
paranoid shards:

```text
anchors              6,137,463
nodes            14,164,880,449
candidate marks 117,889,380,986
solutions                     0
frontier                      0
deepest missing offset       51
```

The deterministic raw archive has empty stderr for every shard; the source,
runner, archive, mode aggregates, exact shard partition and double-checker
witness gate are frozen by `theory-lab/threebranch/verify_threebranch_n25.py`.
This is an **OBSERVED finite-order exclusion** for exactly three branch
vertices. It does not replace the parameter-independent offset engine required
for a uniform theorem.

The finite order-25 validation ladder is now met:

1. Compare every shape/anchor regime with the generic forest engine on small
   orders.
2. Include positive planted controls and require both witness checkers.
3. Maintain paranoid full distance recomputation in certificate runs.
4. Implement an independent geometric enumerator for the smallest nontrivial
   orders before trusting the order-25 run.
5. All order-25 skeleton/anchor shards and their zero-frontier statistics are
   archived, not merely the solution count.

The acceptance criterion is met. Combined with the existing order-25
bi-spider result, any hypothetical order-25 Leech tree has at least four branch
vertices. Combined with II-A, it also has hop-diameter at least five. Both are
finite restrictions, not arbitrary-order nonexistence.

### II-C. Required lemma extraction

The value of Phase II to the general theorem depends on what is extracted from
the computation.  Every terminal or repeated case must be recorded as one of:

- a bounded offset configuration independent of `N`;
- a transition that moves the active near-diameter pair into a proper branch;
- a thick-tip configuration with a branch vertex within bounded weighted
  distance of an extreme tip; or
- a genuinely order-specific arithmetic obstruction.

Only the first three classes feed Phase III.  The fourth helps settle order 25
but does not advance an all-order theorem by itself.

## 6. Phase III — global descent

### III-A. Thin and thick deep tips

**UNVERIFIED definition programme.**  Fix a top window `N-q,...,N`.  A deep tip
is *q-thin* if its weighted `q`-neighbourhood contains no branch vertex, and
*q-thick* otherwise.  The precise definition must be invariant under
subdivision and must identify the branch in which a near-diameter pair lies.

The completed spider and proposed bi-/three-branch searches should supply the
finite realiser catalogues for one, two and three successive branch centres.

### III-B. Descent lemma

> **UNVERIFIED target D.** If both endpoints of a distance-`N` pair are thin,
> the exact tiling of a bounded top window forces another near-diameter pair
> inside a proper branch, with controlled loss in the window parameter.

The proof needs a well-founded measure.  The proposed measure is lexicographic:
the number of vertices in the active branch, then the number of unresolved
branch centres.  Moving to a proper branch must decrease this measure.  At the
same time the deficit `q` must remain bounded by an explicit recurrence; a
descent in which `q` grows without control is not useful.

Phase I supplies the base case with at most two branch vertices.  Phase II
tests the first nontrivial transition through a third centre and identifies
whether the proposed measure and deficit control are actually preserved.

### III-C. Thick-tip contradiction

If descent cannot continue, branch vertices accumulate near the extreme tips.
The intended contradiction combines four already identified ingredients:

1. top-window exact tilings and the pole-cover bound for near-diameter pairs;
2. weak-Sidon constraints on incident branch depths;
3. the `n-1` edge/vertex budget; and
4. the Kruskal merge-profile waste inequality, which penalises balanced heavy
   cuts.

The pole-cover component of item 1 is now **OBSERVED**.  If a matching contains
`k` pairs of distance at least `N-q`, the four-point property forces `k^2`
distinct distances into `[N-2q,N]`, so `k^2<=2q+1`.  Endpoints of a maximal
such matching therefore cover every `q`-far pair using at most
`2 floor(sqrt(2q+1))` vertices.  Proof and independent audit:
`docs/far-pair-crowding.md` and
`theory-lab/topwindow/verify_far_pair_crowding.py`.

The first localisation step of that bridge is now **OBSERVED**.  Relative to a
fixed diameter `(a,b)`, the four-point property orients every `q`-far pair so
that its endpoints are respectively `q`-far from `a` and `b`.  Projecting an
endpoint to `P(a,b)` shows that it is either within distance `3q` of the
opposite diameter endpoint or lies more than `q` deep in a proper off-diameter
component.  Thus every endpoint is rigorously classified as an endpoint cap, a
thin offshoot, or a thick offshoot.  Proof and audit:
`docs/diameter-cap-dichotomy.md` and
`theory-lab/topwindow/verify_diameter_cap_dichotomy.py`.

The still-unproved bridge is now narrower: enumerate the bounded-offset
geometry of the two diameter stars and their shared off-diameter trunks; then
show that every surviving thin trunk gives a strictly smaller component or
that the terminal thick profile contradicts the remaining arithmetic bounds.

The exact global split underlying that sentence is now **OBSERVED**. Every
distinct-distance tree has its metric centre strictly inside an edge. Cutting
there gives two integer radial-deficit sets `A,B` whose cross distances are
`N-(A+B)` with unique sums. If `D` is the larger within-half diameter and
`M=N-D`, the Leech interval forces `A+B` to tile `0,...,M-1` exactly once.
Thus for any fixed `C`, either a proper half contains a pair of distance at
least `N-C`, or the bounded prefix `0,...,C` is an exact two-set tiling. Proof
and audit: `docs/central-edge-sumset-descent.md` and
`theory-lab/topwindow/verify_central_edge_decomposition.py`.

This replaces the informal descent premise by a theorem. What remains is the
inheritance rule that lets the proper-half near-diameter pair carry enough
exact-window data to iterate, plus exclusion of the long mixed-radix tilings
that are possible for arbitrary sets but may be impossible for tree-realised
deficit sets.

The central split now has a sharper **OBSERVED** tree-realised routing
interface (FW203)--(FW204).  Apply the reflected-prefix gap lemma separately
to both central factors.  Unless one half is an FW76 rooted pole of order at
most four or contains the resulting proper-side gap edge, both factors are
blocked and the larger half-diameter satisfies `D>N/2`.  With `C=N-D`, the
internal diameter then either exposes a `C`-deep off-diameter endpoint (the
thin/thick terminal already named in III-A), or forces `C>N/4`, `D<3N/4` and
central cut product greater than `N/4`.  In the latter case both halves have
linear order, with smaller order greater than
`(n-sqrt(n(n+1)/2))/2`.  Thus arbitrary thick--thick geometry has been
replaced by three explicit outputs: proper-side gap descent, the existing
deep-offshoot terminal, or a macroscopic balanced cut.  At that stage their
absorption was **UNVERIFIED**; the shell observation below now closes the
generic fully-blocked handoff without claiming the offshoot already has cap
provenance.

The proper-side gap output is now **OBSERVED absorbed** by (FW205).  A gap
edge stays on the fixed global diameter inside one open metric half, so its
centre side automatically has full support.  Closing any bidirectional run at
its last endpoint-side boundary gives a thin cap.  Each further nonsymmetric
prefix step strictly lowers cap order; a nonpositive tail instead produces a
deep offshoot with strictly smaller deficit.  The finite recurrence therefore
ends at an FW76 cap of order at most four or at the existing deep-offshoot
terminal.  At this stage the remaining Phase III frontier was the small-pole
absorption, deep-offshoot exclusion, and FW204 balanced-cut contradiction;
the gap edge itself was no longer an independent open branch.

The balanced-cut output is now further constrained by the **OBSERVED**
first-hole mass theorem (FW206).  Its absent coefficient `C=N-D` is forced by
the already-used internal `D`-pair.  If `m,k` are the numbers of factor
vertices below that first hole, then `mk>=C`, both central sides have another
vertex above it, and consequently
`C<=floor((n-2)^2/4)` and
`D>=N-floor((n-2)^2/4)`.  In the FW204 residual, `C>N/4` also gives
`m+k>sqrt(N)` and one distinct level-`C` shell edge of weight at least two on
each side.  This replaces a merely balanced product by a large visible
factor core plus two named path edges.  It is not yet a collision: the next
step must use rooted ancestry/LCA differences among those visible vertices,
or prove that the two shell crossings force a smaller cap or deep offshoot.
Replay: `theory-lab/topwindow/verify_central_first_hole_mass.py`.

The balanced branch is now **OBSERVED absorbed as an independent terminal**
by (FW207).  The closure argument of FW205 applies to every fixed-diameter
edge strictly inside an open metric half; its initial gap assumption was not
used after locating that edge.  Start it at either FW206 shell.  The first
endpoint-cap radius is below `C`, and every nested nonsymmetric cap remains
strictly endpointward.  Hence finite cap-order descent ends either at an
FW76 cap of order at most four or at an FW93 deep offshoot with new deficit
`q'<C`.  The strict parameter makes this more than an arbitrary leaf-cap
observation.  The remaining global frontier is now the contextual small-cap
absorption and the strictly smaller-deficit deep-offshoot terminal; neither is yet
excluded.  Replay: `theory-lab/topwindow/verify_central_shell_cap_descent.py`.

The same level-`C` shell exists in every fully blocked FW204 state, including
the generic `h>=C+1` offshoot branch: coefficient `C` is absent because the
internal `D=N-C` pair has already used that global distance, so neither
reflected factor contains `C`, and both factor maxima are strictly above it.
The shell edge is therefore strictly open-half and FW207a applies.  This is
an **OBSERVED all-order absorption of the generic C-deep output** into the
same cap/deficit descent.  It fixes the former written scope seam without
invoking FW208 directly on a cap-free offshoot.

The deep continuation is now **OBSERVED well founded** by (FW208).  Its
complement diameter `E=N-q'` makes coefficient `q'` the first cross hole.
The zero-remainder case would represent `E` again using the cap root and the
old opposite endpoint, so every genuine deep step has `1<=q'<alpha`.  The
resulting shell inside the cap either reaches an FW76 pole or produces a new
deep step with `1<=q''<q'`.  Induction on positive deficit, with cap order as
the inner measure, terminates at an order-at-most-four cap.  This does not
delete the original endpoint pivot: the remaining Phase III object is a
small cap carrying its full pivot/descent history.  Turning that inherited
finite pole geometry into a collision or a proper-core induction remains
**UNVERIFIED**.  Replay:
`theory-lab/topwindow/verify_deep_offshoot_deficit_descent.py`.

The inherited cap is now **OBSERVED reduced to four exact digit/pivot
families** by (FW209).  With first-hole deficit `q_0=N-diam(D)`, its complete
FW76 pole factor forces the complement indicator below `q_0` to be the
canonical FW105 mixed-radix strip, and the hole condition is exactly
`chi_P(q_0)=1`.  Pair counting gives `q_0<=a(n-a)<=4(n-1)` and at least
`ceil(q_0/a)` visible complement vertices.  The complement diameter retains
the old opposite global endpoint and has the exact three-tip equation
`N=2k+r_0+q_0`, with `r_0>=1` and `r_0!=q_0`.  The remaining global task is
therefore a tree-realisation collision or proper-core induction for four
linear-width digit strips with inherited pivot history, rather than arbitrary
balanced/deep geometry.  This last exclusion remains **UNVERIFIED**.  Replay:
`theory-lab/topwindow/verify_terminal_cap_digit_pivot.py`.

The opposite endpoint now gives an **OBSERVED constant-width overlap
reduction** (FW210).  The visible-vertex count first sharpens to
`q_0<=a(n-a-1)<=4(n-5)`.  Following the absent level toward the opposite
endpoint requires a genuine split: it is either a strict open-half edge, or
it is the central edge and must be routed by the one-sided FW203--FW204
prefix before FW205--FW208 can be used.  In both cases one obtains a disjoint
opposite FW76 terminal `K` of radius below `q_0`.  If its first hole is `Q`,
then `q_0!=Q`, and the common top prefix consists only of `J times K` pairs:

```text
min(q_0,Q)<=|J||K|<=16.
```

When `q_0<Q`, both complete factors lie below `q_0`; exact indicator
truncation gives 19 oriented rectangles, and cap-internal distance collisions
leave 11, with `q_0 in {1,2,3,4,6,8}`.  When `Q<q_0`, only the strict
opposite-deficit reversal `Q<=16` follows; the high digits of the inherited
factor cannot be discarded at this stage.  FW212 below absorbs that reversal
by reorienting inner endpoint caps.  FW210 itself is not the global
exclusion.  Replay:
`theory-lab/topwindow/verify_terminal_cap_opposite_overlap.py`.

The 11 nonreversal rows now have an **OBSERVED exact periodic-lattice
stability form** (FW211).  If their factors are `(P,S)` and `q=|P||S|`, then
the `S`-complement indicator is exactly `P+q Z_>=0`.  Writing
`Q=tq+p_*`, the visible count is `w=t|P|+r`, and with `u` unseen complement
vertices besides the root,

```text
|S|(n-|S|-1)-Q=|S|u+delta,             0<=delta<=2,
N-Q-C(n-|S|,2)=C(|S|+1,2)+|S|u+delta.
```

The first `t` complete blocks also force rooted detour mass
`|P|^4 t^4/16-O(t^3)`.  Bounded capacity defect would therefore make a proper
order-`n-O(1)` complement both fixed-defect and nearly saturating at
`n^4/16-O(n^3)`.  FW213 supplies a global LCA branch-count alternative.  With
`D=(t-1)q+max(P)`, ancestor differences and fixed-LCA sums give

```text
C(|P|t,2)<=D+B_D(2D-1),
B>|P|t/(4|S|)-1.
```

Hence a near-saturated lattice forces at least `n/16-O(1)` global branch
vertices.  Only under the additional conditional hypothesis of at most
three global branch vertices do the eleven exact inequalities force `t<=29`,
at most 39 visible complement vertices, `Q<=154`, and `u>=n-44`;
FW203--FW212 do not supply that hypothesis.  What remains **UNVERIFIED** is a
collision or decreasing transfer for the global linear-branch output (and
for the high-coordinate remainder in the conditional subcase).  Replays:
`theory-lab/topwindow/verify_terminal_cap_periodic_lattice.py`.
`theory-lab/topwindow/verify_terminal_cap_lattice_lca_bound.py`.

The visible/unseen LCA partition removes the bounded-defect possibility
globally (FW214).  A lattice pair whose LCA is one of the visible complement
vertices has distance at most `2(Q-1)`, so there are at most that many such
pairs.  Every other LCA is one of the `u` unseen vertices or the root, and a
fixed LCA has at most `2D-1` coordinate sums.  Therefore

```text
C(|P|t,2)<=2(Q-1)+(u+1)(2D-1),
|P|t<=4|S|(u+3),
u>=ceil((n-56)/17).
```

The FW211 capacity defect is consequently at least
`ceil((n-56)/17)`, and FW213/FW214 together give `16B+u>n-24`.  What remains
**UNVERIFIED** is no longer a near-saturated core: it is the explicit linear
high-coordinate/branch-rich remainder.  Replay:
`theory-lab/topwindow/verify_terminal_cap_visible_unseen_balance.py`.

FW215 sharpens the branch-rich half into an **OBSERVED heavy-spine
alternative**.  At a high-coordinate LCA branch with `M` periodic points and
largest marked child `L`, cross-child distance uniqueness gives
`M(M-L)/2<=2D-1`; while `M>=s/2`, each heavy step therefore sheds at most
`8b-1<=31` points.  A visible descendant cannot retain half the lattice once
`s>=80`, so the heavy path has more than `s/[2(8b-1)]` hops.  In particular,

```text
n>=160 => u>=n/2-8 or H>n/124.
```

The next target is now narrow: classify the bounded-size pendant bundles
along this linear high spine and force an additive distance collision or a
strict decreasing transfer.  FW215 itself is not that exclusion.  Replay:
`theory-lab/topwindow/verify_terminal_cap_unseen_spine.py`.

FW216 adds a quadratic weighted-span constraint.  If `e_i<=8b-1` are the
successive shed bundle orders until fewer than `s/2` marked points remain,
then the disjoint shed--retained pair families satisfy

```text
C_sp>=ceil(3s^2/8-(8b-1)s/4-(8b-1)^2/2),
beta-Q>=ceil((C_sp-1)/2)-D=3s^2/16-O(bs).
```

This eliminates an artificially compressed long spine, but not a spine whose
unknown LCA translates use the available `Theta(n^2)` coordinate scale.  The
required next input remains an upper bound below this coefficient, an overlap
theorem for different translates, or a cap/full-support handoff.  Replay:
`theory-lab/topwindow/verify_terminal_cap_spine_span.py`.

Taylor parity separates four of the eleven rows (FW217).  Their periodic
factor has only even coordinates, so its `s` vertices occupy one Taylor
class.  For `n=k^2` or `k^2+2`,

```text
u>=(n-k)/2-a-b>=(n-k)/2-6.
```

Thus these rows feed an asymptotically half-order unseen core rather than an
order-`n` visible lattice.  Excluding that unseen core, and treating the seven
parity-balanced rows, remain **UNVERIFIED**.  Replay:
`theory-lab/topwindow/verify_terminal_cap_parity_routing.py`.

A second independent Max direction review found a shorter unconditional
entry (FW218).  Choose a global diameter endpoint `z` not used by the unique
distance-`N-1` pair.  Deleting it leaves diameter `N-1`; four-point equality
forces that pair to retain the opposite diameter endpoint `x`.  The endpoint
gate then gives the exact FW209 pivot with first hole one.  This directly
re-proves the singleton FW209a--e/FW210 data package without claiming the
historical FW208 provenance.  FW210's opposite terminal has radius below one,
so it is the endpoint singleton `{x}` and the only rectangle is

```text
(q,P,S)=(1,{0},{0}).
```

The complement-root hit can occur only through order four: for `n>=5`, a
root inside the visible band would force rooted depths `0,...,n-2`, hence a
star whose weights `1,2,3` repeat distance three.  Consequently every
hypothetical G18 counterexample enters the full FW211 `q=1` normal form.
This is an **OBSERVED all-order universal endpoint-one singleton extension**,
replayed by `theory-lab/topwindow/verify_universal_endpoint_one.py`; it
bypasses rather than excludes the other ten contextual rows.  The global
goal remains **UNVERIFIED**.  The next exact interface is now also
**OBSERVED** (FW219).  In the q=1 normal form the vertices above the first
hole, together with the complement root, form an ancestor-closed connected
induced proper core `H_Q` of order `u+1`; they are in exact bijection with all
holes of `Spec(T-x)` inside `[1,N-Q]`.  The `Q` visible vertices form pendant
components `W_i` with

```text
sum_i C(|W_i|,2)<=2Q-3,
#components>=ceil(Q^2/(5Q-6)),
max_i |W_i|<=floor((1+sqrt(16Q-23))/2),
Delta(A) intersect Delta(B)={0} at every LCA,
Q<=4u+7,  u>=ceil((n-9)/5),  4B+u>=n-4.
```

Replay: `theory-lab/topwindow/verify_q1_threshold_core.py`.  This removes the
fragmented-unseen ambiguity but does not make the `u+1` holes bounded defect.
A collision, a bounded catalogue of returns, or a strictly decreasing
contextual transfer remains **UNVERIFIED**.

The first cross-Sidon-only shortcut has been falsified at exactly its stated
interface.  An **OBSERVED negative diagnostic** repeatedly sheds the two
endpoints of the current q=1 coordinate interval and retains its middle.
Every stage satisfies `Delta(shed) intersect Delta(retained)={0}`; its FW216
shed--retained distance families occupy disjoint positive blocks inside the
global quadratic scale, while
`sum_i(e_i-1)=floor(Q/4)`.  This is an abstract relaxation, not a Leech-tree
witness, because the terminal retained topology and unmodeled pair classes
are unspecified.  It nevertheless stops the proposed derivation of bounded
total shedding from FW219/FW216 alone.  Replay:
`theory-lab/topwindow/probe_q1_cross_sidon_double_peel.py`.  The active route
is therefore the multi-boundary spectral interface of `H_Q`, not further
span or shedding-count lower bounds.

That active route now has its first strict decrease.  The **OBSERVED all-order
coordinate-zero smaller-cap bridge** (FW220) applies when `Q>=4`.  The visible
component `W_0` containing coordinate zero deletes an initial block of the
top spectrum and yields

```text
1<=q_*<=|W_0|<=floor((1+sqrt(16Q-23))/2)<Q.
```

If its entry is bidirectional, the first endpointward exit from the maximal
bidirectional region cuts a nested open-half dominant thin cap with first
hole at most `q_*`; if the entry is already thin, it is either open-half
dominant or central-thin.  Replay:
`theory-lab/topwindow/verify_q1_coordinate_zero_cap.py`.  This decreases the
local opposite hole from `Q` to `O(sqrt(Q))`, but no-return after cap
normalisation remains **UNVERIFIED**.  The next step must retain enough of the
two-boundary context to prevent a return to the original endpoint-one state.

The first part of that retained-context task is now complete.  The
**OBSERVED all-order q=1 small-return catalogue** (FW221) notes that every
nested cap used to normalise FW220 stays inside the original coordinate-zero
component, so its terminal pole has `q_0<=q_*<Q`.  The original opposite
endpoint edge has weight `g_x>=Q`, hence its level-`q_0` cap is still exactly
the singleton `{x}`.  The frozen FW210 table then leaves only

```text
(q_0,P,S)=(1,{0},{0}), (2,{0,1},{0}), (3,{0,1,2},{0}).
```

These are the endpoint singleton, rooted `L2`, and middle-rooted `L3`; `L6`
is a positive control for the last.  Replay:
`theory-lab/topwindow/verify_q1_small_return_catalogue.py`.  Thus arbitrary
return through any of the other eight FW210 rows is excluded.  The wrapper
left outside the small terminal cap and the three catalogue entries remain
**UNVERIFIED**, as do the original `Q=2,3` cases.

The catalogue now exports an exact proper-core spectral state.  The
**OBSERVED all-order q=1 bounded-defect return-core interface** (FW222) takes
the terminal cap `J` of order `a=1,2,3`, boundary `g`, and proper core
`D=T-J`.  If `R_D` is the rooted-depth polynomial of `D`, then

```text
I_N=F_D+I_C(a,2)+X^g(1+...+X^(a-1))R_D,
Spec(D) intersect [1,g-1]={C(a,2)+1,...,g-1}.
```

Hence the inherited prefix has exactly `0,1,3` fixed initial holes.  Replay:
`theory-lab/topwindow/verify_q1_return_prefix_interface.py`.  This meets the
spectral-interface half of the route, but not the decreasing-induction half:
the return still needs a collision or a strictly smaller contextual state.

The upper spectrum is now **OBSERVED exactly located** rather than
unrestricted (FW223).  Sort the rooted depths of `D` as
`0=s_0<...<s_(d-1)` and write `s_i-s_(i-1)=a+e_i`.  Then

```text
N+1-a(n-a)-g=sum e_i,
Spec(D) above g
  = disjoint union_i [g+s_(i-1)+a,g+s_i-1],
e_(d-1)=Q-a.
```

Thus the old opposite hole pins the last rooted-depth gap to exactly `Q`.
The boundary root has original coordinate `g+a-1`; it is either visible,
with `g<=Q-a` and a proper wrapper, or lies in `H_Q`, in which case the
returned cap is exactly `W_0` and `g>=Q-a+2`.  Replay:
`theory-lab/topwindow/verify_q1_return_gap_ladder.py`.  The remaining
`e_1,...,e_(d-2)` can still carry quadratic mass, so FW223 is a sharper
interface, not the missing induction or G18.

Peeling the return cap and the opposite endpoint simultaneously now gives an
exact smaller contextual state (FW224).  Put

```text
K=T-(J union {x}),  H=H_Q,  h=w(x,neighbor(x)),  M=N-Q.
```

Then the four pair/hole classes tile the smaller complete interval:

```text
I_M=F_K+I_C(a,2)+X^g A_a R_p(K)+X^h R_r(H),
X^hR_r(K)=X^hR_r(H)+I_[M+1,N-a].
```

In particular the old holes are a rooted polynomial of the connected core
`H`, and the other `Q-a` vertices form one consecutive rooted-depth block
at the opposite root.  Replay:
`theory-lab/topwindow/verify_q1_double_peel_tiling.py`.  The ambient maximum
has strictly dropped from `N` to `N-Q`, but another peel has not yet been
proved to preserve this four-class form; FW224 is therefore an exact
contextual interface, not the missing induction or G18.

The same state has an exact near-Leech stability form (FW225).  For
`k=|K|`, `C=binom(k,2)` and `L=(N-Q)-C`,

```text
L=a n+u+1-a(a+3)/2<=4n-14,
Spec(K)=([1,C] minus B_K) disjoint union O_K,
|B_K|=|O_K|=delta<=L,
O_K subseteq [C+1,C+L].
```

Thus the double-peeled proper tree is a linear-defect near-Leech core, not an
arbitrary distinct-distance tree.  Replay:
`theory-lab/topwindow/verify_q1_double_peel_stability.py`.  Bounded `delta`
feeds the finite-hole/endpoint-strip machinery; growing `delta` requires the
same number of low intrusions from the two rooted factors in FW224.  A
rooted-provenance stability/collision theorem remains **UNVERIFIED**.

The root-position split now separates those two regimes quantitatively
(FW226).  The width-`a` return blocks in FW224 are disjoint, so their rooted
starts are `a`-separated.  Partitioning those starts below, across and above
`C=binom(|K|,2)` gives

```text
delta+ceil((delta-binom(a,2))/a)>=|K|-ceil(g/a).
```

If the return root is visible, FW223 has `g<=Q-a`.  Together with
`u>=ceil((n-9)/5)`, this forces the exact linear scales

```text
a=1: delta>=n/10-O(1),
a=2: delta>=2n/5-O(1),
a=3: delta>=11n/20-O(1).
```

Replay: `theory-lab/topwindow/verify_q1_visible_return_defect.py`.  This is
an **OBSERVED all-order reduction**, not an exclusion: the two rooted factors
may still carry linearly many intrusions.  Its decisive routing consequence
is that bounded `delta` at unbounded order is possible only when the return
root lies in the connected threshold core.  The next bounded-defect task is
therefore a threshold-core catalogue/recursive state, while the growing-defect
task is a rooted-factor collision or energy inequality.

The bounded-defect side now has a giant-branch theorem (FW227).  Shell rooted
depths all lie in an interval of length at most `L-a`.  Pairs of shell
vertices in different components of `K-p` are distinct sums, hence

```text
sum_(i<j)b_i b_j<=2(L-a)+1.
```

For a fixed defect cap `Delta`, let
`c_0=Delta+ceil((Delta-binom(a,2))/a)`.  Above the explicit core-order
thresholds

```text
a=1: k>=2c_0+17,
a=2: k>=2c_0+24,
a=3: k>=2c_0+32,
```

one component `B` of `K-p` obeys

```text
|K-B|<=c_0+4a+3,       |T-B|<=c_0+5a+4,
```

and has at most two boundary edges in `T`.  Replay:
`theory-lab/topwindow/verify_q1_bounded_defect_giant_branch.py`.  This is an
**OBSERVED all-order topology compression**, not a recursive Leech theorem:
the bounded wrapper deletes linearly many pairs and its edge-weight catalogue
has not been closed.  The next exact target is the spectrum/provenance of
this giant branch under a one- or two-boundary deletion.

Taylor parity now removes four of the six bounded-defect Taylor/cap rows
(FW228).  If `epsilon` is the odd-outlier count minus the odd-hole count of
`K`, and `xi` is its parity-colour imbalance, then

```text
tau(k)-xi^2=4epsilon,       |epsilon|<=delta,
tau(k)=k or k-2 according as binom(k,2) is even or odd.
```

The known rooted parities of `J union {x}` transfer the original Taylor
imbalance `r` to `K` and give the exact defect floors

```text
                 a=1                 a=2                 a=3
n=r^2       r-2              floor((r-2)/2)       r-2
n=r^2+2     0                floor((r-1)/2)       1.
```

At large core order FW227 also has `g<=C-a+1`, so the entire root block lies
below `C` and `delta>=binom(a,2)+a`.  Replay:
`theory-lab/topwindow/verify_q1_double_peel_parity.py`.  Therefore the
bounded-wrapper catalogue needs only the two rows `(r^2+2,a=1)` and
`(r^2+2,a=3)`; square orders and `a=2` belong to the growing-defect pass.

The bounded catalogue is actually empty at unbounded order (FW229).  Let
`A_0` be the ancestor-closed ball of rooted depths at most `C-g` and put
`ell=ceil((delta-binom(a,2))/a)`.  At most `ell` vertices lie in `A_0`, while
at least `k-delta-ell` vertices lie in the shell.  Same-component shell pairs
use at most `2(L-a)` values; different-component pairs have one of at most
`ell` LCAs in `A_0`, each supplying a translate of only `2(L-a)+1` values.
Therefore

```text
binom(k-delta-ell,2)<=2(ell+1)(L-a)+ell.
```

This gives the exact uniform linear floors

```text
a=1: delta>=ceil((k-7)/12),
a=2: delta>=ceil((k-11)/9),
a=3: delta>=ceil((k-9)/8),
```

and asymptotic constant `a(3-2sqrt(2))/(a+1)`.  Replay:
`theory-lab/topwindow/verify_q1_shell_pair_quadratic.py`.  Thus no finite
bounded-wrapper enumeration is needed; all returns feed the rooted
linear-intrusion collision/energy task.

FW230 resolves how those low intrusions split between the two roots.  If
`q` low coefficients come from the width-`a` return blocks and `b` from the
connected-H factor, then

```text
delta=binom(a,2)+q+b,       t=ceil(q/a),
binom(k-t,2)<=2(t+1)(L-a)+t,
binom(u+1-b,2)<=2(b+1)(L-1)+b,
binom(k-b,2)<=2(b+1)((a+1)k+binom(a,2)-1)+b.
```

The full non-low factor supports already lie in the stated narrow bands, so
neither shell count loses the `delta` outliers.  The second inequality is a
new shell count at the opposite root, and the third adds the exact consecutive
visible block `K-H`; neither is a reparametrisation of FW229.  The paired
inequalities give the rational asymptotic floors `1/5,3/14,2/9`, with
unrounded constants `0.202041...,0.215390...,0.222912...`; replay:
`theory-lab/topwindow/verify_q1_two_factor_shell_allocation.py`.  The
remaining collision theorem may therefore assume two exact rooted
allocations satisfying these positive-density constraints, rather than one
undifferentiated set of holes.

FW231 adds the two root intervals before doing any further polynomial
relaxation.  For `U=K-(A union B)`, where the exact low balls have orders
`t,b`, every pair in different gate fibres of the p-r path lies in one
interval of capacity

```text
R=(L-a)+((a+1)k+binom(a,2)-1)+1.
```

Thus, unless `delta>=ceil(k/2)`, one off-spine fibre contains all but
`rho=O(1)` of at least `k-t-b` crown vertices.  The exact uniform remainder
caps are `15,21,29` after core orders `60,94,126`, and the gate-root depths
inside that component still occupy only a width-`L-a` interval.  Replay:
`theory-lab/topwindow/verify_q1_biroot_crown_compression.py`.  The next
structural target is now precise: use the global diameter endpoints and the
one-boundary giant crown component to prove thinness/collision, or show that
its low trunk yields a strictly smaller contextual state.

FW232 now uses the actual tree inside that one gate fibre.  If `s_c` selected
crown vertices have gate-depth width `W=L-a`, then every fixed LCA supports at
most `P=2W+1` pairs of those vertices.  Following the child with the most
marks gives a unique heavy child while `m^2>4P`; a loss `e` against retained
order `L_m` obeys `eL_m<=P`.  With
`H=floor(sqrt(4P))`, there are at least

```text
J=ceil((s_c^2-H^2)/(3P-1))
```

positive-loss vertices on one path.  A nonbranch positive-loss vertex must
itself be a shell mark, and shell marks on one path form a Golomb ruler in a
width-`W` interval.  Thus at most
`floor((1+sqrt(1+8W))/2)` steps are nonbranch.  In the FW231 low-defect branch
this proves the **OBSERVED** all-order floors
`B_spine>=k/48,k/72,k/96-O(sqrt(k))` for `a=1,2,3`; replay:
`theory-lab/topwindow/verify_q1_crown_heavy_spine.py`.  The remaining
**UNVERIFIED** step is now cross-level: combine the many ordered branch LCAs,
their two endpoint translates and their thin side hairs to force a repeated
distance or a strictly smaller contextual state.  The high-defect
`delta>=ceil(k/2)` branch also remains open; G18 is not inferred.

FW233 attacks the spectral side of both branches.  The `delta` K-outliers all
lie in `[C+1,C+L]`.  Relative to `diam(K)` they are `(D_K-C-1)`-far with
`D_K-C-1<=L-1`; four-point crowding therefore covers their graph by at most
`2 floor(sqrt(2L-1))` poles.  One pole has at least the corresponding
`ceil(delta/cover)` outlier neighbours, and their paths share a common segment
of length at least `(C-2L+3)/2`.  Since the neighbours lie beyond it, the
segment contains an edge of weight at least
`ceil((C-2L+3)/(2(k-d_out)))`.  Combining this with the FW230 linear defect
proves an **OBSERVED** `Omega(sqrt(k))`-neighbour pole, a
`k^2/4-O(k)` common cone and a located `k/4-O(sqrt(k))` edge in every return;
replay: `theory-lab/topwindow/verify_q1_outlier_pole_cone.py`.  The next
**UNVERIFIED** bridge is no longer a generic energy bound: prove that this
outlier cone meets the FW232 crown spine in a nested direction, or charge
their separation to disjoint distance windows strongly enough to collide.

FW234 makes that crown spine genuinely quadratic in weighted length.  If
`e_i` marks are shed and `m_(i+1)` retained at its successive LCAs, the
cross-level pair families are disjoint and have exact total

```text
sum_i e_i m_(i+1)=(s_c^2-m_f^2-sum_i e_i^2)/2.
```

The FW232 loss-product bound gives `m_f=O(sqrt(k))` and
`sum e_i^2=O(k^(3/2))`.  All these pair distances fit in an interval of
capacity only `2(L-a)+2Gamma+1`, where `Gamma` is the weighted LCA-spine
span.  Hence the **OBSERVED** all-order bound
`Gamma>=s_c^2/4-O(k^(3/2))`, uniformly at least
`k^2/16-O(k^(3/2))`; replay:
`theory-lab/topwindow/verify_q1_crown_spine_quadratic_span.py`.  At the
minimum-defect `k=100000` rows the exact coefficients are already
`0.15784,0.18159,0.19524`.  Thus the active bridge now compares two located
quadratic paths, not a linear-hop path with an unlocated moment.  Their
nesting/separation collision remains **UNVERIFIED**.

FW235 now closes the genuinely separated part of that orientation problem.
Apply FW232 first at the crown gate, and let `h_c` be the marked order of its
unique heavy-child side.  Against `d_out` pole neighbours of rooted-depth
width `q_K<=L-1`, disjoint one-boundary sides would give `h_c d_out`
distinct fixed-bridge sums in only `W+L` integer slots.  Thus
`h_c d_out<=W+L` is necessary.  The same calculation at a heavy split says
that a wholly transverse pole side can occur only after the retained marked
order falls to `floor((W+L)/d_out)`.  With the conservative FW229/FW231
floors, exact bridging and all-order tails exclude disjoint sides from
`k=147464,279948,524298` in the three rows; replay:
`theory-lab/topwindow/verify_q1_crown_pole_alignment.py`.  This is an
**OBSERVED alignment theorem**, not a collision or descent.  Containment,
opposing overlap, the high-defect branch and G18 remain **UNVERIFIED**.  The
next scalable step must use the shared corridor in those two surviving
orientations; repeating another unlocated capacity count would lose the new
information.

FW236 quantifies what the surviving nesting/opposing overlap must carry.  In
the nested cases the containing proper half-tree contains every selected
crown mark and pole neighbour.  In opposing overlap, let `x,y` be the crown
and pole vertices outside the other side.  The two boundary roots give the
exact fixed-bridge identity, hence `xy<=C_*:=W+L`.  The balanced split
`X=floor(sqrt(C_*h/d))`, `Y=floor(C_*/(X+1))` forces either a pole-side
carrier with all `d` neighbours and `h-X` crown marks, or a crown-side
carrier with all `h` marks and `d-Y` neighbours.  The respective losses are
`O(k^(3/4))` and `O(k^(1/4))`.  This **OBSERVED proper-carrier theorem** is
replayed by `theory-lab/topwindow/verify_q1_aligned_carrier_absorption.py`.
It is not yet the required contextual descent: the proper side has global
distance uniqueness and both rigid populations, but no inherited consecutive
internal spectrum.  That inheritance/iteration step and G18 remain
**UNVERIFIED**.

FW237 replaces the arbitrary outlier pole by a fixed diameter endpoint of
`K`.  If the `delta`-edge outlier graph has `s` active vertices, then
`binom(s,2)>=delta`; fixed-diameter domination forces one endpoint degree at
least `ceil(s/2)=Omega(sqrt(k))`.  Its common cone is a prefix of that fixed
diameter and has length at least `(C-2L+3)/2`.  Since the endpoint is a leaf,
deleting it gives the exact order-`k-1` carrier, retaining all selected far
neighbours and all but one crown mark.  With this stronger anchored degree,
every common-cone prefix side must meet the first heavy crown side from
`k=1448,2496,3978` in the three low-defect rows, rather than FW235's much
larger conservative thresholds.  This is an **OBSERVED strict-size anchored
carrier theorem**; replay:
`theory-lab/topwindow/verify_q1_anchored_outlier_diameter_cone.py`.  The leaf
deletion still lacks a consecutive-spectrum transfer, so iteration and G18
remain **UNVERIFIED**.

FW238 iterates the anchored leaf while keeping the old threshold
`C=binom(k,2)`.  If `theta` old-`C` outliers remain in the current connected
induced tree, a diameter leaf meets at least
`ceil(min{s:binom(s,2)>=theta}/2)>sqrt(theta/2)` of them.  Hence
`ceil(2 sqrt(2 theta))` is a decreasing integer potential.  In at most
`ceil(2 sqrt(2 delta))=O(sqrt(k))` peels all old outliers disappear, leaving
a connected order-`k-O(sqrt(k))` core.  After `t` actual deletions it has
exactly `t k-binom(t+1,2)` holes in `[1,C]`, and the deleted endpoint rooted
factors telescope coefficientwise with its internal polynomial to `F_K`.
This **OBSERVED near-full endpoint-peeling theorem** is replayed by
`theory-lab/topwindow/verify_q1_outlier_endpoint_peeling.py`.  It preserves
the missing coefficient provenance but leaves a subquadratic, rather than
linear or bounded, hole set.  Rescaling that state into a repeatable return
or colliding its nested endpoint factors is the next **UNVERIFIED** step.

FW239 renormalises after only the first anchored leaf.  At
`C'=binom(k-1,2)` the new defect is exactly the sum of the old holes below
`C'` and the deleted endpoint distances below `C'`.  Therefore it is either
at least `ceil(k/2)`, or at least `floor(k/2)` endpoint depths occupy an
`O(k)` top shell.  The shell-heavy path cannot leave the intact pole child
until only `O(sqrt(k))` marks remain; if the pole branches first, its
quadratic common cone has already been traversed.  The low-new-defect branch
therefore has a shared pole--shell path of length
`k^2/16-O(k^(3/2))`.  This **OBSERVED one-step normalised dichotomy** is
replayed by
`theory-lab/topwindow/verify_q1_one_leaf_normalized_shell.py` and applies
without assuming the old low-defect crown.  The remaining **UNVERIFIED**
problem is now explicit: exclude/absorb the linear new defect, or collide
the two rooted populations along their shared quadratic path.

FW240 freezes the exact inherited interface on the linear side.  Restricting
the FW224 tiling after the leaf decomposition gives a complete prefix at
`C'=binom(k-1,2)` with one fixed interval and exactly three named rooted
suppliers.  Therefore a new defect at least `ceil(k/2)` forces one supplier
to contribute a linear number of holes, supported on a connected
ancestor-closed ball in the new core of order at least `k/(6a)-O(1)` (at
least `k/18-O(1)` uniformly).  This **OBSERVED normalised four-factor
inheritance theorem** is replayed by
`theory-lab/topwindow/verify_q1_normalized_four_factor.py`.  The next lemma
must use the supplier translate against internal distances or the common
FW239 path; merely counting the carrier again would discard the inherited
factor.

FW241 observes that the endpoint factor already has an unconditional
half/half split.  At least half of its vertices form either the low
ancestor ball, whose rooted radius is at least `k^2/16-O(k)`, or the high
FW239 shell, whose heavy path shares `k^2/16-O(k^(3/2))` with the outlier
pole.  This **OBSERVED endpoint half-ball/half-shell normal form** is
replayed by `theory-lab/topwindow/verify_q1_endpoint_half_ball_shell.py`.
Thus every first peel now exposes a located quadratic object without a
new-defect hypothesis.  The active task is value-structured collision or
factor absorption, not another span lower bound.

FW242 supplies the exact contextual object needed to avoid an invalid
recursive shortcut.  In the original FW219 coordinates, delete the visible
vertices `v_0,...,v_(Q-1)` in that order while retaining the opposite
diameter endpoint.  Each `v_j` is then a leaf with unique stage diameter
`N-j`; after its top pair is removed, the remaining rooted factor lies in
`1,...,N-Q`.  These factors and the final tree on `H_Q union {x}` partition
that whole prefix coefficientwise:

```text
I_(N-Q)=F_(H_Q)+X^g R_p(H_Q)+sum_j L_j.
```

This **OBSERVED nested endpoint-prefix ledger theorem** is replayed by
`theory-lab/topwindow/verify_q1_threshold_endpoint_ledger.py`.  It proves
complete external provenance for the connected core, but deliberately does
not call the intermediate trees Leech: the first deletion removes the
unique internal owner of `N-Q`.  The active target is now to compress the
ordered translated factors (at least one core-rooted boundary factor per
visible component) into a bounded-defect catalogue or a strictly smaller
contextual state.  Simply re-running FW209 after each deletion is invalid.

FW243 gives a complementary one-endpoint near-Leech state.  The order-`n-1`
tree `T-x` has ambient maximum
`binom(n-1,2)+|H_Q|`.  Its low holes at its own perfect threshold are exactly
the `x`-distances to the ancestor-closed ball
`{v in H_Q:y(v)>=n-1}`, and their number `delta` equals the number of high
outliers.  Taylor parity (**LITERATURE**) forces `delta` to be at least
`floor((sqrt(n)-1)/2)` or `floor(sqrt(n-2)/2)` in the two admissible order
families.  This **OBSERVED one-endpoint defect-ball theorem** is replayed by
`theory-lab/topwindow/verify_q1_one_endpoint_defect_ball.py`.  It rules out
zero defect and names the entire low-hole carrier; the next step is to align
or collide that rooted ball with the paired outlier diameter cone.

FW244 performs that first alignment and removes the sublinear regime.  The
`m-delta` vertices outside the defect ball have transformed rooted depths
equal to `1,...,m` with exactly the `delta` outlier offsets removed.  Splitting
their pairs by LCA gives the exact capacity inequality

```text
binom(m-delta,2)<=2m-2+delta(2m-1),
```

so `delta/m>=3-2sqrt(2)-o(1)`.  Retaining the actual LCA shifts forces a
quadratic span inside the ball whenever `delta<=m/2`; all top-outlier LCAs
also lie in this same ball.  This **OBSERVED shell/LCA linear-defect
compression theorem** is replayed by
`theory-lab/topwindow/verify_q1_one_endpoint_shell_lca.py`.  The remaining
structural split is now precise: collide the aligned quadratic shell/ball
geometry, or exclude the more-than-half-defect branch.

FW245 resolves the location of that high-defect branch symmetrically.  The
two diameter-endpoint defect counts satisfy
`delta_x+delta_z=m-1+c_0`, where `c_0` counts top pairs avoiding both
endpoints, so one endpoint ball always contains at least half the remaining
order.  Their radii overlap on the middle diameter path by exactly
`binom(m,2)-m`.  If no path vertex lies in both balls, strict edge-cut
rigidity shows that the overlap is spanned by an edge cutting off precisely
an endpoint and its neighbour.  This **OBSERVED two-endpoint ownership and
overlap theorem** is replayed by
`theory-lab/topwindow/verify_q1_two_endpoint_defect_overlap.py`.  The next
task is no longer a generic high-defect estimate: it is the shared-ball
coefficient collision versus a two-vertex-wrapper classification.

FW246 closes the wrapper side for all relevant orders.  Such a wrapper would
make one endpoint ball a singleton and hence have defect one, whereas FW244
forces defect at least two from order 12.  The two balls therefore share a
diameter-path vertex whose eccentricity is at most `binom(n-1,2)`.  This
vertex is isolated in the graph of the `n-1` larger distances.  Since that
graph has `n` vertices and `n-1` edges, it must contain a cycle.  This
**OBSERVED shared-ball/top-cycle reduction** is replayed by
`theory-lab/topwindow/verify_q1_shared_ball_top_cycle.py`.  The active target
is now to classify the tree-metric top cycle into a tripod/opposing-cut
normal form and collide it with the central low-hole carrier.

FW247 completes that tree-metric classification.  The forced top cycle
contains the diameter and reduces to either a top triangle or an induced top
rectangle.  The rectangle deficits obey the exact additive law `c=a+b`; the
triangle is a single tripod whose three arms are all quadratic.  This
**OBSERVED top-cycle normal form** is replayed by
`theory-lab/topwindow/verify_q1_top_cycle_normal_form.py`.  The active target
is now narrower: locate the globally unique owners of the positive deficits
`a,b` (and `a+b` in the rectangle), then use their paths to force a collision
or a strictly smaller contextual carrier at the one or two quadratic gates.

FW248 upgrades the induced-rectangle branch to an exact all-top-band object.
Unless a vertex is top-adjacent to both endpoints (the triangle branch), the
two endpoint-neighbour deficit sets form a unique truncated direct sum of
`0,...,m-1`; their Ferrers sum graph is the only nontrivial top component.
The q=1 visible interval makes `Q` the first positive digit of the opposite
factor, so the branch enters the existing all-order mixed-radix coefficient
recursion.  This **OBSERVED triangle-or-Ferrers-factor theorem** is replayed
by `theory-lab/topwindow/verify_q1_top_ferrers_factor.py`.  The next task is
to retain rooted parent/LCA geometry while scanning those digits; abstract
mixed-radix factors alone are not an exclusion.

FW249 separately sharpens each endpoint carrier.  Popular raw sums in the
almost-complete FW244 shell cannot all be assigned to the bounded set of ball
LCAs: the exact layer count forces
`delta>=m/4-sqrt(m)/2+O(1)`.  This **OBSERVED quarter-defect theorem** is
replayed by `theory-lab/topwindow/verify_q1_shell_popular_sums.py`.  It should
now be retained when analysing the rooted mixed-radix digits or the quadratic
triangle gate; reverting to the older `3-2sqrt(2)` density loses information.

FW250 supplies the missing first rooted realisation on the Ferrers side.  Put
`s=min(Q,m-Q)`.  The vertices of deficits `0,...,s-1` all project to one gate
on the path to the first opposite-digit vertex, and their gate depths are the
consecutive quadratic interval `Z,Z-1,...,Z-s+1`.  Their paths always have
an explicit common trunk of length at least `m/4+O(1)`.  This **OBSERVED common-gate
crown theorem** is replayed by
`theory-lab/topwindow/verify_q1_ferrers_common_gate.py`.  The next target is
now a rooted crown branching theorem: use distance uniqueness and the many
visible components to force a single deeper carrier, a collision, or a
strictly smaller digit state.

FW251 transfers the quarter-defect floor to the whole threshold core, giving
`Q<=3m/4+O(sqrt(m))` and `s>=min(Q,delta_min(m))`.  In the Ferrers branch the
correct prefix length makes the linear common trunk unconditional.  This
**OBSERVED quarter-core/uniform-trunk theorem** is replayed by
`theory-lab/topwindow/verify_q1_core_density_trunk_window.py`.  The no-trunk
alternative is removed; the active target is a first-branch cross-Sidon
compression along the located trunk.

FW252 performs that first compression.  At the common crown LCA, cross-Sidon
injectivity forces one child to retain at least `s-2` of the `s` consecutive
marks for `s>=7`; a two-mark loss can only remove the two endpoint radii.
The corresponding crown cross distances form a linear interval with at most
one hole.  This **OBSERVED first-split giant-carrier theorem** is replayed by
`theory-lab/topwindow/verify_q1_ferrers_first_split.py`.  The precise missing
bridge is now the owner of that one hole in the presence of unmarked vertices:
internal ownership gives a strict handoff, while cross ownership must be
absorbed into the same rooted factor without reopening a large side.

FW253 locates the triangle alternative as a shared-ball pole fibre: its
median gate lies in both endpoint defect balls, all three arms are quadratic,
and a fixed gate supports distinct radii in only a linear-width interval.
It also routes every Ferrers case from `n=38` onward to `Q<=6` or the FW252
giant carrier.  This **OBSERVED triangle-gate/large-Ferrers theorem** is
replayed by
`theory-lab/topwindow/verify_q1_triangle_gate_and_large_ferrers.py`.  The
large-order global remainder is now three named objects: a constant-first-hole
giant core, an at-most-one-hole crown carrier, or shared-ball quadratic pole
fibres.

The finite scope is narrower than that large-order sentence: four Ferrers
rows remain outside it, namely `(Q,s,h)=(18,6,6),(19,5,5)` at `n=25` and
`(20,6,6),(21,5,5)` at `n=27`.  The analogous order-18 exceptions are
already excluded, there is no order-36 exception, and the routing is complete
from `n=38`.  These four rows remain a finite exceptional queue.

FW254 makes the constant-first-hole queue finite at its crown interface:
there are exactly 27 first-LCA rows over `Q=2,...,6`.  Behind each is a
connected core of order `m-Q`, linear excess at most `7m-27`, and a common
trunk of length at least `m-7`.  This **OBSERVED small-Q 27-row theorem** is
replayed by `theory-lab/topwindow/verify_q1_small_q_catalogue.py`.  A useful
next finite symbolic task is now well-scoped: classify how unmarked core
branches can attach to those 27 trunk/partition rows without duplicating the
fixed crown cross window.

FW255 removes wholly new near-crown branches from the FW252 interface.  The
crown itself uniquely owns `s` consecutive h-radii, while a crown-free child
must jump through an additional gap between `s` and `2s-2`, depending on the
one-hole row.  This **OBSERVED crown-shell attachment-gap theorem** is
replayed by `theory-lab/topwindow/verify_q1_crown_shell_attachment_gap.py`.
The only unmarked vertices still capable of affecting the missing
coefficient near the crown are therefore inside the two already marked
sides; this is the next two-factor absorption problem.

FW256 includes the parent side and turns every crown-free incident direction
into one of two separated shift tails.  If such vertices own the FW252 hole,
their shifts satisfy one exact opposing-tail sum.  This **OBSERVED
opposing-tail location theorem** is replayed by
`theory-lab/topwindow/verify_q1_crown_opposing_tails.py`.  The active Ferrers
problem is now to collide or absorb this balanced negative/positive pair and
the residual unmarked vertices inside the two marked directions.

FW257 converts that exact balance into geometry.  The two owners must have
opposite shift signs; the negative owner is in the unique parent direction,
while the positive owner may be in any descendant direction, including a
marked one.  The reflected shift of the diameter endpoint `x` is negative,
so the fixed diameter segment `x--h` must cross the forbidden shift window
in one edge.  This gives the **OBSERVED opposing-owner fixed-diameter
heavy-gateway theorem**: the located edge has weight at least `2s-1`, or
`3s-3` in the endpoint-pair row, and its cut separates `x` from the whole
crown.  Replay is
`theory-lab/topwindow/verify_q1_crown_opposing_gateway.py`.  A collision or
strict contextual handoff across that gateway remains **UNVERIFIED**.

FW258 makes the owner list exhaustive.  It proves `H>=s`, classifies every
h-cross, mixed, internal, rooted and outside-mark owner, and writes every
opposing unmarked owner with one slack `k>=0`.  The positive descendant shift
is its global FW219 coordinate, so `t_+(k)!=Q`; this removes the `a=s-1`
mixed row when `Q=2s-2` and at most one slack value in every opposing row.
The three named families tile a complete consecutive coefficient block when
`k=0` is admissible; for admissible `k>0` they leave exactly two symmetric
k-gaps.  This **OBSERVED complete first-crown
hole-owner interface theorem** is replayed by
`theory-lab/topwindow/verify_q1_crown_hole_owner_interface.py`.  The gaps are
local raw-coefficient gaps, not a proper core's spectral holes.

FW259 consumes the first layer of that slack.  At the first LCA inside the
giant marked child, a coordinate-admissible placement in a gap requires
`k>=s-2`, or `s-3` in the endpoint row; an admissible equality fills the gap
and forces a singleton-versus-rest split.  Otherwise the first LCA has an
explicit linear depth floor.  The `t_+!=Q` restriction only narrows the
premise and leaves these bounds unchanged.  This
**OBSERVED gap-budget/long-trunk fork** is replayed by
`theory-lab/topwindow/verify_q1_crown_gap_budget_trunk.py`.  Since the
long-trunk alternative does not inherit the two-gap state, this reaches the
predeclared stop-loss rather than a closed recursion.

The `Q=2` fallback first gives an exact local picture.  FW260 classifies its
visible forest as a rooted `L2` twig or two singleton components and gives
the exact two/three-root polynomial tilings on the connected threshold core.
At `X=-1` they reproduce Taylor's square-order condition and no stronger
exclusion.  This **OBSERVED exact Q=2 core-tiling theorem** is replayed by
`theory-lab/topwindow/verify_q1_q2_core_tiling.py`.

There is a more useful universal bridge.  In the FW218--FW219 orientation,
use the original coordinate-zero endpoint singleton directly and delete it
together with the opposite endpoint.  FW261 gives, for every `Q>=2`,

```text
I_(N-Q)=F_K+X^gR_p(K)+X^hR_r(H_Q),
|K|=n-2,
L=(N-Q)-binom(n-2,2)=2n-3-Q<=2n-5.
```

The low-hole/high-outlier counts of `K` are equal, `n-2<=2delta+g`, and a
visible endpoint neighbour forces `delta>=ceil((u+1)/2)`.  This
**OBSERVED universal direct endpoint-singleton double-peel theorem** is
replayed by
`theory-lab/topwindow/verify_q1_endpoint_singleton_double_peel.py`.  It
directly covers the original `Q=2,3` states without claiming FW220--FW223
return provenance.

FW262 applies the two rooted LCA-shell counts to this direct state.  If `q`
and `b` are the two low suppliers, then `delta=q+b`; the exact three shell
inequalities have no asymptotic solution with
`delta/(n-2)<10-4sqrt(6)=0.202041...`.  This
**OBSERVED universal direct two-root shell theorem** is replayed by
`theory-lab/topwindow/verify_q1_endpoint_singleton_two_root_shell.py`, with
an exact-real UNSAT certificate.  Thus small `Q` is now in a linear-defect
state rather than a separate algebraic terminal.  What is still
**UNVERIFIED** is precisely the topology-independent location of those
linear low-hole owners, a second peel preserving the same state, any new
order exclusion, and G18.

FW263 rules out the simplest proposed second peel.  If one or two non-root
vertices are removed from the FW261 core while the complement remains
connected, the deleted polynomial has at most `2n-3` coefficients and
contains the edge weight of a true leaf of `T`.  The latter is at most
`N-ceil(binomial(n-1,2)/2)`, whereas any terminal interval of that size ending
at `M=N-Q` begins at least at `N-3n+6`.  These ranges are disjoint for every
`n>=14`.  The resulting **OBSERVED one/two-leaf terminal-annulus
obstruction** is replayed by
`theory-lab/topwindow/verify_q1_two_leaf_terminal_annulus_obstruction.py`.
It says the incident rooted factor must be retained or rerooted; it does not
exclude an order.  The remaining legitimate route is therefore a bounded-
context owner transfer, such as a proper trunk cut whose cross-product
translates collide or compress to at most two boundary factors.

FW264 treats a fixed core `K'=K-{alpha}` and a singleton-boundary ledger whose
blocks are labelled by original actual pairs.  Put `C=binomial(n-2,2)`.  For
`n>=10`, the two old endpoint edges and the peeled true-leaf edge all lie
strictly below `C`, while the stipulated next prefix reaches at least `C`.
The three labels `zp,xr,alpha-a` must therefore remain active; actual-pair
rerooting cannot relabel the low `h,w` coefficients.  They may be order-one
ghosts, so this does not force three full algebraic rooted factors.  The
**OBSERVED one-leaf three-owner retention obstruction** is replayed by
`theory-lab/topwindow/verify_q1_one_leaf_three_owner_retention.py`.  It is a
route obstruction.  Multi-vertex/fragmented cap bundling, arbitrary nonactual
translates and a core exchange placing `x` or `alpha` into the new internal
core are outside its scope; it is not an order exclusion.

FW265 makes the remaining trunk-cut issue exact.  For any edge `e=ab` with
components `A ni a`, `B ni b`,

```text
F_K=F_A+F_B+X^wR_a(A)R_b(B)
   =F_A+F_B+sum_(u in A)X^(w+d(a,u))R_b(B).
```

Thus the formal cross product is an owner-expanded ledger of exactly `|A|`
named `B`-rooted shifts.  Global distance uniqueness makes the refined family
`{F_A,F_B} union {S_u:u in A}` pairwise support-disjoint; it does not force a
collision.  This **OBSERVED universal trunk-cut owner ledger** is replayed by
`theory-lab/topwindow/verify_q1_trunk_cut_ledger.py`.  It does not prove that
the FW259 cut has large `|A|`, or that the retained prefix meets many shifts.
The missing **UNVERIFIED** theorem is prefix locality/absorption, or a bounded
cap catalogue which genuinely controls owner-expanded context.

A controlled Max sprint tested both remaining exits.  On Route A, if
`c_u(L)` counts the coefficients of one named shift below a receiving endpoint
and `supp(F_B) subset I_L`, disjointness gives

```text
sum_u c_u(L)<=L-binomial(b,2),
|{u:c_u(L)>=r}|<=floor((L-binomial(b,2))/r).
```

At an FW261-type endpoint this is at best
`floor((2b-1)/r)`: at most one whole shift, while this bound alone does not
exclude linearly many one-coefficient grazers.  This **OBSERVED conditional
occupancy bound** does not give the missing constant cap, and FW259 does not
yet inherit the required endpoint.

Route B gives the independently audited **OBSERVED FW266 core-exchange
top-band obstruction**.  If a new core `C` contains `x`, its complete
positive internal term lies below `M'`, and `E=T-C` contains `z` with
`e=|E|<Q`, then

```text
M'>=N-e,  N-M'<=e.
```

Thus `M'<=M=N-Q` forces `e>=Q`.  Raising the endpoint to `N-e` is possible,
but its canonical equality state is exactly the old FW242 stage `T_e`, whose
named external ledger grows with `e`.  Replay:
`theory-lab/topwindow/verify_q1_core_exchange_top_band.py`.

The independently replayed **OBSERVED FW267 near-full-prefix external-owner
conservation theorem** makes the growth exact.  For `n>=5` every edge obeys
`w<=N-a(n-a)<=N-(n-1)`.  Hence for any external set of order
`1<=e<=n-2`, every external vertex participates in a unique actual-pair owner
strictly below `N-e`.  A provenance-preserving ledger for `I_(N-e)` cannot
forget those `e` vertex labels merely by repackaging factors.  This is not a
lower bound of `e` algebraic factors and does not rule out rolling exchange,
an owner-preserving merger/absorption with an explicit strictly decreasing
fully charged potential, or a dual-band recurrence.  Replay:
`theory-lab/topwindow/verify_q1_near_full_external_owner_conservation.py`.

The authorised directed-hole follow-up also reached its stop rule.  FW268
first distinguishes an entry leaf of `T-z` from a true rolling leaf of `T`.
For every entry coordinate `b` it freezes the exact actual-pair ledger

```text
I_(N-1)=F_(T-{z,v_b})+L_0+X^(N-b)+L_b,
```

whose high band has the single named hole `N-b`.  The ambient deletion
deficits are nevertheless rigid: zero away from the diameter endpoints, one
at `z`, and `Q>=2` at `x`.  Thus ambient FW218 normalization cannot reset the
hole.  The exchange core is not a smaller Leech tree for any `n>=7`, so it
cannot be normalized by reusing FW218 either.  The exact `L6` control has two
rolling coordinates whose fixed-ambient ledger choices form an involution
with holes `N-1,N-3`; this is not a certified contextual transition.  The
tested coordinate, diameter and numeric opposite-deficit ranks
can reverse, stay flat or increase.  Replay:
`theory-lab/topwindow/verify_q1_directed_hole_interface.py`.

Accordingly the q=1 bounded-cap/core-exchange/directed-hole route is stopped
at FW268.  Reopen it only after an FW259-specific rooted-ball/no-grazing
theorem with an inherited receiving prefix, or a total owner-equivariant
contextual normalizer with an explicit strictly decreasing fully charged
potential and certified empty-owner terminal.  More compatible span, density,
moment or heavy-edge bounds are not a substitute for closure.  This is a
research-direction decision, not an order exclusion; G18 remains
**UNVERIFIED**.  Detailed acceptance criteria and pressure controls are in
`docs/q1-new-mechanism-sprint.md` and `docs/q1-directed-hole-sprint.md`.

### Low-owner successor audit (FW269)

The first authorised successor has now reached its own controlled stop.  The
**OBSERVED** positive part is an exact four-cone theorem for every owner
`1<=d<Q`.  Core--core and same-visible-component owners lie in weighted
`d`-balls below a movable LCA; visible--core owners meet only the last `d-1`
visible coordinates; and owners crossing two visible components satisfy

```text
d=4+(Q-1-i)+(Q-1-j)+2(y(LCA)-Q-1).
```

Because `i!=j`, the last case has `d>=5`.  The unit edge has a second exact
constraint: the rooted-depth sets on its cut sides are cross-Sidon and contain
no consecutive depths.  Consequently the visible indices below it form an
independent set of the `Q`-vertex path and have order at most `ceil(Q/2)`.
This excludes a unit edge from any trunk carrying consecutive visible marks,
but says nothing when its descendant side is a pure-`H` tail.

That escape survives a sharp **OBSERVED negative metric pressure test**.  For
every fixed `kappa` and `Q>=kappa+1`, FW269c constructs globally
distance-distinct integer-weighted trees with the exact q=1 endpoint deficits
and reflected top pattern and with

```text
Spec(T) intersect [1,kappa]=[1,kappa],
```

while the `kappa` unique edge owners slide to separated `Theta(n)`-deep
pure-`H` anchors.  The construction is deliberately not Leech: its diameter
is much larger than `binom(n,2)`, and it fails the exact FW219c/FW261
tight-spectrum tilings.  It therefore does not refute owner localisation for
Leech trees.  It proves only that top geometry, distance uniqueness and any
fixed low interval cannot supply that localisation without additional input;
full spectrum is a load-bearing missing hypothesis in this pressure model,
not asserted to be the only logically possible missing condition.

The **OBSERVED exact** local catalogue through `I_6` has fifteen signatures
but no bounded attachment consequence.  An independently audited **OBSERVED
external/non-replayed engine diagnostic** also misses the predeclared gate:
imposing the stronger permanent-true-leaf
condition on the weight-1 edge visits 1,351 constructed candidates through
insertion depth six, exceeding the 100-fold order-11 threshold 1,233.  The
count is not part of the frozen FW269 arithmetic replay, and no new engine,
order-16 run or order-25 run follows from it.

Reopen this route only after one of the following **UNVERIFIED** bridges is
proved:

1. pure-core-tail elimination, forcing the unit edge or enough low owners to
   meet visible descendants; or
2. a full tight-spectrum owner-provenance theorem converting FW219c/FW261
   coefficient coverage into cut-side rooted-depth incidence.

Assuming that a deep unit edge already has two consecutive visible descendants
would be circular.  G18 is unchanged.  Full proof and scope:
`docs/q1-low-owner-localization.md`; frozen deterministic replay:
`theory-lab/topwindow/verify_q1_low_owner_localization.py`, with certificate
`theory-lab/topwindow/results/q1_low_owner_localization_certificate.json`.

### Pure-tail exactness stop (FW270)

The two FW269 successor proposals have now been audited and this route is
stopped.  The **OBSERVED** exact-spectrum boundary is that FW219c, after the
proved q=1 top-owner class is restored, is coefficientwise equivalent to
`F_T=I_N`; FW261a--b is only a finer owner partition of the same statement.
It is therefore not an intermediate descent condition.

The **OBSERVED** unit-edge deletion identity partitions all pairs incident
with the two endpoints into 2-separated dominos.  In a pure-`H` descendant
cut `A`, with root-side endpoint `b`, it sharpens to

```text
d(x,b)>=2Q+1,
2|A|-1<=M-1-d(x,b)<=M-2Q-2.
```

These inequalities remain feasible.  FW270c supplies an **OBSERVED negative
metric pressure family** realizing formal diameter-`D` owner suppliers that
match the `I_P`-projections of FW219c/FW261 for every `P>=Q>=2`,
with a nonpendant pure-`H` unit edge and first missing coefficient `P+1`.  It
is not an FW219c/FW261 state; its diameter is far larger than the pair count,
so it is not Leech and does not address a quadratically near-complete
spectrum.

The proposed bound

```text
diam(S)>=binom(|S|,2)+|S|-4
```

for a globally distance-distinct integer tree with a nonpendant unit edge is
still **UNVERIFIED**.  The check through order 12 is only **OBSERVED
external/non-replayed finite evidence**; the order-13 attempts were
`UNKNOWN`.  If proved for `S=T-x`, it yields only `Q<=4`, and it does not
cover a singleton unit tail.  Reopening therefore requires a rooted
near-perfect realization theorem plus a separate singleton-tail theorem.
No further finite-prefix algebra or exact-spectrum restatement counts as a
bridge.  G18 remains **UNVERIFIED**.  Full proof, construction and trust
boundary: `docs/q1-pure-tail-stop.md`.

### Full-spectrum mechanism audit (FW271)

The FW270 stop has one exact local strengthening.  Let `ba` be the weight-one
edge with pure-`H` descendant side `A`, put `s=|A|`, `q_b=d(x,b)`, and let
`rho` be the maximum `a`-rooted depth in `A`.  The **OBSERVED** actual-pair
product of the `Q` visible roots with `{b} union A` lies in the single window
`[M+1-q_b,M]`.  It cannot fill that window: its second factor contains
`0,1` but not `2`, so exact interval factorisation would make every visible
start have one parity, whereas the q=1 starts alternate.  Therefore

```text
q_b>=Q(s+1)+1,
q_b>=2Q+rho+1,             q_b<=M-rho-2,
4s<=N-3Q+1,                s(Q+2)<=N-2Q-1.          (FW271a)
```

The high branch `2q_b>=M+1` additionally gives

```text
q_b>=(Q+1)(s+1)+1,         s(Q+3)<=N-2Q-2,
```

and the low branch `2q_b<=M` gives, from one shortened joint window rather
than a duplicate visible rectangle,

```text
(2Q+1)(s+1)<=M,            s(2Q+1)<=N-3Q-1.
```

An **OBSERVED exact** inclusion--exclusion formula also counts the two
actual-pair rectangles when `r` visible vertices lie on the descendant side.
It does not force `r=0` or `Q`, and the FW270c non-Leech pressure family
satisfies every pure-tail inequality with large slack.  Since a Leech tree
has only one unit edge, there is no additive multi-tail closure.

For a pendant unit edge `a--1--b`, FW271b gives the **OBSERVED exact**
self-complement and parity partitions

```text
I_N=F_(T-a) dot-union X R_b(T-a),
Spec(T-a)=I_N minus (1+{d(b,v):v!=a}),
eo=ceil(N/2).
```

Separating even and odd coefficients produces a complete transformed
`e x o` actual-pair cross rectangle with the `a`-row distinguished.  In the
q=1 coordinates, the pendant edge is either one consecutive visible pair or
one consecutive pure-core pair.  This is a real reduction but not a smaller
Leech state.  The parity-halved graph is a forest exactly when the quotient
by even-weight components has maximum degree at most two; even then its
components need not be Leech.  Calhoun--Polhill's perfect-distance labellings
of `t K_(1,3)` for every `t` are a **LITERATURE** control against a
componentwise recursion.

The same audit gives **OBSERVED negative mechanism verdicts** for joint
two-root/no-grazing, all-digit Ferrers propagation, canonical
triangle/triple-boundary deletion, the covariance kernel, signed derivatives,
positive-`q` Hosoya inequalities, finite group characters, and Ma--Yi
path-block packing.  Each stops at a named lack of actual-owner localisation,
full lower-spectrum absorption, or a same-type strictly decreasing charged
state.  Proposed distance-matrix and parity-cross-rectangle consequences
beyond the exact identities remain **UNVERIFIED successor work under
review**.  FW271 has no verifier or certificate and proves no order
exclusion; G18 remains **UNVERIFIED**.  Full theorem and trust boundary:
`docs/q1-full-spectrum-mechanism-audit.md`.

### Pendant-unit mixed-LCA obstruction (FW272)

FW272 resolves one sharply delimited successor question from FW271.  Root a
pendant unit edge `a--1--b` at `b`, let `E,O` be the even/odd root-distance
classes, and put

```text
R={d(b,u)/2:u in E},
S={(d(b,v)-1)/2:v in O},
L_(u,v)=d(b,LCA_b(u,v)).
```

The odd actual owners give the exact transformed cross rectangle

```text
A_(u,v)=(d(u,v)+1)/2
       =1+R_u+S_v-L_(u,v),
{A_(u,v):u in E,v in O}=I_(|E||O|).               (FW272a)
```

If `L` vanished identically, this would be the interval direct sum

```text
R dot+ S=[0,|E||O|-1].                             (FW272b)
```

The **OBSERVED all-order** interval-block lemma now shows `|E|<=3`.  If the
least positive member of `R` exceeded one, a root distance and a pendant-row
distance would coincide.  Otherwise let `[0,k-1]` be the maximal initial
block of `R`.  A block of length at least four contains the root depths
`2,4,6` and collides.  For `k=2` or `3`, any later member `P` forces `P` to
be a multiple of `k`, forces the preceding multiples into `S`, and forces
`[P,P+k-1]` into `R`; the resulting depth-`2P` LCA alternatives all collide.
Thus `R` has no later member and has order at most three.

Taylor's parity sizes are **LITERATURE** input with their proof re-derived in
the project ledger.  Both parity classes have order at least four in every
Leech candidate of order at least eleven.  Consequently every such
pendant-unit candidate, in particular either parity orientation at order
eighteen, has a positive mixed-LCA entry.  The conclusion is independent of
q=1 and therefore covers both the visible and pure-core pendant locations.
The `L6` witness is the asymmetric boundary control: rooted at the nonleaf endpoint
of its unit edge it has

```text
R={0,1},             S={0,2,4,6},             L identically zero.
```

FW272 does not force the unit edge to be pendant and does not convert a
positive laminar LCA block into a repeated distance or an inherited smaller
state.  That closure remains **UNVERIFIED**.  FW272 creates no verifier or
certificate, proves no order exclusion, and leaves G18 **UNVERIFIED**.  Full
proof and trust boundary: `docs/q1-pendant-mixed-lca.md`.

### First positive mixed-LCA edge and terminal completion (FW273)

Continue in the pendant-unit setting and write

```text
z_(u,v)=(d(u,v)-1)/2=R_u+S_v-L_(u,v),
tau=min{z_(u,v):L_(u,v)>0}.
```

The full Leech distinct-distance hypothesis, not merely the odd rectangle,
is part of the theorem.  The **OBSERVED exact** raw convolution satisfies

```text
#{(u,v):R_u+S_v=m}=1       (0<=m<tau),
#{(u,v):R_u+S_v=tau}=0.                         (FW273a)
```

Let `[0,k-1]` be the initial block of the root-even factor `R`.  The actual
depth-`2,4,6` collisions give `k<=3`.  If a later digit `P<tau` exists, the
prefix first forces every multiple of `k` below `P` into `S`, then forces
`P=0 mod k`; the equality `P+k=tau` directly hits the raw hole, while
`P+k<tau` forces the next `R` block and the FW272 collisions.  This proves
the asymmetric **OBSERVED all-order** bounds

```text
tau<=3|O|+2,
w=2tau+1<=6|O|+5.                                (FW273b)
```

The first positive owner is exactly one odd edge not incident with the root,
and every lighter odd edge is root-incident.  At order eighteen, `|O|=7` or
`11`, so `w<=47` or `71`.

There is also an **OBSERVED exact completion lemma**.  For same-parity
`u,u'`, with `c=LCA(u,u')` and `h=rho(c)`,

```text
max_(v in opposite parity) min{L_(u,v),L_(u',v)}=h
iff T_c contains an opposite-parity vertex.       (FW273c)
```

Thus the cross matrix determines every non-monochromatic same-parity LCA.
At a deepest mixed `c`, its relative coordinate sets satisfy an actual
direct block `A dot+ B`; the only undetermined owners are internal pairs of
the maximal pure child subtrees.  Those internal edges are all even and can
be halved, but one child of order `s-2` leaves
`binom(s-2,2)=Theta(s^2)` free owners.  The child is a smaller
globally-distance-distinct tree with a punctured spectrum, not a smaller
Leech/q=1 state.

For q=1 at order eighteen the visible `x` row occupies both parity-sheet
suffixes at half-indices at least 70 and parity capacity gives `Q<=14`.
The first positive coordinate is at most 35, but locating the deepest mixed
terminal on that top owner hull remains **UNVERIFIED**.  A temporary n=11
CP-SAT necessary relaxation returned INFEASIBLE in both parity orientations;
this is only **OBSERVED external/non-replayed diagnostic** evidence, with no
frozen model proof or certificate, and supplies no order exclusion.

FW273 therefore stops the proposed positive-block collision/bounded-state
descent at the pure-child completion term.  It has no verifier or certificate,
does not address a nonpendant unit edge, excludes no order, and leaves G18
**UNVERIFIED**.  Full proof and trust boundary:
`docs/q1-first-positive-lca.md`.

### Absolute first odd-edge bound (FW274)

FW274 retains the pendant hypothesis and the exact first-hole identity from
FW273, but replaces its size-dependent estimate by the **OBSERVED all-order**
absolute bounds

```text
tau<=10,
w=2tau+1<=21.                                      (FW274a)
```

The new input is prefix exhaust.  If `1 notin R`, the forced odd depths
give `binom(tau,2)<=2tau-2`, hence `tau<=4`.  Otherwise the maximal initial
`R` block has radix two or three.  Let `Q_0` be its next coordinate, with
`Q_0=+infinity` if none exists.  The coefficient-one prefix determines all
root coordinates below `min(Q_0,tau)`.  Exhaustive ancestor placements of
the forced depth lattices give

```text
k=3,Q_0>=tau: tau<=9,        k=2,Q_0>=tau: tau<=10,
k=3,Q_0<tau:  tau<=10,       k=2,Q_0<tau:  tau<=9.
```

At the sole apparent `tau=11` boundary, `k=3,Q_0=9`, coefficient `c_10=1`
forces exactly one of `R_10,S_10`.  The `S_10` choice supplies a raw owner
of the hole at eleven, while `R_10` repeats the distance twenty between the
forced root-separated odd vertices at coordinates three and six.

FW272 supplies a positive mixed LCA in every pendant-unit candidate of order
at least eleven, so (FW274a) applies in both order-eighteen orientations.
The eight-vertex pressure tree recorded in the proof has all 28 distances
distinct, exact odd transformed sheet `I_[0,11]`, and `tau=10,w=21`, but
its even half-sheet is not `I_16`; it is not a Leech tree.  Thus the constant
is sharp only for the local interface.

FW274 does not absorb the full even sheet into the deepest mixed terminal,
does not close the q=1 suffix handoff, and does not treat a nonpendant unit
edge.  Its frozen deterministic finite-kernel replay is
`theory-lab/topwindow/verify_q1_absolute_first_odd_edge.py`, with output in
`theory-lab/topwindow/results/q1_absolute_first_odd_edge_certificate.json`;
the replay supports the analytic parent-map ledger but is not a Leech search
or an independent all-order proof.  No order is excluded, and G18 remains
**UNVERIFIED**.  Full proof and trust boundary: `docs/q1-absolute-first-odd-edge.md`.

### Nonpendant-unit rooted-stability stop (FW275)

FW275 reopens only the hard `2|b` branch of the **UNVERIFIED** near-perfect
nonpendant-unit diameter conjecture.  With handle
`c--x--a--1--r--B`, `|B|=b`, its **OBSERVED exact** counterexample state is

```text
O={x} dot-union (1+Y) dot-union (x+1+Y),
D_0=binom(b,2)+3b-2,
F_B dot-union O dot-union H=I_[1,D_0],    |H|=b-3,
|I_[1,D_0]-(O union H union Y_+)|=binom(b-1,2),    (FW275a)
```

where the last set must be owned bijectively by actual nonroot pairs of the
rooted tree `(B,r)`.  For every `b>=5`, the **OBSERVED analytic** formal depths
`Y={0,4} union {8+5i:0<=i<=b-3}` at `x=2` satisfy every first-pivot, spacing and
`2p`-chain condition; their second pivot is impossible because its required
distance is `5` or `21`, both wrapper-owned.  Thus bounded one-pivot audits
do not approach rooted realizability.

Two **OBSERVED hand-checkable actual equality controls** delimit the stronger
idea.  The `m=9,D=41` control has a virtual-row owner triangle on depths
`26,31,37`; the `m=11,D=62` control has long step-eight chains and a row that
absorbs the virtual translate for one diagonal hole.  In both cases
`D=D_0+1`.  They refute cap-blind consequences of local LCA laminarity, not
any implication that essentially uses the strict cap `D<=D_0`.

Accordingly, FW275 is an **OBSERVED STOP** only for the cap-blind
first-pivot / `2p`-boundary / single-virtual-row mechanism, not a disproof of
the near-perfect conjecture.  Reopening requires either an **UNVERIFIED**
strict-cap global potential retaining every owner pair and LCA gate, robust
to cycles and row mergers, or an exact terminal-suffix theorem that peels a nonempty set
`W` together with all incident distances and exactly `|W|` holes.  The
order-at-most-twelve checks remain only **OBSERVED external/non-replayed
finite diagnostic evidence**; there is no new verifier, SAT witness or
exclusion, and G18 remains **UNVERIFIED**.  Full
state and trust boundary: `docs/nonpendant-unit-rooted-stability-stop.md`.

### First-positive edge cut and exact stop (FW276)

FW276 cuts the pendant FW274 state at its first positive edge
`f=pc`, `w=2tau+1<=21`.  Four rooted local-parity factors give **OBSERVED
exact**, coefficientwise partitions of both complete parity sheets.  They
show that the root side owns every odd transformed index below `tau`, while
the two internal sides own every even half-index through `tau+1`.

Immediately before Find-Next inserts `f`, the light-edge component containing
`c` has only even edges.  Halving makes it a distinct-distance weighted tree
of order at most `tau+1<=11`.  This is not a bound on the full descendant
side: later heavy attachments remain free.  The light forest has at most
`2tau` edges, and its root component owns all `tau` low odd values.  Thus at
`tau=10`, order eighteen has `|A|>=7,|B|<=11`; nevertheless the formal local
split `(2,5;6,5)` matches Taylor's `7|11` classes and passes all cut capacity
inequalities.

In q=1 coordinates, visible vertices lying consecutively across `f` would
give a reflected rooted interval, but their location and consecutiveness are
**UNVERIFIED**; a pure-core `H--H` cut may see none, and no relation `w>=Q`
is known.  The reopening gate is an
owner-labelled no-grazing/absorption theorem at the named cut.  FW276 has no
verifier, certificate, computation or order exclusion, and G18 remains
**UNVERIFIED**.  Full proof: `docs/q1-first-positive-edge-cut.md`.

### Light-quotient leaf cap and visible-row area bound (FW277)

FW277 contracts every edge lighter than `w` and chooses a full-quotient leaf
bag on the descendant side of `f`.  The total excess of all nonroot light
bags is **OBSERVED** at most `tau-1` for `tau>=2`; at `tau=1` the only
nontrivial nonroot light bag is the edge of weight two.  The selected bag is
therefore a true pendant even cap of order at most ten and diameter at most
108.  Its actual-owner cut is

```text
I_N=F_C+F_R+X^eR_t(C)R_r(R),
```

and the translated rows from `t,r,b,a` forbid the six cap-depth differences
`1,e,H,H+1,H+e,H+e+1`.  Descendant branching either supplies such a cap
outside the q=1 endpoint or leaves a heavy-edge corridor ending in the
endpoint bag.

The q=1 suffix now propagates quantitatively.  An endpoint cap produces
disjoint translates of the complete visible block.  If `x` is outside a cap
with no visible vertex, its entire visible-by-cap rectangle lies in one named
window and gives the **OBSERVED** area inequality

```text
2e+rho+sQ+(s-1)(Q mod 2)<=N-Q-1.                  (FW277a)
```

For G18 this makes an empty-visible singleton satisfy
`e<=76-Q`.  Saturation would make `C/2` a Leech tree and is in
fact possible only at `tau=1,s=2`.  The strict remaining stop is the
singleton cut `I_N=F_R+X^eR_r(R)`, whose unbounded rooted row is neither a
terminal interval nor a proper same-type state.  FW277 has no verifier,
computation or order exclusion; G18 remains **UNVERIFIED**.  Full proof:
`docs/q1-light-quotient-cap.md`.

### Unit-edge owner propagation audit (FW278)

FW278 cuts away the pendant unit leaf and one singleton heavy leaf.  The
common core has five named rooted supports with one same-owner overlap and at
most six distinct nonzero forbidden differences in every attachment-path
fibre, together with an **OBSERVED exact** descent criterion:
rank compression produces a Leech tree of order `n-2` on the same topology
if and only if the external-hole counting function is additive on every
core path.  The q=1 top block reaches a whole rooted row, but no theorem
routes it to one fibre or forces that additivity; the order-six nonendpoint
leaf is an actual failure control.

On the strict nonpendant `x=2` branch, actual owners of the filled virtual
row give `sum_f w_f(c_f-l_f)=2E`.  The hard cap then requires exactly `E-2`
outside holes with one explicitly prescribed sum.  This excludes the FW275
order-nine equality pattern after truncation, while `E=2,3` and signed-flow
controls prevent a sign shortcut; a general subset-sum exclusion remains
**UNVERIFIED**.  The bordered additive distance matrix is integrally
congruent to a hyperbolic plane plus the diagonal edge factors, so its Smith
form, modular ranks, determinant and inverse do not restore cross-owner
placement.  FW278 has no computation or order exclusion and leaves G18
**UNVERIFIED**.  Full audit: `docs/unit-edge-owner-propagation-audit.md`.

### Closure-architecture decision (FW279)

FW279 replaces the informal A/B/C closure hope by its exact quantified
obligations and finds the current architecture **OBSERVED not closed**.
For the canonical pendant distinguished-endpoint deletion, internal numeric
owners form a strictly decreasing directed forest.  A Leech descent of order
`n-2`, allowing arbitrary owner permutation, occurs exactly when transformed
path sums are injective and all forest sources occupy the prescribed top
band.  Conditional on injectivity, the source displacement is

```text
Delta=sum_(h in H_0)(A_h-B_h),
```

where `A_h` is within-threshold additive overflow and `B_h` is repeated
above-threshold Kruskal coalescence.  The `L6` table cancels only after
summing all thresholds.  Rank anti-coalescence and the reverse multiscale
transport inequality remain two independent **UNVERIFIED** lemmas.

For a general nonpendant `s|t` unit cut, the strict padded cap has the
**OBSERVED exact** certificate

```text
|H_out|=E-kappa,              kappa=(s-2)(t-2)+2,
```

together with a prescribed signed cut-flow sum, consecutive-run correction,
q=1 top suffix and Taylor parity.  A `4|5` actual equality tree is rejected
only after strict truncation; a non-strict `3|6` pressure and two formal
`I_36` tilings show that coefficient data stop at the all-pivot rooted
realisation problem.  Carrying that problem exactly requires the full
`Theta(m^2)` LCA-depth matrix; no decreasing rooted state or actual strict
counterexample is known.

Inside the much narrower order-eighteen pure-`H` `2|15` wrapper, exact hole
decomposition and gate packing exclude `Q=10,...,14`.  The cases
`Q=5,...,9` remain **UNVERIFIED**; a bounded Q9 SMT diagnostic ended
`UNKNOWN`/cancelled and supplied no certificate.  Reopening this route now
requires both pendant lemmas simultaneously, or a general owner-sensitive
rooted-realisation stability theorem.  FW279 proves no order exclusion and
leaves G18 and global nonexistence **UNVERIFIED**.  Full audit:
`docs/g18-closure-architecture-audit.md`.

### Pendant rank anti-coalescence stop (FW280)

FW280 attacks only the first missing pendant lemma.  Cancelling the common
segment of a first transformed collision leaves at most two edge-disjoint
arms on each side.  If

```text
def(P)=q(d(P))-sum_(f in P)q(w_f),
```

then the **OBSERVED exact** full-interval ledger is

```text
def(P)-def(P')=|D intersect (d(P),d(P')]|.
```

At every prefix step `(s,w)`, translation of `[1,w]` by `s` gives

```text
eta(s,w)=|M^+_(s,w)|-|M^-_(s,w)|,
M^+={t in D:t<=w,t+s in H},
M^-={t in H:t<=w,t+s in D}.
```

Every term keeps the actual owner on both sides.  A mismatch owner cannot
concatenate with the prefix, since that would give `t+s` the wrong
internal/external type.  The remaining LCA, gate or connector correction is
not controlled by first-collision minimality: one endpoint of every mismatch
is external, so it is not a smaller collision between two core paths.

A noncanonical orientation of the full `L6` interval has positive and
negative mismatches at complete-overlap, nested and tripod gates.  Separately,
the actual distance-distinct family

```text
a--1--b--(k+1)--c--(2k)--r--3--x,   c--k--y,
```

has an exact `Q=3` endpoint suffix and a transformed collision for every
`k>=4`; even `k` passes Taylor parity, but the family is non-Leech because
its low spectrum has holes.  A temporary order-six one-gap Z3 audit returned
`UNSAT` on 464 rows, but no script, proof log or independent replay was
retained, so it is only **OBSERVED finite, external/non-replayed**.

No canonical full-state counterexample or anti-coalescence proof was found.
The next **UNVERIFIED** bridge must couple canonical top ownership with full
low coverage in one mismatch-gate transport theorem; exact bookkeeping falls
back to `Theta(m^2)` owner/LCA data.  FW280 excludes no order and leaves G18
**UNVERIFIED**.  Full ledger and trust boundary:
`docs/pendant-rank-anti-coalescence-stop.md`.

### Canonical mismatch-gate transport stop (FW281)

FW281 adds the exact threshold identities

```text
F(P)=sum_(d in D) kappa_d(P),
d(P)-F(P)=sum_(h in H_0) kappa_h(P),
```

and the transformed Kruskal bound `K(j)>=j`.  The complete missing datum is
the rooted merge convolution: anti-coalescence holds exactly when every one
of its coefficients is at most one.  Scalar merge products do not imply this;
a noncanonical full `L6` orientation passes its whole `K` schedule and still
collides.

Canonical full-spectrum `L6` does not collide, but its smallest unit/top
shadows lift through two different gates, and its complete AC-2 table contains
both connector and overlap corrections.  This exactly rejects least-`t`,
same-root, uniform-sign and strict local-lift proofs, without rejecting a
global first-collision theorem.  An infinite non-Leech `Q=4` family collides
and passes Taylor parity for odd parameters.  A temporary 232-row `I_4`
diagnostic returned `UNSAT`, but is external/non-replayed and not proof input.

The 60k checkpoint triggers **STOP**.  Reopening requires a global separation
theorem coupling rooted merge convolution coefficients to AC-1; explicitly
retaining all coefficients is the `Theta(m^2)` fallback.  FW281 excludes no
order and leaves G18 **UNVERIFIED**.  Full ledger:
`docs/canonical-mismatch-gate-transport-stop.md`.

### Full-window quotient arborescence and leaf-port tiling (FW282)

FW282 advances the separate edgewise full-window route without reopening
FW281.  For `n>=5`, the strict edge bound makes every edge fully supported on
at least one side.  After contracting full-bidirectional edges, two outgoing
boundaries at one quotient component would force each boundary weight to be
strictly smaller than the other.  Thus every quotient node has outdegree at
most one, the sink is unique, boundary weights strictly increase toward it,
and each away component is a strict thin cap.

Deleting the first-level sink boundaries gives an exact multi-port
actual-owner polynomial partition and a linear weighted skeleton preserving
all full-support tests.  A nontrivial branched sink has at least three ports.
At any core leaf edge of weight `p`, one side is a bouquet of actual thin caps
and the complete suffix has the exact two-colored form

```text
[0,N-p]=(U direct-sum V) dotunion H_S dotunion H_R.
```

Both colors are nonempty.  For `n>=18`, the bounded-handoff theorem makes the
first colored hole at most ten.  This is an **OBSERVED all-order exact
reduction**, not an exclusion.  The remaining **UNVERIFIED LPCT** theorem is
that this leaf-port colored tiling cannot have complete Leech coefficient
coverage.  An actual order-six pressure tree has a two-vertex branched sink,
thin singleton ports and spectrum `[1,15]-{9}+{21}`; it shows that the missing
full coefficient, not support geometry or a finite prefix, is load-bearing.
FW282 also absorbs every nonpendant unit edge into the unique-sink route, but
does not solve the pendant FW281 coefficient-separation problem.  It excludes
no order and does not prove global nonexistence.  Proof, replay and trust
boundary: `docs/full-window-quotient-arborescence.md` and
`theory-lab/topwindow/verify_full_window_quotient_arborescence.py`.

### Bounded leaf-port prefix strict stop (FW283)

FW283 independently rebuilds the rooted-parent recursion underlying LPCT's
first colored hole.  Up to swapping rooted factors, every `eta<=10` has one
necessary prefix row except `eta=7`, which is impossible.  The extremal
`eta=10` state is the strict-thin bouquet `{0,2,8}` against the rooted tree
`{0,1,4,5}`.  The first colored owner path is either the single next edge
`p+eta`, or every proper subpath is below `p` and its endpoint edges are at
least `eta+1`.

These positive facts do not localize the owner.  An affine order-11 family
for every integer `t>=70` realizes the exact extremal prefix with a next-edge
owner `p+10` behind a gate of depth `2t-18`.  All pair distances are distinct,
the full-window sink is the three-vertex core path, the selected leaf side is
a strict singleton bouquet, and both cut sides support.  The family is not
Leech: it has gaps and outliers.  It is therefore a countermodel only to the
proposed inference from bounded single-port data to a bounded owner gate.

This gives a **STRICT STOP** for extending one leaf-port prefix one owner at a
time; it does not refute LPCT.  Continuing that mechanism would recreate an
unbounded owner/LCA ledger.  The next live obligation is a simultaneous
two-port capped owner-return invariant using no-outlier coverage, actual pair
owners, their projections/LCA positions and a common connector inside the
unique sink core.  FW283 excludes no order and leaves LPCT, G18 and global
nonexistence **UNVERIFIED**.  Proof and replay:
`docs/leaf-port-colored-tiling-stop.md` and
`theory-lab/topwindow/verify_leaf_port_colored_tiling_stop.py`.

### Skeleton first-owner cycle reduction (FW284)

FW284 proves the two-port successor required by FW283.  The uniformly
guaranteed configuration is one core-leaf cut plus a first-level cap boundary;
two core leaves share the same cut when the sink core has order two.  The two
cuts give an exact three-block actual-owner identity with vertexwise matched
root depths on their common connector.

For every edge in the linear full-window skeleton, complete Leech coverage
supplies a compensated first cross hole `eta<=10`, `eta!=7`.  If its owner
lies in one first-level cap, thinness strictly lifts to that cap's heavier
boundary.  Otherwise its path crosses a named skeleton edge, where the same
actual pair becomes cross-owned.  Choosing the maximum-weight crossed edge
gives a fixed-point-free total transition map with exactly three arc types:
cap lift, single-edge lift and multi-edge path drop.  Every orbit enters a
cycle, and each cycle obeys the actual-owner balance

```text
sum_path-drops rho = sum_cycle eta + sum_cap-lifts sigma.
```

This compresses unnamed remote gates to `O(n)` named skeleton records.  It
does not bound their metric positions or exclude cycles.  The known L6 Leech
tree has the exact singleton-sink cycle `5->8->5`, proving that the scalar
balance and local prefix factors are insufficient.  The remaining
**UNVERIFIED NSSC** theorem must use nontrivial core endpoint monodromy: compose
the returned pair endpoints and their actual projections around the complete
cycle and force a collision.  NSSC is state-smaller than LPCT, but after
FW284 it is logically equivalent to excluding the nontrivial-sink branch.
FW284 excludes no order and leaves G18 and global nonexistence **UNVERIFIED**.
Proof and replay: `docs/skeleton-first-owner-cycle.md` and
`theory-lab/topwindow/verify_skeleton_first_owner_cycle.py`.

### Compressed endpoint-monodromy stop (FW285)

FW285 audits the proposed NSSC continuation.  The FW284 map has edge
composition, but its records do not define owner composition: at a target
cut the incoming cross owner and the target's next first same-side owner
belong to unrelated coefficients.  Cap lift is even weaker because the
incoming owner lies strictly below the target boundary ledger.

An actual order-five distance-injective path has a nontrivial two-vertex sink
and a total `8->9->8` cycle whose consecutive first-owner pairs are
vertex-disjoint.  An order-eight distance-injective path has a three-vertex
sink, all three FW284 arc types, and a cap lift whose incoming and target
first owners are vertex-disjoint.  The controls are not Leech and lie below
order eighteen.  They therefore do not refute NSSC; they prove a **STRICT
STOP** only for deriving endpoint transport from the compressed local record,
even after retaining side-specific first owners.

The new **UNVERIFIED CCOO** obligation must reuse complete-spectrum
coefficients discarded by FW284.  At every path drop it must force an
immediate edge return, an actual shared endpoint, or overlapping projections
on one named core connector with a composable order rule.  A translated
window without shared endpoint/projection information is insufficient.  CCOO,
NSSC, the nontrivial-sink exclusion, G18 and global nonexistence all remain
**UNVERIFIED**.  Proof and replay:
`docs/skeleton-endpoint-monodromy-stop.md` and
`theory-lab/topwindow/verify_skeleton_endpoint_monodromy_stop.py`.

### Two-cut terminal owner-switch reduction (FW286)

FW286 reopens only the full-spectrum path-drop ledger and proves a smaller
exact reduction.  In `A--q--B--r--C`, both endpoint edges of the returned
owner path have weight at least `eta_q+1`; an endpoint inside a strict
first-level cap promotes to its heavier skeleton boundary.  Since `r` is the
maximum skeleton edge crossed by the path, `w_r>=eta_q+1`.  Every `AC` pair
then has `q`-offset at least `ell+w_r>=eta_q+1`.

Consequently complete coverage forces the translated band to be exactly
`AB` at offsets `0,...,eta_q-1` and `BC` at offset `eta_q`.  The proposed
interior `AB -> AC` switch is impossible.  The remaining path-drop target is
the **UNVERIFIED Terminal AB-to-BC Connector** theorem for those two adjacent
owners.  Cap-to-boundary owner transport and cycle-composition compatibility
remain separate unverified layers, so FW286 proves neither NSSC nor an order
exclusion.  Proof and replay: `docs/two-cut-terminal-owner-switch.md` and
`theory-lab/topwindow/verify_two_cut_terminal_owner_switch.py`.

### Terminal four-cone reduction (FW287)

FW287 writes the two crossed terminal pairs as

```text
X'=X+x+y,        Y'=Y+x-y,
```

where `x` is the change in connector projection and `y` the change in
off-connector height.  Injectivity confines every disjoint terminal state to
four integer cones.  The FW283 endpoint-edge lower bound and
`lambda_b<=eta_q-1` exclude the entire left-projection cone: an off-connector
endpoint makes `lambda_(b')` too large, while an on-connector endpoint puts
the same heavy first edge in the short path to the projection of `b`.

The remaining `R,D,U` modes respectively have both swaps rise, connector
height drop, or connector height rise.  All three occur in actual non-Leech
distance-injective trees with nontrivial sinks.  The next path-drop theorem
must therefore use complete coverage to eliminate them or define a monotone
transport that composes around the FW284 cycle.  Cap transport and cycle
compatibility remain independently unverified.  Proof and replay:
`docs/terminal-four-cone-reduction.md` and
`theory-lab/topwindow/verify_terminal_four_cone_reduction.py`.

### Terminal local transport theorem (FW288)

FW288 proves an exhaustive local record for one path drop.  The direct state
shares the `B` endpoint.  In `D`, the crossed pair `(a,b')` is the unique
earlier `AB` owner at an offset `0<=j<=eta_q-2`.  In `U`, the other crossed
pair `(b,c)` must have distance below the source weight and gives a named
two-hop endpoint bridge.  In `R`, the projections of `b,b'` bound an actual
oriented connector interval of length at least two.

Thus the single-path-drop TABC obligation is proved locally.  The next
**UNVERIFIED PRCC** theorem must show how an `S/D/R/U` record is consumed by
the next FW284 arc without losing its endpoint or interval orientation.
Cap-to-boundary owner transport remains independent, and both are required
before NSSC.  Proof and replay: `docs/terminal-local-transport.md` and
`theory-lab/topwindow/verify_terminal_local_transport.py`.

### Cap endpoint-depth stop (FW289)

FW289 proves the exact cap-lift endpoint dichotomy.  An incoming cap endpoint
of depth below the target first offset `theta` has a canonical shared cross
owner in the target prefix; depth exactly `theta` collides; otherwise both
incoming endpoints have depth at least `theta+1`.  The remote cap pair and
target inward owner yield an equal-sum four-cross-pair rectangle and the
conditional Leech bound

```text
3g+p+eta+theta+2(s_C+s_B)<=2N.
```

An order-nine distance-injective non-Leech control realizes the remote state
at `theta=2` with all four cross distances at most `N` and rectangle sum at
most `2N`.  This strictly stops full cap transport from the target first
prefix and local rooted data alone.  The new **UNVERIFIED RCRT** obligation
must reuse complete coefficients beyond `theta` to connect the incoming cap
pair, target inward owner and a named rectangle cross owner.  PRCC remains
separate.  Proof and replay: `docs/cap-endpoint-depth-stop.md` and
`theory-lab/topwindow/verify_cap_endpoint_depth_stop.py`.

### Path-drop target first-owner fork (FW290)

FW290 proves that if `q -> r` is a path drop and
`delta=w_q-w_r`, then the target first offset satisfies
`eta_r<=delta`.  Equality forces `P_r=q` and the exact edge lift `r -> q`,
so the two arcs form a directed two-cycle.  Strict inequality gives
`d(P_r)<=w_q-1`.

The strict owner decrease is not a skeleton-weight potential: an actual
distance-injective control has `22 -> 16`, target owner distance `17`, then a
cap lift `16 -> 39`.  The next cycle obligations are therefore
**UNVERIFIED ERTC** for exact-return two-cycles and **UNVERIFIED SBCC** joining
strict path-drop output to FW289 cap rectangles.  Proof and replay:
`docs/pathdrop-target-owner-fork.md` and
`theory-lab/topwindow/verify_pathdrop_target_owner_fork.py`.

### Exact-return switchback stop (FW291)

FW291 writes every FW290 equality branch as the exact target-cut owner strip

```text
BC^delta  AB^eta  BC.
```

The corresponding rooted convolutions `U*Lambda` and `Rho*W` have a
complementary prefix, length-`eta` gap and cross return, with `Lambda/Rho`
matched vertexwise along the nontrivial connector.  Known `L6` realizes the
full Leech spectrum with a singleton sink.  Non-Leech controls realize
nontrivial sinks, `eta=1,2`, nonzero connectors and the complete local strip.
Thus neither load-bearing ingredient separately excludes the two-cycle.

ERTC remains **UNVERIFIED** and must use complete coefficients outside the
switchback strip together with nontrivial connector geometry.  Extending only
the bounded rooted prefixes is a **STRICT STOP**.  Proof and replay:
`docs/exact-return-switchback-stop.md` and
`theory-lab/topwindow/verify_exact_return_switchback_stop.py`.

The reversal is now **OBSERVED absorbed** rather than left as a second
terminal (FW212).  Reorienting at its smaller first hole cuts either the old
FW76 cap or the endpoint singleton inside its direct leaf edge.  Repeating
once if necessary reaches a genuine nonreversal pair; if both inner caps are
singletons, the two-cut count forces the smaller hole to be one.  Hence every
FW210 reversal enters one of the same eleven rows after at most two inner
endpoint cuts.  The outer wrapper may remain contextual, so this is not yet
a proper-core induction.  Replay:
`theory-lab/topwindow/verify_terminal_cap_reversal_absorption.py`.

The first extremal mixed-radix branch is now also **OBSERVED closed**. For any
edge `e` of weight `w` and component orders `a,b`, equality in
`w<=N+1-ab` makes the two complete rooted distance sets factor the entire
interval `0,...,ab-1`. Every such factorization has an alternating
mixed-radix normal form. A terminating exact rooted-parent classification
shows that equality occurs only in the known orders `2,3,4`; hence every
hypothetical Leech tree of order at least five has `w<=N-ab`. Proof and audit:
`docs/heaviest-edge-rigidity.md` and
`theory-lab/topwindow/verify_heaviest_edge_rigidity.py`. This eliminates zero
excess, but the required stability statement making the positive excess grow
with `a,b` remains **UNVERIFIED**.

The same finite rooted-prefix recursion gives a stronger local transition at
**every** edge: if `ab>=11`, some value in `w+1,...,w+10` is realised wholly
inside one proper component. The theorem can be applied afresh to another edge
without asking the receiving component to inherit a Leech interval. The
remaining problem is directional: prove that successive handoffs can be
oriented into nested proper sides, or that repeated reverse handoffs force a
thick branch profile. The extremal
delay to 10 is rigid: it forces, up to swapping, rooted depth sets
`{0,1,4,5}` and `{0,2,8}` with the unique jointly compatible shallow core.

Allowing finitely many holes yields an **OBSERVED** quantitative ladder. The
exact death indices for hole budgets `0,...,8` are
`10,19,22,31,34,37,40,48,51`. Consequently the heaviest-edge excess is at
least 3 at orders 25/27, at least 7 at 36/38, and at least 9 at 49/51. Proof
and audit: `docs/heaviest-edge-rigidity.md` and
`theory-lab/topwindow/verify_heaviest_excess_ladder.py`. These within-side
handoffs occur by offsets 22, 40 and 51 and strengthen the final merge-waste
term by at least 24, 69 and 164 at the three target pairs. Turning this finite
ladder into a uniform linear-in-order bound remains **UNVERIFIED**.

Because the result is edgewise, its slacks also satisfy the exact global
budget `sum_e E_e=(n-1)(N+1)-W_hop(T)-sum_e w_e`. Combining the cut-product
ladder with `sum_e w_e>=N` yields a topology-dependent necessary inequality;
it is recorded in `docs/heaviest-edge-rigidity.md`. It is not yet strong enough
alone to exclude every topology, but it supplies the arithmetic side of the
directional/thick-branch dichotomy.

The distance first moment sharpens this to the exact **OBSERVED** identity
`sum_e (a_e b_e)E_e=(N+1)W_hop-sum_e(a_e b_e)^2-N(N+1)/2`. The independent
audit checks all five known witnesses with both checkers and all 2,105,739
edge rows in the frozen order-18 topology archive. Coupled only with the
present finite ladder it excludes 0/123,867 topologies (minimum margin 27,523),
so this is an honest negative diagnostic as well as the intended interface to
a future thick-centre estimate.

There is also an all-order **OBSERVED** rooted-span input. If an edge has side
orders `a,b`, the globally disjoint internal distance sets force the sum of the
two root radii to be at least
`ceil((C(a,2)+C(b,2))/2)+min(ceil(C(a,2)/2),ceil(C(b,2)/2))`. Hence `E_e` is at
least this quantity plus `1-ab`. This grows quadratically on sufficiently
unbalanced cuts. Combined with the finite ladder it lowers the smallest
order-18 weighted-moment margin to 12,784, but still excludes no topology.

The edgewise theorem now has a global **OBSERVED** orientation form. Orient
each edge toward a component containing its bounded handoff. Every leaf points
inward, and an oriented finite tree has a nonleaf sink. At that sink, the
complement of every incident branch contains bounded near-edge-weight pairs;
the finite ladder guarantees multiplicities 2, 4 and 5 at the first three
Taylor target pairs. Thus the remaining terminal geometry is either a genuine
degree-at-least-three thick centre or a degree-two bidirectional corridor.
Proof: `docs/edge-handoff-orientation.md`. Excluding both cases is
**UNVERIFIED**, but the former interval-inheritance problem is no longer needed
for this edgewise route.

The terminal is now canonical. Contract every edge that has a bounded handoff
on both sides and take a sink in the resulting one-way quotient. The sink
component either contains a genuine branch vertex or is a bidirectional path.
Every internal corridor edge has two distinct holes by offset 10. If the path
is a single degree-two vertex with incident weights `p<q=w_j`, elementary
handoff routing plus the component-concentration covering bound forces
`q-p<=10` or `q<=binom(j-1,2)+2`. Thus the remaining corridor is no longer an
unstructured reverse-handoff case; it has near-tied incident weights, a
fragmented light forest, or a genuinely bidirectional segment. Its exclusion
remains **UNVERIFIED**.

Using 20 rather than 10 as the supported-direction window sharpens the
singleton case further. If the fragmented-light-forest bound fails, both
opposite handoffs must contain the sink vertex; otherwise one of the two
central edges is 20-bidirectional. Writing `q=p+r`, their residual rooted
depths are `h-r<=9` and `r+k<=20`. Global distance uniqueness leaves exactly
485 affine parameter rows. This is an **OBSERVED finite normal form**, not yet
an exclusion. In fact all 485 rows have an explicit distance-injective local
realisation at `p=21`, so local rooted-parent filtering alone provably removes
none; the next step must use exact global early-forest coverage or the weighted
excess identity.

The first global intersection is now **OBSERVED analytically**. If the two
singleton-terminal weights have ranks `p=w_i<q=w_j` and the fragmented bound
fails, the covering ceilings and `q-p<=10` give
`binom(j-1,2)-binom(i,2)<=8`. Hence either `p<=29,q<=39`, or `j=i+1` and the
two central edges are consecutive in the complete weight order. In the latter
case the single `p`-edge insertion must cover the whole bounded interval up to
`q-1`, providing the exact forcing constraint needed for the next catalogue.

That catalogue is now **OBSERVED exact as a prefix relaxation**. Enumerating
all 4,537,700 forced forests through rank 10 with the universal distance cap
390 reduces the 485 rows to 9 rows, 14 matches and 7 forests. Every survivor
has zero right residual and is obtained by extending one of the known `L3`,
two `L4`, or `L6` light cores; all four cores pass both checkers. The remaining
all-order task is no longer an arbitrary small-rank corridor: it is to prove
that none of these known-core two-edge tails can preserve the canonical
one-way condition under a full extension. The exact prefix reduction itself
does not prove that future exclusion and remains **UNVERIFIED** at completion
level.

The complementary large-rank branch has now collapsed **OBSERVED
analytically**. Put `C=binom(i,2)` and `delta=C+1-p`. Strict failure of the
fragmented bound makes the `i` light edges one connected component and forces
`delta<=r-2`, where `r=q-p`. The far endpoint of `q` is light-isolated, so the
positive affine residual vanishes. The one-way 20-window condition then makes
the `i`-vertex light core contain `{1,...,C-delta}` and place all `delta`
remaining distances above `p+20`. Coverage of `p+1,...,p+r-1` supplies rooted
depths `1,...,r-1`; the depth-1/depth-2 pair collides when `r>=4`. Hence only

```text
(r,delta)=(2,0),(3,0),(3,1)
```

remain. In a smallest counterexample the zero-defect rows are proper smaller
Leech trees and disappear. The unique new target is a rooted core of order
`i>=11` with

```text
dist(K)={1,...,C-1,D}, D>=C+21,
```

whose weight-1 and weight-2 edges meet at the root. Odd-distance counting adds
a square sieve (`i` or `i-4` when `C` is even; `i+2` or `i-2` when `C` is odd).
Exact forced-prefix runs at core orders 11--14 inspect 3,690,761,100 terminal
states and 162,845 connected cores and find zero prefix-defect-one cores. This
is a rigorous finite base.  A selective 512-shard order-16 diagnostic adds
39,381,216,516 reported nodes and finds zero connected or target cores; its
raw transcript and a local cross-compiler reproduction are **OBSERVED** via
`theory-lab/topwindow/verify_prefix_defect_gap.py`.  Neither finite result is
the missing all-order induction.  Proof and trust boundary:
`docs/edge-handoff-orientation.md`.

The complementary endpoint-strip theorem is now **OBSERVED analytically**.
For a defect core with exceptional diameter `D=C+g`, both diameter pendant
weights are at least `g+1`.  Removing the two endpoints preserves the entire
prefix `1,...,g` and the rooted weight-1/weight-2 fork, while the inner-pair
distances and the two translated rooted-distance sets give an exact disjoint
tiling of `1,...,C-1`.  This supplies a concrete two-leaf descent interface,
but no strictly decreasing defect parameter has yet been proved.  Proof:
`docs/prefix-defect-endpoint-strip.md`.

There is also a stronger **OBSERVED full-window canonical reduction**.  If a
side supports an edge whenever it contains any internal distance larger than
the edge weight, the offset-10 theorem still guarantees a direction on every
edge.  At a singleton degree-two sink `p<q`, both outer component diameters
are below their incident weights and `q` is globally heaviest.  A singleton
outer side would force the other side to be a proper smaller Leech tree;
hence a putative survivor has two nontrivial components before `q`.  The
unique cross-sum tiling below `p` then forces `p<=n-2`,
`binom(a,2)<=n-3` and `binom(b,2)<=2n-7`; for `n>=18` these imply
`a<=n/3`, `b<=n/2`, contradicting `a+b=n-1`.  Thus **all** singleton
degree-two terminals are excluded in the smallest-counterexample argument.
At that intermediate stage the remaining degree-two task is exactly
a nontrivial full-bidirectional path.  The fixed-20 prefix-defect calculation
remains a useful independent finite diagnostic, but is no longer an all-order
bottleneck.  Proof: `docs/edge-handoff-orientation.md`.

For that path, the globally heaviest edge lies on the bare corridor.  If it
is internal, full support on both sides gives `N>=3q+2`.  Reflecting the two
rooted depth sets gives a hole-free prefix; counting the separate far endpoint
as well gives `ell*rho>=2q+2`.  The
exact excess therefore has the stronger lower bound
`N+1-floor(n^2/4)-floor((floor(n^2/4)-2)/2)`.  Since every such high internal
pair touches a corridor vertex, the corridor contains asymptotically at least
`(1-sqrt(3)/2)n`, approximately `0.134n`, vertices.  Thus a bounded internal
corridor is excluded.  In the boundary-heaviest case, if the outer component
has order `a` and diameter `lambda<q`, the reflected prefix plus endpoint gives
`a(n-a)>=q+lambda+1`, while distinct rooted depths and
`diameter<=2lambda-1` give `lambda>=r(a)`, where `r(1)=0` and
`r(a)=ceil((binom(a,2)+1)/2)` for `a>=2`.  The exact excess is consequently at
least `N+2-2a(n-a)+r(a)`, whose all-order minimum is
`(1/18+o(1))n^2`.  The same incident-pair capacity forces at least
`(1-sqrt(8/9)+o(1))n`, approximately `0.057n`, corridor vertices.  Before the
reflection-gap theorem below, both locations of the maximum therefore reduced
to a linearly long bare corridor.  A joint count is stronger: the
`binom(a,2)+binom(b,2)` mutually distinct distances in the two outer
components and the other `c` chain-edge weights all lie below the corridor
maximum.  Combining that lower bound
with the top-prefix upper bound on the maximum forces at least
`(1-1/sqrt(2)-o(1))n`, approximately `0.293n`, corridor vertices when the
maximum is internal.  In the boundary case the exact necessary inequality is
`binom(a,2)+binom(b,2)+c+r(a)+2<=a(n-a)`; optimizing it forces at least
`((5-3sqrt(2))/7-o(1))n`, approximately `0.108n`, corridor vertices.  This
sharpening is **OBSERVED**.  For an internal maximum, an exact slack identity
splits the remaining budget into outer-order imbalance, low corridor paths,
top-prefix slack and cut imbalance.  Summing all length-`k` contiguous windows
in the two sides of the corridor, and using the fact that the two outer
internal-distance sets are globally disjoint to strengthen their joint rooted
span, raises the rigorous asymptotic fraction again to `329/1000=0.329`.  In
the boundary case, deletion of the maximum leaves one corridor segment, so
there are exactly `c-k+1` length-`k` windows.  Its corresponding joint-span
count raises the rigorous asymptotic fraction from approximately `0.108` to
`29/250=0.116`.  Exact rational monotonicity and strong-concavity certificates
prove both constants.  The long-corridor exclusion is still not proved.
Arithmetic audit:
`theory-lab/topwindow/verify_full_window_corridor.py` and
`theory-lab/topwindow/verify_corridor_window_stability.py`, plus
`theory-lab/topwindow/verify_boundary_corridor_window_stability.py`.

The complementary **OBSERVED** upper bound is now also linear.  The `c+2`
cumulative chain positions form a Golomb ruler.  Applying the elementary
Erdos--Turan bounded-index-difference estimate after deleting the maximum
edge, jointly to the one or two remaining chain segments, then subtracting
the joint rooted span of the two outer components, gives
`c<=((3+sqrt(14))/10+o(1))n`, approximately `0.674n`.  Hence the outer
components together have order at least `0.326n-o(n)`; the long-corridor
branch can no longer escape by leaving only `o(n)` vertices outside the bare
path.  The outer-component distance count then forces the chain maximum to be
at least `(0.02654199146...-o(1))n^2`, so the top and bottom factorization
windows also remain quadratic.  Exact target-order bounds and arithmetic audit:
`theory-lab/topwindow/verify_corridor_golomb_upper.py`.

A finite **OBSERVED negative diagnostic** prevents weakening this last step to
top density alone.  There are two rooted seven-vertex weighted trees whose
internal distance spectra are disjoint and whose cross-depth sums are
injective, but whose reflected rooted depth sets nevertheless have 49 unique
sums and contain the entire prefix `0,...,36`.  This is not a Leech witness:
at joined order 14 the diameter equation would give joining weight
`91-36-64=-9`, and the first positive unreflected cross sum is 28.  Thus the
example does not challenge (FW10)--(FW14); it shows that a proof using only a
constant density threshold for the reflected prefix cannot work.  A valid
argument must retain the positive scale and the maximum-edge path geometry;
the surviving boundary case still retains the exact bottom holes.  Verifier and frozen data:
`theory-lab/topwindow/verify_reflected_prefix_barrier.py` and
`theory-lab/topwindow/results/reflected_prefix_barrier_certificate.json`.

The scale-sensitive conclusion is now **OBSERVED at every order**.  For an
internal corridor maximum, reflect the side with smaller eccentricity
`lambda`.  Its factor `U` is completely visible inside the unique-sum prefix
of length `lambda+q`.  Coefficient-block induction gives the exact dichotomy

```text
U=lambda-U, or U has a consecutive gap at least q+1.
```

Every root-to-farthest path uses edge weights strictly below the global
maximum `q`, so the gap alternative cannot connect the endpoints.  In the
symmetric alternative the first edge at the farthest vertex is repeated as a
root depth.  Both alternatives contradict a distinct-distance tree.  Thus the
maximum edge of every surviving bare corridor is a **boundary edge**.  The
all-order proof is in `docs/edge-handoff-orientation.md`; a direct recursion
checks 584,442 oriented prefix factors through length 128 without assuming the
normal form:
`theory-lab/topwindow/verify_internal_corridor_reflection.py`.  At that
intermediate stage the remaining degree-two problem was the boundary-heaviest near-factorisation, with the
rigorous corridor bounds `0.116n-o(n) <= c <= 0.674n+o(n)`.  Its exclusion
was still **UNVERIFIED**.  The same reflection lemma gives its exact
outer normal form.  The boundary rooted-depth set is centrally symmetric and
its farthest point is a root leaf.  An order-one outer side contradicts the
rank of the maximum edge.  An order-two side is the explicit
`lambda--q` thin cap and forces `0,...,lambda-1` into the other reflected
factor.  At every outer order at least three, the boundary root has global
degree at least three and `q>=ceil(3lambda/2)+1`.  Thus the last boundary
corridor either has that thin cap or hands directly to the thick-centre
branch.  The thin cap is now impossible at every `n>=18`.  Its opposite
boundary component creates a complete gap in the reflected factor.  Exact
alternating `lambda`-blocks force boundary edge `lambda+1` and component
diameter `lambda-1`; the first block and the internal-distance count then
force opposite order `b=2` and `lambda=2`, making the entire tree a path.
Thus every surviving terminal configuration either contains a
degree-at-least-three vertex or meets one immediately across its boundary
maximum.  The latter boundary pole is further classified all-order: its outer
order is at most four, and after the thin case is removed its rooted depth set
is exactly `{0,s,2s}` or `{0,s,G,G+s}` with `G>2s`.  Thus it is an exact
degree-three pole rather than an unbounded local bush.  Its attachment to the
inward component is now further rigidified: all nine cases in which the
opposite corridor endpoint enters the reflected prefix are spiders,
unrealizable rooted sets or direct distance collisions.  Hence a survivor has
`p+theta>=q+lambda`, a second near-maximum boundary edge, and a linearly large
opposite outer order.  The same opposite component also has
`binom(b,2)<=p-1<=q-2`; combining the two estimates gives `q<=13` for the
order-three pole and `q<=23` for the order-four pole.  The first is impossible
at `n>=18`; the second reduces to the complete order-18 forest exclusion via
Taylor.  Hence no boundary-maximum corridor survives, and a surviving
canonical sink component must itself contain a degree-at-least-three vertex.
Its thick-centre contradiction remains **UNVERIFIED**.  Audits:
`theory-lab/topwindow/verify_boundary_thin_cap.py` and
`theory-lab/topwindow/verify_boundary_pole_factor.py`,
`theory-lab/topwindow/verify_boundary_pole_handoff.py`,
`theory-lab/topwindow/verify_boundary_corridor_exclusion.py`.

The first thick-centre layer is now an **OBSERVED all-order reduction**.
If the canonical sink is one branch vertex `v`, each outer branch has diameter
below its incident weight.  Thus its largest incident weight `q` is globally
heaviest, the Leech diameter is the sum of the two largest rooted arm heights,
and

```text
q>=sum_i binom(b_i,2)+deg(v),       q>=ceil((N+4)/4).
```

Let `lambda` be the eccentricity beyond `q`, and let `mu>h` be the two
largest other arm heights.  If the `q`-arm misses the diameter or `h>=q`, then
`N>=2q+3` and the `q`-cut has at least three above-`q` internal pairs.  In the
remaining case the reflected `q`-cut factors an exact prefix with tail
`Q=q-h`: full support on the centre side gives `mu+h>q`.  The
coefficient-block dichotomy says that `q-h<lambda`
hands to a scale imbalance (and a nested edge of weight at least `q-h+1` when
the outer factor is nonsymmetric), while `Q>=lambda` makes the outer branch a
complete mixed-radix pole of order at most four.  This is the first rigorous
third-arm parameter in the thick endgame.  The pole prefix additionally gives
`lambda<=2(n-4)` and `q>=ceil((N-2n+11)/3)`, improving the order-25 lower
bound from 76 to 87.  It also forces the third arm to lie within
`4 beta(q)<=4(n-1)` of the smaller diameter arm, where
`binom(beta(q),2)<=q-2`.  Full support confines every thin singleton to
`ceil((N-lambda+3)/3)<=q<=floor((2N-2lambda-2)/3)`; for a leaf pole the
order-25 window is `101<=q<=161`.  Exact accounting below `q` also forces a
pole's third-and-lower arms to contain `(1-sqrt(2/5))n-O(1)` vertices.  Its
mass slack decomposes into three nonnegative defects, and the pole scale forces
one of them to be at least `n^2/54-O(n)`.  Thus the pole cannot hand to one
giant arm with only bounded residue: it must instead produce quadratically
many extra low cross pairs, incident-spectrum holes, or rooted-span surplus.
The pole cross count itself makes the third height `q-O(n)`.  The strict arm
inequality from (FW48) then makes its incident edge unconditionally
quadratic; the earlier internal linear-edge fallback is impossible.  A
height-layer capacity count strengthens this from one arm to a mass statement:
more than `(sqrt(17/30)-sqrt(2/5))n-O(1)>0.12031n-O(1)` third-and-lower
vertices lie behind incident edges of weight `n^2/24-O(n)`.  The same height
layer argument absorbs the thick-third interface: every singleton thick
terminal has `n/sqrt(6)-O(1)` vertices behind quadratic incident edges.
Splitting at `h=q/2` excludes the short case entirely
for `n>=48`; in the remaining finite regimes it produces a proper lower core
of order at least `3n/7-O(1)` whose entire internal spectrum lies below `q`.
The quadratic defect trichotomy then supplies either a second heavy interface
in the `mu`-arm or a vertex with `n/27-O(1)` extra low-cross neighbours.  The
incident-hole defect is now exactly localised: it counts the pairs below that
incident weight in the complementary side, and the remaining complementary
pairs are precisely its high edge excess.  In fact the `mu`-arm incident edge
is unconditionally at least `ceil((N-lambda+5)/6)=n^2/12-O(n)` and obeys
`4t>=q+4`, so every pole exposes heavy interfaces in two different non-`q`
arms.  When the extra-low-cross defect is large, there is additionally a
proper connected induced subtree of order at least
`(1-sqrt(26/27))n-O(1)` whose diameter is below `q`.
The cut at that heavy incident edge now also inherits an exact reflected
prefix of length `mu-h`.  If `t>h`, its controlled gap `t-h<=4(n-1)` either
hands to a genuinely internal edge of the `mu`-arm (up to the explicit
symmetric-factor case) or classifies that arm as another pole of order at
most four.  The `t<=h` branch remains attached to the lower-arm geometry.
The finite-hole excess ladder then routes the heavy `t` edge uniformly from
order 36 onward: either `q-t<=40`, or a pair at one of `t+1,...,t+40` lies
entirely in the proper core formed by the centre and all lower arms.  Hence
the large-order pole now terminates in a bounded two-heavy-edge cluster or
strictly hands to a linearly large lower core.
The bounded cluster also routes completely: if `h>t`, the third-height pair
itself lies in that lower core within offset 39 of `t`; if `h<t`, the exact
reflected `t`-cut sends the positive gap back inside the `mu`-arm, except for
an explicit symmetric rooted factor or a second pole of order at most four.
The symmetric case is now closed by the complete digit-block/root-leaf
classification: it too has order at most four.  Thus the remaining pole
outputs from order 36 onward are a lower-core near-`t` pair, a genuinely
internal `mu`-arm edge, or a second small rooted factor.
When the second factor is also small, top-pair capacity fixes the remaining
width: `1<=t-h<=16`, `q-h<=56`, and the `q`-cut prefix length is at most 112;
at least one top-side gap is at most 16.  The small-factor output is therefore
a finite affine rooted-state classification problem rather than an unbounded
terminal.
Exact low-spectrum counting strengthens this further: the lower core contains
at least `q-53` pairs below `q`.  Splitting them into within-arm and cross-arm
pairs forces either a complete lower arm or the centre's `q/2`-shallow
induced core to have `((9-sqrt(69))/6)n-O(1)` vertices, about `0.11556n`.
This is a mass/defect/descent
reduction, not an exclusion: inheritance of a controlled handoff or decreasing
defect budget is still missing.  A nonsymmetric inherited prefix does now
give an exact transition: its gap edge either cuts off a proper thin cap or
belongs to a nontrivial full-bidirectional edge-component contained in the
receiving arm.  In the latter case the first boundary edge toward the centre
is heavier and closes a proper thin cap, possibly the whole receiving arm.
At the opposite boundary of the same bidirectional component there is always
a strict smaller diameter cap.  Its reflected top prefix is exact again and
gives a well-founded recurrence: an order-at-most-four factor, a child cap of
strictly smaller order and boundary weight, or complementary rooted-diameter
surplus at least the boundary.  The last output contains a new near-diameter
pair of strictly smaller deficit and an off-diameter component at least as
deep as the boundary; the new pair retains one old diameter endpoint and
pivots only the other one.  Its three ray heights are exactly
`k+r,k+q',k`, with the controlled gap `q'` below the old boundary.  It is
therefore exactly the existing thin/thick endpoint interface rather than a
new terminal.  Full-support orientation makes the bidirectional component at
the pivot gate a canonical thick sink unless the `x`-ray has a boundary edge
above `2k+q'`; the latter escape forces `r>=n-1` and a diameter-edge deficit
at least `n-2`.  In the originating pole this escape is confined to the same
`mu`-arm: its two internal tips are less than `t` apart, the new offshoot has
height below `t/2`, and the opposite ray gap is at least `N-t+1`.  This closes the decreasing-measure
problem for inherited caps.  In the escape, every `mu`-arm vertex at reflected
depth below `q'` from the far endpoint lies in the strict cap, and the new tip
is the unique outside vertex at reflected depth `q'`; bounding that weighted
endpoint strip absolutely remains open.  The exact `t`-cut prefix now migrates
to the strict cap and first fails precisely at `q'`.  Before the layer `H-h`
its complement factor is only the classified order-at-most-four pole; after
that layer the lower-arm spectrum has already entered.  Equality is a direct
distance collision.  Hence the inherited-cap route now either forces
`q'<=4|C_z|` through a proper pole-factor cap or joins the lower-core route
before its first hole.
In fact the lower-arm-entry side forces `h>q/2` and returns to the
tall-third-arm heavy-edge handoff as an already identified interface, not an
exclusion.  On the pole-only side, if the strict cap
has order `c` and the pole has order `a<=4`, then
`c(c-1)<=t-4` and `q'<=ac`; hence the new endpoint window is only
square-root scale in `t`, and is at most 16 when both factors are small.  The
small-pole coefficient recursion further forces one of four explicit
mixed-radix digit strips below `q'`, with `q'` obtained by deleting the next
cap-owned digit.  The bounded independent arithmetic replay is
`theory-lab/topwindow/verify_endpoint_pole_first_hole.py`.  The cap above that
first hole is still uncontrolled.  Comparing the two diameter-arm orders
shows that this remaining deficit also satisfies
`q'<min(H,mu)-h<=a beta(q)<=4(n-1)`, so it is no longer quadratic.  The whole
receiving-arm band strictly below `gamma=min(H,mu)-h` has the same canonical digit
layers, and its internal-pair capacity sharpens this to
`gamma<=a floor((1+sqrt(8t-7))/2)`.
The band also has a linear terminal-complexity consequence.  Assign every
band vertex to a descendant rooted leaf in the same band.  All chain-pair
distances across all assignment classes are distinct values in
`{1,...,gamma-1}`; Cauchy--Schwarz then forces at least
`gamma/(2a^2+a)>=gamma/36` band leaves.  If the induced band forest has `c`
components, every within-component pair has distance at most `2gamma-2`.
A second global pair-capacity count forces
`c>=gamma/(4a^2+a)>=gamma/68`; apart from the possible component containing
the attachment root, these are proper terminal subtrees entered from below
the band.  Thus the remaining endpoint is now an **OBSERVED** all-order
branch/hair accumulation terminal with linearly many terminal-subtree
entrances.  The exact forest identity `ell-c=E` also records any branch
excess inside the band.
Each entry has a further exact split.  Its centre side contains the larger
attachment edge `t` (or the `q`-edge when the entry is `t`), so it has full
support.  The terminal component either has diameter below the entry and is
a proper thin cap, or equality is excluded by distance uniqueness and the
entry is full-support bidirectional.  Hence at least `gamma/136` disjoint
thin caps occur, or the edge-union of nontrivial full-bidirectional cores
contains at least `gamma/136` distinct entry edges.  This is an **OBSERVED**
multiplicity bridge to the two existing open terminals, not their exclusion.
Since rooted depth is unimodal on a path, a branch-free maximal
full-bidirectional core crosses the strict band threshold at most twice.
Therefore the bidirectional alternative further gives a core containing a
global branch vertex or at least `gamma/272` distinct nontrivial path cores.
The latter need not yet be whole canonical corridor sinks.
There is also a conditional fixed-window theorem.  In the minimal subtree
joining the attachment root to the band leaves, a branch vertex with `d`
band-bearing child branches supplies `binom(d,2)` distinct leaf-pair distances
inside an interval of only `2gamma-1` integers.  Classifying *all* band-leaf
pairs by their LCA gives a preliminary linear bound.  The sharper count uses
all band pairs: ancestor-related pairs consume at most `gamma-1` small
distances, while every other pair is charged to a global branch LCA with
capacity `2gamma-1`.  This forces at least `gamma/64-O(1)` global branch
vertices.  Equivalently, if the whole tree has at most `K` branch vertices,
then `gamma<=64K+32`, independent of `n`; retaining the pole order gives
`gamma<=224` in the exactly-three-branch
case.  This **OBSERVED** theorem is conditional on the
singleton-pole endpoint normal form, but it converts every fixed branch-
complexity class into a genuinely fixed endpoint window.
The roots of the separate band components also form an antichain.  Their
minimal connector branches only outside the descendant-closed band.  Pairs
from different band components all have their LCA in that connector, while
within-component pairs consume at most `2gamma-2` distances.  Hence the same
all-vertex argument forces `gamma/64-O(1)` additional connector branch
vertices.  The receiving
arm pays the disjoint mass bound
`b>=ceil(gamma/a)+gamma/64-O(1)` (explicitly
`b>gamma/a+gamma/64-17/16` for `gamma>=68`).  This is an
**OBSERVED** branching-buffer refinement, not yet a contradiction with the
global mass balance.
The finite checker
`theory-lab/topwindow/verify_endpoint_branch_capacity.py` independently
replays the four pole orders for `K=0,1,2,3`, including the exact
`K=3` caps `14,56,126,224`, and checks the displayed uniform relaxations
through `gamma=10000`.  Its frozen output is
`theory-lab/topwindow/results/endpoint_branch_capacity_certificate.json`.
This is an **OBSERVED** arithmetic audit only; the all-order ancestor/LCA and
ceiling-tail arguments are (FW123)--(FW126).
For the at-most-three-branch class the singleton centre consumes one global
branch vertex, and the order-three/four pole root consumes another.  Since
every band-pair LCA remains inside `B`, the receiving arm has only `2,2,1,1`
available branch LCAs at pole orders `1,2,3,4`.  The four caps sharpen to
`10,40,54,96`, making the remaining truncated digit data finite.  Enumerating
(FW105)--(FW106) gives 10,597 parameter/mask rows; the exact (FW123) capacity
leaves 3,245, with 42,697 sharp first-hole states.  The next `gamma` after
each cap has no survivor.
This **OBSERVED finite local catalogue** is frozen by
`theory-lab/topwindow/verify_endpoint_threebranch_catalogue.py` and
`theory-lab/topwindow/results/endpoint_threebranch_catalogue_certificate.json`.
For pole orders three and four, `B` has at most one branch vertex.  The band
is therefore a common trunk followed by unbranched rays, or a collection of
terminal ray segments when that branch vertex lies above the band.  Exhaustive
canonical set-partition of the rays reduces the 2,828 order-three/four input
masks to 109, with maximum surviving gaps 13 and 20; their 38,028 sharp-hole
states reduce to 281.  For pole orders one and two, the two available branch
vertices in `B` must be comparable: otherwise their LCA is a third branch
vertex.  The resulting upper-splitter/lower-splitter skeleton has only nested
unlabeled ray partitions.  Its exhaustive canonical filter reduces the
remaining 417 masks to 64 and their 4,669 sharp-hole states to 238.  Hence the
complete exact-three-branch endpoint catalogue now has 173 masks and 519
sharp-hole states, with `gamma<=20`; consequently every genuine sharp first
hole in this terminal has the absolute bound `q'<=19`, independently of the
tree order.  Its pivot gate is a branch centre.  At pole orders three/four it
is an end centre with two pendant legs differing by at most 19, giving an `AC`
anchor; at pole orders one/two every retained third-centre attachment gives an
`AB` or `AC` anchor, never `AA/BB`.  This **OBSERVED connector reduction and
band-internal topology feasibility filter** is frozen by
`theory-lab/topwindow/verify_endpoint_onebranch_topology.py` and
`theory-lab/topwindow/results/endpoint_onebranch_topology_certificate.json`;
`theory-lab/topwindow/verify_endpoint_twobranch_topology.py` supplies the
two-branch certificate.  The optional Z3 diagnostic independently checks the
one-branch survivor hash, and a separate exhaustive reference agrees with the
two-branch DFS on 726 bounded configurations.
For the high-pole rows the strict cap is a segment of the pendant `b`--`z`
leg.  Its deficit differences must be mutually distinct and avoid the fixed
pole distances, so the endpoint imbalance has the **OBSERVED conditional
all-order alphabet** `{1,2,3,6}` at pole order three and `{1,2,4,5,8}` at pole
order four.  The tail-complete finite replay is
`theory-lab/topwindow/verify_endpoint_pole_deficit_alphabet.py`.
At pole order four, retain both alternatives
`delta_B(b)>=gamma` and `delta_B(b)<gamma`.  The `AC` connector lengths and ray
assignments can be kept symbolic while the order equation, vertex budget and
tail divisibility are safely relaxed.  Across 418 all-order parameter classes
(284 outside-band and 134 branch-in-band), 27 seeds satisfy the exact planted
metric.  None realises the entire top-20 window.  Exactly one branch-in-band
seed admits the first new vertex required by diameter-endpoint introduction;
after adding it, neither the complete top-80 window nor a legal second new
vertex is possible.  Thus the complete `a=4` high-pole endpoint terminal is an
**OBSERVED conditional all-order exclusion**, frozen by
`theory-lab/topwindow/verify_endpoint_ep4_symbolic.py` and its full certificate;
the 284-class outside-band subcertificate is also frozen separately.
The order-three row is also an **OBSERVED conditional all-order exclusion**.
Its 218 outside-band/common-trunk classes have 18 feasible planted metrics;
successive diameter-introduction stages leave 10, 6 and 2 children, while
every intervening top-window saturation is impossible.  The final two
classes, both `gamma=6,s=2,q'=1` and differing only by `t=c/t<c`, neither
saturate the top 160 after their third child nor admit a fourth child.  The
full transcript is frozen by
`theory-lab/topwindow/verify_endpoint_ep3_symbolic.py` and its certificate;
Z3 4.15.4 replays all 218 classes and Z3 4.16.0 agrees on the final two.
The `mu<=H` half of the order-one/two endpoint is now also an **OBSERVED
conditional all-order exclusion**.  Here `h=mu-gamma<t` gives
`theta<gamma`, so the controlled band is the complete receiving arm.  Exact
pivot topology leaves no order-one metric and only 13 order-two parameter
states, comprising 29 canonical ray metrics.  In 19 of them the third centre
lies in the lower part.  Its two placements relative to a height vertex give
38 seeds: four collide, the remaining 34 cannot saturate the top twenty, and
none admits the first new vertex required by diameter-endpoint introduction.
A separate direct-distance encoding splits that vertex among 136 lower-
subtree locations and independently returns infeasible in every case.  In the
other ten metrics the third centre lies below the pivot inside the complete
receiving arm.  One seed collides; the remaining nine fail both top-twenty
saturation and all 18 same/new-lower-leg introductions.  An independent
direct metric agrees.  Both Z3 4.15.4
and 4.16.0 return no `unknown`.  The calculation drops the order equation and
vertex budget, so it is uniform for `n>=18`.  Verifiers and certificates are
`verify_endpoint_lowpole_small_radius.py`,
`verify_endpoint_lowpole_small_radius_symbolic.py`, and
`verify_endpoint_lowpole_small_radius_reference.py` under
`theory-lab/topwindow/`, together with the two corresponding
`small_radius_upper` verifiers.
In the complementary `mu>H` branch, the exact inequality
`1<=q-t<=gamma-lambda-1` and the surviving digit catalogue give `q-t<=5`
at pole order one and `q-t<=10` at pole order two.  The latter leaves 48 masks
and 193 sharp holes.  This **OBSERVED conditional all-order fixed-cluster
reduction** is replayed by `verify_endpoint_lowpole_high_gap.py`; excluding
that cluster is still **UNVERIFIED**.  At pole order one the complete deficit
band paired with the `q`-leaf and a lower height-`q-gamma` vertex supplies the
exact doubled top block of deficits `0,...,2gamma-1`; distance uniqueness also
forces `mu-q>=gamma`.  This is a conditional all-order boundary extension for
the next clustered prover, not a closure.  Adding the lower height vertex as
an extra complement factor makes `S_gamma+(P union {gamma})` direct.  In the
order-two row this forces `gamma` to be a multiple of `2lambda`, eliminates
35 of the 48 masks and 150 of 193 sharp holes, and leaves 13 masks/43 holes
whose direct cross-pair block first misses coefficient `gamma+lambda`.  The remaining diameter
separation obeys `mu-H>=gamma-lambda>q-t`; the order-one analogue is
`mu-q>=gamma>q-t`.  This **OBSERVED conditional all-order factor-collision
reduction** is frozen by
`verify_endpoint_lowpole_factor_collision.py`; it is still not the missing
cluster exclusion.  Directness of the same `t`-cut pairs leaves an exact
empty layer on both sides.  It sharpens the root deficit to
`theta>=2gamma` in the order-one row and `theta>=gamma+lambda` in the
order-two row; equivalently `mu-H>=2gamma-(q-t)` and
`mu-H>=gamma-(q-t)`, respectively.  In the first row the attachment-root
pairs further force `theta<h` and `mu-h<t`.  These are uniform structural
constraints for the remaining clustered prover, not an exclusion.  The
symmetric outcome is now impossible at both low pole orders: the empty-layer
truncation leaves only one order-one and two order-two infinite pole tails,
and every allowed incident gap in those tails has a forced `G+gamma`
collision.  Thus every order-one/two `mu>H` state makes a strict handoff to
an internal `B` edge of weight at least `t-h+1`; the open task is to absorb
that proper-arm output into the global descent.  The exact band/truncation/
tail replay is `verify_endpoint_lowpole_symmetric.py`.
Together with the high-pole exclusions and the `mu<=H` low-pole exclusion,
this exhausts the exactly-three-branch singleton-pole endpoint: every row is
contradictory or returns to the FW85 internal-`B` handoff.  Absorbing that
return through the cap recurrence now also fixes the width of its
two-small-factor terminal when there are at most three global branch
vertices.  The exact high-distance factorisation and all-band LCA capacity
leave 66 ordered truncated pole-factor rows, bound the two interface sums by
176 and give `N-2h<=178`; the replay is
`verify_endpoint_two_small_factor_window.py`.  Replaying every remaining high
coefficient then leaves 1,199 necessary affine rows, with first interface at
most 3, longer interface at most 112 and `N-2h<=113`; see
`verify_endpoint_two_small_factor_spectrum.py`.  If both factors have order
at least three, their roots leave only `v` as a lower-core branch vertex;
the exhaustive ray-topology replay
`verify_endpoint_two_small_factor_root_topology.py` excludes all 25 such
rows.  If exactly one factor has order at least three, the remaining lower
core has only `v` and at most one further splitter.  Its exhaustive relaxed
topology replay reduces 740 rows to 61, and exact continuation through the
first `T` layers at/below `2h` leaves three explicit affine rows; see
`verify_endpoint_two_small_factor_nested_topology.py` and
`verify_endpoint_two_small_factor_boundary_continuation.py`.  When both pole factors have order at most
two, an LCA/ancestor-difference matching reduces 434 rows to 111; a complete
first-`T` continuation with freely relaxed internal pair bits reduces those
to 61.  Those bits cannot in fact choose their LCA independently: matching
every forced-band pair to one ancestor difference or to one of at most three
coherent LCA depths rejects 9,197 of the 12,514 relaxed extensions and reduces
the 61 rows to 34.  Together with the three `K=2` rows, 37 terminal rows remain;
see `verify_endpoint_two_small_factor_lca_layers.py`.  Exhaustive placement in
the root-only, one-splitter, nested-chain and forked-two-splitter hierarchies
then excludes three full `K=3` rows (seven extensions, maximum 74,935 states,
no cap hit), leaving 31 `K=3` and hence 34 terminal rows; see
`verify_endpoint_two_small_factor_root_hierarchy.py`.  On the larger original
set of all three plus 61 rows, the deficit cut at `2T` gives a proper connected
induced core after deleting at most 23 vertices;
its diameter is at most `N-12` (and at most `N-24` in the three exactly-one-
high-factor rows).  This is an **OBSERVED conditional constant-deletion core
reduction**, not an exclusion: the missing inheritance theorem must prevent
the omitted endpoint pieces from growing this shallow core back into a Leech
tree.  FW195 subsequently excludes the three `K=2` rows, and FW198 excludes
the first `K=3` row `P=U={0}, Q=2, R=1` by an exact 50-coefficient
chain/fork continuation.  FW199 excludes seven further `K=3` rows by exact
30-coefficient continuations covering 13,874 configurations, and FW200
excludes four more rows by a sharded replay of 7,928 configurations.  The
FW201 persistent-worker replay excludes another eleven rows in 21,802
configurations.  The final mixed `H=40/50` FW202 replay then partitions
30,346 configurations into 7,079 exact shards and excludes the last eight
`K=3` rows, with no frontier, unknown or state-cap hit.  Its row-specific
height-separation signatures are stable for every `h>=259`.  Thus FW195 and
FW198--FW202 give an **OBSERVED conditional all-order exclusion** of the
present at-most-three-global-branch two-small-factor affine terminal.  This
does not cover the thick-surplus, separate lower-core, or higher-global-branch
outputs and is not the global theorem.
The same 64 rows also satisfy the sharper exact low-spectrum bounds
`N-2q<=2` and `q-L_0<=30`.  Reusing the FW78 capacity argument therefore
forces either a complete lower arm or the connected all-low core to have
order at least `K_n=ceil((3n-6-sqrt(7n^2-50n+324))/2)-1`, asymptotically
`((3-sqrt(7))/2)n+O(1)>0.17712n+O(1)`.  This is another **OBSERVED
conditional mass reduction**.  Coupling the arm-internal and shallow-cross
capacities by packing the deep vertices sharpens this to
`Khat_n=((4+sqrt(2))/28)n+O(1)>0.19336n+O(1)`, with exact first values
`7,8,10,11,13,14,16,17` before row correlation.  Retaining each row's actual
`(a,b)` and low-spectrum loss improves these to `8,9,11,11,14,14,17,17` at
orders `36,38,49,51,64,66,81,83`.  If the output is the complete arm, its
incident thin edge now has an exact dichotomy: either the complementary side
contains at least `n^2/50-3n/10+1` internal pairs above that edge, or its cut
product exceeds `4n^2/25`.  This feeds respectively the thick-tip and
weighted edge-excess branches.  The cut product is not itself a Kruskal merge
product, but the exact singleton-centre decomposition now shows that it forces
either a merge product of at least half that size or an explicit waste term;
uniformly the balanced-cut branch has `TW>=n^4/625-O(n^3)`.  A matching waste
upper bound remains **UNVERIFIED**.  The alternative all-low core is no longer
shape-free: for every fixed `d>=2` it contains a complete arm of order at
least `ceil((Khat_n-1)/d)`, or its centre supports more than
`(Khat_n-1)+(d-1)(Khat_n-1)^2/(2d)` distinct low cross pairs.  Thus all rows
in the earlier relaxation route to a
linear thin arm or quadratic thick centre, but neither final
contradiction follows from that routing alone.  Excluding this
core output, the outside endpoints of the singleton
normal form, and the thin/full-
bidirectional continuations remain **UNVERIFIED**.
For the 34-row FW164 relaxation, pointwise recomputation strengthens the historical
64-row bounds to `q-L_0<=22` and `2L_0>=N-28`.  Their connected induced lower
core has order at least `n-5`, misses at most 21 values from `1,...,q-1`, and
its increasing edge schedule satisfies `w_{k+1}<=Pi_k+22` at every rank.
This **OBSERVED conditional defect-21 covering theorem** avoids falsely
treating the core as a smaller Leech tree;
closing or descending this constant-defect schedule remains **UNVERIFIED**.
The same rows have a stronger localized schedule.  Below the receiving edge
`t`, the FW78 pair partition leaves only the two pole-internal distance sets
outside the lower core, while FW77 gives `t>h` and therefore places every
lower-core edge below `t`.  Thus there are at most four holes below `t` and
`w_{k+1}<=Pi_k+5` at every rank (at most two holes on the then 31 `K=3` rows, and
`3,4,3` on the three `K=2` rows).  This **OBSERVED conditional defect-four
prefix inheritance** is audited by
`theory-lab/topwindow/verify_endpoint_terminal_prefix_defect.py`.  It is not
itself interchangeable with a rooted cross-sum hole, but charging a failed
cross deficit either to one of these four genuine missing values or to a
same-side core pair composes it with the finite-hole ladder.  Consequently
every lower-core edge `w` satisfies `t-w<=34`, or one component of `C_0-w`
contains a pair of distance in `{w+1,...,w+34}`.  The offset improves to 22
on every `K=3` row and is `31,34,31` on the three `K=2` rows.  This
**OBSERVED conditional internal directional handoff** is audited by
`theory-lab/topwindow/verify_endpoint_terminal_core_handoff.py`; converting
the internal pair into a heavier nested edge, or forcing reversals to a thick
centre, is now the active synthesis step and remains **UNVERIFIED**.
There is already a bounded form of the reversal alternative: the core has at
most 34 edges in the weight window `[t-34,t-1]`.  Contracting their connected
components and orienting every other edge by the internal handoff produces a
sink component of order at most 35.  This **OBSERVED conditional bounded-sink
reduction** localizes every failure of direct nesting to a fixed-size core;
the branches incident with that core can still be unbounded and must now be
coupled to the thin-arm/quadratic-thick-centre dichotomy.
Using the hole-eight ladder row, every edge farther than 51 below `t` actually
has at least five distinct same-side core pairs by offset 51 (at least seven
for `K=3`, and `6,5,6` for the `K=2` rows).  The certificate composition is
`theory-lab/topwindow/verify_endpoint_terminal_core_handoff_multiplicity.py`.
The bounded sink also has an exact shape: since `t>=135`, an internal arm
edge of weight at least `t-34` together with its still heavier incident edge
would exceed the lower height `h`.  Thus all near edges are incident with
`v`; the FW168 sink is a star at `v` or a singleton.  Every corresponding
near incident arm has order at most 34, so absorbing all of them gives a
star-sink of order at most 1157 whose remaining boundary edges all hand
inward.  These are **OBSERVED conditional all-order reductions**; the active
gap is now the unbounded far arms at this fixed centre.
Those arms have no internal near-`t` exception.  If `u` is an internal arm
edge and `p>u` is its `v`-incident edge, then `p+u<=h`, so
`u<=floor((h-1)/2)`.  With `h>=134` this gives `t-u>=69`; FW169 therefore
supplies at least five same-side pairs by offset 51 at every internal arm
edge (at least seven for `K=3`).  The remaining synthesis problem is now
precise: either one of these handoffs points into a nested far-arm component,
or all of them point back toward the fixed star and must be converted into a
thick-centre collision.
Finally, the branch-count slack is illusory.  Phase I forces exactly three
global branch vertices in this at-most-three-branch terminal.  Thus each
`K=2` row has exactly one hidden lower splitter besides `v` (and it lies
outside the forced band), while each `K=3` row has exactly two lower splitters
besides `v`, in a chain or fork.  Every off-skeleton component is a path by
the three-branch normal form.  This **OBSERVED conditional exact-skeleton
reduction** changes the remaining target from arbitrary far arms to bare
weighted corridors on a fixed one-/two-splitter skeleton; it does not itself
exclude a row because all compulsory splitter vertices may be outside the
finite band.
The Kruskal identity also refines exactly to
`TW=(sum Delta_k^2-N)/2+sum Delta_k sigma_{k-1}`.  For each internal arm edge,
its five same-side handoff paths either contain a heavier edge in the same
proper side, giving strict nested descent, or are already present in the
lighter forest and force `sigma>=5` (`>=7` for `K=3`).  Since the merge
products of all internal edges sum to `I_R`, consistent reversal gives the
global lower bound `TW>=(sum Delta_k^2-N)/2+5I_R`, strengthened to `+7I_R`
for `K=3`.  This **OBSERVED conditional descent-versus-waste theorem** leaves
one quantitative task: upper-bound the waste of the fixed three-centre thick
terminal, with the complementary small-`I_R` regime charged to its cross-arm
mass.
Cut capacity makes the thin side asymptotically sharp enough to matter.  If
an internal edge cuts core orders `s,m-s`, then below `t` it has at least
`max(9-e,floor(h/2)+R-e-s(m-s))` same-side pairs, `e<=4`.  Summing from the
free end of a bare leg shows that a leg of order
`((1-1/sqrt(2))/2)n+O(1)` either contains a nested heavier edge or contributes
`((sqrt(2)-1)/48)n^3+O(n^2)` to the weighted covering surplus.  At orders
`36,38,49,51,64,66,81,83`, the uniform required leg orders are
`6,6,8,8,10,10,12,13` and the corresponding surplus totals are
`315,380,861,987,2013,2220,4191,4520`.  This **OBSERVED conditional cubic-
waste reduction** is audited by
`theory-lab/topwindow/verify_endpoint_terminal_cut_capacity.py`.  The active
case is now the several-short-leg thick centre rather than a long corridor.
The two bare skeleton segments obey the same sum: their cut side orders are
consecutive.  Since the capacity density `1/8-x(1-x)` is positive outside
`[alpha,1-alpha]`, `alpha=(1-1/sqrt(2))/2`, every consistently reversing
linear corridor either pays cubic surplus on its unbalanced tails or leaves
two endpoint blocks each containing at least `alpha(n-O(1))` vertices.  This
**OBSERVED conditional corridor-to-two-thick-blocks reduction** identifies
the final uncharged terminal; its additive collision or waste upper bound is
still **UNVERIFIED**.
The cubic pendant-leg estimate can be amplified without any new state search.
For the first `r` cuts from a free end, the cumulative Kruskal merge product
is at least `binom(r+1,2)`; Abel summation against the decreasing `kappa(s)`
profile therefore gives `sum s kappa(s)`, namely
`((8sqrt(2)-11)/768)n^4+O(n^3)`.  At the eight target orders the exact uniform
charges are `675,850,2380,2800,6990,7860,17776,19656`.  This **OBSERVED
conditional merge-product amplification** is replayed by
`verify_endpoint_terminal_merge_amplification.py`.  Its coefficient is too
small to be a contradiction by itself, so the active step is to aggregate
these quartic charges over all legs and skeleton segments or sharpen the
two-thick-block upper bound.
That aggregation is now exact for a bundle of short pendant arms at one
non-root lower-core branch centre, so every selected edge is internal to a
lower arm rather than incident with `v`.  If the bundle has total off-centre
order `V`, maximum arm order `S<=m/2`, and no selected handoff yields
nested heavier-edge descent,
then connected-subtree merge mass gives
`sum Delta_e sigma_e >= kappa(S) binom(V+1,2)`.  Hence
`V=beta n+O(1)`, `S=gamma n+O(1)` with `gamma<alpha` pays
`beta^2(1/8-gamma(1-gamma))n^4/2+O(n^3)`.  This **OBSERVED conditional
short-arm star-bundle amplification** closes the previous one-edge-at-a-time
loss at a non-root diffuse thick centre.  The exceptional bundle incident
directly with `v` and the missing terminal waste upper bound remain.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_star_bundle.py`.
The root bundle now has a sharp density cap even though its covering surplus
is not yet aggregated.  Taking one farthest point in every component of
`C_0-v` produces a weak Sidon set of root depths.  Kayll's Ruzsa bound is
**LITERATURE** and gives `d_v<=n/2+O(sqrt(n))`; the project reduction and exact
finite difference inequality are **OBSERVED conditional all-order**.  Thus at
least `n/2-O(sqrt(n))` lower-core edges are non-`v`-incident and fall under the
FW171/FW174 regime.  Exact target-order lower bounds are
`5,6,10,12,16,18,23,25`.  This still leaves the robust-spider terminal in
which linearly many order-two arms all reverse their one interior handoff
toward `v`; combining those charges is the next stop-loss milestone.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_root_arms.py`.
That stop-loss milestone is now met through the global path-slack identity,
not through a false connected-bundle claim at `v`.  If the root-incident
weights are `p_1<...<p_d`, every prefix is weak Sidon, so the exact FW178
span bound gives `p_i>=G(i)+1`; the path between the two first arm vertices
has slack `min(p_i,p_j)`.  Therefore
`TW_root>=J(d)=sum_i(d-i)(G(i)+1)`.  Taking
`q=floor(sqrt(i))` in the exact span inequality gives the self-contained
**OBSERVED conditional all-order** consequence
`d=beta n+O(1) => TW_root>=beta^4 n^4/12-O(n^(7/2))`.  Parameterizing at
`beta=1/4` leaves the exact alternative: quartic root slack, or at least
`3n/4-O(1)` non-`v`-incident core edges.  The next milestone is to combine
the latter edge mass with FW176/FW177 across the two-splitter skeleton, while
the former still needs the same missing terminal `TW` upper bound.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_root_slack.py`.
The diffuse part of that milestone is now met without assuming path-shaped
root arms.  If the components of `C_0-v` have orders `s_i<=m/2`, connected-
subtree merge mass and the monotone FW174 profile give the exact
**OBSERVED conditional all-order** bound
`TW>=max(J(d_v),sum_i kappa(s_i)binom(s_i,2))`.  If all `s_i<=m/8`, Cauchy
and FW179 imply `TW=Omega(n^(16/5))`; otherwise there is a linear thick root
component.  Thus the remaining sparse-root geometry is no longer diffuse:
it is a fixed one-/two-splitter thick component, whose reduction to a charged
pendant bundle or the two-thick-block corridor is still **UNVERIFIED**.
Replay: `theory-lab/topwindow/verify_endpoint_terminal_component_aggregation.py`.
The thick component itself now collapses without the skeleton classification.
With `tau=floor(m/8)`, either one internal edge has both core-cut sides at
least `tau+1`, or every internal edge has smaller side at most `tau`; in the
latter case FW174 plus connected-subtree merge mass pays
`kappa(tau)binom(tau+1,2)=Omega(n^4)`.  Combined with FW180, this is the
**OBSERVED conditional all-order** alternative: nested descent, a linear
two-thick-block cut, or `TW=Omega(n^(16/5))`.  The first unresolved geometry
is therefore exactly the thick cut; the other unresolved ingredient is a
terminal `TW` upper bound.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_thick_component.py`.
The thick cut itself now has an exact cross-path slack inequality.  If its
edge has weight `u`, full cut product `c` and Kruskal merge product `Delta`,
then the crossing paths give
`TW>=binom(Delta,2)+u(c-Delta)>=F(c,u)`.  Since the FW181 cut has
`c=Omega(n^2)`, weight `u>=m^(6/5)` already pays
`Omega(n^(16/5))`.  The remaining balanced geometry is therefore a linear
separator of weight below `m^(6/5)+1`.  This is an **OBSERVED conditional
all-order scale reduction**, not an exclusion; its low-weight branch and the
terminal `TW` upper bound remain **UNVERIFIED**.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_balanced_edge_slack.py`.
The defect-four schedule adds a disjoint same-side contribution.  For a core
split `r,m-r`, let `H=[t-u-1-e-r(m-r)]_+`.  Unless one of those same-side
paths exposes a nested heavier edge, their distinct offsets contribute
`H(H+3)/2`, so
`TW>=F(r(m-r),u)+H(H+3)/2`.  With the FW182 low-weight bound this makes every
fixed noncentral band quartic; more sharply a survivor below the
`n^(16/5)` scale must satisfy `|r-m/2|=O(n^(4/5))`.  This is an **OBSERVED
conditional all-order near-bisection reduction**, not an exclusion.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_balanced_edge_holes.py`.
The fixed FW172 skeleton now absorbs that near-bisection geometry.  On the
side away from `v`, at most two bare corridors and two complete non-root
pendant bundles contain all but two vertices.  A linear pendant bin is
quartically charged by FW176/FW177.  A linear corridor has only
`O(n^(4/5))` near-bisection edges; a linear unbalanced tail has
`kappa=Omega(n^2)` and quadratic connected merge mass, hence is also
quartically charged.  Therefore the FW179 sparse branch now satisfies the
**OBSERVED conditional all-order** synthesis: strict nested descent or
`TW=Omega(n^(16/5))`.  The active gaps are no longer sparse aggregation but
closure of the descent and a terminal `TW` upper bound.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_sparse_synthesis.py`.
Retaining all vertices in each root component improves the exponent.  If
`p_1<...<p_d` are the incident weights and `s_i` the component orders, all
`s_i s_j` cross-component paths contribute at least `min(p_i,p_j)`, so
`TW>=sum_{i<j}s_i s_j(G(i)+1)`.  With `Q=sum s_i^2`, FW180 gives
`Omega(n^2 Q)` when `Q` is large; when it is small, Cauchy leaves quadratic
mass after index `k=Theta(n^2/Q)`, where FW179 gives weight
`Omega(k^2)`.  Optimizing yields the stronger **OBSERVED conditional all-
order** synthesis “strict nested descent or `TW=Omega(n^(10/3))`.”  The
large-component skeleton proof parameterizes identically at exponent `10/3`.
Replay: `theory-lab/topwindow/verify_endpoint_terminal_weighted_root_slack.py`.
The constant-window direction can now be followed to its actual endpoint.
An FW167 heavy handoff raises the edge weight by at most its row radius
`K(e)<=34`; an FW169 multiplicity handoff raises it by at most 51.  A core has
only `m-1` edges, while an internal arm edge lies quadratically far in weight
below the near-`t` window.  Consequently the **OBSERVED conditional all-
order** bounded-ascent theorem says that for `n>=271` every FW167 ascent ends
at a light handoff with `sigma>=1`, and for `n>=407` the fivefold version ends
with `sigma>=5` (`>=7` in `K=3`).  This eliminates an infinite/near-star
escape for the bounded window.  It does not yet close FW185: ascent basins
may coalesce, and its larger-offset handoffs do not have the same step bound.
Replay: `theory-lab/topwindow/verify_endpoint_terminal_bounded_ascent.py`.
The waste endgame has also been put on the correct truncated ledger.  Because
`q` is globally heaviest and `q=N/2+O(1)`, the full waste splits exactly as
`TW=binom(N-q+1,2)+RW_q`, with a fixed top triangle
`n^4/32+O(n^3)`.  If `E_q=N-a(n-a)-q+1`, then
`RW_q=sum_{i<r}binom(Delta_i,2)-binom(E_q,2)+sum_{i<r}Delta_i sigma_{i-1}`
and `E_q=n^2/4-O(n)`.  Thus the real terminal problem is a quartic
pre-`q` compensation/upper-bound problem, not merely raising the exponent of
a lower bound for the full `TW`.  This **OBSERVED exact accounting theorem**
also prevents double counting: FW185 cannot automatically be added to the top
triangle unless its charge is localized in `RW_q`.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_truncated_waste.py`.
That compensation is now known to concentrate at quadratic scale.  If `D`
is the largest pre-`q` merge product, `Z` the largest pre-`q` covering
surplus, and `S,E_q` are as above, then the exact **OBSERVED** inequality
`D+2Z>=1+ceil(E_q(E_q-1)/S)` gives
`max(D,Z)>=n^2/24-O(n)`.  Thus the terminal endgame splits into a macroscopic
light-merge cut (whose smaller Kruskal side has order at least
`((1-sqrt(5/6))/2)n-O(1)`) or a quadratically overfilled threshold.  This is
not yet an exclusion: the former needs a thick-cut/corridor contradiction,
and the latter needs a duration or multiplicity bound inside `RW_q`.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_compensation_concentration.py`.
The quadratic event is now **OBSERVED exactly localised**.  A pre-`q` merge
of size `Delta` at weight `w` contributes at least
`sum_{j<Delta}min(j,q-w)` to `RW_q`; a surplus `sigma` at the same threshold
contributes at least `sum_{j=0}^{q-w}max(sigma-j,0)`.  Therefore, for the
FW188 threshold `M`, either `RW_q>=binom(M,2)` or a size-`M` witness lies in
the band `q-M+2,...,q-1`.  FW171 removes every non-incident lower-arm edge
from this band.  For `n>=124`, the merge witness exceeds every bounded outer
cut product and is consequently a `v`-incident lower-arm edge; the surplus
witness has only those centre edges plus at most seven outer positions.
Equivalently, `RW_q=o(n^4)` forces the witness into `q-o(n^2)`.  The remaining
endgame is thus root/top-skeleton congestion rather than arbitrary core
coalescence.  It still needs a residual upper bound or a contradiction at
that skeleton.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_top_localization.py`.
The final `q`-excess now transfers **OBSERVED exactly** to a single lower-core
root boundary.  If `p` is the heaviest edge of `C_0`, then `p` is
`v`-incident and `Delta_p=s(m-s)`.  All pre-`q` outer-factor merge mass is
`O=binom(a,2)+binom(b,2)+bm=O(n)`, so telescoping from `p` to `q` gives
`sigma_p+Delta_p>=E_q-O` and hence
`max(sigma_p,Delta_p)>=n^2/8-O(n)`.  The merge branch has both root-cut sides
linear (the smaller is at least `0.146446...n-O(1)`), while the surplus branch
has an already-connected root side of order `n/2-O(1)`.  This removes the
quadratic-scale basin-coalescence ambiguity: the next proof obligation is a
two-case contradiction at this one named boundary, not aggregation over
arbitrary terminal chains.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_core_boundary_transfer.py`.
The merge half of that boundary dichotomy now has an **OBSERVED** quartic
charge localised in `RW_q`.  An order-`s` last arm has rooted eccentricity at
least `ceil(binomial(s,2)/2)`, so its incident edge has runway
`q-p>=Q+ceil(binomial(s,2)/2)`.  Together with
`s(m-s)>=n^2/8-O(n)`, the exact FW189 path floor gives
`RW_q>=((7-4sqrt(2))/2048)n^4-O(n^3)`.  The remaining proof obligation is
therefore the other FW190 branch: a quadratic surplus immediately before the
last core edge, with an already-connected root side of half order.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_merge_runway.py`.
That surplus branch is now closed at quartic residual scale.  Peel lower arms
from greatest incident weight downward.  Peeled order `z` accounts for at
most `U(z)=z(m-z)+binom(z,2)` later core merge mass; while `z<n/16`, transfer
from `E_q` forces the next `Delta` or `sigma` to be at least `n^2/16`.  The
first case has the FW191 runway charge.  In the second, a hypothetical
`RW_q=o(n^4)` forces every peeled incident edge into `q-o(n^2)` and every arm
to have order `o(n)`.  At total peeled order `n/16`, `Theta(n^2)` cross-arm
distances would then lie in an `o(n^2)` interval below `N`, contradicting
distance uniqueness.  Quantifying the inequalities yields the **OBSERVED
conditional all-order** bound `RW_q>=10^(-6)n^4` for all sufficiently large
orders in every current affine terminal row.  The central remaining task is
now a conflicting upper bound on this same residual, not a further lower-
bound aggregation.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_surplus_peeling.py`.
Keeping the `-z^2/2` suffix term and peeling to `n/7` improves the same
**OBSERVED conditional all-order** conclusion to `RW_q>=n^4/25000` for all
sufficiently large orders.  The exact pairwise decomposition then shows that
pairs outside the order-`n-O(1)` core contribute only `O(n^3)`, so
**OBSERVED conditionally** `RW_C>=n^4/50000`; at least `n^2/20000` core
pairs eventually have capped slack at least `n^2/100000`.  The open step is
therefore a defect-21-core stability/collision theorem, not another global
lower-bound aggregation.  These claims are not an exclusion.  Replay:
`theory-lab/topwindow/verify_endpoint_terminal_surplus_peeling_sharp.py` and
`theory-lab/topwindow/verify_endpoint_terminal_core_residual.py`.
Excluding the deep-offshoot endpoint, the lower-core outcomes and a non-singleton
bidirectional thick core remains
**UNVERIFIED**.  Proof and audit:
`docs/edge-handoff-orientation.md` and
`theory-lab/topwindow/verify_singleton_thick_centre.py`, with the transition
diagnostic in `theory-lab/topwindow/verify_rooted_gap_transition.py`.

The small-distance side of the intended terminal contradiction is also now
**OBSERVED**. In increasing edge-weight order, the merge products
`Delta_k=a_k b_k` sum to `N`, force
`w_{k+1}<=1+sum_{j<=k}Delta_j`, and give the exact path-slack identity and lower
bound

```text
TW = sum_P(d(P)-maxedge(P)) >= (sum_k Delta_k^2-N)/2.
```

Proof and audit: `docs/kruskal-covering-waste.md` and
`theory-lab/smallend/verify_kruskal_waste.py`. Balanced heavy merges therefore
force large waste. The remaining endgame must upper-bound the available waste
in the thick terminal geometries left by the central/top-window dichotomy.

The value-order part is also **OBSERVED**: by diameter-endpoint introduction,
the far-pair graph on distances `N,N-1,...,N-q` is connected in precisely that
decreasing order; every new vertex arrives adjacent to `a` or `b`, and every
pair disjoint from the diameter has both endpoints already present.  Thus the
far graph is dominated by `{a,b}` and has graph hop-diameter at most three.
Proofs and audits: `docs/diameter-endpoint-introduction.md`,
`docs/top-window-connectivity.md` and
`theory-lab/topwindow/verify_top_window_connectivity.py`.

For `2q<N`, all q-far neighbours of a vertex also share an initial
tree segment of length at least `N/2-q`, hence all its incident far edges point
in one tree direction.  Diameter domination eliminates long handoffs entirely:
`diameter_hop(H_q)<=3`.  Proof and
audit: `docs/far-neighbor-cone.md` and
`theory-lab/topwindow/verify_far_neighbor_cone.py`.  The remaining issue is the
bounded geometry of off-diameter trunks and exclusion of its terminal catalogue.

**UNVERIFIED target T.** A Leech tree cannot have both extreme regions thick
at every terminal step of target D.

Neither target D nor target T is presently proved.  A realistic first global
output may be an explicit upper bound `n<=n0`, rather than immediate complete
nonexistence.  Taylor would then leave finitely many admissible orders for
certified computation.

## 7. Do Phases I and II really help Phase III?

Yes, but only under the lemma-extraction requirement of II-C.

| earlier result | contribution to descent | what it does not provide |
|---|---|---|
| uniform spider theorem | complete one-centre terminal catalogue and proof that a long bare extreme cannot survive | no information about nested branching |
| uniform bi-spider theorem | base case for descent by branch complexity; complete two-centre collision catalogue | no contradiction once a third or fourth centre is present |
| order-25 three-branch search | first stress test of the transition through a third centre; exposes missing realiser types and a candidate decreasing measure | a fixed-order zero count is not an all-order lemma |
| order-25 short-diameter search | closes compact terminal geometries and tests many-centre local collisions | it does not control long or deeply nested branch skeletons |

Thus Phase I is directly reusable mathematics.  Phase II is partly a theorem
and partly an experiment designed to discover the correct local transition.
If Phase II is implemented as a black-box order-25 exhaustion, its benefit to
Phase III is limited.  If its case tree is exported as bounded symbolic
transitions, it becomes the first inductive step of target D.

## 8. Verification and promotion rules

These rules are mandatory at every phase:

1. Every conclusion in `README.md` is labelled `OBSERVED`, `LITERATURE` or
   `UNVERIFIED`.
2. Every SAT witness passes both independent repository checkers.
3. Load-bearing searches have a clean-room implementation or an equally
   independent method comparison, with per-regime or per-level invariants.
4. Verifiers reject optimisation modes that remove checks; no proof-critical
   Python `assert` is permitted.
5. Shards report caps and completion explicitly.  `found=0` with `capped=1`
   is not a theorem.
6. Hoffman2 uses SLURM `sbatch`, never `qsub`.
7. A fixed-order computation is not promoted to an all-order claim without a
   written finite partition or induction covering the unbounded parameters.

## 9. Ranked execution order

1. **OBSERVED complete:** all LR and LL anchors at `n>=18`; combined audited
   no-bi-spider theorem.
2. **OBSERVED complete:** the audited 512-shard hop-diameter-four order-25 run
   has zero solutions and a frozen aggregate; arbitrary order-25 trees remain open.
3. **OBSERVED / UNVERIFIED active:** topology normal form, engine and the
   completed `n=25,W=25` diagnostic are audited; its 166,321,078-state frontier
   proves that a wider window or a parameter-independent transition lemma is
   required before order 25 can be exhausted. The later exact `W=60/W=70`
   campaigns close the exactly-three-branch class at orders 25 and 27. An
   affine all-integer lift is calibrated at order 10, but its first `AB,W=8`
   8-by-8 scale run was stopped after eight minutes with no feasible cell
   completed. This **UNVERIFIED negative diagnostic** means the vertex-budget-
   free relaxation should not be scaled further; the next lift must encode a
   sound order/vertex-budget transition or export a structural case lemma.
4. **UNVERIFIED synthesis:** use the edgewise constant-10 handoff and finite
   excess ladder to prove nested directional descent, or turn reverse
   handoffs into the thick-tip contradiction; use this to attempt target D.
5. **UNVERIFIED endgame:** combine descent with a thick-tip contradiction;
   derive an explicit finite order bound and close its remaining Taylor orders.

The programme should be reassessed after milestones B and II-B.  A growing
unbounded frontier, an uncontrolled deficit recurrence, or a third-centre case
that cannot be represented by bounded offsets is evidence that the proposed
descent is wrong and that the project should pivot before larger computations.
