# Checkpoint — 2026-09-01 — s=152 chain remainder forest

## Scope

This checkpoint covers only `δ=279`, `s=152`, `shape=chain`, even
`d1=38,40,...,124` with `d1<d2<128`. The earlier certified range
`d1=2,4,...,36` is recorded in the preceding checkpoints. It does not cover
`shape=star`, any other `s`, or the global S1-279 claim.

## Exact input

- 44 d1 shards; `params_total=990`, `params_valid=977`.
- Primary/replay canonical signature sets match for every d1 and across d1;
  union size `24077`.
- Exact batch certificate: `VERIFIED_REMAINDER_EXACT_BATCH`.
- Exact batch certificate SHA-256:
  `e655cc21aead5b884aa307c0c27e9a1485ee0d8cad5eaa273d015d7c61dda408`.
- Replay-union SHA-256:
  `d3480e7940cb723832b3a3a937df1e687100d1d171c520fd10382773d9ebb218`.
- Primary/replay-matched union SHA-256:
  `f806df1be77c4633bf6c5ecbfdf08ba644a1108bd7775634f1d0ab217db5d372`.
- FW303 prefilter SHA-256:
  `cfd7d39e2083df15cf89768625f0fd2f46baa8825b218c6f2019477614a20247`.

## Forest and independent replay

The Python forest output has 121 shards, each with status
`FW303_ALL_CLASS_FORESTS_EXHAUSTED`, exact filename/range metadata, and
continuous coverage `[0,24077)`. The independent C++ replay was compiled
from `replay_fw303_all_class_forests.cpp` with `-DALLOW_MIXED_D1` so that it
checks each signature's own valid d1 while retaining the original search
logic. It independently rebuilt all 38 rows and produced 71,578 jobs.

Aggregate result (both implementations):

```text
compatible signatures = 11829
rows A/B/C             = 17847 / 62 / 2
canonical jobs         = 71578
root_sets              = 752797
root_colorings         = 12440449
root_edge_legal        = 11757721
capacity_rejects       = 80610
weight_assignments     = 1493494020
parent_legal           = 16155018
spectrum_survivors     = 0
```

Enhanced verifier result: `VERIFIED_EXACT_PER_JOB_MATCH`; all 15 checks true,
including shard status/range/source-count checks, canonical job-key equality,
all seven per-job counters, aggregate counters, and zero full-spectrum
survivors. `mismatch_count=0`.

Key artifact hashes:

- C++ summary:
  `33ec524d938d0ee920cbe6893b0fc2644e5a578cfee7eac08743421d16397914`
- C++ jobs TSV:
  `7e0d8ca96afa7f916b24c30ee0be5f32698e873b95e639b240b60c6fb03724a1`
- Verification certificate:
  `d9405a3853df12152baaa5f098b358b201c2fd2c167da7506c2cb34c5672d4d9`

## Commands

All heavy commands were run on `geo-ws` with `nice -n 15`; no local heavy
enumeration was run. The final verification command was:

```bash
python3 verify_fw303_all_class.py \
  --replay-signatures exact10_batch_s152_chain_20260901/remainder_exact_union_primary.json \
  exact10_batch_s152_chain_20260901/remainder_forest_shards_v2 \
  exact10_batch_s152_chain_20260901/independent_replay/jobs.tsv \
  exact10_batch_s152_chain_20260901/independent_replay/summary.json \
  exact10_batch_s152_chain_20260901/independent_replay/verification_certificate.json
```

## Proof-state consequence

Combining this checkpoint with the prior `d1<=36` certified checkpoints,
the entire fixed branch `δ=279, s=152, shape=chain`, for every possible even
`d1` (`2<=d1<=124`), is now `CERTIFIED FINITE IMPOSSIBLE`. This is a finite
branch result only. The remaining global gaps are the `s=152` star branch and
the two low-tree shapes for `s∈{154,156,158,160}`, plus the proof that these
branches exhaust the full S1-279/global Leech-tree problem.
