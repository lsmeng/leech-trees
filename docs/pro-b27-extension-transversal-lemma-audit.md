# Extension-transversal lemma audit for all-66 canonical augmentation

Date: 2026-08-30

Status: **source-level proof/interface audit**.  This note does not enumerate any
scope, expand incidence states, modify `research_state.md`, or claim FW319
nonexistence.

## 1. Setting

Fix one scope parameter `m` with `0 <= m <= 10`.  The anonymous slots are

```text
A_m = {x0,...,x_(m-1)}
```

and the literal endpoint universe is

```text
E_m = {{x_i,v}: v in K} union {{x_i,x_j}: i<j}.
```

The generic indexer proves by construction that

```text
|E_m| = 15m + C(m,2).
```

A depth-`k` weighted partial base is

```text
P = (m,F,lambda),
```

where `F` is a `k`-subset of `E_m` and `lambda:F -> H37_L` is injective.
The fixed packet, its literal weighted edges, and the fixed J owner `32` are
implicit.  All chains below keep `m` fixed; their root is the separate state

```text
Empty_m = (m, empty edge set, empty lambda).
```

There is no transition from `Empty_0` to `Empty_m`.  An implementation claiming
all-66 coverage must initialize one root for every `m=0,...,10`, or separately
supply a vertex-introduction theorem/interface.

Let `Valid(P)` mean that the materialized low graph passes only the audited
base-level necessary predicates:

1. acyclicity;
2. literal edge-weight injectivity, including collision with fixed edges;
3. no component-internal distance `4`;
4. no duplicate component-internal pair distance;
5. no reuse of a fixed `S0` owner by a non-fixed pair;
6. no duplicate realized H37 owner.

Owner endpoint pairs and literal paths are derived from the materialized forest,
and `owner_status[32]=NOT_L` is fixed.  No port, outward mask, high-completion,
or unproved `34--37` geometry condition enters `Valid` here.

## 2. VERIFIED

### V1. Fixed-depth raw coverage

For every `(m,k)` in `S_cover`, the functions

```text
endpoint_subset_from_rank / endpoint_subset_rank
weight_assignment_from_rank / weight_assignment_rank
descriptor_from_rank / descriptor_rank_from_weighted_edges
```

in `index_pro_b27_generic_low_base_domain.py` are intended as mutually inverse
rank interfaces for

```text
{(F,lambda): F is a k-subset of E_m,
             lambda:F -> H37_L is injective}.
```

Thus every syntactically legal fixed-depth weighted base has a deterministic
raw rank.  This is a **fixed-depth set bijection**; it is not yet a
parent-conditioned extension iterator.

### V2. Deletion heredity of the accepted base predicate

If `Q` is `Valid` and `q` is one of its new weighted edges, then

```text
R = Q minus {q}
```

is `Valid`.

Reason: deleting an edge from an acyclic low forest preserves acyclicity and
cannot create a duplicate literal weight.  It may split one component, but it
does not change the unique path or its weight between any two vertices that
remain connected.  It can therefore delete pair distances but cannot create a
new puncture, pair-distance collision, fixed-owner reuse, or duplicate H37
owner.

### V3. `S_m` equivariance

The exact `S_m` action permutes only anonymous slots, fixes every named vertex
and every edge weight, and transports derived owner endpoints/paths.  Therefore

```text
Valid(g.P) iff Valid(P)
```

for every `g in S_m`.  Canonicalization by the lexicographically least literal
serialization is orbit-invariant and idempotent.

### V4. The set-theoretic parent-extension bijection

For a fixed partial base `P=(m,F,lambda)`, define its complete **raw extension
universe**

```text
U_raw(P) = {(a,w): a in E_m minus F,
                   w in H37_L minus lambda(F)}.
```

A pair `(a,w)` is only syntactically unused; it may subsequently fail `Valid`
because `w` collides with a fixed edge or because the new paths violate a
pair-distance condition.

The map

```text
(a,w) |-> P union {(a,w)}
```

is a bijection from `U_raw(P)` onto the depth-`k+1` raw descriptors whose
weighted-edge set contains `P`.  This follows directly from the endpoint-subset
and injective-weight definitions.  Its cardinality is

```text
(|E_m|-k) * (13-k).
```

This is the precise sense in which the fixed-depth raw domain contains every
one-step extension.  The complete depth-`k+1` raw domain itself is **not**
equivalent to `U_raw(P)`: it is the union of children of many different
parents, and the current indexer exposes no parent-conditioned restriction or
orbit transversal.

### V5. `U_raw(P)` is invariant under `Stab(P)`

Let

```text
H = Stab(P) = {g in S_m: g.P=P}.
```

Every `g in H` preserves the used weighted-edge set of `P`; hence it preserves
both the unused endpoint set `E_m minus F` and the unused weight set.  Therefore
`H` acts on `U_raw(P)`, and taking one representative from each exact
`H`-orbit is a lossless local candidate reduction.

The action must be computed from the complete weighted parent.  Full `S_m` is
not a valid replacement for `H` after `P` has been fixed.

### V6. Canonical-parent existence for every accepted child

Let `C` be a nonempty canonical `Valid` base.  Let `delta(C)` be its
deterministically greatest new weighted edge, set

```text
R = C minus {delta(C)},
P = Can(R).
```

By V2, `R` is `Valid`; by V3, `P` is canonical and `Valid`; and its depth is one
less than that of `C`.  Hence the canonical-parent map always supplies a legal
parent for every accepted weighted-base orbit.

This statement concerns only the theorem-safe low-base predicate.  It does not
say that `P` has been generated by current code, nor that ports/high completions
are preserved by deleting an edge.

## 3. CONDITIONAL: exact canonical-augmentation coverage theorem

The following implication is rigorous once the total extension-transversal
premise is supplied.

> **Extension-transversal coverage lemma.**  Fix `m`.  Suppose a generator:
>
> 1. starts from `Empty_m`;
> 2. for every reached canonical `Valid` parent `P`, constructs the complete
>    set `U_raw(P)`;
> 3. computes the exact weighted-base stabilizer `H=Stab(P)`;
> 4. emits at least one representative from every `H`-orbit in `U_raw(P)`;
> 5. materializes each emitted child, rejects it only by `Valid`, and retains it
>    exactly when its canonical parent is `P`.
>
> Then the generator reaches exactly one canonical representative of every
> `Valid` weighted-base orbit at every depth `e<=m`.

### Proof chain

Induct on depth `e`.

The depth-zero orbit is `Empty_m`, so the base case holds.  Let `C` be any
canonical `Valid` child of depth `e>0`.  Define

```text
R = C minus {delta(C)},
P = Can(R).
```

By V6, `P` is a canonical `Valid` state of depth `e-1`; by induction it is
reached.  Choose a permutation `g` with `g.R=P` and set

```text
q = g.delta(C).
```

Then `q` is in `U_raw(P)`, and

```text
P union {q} = g.C.
```

If another transport `g'` also sends `R` to `P`, then

```text
g' g^(-1) in Stab(P),
```

so `g'.delta(C)` and `q` lie in the same `Stab(P)`-orbit.  Consequently the
required extension orbit is independent of the arbitrary transport choice.

By premise 4, the generator emits a representative `q'` of that orbit.  Thus
`q'=h.q` for some `h in Stab(P)`, and

```text
P union {q'} = h.(P union {q})
```

is in the orbit of `C`.  It is `Valid` by V3.  Its canonical representative is
`C`, and its canonical parent is `P`, so it passes the gate.  This proves the
inductive step.  The edge count is a strict natural-number descent, so the
backward parent chain terminates at `Empty_m`.

The proof establishes an all-depth theorem for a **fixed `m`**.  Applying it to
all 66 scope pairs additionally requires running/instantiating the same total
source interface for every root `Empty_m`, `m=0,...,10`.

## 4. OPEN: why the current source does not yet discharge the premise

The current generic indexer has fixed-depth rank/unrank, materialization,
validity, and incidence rank interfaces.  It does not expose generic functions
of the form

```text
extension_universe(P)
stabilizer(P)
extension_orbit_transversal(P)
canonical_parent(P)
```

for arbitrary `m<=10`.  The existing canonical-parent and stabilizer checker is
an `m=3` structural fixture, not the practical all-`m` generator.

Therefore V4 proves that every required child has a raw fixed-depth rank, but it
does **not** certify that a compressed search, when positioned at a particular
parent, emits the required local candidate orbit.  The missing premise is an
implementation-level totality statement, not another H37 or deletion lemma.

### Exact source-level failure pattern

For

```text
m=3,
P={u--x0=5},
```

`Stab(P)` fixes `x0` and swaps `x1,x2`.  The candidates

```text
p--x0=20,
p--x1=20,
p--x2=20
```

form one orbit under full `S3` but two orbits under `Stab(P)`:

```text
{p--x0=20},
{p--x1=20,p--x2=20}.
```

The singleton orbit gives the independently verified valid child

```text
{u--x0=5,p--x0=20}.
```

Thus fixed-depth rank coverage does not prevent a practical parent iterator
from omitting this child if it quotients candidates by full `S3`, keeps only one
arbitrary representative, or restricts candidates to a preferred endpoint
shape.  The tiny gap fixture verifies exactly this interface failure.

### Additional totality details that must be explicit

A conforming source interface must also:

- include edges incident to currently isolated anonymous slots;
- include anonymous--anonymous edges between two currently isolated slots;
- keep all `m` slots present throughout the fixed-`m` chain;
- carry weights with edges when a permutation changes edge-slot order;
- derive the stabilizer from the complete weighted parent, not its unweighted
  topology;
- partition the **complete** `U_raw(P)` into disjoint `Stab(P)`-orbits before
  applying the canonical-parent gate;
- provide an exact coverage certificate: orbit union equals `U_raw(P)`, orbit
  intersections are empty, and every emitted representative belongs to its
  declared orbit.

Pre-excluding fixed-edge weight collisions or other candidates is permitted
only when the source interface records the corresponding theorem-safe filter
as an exact prefilter.  It must not change the set of accepted children.

## 5. Audit answer

```text
VERIFIED
  The fixed-depth encoder contains every one-step child set-theoretically.
  Accepted children have accepted canonical parents.
  A complete Stab(parent)-orbit transversal gives an exact local reduction.
  Under that totality premise, well-founded induction proves canonical-path
  coverage for every accepted base orbit at fixed m.

CONDITIONAL
  The all-depth/all-66 coverage theorem follows once the practical generator
  implements the complete parent-conditioned universe and exact stabilizer
  transversal for every reached parent and starts from every Empty_m.

OPEN
  No current all-m source implementation or coverage certificate establishes
  those extension transversals.  Existing m=3 fixtures and bounded pilots do
  not quantify over all parents or all 66 scopes.
```

## 6. What must not be inferred

The current raw indexer and `m=3` fixtures do not imply:

1. that a practical compressed generator has covered every parent state;
2. that full `S_m` may replace `Stab(P)` for candidate reduction;
3. that every `m>3` parent stabilizer is handled correctly;
4. that base coverage supplies port/outward-mask coverage;
5. that incidence fibers may be quotiented by more than `Stab(B)`;
6. that the incomplete `(2,2)` workload or bounded `(3,2)` pilots close their
   surrounding scopes;
7. high-stage surjectivity, FW319 nonexistence, or global Leech-tree
   nonexistence.

## 7. Unique minimal next step

Implement and independently audit one generic, non-enumerative source routine

```text
extension_orbit_transversal(m,P)
```

whose contract is:

```text
input:  canonical Valid weighted parent P on all m anonymous slots;
raw universe: exactly U_raw(P);
group: exactly Stab(P) computed from the complete weighted parent;
output: exactly one deterministic representative per group orbit;
certificate: disjoint orbit union equals U_raw(P), with a digest of the ordered
             raw universe, stabilizer, orbit ledger, and representatives.
```

Once this interface is proved total, the induction in Section 3 upgrades it to
canonical-augmentation coverage of the weighted-base layer.  Incidence
quotienting by `Stab(B)` and high completion remain separate later obligations.
