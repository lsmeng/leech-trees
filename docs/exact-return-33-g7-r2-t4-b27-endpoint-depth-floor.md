# FW319 `b=27`: named J endpoint-depth floor

The first concrete pre-z tail row has a second fixed-factor restriction beyond
the carrier-weight floor.  The two named J endpoints cannot begin near the
carrier root.

## Lemma

In the FW319 pre-z cell with `b=27`, the named endpoint depths

```text
d(u,y0)=r,       d(u,y3)=r+3
```

satisfy

```text
r>=16.
```

Consequently the verified carrier floor `w>=38` gives

```text
t=w+r>=54.
```

## Proof

The fixed L factor has rooted depths

```text
B0={0,6,13,14,15,23,27,28}
```

and fixed internal spectrum

```text
S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
    27,28,29,30,31,33,39,40,41,42,50,55}.
```

The actual J root pairs have positive lengths among `r,r+3`, so those lengths
cannot belong to `S0`.  Moreover the cross-distance sets from the three J
depths `{0,r,r+3}` to the fixed depths `B0` must be pairwise disjoint.  Thus
the nonzero differences `r,r+3,3` must avoid

```text
(B0-B0)_+={1,2,4,5,6,7,8,9,10,12,13,14,15,17,21,22,23,27,28}.
```

Direct evaluation of `r=0,1,...,15` shows every value violates one of these
two actual-pair tests; `r=16` passes this fixed-factor test.  Hence `r>=16`.
Combining with `w>=38` proves `t>=54`. `QED`

## Trust boundary

This is not an exclusion: the first fixed-factor-compatible depth `r=16`
remains live, as do larger depths.  The statement uses neither a new global
cap inequality nor an owner-to-depth inference.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_endpoint_depth_floor.py
```

**VERIFIED fixed-factor endpoint floor; `b=27` remains open.**
