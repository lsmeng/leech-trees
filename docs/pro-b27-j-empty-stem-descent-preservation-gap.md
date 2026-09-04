# FW319: empty-stem descent preservation gap

The endpoint-entry audit leaves a free stem length `rho=d(u,A)`.  Existing
translate and injectivity arguments impose only finitely many forbidden values
of `rho`; they do not force `rho` into a finite set.

## Conditional descent lemma

Suppose an endpoint-entry owner path has an open stem `[u,A]` whose interior
contains no named vertex, fixed incidence, or other required owner endpoint.
If deleting the outer stem component (or rerooting at `A`) preserves the full
exact-return branch hypotheses, then a least-remote/minimal counterexample cannot
have such a stem.  The stem must meet a named incidence, so `rho` is a named
rooted depth or a finite path-determined difference of named depths.

This is a minimality argument only; it becomes useful only after the stated
preservation premise is proved.

## Exact missing premise

No current theorem proves that stem trimming preserves all of:

- complete punctured spectrum;
- the J32 single-edge owner;
- the 34--37 owner identities;
- the carrier-cut parameters;
- least-remote minimality; and
- the no-outlier cap.

Consequently the descent statement is **CONDITIONAL**, not a valid forcing
lemma yet.  A small abstract local tree can keep all currently listed local
hypotheses while choosing `rho` arbitrarily large and avoiding the finite
collision set; it is not a complete Leech-tree counterexample, but it shows why
the present assumptions alone are insufficient.

## Smallest next obligation

Prove the exact-return preservation lemma for deleting an empty endpoint stem,
or identify the first listed invariant that fails and replace it with a weaker
descent invariant that is still sufficient to bound `rho`.  Until then the four
remaining endpoint-entry words remain open and no global non-existence claim is
licensed.

## Advisor refinement (2026-08-29; not proved)

The persistent GPT audit sharpens the first missing invariant.  Exact-return,
least-remote, and the no-outlier cap do not imply that owners are separated by
the stem cut: a required surviving value may have its unique owner using a
rootward stem vertex.  Thus the useful minimal target is a **Low-owner
retention lemma**: for every permitted endpoint-stem cut, every value required
by the smaller exact-return instance has both owner endpoints in the retained
side.  Together with the corresponding removable-owner block, this would
imply inherited descent.  The statement is currently `GAP`; the one-edge stem
pattern in the preceding audit shows why local incidence emptiness alone does
not establish it.

## Exact cut-owner formulation (GPT audit, 2026-08-29)

Let `T=R union_A T'` be an endpoint-stem cut, with `R-{A}` the part to be
removed, and let `Sigma'` be the spectrum required by the proposed smaller
instance.  The missing retention statement is the quantified implication

```text
for every genuine T and every permitted cut,
for every s in Sigma', the unique owner of s in T lies wholly in T'.
```

Inherited descent also needs the matching separation statement: the values
owned by pairs meeting `R-{A}` are exactly `Sigma(T) minus Sigma'` (or the
specified removable block).  Exact-return supplies uniqueness globally, but
not either cut-local assertion; least-remote and a cap likewise do not impose
an order on owner locations.

The smallest abstract owner-interleaving pattern is the weighted path

```text
r -[2]- A -[5]- B -[9]- C.
```

Its pair distances are `2,5,9,7,14,16`, all distinct.  Cutting off `r`
removes owner values `{2,7,16}` while retaining `{5,9,14}`.  The removed set
is neither a terminal interval nor separated by magnitude.  This is not a
full FW319 candidate, so it does not refute the target lemma for genuine
Leech trees; it does prove that the currently listed abstract hypotheses do
not logically entail it.  A new cut-monotonicity/owner-rank theorem is needed
before empty-stem descent can be promoted.
