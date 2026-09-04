# FW319/P25 Weighted Incidence Lifting Lemma

## Purpose

The verified rooted-normal-form catalogue is topology/entry-only.  The next
theorem-level bridge is a lossless lifting statement, not another topology
count.

Let `T` be the verified catalogue of rooted topology rows.  For every genuine
FW319 J-internal owner realization `R`, the required statement is

\[
  \exists!\,\tau\in T,\;\exists(\lambda,\iota,\Omega):
  R\cong \operatorname{Lift}(\tau,\lambda,\iota,\Omega),
\]

with the named vertices fixed.  Only this direction is needed: a lifted row
need not be realizable.  The uniqueness is up to the declared rooted
isomorphism, so that a later finite exclusion cannot double-count or omit a
genuine state.

## Required fields

The lift must retain, without compressing a path to its total length:

* `lambda`: the original positive integer weight of every literal edge,
  including every stem/subdivision and side-branch edge; owner-path edges are
  fixed to the selected admissible word;
* `iota`: every incidence mark, including attachment to each low component,
  rootward/outward port, ordered-high arc endpoint/internal vertex, and every
  shared vertex between owner paths;
* `Omega`: the actual owner pairs for 32, 34, 35, 36, 37 together with all
  named-vertex aliases and literal reuse;
* the complete rooted edge list/topology, so every possible attachment point is
  an explicit vertex;
* enough metadata to recompute all rooted depths, LCAs, unordered-pair paths,
  distances, and owner identities from the materialized tree.

## Explicit quantifiers

For every genuine `R`, the lifting proof must establish all of the following.

1. The literal owner path of `R` has one of the verified admissible words.
2. Every actual stem, subdivision, and branch vertex of `R` occurs in the
   chosen topology row; no incidence is attached to a suppressed edge interior.
3. Every actual edge corresponds to exactly one row edge carrying its original
   weight; total-length compression is disallowed.
4. Every low/high attachment and every shared identity is represented by
   `iota`/`Omega`.
5. Materialization from the row preserves every unordered-pair path, hence the
   complete distance multiset and all unique owner endpoints.
6. The resulting row is unique modulo the declared rooted isomorphism.

## Current artifact audit

The existing topology rows contain `tree_edges`, owner word, entry vertex,
`rho_max`, and a placeholder alias pattern.  They deliberately use
`weight_status=OWNER_WORD_ONLY_FREE_STEM_UNASSIGNED`.  They do **not** contain
`lambda`, `iota`, or `Omega`; every non-root vertex is labeled `NEW_*`, so the
placeholder aliases are not evidence of real named-vertex reuse.  Therefore
the current 1,077,588-row result cannot establish the lifting lemma or J34--37
weighted-realization surjectivity.

The exact schema deficiency is recorded by
`theory-lab/topwindow/audit_pro_b27_weighted_incidence_schema.py`.  Its expected
status on the current topology artifact is
`GAP_WEIGHTED_INCIDENCE_SCHEMA`, not a verification of completeness.

## Minimal next gate

Before any large weighted search, extend one bounded topology pilot with the
full edge-list/weight/incidence schema and an independent round-trip checker.
The checker must rebuild the tree from the serialized row and compare the
recomputed rooted depths, owner paths, pair distances, and owner endpoints to
the stored values.  Only after this bounded gate passes should a Geo
Workstation weighted shard be treated as evidence toward the J34--37
quantifier.

This lemma, even if proved, would reduce the remaining work to a finite
weighted exclusion.  It would not by itself prove J34--37 exclusion or the
global `b=27` nonexistence theorem.

## Relation to the universal baseline

The project already has a definition-level fallback catalogue
`docs/pro-b27-universal-catalogue-surjectivity.md`: after fixing the 15-vertex
packet `K`, every genuine order-25 completion has at most ten anonymous
vertices and therefore maps to a named-vertex-preserving canonical full
edge-list/weight state.  This proves the abstract coverage implication
`realization -> U^can_25`; it does not make the catalogue computationally
tractable.

Consequently the remaining practical theorem is more precise: prove that the
compressed low/high generator (with `tau_L, omega_L, Pi, tau_H, I`, and ordered
arc subdivisions) is surjective onto the corresponding full states, or retain
the universal state directly.  A topology-only rooted row cannot be used in
place of this implication, even when its finite row count is independently
verified.
