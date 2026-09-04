# Diagnosis

## Ranked decision

**Rank 1 — Primary route: prefix-defect endpoint-strip strict descent in the singleton-corridor large-rank branch.**

This is the only route that should receive the next bounded Ultra round.

The reason is structural, not merely evidential. The edgewise programme has already reached an all-order state in which the remaining obstruction is sharply isolated: a minimal counterexample reduces to a prefix-defect-one core \(K\) with

\[
\operatorname{dist}(K)=\{1,\ldots,C-1,D\},\qquad
C=\binom{i}{2},\quad D=C+g,\quad g\ge 21,
\]

together with a rooted weight-1/weight-2 fork, and the endpoint-strip theorem gives two forced leaves \(A,B\) with weights \(\alpha,\beta\ge g+1\) such that, for \(K_0=K-\{A,B\}\),

\[
\{1,\ldots,C-1\}
=
\operatorname{dist}(K_0)
\;\dot\cup\;
(\alpha+R_A)
\;\dot\cup\;
(\beta+R_B).
\]

This is actual-owner structure. It is already stronger than scalar moments, threshold schedules, or finite gate kernels. A strict descent from this exact tiling would convert the current finite base cases into an induction and therefore constitutes genuine all-order progress.

**Rank 2 — Thick-centre alternative.** Keep as the successor only if endpoint-strip descent hits a theorem-level obstruction. The thick-centre branch has useful interfaces (edge-excess moments, rooted spans), but no comparable exact owner tiling or nearly closed induction is currently available. Starting there now would discard the strongest invariant already proved.

**Rank 3 — G18 pure-H finite gate analysis.** It is fixed-order progress only. Q=5..9 survive, and the Q9 SMT UNKNOWN shows that pushing the same relaxation is not a controlled analytic route. Even a complete G18 gate closure would not supply an all-order mechanism.

**Rank 4 — General nonpendant unit-cut / all-pivot realization.** Exactness survives only by retaining the known \(\Theta(m^2)\) owner/LCA state. There is no strict descent parameter, so it fails the programme's compression requirement.

**Rank 5 — FW281.** Remains frozen. No new global rooted-convolution/AC-1 coefficient-separation mechanism has been identified. Repackaging convolution coefficients, threshold data, or owner/LCA incidences is explicitly not a new route.

## Diagnosis of the precise bottleneck

The next round should not attempt to prove another endpoint identity. The endpoint identities are already sufficient to expose the real missing theorem: **closure of the prefix-defect class under a proper endpoint-induced descent**.

The right question is therefore:

> Does the exact two-root owner tiling force either an immediate contradiction or a proper connected subcore that is again prefix-defect-one, still carries a 1--2 fork, and has smaller order?

If yes, the large-rank singleton-corridor branch becomes inductive. If no, the failure must be witnessed by a concrete owner-tiling pattern that survives all current exact constraints; that would be a useful theorem-level STOP because it would identify the missing invariant rather than merely kill one proof mechanism.

# Recommended approach

## Smallest theorem-shaped target

Attack the following lemma and nothing broader during the next round.

### Endpoint-Strip Descent Lemma (ESD)

Let \(K\) be a minimal counterexample in the singleton-corridor large-rank branch of order \(i\ge 15\). Put \(C=\binom{i}{2}\). Assume:

1. **Prefix-defect-one spectrum**
   \[
   \operatorname{dist}(K)=\{1,\ldots,C-1,C+g\},\qquad g\ge 21.
   \]

2. **Rooted fork**
   \(K\) contains the inherited rooted weight-1/weight-2 fork required by the corridor reduction.

3. **Endpoint strip**
   The two endpoints of the exceptional distance \(D=C+g\) are leaves \(A,B\), with pendant weights
   \[
   \alpha,\beta\ge g+1.
   \]

4. **Exact two-owner tiling**
   For \(K_0=K-\{A,B\}\),
   \[
   [1,C-1]
   =
   \operatorname{dist}(K_0)
   \;\dot\cup\;
   (\alpha+R_A)
   \;\dot\cup\;
   (\beta+R_B),
   \]
   where \(R_A,R_B\) are the exact rooted-distance owner sets arising from the two forced leaf extensions.

Then **one** of the following holds:

- **Contradiction:** the three sets above cannot tile \([1,C-1]\) while satisfying the inherited rooted 1--2 fork and the exact owner constraints; or

- **Strict descent:** there exists a proper connected subtree/core \(K'\subsetneq K_0\) of order
  \[
  11\le j\le i-2
  \]
  such that, with \(C'=\binom{j}{2}\),
  \[
  \operatorname{dist}(K')
  =
  \{1,\ldots,C'-1,C'+g'\}
  \quad\text{for some }g'\ge 21,
  \]
  and \(K'\) carries the same rooted weight-1/weight-2 fork condition after the canonical inherited rooting/re-rooting used by the corridor programme.

The decreasing parameter is therefore simply **core order**:
\[
\mu(K)=|V(K)|.
\]
No secondary scalar potential is to be introduced unless the proof itself forces one.

### Why this is the smallest genuine checkpoint

A weaker statement such as “one translated owner set contains a long interval”, “one endpoint owns many values”, or “some excess decreases” is not enough unless it mechanically yields a same-class smaller core. Those can be internal sublemmas, but they are not promotion checkpoints.

Conversely, demanding a full nonexistence theorem for the entire edgewise programme is unnecessarily broad. ESD is exactly the missing bridge between the already proved endpoint-strip theorem and the already certified finite base cases.

A successful ESD proof is all-order progress even if the thick-centre branch remains open.

## Token budget and hard stopping rule

Allocate **48k Ultra tokens total**.

- **0--12k:** normalize the exact owner tiling and derive all consequences that use only disjointness, cardinality, endpoint weights, and the rooted 1--2 fork.
- **12--24k:** search for a canonical stripping map \(K\mapsto K'\) and prove that the image preserves prefix-defect-one form and \(g'\ge21\).
- **24k midpoint:** mandatory promotion/STOP decision.
- **24--40k:** only if the midpoint criterion passes, complete the descent proof and discharge fork inheritance / order bounds.
- **40--48k:** adversarial pressure tests, finite certification of any bounded auxiliary claim, and final theorem audit.

### Midpoint STOP rule at 24k

STOP the round at 24k unless **both** conditions hold:

1. A specific candidate subcore \(K'\) is defined from the owner tiling by a deterministic structural rule, not by topology enumeration or solver search; and
2. At least two of the three closure properties have analytic proofs:
   - prefix interval \([1,C'-1]\) survives exactly,
   - there is exactly one exceptional distance \(C'+g'\) with \(g'\ge21\),
   - the rooted 1--2 fork survives canonically.

If no such map exists by 24k, do **not** spend the remaining budget inventing new scalar potentials. Record the minimal owner-tiling obstruction and STOP.

# Files-functions to modify

For the requested deliverable, create/update only:

- `2026-08-26-001-choose-next-leech-tree-research-route-af/response.md` — this decision memo.

During the Ultra research round itself, do not modify the theorem programme until promotion. Work in a scratch proof file or temporary notes.

Only after ESD passes promotion criteria should the result be incorporated into:

- `docs/prefix-defect-endpoint-strip.md` — add the proved descent lemma immediately after the endpoint-strip theorem.
- `docs/edge-handoff-orientation.md` — replace the large-rank singleton-corridor UNVERIFIED boundary with the induction.
- `docs/nonexistence-roadmap.md` — mark the singleton-corridor large-rank branch closed and expose the thick-centre branch as the next unresolved all-order target.
- `docs/heaviest-edge-rigidity.md` — modify only if the proof strengthens or changes the stated all-order handoff hypotheses.

Do **not** modify `docs/canonical-mismatch-gate-transport-stop.md` unless an independent global FW281 convolution-separation theorem is actually discovered.

# Implementation sequence

1. **Freeze the class exactly.** Restate the large-rank minimal-counterexample hypotheses with no weakening: prefix defect one, \(g\ge21\), rooted 1--2 fork, forced \(D\)-end leaves, \(\alpha,\beta\ge g+1\), and exact disjoint owner tiling.

2. **Write the owner map explicitly.** Every \(t\in[1,C-1]\) has exactly one owner:
   \[
   \mathcal O(t)\in\{K_0,A,B\}.
   \]
   Work with owner changes and rooted realizations, not counts of owners.

3. **Exploit the low strip first.** Since \(\alpha,\beta\ge g+1\),
   \[
   [1,g]\subseteq \operatorname{dist}(K_0).
   \]
   Use the rooted 1--2 fork to anchor which vertices realize the first distances. The first objective is to show that the low-prefix realization cannot be repeatedly interrupted by translated endpoint-owner blocks without producing either an overlap or a removable terminal structure.

4. **Define one canonical candidate descent.** The preferred form is: strip the maximal terminal owner block forced by one endpoint, delete the corresponding forced terminal vertices/edges, and take the minimal connected subcore containing the inherited 1--2 fork and all owners of the surviving initial interval. The construction must be deterministic from owner data.

5. **Prove prefix closure.** Show that the selected subcore realizes every value \(1,\ldots,C'-1\). This must be an exact realization statement, not a cardinality equality.

6. **Prove one-defect closure.** Show that all remaining pair distances of the subcore consist of exactly one exceptional value \(C'+g'\), and establish \(g'\ge21\). If this is the step that fails, isolate the first precise owner pattern that causes failure.

7. **Prove fork inheritance.** The 1--2 fork must lie in the retained subcore or have a canonical replacement produced by the stripping operation. No existential “some small fork remains” is sufficient.

8. **Apply minimality.** Once \(11\le |K'|\le i-2\) and the same class is preserved, minimality gives the contradiction. Orders 11--14 then act as finite base cases, not as evidence for the inductive step.

9. **Only after the analytic proof exists**, use finite computation to audit bounded transition claims, not to discover the theorem.

# Edge cases

The following pressure controls must be passed before ESD is promoted.

- **Seven surviving small-rank prefix forests.** Every local inference used by ESD must be checked against all seven exact forests. They are mandatory adversarial models because they already encode the L3/L4/L6 cores with a two-edge tail.

- **Canonical L6 sign/mismatch pathology.** Although FW281 is frozen, any ESD sublemma that quietly assumes uniform sign, same-root ownership, least-threshold ownership, or strict local lifting must be rejected immediately; canonical full-spectrum L6 already invalidates those mechanisms.

- **Endpoint symmetry.** The proof must work when the roles of \(A\) and \(B\) are swapped. No argument may depend on choosing “the better endpoint” unless a proved asymmetric invariant selects it.

- **Equal or nearly equal pendant weights.** Explicitly test \(\alpha=\beta\), \(|\alpha-\beta|=1\), and the boundary \(\min(\alpha,\beta)=g+1\). Disjointness of translated root sets, not informal separation, must handle these cases.

- **Interleaving owner sets.** Do not assume \(\alpha+R_A\) and \(\beta+R_B\) are intervals or appear as two contiguous blocks. Construct synthetic exact set tilings with maximal interleaving consistent with cardinalities and test every claimed monotonicity against them.

- **Fork attached to a stripped endpoint.** Verify that the descent construction cannot delete one arm of the rooted 1--2 fork without producing a canonical replacement. This is a promotion-critical case.

- **Small target order.** If stripping can produce \(j<11\), the induction is not closed by the current finite base. Either prove \(j\ge11\), prove the smaller orders separately, or weaken the claimed closure. Do not hide this under “finite check”.

- **Gap degradation.** The proof must establish \(g'\ge21\). A descent that reduces order but lets \(g'\) fall below the all-order handoff threshold is not a same-class induction.

- **Selective order-16 evidence.** Use the certified selective order-16 zero result only as a pressure test. It must not enter the analytic proof as an implicit base case unless its hypotheses exactly match the descended class.

- **Owner realization versus counting.** Any step of the form “the sizes add up, therefore the distances are the required prefix” is invalid unless the exact realizers/owners are tracked.

# Verification

## Analytic promotion criteria

Promote ESD only if the written proof contains all of the following:

1. A deterministic definition of \(K'\) from the exact owner tiling.
2. A proof that \(K'\subsetneq K_0\), hence \(|K'|\le i-2\).
3. A proof that \(11\le |K'|\).
4. Exact realization of
   \[
   \{1,\ldots,\binom{|K'|}{2}-1\}
   \]
   inside \(K'\).
5. Proof that there is exactly one remaining exceptional distance.
6. Proof that its gap satisfies \(g'\ge21\).
7. Proof of canonical inheritance/reconstruction of the rooted 1--2 fork.
8. No use of an unproved interval-inheritance assumption.
9. No storage of all owner/LCA incidences and no \(\Theta(m^2)\) state disguised as notation.
10. A minimal-counterexample closure paragraph showing precisely how finite base orders 11--14 terminate the descent.

If any one of items 3--7 is absent, the result is a useful sublemma at most, not closure of the large-rank branch.

## Finite verification criteria

Finite computation is admissible only for bounded auxiliary claims.

- Re-run the exact prefix-state checker on the seven surviving forests against every local claim used in ESD.
- Check all finite base orders that the induction can actually reach. If the analytic descent proves \(11\le j\), the existing certified zero results for 11--14 are sufficient only after confirming that their hypotheses exactly match the ESD class.
- Any new bounded enumeration must have a stated finite domain, exact arithmetic, reproducible hash/log, and a theorem sentence saying exactly which finite proposition it verifies.
- UNKNOWN is failure to certify, not evidence.
- No topology search may be used as the reason ESD is believed.

## What success closes

A full ESD proof closes the **singleton-corridor large-rank branch all-order**, because a minimal counterexample would descend to a smaller member of the same class and eventually hit the certified zero base orders.

Combined with the already completed analytic small-rank dichotomy and its exact finite reduction, this should close the **singleton-corridor branch**, provided the seven residual small-rank forests are already discharged exactly under the programme's current statements.

It does **not** by itself prove the full Leech-tree nonexistence theorem. The **thick-centre / bidirectional-corridor alternative** remains. That would become the next all-order target.

It does **not** reopen or close FW281, and it does **not** make G18 gate analysis an all-order theorem.

# Avoid

- Do not reopen FW281 without an explicit new theorem coupling every rooted merge-convolution coefficient to AC-1 strongly enough to separate all coefficients.
- Do not encode the entire rooted convolution vector, all owner/LCA incidences, or equivalent \(\Theta(m^2)\) state.
- Do not spend the round on more fixed-order topology enumeration.
- Do not scale the Q9 UNKNOWN SMT relaxation.
- Do not promote scalar edge-excess moments or rooted-span inequalities unless they force an actual owner-level descent.
- Do not assume translated rooted-distance sets are intervals.
- Do not use cardinality equality as a substitute for exact owner realization.
- Do not claim “induction” unless the descended object satisfies the same quantified class, including \(g'\ge21\) and the rooted 1--2 fork.
- Do not broaden the target to the thick-centre branch during this 48k round.
- At the 24k midpoint, if no deterministic \(K\mapsto K'\) rule exists with at least two closure properties proved analytically, STOP and record the minimal surviving owner-tiling obstruction. That is preferable to another mechanism-specific 60k failure.
