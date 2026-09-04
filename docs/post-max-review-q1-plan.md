# Post-Max-review plan: the universal q=1 route

Status date: 2026-08-24.  This plan synthesises two independent high-effort
direction reviews of mathematical snapshot `83e8ae4`: the Codex Max audit and
the blind Reviewer-2/Fable Max audit.  It is a work plan, not a theorem.

## Joint verdict

Both reviews return **CONTINUE WITH PIVOT** and independently agree that:

- **OBSERVED:** FW203--FW217 are locally sound under their written hypotheses.
- **OBSERVED:** the unseen vertices together with the complement root form an
  ancestor-closed connected induced subtree.
- **UNVERIFIED:** the periodic terminal has no collision, inherited Leech
  state or globally decreasing transfer.
- Route C's quadratic-span lower bound is compatible with the global
  `Theta(n^2)` scale.  More lower bounds of the same type are not the critical
  path.
- Generic order-25 forest search is not a plausible substitute for the
  missing structural interface.

The Codex audit adds a stronger global simplification that Reviewer 2 did not
have: the endpoint-one singleton extension (FW218) bypasses ten of the eleven
FW210 rows.  Every hypothetical G18 counterexample enters the full FW211
normal form with

```text
(q,P,S)=(1,{0},{0}).
```

The other ten rows remain correct contextual terminals; they are bypassed,
not excluded.  The proof programme below therefore specialises Reviewer 2's
connected-core proposal to this single row.

## Critical path

### M0. Scope and ledger cleanup

Deliverables:

1. absorb FW204's generic fully-blocked `C`-deep output through the open-half
   level-`C` shell, without pretending that the original offshoot already has
   FW92--FW93 cap provenance;
2. state explicitly why the two FW210 caps are disjoint by metric location;
3. preserve every status label: these are **OBSERVED** routing statements,
   while G18 remains **UNVERIFIED**.

Acceptance: the proof text, README ledger and roadmap say the same thing.

### M1. FW218 universal endpoint-one singleton extension

Deliverables:

1. a self-contained endpoint selection, four-point retention, gate/pivot and
   root-hit proof;
2. an explicit statement that the singleton directly re-proves the
   FW209a--e/FW210 analytic package rather than inheriting FW208 provenance;
3. a constant-memory verifier and frozen certificate;
4. all five known witnesses through both `src/checker_a.py` and
   `src/checker_b.py`, with L2 recorded as the `n=2` exception.

Acceptance: every `n>=3` Leech tree reaches the FW210 q=1 rectangle, and every
`n>=5` tree reaches the full FW211 q=1 normal form.  This is **OBSERVED** only
after proof, replay and an independent proof pass; it is not G18.

### M2. Exact q=1 core interface

Let `Q` be the opposite first hole, root the complement at the neighbour of
`x`, and write `y(v)=beta-depth(v)`.  Prove and freeze the following exact
specialisation:

```text
visible coordinates: 0,1,...,Q-1 exactly once;
coordinate Q: absent;
H_Q={root} union {v:y(v)>Q}: connected induced, order u+1;
Spec(T-x)=[1,N-Q] minus {d(x,v):v in H_Q}.
```

Also retain the q=1 numeric consequences

```text
n=Q+u+2,
Q<=4u+7,
u>=ceil((n-9)/5),
4B+u>=n-4.
```

Acceptance: a written all-order lemma plus a constant-memory replay of the
integer consequences and all known witnesses.  The exact hole bijection must
not be mislabeled as bounded defect: the number of holes is `u+1`.

### M3. Boundary forest and cross-Sidon strengthening

The visible vertices form pendant components `W_i` below `H_Q`.  Prove and
freeze

```text
sum_i C(|W_i|,2)<=2Q-3,
#components >= ceil(Q^2/(5Q-6)),
max_i |W_i|<=floor((1+sqrt(16Q-23))/2).
```

At every common LCA, use Reviewer 2's forced cross-Sidon relation

```text
(shed-shed) intersect (retained-retained)={0}.
```

First test the falsifiable strengthening

```text
sum_i (e_i-1)=O(1)
```

for the heavy-spine sheds.  A proof would give a rigid caterpillar-like core;
a scalable symbolic countermodel would stop this subroute.  No random search
or materialised Cartesian product is allowed.

**Result:** the subroute is stopped by an **OBSERVED negative diagnostic**.
The q=1 double-endpoint peel satisfies the existing balance, cross-Sidon and
FW216 modeled-family constraints through a scalable family with
`sum_i(e_i-1)=floor(Q/4)`.  It is not a Leech witness, so a stronger statement
with new tree-realisation input is not refuted; the current interface is
insufficient and M4 is now the critical path.

### M4. Multi-boundary no-return / bounded-defect interface

For the `Omega(Q)` visible boundaries, determine which ones normalise to
valid caps.  The milestone passes only if at least one of the following is
proved:

1. a repeated distance;
2. a strict lexicographic decrease of the full two-hole contextual state;
3. a topology-independent finite catalogue of all returns to endpoint
   singletons; or
4. a bounded-defect exact prefix inherited by a proper core.

A single local deficit `q'<Q`, another `Omega(n)` branch/component bound or
another compatible `Omega(n^2)` span does not pass.

**Partial result:** FW220 now supplies that local deficit canonically:
the coordinate-zero component gives `1<=q_*<=O(sqrt(Q))<Q`, with an
open-half dominant nested thin cap in the bidirectional-entry branch and a
direct open-half/central-thin dichotomy otherwise.  This is useful retained
context, but by the acceptance rule above it does not complete M4.  The
remaining target is specifically a no-return theorem for normalising this
smaller cap together with the original endpoint singleton.

**Catalogue result:** FW221 completes the finite-return part of option 3.
Normalisation can return through the original x-singleton only with a
z-singleton, rooted `L2`, or middle-rooted `L3`; the other eight FW210 rows
are incompatible with the retained endpoint-edge scale.  The next target is
to use the discarded wrapper and the many other visible boundaries to
exclude or strictly descend these three rows.  FW261 below later removes the
scope separation for the original `Q=2,3` cases: they enter the same exact
endpoint-singleton double-peel state directly, although they are not thereby
excluded.

**Spectral-interface result:** FW222 supplies option 4 in a precise but not
yet inductive form.  After a catalogue return, the proper core `D=T-J` has
`Spec(D) intersect [1,g-1]=[C(a,2)+1,g-1]` with `a<=3`, together with the
exact pair-polynomial factorisation.

**Anchored-gap result:** FW223 removes the phrase "unclassified above `g`".
If `s_i-s_(i-1)=a+e_i` are the consecutive rooted-depth gaps of `D`, then
the boundary edge excess is exactly `sum e_i`, every `e_i` is an explicit
interval of high internal distances, and the q=1 context forces
`e_(d-1)=Q-a`.  It also gives the exact positional split

```text
boundary root visible:       g<=Q-a, wrapper remains;
boundary root in H_Q:        J=W_0, g>=Q-a+2.
```

The remaining obstruction is the uncontrolled mass in
`e_1,...,e_(d-2)`.  The next milestone is therefore to turn the visible-root
wrapper into a strict contextual decrease, or use the wrapper-free
threshold-core branch to force a collision/finite residual gap catalogue.

**Double-peel result:** FW224 removes the return cap `J` and opposite leaf
`x` simultaneously.  With `K=T-(J union {x})`, `H=H_Q` and `M=N-Q`, the
smaller interval has the exact four-class tiling

```text
I_M=F_K+I_C(a,2)+X^g A_a R_p(K)+X^h R_r(H),
X^hR_r(K)=X^hR_r(H)+I_[M+1,N-a].
```

Thus the holes are no longer arbitrary: they are exactly a rooted factor of
connected `H`, and the remaining visible vertices are one consecutive
rooted-depth block at the opposite root.  The acceptance target is now
closure of this four-class state under another peel with a strictly smaller
`(M,|K|,Q)`, or a collision/finite terminal catalogue.

**Linear-defect stability result:** FW225 puts `C=binom(|K|,2)` and proves
that `Spec(K)` is `[1,C]` with `delta` low holes exchanged for `delta` high
outliers in `[C+1,C+L]`, where

```text
L=a n+u+1-a(a+3)/2<=4n-14.
```

The next split is no longer vague: bounded `delta` is a finite-hole and
endpoint-strip problem, while growing `delta` requires equally many low
coefficients from the two rooted factors in FW224.  Do not spend a pass on
another unlocated diameter/span inequality; the missing input must retain
which rooted factor supplies each low intrusion.

**Visible-root separation:** FW226 now proves

```text
delta+ceil((delta-binom(a,2))/a)>=|K|-ceil(g/a).
```

On the visible-root branch this forces defects of scale at least
`n/10`, `2n/5`, or `11n/20` for `a=1,2,3`.  Consequently the bounded-defect
catalogue is no longer a two-location problem: at unbounded order it lives
only in the connected threshold core.  The visible branch belongs to the
growing-defect collision/energy pass.

**Bounded-defect topology compression:** FW227 now shows that the threshold
case is one giant component of `K-p` plus an explicitly bounded wrapper.  If
`delta<=Delta` and `c_0=Delta+ceil((Delta-binom(a,2))/a)`, then above an
explicit order threshold the giant component omits at most `c_0+5a+4`
vertices of `T` and has at most two boundary edges.  The next bounded pass
must retain the exact spectrum across those one or two boundary factors; a
generic bounded-deletion diameter estimate is insufficient.

**Taylor-parity reduction:** FW228 transfers the original parity imbalance
through deletion of `J union {x}`.  Bounded defect is now possible only in
the two rows `(n=r^2+2,a=1)` and `(n=r^2+2,a=3)`; every square-order row and
the square-plus-two `a=2` row has at least square-root defect.  The bounded
wrapper catalogue should not spend cases on those four eliminated regimes.

**Bounded branch closed:** FW229 counts every pair among the shell vertices,
using the ancestor-closed low ball as the LCA split.  It forces `delta` to be
linear in `k` in all three rows, including threshold-core returns.  Therefore
retire the bounded-wrapper catalogue as a scalable branch; FW227/FW228 remain
finite refinements only.  All further structural budget goes to a collision
or energy inequality for the two rooted factors supplying the linear holes.

**Two-factor allocation frozen:** FW230 splits the defect exactly as
`delta=binom(a,2)+q+b`, replaces the old low-ball cap by the exact count
`t=ceil(q/a)`, and runs an independent shell-pair inequality at the connected
H root.  Both inequalities use the complete non-low factor supports, without
discarding the `delta` high rooted depths; the exact consecutive block `K-H`
extends the r-shell to all `k-b` non-low vertices.  The resulting rational density floors are `1/5,3/14,2/9` for
`a=1,2,3`.  The next pass should work directly with the disjoint low supports
`X^g A_a R_p(K)` and `X^h R_r(H)` and the two shell LCA partitions; another
one-root capacity estimate will only reproduce FW229/FW230.

**Bi-root crown compressed:** FW231 shows that either the defect already
reaches `ceil(k/2)`, or nearly the whole intersection of the two non-low
shells lies in a single off-spine component of the p-r diameter path.  The
next pass should use the three arms at its gate (toward each diameter endpoint
and into the crown) to force thinness or a repeated distance.  Treating its
vertices as an arbitrary third rooted factor would discard the new `O(1)`
outside-fibre bound.

**Crown heavy spine frozen:** FW232 follows the largest marked child inside
that actual gate fibre.  A fixed LCA has only `2(L-a)+1` available distances,
so each heavy step has bounded shed--retained product.  Until the marked order
falls to `O(sqrt(n))`, this creates a single path with linearly many
positive-loss vertices.  The only positive steps that need not be global
branch vertices are shell marks lying on the path; their depth differences
form a Golomb ruler in a width-`O(n)` interval, so only `O(sqrt(n))` exist.
The exact all-order branch-spine floors are
`k/48,k/72,k/96-O(sqrt(k))` in the three cap rows.  This rules out an
unstructured bush as the low-defect escape.  The next pass must use distances
between different spine levels (plus the two diameter endpoint translates),
not another same-LCA capacity estimate.  The separate `delta>=ceil(k/2)`
energy branch remains live.

**Outlier pole cone frozen:** FW233 views the `delta` high K-pairs as a far
graph in the width-`L` band above `C`.  Four-point crowding gives an
`O(sqrt(k))` pole cover; since FW230 has `delta=Omega(k)`, one pole has
`Omega(sqrt(k))` outlier neighbours.  Their paths share a
`k^2/4-O(k)` common cone and force a located edge of weight
`k/4-O(sqrt(k))`.  This applies to the high-defect branch as well as the
minimum-defect crown rows.  The active bridge is now to align this long pole
cone with the FW232 heavy crown spine.  If they nest, the shared direction is
a candidate strict contextual core; if they separate, the cross-pair windows
must be charged as disjoint translated families.  Do not return to an
unlocated first-moment estimate.

**Crown quadratic span frozen:** FW234 counts every shed--retained pair at
the unique heavy-spine level where it separates.  Those disjoint pair
families have total `s_c^2/2-O(k^(3/2))`, yet their distance windows differ
only by twice the LCA-spine displacement.  Therefore the weighted crown spine
has length `s_c^2/4-O(k^(3/2))`, uniformly at least
`k^2/16-O(k^(3/2))`.  On the minimum-defect boundary its coefficient is
already `0.1578--0.1952`.  The next proof should classify the relative
orientation of this path and FW233's `k^2/4-O(k)` pole cone using their
minimal connecting subtree.  Opposite arms should be charged to one near-top
cross interval; nested arms should expose the candidate smaller contextual
component.

**Separated alignment frozen:** FW235 first takes the actual heavy-child
half-tree at the crown gate, then applies the direct-sum count against the
actual common-direction pole side.  If they are disjoint, `h_c d_out`
distinct cross distances fit in only `W+q_K+1<=W+L` slots.  The same inequality rules out a wholly transverse
pole attachment before the heavy retained order falls to
`floor((W+L)/d_out)`.  Conservative all-order exclusion begins at core orders
`147464,279948,524298` in the three low-defect rows.  The next pass must now
work inside the two surviving geometries—nested sides or opposing overlap—
and extract either a shared-corridor collision or a strictly smaller
contextual state.  FW235 does not close the separate high-defect branch.

**Aligned carrier frozen:** FW236 treats the remaining nesting/opposing
overlap without pretending it is already descent.  Nested sides have a
proper container carrying both full selected populations.  In opposing
overlap, the exclusive cross sets satisfy `xy<=W+L`; a balanced exact split
therefore gives a proper side carrying either all pole neighbours plus
`h-O(k^(3/4))` crown marks, or all crown marks plus
`d-O(k^(1/4))` pole neighbours.  The next pass must preserve enough of the
FW224 coefficient provenance inside this carrier to re-create a q=1 return,
or prove that failure of such inheritance consumes more holes than the
discarded `O(k^(3/4))`/`O(k^(1/4))` allowance.

**Diameter endpoint anchored:** FW237 uses the fixed-diameter domination
already available for the outlier graph.  One diameter endpoint has at least
half the minimum active-vertex count, hence `Omega(sqrt(k))` outlier
neighbours; their cone is a fixed diameter prefix.  Deleting this leaf gives
the exact order-`k-1` carrier and loses at most one crown mark.  The resulting
cone--crown alignment thresholds are only `1448,2496,3978`.  The active
problem is therefore sharply isolated: compute the exact spectrum change
under this one endpoint deletion and either recover a smaller four-factor
state or show that its missing top block consumes more than the FW225 defect.

**Old-threshold outliers peeled:** FW238 repeats the anchored diameter-leaf
deletion at the fixed old threshold `C`.  The exact potential
`ceil(2 sqrt(2 theta))` bounds the number of deletions by
`O(sqrt(delta))=O(sqrt(k))`.  The result is a connected
`k-O(sqrt(k))` core with no old-`C` outlier and an exact telescoping sum of
nested endpoint rooted factors accounting for every removed coefficient.
The next pass should not discard that factor order: either show two of these
nested rooted supports collide with the FW224 cap/core factors, or renormalise
at `C_0=binom(|K_0|,2)` and prove that the new defect exponent cannot climb
toward two while the crown spine loses only sublinear mass.

**Immediate renormalisation frozen:** FW239 deletes only the first anchored
leaf and resets at `binom(k-1,2)`.  The new defect is an exact old-hole plus
endpoint-pair count.  It is either linear, or a half-order shell in width
`O(k)` forces its heavy path to follow the outlier pole until a shared
`k^2/16-O(k^(3/2))` path has been certified.  This works in the former
high-defect branch as well.  The next pass should attack the resulting exact
dichotomy, not repeat the all-old-threshold peel: derive a collision/absorption
from the common path, or show that the linear new defect strictly decreases a
well-founded normalised state.

**Normalised prefix provenance frozen:** FW240 restricts the original FW224
tiling after that leaf deletion.  The new prefix holes are still exactly one
fixed small interval plus three rooted factors.  Hence the linear-new-defect
branch has a single rooted supplier with linear mass and a connected
`k/(6a)-O(1)` ancestor ball in the new core.  The next pass should work with
that named translate and the FW239 common path; another carrier-size bound
would not use the new information.

**Endpoint half-ball/half-shell frozen:** FW241 partitions the deleted
endpoint factor itself.  At least half the vertices form either a connected
low supplier ball with quadratic rooted radius or the high shell with a
quadratic pole-aligned common path.  This is unconditional after the first
peel and supersedes further low/high-defect geometry splits.  The next pass
must use the translated hole values along this located object; another path
length estimate is explicitly out of scope.

**Nested threshold ledger frozen:** FW242 orders the FW219 visible vertices
by reflected coordinate and proves that they are successive diameter leaves.
After the unique top monomial is removed, their rooted factors are disjoint
inside `1,...,N-Q` and, together with `F_H+X^gR_p(H)`, fill that prefix
exactly.  This is the correct contextual inheritance state.  The tempting
shortcut of treating each intermediate deletion as a new Leech tree is
false because the first deletion also removes the unique internal owner of
`N-Q`.  The next pass must compress the ordered translated-depth ledger,
using the visible-component/cross-Sidon structure, or prove that no bounded
compression follows before attempting another normalisation.

**One-endpoint defect ball frozen:** FW243 observes that `T-x`, of order
`n-1`, has ambient excess exactly `|H_Q|` over its own perfect threshold.
The low holes are not arbitrary: they are the translate of one
ancestor-closed root ball in `H_Q`, and their number equals the high-outlier
count.  Taylor parity makes this number grow at least on the square-root
scale.  The next pass should use the shared rooted carrier against the
diameter-endpoint outlier cone; another unlocated defect count would lose the
new information.

**Linear one-endpoint compression frozen:** FW244 shows that the complement
of the defect ball is an almost-complete rooted shell and forces
`delta/m>=3-2sqrt(2)-o(1)`.  All outlier LCAs lie in the ball, and below the
half-defect threshold the active shell LCAs have quadratic coordinate span
there.  The next pass has only two legitimate branches: use this automatic
alignment to force a repeated coefficient/contextual descent, or treat
`delta>m/2` directly.  A bounded- or sublinear-defect catalogue is no longer
relevant.

**Two-end high-defect placement frozen:** FW245 couples the two endpoint
defects exactly.  One ball has at least half-order, and the two rooted-radius
intervals overlap on the diameter by `binom(m,2)-m`.  Absence of a common
path vertex forces a single quadratic edge with a two-vertex endpoint
wrapper.  The next proof target is therefore finite in geometry: exclude or
absorb that wrapper, then use a shared ball vertex to intersect the two
coefficient ledgers.  A third generic defect lower bound is out of scope.

**Wrapper closed/top cycle forced:** FW246 uses FW244 to rule out the
two-vertex wrapper from order 12 onward.  A shared diameter-path vertex is
isolated in the graph of all distances above `binom(n-1,2)`, while that graph
has exactly `n-1` edges, so it must cycle.  The next pass should classify a
shortest top cycle by the four-point tree metric and connect its gate(s) to
the shared low-hole vertex.  Further endpoint-defect counting is out of
scope unless it distinguishes those cycle forms.

**Top-cycle normal form frozen:** FW247 shows that the cycle always supplies
either a diameter top triangle or an induced diameter top rectangle; the
rectangle deficits satisfy `c=a+b`, while all triangle median arms are
quadratic.  The next pass must trace the globally unique paths of the small
deficits `a,b` (and `a+b`) relative to these gates.  It should end in a
coefficient collision or a proper contextual carrier with a strict measure;
another top-edge count or an unconstrained cycle classification is out of
scope.

**Ferrers upgrade frozen:** FW248 promotes the rectangle alternative to a
complete truncated direct-sum factorisation of the whole top band.  Its first
opposite digit is exactly `Q`, so this branch now meets the old mixed-radix
coefficient recursion.  The next pass must carry the actual rooted
parent/LCA realisations through that recursion (or obtain a collision from
their failure); enumerating abstract digit strings without the tree geometry
is out of scope.  The top-triangle branch remains a separate quadratic
tripod target.

**Popular-sum defect floor frozen:** FW249 uses exact shell-sum
multiplicities to force each endpoint defect ball to have order
`m/4-sqrt(m)/2+O(1)`.  This is an input to both FW248 branches, not a new
branch.  Subsequent parent/LCA scans must preserve these two large rooted
carriers rather than relaxing them back to the older `0.1715...m` floor.

**First Ferrers gate frozen:** FW250 shows that the first opposite digit
places `s=min(Q,m-Q)` visible vertices at consecutive quadratic radii from
one gate; they always share an initial trunk of length `m/4+O(1)`.  The next pass should
analyse the first branching layer of this crown together with FW219's many
visible components and cross-Sidon rule.  Treating the factor coordinates as
unembedded sets is now an avoidable loss.

**Quarter-core/uniform-trunk result frozen:** FW251 gives
`Q<=3m/4+O(sqrt(m))` and `s>=min(Q,delta_min(m))`.  On the Ferrers side the
corrected prefix size makes the linear common trunk unconditional.  The next
proof pass should press its first crown branching with the exact cross-Sidon
rule; there is no separate near-`C` no-trunk branch.

**First crown split frozen:** FW252 gives a proper child carrying at least
`s-2` marks and an exact linear crown-cross window with at most one hole.
The next pass has one named obstruction: locate the hole owner while retaining
unmarked vertices in the two edge sides.  If it is internal, record the
strict handoff; if it is cross, enlarge the rooted factor and prove that the
giant carrier remains one-sided.

**Triangle gate / large-Ferrers routing frozen:** FW253 puts every triangle
gate inside both endpoint balls and compresses equal-gate tips to a
linear-width quadratic pole fibre.  From `n=38`, the Ferrers side is only
`Q<=6` or FW252.  Subsequent work should therefore maintain three explicit
queues: constant-`Q` core, one-hole giant carrier, and triangle pole fibre;
no generic high-defect branch remains.

The exact finite scope must be kept separate.  The earlier Ferrers routing
does not cover four small-order exceptional rows:

```text
n=25: (Q,s,h)=(18,6,6),(19,5,5),
n=27: (Q,s,h)=(20,6,6),(21,5,5).
```

The corresponding order-18 exceptions are already excluded and the routing
is complete from `n=38`; no such row occurs at `n=36`.  The four displayed
rows remain a finite exceptional queue, not hidden consequences of the
large-order theorem.

**Small-Q finite interface frozen:** FW254 leaves exactly 27 first-LCA rows
for `Q=2,...,6`; every row has an order-`m-O(1)` linear-excess core and an
`m-O(1)` common trunk.  A bounded symbolic relaxation may now enumerate
attachment *types* at this trunk, but it must keep the unbounded core as a
parameter and may not report finite-prefix exhaustion as an all-order row
exclusion.

**Crown-free attachments separated:** FW255 proves that the crown owns a
complete radial shell and pushes every wholly new child across a second
linear gap.  The FW252 hole-owner analysis may now ignore third child types
near the active window and concentrate on unmarked vertices inside the giant
and one/two-mark sides.

**Opposing hole tails frozen:** FW256 extends the gap through the parent
direction and reduces every unmarked cross owner of the crown hole to one
exact negative/positive shift balance.  The next pass should apply the
existing two-sided carrier/alignment machinery to this balance; another
unlocated hole count would discard the new information.

**Opposing gateway frozen:** FW257 shows that an h-cross owner by two
unmarked vertices has one negative parent-side vertex and one positive
descendant-side vertex; the positive direction need not be crown-free.  A
specific edge on the fixed diameter segment `x--h` has weight at least
`2s-1` (and `3s-3` in the endpoint-pair row), and its cut separates `x`
from `h` and the whole crown.  Replacing this cut by a generic heavy-edge
bound would lose the fixed orientation.

**Complete first-owner interface frozen:** FW258 proves `H>=s` and exhausts
every possible owner of the first crown hole: unmarked h-cross, mixed
crown/unmarked h-cross, internal marked-side, rooted, and the two outside
marks.  In the opposing branch the owners have one exact slack parameter
`k>=0`, subject to the positive descendant shift `t_+(k)` not equalling the
globally absent FW219 coordinate `Q`.  This suppresses the `a=s-1` mixed row
when `Q=2s-2` and at most one slack value in each opposing row.  At an
admissible `k=0` the three named families tile a complete consecutive block;
for admissible `k>0` exactly two symmetric k-gaps remain.  The two gaps are only local
raw-coefficient gaps, not holes of an induced subtree.

**Slack stop-loss reached:** FW259 applies the first internal giant-child LCA
to those gaps.  On coordinate-admissible rows a gap branch requires `k>=s-2`
(or `s-3` in the endpoint row), with an admissible equality forcing a
singleton-versus-rest split.  Otherwise the
first LCA lies above an explicit linear floor.  This is genuine slack
consumption; the `t_+!=Q` filter only narrows the premise and does not change
the numerical bounds.  The long-trunk alternative has no inherited two-gap state
and no decreasing contextual parameter.  The primary slack-k subroute
therefore meets its predeclared stop condition rather than being extended by
more compatible span bounds.

**Small-Q fallback result:** FW260 classifies the `Q=2` visible forest as a
rooted `L2` twig or two singleton components and gives the exact two/three-root
core tilings.  Their `X=-1` specialisation recovers Taylor's square orders but
does not exclude them.

**Universal direct bridge:** FW261 observes that the original coordinate-zero
endpoint singleton itself always gives the FW224-shaped exact double peel,
without FW220--FW223 provenance and for every `Q>=2`.  Every `n>=5` candidate
therefore has an order-`n-2` core with paired spectral defect in a band of
length at most `2n-5`; if the endpoint neighbour remains visible, the defect
is at least `ceil((u+1)/2)`.  FW262 applies both rooted shell counts directly
and proves the sharp relaxed asymptotic floor
`delta/(n-2)>=10-4sqrt(6)-o(1)=0.202041...-o(1)`.  Thus the
original `Q=2,3` cases are no longer separate algebraic terminals, but the
two-root near-Leech state still lacks a topology-independent owner catalogue
or a closed second peel.

**Strict suffix peel refuted:** FW263 tests the most optimistic closure
proposal directly.  Deleting one or two non-root leaves removes at most
`2n-3` coefficients, so a terminal deleted interval would lie above
`N-3n+6`.  But it necessarily contains a true leaf-edge coefficient at most
`N-ceil(binomial(n-1,2)/2)`, strictly below that floor for every `n>=14`.
Therefore the incident rooted factor cannot be absorbed into one terminal
suffix while the original two roots remain fixed.  The next state must
retain/reroot that factor or use a proper cut whose many boundary translates
are compressed by new owner provenance.  This is a route obstruction, not an
order exclusion.

**Fixed-core singleton ledger retains three labels:** FW264 fixes
`K'=K-{alpha}` for a true core leaf `alpha` and labels external singleton
blocks by original actual pairs.
For `n>=10`, the two old endpoint edges and the peeled true-leaf edge are all
strictly below `C=binomial(n-2,2)`.  A next actual-pair prefix on the
order-`n-3` core still reaches at least `C`, so all three coefficients must
remain represented.  The old-`x` pair and the peeled incident pair no longer
exist inside the retained tree and cannot acquire new owners under global
distance uniqueness.  Thus the labels `zp,xr,alpha-a` must remain active,
possibly only as order-one ghosts.  This does not force three full algebraic
rooted factors.  Multi-vertex/fragmented caps, nonactual translates and core
exchange are outside scope.

**Trunk-cut ledger exposed:** FW265 proves universally that a cut cross
product is exactly `|A|` named rooted shifts and that, under distance
uniqueness, the refined internal/shift owner family is pairwise disjoint.
Counting that product as one factor therefore does not by itself certify a
decreasing owner-expanded measure.  FW265 does not show `|A|` is large at the
FW259 cut or that the retained prefix meets many shifts.

The authorised successor sprint tested both proposed restarts.  FW266 proves
that a new `x`-core whose complete positive internal term ends at or below the
old `M=N-Q` must leave at least `Q` vertices outside; raising the endpoint to
`N-e` recovers the old FW242 nested ledger.  FW267 proves that every one of
those `e` external vertices still participates in a unique actual-pair owner
below `N-e`.  These are **OBSERVED route obstructions**, not exclusions.

The final directed-hole test is now also complete.  FW268 gives every
entry-eligible visible leaf an exact two-external ledger with one named high
hole.  It then proves that ambient q=1 normalization is unique and that the
exchange core is not a smaller Leech tree.  The `L6` control has two rolling
leaves whose fixed-ambient actual-pair choices form an equal-size involution
control, not a certified contextual transition, while
the complete `Q=2,3` audit supplies finite entry syntax but no terminal force.
These are **OBSERVED interface/route obstructions**, not exclusions.

Current decision: preserve FW258--FW268 as the proved boundary and stop the
present q=1 bounded-cap/core-exchange/directed-hole route.  A future restart
is justified only by an FW259-specific rooted-ball/no-grazing theorem with an
inherited receiving prefix, or a total owner-equivariant contextual
normalizer with an explicit strictly decreasing fully charged potential and a
certified empty-owner terminal.  More span/density/moment constants alone do
not pass the milestone.  See `docs/q1-new-mechanism-sprint.md` and
`docs/q1-directed-hole-sprint.md`.

Stop condition: if a scalable tree-realised relaxation satisfies the q=1
band, boundary-component count, cross-Sidon relations, full-support
orientations and existing moment/Kruskal constraints while avoiding all four
outcomes, stop the periodic route and prepare the partial-results paper.

### M5. Finite computation only after structural compression

No generic order-25 run.  A finite pilot is authorised only after specifying
and auditing a completeness-preserving q=1 row-conditioned rooted-tree
realisation encoder.  The first pilot is one process, order 25 only, with a
hard memory cap and a predetermined state/time cap.  `found=0` at a cap is
`UNKNOWN`, not an exclusion.  Hoffman2, if later authorised, uses `sbatch`,
never `qsub`.

## Resource policy

- M0--M3 need no cluster.
- Use Sol Max for theorem and scope work; mechanical arithmetic may use a
  cheaper model only after the theorem statement is frozen.
- No local process may materialise combinations or large products.  Stay
  within roughly one quarter of available CPU/RAM unless a separate run is
  explicitly approved.
- Every SAT witness, old or new, must pass both repository checkers.

## Current theorem status

- **OBSERVED:** FW203--FW217 local chain and the corrected fully-blocked shell
  handoff.
- **OBSERVED:** FW218 after its verifier/certificate and proof audit pass.
- **OBSERVED:** FW219 completes M2 and the proved part of M3: the exact
  connected core/hole bijection, visible boundary-forest bounds and the
  all-LCA cross-Sidon relation.
- **LITERATURE:** Taylor's necessary order condition remains an imported
  theorem as recorded in the literature ledger.
- **OBSERVED negative diagnostic:** M3's proposed bounded total shedding is
  not implied by the current FW219/FW216 interface.
- **OBSERVED:** FW220 gives M4 a canonical strict local decrease
  `Q -> q_*<=O(sqrt(Q))` and classifies its thin/bidirectional entry.
- **OBSERVED:** FW221 gives a topology-independent three-entry catalogue for
  all returns through the original endpoint singleton when `Q>=4`.
- **OBSERVED:** FW222 gives the returned proper core an exact prefix with at
  most three fixed initial holes and an exact rooted polynomial interface.
- **OBSERVED:** FW223 gives an exact rooted-gap interval decomposition,
  anchors the last excess at `Q-a`, and separates visible-root returns from
  wrapper-free threshold-core returns.
- **OBSERVED:** FW224 gives an exact strict-size double-peel tiling whose
  holes are the rooted factor of the connected threshold core.
- **OBSERVED:** FW225 turns the double-peeled tree into an exact linear-defect
  near-Leech core with paired low holes and high outliers.
- **OBSERVED:** FW226 forces linear defect whenever the return root remains
  visible, routing bounded defect to the connected threshold core.
- **OBSERVED:** FW227 compresses every fixed-defect large-order return to one
  giant branch plus an explicit bounded one- or two-boundary wrapper.
- **OBSERVED:** FW228 transfers Taylor parity through the double peel and
  leaves only two bounded-defect Taylor/cap rows.
- **OBSERVED:** FW229 rules out bounded defect at unbounded order in every
  row and supplies exact linear defect floors.
- **OBSERVED:** FW230 gives the exact two-factor allocation, paired root-shell
  inequalities, and stronger rational asymptotic density floors.
- **OBSERVED:** FW231 compresses the paired non-low shells into one giant
  off-spine crown fibre unless the defect is at least half the core order.
- **OBSERVED:** FW232 turns that giant fibre into one linear heavy branch
  spine; only `O(sqrt(k))` positive-loss steps can fail to be genuine branch
  vertices.
- **OBSERVED:** FW233 localises all linear outliers to `O(sqrt(k))` poles and
  forces a quadratic common cone with a linear-weight edge.
- **OBSERVED:** FW234 forces the heavy crown LCA spine itself to have
  quadratic weighted span.
- **OBSERVED:** FW235 excludes separated and early wholly-transverse
  crown--pole placement at sufficiently large low-defect returns.
- **OBSERVED:** FW236 forces a proper aligned carrier retaining both rigid
  populations, with sublinear opposing-overlap loss.
- **OBSERVED:** FW237 anchors the outlier pole at a diameter leaf and gives
  an exact order-`k-1` carrier plus much smaller alignment thresholds.
- **OBSERVED:** FW238 removes every old-threshold outlier by only
  `O(sqrt(k))` nested diameter-leaf peels and preserves an exact multi-root
  polynomial partition.
- **OBSERVED:** FW239 gives the first immediate-normalisation dichotomy:
  linear new defect or a located quadratic pole--shell common path, uniformly
  across the old low/high-defect split.
- **OBSERVED:** FW240 retains a complete four-factor prefix after the peel
  and localises every linear new defect to one linear rooted supplier ball.
- **OBSERVED:** FW241 gives an unconditional half-ball/half-shell quadratic
  normal form for the deleted endpoint factor.
- **OBSERVED:** FW242 gives the threshold core an exact complete prefix
  ledger of nested external endpoint factors.
- **OBSERVED:** FW243 makes the one-endpoint near-Leech low defect a connected
  ancestor-ball translate and gives its Taylor square-root floor.
- **OBSERVED:** FW244 forces one-endpoint defect density at least
  `3-2sqrt(2)-o(1)` and aligns all outlier LCAs with the defect ball.
- **OBSERVED:** FW245 forces a half-order endpoint ball and reduces failure
  of two-ball vertex overlap to a two-vertex endpoint wrapper.
- **OBSERVED:** FW246 excludes that wrapper for `n>=12`, forces a shared
  central ball vertex and a cycle in the top-distance graph.
- **OBSERVED:** FW247 reduces that cycle to a diameter top triangle or an
  induced diameter top rectangle with additive deficits.
- **OBSERVED:** FW248 promotes the nontriangle side to an exact truncated
  Ferrers/mixed-radix top factor with first opposite digit `Q`.
- **OBSERVED:** FW249 strengthens each endpoint carrier to asymptotic defect
  density `1/4` by exact popular-sum layers.
- **OBSERVED:** FW250 realises the exact first Ferrers prefix as one
  consecutive quadratic crown at a common gate, with a uniform linear trunk.
- **OBSERVED:** FW251 gives a quarter-dense threshold core and a lower bound
  for the crown order; the Ferrers trunk is unconditional.
- **OBSERVED:** FW252 makes the first Ferrers crown split a giant proper
  carrier plus at most two marks and an at-most-one-hole cross window.
- **OBSERVED:** FW253 locates triangle gates in both endpoint balls and
  routes all `n>=38` Ferrers cases to `Q<=6` or FW252.
- **OBSERVED:** FW254 freezes the `Q<=6` first-crown interface to 27 rows on
  a linear-excess giant core with an `m-O(1)` trunk.
- **OBSERVED:** FW255 gives the `s>=7` crown an exact radial shell and
  separates every wholly crown-free child by another linear gap.
- **OBSERVED:** FW256 confines every crown-free direction to opposing shift
  tails and gives an exact balance for any unmarked cross hole owner.
- **OBSERVED:** FW257 turns such an owner into a located parent-side gateway
  edge on the fixed `x--h` diameter segment of weight at least `2s-1`, or
  `3s-3` in the endpoint-pair row.
- **OBSERVED:** FW258 exhausts the first crown-hole owner interface and gives
  the exact opposing slack-k blocks on the corrected domain `t_+(k)!=Q`,
  deleting at most one slack value per row.
- **OBSERVED:** FW259 forces either linear slack consumption or an explicit
  long first-LCA trunk on that narrowed domain, with unchanged numerical
  bounds; it also records why this is not a closed iteration.
- **OBSERVED:** FW260 gives the exact `Q=2` two/three-root core tilings and
  recovers, but does not strengthen, Taylor's order condition.
- **OBSERVED:** FW261 gives every `n>=5` candidate an exact direct
  endpoint-singleton order-`n-2` double-peel state, including `Q=2,3`.
- **OBSERVED:** FW262 forces spectral defect density at least
  `10-4sqrt(6)-o(1)=0.202041...-o(1)` in that direct two-root core.
- **OBSERVED:** FW263 proves that no one/two-leaf deletion can preserve the
  same fixed two-root state by absorbing every deleted coefficient into one
  terminal suffix at any order `n>=14`.
- **OBSERVED:** FW264 proves that the fixed-core singleton-boundary ledger
  after one true core-leaf peel at `n>=10` must retain the three original
  labels `zp,xr,alpha-a`, possibly as order-one ghosts.
- **OBSERVED:** FW265 proves the universal trunk-cut ledger and its exact
  `|A|` owner expansion; the current formal factor count does not by itself
  certify a bounded owner-expanded context.
- **OBSERVED:** FW266 proves the core-exchange top-band tradeoff
  `e<Q => M'>=N-e`; keeping `M'<=N-Q` forces at least `Q` external vertices.
- **OBSERVED:** FW267 proves that every external vertex has a uniquely owned
  incident coefficient below the near-full endpoint `N-e`; factor repackaging
  alone cannot make its actual-pair label disappear.
- **OBSERVED stop decision:** the q=1 route has reached a genuine
  gap-budget/long-trunk fork without a well-founded transfer; the direct
  two-root fallback, fixed-core peel, trunk cut and tested core exchanges all
  retain or grow owner-charged context.
- **UNVERIFIED:** owner transfer with a retained/rerooted incident factor,
  prefix locality/absorption, a bounded label merger, cap bundling or core
  exchange, directed-hole no-return, closure of FW224--FW267 into a collision
  or decreasing contextual transfer, every arbitrary Taylor order
  above 18, and the global G18 theorem.
