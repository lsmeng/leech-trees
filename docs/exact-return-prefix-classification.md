# Exact-return rooted-prefix classification (FW292)

FW291 forces the `BC` rooted convolution in an exact-return two-cycle to have
a coefficient-one prefix, a zero block, and then one exact return.  Combining
that whole block—not only its final coefficient—with the exact FW283
first-cross-hole table excludes 24 of the 81 a priori `(delta,eta)` types.

This is a **PROVED finite local classification plus a matched-root connector
split and a STRICT STOP for the bounded-prefix mechanism**.  It does not
prove ERTC.

## 1. Setup

Keep the FW291 notation

```text
q --path drop--> r --edge lift--> q,
delta = w_q-w_r = eta_r,
eta   = eta_q,
D     = delta+eta.
```

For the `r`-cut factors `Rho,W`, FW291 proves

```text
[X^j](Rho*W)=1,   0<=j<delta,
[X^j](Rho*W)=0,   delta<=j<D,
[X^D](Rho*W)=1.                                  (FW292.1)
```

The exact FW283 table first gives

```text
delta in E={1,2,3,4,5,6,8,9,10};                 (FW292.2)
```

`eta` belongs to the same set.  Up to swapping the two factors, their rooted
depths below `delta` are the unique FW283 row `F_delta=(L_delta,R_delta)`.

## 2. Why the entire zero block is finite data

Every rooted factor contains its root at depth zero.  Therefore a previously
unseen vertex at rooted depth `s<D` would itself create the cross sum
`s+0=s`.  Consequently:

1. the FW283 supports contain every rooted depth below `delta`;
2. (FW292.1) forbids every new rooted depth in `[delta,D-1]`.

Thus the shallow factors `F_delta` themselves must have zero convolution
coefficient throughout `[delta,D-1]`.  At `D` there are exactly two
possibilities:

* `F_delta` already has coefficient one at `D`, and no new depth `D` may be
  added;
* its coefficient is zero, and exactly one factor acquires one vertex at
  rooted depth `D`.

There cannot be two depth-`D` vertices, or one added on each side, because
each pairs with the opposite root and would make the return coefficient at
least two.  Depth multiplicities are also forbidden by global distance
injectivity.

## 3. Exact convolution pruning

The shallow convolution supports after the first hole are:

```text
delta   F_delta                                    positive offsets >=delta
  1     {0} * {0}                                  none
  2     {0} * {0,1}                                none
  3     {0} * {0,1,2}                              none
  4     {0,1} * {0,2}                              none
  5     {0,1,4} * {0,2}                            6
  6     {0,1} * {0,2,4}                            none
  8     {0,1,4,5} * {0,2}                          none
  9     {0,1,4,5,8} * {0,2}                        10
 10     {0,1,4,5} * {0,2,8}                        12,13
```

Hence the zero block immediately forces

```text
delta=5  => eta=1,
delta=9  => eta=1,
delta=10 => eta in {1,2}.                           (FW292.3)
```

For `delta=5,eta=1`, `delta=9,eta=1`, and
`delta=10,eta=2`, the displayed next shallow sum is already the exact return.
Every other coefficient-compatible row must add depth `D` to exactly one
factor.

## 4. Rooted-tree compatibility and the exceptional row

Each finite depth support must be realizable by a rooted weighted tree whose
internal pair distances are unique.  The two factors' internal distance sets
must also be disjoint, since they are actual pairs in disjoint sides of the
same global tree.

Exhaustive parent-map reconstruction proves that both possible depth-`D`
extensions are compatible in every coefficient-compatible row except

```text
(delta,eta)=(8,1),   D=9.                            (FW292.4)
```

Here

```text
F_8=({0,1,4,5},{0,2}).
```

Adding depth `9` to the first factor has no internally distance-injective
rooted realization.  Adding it to the second factor makes the internal root
distance `9`, while the unique rooted realization of `{0,1,4,5}` already has
internal distance `9`; the two sides collide.  Both orientations are
therefore impossible.

## 5. The 57 surviving parameter types

Combining (FW292.2)--(FW292.4), the exact local survivor table is

```text
delta=1,2,3,4,6 : every eta in E,
delta=5         : eta=1,
delta=8         : eta in E-{1},
delta=9         : eta=1,
delta=10        : eta in {1,2}.                     (FW292.5)
```

This is `5*9+1+8+1+2=57` types.  The excluded 24 consist of 23 shallow-gap
collisions and the single rooted-realizability obstruction `(8,1)`.

For every surviving row the replay records an explicit rooted parent-map
witness through `D`.  Such a witness proves only that this bounded local test
does not contradict the row; it is not a complete weighted tree and is not a
Leech-compatible extension.

## 6. Matched two-root connector split

At the `q` cut, `U*Lambda` independently has first hole `eta`.  The two inner
factors are correlated by the actual `B` vertices:

```text
lambda_v+rho_v=ell+2h_v.                            (FW292.6)
```

There is nevertheless one exact consequence before full vertex matching.
Let the two inner roots be `x,y`.  If a positive value `j` occurs in both
shallow supports, then the pairs

```text
{x,v_j},   {y,w_j}
```

both have distance `j`.  Global injectivity makes them the same unordered
pair.  If `x!=y`, this forces `v_j=y`, `w_j=x`, and

```text
j=ell=d(x,y).                                      (FW292.7)
```

Hence, for distinct connector roots, the positive intersection of the two
shallow supports has size at most one.  More precisely:

```text
empty intersection       => ell>=min(delta,eta),
singleton intersection j => ell=j,
two or more values        => ell=0.                (FW292.8)
```

For `ell=0`, the two roots coincide and `lambda_v=rho_v` for every `v`, so
the two supports must agree through `min(delta,eta)`.  Here the endpoint is
included: a first hole at `k` says that neither rooted factor has depth `k`,
because the opposite factor contains its root at depth zero.

FW283's thin-bouquet audit fixes the inner `B` factor in the extremal rows:

```text
eta 8  => {0,1,4,5},
eta 9  => {0,1,4,5,8},
eta 10 => {0,1,4,5}.                               (FW292.9)
```

Applying (FW292.8) to all 57 rows first gives the support-level split

```text
54 rows retain at least one candidate distinct-root signature,
(delta,eta)=(8,8),(8,9),(8,10) force ell=0.        (FW292.10)
```

The tree-metric relations

```text
|lambda_v-rho_v|<=ell,
lambda_v+rho_v == ell (mod 2)                     (FW292.11)
```

remove four of the 54 candidate distinct-root signatures:

```text
(6,8), (6,9), (6,10), (8,6).                     (FW292.12)
```

In each case the extremal inner factor contains `{0,1,4,5}` (and for first
hole `9`, also `8`), while the first-hole-six inner factor is either `{0,1}`
or `{0,2,4}`.  Their unique common positive depth forces respectively
`ell=1` or `ell=4`.  For `ell=1`, the depth-`4` vertex must have
opposite-root depth `3` or `5`; for `ell=4`, the depth-`1` vertex must have
opposite-root depth `3` or `5`.  Both values lie below six and both are absent
from either first-hole-six factor.  Coincident roots are also impossible
because the two supports do not agree below six.

The three multi-intersection rows first force `ell=0`.  The row `(8,9)` then
dies: the first-hole-nine inner factor contains an actual depth-`8` vertex,
whereas the first hole at eight forbids depth `8` in the other inner factor.
Coincident roots would require these depths to be identical.

The final matched-shallow survivor table is therefore

```text
delta=1,2,3,4 : every eta in E,
delta=5       : eta=1,
delta=6       : eta in {1,2,3,4,5,6},
delta=8       : eta in {2,3,4,5,8,10},
delta=9       : eta=1,
delta=10      : eta in {1,2}.                     (FW292.13)
```

This leaves 52 types.  Fifty have an explicit separated two-root `B`
witness in the replay: choose compatible rooted realizations of the two
shallow inner factors, then join their roots by one sufficiently heavy edge.
Unique shallow sums and disjoint internal spectra make the resulting finite
`B` distance-injective, while the heavy connector keeps each opposite ball
beyond the other cutoff.

The other two are exactly `(8,8),(8,10)`.  They are not excluded: their
`Lambda` and `Rho` supports agree through the smaller first hole, so `ell=0`
remains locally consistent.

## 7. Strict stop and successor

Beyond (FW292.8), the first-hole tables do not identify which nonshared
shallow `Lambda` and `Rho` entries belong to the same vertex.  A vertex
shallow from one connector root can lie beyond the recorded prefix from the
other, and no local result bounds `ell`.  It is therefore unsound to
independently permute or forcibly pair the remaining supports.

> **STRICT STOP (FW292).**  Do not continue ERTC by extending bounded rooted
> supports one coefficient at a time.  The next step must enumerate or
> constrain actual matched rows `(v,lambda_v,rho_v,t_v,h_v)` and use complete
> coefficients beyond `D` together with nontrivial connector geometry.  The
> two forced-`ell=0` rows require a separate shared-root branch.

The smallest live successor is the **matched switchback extension problem**:
exclude complete-spectrum extensions of the 50 distinct-root witnesses and
the two shared-root rows in (FW292.13), or derive a strictly smaller matched
state from every such extension.  This is still part of unverified ERTC.

## 8. Replay and trust boundary

The clean-room finite replay is

```text
theory-lab/topwindow/verify_exact_return_prefix_classification.py
theory-lab/topwindow/results/exact_return_prefix_classification_certificate.json
```

It hard-codes the exact FW283 first-hole table, checks every coefficient
through `D`, enumerates every rooted parent map, freezes all 81 rows, and
stores a one-root witness for every member of the 57-row intermediate table,
plus 50 separated and two zero-connector matched-`B` witnesses.

**Proved:** the zero-block reduction, the exact 57-row classification, the
exclusion of `(8,1)` by rooted internal-distance compatibility, the matched
support intersection lemma, the four metric exclusions (FW292.12), the
same-root `(8,9)` exclusion, and the final `50+2` matched-shallow
classification.

**Not proved:** extension of any finite `B` witness to the full exact-return
tree, exclusion of the two `ell=0` rows, coefficients beyond `D`, ERTC,
SBCC, RCRT, PRCC, NSSC, G18, any new order exclusion, or global Leech-tree
nonexistence.

**Verdict: PROOF + EXACT FINITE/MATCHED-SUPPORT REDUCTION + STRICT PREFIX
STOP.**
