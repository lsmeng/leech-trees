# Literal-vertex retention lemma (conditional)

The first load-bearing question in the Weighted Incidence Lifting Lemma is
whether an external branch may attach at a point that the topology row has
suppressed.  Under the project's literal-tree convention this has a clean
conditional answer.

## Lemma

Assume a rooted realization is a finite tree whose edges are the original
edges (an attachment point in the interior of an edge is therefore a vertex,
and subdivides that edge).  Assume the rooted fragment contains at most ten
non-root vertices.  Then every actual attachment point of a low component,
high ordered arc, or owner path is an explicit vertex of some rooted topology
row with at most ten non-root vertices.

## Proof obligation and boundary

If an alleged attachment lies in the interior of an edge, that point is a
tree vertex by the literal-edge convention; the edge is split into two
original edges.  The resulting rooted tree has the same vertex budget and is
among the rooted topology classes.  Thus no genuine realization can require a
hidden midpoint.  The argument is conditional on two hypotheses that are not
yet branch-wide theorems: (i) the ≤10 fragment budget applies to every
J34--37 realization, and (ii) all relevant cross-component identifications can
be represented inside one such rooted fragment.

The existing topology generator does retain every vertex of each enumerated
row: its `tree_edges` use consecutive vertex IDs, have `order-1` edges, and
the owner path is represented by literal vertices.  The lightweight audit
`audit_pro_b27_literal_vertex_retention.py` checks these structural facts on an
artifact.  It cannot prove the two branch-wide hypotheses or attach the
missing semantic labels.

## What this does and does not close

**Conditional PROVED:** no suppressed *topological* attachment point is
needed once the literal-edge convention and the ten-vertex bound hold.

**Still GAP:** the topology row does not say which explicit vertex is attached
to which low component/high arc, does not record shared named identities, and
does not carry edge weights or the complete pair table.  Those fields remain
necessary for weighted incidence lifting and for any J34--37 exclusion.

## Advisor's exact acceptance rule

The extractor is sound only if it suppresses **unmarked vertices of full-tree
degree exactly two**.  Degree must be computed in the incidence-expanded full
tree, not just inside the owner-path fragment.  A locally degree-two vertex can
have a global external branch and hence degree at least three in the full tree.

The minimal counterexample is `A-x-C` with an extra branch `x-B`: suppressing
`x` and retaining only the total `A--C` length loses the attachment point and
therefore cannot reconstruct `d(B,A)` and `d(B,C)`.  This is a codec-failure
template, not a candidate Leech-tree counterexample.
