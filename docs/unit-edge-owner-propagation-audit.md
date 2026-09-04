# Unit-edge owner propagation and exact stops (FW278)

FW278 audits the three narrow successors left by FW275 and FW277.  It keeps
actual unordered-pair owners throughout; its negative conclusions concern
only the displayed mechanisms.

* **OBSERVED exact:** deleting the pendant unit leaf and one singleton heavy
  quotient leaf leaves a common core with five named rooted supports, whose
  sole compatible overlap `h` has the same owner.  Projection to the path
  between their attachment vertices gives at most six distinct nonzero
  forbidden differences in every fibre, and rank compression gives an exact
  if-and-only-if criterion for a same-topology order-`n-2` descent.
* **OBSERVED exact:** in the strict nonpendant `x=2` state, the filled virtual
  row has an actual-owner cut-flow identity.  Combining it with the strict
  cap gives a prescribed subset-sum certificate for the holes outside that
  row.  It excludes the order-nine equality control after strict truncation,
  but has no proved all-order injection.
* **OBSERVED exact:** the bordered additive distance matrix is integrally
  congruent to one hyperbolic plane plus the diagonal edge factors.  Its
  Smith form, modular ranks, inverse sparsity and centred-Gram product bound
  consequently read edge factors, not cross-row owner placement.
* **UNVERIFIED:** no theorem propagates the q=1 top suffix into a named
  projection fibre, forces pathwise rank additivity, or prevents the strict
  hole sum from being an admissible subset sum at every order.

Thus FW278 gives one exact descent criterion, one strict-cap certificate and
three precise stops.  It has no machine verifier, frozen proof certificate,
search or order exclusion.  It does not prove the near-perfect
nonpendant-unit conjecture, and G18 remains **UNVERIFIED**.

## 1. Pendant unit leaf plus singleton heavy leaf

Retain the FW274--FW277 pendant-unit setting.  Let

```text
a --1-- b
```

be the unit leaf, and suppose the selected quotient cap of FW277 is the
singleton leaf

```text
c --e-- r,                    e>=w,
```

where `w=2tau+1<=21` is the first positive odd edge.  Put

```text
U=T-{a,c},        m=|U|=n-2,        h=d_U(b,r),
B=D_b(U)={d_U(b,u):u in U},
R=D_r(U)={d_U(r,u):u in U}.
```

The FW277 orientation has `r` distinct from `a,b`, so `b,r` both lie in
`U` and `h>0`.  Define the two leaf rows and their corner by

```text
A=1+B,             C=e+R,             L=1+h+e.    (FW278.1)
```

Every pair of `T` is either internal to `U`, incident with exactly one of
`a,c`, or the pair `{a,c}`.  Hence the full owner-labelled spectrum has the
coefficientwise disjoint partition

```text
I_N=F_U dot-union A dot-union C dot-union {L}.     (FW278.2)
```

This is the exact two-leaf successor to the singleton identity (FW277.32).
It is stronger than a cardinality equation: every term retains its actual
unordered-pair owner.

### 1.1 Five named rooted supports

The rooted rows already internal to `U` satisfy

```text
(B-{0}) intersect (R-{0})={h}.                    (FW278.3)
```

The common coefficient `h` has the same owner `{b,r}` in both descriptions.
Among the five named supports

```text
B-{0},       R-{0},       A,       C,       {L},
```

all other cross-intersections are empty: an overlap would give two distinct
owners of one distance in `T`.  Their union therefore contains

```text
(m-1)+(m-1)-1+m+m+1=4m-2
```

distinct positive integers.  In particular the exact hull bound is

```text
max{max B+1, e+max R, e+h+1}>=4m-2.               (FW278.4)
```

At order eighteen this gives `m=16` and a lower hull endpoint of 62, but it
does not collide the rows with a prescribed interval.

## 2. Projection fibres and up to six forbidden differences

Let `P` be the `b`--`r` path.  For a path vertex `p_s` at distance `s` from
`b`, let its projection fibre be

```text
V_s={u in U: the gate of u on P is p_s},
Z_s={d_U(p_s,u):u in V_s}.                         (FW278.5)
```

Thus `0 in Z_s`, and every vertex of `U` belongs to exactly one fibre.  The
four rows from `b,a,r,c` against that fibre have offsets

```text
s,             s+1,             h-s,             e+h-s. (FW278.6)
```

All collisions between distinct rows are forbidden.  It follows that the
positive difference set of every fibre avoids the nonzero members of

```text
{1, e, |h-2s|, |h-1-2s|,
       |e+h-2s|, |e+h-1-2s|}.                     (FW278.7)
```

The zero element of the fibre gives the complementary path-vertex rule

```text
2s notin {h-1,h,e+h-1,e+h}.                       (FW278.8)
```

Equations (FW278.7)--(FW278.8) are actual-owner no-grazing statements at
every path gate.  They do not say that a fibre contains a long interval, or
that one of the forbidden values is itself a fibre-depth difference.

## 3. Exact rank absorption criterion

Let the external owner set be

```text
H=A dot-union C dot-union {L},
q(t)=|H intersect [1,t]|,             phi(t)=t-q(t). (FW278.9)
```

By (FW278.2), the internal distances of `U` are exactly the complement of
`H` in `I_N`.  Rank compression therefore gives the unconditional set
identity

```text
phi(Spec(U))=I_[1,binom(m,2)].                    (FW278.10)
```

This alone does not preserve addition along paths.  If a path of `U` has
old edge labels `z_1,...,z_k`, then reweighting each edge by `phi(z_i)` gives
the compressed owner distance exactly when

```text
q(z_1+...+z_k)=q(z_1)+...+q(z_k).                 (FW278.11)
```

Consequently:

> **OBSERVED exact rank-descent criterion.**  Replacing every edge label
> `z` of `U` by `phi(z)` produces an owner-preserving Leech tree of order
> `m=n-2` on the same topology if and only if (FW278.11) holds on every
> path of `U`.

Necessity follows because the new path length is the sum of its new edge
labels.  Sufficiency follows from (FW278.10): every pair then realizes its
unique compressed rank, so the spectrum is the complete required interval.

The criterion is not automatic.  In the known order-six double star, take
the unit leaf at the weight-one pendant and take the weight-four pendant as
the second, non-diameter-end leaf.  A core path has edge labels `5,8`, while

```text
q(13)=8,                 q(5)+q(8)=3+4=7.         (FW278.12)
```

Thus path additivity fails in an actual Leech tree.  Taking instead the
weight-eight diameter-end leaf makes the same criterion succeed.  Endpoint
location matters, and the five-row partition alone does not select it.

## 4. q=1 top-owner interface

Retain the FW218--FW219 q=1 notation

```text
M=N-Q,             d(x,v_j)=N-j,       0<=j<Q.
```

If `c!=x`, deleting `a,c` from the common core removes from the named top
block only the positions whose visible endpoints are `a` or `c`; all other
owners `{x,v_j}` remain internal to `U`.  Thus the internal spectrum retains
`[M+1,N]` with at most those two named positions deleted.

If `c=x`, then `d(x,v_j)=e+d(r,v_j)`.  Hence `R` contains

```text
[N-e-Q+1,N-e]
```

with at most the one position corresponding to `a` deleted.  This is
genuine top-suffix propagation, but it lands only in the whole rooted row
`R`.

No proved implication routes that block to one fibre `Z_s`, makes one of
the gaps in (FW278.7) unavoidable, or enforces the all-path additivity
(FW278.11).  The pendant reopening gate is therefore exact: prove a
top-to-fibre collision, or prove (FW278.11) for every core path.  Counting
the five rows without their gates does neither.

Nor does the FW277 heavy-quotient corridor enter an existing family
exclusion: the root bag may still branch, and the corridor is not thereby a
spider, bi-spider, or the full-window canonical sink of FW35--FW47.  Its
singleton factor `X^eR_r(R)` retains unbounded named owner context.  Reopening
that alternative requires pendant-path absorption with bounded context, or
a theorem forcing the arm to become such a canonical sink.

## 5. Strict nonpendant cap: owner cut flow

Return to the hard FW275 branch at `x=2`:

```text
c --2-- a --1-- r -- B,             |B|=b,
Y={d_B(r,v):v in B},                 Y_+=Y-{0},
D_0=binom(b,2)+3b-2.                                 (FW278.13)
```

The virtual row is `2+Y_+`.  Let `L` be the set of source vertices `v`
for which `y_v+2` is filled by an actual internal pair of `B`, and put
`E=|L|`.  Make a graph `G` on `V(B)` whose edge for `v in L` is that unique
actual owner pair.

Root `B` at `r`.  For each rooted edge `f`, let

```text
w_f = weight(f),
U_f = descendant vertex set below f,
s_f = |U_f|,
c_f = |delta_G(U_f)|,
l_f = |L intersect U_f|.                          (FW278.14)
```

Expanding every owner distance and every source depth across rooted cuts
gives the exact identity

```text
sum_f w_f(c_f-l_f)=2E.                            (FW278.15)
```

Indeed, `sum_f w_fc_f` is the sum of the `E` actual owner distances, while
`sum_f w_fl_f` is the sum of their source depths.  Their pointwise
difference is two.  Formula (FW278.15) survives owner mergers and cycles;
it does not assert `c_f-l_f>=0` edge by edge.  The FW275 equality controls
have both signs, so a monotone cut potential cannot be obtained by dropping
the negative terms.

## 6. The strict-cap hole-sum certificate

Let `W_+` be the sum of all distances between pairs of nonroot vertices of
`B`, and remove the wrapper, root row and virtual row from the strict cap:

```text
X=I_[1,D_0] - (O union Y_+ union (2+Y_+)),
O={2} dot-union (1+Y) dot-union (3+Y).             (FW278.16)
```

The virtual row has `b-1-E` holes.  Since the hard state has `b-3` holes in
total, exactly `E-2` holes remain outside it.  Call this set `H_X subset X`.
Summing the strict cap and then using (FW278.15) gives two equivalent exact
forms:

```text
|H_X|=E-2,

sum H_X = D_0(D_0+1)/2 - 6b - 4 sum Y_+ - W_+
          + sum_(v in L)(y_v+2)                                  (FW278.17)

        = D_0(D_0+1)/2 - 6b
          + sum_f w_f(c_f-s_f(b+3-s_f)).            (FW278.18)
```

Here `sum Y_+=sum_f w_fs_f`, while an edge `f` separates
`s_f(b-s_f-1)` nonroot pairs, giving the second form.  Unlike the cap-blind
reflection count in FW275, (FW278.17) uses the missing top coefficient
through the literal set `X` and its prescribed sum.

For the FW275 order-nine equality control (`b=7`), strict truncation gives

```text
X={8,9,10,11,16,17,18,19,24,25,30,35,36},
|H_X|=3,                         sum H_X=32.        (FW278.19)
```

No three-element subset of this `X` sums to 32.  Thus that specific
multi-gate equality pattern cannot be repaired inside the hard cap.  The
order-eleven control (`b=9`) escapes even earlier:

```text
3+max Y=62>D_0=61.                                 (FW278.20)
```

These are strict-cap rejections of the two pressure controls, not an
all-order proof.  There is no established theorem saying that the right
side of (FW278.17) can never be an `(E-2)`-subset sum of the state-dependent
set `X`.

The smallest flows do not close this gap.  At `E=2`, (FW278.17) is one
global Diophantine equation with no outside hole; at `E=3`, its right side
must merely be the unique element of `H_X`.  The bounds `w_f>=4`,
`c_f<=E` and parity force neither condition to fail.  Actual local controls
have cut differences `-2,+2` on edges of weights `4,6` at `E=2`, and
`-3,+3` on those weights at `E=3`; their weighted sums are respectively
four and six as (FW278.15) requires.  Their `B` plus the `1,2` handle is
globally distance-distinct, although they are not hard-cap states.  Thus
neither sign nor a separate `E=2,3` shortcut replaces the subset-sum gate.

## 7. Whole rows, prefix transport and failed descent

Suppose one vertex `u` owns the complete virtual row away from its diagonal:
for every other positive-depth vertex `v`,

```text
d_B(u,v)=y_v+2.
```

If their common LCA gate has depth `g`, the rooted distance formula forces

```text
y_u=2g+2,
LCA(u,v)=g for every such v.                       (FW278.21)
```

The gate dominates every other positive vertex, and `u` is an independent
leaf attached directly to it, by an edge of weight `g+2`.  Replacing `u` by
a root leaf of weight two
preserves all its distances to other nonroot vertices and changes only

```text
Spec(B')=Spec(B)-{2g+2}+{2}.                       (FW278.22)
```

After adjoining a root leaf of weight one, the corresponding two distances
change as

```text
{2g+2,2g+3}  ->  {2,3}.                           (FW278.23)
```

But `{2,3}` are already the edge and root distance of the original
nonpendant `1,2` handle.  The classified whole row therefore gives an exact
exchange, not a descent inside the hard wrapper class.

There is also no hidden gain in comparing the two leaf extensions.  Put
`q=x+1=3`; let `P` be `B` with a root leaf of weight one and `K` be `B` with
a root leaf of weight `q`.  Inside the common cap their padded hole sets are

```text
H_P=C_0 dot-union (q+Y),
H_K=C_0 dot-union (1+Y),
C_0=H_S dot-union {x},                            (FW278.24)
```

where `H_S` is the hard state's padded hole set.

If `h_P(t),h_K(t)` are their prefix hole counts, then

```text
h_K(t)-h_P(t)=#{y in Y:t-q<y<=t-1}.               (FW278.25)
```

The total transported area is exactly `b(q-1)=bx`.  All common hard-state
holes cancel from (FW278.25), so linear prefix or moment combinations cannot
supply the one extra strict-cap hole.

Finally, source-to-gate depth is not a decreasing potential.  Root a tree
with one leaf at depth four and another branch

```text
r --100-- u --6-- v.
```

Its six pair distances are `4,6,100,104,106,110`, all distinct, and the
virtual target `4+2=6` is owned behind the gate at depth 100.  Adding the
`1,2` handle still leaves all fifteen distances distinct.  Any gate-depth
descent needs a new strict-cap theorem, not rooted-tree geometry alone.

The strict-cap route reopens if one proves either that (FW278.17) is never an
`(E-2)`-subset sum of `X`, or an owner injection producing at least `E-1`
outside holes.  Both statements remain **UNVERIFIED**.

## 8. Additive distance-matrix normal form

Let `D=(d(u,v))` be the additive distance matrix of any positive
integer-weighted tree on `n` vertices, and border it by ones:

```text
M = [0  1^T]
    [1   D ].                                      (FW278.26)
```

Choose a root and use the integral root-edge difference basis.  There is a
unimodular matrix `P` such that

```text
P^T M P = H direct-sum diag_e(-2w_e),
H=[0 1; 1 0].                                     (FW278.27)
```

This integral congruence gives, without a genericity assumption,

```text
det M=(-1)^n 2^(n-1) product_e w_e,
SNF(M)=(1,1,SNF(diag_e(2w_e))),                   (FW278.28)

rank_(F_p) M=n+1-#{e:p divides w_e}   for odd p,
rank_(F_2) M=2.                                   (FW278.29)
```

The unbordered determinant is the classical companion identity

```text
det D=(-1)^(n-1) 2^(n-2)
      (product_e w_e)(sum_e w_e).                 (FW278.30)
```

The vertex-by-vertex block of `M^(-1)` is

```text
-(1/2)L_(1/w),                                    (FW278.31)
```

where `L_(1/w)` is the weighted Laplacian with conductance `1/w_e`.
Consequently an off-diagonal entry of that block is `1/(2w_e)` on an edge
and zero on a nonedge.  The inverse recovers the tree once the *placed*
matrix is known; the Leech condition supplies only its off-diagonal
multiset, not that placement.

### 8.1 Centred Gram bound

Let `J=I-11^T/n` and `G=-(1/2)JDJ`.  The tree metric is squared Euclidean,
so `G` is positive semidefinite of rank `n-1`, with

```text
pdet G=(product_e w_e)/n,
tr G=(1/n)sum_{u<v}d(u,v).                         (FW278.32)
```

For a Leech tree the latter sum is `N(N+1)/2`, hence

```text
tr G=(n-1)(N+1)/4.
```

AM--GM on the nonzero eigenvalues gives

```text
product_e w_e <= n((N+1)/4)^(n-1).                (FW278.33)
```

At `n=18`, even comparison with the minimum distinct-edge product `17!`
leaves a factor about `4.54*10^13`.  The inequality is therefore far from
an order-eighteen contradiction.

The two order-four Leech trees have the same full pair-distance spectrum
but different edge factors (`{1,2,4}` versus `{1,2,3}`); the order-six
double star likewise passes (FW278.27)--(FW278.33).  These actual controls
show the precise information boundary.  Congruence, Smith valuations,
determinants and inverse sparsity read individual edge factors or the placed
matrix.  They do not identify which cross owner carries a given element of
`I_N`, so they cannot absorb the singleton row or evaluate the strict
owner-graph subset sum.

## 9. Mechanism verdict and trust boundary

FW278 narrows both unit-edge branches to explicit algebraic gates:

1. on the pendant branch, a top-to-fibre collision or all-path rank
   additivity in (FW278.11);
2. on the nonpendant branch, an all-order exclusion of the prescribed
   subset sum (FW278.17), or an injection yielding one additional outside
   hole;
3. for any matrix successor, a new invariant retaining actual cross-owner
   placement rather than only edge factors.

The formulas in Sections 1--8 are **OBSERVED analytic** consequences of
tree paths, actual-owner uniqueness, elementary cut expansion and integral
row/column operations.  The order-four and order-six examples and the two
FW275 pressure trees are **OBSERVED hand-checkable controls**.  No new
finite kernel or solver run was used, and there is no verifier or
certificate to freeze.

The STOP statements are mechanism-specific.  They do not say that a
different cap-aware owner potential, a top-suffix theorem or an
owner-sensitive matrix construction is impossible.  They prove no Leech
nonexistence result and leave G18 **UNVERIFIED**.

Antecedents: `docs/nonpendant-unit-rooted-stability-stop.md`,
`docs/q1-first-positive-edge-cut.md`, `docs/q1-light-quotient-cap.md`, and
`docs/q1-full-spectrum-mechanism-audit.md`.
