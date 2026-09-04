# Far-neighbour common cone

**OBSERVED theorem.** Near-diameter neighbours of a fixed vertex cannot occupy
several local branches. This is a shape-independent tree-metric fact and is the
next geometric restriction on the connected Leech top window.

## Statement

Let `T` be a positively weighted tree of diameter `N`, fix `q` with `2q<N`,
and let

```text
F_q(z) = {x : d(z,x) >= N-q}.
```

All geodesics from `z` to vertices of `F_q(z)` share an initial segment of
weighted length at least

```text
N/2-q.
```

In particular, all q-far neighbours of `z` lie in the same component of
`T-z`: every q-far edge incident with `z` points in one tree direction.

For a Leech tree, combine this with top-window connectivity and far-pair
crowding. The far-pair graph `H_q` is connected, every active vertex has one
far direction in `T`, and diameter-endpoint domination gives the sharper bound

```text
diameter_hop(H_q) <= 3.
```

Thus every active top-window vertex is one far edge from a fixed diameter
endpoint, independent of `q` and of the order `n`.

## Proof

For `x,y` in `F_q(z)`, the length of the common initial segment of the paths
`[z,x]` and `[z,y]` is their Gromov product in the tree:

```text
(d(z,x)+d(z,y)-d(x,y))/2.
```

Both first terms are at least `N-q`, while `d(x,y)<=N`, so this is at least
`N/2-q`. Rooted tree paths never rejoin after diverging. Therefore pairwise
agreement through that depth implies that the whole finite family of paths
shares one common initial segment of the stated length. Since `2q<N`, the
segment has positive length, and all paths begin along the same edge at `z`.

For the Leech corollary, diameter-endpoint introduction says every active
vertex is adjacent in `H_q` to `a` or `b`, and `a-b` is itself an edge. Hence
two active vertices are joined through `a`, through `b`, or through `a-b` in
at most three edges. `QED`

## Computational audit and trust boundary

`theory-lab/topwindow/verify_far_neighbor_cone.py` checks every threshold
change with `2q<N` at every root of 1,100 deterministic random positive
weighted trees of orders 4 through 14. It independently reconstructs every
rooted path and checks 213,120 pairwise Gromov products plus 37,518 full-family
common prefixes; 27,735 cases contain multiple far neighbours.

Run:

```text
nice -n 10 python3 theory-lab/topwindow/verify_far_neighbor_cone.py
```

The frozen summary is
`theory-lab/topwindow/results/far_neighbor_cone_certificate.json`.

This theorem forces one local direction at each active vertex; diameter
domination removes long far-pair handoff chains entirely. It does not yet show that the corresponding
long common cones are nested in a strictly decreasing sequence of components,
nor that their terminal branch profiles are impossible. That final descent
step remains **UNVERIFIED**.
