# FW319 `b=27`: no simple Tail-5 L-overlap fork

The residual L-overlap case of the Tail-5 owner funnel has a short additional
metric restriction.  It cannot be completed by attaching one new edge at the
LCA; any surviving complementary arm must be genuinely multi-edge.

## Lemma

In the `b=27` Tail-5 owner funnel, suppose the 32-owner is L-internal with a
positive-arm LCA split and one arm is an actual fixed-L rooted arm.  The other
arm cannot consist of one edge.

## Proof

The fixed L tree rooted at `d6` has only six directed rooted-arm candidates
whose complementary length `32-d` is not already a fixed distance (and is not
the absent value 4).  If that complement were a single edge incident to the
same LCA, the following table lists a resulting collision.

```text
fixed arm        d       new edge    collision from new leaf       fixed owner
d6--b1           14      18          leaf--z = 31                 (b2,P1)
d6--z            13      19          leaf--b1 = 33                (c,P0)
d6--c             6      26          leaf--z = 39                 (a,P1)
d6--P0           27       5          leaf--c = 11                 (b1,a)
c--b1             8      24          leaf--d6 = 30               (b1,P1)
c--z              7      25          leaf--d6 = 31               (b2,P1)
```

Each new pair is distinct from the indicated fixed L pair.  Thus every
one-edge completion violates global distance injectivity. `QED`

## Trust boundary

This does not exclude a complementary arm made of two or more edges.  It is a
finite structural restriction on the remaining L-overlap branch, not an
exclusion of `b=27`.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_tail5_no_simple_fork.py
```

**VERIFIED no-simple-fork restriction; the multi-edge branch remains open.**
