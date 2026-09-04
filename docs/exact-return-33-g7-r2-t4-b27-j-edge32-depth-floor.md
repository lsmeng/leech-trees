# FW319 `b=27`: J single-edge-32 endpoint-depth floor

The three named J-translate filter leaves six isolated low values of `t`:

```text
t in {54,59,61,62,63,64}.
```

In the remaining J branch, the owner of `32` is a single edge.  Root J at
`u`, orient that edge from its shallower endpoint `p` to its deeper endpoint
`q`, and put

```text
h=d(d6,p).
```

Then `d(d6,q)=h+32`.  The cross distances from the fixed L core to
`u,y0,y3,p,q` are five translates of

```text
B0={0,6,13,14,15,23,27,28}.
```

Each translate must avoid the complete fixed-L spectrum `S0`, and distinct
translates must be disjoint.  Exhausting the finite low rows gives:

```text
t=54: (w,r)=(38,16), h>=73=t+19
t=59: (w,r)=(43,16), h>=78=t+19
t=61: (w,r)=(45,16), h>=80=t+19
t=62: (w,r)=(46,16), h>=81=t+19
t=63: (w,r)=(47,16), h>=82=t+19
t=64: (w,r)=(38,26) or (48,16), h>=83=t+19.
```

The verifier checks every candidate `h` from `w` through `t+18` and finds
none; it also records a compatible `h` witness above the floor for each row,
so this is a sharp bound for this relaxed translate test.

This is a genuine placement restriction on the unresolved J edge, but it is
not an exclusion.  The edge may still sit farther out, and the unknown J
LCAs and the full exact-return/cap conditions have not been used.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_j_edge32_depth_floor.py
```

**VERIFIED branch-conditioned endpoint-depth floor; J residual remains open.**
