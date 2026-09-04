# FW319 `b=27`: cross-translate floor for an L direct 32 edge

The L shape audit leaves one new edge of weight `32` attached at `P0` or
`P1`.  Adding that edge to the fixed L core creates new internal distances.
The carrier root and the two named J endpoints have cross-distance offsets
`w`, `w+r=t`, and `w+r+3=t+3` from the `d6` root, so every enlarged-L depth
produces three actual cross distances.

## Necessary floor

The induced enlarged L core has 36 pair distances and remains injective for
both attachments.  Checking all cross distances from its vertices to `u`,
`y0`, and `y3`, over `w>=38`, `r>=16`, gives:

```text
attachment   excluded t       first jointly compatible (w,r,t)
P0           54,...,76        (43,34,77)
P1           54,...,66        (51,16,67)
```

Each excluded row has an explicit equality between a cross pair and an
internal enlarged-L pair (or a cross-cross equality).  The displayed first
pairs have no collision with this necessary check.  Thus the current `t>=54`
floor sharpens conditionally to `t>=77` for the `P0` shape and `t>=67` for the
`P1` shape.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_direct32_cross_floor.py
```

The replay returns `status: VERIFIED` and checks every admissible `(w,r)` pair
in both finite excluded ranges.  It is a branch-conditioned necessary floor,
not a global exclusion: values beyond the displayed first-compatible pairs,
additional J-side distances, the final cap, and complete spectrum remain.
