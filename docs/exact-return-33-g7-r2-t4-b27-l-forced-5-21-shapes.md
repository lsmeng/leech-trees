# FW319 `b=27`: L-path shapes forced by values 5 and 21

The current residual audit forces the complete-spectrum owners of `5` and
`21` into `L`.  Their path shapes can then be classified without assigning
arbitrary owners to rooted depths.

## Verified reduction

Every edge or contiguous subpath on an L-internal owner path is an actual
pair distance.  A fixed-L distance may occur only when the path literally
uses that same fixed-core pair; a new pair cannot reuse it.  The fixed-L
spectrum is

```text
{1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
 27,28,29,30,31,33,39,40,41,42,50,55}
```

and cannot have the punctured value `4`.

For total `5`, allowing literal reuse of fixed edges still leaves only the
single new edge `(5)`: `1+4` uses the absent punctured value, while `2+3`
reuses a fixed non-edge distance (and other cases repeat an edge or exceed
the total).

For total `21`, the candidate edge multisets, including fixed edge reuse, are

```text
(21), (1,20), (2,19), (5,16), (1,2,18),
(5,6,10), (1,2,5,6,7).
```

The `(1,20)`, `(2,19)`, and `(1,2,18)` placements collide explicitly with
fixed pairs at both possible anchors.  The `(5,6,10)` and `(1,2,5,6,7)`
multisets cannot be simple paths in the fixed-core topology.  Thus only
`(21)`, `(5,16)`, and `(16,5)` survive.  Since the `5` owner is unique,
either two-edge shape uses that same existing 5-edge and adds one new edge
of weight `16`.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_forced_5_21_shapes.py
```

The replay returns `status: VERIFIED` and records the collision witnesses.

## Boundary

This is a finite path-shape reduction only.  It does not locate the
attachment vertices, constrain the LCA of the two owners, or exclude either
remaining `32` residual.  The next exact test is the interaction of these
three L-shapes with the J single-edge-32 branch under full cross-distance,
root-shift-four, and cap checks.
