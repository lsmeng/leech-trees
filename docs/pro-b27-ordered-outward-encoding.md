# Ordered outward encoding audit

## Verified finite replay

`theory-lab/topwindow/verify_pro_b27_ordered_outward_encoding.py --max-order 10`
enumerates every non-isomorphic tree of orders one through ten, every root,
and every subset of degree-two incidence marks.  It compresses each maximal
unmarked degree-two path to an ordered edge-weight tuple, rebuilds the graph
with fresh interior names, and compares the complete weighted all-pairs
distance multiset.  The replay returned
`VERIFIED_ORDERED_OUTWARD_ENCODING` with `1,809` rooted tree instances,
`22,515` marked instances, and `143,654` arcs.

An independent stdin-only implementation on `geo-workstation` reproduced the
same status and all three aggregate counts using NetworkX 3.1, without reading
or writing the checkout.

This is a representation audit supporting the bounded ordered-outward state:
the tuple encoding preserves the tested distance data even when subdivision
changes the intermediate edge partition.  It complements
`VERIFIED_HIGH_BRANCH_SKELETON_PARTITION` at the same ten-vertex budget.

## Trust boundary

The replay is finite and graph-theoretic.  It does not prove that every
Leech labeling realizes a state, does not enumerate label-owner assignments,
and does not close `Label-State Completeness`, complete-spectrum reception,
least-remote minimality, or global `b=27` nonexistence.
