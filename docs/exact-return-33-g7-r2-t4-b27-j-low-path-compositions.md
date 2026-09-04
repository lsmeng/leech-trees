# FW319 `b=27`: J low-path composition catalogue

The remaining `b=27` Tail-5 branch has a single possible J-path shape for
the owner of `32`.  The same finite path audit also gives the complete
necessary shapes for the next four forced low values.

## Lemma

For a path lying wholly inside `J`, every interval distance must avoid the
fixed-L spectrum

```text
{1,2,3,6,7,8,9,10,11,12,13,14,15,17,22,23,
 27,28,29,30,31,33,39,40,41,42,50,55}
```

and the reserved value `4`; its interval distances must also be pairwise
distinct.  Under those necessary conditions, the complete ordered edge
sequences for the five target distances are

```text
32: (32)
34: (34), (16,18), (18,16)
35: (35), (16,19), (19,16)
36: (36), (16,20), (20,16)
37: (37), (5,32), (32,5), (16,21), (21,16), (18,19), (19,18).
```

## Consequences

The `32` owner is necessarily a single J edge of weight `32`; this conclusion
does not need the separate endpoint-floor argument.  If any of `34,35,36,37`
is multi-edge and J-internal, it must use one of the displayed two-edge
patterns.  In particular, no longer J path can hide a different low-owner
shape under the fixed-L spectrum.

## Exhaustiveness and replay

The verifier recursively enumerates every ordered composition of each target,
rejecting only a forbidden or repeated interval.  Thus it is exhaustive for
this finite path proposition:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_j_low_path_compositions.py
```

## Trust boundary

This is a necessary path catalogue, not a full-tree construction.  The four
values `34,35,36,37` may still be owned in `L`, and the listed J paths may
interact through shared vertices or cross distances.  The catalogue therefore
does not exclude `b=27`, the single-edge J branch, or global Leech trees.

**VERIFIED finite J-path shape catalogue; owner allocation and global closure
remain open.**
