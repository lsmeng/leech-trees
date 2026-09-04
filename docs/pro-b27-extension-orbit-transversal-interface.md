# Exact extension-orbit transversal interface for all-66 weighted bases

Date: 2026-08-30

Status: **source-level interface definition and proof contract**.  This note does
not claim that an all-66 traversal has been run or independently certified.
No incidence states, high completions, or final Leech-tree candidates are
represented here.

The companion reference module is

```text
theory-lab/topwindow/pro_b27_extension_orbit_transversal.py
```

It is isolated from the existing generic indexer and bounded pilots and uses
only the Python standard library.

## 1. Scope and fixed boundary

Work in the audited FW319 `b=27`, J32-single-edge branch.  For each

```text
0 <= m <= 10
```

let

```text
A_m = {x0,...,x_(m-1)}
```

be the anonymous vertices and keep the fifteen named vertices of the fixed
packet pointwise fixed.  The literal new-endpoint universe is

```text
E_m = {{x_i,v}: x_i in A_m, v in K}
      union {{x_i,x_j}: 0 <= i < j < m}.
```

Thus

```text
|E_m| = 15m + C(m,2).
```

There are no new fixed--fixed endpoints.  The assignable low values are exactly

```text
H37_L = {5,16,18,19,20,21,24,25,26,34,35,36,37}.
```

Value `32` is not an extension weight.  Its J-single-edge owner is outside this
weighted-base interface and its low-owner status remains fixed as

```text
32 = NOT_L.
```

## 2. Weighted partial base

A weighted partial base is

```text
P = (m,F,lambda),       k=|F| <= m,
```

where `F` is a set of distinct endpoints in `E_m` and `lambda` injectively
assigns values of `H37_L` to those endpoints.  The module stores this as
`WeightedPartialBase(m,literal_weighted_edges)`; its `used_h37_weights` field is
derived exactly from the literal edges.

This is a **syntactic raw-base object**.  It does not contain or decide:

- rootward ports;
- outward masks;
- incidence decorations;
- high quotient or ordered high arcs;
- least-remote, descent, or high-completion predicates.

The practical search may later apply only the already audited weighted-base
validity filters: cycle, duplicate literal weight, puncture 4, duplicate
component-internal pair distance, fixed-`S0` owner reuse, and duplicate H37
ownership.  Those filters are not silently built into the transversal itself.

## 3. Complete raw extension universe

For a parent `P` of depth `k<m`, define

```text
U_raw(P) = {(a,w): a in E_m minus F,
                   w in H37_L minus lambda(F)}.
```

The deterministic order is endpoint-major using the frozen named/anonymous
vertex order, then H37-order-minor.  Therefore

```text
|U_raw(P)| = (|E_m|-k)(13-k).
```

If `k=m`, the all-66 scope bound forbids a depth-`m+1` child and the interface
returns the empty universe even if unused endpoints or values remain.

This local universe is the exact one-edge restriction of the fixed-depth raw
domain: adjoining one member of `U_raw(P)` produces a unique syntactically
legal depth-`k+1` raw base containing `P`, and every such child differs from
`P` by exactly one member of `U_raw(P)`.

The generic fixed-depth rank/unrank definition therefore proves a set-theoretic
bijection, but it does not by itself prove that a practical compressed traversal
actually calls this parent-conditioned universe for every reached parent.

## 4. `S_m` action, canonical representative, and stabilizer

For `g in S_m`, `g.P` renames only anonymous endpoints; named vertices and edge
weights are fixed.  Every undirected endpoint is renormalized and the weighted
edge set is sorted deterministically.

The exact canonical representative is

```text
Can(P) = argmin_{g in S_m} ser(g.P),
```

where `ser` is the literal JSON serialization and the minimum is lexical on the
serialization, never on its SHA-256 digest.  Ties are resolved by the
lexicographically least permutation, giving a deterministic transport.

The exact weighted-parent stabilizer is

```text
Stab(P) = {g in S_m: g.P=P}.
```

It is computed from the complete weighted base, not from an unweighted endpoint
shape.  Owner pairs/paths are deterministic functions of the literal weighted
forest, so preserving the weighted base preserves those derived data as well.

## 5. Exact extension-orbit transversal

For canonical `P`, the interface partitions `U_raw(P)` under `Stab(P)` and
returns the lexicographically least candidate in every orbit.  No validity
filter is applied before this partition: otherwise an implementation could
silently omit a legal source extension before the theorem-safe predicates are
checked.

The returned certificate binds at least:

```text
interface_version
schema_version
parent literal payload
parent_serialization_sha256
fixed packet / H37_L / 32=NOT_L boundary
raw_extension_count
raw_extension_universe
raw_universe_sha256
stabilizer_size
stabilizer_sha256
orbit_count
orbit_member_total
orbit_ledger with representative, members, size, and per-orbit digest
orbit_ledger_sha256
representative_ledger
representative_ledger_sha256
disjoint_union_check
certificate_payload_sha256
```

`disjoint_union_check` requires:

```text
pairwise-disjoint orbit member sets;
union of orbit member sets = U_raw(P);
one deterministic representative per orbit;
sum orbit sizes = |U_raw(P)|.
```

The module exposes the exact stabilizer permutations through `stabilizer(P)`;
the certificate stores their deterministic digest rather than claiming that a
smaller guessed subgroup is sufficient.

## 6. Canonical-parent gate

For nonempty `Q`, let `C=Can(Q)`.  Order the new weighted edges by the frozen
weighted-edge order, let `delta(C)` be the greatest one, and define

```text
Parent(Q) = Can(C minus {delta(C)}).
```

For canonical parent `P` and a source candidate `q`, the symmetry-only gate is

```text
canonical_parent_gate(P,q)
    <=> q in U_raw(P) and Parent(P union {q})=P.
```

The gate deliberately does not call ports, masks, high completion, or even the
weighted-base validity predicate.  The correct practical order is:

1. obtain every `Stab(P)`-orbit representative from the complete raw universe;
2. materialize the child;
3. apply only the theorem-safe weighted-base validity filters;
4. apply the canonical-parent gate.

## 7. Why the depth induction is valid, conditionally on this interface

Assume a practical traversal satisfies all four requirements above and starts
from a separate empty parent `Empty_m` for each fixed `m`.

Let `C` be any canonical accepted weighted base of depth `k+1`.  Delete its
distinguished edge `delta(C)` and call the raw deletion `R`.  By deletion
heredity of the audited weighted-base filters, `R` is accepted.  Put

```text
P = Can(R).
```

Then `P` is canonical, accepted, and has depth `k`.

Choose any permutation `g` with `g.R=P` and transport the deleted edge to

```text
q = g.delta(C).
```

Because endpoint and weight injection are preserved, `q` lies in `U_raw(P)`.
The exact transversal therefore emits a representative `q'` in the same
`Stab(P)` orbit, say `q'=h.q` with `h in Stab(P)`.  Since `h.P=P`,

```text
P union {q'} = h.(P union {q})
```

is in the same `S_m` orbit as `C`.  It is accepted by equivariance, and its
canonical parent is `P`, so the gate retains it.

The needed orbit is independent of the choice of `g`: if `g.R=P=g'.R`, then

```text
g' g^{-1} in Stab(P),
```

so the two transported candidates lie in the same stabilizer orbit.

Induction on the well-ordered depth

```text
0 < 1 < ... < e <= m
```

therefore reaches `Can(C)` from `Empty_m`, provided every reached parent invokes
the complete transversal before filtering and the traversal processes every
retained canonical child.

This is a mathematical conditional proof.  No all-parent execution or
independent implementation certificate is asserted by this note.

## 8. Complexity and resource boundary

For a depth-`k` parent,

```text
|U_raw(P)| <= (15m+C(m,2)-k)(13-k).
```

The reference implementation computes `Can(P)` and `Stab(P)` by exact
permutation enumeration, with factorial worst-case cost in `m`.  At `m=10`,
`|S_m|=3,628,800`; the empty parent has the full group as stabilizer.  The
interface is therefore finite and exact but is not presented as a production
all-66 traversal engine.

A scalable implementation may replace permutation enumeration with an exact
graph-automorphism/group algorithm, but it must emit a certificate equivalent
to the fields above.  Sampling permutations, using an unweighted stabilizer,
or limiting candidates by endpoint patterns is not an accepted substitute.

## 9. Explicit failure modes

The following break coverage:

1. treating the fixed-depth raw ranker as if it proved that a parent-conditioned
   traversal emitted every extension;
2. quotienting extension candidates by all of `S_m` instead of `Stab(P)`;
3. computing `Stab(P)` after erasing weights or shared anonymous identities;
4. filtering candidates before the complete raw universe is committed;
5. omitting an `Empty_m` root for some `m`;
6. defining the parent from insertion history or pre-canonical labels;
7. minimizing hashes rather than serializations;
8. including ports, masks, high completion, or an unproved 34--37 geometry in
   the weighted-base validity gate;
9. inferring all-66 coverage from the existing `m=3` fixtures.

The existing tiny gap fixture gives the concrete second failure: for
`P={u--x0=5}`, the three candidates `p--xi=20` form one full-`S3` orbit but two
`Stab(P)` orbits; the singleton orbit produces the known valid same-anonymous
child.

## 10. Proof status and remaining scope obligation

### Defined and proved at interface level

- the exact local raw universe;
- the exact weighted-parent stabilizer;
- deterministic stabilizer-orbit partition and certificate schema;
- the canonical-parent gate;
- the conditional depth-induction proof above.

### Not yet established

No practical all-66 traversal has been shown to invoke this exact interface for
every reached canonical accepted parent.  No independent checker has proved the
module equivalent to the existing generic fixed-depth encoder for arbitrary
`m<=10`, and the factorial reference implementation has not been executed over
all parents.

The single remaining weighted-base **scope/integration obligation** is:

```text
For every m<=10 and every canonical accepted parent reached from Empty_m, the
practical traversal invokes an exact interface equivalent to
extension_orbit_transversal(P), applies only the audited hereditary/equivariant
weighted-base filters, applies the canonical-parent gate, and enqueues every
retained canonical child exactly once up to its orbit.
```

Only after that source/integration obligation is independently certified may
the conditional induction be promoted to all-66 weighted-base coverage.
Incidence quotienting by `Stab(B)`, high-stage surjectivity, and FW319/Leech-tree
nonexistence remain separate later obligations.
