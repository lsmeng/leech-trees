# FW319 `b=27`: early low-owner separation

The `b=27` carrier translate floor and the certified low-owner window combine
to remove the entire cross-cut color for the first forced owners.  This is an
actual distance comparison, not an endpoint-anchoring assumption.

## Lemma

In the FW319 pre-z cell with `b=27`, the unique actual owners of

```text
32, 34, 35, 36, 37
```

are internal to `L` or internal to `J`.  In particular, the unique owner of
`b+5=32` is not cross-cut.

## Proof

The verified `b=27` carrier translate lemma gives

```text
w=d(d6,u)>=38.
```

Every cross-cut pair has the form `(x,y)` with `x` in `L`, `y` in `J`, and
has distance

```text
d(x,y)=xB+w+yR>=w>=38,
```

because rooted depths `xB,yR` are nonnegative.  The certified pre-z
low-owner window gives unique actual owners at offsets

```text
b+{5,7,8,9,10}={32,34,35,36,37}.
```

All five values are strictly below 38, so none can be cross-cut.  Their
owners must therefore be L-internal or J-internal.  Taking the first value
proves the stated Tail-5 consequence. `QED`

## Boundary

The next forced value is `b+11=38`.  In the equality case `w=38`, its owner
may be the carrier edge itself, so this argument intentionally makes no claim
at 38 or above.  Nor does it decide whether the five separated owners lie in
`L` or in `J`, and it does not exclude `b=27`.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_low_owner_separation.py
```

**VERIFIED owner-color separation below the carrier floor; global
nonexistence remains open.**
