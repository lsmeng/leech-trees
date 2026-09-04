# Exact-return unit-owner alignment (FW294)

FW293 removes the two parameter types that can survive only with coincident
inner roots.  FW294 now compares the actual owners of global distances one
and two across the two first-hole factorizations.  It excludes 20 more of the
remaining 50 types.

This is a **PROVED actual-owner reduction from 50 to 30 parameter types**.  It
does not prove that any of the 30 types extends to a complete exact-return
state, and it does not prove ERTC.

## 1. The distance-one owner is shared

Retain the two-cut partition

```text
A -- q -- B -- r -- C
```

and the rooted factors `U,Lambda,Rho,W` from FW291.  Suppose
`delta,eta>=2`.  Both first-hole convolutions have coefficient one at offset
one:

```text
[X](U*Lambda)=1,   [X](Rho*W)=1.                   (FW294.1)
```

Every rooted factor has one root at depth zero.  The only decompositions of
offset one are `0+1` and `1+0`, so exactly one factor at each cut contains one
rooted depth-one vertex.  That vertex and the corresponding root form an
actual unordered pair of global distance one.

The two distance-one pairs must be the same pair, by global distance
injectivity.  A pair internal to `A` cannot equal a pair internal to `B` or
`C`, and similarly at the other cut.  Hence both owners lie in `B`:

```text
1 in Lambda,   1 in Rho,   1 notin U,W.             (FW294.2)
```

This fixes the orientation of every FW283 row with first hole at least two:
the inner factor is the unique factor containing depth one.

Let `x,y` be the `Lambda,Rho` roots.  Equality of the two owner pairs gives
exactly two possibilities:

* `x=y`, and the same rooted depth-one vertex is seen twice;
* `x!=y`, the two vertices are `y,x`, and `d(x,y)=ell=1`.

Thus optional zero-connector signatures are retained; FW294 does not silently
assume that the roots are distinct.

## 2. The distance-two owner

Now suppose also `delta,eta>=3`.  Because (FW294.2) puts depth one only in the
inner factor, the `1+1` decomposition is absent.  Coefficient one at offset
two therefore supplies exactly one actual root-to-depth-two owner at each
cut.

The oriented FW283 rows give

```text
first hole 3:   inner={0,1,2},       outer={0};
first hole k>=4 inner contains 1 but not 2, outer contains 2. (FW294.3)
```

Here `k` ranges over the allowed values `4,5,6,8,9,10`.

The two distance-two owner pairs must again be identical.  There are three
cases.

1. If both first holes are at least four, the owners lie respectively in the
   disjoint parts `A` and `C`, impossible.
2. If exactly one first hole is three, one owner lies in `B` and the other in
   `A` or `C`, impossible.
3. If `(delta,eta)=(3,3)`, both owners lie in `B`.  Distinct roots are still
   impossible: distance-one equality gives `ell=1`, while equality of the
   two root-depth-two pairs would give `ell=2`.  Coincident roots are not
   contradicted, so this row remains only on the `ell=0` face.

Consequently every current type with `delta,eta>=3` is excluded except
`(3,3)`.

## 3. Exact parameter table

The 30 types not excluded by FW294 are

```text
delta=1  : eta in {1,2,3,4,5,6,8,9,10},
delta=2  : eta in {1,2,3,4,5,6,8,9,10},
delta=3  : eta in {1,2,3},
delta=4  : eta in {1,2},
delta=5  : eta=1,
delta=6  : eta in {1,2},
delta=8  : eta=2,
delta=9  : eta=1,
delta=10 : eta in {1,2}.                            (FW294.4)
```

The 20 new exclusions are

```text
(3,4),(3,5),(3,6),(3,8),(3,9),(3,10),
(4,3),(4,4),(4,5),(4,6),(4,8),(4,9),(4,10),
(6,3),(6,4),(6,5),(6,6),
(8,3),(8,4),(8,5).                                 (FW294.5)
```

The known `L6` exact-return control has `(delta,eta)=(3,1)`.  Since the
`q`-cut has its first hole already at one, the simultaneous distance-one
premise of FW294 fails; the control is not rejected.

## 4. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_unit_owner_alignment.py
theory-lab/topwindow/results/exact_return_unit_owner_alignment_certificate.json
```

It rebuilds the FW283 factor table, selects the unique depth-one inner
orientation, locates the depth-two owner, imports the exact FW292 52-type
matched table and the two FW293 exclusions, and classifies all 50 remaining
types.

**Proved:** the distance-one owner alignment, the distance-two owner split,
the 20 exclusions in (FW294.5), and the 30-row necessary table (FW294.4).

**Not proved:** local or complete extension of any of the 30 rows, exclusion
of `(3,3)` on its `ell=0` face, coefficients beyond `D`, ERTC, SBCC, RCRT,
PRCC, NSSC, G18, any new order exclusion, or global Leech-tree nonexistence.

**Verdict: PROOF + EXACT 50-TO-30 OWNER REDUCTION.**
