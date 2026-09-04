# Two-stage projection surjectivity contract

This note records the current proof obligation for the fixed-`K` `b=27`
catalogue.  It is a contract and gap statement, not a certified theorem.

Let `U` be the set of genuine FW319 candidates that lie in the complete
weighted state space `U^can_25` and satisfy the already stated exact-return
predicates.  Threshold every state at weight `37` and write its deterministic
projection as

```text
P(T) = (L(T), H(T)).
```

Here `L(T)` contains the complete literal low forest, its edge weights,
component partition, owner/alias marks, rootward ports, and every
rootward/outward boundary incidence.  `H(T)` contains the rooted high
quotient, both endpoint incidences of each high edge, every retained
high-only subdivision, and the ordered original high-edge weights.

## Exact two-stage obligation

If `G_L` is the practical low generator and `G_H(l)` is the high generator
conditional on a low state `l`, the required coverage is the conjunction

```text
(L-surj)  forall T in U, exists l in G_L: l = L(T),

(H-surj)  forall T in U, forall l in G_L with l = L(T),
          exists h in G_H(l): h = H(T).
```

Together with the lossless materialization interface, these imply

```text
forall T in U, exists (l,h) generated:
    Materialize(l,h) is named-vertex-preserving and edge-for-edge isomorphic to T.
```

No uniqueness of a generated state is required.

## What is already supported

`docs/pro-b27-universal-catalogue-surjectivity.md` supplies the definition-level
map from a genuine realization to `U^can_25`.  The deterministic projection note
proves that retaining literal low components, all boundary endpoint
incidences, the high quotient, ordered high subdivisions, and ordered edge
weights is sufficient for edge-for-edge reconstruction.  The finite port and
ordered-arc round trips validate this reconstruction interface on their stated
bounded families.

These facts do not prove either practical-generator surjectivity statement.

## First unresolved quantifier

The first missing implication is `(L-surj)`: for every genuine state, every
low topology, literal endpoint, low weight, outward-incidence subset, shared
named identity, and owner state must map to an admitted raw low key.  In
particular, bounded `m/e` pilots, assumed `EDGE/FWD/REV` cases, or a preset
`34--37` geometry cannot stand in for this universal decoder.

The next acceptance test is therefore a read-only, field-by-field audit of
the map `T -> raw_key(L(T))`.  If any field has only pilot evidence and no
all-state definition, the status remains `GAP_L_SURJECTIVITY`; no larger
enumeration and no `m=4` extension should be treated as closing it.  Only
after `(L-surj)` is established should the conditional `(H-surj)` audit be
promoted to a coverage claim.

