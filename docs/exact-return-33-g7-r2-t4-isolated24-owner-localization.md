# Isolated-24: exact localization of the 21 and 22 owners

The fixed `b=24` L factor turns the previously generic low-owner question
for 21 and 22 into two finite owner statements.  This uses actual unique
fixed-pair owners and the carrier-cut decomposition; it does not identify an
arbitrary low distance with a rooted depth.

## 1. Fixed arm-owner table

At the `d_6` root, the relevant fixed L distances have these unique owners:

```text
 2: (z,b2)       6: (d6,c)       7: (c,z)
 8: (c,b1)       9: (c,b2)      10: (z,a)
11: (b1,a)      12: (b2,a)      13: (d6,z)
14: (d6,b1)     15: (d6,b2)     19: (c,P1).
```

The fixed root-depth subset remains

```text
B0={0,6,13,14,15,23,24,25} subset B,
```

whose positive difference set is

```text
E={1,2,6,7,8,9,10,11,12,13,14,15,17,18,19,23,24,25}.
```

## 2. Distance 21

The carrier-cut partition says that the unique owner of 21 is L-internal,
J-internal, or cross.

* The cross class is impossible by the fixed-translate pruning.
* For an L-internal owner, its two positive LCA arms must be in `E` and sum
  to 21.  The only unordered pairs are

  ```text
  {2,19}, {6,15}, {7,14}, {8,13}, {9,12}, {10,11}.
  ```

  Their actual fixed owner pairs either have no common endpoint, or share an
  endpoint but leave along the same first edge.  They therefore cannot be
  the two distinct branches below one LCA.  Thus L-internal is impossible.
* For a J-internal owner, both arms are positive `R` differences and hence
  avoid `E` by directness.  The only two positive integers outside `E` that
  sum to 21 are `{5,16}`.

Therefore the owner of 21 is necessarily J-internal, with its two LCA arms
equal to 5 and 16 in either order.

## 3. Distance 22

For L-internal ownership, the arm pairs from `E` are

```text
{7,15}, {8,14}, {9,13}, {10,12}, {11,11}.
```

The first four have the same no-common-endpoint/same-first-edge obstruction
as above.  The final pair would create two distinct paths of distance 11,
contradicting global distance injectivity.  Hence 22 is not L-internal.

For J-internal ownership, no two positive integers outside `E` sum to 22.
Hence 22 is not J-internal either.  The cross-translate theorem now forces
the sole remaining class:

```text
22 = w + 6 + r,
(w,r) in {(11,5),(12,4),(13,3),(16,0)}.
```

The L endpoint is the named fixed vertex `c` at `d_6`-depth six.

## 4. Resolved successor

The forced 21 arm of length 16 and the four cross-22 carrier rows give an
immediate collision; see
`exact-return-33-g7-r2-t4-isolated24-reception-exclusion.md`.  Thus this
localisation does exclude the `b=24` cell once the actual carrier edge itself
is retained.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_isolated24_owner_localization.py
```

**VERIFIED exact 21/22 owner localisation; its `b=24` successor is excluded
by the retained carrier-edge collision.**
