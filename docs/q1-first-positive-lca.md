# The first positive mixed-LCA edge and terminal completion (FW273)

FW273 is the exact successor to the pendant-unit obstruction in FW272.  It
keeps the pendant hypothesis and uses the full Leech distance spectrum.

**Frozen successor.**  FW274 sharpens the size-dependent estimates in this
note to the absolute bounds `tau<=10` and `w<=21`.  The statements below
remain valid, but (FW273.9), (FW273.17) and their order-eighteen numerical
specialisations are no longer the best known bounds.  The complete
prefix-exhaust and ancestor-collision proof is in
`docs/q1-absolute-first-odd-edge.md`.

* **OBSERVED:** the labelled mixed-parity rectangle determines every
  same-parity LCA whose descendant subtree is not monochromatic.
* **OBSERVED:** if `tau` is the first transformed odd distance owned by a
  positive mixed LCA, then the raw convolution has its first hole at `tau`.
  Quantitatively,

  ```text
  tau<=3|O|+2.
  ```

  Its actual owner is a single odd edge not incident with the root, of weight
  `w=2tau+1<=6|O|+5`.  At order eighteen this gives `w<=47` or `w<=71`,
  according to the parity orientation.
* **OBSERVED:** at a deepest mixed descendant subtree, the mixed distances
  are an exact direct block.  All remaining same-parity freedom lies inside
  its pure monochromatic child subtrees, whose edge weights can be divided by
  two.
* **UNVERIFIED:** that terminal freedom can contain quadratically many actual
  owners.  Neither the q=1 visible suffix nor the exact completion formulas
  turn it into a collision or a bounded-context state of the same type.

The theorem below is analytic.  It has no verifier or certificate, proves no
order exclusion, and leaves G18 **UNVERIFIED**.

## 1. Setting and the two exact parity sheets

Let `T` be a Leech tree of order `n`; thus all of its unordered-pair distances
are distinct and are exactly

```text
I_N={1,...,N},                       N=binom(n,2).
```

Suppose that the weight-one edge is the pendant edge `a--1--b`, with `a` the
leaf, and root the tree at `b`.  Write

```text
rho(v)=d(b,v),
E={v:rho(v) is even},                O={v:rho(v) is odd},
e=|E|,                               o=|O|,
K=eo=ceil(N/2),                      P=floor(N/2).
```

In particular `b in E` and `a in O`.  For `u in E`, `v in O`, put

```text
R_u=rho(u)/2,
S_v=(rho(v)-1)/2,
ell(u,v)=rho(LCA_b(u,v)),
z_(u,v)=(d(u,v)-1)/2=R_u+S_v-ell(u,v).
```

Root depths are distinct, since two vertices at the same positive depth
would repeat their distances to `b`.  Hence `R={R_u}` and `S={S_v}` are
sets, both containing zero.  The odd actual owners and the even actual
owners give the two coefficientwise exact identities

```text
{z_(u,v):u in E,v in O}={0,...,K-1},              (FW273.1)

{d(p,q)/2:rho(p)=rho(q) mod 2}={1,...,P}.         (FW273.2)
```

Every value in each display occurs exactly once.  This global
distance-distinctness assumption is essential below: the even-channel
collisions used in Section 4 do not follow from the odd rectangle
(FW273.1) alone.

## 2. Exact root-branch completion

The two sheets can be coupled without discarding their actual-pair owners.
For a finite coordinate family `D`, use

```text
D(X)=sum_(d in D) X^d,
D^[2](X)=sum_({d,d'} subset D) X^(d+d'),
J_[r,s](X)=X^r+X^(r+1)+...+X^s.
```

In `D^[2]` the sum is over unordered pairs of distinct labelled vertices;
the root coordinates are distinct, so the set notation causes no ambiguity.
Let `C` range over the child branches of `b`, with child root `c` and
`h_C=rho(c)`.  Measured from `c`, define

```text
A_C(X)=sum_(u in C, d(c,u) even) X^(d(c,u)/2),
B_C(X)=sum_(v in C, d(c,v) odd)  X^((d(c,v)-1)/2).
```

Let `X_C(X)` be the actual polynomial of the odd distances internal to `C`,
with exponent `(d-1)/2`, and let `Y_C(X)` be the actual polynomial of the
even distances internal to `C`, with exponent `d/2`.  Then

```text
J_[0,K-1]
 = R(X)S(X)
   + sum_C (X_C(X)-X^(h_C) A_C(X)B_C(X)),          (FW273.3)

J_[1,P]
 = R^[2](X)+X S^[2](X)
   + sum_C (Y_C(X)
            -X^(h_C)(A_C^[2](X)+X B_C^[2](X))).   (FW273.4)
```

These are identities in the integer polynomial ring, so their coefficients
retain multiplicity and owner provenance.  For vertices in different root
branches the raw root sum is already the actual distance.  Inside one branch
the displayed correction removes that raw owner and inserts the actual
internal owner.  This proves (FW273.3)--(FW273.4), including both possible
parities of `h_C`.

### 2.1 The visible-LCA completion lemma

The cross sheet also determines most same-parity LCA depths exactly.  For
distinct `u,u' in E`, let

```text
c=LCA_b(u,u'),                       h=rho(c),
ell_vis^O(u,u')
  =max_(v in O) min{ell(u,v),ell(u',v)}.
```

Then

```text
ell_vis^O(u,u')<=h,                                  (FW273.5)

ell_vis^O(u,u')=h
  iff the rooted descendant subtree T_c contains an O vertex. (FW273.6)
```

Indeed, if `v in T_c`, both mixed LCAs have depth at least `h`, and because
`u,u'` separate at `c`, at least one has depth exactly `h`.  Thus their
minimum is `h`.  If `v notin T_c`, both LCAs equal `LCA_b(c,v)` and have
depth strictly below `h`.  Taking the maximum proves the claim.  The same
statement holds with `E` and `O` interchanged.

The mixed matrix `ell(u,v)` itself is read exactly from the labelled pendant
rectangle by the FW272 minor identity.  Therefore (FW273.5)--(FW273.6)
determine every same-parity LCA whose descendant subtree contains the
opposite parity.  The only same-parity LCAs not completed this way lie
inside maximal pure monochromatic descendant subtrees.

## 3. The first positive raw hole

Assume that the mixed LCA matrix is nonzero.  Define

```text
tau=min{z_(u,v):ell(u,v)>0}.                       (FW273.7)
```

The owner of `z=0` is the pendant pair `{b,a}`, whose LCA depth is zero, so
`tau>=1`.  Let

```text
c_m=#{(u,v) in E x O:R_u+S_v=m}.
```

Then the raw convolution has the exact prefix and first hole

```text
c_m=1                    for 0<=m<tau,
c_tau=0.                                            (FW273.8)
```

To prove the prefix, take `m<tau`.  A raw owner with positive LCA would have
actual coordinate

```text
z=m-ell(u,v)<tau,
```

contrary to (FW273.7).  The unique actual owner of `z=m` consequently has
LCA depth zero and raw sum `m`; global distance uniqueness gives `c_m=1`.
For the hole, the positive-LCA owner of the actual coordinate `tau` has raw
sum strictly greater than `tau`.  A raw owner at `tau` with LCA zero would
be a second actual owner of `tau`, while one with positive LCA would produce
a smaller positive-LCA actual coordinate.  Both alternatives are impossible.

Thus the first positive laminar correction does not appear at an arbitrary
place: it fills the first hole of the uncorrected sumset `R+S`.

## 4. The radix bound

The following estimate is deliberately asymmetric: `R` is the parity class
of the root `b`, while `S` contains the unit leaf `a`.  Interchanging the
two factors without also changing that pendant geometry is invalid; the
order-six control in Section 8 has `|S|=4` and no positive mixed LCA.

> **FW273 first-positive bound.** Under the setting of Section 1, if the
> mixed LCA matrix is nonzero, then
>
> ```text
> tau<=3o+2.                                        (FW273.9)
> ```

If `e<=3`, this is immediate from `tau<=eo-1<=3o-1`.  Hence assume `e>=4`.

### 4.1 When `1 notin R`

Let `Q_0` be the least positive member of `R`.  If `Q_0<tau`, the exact raw
prefix forces

```text
{0,...,Q_0-1} subset S.
```

In particular the two distinct actual pairs

```text
{b,e_(Q_0)},                     {a,o_(Q_0-1)}
```

both have distance `2Q_0`, a contradiction.  Therefore `Q_0>=tau`.  The
raw prefix now forces `[0,tau-1] subset S`, and hence

```text
tau<=o.                                            (FW273.10)
```

Here `e_r` denotes the even vertex with `R` coordinate `r`, and `o_s` the
odd vertex with `S` coordinate `s`.

### 4.2 When `1 in R`

Let `[0,k-1]` be the maximal initial consecutive block of `R`.  Since
`c_tau=0`, one has `tau notin R`; in particular `k<=tau`.  The same actual
depth-`2,4,6` collision as in FW272 shows

```text
k<=3.                                              (FW273.11)
```

Indeed, for `k>=4` the LCA of `e_1,e_2` can have depth only `0,1,2`.
Depth one is the true leaf `a` and cannot be an LCA; depths zero and two
repeat respectively `d(b,e_3)` and `d(b,e_1)`.

Thus `k=2` or `3`.  Because `e>=4`, the next member

```text
Q_0=min(R-[0,k-1])
```

exists.  If `Q_0>=tau`, elementary block induction in the exact raw prefix
forces

```text
0,k,2k,... < tau                    to belong to S.
```

There are `ceil(tau/k)` such entries, so

```text
tau<=ko.                                             (FW273.12)
```

It remains to treat `Q_0<tau`.  First apply the same block induction only
below `Q_0`: it gives

```text
{qk:qk<Q_0} subset S.                              (FW273.13)
```

Now write `Q_0=qk+t`, `0<=t<k`.  If `t>0`, the raw coordinate `Q_0` has
the two owners `Q_0+0` and `t+qk`, contradicting `c_(Q_0)=1`.  Only after
this prefix argument may one conclude

```text
Q_0=0 mod k,
Q_0>=2k,
{0,k,...,Q_0-k} subset S.                          (FW273.14)
```

The boundary `Q_0+k=tau` is already impossible: `Q_0 in R` and `k in S`
would give a raw owner of the first hole `tau`.  If instead
`Q_0+k<tau`, the usual local interval-block proof lies wholly inside the
exact prefix.  Uniqueness at `Q_0` excludes `Q_0 in S`, and uniqueness at
`Q_0+k` excludes every `Q_0+t in S` with `1<=t<k`.  Consecutive coverage
then forces

```text
[Q_0,Q_0+k-1] subset R.                            (FW273.15)
```

This produces an actual collision for both possible radices:

* If `k=2`, (FW273.14)--(FW273.15) give `Q_0-2 in S` and
  `Q_0,Q_0+1 in R`.  The LCA of `e_1,e_(Q_0)` has depth `0` or `2`.
  The first choice repeats `d(b,e_(Q_0+1))`; the second repeats
  `d(a,o_(Q_0-2))`.
* If `k=3`, the vertices `e_1,e_2` must lie in different root branches.
  A root LCA for `e_1,e_(Q_0)` repeats `d(b,e_(Q_0+1))`, so
  `e_(Q_0)` lies below `e_1`.  It then has root LCA with `e_2`, and their
  distance repeats `d(b,e_(Q_0+2))`.

Consequently `Q_0+k>tau`, so `Q_0>=tau-k+1`.  The `Q_0/k` entries in
(FW273.14) also give `Q_0<=ko`.  Combining these inequalities yields

```text
tau<=ko+k-1<=3o+2,
```

which proves (FW273.9).  Notice that the equality boundary
`Q_0+k=tau` was handled directly by the raw hole rather than by invoking a
block statement beyond its valid prefix.

## 5. The first positive owner is an edge

Let `(u,v)` be the unique positive-LCA owner of `z=tau`, and put

```text
w=d(u,v)=2tau+1.                                  (FW273.16)
```

Because `ell(u,v)>0`, the `u--v` path lies strictly below the root and does
not pass through `b`.  Its total weight is odd, so it contains an odd-weight
edge `f`.  The endpoints of `f` have opposite root parity, and because `f`
is not incident with `b`, their mixed LCA has positive depth.  Minimality of
`tau` therefore gives

```text
weight(f)>=2tau+1=w.
```

On the other hand `f` is part of a path of total weight `w`, so
`weight(f)<=w`.  Equality holds; positivity of all other edge weights means
that the path consists of `f` alone.  Thus:

> The first positive mixed-LCA owner is exactly one odd edge not incident
> with `b`.  Every lighter odd edge is incident with `b`.

Together with (FW273.9),

```text
w<=6o+5.                                          (FW273.17)
```

At order eighteen the two Taylor parity class orders are `7` and `11`.
If `o=7`, then `tau<=23` and `w<=47`; if `o=11`, then `tau<=35` and
`w<=71`.  Hence the orientation-free order-eighteen bound is

```text
w<=71.                                            (FW273.18)
```

This is only a bound inside the pendant branch.  It is not an order-eighteen
exclusion, and G18 remains **UNVERIFIED**.

## 6. Deepest mixed terminal and exact direct block

Choose a descendant-minimal vertex `c` such that its rooted descendant
subtree `T_c` contains both root parities.  Equivalently, `c` is a deepest
mixed vertex in the rooted descendant order.  Every proper child subtree of
`c` is then monochromatic.

Measured from `c`, set

```text
A={d(c,u)/2:u in T_c, d(c,u) even},
B={(d(c,v)-1)/2:v in T_c, d(c,v) odd}.
```

Here `0 in A`.  No child subtree can contain both an `A` vertex and a `B`
vertex.  Hence every `A--B` pair has LCA exactly `c`, and its transformed
odd coordinate is the raw sum.  Global uniqueness gives the actual direct
block

```text
A dot+ B.                                         (FW273.19)
```

Partition `A-{0}` and `B` into the coordinate sets `A_i` and `B_j` of the
pure child subtrees.  All edges internal to such a child subtree are even:
an odd edge would change root parity.  After division by two, each child is
a positive-integer weighted, globally distance-distinct tree.  Let `F_i(X)`
and `F_j(X)` denote its actual internal half-distance polynomial.  The exact
same-parity completion inside `T_c` is

```text
Y_c(X)
 = A^[2](X)+X B^[2](X)
   + sum_i (F_i(X)-A_i^[2](X))
   + sum_j (F_j(X)-X B_j^[2](X)).                  (FW273.20)
```

Thus the cross matrix plus (FW273.5)--(FW273.6) determines every
same-parity owner except pairs internal to the maximal pure child subtrees.
If those child orders are `s_1,s_2,...`, the number of still-free actual
owners is exactly

```text
U=sum_i binom(s_i,2).                              (FW273.21)
```

This is the strongest exact completion currently available.  It does not
give bounded owner context.  A terminal subtree of order `s` may consist of
`c`, one pure child of order `s-2`, and one opposite-parity singleton child.
Then (FW273.19) is only a one-column direct block while

```text
U=binom(s-2,2)=Theta(s^2).                         (FW273.22)
```

The large child is strictly smaller, but after halving it inherits only an
arbitrary punctured subset of the even spectrum: it need not inherit an
interval, a pendant unit edge, Taylor parity data, or a q=1 state.  Recording
all of its external owners requires unbounded context.  Consequently
(FW273.20) is not a same-type descent.

This obstruction is scalable even before imposing the missing global Leech
completion.  An all-even superincreasing star or an all-even
superincreasing comb gives arbitrarily many distinct internal distances in
the pure child; adjoining one opposite-parity singleton leaves the mixed
terminal block one-column.  These are red-team families for the completion
mechanism, not Leech constructions.

## 7. What the q=1 suffix does and does not add

For a q=1 order-eighteen state, `N=153` and `P=76`.  Its visible vertices
obey

```text
d(x,v_j)=N-j,                       0<=j<Q.
```

Writing `j=2r` or `2r+1` shows that the `x` row occupies matching top
suffixes of the two parity sheets:

```text
j=2r:     (d(x,v_j)-1)/2=P-r,
j=2r+1:   d(x,v_j)/2=P-r.                           (FW273.23)
```

If `x` belongs to the parity class of order seven, its same-parity row has
only six available vertices, so `floor(Q/2)<=6` and `Q<=13`.  If `x`
belongs to the class of order eleven, the opposite class has order seven,
so `ceil(Q/2)<=7` and `Q<=14`.  Therefore

```text
Q<=14,
all visible x-row half-indices in (FW273.23) are at least 70. (FW273.24)
```

By contrast the first positive coordinate satisfies `tau<=35`.  The gap
between these facts is not a propagation theorem.  If `x` lies outside the
deepest mixed terminal, the terminal identities see no distinguished top
row.  If `x` lies inside it, the odd top suffix can be the direct `x` row
while the even top suffix lies inside the largest pure child and hence in
the undetermined polynomial `F_i` of (FW273.20).  The visible/pure-core
location of the unit edge does not force the terminal mixed vertex onto the
owner hull of `x`.

Thus the q=1 suffix gives a sharp positional diagnostic, but it does not
reduce the `Theta(s^2)` terminal owner freedom.

## 8. Controls and finite diagnostics

### 8.1 Known Leech controls

The two known order-four trees and the order-six tree meet the small-factor
boundary.  In the order-six labelling

```text
(0,1,1), (0,2,2), (0,3,5), (3,4,4), (3,5,8),
```

rooting at `b=0` with `a=1` gives

```text
R={0,1},                    S={0,2,4,6},
ell identically zero.
```

This verifies the required asymmetry of (FW273.9).  The known order-four
star and path similarly lie on the `e<=3` side of FW272.

A separate pressure tree has edges

```text
b--a:1,       b--u:2,       b--v:5,
b--w:9,       u--t:13.
```

Here `E={b,u}`, `O={a,v,w,t}`.  Its one-based transformed odd rows
`(d+1)/2` are

```text
{1,3,5,8},                  {2,4,6,7},
```

so the odd rectangle is exactly `I_8`, and the unique positive entry is
`ell(u,t)=2`.  But its same-parity half-distances are

```text
{1,3,5,7,8,10,12},
```

which overflow `I_7`.  Its deepest mixed terminal at `u` has `A={0}` and
`B={6}`, so the local direct block itself does not collide.  This is a
positive control for the coupled-sheet direction, but it does **not** prove
that every positive mixed block forces even overflow.

The perfect-distance forest constructions recorded in the literature ledger
remain a separate control: an even-halved component need not recursively be
a Leech tree.

### 8.2 n=11 CP-SAT diagnostic

The following is only an **OBSERVED external/non-replayed diagnostic**.  A
temporary script `/tmp/pendant_matrix.py` (recorded SHA-256 prefix
`55ebd2...`) was run with OR-Tools 9.15 and one worker.  The necessary
relaxation contained the exact odd/even spectrum arrays for the `4 x 7` or
`7 x 4` mixed rectangle, labelled mixed-LCA owner variables, at least one
positive mixed LCA, and the mixed-rectangle four-point conditions.  It
deliberately omitted triangle inequalities and same-colour quadruple
four-point conditions.  It returned

```text
4 x 7: INFEASIBLE in 24.76 s,
7 x 4: INFEASIBLE in 25.69 s.
```

Removing all mixed-rectangle four-point conditions made both orientations
SAT in about `0.12 s`; the no-positive-LCA order-six control was SAT.  The temporary
model and solver proof log were not frozen in the repository, and no
independent replay or certificate exists.  Therefore these INFEASIBLE
statuses are not a proof, do not certify any order exclusion, and add nothing
to the already known order-eleven range.

As an **OBSERVED external/non-replayed operational STOP calibration**, the
still weaker order-eighteen model containing only the mixed rectangle and
labelled positive-LCA data (no triangle or same-colour quadruple constraints)
returned `UNKNOWN` after 300 seconds in both orientations: `7 x 11` used
206,689 conflicts and 1,242,259 branches, while `11 x 7` used 221,384
conflicts and 1,276,210 branches (OR-Tools 9.11, one worker, about 155 MB).
Neither status is an exclusion, and no further run is authorised by FW273.

## 9. Stop verdict and reopening gate

FW273 proves an exact first-hole theorem, localises its owner to a bounded
odd edge, and completes all non-monochromatic LCA data.  It also identifies
the precise remaining obstruction: a deepest mixed terminal can hide
quadratically many same-parity owners inside one pure child, and halving that
child loses the interval and q=1 hypotheses.

Accordingly the proposed implication

```text
positive mixed block
  => actual collision or strictly smaller same-type bounded-owner state
```

is **UNVERIFIED** and is stopped at (FW273.20)--(FW273.22).  Reopening this
route requires at least one genuinely new statement:

1. a parity-scope rigidity theorem forcing a large pure child to absorb a
   named interval of the even sheet;
2. a terminal-absorption theorem locating the deepest mixed vertex on the
   q=1 top owner hull; or
3. a no-grazing theorem that charges all child-internal owners with bounded
   boundary data.

No current identity supplies any of these.  The nonpendant unit-edge branch
is untouched; no new order is excluded; G18 remains **UNVERIFIED**.

Antecedents and controls:

```text
docs/q1-pendant-mixed-lca.md
docs/q1-full-spectrum-mechanism-audit.md
docs/literature-ledger.md
data/known_leech_trees.json
```

## 10. Frozen absolute successor (FW274)

FW274 keeps the hypotheses and first-hole identity of Sections 1--5 and
uses the prefix below `tau` more rigidly.  If `1 notin R`, the forced odd
depths already give `binom(tau,2)<=2tau-2`, hence `tau<=4`.  If `1 in R`,
the initial radix is `k=2` or `3`.  Defining the next later `R` coordinate
to be `Q_0=+infinity` when it does not exist makes the two cases exhaustive:
prefix convolution coefficients determine every root coordinate below
`min(Q_0,tau)`, not only a forced subset.

Explicit rooted-ancestor collisions then give the **OBSERVED all-order**
case ledger

```text
k=3,Q_0>=tau:       tau<=9,
k=2,Q_0>=tau:       tau<=10,
k=3,Q_0<tau:        tau<=10,
k=2,Q_0<tau:        tau<=9.
```

In the only apparent `tau=11` boundary, `k=3,Q_0=9`, the exact coefficient
`c_10` says that exactly one of the root coordinates `R_10,S_10` exists.
The `S_10` choice hits the raw hole at eleven using `R_1`; the `R_10`
choice repeats the distance twenty between the already root-separated odd
vertices at `S=3,6`.  Therefore

```text
tau<=10,                  w=2tau+1<=21.           (FW274)
```

FW272 supplies a positive mixed LCA for every pendant-unit candidate of
order at least eleven.  An eight-vertex globally distance-distinct pressure
tree attains `tau=10,w=21` and has exact odd transformed sheet
`I_[0,11]`, but its even half-sheet is not `I_16`; it is not Leech.  Thus
the constant is sharp only at the local interface.  Full even-sheet terminal
absorption remains **UNVERIFIED**, the nonpendant branch is untouched, no
order is excluded, and G18 remains **UNVERIFIED**.  Full proof and trust
boundary: `docs/q1-absolute-first-odd-edge.md`.  A frozen deterministic replay
of the finite parent-map/collision kernel is
`theory-lab/topwindow/verify_q1_absolute_first_odd_edge.py`, with output in
`theory-lab/topwindow/results/q1_absolute_first_odd_edge_certificate.json`;
it is support for the analytic proof, not an independent all-order proof.
