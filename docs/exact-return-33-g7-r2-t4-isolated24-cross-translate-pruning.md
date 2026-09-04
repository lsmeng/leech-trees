# Isolated-24: cross-translate pruning for low owners

In the sharp FW319 `b=24` cell, complete low ownership of 21 and 22 can be
tested against the *whole* translate caused by any one cross-cut endpoint.
This gives an owner-class reduction without identifying a generic distance
owner with a rooted depth.

## 1. Fixed translate data

Root the L factor at the carrier gate `g=d_6`.  The fixed core and the two
named five-block endpoints give the rooted subset

```text
B0={0,6,13,14,15,23,24,25} subset B.
```

The already uniquely owned distances are

```text
S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,19,23}
   union {24,25,26,27,28}.
```

Suppose a new low distance `m` has a cross-cut owner `(x,y)`, where
`d(g,x)=b in B0`, `d(u,y)=r in R`, and the carrier edge has weight `w`.  Put
`t=w+r`.  The same vertex `y` has distances

```text
d(x',y)=t+d(g,x')       for every fixed x' with depth in B0.
```

As all the pairs `(x',y)` are distinct from the pairs already owning `S0`,
global injectivity requires

```text
(t+B0) intersect S0 = empty.                         (CT)
```

This is stronger than checking only the nominated distance `m=t+b`.

## 2. Exact low-owner consequences

Checking every `b in B0` with `t=m-b>0` gives:

```text
m=21:  every candidate translate meets S0;
m=22:  the sole collision-free candidate is b=6, t=16.
```

Hence 21 cannot have a cross-cut owner.  Its required owner is L-internal or
J-internal.  A cross owner of 22, if one exists, is necessarily

```text
22 = w + 6 + r,       w+r=16,                         (CT22)
```

where the L endpoint is the fixed depth-six vertex `c`.

The FW309 carrier lower bound is `a+w>=19`; here
`a=d(b_1,d_6)=14`, so `w>=5`.  Also `0 in R`, and directness gives
`(R-R)_+ intersect (B-B)_+=empty`.  Applying this to
`r=16-w` and the displayed `B0` subset leaves only

```text
(w,r) in {(11,5),(12,4),(13,3),(16,0)}.              (CT22')
```

## 3. Trust boundary and successor

This proves no rooted reception and no exclusion of `b=24`: an L-internal or
J-internal owner of 21 remains possible, and 22 can also be L/J-internal.
It does, however, replace the unrestricted cross-owner alternative by one
named L endpoint and four carrier arithmetic rows.  The next exact task is
to retain the LCA of an internal 21 owner together with these four possible
cross-22 rows, and test their full translates against the five-block and the
complete punctured interval.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_isolated24_cross_translate.py
```

**VERIFIED cross-owner pruning; Isolated-24 Reception remains open.**
