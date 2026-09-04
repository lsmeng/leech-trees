# FW319 `b=27`: J cannot own 5 or 21

The fixed L factor gives one small but genuine reception constraint on the
remaining b=27 frontier.  It uses both the rooted carrier directness and the
fact that every interval of a J path is an actual J-internal pair distance.

## Lemma

In the audited FW319 b=27 cell, the complete-spectrum owners of distances

```text
5 and 21
```

are both L-internal.

## Proof

The fixed L rooted depths at `d6` are

```text
B0={0,6,13,14,15,23,27,28}.
```

Their positive difference set is

```text
Delta_B={1,2,4,5,6,7,8,9,10,12,13,14,15,17,21,22,23,27,28}.
```

For an edge in J, the two endpoint depths from the J root `u` differ by the
edge weight.  Carrier directness therefore forbids every J edge weight in
`Delta_B`.

Every interval sum along a J path is an actual J-internal distance.  It must
avoid the complete fixed-L spectrum

```text
S0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
    27,28,29,30,31,33,39,40,41,42,50,55}
```

and the punctured value `4`.  Exhaustive ordered positive compositions under
these two necessary conditions gives

```text
target 5:  no composition;
target 21: no composition.
```

Thus no J-internal pair can have distance 5 or 21.  The verified carrier
floor is `w>=38`, so neither value can be cross-cut.  In a complete Leech
spectrum both values must therefore be owned inside L.

## Replay

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_j_forced_l_values.py
```

The recursion is finite and prunes only repeated interval sums, fixed-L
distances, the punctured value, and forbidden J edge weights.  Its output is
`status: VERIFIED`.

## Trust boundary

This does not identify the L owner pairs of 5 and 21, and it does not exclude
the L single-edge-32 or J single-edge-32 residual.  The next structural task
is to combine these two forced L owners with the low-edge placement and the
complete-spectrum cap without replacing arbitrary owner pairs by rooted
depths.
