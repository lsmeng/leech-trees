# Endpoint-tail gap-cap checkpoint

This checkpoint records the current endpoint-strip branch after an
independent local audit of the external advisor's suggestions.  It is not an
all-order nonexistence proof.

## VERIFIED

For a prefix-defect-one core of order `i`, with

```text
C=binom(i,2),
dist(K)={1,...,C-1,C+g}, g>=21,
```

and the forced pendant weight-`1`/weight-`2` fork, let `A,B` be the diameter
leaves and `K0=K-{A,B}`.

1. The endpoint collar implies

   ```text
   diam(K0) <= C-g-2.
   ```

   Therefore every value in `{C-g-1,...,C-1}` is endpoint-cross; no inner
   pair of `K0` owns that high tail.

2. On the inner diameter backbone `P=[A',B']`, all pair distances have gap
   at least four because `1,2,3` are already uniquely realised by the fork.
   The two endpoint translates consequently force at least

   ```text
   floor((g+1)/4)
   ```

   distinct off-backbone vertices to occur in high-tail owners.

3. Since `K0` has only `i-2` vertices and `P` has at least two,

   ```text
   g <= 4i-14.
   ```

   The formerly unbounded outlier search is therefore reduced to
   `C+21 <= D <= C+4i-14`.

4. If the fork root lies on the backbone and two non-fork vertices each own
   both endpoint tail values, then the relevant tail indices are
   three-separated on either fixed side of the fork.  This yields capacity
   `floor(g/3)+1` per side, but does not yet contradict the tail quota.

5. In the separated diameter case, if either
   `d(A,u)<C/2+4` or `d(B,u)<C/2+4`, the corresponding endpoint tail owners
   all meet the fork root at the same backbone gate and are three-separated.
   Therefore

   ```text
   (g+1)-ceil((g+1)/3) <= i-2.
   ```

   At order 18 this gives `g<=24` in this entire near-balanced case.  Any
   larger gap is forced into the narrower balanced interior
   `d(A,u),d(B,u)>=C/2+4`.

6. In that remaining separated interior, relabel the endpoints so that
   `p=d(A,u)<=q=d(B,u)`.  Any `A`-tail owner whose projection is on the
   `A`-to-`u` side is automatically two-sided: its `B`-cross distance also
   lies in the high tail.  If its two tail indices are `a,b`, then

   ```text
   2r=C+g+b-a,  2h=C-g-2-a-b,  b<=a.
   ```

   Thus the sole one-sided `A`-tail escape is the trans side.  This is a
   localisation fact, not a tail-cap contradiction.

7. If additionally the endpoint imbalance is `q-p<=8`, the remaining
   long-side one-sided cis owners all project to a single backbone gate.
   Their nonexceptional `B`-tail indices are three-separated; the exact
   capacity is `ceil((g+1)/3)+3` after retaining the three exceptions
   `u,v1,v2`.  This is a bounded-imbalance classification only; the owner
   channels can still interleave.

8. For two nonexceptional two-sided owners on opposite sides of the fork
   root, with `A/B` tail indices `(a_L,b_L)` on the left and `(a_R,b_R)` on
   the right, the shared fork-root profile forbids the three diagonals

   ```text
   |a_R-b_L-(q-p)| < 3.
   ```

   This rejects the external advisor's proposed three-gate abstract matching:
   two of its advertised owners had the same fork-root depth.  The diagonal
   exclusion is verified, but it alone does not settle all matchings.

9. For strict-left and strict-right two-sided owner sets of sizes `ell,rho`,
   every cross pair has internal distance

   ```text
   C-g-2-b_left-a_right.
   ```

   Global distance injectivity makes the cross sums distinct, hence
   `ell*rho<=2g+1`.  This is the first verified constraint that uses both
   tail matching and true cross-gate internal distances; it is still too
   weak by itself to force a contradiction.

The proofs and narrowly scoped arithmetic replays are in
`prefix-defect-endpoint-strip.md` and the `verify_prefix_defect_endpoint_*`
scripts in `theory-lab/topwindow/`.

## Advisor audit boundary

The advisor correctly pointed toward tail spacing, but two proposed jumps were
rejected:

* it counted every off-backbone tail value as requiring a new vertex; one
  vertex may legally own an `A`-cross and a `B`-cross value;
* it omitted the factor `1/2` in a separated-gate collar inequality.

The corrected gate bound and explicit non-root / two-sided local
countermodels are recorded in `prefix-defect-fork-root-separation.md`.

## OBSERVED bounded search probe

At order `i=18`, the verified cap gives

```text
C=153,
174 <= D <= 211.
```

One controlled shard was compiled from
`forest_prefix_defect_gap.cpp` with this target window and run under a
30-CPU-second limit:

```text
shard=[0,4096,10]
nodes=28,506,530
elapsed=13.556 seconds
target_cores=0
```

No process remained after completion.  This excludes only that fixed shard;
it is diagnostic evidence, not an order-18 theorem or a global conclusion.

## First unclosed implication

The high tail is now known to be endpoint-cross and has a quantitative
off-backbone quota.  The short-side cis owners are also localised as
two-sided, but there is still no bound for the short-side trans owners or the
long-side cis owners, and no theorem converting the complete consecutive tail
into a repeated low distance.  The next proof target is a global owner/LCA
lemma that controls those remaining owner modes, rather than only cardinality
or same-side spacing.

## Checks

```bash
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_endpoint_diameter_cap.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_endpoint_tail_quota.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_endpoint_gap_cap.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_endpoint_two_sided_tail_indices.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_endpoint_unbalanced_tail.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_endpoint_nearbalanced_tail.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_short_side_cis_twosided.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_long_side_one_sided_cis.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_tail_matching_cross_root.py
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_cross_gate_sumset.py
```
