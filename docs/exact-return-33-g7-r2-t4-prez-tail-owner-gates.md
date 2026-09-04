# FW319 pre-z tail: carrier floor and Tail-5 gate exclusions

The low-owner window makes `b+5` an actual uniquely owned distance. Before
classifying arbitrary LCA locations, the fixed rectangle already eliminates
three of its four named endpoint incidences.

## Lemma

In every surviving FW319 pre-z tail state,

```text
w>=16.                                                   (G1)
```

Let `O` be a cross-cut owner of `b+5`.

* `O` cannot use `P0` or `P1` on the L side;
* `O` cannot use the higher monotone J endpoint `y3`;
* hence, if `O` meets one of the four named rectangle endpoints, it can only
  meet `y0` and has the exact L root coordinate `b+5-t`.

This is an endpoint-incidence reduction, not a full Tail-5 anchoring lemma.

## Proof

The carrier pair itself has distance `w`, so it cannot repeat a fixed-core
distance. In particular it avoids

```text
{6,7,8,9,10,11,12,13,14,15}.
```

The only remaining value below 16 allowed by that test is `w=5`. But then
the distinct cross and L-internal pairs satisfy

```text
d(P1,u)=(b+1)+5=b+6=d(c,P0),
```

contradicting injectivity. Together with the pre-existing `w>=5`, this
proves (G1).

For a cross owner of `b+5`, writing its L and J rooted coordinates as
`xB,yR`,

```text
w+xB+yR=b+5.                                            (G2)
```

If `x=P1`, (G2) gives `w+yR=4`, impossible. If `x=P0`, it gives
`w+yR=5`, again impossible by (G1). If the J endpoint is `y3`, then
replacing it by the actual companion endpoint `y0` lowers the cross value by
three, producing a cross pair of distance `b+2`. This repeats the named
L pair `(z,P1)`, so `y3` is impossible.

If the J endpoint is `y0`, then (G2) is exactly

```text
xB=b+5-(w+r)=b+5-t.
```

Thus this remaining named-endpoint incidence is fully coordinate-anchored.
`QED`

## Trust boundary

An owner wholly in L or J, or a cross owner using neither `y0` nor `y3`, is
not excluded. The lemma therefore does not prove root provenance of `b+5`.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_prez_tail_owner_gates.py
```

**VERIFIED Tail-5 named-endpoint gate exclusion; arbitrary owner LCAs remain
open.**
