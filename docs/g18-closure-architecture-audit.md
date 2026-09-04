# G18 closure-architecture audit (FW279)

FW279 records the decision reached after stress-testing the proposed
pendant/nonpendant/small-`Q` closure architecture.  The decision is negative
for the architecture, not for the mathematical problem:

* **OBSERVED exact:** the canonical pendant deletion has a decreasing
  owner-value forest.  Arbitrary-owner descent is equivalent to injectivity
  of its transformed path sums and placement of all forest sources in one
  prescribed top band.  A second exact, multiscale identity expresses the
  remaining source displacement as threshold transport minus threshold
  coalescence.
* **OBSERVED exact:** an arbitrary nonpendant unit cut has a strict-cap
  outside-hole cardinality and sum certificate.  It retains all cut sizes,
  rooted edge cuts and actual owners; it does not reduce to the
  special `2|b` wrapper.
* **OBSERVED exact, restricted:** in the order-eighteen, q=1, pure-`H`
  `2|15` wrapper, the true holes split into a terminal suffix, three named
  root holes and a residual set.  Gate packing excludes only
  `Q=10,11,12,13,14`; `Q=9` already retains weak boundary states.
* **UNVERIFIED:** neither rank anti-coalescence nor the required multiscale
  transport inequality is known on the pendant side.  No general
  rooted-realisation stability theorem excludes the arbitrary nonpendant
  certificate.  The restricted `2|15` calculation does not bridge that gap.

Consequently the current A/B/C architecture is **not closed**.  FW279 proves
no new order exclusion: G18 and the all-order nonexistence statement both
remain **UNVERIFIED**.  The pressure trees and formal states below locate
missing hypotheses; none is a Leech counterexample, a full-state
countermodel, a SAT witness or a proof certificate.

## 1. Scope and logical coverage

Let `T` be a hypothetical Leech tree of order `n`, with

```text
N=binom(n,2),                 Spec(T)=I_N={1,...,N}.
```

Its unique weight-one edge is either pendant or nonpendant.  The architecture
under audit was:

1. **A, pendant:** use the canonical q=1 distinguished endpoint and delete it
   together with the unit leaf; rank-compress the common core to order `n-2`.
2. **B, nonpendant:** use the strict near-perfect cap to exclude a nonpendant
   unit cut.
3. **C, small `Q`:** close the finite residual q=1 rows if A or B leaves only
   a bounded endpoint parameter.

The correct load-bearing versions are stronger than the original informal
interfaces.  A must prove a canonical *arbitrary-owner* rank descent, not
pathwise preservation of the old owners.  B must handle every nonpendant
`s|t` cut, not only a pure-`H` `2|b` tail.  Sections 2--5 give the exact A
reduction; Sections 6--8 give the general B certificate and its stops;
Section 9 records what the restricted C calculation really excludes.

## 2. Canonical distinguished-endpoint deletion

Retain the pendant unit edge

```text
a --1-- b
```

and, within the canonical FW218 q=1 orientation, let the distinguished
diameter endpoint `x` (the endpoint with first hole `Q`) be a leaf distinct
from `a`.  Write

```text
x --e-- r,              U=T-{a,x},
m=|U|=n-2,              C=binom(m,2),
B=D_b(U),               R=D_r(U),
h=d_U(b,r),             L=1+h+e.
```

The external owner values are the coefficientwise disjoint set

```text
H=(1+B) dot-union (e+R) dot-union {L}.             (FW279.1)
```

Let `Q` be the q=1 first-hole parameter and put

```text
D_0=N-Q=C+G,                 G=2m+1-Q,
H_0=H intersect [1,D_0].                              (FW279.2)
```

The canonical top owners give

```text
H intersect [D_0+1,N]=[D_0+1,N],
Spec(U)=[1,D_0]-H_0,              |H_0|=G.          (FW279.3)
```

These are owner-labelled identities.  In particular the `Q` top external
owners are not being counted a second time in `H_0`.

Define the external-hole rank map

```text
q(t)=|H intersect [1,t]|,             phi(t)=t-q(t). (FW279.4)
```

Every edge of `U` has weight at least two, because the only distance one in
`T` is the deleted edge `a--b`; also `1 in H`.  If an internal value
`d in Spec(U)` has `U`-path `P_d`, define its transformed path value by

```text
F(d)=sum_(w edge of P_d) phi(w).                    (FW279.5)
```

Since an edge weight of `U` is itself internal and hence is not in `H`, each
transformed edge is positive.  The occurrence of `1 in H` makes every one
strictly smaller.  Therefore

```text
1<=F(d)<d                   for every d in Spec(U). (FW279.6)
```

This strict decrease is unconditional in the displayed canonical
state; it does not assert that two different paths have different `F`-values.

## 3. The exact source forest and arbitrary-owner descent

Place a directed arrow

```text
d -> F(d)                   for d in Spec(U)         (FW279.7)
```

on the numeric vertices `[1,D_0]`.  Vertices in `Spec(U)` have outdegree one
and the holes `H_0` have outdegree zero.  By (FW279.6), every arrow points to
a smaller integer, so every directed walk terminates in `H_0`.

Assume first the missing **rank anti-coalescence** statement:

```text
F is injective on Spec(U).                          (FW279.8)
```

Then the directed components are `G` disjoint chains.  Let `Z` be their
source set, equivalently the values of `[1,D_0]` not hit by `F`.  Exact
cardinality and prefix transport give

```text
|Z|=G,
|Z intersect [1,t]| <= |H_0 intersect [1,t]|
                                      for every t.  (FW279.9)
```

Indeed, pairing each chain source with its terminal hole gives a terminal
not exceeding its source, which proves the prefix inequality.  Thus holes
can move only to the right along these chains.  The pairwise
distance set of the edge-reweighted core `U_phi` is exactly

```text
Spec(U_phi)=F(Spec(U))=[1,D_0]-Z.                  (FW279.10)
```

No old owner needs to retain its old compressed rank.  Consequently the
right arbitrary-owner criterion is

> **OBSERVED exact any-owner descent criterion.**  The edge-reweighted core
> `U_phi` is a Leech tree of order `m=n-2` if and only if `F` is injective
> and
>
> ```text
> Z=[C+1,D_0].                                     (FW279.11)
> ```

Indeed, (FW279.11) is equivalent to `Spec(U_phi)=I_C`.  This strictly weakens
the owner-preserving path-additivity test in FW278: transformed owners may
permute freely.

Under injectivity define the source displacement

```text
Delta=sum_(d in Spec(U))F(d)-C(C+1)/2
     =sum_(z=C+1 to D_0)z-sum_(z in Z)z.           (FW279.12)
```

The prefix dominance in (FW279.9) gives `Delta>=0`, and equality holds
exactly when (FW279.11) holds.  Thus pendant closure has two logically
independent obligations:

1. prove rank anti-coalescence (FW279.8);
2. after injectivity, prove `Delta=0`.

Neither obligation is supplied by the five named rows or by the six local
projection-fibre gaps of FW278.

## 4. Multiscale threshold identity

There is an exact expansion of the second obligation.  Fix `h in H_0`.
No `U` edge has weight `h`, because `h` is an external hole.  Delete from
`U` every edge of weight greater than `h` (equivalently, at least `h` among
the edge weights).  For a `U`-path `P`, put

```text
k_h(P)=#{w edge of P:w>h},
A_h=#{P:k_h(P)=0 and d_U(P)>h},
B_h=sum_P max(0,k_h(P)-1).                         (FW279.13)
```

All paths and sums in (FW279.13) range over the `C` paths between distinct
unordered pairs of vertices of `U`.

Here `A_h` counts paths contained in one threshold component whose additive
length nevertheless crosses `h`.  The term `B_h` counts repeated crossings
of distinct above-threshold edges on a path: it is the exact Kruskal
coalescence correction, not a cut-product surrogate.

Summing the contribution of every hole threshold gives

```text
Delta=sum_(h in H_0)(A_h-B_h).                    (FW279.14)
```

For one path and one hole, the contribution is `+1` when it has no heavy
edge but total length exceeds `h`, zero when it has exactly one heavy edge,
and `-(k_h(P)-1)` when it has at least two.  This proves (FW279.14) by
double counting and explains why a single-scale cut inequality cannot
replace it.

Under rank anti-coalescence, `Delta>=0`; descent would follow from the new
multiscale transport inequality

```text
sum_(h in H_0) A_h <= sum_(h in H_0) B_h.          (FW279.15)
```

No such inequality is proved.  It is independent of anti-coalescence:
(FW279.15) controls the total displacement only after collisions of distinct
transformed paths have already been ruled out.

The known order-six Leech tree `L6`, oriented at its canonical pendant unit
leaf and distinguished endpoint, is the sharp positive control.  It has

```text
H_0={1,3,6,8,10}

h       A_h       B_h       A_h-B_h
1         0         4          -4
3         0         2          -2
6         3         0           3
8         2         0           2
10        1         0           1
```

The differences sum to zero, but their signs reverse across thresholds.
Thus even the positive base case needs genuinely multiscale cancellation;
neither `A_h<=B_h` nor the reverse holds threshold by threshold.

## 5. Two-root windows and pendant pressure controls

The exact two-root form of `q` is

```text
q(t)=|B intersect [0,t-1]|+|R intersect [0,t-e]|
     +1_(L<=t).                                    (FW279.16)
```

For a concatenation of positive lengths `s,w`, its rank-additivity defect is

```text
eta(s,w)=q(s+w)-q(s)-q(w)

 = |B intersect [s,s+w-1]|-|B intersect [0,w-1]|
 + |R intersect [s-e+1,s+w-e]|-|R intersect [0,w-e]|
 + 1_(s<L<=s+w)-1_(L<=w).                         (FW279.17)
```

Equivalently
`phi(s+w)-phi(s)-phi(w)=-eta(s,w)`.  Formula (FW279.17) is an exact
owner-window ledger, but the unmatched owner in a translated window need not
project to the fibre of the path producing that window.  The q=1 top suffix
therefore does not by itself prove either rank anti-coalescence or
(FW279.15).

Two hand-checkable pressure trees delimit this claim.

### 5.1 Named-top rank-additivity pressure

Take the six-vertex weighted tree

```text
a--b:1,  b--p:12,  p--c:6,  c--x:17,  c--y:15.
```

Its fifteen distances are all distinct.  Deleting `x` leaves diameter 34,
while the two named top values in the `x`-row are `{35,36}`.  Deleting
`a,x` gives

```text
H={1,13,17,19,23,32,34,35,36},
Spec(U)={6,12,15,18,21,33},
q(18)=3 > q(12)+q(6)=2.                            (FW279.18)
```

Thus named top ownership and the two-root rows do not force even the stronger
owner-preserving additivity.  This tree is **not Leech**: its spectrum is not
`I_15`.  It is a metric pressure control only, not a counterexample to a
theorem using the full interval.

### 5.2 One-even-coefficient pressure

Take instead

```text
a--b:1,  b--p:8,  p--c:3,  c--y:2,  c--x:4.
```

Its distance spectrum is

```text
[1,9] union [11,16].                               (FW279.19)
```

The odd sheet is exact; the even sheet replaces the required coefficient
ten by the excess coefficient sixteen.  Relative to the artificial cap 16,
this is q=1-shaped with `Q=2`, `tau=1`, first positive edge `3`, singleton
`x`, the FW278 five rows and six fibre gaps.  It is **not** an actual
order-six FW218 q=1 state: here `N=15`, and no single endpoint owns both
values 14 and 15.  The external-`q` all-path additivity test nevertheless
passes.
Nevertheless the actual edge-reweighted core has spectrum

```text
{1,2,3,4,6,7};                                    (FW279.20)
```

it is injective but overflows the order-four target.  Exactly one missing
even coefficient is enough to break source placement.  This is again a
non-Leech pressure control, not a full-state countermodel.  It shows that
full interval coverage is a load-bearing input to any proof of
(FW279.15).

## 6. General nonpendant unit cut

The nonpendant target needed by architecture B is the following
near-perfect statement:

> **UNVERIFIED target B\*.**  Every globally distance-distinct
> positive-integer weighted tree of order `m` with a nonpendant unit edge has
> diameter at least
> `binom(m,2)+m-4`.

Equivalently, put

```text
C_m=binom(m,2),                 D_0=C_m+m-5.       (FW279.21)
```

The strict counterexample state `D<=D_0` must be impossible.  Denote such an
order-`m` state by `S`.  This is the
right quantifier for a q=1 endpoint deletion: when `m=n-1` and `Q>=5`, its
remaining diameter is at most `N-Q<=N-5=D_0`.

Let a nonpendant unit edge `ab` split `S` into rooted
sides `A,B` of orders

```text
s,t>=2,                         s+t=m.
```

Let `X,Y` be the distinct depth sets from `a,b`, both including zero, and
write `X_+=X-{0}`, `Y_+=Y-{0}`.  Pad the missing values through `D_0` by a
hole set `H`.  Actual-owner uniqueness gives

```text
I_[1,D_0]
 = F_A dot-union F_B dot-union (1+X dot+Y) dot-union H,
|H|=m-5.                                             (FW279.22)
```

The rooted sum `X dot+Y` is coefficientwise unique; otherwise two cross
pairs would have the same distance after adding the unit edge.

Remove that unit translation and put

```text
V=X_+ dot+Y_+,                    K=(s-1)(t-1).
```

Every `v in V` has the actual cross successor `v+1`, so
`V subset [1,D_0-1]`.

Let

```text
L={ell in V:ell is occupied by its unique actual unordered-pair owner},
E=|L|.
```

The owner of `ell` may be internal to a side or may itself be a cross pair.
Then

```text
H intersect V=V-L,
H_out=H-V,
kappa=K-m+5=(s-2)(t-2)+2,
|H_out|=E-kappa.                                  (FW279.23)
```

This is the arbitrary-cut generalisation of the `E-2` count in FW278.  The
constant is two only when one side has order two.

Put

```text
S_X=sum X_+,              S_Y=sum Y_+,
W(S)=sum_{unordered pairs {u,v}}d_S(u,v).
```

Since `sum V=(t-1)S_X+(s-1)S_Y`, the outside holes have the exact prescribed
sum

```text
Phi=sum H_out
   =D_0(D_0+1)/2-W(S)-(t-1)S_X-(s-1)S_Y
     +sum_(ell in L)ell.                           (FW279.24)
```

In particular `H_out` must be an `(E-kappa)`-element subset, of sum `Phi`,
of the relaxed candidate universe

```text
U_0=[1,D_0]\(V union (1+X+Y) union X_+ union Y_+). (FW279.25)
```

The universe is deliberately a relaxation: other already-owned internal
values may shrink it further.  Thus failure of its subset-sum condition is
a valid rejection, while success is not a rooted-tree realisation.

There are two exact cut expansions.  For every `ell=x+y in L`, select its
unique actual owner path and compare it with the two rooted source
paths of total length `x+y`.  For an edge `f`, let `c_f` count selected owner
paths crossing `f`, and let `l_f` count selected source paths crossing it.
Then

```text
sum_f w_f(c_f-l_f)=0.                              (FW279.26)
```

Alternatively let `k_f` be either full-`S` cut order, and for an edge in
one rooted side let `r_f` be its descendant order in that side.  Expansion
of `W(S),S_X,S_Y` in (FW279.24) gives

```text
Phi=D_0(D_0+1)/2
    +sum_f w_f(c_f-k_f(m-k_f))
    -(t-1)sum_(f in A)w_f r_f
    -(s-1)sum_(f in B)w_f r_f.                    (FW279.27)
```

The summands in (FW279.26)--(FW279.27) have both signs in actual
distance-distinct trees.  Dropping negative terms is therefore not a sound
monotone potential.

### 6.1 Consecutive runs and the q=1 suffix

Write `R_V` for the number of maximal consecutive runs of the numeric set
`V`, and let `f_V` count run starts that belong to `L`.  If `v-1,v in V`,
the cross pair that owns `1+(v-1)` already owns `v`.  Hence only a run start
can be a hole in `V`, and exactly

```text
E=K-R_V+f_V,
|H intersect V|=R_V-f_V,
|H_out|=m-5-R_V+f_V.                              (FW279.28)
```

Now apply the certificate to the q=1 endpoint deletion, so

```text
m=n-1,              N=binom(n,2),
M=N-Q,              D_0=N-5,              Q>=5.
```

Every element of `V` is at most `M-1`.  Therefore the terminal interval

```text
J=[M+1,D_0],                    |J|=Q-5             (FW279.29)
```

lies in `H_out`.  In particular

```text
E>=kappa+Q-5.                                      (FW279.30)
```

Writing `H_res=H_out-J` gives the residual certificate

```text
|H_res|=E-kappa-Q+5,
sum H_res=Phi-(Q-5)(M+1+D_0)/2,
H_res subset U_0 intersect [1,M].                 (FW279.31)
```

Taylor parity is an additional exact equation, not a replacement for owner
placement.  Root the whole state and let

```text
gamma=#even-depth vertices-#odd-depth vertices.
```

Then

```text
sum_(h in H)(-1)^h
 =sum_(j=1 to D_0)(-1)^j-(gamma^2-m)/2.           (FW279.32)
```

After (FW279.28)--(FW279.29), this fixes the signed parity sum of `H_res`
exactly:

```text
sum_(h in H_res)(-1)^h
 =sum_(j=1 to D_0)(-1)^j-(gamma^2-m)/2
  -sum_(v in V-L)(-1)^v-sum_(j=M+1 to D_0)(-1)^j. (FW279.33)
```

Equations (FW279.22)--(FW279.33) are necessary for every strict
counterexample and retain arbitrary `s|t`.  They do not prove target B\*.

## 7. General-cut pressure and formal boundary states

The next four controls separate the strict cap from the local owner algebra.

### 7.1 An actual `4|5` equality control

On vertices `0,...,8`, take the edges

```text
01:1, 23:2, 45:3, 06:4, 47:6, 26:8, 08:16, 14:18.
```

This is an **OBSERVED hand-checkable**, globally distance-distinct tree.  At
the unit cut its two rooted depth sets are

```text
X={0,4,12,14,16},              Y={0,18,21,24}.
```

It has diameter 41 and holes

```text
{7,11,27,32,40}                                    (FW279.34)
```

inside `[1,41]`.  Its general-cut data are

```text
V={22,25,28,30,32,33,34,35,36,37,38,40},
E=10,                 kappa=8,
V-L={32,40},
R_V=6,                f_V=4.                       (FW279.35)
```

For edge weights `1,2,3,4,6,8,16,18`, the signed values `c_f-l_f` are

```text
8, 1, 0, -2, -1, 1, 2, -2,
```

whose weighted sum is zero as required by (FW279.26).

Here `m=9`, so the strict cap is `D_0=40`.  Truncating this equality control
by its single excess coefficient gives the relaxed candidate set

```text
U_0={2,3,6,7,8,9,10,11,20,27},
|H_out|=2,                       Phi=4.             (FW279.36)
```

No two-element subset of `U_0` sums to four.  Thus the exact coefficient 41
is load-bearing: the actual `D_0+1` control is rejected as soon as the strict
cap is imposed.  It is not an actual strict survivor and not a counterexample
to target B\*.

### 7.2 An actual `3|6` non-strict pressure tree

Take instead

```text
01:1, 23:2, 45:3, 06:4, 47:6, 12:10, 68:16, 46:19.
```

Its rooted sets at the unit cut are

```text
X={0,4,20,23,26,29},              Y={0,10,12}.
```

The 36 distances are distinct, the diameter is 42, and its holes in
`[1,42]` are

```text
{7,8,14,18,28,32}.                                  (FW279.37)
```

For weights `1,2,3,4,6,10,16,19`, the signed flow is

```text
4, -1, 0, -4, 0, -5, 4, 0,
```

again with weighted sum zero.  Relative to the strict `D_0=40` formula,
the two overflow values 41 and 42 produce `Phi=-22`.  This is a non-strict
metric pressure tree showing that local signed flow alone has no cap
monotonicity; it is not a strict state.

### 7.3 A smaller cap-blind run pressure

The seven-vertex tree

```text
01:1, 02:5, 23:3, 14:10, 45:2, 16:14
```

is an actual globally distance-distinct `3|4` tree, with spectrum

```text
{1,2,3,5,6,8,9,10,11,12,13,14,15,16,18,19,20,21,23,24,26}.
```

Its predecessor set

```text
V={15,17,18,19,20,22}
```

has only three consecutive runs, fewer than `m-3=4`.  Thus actual rooted
geometry alone does not force the tempting run lower bound
`R_V>=m-3`.  Its diameter is 26, above the strict cap `D_0=23`; this is a
cap-blind pressure control, not a strict survivor.

### 7.4 Two exact formal `I_36` survivors

At `m=9,n=10,Q=9`, put `M=36,D_0=40`.  The following two formal `3|6`
tilings both have

```text
H={37,38,39,40},       K=10,       kappa=6,       E=10,
H_out=H,               Phi=154.                    (FW279.38)
```

They pass the exact partition, subset-sum, run, suffix and Taylor tests of
Section 6.

The first is

```text
X={0,2,6},             F_A={2,4,6},
Y={0,9,14,19,24,29},
F_B={5,8,9,11,13,14,18,19,23,24,28,29,33,34,35},
1+X+Y={1,3,7,10,12,15,16,17,20,21,22,25,26,27,
       30,31,32,36}.                                (FW279.39)
```

It is not a rooted tree: for the vertices at depths 9 and 29, the first
rooted pivot allows only mutual distance 20 or 38, and neither belongs to
the permitted nonroot row `F_B`.

The second is

```text
X={0,17,20},          F_A={3,17,20},
Y={0,4,6,8,10,15},
F_B={2,4,6,8,10,12,13,14,15,19,23,30,32,34,35},
1+X+Y={1,5,7,9,11,16,18,21,22,24,25,26,27,28,29,
       31,33,36}.                                   (FW279.40)
```

It passes the first pivot.  That pivot forces depth four to be a root child,
depth six below it by an edge of weight two, and depths `8,10,15` outside
that branch.  The second pivot then gives

```text
d(6,8)=14=d(4,10),                                  (FW279.41)
```

a forbidden duplicate.  Both states are exact integer-spectrum
relaxations, not actual weighted trees and not strict counterexamples.  They
show that the general coefficient ledger reaches the rooted-realisation
boundary at the first or second pivot; it does not reduce that boundary to
the `2|b` wrapper.

## 8. Rooted-realisation stability stop

There is an exact complete test, but it retains quadratic owner context.
For a proposed rooted side with distinct depths `rho(u)` and proposed pair
distance `d(u,v)`, define

```text
lambda(u,v)=(rho(u)+rho(v)-d(u,v))/2.              (FW279.42)
```

It is rooted-tree-realised if and only if every `lambda(u,v)` is a
nonnegative integer equal to the depth of an existing unique vertex, the
relation

```text
u <= v  iff  lambda(u,v)=rho(u)                    (FW279.43)
```

has a chain of ancestors below every vertex, and the vertex at depth
`lambda(u,v)` is the deepest common ancestor of `u,v`.  The parent of a
nonroot vertex is then its greatest proper ancestor, and the edge weight is
the positive difference of their depths.  Thus (FW279.42)--(FW279.43)
reconstruct the rooted weighted tree uniquely.

This exact state has `Theta(k^2)` pair placements on a side of order `k`.
It does not collapse under a shallow pivot.  If a root-child edge of weight
`p` separates descendant factor `C` from root-side factor `O`, their rooted
and pair polynomials satisfy

```text
R=R_O+X^p R_C,
F=F_C dot-union F_O dot-union X^p R_C R_O.         (FW279.44)
```

Every pivot regenerates a product row with the full opposite context.  The
global hole set and q=1 terminal suffix are not separately inherited by
`C` or `O`.  A bounded-`k` recursive schema is therefore only
**UNVERIFIED**; no scalar decreasing potential or constant-state parent map
has been proved.

There is an equivalent forest reformulation, but no simplification.  A
strict counterexample with

```text
D=C_m+h,                    0<=h<=m-5
```

has exactly `h` missing coefficients in `[1,D]`.  Adjoining `h` disjoint
weighted copies of `K_2`, one at each missing coefficient, gives a
perfect-distance forest

```text
S dot-union h K_2                                   (FW279.45)
```

with the marked nonpendant unit edge in `S`; deleting those isolated
edges reverses the construction.  The forest spectrum here counts only
within-component pair distances.  This is an **OBSERVED exact equivalence**,
not an exclusion: ordinary perfect-distance forest coverage does not recover
the component, root, owner and marked-unit placement needed for target B\*.

## 9. Restricted order-eighteen pure-`H` `2|15` state

This section has a deliberately narrow quantifier.  Assume an actual
order-eighteen q=1 Leech tree, with distinguished endpoint `x`, and put

```text
S=T-x,              M=N-Q,              N=153.
```

Assume further that the unit edge lies in the pure-`H` wrapper

```text
c --2-- a --1-- r -- B,                 |B|=b=15,
q=d(x,r),                                5<=Q<=14,
D_0=N-5=148.
```

The upper bound `Q<=14` is the inherited FW273/global q=1 bound; this
section makes no claim outside the displayed interval.

Let `Y` be the rooted depth set of `B`, `Y_+=Y-{0}`, and let
`Z=2+Y_+` be the virtual row.  Write `E` for the number of positions of `Z`
filled by actual internal pairs of `B`; let `X` be the candidate set for
true holes outside the named wrapper rows and write `H_X subset X` for the
true hole set.

The q=1 suffix and the three removed-row owners give the **OBSERVED exact**
decomposition

```text
H_X=[M+1,D_0] dot-union {q,q+1,q+3} dot-union H_rem,
|H_rem|=E-Q,                                      (FW279.46)
```

where every member of `H_rem` is an actual `x`-core owner.  In particular

```text
[q,q+3] subset X,                 E>=Q.            (FW279.47)
```

For a filled virtual position, form its actual-owner graph on `B`; root `B`
at `r`.  For each rooted edge `f`, let `w_f` be its weight, `s_f` its
descendant order and `c_f` the number of selected owner edges crossing its
cut.  The residual holes have the exact sum

```text
sum H_rem
 = D_0(D_0+1)/2-6b
   +sum_f w_f(c_f-s_f(b+3-s_f))
   -(Q-5)(M+1+D_0)/2-(3q+4).                      (FW279.48)
```

No unsigned term has been discarded in (FW279.48).

Root the ambient tree `T` at `x`.  Let `H_Q` be the connected q=1 threshold
core, and put

```text
H_B=B intersect H_Q.
```

The strict pure-`H` state gives the load-bearing facts

```text
H_B is connected,       r in H_B,       |H_B|=b-Q=15-Q. (FW279.49)
```

For the visible owners `d(x,v_j)=N-j`, `0<=j<Q`, define

```text
g_j=LCA_x(r,v_j),       d_j=d_B(r,g_j),
t_j=N-q+2d_j-j.                                      (FW279.50)
```

Every `g_j` lies in the `H_B` portion of the `x`--`r` chain; for `j=0` one
may have `g_0=r,d_0=0`.  Reflection along that chain gives
`t_j=d_B(r,v_j)`, so `t_j in Y`.  The rooted row `Y` avoids differences one,
two and three.  Hence indices assigned to one gate satisfy

```text
g_i=g_j  =>  |i-j|=|t_i-t_j|>=4.                  (FW279.51)
```

There is also an actual-owner rule between distinct gates.  If two distinct
ordered gates both realised the same positive index difference `d`, say on
`(i,i+d)` and `(j,j+d)`, then the cross pairs

```text
{v_i,v_(j+d)}  and  {v_(i+d),v_j}
```

would have the same LCA at whichever of those gates is closer to `x` and the
same distance

```text
2(N-q)+2d_high-i-j-d,
```

where `d_high` is the `d_B(r,.)` coordinate of that common higher gate.
This contradicts owner uniqueness.  Positive index-difference sets of
distinct ordered gates are therefore disjoint.  This argument does **not**
forbid a repeated difference within one gate.  The number of available
gates is at most `|H_B|=15-Q`.

Finally the visible starts obey

```text
t_j in [M+1-q,M-3]
```

and their parities alternate with `j`, so the `Q` starts include both
parities.  The named block `q+{0,1,3}` and every actual block
`t_j+{0,1,3}` are owner-disjoint.  Consequently

```text
|q-t_j|>=4,                         q+3<=M.
```

In sorted order the neighbouring `t_j` gaps are at least four and at least
one gap is at least five.  Their required span is at least `4(Q-1)+1`, while
the available span is `q-4`; therefore

```text
q>=4Q+1.                                          (FW279.52)
```

If `2q>=M+1`, the named start `q` lies in the same high window.  The resulting
`Q+1` starts have gaps at least four, with at least one gap five because the
`t_j` include both parities.  Comparing their required span `4Q+1` with the
available span `q-4` gives `q>=4Q+5`.  If `2q<=M`, the value `q` is the
strict minimum of the corresponding `Q+1` low-window starts in `[q,M-3]`;
the same span `4Q+1` gives

```text
M-q>=4Q+4,                    M>=8Q+5.             (FW279.53)
```

At order eighteen these facts give genuine exclusions only for

```text
Q=10,11,12,13,14.                                 (FW279.54)
```

For `Q=12,13,14`, same-gate four-spacing gives the explicit capacity

```text
(15-Q)ceil(Q/4)<Q,
```

so the available gates cannot hold the visible indices.  At `Q=11`, four
gates force the mod-four recurrence, after which
two ordered gates both contain positive index difference four.  At `Q=10`,
the five-gate colouring closes by the following finite hand argument.  Name
the colours of indices `0,1,2,3` as `A,B,C,D`.  If index four is `A`, then
indices five through seven are `E,B,C`, and `B,C` repeat difference five.
If index four is `E`, index five is `A` or `B`.  In the first case indices
six through eight are `C,B,D`, and `D` repeats difference five with `A`; in
the symmetric second case they are `A,C,E`, and `E` repeats difference four
with `B`.

The boundary of this weak packing kernel is real.  At `Q=9` its constraints retain 26
partitions, including a six-gate pattern with groups `{0,4,8}`, `{2,7}` and
four singletons.  A unified direct-arm SMT model imposed every one of those
partitions and orders together with the `q` and gate depths, one- and
two-vertex tails, `t`-windows, `Y`-gaps, high/low packing, the Wiener sum,
all 153 distance bounds and global `Distinct`.  Its bounded 120-second run
ended `UNKNOWN`/cancelled.  It produced no exclusion, witness or proof
certificate and is not promoted to an **OBSERVED** solver theorem here.
The external, non-replayed model string had SHA-256
`9f8e4fcdbaf1140cfeb62c82690608ec938a4f22ddcbbb5912d02d30bf53b008`;
no script or solver artefact is frozen by FW279.

Dropping the final global `Distinct` leaves the explicit scalar/LCA pressure
state

```text
q=109,
gate depths=(0,6,20,24,28,32),
gate assignment for j=0,...,8=(0,5,1,4,0,3,2,1,0),
direct arms=(44,75,48,69,40,63,58,43,36),
t=(44,107,54,97,40,87,78,49,36),
W=11781.                                           (FW279.55)
```

All its distances are at most 153, but only 116 are distinct.  It is a
formal noninjective pressure state, not a tree satisfying the Leech owner
condition.  At `Q=8`, `{0,4}` plus singleton gates survives the weak kernel;
for `Q<=7`, all-singleton gate patterns survive and leave additional core
vertices.  Thus `Q=5,6,7,8,9` all remain **UNVERIFIED**.

The augmented owner graph also records why Euler counting stops.  For a
positive-depth vertex `v in B-{r}`, write `y_v=d_B(r,v)`, and let

```text
L={v:y_v+2 is filled by an actual internal pair of B},       |L|=E.
```

Construct `F*` on `B union {x}`.  If `v in L`, add the unique internal owner
edge of `y_v+2`; if `v notin L`, that virtual position is a hole of `S` and
has a unique removed owner `{x,u_v}` in `T`, so add that external edge.
Label the added edge by its source vertex `v`.  Thus every vertex of
`B-{r}` supplies exactly one label, while `x,r` are unlabelled; `F*` has
`b+1` vertices and `b-1` edges.

Make the component-transfer digraph by directing each label from the `F*`
component containing its label vertex to the component containing its owner
edge.  For a component `C_i`, let `u_i` count unlabelled vertices and `mu_i`
be its cycle rank.  Its transfer indegree is its edge count
`|C_i|-1+mu_i`, while its transfer outdegree is its label count
`|C_i|-u_i`.  Therefore, if the total cycle rank is `mu`, `F*` has `2+mu`
components and

```text
indeg(C_i)-outdeg(C_i)=u_i-1+mu_i,                (FW279.56)
```

Cycles and mergers are therefore allowed.

There is one exact whole-row classification, but it consumes only an existing
hole.  If a universal vertex `u in B` satisfies

```text
d_B(u,v)=y_v+2        for every positive-depth v!=u,
```

then the common-gate classification gives `u in H_B` nonvisible and
`d(x,u)=q+2`.  Hence the removed value `q+2` belongs to `H_rem`; it is not an
additional hole beyond (FW279.46).  In particular neither

```text
|H_rem|>=E-Q+1
```

nor terminal four-row rank additivity is known.  This restricted calculation
does not prove the all-order near-perfect nonpendant-unit theorem.

## 10. Architecture verdict and reopening gate

The exact reductions identify three facts that must not be conflated.

1. The pendant numeric owner forest is acyclic automatically, but it may
   merge.  Preventing those mergers is the new rank anti-coalescence lemma.
2. Even an injective forest may leave sources below the top band.  Moving all
   sources to `[C+1,D_0]` requires the independent multiscale transport
   inequality (FW279.15).
3. The strict `2|15` q=1 exclusions are a real finite theorem inside that
   wrapper, but a general nonpendant unit edge has an arbitrary `s|t`
   interface and a larger owner-realisation problem.

Therefore the present A/B/C architecture is **OBSERVED not closed**.  This
is a decision about the displayed proof mechanisms, not a proof that no
future closure exists and not a proof of mathematical independence.

A renewed attack must add, simultaneously, both pendant lemmas

```text
rank anti-coalescence  +  multiscale source transport,
```

or replace that route with a general rooted-realisation stability theorem
strong enough to reject the arbitrary nonpendant strict-cap certificate.
Further coefficient-only packing inside the special `2|b` wrapper does not
cover the missing quantifier.

All statements labelled **OBSERVED exact** above are analytic consequences
of path addition, owner uniqueness, q=1 suffix ownership and finite gate
packing.  The `L6` table and the two six-vertex trees are hand-checkable
controls.  The formal states recorded in Section 7 are integer
relaxations only.  FW279 found no actual strict nonpendant counterexample.
It records one disclosed, non-replayed Q9 SMT sentinel ending
`UNKNOWN`/cancelled, but adds no frozen verifier, certificate, SAT/UNSAT
result or order exclusion.  G18 and global nonexistence remain
**UNVERIFIED**.

Antecedents: `docs/q1-light-quotient-cap.md`,
`docs/unit-edge-owner-propagation-audit.md`,
`docs/nonpendant-unit-rooted-stability-stop.md`, and
`docs/q1-full-spectrum-mechanism-audit.md`.
