# FW319/P25 conditional lemma: low-owner saturation

## Scope and status

This note records a conditional, theorem-level lemma for the `b=27`,
J32-single-edge-32, order-25 branch.  It is not a global nonexistence claim
and it does not assert that the existing finite catalogue is complete.

Let `K` be the already fixed named packet.  Assume

1. every `d in [1,37]` except `4` has exactly one global unordered owner,
   while `4` has none;
2. distinct unordered vertex pairs have distinct distances;
3. the fixed packet owns the set
   `S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,27,28,29,30,31,33}`
   with its literal endpoint pairs;
4. `32` is the already fixed J single edge, and the `5/21` owners obey the
   literal shared-5-edge alternatives `(21)`, `(5,16)`, `(16,5)`;
5. an edge is low when its weight is at most `37`, and every path of distance
   at most `37` is therefore contained in one connected component of the
   low-edge forest.

Define

`H37 = [1,37] \ (S0 union {4,32})`

`= {5,16,18,19,20,21,24,25,26,34,35,36,37}`.

## Lemma (conditional low-owner saturation)

For every low component `C` and every pair `{x,y}` in `C` with
`d_C(x,y) <= 37`, exactly one of the following holds:

* `{x,y}` is the literal fixed owner pair of a value in `S0`, or is one of
  the explicitly fixed `5/21/32` owner pairs; or
* `d_C(x,y)` lies in `H37` and `{x,y}` is the unique global owner pair of
  that value.

In particular, every low edge not already among the fixed `5/21/32` packet has
weight in `H37`, and distinct such edges have distinct weights.  Hence there
are at most `|H37|=13` new low edges (and at most ten new vertices from the
separate vertex-budget lemma).

## Proof

If `d_C(x,y) <= 37`, no path from `x` to `y` can contain a high edge, whose
positive weight is at least `38`; thus the pair lies in one low component.
By complete punctured ownership it has exactly one owner unless its distance is
`4`, which is absent.  If its value is in `S0`, or is one of the fixed literal
`5/21/32` owners, a second endpoint pair would contradict global injectivity.
Every remaining value in `[1,37]` is therefore in `H37`, and its endpoint pair
is its unique owner.  Applying this to the endpoints of a new low edge gives
the edge-weight assertion.  Injectivity gives distinct weights for distinct
new edges.

## Independent audit and boundary

The set subtraction and the implication above are direct consequences of the
listed hypotheses; no solver or finite enumeration is needed.  The statement
does **not** prove that every abstract owner-state satisfying these conditions
appears in the current catalogue.  In particular it leaves open incidence
sharing among the owner paths for `16,18,19,20,24,25,26` and `34--37`, the
rootward/outward attachment geometry, and complete high-incidence coverage.
Those are the remaining `Label-State Completeness` obligations.

## Branch-local status update (2026-08-29)

The citation-chain audit in
`docs/pro-b27-branch-hypothesis-discharge-audit.md` discharges the five
hypotheses for a genuine order-25 FW319 exact-return-33 candidate in the fixed
`K`, J32-single-edge residual branch.  Thus the saturation implication is
`VERIFIED_BRANCH_LOCAL_LOW_SATURATION` on that explicitly defined branch.  The
result remains conditional with respect to entering the branch: it is not a
global theorem about arbitrary catalog rows and does not close high-state
surjectivity, least-remote/descent, or nonexistence.
