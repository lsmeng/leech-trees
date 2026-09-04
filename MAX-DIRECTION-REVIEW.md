# Independent direction review — the all-order Leech-tree programme

**Mathematical review snapshot:** commit
`83e8ae48c631284b56498e70191f975efd6196bd` (`Route monochromatic terminal
lattices by parity`, 2026-08-24).  The comparison baseline is
`b5064a746c09765b4ace80617da162885670a26a` (`Localize sharpened residual in
the lower core`).  This guide itself is stored in the immediately following
documentation-only commit; that child commit changes no mathematical source,
verifier, certificate, or status ledger.

**Purpose:** this is a prompt and evidence guide for two blind, independent
AI reviews of the current research direction.  It is not a proof and it does
not promote any `UNVERIFIED` claim.  One review may be performed by Codex
GPT-5.6 Sol at `max` reasoning effort and the other by an unrelated model.
The reviewers should not see each other's reports before both reports are
frozen.

---

## 1. Role and requested decision

Act as a sceptical research mathematician reviewing a long computer-assisted
programme in additive/tree metric combinatorics.  The project has accumulated
many correct local reductions.  The question is no longer whether those
reductions are interesting.  The question is whether the current chain is a
credible route to the global theorem, or whether it is repeatedly replacing
one unconstrained terminal by another.

The primary target is:

> **UNVERIFIED target G18.** No Leech tree exists at any order `n>=18`.

The order-18 case itself is already excluded by a separate, replicated
finite computation.  Taylor's necessary condition leaves the future orders

```text
25, 27, 36, 38, 49, 51, 64, 66, ...,
```

so G18 is an all-order structural problem, not an invitation to run the
order-18 search again.  The stronger historical formulation “the five known
trees are the only Leech trees”, equivalently no examples for `n>=7`, is not
needed for this direction review.

Your main output must answer five questions.

1. Is the chain from the global diameter reduction through `FW203--FW217`
   mathematically sound under its stated hypotheses?
2. Is that chain globally exhaustive, or do earlier thick-core, lower-core,
   contextual-cap, or reversal branches remain outside it?
3. Does at least one of the proposed next routes have a plausible, precisely
   stated bridge lemma that would materially move toward G18?
4. What is the smallest abstract countermodel or obstruction showing why
   each unsuccessful route cannot work from the present hypotheses alone?
5. Should the project invest another substantial proof budget in this route?
   Give `CONTINUE`, `CONTINUE WITH PIVOT`, or `STOP THIS ROUTE`, with explicit
   milestones and a stop condition.

Do not give a motivational review.  Try to falsify the programme.  A useful
negative result is better than an unsupported endorsement.

---

## 2. Mathematical object and conventions

A **Leech tree** of order `n` is a tree on `n` vertices with positive integer
edge weights for which the `N=binom(n,2)` unordered vertex-pair distances are
exactly

```text
{1,2,...,N}.
```

Thus every pair distance is distinct, every distance is at most `N`, and the
weighted diameter is exactly `N`.  There are five known examples: orders
`2`, `3`, two at order `4`, and one at order `6`.

The repository uses these status labels.

- **OBSERVED:** proved or exhaustively verified inside the project, with the
  stated trust boundary.  This is not the same as peer-reviewed literature.
- **LITERATURE:** taken from a cited source; the source-verification level is
  recorded separately.
- **UNVERIFIED:** conjectural, conditional beyond an unclosed hypothesis, or
  a proposed transition.

Preserve those distinctions.  In particular:

- a finite search at one order is not an all-order theorem;
- a lower bound is not a contradiction unless a genuinely incompatible
  upper bound is proved;
- a proper subtree is not automatically a smaller Leech tree;
- a finite cap obtained inside a larger tree retains its contextual wrapper;
- “all-order” means that the displayed implication holds for all orders in
  its stated subcase, not that the subcase is excluded;
- an exact replay verifies the encoded statement, not necessarily that the
  encoded statement is the right global statement.

Every hypothetical witness introduced during the review must be checked by
both `src/checker_a.py` and `src/checker_b.py`.  An abstract countermodel to a
lemma may violate the full Leech conditions, but then it must be labelled
clearly as an abstract countermodel showing insufficiency of the listed
hypotheses, not as a Leech witness.

---

## 3. Repository and audit boundary

Audit the mathematics tracked at the exact snapshot above.  It is acceptable
for repository `HEAD` to be the immediately following guide-only commit, but
verify that its only tracked difference from the mathematical snapshot is
this file.  At the time this guide was written the working directory also
contained seven untracked exploratory
scripts under `theory-lab/topwindow/`.  They are outside this audit snapshot,
have no promoted conclusions, and must not be used as evidence.

Begin by recording:

```bash
cd ~/Documents/claude/projects/leech-trees
git rev-parse HEAD
git status --short
git diff --stat 83e8ae4..HEAD
git log --oneline b5064a7..83e8ae4
```

If `HEAD` is neither the pinned mathematical hash nor its guide-only child,
state the actual hash and do not silently mix versions.  Prefer a clean clone
or read-only worktree.  Do not edit the project during the review.

### Read in this order

1. `README.md`, especially the initial problem/status ledger and the current
   summary beginning with the diameter-edge and terminal-cap reductions.
2. `docs/nonexistence-roadmap.md`, Sections 1--3 and 6--9.  Treat its roadmap
   arrows as claims to audit, not as established implications.
3. `docs/edge-handoff-orientation.md`, first the sections containing
   `FW193--FW202`, then the complete block from the heading
   “A diameter edge either extends a reflected prefix or exposes a
   double-deep fork” through `FW217`.
4. The verifier scripts and frozen JSON certificates named immediately after
   each of `FW203--FW217`.
5. Only as needed for dependencies, return to the original statements and
   proofs of `FW34`, `FW76`, `FW89`, `FW92`, `FW93`, `FW105`, and `FW148` in
   `docs/edge-handoff-orientation.md`.
6. For a proposed waste or small-weight synthesis, read
   `docs/kruskal-covering-waste.md`.  For a proposed endpoint/cap argument,
   read the specific earlier lemma rather than relying on its one-line
   summary in `README.md`.

Do not use `AUDIT-PROMPT.md` as the main guide.  That file audits the separate
finite order-18 theorem and manuscript; the present task audits the global
research direction.

### Evidence rule

Every pass, failure, and strategic judgement must cite at least one concrete
anchor: a file and line, an equation number, a code identifier, an exact
counterexample, or a reproduction command and result.  “The algebra looks
fine” and “this seems promising” are not findings.

Separate three levels of evidence:

1. **re-derived:** you independently proved or recomputed it;
2. **replayed:** you ran the repository verifier and obtained its result;
3. **inspected only:** you read an existing proof/certificate without an
   independent derivation.

---

## 4. What was accomplished before the current terminal

The following facts explain why the global route is being attempted.  They
are context, not substitutes for auditing their use.

- The finite order-18 nonexistence result is replicated by two independent
  forest implementations and multiple runs.
- No spider Leech tree exists for any `n>=5`.
- No bi-spider Leech tree exists for any `n>=18`.
- Exactly-three-branch trees are excluded at orders `25` and `27` by finite
  searches, but there is no uniform three-branch theorem.
- Hop-diameter at most four is excluded at order `25`, but there is no
  all-order short-diameter theorem.
- The earlier endpoint analysis reached a fixed affine terminal.  `FW193` and
  `FW194` forced a quartic residual and many high-slack pairs in an
  order-`n-O(1)` lower core.  `FW195--FW202` then excluded the finite `K=2`
  and `K=3` affine rows that arose in that terminal.

The last bullet is easy to overread.  Closing those affine rows did not by
itself prove G18.  The subsequent `FW203--FW217` programme attempts to replace
the special endpoint setup with a global diameter/cap descent and then to
classify the resulting periodic complement.  A central purpose of this
review is to decide whether that replacement is genuinely global.

---

## 5. Intended current dependency chain

The intended chain, with the final arrows still under review, is:

```text
hypothetical large Leech tree
        |
choose a diameter edge / the central diameter edge
        |
FW203--FW204: prefix, proper-side gap, deep offshoot, or balanced cut
        |
FW205--FW208: strict deficit descent to a contextual cap of order <=4
        |
FW209: one of four complete mixed-radix digit factors
        |
FW210 + FW212: a disjoint opposite cap; reversal absorbed
        |
eleven fixed oriented rectangles with q in {1,2,3,4,6,8}
        |
FW211: exact visible periodic lattice P+q Z_>=0 below first hole Q
        |
FW213--FW214: branch-rich / unseen-vertex resource inequalities
        |
FW215: half-order unseen part or a long bounded-shedding heavy spine
        |
FW216: quadratic reflected-coordinate span on the heavy spine
FW217: four monochromatic rows route to an asymptotically half-order unseen part
        |
OPEN: collision, strict proper-core descent, or incompatible span upper bound
```

The phrase “contextual cap” matters.  The small cap is embedded in the
original tree and carries inherited diameter/pivot history.  Neither cutting
it off nor finding a smaller first-hole deficit makes the remaining component
a Leech tree.  Every purported induction must specify exactly what structure
is inherited and what well-founded quantity decreases.

---

## 6. Local audit checklist for `FW203--FW217`

For every item below return one of:

```text
CORRECT AS STATED
CORRECT AFTER SPECIFIED FIX
INSUFFICIENTLY JUSTIFIED
FALSE (give counterexample)
NOT CHECKED
```

### `FW203`: diameter-edge prefix/fork interface

Re-derive the reflected-prefix factorisation above an internal side diameter
`D`.  Check the equality case `D=q+lambda`, the use of the complete
mixed-radix conclusion from `FW34` rather than mere set symmetry, and the
claim that a gap-crossing edge lies wholly in the proper side.  Verify that
the double-deep fork really produces a global branch vertex and that no
degree-two or root boundary case is mislabeled.

### `FW204`: two-sided central-edge specialization

Audit all four-point orientations, the gate coordinate inequalities, and the
strict inequalities at `h=q` and `C=N-D`.  Check that the cases are exhaustive
when one or both reflected remainders are nonpositive.  Recompute the exact
quarter threshold and the component-order lower bound.  Decide whether the
deep-offshoot/balanced alternatives retain every hypothesis needed later.

### `FW205--FW208`: cap and deficit descent

This is the most important well-foundedness audit.  Draw the fixed global
diameter and follow every reorientation.  Check:

- the gap/bidirectional-component boundary edge exists in the required open
  metric half;
- the centre-side support pair is distinct from the edge pair;
- the new first-hole deficit is a positive integer strictly smaller than the
  previous one in every recursive branch;
- termination in an `FW76` cap does not discard the outer tree or pivot
  history;
- the balanced `FW206` shell branches are actually absorbed by `FW207`, not
  merely analogous to the proper-gap branch;
- the recurrence cannot alternate orientations while decreasing different,
  incomparable quantities.

State a single explicit well-founded measure, including any contextual data,
or report that the documents prove only local decrease.

### `FW209`: terminal-cap digit/pivot normal form

Verify the exact hypotheses inherited at the end of `FW208`.  Re-derive the
four factor shapes, the parity restriction, `chi_P(q_0)=1`, the bound on
`q_0`, and the pivot identity `N=2k+r_0+q_0` with `r_0!=q_0`.  Check whether
the factor classification applies to every terminal cap produced above or
only to a narrower “complete exact-prefix” cap.

### `FW210` and `FW212`: opposite cap and reversal absorption

Audit the open-half versus central-edge split used to obtain the second cap.
Verify disjointness of the two cap cuts, the bound `min(q_0,Q)<=ab<=16`, and
the removal of the eight internally colliding factor rectangles.  In the
reversal argument, track actual vertices through each endpoint peel.  The
outer wrapper is explicitly retained; decide whether applying `FW211` to the
nested nonreversal pair remains valid in its presence.

### `FW211`: periodic-lattice stability

Distinguish carefully between:

1. the infinite algebraic indicator identity for a mixed-radix factor;
2. the finite set of actual complement vertices visible below its first hole
   `Q`;
3. the `u` complement vertices above that hole.

Recompute the phase error `delta`, the two capacity identities, the formula
for the sum of absolute coordinate differences, and the rooted-detour lower
bound.  Check all ceiling and ordered/unordered-pair factors.  Confirm exactly
which induced or rooted component contains the periodic vertices.  Do not
accept quartic scale alone as progress toward a contradiction.

### `FW213--FW214`: LCA resource bounds

For `Lambda_t`, verify that every relevant LCA is counted in the claimed
visible/unseen class, including the root and the cap attachment.  Check the
per-LCA limit `2D-1`, ancestor cases, and the branch-vertex correction when
`b>=3`.  Independently derive the uniform constants in

```text
B > at/(4b)-1,
at <= 4b(u+3),
u >= ceil((n-56)/17),
16B+u > n-24.
```

The conditional `B<=3` table must remain explicitly conditional.  Determine
whether branch-richness is useful structural information or just another
resource lower bound compatible with arbitrary trees.

### `FW215--FW216`: heavy spine and quadratic span

Audit the marked-subtree construction and prove that the heavy-child steps
form one actual rooted path.  Check the bounded-shedding inequality, the
threshold for entering the visible band, all off-by-one constants, and the
telescoping count of disjoint shed--retained pairs.  Verify that their
distances really lie in one common interval and that global uniqueness gives
the stated span lower bound.

Then state plainly what is missing: `beta-Q=Omega(s^2)` is compatible with a
global diameter of order `n^2`.  Identify any additional information already
proved elsewhere that gives a nontrivial upper bound on the same quantity;
do not substitute an upper bound on a different span or a different core.

### `FW217`: Taylor-parity routing

Check all four listed oriented rows, the parity of the complete visible
lattice, Taylor's two possible orders, and which bipartition class is larger.
Re-derive the lower bound for `u`.  Confirm that this routes only four of the
eleven rows and supplies no connectivity or inherited-prefix theorem for the
unseen vertices.

---

## 7. Global scope audit

Even if every displayed equation is correct, the programme can fail through
a missing arrow.  Build a scope ledger with one row for every terminal named
in `README.md` and `docs/nonexistence-roadmap.md` from `FW193` onward.  At a
minimum include:

- the defect-21 near-full lower core;
- the `K=2` and `K=3` affine rows;
- proper-side gap edges;
- deep thin/thick offshoots;
- the fully blocked balanced central cut;
- contextual order-at-most-four caps;
- opposite-deficit reversals;
- the eleven periodic rows;
- the high-coordinate unseen remainder;
- the branch-rich remainder;
- the bounded-shedding heavy spine;
- any non-singleton bidirectional thick core or lower-core output still named
  `UNVERIFIED` in the status ledger.

For each terminal record:

```text
originating hypotheses
claimed successor
equation/theorem proving the handoff
decreasing measure, if any
context that must be retained
status: CLOSED / ABSORBED / STILL OPEN / SCOPE GAP
```

Specifically answer:

1. Does every hypothetical Leech tree of sufficiently large admissible order
   reach an `FW209` terminal cap?
2. Does every `FW209` cap reach one of the eleven `FW210e` rows after `FW212`,
   without losing a hypothesis or a vertex?
3. Are `FW213--FW217` consequences of all eleven rows, or are some estimates
   conditional on a near-saturated/bounded-defect regime no longer available
   after `FW214`?
4. Is the current route an exhaustive descent, or merely an implication from
   one selected terminal subcase?
5. If it is not exhaustive, which missing terminal should be attacked before
   spending more effort on the heavy spine?

This scope ledger is more important than rerunning millions of arithmetic
rows.

---

## 8. Evaluate the proposed next routes

The review should not merely rank labels.  For each route, formulate the
strongest lemma that appears derivable from the *current* hypotheses, attempt
to prove it, and attempt to refute it with an abstract tree/coordinate model.

### Route A — translate-overlap collision along the heavy spine

At a high LCA of reflected coordinate `gamma`, pair distances from two marked
child groups have the form

```text
2 gamma - y - z,
```

where `y,z` lie in pieces of the fixed periodic coordinate set.  Successive
heavy-spine LCAs give translated sumsets.  `FW216` only packs their total
number into a common interval; it does not force two translated families to
overlap.

Audit questions:

- Does bounded shedding make the consecutive sumsets sufficiently dense or
  nested to force an overlap?
- Do the moduli `q in {1,2,3,4,6,8}` and the eleven exact digit sets leave a
  residue-class obstruction or instead make collision easier?
- Can a Golomb-like placement of the LCA coordinates keep every translate
  disjoint throughout the allowed quadratic span?
- Can cross-level pairs, not only pairs within one shed--retained family,
  provide the missing collision?
- Is there a usable additive-energy or interval-cover inequality stronger
  than cardinality packing and valid for these structured, changing subsets?

A successful milestone is an exact lemma, with the hypotheses of
`FW211--FW215`, that forces a repeated distance, or else forces a new cap/core
with a strictly smaller explicit parameter.  “Random translates should
overlap” is not a milestone.

### Route B — turn the unseen vertices into a smaller inherited core

`FW214` gives a linear unseen set in every row, and `FW217` makes it
asymptotically half the tree in four rows.  But the unseen vertices are
defined by lying above a coordinate threshold; they are not automatically a
connected induced subtree and do not automatically inherit an interval of
unique distances.

Audit questions:

- What can be proved about the number and arrangement of unseen components?
- Does one unseen component have linear order, or can the unseen mass be
  fragmented into many small pendant bundles?
- Is there a canonical connecting skeleton whose inclusion preserves a
  useful first-hole or reflected-prefix condition?
- What exact data would a recursive state need: order, boundary radius,
  first-hole deficit, pivot parity, contextual caps, and/or branch count?
- Which measure decreases under the proposed recursion?  Order alone is not
  enough if adding the connecting skeleton restores the deleted mass.
- Can the no-spider/no-bi-spider theorems close a genuinely low-branch unseen
  component, or are they irrelevant because the ambient connections create
  more branch vertices?

A successful milestone is a theorem extracting either a connected proper
core of order at least `c u-O(1)` with an inherited exact spectral interface,
or a bounded catalogue of fragmented alternatives.  Merely observing that
`u=Omega(n)` does not qualify.

### Route C — contradict the quadratic spine span with a global upper bound

`FW216` forces

```text
beta-Q >= 3s^2/16-O(bs).
```

The trivial diameter scale permits `Theta(n^2)`, so the constants and the
relation between `s`, `u`, and `n` matter.

Audit questions:

- What is the strongest existing upper bound on this exact `beta-Q`, not on
  a neighbouring edge weight or unrelated residual?
- Can the global diameter identity, the opposite cap, the capacity defect,
  Taylor parity, or the cut-product budget improve the upper constant?
- Do any of the eleven rows already contradict the lower span for sufficiently
  large `n` after optimizing over `s,u,t`?
- Can the span be charged simultaneously to another disjoint distance family,
  leaving too little of `[1,N]`?
- If a constant comparison cannot work, can the inequalities at least force
  a finite upper bound on `n`?

A successful milestone is a proved strict inequality whose asymptotic
constants are incompatible in every surviving row, or an explicit finite
order bound.  Another `Omega(n^2)` lower bound with no new upper bound is not
progress.

### Optional Route D — exploit branch proliferation

`FW213` can force linearly many global branch vertices.  Assess whether this
can feed a separate contradiction through degree, many small caps, Kruskal
merge products, or repeated local digit patterns.  Beware that a tree can
have linearly many degree-three vertices while keeping every local branch
small.  A pigeonhole statement must preserve weights and metric positions,
not just unweighted shapes.

You may recommend a different route if you can state its bridge lemma more
precisely than A--C.

---

## 9. Mandatory abstract-countermodel exercise

Before endorsing a route, try to build finite abstract data satisfying all of
the inequalities and local uniqueness conditions used by that route while
avoiding its desired conclusion.  The purpose is to detect missing structural
hypotheses cheaply.

At minimum try three constructions.

1. A bounded-shedding chain with marked orders `M_i`, legal LCA coordinates
   `gamma_i`, and disjoint translated sumsets across a quadratic interval.
2. A linear unseen set fragmented among many small components, with no single
   large inherited core.
3. Parameters satisfying `FW211--FW216`, Taylor's admissible order condition,
   and the trivial global diameter bounds for arbitrarily growing `n`.

Use an SMT/MILP or short script only if it represents the mathematics
symbolically or streams bounded states.  Do not materialize combinations or
large Cartesian products.  A countermodel to the relaxation is valuable even
if it is not realizable by an actual tree: it proves the relaxation alone
cannot close the route.  Conversely, failure to find a countermodel is not a
proof.

---

## 10. Verifier and computation review

The direction review is primarily mathematical.  Do not launch Hoffman2,
`geo-ws`, or a large local search.  The existing verifiers are intended to be
constant-memory arithmetic replays.  Sample commands include:

```bash
python3 theory-lab/topwindow/verify_diameter_edge_prefix_fork.py
python3 theory-lab/topwindow/verify_central_edge_prefix_offshoot.py
python3 theory-lab/topwindow/verify_central_gap_cap_descent.py
python3 theory-lab/topwindow/verify_central_shell_cap_descent.py
python3 theory-lab/topwindow/verify_deep_offshoot_deficit_descent.py
python3 theory-lab/topwindow/verify_terminal_cap_digit_pivot.py
python3 theory-lab/topwindow/verify_terminal_cap_opposite_overlap.py
python3 theory-lab/topwindow/verify_terminal_cap_reversal_absorption.py
python3 theory-lab/topwindow/verify_terminal_cap_periodic_lattice.py
python3 theory-lab/topwindow/verify_terminal_cap_lattice_lca_bound.py
python3 theory-lab/topwindow/verify_terminal_cap_visible_unseen_balance.py
python3 theory-lab/topwindow/verify_terminal_cap_unseen_spine.py
python3 theory-lab/topwindow/verify_terminal_cap_spine_span.py
python3 theory-lab/topwindow/verify_terminal_cap_parity_routing.py
```

It is acceptable to run only a justified subset.  Record wall time, peak
memory if observed, and the exact certificate/result.  Inspect whether each
script proves a symbolic tail or only checks a finite horizon.  Check that
load-bearing checks do not disappear under `python -O` and that a certificate
does not merely duplicate hard-coded expected values.

Resource rules, if any local experiment is necessary:

- no more than roughly 25--50% of the machine;
- prefer one process at `nice -n 10`;
- no unbounded state retention, combination materialisation, or giant Python
  sets/dictionaries;
- state a hard memory cap and a progress/cap outcome;
- `found=0` at a cap is `UNKNOWN`, not an exclusion;
- Hoffman2, if separately authorized later, uses `sbatch`, never `qsub`.

The prior memory failure from a three-level Python combination/product
materialisation is a known warning.  Do not reproduce that experiment.

---

## 11. Decision rubric

Score each category from `0` to `4` and justify the score with evidence.

| category | 0 | 2 | 4 |
|---|---|---|---|
| local soundness | false load-bearing lemma | fixable gaps | all key lemmas independently sound |
| global exhaustiveness | major branches untracked | scope mostly mapped, gaps remain | every branch has a proved successor |
| well-founded descent | no common measure | local decreases only | explicit global measure strictly decreases |
| route A | current relaxation admits easy countermodels | plausible but missing density lemma | bridge lemma essentially identified/proved |
| route B | unseen mass structurally arbitrary | partial component control | inherited proper-core theorem available |
| route C | lower and upper scales compatible | constants may help some rows | incompatible bounds/finite bound obtained |
| computational trust | replay not tied to theorem | arithmetic checked, semantics partly trusted | independent derivation plus meaningful replay |
| value of next budget | likely more parallel lower bounds | focused experiment could decide | named theorem is realistically within reach |

Use the following final recommendations.

- **CONTINUE:** no fatal soundness/scope gap, and at least one route has a
  named bridge lemma with a realistic falsifiable milestone.
- **CONTINUE WITH PIVOT:** the current structural chain is useful, but A--C as
  presently formulated will not close; specify the replacement route and why
  it uses existing results.
- **STOP THIS ROUTE:** a load-bearing lemma is false, the chain is not global,
  or the remaining relaxation admits scalable countermodels with no identified
  missing hypothesis.

Do not infer probability from the number of existing lemmas.  Give a rough
subjective probability only after the structural verdict, and separate:

```text
probability that the current route yields a new theorem;
probability that it yields the full G18 theorem;
probability that another route could still solve G18.
```

---

## 12. Required report format

Return one report with the following sections.

### A. Executive verdict

In at most 500 words: `CONTINUE`, `CONTINUE WITH PIVOT`, or `STOP THIS ROUTE`;
the single strongest reason; the single largest gap; and the recommended next
milestone.

### B. Snapshot and work performed

Give the audited commit, files read, commands run, results reproduced, and
items not checked.  Distinguish re-derived, replayed, and inspected evidence.

### C. Equation-by-equation audit

A table covering `FW203--FW217`, with status, exact hypotheses, finding, and
evidence anchor.  Group consecutive lemmas only when their hypotheses and
failure modes genuinely coincide.

### D. Scope ledger

List every terminal and classify it as `CLOSED`, `ABSORBED`, `STILL OPEN`, or
`SCOPE GAP`.  State the claimed successor and well-founded measure.

### E. Route analysis

For A, B, and C (and D if used): strongest plausible lemma, proof attempt,
countermodel attempt, missing hypothesis, value of another proof budget, and
a `0--4` score.

### F. Findings

Label every finding:

```text
FATAL       invalidates the intended global chain
MAJOR       material scope or proof gap; direction may need a pivot
MINOR       correctable statement, boundary, notation, or verifier issue
STRATEGIC   mathematics may be correct but does not advance the claimed route
NIT         presentation only
```

For every `FATAL` or `MAJOR` item, provide a minimal counterexample or a
precise failed inference whenever possible.

### G. Recommended next allocation

Specify one next task, its acceptance test, stop condition, suggested model
effort, and token range.  Do not recommend a large open-ended allocation.
If no bridge lemma is identifiable, recommend a partial-results paper or a
different research programme rather than “continue exploring”.

### H. Confidence and independence statement

State what evidence could change the verdict, whether any other review was
seen, and the three separate subjective probabilities requested in Section
11.

---

## 13. Suggested bounded mandate for the reviewing model

Use this guide as the complete task prompt.  A sensible first pass is
`50,000--80,000` tokens at a high reasoning setting.  Spend the budget in this
order:

```text
20%  definitions, dependency and scope map
35%  independent derivation of FW203--FW217 load-bearing steps
30%  countermodels and route A/B/C analysis
15%  synthesis, decision rubric and next milestone
```

Do not use the budget to invent a long sequence of new lemmas.  If a new
lemma appears, state it precisely and test its hypotheses; otherwise remain
in reviewer mode.  Stop early if a fatal scope gap or counterexample is found,
but document it completely.

The most useful positive outcome is not “the approach looks promising.”  It
is a precise bridge lemma whose proof would close a named arrow.  The most
useful negative outcome is not “this seems hard.”  It is a small model showing
that the current hypotheses permit the terminal to persist indefinitely.
