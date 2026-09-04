# The light-quotient leaf cap and visible-row area bound (FW277)

FW277 returns to the pendant-unit first-positive edge of FW274--FW276.  It
does not try to bound the whole descendant side of that edge.  Instead it
contracts the complete light forest and selects a genuine leaf bag of the
resulting heavy quotient tree.

* **OBSERVED:** below the first positive edge, all nonroot light bags have a
  globally bounded total excess.  A descendant quotient leaf is therefore a
  true pendant even cap of order at most ten, apart from the explicit
  `tau=1` two-vertex case, and has diameter at most 108.
* **OBSERVED:** cutting that cap gives one exact direct-sum factorisation and
  four actual translated rows.  The pendant unit edge forbids six named
  rooted-depth differences.
* **OBSERVED:** on the q=1 branch, a cap containing the endpoint transports
  the complete visible suffix into disjoint translated blocks.  A cap outside
  the endpoint with no visible vertex satisfies a new owner-labelled
  visible-row area inequality.
* **OBSERVED:** a saturated cap would halve to a smaller Leech tree.  The
  complete light forest strengthens this: saturation is possible only at
  `tau=1`, where the light forest is fixed through weight two.
* **UNVERIFIED:** none of these statements absorbs a singleton quotient cap.
  Its cut factor is still one nonterminal rooted row of order `n-1`, and the
  proved invariants place no order-independent bound on the number of heavy
  singleton bags in a quotient corridor.

Thus FW277 is a bounded one-cap normal form and a genuine row-area
strengthening of FW276, but not a same-type descent.  It has no verifier,
certificate, computation or order exclusion.  G18 remains **UNVERIFIED**.

## 1. Setting

Let `T` be a Leech tree of order `n>=11`, so its unordered-pair distances
are distinct and equal

```text
I_N={1,...,N},                         N=binom(n,2).
```

Suppose the weight-one edge is the pendant edge `a--1--b`, with `a` the
leaf, and root `T` at `b`.  Retain the FW274 first positive mixed-LCA edge,
oriented away from `b`, as

```text
f=p--c_f,                   weight(f)=w=2tau+1,
1<=tau<=10,                 w<=21.                 (FW277.1)
```

FW274 proves that every odd edge lighter than `w` is incident with `b`.
FW276 proves that the forest `F_<w` of edges lighter than `w` realizes every
distance in `[1,w-1]` and that `f` is the next Find-Next edge.

Contract every component of `F_<w`.  The result is a tree `Q`; root it at
the bag `B_b` containing `b`.  The edge `f` survives as an edge of `Q`.
After deleting that quotient edge, let `Q_f` be the component containing the
bag of `c_f`, hence the component away from `b`.

Choose a bag `C` which lies in `Q_f` and has degree one in the full quotient
tree `Q`.  Such a bag always exists: if `Q_f` is a singleton, use it; if not,
use a descendant leaf of `Q_f`, not its attachment vertex.  This full-`Q`
leaf condition is essential.  Merely choosing an arbitrary leaf of the
induced tree `Q_f` could select its root, which can have the additional edge
`f` in `Q`.

Write the unique boundary edge of this bag as

```text
g=r--t,                  r in R=T-C, t in C,
weight(g)=e.                                        (FW277.2)
```

The symbols `c_f` and `t` are deliberately different: the selected leaf bag
need not be the light component containing the original endpoint `c_f`.

## 2. The bounded descendant cap

The selected vertex set `C` is an induced connected pendant subtree of the
full tree `T`, with `g` as its only boundary edge.  It lies on the
descendant side of `f`, so

```text
a,b notin C,             r notin {a,b},
H=d(b,r)>=2,             e>=w.                     (FW277.3)
```

If `C` is the bag of `c_f`, then `Q_f` must be a singleton and `g=f`, so
`e=w`.  In every other case `g` and `f` are distinct edges.  Edge weights
are globally distinct pair distances, hence then `e>w`.

Every internal edge of `C` belongs to `F_<w`.  It cannot be odd, since all
lighter odd edges are incident with `b`, which is not in `C`.  Therefore its
edge weights are a distinct subset of

```text
{2,4,...,2tau}.                                    (FW277.4)
```

More is true globally.  Let `E_nb` be the total excess of all nonroot light
bags:

```text
E_nb=sum_(B component of F_<w, B!=B_b) (|B|-1).
```

All edges counted by `E_nb` are distinct even elements of (FW277.4), so the
first bound is `E_nb<=tau`.  Equality is almost impossible.

If `E_nb=tau`, the nonroot bags use every even light edge weight
`2,4,...,2tau`.  The root bag can then contain no even edge.  Its odd light
edges are all incident with `b`, so it is an odd star centred at `b`.  If it
had an edge `b--q--u` other than the unit edge, then `q` would be odd with
`3<=q<2tau+1`, and

```text
d(a,u)=q+1
```

would duplicate the nonroot edge of weight `q+1`.  Thus the root light bag
would contain only the unit edge.  For `tau>=2` no component of `F_<w` could
then realize distance three: the root bag has only distance one and every
nonroot bag is even.  This contradicts the exact light coverage below `w`.
Consequently

```text
tau>=2  ==>  E_nb<=tau-1.                          (FW277.5)
```

At `tau=1`, distance two forces the unique edge of weight two.  It cannot
lie in the root bag: since `a` is a leaf it would have to be `b--2--u`, and
then `d(a,u)=3` would duplicate `f`.  Hence

```text
tau=1  ==>  E_nb=1,
F_<3 consists of the root unit component, one nonroot
two-vertex edge-2 component, and isolated vertices. (FW277.6)
```

Put `s=|C|`.  Equations (FW277.4)--(FW277.6) give

```text
tau=1:  s<=2,
tau>=2: s<=tau<=10.                                (FW277.7)
```

Every path internal to `C` uses a subset of its even light edges.  Therefore

```text
diam(C)<=2+4+...+2tau=tau(tau+1),
diam(C)<=108 under the strengthened total-excess bound. (FW277.8)
```

The last numerical bound includes `tau=1`, where the diameter is at most
two; for `tau>=2` the largest possible sum of at most `tau-1` weights from
(FW277.4) is `4+6+...+2tau=tau(tau+1)-2<=108`.

## 3. Exact cut identity and six forbidden differences

For a weighted tree `S`, write

```text
F_S(X)=sum_{{u,v} subset V(S)} X^d(u,v),
R_z(S;X)=sum_(u in V(S)) X^d(z,u).
```

Every path from `C` to `R` crosses `g`.  The full spectrum therefore has the
coefficientwise, actual-owner identity

```text
I_N(X)=F_C(X)+F_R(X)+X^e R_t(C;X)R_r(R;X).         (FW277.9)
```

All three summands have disjoint support, and every coefficient of the
product is zero or one.  In rooted-depth notation put

```text
D_C={d(t,u):u in C},       D_R={d(r,v):v in R},
rho=max D_C,               sigma=max D_R.          (FW277.10)
```

The product in (FW277.9) is an exact direct sum.  Comparing two cross pairs
gives the difference-set restriction

```text
(D_C-D_C) intersect (D_R-D_R)={0}.                 (FW277.11)
```

There are also four named rows against the same cap factor:

```text
D_C-{0},                    owners {t,u}, u!=t,
e+D_C,                      owners {r,u},
H+e+D_C,                    owners {b,u},
H+e+1+D_C,                  owners {a,u}.           (FW277.12)
```

The four row origins `t,r,b,a` are distinct by (FW277.3) and the pendant
hypothesis, so (FW277.12) consists of distinct actual owner pairs.  Their
supports are pairwise disjoint.  Comparing their four offsets shows that the
positive difference set of `D_C` avoids the following at most six values,
with repetitions allowed in the list:

```text
(D_C-D_C)^+ disjoint from
{1,e,H,H+1,H+e,H+e+1}.                             (FW277.13)
```

The missing zero term in the first row causes no exception: in every
putative overlap with that row, the required larger cap depth is positive.
Since `D_C` is even, odd members of (FW277.13) are automatic; the statement
does not forbid an interval of differences.

The same comparison is available at the original first-positive cut.  If
`B` is the full descendant side of `f`, put

```text
D_f={d(c_f,y):y in B},             h=d(b,p).
```

The four rows with offsets `0,w,h+w,h+w+1` give

```text
(D_f-D_f)^+ disjoint from
{1,w,h,h+1,h+w,h+w+1}.                            (FW277.14)
```

This is an actual-owner restriction on the unbounded side `B`; it is not a
bound on `|B|`.

## 4. Leaf or heavy corridor

Fix any distinguished vertex `x`, and let `B_x` be its quotient bag.  The
descendant quotient `Q_f` has the following exhaustive alternative.

1. It has a full-`Q` leaf bag not containing `x`.  Choosing that leaf gives
   the bounded cap above with `x in R`.
2. It has no such leaf.  Then every descendant leaf of the rooted tree
   `Q_f` is the single bag `B_x`.  A finite rooted tree with one descendant
   leaf is a path, so `Q_f` is a heavy-edge corridor from the bag of `c_f`
   to the terminal bag `B_x`.

Thus all branching on the descendant side produces a bounded cap avoiding
`x`; otherwise that entire side is a path of edges of weight at least `w`,
whose intermediate light bags share the total excess (FW277.5)--(FW277.6).
The root side of `f` may still branch.  FW277 does not assert that the whole
quotient `Q` is a `b`--`x` path.

## 5. q=1 endpoint branches

Retain the q=1 notation of FW218--FW219 and FW270:

```text
M=N-Q,
d(x,v_j)=N-j,                         0<=j<Q,
```

with one visible vertex `v_j` at each displayed coordinate, no vertex at
coordinate `Q`, and all other vertices of `T-x` in the set `H_Q` of
coordinates strictly greater than `Q`.

### 5.1 The endpoint lies outside the cap

Assume `x in R` and define

```text
J_C={j: v_j in C},                 q_r=d(x,r).
```

For every `j in J_C`, the path crosses `g`, so

```text
d(t,v_j)=N-j-q_r-e.                                (FW277.15)
```

All cap depths are even.  Hence `J_C` lies in one parity class, and its
positive difference set avoids the six values in (FW277.13).  In particular
it contains no consecutive indices.

The unit rows retain more exact provenance.  For `j in J_C`,

```text
d(b,v_j)=N-j+H-q_r,
d(a,v_j)=N-j+H-q_r+1.                              (FW277.16)
```

Therefore a step-two run

```text
j_0,j_0+2,...,j_1  subset J_C
```

tiles the complete actual-owner interval

```text
[N-j_1+H-q_r, N-j_0+H-q_r+1]                      (FW277.17)
```

by the adjacent `b`- and `a`-rows.  This is conditional on the run; the
quotient theorem alone does not force one.

There is a stronger conclusion in the empty branch.  If `J_C` is empty,
then, because `x` is outside `C`, every cap vertex lies in `H_Q`.  For all
`0<=j<Q` and `u in C`, the actual pair `{v_j,u}` satisfies

```text
e+M+1-q_r <= d(v_j,u) <= M.                        (FW277.18)
```

The lower bound is the triangle inequality
`d(r,v_j)>=N-j-q_r`; the upper bound holds because the top interval
`[M+1,N]` already has the distinct owners `{x,v_j}`.  Thus the `Qs` actual
owners in the visible-by-cap rectangle occupy a window of exactly `q_r-e`
integer positions.

The parity of `d(r,v_j)` alternates with `j`, while every cap depth is even.
Define

```text
A_Q(s)=sQ+(s-1)(Q mod 2).
```

Ordinary owner counting gives `q_r-e>=sQ`.  If `Q` is odd, the two parity
counts differ by `s`, so the shortest containing interval has length
`sQ+s-1`.  Consequently

```text
q_r-e>=A_Q(s).                                      (FW277.19)
```

The absent coordinate `Q` is also essential.  Since `C subset H_Q`,

```text
q_r+e+rho=max_(u in C)d(x,u)<=M-1.
```

Combining this with (FW277.19) gives the owner-labelled visible-row area
bound

```text
2e+rho+A_Q(s)<=N-Q-1.                              (FW277.20)
```

Unlike the cut capacity alone, (FW277.20) uses a named complete top owner
class, transports all `Q` visible rows against the actual cap factor, and
uses the missing q=1 coordinate.

### 5.2 The endpoint lies inside the cap

Assume `x in C` and

```text
N-Q+1>diam(C).                                     (FW277.21)
```

No visible vertex can then lie in `C`, because each visible distance from
`x` is at least `N-Q+1`.  All `v_j` lie in `R`, and, with
`t_x=d(t,x)`, their rooted depths from `r` contain the complete interval

```text
{N-e-t_x-Q+1,...,N-e-t_x} subset D_R.              (FW277.22)
```

For every `u in C`, put `t_u=d(t,u)`.  Transporting the same visible row
through `u` gives the actual block

```text
d(u,v_j)=N-j-(t_x-t_u),             0<=j<Q.        (FW277.23)
```

The top block for `u=x` is `[N-Q+1,N]`.  For `u!=x` the block cannot overlap
it and, since it is not incident with `x`, must lie at or below `M`.  Hence
`t_x-t_u>=Q`.  Equivalently, (FW277.11) and the consecutive interval in
(FW277.22) force every positive difference of cap depths to be at least
`Q`.  Those depths are even, so with

```text
q_0=2ceil(Q/2)
```

one obtains

```text
t_x=rho,
rho>=q_0(s-1),
every internal cap edge has weight at least q_0.   (FW277.24)
```

The internal edge weights are distinct even values at most `2tau`.  Thus,
when `s>1`,

```text
Q<=2tau,
s<=tau-ceil(Q/2)+2.                                (FW277.25)
```

Equations (FW277.22)--(FW277.24) are the exact row-transport conclusion:
there are `s` disjoint translates of the complete visible block, with the
`x`-row at the top and every other row shifted down by at least `q_0`.

### 5.3 Order eighteen

For G18, `N=153` and FW273 gives `Q<=14`.  Equation (FW277.8) therefore
makes (FW277.21) automatic:

```text
N-Q+1>=140>108>=diam(C).                           (FW277.26)
```

Hence an endpoint cap always satisfies (FW277.22)--(FW277.25).  A nonendpoint
cap with no visible vertex satisfies

```text
2e+rho+A_Q(s)<=152-Q.                              (FW277.27)
```

In particular a singleton empty-visible cap obeys

```text
e<=76-Q.                                           (FW277.28)
```

There is also a q=1-independent metric check.  All odd values below `e` are
owned inside `R`, because cross distances start at `e` and all cap distances
are even.  Since rooted depths in `D_R` are distinct,
`diam(R)<=2sigma-1`; the farthest cross pair gives
`e+rho+sigma<=153`.  Therefore

```text
e even: 3e+2rho<=306,
e odd:  3e+2rho<=307,
in all cases e<=102.                               (FW277.29)
```

The new visible-row bound (FW277.27), not (FW277.29), is the stronger branch
when the selected nonendpoint cap is empty of visible vertices.  Neither
bound is an order-eighteen exclusion.

## 6. Saturated caps halve to Leech trees

Before using the stronger total-excess result, suppose only that a nonroot
light cap attains the elementary bound

```text
s=tau+1.
```

It then has `tau` distinct even edge weights below `w`, hence exactly
`2,4,...,2tau`.  Divide all its weights by two.  The resulting order-`s`
tree has edge weights `1,...,tau`, globally distinct pair distances, and
every distance at most

```text
1+2+...+tau=binom(s,2).
```

It has exactly `binom(s,2)` pair distances, so they must be the complete
interval `1,...,binom(s,2)`.  Thus

```text
s=tau+1  ==>  C/2 is a Leech tree,
Spec(C)={2,4,...,tau(tau+1)}.                      (FW277.30)
```

Equations (FW277.5)--(FW277.6) sharpen this abstract conclusion in the full
pendant first-positive state:

```text
a saturated cap can occur only for tau=1 and s=2.  (FW277.31)
```

No catalogue of small Leech trees is needed for (FW277.31).

## 7. Exact stop

The quotient contraction removes the unbounded *interior* of a selected
light bag, but it does not bound the surrounding owner context.  The cross
factor in (FW277.9) still contains `s(n-s)` actual pairs.  Repeatedly peeling
leaf bags would retain cross rows between every earlier cap and the remaining
heavy skeleton, with no proved interval inheritance or decreasing exact
potential.

The obstruction is already present at `s=1`.  Then `F_C=0` and
`R_t(C)=1`, so (FW277.9) becomes

```text
I_N(X)=F_R(X)+X^e R_r(R;X).                        (FW277.32)
```

This is one complete rooted row with `n-1` actual owners.  It is not a
bounded context.  If the singleton is `x`, the row contains the q=1 top
suffix together with all nonvisible `x`-owners.  If it is an empty-visible
cap outside `x`, (FW277.20) locates its visible cross rows but does not make
the full row terminal.  In neither case does deleting the singleton make
`F_R` an initial interval or a Leech tree of order `n-1`.

Similarly, the conclusions above place no order-independent bound on the
number of heavy singleton bags in the corridor alternative of Section 4;
(FW277.5) bounds only the total nontrivial light-bag excess.  Thus the current
theorem supplies neither an actual collision nor a proper same-type strictly
decreasing state.

The reopening gate is now narrower than FW276's.  A successor must use the
full interval to prove that the rooted row in (FW277.32), or a bounded number
of its row transports, is a named terminal interval that can be absorbed;
alternatively it must attach a well-founded actual-owner potential to the
heavy corridor.  Capacity, moment or Ferrers estimates that leave the
singleton row unrestricted do not pass this gate.

FW277 therefore records an **OBSERVED** bounded-cap theorem and q=1
row-area bridge, together with an exact singleton stop.  It proves no order
exclusion and leaves G18 **UNVERIFIED**.
