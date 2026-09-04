# Double-end (two-anchor) normal form for Leech trees

Derived from scratch 2026-09-02 (Fable).  Nothing here depends on the earlier
S1 / FW303 programme.  Everything below is elementary and is checked
numerically by `validate_double_end.py` (small orders) and by the independent
brute force in `brute_leech_small.py`.

## 1. Setup

Let `T` be a Leech tree of order `n`, `N = C(n,2)`, so the `N` pairwise
distances are exactly `1,...,N`.  Let `(a,b)` be the (necessarily unique) pair
with `d(a,b) = N`.  Being a diametral pair, `a` and `b` are leaves; let `P` be
the `a`-`b` path, of length `N`.

For a vertex `u` write `p(u)` for the position on `P` of the foot of `u`
(distance from `a` along `P`) and `h(u)` for the distance from `u` to `P`.
Then `d(a,u) = p + h` and `d(b,u) = (N-p) + h`.

**Gap coordinates.**  For `u` outside `{a,b}` set

    e(u) = N - d(a,u),      f(u) = N - d(b,u).

Then

    p(u) = (N + f - e)/2,   h(u) = (N - e - f)/2.

Immediate consequences (`V := n-2` non-anchor vertices):

* `1 <= e,f <= N-1`;
* `e + f = N (mod 2)` and `e + f <= N` (because `h >= 0`).  NOTE: this is
  **not** `e = f (mod 2)`; the two coincide only when `N` is even.  An earlier
  draft of this file stated the wrong form; it was caught by the independent
  brute force, which found it false at n=3 and n=6 (N odd) and true at n=4
  (N even).  The code has always used the correct form `(e+f) % 2 == N % 2`;
* the values `N-e` are `V` distinct distances `d(a,u)` and the `N-f` are the
  `V` distinct `d(b,u)`; no `d(a,u)` equals a `d(b,v)` (different pairs), so
  **`E = {e(u)}` and `F = {f(u)}` are disjoint `V`-sets**.  In particular
  `e(u) != f(u)`, i.e. no vertex sits at `p = N/2`.

## 2. The gap of a pair, without any ordering

For `u,v` outside `{a,b}`:

* if `p(u) != p(v)` then `d(u,v) = h(u) + h(v) + |p(u) - p(v)|`;
* if `p(u) = p(v)` then `d(u,v) = h(u) + h(v) - 2 h_c` where `h_c >= 0` is the
  height above `P` of the meeting point of `u` and `v` (`h_c = 0` iff they
  hang in different branches at that point of `P`).

Substituting the coordinates, with `gap(x,y) := N - d(x,y)`:

    gap(a,b) = 0,   gap(a,u) = e(u),   gap(b,u) = f(u),

**Lemma A.**  For non-anchor `u,v`,

    gap(u,v) = min( f(u) + e(v),  f(v) + e(u) ) + 2 h_c(u,v),

with `h_c = 0` unless `f(u) - e(u) = f(v) - e(v)` (i.e. `p(u) = p(v)`), in
which case `0 <= h_c <= min(h(u),h(v))`.

*Proof.*  `p(u) <= p(v)` iff `f(u) - e(u) <= f(v) - e(v)` iff
`f(u) + e(v) <= f(v) + e(u)`.  For `p(u) < p(v)` a direct substitution gives
`d(u,v) = N - f(u) - e(v)`, and the two crossings are then unequal with
`f(u)+e(v)` the smaller.  For `p(u) = p(v)` the two crossings are equal and
`d = h(u)+h(v)-2h_c = N - (f(u)+e(v)) - 2h_c`. ∎

**Theorem B (double-end normal form).**  `T` is a Leech tree of order `n` iff
the `V` pairs `(e(u),f(u))` satisfy the constraints of §1 and

    {0}  ⊔  E  ⊔  F  ⊔  { gap(u,v) : u<v }   =   [0, N-1],

all `1 + V + V + C(V,2) = N` values distinct.

## 3. First consequences

**Parity split.**  `h_c` shifts by an even amount, so parities are decided by
the types of the vertices: call `u` *even* if `e,f` are both even, *odd*
otherwise; let `α` = #even, `β` = #odd, `α+β = V`.  Counting even and odd
gaps,

    even:  1 + 2α + C(α,2) + C(β,2)  =  #{even values in [0,N-1]},
    odd:   2β + αβ                   =  #{odd values in [0,N-1]}.

For `n = 25` (`N = 300`, `V = 23`) both equations reduce to `β(25-β) = 150`,
so `β ∈ {10,15}`, i.e. `(α,β) ∈ {(13,10),(8,15)}`.  This recovers Taylor's
parity obstruction inside the double-end picture and pins the split exactly.

**Attachment lemma (R1).**  If `h(u) > 0` then the branch containing `u` is
attached to `P` at a vertex of `T` with the same `p` and height `0`; hence
there is a vertex `w` with `e(w) + f(w) = N` and `f(w) - e(w) = f(u) - e(u)`.

**Cross-Sidon condition.**  All `C(V,2)` values `gap(u,v)` are distinct.  For
untied pairs this says: there are no four vertices with
`f(u) - f(u') = e(v') - e(v) != 0` and the corresponding orderings, i.e. the
positive difference sets of `E` and of `F` must be almost disjoint.

## 4. Why this is a good search order

Every `e` and every `f` is itself a gap.  Process gaps `g = 1,2,...,N-1` in
increasing order and maintain the invariant that all gaps `< g` are realised.

*Determination lemma.*  Suppose all coordinates with value `< g` are known.
Two different invariants are in force at two different moments, and the
distinction matters:

* while the step for gap `g` is being *decided*, every unassigned coordinate is
  `>= g` (the coordinate about to be assigned may itself equal `g`), so a
  crossing with one unknown coordinate is `>= 1 + g = g+1`;
* immediately *after* a coordinate has been assigned the value `g`, every
  remaining unassigned coordinate is `> g`, so such a crossing is `>= g+2`.

The implementation uses `lo = g` in `rescan` and `lb_prune` and `lo = g+1`
inside `assign`, matching the two cases.  The test for determination is never
against a fixed threshold but against the *computed* lower bound `Y-` of the
other crossing:

* if both crossings are known: the gap is `min` of them, plus `2h_c` if tied;
* if exactly one crossing `X` is known and `X < Y-`: the gap equals `X`;
* otherwise the gap is `> g`.

An earlier draft of this file wrote the threshold as the constant `g+2`, which
would be unsound at the decision moment when a coordinate equals `g`; the code
does not do this.

Consequently **the smallest unrealised gap `g` must be realised either by
assigning `g` as an `e`- or `f`-coordinate of some vertex, or by resolving a
previously deferred tied pair.**  Vertices may be created with only one
coordinate known; the partner is filled in later at its own gap step.  This
gives a search of depth exactly `2V` decisions (the coordinate gaps), all
other gaps being forced.

## 5. A covering lemma

Put `A(x) = Σ_i x^{e_i}`, `B(x) = Σ_i x^{f_i}`, `H(x) = Σ_i x^{e_i+f_i}`.  For an
unordered pair `{i,j}` the two crossings `f_i+e_j` and `f_j+e_i` are the
minimum `m_ij = gap - 2h_c` and the maximum `M_ij`, and
`m_ij + M_ij = (e_i+f_i) + (e_j+f_j)`.  Expanding `A·B` by the pair and using
the tiling identity `1 + A + B + Σ x^{gap} = 1 + x + ... + x^{N-1}` gives

**Lemma D.**
    (A+1)(B+1) = (1 + x + ... + x^{N-1}) + H + Σ_{pairs} x^{M_ij}
                 + Σ_{tied pairs with h_c>0} ( x^{m_ij} - x^{m_ij + 2h_c} ).

Every term other than the last is non-negative, and the last subtracts at most
1 from any single coefficient because the gaps are distinct.  Hence:

**Corollary (covering).**  With `E' = E ∪ {0}` and `F' = F ∪ {0}`, every
`w ∈ [0, N-1]` is representable as `e + f` with `e ∈ E'`, `f ∈ F'`, except
possibly the gaps realised by a tied pair with `h_c > 0`.

**CAVEAT (checked 2026-09-02).**  The covering corollary is a tautology, not
a new constraint: a gap `w` realised by an untied pair already *is* `f_u+e_v`,
so it is representable by construction, and the same holds in a partial state
because both of those coordinates are `< w`.  Implementing it as a prune
(`cover_ok`) changed the n=9 node count by exactly zero, which is the expected
outcome and is recorded here so nobody mistakes it for a live constraint.  The
non-trivial content of Lemma D is the *multiplicity* statement: the number of
representations of `w` in `E' + F'` equals `1 + #{i : e_i+f_i = w} +
#{pairs : M_ij = w}` up to the tie correction, so the sumset multiplicities
read off the heights and the maximal crossings.  Since `|E'| = |F'| = V+1`
and `(V+1)^2 = N + V + C(V,2)`, the total excess is exactly `V + C(V,2)`.

Counting the sums that reach `N` gives, with `k` = number of on-path vertices,
    #{(e,f) ∈ E×F : e+f >= N}  =  k + #{pairs : |p_i - p_j| >= h_i + h_j}.

## 6. Two more elementary bounds

*Golomb.*  The vertices of `T` lying on `P`, together with `a` and `b`, have
all pairwise distances distinct, so their positions form a Golomb ruler of
length `N`.  Using the known optimal-Golomb-ruler lengths, `N = 300` admits at
most 20 marks, so at most 18 of the 23 non-anchor vertices lie on `P` and at
least 5 hang off it.  (This uses the published OGR values, a finite computation
we do not re-verify here.)

*Balls.*  If `B` is any ball of radius `D` in `T` then all `C(|B|,2)` distances
inside it are distinct and at most `2D`, so `C(|B|,2) <= 2D`.  Applied at `a`:
at most `(1+sqrt(1+16D))/2 - 1` vertices satisfy `e >= N - D`.

## 7. Status of the implementation

`double_end_search.py` is the reference gap-order engine;
`brute_double_end.py` is an independent vertex-order enumerator of the pure
relaxation, and `differential_test.py` compares them with every optional prune
switched off.  They agree exactly for `n = 3, 4, 6`.  At `n = 6` the relaxation
has **12 distinct coordinate systems `(E,F)`**, which is what the differential
compares; the engine prints **16** raw solutions there because a tied pair with
more than one admissible `h_c` yields several records with the same `(E,F)`.
Both numbers are correct and must not be conflated.  With all prunes on, the engine returns exactly the genuine Leech
trees for `n = 3, 4, 6` (verified by rebuilding the tree and doing BFS), and
exhausts `n = 9` with no solutions.  Symmetry breaking (gap 1 is always a
coordinate, and `a`/`b` may be swapped, so `1 ∈ E` may be assumed) halves the
search exactly.

Three real bugs were found and fixed during validation and are recorded here
because they invalidate any earlier numbers: an unsound `hc_heights` that
required the meeting vertex to already exist; an unstable index in the
deferred-pair loop; and, most importantly, the fact that an undetermined pair
becomes determined as `g` grows even with no new assignment, which requires a
rescan at every gap step.


## 8. What each prune is actually worth (n = 9, sound versions only)

| prune | n=9 nodes with it off |
|---|---|
| all on | 24,335 |
| no upper-bound Hall (`ub_prune`) | 67,432 before the ancestor condition; 62,612 with it |
| no covering (`cover_ok`) | 24,335 -- no effect, see the caveat in §5 |

The single largest structural gain came from the last condition added to
`ultrametric_ok`: inside one p-class the heights are automatically distinct
(same p and same height forces the same (e,f)), so a meeting height `h_c > 0`
identifies a *unique* class vertex, which must then be an ancestor of both
endpoints.  That took n=9 from 62,612 to 24,335 nodes.

## 9. Two things that did NOT help (recorded so they are not retried)

*Domain forward checking.*  For each half-known vertex, filtering its partner
domain by tentatively assigning each candidate and rejecting those that would
immediately duplicate a gap or violate the attachment lemma, then running the
Hall condition on the filtered domains.  Prototyped in full; n=9 went from
24,335 to 24,170 nodes, a 0.7% gain for a 30% slowdown.  The existing prunes
already capture essentially all of it.

*The covering prune.*  See the caveat in §5: exactly zero effect, as the
tautology argument predicts.

Note also, for anyone sharding the restricted runs: with `--force-e-upto S` the
first `S` gap steps have exactly one option each (only "new vertex with e = g"
is legal, since every existing vertex already has its e set and f-options are
forbidden), so the search is a forced chain down to level `S`.  Splitting at a
level below `S` puts the entire search in shard 0 and leaves every other shard
with only the prefix.

Measured for `n = 25, S = 15`: shard 1 of 1000 at levels 13 and 14 is
EXHAUSTED after 14 and 15 nodes respectively (the prefix only, so those levels
hold a single node), while at level 15 and beyond the same shard is still
running after millions of nodes.  The forced chain is therefore exactly the
`S` steps the restriction implies, and the first free decision is at gap
`S+1`; there is no extra forcing beyond it.

**Methodological warning.**  The per-depth histogram printed by `--debug` after
a run that stopped at a node limit does NOT establish that a level is forced.
Depth-first search descends before it backtracks, so a shallow level shows a
count of 1 simply because its remaining siblings have not been reached.  An
early reading of such a histogram suggested a 24-step forced chain and an
arithmetic pattern (`E` continuing 18, 36, 54, ... and `F` continuing 16, 32,
48, ...); the shard test above and an exhaustive small-order run
(`n = 9, S = 5`: depths 0-5 hold one node each, first branching at depth 6)
both refute it.  That pattern is the first depth-first path, nothing more.
Only an exhaustive run, or a shard test of the kind above, decides forcedness.  Split deeper than `S`, or not at all.

## 10. Why the restricted case (diam(T-a) <= N-16) is so rigid

This explains the shape of the `--force-e-upto 15` search at `n = 25` and is
worth stating on its own.

**Lemma E.**  Let `T` be a Leech tree of order 25 with `diam(T-a) <= 284`.
Then the sixteen largest distances `285, 286, ..., 300` are *all* realised by
pairs containing `a`.  Writing `W` for the sixteen vertices `u` with
`d(a,u) >= 285`, the map `u |-> d(a,u)` is a bijection from `W` onto
`{285,...,300}`, and every pair not containing `a` has distance `<= 284`.

*Proof.*  A pair avoiding `a` has distance at most `diam(T-a) <= 284`.  There
are exactly 16 distances in `[285,300]` and `a` has 24 distances to the other
vertices, so 16 of those are `285,...,300`. ∎

In gap coordinates this is exactly `E ⊇ {1,...,15}` together with `0` for the
pair `(a,b)`; `b ∈ W` since `d(a,b) = 300`.

**Consequence (crowding with consecutive labels).**  Put `α_u = d(a,u)` for
`u ∈ W` and write `α_u = 284 + i_u`, so that `i` is a *bijection* `W -> [1,16]`.
For `u,v ∈ W`,
    d(u,v) = α_u + α_v - 2 μ_uv = 568 + i_u + i_v - 2 μ_uv,
where `μ_uv = d(a, m)` and `m` is the median of `a,u,v`, necessarily a vertex
of `T`.  Grouping the `C(16,2) = 120` pairs by their median, inside one group
the distance is a constant plus `i_u + i_v`, so the sums `i_u + i_v` must be
pairwise distinct there; a set of labels drawn from `[1,16]` admits at most
`2·16 - 3 = 29` distinct pairwise sums.  Hence each median carries at most 29
pairs, and at a median whose children below it hold `n_1, ..., n_t` members of
`W` we need `Σ_{i<j} n_i n_j <= 29`.  At the top, `t` parts summing to 16 must
satisfy `Σ n_i^2 >= 198`, which allows only `{15,1}`, `{14,2}` and `{14,1,1}`.
The same bound applied to a two-part split of `m` members reads
`p (m - p) <= 29`, so **the forcing is confined to the top of the hierarchy**:

| members `m` still below the split | largest part that can be peeled off |
|---|---|
| 16, 15, 14, 13 | 2 |
| 12 | 3 |
| 11 | 4 |
| <= 10 | no constraint from this bound |

So the first four splits are caterpillar-like and after that the argument stops
biting.  (An earlier draft of this section claimed a caterpillar all the way
down; that is false, and the table is the correct statement.)  Moreover
`d(u,v) <= 284` forces
`μ_uv >= (285+286-284)/2`, i.e. `μ_uv >= 144`, so every median is a vertex `x`
with `e(x) <= 156`.

This is the top-block crowding phenomenon of the delta-indexed programme,
recovered inside the two-anchor picture, and in a sharper form: there the top
block was a block of consecutive *depths*, here the labels `i_u` are forced to
be exactly the interval `[1,16]`.  It is why the restricted search is far
cheaper than the unrestricted one.  It is **not**, by itself, a contradiction:
`120 <= 15 x 29` and enough medians are available, so the restricted case still
has to be decided by search.  Whether the caterpillar constraint plus the
`μ >= 144` bound plus the requirement that the medians be distinct vertices of
`T` can be pushed to a contradiction by hand is open, and is the most promising
route to replacing the whole delta = 279..284 certificate chain with a proof.

### 10.1 A sum condition on the medians

Keep the notation of Lemma E.  Summing `d(u,v) = α_u + α_v - 2 μ_uv` over the
`120` pairs inside `W` gives `Σ d = 70200 - 2 Σ μ`.  Those 120 distances are
distinct integers in `[1,284]`, so `Σ d <= 165 + 166 + ... + 284 = 26940`, and
therefore

    Σ_{u<v in W} μ_uv  >=  21630,

a weighted average median depth of at least `180.25`.  This is much stronger
than the pointwise bound `μ >= 144`, which alone yields only `17280`.  The
matching upper bound is `Σ μ <= Σ min(α_u,α_v) = 34760`, so the condition is
restrictive but not yet contradictory.

Two further handles, both unexploited:

* Let `x_0` be the vertex where the 16 paths `a -> u` first diverge, at depth
  `μ_0 = d(a,x_0)`.  If `x_0 ∉ W` then `d(x_0,u) = α_u - μ_0` for every
  `u ∈ W`, so **`x_0` has sixteen of its distances forming a complete run of
  sixteen consecutive integers**, contained in `[1, 156]`.  If instead
  `x_0 ∈ W` then `x_0` is the member with `α = 285` and the fifteen distances
  `d(x_0,u)` are exactly `1,...,15`.
* Under a one-at-a-time peeling with medians `μ_1 < ... < μ_15`, the sum
  condition reads `Σ_k μ_k (16-k) >= 21630`; with minimal spacing
  `μ_k = c + k - 1` this forces `c >= 176`, i.e. the first branch point would
  have to sit at depth at least `176`, well above the pointwise bound `144`.
  (This is a calculation under an assumed peeling pattern, not a proof.)

Closing the gap between `21630` and `34760` using the requirement that the
medians be distinct vertices of `T` with distinct depths, together with the
caterpillar table, is the concrete open problem here.

### 10.2 A depth bound on common ancestors

Still in the setting of Lemma E.  Let `x` be any vertex at depth `μ = d(a,x)`
with `m` members of `W` strictly below it.  Every one of the `C(m+1,2)`
distances inside `{x} ∪ (W below x)` is a distinct positive integer, and each
is at most `α' + α'' - 2μ` where `α' > α''` are the two largest `α`-values
below `x`; in particular at most `599 - 2μ`.  Hence

    C(m+1,2) <= 599 - 2μ,     i.e.    μ <= (599 - C(m+1,2)) / 2.

| `m` | 16 | 15 | 14 | 12 | 10 | 8 | 5 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|
| `μ <=` | 231 | 239 | 247 | 260 | 272 | 281 | 292 | 296 | 298 |

So the vertex where the sixteen paths `a -> u` first diverge sits at depth at
most `231`.  The same inequality rules out the extreme configuration in which
some `x_0 ∈ W` is an ancestor of the other fifteen: there `d(x_0,u) = 1,...,15`
and every one of the `C(15,2) = 105` remaining pairs has distance at most
`15 + 14 = 29`, leaving only `29 - 15 = 14` unused values for `105` pairs.

Combining §10.1 and §10.2 constrains the median depths from both sides, but the
two are still compatible: maximising `Σ μ = Σ_e w_e C(n_e,2)` subject to
`Σ_e w_e n_e = Σ_u α_u = 4680`, to the nesting of the subtrees `S_n` (edges
with at least `n` members of `W` below), and to the depth bound above, gives
about `32500`, comfortably above the required `21630`.  A contradiction, if
there is one, needs a further ingredient.
