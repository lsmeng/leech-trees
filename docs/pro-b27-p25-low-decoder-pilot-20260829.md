# P25 low-decoder pilot report (2026-08-29)

This report records a bounded protocol test, not a P25 catalogue or a
nonexistence result.

## Remote runs

All computation ran on Hoffman2, never on the local workstation.

```text
job 101662: m<=1, max-low-edges=1, outward_mode=none
job 101663: m<=2, max-low-edges=1, outward_mode=none
job 101665: m<=2, max-low-edges=1, outward_mode=all
job 101668: m<=2, max-low-edges=2, outward_mode=all (corrected)
job 101669: m<=3, max-low-edges=2, outward_mode=all
```

The final run used one CPU, 2 GiB, and a 10-minute wall-clock limit under
`account=pi_lsmeng`, `partition=campus`, `qos=campus24`.

## Final pilot result

The JSON artifact is
`theory-lab/topwindow/results/pro_b27_p25_low_decoder_pilot_m2_e1_all_101665.json`
with SHA-256

```text
c38c700837a835d83cca554ef9b1237eec1e8b0f19976542e893649beb1998ce
```

The generator reported:

```text
raw_candidates             = 463
accepted_raw_candidates    = 343
canonical_state_count      = 202
status                     = OBSERVED_P25_PILOT
```

The independent replay
`theory-lab/topwindow/verify_pro_b27_p25_low_decoder_pilot.py` returned

```text
VERIFIED_P25_PILOT_STRUCTURAL_REPLAY
```

It reconstructed the fixed low edges, low-component partition, low distances,
H37 owner map, component ports, outward masks, canonical hashes, and the
raw-to-canonical multiplicity accounting.

## Trust boundary

The pilot covers only `m<=2` and at most one added low edge.  Its optional
shape filter tests only the direct-21 branch; the shared `(5,16)` branch is not
included.  The fixed packet's incidences are held to the bounded control
convention.  The independent replay does not regenerate the raw candidate
space, so exact catalogue coverage is not established.

Therefore the proof-state label is:

```text
OBSERVED_P25_PILOT /
VERIFIED_P25_PILOT_STRUCTURAL_REPLAY /
P25_SURJECTIVITY_OPEN
```

## Corrected two-edge replay

An initial `m<=2,e<=2,outward_mode=all` run (`101665`) exposed two
canonicalization bugs: derived owner/distance endpoint labels were not
renamed with anonymous vertices, and renamed pair endpoints were not
re-sorted.  That artifact is invalid and is not used as evidence.  After both
fixes, job `101668` completed with the same raw search space and returned:

```text
raw_candidates             = 40963
accepted_raw_candidates    = 1639
canonical_state_count      = 850
independent replay         = VERIFIED_P25_PILOT_STRUCTURAL_REPLAY
```

The corrected JSON is
`theory-lab/topwindow/results/pro_b27_p25_low_decoder_pilot_m2_e2_all_101668.json`
with SHA-256

```text
ddda92205cd44448259338f59ce4c2ed8726232e41ab986bd869b296b9dbc2d5
```

This strengthens the protocol evidence to two anonymous vertices and two
added low edges, but it remains bounded and does not establish raw-space
surjectivity for `m<=10`.

## Three-vertex extension

After the corrected `m<=2,e<=2` replay passed, job `101669` extended the same
protocol to `m<=3,e<=2,outward_mode=all` on Hoffman2 (one CPU, 4 GiB, 30-minute
limit).  It completed in nine seconds:

```text
raw_candidates             = 132164
accepted_raw_candidates    = 19791
canonical_state_count      = 3934
independent replay         = VERIFIED_P25_PILOT_STRUCTURAL_REPLAY
```

The JSON is
`theory-lab/topwindow/results/pro_b27_p25_low_decoder_pilot_m3_e2_all_101669.json`
with SHA-256

```text
a2d069d8da4f5afe3c1b4737a69877dcc30a2a304b79bf1072e9544c670aa6e2
```

## Canonical-minimum audit correction

An additional independent audit initially reported a failure on row 12.  The
failure was in the audit itself: it compared the smallest SHA-256 digest,
rather than hashing the lexicographically smallest canonical JSON.  SHA-256
does not preserve lexicographic order.  The generator's representative rule
was already the correct one.  The verifier was corrected to select
`min(canonical_json)` first and hash that string; the corrected verifier was
copied to Hoffman2 and replayed against the unchanged `101669` artifact:

```text
accepted_raw_candidates    = 19791
canonical_state_count      = 3934
status                     = VERIFIED_P25_PILOT_STRUCTURAL_REPLAY
```

Thus the m3 artifact now passes the strengthened structural replay, including
the canonical-minimum check.  This remains protocol evidence only: the
verifier does not independently regenerate the raw candidate space.

This is still a bounded protocol test: it omits `m>3`, three-or-more added
low edges, the shared `(5,16)` realization of 21, and complete raw-space
surjectivity.

The next legitimate step is to freeze the deterministic raw-state ordering and
shard/checkpoint/merge contract (including every rootward port and outward
incidence mask), then implement an independent raw-key/orbit checker before
any `m=4` expansion.  The shared `(5,16)` realization of 21, explicit 32
non-L ownership, and 34–37 geometry remain theorem-level omissions.

## Geo Workstation raw-shard smoke check

The hierarchical raw-state prototype was run only on Geo Workstation for the
small `m<=1,e<=1,outward_mode=all` domain.  It produced 152 ordered base
blocks and a global raw domain of 202 states.  A two-way split `[0,101)` and
`[101,202)` was independently merged and checked:

```text
accepted_raw             = 59
rejected_base_sentinels  = 143
global_index_digest      = f2e218db17f39543d17776ca0a16379f0586349897be92793a467a0cb8a7cb78
status                   = VERIFIED_P25_RAW_SHARD_PROTOCOL
```

The full reference artifact and both shard artifacts are stored under
`theory-lab/topwindow/results/` with `geoworkstation` in their names.  This is
an engineering/protocol check only; it does not add any P25 catalogue states
or close the theorem-level owner gaps.

The same protocol was then checked on the existing `m<=2,e<=1` domain and on
the full existing `m<=3,e<=2` pilot domain.  For `m<=2,e<=1`, the independent
merge returned `775` raw states (`343` accepted and `432` sentinels).  For
`m<=3,e<=2`, it returned:

```text
global_raw_count         = 173085
accepted_raw             = 19791
rejected_base_sentinels  = 153294
status                   = VERIFIED_P25_RAW_SHARD_PROTOCOL
global_index_digest      = dcd3097f2953e796c4337d813b6e2ca9a20cc46f767f8a65092af133afbb2d65
```

The m3 two-shard merge and a separate single-interval reference run produced
the same digest.  This closes the bounded sharding-consistency gate for the
current pilot domain; it is still not raw-space coverage of the full P25
domain.

Finally, the same m3/e2 shards were regenerated with canonical payloads
materialized on every accepted raw state.  The independent canonical merger
recomputed every representative (including the corrected lexicographic
minimum), found 3,934 unique keys, and checked

```text
orbit_sum                  = 19791
reference pilot key-set    = identical
reference multiplicities   = identical
status                     = VERIFIED_P25_CANONICAL_SHARD_MERGE
```

The canonical-integrated single-interval run and the two-shard merge also
agreed on rolling digest
`122cec60ed659ef459c273877295e3c9c7ef5087db3e9488bda8d48395d8b2bc`.

## Theorem-field audit (observation only)

An independent read-only audit of the 19,791 accepted canonical states recorded
the currently visible owner/shape fields:

```text
shape21 = EDGE21       5952
shape21 = UNRESOLVED   13839
32 owner = NOT_L       19791
34 owner = L_ACTUAL    19791
35 owner = NOT_L       19791
36 owner = L_ACTUAL    19791
37 owner = L_ACTUAL    19791
```

The `UNRESOLVED` rows are expected because this pilot does not materialize the
shared `(5,16)`/`(16,5)` shape.  The 34--37 labels reflect literal low paths
in the current fixed packet and are not a proof of the missing rooted
geometry.  Thus this audit identifies exactly what must be added to the schema;
it does not close those theorem-level gaps.

## Theorem-field integration: marked m3/e2 rerun

The same hierarchical raw domain was regenerated with `shape21`,
`owner32_location`, and conservative `owners34_37` fields included in the
canonical payload.  On Geo Workstation the independent raw checker returned

```text
global_raw_count         = 173085
accepted_raw             = 19791
rejected_base_sentinels  = 153294
index_digest              = f897d61584d8dbea35c71bf13af99044c41a17db98b9aa851357e856499e8b53
status                   = VERIFIED_P25_RAW_SHARD_PROTOCOL
```

The independent canonical merger returned `3934` canonical keys and orbit sum
`19791`, and the two marked shard files reproduce the full-file digest exactly.
The local copies are retained under `theory-lab/topwindow/results/`.

The theorem-field audit remains observational: `owner32=NOT_L` for all
`19791` accepted rows; `shape21=EDGE21` for `5952` and `UNRESOLVED` for
`13839`; the visible 34--37 statuses are `L_ACTUAL, NOT_L, L_ACTUAL,
L_ACTUAL`.  The unresolved and rooted-geometry cases are not theorem
conclusions.

The conditional low-owner saturation lemma is recorded separately in
`docs/pro-b27-h37-owner-saturation.md`.  It excludes the already fixed 32
owner from the set of *new* low-edge weights and is a finite-state bound only;
it does not establish catalogue surjectivity.
