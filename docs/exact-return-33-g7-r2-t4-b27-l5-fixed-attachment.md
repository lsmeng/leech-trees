# FW319 `b=27`: fixed-core cells for the forced L edge `5`

The residual audit proves that the complete-spectrum owner of `5` is a
single L edge.  A finite attachment-cell check now rules out all eight
already named fixed-core vertices as its attachment point.

## Verified check

The fixed L core is the weighted tree

```text
d6-c=6, c-z=7, z-b1=1, z-b2=2, z-a=10,
d6-P0=27, c-P1=22.
```

Its 28 pair distances are distinct and have spectrum

```text
{1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
 27,28,29,30,31,33,39,40,41,42,50,55}.
```

For each of `d6,c,z,b1,b2,a,P0,P1`, add one new leaf by an edge of weight
`5` and recompute all pair distances.  Every one of the eight completions
has a repeated distance; the machine-readable verifier records two witness
pairs for each cell.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l5_fixed_attachment.py
```

## Boundary

This only removes direct attachment to the named fixed core.  It does not
show that a remote attachment is impossible, does not locate the `21` owner,
and does not exclude the J or L single-edge `32` residual.
