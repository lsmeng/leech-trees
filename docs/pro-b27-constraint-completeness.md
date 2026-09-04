# Constraint-completeness interface for the `b=27` branch

This note fixes the logical target that remains after the definition-level
universal catalogue in `pro-b27-universal-catalogue-surjectivity.md`.  It is an
interface and audit ledger, not a claimed global nonexistence theorem.

## Candidate statement

Let `U_res` be the named-vertex-preserving catalogue of 23-vertex residual
trees extending the fixed 15-vertex packet by exactly eight anonymous
vertices, together with typed cut data `(x,s,cap4)`, as defined in
`pro-b27-universal-catalogue-surjectivity.md`.  For a member `K`, write
`Phi_res(K,x,s,cap4)` for the conjunction of the branch conditions below.  The
desired completeness implication is conditional on the still-open branch-entry
statement:

```
every genuine b=27 exact-return candidate X entering the R2,t=4 cap branch
    -> (K,x,s,cap4) in Good_res(U_res) and Phi_res(K,x,s,cap4).
```

The first part is the branch-conditional cut/reconstruction proposition.  It
does not prove `RETURN-COVER`, `R2-COVER`, or `T4-COVER`/owner-side
normalization.  The second part is the still-open
**Constraint-Completeness Lemma**: every hypothesis used by the branch proof
must be an explicit predicate on the materialized tree, and every genuine
candidate must satisfy it without invoking an experimental catalogue.

## The predicate ledger

`Phi(T)` must contain all of the following.  The status labels are deliberately
conservative.

| predicate | current evidence | remaining obligation |
| --- | --- | --- |
| full spectrum of `X` is `{1,...,300}` | exact-return definition | connect it to the four-set residual/cap decomposition |
| `F_K`, `{4}`, `s+D`, and `s+4+D` are pairwise disjoint and have union `{1,...,300}` | FW303.11/FW304.1 cut identity | prove branch entry and carry all typed cut data into every materialized state |
| global pair-distance injectivity and edge-weight injectivity | exact-return definition; fixed-core replays | formalize once for the whole `Good_res(U_res)` filter |
| fixed literal core `K`, root, and no subdivision of fixed edges | canonical-incidence lemma and universal-catalogue definition | audit that every branch reduction uses the same literal core |
| forced `L` owners `5` and `21` | conditional local owner lemmas and fixed-core controls | prove the geometric hypotheses branch-wide, including all attachment modes |
| `J` single-edge owner `32` | `VERIFIED_FRONTIER` under the stated exact-return assumptions; restricted replays | carry the assumptions into the full predicate, not just the replayed catalogue |
| owners `34,35,36,37` and their endpoint/path identities | partial local/finite evidence | complete the joint incidence-sharing classification |
| low-forest components, unique rootward ports, and carrier orientation | general tree contraction and canonical-incidence round-trip | show the generated low-state keys are surjective, or use the universal catalogue directly |
| ordered high quotient, all endpoint incidences, and ordered arc weights | round-trip and order-10 finite controls | cover arbitrary high skeletons and all arc subdivisions |
| residual puncture exclusion and all fixed/named translates | branch-conditional cut identity and finite controls | keep residual and full-tree predicates typed; express every translate on the materialized reconstruction |
| least-remote/minimality and inherited descent | not closed | state exact quantifiers and prove preservation under every reduction |
| `t >= 86` full `J`-tree constraints | only partial translate probes; `h >= w` geometry lemma | use the complete internal `J` distances and owners; no five-translate shortcut |

The finite Geo `max-edges=3` shard and the Hoffman2 order-5 attachment/LCA
shard are tests of proper subfamilies of this ledger.  Even an exact zero from
either shard establishes only the corresponding finite exclusion.

## Minimum proof obligation

The next theorem-sized task is therefore:

```
For every genuine candidate T, construct Phi(T) from the branch definitions
and previously proved lemmas, with no use of EDGE/FWD/REV, bounded skeleton
order, max-edges, or other experimental restrictions.
```

For each conjunct, the proof record must include its source (theorem, exact
definition, or finite observation), its quantifiers, and the exact hypotheses
under which it is valid.  A conjunct marked only `OBSERVED` remains a gap and
cannot be used to upgrade a solver result.

## Acceptance gate

This interface is complete only when:

1. branch entry is proved, and every genuine candidate then implies
   `(K,x,s,cap4) in Good_res(U_res) and Phi_res(K,x,s,cap4)`;
2. every compressed remote shard has a proved surjection from the relevant
   `Phi`-states and exact, duplicate-free shard coverage;
3. all rows are `INFEASIBLE`, or every survivor has a full edge/port/owner/
   distance certificate and is independently replayed; and
4. the final contradiction is applied to the whole predicate, including
   least-remote/descent and the full `t >= 86` branch.

Until these gates are met, the authoritative conclusion remains a conditional
frontier, not a global `b=27` nonexistence proof.

### Conditional J-side shape information

The existing exhaustive interval-composition replay gives one safe refinement
of `Phi_pair`: **if** an `H37` owner path is wholly internal to `J`, then its
edge sequence must be one of

```
32: (32)
34: (34), (16,18), (18,16)
35: (35), (16,19), (19,16)
36: (36), (16,20), (20,16)
37: (37), (5,32), (32,5), (16,21), (21,16), (18,19), (19,18)
```

This is a finite path-level consequence of forbidden fixed distances,
puncture `4`, distinct interval sums, and positive edge weights.  It is
useful as a conditional filter, but it does not prove that a given owner is on
the `J` side rather than `L`, does not locate its endpoints, and does not cover
owners whose path leaves the component.  Those omitted alternatives remain in
the global `Phi_pair` obligation.

## Minimal pair/owner sublemma

The first sublemma can be stated without choosing any compressed catalogue.
For a materialized full tree `X` reconstructed from `(K,x,s,cap4)`, let

```
D_X : {unordered vertex pairs} -> positive integers,
D_X({u,v}) = distance_X(u,v).
```

Define `Phi_pair(X)` to require: (i) `D_X` is injective; (ii) its image is
exactly `{1,...,300}`; (iii) `4` is owned by the typed cap edge and is absent
from `F_K`; (iv) the already certified fixed
distances have their prescribed literal owners; and (v) each

```
H37 = {5,16,18,19,20,21,24,25,26,32,34,35,36,37}
```

has a unique owner pair.  Add only the owner types already proved in the
branch chain: `5` is an `L`-internal single edge, `21` is one of
`(21),(5,16),(16,5)`, and `32` is a `J`-internal single edge.  For `34--37`,
record only the type/side conditions that are genuinely theorem-level; do not
silently add a finite-catalogue geometry.

The exact target is

```
forall genuine exact-return b=27 candidates X in the R2,t=4 branch:
  Phi_pair(X).
```

Injectivity, positivity, the cap, and the absence of `4` follow directly if
they are part of the exact-return definition.  The fixed owners, the `5/21`
shape reduction, and the `J32` single-edge statement require explicit
citations to the existing conditional lemmas.  The earliest unresolved
implication is whether the proof state already gives a global exhaustive
endpoint/path classification for owners `34,35,36,37`.  Until that is proved,
`Phi_pair` may assert their existence and uniqueness plus known type
conditions, but cannot identify them with the current finite catalogue.
