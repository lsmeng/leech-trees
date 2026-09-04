# FW319 pre-z `b=27`: carrier translate floor

The first surviving value in the FW319 pre-z tail is `b=27`.  Although this
row is not yet excluded, the complete fixed L-side factor already forces a
substantially stronger lower bound on the actual carrier weight.

## Lemma

In the FW319 `d6/(6,6,6)/O1` pre-z cell with `b=27`, the least-remote carrier
edge `f=d6-u` has

```text
w=d(d6,u) >= 38.
```

## Proof

The exact fixed L factor has edges

```text
d6-c=6, c-z=7, z-b1=1, z-b2=2, z-a=10,
d6-P0=27, c-P1=22.
```

Therefore its named rooted-depth subset and its complete internal spectrum
on those eight vertices are

```text
B0={0,6,13,14,15,23,27,28},
S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
    27,28,29,30,31,33,39,40,41,42,50,55}.
```

The J root itself is the vertex `u`, of `u`-depth zero.  Hence its cross
distances to the vertices of those eight L vertices are exactly

```text
w+B0.
```

All these pairs are cross-cut pairs, distinct from the L-internal pairs
already owning `S0`.  Global distance injectivity requires

```text
(w+B0) intersection S0 = empty.                         (CF)
```

Direct finite evaluation of (CF) gives a collision for every integer
`5<=w<=37`.  The general carrier bound already gives `w>=5`; hence `w>=38`.
`QED`

## Trust boundary

This is a fixed-row translate consequence only.  It neither excludes
`b=27` nor controls the full `b>=27` tail: `w=38` itself passes this one
fixed-factor collision test, and additional vertices and the global cap have
not been incorporated.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_prez_b27_carrier_floor.py
```

**VERIFIED `b=27 => w>=38`; no b=27 exclusion.**
