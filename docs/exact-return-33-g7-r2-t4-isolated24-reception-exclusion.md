# Isolated-24 Reception Exclusion

The sharp FW319 pre-z reverse cell with `b=24` is impossible under the full
`R2,t=4` punctured-low-spectrum hypotheses. The proof uses the exact 21/22
owner localisation and retains the carrier edge as an actual pair.

## Theorem

In the FW319 `d_6/(6,6,6)/O1` pre-z cell, the surviving parameter value

```text
b=24
```

cannot occur. Consequently that cell's verified FW319 window sharpens from

```text
b=24 or b>=27
```

to

```text
b>=27.
```

## Proof

The `R2,t=4` low window has `s>=24`, so distances 21 and 22 both have unique
actual owners in the punctured low spectrum.

The fixed-root translate and arm-owner analysis proves:

```text
21: J-internal, with its two LCA arms equal to 5 and 16;
22: cross, with 22=w+6+r and
    (w,r) in {(11,5),(12,4),(13,3),(16,0)}.
```

Here `w` is the weight of the actual carrier edge `f=gu`. Therefore `w`
itself is an actual globally unique pair distance.

For the first three rows, `w` is respectively 11, 12, or 13. These values
already have the unique fixed-L owners

```text
11:(b1,a),   12:(b2,a),   13:(d6,z).
```

The carrier edge `(g,u)` is a distinct pair, so all three rows contradict
global distance injectivity.

The only remaining row has `w=16` and `r=0`. But the forced J-internal owner
of 21 has an actual LCA arm of length 16. That arm is a pair entirely inside
`J`, whereas the carrier edge `(g,u)` crosses the cut and has `g` in `L`.
They are distinct unordered pairs of the same distance 16, again
contradicting global distance injectivity.

Every cross-22 row is impossible, while 22 was forced to be cross. Hence the
`b=24` cell is impossible. `QED`

## Trust boundary

This excludes only the isolated `b=24` branch of the stated FW319 pre-z
reverse cell. It does not exclude the surviving tail `b>=27`, the other
attachment cells, the complete monotone rectangle, remote owner modes,
`R2,t=4`, or global Leech-tree existence.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_isolated24_reception_exclusion.py
```

**VERIFIED `b=24` cell exclusion; FW319 pre-z reverse cell now has `b>=27`.**
