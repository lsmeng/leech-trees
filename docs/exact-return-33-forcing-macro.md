# Exact-return `(3,3)` seven-value forcing macro and full-range stop (FW298)

FW297 shows that a complete pre-target interval does not exclude the last
two-large-hole row.  FW298 keeps the complete-spectrum hypothesis and changes
coordinates: instead of extending another rooted prefix, it views the two
return edges in the increasing-edge-weight forced-forest process.

This gives an **all-order exact two-merge reduction**.  It also gives a
**STRICT STOP** for using only the three top caps and coarse rooted metrics:
an explicit full-range formal tiling survives those tests, including parity,
the first moment and every individual root-triangle constraint.  The formal
internal polynomial is not a tree metric.

## 1. The internal seven-value gap

Retain

```text
A -- q -- B -- r -- C,
p=w_q=g+3,   w_r=g,   delta=eta=3,   ell=0.
```

Write `D_int` for the disjoint union of the three internal distance spectra
of `A,B,C`.  Every cross-part path uses `r`, `q`, or both, so its distance is
at least `g`.  Complete Leech coverage therefore gives

```text
{1,...,g-1} subset D_int.                         (FW298.1)
```

The exact owner strip is

```text
g,g+1,g+2       BC,
g+3,g+4,g+5     AB,
g+6             BC.                              (FW298.2)
```

All seven owners cross between two of the parts.  Global owner uniqueness
therefore gives the exact internal gap

```text
D_int intersect {g,...,g+6}=empty.                (FW298.3)
```

In particular no edge internal to `A,B`, or `C` has weight in this block.
This uses all seven actual owners, not merely their coefficient values.

## 2. Consecutive forced merges

Let `F_<g` contain all edges of the hypothetical tree whose weights are less
than `g`.  An owner path of total weight less than `g` uses only such edges.
By (FW298.1),

```text
Spec(F_<g) contains {1,...,g-1}, and g is absent.  (FW298.4)
```

Thus the forcing lemma makes `r`, of weight `g`, the next edge.  The common
`B` root has actual depths `0,1,2`.  The exact return supplies one actual
root-depth-six vertex in `B` or `C`; because `g>=7`, all edges on that path
already lie in `F_<g`.  Adding `r` therefore creates

```text
g,g+1,g+2,g+6,                                    (FW298.5)
```

while the zero block in `Lambda*W` forbids `BC` owners at
`g+3,g+4,g+5`.  The internal gap forbids same-part owners there, and `A` is
still disconnected, so no `AB` or `AC` owner exists yet.  The next missing
distance is consequently `p=g+3`, and the forcing lemma makes `q` the next
edge.  Within the seven-value block, its pairs with the common root and the
depth-one/depth-two `B` vertices create exactly

```text
p,p+1,p+2 = g+3,g+4,g+5.                          (FW298.6)
```

Hence `r=g` and `q=g+3` are consecutive edge weights and consecutive forced
component merges.  Together they fill the entire seven-value block
`[g,g+6]`; either insertion may also create distances above that block.  The
next edge weight, if any, is at least `g+7`.

> **SEVEN-VALUE FORCING MACRO (FW298).**  Every complete-spectrum
> `(3,3),ell=0` exact return contains the consecutive forced merge
> `r=g`, then `q=g+3`, sharing the `B` root and converting the internal
> seven-value gap into a complete global seven-value block.

The FW297 order-seventeen tree is an actual pressure control.  Before `r` its
low-edge forest covers `1,...,9`; after `r=10` it contains
`10,11,12,16`; after `q=13` it covers the whole prefix through `18`.  Thus the
macro is not itself a contradiction.

## 3. A full-range formal pressure tiling

The following example tests whether the full coefficient identity and the
three cap inequalities alone can close the row.  It is deliberately a formal
factor state, not a weighted tree.  Put

```text
n=9, N=36, (|A|,|B|,|C|)=(1,7,1),
g=7, p=10,
U=W={0},
Lambda=Rho={0,1,2,6,20,21,26},
I_A=I_C=0,
I_B={1,2,3,4,5,6,14,15,18,19,20,21,22,23,24,25,26,29,32,34,35}.
                                                               (FW298.7)
```

Direct expansion gives the coefficientwise identity

```text
X+...+X^36
 = I_B + X^10 Lambda + X^7 Lambda + X^17.          (FW298.8)
```

Every coefficient is one and there are no outliers.  The common factor has
the required coefficients `1,1,1,0,0,0,1` through degree six.  The three
maximum constraints hold:

```text
0+26+10=36,       26+0+7=33<=36,       0+0+17=17<=36.
```

Several stronger necessary rooted-metric tests also pass:

* every positive rooted depth belongs to `I_B`;
* the rooted parity classes have orders `5|2`, and `I_B` has exactly ten odd
  distances;
* the necessary radius/diameter inequality
  `max I_B=35<=2 max Lambda=52` holds (neither quantity is asserted to come
  from a realized tree);
* with `S=sum Lambda=76` and `W_B=sum I_B=378`, the universal rooted-tree
  first-moment bounds `S<=W_B<=(|B|-1)S` hold;
* the fifteen nonroot vertex pairs can be bijected with the fifteen remaining
  values of `I_B` so that every assigned distance satisfies its individual
  triangle and parity conditions relative to the two rooted depths.

Nevertheless, a rooted tree with distinct depths in increasing order chooses
for each nonroot vertex one parent of smaller depth.  Exhausting all

```text
1*2*3*4*5*6 = 720
```

parent maps for (FW298.7) finds zero whose internal spectrum is exactly
`I_B`.  This is exhaustive for a rooted tree on these seven specified
vertices: distinct positive root depths force every parent to have smaller
depth, and the prescribed order leaves no hidden intermediate or Steiner
vertices.
Therefore the formal state is not a tree metric.  Its role is narrower and
exact:

> **FULL-RANGE COARSE-INVARIANT STOP (FW298).**  Complete coefficients, the
> shared factor, all three top caps, parity, the necessary radius/diameter
> inequality, the rooted first moment and independently feasible pair
> triangles do not exclude `(3,3)`.
> A valid proof must use coherent parent/LCA data, not only scalar or
> pair-by-pair consequences of rooted-tree realizability.

Because (FW298.7) is not a tree, it also does not instantiate nontrivial
full-window sink geometry.

## 4. Smallest live successor

The seven-value macro supplies a bounded event in the increasing-weight
Kruskal/forced-forest history.  The formal tiling identifies the information
that is still missing.  The weakest live successor is the
**Rooted-LCA Merge Obstruction**:

> In a complete-spectrum exact-return `(3,3),ell=0` state with nontrivial
> sink, the coherent rooted parent/LCA structures of `A,B,C` cannot realize
> the full three-part identity across the consecutive forced merges
> `r=g`, `q=g+3`; or those two merges produce a strictly smaller inherited
> forced-forest state.

This is **UNVERIFIED**.  It is stronger than the false pre-target lemma but
more specific than the original Full-Range Three-Part Tiling Lemma: it names
the exact missing data and a finite event in the edge-order history.

## 5. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_33_forcing_macro.py
theory-lab/topwindow/results/exact_return_33_forcing_macro_certificate.json
```

It checks the actual FW297 owners and low-edge forests, the formal
coefficient identity and caps, all listed coarse rooted invariants, the
explicit pairwise metric assignment, and all 720 rooted parent maps.

**Proved:** (FW298.1)--(FW298.6) and the seven-value forcing macro.

**Verified pressure evidence:** the actual FW297 macro control and the formal
full-range tiling (FW298.7)--(FW298.8), with individual triangle/parity
constraints but no coherent common-LCA realization or sink geometry.

**Not proved:** rooted-tree realizability of the formal tiling (it is
disproved), the Rooted-LCA Merge Obstruction, exclusion of `(3,3)`, ERTC,
NSSC, an order exclusion, G18, or global nonexistence.

**Verdict: EXACT FORCED-MERGE REDUCTION + STRICT COARSE FULL-RANGE STOP.**
