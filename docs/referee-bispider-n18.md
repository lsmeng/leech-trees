# Adversarial review of the no-bi-spider theorem for n>=18

**OBSERVED referee verdict — SOUND, 2026-08-21.**  Under the documented
ordinary-Python verifier, the computer-assisted conclusion

> no Leech tree of order `n>=18` has at most two branch vertices

follows from the written reductions and the paired finite searches.  I found
no missing anchor orientation, parameter region, endpoint role or unsound
pruning condition in the final version.  This verdict does not address trees
with three or more branch vertices, and it does not prove the stronger
`n>=7` bi-spider conjecture.

## 1. Claims and trust boundary reviewed

The load-bearing sources are the seven `LR` verifier pairs listed in
`theory-lab/catspider/README.md`, the three `LL` searches in
`bispider_ll_prover.py`, their region-specific clean-room counterparts, and
`verify_bispider_ll.py`.  The mathematical reductions are in
`docs/bispider-progress.md`.  The fixed-order C runs are calibration, not the
reason an infinite range is covered.

No SAT witness occurs in these nonexistence computations.  If a future run
does produce a witness, it remains mandatory to pass both `src/checker_a.py`
and `src/checker_b.py`.

## 2. Exhaustive anchor normalisation

In a finite tree, a diameter pair consists of leaves.  With at most two branch
vertices, contract the degree-two layout conceptually to two centres joined by
a path, retaining every original vertex as a positive integral mark on a leg
or on that path.  Up to reflection, a pair at the unique maximum distance
`N=binom(n,2)` is either:

```text
LR: one tip on each side;
LL: two tips on the same side.
```

The cases are exhaustive even when one or both centres have degree two: the
description then degenerates to a spider or path and is still represented.
The seven LR regions form a written disjoint cover for `n>=18`.  The present
review concentrated on the new LL half.

For LL tips of depths `T>U`,

```text
N=T+U,       delta=T-U,       1<=Q<U,       L=U-Q.
```

Every other left tip has depth `<U`; every right tip has depth `<L`.  Equality
would create a second pair at distance `N`, while a larger value would exceed
the diameter.  A non-long vertex has radial distance `U-z` from the left
centre.  The roles and strict boundaries are:

```text
short-left mark: 0<=z<U;
right-leg mark:  0<z<L;
right centre:    z=L;
spine mark:      L<z<U.
```

Two distinct vertices cannot have the same `z`, because their distances to
the left centre would then coincide.  This justifies the global `z`
uniqueness used in all three searches.

## 3. LL top-window classification

Set `W=36`.  Since `n>=18`, `N>=153`.  Exactly one of the following holds.

### Small second tip: `2<=U<=36`

Here `delta=N-2U>=81>W`, so a pair avoiding the long leg cannot reach
`N-W`.  A high pair is either on different left-centre branches or uses the
two separated ends of the long leg.  With `a` the long-tip deficit and `x`
the long-leg depth from the centre, its offset is exactly

```text
a+z       or       U+a+x.
```

The clusters cannot overlap: `T-a >= N-U-W > W-U >= x`.  The legal table
`2<=U<=36`, `1<=L<U` has 630 entries.

### Large second tip, near far centre: `U>36`, `1<=L<=36`

Same-long-leg pairs leave the window.  The exact high forms are

```text
a+z       and       delta+z+z'
```

with the second pair on different left-centre branches.  A pair on different
right legs has base offset

```text
rho=delta+2Q=N-2L>=81,
```

so it is absent here.  Exact `delta=1,...,36` plus sentinel 37 and exact
`L=1,...,36` give 1,332 entries.

### Large second tip, remote far centre: `U>36`, `L>36`

This was the main adversarial boundary.  It is incorrect to delete the entire
far side merely because its centre has left the window: a mark near a right
tip can still have bounded deficit `c`.  The final classification retains all
three forms

```text
a+z,
delta+z+z'              on different left-centre branches,
rho+c+c'                on different right legs,
rho=delta+2Q=N-2L.
```

The first draft omitted the last class; that draft was rejected before
promotion.  The corrected table contains every compatible exact pair through
36, one `rho>36` sentinel for every exact `delta`, and the joint large-large
sentinel: 343 entries.  `bispider_ll_prover.far_regimes` and the independently
written clean-room table are compared literally by the final verifier.

These three cases are pairwise disjoint and exhaustive.  Sentinels are safe:
once `delta` or `rho` exceeds `W`, its whole nonnegative-offset class has left
the high window.  The implementations then omit parameter-dependent low
collisions rather than imposing guessed ones, which enlarges the search.

## 4. Why zero frontier is a proof

Each state records selected bounded endpoint deficits.  Its retained
conditions are necessary equal-distance exclusions: high offsets, same-leg
differences and the relevant different-branch sums must be unique.  Some
cross-class collisions, all invisible vertices and the global vertex budget
are deliberately omitted.  Therefore a retained state may be spurious, but a
valid Leech partial tree is never rejected by an omitted condition.

At a state, take the least absent offset `k` in `1,...,36`.  In an actual
Leech tree, `N-k` must occur.  Section 3 puts its endpoints in one of the
enumerated forms.  Adding the previously unselected endpoint or endpoints
therefore maps the actual tree to a child.  Induction gives a path to a state
containing all 36 offsets.  Such a state is called a frontier state, so zero
frontier contradicts the existence of the actual tree.

Canonicalising interchangeable legs is only a symmetry quotient.  The long
anchor leg and the leg containing the `U` anchor tip remain distinguished;
the remote-side legs are permuted only among themselves.

## 5. Independent implementation and reproduction checks

The final W=36 comparison covers every finite regime:

| LL region | regimes | states | deepest missing offset | frontier |
|---|---:|---:|---:|---:|
| `U>36,L<=36` | 1,332 | 433,069 | 28 | 0 |
| `U>36,L>36` | 343 | 89,723 | 36 | 0 |
| `2<=U<=36` | 630 | 217,802 | 20 | 0 |
| total | 2,305 | 740,594 | 36 | 0 |

The primary code uses one canonical graph walker and three placement
routines.  The clean-room side uses three separately written immutable
searches; the small-`U` program uses a layered DAG traversal instead of DFS.
They import no search code from one another and agree on every per-regime row,
including children, dead states, depth and selected-vertex maxima.  The
verifier rejects `python -O/-OO` and uses explicit exceptions for all
certificate comparisons.

Additional checks are deliberately non-load-bearing but useful:

- the verifier maps 624,389 actual LL anchors at orders 18 through 40 into
  exactly one table entry;
- the paranoid C engine recomputes distances and closes all 2,825 order-18 LL
  anchors in 723,912 states with zero solutions;
- W=35 leaves eight remote-region frontier states, all in the `delta=3`,
  `rho>35` row; W=36 closes them, while W=37, 40, 45 and 50 remain closed.

The paired programs share the mathematical top-window classification, so they
are independent implementations rather than two independent mathematical
proofs.  The classification and sentinel argument in Sections 2--4 are the
human-audited part of the trust boundary.

## 6. Verdict and remaining claims

The LL reduction is exhaustive for every `n>=18`, its relaxation direction is
safe, and its finite searches have zero frontier in two per-regime-matching
implementations.  Together with the previously audited LR cover, the stated
no-bi-spider theorem is sound.

The following remain **UNVERIFIED**:

- exclusion of bi-spiders throughout the stronger range `7<=n<=17` by a
  uniform argument;
- exclusion of any tree with at least three branch vertices;
- the global descent/thick-tip programme for all `n>=18`.
