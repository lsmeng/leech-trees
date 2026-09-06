# Route review for order 25 — is there a better idea than the fourteen finite cases?

- Date: 2026-09-05
- Author: Fable 5.1 (this session), answering `docs/INSPECTION-PROMPT.md`
- Inputs read: `paper/main.tex` §8 and §9, `theory-lab/double_end/THEORY.md`,
  `research_state.md` (2026-09-01 onwards), the second referee brief
  `docs/fable-second-referee-takeover-2026-09-04.md`
- Positive controls: `theory-lab/double_end/ground_truth_small.json` (the five
  Leech trees, n = 2,3,4,4,6), script `check_new_lemmas.py` (scratchpad; copied
  below in §5); `check_signed.py` (scratchpad) for §1.5
- Labels used: **PROVED**, **FINITE VERIFIED**, **OBSERVED**, **CANDIDATE**,
  **OPEN**, **NEGATIVE** (a measured or derived reason a route cannot work)

## 0. Verdict

No. I do not see a route that closes order 25 more cheaply than the measured
ones, and I can say why the delta ladder in particular cannot be finished:
from delta = 287 onwards a *single* rung costs more than the whole-problem
direct search (§2). Three small structural facts are new and proved (§1); they
tidy the picture and give one prune, but none of them bites in the open range.
If order 25 is to be closed with today's ideas it will be by the increasing-
weight forest engine on a cluster at 10^6–10^8 CPU-hours (§4), not by the
ladder. Of the fourteen rungs, delta = 285 is the only one worth running, and
only as incremental evidence.

## 1. Three small new facts (PROVED, positive controls pass on all five known Leech trees)

Notation as in the paper: n = 25, N = 300, {a,b} the pair at distance N,
named so that d(a,w) = N-1; e(u) = N - d(a,u), f(u) = N - d(b,u) for
u not in {a,b}; delta = diam(T-a); m = N - delta; W = the m vertices with
d(a,u) > delta; a_1 = the neighbour of a, s = w(a a_1).

### 1.1 The pair attaining diam(T-a) contains b, for every delta

**Lemma 1 (PROVED).** Let T be a Leech tree of order n >= 3 with the naming
above and delta = diam(T-a). Then the unique pair at distance delta contains b.
Equivalently

    delta = N - min { f(u) : u not in {a,b} },   i.e.   m = min F.

*Proof.* Suppose x, y avoid {a,b}, labelled so that the foot of x is not after
the foot of y (the labelling only decides which of the two symmetric bounds
below is used; both hypotheses hold for either vertex). Then
d(x,y) = N - f(x) - e(y) - 2h_c <= N - f(x) - e(y). The pair
{b,x} avoids a, so d(b,x) <= delta and f(x) >= N - delta. Also e(y) >= 1. Hence
d(x,y) <= delta - 1 < delta. So the pair attaining delta contains a or b; it
avoids a by definition; so it contains b. The pair is {b,y} with
f(y) = N - d(b,y) = N - delta, and no f is smaller because every d(b,u) with
u != a is at most delta. QED

The paper (Theorem 8.5, last sentence) proves this only for delta = N-2. The
general form is the same argument. Control: on the five known Leech trees the
pair at distance delta contains b and delta = N - min F in every case
(n = 3: delta = 1; n = 4: delta = 3 and 4; n = 6: delta = 11, min F = 4).

**Consequences.**

(a) *The ladder is the first-F-gap branching of the two-anchor engine.* Gaps are
processed in increasing order in `double_end_search`; every gap below the first
non-anchor gap is an e or an f. Lemma 1 says the first gap that is an f is
exactly m = N - delta. So the fourteen open rungs are precisely the branches
"gaps 1..m-1 are all e, gap m is an f" for m = 2..15, and the closed range
delta <= 284 is the branch "gaps 1..15 are all e", which is the
`--force-e-upto 15` run (THEORY.md §10 already notes that E ⊇ [1,15] is the
closed case; Lemma 1 makes the equivalence two-sided). This is why the
parameter-free two-anchor search cannot be cheaper than the ladder: it *is* the
ladder with the rungs interleaved, and it was measured to be four orders of
magnitude worse on the one rung both have run (delta = 284: 1.64e9 leaves
versus a floor of 1.96e13 nodes).

(b) *The pendant weight is bounded below: s >= m = N - delta.* Because a_1 lies
on the a–b path at height 0, f(a_1) = s, and m = min F <= s. At delta = 285
this is s >= 15, at delta = 279 it is s >= 21; the delta = 279 sweep used
s in [13,160] (from the heaviest-edge hypothesis later dropped), so this is a
hypothesis-free replacement for the lower end. Mild.

(c) *Where the second endpoint sits.* The vertex y with f(y) = m has
p(y) = m + h(y) and d(a,y) = m + 2h(y). If s = m then y = a_1 and the
diametral path of T-a is the spine minus its first edge; if s > m then y is a
pendant vertex with h(y) = p(y) - m >= s - m >= 1. In the normal form this is a
free prune: the value delta must be realised by the deepest high vertex
h_{m-1} (which is b), i.e. max_u d(h_{m-1}, u) = delta in K. The engines
realise every value anyway, so the saving is a constant factor at most.

### 1.2 The near-graphs form a chordal filtration (weight-free ordering condition)

**Lemma 2 (PROVED).** For any tree metric and any threshold t, the graph N_t
on V whose edges are the pairs with d(u,v) <= t is chordal (distinctness of
the distances is not needed for this). For a Leech tree of order n, N_t has
exactly t edges,
so the distance ordering is an ordering e_1, ..., e_N of the edges of K_n in
which every prefix is chordal; equivalently, when the pair {u,v} at distance
t+1 is added, u and v are in different components of N_t or are separated in
N_t by their common neighbours.

*Proof.* In the geodesic (continuous) tree, the closed ball of radius t/2
about a vertex is a subtree; two such balls meet iff d(u,v) <= t; intersection
graphs of subtrees of a tree are chordal (Gavril/Buneman). The last sentence is
the standard characterisation of when adding an edge to a chordal graph keeps it
chordal. QED

Control: every N_t is chordal on the five known trees (maximum-cardinality
search + perfect-elimination check, all t). This uses nothing about integer
weights, so it is a constraint on *which pair gets which rank*, independent of
the values. I looked for a bite and found none: N_t stops being triangle-free
as soon as three mutual distances are <= t (already at t = 3 when weights 1 and
2 share a vertex), and after that the separation condition is weak. Recorded so
that it is not re-derived.

### 1.3 Roots-of-unity identities generalising Taylor

**Lemma 3 (PROVED).** Root T anywhere; h(y) = weighted depth; for a complex
number z put sigma_y(z) = sum over u in the subtree of y of z^{h(u)}. Then

    sum over ordered pairs (u,v), u=v allowed, of z^{d(u,v)}
      = sum over vertices y of z^{-2h(y)} ( sigma_y^2 - sum over children c of y of sigma_c^2 ).

If T is a Leech tree of order n then the left side is n + 2(z + z^2 + ... + z^N),
so for every N-th root of unity z != 1 the right side equals n. The case z = -1
is Taylor's parity argument; the cases z = i, omega, zeta_5, ... say that the N
distances are equidistributed modulo every divisor of N and express that through
the residues of the depths and the subtree sums.

*Proof.* Pairs with lowest common ancestor y contribute
z^{h(u)+h(v)-2h(y)}; summing over ordered pairs with lca y gives
z^{-2h(y)}(sigma_y^2 - sum_c sigma_c^2) because sigma_y^2 counts all ordered
pairs in the subtree and the sigma_c^2 remove those inside one child. QED

Control: the identity holds to 1e-7 for every root vertex and every nontrivial
N-th root of unity on all five known trees, and agrees with the direct sum.

What it does and does not do. It is a family of necessary conditions on
(shape, edge-weight residues mod 4, mod 3, mod 5, ...). As a *pre-filter* on
residues before depths are assigned it is hopeless: the residue space is
60^24 per shape and the identities pass a fraction I estimate at 1e-6–1e-9 of
random residue assignments, which still leaves ~1e33 survivors. Inside an exact
engine the exact tiling already implies them. Whether any single identity
(z = i or z = omega) excludes n = 25 outright the way z = -1 excludes n = 23 is
**OPEN**; I do not expect it (the quadratic form has no sign structure to
exploit), and I did not find a 25-vertex tree satisfying mod 4 and mod 3
equidistribution either, because random search cannot reach a 1e-6 event.

### 1.4 A tiny bound: the second deletion diameter

**Lemma 4 (PROVED).** Let delta_2 = diam(T - {a,b}) and g_2 = N - delta_2.
Then g_2 <= 46 at n = 25. *Proof.* If g_2 = 47 the 47 anchor pairs occupy
[254,300] and T - {a,b} is a Leech tree of order 23, which fails Taylor's
condition. QED. Also every value in (delta_2, 300] is an a-depth or a
b-depth, so the far graph {d >= t} for t > delta_2 is a double star at a and
b. I checked whether crowding applied to this double star bites (§3, item 1):
it does not.

### 1.5 Astra 6's signed first moment (external idea, checked here) and where it sits

On 2026-09-04 an OpenAI Astra 6 run (`~/Documents/Codex/leech-ideas-2026-09-04/`)
proposed the **signed first moment**: for a Leech tree of order 25,

    sum_{u<v} (-1)^{d(u,v)} d(u,v) = (2+4+...+300) - (1+3+...+299) = 150,

with the cut form sum_e w_e q_e (S - q_e), where sigma_v = (-1)^{d(o,v)},
S = sum sigma_v = ±5 and q_e is the sigma-sum of one side of e. Once the parity
pattern (lowpar, hpar, depth parities) is fixed, q_e is a constant and the
identity is a second integer *linear* equation in the depths, alongside the
Wiener equation sum_e w_e |A_e|(25-|A_e|) = 45150.

**Status after my check.** PROVED and correct (I re-derived it and verified the
cut identity on the five known trees and on 300 random weighted trees, n <= 14;
Astra's script also reproduces). It is **new to the project's presolver**: the
repository's `parity_moment_audit.py` and `colored_moment_hall_presolve.py`
use the odd *count* and the *unsigned* sum only, and no file mentions a signed
sum. Astra's own evidence is honest and small: one delta = 285 candidate that
passes Hall, parity-Hall, moment-Hall, global parity and Wiener is rejected
(478 != 150), and one parity branch of a delta = 286 structure is excluded by
J ≡ 2 (mod 8) against 150 ≡ 6 (mod 8); at the parity-pattern level the gain is
0 of 48 (r = 9) and 1 of 88 (r = 10).

**Where it sits.** It is the k = 1, z = -1 member of one family. Since
P(z) = sum_{u<v} z^{d(u,v)} equals z + z^2 + ... + z^N exactly, every derivative
at every point is determined; the first derivatives are the ones linear in the
weights. Lemma 3 above is k = 0 (P(zeta) = 0 for all nontrivial N-th roots);
Wiener is k = 1, z = 1; Astra's is k = 1, z = -1. For a nontrivial N-th root of
unity zeta the value is

    P'(zeta) = -N / (1 - zeta)          (z = -1 gives -150, i.e. the signed sum 150),

and the cut decomposition still applies because a pair crossing edge e = (x,y)
has d(u,v) = d(u,x) + w_e + d(y,v) exactly:

    sum_{u<v} d(u,v) zeta^{d(u,v)} = sum_e w_e zeta^{w_e} (sum_{u in A_e} zeta^{d(u,x)}) (sum_{v notin A_e} zeta^{d(v,y)}).

(PROVED; checked numerically for zeta = i on the five trees and 300 random
trees.) For zeta = i this is linear in the weights once the residues mod 4 are
fixed and gives two real equations; but the engines fix parities, not residues
mod 4, and fixing residues multiplies the pattern count by 2^r, so I list this
as CANDIDATE, not as a recommendation.

Astra's second identity, 5M + sum_e w_e (2a_e - 3b_e)^2 = 44400 with M the sum
of the 45 minority-class distances, is also correct (the same cut argument with
zero-sum charges +2/-3), but note what it constrains: M is not otherwise known,
so the content is the bound 2070 <= M <= 11520 (45 distinct even values), i.e.

    sum_e w_e (2a_e - 3b_e)^2 <= 34050,

which says the two parity classes must be nearly proportionally mixed across
every heavy cut (a cut with 12 vertices all of one class costs 576 w_e or
1296 w_e). That is a genuinely different linear functional from Wiener and the
signed sum and could be a useful inequality; its bite is untested. Astra's
M <= 8838 is the weak direction and can be ignored.

**Verdict.** A correct, cheap, sound prune valid for all fourteen rungs, worth
wiring into the depth phase at delta = 285 exactly as Astra suggests: with
Wiener it lets the last two free depths be solved rather than enumerated, and
its residues mod 8 exclude parity branches before any depth is placed. It is a
constant-factor gain per rung. It does not touch the exponential growth in r
of §2, so it does not change the verdict of §0; it changes how fast the one
affordable rung finishes.

**Measured 2026-09-06 (WP-A1, FINITE VERIFIED).** Wired into the depth phase
of `abstract_class_search` (new file `abstract_class_search_moment.cpp`, four
levels, exact differential against the frozen delta = 284 records and against
an independent Python check on 4040 complete assignments at n <= 10): the
speed-up is 1.01x. With seven or eight free depths the two-equation integer
system is almost always solvable (structure-level kills 8/1811, 4/2170,
0/2736), the exact test at complete assignments is subsumed by the distance
check, and pinning the last two depths inside the DFS is 8.7x *slower*
because the collision pruning kills branches before those depths are reached
while the memo is invalidated. So the verdict above was optimistic: inside
this engine the signed moment is sound but worthless at r >= 8; it bites only
when few depths are free (order 6: 14 of 22 structures killed with no depth
search). Gate G1 of the plan fails and the delta ladder is closed.

### 1.6 The a-side spine is coarse (PROVED, all delta; added 2026-09-05 while WP-A1/B1 ran)

Let x_0 be the lowest common ancestor (rooted at a) of the m high vertices W,
m >= 2. Every vertex x on the path from a to x_0, at depth p, has
d(x,u) = delta + i_u - p for all u in W, i.e. a run of m consecutive distances
(delta - p) + [1, m]. Runs at two such vertices at depths p < p' are disjoint
sets of distances (different pairs), so p' - p >= m.

**Lemma 5 (corrected 2026-09-06 after audit).** On the a–x_0 path
consecutive vertices differ in depth by at least m = N - delta; every edge on
it has weight >= m; and mu_0 = depth of x_0 satisfies
mu_0 <= (2N - 1 - C(m,2))/2, improving to (2N - 1 - C(m+1,2))/2 **only when
x_0 is not in W**. The unconditional C(m+1,2) form printed here on 09-05 was
false: the n = 4 path (N = 6, delta = 4, m = 2) has x_0 in W at depth 5,
against (11 - 3)/2 = 4, and meets the C(m,2) bound (11 - 1)/2 = 5 with
equality; the n = 3 tree and the n = 4 star fail the same way. The paper's
Corollary cor:secondend carries the two-branch statement and a proof whose
two gaps (a vertex of W before x_0; the last edge when x_0 is in W) were
closed on 09-06. In particular s >= m (Lemma 1(b) again). More generally, for any two vertices x, y
of the a–W skeleton with W-label sets I_x ⊇ I_y below them, the depth gap
mu_y - mu_x is not in the difference set I_y - I_x; for the closed range
(m = 16, top split {15,1}) this gives mu_1 - mu_0 >= 15 for the first two
medians.

Control (n = 6, vertex numbers as in ground_truth_small.json, edges 0-1:5,
0-2:1, 0-3:2, 1-4:4, 1-5:8): a = 5, W = {3,2,0,4} with d(a,·) = 15,14,13,12,
m = 4, x_0 = vertex 1 at depth 8 = s >= 4, and its distances to W are 4,5,6,7,
a run of four; x_0 is not in W, so the C(m+1,2) branch applies:
(2N-1-C(5,2))/2 = (29-10)/2 = 9.5 >= 8. Control for the other branch: the
n = 4 path above, x_0 in W, equality in the C(m,2) bound. Use: a free depth prune in the normal form (the low vertices between
the root and the lca of the high block are spaced >= m); not yet wired in.

## C. Results of the theory work packages (WP-C1, WP-C3), 2026-09-05

**WP-C3 — does P(i) = 0 have a shape-level corollary like Taylor? NEGATIVE.**
For cross pairs u in P (even depth), v in Q (odd), write tau(u) = (-1)^{h(u)/2},
tau(v) = (-1)^{(h(v)-1)/2}; then i^{d(u,v)} = i·tau(u)tau(v)·eps(lca) with
eps = +1 if the lca is in P and -1 if in Q, and similarly for within-class
pairs. So c_1 = c_3 reads sum_{P×Q} tau_u tau_v eps(lca) = 0 and c_0 = c_2
reads sum_{P pairs} tau tau eps = sum_{Q pairs} tau tau eps: the lca class is
intrinsic and cannot be removed by any choice of root, because i^{w_e} does not
telescope along an up-then-down path (only ±1 does). The counts are not even
determined by the four depth-residue class sizes: the star with weights
1,2,3,4 and the path with weights 1,1,1,1 both have residue classes
{0,1,2,3,0} but mod-4 distance counts (2,3,2,3) and (1,4,3,2). Hence no
Taylor-type condition on n or on class sizes comes from z = i; the identity
stays an engine-level check only.

**WP-C1 — bite of the charge inequality sum_e w_e (2a_e - 3b_e)^2 <= 34050.
Low expected value; not pursued with an enumeration.** For a cut with k
vertices on one side and classes placed at random (hypergeometric 15/10),
E[(2a-3b)^2] = k(25-k)/4, so the expected left side is
(1/4) sum_e w_e k_e (25-k_e) = 45150/4 ≈ 11,290, three times below the bound.
It bites only when heavy cuts are strongly class-segregated; the high block is
parity-balanced (⌈m/2⌉, ⌊m/2⌋) and the anchors share a class, so nothing in
the normal form pushes towards segregation. Label: CANDIDATE, expected
constant-factor at most; test only if WP-A1's two equalities prove strong.

**WP-C2 (Lemma E closure) — parked after one look.** The sum condition
Σμ >= 21630 is tight exactly when the 120 within-W distances are the top 120
values [165,284], which is consistent with everything else counted so far; the
only new handles found are the median-gap statements of Lemma 5. A hand proof
would have to reproduce the packing the delta = 284 search does (1.64e9
leaves); two sessions are unlikely to suffice, so this stays parked unless a
sharper invariant appears.

## 2. Why the ladder cannot close order 25 (NEGATIVE)

### 2.1 The numbers

| rung | structure-bearing low trees | cost | source |
|---|---|---|---|
| delta = 284 (r = 8) | 7 of 115 | 1.64e9 leaves, 3.93e10 nodes, 448 records; hours | certificate `depthv7_r8`, frozen re-run |
| delta = 285 (r = 9) | 95 of 286 | ~1e4 CPU-h (3,196 of 24,320 pairs done, all empty) | project estimate 2026-09-02 from 30/95 shapes in 8 h on one of 256 tasks |
| delta = 286 (r = 10) | 317 of 719 | ~60x delta = 285, i.e. ~6e5 CPU-h | project estimate 2026-09-02 |
| delta = 287 (r = 11) | 1523 of 1842 | ~5e7 CPU-h | **my extrapolation**: count ratio 1523/317 = 4.8 times the per-tree growth 60/(317/95) ≈ 18 implied by the previous step |
| whole problem, forest engine | — | 1.4e17–2.2e17 nodes at 0.46–0.47 µs = 1.9e7–2.9e7 CPU-h (measured n = 19, 20 on 09-06; the 09-05 row read 1e16–1e17 nodes / 1e6–1e7 CPU-h from paper §9) | §4 update; growth 5.71 → 8.19 per vertex over n = 12..20 |

So one rung, delta = 287, already exceeds the estimate for the *entire*
problem by the direct engine (by about 1.7x against the measured 09-06
figure, by an order of magnitude against the 09-05 one), and eleven rungs
remain after it, each larger.
The only assumption I add is that the per-tree cost keeps growing at the rate
the project itself measured between 285 and 286; every other number is the
project's. Even if that rate halved, delta = 288 would cross the line instead.

The forest-engine figure is itself optimistic: the per-vertex growth factor
rose by about 0.3 per step over n = 12..18. Continuing that trend
(8.0, 8.35, ..., 10.1 for the seven remaining vertices) gives ~3e17 nodes,
~1e8 CPU-h.

### 2.2 The structural reason

The crowding inequality needs a star with about twenty far leaves: it is
C(m,2) <= (r+1)(2m-3), which fails only for m >= 20 at k = 24. In the open
range m = N - delta <= 15 by definition, so no rung can be helped by crowding;
that is not a weakness of the implementation but of the parameter. At the top
rung delta = 298 the normal form is a rooted tree on 24 vertices with 22 free
low depths and two pinned high vertices: it *contains* the generic 24-vertex
problem, and the "depth-free phase" keeps essentially every rooted low tree
(the survival fraction rises 33% → 44% → 83% over r = 9, 10, 11).

I also tried to make crowding two-sided, using Lemma 4: for t > delta_2 the
far graph is a double star with m_a leaves at a and m_b at b, m_a + m_b =
g_2 <= 46, and the C(m_a,2) pairs inside the a-star have distances at most
delta_2 with lowest common ancestors at depth > delta_2/2. The capacity per
class is 2g_2 - 3 and the number of classes is at most 26 - m_a, so the
inequality is C(m_a,2) <= (26 - m_a)(2g_2 - 3) with g_2 = m_a + m_b; it can
fail only for m_a >= 21, and then only for small m_b (m_b <= 1, 8, 20 at
m_a = 21, 22, 23 respectively) — i.e. it is the original one-sided
inequality again, and the open range has m_a >= m with m <= 15 giving it
nothing. Dead, with the arithmetic above as the reason (parenthetical
corrected 09-06 after audit).

## 3. The five "what would help" items, one by one

1. **A stronger crowding inequality that bites when the top block is short.**
   NEGATIVE. §2.2 gives the reason: every capacity bound of this family is of
   the form (number of pairs among far vertices) <= (classes) × (window
   capacity), and with m <= 15 the left side is at most 105 against a right
   side of at least 270. The project's joint-interval Hall, demand-span and
   moment-Hall pilots (research_state 2026-09-02) are the correct sharper
   versions and were found redundant on complete candidates; the minimal
   counterprofile at r = 5 recorded there is the right witness that total
   capacity cannot improve the bound.
2. **Additive structure on E and F.** NEGATIVE for any Sidon-type bound on E
   (or F) alone. Minimal counterexample: three pendant paths of heights
   h, h+1, h+2 hanging in different branches at one foot p give
   e = N - p - h - j and f = p - h - j for j = 0,1,2, so E and F each contain
   a 3-term arithmetic progression, while the mutual distances 2h+1, 2h+2,
   2h+3 are distinct and every crossing sum with other vertices is unaffected.
   So distance injectivity bounds neither the additive energy of E nor that of
   F; any bound must involve the heights, and on the spine (h = 0) it is the
   Golomb condition already used. The cross condition "f(u) + e(v) distinct for
   u before v" is a *half* Sidon condition (ordered pairs only) and I could not
   extract a nontrivial size bound from it at n = 25 (|E| = |F| = 23 in
   [1,299]; the trivial bound allows up to ~150).
3. **Parity coupled to crowding.** NEGATIVE as a new route: W has ⌈m/2⌉ and
   ⌊m/2⌋ vertices of the two parities, the colored moment-Hall presolver already
   resolves classes by parity, and the 2026-09-02 audit shows those layers are
   implied once a candidate's class sets are exact. Lemma 3 is the correct
   generalisation (mod 4, mod 3, mod 5) and §1.3 says why it does not prune.
4. **Collapse to finitely many small cases.** NEGATIVE. The ladder does
   collapse to fourteen finite cases, but they are not small: delta = 298 is
   the generic problem (§2.2). Lemma 1 shows the two-anchor engine's branching
   is the same fourteen cases, so there is no second, cheaper collapse hiding
   there.
5. **An argument that order 25 is not decidable by a search of this shape.**
   Given above as far as it can be given honestly: any leaf-deletion ladder
   pays the generic cost on its top rungs, so it cannot beat the direct engine;
   the direct engine is 1e6–1e8 CPU-h. That is not undecidability, it is a
   price.

## 4. What I would do

- **If the goal is closure with today's ideas:** the increasing-weight forest
  engine on Hoffman2, not the ladder. Budget 1e6–1e8 CPU-h; at 1,000 cores the
  low end is six weeks and the high end is eleven years, so measure first:
  run n = 19 and n = 20 to completion (expected 5e11 and 4e12 nodes, 40 and
  350 CPU-h) to see whether the growth factor keeps rising. If it stabilises
  near 7.6 the campaign is 1e6 CPU-h and worth proposing; if it keeps rising it
  is not, and the honest statement is that order 25 waits for a new idea.
  Nothing in §1 makes that engine faster: every new necessary condition is
  implied by the exact tiling the engine already enforces.
**Update 2026-09-05 (WP-B1, measured).** n = 19 completed on Hoffman2:
474,060,441,097 nodes, 0 survivors, 60.74 CPU-h (0.46 µs per node on that
cluster), g(19) = 7.928. The growth factor is still rising by about 0.34 per
vertex (5.71, 5.93, 6.10, 6.38, 6.74, 7.19, 7.59, 7.93). Extrapolating with
that trend gives ~2.7e17 nodes ≈ 1.2e8 CPU-h at n = 25; holding it at 7.93
gives ~1.2e17 nodes ≈ 5e7 CPU-h. **n = 20 completed 2026-09-06** (after an n = 17 control reproduced the
published count exactly under the MAXV=21 binary): 3,883,033,661,682 unique
nodes, 0 survivors, 510 CPU-h at 0.47 µs per node, g(20) = 8.193, verifier
prefix_ok. The factor is still rising (7.59, 7.93, 8.19). Extrapolation to
n = 25: 1.4e17 nodes / 1.9e7 CPU-h if the factor freezes at 8.19, 2.2e17 /
2.9e7 CPU-h if it keeps rising by 0.27. **Gate G2: NEGATIVE.** No campaign
proposal; the paper's §9 estimate has been raised accordingly.

- **If the goal is incremental evidence:** finish delta = 285 by harvesting
  the `.tmp` records (13% done, all empty) — it is the only rung whose cost is
  known and affordable. Do not start delta = 286.
- **For the paper, independent of computation:** the Lemma E programme in
  THEORY.md §10 (closing 21630 <= Σμ <= 32500) would replace the delta <= 284
  certificates by a proof. It is worth a week of hand work; it does not touch
  the open range.
- **Record, do not pursue:** Lemmas 2 and 3 are clean necessary conditions
  with no bite found; Lemma 4 and consequence 1.1(b) are one-line prunes.

## 5. Controls

Script (pure Python, no project imports) run on the five known Leech trees from
`ground_truth_small.json`: for each tree it names a, b by the N-1 pair, computes
delta and min F and checks Lemma 1; checks chordality of every N_t by
maximum-cardinality search plus perfect-elimination test; and evaluates both
sides of Lemma 3 for every root vertex and every nontrivial N-th root of unity.
All checks pass. An independent adversarial pass (a separate model, given only
the three statements and no repository access) could not refute any of the
three and flagged two presentational points, both now incorporated: the
labelling in Lemma 1 is a harmless WLOG, and Lemma 2 does not need distinct
distances. The script is `check_new_lemmas.py` in the session scratchpad
and is copied to `theory-lab/double_end/check_new_lemmas.py`.
