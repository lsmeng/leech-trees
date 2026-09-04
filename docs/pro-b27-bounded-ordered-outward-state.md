# Conditional bounded ordered-outward state

## Proposition

Work in the audited `b=27`, order-25 branch in which the following fifteen
vertices are already present:

```text
K = {d6,c,z,b1,b2,a,P0,P1,v34,u,v,y0,y3,p,q}.
```

Let `T` be any completion satisfying the same exact-return hypotheses and let
`U` be any outward high-edge subforest of the residual `J32` branch.  Then
`|V(T)\K| <= 10`.  Consequently the incidence data of `U` can be represented
by a finite state consisting of:

1. the vertices of `U` in `K` and their retained endpoint incidences;
2. at most ten named new vertices, with their rooted tree topology;
3. the low/fixed incidence marks and the rootward port of every retained low
   component; and
4. for each maximal high-only path whose internal vertices are unmarked
   degree-two vertices, the **ordered** tuple of its actual edge weights.

Every such state reconstructs the supplied outward subforest edge-for-edge.
Therefore it preserves all pair distances and owner identities *of the
retained subforest*.  Since every high edge has weight at least `38` and every
pair distance is at most `300`, any single ordered high arc has at most seven
edges.

## What this does and does not say

This proposition is a finite-state reduction conditional on the fixed
15-vertex branch and the exact-return hypotheses.  It does **not** say that
`NONE/PATH2/FORK2` exhausts the outward possibilities.  It also does not prove
that every state is compatible with the complete Leech spectrum, that every
low-component attachment is represented by the current catalogue, or that
the `L32`/`J32` branches are impossible.  Those are precisely the remaining
`Label-State Completeness` interfaces.

## Evidence

- `verify_pro_b27_vertex_budget.py` verifies `|K|=15` and the ten-vertex
  remainder under the stated branch hypotheses.
- `verify_pro_b27_high_branch_skeleton_partition.py --max-order 10` verifies
  the ordered-arc partition on the finite topology audit.
- `verify_pro_b27_ordered_outward_encoding.py --max-order 10` verifies that
  retaining ordered edge-weight tuples gives a lossless weighted reconstruction
  on the audited topologies.

The evidence is finite/conditional; the proposition is not a global
nonexistence theorem.
