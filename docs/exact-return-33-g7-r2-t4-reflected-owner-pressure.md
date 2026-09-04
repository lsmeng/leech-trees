# FW315: reflected low-owner pressure layer

FW314 leaves every complementary owner mode alive.  In an X-containing mode,
however, the endpoint-relative holes themselves lie below the final bridge
and hence must have actual owners in a Leech tree.  This gives the first
finite ownership layer beyond the original X-owner.

It is a strict pressure refinement, not an exclusion.

## 1. Exact reflected values

Let a complementary value have a cross owner

```text
c = w+b+r = s-delta,
eta = s-w,
```

with `b in B`, `r in R`, `w>=1`, and `delta>0`.  Define

```text
q_B = b+delta = eta-r,
q_R = r+delta = eta-b.
```

Both values are positive.  Since `b,r>=0` and `w>=1`,

```text
1 <= q_B,q_R <= eta <= s-1.
```

Thus complete Leech coverage gives each value a unique actual pair owner.
If the two values coincide, this is one value and one owner, not two owners.

FW314 simultaneously gives the rooted-depth exclusions

```text
q_B not in B,       q_R not in R.
```

When `q_B+4<s` or `q_R+4<s`, complete coverage also gives the shifted value
an actual owner, while FW314 excludes it from the corresponding rooted
factor.

## 2. Why this does not close

An owner pair of distance `q_B` does not produce a vertex at `g`-rooted depth
`q_B`; similarly an owner of `q_R` need not produce a vertex at `u`-rooted
depth `q_R`.  Its LCA may be elsewhere in either cut factor, or the pair may
cross the cut.  Therefore iterating global ownership does not yet contradict
the endpoint-relative holes.

The tempting extra identification `delta =` a rooted arm from `u` is also
invalid in general.  FW311 constructs `alpha,beta` as lengths of two actual
ancestor--descendant subpaths of the least remote path.  They lie in
`(R-R)_+`, but need not be depths from `u`.  The FW314 controls happen to put
their split at `u`; that is pressure-model geometry, not an inherited
theorem.

The exact successor obligation is therefore:

> **Reflected-Owner Reception.**  Under the complete punctured low spectrum
> and no-outlier cap, show that one reflected owner forces a forbidden rooted
> depth, a repeated owner of `s` or `s+4`, or a strictly smaller inherited
> carrier state.

This is narrower than asking only for the color of the original
complementary owner, but it remains open.

## 3. Replayed pressure controls

The verifier reconstructs every FW314 control containing an X-owner.  In all
six ordinary X rows and the exceptional `4X` row:

- the two reflected values satisfy the exact identities and lie below `s`;
- `q_B,q_B+4` are absent from `B` and `q_R,q_R+4` are absent from `R`;
- `q_R` already has one actual J-internal owner in the sparse control;
- `q_B`, `q_B+4`, and `q_R+4` are missing globally.

The existing controls first miss five and violate their own order caps, so
these missing reflected values are consistent with their role as non-Leech
pressure controls.  They do not refute the full-spectrum obligation.

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_reflected_owner_pressure.py
```

The certificate is
`theory-lab/topwindow/results/exact_return_33_g7_r2_t4_reflected_owner_pressure_certificate.json`.

## 4. Verdict

**VERIFIED pressure refinement; no X-containing signature excluded.**

The earliest gap remains root provenance, now attached to the two named
reflected low values rather than to an arbitrary owner-color iteration.
