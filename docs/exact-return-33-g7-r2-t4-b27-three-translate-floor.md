# FW319 `b=27`: three named J-translate filter

The existing endpoint-depth audit gives `w>=38`, `r>=16`, and hence
`t=w+r>=54`.  There is a separate necessary condition from the complete fixed
L core: for each of the three J-side vertices `u,y0,y3`, all cross distances
to the eight fixed-L vertices are a translate of the fixed depth set

```text
B0={0,6,13,14,15,23,27,28}.
```

Every translate must avoid the fixed-L internal spectrum

```text
S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
    27,28,29,30,31,33,39,40,41,42,50,55},
```

and the three translates must be pairwise disjoint.  The latter is equivalent
to requiring each offset difference to avoid
`{0} union (B0-B0)_+`.

## Exact low-window result

For `54<=t<=66`, exhaustive integer arithmetic with `w>=38` and `r=t-w>=16`
leaves exactly

```text
t=54: (w,r)=(38,16)
t=59: (w,r)=(43,16)
t=61: (w,r)=(45,16)
t=62: (w,r)=(46,16)
t=63: (w,r)=(47,16)
t=64: (w,r)=(38,26),(48,16).
```

The values `55,56,57,58,60,65,66` have no compatible `(w,r)` under this
necessary filter.  For every `t>=67`, the pair `w=38`, `r=t-38` passes the
filter because all `t`-translates lie above 55 and their gaps from 38 exceed
the maximum fixed-depth difference 28.

Thus the new necessary window is

```text
t in {54,59,61,62,63,64} union [67,infinity).
```

This is a genuine cross-translate refinement, but it does not remove the
J branch: the six isolated values and the entire upper tail remain possible
at this level.  When combined with the existing L direct-32 floors, it is
subsumed by `t>=67` for the `P1` branch and by `t>=77` for the `P0` branch;
its main use is to sharpen the unresolved J single-edge-32 branch.

## Replay and boundary

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_three_translate_floor.py
```

The replay checks the complete low table and the generic upper-tail witness
through a finite audit horizon.  It introduces no unlisted J vertex, no owner
assignment, and no global cap assumption.  Therefore it is a necessary local
filter, not an exclusion or a Leech-tree construction.

**VERIFIED three-translate arithmetic filter; J residual remains open.**
