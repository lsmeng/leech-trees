# `b=27` branch-hypothesis discharge audit for low-owner saturation

This note audits the hypotheses of
`docs/pro-b27-h37-owner-saturation.md` against the current genuine
FW319/exact-return-33 residual branch.  It is a logical citation-chain audit;
it starts no computation and does not claim global nonexistence.

## Target

Let `B27^J32` be a genuine order-25 exact-return candidate in the residual
branch whose fixed core is the literal packet `K`, whose surviving `32`
residual is the J-single-edge branch, and whose already proved local reductions
include the forced L owners `5` and `21`.  The target is to discharge the five
hypotheses used by the conditional saturation lemma:

```text
H1  every d in [1,37] except 4 has exactly one global owner; 4 has none;
H2  unordered pair distances are globally injective;
H3  K owns the fixed S0 values by its literal pairs;
H4  32 is the fixed J single edge and 5/21 have the literal L shapes;
H5  every edge has positive integer weight, so a path of distance <=37
    cannot contain an edge of weight >=38.
```

## Discharge table

| hypothesis | source / derivation | status |
|---|---|---|
| H1 | Full exact-return `(R2,t=4)` means the pair-distance generating function is the punctured interval: all values in `[1,N]` occur once except the designated missing value `4`.  Restricting to `[1,37]` gives H1. | `BRANCH-DEFINITION` |
| H2 | The same exact-return definition requires distinct unordered pair distances; the fixed-core and residual documents use this as the global injectivity predicate. | `BRANCH-DEFINITION` |
| H3 | The fixed literal edges of `K` remain literal in the residual branch.  Distances between vertices of `K` are unchanged when the rest of the tree is attached.  By H2, no second pair can reuse any fixed distance, so the literal `S0` pairs are the unique global owners of `S0`. | `DERIVED-H2+FIXED-K` |
| H4 | `...b27-residual-two-branch-frontier.md` gives the complete local residual decomposition into L-direct-32 or J-single-edge-32.  `...j-forced-l-values.md` forces 5 and 21 into L, and `...l-forced-5-21-shapes.md` gives exactly `(5)` and `(21),(5,16),(16,5)`. | `VERIFIED-LOCAL-CHAIN` |
| H5 | Edge weights are positive integers by the weighted-tree definition.  Therefore any path of total at most 37 is contained in the subgraph of edges of weight at most 37.  This is elementary and does not require a catalogue. | `DEFINITION/ARITHMETIC` |

The `b=27` carrier-floor audit additionally gives `w>=38` for the carrier edge;
that stronger floor is needed by the separate L/J cross-cut arguments, but is
not needed for the elementary low-path implication in H5.

## Branch-local theorem

Under the branch definition above, H1--H5 are all discharged.  Consequently,
for every `T in B27^J32` and every edge `e` outside the fixed literal packet
`K`,

```text
w(e) <= 37  ==>  w(e) in H37
```

where

```text
H37 = {5,16,18,19,20,21,24,25,26,34,35,36,37}.
```

Proof: apply H5 to place the edge endpoints in one low component.  H1 gives
their unique owner value unless the value is `4`; `4` is absent.  H3 excludes
every value in `S0`, and H4 excludes the already occupied `32` owner and fixes
the `5/21` alternatives.  The only remaining values in `[1,37]` are exactly
`H37`.  H2 makes the owner unique and prevents two new low edges from sharing
one value.  This is precisely the proof in the saturation note, with its
hypotheses now attached to the branch definition.

## Boundary

This promotes **low-owner saturation** to a branch-local theorem, not the
entire finite search or the Leech-tree nonexistence claim.  It does not classify
the endpoint/LCA/attachment realizations of `34--37`; those must still be
represented literally and derived from the materialized pair table.  It also
does not prove high-completion surjectivity, least-remote preservation,
inherited descent, or the final contradiction.

The safe generator consequence is therefore only:

```text
new low edges use distinct labels from H37;
34--37 are stored as actual endpoint/path states or NOT_L;
no EDGE/FWD/REV endpoint shortcut is sound.
```

**Verdict: `VERIFIED_BRANCH_LOCAL_LOW_SATURATION`; global search remains open.**

## Strongest safe `34--37` refinement

The same branch hypotheses give one further theorem-level statement, without
classifying attachment cells.  Let `P_h` be the unique owner path for
`h in {34,35,36,37}`.  Since the carrier edge has weight at least `38`, a path
crossing the carrier cut has length at least `38`; hence

```text
P_h is wholly in L or wholly in J.
```

If `P_h` is in `J`, its edge word is restricted to

```text
34: (34), (16,18), (18,16)
35: (35), (16,19), (19,16)
36: (36), (16,20), (20,16)
37: (37), (5,32), (32,5), (16,21), (21,16), (18,19), (19,18).
```

The existing rooted-difference checks soundly remove all middle-entry words
except `35=(16,19)/(19,16)` and remove the `37` endpoint-entry words containing
`5,32,16,21`; the remaining endpoint-entry words
`(16,18),(16,19),(16,20),(18,19)` must stay in the literal generator.

If `P_h` is in `L`, every contiguous non-fixed subpath has distance neither
`4` nor a fixed `S0` value; otherwise it would create a second owner.  This is
safe materialized-path pruning, but it does not force a finite named endpoint
or LCA list.  The minimum remaining coverage obligation is therefore actual
endpoint/incidence realization for the residual L/J words, not low-edge
saturation itself.
