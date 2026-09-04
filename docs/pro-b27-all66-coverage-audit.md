# Generic all-66 canonical-augmentation coverage audit

Date: 2026-08-30

Status: **source-level proof/interface audit only**.  No large enumeration, no
incidence expansion, no remote job, and no modification of `research_state.md`.

## Target

Work in the audited FW319 `b=27`, J32-single-edge branch.  The implementation
domain is

```text
S_impl = {(m,e): 0 <= m <= 10, 0 <= e <= m},
```

66 scope pairs in total.  After the corrected two-vertex-cap typing, a real
residual factor has only eight anonymous vertices, so its branch-realizable
subdomain is

```text
S_res = {(m,e): 0 <= m <= 8, 0 <= e <= m},
```

45 scope pairs in total.  The 21 scopes with `m=9,10` are syntactic tests but
cannot represent real residual states.  For fixed `m`, let
`A_m={x0,...,x_(m-1)}` and let
`E_m` be all named--anonymous and anonymous--anonymous literal edges.  A
weighted base is `(m,F,lambda)` with `F subset E_m` and injective
`lambda:F -> H37_L`.

The audit question is whether the current generic encoder plus the existing
canonical-parent / `Stab(parent)` interface is already sufficient to prove that
every genuine encoded weighted base in all 66 scopes is reached by a practical
canonical-augmentation search.

## VERIFIED

| item | exact conclusion |
|---|---|
| Typed residual scope bound | Conditional on the R2,t=4 branch reduction, every genuine residual state has `m<=8` and `e<=m`; thus every genuine weighted base lies in one of the 45 pairs in `S_res`.  `S_impl` is a conservative syntactic superset. |
| Fixed-depth raw encoder | `theory-lab/topwindow/index_pro_b27_generic_low_base_domain.py` defines every `e`-subset of `E_m` and every injective H37 assignment for each `(m,e) in S_impl`, with deterministic rank/unrank and simultaneous materialization.  This closes the **uncompressed source raw-domain interface**, not compressed search coverage or branch entry. |
| Theorem-safe filter heredity | Cycle, duplicate edge-weight, puncture 4, duplicate component-internal pair distance, fixed-`S0` owner reuse, and duplicate H37 ownership are deletion-hereditary: deleting a new edge from a valid weighted base cannot create one of these violations. |
| `S_m` equivariance | Anonymous renaming preserves the literal weighted graph, all theorem-safe validity predicates, and derived owner-status/path data.  Named vertices and weights remain fixed. |
| Canonical representative / parent interface | `Can(P)` as the lexicographically least literal serialization in the `S_m` orbit is orbit-invariant and idempotent.  `Parent(Q)=Can(Can(Q)-{delta(Can(Q))})`, with deterministic distinguished edge `delta`, is an orbit-defined depth-reducing parent map. |
| Stabilizer rule | For a fixed canonical parent/base, candidate extensions and later incidence decorations may be quotiented only by its exact weighted-base stabilizer.  The two verified `m=3,e=2` pilots exhibit both trivial and nontrivial stabilizers. |

### Currently closed / bounded computational scopes

The following are the relevant **existing verified finite scopes or bounded
interfaces**; none should be conflated with all-66 canonical-augmentation
coverage.

- `(m,e)=(2,1)`: frozen-v3 low-slice scope merge is closed, including hardened
  replay/transport/stabilizer provenance.
- `(m,e)=(3,0)`: frozen low-slice gate is closed, with independent full-stream
  replay and an exact `S3` orbit/stabilizer theorem for the singleton-mask
  action.
- `(m,e)=(2,2)`: the complete 72,540-base validity census is closed, but the
  incidence workload is **not** globally closed; only workload shards 0, 1, and
  2 currently have generator + independent replay + provenance closure.
- `(m,e)=(3,1)`: the complete 624 **weighted-base-only** domain was checked and
  exactly compressed under `S3`; no incidence expansion and no all-scope
  theorem follows.
- `(m,e)=(3,2)`: only the two explicitly declared complete `S3`-invariant
  endpoint subdomains are verified (`same_named_two_spokes` and
  `same_anon_two_fixed_named_pair(u,p)`); the complete 175,968-base scope is not
  closed.

Therefore there is presently **no proof that all 66 scope pairs are covered by
canonical augmentation**.

## OBSERVED

| evidence | what it supports, and no more |
|---|---|
| `m=3,e=1` complete weighted-base pilot | On one full one-edge scope, theorem-safe pre-incidence filtering and exact `S3` canonicalization agree with an independent reference. |
| `same_named_two_spokes` | A genuine two-edge family with trivial weighted-base stabilizer (`|Stab|=1`, orbit size 6) behaves coherently under exact `S3` quotienting. |
| `same_anon_two_fixed_named_pair(u,p)` | A complementary two-edge family with nontrivial stabilizer (`|Stab|=2`, orbit size 3) behaves coherently. |
| Canonical-augmentation structural fixture | Representative `m=3` states satisfy canonical idempotence, orbit invariance, orbit-stabilizer identity, filter equivariance, owner-status transport, monotone rejection, and the canonical-parent gate. |

These observations strongly support the proposed interface, but they are
finite fixtures.  They do not quantify over arbitrary parent states, arbitrary
real `m<=8`, arbitrary depth `e<=m`, or the complete extension universe.

## OPEN: first load-bearing premise

The generic encoder currently provides **fixed-depth rank/unrank**, but it does
not provide a practical source-level routine/certificate of the following form:

```text
for every canonical accepted parent P=(m,F,lambda),
  enumerate the complete set U(P) of legal unused one-edge/one-weight
  extensions, partition U(P) into exact Stab(P)-orbits, and emit at least one
  representative from every such orbit before applying the canonical-parent
  gate.
```

This is the smallest missing implementation/proof premise.

Equivalently, the required all-66 coverage lemma is:

> **Canonical-augmentation coverage lemma.**  For every genuine encoded
> weighted base `B` with `(m,e) in S_res`, there exists a chain
>
> ```text
> empty = B_0, B_1, ..., B_e = Can(B)
> ```
>
> such that for every `k<e`, `B_k` is canonical and accepted, the practical
> generator's **complete** extension universe contains a representative of the
> required `Stab(B_k)`-orbit, and that representative produces `B_(k+1)` after
> the canonical-parent gate.

The mathematical parent map plus hereditary filters show how such a chain is
defined *once every required extension orbit is available*.  What is not yet
proved is that the practical compressed generator emits every required
`Stab(parent)` extension orbit for every parent in all 66 scopes.

### Minimal concrete failure pattern if the premise is omitted

At `m=3`, take the accepted parent

```text
P = {u--x0 = 5}.
```

Its stabilizer fixes `x0` and swaps `x1,x2`, so `|Stab(P)|=2`.  For a candidate
weight 20 and named vertex `p`, the three candidates

```text
p--x0=20, p--x1=20, p--x2=20
```

form **two** `Stab(P)`-orbits:

```text
{p--x0=20},
{p--x1=20, p--x2=20}.
```

The first orbit gives the already verified valid child class
`{u--x0=5, p--x0=20}`.  Thus an implementation that keeps only an arbitrary
candidate representative, or quotients candidates by full `S3` rather than
`Stab(P)`, can omit a genuine valid child orbit.  This is an interface failure,
not a heuristic concern.

## What current fixtures cannot imply

The current `S3` fixture and two multi-edge pilots **cannot** establish any of
the following:

1. that every one of the 66 `(m,e)` scopes has an accepted
   canonical-augmentation path;
2. that the practical generator enumerates the complete extension universe for
   every canonical parent;
3. that checking representative `m=3` stabilizers proves the stabilizer action
   for arbitrary real `m<=8`;
4. that a full-`S_m` candidate quotient is safe at a fixed parent (the correct
   local group is `Stab(parent)`);
5. that weighted-base canonicalization alone covers rootward ports or outward
   masks;
6. that incidence states may be quotiented by all `S_m` after fixing a base;
7. that the incomplete `(2,2)` workload or the bounded `(3,2)` endpoint pilots
   imply complete `(3,2)` coverage;
8. that any current low-side result proves high-completion surjectivity,
   `L`-surjectivity of the final reduced search, or FW319/Leech-tree
   nonexistence.

## Audit verdict

```text
VERIFIED:
  generic 66-scope syntactic cover and corrected 45-scope residual bound;
  total fixed-depth generic raw encoding;
  theorem-safe hereditary/equivariant filters;
  exact canonical representative/parent definitions;
  exact Stab(base) symmetry principle.

OBSERVED:
  the contract works on the complete m3e1 base pilot and two complementary
  m3e2 S3-invariant endpoint classes, including stabilizer sizes 1 and 2.

OPEN:
  complete Stab(parent)-extension-orbit enumeration for every canonical parent,
  hence the branch-relevant all-45 canonical-augmentation coverage lemma.
```

The next unique minimal mathematical/interface question is therefore:

```text
Can one prove, and then implement as a total source interface, that for every
canonical accepted parent P occurring on a genuine base, every legal unused
endpoint/weight extension needed by Parent^-1(P) is represented by one of the
generator's complete Stab(P)-orbit representatives?
```

Until that premise is proved and audited, the branch-relevant all-45
compressed search remains `OPEN`, even though the uncompressed fixed-depth
generic encoder covers the larger 66-domain syntactic superset by definition.
