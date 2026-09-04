# FW318: one-coreward fixed-core attachment cells

FW317 forces at least one monotone-rectangle L endpoint into the fixed-core
component.  In the exactly-one-coreward case the actual fixed core gives a
finite LCA-cell table.  One cell/orientation is impossible, and its reverse
orientation forces five consecutive named owners.

This is the first genuine subfamily exclusion after FW314; it does not
exclude the full monotone rectangle.

## 1. Exhaustive LCA cells

For the coreward endpoint `P_c`, record the `g`-depths of its LCAs with
`(z,b_1,b_2)`.  The actual fixed-core topology gives

```text
g=a:
  (10,10,10), (10,11,10), (10,10,12);

g=d_6:
  (6,6,6), (13,13,13), (13,14,13), (13,13,15).
```

The extra `d_6` cell is the `c`-side cell before the path enters the `z`
subtree.  No interior point of a fixed core edge is an attachment cell,
because the fixed core edges are actual unsubdivided tree edges.

Let `O0` mean that `P_0` is coreward at depth `b` and `P_1` is external at
depth `b+1`; `O1` is the reverse orientation.

## 2. One universal collision

At `g=d_6` in the `(6,6,6)` cell and orientation `O0`,

```text
d(z,P_0)=13+b-2*6=b+1=d(d_6,P_1).
```

The unordered pairs `(z,P_0)` and `(d_6,P_1)` are distinct, so global
distance injectivity excludes this entire subfamily.

The other thirteen cell/orientation rows have no universal affine collision.
All their named distances have forms `b+c_j`, `2b+1`, or a fixed-core
constant; only finitely many `b` values can collide.  The verifier finds
abstract surviving `b` values for every such row.  This is a mechanism
survival statement, not a full FW316 realization.

## 3. Sharp reverse orientation

The reverse `d_6/(6,6,6)/O1` cell has the named owners

```text
value   owner
b       (d_6,P_0)
b+1     (d_6,P_1)
b+2     (z,P_1)
b+3     (b_1,P_1)
b+4     (b_2,P_1).
```

Thus this surviving cell carries a five-consecutive block with every
endpoint and basepoint fixed.

The fixed-core spectrum immediately forces the block away from its existing
owners.  Carrier directness can then test the same `b` values against the
rooted difference three on the J side.  This is the next cheaper target than
another cap estimate.

## 4. Successor and trust boundary

The next task is **Five-Block Reception at the pre-z cell**: combine the
named block with the fixed-core spectrum, the carrier difference-three row,
the FW311 holes, and the FW316 six distances.  Either exclude the reverse
cell or freeze its remaining `b` window.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_attachment_cells.py
```

The replay checks the fourteen affine rows and the fixed-core spectrum.  It
does not construct a carrier, verify complete low coverage, or prove any
owner-mode, order, ERTC, NSSC, or global nonexistence theorem.

**VERIFIED one-cell/orientation exclusion; thirteen rows remain.**
