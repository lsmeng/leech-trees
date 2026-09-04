# Audit of the Pro Tail-5 root-provenance proposal

The right-side ChatGPT Pro consultant proposed a four-way classification for
the unique owner of `b+5`.  This audit checks the new finite arithmetic and
records the correction needed before any part of the proposal can enter the
proof state.

## Accepted finite deductions

For `b=27`, an endpoint edge of weight `e<=5` leaves a pair at distance
`b+5-e`:

```text
e=1: 31, whose fixed owner is (b2,P1);
e=2: 30, whose fixed owner is (b1,P1);
e=3: 3, already owned by the fixed core;
e=4: absent from the punctured spectrum;
e=5: 27, whose fixed owner is (d6,P0).
```

The unique fixed edges of weights 1 and 2 have endpoint sets `{z,b1}` and
`{z,b2}`, respectively, so the `e=1,2` rows cannot trim to their displayed
fixed owners.  The `e=5` row leaves exactly the two attachment shapes:

```text
new--d6 = 5 with the remainder ending at P0,
new--P0 = 5 with the remainder ending at d6.
```

For a positive-arm owner with no named fixed overlap, every arm below 16 is
forbidden (fixed spectrum, reserved 4, or the already handled 5-case).  The
arms are distinct.  Their complete finite sums are:

```text
b=27: no pair >=16 has sum 32;
b=28: only (16,17), but 17 is already in the fixed spectrum.
```

Thus the consultant's “deep two-arm” alternative is empty at `b=27` (and at
the adjacent `b=28` boundary), once the separate L-overlap audit is applied.

## Correction and trust boundary

The proposed four-way statement is not exhaustive as written.  It omits the
case where an L-internal positive arm is exactly an existing fixed-L pair.
That case is not accepted from the consultant; it is closed independently by
the committed FW319 multi-edge overlap verifier.  The corrected statement is
therefore “consultant alternatives plus the prior L-overlap closure.”

For a cross owner, the displayed equation

```text
w + x + rho = b+5,
```

and the common-endpoint translate packet are valid identities.  They do not
by themselves exclude the cross owner or turn an arbitrary pair owner into a
new rooted depth.  The L ancestor-32 branch and the J single-edge-32 branch
remain live.

The Pro response itself was written against the weaker pre-b27 bound
`t>=24` (and discussed a `t=21` branch).  In the current b=27 checkpoint the
independently verified floors are stronger:

```text
w>=38, r>=16, t=w+r>=54.
```

Thus the response's `t=21` discussion is stale and is not part of the live
state; only its finite trim/deep-arm arithmetic survives this audit.

Post-closure update: the originally omitted L-internal fixed-overlap class is
now closed by the committed multi-edge audit, and the remaining L
ancestor--descendant class is shape-reduced by the committed L-shape audit.
Therefore, for the current `b=27` state, the consultant alternatives plus
those independent closures leave exactly two non-cross residual shapes:

```text
L: one new edge 32 at P0 or P1;
J: one J edge 32.
```

This is a complete local residual decomposition, not an exclusion of either
shape and not a global theorem.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_consultant_root_provenance_audit.py
```

The replay returns `status: VERIFIED_AUDIT`.  This is an independent audit of
the consultant output, not a global nonexistence theorem.
