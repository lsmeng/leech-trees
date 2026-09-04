# Escalation Request — 2026-08-26-001-choose-next-leech-tree-research-route-af

- **Type:** MATHEMATICAL
- **Title:** Choose next Leech-tree research route after FW281 STOP
- **Repo:** /Users/geoclaw/Documents/Codex

## Exact question

Given the current audited Leech-tree programme, which single research route
should receive the next bounded Ultra round, and what is the smallest theorem
statement/checkpoint that would constitute genuine progress rather than
another mechanism-specific STOP?

## Current state

The just-completed FW281 route tried to prove canonical pendant rank
anti-coalescence.  It reached a strict 60k checkpoint STOP:

- Exact threshold identities and the exact rooted Kruskal merge polynomial
  are proved.
- Scalar threshold/Kruskal data are insufficient.
- Canonical full-spectrum L6 invalidates least-threshold, same-root,
  uniform-sign and strict local-lift arguments.
- A non-Leech Q=4 pressure family passes exact top ownership and Taylor
  parity but collides after transformation.
- Reopening FW281 requires a genuinely global theorem separating every
  coefficient of all rooted merge convolutions by coupling them to AC-1.
  Directly storing the coefficients is the known Theta(m^2) fallback.
- FW281 proves no exclusion and gives no canonical full-state counterexample.

There is a separate, more advanced edgewise programme with actual all-order
input:

- Every edge with cut product at least 11 has an internal handoff within
  offset 10.  Finite exact ladders strengthen the excess through nine holes.
- Edge orientations reduce terminals to a thick centre or bidirectional
  corridor; this avoids the old interval-inheritance requirement.
- The singleton corridor has an analytic rank dichotomy.  The small-rank
  branch was reduced by 4,537,700 exact prefix states to seven forests, all
  extensions of known L3/L4/L6 cores with a two-edge tail.
- The large-rank branch analytically reduces, in a minimal counterexample, to
  one prefix-defect-one core K of order i:
    dist(K) = {1,...,C-1,D}, C=binom(i,2), D=C+g, g>=21,
  with a rooted weight-1/weight-2 fork.
- Orders 11--14 and a selective order-16 version have certified zero cores,
  but this is finite evidence, not induction.
- The endpoint-strip theorem is analytic: the D endpoints are leaves with
  weights alpha,beta>=g+1; deleting both preserves 1,...,g and the 1--2 fork;
  for K0=K-{A,B}, exact owner tiling holds
    {1,...,C-1} = dist(K0) disjoint_union
                    (alpha+R_A) disjoint_union (beta+R_B).
  The missing step is a decreasing induction/parameter from this exact
  two-root tiling.

Other open routes are weaker at present:

- G18 pure-H finite gate analysis excludes only Q=10..14; Q=5..9 survive and
  a Q9 SMT run was UNKNOWN.
- General nonpendant unit-cut arithmetic certificates survive until full
  all-pivot rooted realization, which retains Theta(m^2) owner/LCA state.
- Weighted edge-excess moments and rooted-span bounds currently eliminate no
  order-18 topology; they are interfaces to a future thick-centre theorem.

## Relevant files

- /Users/geoclaw/Documents/claude/projects/leech-trees/docs/canonical-mismatch-gate-transport-stop.md — FW281 exact STOP and only reopen condition.
- /Users/geoclaw/Documents/claude/projects/leech-trees/docs/heaviest-edge-rigidity.md — all-order edge handoff, finite excess ladder and global moment identities.
- /Users/geoclaw/Documents/claude/projects/leech-trees/docs/edge-handoff-orientation.md:11980 — singleton-corridor reduction, seven prefix forests and large-rank collapse.
- /Users/geoclaw/Documents/claude/projects/leech-trees/docs/prefix-defect-endpoint-strip.md — exact endpoint-strip theorem and remaining induction gap.
- /Users/geoclaw/Documents/claude/projects/leech-trees/docs/nonexistence-roadmap.md:1980 — FW281 STOP followed by the edgewise successor programme.

## Attempts already made

1. Local AC-2 mismatch pairing -> canonical L6 has both connector-positive
   and overlap-negative corrections through different gates.
2. Threshold/Kruskal scalar potential -> noncanonical full L6 satisfies the
   complete scalar schedule while a rooted convolution coefficient repeats.
3. Direct all-owner/LCA state -> exact but Theta(m^2), no strict descent.
4. Fixed G18 gate kernel -> closes Q=10..14 only; Q=5..9 remain.
5. Edgewise handoff/corridor reduction -> genuine progress; now stalls only
   at the prefix-defect endpoint-strip induction and thick-centre alternative.

## Observed failure

FW281's frozen conclusion is:

"The 60k checkpoint therefore triggers STOP. ... The route may be reopened
only with a genuinely global theorem combining the rooted merge convolution
(FW281.6) with AC-1 (FW280.12) to separate every coefficient. A proposal that
merely stores all convolution coefficients or owner/LCA incidences is the
known Theta(m^2) fallback, not a descent."

The endpoint-strip note's exact remaining boundary is:

"The remaining all-order step is to combine the exact tiling (2) for both
forced leaf extensions with the rooted 1--2 fork, or to prove that repeated
endpoint stripping creates a proper prefix-defect core with a strictly
smaller parameter. Until that decreasing parameter is proved, the
singleton-corridor branch remains UNVERIFIED."

## Constraints

- Recommend one primary route, not a portfolio of vague ideas.
- Do not recommend more brute-force topology enumeration or scaling an
  UNKNOWN solver relaxation.
- The next round must have an explicit token budget, midpoint stop criterion,
  pressure controls and a theorem-shaped success condition.
- Distinguish all-order progress from fixed-order/G18-only progress.
- Prefer actual-owner analytic structure over scalar moment/counting bounds.
- The current FW281 route is frozen unless a new global convolution-separation
  mechanism is explicitly identified.

## Requested output

Return, in `response.md`:

1. Ranked decision: the single recommended route and why the alternatives lose.
2. The exact smallest lemma to attack, with quantified hypotheses/conclusion.
3. A bounded execution plan, token budget and midpoint STOP rule.
4. Pressure controls/counterexamples that must be tested before promotion.
5. What success would close (singleton corridor, G18, or all-order theorem)
   and what would still remain.
6. Verification/promotion criteria for analytic and finite parts.
