# Q1 directed-hole / no-return sprint

Status: controlled 400k-token Ultra research sprint, stopped at FW268 on
2026-08-25 after its predeclared no-return test failed.

This sprint begins strictly after FW267.  Its purpose is not to improve a
span or density constant.  It tests the last narrow escape left by the
bounded-cap/core-exchange audit: whether the position of a high-band hole can
be oriented into a normalization-invariant, strictly decreasing state.
Nothing below is G18.  Every proposed conclusion remains **UNVERIFIED** until
it has an all-branch proof, independent audit and frozen controls.

## Frozen ambient state

For every hypothetical Leech tree of order `n>=5`, FW218 fixes the q=1
diameter orientation.  Write its diameter endpoints as `x,z`, where deleting
`z` leaves diameter `N-1`, and put

```text
Q=N-diam(T-x)>=2,  M=N-Q.
```

FW219 supplies the unique reflected-coordinate vertices
`v_0=z,v_1,...,v_(Q-1)` and the missing coordinate `Q`; FW242 supplies the
nested actual-pair ledger `T_j`; FW261 supplies

```text
I_M=F_K+X^gR_p(K)+X^hR_r(H_Q).
```

FW266 proves that a same/lower-prefix `x`-core with fewer than `Q` external
vertices is impossible.  FW267 proves that a near-full prefix cannot forget
the actual-pair vertex labels of its accumulated external set.

## Candidate exchange state

Let `alpha=v_j` be a true visible leaf eligible for exchange, and put

```text
C_alpha=T-{z,alpha},  E_alpha={z,alpha}.
```

The internal high band of `C_alpha` has the unique missing owner

```text
d(x,alpha)=N-j,
```

which is retained externally with its original pair label `{x,alpha}`.  The
raw candidate rank is the coordinate `j`, possibly refined by the visible
component order, its entry coordinate and the opposite first hole `Q`.

This is only a state description.  The L6 control already shows that changing
`alpha` can move the high hole reversibly while every coarse mass/count stays
fixed.

## Definition of success

A directed-hole mechanism is accepted only if all of the following are
proved.

1. **Complete eligibility.** Every nonterminal FW261 state contains a stated
   eligible leaf, or belongs to a finite certified exception list.
2. **Actual-pair exchange.** Every low/high coefficient after the exchange is
   assigned to its unique original unordered pair; no anonymous numerical
   hole or ghost substitutes for provenance.
3. **Normalizer.** A deterministic normalization map is defined on the full
   contextual output, including all external owners.  It may not silently
   reapply a theorem whose hypothesis requires an ambient Leech tree to a
   non-Leech induced core.
4. **Invariant rank.** The rank is independent of equivalent factor
   packaging and is comparable before and after every allowed endpoint
   reorientation.
5. **Strict no-return.** Every noncollision branch strictly lowers a
   well-founded rank, and no later normalization can restore a previous rank
   or state with the same fully charged owner context.
6. **Closure.** The normalized output re-enters the same state definition or
   a finite terminal catalogue.  Merely walking along the FW242 nested ledger
   while its external order grows is not closure.
7. **Terminal force.** A minimal-rank state gives a distance collision, a
   checker-verified known witness below the target range, or a separately
   certified finite contextual exclusion.

## First audit question: can ambient normalization change?

The first branch to settle is the following **UNVERIFIED uniqueness claim**.
If the distance-`N` pair is unique, every vertex other than its two endpoints
has deletion deficit zero because the diameter pair remains.  If, for
`n>=5`, exactly one diameter endpoint has deletion deficit one, then every
ambient q=1 normalization returns the same ordered pair `(z,x)` and the same
`Q`.  In that case neither `Q` nor an ambient visible coordinate can decrease
under reorientation; a successful rank would require a genuinely contextual
normalizer rather than a second application of FW218.

This claim has now been proved and frozen in FW268.  It is an ambient
normalization rigidity statement, not a contextual no-return theorem.

## Hard stop

At approximately 200k tokens, stop the route unless at least one of the
following has been proved:

- an actual contextual normalizer with bounded fully charged owner order;
- a normalization-invariant rank with a strict no-return proof;
- a complete `Q=2,3` terminal catalogue which is a valid base of that rank.

If ambient q=1 normalization is unique, contextual normalization is not
closed, and all proposed ranks admit a reversible or context-growing walk,
freeze the exact obstruction and pivot away from directed-hole exchange.
Do not spend the remaining budget on another compatible inequality.

## Outcome

The sprint reached the hard stop.  It produced an exact owner-labelled
exchange interface and two normalization obstructions, but no recurrence,
collision, finite terminal catalogue, order exclusion or G18.

### Entry and rolling eligibility are different

For `1<=b<Q`, let `p_z` be the neighbour of `z` and define

```text
Entry(b)  iff deg_(T-z)(v_b)=1,
Roll(b)   iff Entry(b) and v_b!=p_z
          iff deg_T(v_b)=1.
```

`Entry(b)` is exactly what is needed for
`C_b=T-{z,v_b}` to be connected and for its deleted endpoint class to be a
single rooted factor.  `Roll(b)` is the stronger condition needed to put `z`
back and regard exchange between two visible leaves as reversible.  FW242
only proves that `v_b` is a leaf at its own nested stage; it does not prove
`Roll(b)`.  In particular, the `L4` path has an entry-only `v_1=p_z`, whereas
the `L6` witness has rolling coordinates `b=1,3`.

### Exact directed-hole ledger

For every entry-eligible `b`, actual unordered pairs give the disjoint
identity

```text
I_(N-1)=F_(C_b) + L_0 + X^(N-b)_[owner {x,v_b}] + L_b,
supp(L_0),supp(L_b) subset I_M,
|L_0|=n-2, |L_b|=n-3.
```

Here `L_0` consists of the pairs `{z,u}` with `u` different from `z,x`, and
`L_b` consists of `{v_b,u}` with `u in C_b-{x}`.  Consequently

```text
Spec(C_b) intersect [M+1,N-1]
  =[M+1,N-1]-{N-b},
```

and the named high-hole height is `Q-b`.  This is an **OBSERVED exact weak
two-external interface**.  It is not the FW261 state again: its prefix ends at
`N-1`, not `M`, and the rooted-factor schema has changed.

### Both obvious normalizers fail

Define `q_T(u)=N-diam(T-u)`.  FW268 proves

```text
q_T(u)=0 for u not in {x,z},
q_T(z)=1,
q_T(x)=Q>=2.
```

Thus the ambient FW218 normalizer is unique and always returns the same
`(z,x,Q)`; it cannot reset `Q` or the reflected coordinate `b`.

The other obvious move is also invalid.  For target orders, `C_b` is never an
order-`n-2` Leech tree.  If `Q>=3`, another visible `v_i` remains and its
internal distance from `x` is `N-i>binomial(n-2,2)`.  If `Q=2` and `n>=7`,
the `z`-leaf edge has its unique owner outside `C_b` but lies within
`[1,binomial(n-2,2)]`, which a smaller Leech tree would have to fill.  Hence
FW218/FW219 cannot be reapplied to the exchange core.

These two results do not rule out a newly defined owner-aware contextual
normalizer.  No such normalizer is presently known.

### Exact no-return pressure and small-Q audit

The `L6` witness gives two actual-pair states, at `b=1` and `b=3`, with the
same core order, external order, prefix endpoint, low internal mass and high
band length.  Their single high holes are respectively `N-1` and `N-3`, and
the two choices form an involution inside the fixed ambient owner ledger.
This is a pressure control, not a certified contextual transition.  The
ambient `Q` stays four; a purely numeric
normalization of the two non-Leech cores has opposite deficits four and
eight.  Thus raw `b`, `Q-b`, high-hole location, internal diameter and numeric
opposite deficit can all stay flat, reverse or increase.  This is an
**OBSERVED known-witness obstruction** to every potential which treats both
rolling directions as legal or identifies the two states by normalization.
It is not a large-order Leech counterexample.

The complete small-band audit also fails to supply a terminal base.  `Q=2`
has two visible-forest forms: a rooted-`L2` twig with no rolling entry, and a
two-singleton row already at rank one.  `Q=3` has five collision-free forms
after the double weight-one chain is removed; four already contain a rank-one
leaf, and the all-singleton row allows a reversible choice.  Their core
`H_Q` still has order `n-Q-1`, so this finite entry syntax is not a uniformly
finite contextual catalogue.  The classification is **OBSERVED as a finite
interface diagnostic**; terminal collision/UNSAT remains **UNVERIFIED**.

## Decision

The directed-hole route is stopped at FW268.  Reopen it only after defining a
total owner-equivariant contextual normalizer whose input and output have the
same bounded charged state, whose transition strictly removes an actual
eligible owner without creating or restoring one, and whose empty-owner case
has a certified terminal.  An artificial rule `b` increasing gives only a
finite walk inside one fixed ambient tree and does not meet this requirement.

The frozen replay is:

```text
theory-lab/topwindow/verify_q1_directed_hole_interface.py
theory-lab/topwindow/results/q1_directed_hole_interface_certificate.json
```

Any later filename adjustment must be mirrored here and in the README,
roadmap and main proof ledger.  G18 remains **UNVERIFIED**.
