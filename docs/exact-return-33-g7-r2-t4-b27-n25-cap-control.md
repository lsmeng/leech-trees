# FW319 `b=27`: J-edge-32 control below the order-25 cap

The remaining J branch survives even after imposing the global cap available
at the first open Taylor order.  This is a deliberately incomplete local
control, so it is evidence against a cap-only closure, not a counterexample
to Leech-tree nonexistence.

## Control

Use the fixed `b=27` L factor and add the following edges:

```text
d6--u = 45,
u--v = 38,
v--y0 = 16,
v--y3 = 19,
u--p = 86,
p--q = 32,
b2--v34 = 34.
```

The named J endpoint depths from `u` are `54` and `57`, so their difference
is three and `t=w+r=99`.  Their actual pair distance is `35`.  The five
relevant owners are

```text
32: (p,q),       34: (b2,v34),
35: (y0,y3),     36: (z,v34),
37: (b1,v34).
```

The induced tree has 15 vertices and 105 pair distances.  Every edge weight
and every pair distance is distinct, and the maximum pair distance is `212`.
For order `25`,

```text
N = binom(25,2) = 300,
```

so this local control lies 88 below the global cap.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_n25_cap_control.py
```

The replay returns `status: OBSERVED_CONTROL`.

## Consequence and boundary

The fixed factor, `w>=38`, the branched J endpoint pair, a single J edge of
weight 32, actual ownership of 34--37, and the order-25 global cap do not by
themselves force a collision.  The control is not a Leech tree: it has only
15 vertices, does not realize the complete `1,...,300` spectrum, and does
not satisfy least-remote minimality.  The remaining exclusion must therefore
use complete-spectrum reception, a cap-aware rooted descent, or a stronger
global invariant.

**OBSERVED_CONTROL; cap-only closure is refuted for this local branch.**
