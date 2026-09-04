# FW319: J endpoint-entry translate lemma

This note records a theorem-level conditional lemma for the FW319 `b=27`,
`J32` branch.  It is deliberately scoped to the carrier-cut hypotheses below;
it is not a catalogue-completeness or global non-existence result.

## Hypotheses

Let the J-internal owner path be

```text
A --alpha-- M --beta-- C,       alpha,beta > 0.
```

Assume the geodesic from the J-root `u` first enters this path at the endpoint
`A`, with `d(u,A)=rho`.  Thus the rooted depths of `M` and `C` are
`rho+alpha` and `rho+alpha+beta`.  Assume the already established carrier-cut
formula for fixed-L vertices at carrier weight `w` and the fixed depth set

```text
B0 = {0,6,13,14,15,23,27,28}.
```

The endpoint-first-entry-at-`C` case is symmetric.

## Lemma

Let

```text
Delta(B0) = {1,2,4,5,6,7,8,9,10,12,13,14,15,17,21,22,23,27,28}.
```

If either `alpha` or `beta` belongs to `Delta(B0)`, the endpoint-entry
realization contradicts global unordered-pair distance injectivity.

For example, if `alpha` is in `Delta(B0)`, choose fixed-L vertices `X,Y` with
`d(d6,Y)-d(d6,X)=alpha`.  The carrier-cut equations give

```text
d(X,M) = d(d6,X) + w + rho + alpha
d(Y,A) = d(d6,Y) + w + rho,
```

so the two distinct unordered pairs `{X,M}` and `{Y,A}` have equal distance.
The `beta` case compares `{X,C}` with `{Y,M}`.  The same argument with the
path reversed handles first entry at `C`.

## Immediate word-level consequences

Under the hypotheses above, endpoint entry is excluded for all orientations
of

```text
37 = (5,32), (32,5), (16,21), (21,16).
```

The words `(16,18)`, `(16,19)`, `(16,20)`, and `(18,19)` remain open under
this lemma because `16,18,19,20` are not in `Delta(B0)`.  A named packet can
remove one of these only if the relevant actual unordered pair and distance
are already fixed by a theorem applying to every candidate tree; a finite
reservation or a pair seen in one control run is insufficient.

## Scope boundary

This note does not address middle entry (handled separately), an edge-interior
subdivision, one-sided owners, L-side geometry, arbitrary high incidence, or
Label-State Completeness.  It therefore only removes the stated endpoint-entry
subcases and cannot be promoted to the global `b=27` non-existence theorem.

