# FW319 pre-z tail: endpoint-rectangle exclusion

After the isolated `b=24` cell is excluded, the pre-z reverse cell has
`b>=27`.  The two named L endpoints and the two J monotone endpoints still
give a small exact cross rectangle.  It rules out many possible carrier-plus-
J-depth values without treating a generic distance as a rooted depth.

## Lemma

Let `P0,P1` be the FW319 pre-z endpoints, with `d(d6,P0)=b` and
`d(d6,P1)=b+1`, and let `y0,y3` be the two J monotone endpoints, with

```text
d(u,y0)=r,       d(u,y3)=r+3.
```

If the carrier edge has weight `w`, put `t=w+r`.  Then global distance
injectivity forces

```text
t notin {5,6,8,9,10,11,12,13,14,15,19,20,22,23}.       (ER)
```

In particular, the already verified carrier bound `w>=5` and `r>=0` give

```text
t in {7,16,17,18,21} union [24,infinity).              (ER')
```

## Proof

The four distinct cross pairs have distances

```text
d(P0,y0)=b+t,     d(P1,y0)=b+t+1,
d(P0,y3)=b+t+3,   d(P1,y3)=b+t+4.
```

The fixed pre-z attachment geometry gives the following already-existing,
distinct L-pair distances:

```text
b+1:(d6,P1),  b+2:(z,P1),   b+3:(b1,P1),
b+4:(b2,P1), b+6:(c,P0),   b+12:(a,P1),
b+13:(z,P0), b+14:(b1,P0), b+15:(b2,P0),
b+23:(a,P0).
```

For each listed value of `t` in (ER), one member of the four cross values
equals one of these fixed L values.  Explicit witnesses are:

```text
t=5,6       -> b+6;
t=8,9,11,12 -> b+12;
t=10,13     -> b+13;
t=14        -> b+14;
t=15        -> b+15;
t=19,20,22,23 -> b+23.
```

The corresponding pairs are cross-cut on one side and L-internal on the
other, so they are distinct.  Each equality contradicts global distance
injectivity.  This proves (ER), and (ER') follows from `t>=w>=5`. `QED`

## Trust boundary

This is a restriction on the *two specific monotone J endpoints*; it does
not bound all depths in `R`, exclude `b>=27`, or classify owners of the
remaining punctured-low values.  The next smallest rigorous target is to
combine (ER') with the complete ownership of a named value such as `b+5`,
while preserving all possible cross owners through other L-core vertices.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_prez_tail_endpoint_rectangle.py
```

**VERIFIED endpoint-rectangle exclusion; `b>=27` remains live.**
