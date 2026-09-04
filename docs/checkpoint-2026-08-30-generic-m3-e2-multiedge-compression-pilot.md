# Checkpoint: bounded generic m=3,e=2 multi-edge compression pilot

Date: 2026-08-30

## Goal

Test the theorem-safe weighted-base compression interface beyond the one-edge
m=3,e=1 pilot, without expanding any incidence rows and without touching the
existing m=2,e=2 workload artifacts.

## Full-domain attempt and bounded fallback

The complete generic m=3,e=2 weighted-base domain has

```text
C(48,2) * P(13,2) = 1,128 * 156 = 175,968
```

raw bases. Standalone full-domain pilot/checker scripts were created and their
fixtures passed, but the full pilot did not complete within the DevSpace
300-second controlled execution limit. The run was stopped by the tool timeout;
no result artifact and no theorem claim are attached to the full 175,968 domain.
No longer timeout or remote computation was started.

The accepted fallback is the complete S3-invariant subdomain
`same_named_two_spokes`:

- choose any of the 15 fixed named vertices as a common center;
- choose any 2 of x0,x1,x2 as the anonymous leaves: C(3,2)=3;
- use both literal edges from the named center to those leaves;
- assign all ordered injective pairs from H37_L: P(13,2)=156.

Thus the exact bounded domain size is

```text
15 * 3 * 156 = 7,020 raw weighted bases.
```

This family is closed under the full S3 action on x0,x1,x2 and contains genuine
multi-edge interactions through a shared named endpoint.

## Pilot result

`pilot_pro_b27_generic_m3_e2_same_named_two_spokes.py` returned

```text
VERIFIED_GENERIC_M3_E2_SAME_NAMED_TWO_SPOKES_PILOT
```

with exact counts:

```text
raw = 7,020
accepted = 132
rejected = 6,888
edge_weight_duplicate = 2,970
fixed_owner_reuse = 693
pair_distance_duplicate = 3,225
canonical S3 weighted-base orbits = 22
orbit sum = 132
stabilizer histogram = {1: 22}
orbit-size histogram = {6: 22}
incidence rows enumerated = 0
```

The staged theorem-safe filter agrees with the generic reference on all 7,020
ranks. Rejection stages are:

```text
injective_lambda = 2,970
fixed_owner = 693
pair_distance = 3,225
```

No heuristic owner shape, endpoint/LCA restriction, port restriction, outward
mask restriction, or high-completion predicate is used.

## Independent checker

`verify_pro_b27_generic_m3_e2_same_named_two_spokes.py` does not import the
pilot or generic indexer. It independently reconstructs all 7,020 subdomain
ranks, computes their corresponding generic m=3,e=2 descriptor ranks,
re-materializes the low forest, rechecks validity and owner paths, performs the
full S3 weighted-base canonicalization, and recomputes stabilizers, orbit
multiplicities, and port/mask radix metadata without incidence expansion.

It returned

```text
VERIFIED_INDEPENDENT_GENERIC_M3_E2_SAME_NAMED_TWO_SPOKES_PILOT
```

with zero mismatches on rejection counts/reasons, canonical-key-set commitment,
orbit ledger, stabilizers, valid-rank commitments, generic-rank commitments,
and incidence-metadata commitment.

## Commitments

```text
valid_rank_list_sha256 = d50f0a06a7e4a935dbb822fdada07f522a521aa9f84238871b6a7b652b2b5a08
valid_generic_rank_list_sha256 = 575e1711cfe299e305953641e679f30a9ac2eb1828df7efd14a5d992b52ac2e1
rank_ledger_sha256 = 0e8f64eb2f6a29824be86c0cead8606843abdf1319cc7a2d15ca1109b16ec387
canonical_key_set_sha256 = cb2b487e2e6d581e58df8fc61e67d5c70c8a2dfbe604ce72394761fce50d0abd
orbit_ledger_sha256 = 87137017bd6a932699ebf46360e2f878f8b0037c63a0f80df36b436b776d8a1f
incidence_metadata_sha256 = 03f851ff66fd6e10926a2f5836ec255e5cf302c96b687424a248231107843526
pilot_payload_sha256 = 8251297c748bf5cf0649252100e6d978f86e7d4c47b27bbe690ccff124279c36
```

## Evidence boundary

This closes only the exact `same_named_two_spokes` S3-invariant subdomain of
m=3,e=2. It is evidence that theorem-safe pre-incidence filtering and exact
full-S3 weighted-base orbit/stabilizer accounting remain coherent in a true
multi-edge family. It does not close the complete 175,968-base m=3,e=2 domain,
other m/e scopes, incidence-orbit compression, high completion, practical
L-surjectivity of a reduced search, or FW319/Leech-tree nonexistence.
