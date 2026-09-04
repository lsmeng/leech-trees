# Scratch advisory: `m=4`, depth-3 64-way canonical traversal

Date: 2026-08-30

Status: **non-authoritative bounded advisory**.  This note records a read-only
snapshot and proof/interface audit.  It does not modify `research_state.md` or
an authoritative checkpoint, does not launch a remote job, and does not claim
completion of the depth-3 layer, all-66 coverage, incidence coverage, high
completion, or Leech-tree nonexistence.

## VERIFIED

### Fixed parent layer and source snapshot

The authoritative parent layer for the current computation is

```text
/home/geo/codex-work/leech-trees/remote_scratch/
  canonical_traversal_shard_20260830/theory-lab/topwindow/results/
  pro_b27_canonical_traversal_m4_d2_0_of_16.layer_merge.json
```

with SHA-256

```text
b22486d8379e4e38e090c0877c42ebced65bb56cf70dbf519807d8c7fbd22610
```

and scope

```text
m=4, parent_depth=2, child_depth=3,
canonical_base_count=3803,
weighted_base_only=true,
incidence_rows_enumerated=0.
```

Every inspected depth-3 shard binds this exact parent-layer SHA and the same
source hashes:

```text
runner
466ce529e85dca803de77980cf2c99ecf92afa6091fc526c656df4e48322441b

independent checker
378c0bb30695eaf64e2c9a68a5ec70d94acfa6e28fae267309bfd8011fb2fec2

layer merge
6c4129e2de6bdd78cf26769c8f31aefe3df8a240de90fafe9654d6f074dccf12

extension transversal
fb127ff978241efafa856c350e52c9f804cf88ea9d6789b60558b8420451e496

generic indexer
f524f469461de1304eadb33c077122ede55e01c4b9b06444c6387f25fd201ebd
```

### Current Geo batch snapshot

At the final snapshot, the sequential batch over shards `5..8` had ended and
no matching traversal/replay worker remained active.  Generator and independent
replay artifacts exist and pass for shards `0..8`, so the current exact state
is **9/64 verified shards**, not the older local checkpoint's 5/64 state.

| shard | parent interval | generator SHA-256 | replay SHA-256 | depth-4 children |
|---:|---:|---|---|---:|
| 0 | `[0,59)` | `f8d844362996f8c4ae2ae31fdda2c11653369845049ad48e8bd918d140e569f6` | `573c421e2f4412e3f75799e7d27058200792ec001007da3df17a013e4c32dd66` | 21 |
| 1 | `[59,118)` | `783b19d449bd1b7b1f87a58470723b77549d5227894de2a461a3ca6519d4d5cc` | `47b1cb9d28178da1e8cea51bdbab843c8dade54bcf5542498d553ac457d53189` | 92 |
| 2 | `[118,178)` | `e490a2e00d62501b0e0ee89aa07b8b964c33c35586578b64e654d570c80a6232` | `df907b7f4a831e93fc2d5eb7ef3b2f2b0bb51fee8cf19d7e75fbaff36a061a13` | 83 |
| 3 | `[178,237)` | `90ed030f432cf32905498680eaffdec6737d97d547748e9c24c817f73f91da07` | `8947b8773eeab77f60029b8c44ab735d91167016dd2d1e32401b678c675b7f2e` | 42 |
| 4 | `[237,297)` | `8405e2a75c19a768f60f2202fd4c17ac73b89920310471d8cf964b3e7de36e4d` | `caa54ff0feb5e11b0d3a903865179ee33e498b88f6c8f73e642bdc3c0b88dbef` | 175 |
| 5 | `[297,356)` | `680678902e4815522feed53994129a85d7f3a243fee755d5e05f7b42d8f5de96` | `5e46275376c2744fcc9d8a4945fd2d6c8c622c60bc54a72aef6664b29b5f14ba` | 129 |
| 6 | `[356,415)` | `51001a8b47917a9adc6143ead59b8fe3781ed1948c7b647aa0e0612b3bed0fa9` | `6f7816703fe0316ad964ec2f0df540bcee18d1e42236676ea8b7137dcd91840b` | 47 |
| 7 | `[415,475)` | `752d982649b7fea90bc5e5493299d1e014af19998f9e848191b9b04ae1cdd169` | `bd03fe5de80bc657f62dcdc07d0b095ee4c09475d45afe505fe8faaf5bb1d503` | 39 |
| 8 | `[475,534)` | `6941fb60057621392a3ed30d52bafbf1c945974448e1f45b41ec068477855e48` | `aea26b2d85ed1099c5357e2d0e6dc5bb0383948a395b45c1319101f61cf04271` | 19 |

The verified prefix therefore covers exactly

```text
parent indices     [0,534)
parent count        534
raw extensions      336420
Stab-parent orbits  286610
depth-4 children    647
```

The 647 emitted child serializations are pairwise distinct across these nine
shards.  Every replay has status

```text
VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD
```

and independently verifies parent-layer provenance, raw extension universes,
weighted stabilizers, orbit partitions, validity/gate ledgers, complete child
ledgers, source hashes, and payload hashes.

## OBSERVED

### No current uniform shortcut over the remaining parents

For every depth-3 parent in this fixed `m=4` layer,

```text
|E_4| = 15*4 + C(4,2) = 66,
raw_extension_count = (66-3)*(13-3) = 630.
```

The first eight replayed shards contain 475 parents.  Their parent-level data
show:

```text
zero-child parents       271
positive-child parents   204
maximum children/parent   11
stabilizer size 1         219
stabilizer size 2         256
candidate-orbit range     460..630
```

Thus the canonical/gate structure is not uniform across the observed prefix:
some parents have no valid gated extension, while nearby parents have between
one and eleven.  Existing theorems give a deterministic unique canonical
parent for every depth-4 child, but they do not give a parent-independent
criterion that makes all omitted parents childless.

### Consequence of canonical-parent uniqueness

Let `P_3(4)` be the 3,803 canonical accepted depth-3 bases.  For each
`P in P_3(4)`, let `C(P)` be the set obtained by evaluating every
`Stab(P)`-orbit representative in `U_raw(P)`, applying theorem-safe validity,
and retaining exactly the children that pass the canonical-parent gate.
The canonical-parent definition gives

```text
P != Q  =>  C(P) and C(Q) are disjoint.
```

Therefore a completed shard cannot cover any unprocessed parent's children.
Under the present computational route, the only two sound ways to close the
layer are:

1. process every one of the 3,803 parent indices; or
2. prove, separately, `C(P)=empty` for every omitted parent.

No such zero-child theorem is present in the current proof state, and the
observed heterogeneity supplies no basis for asserting one.

## OPEN

### First unclosed logical quantifier

The first unclosed weighted-base quantifier is

```text
for every P in P_3(4),
  for every orbit O in U_raw(P)/Stab(P),
    the traversal evaluates one representative of O; and
    whenever P+q is theorem-safe valid and
      Parent(Can(P+q)) = P,
    Can(P+q) appears exactly once in the depth-4 ledger.
```

The nine verified shards discharge this only for `P` in the half-open prefix
`[0,534)`.  The remaining open parent interval is

```text
[534,3803), 3269 parents, shards 9..63.
```

Hence all 64 generator shards and all 64 matching independent replays are
required by the current merge contract.  The existing 9/64 files cannot be
mixed with a new 128-way partition because the merge requires one common
`shard_count`, complete indices `0..K-1`, and the exact common boundary table.

### Runner/checker/merge audit

The current v2 interfaces are sufficient for the next nonterminal merge:

- the runner consumes the verified depth-2 merge without silently rebuilding
  the parent layer and emits a complete `child_layer_bases` ledger;
- the checker independently reloads the same verified parent layer and rebuilds
  all selected-parent transversal/gate/child commitments;
- the merge requires all shard indices, exact half-open coverage of `[0,3803)`,
  one matching replay per artifact, common source and parent-layer provenance,
  and globally unique child serializations;
- the resulting scope will be
  `m=4, parent_depth=3, child_depth=4`, exactly what a terminal
  `--m 4 --depth 4 --parent-layer <merge>` run requires.

No concrete blocker was found for completing the depth-3 merge.

There is one future interface boundary: the current layer merge deliberately
rejects terminal artifacts whose `child_depth` is `null`.  Therefore:

- one unsharded terminal depth-4 generator plus replay needs no merge and is
  fully supported;
- if the eventual depth-4 parent count makes an unsharded terminal run too
  large and terminal processing must be split, runner/checker can certify each
  terminal shard but there is presently no metadata utility that certifies the
  union of multiple terminal shards as exact coverage of all depth-4 parents.

This is not a blocker for the current 64-way depth-3 computation.  It should be
revisited only after the depth-4 merged parent count is known.

## Recommendation

**Continue the existing 64-way partition.**  Nine consecutive shards and their
independent replays have completed under the frozen source and parent-layer
hashes.  Changing partition size now would strand those verified shards under
the current exact merge contract.  Continue sequentially in small batches so a
single timeout stops before later shard indices are started.

### Next bounded Geo command

Run this only when no canonical traversal/replay process is active.  The guard
exits with code 75 instead of overlapping another batch.  It advances shards
`9..12` and stops on the first generator/replay failure.

```bash
ssh geo-ws '
set -euo pipefail
ROOT=/home/geo/codex-work/leech-trees/remote_scratch/canonical_traversal_shard_20260830/theory-lab/topwindow
cd "$ROOT"

if pgrep -af "[p]ro_b27_canonical_traversal_shard.py --m 4 --depth 3|[v]erify_pro_b27_canonical_traversal_shard.py --artifact results/pro_b27_canonical_traversal_m4_d3" >/dev/null; then
  echo "REFUSE_OVERLAP: an m4 depth3 generator/replay is active" >&2
  exit 75
fi

for i in 9 10 11 12; do
  artifact="results/pro_b27_canonical_traversal_m4_d3_${i}_of_64.json"
  replay="results/pro_b27_canonical_traversal_m4_d3_${i}_of_64.independent_verification.json"
  test ! -e "$artifact"
  test ! -e "$replay"

  /usr/bin/time -v timeout 180s python3 \
    pro_b27_canonical_traversal_shard.py \
    --m 4 --depth 3 \
    --shard-index "$i" --shard-count 64 \
    --parent-layer results/pro_b27_canonical_traversal_m4_d2_0_of_16.layer_merge.json \
    --output "$artifact" \
    > "results/pro_b27_canonical_traversal_m4_d3_${i}_of_64.log" 2>&1

  /usr/bin/time -v timeout 180s python3 \
    verify_pro_b27_canonical_traversal_shard.py \
    --artifact "$artifact" \
    --parent-layer results/pro_b27_canonical_traversal_m4_d2_0_of_16.layer_merge.json \
    --output "$replay" \
    > "results/pro_b27_canonical_traversal_m4_d3_${i}_of_64.independent_verification.log" 2>&1
done
'
```

Expected parent intervals are

```text
shard  9: [534,594), 60 parents, aggregate raw extensions 37800
shard 10: [594,653), 59 parents, aggregate raw extensions 37170
shard 11: [653,713), 60 parents, aggregate raw extensions 37800
shard 12: [713,772), 59 parents, aggregate raw extensions 37170
```

### Stop conditions

Stop the batch and do not start a later shard if any of the following occurs:

- overlap guard returns 75;
- generator or replay exits nonzero, including timeout exit 124;
- source hashes differ from the frozen values above;
- parent-layer SHA differs from `b22486d...2610`;
- `global_parent_count != 3803`;
- declared interval differs from the expected half-open interval;
- any parent has `raw_extension_count != 630`;
- aggregate raw extensions differ from `630 * parent_count`;
- generator status is not
  `VERIFIED_PRO_B27_CANONICAL_TRAVERSAL_SHARD_INTERNAL_CHECKS`;
- replay status is not
  `VERIFIED_INDEPENDENT_PRO_B27_CANONICAL_TRAVERSAL_SHARD`;
- replay's artifact SHA, child count/digest, parent-source commitment, or source
  hashes fail to match the generator artifact;
- `incidence_rows_enumerated != 0`.

After all 64 shards satisfy these gates, run the existing exact merge over all
64 generator and 64 replay files.  Do not attempt the terminal depth-4 step
before that merge produces a verified `m=4, parent_depth=3, child_depth=4`
parent layer.
