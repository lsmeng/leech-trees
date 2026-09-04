# Anchored one-vertex completion lemma

**OBSERVED theorem.** This lemma is a shape-independent reduction for any
top-down distinct-distance tree search once a diameter pair has been selected.

## Statement

Let `T` be a positively weighted tree with distinct integer vertex-pair
distances, maximum distance `N`, and diameter endpoints `a,b` with
`d(a,b)=N`. Let a partial selected vertex set contain `a,b`, have no repeated
internal distances, and already realize every value

```text
v+1, v+2, ..., N
```

for some `v<N`. If the partial state extends to `T` and `v` is a distance of
`T`, then a pair realizing `v` has at least one endpoint already selected.
Consequently a descending greatest-missing-distance search never needs to add
two new vertices at one step: one new vertex is exhaustive.

## Proof

Tree metrics satisfy the four-point property: for any four vertices
`a,b,x,y`, the two largest of

```text
d(a,b)+d(x,y),
d(a,x)+d(b,y),
d(a,y)+d(b,x)
```

are equal. This follows directly from the minimal subtree spanning the four
vertices: after suppressing degree-two vertices it is either a four-way star
or two forks joined by a path, and the two pairings crossing the central path
have the same larger total.

Suppose for contradiction that both endpoints `x,y` realizing the current
greatest missing value are new, so `d(x,y)=v`. The first four-point sum is
`N+v`. Hence at least one of the other two sums is at least `N+v`. One of its
two summands is therefore strictly greater than `v`, since otherwise their
sum would be at most `2v<N+v`. Thus one of

```text
d(a,x), d(a,y), d(b,x), d(b,y)
```

is an integer `w` with `v<w<=N`.

The partial state already realizes `w`. Adding the corresponding new vertex
realizes `w` again with `a` or `b`, contradicting distinctness. Therefore a
valid extension cannot first realize `v` between two absent vertices. This
proves the claim. `QED`

## Computational audit and use

`theory-lab/threebranch/verify_one_vertex_lemma.py` checks the four-point and
strict-cross-distance implication on deterministic random weighted trees. It
then runs the exact three-centre engine through order 15 with the pair branch
disabled and compares every anchor, node, child and solution invariant with
the earlier conservative runs that explicitly enumerated pairs.

The engine retains both paths:

```text
threebranch_exact n all              # explicitly enumerate two-new pairs
threebranch_exact n all --no-pairs   # apply this lemma
threebranch_exact --pair-probe       # positive non-anchored two-new test
```

The synthetic probe has three legal two-new children, so agreement is not
caused by dead pair code. The lemma, rather than the finite zero count, is what
authorizes `--no-pairs` in later certificate searches.

This result reduces branching but does not by itself exclude any order or
topology. All order-25 and uniform three-branch conclusions remain
**UNVERIFIED**.
