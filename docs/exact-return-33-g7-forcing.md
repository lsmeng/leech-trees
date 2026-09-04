# Exact-return `(3,3)` `g=7` LCA and weight-sixteen reduction (FW299)

In the standing `n>=18` nonexistence regime, FW298 shows that every complete
`(3,3),ell=0` return contains the consecutive forced merges `r=g`, `q=g+3`.
FW299 resolves the smallest target weight
`g=7` through the next forced edge.  Coherent LCA data first forces the
depth-six return out of `B`; the resulting low-edge forest is unique.

This is an **all-order analytic reduction plus a complete ten-state finite
catalogue**, not an exclusion of `g=7`.

## 1. The depth-six owner cannot lie in `B`

Let `z` be the common inner root and let

```text
z--b_1=1,       z--b_2=2,       d(b_1,b_2)=3.
```

Suppose a vertex `v in B` has root depth six.  The depth-one edge has no
interior vertex, so `LCA(b_1,v)` is either `z` or `b_1`.  Likewise
`LCA(b_2,v)` is either `z` or `b_2`.  The two shallow vertices lie in
different root branches, so `v` can descend below at most one of them.  The
three possibilities are

```text
location of v          d(b_1,v)   d(b_2,v)
separate branch             7          8
below b_1                   5          8
below b_2                   7          4.          (FW299.1)
```

For `g=7`, the edge `r` already owns distance seven and the forced `BC` pair
`b_1--r--c` already owns distance eight.  Every row of (FW299.1) repeats one
of those actual owners.  Hence the unique return-side rooted depth six is in
`C`, not `B`.

## 2. The return is the edge of weight six

Every edge weight is itself a global distance.  The unique weights one and
two lie in `B`, while weight three is absent because the path
`b_1--z--b_2` already owns distance three.  A multi-edge positive-integer
path of total six with distinct edge weights has one of the sets

```text
{1,5}, {2,4}, {1,2,3}.
```

Every possibility uses a weight from `{1,2,3}`, none of which is available
inside `C`.  Thus the `C` root-depth-six owner is the single edge of weight
six.

FW296 already proves that distances four and five are also single-edge
weights.  For
completeness: the only distinct multi-edge partition of four is `1+3`; for
five the possibilities are `1+4` and `2+3`.  Weight three is absent, while
placing edge four next to the weight-one edge would give forbidden `B` root
depth four or five.  Therefore weights four and five are single edges.  Their
separation from all other sub-seven edges is proved next, after all five low
edge weights are available.

## 3. The unique forest below seven

Because `W` contains depth six and `Lambda` contains depths one and two, the
`BC` class additionally owns

```text
g+6+1=14,          g+6+2=15.                      (FW299.2)
```

Together with the FW291 strip, all values `7,...,15` have unique cross-part
owners: `7,8,9,13,14,15` are `BC`, while `10,11,12` are `AB`.  No same-part
path may realize any of them.

The only edge weights below seven are now `1,2,4,5,6`.  Apart from the forced
adjacency `1+2=3`, every possible adjacency of two of these edges gives either
a repeated edge value or a forbidden internal value in `[7,15]`:

```text
1+4=5, 1+5=6, 1+6=7,
2+4=6, 2+5=7, 2+6=8,
4+5=9, 4+6=10, 5+6=11.                            (FW299.3)
```

Consequently the threshold forest formed by all edges of weight below seven
is exactly

```text
the rooted 1--2 star  dotunion  edge 4  dotunion  edge 5  dotunion  edge 6,
```

plus unused isolated vertices.

## 4. The post-return forest and the next edge

Insert `r=7` between `z` and the root `c` of edge six.  Before inserting
`q=10`, its outer root `a` is still an isolated vertex of the forced forest.
Indeed, the only unassigned sub-seven edges are four and five.  If `a` were
an endpoint of edge four, its `AB` pairs with the `B` depths `0,1,2` would
create `14,15,16`, repeating the existing `BC` owners at `14,15`.  If it were
an endpoint of edge five, they would create `15,16,17`, repeating `15`.
Weights one and two are in `B`, and weight six is in `C`, so there is no other
low edge that can contain `a`.

Now insert `q=10` between `z` and this singleton outer root `a`.  On the
six-vertex component the edges are

```text
z--b_1=1, z--b_2=2, c--d=6, z--c=7, z--a=10.
```

Adding the separate weight-four and weight-five components gives the exact
forest spectrum

```text
{1,...,15} dotunion {17,23}.                      (FW299.4)
```

Thus the least missing value is sixteen, and the forcing lemma makes weight
sixteen the next edge.

At this point the nontrivial components have orders `6,2,2`.  Since `n>=18`,
there are enough unused vertices for both singleton attachment and new-edge
placements, and the pair cap is `N>=153`; every distance created below is at
most `44`.  A next edge can
only join two components, attach one unused vertex, or form a new single-edge
component.  There are

```text
6*2 + 6*2 + 2*2 + 10 + 1 = 39                   (FW299.5)
```

representative placements on the displayed ten-vertex prefix, after
quotienting the unused isolated vertices as symmetric.  Exact recomputation
leaves eighteen distance-injective prefix representatives.  Because every
edge weight is distinct, the multiset of vertex
incident-weight profiles reconstructs the weighted forest up to isomorphism;
it gives exactly ten canonical states (including the endpoint swaps of the
isolated weight-four and weight-five components).  Nine have next forced
weight eighteen; attaching weight sixteen at `b_2` also creates eighteen and
nineteen, so its next forced weight is twenty.

> **`g=7` FORCING REDUCTION (FW299).**  Every complete-spectrum exact-return
> `(3,3),ell=0,g=7` state passes through the unique low forest (FW299.3), the
> post-return spectrum (FW299.4), and one of ten canonical weight-sixteen
> states.

## 5. Strict stop and successor

The ten states are genuine distance-injective **uncoloured forced forests**.
They are a complete necessary relaxation: every full exact-return state must
map to one of them, but a listed forest is not asserted to admit compatible
`A/B/C` parts, roots, a nontrivial sink, or a complete extension.  Therefore
the coherent LCA argument and the uncoloured low-edge prefix do not yet
exclude `g=7`.

> **STRICT STOP (FW299).**  Do not infer a `g=7` contradiction merely from
> the side of the depth-six owner, the isolated `4,5,6` edges, or the forced
> edge sixteen.

The weakest live successor is finite and owner-aware: exclude or descend from
the nine next-weight-eighteen states and the one next-weight-twenty state by
retaining their actual `A/B/C` part, root and sink assignments.  Continuing a
generic uncoloured forest search is not a theorem and grows rapidly.

## 6. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_33_g7_forcing.py
theory-lab/topwindow/results/exact_return_33_g7_forcing_certificate.json
```

It checks the three LCA locations, all integer path partitions used above,
the complete adjacency table, the outer-root isolation collisions, the exact
post-return spectrum, the `n>=18` cap margin, all 39 weight-sixteen prefix
representatives, and the ten canonical necessary states.

**Proved:** the depth-six `C` location, the single edge six, the unique
sub-seven forest, the exact post-return spectrum, and the forced edge sixteen.

**Verified finite classification:** 18 distance-injective representatives on
the displayed prefix and ten canonical uncoloured weight-sixteen states; this
is a necessary relaxation, not a sufficient exact-return realization.  The
counts already quotient unused isolated-vertex labels.

**Not proved:** exclusion of any of the ten states, exclusion of `g=7`, any
other target weight, ERTC, NSSC, an order exclusion, G18, or global
nonexistence.

**Verdict: EXACT `g=7` REDUCTION + TEN-STATE STRICT STOP.**
