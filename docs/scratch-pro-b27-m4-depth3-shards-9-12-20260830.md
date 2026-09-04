# Scratch advisory: `m=4`, depth-3 shards 9--12

Date: 2026-08-30

Status: **non-authoritative execution record**. This note does not modify or replace
`research_state.md` or an authoritative checkpoint. It records one bounded Geo
Workstation batch only; no new research epoch is opened.

## Scope and frozen inputs

Remote working directory:

```text
/home/geo/codex-work/leech-trees/remote_scratch/canonical_traversal_shard_20260830/theory-lab/topwindow
```

Verified parent layer:

```text
results/pro_b27_canonical_traversal_m4_d2_0_of_16.layer_merge.json
SHA-256 b22486d8379e4e38e090c0877c42ebced65bb56cf70dbf519807d8c7fbd22610
```

Frozen source hashes committed by every artifact and replay:

```text
runner
466ce529e85dca803de77980cf2c99ecf92afa6091fc526c656df4e48322441b

independent replay checker
378c0bb30695eaf64e2c9a68a5ec70d94acfa6e28fae267309bfd8011fb2fec2

extension transversal
fb127ff978241efafa856c350e52c9f804cf88ea9d6789b60558b8420451e496

generic indexer
f524f469461de1304eadb33c077122ede55e01c4b9b06444c6387f25fd201ebd
```

Before the batch, a Geo-side process check found no active `m=4, depth=3`
generator or replay, the parent-layer SHA matched, and the shard 9--12 output
paths were absent. One intermediate guard invocation before shard 10 returned
exit 75 because its broad `pgrep` expression matched the checking shell's own
command line; it exited before creating any shard-10 artifact. The guard was
then narrowed to process name `python3`, confirmed no overlap, and execution
continued.

## Exact shard results

Each shard was run strictly as generator followed by independent replay, with
`--shard-count 64` and `timeout 180s` for each phase.

| shard | parent interval | parents | raw extensions | child orbits | generator artifact SHA-256 | replay artifact SHA-256 |
|---:|---:|---:|---:|---:|---|---|
| 9 | `[534,594)` | 60 | 37,800 | 39 | `74a8336dcd8b5e2712188ed5a1d0438cf22f3be3b76557db038b9d6c628fbf62` | `af0e328378b4df4e2b60a44b1be88e32fb932139c0c5a13ddb924f8d196ea3db` |
| 10 | `[594,653)` | 59 | 37,170 | 24 | `e8bce85a3c7d61b0542ff23ca7a6ed825cdab4cca0eead3548f06b0087c16a45` | `55270d0f55de7253cef765757cb0807c61260c0fb284ebf6ef19edf957056c41` |
| 11 | `[653,713)` | 60 | 37,800 | 14 | `b6cfd1a13d62dd8e88d8b3e74461ee01f4dfda44a1aacfadffba00aa0426716a` | `f48ec6c299a205a33205d36648c6afbadfdf78b8b822f9f8492b636abac5898e` |
| 12 | `[713,772)` | 59 | 37,170 | 10 | `adb3faa3d03c0bcaf85d68762d3eb4cb9e470c8ea89e0ce928de3d87e595ec8e` | `6a7c3854a5fb402a62436b02ee376f4b4021b53fac2279fa7455a57e8d3e461b` |

Every generator returned:

```text
VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS
```

Every replay returned:

```text
VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD
```

## Acceptance checks applied

For each shard, the post-run audit independently required:

- exact scope `m=4`, `parent_depth=3`, `child_depth=4`;
- exact half-open interval and parent count;
- `global_parent_count=3803`;
- parent-layer file SHA equal to the frozen value above;
- every selected parent to have `raw_extension_count=630`;
- aggregate raw extensions equal to `630 * parent_count`;
- complete child ledger length equal to `shard_child_orbit_count`;
- `child_layer_bases_sha256` to recompute exactly;
- generator `certificate_payload_sha256` to recompute exactly;
- replay `artifact_sha256`, scope, shard, parent source, source hashes, child
  count and child-ledger digest to match the generator;
- every replay check flag required at depth 3 to pass;
- replay `verification_payload_sha256` to recompute exactly;
- `incidence_rows_enumerated=0`.

No source, ledger, payload, scope, parent-layer, or replay mismatch occurred.

## Batch and cumulative commitments

For shards 9--12:

```text
status                  VERIFIED_M4_D3_BATCH_9_12_METADATA_AUDIT
parent interval         [534,772)
parent count            238
raw extensions          149,940
child orbits            87
unique child serializations 87
cross-shard duplicates  0
```

Combining this metadata with the already verified shards 0--8 gives the current
verified prefix:

```text
status                  VERIFIED_M4_D3_PREFIX_0_12_METADATA_AUDIT
verified shards         13/64
parent interval         [0,772)
parent count            772
raw extensions          486,360
child orbits            734
unique child serializations 734
cross-shard duplicates  0
```

## Trust boundary

This note certifies only the completed Geo artifacts and independent replays for
shards 9--12, plus a metadata-only cumulative uniqueness/interval audit for
shards 0--12. It does not certify shards 13--63, the complete depth-3-to-depth-4
layer merge, terminal depth 4, all-66 coverage, incidence quotients, high
completion, FW319 nonexistence, or global Leech-tree nonexistence.
