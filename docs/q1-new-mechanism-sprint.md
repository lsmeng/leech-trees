# Q1 bounded-context mechanism sprint

Status: controlled 300k-token Max research sprint concluded at FW267,
2026-08-25; no bounded-context closure or order exclusion.

This note starts strictly after FW265.  It contains proof obligations, not
G18.  Every proposed mechanism below is **UNVERIFIED** until it has a complete
actual-pair proof, an independent audit and a frozen replay certificate.

## Frozen input

For every hypothetical candidate of order `n>=5`, FW261 supplies the exact
q=1 two-root state on `K=T-{x,z}`,

```text
I_(N-Q)=F_K+X^gR_p(K)+X^hR_r(H_Q),
```

and FW262 supplies a positive linear defect floor.  FW263 rules out deleting
one or two leaves while absorbing every deleted coefficient into one terminal
suffix.  FW264 shows that a fixed-core singleton-boundary ledger retains the
three actual-pair labels `zp,xr,alpha-a`.  FW265 expands a cut product into
exactly `|A|` named rooted shifts.  None of FW263--FW265 is an order
exclusion.

## Definition of a successful mechanism

A candidate recurrence is accepted only if all of the following are proved.

1. **Complete entry.** Every state produced by the frozen q=1 interface enters
   one of finitely many stated branches; no topology or owner class is
   silently omitted.
2. **Actual-pair provenance.** Every coefficient in every external block is
   labelled by an actual unordered pair of the original tree.  Numerical
   ghosts may be retained only with their original pair labels.
3. **Controlled context.** Preferably the number of boundary blocks and total
   cap order are bounded independently of `n`.  A nonconstant context is
   admissible only if its full owner-expanded order is charged in an explicit
   well-founded potential which proves eventual absorption or termination.
   A formal product such as `R_a(A)R_b(B)` is charged by its owner-expanded
   cap order, not counted as one factor.
4. **Exact prefix identity.** The receiving connected induced core and its
   boundary blocks tile a specified interval coefficientwise, with all holes,
   maxima and root shifts stated exactly.
5. **Strict descent.** A well-founded measure such as
   `(core order, total cap order, boundary-label count, first-hole parameter)`
   decreases on every noncollision branch.  Merely decreasing one component
   while allowing an earlier component to grow is insufficient.
6. **Closure.** The output satisfies the same contextual state definition, or
   lands in a finite certified terminal catalogue.  A smaller tree without an
   inherited interval is not a recurrence.
7. **Controls and scope.** Every SAT witness passes `src/checker_a.py` and
   `src/checker_b.py`; the five known witnesses are explicit boundary
   controls.  All conclusions are labelled OBSERVED, LITERATURE or
   UNVERIFIED in the repository ledger.

## Route A: bounded cap / prefix locality

Let a selected edge `e=ab` split `K` into `A ni a` and `B ni b`.  FW265 gives

```text
F_K=F_A+F_B+sum_(u in A) X^(w+d(a,u))R_b(B).
```

The **UNVERIFIED target** is to prove that, for a cut selected from the FW259
trunk segment, all shifts meeting the retained `B` prefix arise from a cap of
uniformly bounded order, while every remaining shift lies completely above
that prefix.  The conclusion must state the prefix endpoint and preserve the
old endpoint owners.

Failure condition: a scalable actual-tree/LCA model satisfying all currently
used q=1 hypotheses has an unbounded set of prefix-intersecting named shifts,
or current hypotheses leave their intersections freely placeable.

## Route B: core exchange

FW264 does not cover a state which moves `x` or the peeled leaf into the next
internal core.  The **UNVERIFIED target** is an exchange

```text
(internal core C, bounded boundary context E)
    -> (internal core C', bounded boundary context E')
```

with an exact coefficient identity, actual-pair labels and a strict
well-founded decrease.  The exchange must account explicitly for every pair
between the vertices entering and leaving the core; it may not relabel the
unique coefficients `h` or `w`.

Failure condition: every exchange necessarily creates a cross product whose
owner-expanded cap order is unbounded, or produces a context component which
can grow on the next step.

## Stop rule

Stop this sprint without promoting a new theorem if both routes require an
unproved bounded-context assertion, if pressure models show that the current
hypotheses do not control the relevant owner locations, or if the only gains
are new density/span/heavy-edge constants.  A negative result must identify
the exact missing hypothesis and the strongest statement which remains
correct.

## Sprint outcome

The controlled sprint reached the stop rule.  It produced two exact
obstructions, but no bounded-context recurrence and no order exclusion.

- **OBSERVED (FW266):** a same- or lower-prefix core exchange containing the
  endpoint `x` must leave at least `Q` vertices outside the new core.
- **OBSERVED (FW267):** a near-full actual-pair prefix cannot forget any of
  its external vertices merely by changing the algebraic packaging of their
  owner classes.
- **UNVERIFIED:** bounded prefix locality at the FW259 trunk cut, a repeatable
  dual-band exchange, a normalization-invariant directed-hole descent, every
  new order exclusion and G18.

The conclusion is a route decision.  It does not assert that bounded-cap or
core-exchange arguments are false for hypothetical Leech trees; it says that
the frozen FW261--FW265 input does not currently supply the missing closure
theorem.

## FW266: top-band cost of exchanging the core

Keep the FW261 orientation, so the visible vertices satisfy

```text
d(x,v_j)=N-j,  1<=j<Q,  M=N-Q.
```

Let `x in C`, put `E=T-C`, and suppose a positive coefficientwise state
contains the complete actual-pair internal term `F_C` with
`supp(F_C) subset I_(M')`, where `M'=M+s` and `s` is an integer.  If
`v_j in C`, the monomial owned by `{x,v_j}` forces

```text
N-j<=M+s,  hence j>=Q-s.                            (FW266a)
```

Therefore

```text
|C intersect {v_1,...,v_(Q-1)}|
    <=max(0,min(Q-1,s)).                            (FW266b)
```

For `0<=s<Q`, the diameter endpoint `z` is also outside `C`, and

```text
|E|>=Q-s.                                          (FW266c)
```

Equivalently, if `z in E`, `1<=e=|E|<Q`, and
`supp(F_C) subset I_(M')`, a pigeonhole among `v_1,...,v_e` gives

```text
M'>=N-e,  q'=N-M'<=e.                              (FW266d)
```

In particular,

```text
M'<=M=N-Q  implies  |E|>=Q.                        (FW266e)
```

Equations (FW266a)--(FW266e) prove the **OBSERVED q=1 core-exchange
top-band obstruction**.  For the canonical deleted set
`E={z,v_1,...,v_(e-1)}`, its complement `C=T-E` is exactly the old FW242
stage `T_e`; its equality does not create a new recurrence.  The result does
not exclude `M'>M`, a dual-band
state, `Q=O(1)`, `e>=Q`, a state without the complete `F_C` term, or signed
cancellation.  Replay:

```text
theory-lab/topwindow/verify_q1_core_exchange_top_band.py
theory-lab/topwindow/results/q1_core_exchange_top_band_certificate.json
```

## Route A audit: what prefix occupancy really gives

For the FW265 cut, write the `B`-rooted depth set as `D_B`, put

```text
lambda_u=w+d_A(a,u),  S_u=lambda_u+D_B,  u in A,
```

and let `c_u(L)=|S_u intersect I_L|`.  Since `0 in D_B`, the exact entry
criterion is

```text
S_u intersects I_L  iff  lambda_u<=L.              (A1)
```

Thus bounded prefix locality is exactly a bounded rooted-ball assertion for
`A` at `a`; it is not supplied by the FW265 product identity.  If
`supp(F_B) subset I_L`, support-disjointness gives the **OBSERVED conditional
occupancy bound**

```text
sum_u c_u(L)<=R_L:=L-binomial(b,2),                 (A2)
N_r(L):=|{u:c_u(L)>=r}|<=floor(R_L/r).              (A3)
```

For a proposed FW261-type receiving endpoint
`L=binomial(b,2)+b+h_B`, with `0<=h_B<=b-1`, this becomes

```text
N_r(L)<=floor((2b-1)/r).                            (A4)
```

Consequently at most one whole order-`b` shift can lie in the prefix, but
(A2)--(A4) alone do not exclude as many as `2b-1` one-coefficient grazers.
No `O(1)` consequence has been proved from the current moment/Kruskal/LCA
interface.

The missing Route A input is now exact.  One must prove, at a specified FW259
cut and an inherited receiving endpoint, at least one of

```text
|{u in A:d_A(a,u)<=L-w}|=O(1),
every non-cap shift contributes Omega(b) prefix coefficients,
or a complete owner-preserving absorption of the grazing shifts.
```

FW259 does not yet inherit the required `B`-state or its endpoint `L`, so
even a constant active-shift bound would be necessary but not sufficient for
closure.  The bounded-cap / prefix-locality theorem remains **UNVERIFIED**.

## Route B audit: exact exchanges conserve the owner context

Raising the endpoint avoids (FW266e) for one step.  For an integer
`1<=c<=Q`,
moving `v_0=z,v_1,...,v_(c-1)` outside leaves the connected old FW242 core
`T_c`, and the top `c` values are exactly the pairs
`xv_0,...,xv_(c-1)`.  Hence `I_(N-c)` has an exact actual-pair ledger on
that core.  This is **OBSERVED**, but it is FW242 partial telescoping, not a
new state: advancing from `T_c` to `T_(c+1)` adds the next named external
owner class, so the context grows to order `Q`.

There is also a general obstruction to erasing that history.  For `n>=5`,
strict heaviest-edge rigidity gives every incident edge `f`

```text
w(f)<=N-a(n-a)<=N-(n-1).                           (FW267a)
```

If `E` has order `1<=e<=n-2`, then

```text
w(f)<=N-e-1<N-e.                                   (FW267b)
```

For every `y in E`, an incident pair `{y,u}` therefore has its globally
unique coefficient inside `I_(N-e)`.  An actual-pair ledger for that prefix
must keep `y` in its external vertex-label support.  Thus the active external
vertex order is at least `e`.  This proves the **OBSERVED near-full-prefix
external-owner conservation theorem** (FW267).  It counts vertices in the
owner labels, not coefficients or algebraic factors: one external--external
edge may witness two vertices, and bundling remains allowed.  Replay:

```text
theory-lab/topwindow/verify_q1_near_full_external_owner_conservation.py
theory-lab/topwindow/results/q1_near_full_external_owner_conservation_certificate.json
```

FW267 does not forbid a rolling exchange, an owner-preserving
merger/absorption with an explicit strictly decreasing fully charged
potential, signed cancellation, or a dual-band recurrence.  It does prove
that a nested core cannot shrink through near-full prefixes while its fully
owner-charged external vertex order stays uniformly bounded.

## Pressure controls and the remaining narrow exit

**OBSERVED L6 control:** the known witness has a two-state core-exchange
plateau: two different visible leaves can be exchanged while core order,
external order, prefix endpoint, low external mass and high-band length all
remain fixed; only the position and owner of one high hole changes.  Thus
those coarse counts do not strictly decrease on this specific swap.  A
scalable exact plateau theorem for hypothetical large-`Q` candidates remains
**UNVERIFIED**, as does a potential directed by the hole position.

The only unclosed core-exchange exit found in this sprint is therefore the
following **UNVERIFIED directed-hole lemma**:

> Exchanging an extremal eligible visible leaf either gives a collision or
> returns a bounded-context state in which a normalization-invariant hole
> rank (or `Q`) strictly decreases and cannot be reset by reorientation.

Without the no-return clause this is merely a directed walk across an
equal-size plateau.  No such invariant, collision or finite terminal
catalogue is currently proved.

## Decision and next trigger

Routes A and B are stopped at FW267 under the predeclared rule.  Further
density, span, moment or heavy-edge constants do not address owner locality.
Reopen this mechanism only if one of the following arrives:

1. an FW259-specific rooted-ball/no-grazing theorem together with an inherited
   receiving prefix;
2. an owner-preserving merger/absorption with an explicit strictly decreasing
   fully charged potential;
3. a normalization-invariant directed-hole no-return theorem;
4. a proof that `Q` belongs to a fixed finite set, followed by a complete
   finite contextual catalogue.

Until then, the q=1 interface is a strong exact normal form with two audited
route obstructions, not an all-order exclusion.  G18 remains **UNVERIFIED**.
