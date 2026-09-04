# Diameter-endpoint introduction

**OBSERVED theorem.** This strengthens the anchored one-vertex completion
lemma. In a descending distinct-distance search, every new vertex is first
introduced by a pair with one of the two fixed diameter endpoints.

## Statement

Let `T` be a positively weighted tree with distinct vertex-pair distances, and
let `a,b` be its unique diameter pair of distance `N`. If `(x,y)` is disjoint
from `(a,b)`, then one of the two cross orientations satisfies

```text
d(a,x)>d(x,y) and d(b,y)>d(x,y),
```

or the same inequalities with `x,y` interchanged.

Consequently, when all pairs longer than a target value `v` have already been
processed, a pair of length `v` disjoint from `(a,b)` has both endpoints already
present. A new vertex at level `v` can only be introduced by `(a,x)` or `(b,x)`.

Equivalently, at every distance threshold the non-isolated far-pair graph is
dominated by `{a,b}`; it is connected and has graph hop-diameter at most three.
For a Leech tree, the pairs at distances `N,N-1,...` therefore admit an exact
top-down search with only two types of step:

1. introduce one vertex through a prescribed distance to `a` or `b`; or
2. skip the target because it is already a distance between present vertices.

No introduction through an arbitrary previously selected vertex is needed.

## Proof

For four distinct vertices `a,b,x,y`, apply the tree four-point property to

```text
N+d(x,y),
d(a,x)+d(b,y),
d(a,y)+d(b,x).
```

At least one cross sum is at least `N+d(x,y)`. Suppose it is the second. Since
every distance is at most `N`, neither summand can be smaller than `d(x,y)`.
The pairs `(a,x)` and `(b,y)` are different from `(x,y)`, so global distance
distinctness makes both inequalities strict. Thus both `x` and `y` occur in
longer pairs. The other cross sum gives the reversed orientation.

If the target pair meets `a` or `b`, it introduces at most its other endpoint.
If it is disjoint, the strict-cross conclusion says both endpoints were already
introduced at higher levels. This proves the exhaustive two-step search rule.
The domination, connectivity and hop-diameter statements follow as in the
diameter-cap theorem. `QED`

## Engine reduction and audit

The exact three-centre engine retains both candidate modes:

```text
threebranch_exact n all --no-pairs
threebranch_exact n all --no-pairs --diameter-intro
```

The second generates a new mark only by pairing it with one of the two anchor
tips. `theory-lab/topwindow/verify_diameter_introduction.py` checks the strict
cross conclusion on 16,500 disjoint pairs in 900 deterministic random
distinct-distance trees. It then rebuilds the C engine and compares the two
candidate modes through orders 8--15. All 40,704,104 search nodes and
40,167,617 legal children agree exactly, while candidate marks fall from
705,215,286 to 294,821,373.

Run:

```text
nice -n 10 python3 theory-lab/topwindow/verify_diameter_introduction.py
```

The frozen summary is
`theory-lab/topwindow/results/diameter_introduction_certificate.json`.

This theorem sharply reduces a universal top-window engine to two diameter
stars plus already determined cross distances. It still does not enumerate all
possible off-diameter branching geometry, so global nonexistence remains
**UNVERIFIED**.
