# Universal literal low encoder (definition-level contract)

This note gives the non-enumerative encoder needed for the definition-level
`L-surj` statement.  It is not a search-reduction theorem.

## Domain

Fix the named packet `K`, root `d6`, and an anonymous slot set
`A_m={x_1,...,x_m}` for `0<=m<=10`.  A universal literal low state is the
threshold-37 projection of a member of `U^can_25`, retaining:

* every literal low edge and its positive weight;
* the full component partition;
* every named vertex and every anonymous identity;
* the rootward port and every outward boundary incidence of each component;
* owner/alias marks, including the actual pair/path data when present.

No owner shape, incidence mode, or weight value is excluded from this domain;
the exact-return predicates are filters applied after encoding.

## Encoder and decoder

For a state `L`, choose the lexicographically least serialization among all
permutations of its genuinely anonymous vertices, while keeping every name in
`K` fixed.  The serialization contains sorted literal edge triples, sorted
component records, all port/incidence records, and all owner/alias records.
Call this finite canonical word `E_L(L)`.  Let `K_L` be the set of all such
canonical words.  Define `D_L` by parsing the word and restoring exactly the
listed vertices, edges, weights, components, incidences, and marks.

Because `m<=10`, the minimization is over a finite permutation set.  Because
all records are literal and sorted only after the anonymous renaming, the
definition does not identify two named vertices or erase a shared anonymous
identity.

## Left-inverse proposition

For every universal literal low state `L`,

```text
E_L(L) belongs to K_L,
D_L(E_L(L)) = L
```

up to the permitted canonical renaming of anonymous slots.

**Proof.** The identity permutation supplies at least one serialization, so
the finite lexicographic minimum exists and is in `K_L`.  Decoding that word
recovers its complete literal edge list and all attached records.  Reapplying
the same finite minimization cannot change any named vertex or any shared
anonymous identity; it only chooses the same canonical representative.
Therefore the decoded state equals the input state modulo anonymous
renaming. `QED`.

## Consequence and boundary

If `L(T)` is the threshold-37 state of any genuine `T` in the admitted parent
space, then `E_L(L(T))` is a legal key in `K_L` and
`D_L(E_L(L(T)))=L(T)`.  This proves the definition-level implication

```text
forall T: exists k in K_L with D_L(k)=L(T).
```

It does **not** prove that the current pilot generator, or any finite search
subset `K_L_search`, contains every such key.  A separate finite-search
reduction lemma, sound pruning proof, and exact remote shard coverage remain
necessary before a zero-survivor computation can imply nonexistence.

