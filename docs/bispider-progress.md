# Bi-spider theorem for n>=18: paired LR/LL certificates and audit

**OBSERVED — computer-assisted theorem, updated 2026-08-21.** Seven paired
finite relaxations exclude every `LR` anchor at every order `n>=18`; three
paired W=36 relaxations exclude every `LL` anchor there.  Thus no Leech tree
of order `n>=18` has at most two branch vertices.  **UNVERIFIED:** the stronger
conjecture that no bi-spider of order `n>=7` is Leech remains open.

## 1. Normalisation and the finite numeric search

A bi-spider has branch centres `cL,cR`, joined by a path of weighted length
`Q>=1`.  Its other vertices are marks on left legs, right legs, or in the
interior of that path.  If the pair at distance `N=binom(n,2)` is on opposite
sides, mirror so that its tip depths satisfy

```text
LR:  A < B,    A + Q + B = N.
```

If both tips are on one side, mirror that side to the left and write

```text
LL:  T1 > T2,  T1 + T2 = N,  1 <= Q < T2.
```

These cases are exhaustive because a maximum-distance pair consists of two
leaves.  In the `LR` case any further left/right tip is strictly below `A/B`.
In the `LL` case every further left tip is below `T2`, and every right mark is
below `T2-Q`; equality in either statement would repeat `N`.  These are exactly
the caps used by the numeric search.

The production Python and C programs share a hand-written realiser case split,
so their previous agreement was differential testing of a port, not an
independent algorithm.  `bispider_cleanroom.py` instead uses immutable geometric
states, recomputes every distance from scratch, enumerates every legal position
slot, and solves the single metric equation `d(x,y)=v` for a second new endpoint.
It imports no production search code.

`verify_bispider_cleanroom.py` freshly compiles the C engine and compares `LR`
and `LL` separately for every order `4,...,10`.  All 14 regimes agree exactly
on anchor, node and solution counts (27,046 nodes per implementation):

| order | both-case nodes | solutions |
|---:|---:|---:|
| 4 | 2 | 2 |
| 5 | 13 | 0 |
| 6 | 143 | 1 |
| 7 | 644 | 0 |
| 8 | 1,989 | 0 |
| 9 | 6,156 | 0 |
| 10 | 18,099 | 0 |

The two order-4 witnesses and the order-6 double star pass both
`src/checker_a.py` and `src/checker_b.py`.  This audit independently validates
the realiser enumeration on the stated orders; it is not an independent rerun
of the order-25 or order-27 search.

## 2. Balanced-centre LR region

Put `r=Q-(B-A)`.  The following is now proved.

> **OBSERVED theorem A.** No `LR`-anchored Leech bi-spider satisfies
> `A>20` and `r>20`.

Indeed, for a non-`LR` pair the potentially largest same-side distances are
`2A-1` and `2B-1`.  Their deficits below `N` are respectively
`Q+B-A+1` and `Q+A-B+1=r+1`.  Centre/leg and spine/leg pairs have deficits at
least `A` or `B`.  Since `A<B`, the two hypotheses put every non-`LR` distance
strictly below `N-20`.

Consequently a realiser of `N-k`, `k<=20`, has the form

```text
(A-a) + Q + (B-b) = N-k,    a+b=k.
```

The finite relaxation retains only necessary bounded collision classes:
left-right offset sums, all same-leg offset differences, and different-leg
offset sums on each side.  It drops parameter-dependent collisions, the spine,
and the vertex budget, so it is a supertree of every exact search in the stated
region.  Both the incremental implementation and an immutable full-recomputation
implementation close with identical statistics:

```text
W=20, nodes=2871, accepted=2870, dead=1754,
deepest missing offset=20, max marks=10, frontier=0.
```

## 3. Right-tip-dominant LR region

Put `C=A+Q`, so that `N=B+C`.  A second infinite region is also closed.

> **OBSERVED theorem B.** No `LR`-anchored Leech bi-spider satisfies
> `A>15` and `B-C>15`.

View the tree from `cR`.  The distinguished right leg has extent `B`; every
vertex outside it has depth at most `C`, since a larger depth would make its
distance to the `B`-tip exceed `N`.  Two outside vertices are at distance at
most `2C`, and two points on the distinguished leg are at distance at most
`B`.  Thus a value `N-k`, `k<=15`, joins a mark `B-a` on that leg to an outside
mark at depth `C-b`, with `a+b=k`.  Because `A>15`, a point within 15 of depth
`C=A+Q` cannot be a centre or an interior spine point; it is either a left mark
`A-b` or a mark `C-b` on another right leg.

The relaxation keeps the necessary high sums, all same-leg differences,
different-left-leg sums, and the common-base sums for left/right and
different-right-leg pairs.  It omits every other collision class.  The
incremental and immutable implementations agree exactly:

```text
W=15, nodes=1881, accepted=1880, dead=1057,
deepest missing offset=15, max marks=10, frontier=0.
```

`verify_bispider_regular.py` recomputes both theorem A and theorem B with both
implementations and checks the frozen statistics above.

## 4. Bounded-imbalance LR region

The remaining imbalance strip can also be made finite.  Continue to put

```text
r = Q-(B-A),       h = N-2A = 2Q-r.
```

> **OBSERVED theorem C.** No `LR`-anchored Leech bi-spider satisfies
> `A>50` and `-15 <= r <= 20`.

Here is the reduction audited by `verify_bispider_strip.py`.  Fix the window
`W=50`, and write a selected left mark as `A-a` and a selected right mark as
`B-b`; the two anchor tips have offsets `a=b=0`.  Because `A>W`, every realiser
of `N-k`, `0<=k<=W`, is one of exactly three types:

```text
LR:  k = a+b,
RR:  k = r+b+b'       (different right legs),
LL:  k = h+a+a'       (different left legs).
```

Indeed, a centre/leg or spine/leg distance has deficit at least `A` or `B`, a
spine/spine distance has deficit at least `A+B`, and a same-leg distance is
also below this top window.  The displayed formulae follow by subtracting the
three remaining pair distances from `N=A+Q+B`.

Every selected offset is at most

```text
M = W-min(r,0).
```

The search keeps only necessary conditions: all displayed offsets are globally
unique; all same-leg offset differences are globally unique and avoid the
centre distance `Q=(h+r)/2`; and the centre/mark equalities `a-b=r` and
`b-a=h` are forbidden.  Different-leg sums on each side are also unique.  It
omits other collision classes, the actual leg caps, the spine positions and
the vertex budget, so every exact Leech continuation maps into this relaxed
search.

At a state, let `k` be the least missing offset in `1,...,W`.  The three
displayed equations enumerate all ways to realise `N-k`, assigning same-side
endpoints to different legs.  Thus a state with every offset through `W` would
be a frontier state, while an empty frontier proves nonexistence.

Only finitely many `h` need be searched.  For fixed `r`, positivity of `Q` and
`A<B` give

```text
Q >= max(1,r+1),       h = 2Q-r.
```

The prover checks every admissible `h` through

```text
H(r) = max(W, 2M+|r|)
```

and the first admissible value above `H(r)`.  That last value represents the
entire infinite tail: when `h>H(r)`, the `LL` class has left the top window;
an `LL` offset cannot collide with an `LR` or `RR` offset; `b-a=h` is
impossible; and `Q>M`, so `Q` cannot equal a retained same-leg difference.
All remaining comparisons are independent of `h` (or have `h` on both sides).

Across `r=-15,...,20`, this finite partition contains 1,956 `(r,h)` regimes.
The incremental prover closes all of them with the frozen aggregate

```text
nodes=2,402,716, frontier=0,
deepest missing offset=46, max marks=12,
per-regime SHA-256 = b445823ef3fc6541f4e7e260260376fdf4a76f0c0d54d577e56b39619458add8.
```

The immutable clean-room implementation reconstructs every retained collision
set from scratch and uses a separate child generator.  It agrees on the full
1,956-regime table, not only on the aggregate.  Run

```text
nice -n 10 python3 theory-lab/catspider/verify_bispider_strip.py --full-cleanroom
```

for the full comparison; the default invocation reruns the complete primary
table and a boundary/midpoint/tail clean-room sample.  The verifier refuses
`python -O` so that no proof-critical check can disappear.  The frozen summary
is `theory-lab/catspider/results/bispider_strip_certificate.json`.  As a guard
on the tail reduction, it also checks the next admissible tail value in both
implementations for every one of the 36 values of `r`.

Theorems A--C have disjoint `r` ranges.  Therefore they give the simpler
combined consequence:

> **OBSERVED corollary.** No `LR`-anchored Leech bi-spider with `A>50` exists.

## 5. Small-`A`, positive-imbalance LR region

The condition `A>20` in theorem A excludes centres and spine marks from the
top window.  When `A` is small those vertices must be retained explicitly,
but they still have a finite deficit description.

> **OBSERVED theorem D.** No `LR`-anchored Leech bi-spider satisfies
> `1<=A<=50`, `B>20` and `r=Q-(B-A)>20`.

Take `W=20`.  Since

```text
h = N-2A = r+2(B-A) > W,
```

different-left-leg pairs are below the top window.  Different-right-leg
pairs have deficit `r+b+b'>W`; a same-right-leg or right-centre/right-leg
distance has deficit at least `C=A+Q=B+r>W`; and every pair wholly inside the
left/spine branch has deficit at least `B>W`.

Thus every realiser of `N-k`, `k<=W`, joins a right mark `B-b` to exactly one
of the following:

```text
left mark A-a:            p=a,
left centre cL:           p=A,
spine mark at coordinate s: p=A+s.
```

In all three cases `k=p+b`.  Only deficits `p,b<=W` can be newly required.
The finite relaxation keeps global uniqueness of all sums `p+b`; every
bounded distance inside the left/spine branch and on a single right leg; and
all different-right-leg offset sums.  It omits the exact values of `B,Q,r`,
all parameter-dependent cross-class collisions and the vertex budget, so it
is a supertree of every exact continuation in the theorem region.

The incremental and immutable full-recomputation implementations agree on
the complete table for `A=1,...,50`:

```text
W=20, regimes=50, nodes=87,885, accepted=87,835,
dead=53,581, deepest missing offset=20,
max selected vertices (including cL)=11, frontier=0,
per-A SHA-256 = baf3929973241ec3b1a24673083d1d9fd6cb998f51c7e4b8fbccc22bfa62d87e.
```

Reproduce with

```text
nice -n 10 python3 theory-lab/catspider/verify_bispider_smalla_positive.py
```

The frozen summary is
`theory-lab/catspider/results/bispider_smalla_positive_certificate.json`.
Combining theorem D for `A<=20` with theorem A for `A>20` gives the cleaner
consequence:

> **OBSERVED corollary.** If `r>20`, every surviving `LR` anchor has `B<=20`
> (and hence `A<20`).

## 6. Small-`B`, positive-imbalance LR region

The final positive-imbalance boundary is finite after separating a short
spine base from a stable long-spine tail.

> **OBSERVED theorem E.** No `LR`-anchored Leech bi-spider satisfies
> `B<=20` and `r=Q-(B-A)>20`.

Here `1<=A<B<=20`.  Again set `W=20`, and write leg marks as `A-a`
and `B-b`.  Different-left-leg and different-right-leg distances have
deficits at least `h=r+2(B-A)>W` and `r>W`, respectively.  Every top-window
realiser is therefore one of four types:

```text
left leg -- right leg:       k = a+b,
left leg -- right spine:     k = B+a+t,
left spine -- right leg:     k = A+s+b,
left spine -- right spine:   k = A+B+s+t.
```

Here `s` is distance from `cL` and `t` is distance from `cR`; the centres are
included by `s=0` or `t=0`.  Hence only spine marks with `s<=W-A` or
`t<=W-B` can occur.  The finite search retains all pair distances among every
selected vertex in those boundary zones.  It omits all other vertices and the
vertex budget, so every exact continuation maps into the searched relaxation.

For fixed `A,B`, every admissible `Q` from `21+B-A` through 80 is checked
individually.  The single regime `Q=81` represents the infinite tail.  Indeed,
when `Q>80`, every distance internal to one boundary cluster is at most 40,
whereas every cross-cluster distance exceeds 40 and has the form `Q+c`.
Internal/cross collisions are impossible and cross/cross equality depends
only on `c`, so the collision pattern is independent of `Q`.

The mutable incremental and immutable full-distance implementations agree on
the complete 10,260-regime table:

```text
W=20, nodes=564,478, accepted=554,218, dead=323,655,
deepest missing offset=16, max selected vertices=9,
frontier=0,
per-regime SHA-256 = 621e3766337525fb13ecd4f2f20f490c501d1aa7b6fa18ac0d11e516cbdd16b7.
```

Reproduce with

```text
nice -n 10 python3 theory-lab/catspider/verify_bispider_smallb_positive.py
```

The frozen summary is
`theory-lab/catspider/results/bispider_smallb_positive_certificate.json`.
Together with theorems A and D this closes the entire positive tail:

> **OBSERVED corollary.** No `LR`-anchored Leech bi-spider has `r>20`.

## 7. Small-`A`, negative-imbalance LR region

The left-depth hypothesis in theorem B can likewise be removed by retaining
the centre and short-spine possibilities explicitly.

> **OBSERVED theorem F.** No `LR`-anchored Leech bi-spider satisfies
> `1<=A<=15` and `r=Q-(B-A)<-15`.

Put `C=A+Q` and `d=B-C=-r>15`, and set `W=15`.  A pair not incident with the
distinguished `B`-leg has distance at most `2C`, whereas

```text
N-W = B+C-W > 2C.
```

Thus a realiser of `N-k`, `k<=W`, has one endpoint `B-x` near the distinguished
tip.  If the other endpoint lies on a different branch at `cR`, write its
depth as `C-p`; the offset is `k=x+p`.  The possible `p` values come from a
left mark (`p=a`), a spine point (`p=A+s`), another right leg, or `cR` itself
(`p=C`).  A second possibility exists only when `C<=W`: a mark of depth `y`
near `cR` on the distinguished leg gives `k=C+x+y`.

The relaxation requires global uniqueness of all such tip-incident offsets.
Separately, it requires uniqueness of every actual distance internal to the
complementary cluster and every difference inside the tip cluster.  It omits
parameter-dependent collisions between those two classes, all other vertices
and the vertex budget, so it contains every exact continuation.

The dominance gap no longer appears in either retained class; `B=C+16`
therefore represents every `B-C>15`.  For each `A=1,...,15`, all `C=A+1,...,45`
are checked individually.  When `C>45`, coefficient-zero internal distances
are at most 30, coefficient-one distances are at least `C-15>30`, and the
coefficient-two class is separated as well.  Tip offsets split similarly into
values at most 30 and values at least `C`.  Hence `C=46` represents the entire
stable tail.

The incremental and immutable full-recomputation implementations agree on all
570 regimes:

```text
W=15, nodes=78,835, accepted=78,280, dead=43,776,
invalid initial regimes=15, deepest missing offset=15,
max selected vertices=11, frontier=0,
per-regime SHA-256 = eed4b9ab8075fa09499a472c281d563629b4eb6c76fdf8c6f7dc48ca498f0308.
```

Reproduce with

```text
nice -n 10 python3 theory-lab/catspider/verify_bispider_smalla_negative.py
```

The frozen summary is
`theory-lab/catspider/results/bispider_smalla_negative_certificate.json`.
Together with theorem B:

> **OBSERVED corollary.** No `LR`-anchored Leech bi-spider has `r<-15`.

## 8. Exact anchor coverage and large-order probe

`bispider_region_coverage.py` counts initially legal `LR` anchors and applies
only the six proved inequalities:

| order | legal LR anchors | theorem A | theorem B | theorem C | new D | theorem E | theorem F | union |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 18 | 5,625 | 1,013 | 1,359 | 377 | 920 | 190 | 885 | 84.3% |
| 25 | 21,905 | 6,963 | 7,945 | 1,592 | 2,380 | 190 | 1,995 | 96.2% |
| 27 | 30,276 | 10,368 | 11,408 | 2,150 | 2,900 | 190 | 2,370 | 97.1% |
| 36 | 97,969 | 40,045 | 42,348 | 4,396 | 5,680 | 190 | 4,470 | 99.1% |
| 51 | 404,496 | 183,618 | 187,892 | 10,466 | 12,140 | 190 | 9,300 | 99.8% |

Corroboration not used in any uniform proof: a four-shard `--fast` probe at order 25
reproduced the archived 32,882 anchors and 29,155,730 nodes, with zero solutions.
The deepest missing offsets were 34 in `LR` and 33 in `LL`, and no state fixed
more than 12 non-centre marks.  `--fast` disables the full diagnostic distance
recomputation and is explicitly not a certificate mode; the archived order-25
runs retain the paranoid check at every node.  Restricted to `A<=50`, exact
numeric probes close 12,275 order-25 anchors in 11,790,276 states (deepest 34)
and 14,875 order-27 anchors in 15,716,380 states (deepest 32), with at most 11
marks.  Summary: `theory-lab/catspider/results/bispider_smalla_calibration.json`.
For the theorem-E strip, paranoid exact runs at orders 13, 25 and 27 have the
same stable total of 10,866 states over 190 anchors, deepest offset 16 and at
most seven non-centre marks.  At orders 12 and 25, all 380 individual anchors
also match the symbolic prover in node count, deepest offset, selected-mark
maximum and zero-solution verdict.  Summary:
`theory-lab/catspider/results/bispider_smallb_calibration.json`.
For theorem F, paranoid order-25 and order-27 runs close 1,995 and 2,370
anchors in 465,945 and 570,497 states, respectively, with deepest offset 15.
At order 25, 1,875 symbolic regimes match all exact statistics, 120 are strict
relaxations as intended, and 15 parameter cases fail at the fixed anchor.
Summary: `theory-lab/catspider/results/bispider_smalla_negative_calibration.json`.

## 9. Large-`h` middle tail and the target-order LR corollary

The remaining boundary after theorems A--F was

```text
-15 <= r <= 20,     1 <= A <= 50.
```

Put `D=B-A`, so that

```text
r = Q-D,             h = Q+D = N-2A,
Q = (h+r)/2,          B = A+(h-r)/2,
C = A+Q = A+(h+r)/2.
```

Fix `W=35` and

```text
H(A,r) = max(W, 2(W-A)+abs(r)).
```

> **OBSERVED theorem G.** No `LR`-anchored Leech bi-spider satisfies
> `1<=A<=50`, `-15<=r<=20`, and `h>H(A,r)`.

Here is the reduction checked by the verifier.  Write a left-leg vertex as
depth `A-a`, a right-leg vertex as depth `B-b`, and a spine vertex at distance
`s` from the left centre as `p=A+s`; the left centre itself has `p=A`.
If `h>H(A,r)`, then

```text
h > W,       B = A+(h-r)/2 > W,       C = A+(h+r)/2 > W.
```

These inequalities remove every left-left, left-spine, spine-spine,
right-same-leg and centre-boundary distance from the top window.  Every
remaining distance `N-k`, `0<=k<=W`, therefore has exactly one of the forms

```text
k = p+b,                 (left/right or spine/right),
k = r+b+b',              (two different right legs).
```

For the second form it is enough to retain `0<=b<=W-min(r,0)`; for the first,
`0<=p,b<=W`.  The relaxation also retains the necessary uniqueness of all high
offsets and of the parameter-free internal collision classes

```text
abs(a-a'),  2A-a-a',  abs(p-p'),  p-a,  abs(b-b'),  b+b'.
```

It deliberately omits collisions between those classes, vertices which never
meet the top window, and the vertex budget.  Hence it is a super-search: an
actual Leech extension would still define a path through it.  At each first
missing offset the search enumerates every one- or two-endpoint realisation of
the two displayed forms.

`verify_bispider_middle_tail.py` compares an incremental collision-set prover
with an immutable full-recomputation implementation on every one of the
`50*36=1,800` pairs `(A,r)`.  They agree per regime: 1,386,587 states,
1,384,787 accepted children, 810,109 dead states, deepest missing offset 34,
at most 12 selected vertices, and zero frontier.  The frozen table SHA-256 is
`0cf2bb93dea516b883d1756492c3253b947b5bbe3555df498dacda2c7ca3f997`.
Certificate: `theory-lab/catspider/results/bispider_middle_tail_certificate.json`.

The bridge to the requested orders is purely arithmetic.  If `n>=18`, then
`N=n(n-1)/2>=153`, and for every `1<=A<=50`, `-15<=r<=20`,

```text
h = N-2A >= 153-2A > 35,
h >= 153-2A > 2(35-A)+abs(r),       since abs(r)<=20<83.
```

Thus every remaining middle-boundary anchor at order at least 18 is already in
the stable tail.  Combining theorem G with theorems A--F gives:

> **OBSERVED corollary.** No `LR`-anchored Leech bi-spider of order `n>=18`
> exists.

## 10. Complete LL classification at the target orders

For an `LL` anchor write its two tip depths as `T>U`, so

```text
N = T+U,       delta = T-U,       1 <= Q < U,       L = U-Q.
```

Every other left tip has depth below `U`; every right tip has depth below
`L`, since otherwise the long anchor tip and that right tip would give a
distance at least `N`.  A non-long vertex has radial distance `U-z` from the
left centre.  Its bounded deficit `z` determines its role:

```text
short left leg:  0 <= z < U,
right leg:       0 < z < L,
right centre:    z = L,
spine:           L < z < U.
```

Different vertices cannot share `z`, because their distances `U-z` from the
left centre would coincide.  On the long anchor leg, write a near-tip vertex
as `T-a` and, when needed, a near-centre vertex by its depth `x`.

Fix `W=36`.  Since `n>=18`, `N>=153`.  The following three cases are disjoint
and exhaustive.

### 10.1 Small second tip: `2<=U<=W`

Here

```text
delta = N-2U >= 153-72 = 81 > W.
```

Thus no pair avoiding the long leg reaches the top window.  A long-leg
same-path pair can reach it because the second anchor tip is short.  The full
list of high offsets is

```text
k = a+z,                 (long near-tip / another cL branch),
k = U+a+x.               (the two ends of the long anchor leg).
```

The two long-leg clusters are disjoint: `T-a >= N-U-W > W-U >= x`.
The exact parameter table is `2<=U<=36`, `1<=L<U`, or 630 regimes.

### 10.2 Large second tip, near far-centre: `U>W`, `1<=L<=W`

Same-long-leg distances now miss the window.  Besides `a+z`, two vertices on
different branches at the left centre can give

```text
k = delta+z+z'.
```

Use exact `delta=1,...,36` and sentinel `delta=37` for every `delta>36`.
Two different right legs would have offset

```text
rho+c+c',       rho = delta+2Q = N-2L >= 153-72 = 81,
```

so that class is outside the window in this case.  Exact `L=1,...,36` gives
`37*36=1,332` regimes.

### 10.3 Large second tip, remote far-centre: `U>W`, `L>W`

The right centre and all spine points leave the window, but a right-leg mark
with deficit `c<=W` can remain.  The exhaustive high forms are

```text
k = a+z,
k = delta+z+z'           on different cL branches,
k = rho+c+c'             on different right legs,
rho = delta+2Q = N-2L.
```

The finite table uses exact values through 36 and sentinel 37 for each large
tail.  When both parameters are exact,
`Q=(rho-delta)/2` is integral and at least one.  Therefore the admissible
finite pairs are `rho=delta+2,delta+4,...,36`, plus one `rho>36` sentinel for
each `delta<=36`, and the joint `(delta,rho)=(37,37)` tail: 343 regimes.

### 10.4 Relaxation and exhaustive search

All three searches retain global uniqueness of the displayed high offsets,
same-leg differences, and different-branch deficit sums.  The near-centre
case retains the exact internal spine/right distances.  The remote case also
retains right-leg sum uniqueness; for finite `rho` it uses the known `Q` and
checks all endpoint-to-centre affine offsets.  The small-`U` case retains the
two long-leg clusters and all exact far-branch internal distances.

Collisions between unrelated classes, vertices which never meet the top
window, and the vertex budget are omitted.  These omissions only enlarge the
state space.  If an actual Leech extension existed, take its first missing
offset `k<=W`; the classification above supplies one of the enumerated
one- or two-endpoint additions, so the actual extension maps inductively to a
search path.  Zero frontier therefore excludes every actual anchor in the
covered region.

`verify_bispider_ll.py` compares a canonical-state prover with three immutable
clean-room searches on every regime.  No implementation imports search code
from the other.  The per-regime tables agree exactly:

| region | regimes | states | children | dead | max depth | max selected | frontier | SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `U>36,L<=36` | 1,332 | 433,069 | 431,737 | 253,306 | 28 | 12 | 0 | `94cd15d9...c3f3` |
| `U>36,L>36` | 343 | 89,723 | 89,380 | 52,129 | 36 | 12 | 0 | `db87ce98...b584` |
| `2<=U<=36` | 630 | 217,802 | 217,172 | 131,397 | 20 | 11 | 0 | `9d94098e...d28b` |

The verifier additionally maps every 624,389 actual LL anchors at orders
18 through 40 into exactly one finite regime.  As independent numeric
calibration, the paranoid C engine closes all 2,825 order-18 LL anchors in
723,912 states, deepest offset 33, at most 11 non-centre marks, and zero
solutions.  Frozen details and full hashes:
`theory-lab/catspider/results/bispider_ll_certificate.json`.

> **OBSERVED theorem H.** No `LL`-anchored Leech bi-spider of order `n>=18`
> exists.

Combining theorem H with the LR corollary gives the target structural result:

> **OBSERVED bi-spider theorem.** No Leech tree of order `n>=18` has at most
> two vertices of degree at least three.

## 11. What remains

- **OBSERVED:** all `LR` and `LL` anchors are excluded for `n>=18`; hence any
  hypothetical target-order Leech tree has at least three branch vertices.
- **UNVERIFIED:** the stronger conjecture that the order-six double star is the
  only Leech bi-spider, equivalently no bi-spider exists for every `n>=7`.
- **UNVERIFIED:** the global project still must exclude trees with at least
  three branch vertices, beginning with the planned three-branch and
  hop-diameter-at-most-four cases before a general descent theorem.

No SAT witness arises in these nonexistence certificates.  Any future
positive output must continue to pass both repository witness checkers.
