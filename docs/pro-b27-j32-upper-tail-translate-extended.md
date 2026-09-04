# J32 upper-tail translate-only negative control

The original five-translate probe proves the shallow-endpoint floor
`h >= t+19` only through `t=85` and first finds `(w,r,h)=(54,32,38)` at
`t=86`.  An exact extension of the same predicate over `86 <= t <= 300`
confirms that this is not an isolated accident:

```text
three-translate rows:       26,015
five-translate triples:  2,701,986
floor-violating triples: 1,937,923
t values with violations:     208
first witness: (t,w,r,h)=(86,54,32,38)
last violating t:              300
```

The deterministic replay is

```bash
.venv/bin/python theory-lab/topwindow/verify_pro_b27_j32_upper_tail_translate_extended_probe.py
```

An independent stdin-only replay on `geo-workstation` reproduced exactly the
same four aggregate counts (`26,015`, `2,701,986`, `1,937,923`, and `208`),
without reading or writing the checkout.  This is a cross-host arithmetic
consistency check, not an additional structural assumption.

This is an `OBSERVED_TRANSLATE_PROBE_EXTENDED` negative control.  It shows
that the five fixed-L translates alone cannot close the `t>=86` upper tail.
It is not a weighted-tree counterexample: the full J internal distances,
owner assignments, attachment/LCA state, complete spectrum, and realization
of the order cap are intentionally absent.  The remaining proof target is a
full-J structural lemma or a completeness theorem, not a larger
translate-only scan.
