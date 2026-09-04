# FW319 `b=27`: L ancestor-32 path-shape reduction

The remaining L branch is an ancestor--descendant owner of distance `32`,
with both endpoint edges already forced to have weight at least `6`.  This
audit enumerates its possible interaction with the fixed `b=27` L core.

## Enumeration

If an owner endpoint is fixed, its path has a fixed-core ancestor/descendant
segment followed by a chain of new vertices.  Every new edge weight and every
new-vertex pair distance must avoid the fixed spectrum and the reserved value
`4`; the full induced fixed-core subtree must remain distance-injective.  The
endpoint edge at the fixed ancestor is also required to be at least `6`.

If both owner endpoints are new, the ancestor path has left the fixed core
before the first endpoint and is an all-new chain.  Its first and last edge
weights are both at least `6`.  No distinct positive composition of `32`
with both endpoint weights at least `6` survives the fixed-spectrum edge
restriction: the only possible lower endpoint weight is `16`, and two such
edges would repeat an edge weight.

The fixed-core-plus-new-chain enumeration checks every remaining composition
and every fixed ancestor/attachment vertex.  Exactly two induced subtrees are
distance-injective:

```text
P0 --(32)-- new,
P1 --(32)-- new.
```

Each has maximum local distance `87`; all other candidates have an explicit
induced distance collision.  The two surviving shapes are therefore the only
L ancestor-32 shapes under the current endpoint-floor hypothesis.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_rootdiff32_shape.py
```

The replay returns `status: VERIFIED`.

## Boundary

This is a finite shape reduction, not an exclusion.  The surviving direct
`32` edge at `P0` or `P1` still needs to be combined with complete ownership
of `34,35,36,37`, the full exact-return spectrum, least-remote minimality, or
a strict inherited descent.
