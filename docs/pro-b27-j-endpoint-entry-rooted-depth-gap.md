# FW319: endpoint-entry rooted-depth gap

This note audits the remaining J-internal endpoint-entry words after the
`Delta(B0)` translate lemma.  It records a negative theorem-level result:
the current hypotheses do not exclude any of these words unconditionally.

## Current named data

The named J packet supplies only

```text
d(u,y0) = r,  d(u,y3) = r+3,  r >= 16,
d(d6,u) = w,  w >= 38.
```

Thus the named rooted-depth differences are `3`, `r`, and `r+3`; finite
offsets such as `(38,54,57)` cannot be promoted to branch-wide assumptions.

For an endpoint-first-entry path

```text
A --alpha-- M --beta-- C,  d(u,A)=rho,
```

the three relevant rooted depths are `rho`, `rho+alpha`, and
`rho+alpha+beta`.  Global depth injectivity only forbids their coinciding
with `r` or `r+3`, unless the corresponding vertices literally coincide with
the named endpoints.  It does not force `rho` to any particular value.

## What remains open

The words

```text
(16,18), (16,19), (16,20), (18,19)
```

therefore retain endpoint-entry gaps in both orientations.  For example,
`rho=1, r=40` gives distinct local depths `1,17,35,40,43` for the `(16,18)`
pattern, and neither 16 nor 18 lies in the fixed `Delta(B0)` difference set.
This is only an abstract local obstruction pattern, not a complete Leech-tree
counterexample; it shows that the present local hypotheses do not logically
imply impossibility.

Likewise, exact-spectrum uniqueness by itself says only that each distance has
one owner pair.  It does not identify that owner with a named pair unless a
separate theorem fixes the actual vertices in every candidate tree.  A finite
reservation or one control realization is insufficient.

## Smallest next obligation

Prove a **rooted-depth forcing lemma**: every J-internal 34--37 owner in the
endpoint-entry case has `rho` in a finite set forced by the named packet (ideally
`{0,r,r+3}` or a proved fixed translate).  Only after that reduction can the
existing rooted-depth injectivity, fixed-L translate differences, and literal
owner-reuse arguments be applied case by case.

Until such a lemma is proved, no one of the four words above should be marked
`VERIFIED`-excluded, and this gap remains separate from L-side geometry,
edge-interior subdivision, catalogue completeness, and the global theorem.

