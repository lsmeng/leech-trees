# Exact `S_m`-equivariant canonical augmentation and stabilizer transport

Status: **proof-state contract / bounded structural interface**, not an all-`S_cover`
surjectivity theorem.

This note records the exact symmetry interface suggested by the two independently
verified `(m,e)=(3,2)` multi-edge pilots:

- `same_named_two_spokes`: 132 valid weighted bases, 22 `S3` orbits, every
  stabilizer trivial and every orbit of size 6;
- `same_anon_two_fixed_named_pair` for `(u,p)`: 33 valid weighted bases, 11
  `S3` orbits, every stabilizer of size 2 and every orbit of size 3.

Those pilots are evidence for this interface only.  They do not prove that the
interface has been implemented or exhaustively checked for all
`S_cover={(m,e):0<=m<=10,0<=e<=m}`.

## 1. Partial weighted-base states and the `S_m` action

Fix the named packet `K` pointwise and let

```text
A_m = {x0,...,x_(m-1)}.
```

A depth-`k` partial weighted base is

```text
P = (m, F, lambda),     0 <= k=|F| <= e,
```

where every edge of `F` is named--anonymous or anonymous--anonymous and
`lambda` assigns a distinct candidate value in

```text
H37_L = {5,16,18,19,20,21,24,25,26,34,35,36,37}
```

to its edge slot.  The fixed packet and the fixed `32` J edge are implicit and
never moved.

For `g in S_m`, define `g.P` by replacing every anonymous endpoint `xi` by
`g(xi)`, keeping named endpoints and weights fixed, normalizing each undirected
edge, and sorting the resulting weighted-edge set.  This is an exact group
action.  No owner-shape tag or incidence choice participates in the base action:
owner pairs/paths are derived from the materialized literal forest.

## 2. Canonical representative and stabilizer

Let `ser(P)` be a deterministic literal serialization of the normalized added
weighted edges, with named vertices ordered by the frozen `FIXED_VERTICES`
order and anonymous vertices by index.  Define

```text
Can(P) = argmin_{g in S_m} ser(g.P)
```

using the **lexicographically least serialization**, not the least hash.
The hash, when stored, is only a digest of that canonical serialization.

The base stabilizer is

```text
Stab(P) = {g in S_m : g.P = P}.
```

Hence the exact orbit identity is

```text
|Orb(P)| * |Stab(P)| = m!.
```

Canonicalization is orbit-invariant and idempotent:

```text
Can(g.P)=Can(P),
Can(Can(P))=Can(P).
```

The stabilizer must be computed from the **complete weighted base**.  Computing
it from endpoint topology while forgetting weights or shared identities can
make the stabilizer artificially too large.

## 3. Theorem-safe partial rejection predicate

Materialize `K union P`.  A partial state is rejected only by predicates already
necessary for every genuine FW319 branch:

1. a cycle in the materialized low graph;
2. duplicate literal edge weights, including collision with a fixed edge;
3. puncture distance `4` inside an actual low component;
4. duplicate component-internal pair distances;
5. reuse of a fixed `S0` owner by a non-fixed pair;
6. duplicate realized H37 ownership.

For a surviving partial state, H37 owner pairs and literal owner paths are
derived from the materialized pair table and `owner_status[32]=NOT_L` is forced.
No `34--37` `EDGE/FWD/REV` geometry, rootward port, outward mask, or high-side
predicate is used at this stage.

### Monotonicity

Each listed rejection predicate is monotone under a later acyclic edge
extension:

- an existing cycle or duplicate edge weight cannot be repaired;
- adding an acyclic edge joins components or attaches new vertices and does not
  alter any already existing component-internal path distance;
- therefore an already realized puncture, repeated pair value, fixed-owner
  reuse, or duplicate H37 owner remains present.

The *first reported reason* need not remain the same after extension; only the
existence of a theorem-level violation is required to be monotone.

### Equivariance

Every filter above depends only on unlabeled tree incidence, literal weights,
pair distances, and fixed named owner pairs.  Anonymous renaming preserves all
of these.  Therefore

```text
Reject(g.P) = Reject(P)
```

for every `g in S_m`.  For accepted states, the owner-status/path table is
transported by the same renaming.  This is the exact reason symmetry reduction
may be performed before incidence expansion.

## 4. Exact canonical augmentation

A symmetry-reduced branch-and-bound search must not choose extensions by an
unproved preferred endpoint shape.  Use an exact canonical-parent test.

For nonempty `Q`, first form `C=Can(Q)`.  In `C`, order the **new weighted
edges** by one fixed deterministic weighted-edge order and let `delta(C)` be
the greatest one.  Define

```text
Parent(Q) = Can(C minus {delta(C)}).
```

For a canonical parent `P`, enumerate legal one-edge/one-weight extension
candidates modulo `Stab(P)`.  A candidate extension `Q=P+q` is admitted iff

```text
(a) q is a legal unused literal endpoint/weight assignment;
(b) Q passes the theorem-safe monotone partial filters; and
(c) Parent(Can(Q)) = P.
```

Condition (c) is the canonical-parent gate.  It is orbit-defined, so it cannot
depend on the arbitrary anonymous names used before canonicalization.  Every
accepted weighted-base orbit has a canonical parent orbit obtained by this
rule; conversely the gate suppresses duplicate construction paths to the same
child orbit.

For implementation efficiency, extension candidates from a fixed canonical
parent may first be quotiented by `Stab(P)`.  That is a safe local orbit
reduction because every element of `Stab(P)` leaves the parent exactly fixed.
The canonical-parent test is still required after extension.

## 5. Incidence transport: quotient only by `Stab(B)`

Let `B` be a fixed canonical **complete weighted base** and let `I(B)` be its
port/outward-mask incidence decorations.  After selecting `B`, the exact
symmetry acting within this fiber is

```text
Stab(B),
```

not all of `S_m`.

For `g in Stab(B)`, transporting every component vertex, rootward port, and
outward-mask vertex gives another incidence state over the same base `B`.
Thus the exact base-first incidence quotient is

```text
I(B) / Stab(B).
```

A permutation `g notin Stab(B)` sends `(B,I)` to `(g.B,g.I)` over a *different*
base representative.  Quotienting the incidence fiber by all of `S_m` after
fixing `B` can therefore identify decorations that are not related by an
automorphism of `B`; it is an over-quotient unless one instead canonicalizes
the entire `(base,incidence)` pair globally from scratch.

The two bounded multi-edge pilots exhibit both cases that an implementation
must handle: trivial base stabilizer (`same_named_two_spokes`) and a nontrivial
size-2 stabilizer (`same_anon_two_fixed_named_pair`).

## 6. Explicit failure modes

The following are **not** accepted reductions under this contract:

1. minimizing SHA-256 digests instead of canonical serializations;
2. permuting named vertices or treating fixed names as anonymous;
3. computing `Stab(B)` from unweighted topology while ignoring weights,
   owner-derived shared identities, or other retained base data;
4. using all of `S_m` to quotient incidence states after a base representative
   has already been fixed;
5. dropping a partial branch because its endpoint/owner shape was absent from a
   bounded pilot;
6. using preset `34--37` endpoint/LCA/attachment cells as pruning;
7. using rootward-port/outward-mask restrictions before those restrictions have
   an independent theorem;
8. applying high-completion, least-remote, or descent predicates to a partial
   low base unless their monotonicity and projection semantics are separately
   proved;
9. defining the canonical parent from pre-canonical anonymous labels or from an
   arbitrary insertion history.

## 7. What remains unproved

This contract supplies an exact target for a compressed implementation.  The
small fixture accompanying this note checks the group identities and filter
equivariance on representative states from the two verified `(3,2)` endpoint
classes only.

The load-bearing theorem/implementation gap remains:

```text
for every (m,e) in S_cover and every genuine encoded weighted base B,
there exists an accepted canonical-augmentation path from the empty base to
Can(B), and the practical generator enumerates every required parent candidate
orbit and canonical-parent child exactly as specified above.
```

No all-`S_cover` canonical-augmentation coverage, incidence coverage, high-side
surjectivity, or FW319/Leech-tree nonexistence claim is made here.
