# P25 low-state raw-index and shard contract

This document freezes the enumeration interface before any `m=4` run.  It is
a reproducibility contract, not a P25-surjectivity claim.

## Raw-state ordering

The global order is lexicographic in the following fields:

1. `m` (number of anonymous vertices);
2. `e_new` (number of added low edges);
3. the lexicographic rank of the sorted endpoint-set combination;
4. the lexicographic rank of the ordered distinct weight assignment;
5. the lexicographic rank of the component port choices;
6. the lexicographic rank of the outward-incidence masks.

For each fixed `(m,e_new,endpoint-set,weight-assignment)` **base block**,
components are sorted by their sorted vertex lists.  A component's port
options are sorted by vertex name; its mask is the binary integer obtained from
that same sorted vertex list.  The raw domain is hierarchical:

```text
base block -> preliminary-graph validity
           -> invalid-base sentinel (one state), or
              all component ports × all incidence masks
```

Consequently, if `B` is a base block and `I(B)` says it is invalid,

```text
block_count(B) = 1
```

otherwise `block_count(B)` is the product of its port and mask radices.  This
fixes the otherwise ambiguous question of assigning incidences to a cyclic or
multi-attached graph.  A raw state is identified by the tuple of its base
indices plus (when the base is valid) its port/mask indices, never by a
filesystem order or a hash.

Every indexed state is emitted with `accepted`; rejected states also carry
`rejection_stage` (`base`, `incidence`, `pair-closure`, or `shape`) and an
explicit `rejection_reason` such as cycle, multiple fixed attachment,
puncture, or distance collision.  Counting only states returned by a
`build_rows`-style filter is not coverage: it silently removes rejected states
and cannot prove that the raw interval was processed.

The implementation must expose inverse `unflatten` and verify both identities:

```text
flatten(unflatten(i)) = i
unflatten(flatten(state)) = state
```

The semantic ordering version and all fixed constants enter
`semantic_input_hash`.

## Shard boundaries and checkpoints

Each remote shard owns exactly one half-open interval `[start,end)` of the
global raw index.  Its artifact records:

```text
semantic_input_hash, raw_schema_version, ordering_version, global_raw_count
base_block_count
start, end, processed_raw, accepted_raw
first_flat_index, last_flat_index, index_digest
index_digest_scope, global_index_digest (when the shard is the full interval)
```

Acceptance requires `processed_raw == end-start`.  Periodic checkpoints record
`next_flat_index`, `processed_raw`, accepted count, and rolling index/raw-state
digests.  A timeout, parse error, or incomplete checkpoint is `INCOMPLETE` and
cannot be merged.

The merge verifier sorts shards by `start` and requires

```text
start_0 = 0
end_i = start_(i+1)
end_last = global_raw_count
```

with one common semantic hash.  Thus no gap or overlap can hide a raw state.
`index_digest` is checked within each shard; a full-interval reference run
records `global_index_digest`, which the merge verifier compares against its
recomputed digest.

## Canonical/orbit merge

Every accepted raw state contributes `(flat_index, canonical_json_key,
raw_state_hash)`.  For a canonical key `k`, the merged orbit size is

```text
orbit_size(k) = sum_s count_s(k)
```

and the verifier checks
`sum_k orbit_size(k) == sum_s accepted_raw_s`.  The canonical representative
is selected by the lexicographically least structural JSON; SHA-256 is only its
digest.  The independent checker must recompute that minimum, not minimize
digests.

## Theorem-level limits still in force

This contract does not by itself establish P25 low-decoder surjectivity.  A
full catalogue additionally needs literal `(5,16)` shared-path handling for
21, explicit non-L ownership of the J-32 edge, and a proved treatment of the
34--37 geometry.  Until those fields and quantifiers are materialized, any
larger run remains protocol evidence only.
