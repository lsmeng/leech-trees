# Deterministic threshold projection lemma

This note separates a mathematical projection fact from the unresolved
surjectivity of the practical compressed generator.

## Full state and projection

Let `(K,x,s,cap4)` be a genuine named-vertex-preserving residual state in
`Good_res(U_res)`, conditional on the R2,t=4 branch entry, with literal edge
list and positive integer edge weights.  Threshold the edges of `K` at 37;
the bridge and cap remain separate typed reconstruction data.  Define:

1. `F_L(T)` as the subgraph of edges of weight at most 37, retaining every
   vertex and every literal low edge;
2. `tau_L` as the canonical rooted weighted-tree code of each low component;
3. `omega_L` as the owner/alias marks for the fixed packet and all currently
   forced low values;
4. `Pi` as the component partition, the unique rootward port of each
   non-root component, and **all** low/high boundary endpoint incidences;
5. `tau_H` as the rooted quotient obtained by contracting each low component,
   with every quotient vertex incident to a low component, a named vertex, or
   a high-subgraph degree different from two retained explicitly;
6. `I` as the two endpoint incidences of every high edge; and
7. `arc_subdivision_code` plus ordered high-weight tuples for each remaining
   maximal high-only path.

The projection is deterministic once the root, named vertices, and anonymous
slot canonicalization are fixed.

## Lossless reconstruction proposition

Assume the low components are connected subtrees, every boundary endpoint is
retained in `Pi`/`I`, and every maximal high-only arc stores its ordered
original edge weights.  Then materializing the projected tuple

```text
(tau_L, omega_L, Pi, tau_H, I, arc_subdivision_code,
 ordered_high_weight_tuples)
```

reconstructs the original residual weighted tree `K` edge-for-edge.  Together
with `(x,s,cap4)` it reconstructs the full tree `X`.  In particular it
preserves every unordered-pair path, distance, and owner endpoint.

**Proof.** Thresholding partitions the original edge set into disjoint low and
high edges.  The low component records reproduce every low edge.  Contracting
and then expanding each component using its literal edge list restores every
high endpoint and boundary edge recorded by `I`.  The marked quotient vertices
split the high subgraph uniquely into maximal high-only paths; their ordered
tuples restore every internal high edge and vertex.  Since the quotient is a
tree, no two expansions can rejoin or create an extra edge.  Thus the restored
edge list is exactly the original one, and all tree paths and weighted
distances agree. `QED` (conditional on the stated retention hypotheses).

## Exact remaining quantifier

The proposition gives

\[
  \forall (K,x,s,cap4)\in Good_res(U_res)\;\exists!\,P(K),
\]

where `P(K)` is the displayed compressed tuple.  It does **not** prove that a
particular implementation enumerates every value of `P(K)`.  That separate
surjectivity statement is

\[
  \forall (K,x,s,cap4)\in Good_res(U_res)\;\exists q\in
  \mathrm{GeneratedStates}: q=P(K),
\]

and is the current `Low-Catalogue/Label-State Completeness` gap.  Any generator
that omits a boundary endpoint, shared identity, or ordered arc subdivision
fails this implication even if its own finite run is internally consistent.

The existing finite port/skeleton round-trip audits verify the reconstruction
direction on bounded unweighted topologies.  They do not establish this
surjectivity for the corrected weighted 23-vertex residual state space, nor
the separate branch-entry implication.

## Unique high-quotient completion obligation

For each verified canonical low row `D_L`, every genuine full weighted
completion `T` must induce a rooted quotient `Q_H` satisfying:

1. contracting every low component of `D_L` gives a tree;
2. every non-root low component has exactly one parent/rootward high edge;
3. every high edge stores both actual endpoint incidences in the corresponding
   low/fixed or quotient vertices; and
4. every high-only degree-two subdivision vertex is retained in an ordered arc
   state.

Equivalently, the materialization map from
`(D_L,Q_H,endpoint incidences,ordered high-edge tuples)` to `T` must be
lossless and surjective onto all genuine completions of `D_L`.  The single
load-bearing acceptance condition is:

> No high edge or high branch may attach at an incidence point absent from
> `D_L` or `Q_H`.

This is the next theorem contract.  Once it holds, full pair distances, rooted
depths, LCAs, and owner identities are mechanically reconstructible; it still
does not assert that the practical generator has enumerated every `Q_H`.

In particular, the existing high-skeleton partition verifier has been checked
through order 10 (including `143654` marked arcs), and the ordered weighted-arc
round-trip covers `1809` rooted tree instances and `22515` marked cases.  These
are useful reconstruction checks for the `tau_H/I/arc_subdivision` fields, but
they are still finite graph audits: they do not prove that every fixed-`K`
incidence state appears in the practical generator.
