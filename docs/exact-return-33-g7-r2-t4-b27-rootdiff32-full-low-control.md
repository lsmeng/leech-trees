# FW319 `b=27`: full Tail-5 local control with a J edge `32`

The remaining J alternative survives a stronger local pressure test.  Keep
the exact fixed L factor, choose carrier weight `w=56`, and take named J
depths `16,19`.  Put a single J edge of weight `32` below a J vertex at depth
`61`.  Add one L leaf of weight `34` at `b_2`.

The resulting 14-vertex weighted tree has all `91` pair distances distinct.
The five forced low values have the following actual owners:

```text
32: (p,q)                 J edge
34: (b2,v34)              L
35: (y0,y3)               J
36: (z,v34)               L
37: (b1,v34)              L
```

The local parameters satisfy

```text
w=56>=38,  r=16>=16,  t=w+r=72>=54.
```

This is not a Leech tree: its maximum pair distance is `198`, while its
order-14 cap is `binom(14,2)=91`.  It is therefore an `OBSERVED_CONTROL`, not
a counterexample to nonexistence.  It does show that the fixed factor,
carrier/endpoint floors, the single-edge J shape, and complete internal
ownership of `34,...,37` do not by themselves force a collision.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_rootdiff32_full_low_control.py
```

The remaining exclusion must use the full exact-return spectrum, the final
no-outlier cap, least-remote minimality, or a strict inherited descent.
