# Canonical incidence-state lemma (conditional FW319 bridge)

This note records a structural representation lemma suggested by the external
mathematical review and checked against the endpoint-incidence round-trips.  It
is not a claim that the current finite catalogue is complete.

## Statement

Let `T` be a finite positively edge-weighted tree in the audited `b=27`
branch, and let `K` be the named, connected literal fixed subtree with root
`r=d6`.  Split edges outside `K` into

\[
E_{\rm low}=\{e:w(e)\le 37\},\qquad
E_{\rm high}=\{e:w(e)\ge 38\}.
\]

Define `C(T)` to contain:

1. every connected component of the low-edge forest outside `K`, with its full
   weighted tree and named/anonymous vertex identities;
2. the rooted quotient obtained by contracting those components and retaining
   `K`;
3. for each non-root low component, its unique rootward high boundary edge and
   every outward high boundary edge, including the actual endpoint on each
   side;
4. the maximal high-only arcs after marking `r`, every high-degree-not-two
   vertex, and every vertex incident to `K` or a low component, with each arc's
   ordered internal vertices and ordered edge-weight tuple; and
5. the actual unordered owner endpoint/path data for the designated values
   `5,21,32,34,35,36,37`, whenever those owners are part of the hypotheses.

Then every such `T` has a state `C(T)`, and `C(T)` reconstructs `T`
vertex-for-vertex and edge-for-edge (up to renaming only genuinely anonymous
vertices).  Consequently it preserves every pair distance, rooted depth/LCA,
edge incidence, and owner identity.  If anonymous vertices are canonically
labelled while named vertices are held fixed, isomorphic rooted weighted trees
have the same canonical key.

## Proof

Contract each connected low component outside `K`.  A connected-subgraph
contraction of a tree is a tree, so the quotient has exactly one first edge on
the path from a non-root component to `r`; this is its rootward incidence.  All
other boundary incidences point childward.  Contracting all components at once
does not create a cycle, so these choices are compatible across components.

In the remaining high subgraph, mark the stated vertices.  Every unmarked
degree-two run is a unique maximal high-only arc.  Arc interiors are disjoint,
and retaining the ordered vertices and ordered weights restores each original
high edge.  Expanding the low components and `K`, then restoring every saved
boundary incidence, therefore recovers the original tree exactly.  Any
distance, LCA, or owner path is a function of this recovered edge-labelled
tree, so it is preserved.

## Evidence and boundary

The repository's independent port/skeleton round-trip has now been run on
Geo Workstation through `max-order 10`, covering `680,961/680,961` low/high
partitions and `3,657,039` components.  This is implementation evidence for
the incidence representation, not the source of the theorem's universal
quantifier.

The missing implication remains the catalogue-coverage statement

\[
\forall T,\quad \operatorname{key}(C(T))
  \in \mathscr C_{\rm current\ catalogue}.
\]

The current work still does not prove that all low forests, all ordered high
arcs, all `34--37` owner geometries, the `t\ge86` tail, or the
least-remote/inherited-descent conditions are present in the finite catalogue.
No finite replay here is a global `b=27` non-existence proof.
