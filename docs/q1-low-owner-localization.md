# The q=1 low-owner localisation audit

This note freezes the first proof/no-go audit after the q=1 row encoder was
stopped.  It uses the notation of FW218--FW219.  Its conclusions have three
different scopes:

* **OBSERVED:** the exact four-cone description (FW269a) and the edge-domino
  lemma (FW269b) are consequences of the Leech axioms;
* **OBSERVED negative diagnostic:** the fixed-`I_kappa` family (FW269c) is a
  family of globally distance-distinct integer-weighted trees satisfying the
  q=1 *top geometry*, but it is not a family of Leech trees;
* **UNVERIFIED:** a pure-core-tail elimination theorem, or an owner-provenance
  bridge using the full tight spectrum, is still required before low owners
  can be confined to a bounded q=1 interface.

In particular, this note proves neither an order exclusion nor G18.  The
frozen deterministic arithmetic replay is
`theory-lab/topwindow/verify_q1_low_owner_localization.py`, with certificate
`theory-lab/topwindow/results/q1_low_owner_localization_certificate.json`.
The analytic proofs below, rather than the finite certificate, are the theorem
source.

## 1. q=1 notation

Let `T` be a Leech tree of order `n>=5`, and put

```text
N=binom(n,2).
```

Choose the FW218 orientation of diameter endpoints `x,z`.  Thus
`diam(T-z)=N-1`, while

```text
Q=N-diam(T-x)>=2.
```

Delete `x`, call its neighbour `o`, root `T'=T-x` at `o`, and write

```text
beta=d(o,z),                 y(v)=beta-d(o,v).
```

There is one visible vertex `v_i` at each coordinate `i`, `0<=i<Q`, no
vertex at coordinate `Q`, and

```text
H={v in T': y(v)>Q}
```

is an ancestor-closed connected induced subtree.  The connected components
of `T'-H` are the visible components.  Coordinates strictly increase on a
path towards the root, and distinct vertices have distinct coordinates:
otherwise their equal `o`-depths would repeat a distance.

If `h=w(xo)`, then `beta=N-h`.  The `o--z` path survives in `T-x`, so

```text
beta<=diam(T-x)=N-Q,
h>=Q.                                                     (1)
```

Consequently no path of weight less than `Q` can contain `x`.

## 2. FW269a: the exact low-owner four-cone

Fix `1<=d<Q`, and let `{a,b}` be the unique actual pair at distance `d`.
By (1), `a,b` both belong to `T'`.  Let

```text
ell=LCA_o(a,b).
```

The rooted-distance identity becomes

```text
d=2y(ell)-y(a)-y(b)
 =[y(ell)-y(a)]+[y(ell)-y(b)].                         (FW269a.1)
```

The owner lies in exactly one of the following four mutually exclusive
cones.

### HH: both endpoints are in the core

Here `a,b in H` and `ell in H`.  Put

```text
A=y(ell)-y(a),   B=y(ell)-y(b).
```

Then

```text
A,B>=0,   A+B=d,   A!=B.                              (FW269a.2)
```

Thus both endpoints lie in the weighted `d`-ball below `ell`, and one lies
within `floor((d-1)/2)` of `ell`.  The cone may slide arbitrarily far inside
`H`; (FW269a.2) gives no absolute bound from the threshold coordinate `Q`.

### VH: one endpoint is visible and one is in the core

After exchanging endpoints if necessary, write `a=v_i` and `b in H`.
Ancestor closure puts `ell` in `H`.  With

```text
A=y(ell)-y(b),   B=y(ell)-i,
```

equation (FW269a.1) gives `A+B=d`, with `A>=0` and `B>=2`.  Hence

```text
i>=Q+1-d,
Q+1<=y(b)<=y(ell)<=Q+d-1.                            (FW269a.3)
```

The owner path crosses the unique `H`-entry of the visible component of
`v_i`, and the entire path lies in the weighted `d`-ball below `ell`.

### VV-same: both endpoints are in one visible component

Write `a=v_i`, `b=v_j`.  Their LCA is visible; put
`lambda=y(ell)<Q`.  Then

```text
A=lambda-i,   B=lambda-j,
A,B>=0,       A+B=d,       A!=B.                    (FW269a.4)
```

In particular,

```text
i,j in [lambda-d,lambda] intersect [0,Q-1],
min(A,B)<=floor((d-1)/2).
```

Again this is a sliding cone, now inside one visible component, rather than
an absolute threshold anchor.

### VV-cross: the endpoints are in different visible components

Now `ell in H`.  Define

```text
A=Q-1-i,   B=Q-1-j,   C=y(ell)-(Q+1).
```

The missing coordinate `Q` gives `A,B,C>=0`, and distinct coordinates give
`A!=B`.  Direct substitution in (FW269a.1) gives the exact identity

```text
d=4+A+B+2C.                                          (FW269a.5)
```

Therefore this case is impossible for `d<=4`; more precisely,

```text
d>=5,
i,j>=Q-d+3,
Q+1<=y(ell)<=Q+1+floor((d-5)/2).                    (FW269a.6)
```

The weaker last upper bound with `floor((d-4)/2)` follows without using
`A!=B`; (FW269a.6) records the sharp integer consequence.

These four cases are exhaustive because `H` and the visible components
partition `T'`, and ancestor closure decides whether the LCA is in `H` or in
the same visible component.  They are mutually exclusive by endpoint class
and visible-component membership.

There is also a topology-free hop bound.  If the owner path has `r` edges,
its edge weights are `r` distinct positive integers, so

```text
binom(r+1,2)<=d,
r<=floor((sqrt(8d+1)-1)/2).                          (FW269a.7)
```

Thus FW269a simultaneously controls every owner in `I_(Q-1)`.  It confines
visible endpoints to explicit cones, but the HH and VV-same cones can slide.
It is not the requested bounded-interface theorem.

## 3. FW269b: edge dominoes and the unit-edge independent set

The following lemma is useful outside the q=1 setting.  Let `S` be any
positive-integer-weighted tree whose unordered-pair distances are globally
distinct.  Let an edge `e=ab` of weight `w` split `S-e` into sides
`A` containing `a` and `B` containing `b`, and define

```text
D_A={d(a,u):u in A},       D_B={d(b,v):v in B}.
```

Every cross-edge pair has distance

```text
w+alpha+beta,       (alpha,beta) in D_A x D_B.
```

Global distance uniqueness makes this sum map injective.  If the same
nonzero signed difference belonged to both difference sets, say
`alpha-alpha'=beta-beta'!=0`, then the distinct cross pairs with depth data
`(alpha,beta')` and `(alpha',beta)` would collide.  Hence

```text
(D_A-D_A) intersect (D_B-D_B)={0}.                  (FW269b.1)
```

Each side separately also obeys an edge-domino exclusion:

```text
D_A intersect (D_A+w)=empty,
D_B intersect (D_B+w)=empty.                        (FW269b.2)
```

Indeed, suppose `r,r+w in D_A`.  If `r=0`, an internal `A`-pair has distance
`w` and duplicates `e`.  If `r>0`, choose vertices at the two depths.  The
internal pair from `a` at depth `r+w` and the cross pair from `b` to the
vertex at depth `r` both have distance `r+w`.  The proof on side `B` is
identical.  This also proves (FW269b.2) when one of the two depths is zero;
no implicit nonzero-depth assumption is being made.

Return to the FW219 tree.  The distance `1` must be a single edge, and (1)
shows that this unit edge lies in `T'`.  More generally, orient any edge
`e=ab` of `T'` so that `b` is on the root side and `a` is on its descendant
side.  Let

```text
J_e={j in {0,...,Q-1}: v_j lies on the a-descendant side}.
```

For `j in J_e`, the root path goes through `a`, so

```text
d(a,v_j)=d(o,v_j)-d(o,a)=beta-j-d(o,a).             (FW269b.3)
```

If `j,j+w` both belonged to `J_e`, these two depths would differ by `w`,
contradicting (FW269b.2).  Thus `J_e` contains no two indices whose
difference is `w`.  For the unit edge this says that `J_e` is an independent
set in the path on `0,...,Q-1`, and therefore

```text
|J_e|<=ceil(Q/2).                                   (FW269b.4)
```

In particular, the unit edge cannot lie on a common trunk still carrying two
consecutive visible coordinates.  This is the strongest unconditional
owner-localisation consequence found in the audit.  It has a precise escape:
a pendant or tail edge wholly inside `H` may have `J_e=empty`, making
(FW269b.4) vacuous.

## 4. FW269c: a fixed-I_kappa sliding metric pressure family

The pure-`H` escape is not just a verbal possibility at the level of top
geometry.  The following strengthened family preserves any prescribed fixed
initial interval while sliding all its edge owners arbitrarily far down the
core.  A simpler single-unit spine was used as a discovery control; the
strengthened family below subsumes it and is the required pressure test.

Choose integers

```text
kappa>=1,          Q>=kappa+1,          L>=1,
m=Q+2+kappa L,     B>=4Q+5,             R=B^(m+2),
C_0=0,             C_i=sum_(h=1)^i B^h,
t_a=Q+2+aL         (1<=a<=kappa).                       (FW269c.1)
```

The indexing is deliberate:

```text
t_1>Q,       t_1<...<t_kappa=m,
m>=Q+kappa+2>Q+kappa+1.                              (FW269c.2)
```

Construct a tree with vertices

```text
x,r, s_0,...,s_m, v_0,...,v_(Q-1), ell_1,...,ell_kappa
```

and the following edges:

```text
x--r                         weight Q,
r--s_0                       weight 3R,
s_(i-1)--s_i                 weight B^i       (1<=i<=m),
s_j--v_j                     weight 2R-C_j-j  (0<=j<Q),
s_(t_a)--ell_a               weight a         (1<=a<=kappa).
                                                               (FW269c.3)
```

All weights are positive.  Put `z=v_0`.  Direct path summation gives

```text
D=diam(T)=d(x,z)=5R+Q,
diam(T-z)=D-1,
diam(T-x)=D-Q.                                      (FW269c.4)
```

The second equality is attained by `{x,v_1}` and uses `Q>=2`; the third is
attained by `{r,v_0}`.  All other pair types are strictly shorter by the
layer bounds proved below.  Rooting `T-x` at `r` gives `beta=d(r,z)=5R` and

```text
y(v_j)=j,
y(r)=5R,
y(s_i)=2R-C_i,
y(ell_a)=2R-C_(t_a)-a>Q.                            (FW269c.5)
```

Thus the reflected coordinates are exactly the q=1 top pattern: one vertex
at each `0,...,Q-1`, none at `Q`, and every spine and `ell` vertex is in the
ancestor-closed region above `Q`.  Every visible component is a singleton.

### Complete distance audit

The unordered-pair distances fall into the following disjoint `R`-layers.
Index ranges are `0<=i<l<=m`, `0<=j<Q`, `1<=a<b<=kappa`, and the conditions
printed beside the two `v_j--s_i` formulas avoid counting their common
`i=j` boundary twice.

| layer | pair type | offset or distance |
|---:|---|---|
| `0R` | `x--r` | `Q` |
| `0R` | `s_i--s_l` | `C_l-C_i` |
| `0R` | `ell_a--s_i` | `a+abs(C_(t_a)-C_i)` |
| `0R` | `ell_a--ell_b` | `a+b+abs(C_(t_a)-C_(t_b))` |
| `2R` | `v_j--s_i`, `i<=j` | `2R-C_i-j` |
| `2R` | `v_j--s_i`, `i>j` | `2R+C_i-2C_j-j` |
| `2R` | `ell_a--v_j` | `2R+C_(t_a)-2C_j+a-j` |
| `3R` | `r--s_i`, `r--ell_a` | `3R+C_i`, `3R+C_(t_a)+a` |
| `3R` | `x--s_i`, `x--ell_a` | `3R+Q+C_i`, `3R+Q+C_(t_a)+a` |
| `4R` | `v_i--v_j`, `i<j<Q` | `4R-2C_i-i-j` |
| `5R` | `r--v_j`, `x--v_j` | `5R-j`, `5R+Q-j` |

This table covers every pair of vertex classes.  To prove that its entries
are all distinct, first note

```text
C_m/R<1/[B(B-1)].                                  (FW269c.6)
```

Together with `B>=4Q+5`, this puts every displayed offset in an interval of
width less than `R/2`; the five listed `R`-layers therefore do not overlap.

Within a layer, write each offset in signed base `B`.  Across all displayed
types, the units tags lie in

```text
[-(2Q-3),2Q-1],
```

an interval of width `4Q-4<B`; every higher coefficient lies in `[-2,2]`,
so the difference of two such coefficients has absolute value at most
`4<B`.  In a proposed equality the units-tag difference is a multiple of
`B`, and the width bound forces it to be zero.  Subtracting that tag, dividing
by `B`, and repeating uses the higher-coefficient bound to recover every
signed digit coefficientwise.  The higher-digit patterns are:

* a consecutive `+1` block for `C_l-C_i`;
* a consecutive `-1` block for `-C_i`;
* a `-1` block through `j` followed by a `+1` block through `i` or `t_a`
  for `C_i-2C_j` or `C_(t_a)-2C_j`;
* the endpoint block `-2C_i` in the `4R` layer.

These blocks recover their endpoints.  If an old `v_j--s_i` signature has
the same higher digits as an `ell_a--v_j` signature, then necessarily
`i=t_a`, but their units digits are `-j` and `a-j`, so they are different.
In the `0R` layer, a spine interval has units digit zero, a one-leaf interval
has units digit `a`, and a two-leaf interval has units digit `a+b`.  Two
one-leaf intervals can have the same unsigned higher block only by using the
same anchor or by exchanging the two block endpoints; the first fixes `a`,
while the second changes the units tag from `a` to the distinct anchor label.
If an `ell--s` interval has the same higher block as an `ell--ell` interval,
the one-leaf anchor must be one endpoint of the common block, hence its label
is one of the two labels in the `ell--ell` pair.  Its positive units tag is
therefore strictly smaller than their sum, so equality is impossible.  At a
fixed anchor in the `3R` layer the four possible units tags are
`0,a,Q,Q+a`, which are distinct because `1<=a<=kappa<Q`.  The `4R` higher
block fixes `i` and its units digit then fixes `j`; the two `5R` offset
intervals `[-Q+1,0]` and `[1,Q]` are disjoint.  This proves global
pair-distance distinctness.

The only distances at most `kappa` are the pendant edges
`s_(t_a)--ell_a` themselves.  Indeed `Q>=kappa+1`, every nonempty spine
block is at least `B`, and every other layer is much larger.  Consequently

```text
Spec(T) intersect [1,kappa]=[1,kappa],
owner(a)={s_(t_a),ell_a}       (1<=a<=kappa).        (FW269c.7)
```

For the unit edge, the `ell_1` side has rooted-depth set `{0}` and
`J_e=empty`, exactly as FW269b permits.  Its anchor is `L+3` spine edges
beyond `s_(Q-1)`.  With fixed `Q,kappa` and `L` tending to infinity, its
depth is `Theta(m)`.  The same holds, at separated anchors, for every owner
in the fixed interval `I_kappa`.

### Trust boundary

The order of the pressure tree is

```text
n=m+Q+kappa+3,
```

whereas its diameter is `D=5B^(m+2)+Q`, enormously larger than
`binom(n,2)`.  It is therefore not a Leech tree.  Its very sparse spectrum
also fails the exact FW219c core-hole bijection and the exact FW261
three-factor tiling.  It is not a counterexample to either theorem.

What FW269c proves is narrower and exact: q=1 endpoint deficits, the reflected
visible/core pattern, global distance uniqueness, and even an arbitrary
fixed initial interval `I_kappa` do not by themselves anchor the owners near
the threshold.  The construction identifies the full tight-spectrum
interface as a load-bearing hypothesis absent from this pressure model.  It
does **not** prove that full spectrum is the only possible missing condition,
or that full spectrum would still be insufficient.

## 5. Why this does not authorise a new engine

The local owner catalogue through value six is finite.  Write `E_i` when
coefficient `i` is introduced by a new edge of weight `i`, `P_ij` when the
unique owner of `i+j` is the path on adjacent previously introduced edges
`i,j`, and `P_132` for the forced three-edge path of total six.  (`E_1,E_2`
are implicit.)  The exact fifteen signatures are

```text
A1  P12,E4,P14,P24       A2  P12,E4,P14,E6
A3  P12,E4,E5,P15        A4  P12,E4,E5,P24
A5  P12,E4,E5,E6

B1  E3,P13,P23,P132      B2  E3,P13,E5,P15
B3  E3,P13,E5,E6

C1  E3,E4,P14,P24        C2  E3,E4,P14,E6
C3  E3,E4,P23,P24        C4  E3,E4,P23,E6
C5  E3,E4,E5,P15         C6  E3,E4,E5,P24
C7  E3,E4,E5,E6.                                      (FW269d)
```

For completeness, values one and two must be `E_1,E_2`.  Value three is
either `P12` or `E3`.  In the first branch value four must be `E4`, after
which the mutually exclusive path possibilities at five and six give the
five `A` rows.  In the second branch value four is `P13` or `E4`.  If it is
`P13`, value five is `P23` or `E5`; simultaneous `P13,P23` forces the
opposite-end attachment and hence `P132`, giving the three `B` rows.  If
value four is `E4`, value five is exactly one of `P14,P23,E5`, and the
available unique owner at six gives the seven `C` rows.  Two displayed path
choices for the same value cannot coexist because all pair distances are
unique.  This proves exhaustion of the fifteen local signatures.

This is a catalogue of local actual-pair types, not a bounded attachment
catalogue.  The pressure family shows why: the same low signature can be
realised on arbitrarily deep pure-`H` tails.

An independently audited **OBSERVED external/non-replayed engine diagnostic**
also fails the predeclared 100-fold gate.  The generic order-11 forest search
visits 123,309 DFS nodes in total, so the charged-node threshold is
`floor(123309/100)=1233`.  Even under the deliberately stronger predicate
that the weight-1 edge has a permanent true-leaf endpoint, online generation
through inserted-edge depths `0,...,6` visits

```text
1, 1, 2, 8, 38, 190, 1111
```

candidate states, or `1351>1233` in total.  A visit counts a child once it is
constructed and tested, including immediate predicate rejections.  The kept
counts are `1,1,2,7,32,170,990`, but treating rejection as free does not
rescue the route: kept depth seven alone rises to 6,035.  Here depth means
the number of inserted edges, not the largest consecutively realised value;
one of the fifteen `I_6` signatures can become determined after three to six
insertions.  This diagnostic is not part of the frozen FW269 arithmetic
replay and is not a theorem or a hardware-normalised benchmark.

Accordingly no custom engine, order-16 run, or order-25 run is authorised by
FW269.  The exact successor is one of:

1. a **pure-core-tail elimination theorem** forcing the unit edge, or enough
   low owners, to meet visible descendants; or
2. a **full tight-spectrum owner bridge** that turns FW219c/FW261 coefficient
   coverage into cut-side rooted-depth incidence without assuming the desired
   localisation.

Both remain **UNVERIFIED**.  Any proof that simply assumes a deep unit edge's
descendant side contains two consecutive visible marks is circular: that is
the owner-locality statement the argument is meant to establish.  Until one
of the two bridges is proved, the low-owner route is stopped and G18 is
unchanged.
