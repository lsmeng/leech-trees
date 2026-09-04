# Independent replay contract for canonical traversal shards

Date: 2026-08-30

Status: **checker/interface documentation only**.  The checker described here
was written under a no-Python/no-enumeration restriction and has not been run by
this audit.  It does not certify all 66 scopes, incidence states, high
completion, or Leech-tree nonexistence.

## Checker

```text
theory-lab/topwindow/verify_pro_b27_canonical_traversal_shard.py
```

The checker does **not** import
`pro_b27_canonical_traversal_shard.py` and does not import any pilot.  It uses
only the two audited source interfaces:

```text
index_pro_b27_generic_low_base_domain.py
pro_b27_extension_orbit_transversal.py
```

The generator source is opened only as a byte stream when its SHA-256 is checked
against the artifact's `source_hashes` commitment.

## Independent reconstruction

For an artifact with fixed `m`, parent depth `d`, and shard `i/k`, the checker:

1. constructs the separate root `Empty_m`;
2. independently regenerates every complete canonical accepted level from
   depth `0` through depth `d`;
3. recomputes the global ordered parent list at depth `d`;
4. recomputes every half-open boundary

   ```text
   [floor(N*i/k), floor(N*(i+1)/k));
   ```

5. selects the corresponding parent slice and verifies its ordered digest;
6. independently processes every selected parent and reconstructs all child
   commitments.

For each parent it independently forms the endpoint-major/H37-minor raw
extension universe, enumerates `S_m` to recover the exact weighted-parent
stabilizer, partitions the raw universe under `Stab(P)`, and recomputes the
orbit and representative ledgers.  These independently derived ledgers are
cross-checked against the extension-transversal source-interface certificate;
the checker does not merely copy the artifact's digests.

## Exact acceptance conditions

The checker emits

```text
VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD
```

only when all of the following hold:

- artifact status, traversal version, schema, generic-index version,
  transversal-interface version, fixed vertex order, `H37_L`, `MAX_M=10`, and
  fixed `32=NOT_L` agree with the source interfaces;
- all three committed source hashes equal the actual traversal, transversal,
  and generic-indexer files;
- `Empty_m` and every prefix level are reconstructed exactly;
- global parent count, global parent-list digest, prefix-level summaries, and
  prefix payload hashes match;
- the complete half-open boundary table has no gap or overlap and the selected
  parent list matches the artifact parent records exactly;
- each selected parent's raw-extension count and digest, weighted stabilizer,
  exact `Stab(P)` orbit partition, representatives, and transversal payload
  hash match;
- theorem-safe validity, rejection reasons, canonical-parent pass/fail counts,
  duplicate post-gate hits, candidate-gate digest, emitted-child ledger, and
  child-list digest match;
- shard aggregate counts and rejection histograms match;
- the artifact core exactly equals the independently reconstructed core;
- recomputing SHA-256 over that core yields the artifact's
  `certificate_payload_sha256`.

The output also binds the input artifact SHA, checker SHA, reconstructed source
hashes, exact scope and shard interval, prefix-level count, parent and child
commitments, and a deterministic verification-payload SHA.

If `--output` is omitted, the verification JSON is written next to the input as

```text
<artifact-stem>.independent_verification.json
```

No success artifact is written unless every gate above passes.

## Weighted-base boundary

The checker evaluates only literal weighted bases and the already audited
base-validity predicates.  It does not enumerate or validate:

- rootward ports;
- outward masks;
- incidence rows or `I(B)/Stab(B)`;
- high quotients or ordered high arcs;
- high completion;
- least-remote or descent predicates.

A verified shard therefore certifies only that fixed-`m`, fixed-parent-depth,
half-open parent shard.  Proof use still requires exact replayed merge of every
shard at that level.  All-66 coverage additionally requires every relevant
level for every `m<=10`, or a separate structural reduction.

## First Geo command

For the existing unsharded `m=3`, parent-depth `1` artifact:

```bash
cd /home/geo/codex-work/p25-low-schema-lift-20260829/remote_scratch/canonical_traversal_shard_20260830/theory-lab/topwindow

python3 verify_pro_b27_canonical_traversal_shard.py \
  --artifact results/pro_b27_canonical_traversal_m3_d1_0_of_1.json \
  --output results/pro_b27_canonical_traversal_m3_d1_0_of_1.independent_verification.json
```

Run it from this frozen scratch tree so the traversal, transversal and generic
indexer byte hashes match the source hashes embedded in the artifact.  This
command rebuilds
the depth-1 parent layer from `Empty_3` and then replays all selected depth-1
parents.  It performs no incidence expansion.
