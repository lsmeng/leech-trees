# FW319 `b=27` tail: endpoint-band exclusion

The generic endpoint rectangle leaves the live FW319 pre-z tail at `t>=24`.
At the first concrete value `b=27`, the same two named J endpoints give a
further finite band exclusion.  This statement keeps every witness as an
actual pair; no distance owner is reinterpreted as a rooted depth.

## Lemma

In the FW319 pre-z cell, suppose `b=27`.  Let `t=w+r`, where the named J
endpoints satisfy `d(u,y0)=r` and `d(u,y3)=r+3`.  Then

```text
t notin {24,25,...,42}.
```

Together with the already verified live-tail condition `t>=24`, this gives

```text
b=27  =>  t>=43.
```

## Proof

Root `L` at `d6`.  The three used L vertices have depths

```text
d(d6,d6)=0,  d(d6,c)=6,  d(d6,z)=13.
```

Thus each pair `(x,y0)` has distance `d(d6,x)+t`, and `(x,y3)` has distance
`d(d6,x)+t+3`.  The following table gives, for every possible `t` in the
displayed band, an equal already-existing L-internal distance.

```text
t       cross pair       distance       equal L-internal pair
24      (c,y0)           30             (b1,P1) = b+3
25      (c,y0)           31             (b2,P1) = b+4
26      (z,y0)           39             (a,P1)  = b+12
27      (d6,y0)          27             (d6,P0) = b
28      (d6,y0)          28             (d6,P1) = b+1
29      (z,y0)           42             (b2,P0) = b+15
30      (d6,y3)          33             (c,P0)  = b+6
31      (c,y3)           40             (z,P0)  = b+13
32      (c,y3)           41             (b1,P0) = b+14
33      (c,y3)           42             (b2,P0) = b+15
34      (c,y0)           40             (z,P0)  = b+13
35      (c,y0)           41             (b1,P0) = b+14
36      (c,y0)           42             (b2,P0) = b+15
37      (d6,y3)          40             (z,P0)  = b+13
38      (d6,y3)          41             (b1,P0) = b+14
39      (d6,y3)          42             (b2,P0) = b+15
40      (d6,y0)          40             (z,P0)  = b+13
41      (d6,y0)          41             (b1,P0) = b+14
42      (d6,y0)          42             (b2,P0) = b+15
```

The pair in the middle column is cross-cut, while the final pair is entirely
inside `L`; therefore the two pairs are distinct.  Every row contradicts
global distance injectivity. `QED`

## Trust boundary

This improves the `b=27` tail floor but does **not** exclude `b=27`: values
`t>=43` remain open, and the Tail-5 Owner Anchoring gap is not addressed.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_tail_band.py
```

**VERIFIED finite endpoint-band exclusion; no global nonexistence claim.**
