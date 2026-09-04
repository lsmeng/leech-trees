# Typed universal catalogues for the `b=27` exact-return branch

This note repairs an earlier type error: the full order-25 tree and the
23-vertex residual factor obtained after cutting the final two-vertex cap are
different objects.  Their distance tables must not be assigned the same
cardinality or the same catalogue.

## Exact-return decomposition

Let `X` be a genuine order-25 exact-return candidate in the two-vertex-cap
branch, let `K` be the 23-vertex component below the final bridge, let the cap
edge have weight `4`, and let the bridge have weight `s`.  If `x` is the root
of `K` incident with the bridge and

```text
D = {d_K(x,v): v in V(K)},
```

then the full pair-distance multiset is the disjoint union

```text
F_X = F_K disjoint_union {4}
          disjoint_union (s + D)
          disjoint_union (s + 4 + D).
```

The cardinalities are

```text
|F_K| + 1 + |D| + |D| = 253 + 1 + 23 + 23 = 300.
```

Thus `X` has the complete spectrum `{1,...,300}`, including `4`; `K` has only
253 internal pair distances.  The old definition demanding that a tree on
`15+m` vertices have distance set `{1,...,300} minus {4}` was impossible:
`binom(15+m,2)` is never 299 for `0<=m<=10`.

## Two typed catalogues

Let `P` be the fixed named 15-vertex packet in the audited branch, with its 11
literal weighted edges and four connected components retained.

1. `U_full` is the finite named-vertex-preserving catalogue of weighted trees
   on 25 vertices extending the typed packet and final cap data.  Its `Good`
   predicate requires the complete pair-distance table to be exactly
   `{1,...,300}`.
2. `U_res` is the finite named-vertex-preserving catalogue of weighted
   23-vertex residual trees `K` extending `P` by exactly eight anonymous
   vertices, together with typed data `(x,s,cap4)`.  Its `Good_res` predicate
   requires injectivity and disjointness of the four sets in the displayed
   exact-return decomposition and requires their union to be
   `{1,...,300}`.

Canonicalization quotients only permutations of the eight anonymous residual
vertices and keeps every named packet vertex, `x`, `s`, and the cap data.

## Conditional reconstruction proposition

**Proposition.** Conditional on entry into the two-vertex final-cap branch,
cutting the final bridge and recording `(K,x,s,cap4)` is lossless.  Conversely,
materializing a member of `Good_res(U_res)` and reattaching the typed cap and
bridge produces a full 25-vertex tree with complete spectrum
`{1,...,300}`.

**Proof.** Cutting the bridge uniquely produces the 23-vertex component `K`,
the rooted attachment vertex `x`, bridge weight `s`, and the two-vertex cap
with edge weight `4`.  Every unordered pair of vertices of `X` lies in exactly
one of four classes: both in `K`, both in the cap, one in `K` and the nearer
cap vertex, or one in `K` and the farther cap vertex.  Their distances are
respectively `F_K`, `{4}`, `s+D`, and `s+4+D`.  These classes give the displayed
identity and reconstruct every pair distance.  Reattaching the recorded edge
and cap reverses the cut. `QED`

This proposition does **not** prove that every FW319 candidate enters the
two-vertex-cap branch.  That branch-entry/discharge implication remains a
separate proof obligation.

## Threshold-37 projection and exact counts

Let `m` be the number of the eight anonymous residual vertices active in the
threshold-37 low projection, and let `e` be the number of new low edges.  Then

```text
low vertices                    = 15 + m
low edges                       = 11 + e
low components                  = 4 + m - e
residual vertices outside low   = 8 - m
residual edges outside low      = 11 - e
residual quotient vertices      = 12 - e
residual quotient edges         = 11 - e.
```

If the still-open semantic saturation statement later proves `e=m`, the
residual quotient has `(12-m,11-m)`.  If the cap is included as an explicit
low component, the corresponding full-tree quotient has `(13-e,12-e)`, hence
`(13-m,12-m)` after saturation.  Retaining both cap vertices uncontracted can
produce the older `(14-m,13-m)` count, but those are known cap vertices, not
anonymous residual budget.

The real residual branch has `0<=m<=8`, hence 45 `(m,e)` scopes with
`0<=e<=m`.  A code domain using `MAX_M=10` and all 66 pairs is an overinclusive
syntactic superset; its `m=9,10` scopes cannot represent a residual `K` state.
Existing `m=5` shards remain within the corrected real domain.

## Remaining proof chain

The corrected load-bearing chain is

```text
universal exact-return applicability (`RETURN-COVER`)
    -> two-vertex cap coverage (`R2-COVER`)
    -> weight-4/owner-side coverage (`T4-COVER`)
    -> H37 semantic saturation (`e=m`, with exact owner incidences)
    -> complete high-stage surjectivity
    -> certified finite exclusion.
```

The universal typed catalogues remove the cardinality ambiguity.  They do not
prove branch entry, `H37` saturation, least-remote/descent preservation, or
high-stage search coverage, and no finite zero may be promoted across those
open implications.
