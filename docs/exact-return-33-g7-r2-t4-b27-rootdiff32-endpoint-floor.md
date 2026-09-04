# FW319 `b=27`: endpoint floor for rooted difference 32

After the L-overlap branch is closed, the remaining Tail-5 alternatives are
ancestor--descendant owners of distance `32` on L or J.  This audit gives a
common endpoint lower bound for both alternatives.

## Lemma

Every L-internal or J-internal ancestor--descendant owner of distance `32`
has both endpoint edges of weight at least `6`.

## Proof

If an endpoint edge has weight `e≤5`, deleting it leaves a pair at distance
`32-e`, hence one of `27,28,29,30,31`.  The fixed L factor has the unique
owners

```text
27: (d6,P0)    28: (d6,P1)    29: (z,P1)
30: (b1,P1)    31: (b2,P1).
```

For a J-internal owner, the shortened pair remains wholly in J and therefore
cannot equal any of these distinct fixed-L pairs.  Thus J has no such small
endpoint edge.

For an L-internal ancestor--descendant owner, global uniqueness forces the
shortened pair to be exactly the displayed fixed-L pair.  Checking both
possible attachment endpoints and retaining only cases where the new endpoint
and the other fixed endpoint are genuinely ancestor--descendant leaves one
candidate: attach a new weight-5 edge at `P0`, extending `(d6,P0)` from 27 to
32.  The induced fixed-L-plus-new-leaf tree repeats distance 55:

```text
d(P0,P1)=55=d(a,new).
```

Hence that candidate is impossible.  Weight `4` is separately forbidden as
the reserved punctured/cap value, so all endpoint edges are at least 6.

The replay enumerates the five fixed owners, both endpoint orientations, and
the resulting distance-injectivity check.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_rootdiff32_endpoint_floor.py
```

## Trust boundary

This is a genuine common endpoint floor, not an exclusion of the rooted
difference-32 branch.  Paths with endpoint edges at least 6 remain open and
must be tested against complete low ownership, the final cap, or least-remote
descent.
