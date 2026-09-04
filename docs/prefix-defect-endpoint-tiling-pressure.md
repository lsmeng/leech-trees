# Endpoint-strip set-level pressure control

The endpoint-strip theorem gives an exact disjoint owner tiling after removing
the two diameter leaves:

```text
[1,C-1] = dist(K0) disjoint-union (alpha+R_A) disjoint-union (beta+R_B).
```

It is tempting to infer that the inner spectrum has a long initial interval.
That inference cannot use only the set tiling, cardinalities, endpoint lower
bounds, the diameter equation, and the necessary two-root overlap rule.

Here is an exact algebraic pressure control at the first parity-admissible
order not already eliminated by the certified small-core and selective
order-16 audits.  Put

```text
i=18, C=153, g=22, D=C+g=175,
|K0|=16, binom(16,2)=120,
alpha=23, beta=40, d(A',B')=112.
```

The exceptional distance is odd, so the full 18-vertex parity equation has
the admissible bipartition `7*11=77` odd pairs.  Thus this pressure row does
not evade the global parity sieve.

Choose the rooted-distance *sets*

```text
R_A={0,1,2,3,4,5,6,7,8,9,11,13,15,19,21,112},
R_B=112-R_A.
```

Both have the required size sixteen, and their only positive common element
is `112`, the designated distance between the two inner roots.  The profiles
are also metrically matched, not independently invented: pair

```text
(r,112-r) for every r in R_A.
```

Every pair sums to `d(A',B')=112`, so these are the actual two-root distance
profiles of sixteen points on one `A'--B'` path.  The first profile has six
even and ten odd depths. Since `alpha` is odd and `beta` is even, adding the
two diameter leaves gives the compatible full-tree parity split `(7,11)`.
The translated sets are disjoint:

```text
alpha+R_A = {23,...,32,34,36,38,42,44,135},
beta +R_B = {40,131,133,137,139,141,143,144,...,152}.
```

Define `S` to be the complement of those 32 values in `[1,152]`.  Then

```text
|S|=120,
[1,152] = S disjoint-union (alpha+R_A) disjoint-union (beta+R_B),
D=alpha+d(A',B')+beta,
[1,22] subset S, but 23 not-in S.
```

Thus the entire set-level footprint of the endpoint strip is compatible with
the inner spectrum losing its prefix immediately after the inherited gap.
In particular, no proof of a strict descended prefix-defect core may infer
prefix closure from the tiling or from cardinality alone.

This is deliberately **not** an actual *distinct-distance* weighted tree: the
two profiles have a literal path metric, but the complement `S` is not claimed
to be its pair spectrum.  In fact its inner set contains `142`, whereas the
endpoint-strip collar diameter cap is `C-g-2=129`; so it cannot be the pair
spectrum of any actual `K0` under the strip hypotheses.  Hence it is not a
counterexample to endpoint-strip descent.  Its use is narrower and important:
a successful proof must invoke the full internal pair-distance/LCA-owner
geometry together with the inherited `1--2` fork (which this control does not
realize), not merely treat the two translates as ordered blocks or apply
triangle/parity matching to their root profiles.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_prefix_defect_endpoint_tiling_pressure.py
```

**VERIFIED set-level pressure control; no tree realization or all-order
nonexistence claim.**
