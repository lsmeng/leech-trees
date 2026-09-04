# Checkpoint: generic frozen-v3 `(m,e)=(3,1)` weighted-base pilot

Date: 2026-08-30

## Scope

This checkpoint covers exactly the complete generic pre-incidence base domain
for `(m,e)=(3,1)` under the frozen `literal-low-v3-owner-status` schema.
There are 48 admissible literal endpoint choices and 13 assignable values in
`H37_L`, hence exactly `48 * 13 = 624` raw weighted bases.

No rootward-port/outward-mask incidence row was enumerated.  Ports/masks are
represented only by their exact component-derived radix metadata.

## Files

- `theory-lab/topwindow/pilot_pro_b27_generic_m3_e1_weighted_base.py`
- `theory-lab/topwindow/verify_pro_b27_generic_m3_e1_weighted_base.py`
- `theory-lab/topwindow/results/pro_b27_generic_m3_e1_weighted_base_pilot.json`
- `theory-lab/topwindow/results/pro_b27_generic_m3_e1_weighted_base_pilot_verification.json`

## Pilot contract

For every rank `0..623`, the pilot:

1. uses the generic raw indexer to rank/unrank the literal endpoint and H37
   weight assignment and materialize the one new low edge;
2. runs the reference full low-base validity predicate;
3. independently stages the theorem-safe pre-incidence filters in order:
   cycle, literal edge-weight injectivity, complete component pair distances,
   puncture/fixed-owner checks, and derived H37 owner-status/path data with
   forced `32=NOT_L`;
4. requires reference and staged classifications to agree rank by rank;
5. for every surviving weighted base, canonicalizes under the exact `S3`
   action on `x0,x1,x2`, computes the stabilizer and orbit size, and records
   the component port/mask radices without expanding any incidence state.

The independent checker does not import either the pilot or the generic
indexer.  It reconstructs the 48-by-13 rank domain, graph predicates, owner
paths, S3 canonicalization, orbit memberships, stabilizers, and incidence
metadata independently and compares them to the pilot commitments.

## Commands actually run

```text
python3 -m py_compile theory-lab/topwindow/pilot_pro_b27_generic_m3_e1_weighted_base.py theory-lab/topwindow/verify_pro_b27_generic_m3_e1_weighted_base.py
python3 theory-lab/topwindow/pilot_pro_b27_generic_m3_e1_weighted_base.py --compact
python3 theory-lab/topwindow/verify_pro_b27_generic_m3_e1_weighted_base.py theory-lab/topwindow/results/pro_b27_generic_m3_e1_weighted_base_pilot.json
```

## Exact result

Pilot status:

`VERIFIED_GENERIC_M3_E1_WEIGHTED_BASE_PILOT`

Independent checker status:

`VERIFIED_INDEPENDENT_GENERIC_M3_E1_WEIGHTED_BASE_PILOT`

Counts:

- raw bases: `624`
- rank/unrank checks: `624/624`
- reference/staged classification matches: `624/624`
- accepted bases: `99`
- rejected bases: `525`
- rejection reasons:
  - `edge_weight_duplicate = 144`
  - `fixed_owner_reuse = 51`
  - `pair_distance_duplicate = 330`
- canonical weighted-base keys: `33`
- orbit sum: `99`
- every canonical orbit has stabilizer size `2`
- every canonical orbit has orbit size/multiplicity `3`
- incidence rows enumerated: `0`

Commitments:

- valid-rank-list SHA-256:
  `23f1b176fcf6f04e31618744ee3105463bef3298435df33bab2c79f2ea058f4a`
- rank-ledger SHA-256:
  `c61e4ce5a8263adb17e02799800fc7c885f796c163380d662b71faa474de8429`
- incidence-metadata SHA-256:
  `a4618d7007fa56a33b3ab394cc741ee867af6226e6da1fa5f5b37d7c214770a4`
- pilot payload SHA-256:
  `21b6192d371aa55738a3c0eae6bef73b895aa8e093e4f173b3fdc9b990bb9e7c`

No mismatch was found.

## Evidence boundary

This is an exact finite interface certificate for only `(m,e)=(3,1)`.  It
shows that theorem-safe pre-incidence filtering and exact anonymous-orbit
compression can agree with the reference generic encoder on this complete
624-base slice while postponing all incidence expansion.

It does **not** prove that the same staged/canonical branch-and-bound is
surjective or computationally sufficient for every pair in
`S_cover={(m,e):0<=m<=10,0<=e<=m}`.  In particular, higher `e` introduces
nontrivial partial-edge canonical augmentation and potentially larger/different
stabilizers.  A general canonical-augmentation/stabilizer preservation lemma,
or a second bounded multi-edge pilot testing that interface, remains required.
It also says nothing about high-completion surjectivity or FW319/Leech-tree
nonexistence.
