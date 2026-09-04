# FW319 `b=27`: Tail-5 owner funnel

At `b=27`, the forced unique owner of `b+5=32` is much more constrained than
the generic Tail-5 owner.  The result below is an exact owner classification
up to two residual rooted cases; it deliberately does not claim that either
residual is impossible.

## Lemma

In the FW319 pre-z cell with `b=27`, let `O` be the unique owner of
`b+5=32`.  Then exactly one of the following holds:

1. `O` is L-internal and is an ancestor--descendant pair, so 32 is an
   actual positive `d6`-rooted depth difference;
2. `O` is J-internal and is an ancestor--descendant pair, so 32 is an
   actual positive `u`-rooted depth difference;
3. `O` is L-internal with a positive-arm LCA split, and one of its two
   LCA-to-endpoint arm pairs is exactly an already-existing fixed-L pair.

In particular, `O` is never cross-cut, and a J-internal owner never has a
positive-arm LCA split.

## Proof

The verified carrier floor is `w>=38`.  A cross-cut distance has form
`w+xB+yR>=38`, so it cannot equal 32.  Thus `O` is L-internal or J-internal.

Root the relevant component at `d6` (on L) or `u` (on J), and split `O` at
its actual LCA.  If one arm has length zero, this is an ancestor--descendant
pair, giving cases 1 or 2.

Suppose both arms are positive.  On the fixed L side at `b=27`, the complete
eight-vertex fixed spectrum is

```text
S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
    27,28,29,30,31,33,39,40,41,42,50,55}.
```

If a positive arm pair has a length in `S0`, global injectivity makes it the
same actual pair as the fixed L pair owning that length.  This produces case
3 on the L side.  On the J side it is impossible, because the components are
disjoint.

It remains to consider two arm pairs whose lengths avoid `S0`.  Distance 4 is
absent from the full spectrum.  Below 32, the remaining possible lengths are

```text
{5,16,18,19,20,21,24,25,26}.
```

No two *distinct* members of this set sum to 32.  Equal arms are also
impossible, since the two distinct LCA-to-endpoint pairs would have equal
distance.  Hence an unanchored positive-arm split cannot occur. `QED`

## Audit correction

This is the audited replacement for the Pro advisor's proposed four-way
"Tail-5 Root-Provenance Lemma."  That proposal omitted the L-internal
positive-arm case where an arm already equals a fixed-L distance; it therefore
was not exhaustive as written.  The present statement retains that necessary
overlap case explicitly.

## Trust boundary

The lemma leaves the two ancestor--descendant alternatives: a rooted
difference 32 on L or on J.  The separate FW319 multi-edge overlap audit
closes the L-internal positive-arm overlap alternative, and the endpoint-shape
audit reduces the J alternative to a single edge of weight 32.  None of these
local results excludes `b=27` or establishes global nonexistence.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_tail5_owner_funnel.py
```

**VERIFIED finite owner funnel; the L rooted branch and the single-edge J
branch remain open.**
