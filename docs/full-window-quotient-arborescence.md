# Full-window quotient arborescence and leaf-port colored tiling (FW282)

This note strengthens the canonical full-window terminal in
`docs/edge-handoff-orientation.md`.  It is an **OBSERVED analytic theorem**
and an exact reduction, not a nonexistence proof.  The former instruction to
"take a sink" can be made canonical: the full-window quotient has a unique
sink, and every other quotient component belongs to a strictly increasing
tree of nested thin caps.  A non-singleton branched sink then reduces at any
core leaf to one two-colored owner-tiling interface.

The statement uses **full support**, not the offset-10 or offset-20 support
relations.  None of the uniqueness conclusions below should be transferred to
those bounded-window orientations.

## 1. Unique full-window sink

Let `T` be a Leech tree of order `n>=5`, put `N=binom(n,2)`, and let an edge
`e` have weight `w`.  Deleting `e` leaves sides `A_e,B_e` of orders `a,b`.
A side *fully supports* `e` when it contains an actual internal pair of
distance greater than `w`; call `e` *full-bidirectional* when both sides do.

There are `ab-1` cross pairs other than the endpoints of `e`, and all of
their distances are greater than `w`.  Hence the number of internal owners
above `w` is exactly

```text
E_e=(N-w)-(ab-1)=N+1-ab-w.                       (FW282.1)
```

The strict edge bound in `docs/heaviest-edge-rigidity.md` gives
`w<=N-ab` for every edge of every Leech tree of order at least five.  Thus
`E_e>=1`: every edge has a fully supported side.

Contract every maximal connected component of full-bidirectional edges.
Every remaining quotient edge has exactly one supported side; orient it
toward that side.  The direction is fixed by actual within-side pair owners.

### Lemma 1 (outdegree one)

Every quotient node has outdegree at most one.

**Proof.**  Suppose a quotient component `K` had distinct outgoing boundary
edges `e,f`.  The complete edge `f`, including both endpoints, lies on the
`K`-side of `e`.  Since that side does not support `e`, `w(f)<=w(e)`.
Equality would repeat an edge distance, so `w(f)<w(e)`.  Interchanging `e,f`
gives `w(e)<w(f)`, a contradiction.  `QED`

### Theorem 2 (arborescence)

The quotient has a unique sink `C`.  Rooting it at `C`, every nonroot node
has one outgoing edge toward its parent.  Along every rootward quotient path,
the boundary weights strictly increase.  If `e` is the outgoing edge of a
node and `B_e` is the full original-tree component away from `C`, then

```text
diam(B_e)<w(e).                                   (FW282.2)
```

**Proof.**  A finite directed tree has a sink.  If it had two, the unique
path between them would switch from pointing toward one endpoint to pointing
toward the other; the switch vertex would have two outgoing edges, contrary
to Lemma 1.  Thus the sink is unique.

At an intermediate quotient node, the preceding boundary edge is a complete
actual pair in the nonsupporting side of the outgoing edge.  Its weight is
therefore strictly smaller than the outgoing weight.  Finally the away
component does not support its boundary, so its diameter is at most the
boundary weight; equality would repeat the distance of that edge.  This
proves (FW282.2).  `QED`

Thus every nonroot quotient basin is a strict thin cap, and the full-window
quotient is a strictly increasing nested-thin-cap arborescence.  This removes
multiple-sink and reversal ambiguity only at the quotient level.  The
unresolved geometry remains inside the bidirectional root component `C`.

## 2. First-level decomposition of the sink

Delete the boundary edges of `C`.  Write the exterior components as
`A_1,...,A_d`, where `A_i` attaches at `c_i in C` by an edge `g_i` whose
outer endpoint is `a_i`; put `s_i=|A_i|` and `c=|C|`.  Theorem 2 gives

```text
diam(A_i)<g_i.                                    (FW282.3)
```

Three immediate consequences will be used below.

1. Every edge internal to `A_i` has weight below `g_i`.  Hence the globally
   heaviest edge lies in `E(C)` or among the first-level boundary edges.
2. Both endpoints of the distance-`N` pair lie outside `C`, and they lie in
   two different `A_i`.  A global leaf cannot lie in a nontrivial
   bidirectional component; a singleton leaf quotient node is not a sink;
   and one thin cap has diameter below its boundary and hence below `N`.
3. If `C` is nontrivial and contains a global branch vertex, then `d>=3`.
   Every graph-theoretic leaf of `C` needs an attached cap, or it would be a
   global leaf.  With at most two ports, `C` would therefore be a path with
   one port at each endpoint and no global branch vertex.

Order the boundary weights as `g_1<...<g_d`.  For each `k`, all internal
distances of `A_1,...,A_k` and the first `k-1` boundary-edge distances are
different actual owners below `g_k`.  Therefore

```text
g_k >= k + sum_(i<=k) binom(s_i,2).               (FW282.4)
```

If `q` is the globally heaviest edge, all cap-internal distances and all but
`q` among the core and boundary edges are below it, so

```text
q >= sum_i binom(s_i,2) + c + d - 1.              (FW282.5)
```

These are actual-owner packing bounds, not moment inequalities.

## 3. Exact multi-port owner identity

For a weighted tree `H`, write

```text
F_H(X)=sum_({u,v} subset V(H)) X^d(u,v).
```

At every port define the rooted polynomial

```text
R_i(X)=sum_(x in A_i) X^d(a_i,x),
R_(C,i)(X)=sum_(y in C) X^d(c_i,y).
```

Partitioning actual unordered pairs into core, one-cap, cap--core and
cap--cap classes gives the coefficientwise identity

```text
I_N(X)
 = F_C(X) + sum_i F_(A_i)(X)
 + sum_i X^g_i R_i(X) R_(C,i)(X)
 + sum_(i<j) X^(g_i+d_C(c_i,c_j)+g_j) R_i(X)R_j(X).  (FW282.6)
```

Every monomial retains its actual pair owner and actual core connector.
Global distance injectivity makes every product coefficient at most one and
makes the displayed pair classes support-disjoint.  Equation (FW282.6) is an
exactness certificate; the proposed successor does not retain its full
quadratic coefficient vector as a dynamic state.

There is also an exact linear-size support skeleton.  Put

```text
rho_i=max_x d_(A_i)(a_i,x),       H_i=g_i+rho_i,
```

and mark one actual farthest vertex of each cap.  Replace each cap, only for
support calculations, by a marked ray of length `H_i` at `c_i`.  For either
side of a core edge, its diameter is the maximum of

```text
d_C(u,v),
H_i+d_C(c_i,u),
H_i+d_C(c_i,c_j)+H_j,                         (FW282.7)
```

over core vertices and ports on that side.  Same-cap pairs are smaller than
`g_i<=H_i`; every other maximum in (FW282.7) is attained by the marked
actual vertices.  Consequently a core edge is full-bidirectional exactly
when both sides of this weighted skeleton have diameter greater than its
weight.  The complete owner tiling remains in (FW282.6); the skeleton is used
only for full-support geometry.

## 4. Leaf-port colored tiling

Assume now that `C` is nontrivial.  Let `v` be a graph-theoretic leaf of
`C`, let `e=vv'` be its unique core edge of weight `p`, and let `I(v)` index
the first-level caps attached at `v`.  This set is nonempty because `C`
contains no global leaf.  Deleting `e` gives

```text
S={v} union union_(i in I(v)) A_i,       R=T-S.    (FW282.8)
```

Thus `S` is a one-port bouquet of actual strict thin caps.  With
`H_i=g_i+rho_i` and zero included as an empty ray, its diameter is the sum
of the two largest `H_i`.  Since `e` lies in the bidirectional core,

```text
diam(S)>p,                 diam(R)>p.              (FW282.9)
```

Define the two actual rooted depth sets

```text
U={d_S(v,x):x in S}
  ={0} dotunion dotunion_(i in I(v)) (g_i+R_i),
V={d_R(v',y):y in R}.                              (FW282.10)
```

Repeated root depth would already repeat a pair distance, so both unions are
genuinely disjoint.  Every cross-`e` distance has the unique form
`p+u+v`, with `u in U,v in V`.  Color the within-side owners above `p` by

```text
H_S={d-p:d in dist(S), d>p},
H_R={d-p:d in dist(R), d>p}.                       (FW282.11)
```

The full Leech spectrum gives the exact colored tiling

```text
[0,N-p]=(U direct-sum V) dotunion H_S dotunion H_R. (FW282.12)
```

Both colors are nonempty by (FW282.9).  For `n>=18`, both cut sides have at
least two vertices and their cut product is at least `2(n-2)>=32`.  The
bounded-handoff theorem therefore gives

```text
eta=min(H_S union H_R)<=10.                       (FW282.13)
```

In particular `U direct-sum V` fills every coefficient `0,...,eta-1`
uniquely, while coefficient `eta` is first replaced by one actual same-side
owner of a specified color and with its actual path/LCA retained.

This is the **leaf-port colored-tiling state**.  It uses one core leaf edge,
one already compressed thin bouquet, an arbitrary opposite side, two rooted
sets and the first actual colored owners.  It does not require a catalogue of
the whole sink topology or an all-pairs LCA matrix.

## 5. Actual pressure control

The six-vertex weighted tree

```text
a --11-- u --3-- v --7-- c
           |        |
           2        1
           b        d
```

has pair spectrum

```text
{1,2,3,4,5,6,7,8,10,11,12,13,14,15,21}
 = [1,15]-{9}+{21}.                               (FW282.14)
```

The edge `uv` is full-bidirectional: the two side diameters are `13` and
`8`, both greater than `3`.  Every other edge is a leaf boundary pointing
inward, so the unique sink is the two-vertex branched core `{u,v}` with four
singleton thin caps.

At the `u` leaf port,

```text
p=3,       U={0,2,11},       V={0,1,7},
H_S intersect [0,12]={8,10},
H_R intersect [0,12]={4,5}.                       (FW282.15)
```

The cross sums and two colors fill `[0,12]-{6}`; the missing offset gives
the missing distance `9`, while the cross sum `11+7=18` gives the outlier
`21`.  This is an actual tree with actual owners, connectors, thin caps and
a non-singleton branched sink.  It is not Leech.  It shows exactly why full
coefficient coverage in (FW282.12), rather than support geometry or a finite
prefix alone, is load-bearing.

## 6. Remaining theorem and trust boundary

The non-singleton thick-sink branch is now reduced to the following single
owner-level statement.

> **UNVERIFIED LPCT (Leaf-Port Colored-Tiling Impossibility).**  For
> `n>=18`, no Leech tree has an edge satisfying (FW282.8)--(FW282.13): one
> side is an actual bouquet of strict thin caps, both sides support the edge,
> and the two rooted cross factors together with two nonempty actual
> same-side colors tile the complete suffix, with their first colored hole at
> offset at most ten.

Every non-singleton full-window sink has a core leaf and hence supplies all
LPCT antecedents.  Therefore LPCT would exclude the entire non-singleton
sink branch.  It does not address the already separately routed singleton
interfaces, and it does not reopen FW281.

There is one useful logical absorption.  If the unit edge is nonpendant, each
side has an internal pair; its distance is greater than one because the unit
edge already owns distance one.  Thus the unit edge is full-bidirectional and
belongs to this unique-sink arborescence.  The nonpendant unit-edge geometry
is therefore part of the thick-sink route, rather than an independent
all-order terminal.  Pendant-unit coefficient separation remains at the
FW281 mechanism-specific STOP.

The analytic proof above establishes no new order exclusion and does not
prove global nonexistence.  The deterministic replay

```text
theory-lab/topwindow/verify_full_window_quotient_arborescence.py
theory-lab/topwindow/results/full_window_quotient_arborescence_certificate.json
```

checks all five known witnesses with both independent checkers, 9,499
distance-injective full-support pressure controls, and the exact six-vertex
tree.  It audits the algebra and graph routing; it is not an independent
all-order proof of the theorem and does not prove LPCT.

FW283 has since exhausted the bounded single-port continuation of this
interface.  It gives the complete first-cross-hole table through offset ten,
an actual affine family with `eta=10` whose first owner gate is arbitrarily
remote, and a **STRICT STOP** for extending one leaf-port prefix one owner at
a time.  LPCT remains open.  The next live mechanism is a simultaneous
two-port capped owner-return invariant.  See
`docs/leaf-port-colored-tiling-stop.md`.
