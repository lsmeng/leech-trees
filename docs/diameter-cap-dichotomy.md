# Diameter-cap/deep-offshoot dichotomy

**OBSERVED theorem.** This shape-independent lemma localises every
near-diameter pair relative to one fixed diameter. It is a geometric bridge
between the pole-cover theorem and the proposed thin/thick descent, but the
descent itself remains **UNVERIFIED**.

## Statement

Let `T` be any positively weighted tree with diameter endpoints `a,b` and
`d(a,b)=N`. A pair is *q-far* when its distance is at least `N-q`.

For every q-far pair `(x,y)`, its endpoints can be oriented as `(u,v)` so that

```text
d(a,u) >= d(x,y) >= N-q,
d(b,v) >= d(x,y) >= N-q.
```

Consequently the non-isolated part of the q-far graph is dominated by the two
diameter endpoints: every active vertex is q-far from `a` or from `b`. It is
connected and has graph hop-diameter at most three. This conclusion holds even
when distances are not distinct.

Let `c(u)` be the gate at which the path from `u` first meets the diameter path
`P(a,b)`, and put `h(u)=d(u,c(u))`. Then

```text
h(u) <= q  implies  d(u,b) <= q+2h(u) <= 3q,
h(u) > q   implies  u lies q-deep in a component off P(a,b).
```

The symmetric statement holds for `v`, with `a` and `b` interchanged.
Consequently every q-far pair has an orientation in which each endpoint is
either in the weighted `3q`-cap of the corresponding diameter endpoint or is
more than `q` deep in a proper off-diameter component. A deep endpoint is then
either q-thick (a branch vertex occurs within distance `q`) or q-thin (none
does), giving exactly the terminal/descent dichotomy required by the roadmap.

The theorem does not require distinct distances or the Leech interval property.

## Proof

First suppose `(x,y)` is disjoint from `(a,b)`. The tree four-point property
says that the two largest of

```text
N+d(x,y),
d(a,x)+d(b,y),
d(a,y)+d(b,x)
```

are equal. Therefore one cross sum is at least `N+d(x,y)`. If it is the second
sum, then neither summand can be smaller than `d(x,y)`: for example,
`d(a,x)<d(x,y)` would force `d(b,y)>N`, contradicting the definition of the
diameter. Thus choose `(u,v)=(x,y)`. The third sum gives the opposite
orientation. If the two pairs share an endpoint, the same orientation follows
directly; for example `(a,y)` is oriented as `(y,a)`.

For the metric localisation, write

```text
p=d(a,c(u)),  h=h(u).
```

Because paths from `u` to `a` and `b` meet the diameter at `c(u)`,

```text
d(a,u)=p+h,       d(b,u)=N-p+h.
```

The first part gives `p+h>=N-q`, hence `N-p<=q+h`. If `h<=q`, then

```text
d(b,u)=N-p+h <= q+2h <= 3q.
```

If `h>q`, then `u` is not on `P(a,b)` and its gate lies more than `q` away, so
`u` is q-deep in the proper component of `T-P(a,b)` containing it. The proof
for `v` is identical. `QED`

For diameter domination, take any active vertex `x` and a q-far edge `(x,y)`.
The orientation just proved makes `x` q-far from one of `a,b`. Hence every
active vertex is adjacent to the dominating pair, which itself is an edge.
Connectivity follows, and any two active vertices are joined through `a`,
through `b`, or through `a-b`, using at most three edges.

## Computational audit and trust boundary

`theory-lab/topwindow/verify_diameter_cap_dichotomy.py` generates 1,100
deterministic random positive weighted trees of orders 4 through 14. It checks
all 45,100 vertex pairs at their sharp deficit `q=N-d(x,y)`, independently
reconstructs the diameter path and every gate, and verifies the cross
orientation, cap inequality and thin/thick classification. The audit includes
3,851 genuinely deep offshoot endpoints rather than testing only the easy cap
case. At all 41,099 threshold changes it separately constructs the full far
graph, checks diameter domination for 397,034 active vertices, and obtains
maximum graph hop-diameter three.

Run:

```text
nice -n 10 python3 theory-lab/topwindow/verify_diameter_cap_dichotomy.py
```

The frozen summary is
`theory-lab/topwindow/results/diameter_cap_dichotomy_certificate.json`.

The remaining **UNVERIFIED** step is combinatorial rather than metric: use the
exact Leech top-window tiling to show that a q-thin offshoot produces a
well-founded proper-branch transition, while repeated q-thick endpoints violate
the weak-Sidon, vertex-budget or merge-profile constraints.

Subsequent **OBSERVED** progress closes the well-foundedness issue for the
specific diameter caps produced by the singleton-pole reflected prefix.  A
nonsymmetric factor either enters a cap of strictly smaller order and boundary
weight, or its proper complement contains a near-diameter pair of strictly
smaller deficit together with an off-spine component at least as deep as the
old cap boundary.  Four-point rigidity forces that pair to keep the opposite
old diameter endpoint, so the transition is an endpoint pivot rather than an
arbitrary new anchor.  Its bidirectional gate component is already a canonical
thick sink unless the uncontrolled ray gap is at least `n-1`; see
(FW85)--(FW109) in
`docs/edge-handoff-orientation.md`.  This identifies the latter output with
the thick endpoint in the theorem above; excluding it, and extending the
recurrence to the separate lower-core handoffs, remain **UNVERIFIED**.  The
result is therefore not yet target D in full generality.
