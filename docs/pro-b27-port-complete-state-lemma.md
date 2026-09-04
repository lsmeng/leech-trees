# Rooted low-component port decomposition

## Theorem (port-complete state for a fixed rooted tree)

Let `T` be a finite tree with root `r`, and let its edge set be partitioned
into low edges `E_L` and high edges `E_H`. Let `C_0` be the component of `r`
in the low-edge subgraph `(V(T),E_L)`. For every other low component `C`,
there is exactly one high boundary edge whose endpoint outside `C` is closer
to `r` than every vertex of `C`. The endpoint inside `C` is the unique
rootward port `p(C)`.

Moreover, the following state is lossless for the rooted edge-coloured tree:

```text
{ rooted low tree T[C], port p(C), carrier tag sigma(C),
  rooted high quotient, and both endpoint incidences of every high edge }.
```

The LCA of any two retained vertices and every weighted pair distance are
determined by the reconstructed tree; they do not need to be stored as extra
abstract metadata. In particular, if `H(C)=d_T(r,p(C))`, then for `x in C`

```text
d_T(r,x) = H(C) + d_C(p(C),x),
```

and distances within `C` are the distances in its recorded low tree. A path
between `x in C` and a vertex outside `C` may leave through a child-side
boundary vertex `q`, not necessarily through `p(C)`; the recorded endpoint
incidences identify that `q` and give
`d_T(x,y)=d_C(x,q)+d_T(q,y)`.

### Proof

Contract each connected low component to one quotient vertex and retain every
high edge, including its two original endpoint incidences. A quotient cycle
would lift to a cycle in `T`, so the quotient is acyclic. It is connected
because `T` is connected; hence it is a tree. Root the quotient at `C_0`.
Every non-root quotient vertex has exactly one edge to its parent. That edge
is the unique boundary edge of `C` directed toward `C_0`; all other boundary
edges, if present, lead to child components. This proves existence and
uniqueness of `p(C)`. Replacing each quotient vertex by its recorded rooted
low tree and restoring every high edge at its two recorded incidences gives
back `T` edge-for-edge. Therefore the rooted topology, LCAs, and weighted
distances are recovered exactly. `sigma(C)` is an additional carrier label
and does not alter the reconstruction.

This is a general combinatorial theorem, not a finite-order assertion.

## Corollary (ordered high-arc partition)

Let `H=(V,E_H)` be the high-edge subgraph of the same rooted tree. Mark the
root, every vertex whose degree in `H` is not two, and every degree-two vertex
that carries a low or fixed incidence. Then the maximal paths whose internal
vertices are unmarked degree-two vertices form a pairwise interior-disjoint
partition of `E_H`. Each path is an ordered arc between its marked endpoints.

Indeed, starting from any high edge and extending in both directions through
unmarked degree-two vertices is deterministic. The extension stops at a marked
vertex or at a degree-one endpoint, which is marked by the degree condition.
If two such arcs had a common interior vertex, that vertex would have two
distinct deterministic continuations and hence would belong to the same
maximal path, a contradiction. Every high edge is reached by this extension,
so the arcs partition the high edges. This is again an unrestricted tree
statement; it does not bound the number of arcs or their weights.

## Evidence and boundary for FW319

The implementation
`theory-lab/topwindow/verify_pro_b27_low_component_port_skeleton_roundtrip.py`
checks the extraction/reconstruction contract through order ten, including
all low/high edge partitions. The independent Prüfer-tree implementation
`theory-lab/topwindow/verify_pro_b27_low_component_port_skeleton_independent.py`
replays it without NetworkX through order six. Those runs are finite evidence
for the implementation; the theorem above supplies the unrestricted
tree-theoretic implication.

The exact depth and cross-distance identities are independently replayed by
`theory-lab/topwindow/verify_pro_b27_port_depth_decomposition.py` (labelled
Prüfer trees through order five, including every root and low/high partition),
with status `VERIFIED_PORT_DEPTH_DECOMPOSITION`. This replay intentionally
checks the child-side exit case and therefore does not smuggle in a false
rootward-port-only assumption.

To apply this state to the Leech-tree problem, a separate completeness result
is still required: every possible low-support/fixed-incidence decomposition
must be assigned to a covered state, with its carrier tags and allowed
attachment ports. The theorem does not bound the high quotient, prove the
complete punctured spectrum, establish least-remote minimality or inherited
descent, or exclude the remaining `L32` and `J32` branches.

Status: `VERIFIED_PORT_DECOMPOSITION_LEMMA`; global Label-State Completeness:
`GAP`.
