# Canonical weighted-base traversal shard contract — v2

Date: 2026-08-30

Status: **source/interface contract only**.  The matching runner is
`theory-lab/topwindow/pro_b27_canonical_traversal_shard.py` with traversal
schema `canonical-traversal-shard-v2`.  This contract is weighted-base only: it
does not enumerate ports, outward masks, incidence states, high completions,
least-remote states, or descent states, and it does not prove all-66 coverage or
Leech-tree nonexistence.

## 1. CLI and depth semantics

The runner CLI is

```text
python3 pro_b27_canonical_traversal_shard.py \
  --m M \
  --depth D \
  --shard-index I \
  --shard-count K \
  [--parent-layer VERIFIED_LAYER.json] \
  --output SHARD.json
```

`--depth D` is the **parent depth** processed by the shard.  Its emitted bases,
when `D<M`, have child depth `D+1`.

The parent-source rule is exact:

- `D=0`: reconstruct only `Empty_m`; `--parent-layer` is forbidden.
- `D=1`: reconstruct `Empty_m` and the complete canonical accepted depth-1
  layer from the root; `--parent-layer` is forbidden.
- `D>=2`: `--parent-layer` is mandatory.  The supplied verified merged layer is
  the sole authoritative parent list.  The runner must not silently rebuild a
  potentially different depth-`D` list from `Empty_m`.

Thus the first intended chained use is:

1. generate and independently replay the `m=3,D=1` shard;
2. merge that one shard into a verified layer whose `canonical_bases` are the
   depth-2 bases;
3. pass that merged file as `--parent-layer` to every `m=3,D=2` shard.

## 2. Fixed branch and source interfaces

The runner requires exact agreement between:

- `index_pro_b27_generic_low_base_domain.py`, supplying the audited
  theorem-safe weighted-base validity predicate;
- `pro_b27_extension_orbit_transversal.py`, supplying the complete
  `Stab(P)` extension-orbit transversal and canonical-parent interface.

The fixed named order, `H37_L`, schema version, `MAX_M=10`, and fixed
`32=NOT_L` boundary must match.  New weighted-base edges remain only
named--anonymous or anonymous--anonymous literal edges.

## 3. Required verified parent-layer schema

For a run with `--m M --depth D`, where `D>=2`, the supplied JSON must have

```text
status        = VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_LAYER_MERGE
merge_version = canonical-traversal-layer-merge-v2
```

and exact scope

```json
{
  "m": M,
  "parent_depth": D-1,
  "child_depth": D,
  "weighted_base_only": true,
  "ports_enumerated": false,
  "outward_masks_enumerated": false,
  "incidence_rows_enumerated": 0
}
```

The list used as the depth-`D` parent layer is

```text
canonical_bases
```

with exact commitments

```text
canonical_base_count
ordered_canonical_base_digest
canonical_bases_sha256
source_hashes
layer_payload_sha256
trust_boundary
```

Each `canonical_bases` row is the exact portable record

```json
{
  "serialization": "<WeightedPartialBase.serialization()>",
  "serialization_sha256": "<SHA-256 of serialization>",
  "payload": {
    "m": M,
    "depth": D,
    "literal_weighted_edges": [["...", "...", 5]],
    "used_h37_weights": [5],
    "fixed_32_owner_status": "NOT_L"
  }
}
```

The loader reconstructs every base from the literal weighted-edge payload and
requires all of the following:

1. the row is exactly reproduced by the reconstructed base;
2. `m=M`, depth `D`, and fixed `32=NOT_L`;
3. the base is canonical under the full anonymous `S_m` action;
4. the base passes the theorem-safe weighted-base predicate;
5. the list is lexicographically ordered by the stored serialization;
6. serializations are unique;
7. `canonical_base_count` equals the list length;
8. `ordered_canonical_base_digest` equals the SHA-256 commitment to the ordered
   serialization list;
9. `canonical_bases_sha256` equals the SHA-256 commitment to the complete
   ordered serialization/payload rows;
10. `source_hashes` equal the current runner, transversal, and generic-indexer
    source hashes;
11. `layer_payload_sha256` equals the digest of every top-level field except
    `status`, `layer_payload_sha256`, and `trust_boundary`.

Failure of any condition aborts the depth-`D` run.  There is no root-rebuild
fallback for `D>=2`.

## 4. Parent sharding

Let the authoritative ordered parent list have size `N`.  Shard `I/K` handles
exactly

```text
start = floor(N*I/K)
end   = floor(N*(I+1)/K)
[start,end)
```

in lexicographic canonical serialization order.  The shard records the full
boundary table, global parent-list digest, selected-parent digest, and exact
parent indices.  The boundary table must start at zero, end at `N`, and have
adjacent equal end/start coordinates.

For `D=0/1`, `parent_source.mode` is `root_reconstruction` and commits to the
root-prefix summary.  For `D>=2`, `parent_source.mode` is
`verified_merged_parent_layer` and commits to the parent-layer file hash,
payload hash, scope, count, serialization digest, and payload-ledger digest.

## 5. Per-parent processing

For every selected canonical accepted parent `P`, the runner must call

```text
extension_orbit_transversal(P)
```

and must verify that its `Stab(P)` orbits are pairwise disjoint, exactly cover
`U_raw(P)`, and have one deterministic representative per orbit.  It may not
replace this with a full-`S_m` quotient or an endpoint-shape catalogue.

Every representative is processed in the order

1. materialize `P+q`;
2. apply only the theorem-safe weighted-base validity predicate;
3. if valid, apply the canonical-parent gate;
4. if the gate passes, emit `Can(P+q)`.

The existing per-parent raw-universe, stabilizer, orbit, representative,
validity, rejection, gate, and emitted-child digest fields remain mandatory.

## 6. Complete child-layer ledger in every shard

In addition to the existing

```text
shard_child_orbit_count
shard_child_list_sha256
```

every v2 shard stores the complete ordered child serialization/payload ledger:

```text
child_layer_bases
child_layer_bases_sha256
```

`child_layer_bases` uses exactly the portable row schema in Section 3.  It is
sorted by canonical serialization and contains every canonical child emitted by
this parent shard, not samples.  `child_layer_bases_sha256` commits to the full
ordered rows, while the preserved `shard_child_list_sha256` commits only to the
ordered serialization list.

These fields are necessary because a digest alone cannot be used as the next
parent layer.

## 7. Exact layer merge and one-shard merge semantics

A theorem-supporting layer merge must first require an independent replay for
every source shard.  It must then check common `m`, parent depth, child depth,
traversal/source hashes, global parent count and digest; exact shard-index and
half-open parent coverage; and unique parent indices.

It concatenates all `child_layer_bases`, rejects any repeated serialization
across shards, sorts the union by serialization, and recomputes both the
serialization-only and full-payload digests.  Its portable output is

```text
status        = VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_LAYER_MERGE
merge_version = canonical-traversal-layer-merge-v2
scope          = the common source-shard scope
source_hashes  = the common source hashes
canonical_base_count
canonical_bases
ordered_canonical_base_digest
canonical_bases_sha256
layer_payload_sha256
trust_boundary
```

For a one-shard layer such as `m=3,D=1,I/K=0/1`, the merge is still explicit;
it is not merely a file rename.  After the shard's independent replay passes,
the one-shard merge must set

```text
canonical_bases                 = shard.child_layer_bases
canonical_base_count            = shard.shard_child_orbit_count
ordered_canonical_base_digest   = shard.shard_child_list_sha256
canonical_bases_sha256          = shard.child_layer_bases_sha256
```

and recompute its own `layer_payload_sha256`.  That verified merged artifact is
the only admissible `--parent-layer` input for `D=2`.

## 8. Independent replay boundary

The v2 replay must mirror the parent-source rule:

- for `D=0/1`, independently reconstruct the required root prefix;
- for `D>=2`, independently validate and consume the exact declared merged
  parent layer rather than silently rebuilding it;
- recompute the half-open shard, every selected-parent transversal and gate
  ledger, `child_layer_bases`, both child digests, source hashes, parent-source
  commitments, and the outer certificate payload hash.

The previously written replay checker targets traversal schema v1 and was not
modified in the bounded runner-only repair that introduced this contract.  It
must be upgraded separately before a v2 artifact can receive independent replay
status.

## 9. Backward incompatibility

The already generated Geo traversal artifact made with runner hash

```text
f712825aa22780969f4ff43cfa75c770d9d420775d0a92f77b0837d0706d88da
```

uses `canonical-traversal-shard-v1`.  It has no `parent_source`, no
`child_layer_bases`, and no `child_layer_bases_sha256`.  It therefore cannot be
promoted by renaming into a v2 verified merged parent layer and cannot be used
as `--parent-layer` for a depth-2 run.

The safe options are to regenerate the bounded depth-1 artifact under v2 and
independently replay/merge it, or to build a separately audited migration that
reconstructs the complete child ledger from the v1 source.  No migration is
claimed by this document.

## 10. Theorem boundary

This schema repair makes chained weighted-base traversal representable and
prevents silent parent-layer drift.  It does not itself certify a depth-1 or
depth-2 run, all-66 traversal coverage, the incidence quotient
`I(B)/Stab(B)`, high completion, FW319 nonexistence, or global Leech-tree
nonexistence.
