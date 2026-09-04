# Referee prompt: "There is no Leech tree on 18 vertices..."

You are refereeing a submitted mathematics paper. Read the attached PDF in full
before writing anything. Apply the standard of a combinatorics journal: a claim
is either proved, or supported by a computation whose scope is stated exactly,
or it does not belong in the paper.

Two things you should know before you start, because they change where to look.

**The paper was written with AI assistance, and some of its theorems were first
drafted by an AI and then checked by the author.** Treat every argument as
unverified. Machine-drafted mathematics fails in a particular way: the prose is
fluent and the structure is conventional, but a quantifier is wrong, a lemma is
applied outside its hypotheses, or a step that "clearly follows" does not. Do
not be reassured by confident phrasing or by the presence of a proof
environment. Read each proof line by line and ask what would have to be true for
the step to hold.

**Most of the paper's results rest on exhaustive computer search, and you cannot
re-run those computations.** Do not try. Judge instead whether the computation
*as described* would establish the claim if it ran correctly, whether its scope
matches the scope of the theorem it supports, and whether the acceptance
criterion is strong enough. A search that is exhaustive over the wrong set
proves nothing, and that is the failure mode to hunt for.

## What to check, in order of how much it matters

1. **Quantifier discipline in every numbered statement.** For each theorem,
   lemma, proposition and corollary: are the hypotheses actually used? Is the
   conclusion the one the argument gives, or a stronger one? Where a statement
   depends on an earlier result, is that dependence stated? Flag any place where
   a finite computation is presented as, or slides into, a general theorem.

2. **The distinction between "no such object exists in this finite range" and
   "the conjecture is proved."** The paper's order-25 material is deliberately
   partial. Check that it never claims more than a fixed finite range, that the
   open range is stated correctly and consistently everywhere it appears, and
   that no sentence in the abstract, introduction or discussion overstates it.

3. **The load-bearing new results.** In the order-25 section: the top-block
   crowding inequality, the diametral-endpoint reduction, and the corollary that
   reduces order 25 to a finite list. These are the newest and least reviewed.
   Re-derive the crowding inequality's algebra yourself, including the quadratic
   and its roots, and recompute every entry of the table that applies it. Check
   the case analysis in the endpoint reduction for a missing configuration.

4. **Whether the computations support what they are cited for.** For each
   certificate: what set was searched, what was the acceptance token, what
   happens to a task that does not finish, and is a partial result anywhere
   being used as if it were complete? The paper reports one computation that was
   stopped before finishing; check that nothing depends on it.

5. **Arithmetic and internal consistency.** Recompute the table entries. Check
   that a quantity quoted in two places agrees. Check that cross-references
   point at statements that say what the citing sentence needs.

6. **Literature.** Are prior results attributed correctly and are the
   comparisons to them accurate? The paper claims to strengthen or correct
   several published statements; check each claim of novelty and each claim of
   improvement. Flag any place where priority is asserted without justification.

7. **Correctness of the elementary lemmas.** They look routine and that is
   exactly why they are worth reading: an error there propagates everywhere.
   Pay attention to conventions that decide an off-by-one, such as whether a
   counted set includes its own endpoint.

## What to produce

A numbered list of findings, most serious first. For each: the location, what
is wrong or unsupported, why it matters, and what would fix it. Mark each as
**blocking** (the paper cannot be published as stated), **major** (must be
addressed but the result survives), or **minor**.

Then, separately and briefly: is the main theorem established? Is the order-25
material honest about its own limits? Would you accept, accept with revisions,
or reject?

Do not summarise the paper back to me and do not praise it. If you find nothing
wrong in a section, say so in one line and move on. If you are unsure whether
something is an error, say that you are unsure and say precisely what would
settle it. A confident wrong finding costs more than an honest "I could not
check this."
