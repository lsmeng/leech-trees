# Q1 two-root closure sprint

Status: controlled proof specification, 2026-08-25.

This note freezes the only global route authorised after FW258--FW262.  It
does not assert G18.  Every statement labelled **UNVERIFIED target** is a
proof obligation, not a theorem.

## 1. Frozen exact state

Use the universal endpoint-one orientation of FW218--FW219.  Delete the two
diameter endpoints `x,z` and write

```text
K=T-{x,z},          k=|K|=n-2,
H=H_Q subset K,     M=N-Q,
g=w(zp),            h=w(xr).
```

FW261 gives the coefficientwise disjoint identities

```text
I_M = F_K + X^g R_p(K) + X^h R_r(H),
X^h R_r(K) = X^h R_r(H) + I_[M+1,N-1].             (S1)
```

FW262 allocates the low holes of `F_K` exactly between the two rooted
factors.  If their counts are `q,b`, then

```text
delta=q+b,
delta/k >= 10-4sqrt(6)-o(1).                       (S2)
```

These are **OBSERVED** inputs.  They locate two linear suppliers but do not
locate the owner pairs inside their tree/LCA geometry.

## 2. Exact one-leaf obstruction

Let `alpha` be a leaf of `K`, with neighbour `a` and incident weight `w`, and
put `K'=K-alpha`.  If `alpha` is not in `H`, direct subtraction from (S1)
gives

```text
D_alpha
 = X^w R_a(K') + X^(g+d(p,alpha)).                 (S3a)
```

If `alpha` is a leaf of both `K` and `H`, put `H'=H-alpha`.  Then

```text
D_alpha
 = X^w R_a(K')
   +X^(g+d(p,alpha))
   +X^(h+d(r,alpha)).                              (S3b)
```

Thus a one-leaf same-state peel is possible only if the rooted-depth factor
in (S3a) fills a terminal interval with one omitted singleton, or the factor
in (S3b) fills one with two omitted singletons.  A generic endpoint peel adds
a third rooted factor; it does not preserve the two-root state.

The unconditional version is false even on the known `L6` control.  In the
FW261 orientation

```text
Q=4, M=11, K={0,1,3,4}, H={3}.
```

The admissible leaf deletions have deleted supports

```text
{1}:   {1,3,6,10},
{4}:   {4,9,10,11},
{1,4}: {1,3,4,6,9,10,11},
```

none of which is a terminal interval.  Therefore any large-order theorem
must use additional owner locality; defect density alone is insufficient.

## 3. The strict terminal-annulus target is impossible

The first proposed target was to find a leaf set `S`, with
`1<=|S|<=2`, such that

```text
K'=K-S and H'=H-S are connected,
p,r not in S,
D_S=(F_K-F_K')
    +(X^g R_p(K)-X^g R_p(K'))
    +(X^h R_r(H)-X^h R_r(H'))
    =I_[M'+1,M]
```

for some `M'<M`.  Coefficientwise subtraction would then give

```text
I_M' = F_K' + X^g R_p(K') + X^h R_r(H'),           (S4)
```

with no third external factor and `|K'|<|K|`.

FW263 proves that this is impossible throughout the target range, independent
of owner locality.  At least one vertex `alpha` of such an `S` is already a
leaf of `K`; because `p,r` are retained, it is a leaf of `T`.  If its edge has
weight `w`, then `T-alpha` is an order-`n-1` positive-integer
distinct-distance tree, whence

```text
w <= N-ceil(binomial(n-1,2)/2).                    (S5)
```

The deleted polynomial has at most `2n-3` coefficients.  Since
`M=N-Q` and `Q<=n-2`, a terminal deleted interval would begin at least at
`N-3n+6`.  For `n>=14`,

```text
N-ceil(binomial(n-1,2)/2) < N-3n+6,
```

so the leaf-edge coefficient `w` lies strictly below that interval.  Thus
(S4) cannot occur for any hypothetical G18 candidate.  The verifier checks
999,870 exact arithmetic rows through order 100,000, the complete `L6`
obstruction, and inherits all five A/B witness controls.

This is an **OBSERVED route obstruction**, not an order exclusion.  Every
valid next recurrence must retain or reroot the deleted incident factor; it
cannot make that factor disappear into one high terminal suffix.

## 4. Fixed-core singleton ledger retains three labels

Fix a true `T`-leaf `alpha in K\{p,r}`, put `K'=K-{alpha}`, and require each
external block to be a singleton-boundary class labelled by an original
`T`-pair.  FW264 tests this smallest rerooting escape from FW263.  Put
`C=binomial(k,2)=binomial(n-2,2)`.  The global true-leaf radius bound applies
to the old endpoint edges `g,h` and to the peeled core-leaf edge `w`; for
`n>=10`,

```text
g,h,w < C.                                         (S6)
```

The stipulated next prefix on this fixed order-`k-1` core has length
`C+|H'|` and therefore contains every coefficient up through `C`.  The
actual-pair owners of `h` and `w` used the deleted old endpoint and leaf.
Global uniqueness forbids a different retained pair from re-owning either
value.  Consequently the three labels `zp,xr,alpha-a` must remain active.
The latter two may be order-one ghosts; FW264 does not force retention of
three full algebraic rooted factors.

This is an **OBSERVED owner-provenance obstruction** in the stated ledger.
Multi-vertex or fragmented cap bundling, arbitrary nonactual translates and
core exchange placing `x` or `alpha` into the next internal core are outside
scope.

## 5. Alternate target: trunk-cut provenance

FW259 locates a weighted trunk segment from `h` to the first giant-child LCA;
it does not locate a particular edge or bound either side order.  Choose an
edge `e=ab` on that segment and write `K=A union_e B`, with `B` on the crown
side.  The internal cross-pair polynomial has the exact product form

```text
X^w R_a(A) R_b(B).                                  (S7)
```

Owner-expanded on the `B` side, this is

```text
sum_(u in A) X^(w+d_A(a,u)) R_b(B),                 (S8)
```

so it contains `|A|` distinct, pairwise-disjoint boundary translates.  The
old `z` and `x` factors can contribute up to two further translates.  Calling
(S7) one formal product factor would hide this unbounded cap order.

**UNVERIFIED target B.**  Retain the owner provenance of (S7) together with
the restrictions of both rooted factors in (S1).  Prove either

1. two named translates overlap, giving a repeated distance; or
2. the `A` shift set is forced to be a bounded complete cap and an initial
   interval is supplied by `F_B` and at most two owner-expanded boundary-root
   factors, giving an FW261-type state on `B`.

Only after the owner-expanded bound in the second outcome is proved would the
strict measure

```text
(core order, boundary-factor count),
```

be valid, because `|B|<|K|` and the factor count would remain at most two.
FW259 currently gives no bound on `|A|`, `R_a(A)` or its shift starts.

FW265 verifies (S7)--(S8) for arbitrary weighted-tree cuts and makes the
support statement precise.  Under global distance uniqueness, `F_A`, `F_B`
and the whole cross class are pairwise disjoint; the named shifts inside the
cross class are pairwise disjoint; equivalently the refined family
`{F_A,F_B} union {S_u:u in A}` is pairwise support-disjoint.  It follows only
that the unexpanded formal factor count does not by itself certify a bounded
owner-expanded state.  FW265 does not connect the arbitrary cut to FW259,
prove that `|A|>2`, or prove any shift meets the retained prefix.

## 6. Hard stop

Stop this q=1 route if any of the following survives a tree-realised pressure
test carrying LCA provenance, cross-Sidon, full-support orientations and the
moment/Kruskal constraints:

- terminal owners occupy an unbounded number of branches;
- every peel necessarily grows the external-factor ledger;
- the FW259 internal/parent carriers absorb both slack gaps at all scales;
- target B does not yield a coefficientwise smaller state with bounded
  boundary context;
- the only new conclusions are density, span, trunk-length or heavy-edge
  lower bounds.

The sprint stops here.  FW263 eliminates strict terminal absorption, FW264
retains three singleton labels in the fixed-core ledger, and FW265 exposes
the uncontrolled `|A|` owner expansion of a trunk cut.  Target B remains
mathematically **UNVERIFIED**, but the current inputs provide neither its
prefix-locality premise nor a well-founded owner-expanded measure.  Restart
requires a genuinely new bounded-cap, prefix-absorption or core-exchange
lemma; adding compatible constants does not qualify.

### Successor audit

The subsequently authorised Max audit is recorded in
`docs/q1-new-mechanism-sprint.md`.  It adds the **OBSERVED FW266 top-band
core-exchange obstruction** and **OBSERVED FW267 near-full external-owner
conservation theorem**.  The same/lower-prefix exchange requires at least
`Q` external vertices; raising to the canonical near-full prefix recovers
FW242 and preserves every accumulated external vertex in actual-pair owner
support.  No bounded recurrence or order exclusion resulted.  The updated
stop boundary is FW267; the hashes below remain the historical frozen
baseline of this earlier sprint.

## 7. Frozen baseline hashes

The repository baseline commit and current independent closure-artifact
hashes are

```text
HEAD                                      6eb04cacf191095f996aa1d12cc8f0a2a8bfa89d
FW261 verifier                            dece3c2e00cf5cb4fdbacb672f42201b4c2d31770fdd53cabf53880e49847beb
FW261 certificate                         8edf4228ce4f106f7679c4875567ade23a99e2bf94c819119192c0a779c2ba58
FW262 verifier                            6ba64464600f2e7e9ac36740c46bd0a71e95b134cb6450e55a19a05487633423
FW262 certificate                         f45f20c5a80cf36ebe1064ad96eececd5f525d4a4a4a2a2bfda967c434591f43
FW263 verifier                            0a7d138496ae3d9774ae872b96175bcca8809784c4b9a91a1481cbbd0539cb1a
FW263 certificate                         e4e497a19964dc631db9bfe2d936f1d59d1fdb80d761afd9040e9be48cfbda52
FW264 verifier                            13c9732ff41b2e1f90353284de00e8d86bc7a87a534f13fe8254151646f709bb
FW264 certificate                         df647faa14dbbbdc74ed7541ccbc7d4f268cba54471b2750737fc1c9ae9d9fbe
FW265 verifier                            3de09eaae76c0cc25ded7fbbb87af66be51796d81ebdd0c127799afa083e13ce
FW265 certificate                         c87613f06a26c671f1620ff9815bf3c4c688bdca13f18a6292235b3dd31cb6b2
```

The FW258 scope correction may change its own verifier/certificate and parent
hashes downstream from FW258.  It does not alter the independent direct
FW261--FW262 chain.
