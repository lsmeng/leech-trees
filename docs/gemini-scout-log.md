# Gemini mathematical scout experiment log

Gemini is used only for fast speculative exploration. No Gemini statement is
promoted to proved or certified without independent derivation or computation.

## Trial 1 — FW312/FW313 paired reception and top strip

**Model/mode:** Gemini Flash Extended (user-designated Gemini 3.7 Flash).

**Exact task sent:** Given the certified FW309--FW312 remote-carrier state,
the four FW311 complementary root holes, the nine paired-owner colors and
three cross--cross rectangles, plus the provisional 46-row small-order
top-strip enumeration, (A) seek an exclusion or sharper classification of the
top-strip rows using named owners, directness, endpoints/LCA and the cap;
(B) propose several different attacks on large-order Paired Reception
Exclusion; and (C) actively seek counterexamples to tempting local
implications. The response was required to separate rigorous deductions,
candidate lemmas, possible counterexamples/gaps, and the best micro-target.

**Approximate usefulness:** high for a short scouting round; one concrete
enumeration defect was found before commit.

**Classification and audit:**

- GEMINI_CANDIDATE_LEMMA: apply the FW311 gate-forbidden table to both
  complementary lengths, not only to the chosen smaller one.
  **Independent result:** correct. FW311 explicitly applies the table to both
  c_alpha,c_beta. Recomputing FW313 reduced the provisional 46 rows to 41
  (23 at order 27). Integrated into the verifier and certificate.
- GEMINI_POSSIBLE_GAP: an L-internal pair owner need not be a gate-rooted
  depth in B. **Independent result:** correct but already part of the
  FW311/FW312 trust boundary; it prevents a false shortcut.
- GEMINI_USEFUL_REFORMULATION: the four non-P_2 top-strip owners are
  entirely on the L/cap side of the remote carrier. **Independent result:**
  correct, but it restates the named-owner handoff rather than excluding a
  row.
- GEMINI_POSSIBLE_COUNTEREXAMPLE: proposed switch data
  w=5,r=1,r'=7,b=6,b'=0. **Independent result:** invalid; it gives
  x+y=0, not 4, and the alleged t+4 distance equals t.
- Other proposed switch and monotone lemmas were conditional restatements of
  directness and did not supply the missing membership in (Q-Q)_+.
  One displayed d_6 fixed-core difference set also omitted the value 6.

**New idea survived verification:** yes — the symmetric forbidden-value
filter.

**Claimed proof gap/error rate:** substantial; several later claims were
tautological or arithmetically wrong.

**Real counterexample found:** no.

**Saved expensive reasoning:** yes. It caught a concrete left-side
enumeration omission immediately, before the FW313 commit.

**Routing implication after trial 1:** Flash is useful for adversarial review
of fresh finite reductions and for generating micro-targets. Every numerical
or set-theoretic claim still needs line-by-line or computational checking.

## Trial 2 — corrected 41-row top-strip closure attempt

**Exact task sent:** After reporting the verified symmetric-forbidden filter
and correcting the invalid switch arithmetic, attack only the 41 remaining
rows. Derive a new necessary condition, exclude a genuine subset, or build a
valid local countermodel; avoid conditional restatements and check every
distance equation.

**Gemini claim:** all 41 rows are impossible.

**Classification:** GEMINI_POSSIBLE_GAP, rejected.

**Earliest failed step:** the response treated the FW311 arm lengths
`alpha,beta`, measured from an internal split/LCA vertex of the remote path,
as rooted endpoint depths from `b_1`. It therefore asserted
`r_endpoint=alpha-a-w` without justification. The resulting claimed
contradiction to a J-internal remote owner actually contradicts the certified
setup and invalidates every later row elimination.

**New idea survived verification:** no.

**Real counterexample found:** no.

**Usefulness:** moderate as a calibration result. The failure mode is now
specific: Flash readily loses the base point of rooted distances and arm
lengths in nested tree decompositions.

**Routing implication after trial 2:** use Flash for finite-list auditing and
counterexample search, but do not assign it a nested-LCA proof unless the
basepoint of every distance variable is restated and checked explicitly.

## Trial 3 — local-model challenge after the rooted-depth correction

**Exact task sent:** Accept the failure of the Trial 2 rooted-depth identity.
Either construct a genuinely valid local carrier model for one of the 41 rows,
with every basepoint and directness set explicit, or report no progress.

**Gemini output:** for the row
`(g,h_0,s,t-s,c,c_other)=(d_6,2,28,-4,10,16)`, it proposed the
fixed rooted set `B_{d_6}={0,6,13,14,15,23}`, a remote split with arm
lengths 5 and 25, and the cap-root depths 42 and 46.  It checked
`{5,20,25} \cap (Q-Q)_+=empty` for
`Q=B_{d_6} union {42,46}` and kept all four FW311 root holes open.

**Classification:** GEMINI_USEFUL_REFORMULATION / GEMINI_CANDIDATE_LEMMA,
not a counterexample and not an exclusion.

**Independent audit:** the displayed arithmetic is internally consistent:
`10+16=26=s-h_0`, `a+c=24=t`, `t+4=28=s`, both complementary
lengths avoid the certified `d_6` forbidden set `{1,5,9}`, and the two
displayed positive-difference sets are disjoint.  Thus the already-certified
local hole/directness conditions do not by themselves contradict this row.

However, the construction is only an abstract two-set carrier model.  It
does not build the complete weighted tree, check distinct edge weights and
all cross distances, or realize the full interval spectrum.  In particular,
the suggested arm length 5 must be reconciled with the fixed core before it
could define a valid partial Leech witness.  Calling it a
`VALID_COUNTERMODEL` therefore overstates what was established.

**New idea survived verification:** only the narrower obstruction statement:
an exclusion of the 41 rows must use more than the present root holes and the
single `(R-R)_+ cap (Q-Q)_+` directness test.

**Real counterexample found:** no.

**Best next micro-target after audit:** test the 41 rows against the full
named-owner geometry (including all cross distances and edge-label
injectivity), not merely arbitrary partitions of the remote path length.

## Trial 4 — X-containing owner modes after FW314

**Exact task sent:** seek a new obstruction in X-containing complementary
owner modes using the cross equations, endpoint-relative holes, root
shift-four exclusion, and complete low coverage.

**Gemini claims:** it asserted that a shared J endpoint and many switch
shifts are impossible, proposed a collinear-J restriction, and displayed an
abstract monotone `(3,1)` model.

**Classification:** GEMINI_POSSIBLE_GAP with one
GEMINI_CANDIDATE_LEMMA; most claimed exclusions were rejected.

**Earliest failures:**

- The L endpoint depths `b,b'` are arbitrary `g`-rooted depths in the full
  factor `B`, not differences between fixed-core vertices.  The fixed-core
  difference table therefore cannot enumerate `y=b'-b`.
- `D intersect (D+4)=empty` concerns `b_1`-root depths in the global factor
  `A union X^(a+w)R`; it cannot be applied directly to arbitrary
  `g`-root depths in `B`.  Thus the proposed shared-J exclusion was invalid.
- The displayed local model reused edge weight one from the fixed core and
  did not check all unordered pair distances, so it was not an actual
  distance-injective pressure control.

**Surviving candidate:** if the two J endpoints of a cross--cross rectangle
are ancestor/descendant in the tree rooted at `u`, their mutual distance is
`|x|`.  Hence `|x|` cannot equal a distance already owned by the fixed core.
This is a correct elementary conditional restriction, but it excludes only
the collinear realization, not the cross mode.

## Trial 5 — corrected collinear-J audit

**Exact task sent:** discard the false fixed-core enumeration and audit only
the collinear-J observation, including its earliest hidden assumption.

**Gemini result:** correctly separated the collinear and branched cases.  If
`|x|` is in the fixed-core spectrum
`{1,2,3,6,7,8,9,10,11,12,13,14,15,17,23}`, the two J endpoints must have a
strict LCA below neither endpoint.  With branch arms `l_1,l_2`,

```text
|l_2-l_1|=|x|,
d_J(u_1,u_2)=l_1+l_2=|x|+2 min(l_1,l_2).
```

The four cross-corner distances are unchanged by this branching.

**Classification:** GEMINI_USEFUL_REFORMULATION, independently accepted as
an elementary conditional LCA restriction.  It does not exclude any complete
owner mode and has not been promoted to a separate certified theorem.

**Real counterexample found:** no.

**Routing implication:** the next rigorous round should ask whether the
branched monotone `(3,1)` case can satisfy directness and the global cap; it
must not repeat the invalid assumption that arbitrary `B` depths are fixed
core depths.

## Trial 6 — reflected low-value ownership after FW314

**Exact task sent:** rank five possible routes for the X-containing
complementary-owner modes, derive the forced cross distances, try to build a
local countermodel, list hidden assumptions, and identify one smallest
rigorous successor question.

**Gemini output:** it correctly rewrote the endpoint-relative forbidden
depths for a cross owner `c=w+b+r`, `delta=s-c`, `eta=s-w` as

```text
b+delta   = eta-r,       r+delta   = eta-b,
b+delta+4 = eta+4-r,     r+delta+4 = eta+4-b.
```

It also restated the exact conditional contradiction: membership of either
unshifted reflected depth in its corresponding rooted factor gives a second
cross realization of `s`, and the `+4` version gives one of `s+4`.

**Classification:** `GEMINI_USEFUL_REFORMULATION`, with the proposed
exclusions and countermodel rejected.

**Earliest failures:**

- The claimed density and additive-energy consequences do not follow from
  the displayed rooted holes.  Neither rooted factor is an interval or a
  dense subset of its span.
- The proposed finite sets `B,R` are not an actual weighted tree, do not
  implement the fixed core, and do not check all pair distances, the exact
  order cap, or the complete punctured spectrum.  Their cardinalities cannot
  be substituted into the Leech order cap.
- The suggested five-value exact-cover test is much weaker than the live
  all-order hypothesis and cannot exclude an owner mode.

**Independent audit:** the four reflected identities and their conditional
collision interpretation are already exactly the FW314 endpoint-relative
holes in different notation.  Complete low ownership supplies pair owners
of the reflected values when they lie in range, but it does not place those
owners at the carrier gate or turn a distance value into a rooted depth.

**Real counterexample found:** no.

**Routing implication:** retain the reflected-value notation only as a clean
target for the rigorous ownership-incidence audit.  Do not use Gemini's
density, modulo-four, or toy-cardinality arguments.
