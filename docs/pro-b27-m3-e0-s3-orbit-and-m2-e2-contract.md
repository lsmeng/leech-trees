# FW319 b=27: frozen-v3 m=3,e=0 S3 audit and next m=2,e=2 contract

Date: 2026-08-29

## Scope

This note is a bounded proof/interface audit.  It does not change any verified
artifact and it does not replace the Geo full-stream replay currently running
for `m=3,e=0`.

## Already verified before this note

1. The frozen `m=2,e=1` literal-low-v3 scope merge is closed in both the local
   and Geo environments.  The merge certificate records
   `VERIFIED_FROZEN_M2_E1_SCOPE_MERGE_CERTIFICATE`, common semantic base hash
   `a193611ae7d07201e6c9a7e8ecaa00870910cb0f0fb0a21d9e92bd950b65c4b1`,
   exact raw-domain count `72,352,088`, accepted count `72,351,744`, and
   canonical-union count `36,175,872`.
2. The Geo `m=3,e=0` generator completed under frozen schema
   `literal-low-v3-owner-status`.  Its artifact has SHA-256
   `6db04e4a29d311b0b5cfaa9062f15e0a67bf94c908d6814b1629ef08813f06df`
   and reports
   `raw=processed=accepted=1,572,864`, `canonical=786,432`, `sentinel=0`.
3. The ordinary independent verifier already accepted that artifact.  A
   separate full-stream owner/canonical replay is still required before the
   whole `m=3,e=0` slice is promoted to the same provenance-hardened status as
   the closed `m=2,e=1` scope.

## Structural S3 orbit/stabilizer lemma

In the frozen `m=3,e=0` scope there is no new low edge.  Hence `x0,x1,x2` are
three singleton low components.  Each singleton has exactly one rootward-port
choice (the vertex itself), contributes no low owner pair, and has one binary
outward-incidence mask.  Therefore, after fixing the named part, the complete
anonymous marked state is exactly a bit vector in `{0,1}^3`, and `S3` acts by
coordinate permutation.

The named/fixed components have port/mask multiplicity

```
K9 root component:       1 * 2^9
{u}:                     1 * 2
{v,y0,y3}:               3 * 2^3
{p,q}:                   2 * 2^2
```

so the fixed-side factor is

`F = 196,608`.

For the eight anonymous bit patterns, the `S3` conjugacy classes have fixed
pattern counts

```
identity (class 1):      8
transposition (class 3): 4 per element
3-cycle (class 2):       2 per element
```

and Burnside gives `(8 + 3*4 + 2*2)/6 = 4` anonymous canonical states per
fixed-side state.  Equivalently the four anonymous orbits are indexed by the
number of marked singleton components `0,1,2,3`, with orbit/stabilizer sizes

```
ones=0: orbit 1, stabilizer 6
ones=1: orbit 3, stabilizer 2
ones=2: orbit 3, stabilizer 2
ones=3: orbit 1, stabilizer 6
```

Thus the exact structural predictions are

`raw = accepted = 8F = 1,572,864`

and

`canonical = 4F = 786,432`.

The independent lightweight verifier
`theory-lab/topwindow/verify_pro_b27_m3_e0_s3_orbit.py` checks these facts from
the fixed literal packet and the artifact scope.  The emitted certificate is
`theory-lab/topwindow/results/pro_b27_m3_e0_s3_orbit_certificate.json` with
status `VERIFIED_M3_E0_S3_ORBIT_STABILIZER_CERTIFICATE`.

### Trust boundary

This proves the `S3` orbit/stabilizer structure and the aggregate raw/canonical
counts.  It does **not** prove that every accepted row's stored owner-status or
canonical serialization equals an independently rebuilt full-stream row.
That remains the role of the pending Geo full-stream replay.  Therefore the
current theorem boundary is:

`VERIFIED structural S3 orbit/stabilizer + aggregate count;`

`GAP pending full-stream owner/canonical replay for m=3,e=0.`

## Minimal next contract: frozen m=2,e=2

Only after the `m=3,e=0` full-stream replay/provenance gate is closed should
the next remote layer be `m=2,e=2`.  Its universal raw domain must be defined
without EDGE/FWD/REV restrictions:

1. vertices are fixed `K` plus `x0,x1`;
2. choose every unordered two-edge set of admissible new literal endpoints,
   where every new edge touches at least one anonymous vertex;
3. impose a deterministic ordering on the two chosen edge slots and enumerate
   every injective assignment of two distinct weights from the 13-value
   `H37_L` domain;
4. invalid bases are explicit one-slot sentinels, never silently skipped;
5. for every valid materialized low forest enumerate every rootward-port choice
   for each non-root component and every outward-incidence mask;
6. recompute total owner status for all 13 `H37_L` values and force
   `status[32]=NOT_L`; shared owner paths are derived from the literal forest,
   not selected from a finite path-shape catalogue;
7. endpoint-intersection types (disjoint, shared-anonymous, shared-named, mixed)
   may be used only as deterministic shard partitions, not as pruning.

### Minimum acceptance certificates for m=2,e=2

A theorem-supporting merge requires:

- exact half-open/hierarchical raw-domain coverage with no gap or overlap;
- provenance certificate binding artifact SHA, frozen schema, ordering,
  semantic base/scope hashes, generator/replay script SHAs, counts, rejection
  reasons, and raw/canonical stream digests;
- full-stream independent reconstruction of forest validity and total owner
  status;
- independent `S2` canonical/orbit certificate for the complete marked state,
  including literal edges/weights, components, rootward ports, outward masks,
  owner-status, and shared identities;
- cross-shard canonical multiplicity conservation
  `sum_k multiplicity(k) = accepted_raw`;
- theorem-level 5/21 validation from actual paths and no assumed 34--37
  endpoint/LCA geometry.

Passing this contract would certify only the frozen `m=2,e=2` low slice.  It
would not prove `m>3`, `e>2`, full low-generator surjectivity, high-completion
surjectivity, the `b=27` residual nonexistence theorem, or global Leech-tree
nonexistence.
