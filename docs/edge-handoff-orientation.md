# Edge-handoff orientation and the terminal sink

**OBSERVED theorem.** Every hypothetical Leech tree of order `n>=12` admits an
orientation of all its edges with a nonleaf sink. At a sink vertex `v`, every
incident branch has a bounded high-distance handoff in its complement. More
precisely, if `e_i=vu_i` has weight `w_i` and `B_i` is the component beyond
`u_i`, then `V(T)\B_i` contains a pair at one of the distances

```text
w_i+1, ..., w_i+10.
```

This turns the edgewise sumset theorem into a global descent/terminal
dichotomy. It does **not** yet exclude either terminal type, so the general
nonexistence theorem remains **UNVERIFIED**.

## Orientation proof

Deleting any edge of an order-`n` tree leaves component orders `a,b`, with

```text
ab >= n-1 >= 11.
```

The edge-cut handoff theorem in `docs/heaviest-edge-rigidity.md` therefore
supplies a pair of distance `w+h`, `1<=h<=10`, wholly in one of the two
components. Choose one such component and orient the edge toward it.

Every orientation of a finite tree has a sink: repeatedly follow an outgoing
edge; acyclicity forces the walk to terminate. A leaf cannot be a sink, since
the singleton component on its side of the incident edge contains no vertex
pair, so that edge must point away from the leaf. Hence every sink has degree
at least two.

If `v` is a sink, the edge `vu_i` points toward the component containing `v`,
which is exactly `V(T)\B_i`. Its selected handoff pair is therefore outside
the `i`th branch, as claimed. `QED`

## Thick multiplicity at the next Taylor orders

The finite-hole ladder strengthens the orientation. At every edge, cut product
thresholds `21,35,44` force at least `3,7,9` holes by offsets `22,40,51`.
Orient the edge toward a side containing a majority of those within-component
pairs. At a resulting sink, every incident branch complement contains at
least

```text
order 25 or 27:  2 pairs by offset 22;
order 36 or 38:  4 pairs by offset 40;
order 49 or 51:  5 pairs by offset 51.
```

For a fixed edge, these pairs have distinct values and hence are distinct
global vertex pairs. Selections made for different edges need not be disjoint:
overlapping windows may reuse the same global pair. The multiplicity statement
is therefore an edge-by-edge statement, not a sum over all incident edges.

## The two remaining terminal geometries

The sink has one of two forms.

1. `deg(v)>=3`: a genuine thick branch centre. For every incident branch,
   several near-edge-weight distances live in the union of the other branches.
   This is the intended interface to weak-Sidon and merge-waste bounds.
2. `deg(v)=2`: a bidirectional corridor. Each of the two incident edges has a
   bounded handoff in the rooted half on the other side of `v`. A proof must
   either push one handoff into a nested proper side or show that the two
   opposing handoffs create a collision/branch accumulation. The selected
   handoff pairs on the two sides are necessarily different, because their
   allowed vertex sets intersect only in `{v}` and a pair needs two vertices.

The former interval-inheritance problem is absent here: the handoff theorem is
re-applied using the global Leech interval at each new edge. What remains is
to prove that the orientation yields strict nested descent, or that its sink
configuration violates the arithmetic bounds.

The finite computations underlying the theorem have two independent audits:
`theory-lab/topwindow/verify_heaviest_edge_rigidity.py` and
`theory-lab/topwindow/verify_heaviest_handoff_cleanroom.py`; the multiplicity
ladder is checked by
`theory-lab/topwindow/verify_heaviest_excess_ladder.py`.

## Canonical terminal component

The arbitrary choice made when an edge has handoffs on both sides can be
removed. Say that an edge *supports* a direction when its target side contains
a pair of distance `w+h`, `1<=h<=10`, and call the edge *bidirectional* when it
supports both directions. Contract every connected component of bidirectional
edges. Every remaining quotient edge supports exactly one direction, so the
quotient is a finite directed tree and has a sink component `C`.

Every boundary edge of `C` points into `C`. A leaf edge can never be
bidirectional and points away from its singleton leaf side, so `C` contains no
global leaf. It follows that exactly one of the following holds.

1. `C` contains a vertex of degree at least three: this is the genuine thick
   terminal.
2. Every vertex of `C` has degree at most two: `C` is a path, possibly a
   single degree-two vertex, with all boundary arrows pointing inward. Every
   internal edge of a nontrivial such path is bidirectional.

This is a canonical version of the thick-centre/corridor dichotomy: it does not
depend on how bidirectional edges were oriented.

A bidirectional edge has two *different* holes among `w+1,...,w+10`, one on
each side. The values must differ because the two side pairs are distinct and
all global distances are distinct. Consequently

```text
E_e>=2, and the first two hole offsets have sum at most 19
```

on every internal edge of a nontrivial terminal corridor. This improves the
unoriented second-hole bound 19 to 10 on those edges.

## Full-window canonical terminal

The same canonical construction can use the entire available window.  Say
that a side of an edge of weight `w` has *full support* when it contains an
internal pair of distance greater than `w` (necessarily at most the Leech
maximum `N`).  The offset-10 handoff theorem guarantees that every edge has
at least one fully supported direction.  Contract all edges with full support
on both sides and take a sink component of the resulting directed quotient.

FW282 strengthens this last sentence.  The full-window quotient has
outdegree at most one at every node and therefore has a **unique** sink; its
boundary weights strictly increase toward that sink, and every component
away from it is a strict thin cap.  A non-singleton branched sink reduces at
any core leaf to an exact two-colored owner tiling whose first same-side hole
has offset at most ten.  The proof, actual pressure control and precise
remaining LPCT boundary are in
`docs/full-window-quotient-arborescence.md`.  This strengthening is specific
to full support and does not make the offset-10/20 handoff orientations
canonical.

FW283 subsequently freezes the bounded one-leaf-port continuation: an exact
affine pressure family keeps the extremal offset-10 prefix while sending its
first actual owner gate arbitrarily far from the cut root.  LPCT remains open;
the required new mechanism must couple two actual sink ports.  See
`docs/leaf-port-colored-tiling-stop.md`.

FW284 constructs that coupling on the complete full-window skeleton.  Each
first compensated owner makes a strict cap lift or an actual owner-return
across a named skeleton edge, so the finite transition map contains a
lift/drop cycle.  Its scalar balance does not exclude the real L6 cycle; the
remaining NSSC obligation is endpoint monodromy on a nontrivial core
connector.  See `docs/skeleton-first-owner-cycle.md`.

FW285 strictly stops the direct endpoint-composition continuation.  FW284
defines `q->tau(q)` but no canonical `P_q->P_(tau(q))`; actual non-Leech
pressure trees with nontrivial sinks realise total cycles with vertex-disjoint
successive owners.  This does not refute NSSC.  The next live all-order input
must recover connector-crossing owner overlap from full coefficients discarded
by the one-record-per-edge compression.  See
`docs/skeleton-endpoint-monodromy-stop.md`.

FW286 extracts the first such full-spectrum consequence for path drops.  In
the two-cut decomposition `A--q--B--r--C`, endpoint-edge promotion gives
`w_r>=eta_q+1`, so the complete translated band is forced to be `AB` through
offset `eta_q-1` and `BC` at `eta_q`; `AC` cannot occur in the band.  The
remaining local path-drop target is only the terminal adjacent `AB -> BC`
connector theorem.  Cap-lift transport and later cycle composition remain
unverified.  See `docs/two-cut-terminal-owner-switch.md`.

FW287 gives exact crossed-swap and four-point identities for that terminal
pair.  Injectivity yields four integral projection/height cones, and the
critical endpoint-edge bound excludes the whole left-projection cone without
a connector-root exception.  The locally realized `R,D,U` modes now form the
precise remaining path-drop transport obligation.  See
`docs/terminal-four-cone-reduction.md`.

FW288 proves the exhaustive one-path-drop output: a direct shared endpoint,
an earlier `AB` bridge, an oriented marked connector interval, or a
sub-source-weight `BC` bridge.  The remaining path-drop issue is composition
of that typed record with the next skeleton arc, not local record existence.
Cap-to-boundary transport remains separate.  See
`docs/terminal-local-transport.md`.

FW289 reduces that separate cap-lift problem to shallow endpoint transport or
a remote--remote cap rectangle.  The target first prefix cannot exclude the
remote state: an actual non-Leech control keeps all four rectangle cross
distances inside the pair cap.  The live cap target is full-spectrum Remote
Cap Rectangle Transport.  See `docs/cap-endpoint-depth-stop.md`.

FW290 proves the path-drop target fork: equality of the target first offset
with the returned old-edge offset is the exact edge-lift two-cycle; strict
inequality yields a sub-source next owner.  A following cap lift can still
jump above the source, so cycle composition must join strict output to the
FW289 cap rectangle rather than use scalar descent.  See
`docs/pathdrop-target-owner-fork.md`.

FW291 turns the exact-return two-cycle into the correlated owner strip
`BC^delta AB^eta BC`.  The strip and connector matching are locally
insufficient: `L6` supplies complete coverage with a singleton sink, while
non-Leech controls supply nontrivial connectors.  ERTC must use global
extension outside the strip.  See `docs/exact-return-switchback-stop.md`.

This gives a stronger **OBSERVED reduction** for a singleton degree-two sink,
used inside the smallest-counterexample proof.
Let its incident weights be `p<q`, and write `A,B` for the components beyond
the `p`- and `q`-edges respectively.  Since the two boundary arrows point into
the singleton, their opposite sides have no full support:

```text
diam(A)<p,  diam(B)<q.                              (FW1)
```

Every edge internal to `A` or `B` is itself an internal distance.  Hence all
edges of `A` are lighter than `p`, all edges of `B` are lighter than `q`, and
`q` is the globally heaviest edge.  The `q`-edge can point inward only because
some pair in `A union {v}` exceeds `q`; (FW1) says that pair must have the form

```text
p+d_A(u,x)>q.                                      (FW2)
```

Here `u` is the endpoint of the `p`-edge in `A`.

Neither outer side can be a singleton in a smallest counterexample of order
at least 18.  Side `A` cannot be a singleton directly from (FW2).  If `B` were
a singleton, then `q` would be a leaf edge and all edges before `p` would form
the connected tree `A`.  Put `i=|A|` and `C_i=binom(i,2)`.  The forcing lemma
and the fact that every distance of `A` is below `p` give opposite ceilings

```text
p-1 <= C_i,       C_i <= p-1.
```

Thus `p=C_i+1` and `dist(A)={1,...,C_i}`: `A` is a proper smaller Leech tree.
If `n=18`, then `i=16`, contradicting the known order-16 exclusion.  The next
Taylor-admissible target order is 25, so every other case has `i>=23` and
contradicts minimality directly.

Consequently every surviving full-window singleton terminal has

```text
|A|>=2, |B|>=2, q is globally heaviest,
and deleting q leaves exactly two nontrivial light components.              (FW3)
```

The fragmented alternative in (FW3) is impossible as well.  Immediately
before the globally heaviest edge `q` is inserted, the two components are
`A union {v}` and `B`.  Put `r=q-p`.  Their rooted distance sets at the
endpoints of `q` are

```text
X={0} union (p+R_A),       Y=R_B,
```

where `R_A={d_A(u,x):x in A}` and `R_B` is defined analogously.  The forcing
lemma says that the pre-`q` forest contains `1,...,q-1`.  Let `E` be the
number of its distances greater than `q`.  By (FW1), all such distances are

```text
p+d_A(u,x),  d_A(u,x)>r,
```

so `E<=a-1`, where `a=|A|`.  After subtracting `q`, the cross sums `X+Y`
uniquely cover `0,...,N-q` except for the `E` holes

```text
d_A(u,x)-r,  d_A(u,x)>r.                           (FW4)
```

Every hole in (FW4) lies strictly between `0` and `p`: indeed
`d_A(u,x)<=diam(A)<=p-1`.  Also `p+q<=N`, since the two adjacent edges form a
path, so the whole interval `0,...,p-1` is in range.  Every non-hole `k<p`
has a representation `k=x+y`; the least positive member of `X` is `p`, hence
that representation must be `0+k` and `k in Y`.  Therefore

```text
b=|Y| >= p-E >= p-a+1,
p <= a+b-1=n-2.                                    (FW5)
```

The `binom(a,2)` distances inside `A` are distinct and below `p`, giving

```text
binom(a,2)<=p-1<=n-3.                              (FW6)
```

Furthermore (FW2) gives `r<=p-2`, so
`q=p+r<=2p-2<=2n-6`.  The distances inside `B` are distinct and below `q`,
hence

```text
binom(b,2)<=q-1<=2n-7.                             (FW7)
```

For `n>=18`, (FW6) forces `a<=n/3`: otherwise monotonicity of
`x(x-1)/2` and

```text
binom(n/3,2)-(n-3)=(n-18)(n-3)/18 >= 0
```

would contradict (FW6).  Similarly (FW7) forces `b<=n/2`, because

```text
binom(n/2,2)-(2n-7)=(n-14)(n-4)/8 > 0.
```

But `a+b=n-1`, whereas `a+b<=5n/6<n-1` for `n>6`, a contradiction.

Thus the full-window canonical sink component of a smallest hypothetical
order-`n>=18` Leech tree can never be a single degree-two vertex.  This is
exactly what the global minimal-counterexample argument needs, and closes both
the nonfragmented and fragmented singleton branches at all target orders,
without needing an all-order classification of the fixed-20 prefix-defect
core.  At this stage the only remaining degree-two terminal is a **nontrivial path of
full-bidirectional edges**; the alternative terminal contains a vertex of
degree at least three.  The finite-set implication in (FW5), the two quadratic
thresholds and every integer outer-order pair through order 10,000 are audited
by `theory-lab/topwindow/verify_full_window_singleton.py`; the factorisations
in the displayed proof cover all larger orders.

## Exact form of the remaining nontrivial corridor

If the full-window sink component has no degree-at-least-three vertex and is
not a singleton, it has the unique bare-chain form

```text
A --e_0-- v_0 --e_1-- ... --e_k-- v_k --e_{k+1}-- B,   k>=1.       (FW8)
```

Here `A,B` denote the two outer rooted components, all `v_j` have global
degree two, the internal edges `e_1,...,e_k` have full support on both sides,
and the two boundary arrows point inward.  Therefore

```text
diam(A)<e_0,  diam(B)<e_{k+1}.                       (FW9)
```

Every edge internal to `A` is below `e_0`, and every edge internal to `B` is
below `e_{k+1}`.  Consequently the globally heaviest edge `q` lies on the
displayed bare chain, including its two boundary edges.

Deleting `q` gives rooted components `L,R` of orders `ell,rho`, with rooted
distance sets `X,Y`.  Since `q` is the last edge in forcing order, the
pre-`q` forest contains `1,...,q-1`.  If

```text
E=binom(ell,2)+binom(rho,2)+1-q,
```

then the exact complement relation is

```text
X+Y = {0,...,N-q} minus
      {d-q : d>q is an internal distance of L or R}.                (FW10)
```

All sums in `X+Y` are unique and the deleted set has exactly `E` elements.
If `q` is internal to the sink path, full bidirectionality says that (FW10)
has at least one deleted offset contributed by each side; if `q` is a boundary
edge, all deleted offsets occur on its inward side.  Thus the last unresolved
degree-two problem is no longer an arbitrary corridor: it is the near-interval
unique-sum factorisation (FW10), with the globally heaviest edge on a bare
chain and with holes on the side(s) prescribed by full support.  Turning
(FW10) plus the finite-hole ladder into a contradiction remains
**UNVERIFIED**.

There is a further metric amplification.  A component on either side of an
internal corridor edge is an outer component satisfying (FW9) with a bare
path appended.  Its maximum internal distance is therefore realised from the
corridor endpoint: moving an endpoint outward along the bare path can only
increase the distance, while pairs wholly in the outer component have weight
below the boundary edge and hence below `q`.  If the globally heaviest `q` is
internal to the sink path, full support on both sides gives rooted
eccentricities at least `q+1`, so

```text
N >= (q+1)+q+(q+1)=3q+2.                          (FW11)
```

If `q` is a boundary edge, the same argument on its inward side gives only
`N>=2q+1`.  Thus the remaining path splits into a boundary-heaviest case and
an internal-heaviest case with `q<=floor((N-2)/3)`.

For the latter, if deleting `q` gives orders `ell,rho`, the hole count in
(FW10) obeys the all-order lower bound

```text
E=N+1-ell*rho-q
 >= N+1-floor(n^2/4)-floor((N-2)/3).              (FW12)
```

Let `c` be the number of vertices of the full-window sink path.  No pair
wholly in either outer component can exceed `q`; consequently every one of
the `E` high internal pairs touches a corridor vertex.  Hence

```text
E <= c(n-c)+binom(c,2)=cn-c(c+1)/2.               (FW13)
```

Equations (FW12)--(FW13) force
`c >= (1-sqrt(5/6)+o(1))n`, approximately `0.087n`, whenever the heaviest
edge is internal.  This does not yet contradict the available path-length bounds,
but it already rules out a bounded-size internal terminal.  The reflected
factorisation below strengthens the constant further.

The same geometry also gives an exact no-hole condition at the *top* of the
distance interval.  Let `lambda=max X` and `mu=max Y` be the rooted
eccentricities of the two components obtained by deleting the corridor
maximum `q`.  The path-appended argument above gives

```text
diam(L)=lambda,  diam(R)=mu,  N=q+lambda+mu.
```

Every value above `max(lambda,mu)` is therefore cross.  Reflect the rooted
sets at their maxima,

```text
X*={lambda-x:x in X},  Y*={mu-y:y in Y}.
```

Distance uniqueness and the complete Leech interval imply the **OBSERVED
top-prefix factorisation**

```text
{0,...,q+min(lambda,mu)-1} subset X*+Y*,           (FW14)
```

with every displayed sum represented exactly once.  If `q` is internal,
`lambda,mu>=q+1`, so (FW14) has at least `2q+1` consecutive values and in
particular `q+min(lambda,mu)` representations.  The original sumset also
contains `0`; equivalently the reflected sumset contains the separate endpoint
`lambda+mu`, outside (FW14).  Counting that additional representation gives

```text
ell*rho >= q+min(lambda,mu)+1 >= 2q+2,
hence q <= floor((ell*rho-2)/2).                    (FW15)
```

Substituting (FW15) in the exact excess identity (FW10), and using
`ell*rho<=floor(n^2/4)`, sharpens (FW12) to

```text
E >= N+1-floor(n^2/4)
       -floor((floor(n^2/4)-2)/2).                 (FW16)
```

Together with (FW13), this forces
`c >= (1-sqrt(3)/2+o(1))n`, approximately `0.134n`.  Thus the two cases left
at this intermediate stage were a boundary-heaviest near-factorisation or a
linearly long bare corridor; (FW35) below subsequently removes the latter
internal-maximal branch completely.
The exact strengthened excess and minimum corridor orders through 10,000,
including the next Taylor orders, are audited by
`theory-lab/topwindow/verify_full_window_corridor.py`.  If `q` is a boundary
edge, (FW14) has length
`q+lambda`, where `lambda<q` is the eccentricity of its outer component.
Let `a` be the order of that outer component.  Its `binom(a,2)` internal
distances are distinct positive integers, so its diameter is at least
`binom(a,2)`.  The rooted depths are also distinct, so only one vertex can
have depth `lambda`; for `a>=2` every pair is therefore at distance at most
`2lambda-1`.  Put `r(1)=0` and
`r(a)=ceil((binom(a,2)+1)/2)` for `a>=2`; then `lambda>=r(a)` in every case.
Counting the prefix and the separate reflected endpoint, exactly as in
(FW15), gives

```text
a(n-a) >= q+lambda+1
       >= q+r(a)+1,
q <= a(n-a)-r(a)-1.                               (FW17)
```

All above-`q` internal distances are now on the inward side.  Substitution in
(FW10) yields the all-order boundary lower bound

```text
E >= N+2-2a(n-a)+r(a).                            (FW18)
```

The quadratic in (FW18) is minimised at
`a=(4/9+o(1))n`, where it is `(1/18+o(1))n^2`.
Every above-`q` inward pair still touches a corridor vertex, because pairs
wholly in the far outer component have distance below its boundary edge and
hence at most `q`.  Combining (FW18) with (FW13) therefore forces

```text
c >= (1-sqrt(8/9)+o(1))n,
```

approximately `0.057n`.  Thus, before (FW35), both locations of `q` forced a
linearly long bare corridor (with the stronger `0.134n` constant when `q` was
internal).  The boundary lower bound remains load-bearing after (FW35).

The two outer components sharpen both constants substantially.  Write their
orders as `a,b`.  Every internal distance wholly in either outer component is
below its boundary edge and hence below `q`.  These distances are globally
distinct.  The chain has `c+1` edges, and its `c` edge weights other than `q`
are further distinct distance values below `q`.  None can duplicate an outer
internal distance.  Thus all these values occupy distinct members of
`{1,...,q-1}` and

```text
q >= binom(a,2)+binom(b,2)+c+1.                   (FW19)
```

If `q` is internal, (FW15) and `ell*rho<=floor(n^2/4)` give

```text
binom(a,2)+binom(b,2)+c+1
 <= floor((floor(n^2/4)-2)/2).                    (FW20)
```

For fixed `a+b=n-c`, the left side is smallest when `a,b` are as balanced as
possible.  Consequently

```text
c >= (1-1/sqrt(2)-o(1))n,
```

approximately `0.293n`.  This dominates the earlier excess-capacity constant
`0.134`.

If `q` is the boundary next to the order-`a` outer component, combine (FW17)
and (FW19):

```text
binom(a,2)+binom(b,2)+c+r(a)+2 <= a(n-a).         (FW21)
```

Put `x=a/n`, `y=b/n`, and `z=c/n`.  After division by `n^2`, every sequence
of survivors must satisfy asymptotically

```text
3x^2/4+y^2/2 <= x(1-x).
```

The maximum of `x+y` occurs at

```text
x=(6+2sqrt(2))/21,  y=sqrt(2)/3.
```

Thus

```text
c >= ((5-3sqrt(2))/7-o(1))n,
```

approximately `0.108n`, improving the earlier boundary constant `0.057`.
The verifier computes the exact integer outer-order bounds at the displayed
target orders as well as both asymptotic optimisations.

There is a further **OBSERVED multiscale stability bound** when `q` is
internal.  Put

```text
Q=floor((floor(n^2/4)-2)/2),
B(s)=binom(floor(s/2),2)+binom(ceil(s/2),2),
h=q-1-binom(a,2)-binom(b,2)-c.
```

Here `h>=0` counts low, corridor-related distances other than the `c` chain
edge weights.  If

```text
D=binom(a,2)+binom(b,2)-B(n-c),
u=floor((ell*rho-2)/2)-q,
t=Q-floor((ell*rho-2)/2),
```

then all four terms are nonnegative and the exact **slack identity** is

```text
Q-[B(n-c)+c+1] = D+h+u+t.                         (FW22)
```

This identity makes near equality rigid: it simultaneously bounds the outer
order imbalance, the low corridor slack, the top-prefix slack and the
imbalance of the cut at `q`.

The path geometry forces `h` itself to be large.  First use the fact that the
two outer components live in the same globally distinct-distance tree.  Put
`C_a=binom(a,2)` and `C_b=binom(b,2)`.  If their rooted eccentricities are
`lambda_A<=lambda_B`, then the `C_a` distances in the first component are at
most `2lambda_A-1`, while all `C_a+C_b` internal distances in their disjoint
union are at most `2lambda_B-1`.  Interchanging the components if necessary
gives the joint lower bound

```text
J(a,b)=ceil((C_a+C_b+1)/2)+min(r(a),r(b)),         (C_a+C_b>0),
J(1,1)=0.
```

This is stronger than treating the two radii independently.

Delete `q`; its other `c` chain edges form two nonempty path segments.  If
their total weight is `W`, joining farthest vertices of the two outer rooted
components gives

```text
W <= N-q-J(a,b).
```

For each `k>=2`, the two segments contain at least
`max(c-2k+2,0)` length-`k` windows.  The sum of all such window weights is at
most `kW`, so at most `floor(kW/(q+1))` can exceed `q`.  Every remaining
window is a distinct non-edge distance counted by `h`.  Therefore

```text
h >= sum_{k>=2} max(0, c-2k+2
                       -floor(k[N-q-J(a,b)]/(q+1))).               (FW23)
```

For the limiting calculation orient the split so that `x=a/n<=y=b/n`, put
`z=c/n` and `beta=(x^2+y^2)/2`.  The joint root span has leading term
`R=(2x^2+y^2)/4`.  Combining (FW22)--(FW23), and using the largest permitted
internal weight `q/n^2=1/8`, gives the necessary inequality

```text
(1/8-beta)[10-4(2x^2+y^2)] >= z^2.               (FW24)
```

An exact rational monotonicity and strong-concavity certificate proves that
(FW24) has no feasible point for `z<=329/1000`.  Hence

```text
c >= (329/1000-o(1))n = (0.329-o(1))n.           (FW25)
```

The proof writes `x=(1-z)/2-d`, observes that the left side of (FW24) is
increasing in `z` on its feasible domain, and at `z=329/1000` bounds its
second `x`-derivative by `-17`; the final rational tangent upper bound has
numerator `-5100826409341295611`.  The exact relaxed integer calculation,
which scans the actual outer split rather than minimizing its two terms
separately, gives internal minimum corridor orders
`6,8,9,12,12,16,16,21` at `n=18,25,27,36,38,49,51,64`.
Verifier and frozen summary:

```text
theory-lab/topwindow/verify_corridor_window_stability.py
theory-lab/topwindow/results/corridor_window_stability_certificate.json
```

There is an analogous, and slightly sharper, **OBSERVED one-segment bound**
when `q` is the boundary edge next to the order-`a` outer component.  Keep the
same definition of `h`.  The upper bound (FW17) gives the exact slack cap

```text
h <= a(n-a)-binom(a,2)-binom(b,2)-c-r(a)-2.       (FW26)
```

After deleting `q`, the other `c` corridor edges now form one segment rather
than two.  If their total weight is `W`, farthest rooted vertices in the two
outer components give

```text
W <= N-q-J(a,b).
```

There are exactly `c-k+1` length-`k` windows in that segment.  The same
total-weight argument as above therefore gives the stronger exact inequality

```text
h >= sum_{k>=2} max(0, c-k+1
                       -floor(k[N-q-J(a,b)]/(q+1))).               (FW27)
```

For the limiting calculation put `x=a/n`, `y=b/n`, `z=c/n`,

```text
beta=(x^2+y^2)/2,       u=x-5x^2/4.
```

If `theta=q/n^2`, the Riemann sum of (FW27) and the joint root span give a
low-window density at least
`z^2 theta/[1-beta-min(x^2,y^2)/2]`.  Since `beta<=theta<=u`, a survivor must
satisfy

```text
(u-beta)[1-beta-min(x^2,y^2)/2] >= z^2 u.         (FW28)
```

An exact rational calculus certificate proves that even the weaker right
side `z^2 beta` is impossible for `z<=29/250`.  It treats the two branches of
the minimum separately, uses monotonicity in `z`, and applies a rational
strong-concavity tangent bound at `z=29/250`; the final upper-bound numerator
is `-1581606834549019`.  Consequently

```text
c >= (29/250-o(1))n = (0.116-o(1))n.              (FW29)
```

in the boundary-heaviest case.  The exact relaxed target-order minima are
`2,2,3,4,4,5,5,7` at `n=18,25,27,36,38,49,51,64`; the positive forced
low-window slacks now first appear in these rows at `n=27`.  Verifier and frozen
summary:

```text
theory-lab/topwindow/verify_boundary_corridor_window_stability.py
theory-lab/topwindow/results/boundary_corridor_window_stability_certificate.json
```

There is also an **OBSERVED upper bound** on the same corridor, independent of
which chain edge is maximal.  Include the roots of `A,B` with the `c`
corridor vertices and write their cumulative chain positions as

```text
0=t_0<t_1<...<t_{c+1}=S.
```

Every positive difference `t_j-t_i` is a different global tree distance, so
these `c+2` positions form a Golomb ruler.  The following elementary
Erdos--Turan estimate is included here for completeness.  Fix
`1<=v<c+2` and take all differences with index gap at most `v`.  Their number
is

```text
K=v(c+2)-v(v+1)/2.
```

They are distinct positive integers, so their sum is at least `K(K+1)/2`.
Each adjacent ruler gap occurs in at most `v(v+1)/2` selected differences;
therefore their sum is at most `v(v+1)S/2`.  Hence the exact necessary
inequality is

```text
K(K+1) <= v(v+1)S.                               (FW30)
```

The chain span satisfies `S<=N-J(a,b)`: joining farthest vertices of the two
outer rooted components adds at least their joint root span to the chain.
Taking `v` to infinity more slowly than `c` in (FW30) gives asymptotically
`c^2<=S`.  If `s=(a+b)/n=1-z`, the exact square completion

```text
[(s-t)^2+2t^2]/4 = s^2/6+3(t-s/3)^2/4
```

shows that `J(a,b)/n^2>=s^2/6-o(1)`.  Consequently

```text
z^2 <= 1/2-(1-z)^2/6,
z <= (1+sqrt(15))/7+o(1) = 0.6961404780...+o(1). (FW31)
```

The globally maximal chain edge itself can be removed from this span.  If it
is a boundary edge, the other `c` edges form one Golomb ruler of span `W`.  If
it is internal, they form two rulers; their selected differences are still
globally distinct.  When both segment lengths are linear, apply the preceding
bounded-index argument to their union.  When one is sublinear, the longer
segment alone has `c-o(n)` edges.  Passing to a subsequence covers the
intermediate cases and gives, in either location of `q`,

```text
c^2 <= W+o(n^2) <= N-q-J(a,b)+o(n^2).
```

Put `s=(a+b)/n`, `t=min(a,b)/n`.  The lower bounds (FW19) and `J(a,b)` have
combined leading term

```text
[3(s-t)^2+4t^2]/4
  = 3s^2/7+7(t-3s/7)^2/4.
```

Consequently the preliminary (FW31) sharpens to

```text
z^2 <= 1/2-3(1-z)^2/7,
z <= (3+sqrt(14))/10+o(1) = 0.6741657387...+o(1). (FW32)
```

Equivalently, the two outer components together have at least
`((7-sqrt(14))/10-o(1))n`, approximately `0.326n`, vertices.  Thus the
remaining long-corridor problem has no sublinear-outer escape regime.  In
particular (FW19) and the balanced lower bound on the two outer pair counts
give the uniform quadratic maximum-edge bound

```text
q >= (((7-sqrt(14))/10)^2/4-o(1))n^2
  = (0.02654199146...-o(1))n^2.                  (FW33)
```

Thus the bottom finite-hole factorization and the reflected top prefix both
have positive quadratic scale in every surviving corridor; there is no
remaining `q=o(n^2)` regime.  The
exact relaxed upper corridor orders are `14,19,21,28,29,38,39,49` at
`n=18,25,27,36,38,49,51,64`; each next value violates (FW30), and the
corresponding exact lower bounds on `q` are `17,26,28,41,46,64,70,99`.
Verifier and frozen summary:

```text
theory-lab/topwindow/verify_corridor_golomb_upper.py
theory-lab/topwindow/results/corridor_golomb_upper_certificate.json
```

The missing degree-two step is now uniformly to exclude these still-longer
corridors using the simultaneous bottom finite-hole and top no-hole
factorizations.  Equations (FW22), (FW26)--(FW27) and (FW32) confine every
survivor to a genuinely linear corridor with a genuinely linear total outer
order; a descent must now exploit the two outer components separately.

One tempting relaxation is provably too weak.  The explicit rooted depth sets

```text
X=(0,28,29,30,34,35,36),
Y=(0,37,40,49,52,61,64)
```

admit rooted parent maps with distinct, mutually disjoint internal distance
sets and have 49 distinct cross sums.  After reflection their factors are

```text
X*=(0,1,2,6,7,8,36),
Y*=(0,3,12,15,24,27,64),
```

and `X*+Y*` contains every value `0,...,36` uniquely.  Hence rooted
realizability plus a `37/49` reflected-prefix density does not by itself imply
a collision.  This is only an **OBSERVED negative diagnostic**, not a Leech
witness: the joined order is 14, so the Leech diameter equation would require
`q=91-36-64=-9`, and the first positive unreflected cross sum is 28.  It
follows that the remaining argument must retain the positive scale equation
`N=q+lambda+mu` and the exact equality of the holes in (FW10), not merely a
lower bound on the size of the prefix in (FW14).  The calculation is audited
by `theory-lab/topwindow/verify_reflected_prefix_barrier.py`.

## A reflected-prefix dichotomy excludes an internal maximum

The missing scale condition makes the internal-maximal case rigid.  We first
record the elementary one-dimensional tiling fact that supplies the rigidity.

**Prefix reflection-gap lemma.**  Let `U,V` be finite subsets of the
nonnegative integers, both containing zero, and suppose every integer in
`0,...,T-1` has exactly one representation in `U+V`.  Put

```text
lambda=max(U)<T,        q=T-lambda,
g(U)=the largest gap between consecutive elements of U.
```

Then at least one of the following alternatives holds:

```text
U=lambda-U,             or             g(U)>=q+1.       (FW34)
```

Here the first equality is equality of sets.  For completeness, this is a
prefix, rather than a complete-interval, version of the usual mixed-radix
factorisation argument.  Scan coefficients from zero upward.  If the factor
containing `1` contains the initial digit block `0,...,r-1`, where `r` is the
first coefficient assigned to the other factor, every completely exposed
block of length `r` is owned by exactly one quotient factor.  Thus, after
discarding a possibly unfinished last block and scaling by `r`, the two
factors have one of the two forms

```text
[0,r-1]+rU',  rV'             or             rU',  [0,r-1]+rV'.
```

This statement follows directly by induction over a block: the translate
starting at `jr` covers the whole block `jr,...,(j+1)r-1`; inserting any
second owner inside that block gives two representations, while omitting an
entry leaves the first such coefficient uncovered.  Repeat on the quotient
factors.  The induction invariant is that an unfinished final quotient level
contributes a consecutive gap `d` to its owner and can remain compatible with
only `d-1` subsequent coefficients.  Indeed, before the translated block has
length `d` its uncovered entries can only be assigned at that same level; at
the `d`th coefficient, failing to finish the block leaves a hole, while
assigning it to the other owner duplicates the sum of the two block starts.
Thus, if the last block belonging to `U` is unfinished, its separation from
the preceding completed block satisfies `d>=q+1`, giving the second
alternative in (FW34).  Otherwise every digit
block belonging to `U` is complete.  Write `g'=g(U')` and let `Q` be the
visible quotient tail.  In the first displayed form

```text
g(U)=max(1,r*g'-(r-1)),
```

and in the second `g(U)=r*g'`; in both cases `Q=ceil(q/r)`.  Hence
`g(U)<=q` implies `g'<=Q`.  Induction reaches a singleton factor.  Every
complete digit block is symmetric about its own maximum, and direct sums of
such blocks are symmetric, proving `U=max(U)-U`.  This proves (FW34) at every
length, with no finite cutoff.

Now return to an internal corridor maximum `q`.  Delete that edge and choose
the side with smaller rooted eccentricity, say `lambda<=mu`.  Put

```text
U={lambda-x:x in X},        V={mu-y:y in Y}.
```

By (FW14), `U+V` represents `0,...,lambda+q-1` exactly once, so (FW34)
applies with the same `q`.  Every other edge weight is strictly below `q`,
because all tree distances, hence all edge weights, are distinct and `q` is
globally maximal.  Let `z` be a vertex at rooted depth `lambda`.  The path
from `z` to the root becomes, after reflection, a path from `0` to `lambda`
through elements of `U`, and every consecutive step is an edge weight below
`q`.

If the gap alternative in (FW34) holds, it disconnects `0` from `lambda` and
is impossible.  Hence `g(U)<=q`, so (FW34) forces `U=lambda-U=X`.  If `e<q` is the
first edge weight on the path from `z` toward the root, its parent has
reflected depth `e`, so `e in U=X`.  A vertex at rooted depth `e` therefore
exists.  The root-to-that-vertex pair and the first edge at `z` are distinct
pairs at the same distance `e`, a contradiction.  We have proved the new
all-order conclusion

```text
the globally maximal edge of a surviving bare corridor is a boundary edge.
                                                               (FW35)
```

This is an **OBSERVED theorem**, not a finite extrapolation.  A direct
coefficient recursion independently checks all 584,442 oriented prefix
factors arising through length 128: every nonsymmetric factor has gap slack
at least one, with no violation of (FW34).  Verifier and frozen summary:

```text
theory-lab/topwindow/verify_internal_corridor_reflection.py
theory-lab/topwindow/results/internal_corridor_reflection_certificate.json
```

Consequently all internal-maximal lower bounds (FW11)--(FW16), (FW22) and the
internal branch of (FW27) are now historical diagnostics rather than surviving
cases.  At this intermediate stage the degree-two endgame has been reduced to the boundary-heaviest
factorisation, where the smaller outer eccentricity satisfies `lambda<q` and
the internal-path contradiction no longer applies.

It does, however, rigidify that boundary component.  Let its order be `a` and
keep `X,U,lambda` for its rooted depths, reflected depths and eccentricity.
Now `lambda<q`, so every consecutive gap of `U` is at most `lambda<q+1`.
The gap branch of (FW34) is unavailable and hence

```text
U=lambda-U=X.                                      (FW36)
```

The same first-edge argument shows that a farthest vertex `z` is joined
directly to the boundary root by an edge of weight `lambda`; otherwise that
first edge repeats as a root depth.  The cases `a=1,2` and `a>=3` are then
sharply different.

If `a=1`, (FW17) gives `q<=n-2`, while the largest of the `n-1` distinct
positive edge weights is at least `n-1`.  Thus `a=1` is impossible.  If
`a=2`, the boundary component is exactly the single `lambda`-edge.  Since
`U={0,lambda}`, uniqueness of the reflected factorisation forces

```text
{0,...,lambda-1} subset V,       hence lambda<=n-2. (FW37)
```

This is the sole genuinely degree-two thin cap left at the boundary.

Finally suppose `a>=3`, and let `s` be the least positive rooted depth in
`X`.  Symmetry gives another vertex at depth `lambda-s` and
`s<=lambda-s`.  The `lambda`-vertex is a root leaf, so its distance from the
`lambda-s` vertex is `2lambda-s<q` by (FW9).  Therefore

```text
q >= 2lambda-s+1 >= ceil(3lambda/2)+1.             (FW38)
```

Moreover any third vertex must start in a root branch different from the
`lambda`-leaf, so the boundary root has global degree at least three (the
`q`-edge, the `lambda`-leaf and that additional branch).  Thus the surviving
boundary corridor is no longer an independent diffuse case: it is either the
explicit two-edge thin cap `a=2`, or it meets a degree-at-least-three thick
profile immediately across `q`.  The thin branch is closed below; excluding
the degree-at-least-three thick profile remains **UNVERIFIED**.

## The boundary thin cap is impossible

This is an **OBSERVED theorem** at every target order `n>=18`.  Continue with
the thin case `a=2`, let `b` be the order of the opposite outer component
`B`, and let `c` be the number of corridor vertices.  Thus `n=b+c+2`.
Equations (FW17) and (FW19) first give

```text
binom(b,2)+c+2 <= q <= 2n-6,
hence b(b-3)<=2n-12.                              (FW39)
```

Put `L=q+lambda`.  Since `U={0,lambda}`, coefficient uniqueness throughout
the reflected prefix says exactly

```text
t in V  iff  floor(t/lambda) is even,   0<=t<L.   (FW40)
```

In particular `V` alternates occupied and empty blocks, each of length
`lambda`.  If `A(s)=|V intersect {0,...,s-1}|`, counting the unique
representations in `U+V` gives `A(L)+A(q)=L`.  Hence
`A(L)>=ceil(L/2)>=ceil(n/2)`.  Meanwhile (FW39) implies `b<n/2` for
`n>=18`: otherwise

```text
b(b-3) >= (n/2)(n/2-3) > 2n-12,
```

where the last difference is `(n^2-14n+48)/4>0`.

Let `p` be the boundary edge entering `B` and let `theta` be the eccentricity
of its boundary root.  In the reflected set `V`, the vertices of `B` lie in
`[0,theta]`, while the nearest corridor vertex has reflected depth
`p+theta`; both endpoints belong to `V`, and no value strictly between them
does.  Since `A(L)>b`, some corridor vertex lies below `L`, so
`p+theta<L` and the exact block pattern (FW40) applies to this whole gap.

If `b=1`, both outer components and the corridor already make the whole tree
a path, impossible at order at least five.  Thus `b>=2`, so `theta>=1` and
`p>diam(B)>=theta` gives `p>=2`.  Two occupied points of (FW40) with a
nonempty interval of missing points between them must be the last point of
one occupied block and the first point of the next.  Therefore, for some
`j>=0`,

```text
theta=(2j+1)lambda-1,       p=lambda+1.            (FW41)
```

But (FW9) gives `theta<=diam(B)<p=lambda+1`, forcing `j=0` and
`theta=lambda-1`.  The distance `lambda` is already the outer cap edge, so
global uniqueness forbids it inside `B`; hence in fact

```text
diam(B)=theta=lambda-1.
```

Now `p+theta=2lambda`.  The first occupied block
`0,...,lambda-1` of `V` therefore consists entirely of vertices of `B`, so
`b>=lambda`.  On the other hand the `binom(b,2)` distinct positive internal
distances of `B` all lie in `1,...,lambda-1`, giving

```text
binom(b,2) <= lambda-1 <= b-1.
```

For `b>=2` this forces `b=2`, and then `lambda=2`, `theta=1`, `p=3`.
Both outer components are single edges and all corridor vertices have degree
two, so the entire tree is a path.  Since a Leech path has order at most four,
this is the final contradiction to the thin case.  Consequently every
surviving terminal configuration either contains a vertex of degree at least
three or meets one immediately across its boundary maximum.  The arithmetic
audit is

```text
theory-lab/topwindow/verify_boundary_thin_cap.py
theory-lab/topwindow/results/boundary_thin_cap_certificate.json
```

## Classification of the surviving boundary pole

The adjacent thick profile is itself bounded.  This is another **OBSERVED
theorem**: in the boundary-maximum case the outer component has order at most
four.  After the order-two thin cap is removed, its rooted depth set and
rooted topology have exactly one of the forms

```text
{0,s,2s}:          root with leaves at depths s and 2s;
{0,s,G,G+s}:       root--s--G and a root leaf at G+s, with G>2s.   (FW42)
```

Indeed the symmetric branch of the coefficient-block proof of (FW34) gives
more than `X=lambda-X`: `X` is a direct sum of complete mixed-radix digit
blocks.  Let its lowest owned block be

```text
{0,s,2s,...,(r-1)s}
```

and write `D` for the direct sum of its higher owned blocks.  The maximum
depth vertex is the root leaf already obtained in (FW36).

We use two elementary collision rules.  If distinct positive depths `x,y`
and `x+y` all belong to `X`, then the `x`- and `y`-vertices must start in the
same root branch; otherwise their distance `x+y` repeats the root depth
`x+y`.  Likewise complementary depths `x,lambda-x` must start in the same
branch unless they are the same vertex, since different branches would give
a second distance `lambda` besides the root leaf.

If `r>=4`, the vertices at depths `s` and `2s` must share a branch because
`3s` is another root depth.  The `s`-vertex is a root child, so their distance
is `s`, repeating its incident edge.  If `r=3` and `D` has a positive member
`H`, the inclusions `H+s,H+2s in X` force `H` to lie simultaneously in the
root branches of `s` and `2s`; those branches must be different by the same
edge-`s` collision.  Thus `r=3` gives only `{0,s,2s}`.

It remains that `r=2`.  Every positive `H in D` shares the `s`-branch because
`H+s in X`.  If `D` had an intermediate member `0<H<max D`, symmetry of `D`
would put the complementary vertex to `H+s` in that same branch, and hence
put `H+s` there as well.  Its distance from the root child at `s` would then
be `H`, repeating the root depth `H`.  Therefore `|D|<=2`.  The singleton
case is the removed order-two pole; otherwise `D={0,G}` and the unique rooted
topology is the second form in (FW42).  Its edge from depth `s` to depth `G`
has `G>=2s` because `G` is the next higher digit place, and equality would
repeat distance `s`; hence `G>2s`.

Consequently a surviving boundary maximum meets an **exact degree-three
pole**, not an unbounded bush: either outer order three with

```text
diam(A)=3s,              hence q>=3s+1,
```

or outer order four with internal distance set

```text
{s,G,G+s,G-s,G+2s,2G+s},
diam(A)=2G+s,            hence q>=2G+s+1.           (FW43)
```

At this classification stage the pole shapes can still attach to an arbitrary
inward component; the next two subsections exclude that attachment.  A direct
parent-map audit of all 1,442 canonical factors arising through interval
length 128 finds 193 root-leaf pole realizations, all of orders two, three or
four and all in the displayed forms:

```text
theory-lab/topwindow/verify_boundary_pole_factor.py
theory-lab/topwindow/results/boundary_pole_factor_certificate.json
```

## The boundary pole hands to a thick opposite side

The exact pole shapes also control the other end of the corridor.  Let `p`
be the boundary edge entering the opposite outer component `B`, let `theta`
be its rooted eccentricity, and retain `L=q+lambda`.  The reflected vertices
of `B` lie at most `theta`, while the nearest corridor vertex is at
`p+theta`, with a complete gap between them.

For the order-three pole `X={0,s,2s}`, exact coefficient recursion gives

```text
t in V  iff  floor(t/s)=0 mod 3,        0<=t<L.    (FW44)
```

Thus occupied `s`-blocks alternate with empty `2s`-blocks.  If
`p+theta<L`, the outer gap must be one of those complete empty blocks.  Since
`diam(B)<p`, block phase and length force

```text
p=2s+1,       theta=s-1.
```

The first occupied block then gives `b>=s`.  The internal distances of `B`
lie below `p` and avoid the already used pole distances `s,2s,3s`, so

```text
binom(b,2)<=2s-2.
```

This leaves only `(s,b)=(1,1),(2,2),(3,3),(4,4)`.  The first two make the
whole tree a spider and are excluded by the all-order spider theorem.  For
the latter two the forced rooted depth sets are `{0,1,2}` and
`{0,1,2,3}`: the first has internal distance `3=s`, colliding with the pole,
and the second has no distinct-distance rooted realization.

For the order-four pole `X={0,s,G,G+s}`, the digit structure has
`G=2sr` for an integer `r>=2`.  Within each period `2G`, the factor `V`
occupies alternating `s`-blocks below `G` and is empty throughout the second
half.  Hence a complete outer gap below `L` is either

```text
small: p=s+1,       theta=s-1;
large: p=G+s+1,     theta=G-s-1.                  (FW45)
```

The small case gives `b>=s` and `binom(b,2)<=s-1`, leaving only
`(s,b)=(1,1),(2,2)`, both spiders.  In the large case the occupied blocks
below `G` give `b>=G/2`, while the `B`-distances have only `G+s-4` available
values below `p` after removing the four pole distances there.  Therefore

```text
binom(b,2)<=G+s-4.
```

Since `s<=G/4`, this forces `(G-4)(G-8)<=0`; divisibility leaves only

```text
(s,G,b)=(1,4,2), (1,6,3), (2,8,4).
```

The first is again a spider.  The other two force rooted depth sets
`{0,2,4}` and `{0,1,4,5}`.  Their unique feasible rooted realizations contain
distance `6`, which is already a pole distance in both cases.

Consequently every surviving boundary pole satisfies the strict handoff

```text
p+theta >= q+lambda.                               (FW46)
```

No corridor vertex occurs in the reflected top prefix; all its vertices come
from the opposite outer component.  Counting the unique representations gives

```text
order-three pole: b >= ceil((q+2s)/3),
order-four pole:  b >= ceil((q+G+s)/4).
```

Also `theta<p<q` in (FW46) gives

```text
p >= ceil((q+lambda+1)/2).
```

Thus the intermediate boundary-pole lemma hands to a linearly large,
large-radius opposite component through a second near-maximum edge.  The next
subsection turns this thick-opposite normal form into a contradiction.  The
finite local catalogue is audited by

```text
theory-lab/topwindow/verify_boundary_pole_handoff.py
theory-lab/topwindow/results/boundary_pole_handoff_certificate.json
```

## Boundary-maximum corridors are excluded

The thick handoff inequalities already close the boundary branch.  This is an
**OBSERVED theorem** for every target order `n>=18`.  Since all
`binom(b,2)` internal distances of `B` lie below `p<q`,

```text
binom(b,2) <= p-1 <= q-2.                          (FW47)
```

For the order-three pole, the representation count after (FW46) gives
`q+2s<=3b`.  Combining it with (FW47) yields

```text
b^2-7b+4s+4<=0.
```

As `s>=1`, this forces `2<=b<=5`, and hence

```text
q <= 3b-2s <= 13.
```

But the largest of the `n-1` distinct positive edge weights satisfies
`q>=n-1>=17`.  Thus the order-three boundary pole is impossible.

For the order-four pole, `q+G+s<=4b`, so (FW47) gives

```text
b^2-9b+2G+2s+4<=0.
```

Here the next digit place has `G>=4s`, whence
`b^2-9b+14<=0` and `2<=b<=7`.  Therefore

```text
q <= 4b-G-s <= 23,
```

so `n<=24`.  Taylor's necessary order condition leaves only `n=18` in
`18<=n<=24`, and the complete 512-shard forest certificate has
`nsol=0` at order 18.  This removes the last order-four possibility.

Together with (FW35) and the thin-cap theorem, this proves that a nontrivial
degree-two canonical sink path cannot occur in a target counterexample.
Hence the canonical sink component itself must contain a
vertex of degree at least three.  Excluding that genuine thick sink remains
**UNVERIFIED**.  The arithmetic rows and the exact order-18 forest hash are
audited by

```text
theory-lab/topwindow/verify_boundary_corridor_exclusion.py
theory-lab/topwindow/results/boundary_corridor_exclusion_certificate.json
```

## Singleton thick-centre normal form

The first genuine thick terminal also has an exact all-order normal form.
This is an **OBSERVED reduction**, not yet an exclusion.  Suppose that the
full-window canonical sink component is the single vertex `v`, now with
degree `d>=3`.  Let its incident edges have weights `w_i`, and let `B_i` be
the rooted component beyond the `i`th edge.  Write

```text
b_i=|B_i|,  theta_i=ecc(B_i),  H_i=w_i+theta_i.
```

Every boundary edge points into the singleton sink, so its outer side has no
full support.  This gives `diam(B_i)<=w_i`; equality would repeat the
distance of the incident edge, so in fact

```text
diam(B_i)<w_i,       theta_i<=w_i-1.              (FW48)
```

In particular every edge internal to `B_i` is lighter than `w_i`.  If
`q=max_i w_i`, then `q` is the globally heaviest edge.  All internal spectra
of the branches, together with the other `d-1` incident weights, occupy
different members of `{1,...,q-1}`.  Hence

```text
q >= sum_i binom(b_i,2)+d.                         (FW49)
```

The numbers `H_i` are the maximum distances from `v` into the branches and
are pairwise distinct.  A pair within one branch has distance below `w_i`,
whereas the farthest pair in two different branches has distance `H_i+H_j`.
Consequently the Leech diameter `N` is the sum of the two largest `H_i`.
If `p` is the second-largest incident weight, (FW48) gives

```text
N <= (2q-1)+(2p-1) <= 4q-4,
q >= ceil((N+4)/4).                               (FW50)
```

This quadratic lower bound on the heaviest edge is specific to a singleton
thick sink.

Now distinguish the branch `A` incident with `q`.  Put
`lambda=theta(A)` and `H_q=q+lambda`.  Among all other branches let `mu>h`
be the two largest arm heights.  If the `q`-branch is not on a diameter, or
if `h>=q`, then `h` cannot equal `q`: its farthest `v`-pair is distinct from
the `q`-edge.  The three relevant arm heights are distinct and the two
largest are at least `q+1,q+2`.  Thus

```text
N>=2q+3.                                          (FW51)
```

Moreover the complement of `A` contains the three distinct pairs from `v`
to the `mu`- and `h`-vertices and between those two vertices.  Their
distances are `mu,h,mu+h`, all greater than `q`.  Therefore the exact
heaviest-edge excess

```text
E_q=N+1-|A|(n-|A|)-q
```

is at least three in this thick-third-arm branch.

It remains that the `q`-branch lies on a diameter and `h<q`.  The other side
of the `q`-cut has rooted eccentricity `mu` and diameter exactly `mu+h`, while
`diam(A)<q`.  Since

```text
N=q+lambda+mu,
D=max(diam(A),mu+h),
```

all values `D+1,...,N` cross the `q`-edge.  Reflect the two rooted depth sets
at `lambda` and `mu`, obtaining `U,V`.  Their sums therefore represent
`0,...,N-D-1` exactly once.  In particular, with

```text
Q=min(mu+1,q-h),
```

we have the exact prefix

```text
{0,...,lambda+Q-1} subset U+V.                    (FW52)
```

Indeed `N-diam(A)>=lambda+mu+1` and
`N-(mu+h)=q+lambda-h`.

The `q`-edge points into the singleton sink, so its centre side has full
support.  That side has diameter `mu+h`, and therefore

```text
mu+h>q,       mu+1>q-h,       Q=q-h.              (FW53)
```

Thus the scale boundary below is exactly `h+lambda>q`, rather than an
uncontrolled minimum involving `mu`.

The same full-support inequality gives a two-sided scale window.  Since
`h<=mu-1`, we have `2mu-1>q`; and since the `mu`-arm uses an incident edge
strictly below `q`, (FW48) gives `mu<=2q-3`.  Substituting
`N=q+lambda+mu` yields

```text
ceil((N-lambda+3)/3) <= q
 <= floor((2N-2lambda-2)/3).                      (FW56)
```

Thus every surviving thin singleton centre has its heaviest edge in a fixed
middle-scale interval; it cannot approach either zero or the Leech diameter.

Apply the coefficient-block dichotomy (FW34) to this shorter prefix.  Either
`U=lambda-U`, or `U` has a consecutive gap at least `Q+1`.  In the latter
case the reflected root-to-farthest path must cross that gap, so `A` contains
an internal edge of weight at least `Q+1`.  This is the promised nested-heavy
handoff into a proper branch.

In the symmetric case, the symmetric branch of the proof of (FW34) expresses
`U` as a direct sum of complete mixed-radix digit blocks.  The first-edge
argument and rooted collision classification of (FW42) apply to `A` itself,
so this alternative already has `a<=4`.  Thus the `Q<lambda` scale interface
is a genuine internal-edge handoff unless its outer rooted factor is one of
the same four small mixed-radix forms.

If `Q>=lambda`, no factor of maximum `lambda` can have such a gap.  The
coefficient-block proof then makes `U` a complete mixed-radix factor, and the
farthest vertex of `A` is a root leaf by the repeated-first-edge argument.
The pole classification (FW42) applies verbatim: `A` has order at most four,
with rooted depth set

```text
{0};  {0,lambda};  {0,s,2s};  or  {0,s,G,G+s}, G>2s.
```

The prefix in (FW52) uses `lambda+Q` different pairs across the `q`-cut.
Thus in this pole branch, writing `a=|A|`,

```text
2lambda <= lambda+Q <= a(n-a),       lambda<=2(n-4).
```

Also `h<=mu-1=N-q-lambda-1`, so (FW53) gives

```text
Q=q-h >= 2q+lambda-N+1.
```

Combining this with the same cross-pair count gives the pole upper bound

```text
q <= floor((N+a(n-a)-2lambda-1)/2).               (FW57)
```

For the leaf pole `a=1,lambda=0`, (FW56)--(FW57) reduce to

```text
ceil((N+3)/3) <= q <= floor((N+n-2)/2),
Q<=n-1.
```

At order 25 this is the explicit interval `101<=q<=161`.

The arm of height `mu` uses an incident edge at most `p<=q-1`, so
`mu<=2q-3`.  Since `N=q+lambda+mu`, every pole survivor satisfies the
stronger scale bound

```text
q >= ceil((N-lambda+3)/3)
  >= ceil((N-2n+11)/3).                           (FW54)
```

For example the last lower bound is `87` at order 25, compared with `76`
from the generic singleton-centre bound (FW50).

The pole also forces the three highest arms to cluster.  Put

```text
g=min(q+lambda,mu)-h
```

for the gap from the third arm to the smaller diameter arm, and let `beta(q)`
be the largest integer `k` with `binom(k,2)<=q-2`.  The reflected prefix
(FW52) contains `0,...,g-1`: indeed
`g<=mu-h` and `g<=q+lambda-h`.  Every complement vertex represented there
has rooted depth greater than `h`, so it lies in the unique `mu`-arm.  If
`a=|A|`, counting the `g` unique sums gives at least `ceil(g/a)` such
vertices.  Their internal distances are all below their incident edge and
hence below `q`, so

```text
binom(ceil(g/a),2)<=q-2,
g<=a beta(q)<=4 beta(q)<=4(n-1).                  (FW55)
```

Thus the pole alternative cannot hand to three quadratically separated
arms: the third arm is within `O(n)` weighted distance of the smaller
diameter arm, while the arms themselves may have quadratic height.

There is a second, independent restriction on how many vertices may hide in
the `mu`-arm.  For each branch let `D_i` be its set of distances from `v`, and
augment these sets by `D_0={0}` for the centre.  A pair is *cross* when its
vertices lie in different augmented branches.  Put

```text
I=sum_i binom(b_i,2),
L_q=#{cross pairs of distance strictly below q}.
```

All `I` within-branch distances are below `q` by (FW48).  Conversely every
pair is either within one branch or cross through `v`.  The Leech bijection on
the values `1,...,q-1` therefore gives the exact low-spectrum balance

```text
q=I+L_q+1.                                         (FW58)
```

In the thin case, let `a=|A|`, let `b` be the order of the `mu`-arm, and let
`r=n-1-a-b` be the total order of all lower arms.  Every one of those `r`
vertices has `v`-depth at most `h<q`.  If `t` is the incident weight of the
`mu`-arm, its incident root has depth `t<q`.  These are `r+1` different low
cross pairs, so (FW58) yields

```text
q>=I+r+2.                                          (FW59)
```

The `binom(b,2)` internal distances of the `mu`-arm are distinct positive
integers below `t`, whence `t>=binom(b,2)+1`.  Its `b` distinct rooted depths
include zero, so its rooted eccentricity is at least `b-1`.  Consequently

```text
mu>=binom(b+1,2).
```

If `I_R` is the sum of `binom(s,2)` over the lower arms, combine this with
`N=q+lambda+mu` and (FW59) to obtain the all-order mass inequality

```text
b(b-1)+I_R+[binom(a,2)+lambda-a+1] <= N-n.         (FW60)
```

The loss in (FW60) has an exact decomposition.  Put

```text
X=L_q-(r+1),
delta=t-1-binom(b,2),
eta=theta-(b-1),
```

where `theta=mu-t` is the eccentricity measured from the `mu`-arm attachment
root.  The three quantities are nonnegative: the low-cross-pair count in the
proof of (FW59), equivalently (FW58)--(FW59), gives `X>=0`; the internal
distances of the arm give `delta>=0`; and its distinct rooted depths give
`eta>=0`.
Equations (FW58) and the definition of `delta` give

```text
q=binom(a,2)+binom(b,2)+I_R+r+X+2,
mu=binom(b+1,2)+delta+eta.
```

Consequently the mass slack is not merely nonnegative but satisfies the
exact identity

```text
M := N-[b^2+binom(a,2)+I_R+r+lambda+2]
   = X+delta+eta.                                  (FW61)
```

There is also an unavoidable quadratic contribution inside `eta`.  If
`b>=2`, the `b` rooted depths are distinct integers.  Hence the two largest
rooted depths are at most `theta` and `theta-1`, and every internal distance
of the arm is at most `2theta-1`.  Its `binom(b,2)` distinct positive
internal distances therefore imply

```text
binom(b,2)<=2theta-1,
eta>=rho(b),
rho(1)=0,
rho(b)=ceil((binom(b,2)+1)/2)-(b-1)  (b>=2).
```

Thus (FW60) sharpens, without any small-order classification hypothesis, to

```text
b(b-1)+rho(b)+I_R+[binom(a,2)+lambda-a+1] <= N-n. (FW62)
```

This applies to both thin interfaces.  In the pole interface the slack itself
is necessarily quadratic.  The upper half of (FW56) and
`mu=N-q-lambda` give

```text
3mu>=N-lambda+2.
```

For pole orders `a=1,2,3,4`, respectively, (FW53) and the classified pole
depth sets give

```text
lambda <= 0, n-2, 2 floor(3(n-3)/4), 2(n-4).
```

Call these four bounds `Lambda_a`, and put

```text
L_{n,a}=ceil((N-Lambda_a+2)/3).
```

Since `mu=binom(b+1,2)+delta+eta`, (FW61)--(FW62) imply the pointwise defect
floor

```text
M >= Psi_{n,a}(b)
  := max(rho(b), L_{n,a}-binom(b+1,2)).             (FW63)
```

Uniformly in the four pole orders,

```text
min_b Psi_{n,a}(b)=n^2/18+O(n).
```

Indeed the two entries in the maximum have leading terms `b^2/4` and
`n^2/6-b^2/2`, whose crossing is at `b^2=2n^2/9`.  Therefore every pole has

```text
max(X,delta,eta) >= n^2/54-O(n).                  (FW64)
```

This is a structural trichotomy rather than an exclusion: quadratically many
extra low cross pairs occur, or the receiving arm has quadratically many
holes below its incident weight, or its rooted eccentricity has quadratic
surplus.  At the target orders `18,25,27,36,38,49,51`, the uniform exact lower
bounds for `M` are respectively `8,21,25,53,60,105,116`; the certificate also
records the stronger value for each of the four pole orders.

The third-arm scale gives a stronger interface than path averaging suggests.
Choose a lower arm `P` whose `v`-height is `h`, and write

```text
h=w+vartheta,
```

where `w` is its edge incident with `v` and `vartheta` is its eccentricity
from the attachment root.  Equation (FW48) applies to this complete arm, so
`vartheta<=diam(P)<w`.  In particular the apparent alternative `w<h/2`
cannot occur: integrality gives `h<=2w-1`.  The prefix capacity in (FW52)
gives `lambda+Q<=a(n-a)`, while `h=q-Q`; hence

```text
w>=ceil((h+1)/2)
 >=ceil((q+lambda-a(n-a)+1)/2)
 =n^2/12-O(n).                                    (FW65)
```

The exact middle lower bound remains valid when its argument is nonpositive,
but is then weaker than `w>=1`.  For an explicit uniform asymptotic bound,
put `A=q+lambda-a(n-a)`.  Equation (FW54), `a<=4` and `lambda>=0` give

```text
A>=n^2/6-(29/6)n+59/3,
w>=n^2/12-(29/12)n+31/3.
```

Thus every pole exposes three heavy *incident* interfaces at the same centre:
the globally heaviest `q`-edge, the quadratic `mu`-arm edge `t` from (FW72),
and the quadratic third-height-arm edge `w`.  No averaging over the order of
the third arm, and no internal-edge fallback, is needed.

For a sharper finite split, first suppose `h>=q/2`.  The same incident-edge
observation gives the exact order-free bound

```text
w>=ceil((ceil(q/2)+1)/2)
 >=ceil((ceil(ceil((N-2n+11)/3)/2)+1)/2).          (FW66)
```

Thus the tall-third alternative contains a non-`q` *incident* edge of
quadratic, rather than merely linear, weight.

Now suppose `h<q/2`.  Then `2Q>q`, while (FW53) gives
`Q<=a(n-a)-lambda`.  Since all quantities are integral,

```text
q<=2a(n-a)-2lambda-1.                             (FW67)
```

Combining this with (FW54) completely excludes the short case for a leaf
pole at every `n>=18`, for an order-two pole at `n>=26`, for an order-three
pole at `n>=37`, and for an order-four pole at `n>=48`.  In particular every
pole at every order `n>=48` is in the tall case (FW66).

For the remaining finite short regimes, the set consisting of `v` and all complete lower
branches is connected and induces a subtree `C`, of order `r+1` and diameter
at most `2h<q`.  Its `binom(r+1,2)` internal
distances, the internal distances of `A` and `B`, and the pair joining `v` to
the `B` attachment root are mutually distinct values below `q`.  Hence

```text
q>=binom(a,2)+binom(b,2)+binom(r+1,2)+2,
b^2+rho(b)+binom(r+1,2)+binom(a,2)+lambda+2<=N.   (FW68)
```

Since `r=n-1-a-b`, `a<=4` and `lambda=O(n)`, the leading part of the second
inequality is

```text
(5/4)b^2+(1/2)r^2 <= (1/2)n^2+O(n),
```

which gives

```text
b<=4n/7+O(1),             r>=3n/7-O(1).
```

A direct expansion gives the usable explicit version
`b<4n/7+3` and `r>3n/7-8`.

The quadratic defect floor also has a direct geometric interpretation.  Put

```text
D_{n,a}(b)=ceil(Psi_{n,a}(b)/3).
```

Since `M=X+delta+eta>=Psi_{n,a}(b)`, at least one of the following holds:

```text
delta>=D:  t=binom(b,2)+1+delta >=D;
eta>=D>=1: some edge of B (hence not the external edge t) has weight
           >=1+ceil(D/(b-1))       (necessarily b>=2);
X>=D:      some vertex has at least ceil(2D/n)
           extra low-cross neighbours.                       (FW69)
```

For the last line, let `mathcal L` be the set of unordered low cross pairs and
let `mathcal B` be the `r` distinct pairs from `v` to lower vertices together
with the distinct pair from `v` to the `B` attachment root.  Then
`mathcal B` is a subset of `mathcal L` and
`X=|mathcal L minus mathcal B|`; these remaining pairs are exactly the edges of a
simple graph.  The handshake lemma gives its maximum degree.  If `D=0`, the
displayed alternatives are only the original nonnegativity statements.  For
sufficiently large `n`, the uniform positive floor in (FW63) turns (FW69)
into the trichotomy

```text
t>=n^2/54-O(n),
or an edge of B distinct from t has weight n/54-O(1),
or one vertex has n/27-O(1) extra low-cross neighbours.
```

Together with (FW65), the first two alternatives give heavy interfaces in two
different arms; the last gives a linear-size low-distance crowding cone in
addition to the heavy third-height arm.

The incident-hole alternative has a sharper, exact location.  Delete the
`mu`-arm incident edge `t`, and write `C=V(T) minus B`, so `|C|=c=n-b>=1`.
Every internal pair of `B` has distance below `t` by (FW48).  Every pair
crossing the cut has distance at least `t`, with equality only for the two
endpoints of the edge; no internal pair of `C` can also have distance `t`
because distances are globally unique.  Now use the full Leech spectrum
`{1,...,N}`, not merely distance injectivity: exactly `t-1` pairs lie below
`t`.  Therefore

```text
#{pairs internal to C with distance <t}=t-1-binom(b,2)=delta.
```

Similarly, among the exactly `N-t` pairs above `t`, exactly `bc-1` cross the
cut.  Thus the ordinary edge excess is entirely realised inside `C`, and

```text
#{pairs internal to C with distance >t}
 = E_t := N+1-bc-t
 = binom(c,2)-delta.                              (FW70)
```

In particular, if the first line of (FW69) holds, the graph on `C` joining
pairs at distance below `t` has `delta>=D` edges.  The handshake lemma gives
some vertex of this proper side at least `ceil(2D/c)` such neighbours.  (For
`D=0` this is only the trivial nonnegative statement.)  Asymptotically the
`delta` alternative supplies both the quadratic incident edge
`t>=n^2/54-O(n)` and a complement-localised crowding cone of degree
`n/27-O(1)`.  This exact cut localisation is still a descent interface, not a
collision proof.

The three defect alternatives can now be collapsed to a two-way descent.
Let

```text
S={x in V(T): d(v,x)<q/2},       s=|S|.
```

By the definition of cross pairs, the two endpoints of every pair counted by
`X` lie in different arms of `T-v` (or one is `v`), so their unique path goes
through `v`.  Its distance is the sum of the endpoints' `v`-depths; because
that sum is below `q`, at least one endpoint lies in `S`.
Therefore `S` is a vertex cover of the simple `X`-graph, and

```text
X<=binom(n,2)-binom(n-s,2)=s(2n-s-1)/2.
```

Positive edge weights make `S` ancestor-closed from `v`, so the induced
subtree `T[S]` is connected.  It is proper because the `q`-arm is disjoint
from `S`, and any two of its vertices have distance less than `q`.
On the other hand, `delta>=D` gives `t>=D+1` directly.  If `eta>=D`, then
`theta=b-1+eta<=diam(B)<t`, so integrality of the weights and distances gives
`t>=b+eta>=D+1`.  Since at least one of `X,delta,eta` is at least `D`, every
pole satisfies the exact dichotomy

```text
t>=D+1,
or T[S] is a proper connected induced subtree with diam(T[S])<q
   and s(2n-s-1)/2>=D.                            (FW71)
```

Using `D=n^2/54-O(n)`, the second inequality has smaller limiting root

```text
s >= (1-sqrt(26/27))n-O(1) > 0.01869n-O(1).
```

Thus (FW71) exposes a quadratic `mu`-arm incident edge or a proper all-low
induced core of linear order.  In fact the next estimate makes the heavy
incident edge unconditional; the value of the second line is that the
`X`-large branch additionally supplies an actual nested core.

Indeed `theta<=diam(B)<t`, so integer weights give

```text
mu=t+theta<=2t-1.
```

On the other hand the pole scale used in (FW63) says
`3mu>=N-lambda+2`.  Combining the two inequalities, and also using
`N=q+lambda+mu`, gives

```text
t>=ceil((N-lambda+5)/6),             4t>=q+4.     (FW72)
```

Thus every pole, independently of which defect is largest, has a second
incident edge at least one quarter of the heaviest-edge scale and in fact

```text
t>=n^2/12-O(n).
```

For pole orders `a=1,2,3,4`, substituting the four exact upper bounds
`Lambda_a` from (FW63) gives the following lower bounds for `t` at the target
orders:

```text
n=18:  27, 24, 23, 22       n=25:  51, 47, 46, 44
n=27:  60, 56, 54, 52       n=36: 106,101, 98, 96
n=38: 118,112,110,107       n=49: 197,189,186,182
n=51: 214,206,202,198.
```

Together with (FW65), a pole therefore always exposes quadratic incident
interfaces in two different non-`q` arms: `t` in the `mu`-arm and `w` in the
third-height arm.  The missing step is directional inheritance of one of
these interfaces, not the existence of a second or third scale.

There is nevertheless exact inherited top-window data at `t`.  Put
`H=q+lambda`.  After deleting `t`, the `B` side rooted at its attachment root
has eccentricity `theta` and diameter below `t`.  The complementary side `C`
rooted at `v` has eccentricity `H` and diameter exactly `H+h`: the value is
realised between farthest vertices of the `q`-arm and a third-height arm, and
all other arm pairs have length at most `H+h`.  Since

```text
N=H+t+theta=H+mu,
```

every value above `H+h` crosses `t`.  Reflect the rooted depth sets of `B`
and `C` at `theta` and `H`, respectively.  The full Leech spectrum and global
distance uniqueness give the exact unique-sum prefix

```text
{0,...,mu-h-1} subset (theta-D_B)+(H-D_C).        (FW73)
```

This includes the two attachment roots correctly: their pair is the external
edge `t`, not an internal pair of `B`.

If `R=t-h>0`, the prefix length is `theta+R`.  The coefficient-block argument
of (FW34)--(FW52), now with the rooted `B` factor, gives the following
secondary scale handoff.  If `0<R<theta`, either the reflected rooted depth
set of `B` is symmetric or an edge wholly inside `B` has weight at least
`R+1`; the symmetric case is closed uniformly in (FW76) below.  If
`R>=theta`, then `theta=0` already means `b=1`; otherwise the same
complete-factor and rooted-parent classification used after (FW53) applies
with `u` as root and the external edge `t` omitted, forcing `B` to be a
mixed-radix pole of order `b<=4`.

The inherited gap is controlled.  Indeed `t<q<=H` and `t<=mu`, so

```text
0<R<=min(H,mu)-h<=4(n-1)
```

by (FW55).  Thus whenever `t` rises above the third height, it either hands a
linear-size-or-smaller gap to a genuinely internal edge of `B` (up to the
explicit symmetry case), or terminates in another pole of order at most four.
The remaining branch `t<=h` sends the quarter-scale interface into the lower
arm geometry instead.  This is controlled one-step inheritance, but it is not
yet a well-founded iteration.

The finite-hole ladder routes the `t`-handoff even more sharply.  Let
`C_0` be the connected induced subtree consisting of `v` and all lower arms,
so `|C_0|=r+1`; the complement of `B` is the disjoint union of the `q`-arm
`A` and `C_0`, joined by the edge `q`.  To force more near-`t` internal pairs
than the `binom(a,2)` pairs available inside `A`, the edgewise ladder gives

```text
a       pairs needed       cut product threshold       last offset L_a
1            1                       11                       10
2            2                       19                       19
3            4                       29                       31
4            7                       35                       40.
```

Suppose the relevant threshold holds and `q-t>L_a`.  The edge `t` is
non-heaviest, and its cut product is `b(n-b)>=n-1`.  The ladder forces the
displayed number of distinct unordered within-side pairs with distances
`t+k`, `1<=k<=L_a`.  None lies inside `B`, whose diameter is below `t`, so all
lie in `C=A union C_0`.  At most `binom(a,2)` lie inside `A`; a pair crossing
from `A` to `C_0` has distance at least `q>t+L_a`.  Hence a remaining pair
lies entirely in `C_0`.  Equivalently, whenever the indicated order threshold
is available,

```text
q-t<=L_a,
or C_0 contains a pair of distance t+k, 1<=k<=L_a. (FW74)
```

Since the four cut-product thresholds correspond to
`n>=12,20,30,36`, respectively, every pole of every order `n>=36` satisfies
the uniform alternative

```text
q-t<=40,
or the proper lower core C_0 contains a pair in {t+1,...,t+40}.
```

At the smaller target orders, this routing is available for `a=1` at `n=18`
and for `a=1,2` at `n=25,27`; all four are covered from `n=36` onward.  Thus the
large-order pole endgame is reduced to bounded clustering of the two
quadratic incident edges or a strict handoff into the linearly large lower
core.  The next refinement routes the apparent bounded cluster as well.

The bounded cluster is not actually a separate terminal.  Put

```text
k=q-t,             Q=q-h,             R=t-h=Q-k.
```

The edge endpoints realising `t` and the centre-to-farthest pair realising
`h` are different unordered pairs, so global distance uniqueness gives
`t!=h`.  In the cluster branch `k<=40` there are therefore exactly two cases.

If `h>t`, then `Q>=1` because `h<q`, and the farthest lower vertex itself
gives a pair wholly in `C_0` with

```text
h=t+(k-Q),             1<=k-Q<=39.
```

This is already the strict lower-core handoff promised by the other line of
(FW74).  If instead `h<t`, then `R=Q-k>=1`, so the unconditional reflected
prefix (FW73) and its coefficient-block conclusion apply: for
`0<R<theta`, the rooted depth factor of `B` is symmetric or an edge wholly
inside `B` has weight at least `R+1`; for `R>=theta`, the `mu`-arm is a pole
of order `b<=4`.  Consequently, for every pole of order `n>=36`,

```text
C_0 contains a pair in {t+1,...,t+40};
or 0<t-h<theta and B is symmetric or has an internal edge >=t-h+1;
or b<=4.                                                   (FW75)
```

Thus the apparent bounded two-heavy-edge cluster always routes either into
the linearly large lower core or back into the receiving arm.  At this
intermediate point the symmetric rooted factor looks exceptional; the next
paragraph shows that it is another small pole.

The symmetric rooted factor is also a small pole rather than a new terminal.
The argument is general.  Let a rooted branch `J` have depth set `X`, maximum
`theta`, and reflected factor `U=theta-X` in an exact prefix of length
`theta+R`, where `R>=1`.  If (FW34) returns its symmetric outcome, then
`U=theta-U=X`.  The symmetric branch of the coefficient proof supplies a
direct sum of complete mixed-radix digit blocks; this completeness, not set
symmetry alone, is essential.

Let `z` be the farthest vertex and let its first edge toward the root have
weight `e`.  The parent of `z` has reflected depth `e`, so `e in U=X`.  Unless
that parent is the root, the edge at `z` and a root-depth pair at `e` are
different unordered pairs with the same distance.  Hence `z` is a direct
root leaf (with the `theta=0` singleton handled separately).  The collision
classification in the proof of (FW42), which uses only the complete digit
blocks, this root leaf, and global distance uniqueness, now applies verbatim:

```text
|J|<=4, with rooted depths
{0}, {0,theta}, {0,s,2s}, or {0,s,G,G+s}, G>2s.  (FW76)
```

Consequently the symmetric alternatives in both (FW52) and (FW73) terminate
in a small rooted factor.  In particular (FW75) simplifies, for every
`n>=36`, to a lower-core near-`t` pair, a genuinely internal edge of `B` of
weight at least `t-h+1`, or `b<=4`.  The symmetric factor is no longer among
the unverified pole obstacles.

The last two-small-factor terminal has fixed width.  In the residual `b<=4`
case of (FW75), necessarily `q-t=k<=40` and `h<t`; the other cases have
already routed to `C_0`.  Recall `H=q+lambda`, `mu=t+theta`, and put

```text
g=min(H,mu)-h=min(Q+lambda,R+theta).
```

Every pair not crossing between `A` and `B` has distance at most
`max(H+h,mu+h)`: pairs from either top arm to `C_0` give the two displayed
bounds, pairs inside `C_0` are at most `2h`, and within-arm pairs are smaller
still.  The full spectrum therefore has exactly `g` values strictly above
that maximum, and all must be realised by distinct pairs in `A times B`.
Since `a,b<=4`,

```text
1<=R=t-h<=g<=ab<=16.                              (FW77)
```

Together with `Q=k+R` and the pole inequality `lambda<=Q`, this gives the
fixed bounds

```text
Q<=56,             lambda<=56,             lambda+Q<=112,
min(Q+lambda,R+theta)<=16.
```

In the last line, either the `q`-side top gap is at most 16, or
`R+theta<=16` and hence `theta<=15`.  Thus the residual is a fixed-width
affine two-small-factor state, not an unbounded new geometry.  A finite
rooted-state classification of this width is the next concrete task; (FW77)
does not itself exclude the state.

Even this fixed-width state must hand to a linear proper structure.  Let
`L_0` count pairs internal to `C_0` with distance below `q`.  All pairs inside
`A` are below `q` by (FW48), and all pairs inside `B` are below `t<q`.
Pairs from `A` to `C_0` have distance at least `q`, and pairs from `A` to `B`
are larger still.  A low pair from `B` to `C_0` has distance

```text
t+x,                 0<=x<q-t=k.
```

The offsets are distinct by global distance uniqueness, so there are at most
`k<=40` such pairs.  The exact `q-1` low values therefore give

```text
L_0=q-1-binom(a,2)-binom(b,2)-#{low B--C_0 pairs}
   >=q-53.                                             (FW78)
```

Write the orders of the complete lower arms (excluding `v`) as `s_i`, put
`m=max_i s_i`, and recall `sum_i s_i=r`.  Their internal pairs all have
distance below `q` by (FW48), and

```text
2I_R=sum_i s_i(s_i-1)<=r(m-1).
```

Let `Y=L_0-I_R` be the low cross-pair count among the lower arms augmented by
the centre, and put

```text
S={x in C_0:d(v,x)<q/2},             s=|S|.
```

Every pair counted by `Y` has its path through `v` and at least one endpoint
in `S`.  Hence

```text
2Y<=s(2(r+1)-s-1).
```

As before, positive weights make `T[S]` a connected induced subtree with
diameter below `q`; it is proper because the nonempty arms `A,B` are omitted.
Combining the last three displays with (FW54) gives the all-order dichotomy

```text
some complete lower arm has order at least alpha*n-O(1),
or T[S] has order at least alpha*n-O(1),
alpha=(9-sqrt(69))/6=0.115562... .
```

Indeed the two capacity terms have leading sum
`(3alpha-alpha^2)n^2/2`, and `alpha` is the smaller root making this `n^2/6`.
Thus the two-small-factor terminal also descends to a linear proper branch or
a proper all-low core.  For a coarse exact finite form, let
`L=q_lo-53`, with `q_lo=ceil((N-2n+11)/3)`.  If both structures had order
below `K`, then

```text
2L <= (n-3)(K-2)+(K-1)(2(n-2)-K).
```

The strict reverse inequality certifies `K=4,4,5,6` at
`n=36,38,49,51`, respectively.

There is also a layer-by-layer form of the third-heavy-arm phenomenon that
does not depend on the two-small-factor state.  Order all arms at `v` by
their distinct heights

```text
H_1>H_2>...>H_d>0,              H_1+H_2=N,
```

and let their orders be `c_1,...,c_d`; put `H_{d+1}=0`.  For every `k>=2`,
all distances strictly above `H_1+H_{k+1}` must join two of the first `k`
arms.  Root pairs and within-arm pairs are at most `H_1`, while a cross pair
using a later arm is at most `H_1+H_{k+1}`.  The full spectrum therefore gives

```text
H_2-H_{k+1} <= sum_{1<=i<j<=k} c_i c_j.           (FW79)
```

Choose the least `k` for which `H_{k+1}<H_2/2`, and put
`C_k=sum_{i<=k}c_i`.  Minimality gives `H_i>=ceil(H_2/2)` for every
`i<=k`, while (FW79) and positivity of the arm orders give

```text
C_k(C_k-1)
 >= C_k^2-sum_{i<=k}c_i^2
 =2 sum_{i<j<=k}c_i c_j
 >H_2.                                             (FW80)
```

In a pole, the two diameter arms are `A` and `B`.  Both their heights are at
least

```text
L_{n,a}=ceil((N-Lambda_a+2)/3),
```

because `3mu>=N-lambda+2` and the lower half of (FW56) gives the same lower
bound for `q+lambda`; explicitly,

```text
q+lambda>=ceil((N-lambda+3)/3)+lambda>=L_{n,a}.
```

Thus more than `sqrt(L_{n,a})` vertices lie in arms
whose incident edges have weight at least

```text
ceil((ceil(L_{n,a}/2)+1)/2)=n^2/24-O(n).          (FW81)
```

This mass cannot all be hidden in the two diameter arms.  Let `c` be the
total order, among the first `k` arms, contributed by third-and-lower arms.
If `b=|B|`, then

```text
sum_{i<j<=k}c_i c_j
 <=ab+(a+b)c+binom(c,2).
```

Let `B_{n,a}` be the exact maximum `b` allowed by (FW62).  Equations
(FW79)--(FW80) force `c` to be at least the least nonnegative integer with

```text
2a B_{n,a}+2(a+B_{n,a})c+c(c-1)>L_{n,a}.          (FW82)
```

Since `B_{n,a}<=sqrt(2/5)n+O(1)` and
`L_{n,a}=n^2/6+O(n)`, this gives the uniform asymptotic accumulation

```text
c >= (sqrt(17/30)-sqrt(2/5))n-O(1)
  >0.12031n-O(1).                                 (FW83)
```

Consequently a pole contains a linear mass of third-and-lower arms whose
*incident* edges are all quadratic.  This is the desired quantitative
thin/thick bridge: either one such proper arm is linearly large, or that mass
is spread over several quadratic interfaces at the same branch centre.  It
is still a reduction, not a collision or a well-founded iteration.

The same layer bound also absorbs the thick branch left by (FW51).  In that
branch either the `q`-arm is not on a diameter, in which case `H_2` is larger
than its height and hence larger than `q`, or the third height is at least
`q`, in which case again `H_2>=q`.  Equation (FW48) gives
`H_1<=2q-1`, so

```text
N=H_1+H_2<=2q-1+H_2<=3H_2-1,
H_2>=ceil((N+1)/3).                               (FW84)
```

Applying (FW80)--(FW81) with this value shows that more than
`sqrt((N+1)/3)` vertices lie in arms whose incident edges have weight at
least `N/12-O(1)`.  The pole branch has the same conclusion with the
`L_{n,a}` loss of only `O(n)`.  Thus *every* singleton thick terminal now has
a common output: `n/sqrt(6)-O(1)` vertices behind quadratic incident
interfaces.  What remains is to turn a large proper arm into inherited
window data, or to contradict the alternative in which this mass is spread
over several interfaces.

There is a rigorous transition at every nonsymmetric inherited interface,
although it is weaker than the tempting assertion that the reflected gap
itself always cuts off a thin cap.  Use the notation of (FW73), assume
`R=t-h>0`, and let `U=theta-D_B`.  If `U` is nonsymmetric, (FW34) gives two
consecutive members of `U` separated by at least `R+1`.  On a path from a
farthest vertex of `B` to its attachment root, reflected depth increases from
`0` to `theta`.  That path must cross the empty interval in one step, so it
contains an edge `e` wholly inside `B` with

```text
e>=R+1.                                             (FW85)
```

Delete `e` and let `P` be its component away from the attachment root.  Since
`diam(B)<t`, we have `e<t`, while the root-side component of `T-e` contains
the whole edge `t`.  Thus `e` always has full support toward the root side.
There are exactly two possibilities:

```text
diam(P)<e;  or  e is full-support bidirectional.   (FW86)
```

Indeed equality `diam(P)=e` is impossible: a pair internal to `P` at distance
`e` would repeat the distinct pair formed by the endpoints of `e`.  If the
diameter is larger, `P` supplies full support in the other direction.  In the
second case the full-bidirectional edge-component containing `e` is
nontrivial, is contained in `B`, and does not cross the attachment edge `t`,
because `t` is not bidirectional (`diam(B)<t`).  It may contain the attachment
root, so “strictly inside” must be understood edgewise rather than as a
statement about its vertex set.

Closing this edge-component gives an unconditional cap.  If the first line
of (FW86) holds, take `f=e` and `C=P`.  Otherwise let `K` be the maximal
connected bidirectional edge-component containing `e`, and let `f` be its
first boundary edge on the path toward `v`.  If `f` is internal to `B`, its
`v`-side contains the complete edge `t>f`; if `f=t`, that side has full
support by the singleton-sink definition (equivalently, in the present pole
setting it contains the complete edge `q>t`).  Thus the `v`-side supports `f`.
Maximality of `K` says that `f` is not bidirectional, so the component `C`
away from `v` has no pair above `f`; global distance uniqueness again removes
equality.  In the bidirectional branch `C` contains both endpoints of `e`,
and hence `f>e`; in the thin branch `f=e` by definition.  Uniformly,

```text
C subseteq B,   diam(C)<f,   f>=e>=R+1.           (FW87)
```

Here `C` is always a proper component of `T`, but it may equal the whole arm
`B` when `f=t`.  Consequently a nonsymmetric singleton handoff always closes
to a proper thin cap; if the original gap edge was not already its boundary,
the proof additionally exposes a proper non-singleton bidirectional
edge-component on the way.  This connects the two remaining terminal
geometries, but does not exclude either one.

There is also a strict cap on the far side, at the cost of forgetting the
lower bound on its boundary weight.  In the thin line of (FW86), use
`g=e,C_z=P`.  In the bidirectional line, follow the maximal component `K`
from `e` toward the chosen farthest vertex `z`.  The last edge at `z` cannot
be bidirectional, because its far side is a singleton, so this path has a
first boundary edge `g`.  The side toward `v` contains `t>g` and supports
`g`; maximality makes `g` non-bidirectional.  The other side `C_z` therefore
satisfies

```text
z in C_z,   C_z proper-subset B,   diam(C_z)<g<t. (FW88)
```

Unlike (FW87), this transition always strictly decreases vertex order.
Here `z` is the farthest vertex of the `mu`-arm and `x` is the farthest
vertex of the `q`-arm, so `xz` is the original diameter used in (FW49).

The top prefix persists across every such diameter cap in an exact form.
More generally, let an edge `g` on the fixed diameter `xz` cut off the
`z`-side component `C`, suppose `diam(C)<g`, and suppose the `x`-side rooted
eccentricity is larger than `diam(C)`.  Denote the endpoints of `g` by
`c in C` and `p in D=T-C`, and put

```text
alpha=d(c,z),  beta=d(p,x),  sigma=diam(D)-beta.
```

The diameter property shows that `alpha` and `beta` are the two rooted
eccentricities: a farther vertex on either side would make a path to the
opposite diameter endpoint longer than `N`.  Since `diam(D)>=beta`, we have
`sigma>=0`; the dominance hypothesis makes `diam(D)>diam(C)`.  Also
`N=alpha+g+beta`.  Hence all distances above `diam(D)` cross `g`, and after
reflecting the two rooted depth sets they give exactly one representation of

```text
0,...,alpha+R_g-1,   R_g:=g-sigma.                (FW89)
```

For the caps produced by (FW88), the dominance hypothesis is automatic: the
`x`-side rooted path contains the old attachment scale `t>g>diam(C)`.

If `R_g>0`, apply (FW34) to the reflected `C` factor.  Its symmetric outcome
is one of the order-at-most-four factors in (FW76).  In the nonsymmetric
outcome the gap path lies wholly inside `C`; repeating the far-side closure
above gives another diameter cap `C'` with

```text
|C'|<|C|,   boundary(C')<g.                       (FW90)
```

If `R_g<=0`, the complementary rooted tree instead has the exact thick
surplus

```text
diam(D)-beta=sigma>=g.                            (FW91)
```

This surplus is itself a strict near-diameter handoff.  Let

```text
q'=N-diam(D)=alpha+R_g.
```

The unique distance-`N` pair uses `z`, which is not in `D`, so `q'>=1`.
Moreover `alpha<=diam(C)<g`, and `R_g<=0`, whence

```text
1<=q'<=alpha<g.                                   (FW92)
```

Thus a pair wholly inside the proper complement `D` is `q'`-far, with a
strictly smaller deficit than the cap boundary.  In fact this pair keeps the
old endpoint `x`.  Apply the four-point property to the old diameter `xz` and
the diameter pair of `D`.  If that pair already contains `x`, the conclusion
is immediate.  Otherwise one of the two cross distances from `x` is at
least `diam(D)`.  Both endpoints lie in `D`, so that cross distance is at
most `diam(D)`; equality and global distance uniqueness force `x` itself to
be the other endpoint of the diameter pair.  Write it as `{x,y}`.

The word “thick” in (FW91) now has a literal geometric meaning.  Project `y`
to the root-to-`x` path in `D`; measure its gate position `s` from `p` and
write `k` for its off-path height.  Since

```text
d(x,y)=beta-s+k=diam(D)=beta+sigma,
```

we have `k=s+sigma>=sigma>=g`.  Consequently the strict handoff is an
endpoint pivot

```text
d(x,y)=N-q',  1<=q'<g,
y lies in a g-deep offshoot from the old x--z diameter. (FW93)
```

The pivot has an exact three-ray normal form.  Let `b` be the gate of `y` on
the old diameter and put `k=d(b,y)`.  The two other ray heights differ from
`k` by positive integers `r` and `q'`:

```text
d(b,x)=k+r,   d(b,z)=k+q',
N=2k+r+q',   k>=g,   r>=1,   r!=q'.              (FW94)
```

The second equality follows by subtracting `d(x,y)=N-q'` from
`d(x,z)=N`.  The global diameter is strictly longer than `d(y,z)`, so
`r>=1`; uniqueness of those two nonmaximum pair distances gives `r!=q'`.
This is precisely an affine three-tip anchor with one controlled gap
`q'<g`.  The uniform spider and `n>=18` bi-spider theorems exclude it when no
further branching is present, but they do not localise the extra branch
vertices inside the three rays.

Full-support orientation localises that extra branching to one direction.
Let `K` be the maximal full-bidirectional edge-component containing the pivot
gate `b` (possibly just the vertex `b`).  Consider a boundary edge `f` of
`K`.  If its far component contains neither `x`, `y` nor `z`, the `K`-side
contains the distance-`N` pair `xz`.  If it contains `y`, the same is true.
If it contains `z`, then `f` lies on the `b`--`z` ray, so

```text
f<=k+q'<2k+r=d(x,y).
```

Thus in all three cases the `K`-side fully supports `f`, and the non-
bidirectional boundary edge points into `K`.  The only possible outward
boundary is the unique one whose far component contains `x`.  For that edge
the `K`-side contains the pair `yz` of distance `2k+q'`; distance uniqueness
excludes equality.  Consequently

```text
K is a canonical thick sink; or
there is an x-side boundary edge f>2k+q'.          (FW95)
```

In the second line the boundary is non-bidirectional, so its `x`-side is the
fully supported direction.  Let `q_max` denote the globally heaviest edge
(the earlier singleton-centre edge `q`).  Then

```text
2k+q'<f<=q_max.                                   (FW96)
```

There is also a useful order-free deficit bound on this exceptional edge.
It lies on the global diameter `xz`; put `j=N-f`.  Deleting it leaves rooted
sides of eccentricities whose sum is `j`.  Rooted depths are distinct
integers, so a side of eccentricity `u` has at most `u+1` vertices.  Adding
the two sides gives `n<=j+2`.  Since (FW94) says `2k+q'=N-r`, (FW95) gives

```text
n-2<=j=N-f<r,   hence r>=n-1.                    (FW97)
```

Therefore every endpoint pivot with `r<=n-2`, or more generally with
`2k+q'>=q_max` (equality is itself forbidden), already lands in a canonical
thick sink.  The sole escape is a directed `x`-side component behind a
near-diameter edge, in the explicit large-gap regime `r>=n-1` and
`2k+q'<q_max`.  This is a reduction, not yet an exclusion of that tail.

In the original singleton-pole geometry the escape is confined much more
tightly.  Recall that the `q_max`-edge is the incident edge of the `q`-arm and
is not bidirectional.  If the pivot gate `b` were on the `x`-side of that
edge, then every `x`-side boundary of `K` would leave the complete
`q_max`-edge on the `K`-side, giving support larger than the boundary and
preventing an outward arrow.  If `b=v`, the component is the original
singleton sink.  Hence an escape gate lies strictly on the `mu`-arm side of
`v`; both `b` and the pivot endpoint `y` belong to the rooted arm `B`.

The outward boundary is therefore encountered at or before crossing the
attachment edge `t`.  Internal edges of `B` are below `t`, so (FW95)--(FW97)
sharpen to

```text
d_B(y,z)=2k+q'<f<=t,
k<t/2,
N-t<=N-f<r,  hence r>=N-t+1.                     (FW98)
```

Thus the only nonsink endpoint pivot is a two-tip configuration inside the
same receiving arm: its internal tip distance is below the arm attachment
weight, while the opposite ray gap exceeds `N-t`.  This exact rooted-arm
tail, rather than arbitrary extra branching elsewhere in the tree, is the
remaining escape case.

The rooted endpoint strip in that escape is exact.  Let `u` be the attachment
root of `B`, let `theta=d_B(u,z)`, and for `w in B` put

```text
delta_B(w)=theta-d_B(u,w).
```

The old diameter enters `B` through `u` and passes through `b` on its way to
`z`.  Hence the affine pivot equations give

```text
delta_B(y)=d_B(u,z)-d_B(u,y)=q'.
```

Moreover `x` and `y` belong to the cap complement `D` by (FW92)--(FW93),
whose diameter is `N-q'`.  If `w in D intersect B`, then the fact that, for
every `w in B`, the unique `x`--`w` path enters `B` through `u` gives

```text
d(x,w)=N-delta_B(w)<=diam(D)=N-q'.
```

Thus `delta_B(w)>=q'`; equality repeats the distance `d(x,y)=N-q'`, so global
distance uniqueness forces `w=y`.  Equivalently,

```text
{w in B : delta_B(w)<q'} subset C_z,
{w in D intersect B : delta_B(w)=q'}={y}.         (FW99)
```

The boundary of `C_z` lies between `b` and `z`: both `x` and `y`, hence their
connecting path and its gate `b`, lie in `D`.  Therefore the pivot endpoint
`y` is exactly the first receiving-arm vertex outside the strict endpoint cap
in reflected-depth order.  This is an exact weighted endpoint-strip
localisation; it does not yet bound `q'` by an absolute constant.

The original `t`-cut prefix now migrates to this strict cap.  Let

```text
U_z={delta_B(w):w in C_z},
V=H-D_C
```

where `C` is the rooted complement of `B` from (FW73).  We have
`q'<=alpha<=theta<theta+R`, so the coefficient `q'` is still inside the
exact prefix (FW73).  For every `j<q'`, its unique representation `j=u+v`
has `u<q'`; (FW99) therefore puts the corresponding `B` vertex in `C_z`.
At `j=q'`, the original factorisation is represented by the pair `xy`, with
reflected coordinates `(q',0)`; here `0=H-d_C(v,x)` because `x` is the
depth-`H` endpoint in the `q`-arm.  Any representation using `U_z+V` would
be a different pair at the same distance.  Consequently

```text
every j in {0,...,q'-1} has exactly one representation in U_z+V,
q' has no representation in U_z+V.                (FW100)
```

Thus the strict cap inherits not merely a prefix lower bound but a sharp first
hole.

This first hole meets the lower-arm route at an exact layer.  In the rooted
complement of `B`, the reflected values below `H-h` come only from the
`q`-arm.  They form its classified pole factor

```text
P={0}, {0,lambda}, {0,s,2s},
  or {0,s,G,G+s} with G>2s,
```

and all values of `P` are at most `lambda<H-h`.  The farthest vertex of a
third-height arm supplies the complement value exactly `H-h`.  Hence
`q'=H-h` is impossible: together with `0 in U_z` it would represent the
forbidden coefficient `q'` in (FW100).  There are precisely two routes:

```text
q'<H-h:  U_z+P represents 0,...,q'-1 uniquely and first misses q';
q'>H-h:  the third-and-lower-arm spectrum enters the inherited prefix
          strictly before its first hole.                         (FW101)
```

In the first route, pair counting also gives

```text
q'<=|C_z| |P|<=4|C_z|.
```

The two routes sharpen further.  Put `c_z=|C_z|` and `a=|P|<=4`.  In the
pole-only route, the `binom(c_z,2)` internal cap distances are distinct positive
integers below `g`, while (FW93) and (FW98) give

```text
2g+q'<=2k+q'<t.
```

Integer strictness therefore yields

```text
c_z(c_z-1)<=t-4,
q'<=a c_z<=a floor((1+sqrt(4t-15))/2).            (FW102)
```

In particular the remaining pole-only endpoint window has square-root scale
in the attachment weight; if the strict cap is itself one of the
order-at-most-four terminal factors, then `q'<=16`.

In the second route,

```text
H-h<q'<g<=k<t/2.
```

Since `H=q+lambda` and `t<q`, this forces

```text
h>H-t/2>q/2+lambda>=q/2.                         (FW103)
```

Thus lower-arm entry before the endpoint hole is not a new terminal: it
returns to the tall-third-arm heavy-edge handoff (FW65)--(FW66).  The only
new endpoint output is the small-pole first-hole factorisation with (FW102).
An exclusion still requires a collision there or a proof that its proper cap
continues the decreasing recurrence.

The small-pole first hole has an explicit digit normal form.  For
`j=0,...,q'-1`, write `u_j=1` when `j in U_z` and zero otherwise.  Coefficient
uniqueness in (FW101) recursively forces

```text
u_j=1-sum_{p in P, p>0, p<=j} u_{j-p}.            (FW104)
```

Here the `q`-arm pole came from the complete-block branch of
(FW52)--(FW34), not merely from a symmetric set having the displayed shape.
The complete mixed-radix structure used in (FW42) and (FW76) makes the lower
binary digit block have place `s`; hence its next binary place is
`G=2sr` for an integer `r>=2` in the order-four case.  Solving (FW104) gives
the following canonical complement indicator `chi_P`:

```text
P={0}:                 chi_P(j)=1;
P={0,lambda}:          chi_P(j)=1 iff floor(j/lambda) is even;
P={0,s,2s}:            chi_P(j)=1 iff floor(j/s)=0 mod 3;
P={0,s,G,G+s}:         chi_P(j)=1 iff floor(j/s) and floor(j/G)
                                      are both even.                (FW105)
```

Thus `u_j=chi_P(j)` for every `j<q'`.  At coefficient `q'`, (FW100)
requires all the defined shifted terms `u_{q'-p}`, with
`p in P-{0}` and `p<=q'`, to vanish, while `q'` itself is absent from `U_z`.
Toggling the owned mixed-radix digit shows that this happens exactly when

```text
chi_P(q')=1.                                           (FW106)
```

Equivalently, the sharp first hole is a single deletion from the next block
that the canonical complement would own.  This removes arbitrary reflected
depth sets from the endpoint terminal: only the four explicit digit strips
(FW105)--(FW106), together with the geometric cap constraints (FW102), remain.
It is still a reduction rather than a collision theorem, because the rooted
cap may resume with uncontrolled reflected depths above `q'`.

The old three-arm clustering bound also applies uniformly to this remaining
route.  To avoid confusing it with the cap boundary `g`, write

```text
gamma=min(H,mu)-h
```

for the height gap in (FW55).  If `H<=mu`, the pole-only line of (FW101)
gives `q'<H-h=gamma`.  If `H>mu`, then (FW92) and `R=t-h>0` give
`q'<=alpha<=theta<theta+R=mu-h=gamma`.  Hence every genuinely new endpoint
terminal satisfies

```text
q'<gamma<=a beta(q)<=4 beta(q)<=4(n-1).           (FW107)
```

Together, (FW102) and (FW107) replace the formerly quadratic uncontrolled
deficit by a linear-in-order, square-root-in-`t` mixed-radix window.  They do
not yet make that window constant.

In fact the entire receiving-arm band strictly below `gamma`, not only its
first cap seam, has the same digit form.  Return to the exact `q`-cut prefix
(FW52).
Below `gamma`, a reflected complement value cannot come from a lower arm,
because those values are at least `mu-h>=gamma`.  A vertex `w` in `B` has
reflected `q`-cut coordinate

```text
mu-[t+d_B(u,w)]=theta-d_B(u,w)=delta_B(w).
```

The pole factor on the other side is `P`.  Coefficient recursion therefore
gives the exact identity

```text
{delta_B(w):w in B, delta_B(w)<gamma}
   ={j in {0,...,gamma-1}:chi_P(j)=1}.            (FW108)
```

Let `m_gamma` be the cardinality of this set.  The `gamma` unique top
coefficients use pairs in `P` times this band, so

```text
m_gamma>=ceil(gamma/a).
```

All `m_gamma` vertices lie in the same arm `B`; their internal pair distances
are distinct positive integers below `t`.  It follows that

```text
binom(ceil(gamma/a),2)<=binom(m_gamma,2)<=t-1,
gamma<=a floor((1+sqrt(8t-7))/2).                 (FW109)
```

Thus the whole controlled endpoint band through `gamma-1` has attachment
square-root scale.
Equations (FW99)--(FW100) locate its first seam exactly: the layers below
`q'` lie in `C_z`, the unique layer-`q'` vertex is `y` outside the cap, and
the remaining canonical layers up to `gamma` lie in the rest of `B`.
Geometry above the band and the parent relations among its forced layers
remain uncontrolled.

The digit band nevertheless forces linear terminal complexity, not merely the
square-root order bound in (FW109).  Let `S_gamma` denote the vertex set on the
left of (FW108), and let `ell_gamma` be the number of rooted leaves of `B`
that it contains.  Since `theta` is the rooted eccentricity of `B`, every
band deficit lies in `{0,...,gamma-1}`.  Moreover `S_gamma` is closed under
rooted descendants: moving away from the attachment root increases rooted
depth and decreases `delta_B`.  Thus every band vertex can be assigned to a
descendant rooted leaf that is still in `S_gamma`.

Group the `m_gamma` band vertices by their assigned leaf, allowing empty
groups, and write the group sizes as `r_1,...,r_{ell_gamma}`.  Vertices in one
group lie on one attachment-root-to-leaf chain.  A pair in that group has
distance equal to the absolute difference of its two deficits, hence in
`{1,...,gamma-1}`.  All such pairs, including pairs from different groups,
are different unordered vertex pairs, so global Leech distance uniqueness
gives

```text
sum_i binom(r_i,2)<=gamma-1.
```

Consequently Cauchy--Schwarz and (FW109), with
`M=ceil(gamma/a)`, give

```text
m_gamma^2
 <=ell_gamma sum_i r_i^2
 <=ell_gamma(2gamma-2+m_gamma),

ell_gamma
 >=ceil(m_gamma^2/(2gamma-2+m_gamma))
 >=ceil(M^2/(2gamma-2+M))
 >=gamma/(2a^2+a)>=gamma/36.                    (FW110)
```

For the second inequality, `x^2/(2gamma-2+x)` is increasing for positive
`x`; the coarse last line uses `a<=4`.  Thus the forced endpoint band itself
contains linearly many terminal leaves.

In fact linearly many separate terminal pieces are forced inside that band.
The induced subgraph on `S_gamma` is a rooted forest.  Let `c_gamma` be its
number of components, write their orders as `s_1,...,s_{c_gamma}`, and let
the root of component `i` have deficit `j_i<gamma`.  Every LCA inside that
component has rooted depth at least `theta-j_i`, while every vertex of `B`
has rooted depth at most `theta`.  Hence every internal pair in component
`i` has distance at most `2j_i<=2gamma-2`.  Global distance uniqueness across
all components gives

```text
sum_i binom(s_i,2)<=2gamma-2.
```

Another Cauchy--Schwarz application therefore yields

```text
m_gamma^2
 <=c_gamma sum_i s_i^2
 <=c_gamma(m_gamma+4gamma-4),

c_gamma
 >=ceil(m_gamma^2/(m_gamma+4gamma-4))
 >=ceil(M^2/(M+4gamma-4))
 >=gamma/(4a^2+a)>=gamma/68.                     (FW111)
```

The monotonicity argument is the same as in (FW110).  Each component is a
descendant-closed terminal subtree and has one distinct edge by which it
enters the band in `T`: the parent edge of its component root, or the
attachment edge `t` for the possible component containing the attachment
root.  Thus (FW111) directly forces linearly many endpoint-subtree entrances.
For completeness, if `c_S(w)` is the number of children of `w` that remain
in the band, the exact rooted-forest identity

```text
sum_{w in S_gamma} max(c_S(w)-1,0)=ell_gamma-c_gamma
```

records the additional branch excess.  Components may be singletons, and
branch excess may concentrate at a high-degree vertex; (FW110)--(FW111) are
therefore branch/hair accumulation lemmas, not by themselves a collision or
a proof of a non-singleton full-bidirectional thick core.

The component entrances give the missing multiplicity bridge to that core.
For a component `C_i` with root deficit `j_i`, let `e_i` be its entry edge.
If `C_i` does not contain the attachment root, its parent lies outside the
band and

```text
e_i=delta_B(parent(C_i))-j_i>=gamma-j_i.
```

If it does contain the attachment root, descendant closure gives `C_i=B`;
take `e_i=t`.  Since `gamma<=mu-h=t+theta-h` and now `j_i=theta`, the same
inequality `e_i>=gamma-j_i` holds.  In both cases (FW111) also gives

```text
diam(C_i)<=2j_i.                                  (FW112a)
```

In particular `j_i<gamma/3` makes `diam(C_i)<e_i`, so every component rooted
in the bottom third of the deficit band is a proper thin cap.

More generally there is an exact thin/full-support split at every entry.  A
non-root entry is internal to `B`, so (FW48) gives `e_i<t`; after deleting it,
the centre side contains the complete edge `t` and hence fully supports
`e_i`.  At the root entry `e_i=t`, the centre side instead contains the
complete edge `q>t`.  The outward component is exactly `C_i`.  Therefore

```text
diam(C_i)<e_i;  or  e_i is full-support bidirectional. (FW112b)
```

Indeed, if `diam(C_i)>=e_i`, equality would repeat the distance of the entry
edge by a different pair internal to `C_i`; hence strict inequality in the
other direction supplies outward full support.  The two lines of (FW112b)
partition the `c_gamma` distinct component entrances.  Together with
(FW111), at least one of the following holds:

```text
at least gamma/136 pairwise disjoint proper thin caps occur; or
at least gamma/136 distinct entry edges are full-support bidirectional.
                                                               (FW112)
```

In the second line the maximal full-bidirectional edge-components containing
those entries may coalesce, but their edge-union contains at least
`gamma/136` edges.  Thus the endpoint digit terminal no longer merely points
qualitatively at the thin/non-singleton-thick interface: it puts linear edge
mass into one side of that interface.  Excluding either multiplicity remains
open.

The bidirectional side has one more exact topological split.  Let `K` be a
maximal full-bidirectional edge-component containing marked entry edges from
(FW112).  The root entry `t` is never marked: if its component occurs then it
is all of `B`, whose diameter is below `t` by (FW48).  Hence every marked
entry and every such `K` lies edgewise inside `B`.

If `K` contains no vertex of global degree at least three, then `K` is a path.
Along any simple path in the tree, rooted depth from the attachment root
strictly decreases to the LCA and then strictly increases.  The strict
superlevel set

```text
S_gamma={w:d_B(u,w)>theta-gamma}
```

therefore meets a path `K` in at most two connected end intervals.  A marked
entry crosses from outside this set into one of those intervals, so a
branch-free path core contains at most two marked entries.  Consequently the
full-bidirectional line of (FW112) sharpens to

```text
some maximal full-bidirectional core contains a global branch vertex; or
at least gamma/272 distinct nontrivial bidirectional path cores occur.
                                                               (FW113)
```

These path cores need not individually be the whole canonical corridor sink;
they may be pieces of longer degree-two chains.  Thus (FW113) is a bridge to
the branched-core/corridor multiplicity problem, not its exclusion.

There is now a genuine fixed-window consequence when branching complexity is
bounded.  Let `R_band` be the minimal rooted subtree of `B` joining the
attachment root to all `ell_gamma` band leaves, and let `k_gamma` be its
number of vertices having at least two children.  Every such vertex is a
global branch vertex of `T`: a non-root vertex also has its parent, while the
attachment root also has the edge `t`.

At a vertex `w` of `R_band` with `d_w>=2` children, choose one band leaf from
each child branch.  Write `J=delta_B(w)` and let their deficits be
`j_1,...,j_{d_w}` in `{0,...,gamma-1}`.  Leaves chosen from different child
branches have LCA `w`, so their pair distances are

```text
2J-j_i-j_j.
```

These are globally distinct and lie in an integer interval containing at
most `2gamma-1` values.  Hence, with

```text
D_gamma=floor((1+sqrt(16gamma-7))/2),
```

the rooted leaf identity and (FW110) give

```text
binom(d_w,2)<=2gamma-1,       d_w<=D_gamma,

ell_gamma-1=sum_w(d_w-1)<=k_gamma(D_gamma-1),

gamma/(2a^2+a)-1<=k_gamma(D_gamma-1).             (FW114)
```

In particular, when `gamma>2a^2+a`, the endpoint window forces

```text
k_gamma>sqrt(gamma)/(2(2a^2+a))-1/(2sqrt(gamma))
       >=sqrt(gamma)/72-1/(2sqrt(gamma)).          (FW115)
```

Conversely, suppose the whole tree has at most `K>=1` global branch vertices.
Put `C=2a^2+a<=36`.  Since `D_gamma-1<2sqrt(gamma)`, (FW114) implies

```text
sqrt(gamma)<CK+sqrt(C^2 K^2+C),
gamma<(72K+1)^2.                                  (FW116)
```

If there are no global branch vertices, the non-strict line of (FW114)
instead gives `gamma<=C<=36`.  Thus bounded global branch count gives an
absolute endpoint window independent of `n`; the displayed estimate is only
a preliminary quadratic-in-`K` bound.  This fixed-window theorem is
conditional on the singleton-pole endpoint normal form (FW108), not a theorem
about an arbitrary rooted region of an arbitrary Leech tree.  Unbounded
branch complexity remains the route by which an unbounded window can escape.

Counting every pair of band leaves at once makes the dependence linear.
Every such pair has an LCA among the `k_gamma` branch vertices of `R_band`.
For a fixed LCA of deficit `J`, all pair distances again have the form
`2J-j_x-j_y` and occupy at most `2gamma-1` integer values.  Thus

```text
binom(ell_gamma,2)<=k_gamma(2gamma-1).             (FW119)
```

With `C=2a^2+a`, (FW110) now gives, when `gamma>C`,

```text
k_gamma>gamma/(4C^2)-1/(4C)
       >=gamma/5184-1/144.
```

If the whole tree has at most `K` global branch vertices, including `K=0`,
the same inequality rearranges to the sharper fixed-window theorem

```text
gamma<=4K C^2+C<=5184K+36.                        (FW120)
```

For `K=3`, the exact bounds for pole orders `a=1,2,3,4` are respectively
`111,1210,5313,15588`.  Hence an unbounded endpoint window actually forces
linear, not merely square-root, global branch complexity.

That escape also pays for branching *outside* the band.  The roots of the
`c_gamma` band components form a rooted antichain.  Let `R_conn` be the
minimal rooted subtree joining the attachment root to those component roots,
and let `k_out` be its number of vertices with at least two children.  Its
rooted leaves are exactly the component roots.  Moreover every one of its
branch vertices lies in `B-S_gamma`: if such a vertex were in the
descendant-closed band, its two descendant paths would join two roots inside
one band component.  Each is also a global branch vertex of `T`.

Choosing one component root from each child branch repeats the interval
argument of (FW114), so, with `C_2=4a^2+a<=68`,

```text
c_gamma-1<=k_out(D_gamma-1),
gamma/C_2-1<=k_out(D_gamma-1).                    (FW117)
```

When `gamma>C_2`, this gives the disjoint branching-buffer bounds

```text
k_out>sqrt(gamma)/(2C_2)-1/(2sqrt(gamma))
     >=sqrt(gamma)/136-1/(2sqrt(gamma)),

b-m_gamma>=k_out,
b>=ceil(gamma/a)+k_out.                           (FW118)
```

If the band contains the attachment root then it is all of `B`, so
`c_gamma=1`; (FW111) already forces `gamma<=C_2` and the exceptional line of
(FW118) never arises.  Thus an unbounded endpoint band requires both its
linear population and a separate branching connector below it.

Again all pairs, now of component roots, improve the scale.  Their LCA is one
of the `k_out` connector branch vertices, and each LCA class has at most
`2gamma-1` possible distances.  Therefore

```text
binom(c_gamma,2)<=k_out(2gamma-1).                 (FW121)
```

For `gamma>C_2=4a^2+a`, (FW111), (FW118) and (FW121) give

```text
k_out>gamma/(4C_2^2)-1/(4C_2)
     >=gamma/18496-1/272,

b-m_gamma>=k_out,
b>=ceil(gamma/a)+k_out.                           (FW122)
```

Thus the connector cost outside the band is linear in an unbounded
`gamma`; it cannot be hidden in a bounded collection of high-degree junctions.

The leaf reduction is not needed for the strongest branch count: use every
pair of band vertices.  Because band deficits are distinct, every
ancestor--descendant band pair has distance in `{1,...,gamma-1}`.  Global
distance uniqueness permits at most `gamma-1` such pairs altogether.  Every
remaining band pair has an LCA with two band-bearing child branches, hence a
global branch vertex.  For a fixed LCA the familiar expression
`2J-j_x-j_y` again supplies at most `2gamma-1` possible values.

Let `k_band` be the number of distinct LCAs arising this way, put
`M=ceil(gamma/a)`, and write `[x]_+=max(x,0)`.  Then

```text
binom(m_gamma,2)-(gamma-1)<=k_band(2gamma-1),

k_band>=[binom(M,2)-gamma+1]_+/(2gamma-1)
      =gamma/(4a^2)-O(1).                         (FW123)
```

Uniformly for `a<=4`, this is `gamma/64-O(1)`, a factor-order improvement
over (FW119).  Conversely, if the whole tree has at most `K` global branch
vertices, the left inequality and `m_gamma>=gamma/a` first give
`gamma<=4a^2K+2a^2+a`.  The last `a` integers are impossible as well.
Put `R=2K+1` and `gamma_0=2a^2R`.  If
`gamma=gamma_0+s` with `1<=s<=a`, then `M=2aR+1`; the left side of
(FW123) exceeds its allowed right side by `R(a-s)+K+1>0`.  Therefore

```text
gamma<=2a^2(2K+1)<=64K+32.                       (FW124)
```

For `K=3` and pole orders `a=1,2,3,4`, the four bounds are now only
`14,56,126,224`.  These replace the weaker numerical bounds following
(FW120).

The same all-vertex count localises nearly all of this branch cost outside
the band.  Pairs from different `S_gamma` components cannot be
ancestor-related, and their LCA cannot lie in the descendant-closed band.
Using the within-component capacity from the proof of (FW111) gives

```text
binom(m_gamma,2)-2gamma+2<=k_out(2gamma-1),

k_out>=[binom(M,2)-2gamma+2]_+/(2gamma-1)
     =gamma/(4a^2)-O(1).                          (FW125)
```

In particular, for `a<=4` and `gamma>=68`,

```text
k_out>gamma/64-17/16,

b-m_gamma>=k_out,
b>=M+k_out>gamma/a+gamma/64-17/16.               (FW126)
```

Thus a growing endpoint band forces a *linear* connector of global branch
vertices strictly below it, with leading constant depending only on the
order-at-most-four pole.  This is still a mass/descent constraint rather than
a collision.

The finite arithmetic replay
`theory-lab/topwindow/verify_endpoint_branch_capacity.py` checks all four
pole orders for global branch caps `K=0,1,2,3` (1,000 ceiling-cap values in
total) and 79,592 instances of the uniform relaxations through
`gamma=10000`.  Its frozen summary is
`theory-lab/topwindow/results/endpoint_branch_capacity_certificate.json`.
This audit checks the constants and integer tails only; the all-order
ancestor/LCA partition, component argument and ceiling-tail proof are the
derivation above.

For the first open branch-complexity class this sharpens before any
enumeration.  Assume the whole target-order tree has at most three global
branch vertices; the no-bi-spider theorem makes that count exactly three.
The singleton centre `v` already uses one.  If `a=3` or `a=4`, the classified
pole in (FW42) has two rooted child branches, so its attachment root is a
second, distinct global branch vertex.  On the other hand, the path joining
any two vertices of `S_gamma subset B` stays wholly in the component `B` of
`T-v`.  Every LCA counted by (FW123) is therefore a branch vertex inside
`B`, distinct from both `v` and the pole root.  Consequently

```text
number of available band LCAs in B <= 2,2,1,1
for pole orders                         a = 1,2,3,4.       (FW127)
```

Applying the ceiling-tail proof of (FW124) with these *receiving-arm* caps,
rather than the looser whole-tree value three, gives

```text
gamma <= 10,40,54,96                 for a=1,2,3,4.       (FW128)
```

The endpoint data are now a genuinely finite local catalogue.  Parameters
whose digit places lie at or above `gamma` are indistinguishable inside the
truncated band, so (FW105) has only 10,597 parameter/mask rows.  Applying the
exact first line of (FW123), not merely the coarse caps, leaves 3,245 rows;
the first-hole rule (FW106) expands them to 42,697 `(mask,q')` states.  At the
next four boundary values `11,41,55,97`, no mask passes its receiving-arm LCA
capacity bound.  Thus

```text
at most three global branches => one of 42,697 finite local band/hole states.
                                                               (FW129)
```

The enumeration is reproduced by
`theory-lab/topwindow/verify_endpoint_threebranch_catalogue.py`; its frozen
summary and survivor hash are
`theory-lab/topwindow/results/endpoint_threebranch_catalogue_certificate.json`.
This is only a necessary *truncated local* catalogue.  It does not yet assign
the surviving band vertices to a three-branch topology, control pole
parameters invisible above `gamma`, or exclude the thin-cap and
full-bidirectional continuations.

For pole orders three and four, the topology assignment itself is already
one-dimensional.  By (FW127), `B` contains at most one global branch vertex
`c`.  Put `J=delta_B(c)` when it exists.  If `c` belongs to `S_gamma`, then
`J` is one of the forced band deficits.  The vertices with deficit at least
`J` form a common trunk, and the vertices with smaller deficit split into
unbranched child rays.  If `c` does not belong to `S_gamma`, then `J>=gamma`
(or `c` does not exist), and the band is a disjoint collection of terminal
ray segments.  Descendant closure of `S_gamma` rules out every other shape.

For two band deficits `x>y`, their distance is therefore

```text
x-y                    on the trunk or on one child ray,
2J-x-y                 on two different child rays.             (FW130)
```

When `J<gamma`, all these values must be pairwise distinct for the actual
band value `J`.  When `J>=gamma`, equality between two cross-ray distances is
equivalent to equality of the corresponding sums `x+y`; ignoring collisions
between cross-ray distances and same-ray differences only enlarges the set
of possible bands and is consequently a safe necessary relaxation.

A canonical feasibility search now assigns the band deficits in decreasing
order to child rays.  Existing rays are ordered by their first (largest)
deficit, and the only new ray offered at each step is the final one.  Thus
each unlabeled ray partition has exactly one search path; rejected masks
exhaust all such paths, while survivors stop at their first witness.  Same-ray
differences and cross-ray sums (or the exact values `2J-x-y` when `J<gamma`)
are accumulated when their smaller endpoint is inserted, so every band pair
is checked exactly once.  An independent reconstruction recomputes the full
metric for each survivor.

For `a=3,4`, respectively, the 478 and 2,350 masks surviving (FW129) reduce
to 42 and 67 masks.  No survivor needs a branch vertex inside the band, and
the largest surviving gaps are only 13 and 20.  The sharp first-hole choices
reduce from 4,729 and 33,299 to 96 and 185.  Together with the as-yet
unfiltered order-one/two rows, the complete necessary catalogue is therefore

```text
at most 526 band masks and 4,950 sharp first-hole states.         (FW131)
```

The clean-room verifier is
`theory-lab/topwindow/verify_endpoint_onebranch_topology.py`, with frozen
output
`theory-lab/topwindow/results/endpoint_onebranch_topology_certificate.json`.
The optional Z3 diagnostic
`theory-lab/topwindow/probe_endpoint_onebranch_topology.py` independently
returns the same counts and survivor hash.  This is an **OBSERVED necessary
band-internal topology filter**, not an exclusion: the outside-band branch
position was deliberately relaxed, and the remaining masks have not yet
been checked against vertices outside `S_gamma` or the thin/full-
bidirectional continuation.  Pole orders one and two still permit two branch
vertices in `B` and require the corresponding two-branch topology filter.

That last topology is also rigid.  Two global branch vertices of rooted `B`
must be comparable: if they were incomparable, their LCA would have two
distinct child directions containing them and (including the parent edge, or
the attachment edge when the LCA is the root of `B`) would be a third,
distinct global branch vertex in `B`.  Thus the reduced skeleton consists of
an upper splitter `X`, some terminal side rays, and one distinguished ray
containing a lower splitter `Y` and its terminal rays.  With
`J_X=delta_B(X)>J_Y=delta_B(Y)`, every band-pair distance is one of

```text
|x-y|                  for comparable vertices on one skeleton ray,
2J_X-x-y               across two child directions of X,
2J_Y-x-y               across two child directions of Y.         (FW132)
```

The only possible threshold states are: both splitters above the band;
`X` above and `Y` inside; or both inside.  The reverse state is impossible
because deficit strictly decreases along rooted descendants.  For an inside
splitter its deficit is a forced value in `S_gamma` and (FW132) is checked
exactly.  For an outside splitter, equal sums within its cross-pair class are
unavoidable collisions; distinct sums can be given a sufficiently large
common translate.  Keeping the two outside translates separate is again a
safe necessary relaxation.

A nested canonical feasibility search orders the unlabeled `X`-side rays and
the unlabeled `Y`-rays by first appearance.  If either splitter has only one
band-bearing child direction, the induced band has at most one visible branch
and is already covered by the preceding one-branch relaxation.  Otherwise the
search uses at least one `X`-side ray and at least two `Y`-rays, and applies
(FW132) to every pair.  For `a=1,2` this reduces the 9 and 408 input masks to
5 and 59; their 45 and 4,624 sharp first-hole states reduce to 15 and 223.
No additional mask is rescued by placing a splitter inside the band.  The
largest surviving gaps are 6 and 14.  Combining all four pole orders gives

```text
exact-three-branch endpoint catalogue:
173 band masks, 519 sharp first-hole states, gamma<=20.           (FW133)
```

The endpoint pivot itself therefore has an absolute deficit bound in this
branch-complexity class.  Every genuine first hole satisfies `1<=q'<gamma`,
while every genuine band must survive the necessary topology filter.  Hence

```text
exactly three global branches in this endpoint terminal =>
1<=q'<=19, and its cap boundary has g>=q'+1.                      (FW134)
```

This is a conditional all-order fixed-window theorem: it is independent of
`n`, but applies only after the singleton-pole endpoint reduction has been
reached.

The fixed deficit also identifies the relevant part of the exact
three-centre normal form.  The pivot gate `b` is itself a global branch
vertex: its three nontrivial directions lead to `x`, `y` and `z`.  The old
centre `v` lies strictly inside the `b`--`x` path, because `b` is strictly in
`B` while `x` is in the `q`-arm.  Both other pivot tips are leaves.  The tip
`z` is a farthest vertex of rooted `B`; and `y` is an endpoint of the diameter
of the cap complement `D`, with the only omitted cap attached in the
`b`--`z` direction, so any continuation beyond `y` would contradict
`diam(D)=d(x,y)`.

If `a=3` or `a=4`, the pole attachment root `c_A` is already the third global
branch vertex.  The branch-centre path is therefore

```text
b ---- v ---- c_A,
```

and no branch vertex remains on the `b`--`y` or `b`--`z` paths.  Those are
two pendant legs at the end centre `b`, of lengths `k` and `k+q'`.  In the
notation of the exact three-branch engine, the diameter pair `xz` is an `AC`
anchor and its two `b`-end leg caps differ by at most 19.

If `a=1` or `a=2`, the `q`-arm is branch-free.  The one remaining branch
vertex may lie on a pivot ray, in a lower arm at `v`, or in an additional
direction attached directly at the already-branching `b` or `v`; these
possibilities must all be retained.  Nevertheless `x` is a leg based at `v`,
whereas `z` is based at `b` or at the remaining centre when that centre lies
on the `b`--`z` ray.  Thus the diameter anchor is again between distinct
centres and belongs only to class `AB` or `AC`, never `AA` or `BB`.  Summarising,

```text
exact-three-branch endpoint escape:
a=3,4 => AC with two end-leg caps differing by 1,...,19;
a=1,2 => AB or AC, with the third-centre attachment cases explicit. (FW135)
```

This is an **OBSERVED connector reduction**, not a closure of the `AB/AC`
regimes.  It supplies the precise bounded-imbalance boundary condition that a
uniform three-centre prover must now consume.

The production verifier and frozen output are
`theory-lab/topwindow/verify_endpoint_twobranch_topology.py` and
`theory-lab/topwindow/results/endpoint_twobranch_topology_certificate.json`.
An implementation-independent bounded reference enumerates every nested set
partition for 726 splitter configurations on deficit subsets of
`{0,...,6}` and agrees in every case; see
`theory-lab/topwindow/verify_endpoint_twobranch_reference.py` and its frozen
certificate.  This completes the **OBSERVED band-internal topology
feasibility filter**, not the three-branch exclusion.  Every surviving low-pole mask
already has a relaxed realisation with its visible splitters above the band;
the uncontrolled connector positions, pole parameters above the truncation,
pairs involving vertices outside `S_gamma`, and the thin/full-bidirectional
continuations remain **UNVERIFIED**.

For the two high-pole rows, the numerical end-leg imbalance has a much smaller
alphabet than the coarse interval `1,...,19`.  Every occupied `B`-layer
(equivalently, every `B`-vertex) of deficit below `q'` belongs to the strict
`z`-cap by (FW99).  In the exact-three-branch `a=3,4` geometry,
`b` is the only branch vertex in `B`; hence that cap is a terminal segment of
the pendant `b`--`z` leg.  Put

```text
U_<q'={j in {0,...,q'-1}:chi_P(j)=1}.
```

The internal distances among these cap vertices are exactly the positive
differences `j-i` for `i<j` in `U_<q'`.  They must be mutually distinct, and
none may equal an internal distance of the disjoint pole `A`.  From (FW43)
the forbidden pole sets are

```text
a=3: {s,2s,3s};
a=4: {s,G,G+s,G-s,G+2s,2G+s},  G=2sr, r>=2.
```

Together with `chi_P(q')=1` and `q'<=19`, this is a finite residue check with
an all-order tail.  For `a=3`, digit places `s>=20` have the same truncation
through 19 and all pole distances exceed every possible cap difference.  For
`a=4`, the same holds for `s>=20`; at fixed `s<20`, once
`G>max(19,s+18)`, the higher digit is invisible through 19 and every
`G`-dependent pole distance exceeds 18.  Checking the remaining legal digit
places leaves exactly

```text
a=3: q' in {1,2,3,6};
a=4: q' in {1,2,4,5,8}.                           (FW136)
```

This is an **OBSERVED conditional all-order local theorem**, not an endpoint
exclusion.  Its independent arithmetic replay checks 1,083 finite rows,
including one proved-stable representative for every infinite digit tail:

```text
theory-lab/topwindow/verify_endpoint_pole_deficit_alphabet.py
theory-lab/topwindow/results/endpoint_pole_deficit_alphabet_certificate.json
```

At pole order four the complete high-pole `AC` endpoint terminal can now be
excluded, rather than merely catalogued.  Write the pole as

```text
{0,s,G,G+s},  G=2sr, r>=2,
```

let the two pendant `b`-legs have lengths `k` and `k+q'`, let `c=d(v,b)`,
and let `t` be the actual attachment edge of the rooted receiving arm.  With
`h` the third-and-lower height, every genuine state satisfies

```text
q' in {1,2,4,5,8},                         2k+q'<t<q,
t<=c,
q>=2G+s+1,
h=min(q+G+s,c+k+q')-gamma,                 1<=h<t.       (*)
```

The diameter is

```text
N=(G+s)+q+c+(k+q').
```

First suppose that the pivot branch lies outside the band,
`delta_B(b)=k+q'>=gamma`.  Plant the three centres `c_A,v,b`; the complete
order-four pole; the two pendant tips at `b`; every forced receiving-arm
layer in `S_gamma`; a vertex at the lower height `h`; and, when `t<c`, the
attachment root on the `v`--`b` spine.  Deficits below `q'` lie on the
`z`-ray, deficit `q'` lies on the other pendant ray, and every larger band
deficit may be assigned freely to an old or new ray.  Thus symbolic ray
labels cover every genuine outside-band topology.

The all-order pole and band tails have only finitely many behaviours below
`gamma<=20`: exact small digit places are retained, while a tail constraint
such as `G>=gamma` deliberately drops divisibility and is a relaxation.
Together with the two possibilities `t=c` and `t<c`, (FW130)--(FW136) give
284 symbolic seed classes.  Exact integer metric constraints leave only 20
feasible seeds.  None realises the whole top-twenty window and none admits
the first new vertex below.

It remains essential to include the other alternative of (FW130), rather
than infer it away from (FW131).  If

```text
J=delta_B(b)=k+q'<gamma,
```

then `J` is an occupied band deficit represented by the centre `b` itself.
The occupied deficits below `J` split canonically among the two pendant rays
and any further rays at `b`; the deficits above `J` lie on the common
`u`--`b` trunk, at absolute coordinate `q+c+J-j` for deficit `j`.  The exact
condition `t+j-J<=c` keeps every such forced layer on that trunk.  The
canonical ray partitions from (FW131), again with both `t=c` and `t<c`, add
134 symbolic classes.  Seven have a feasible planted metric.  No planted
seed saturates the top-twenty window; exactly one class admits a legal first
new vertex:

```text
gamma=5, s=2, G>=gamma, chi_P=0x13, q'=1, J=4, t=c.
```

For any planted seed there are two exhaustive possibilities.  Either it already
realises all of

```text
N-1,...,N-20,
```

or its first missing value is `N-d` for some `1<=d<=20`.  In the latter
case diameter-endpoint introduction and anchored one-vertex completion say
that the next new vertex meets `x` or `z` at distance `N-d`.  Its position is
one of exactly four types:

```text
the existing lower leg at v;       a new lower leg at v;
an existing or new ray at b;       the remaining u--b spine.
```

There is no fifth location: the pole is complete, `c_A`--`v` is the single
`q`-edge, and `v`--`u` is the single `t`-edge.  Checking all distances from
the proposed vertex, with ray labels and connector lengths still symbolic,
finds no outside-band first child and leaves only the one branch-in-band class
displayed above.

For that survivor, add the first child to the planted metric and repeat the
same dichotomy through the top eighty values.  The next vertex can only lie
on a lower leg at `v` (the planted leg, the first fresh leg, or one further
fresh leg), on an old or new ray at `b`, or on the remaining `u`--`b` spine.
These possibilities are exhaustive for the same reason as before.  The
post-child metric cannot saturate `N-1,...,N-80`, and its earliest missing
value admits no legal second child.  Hence

```text
exactly three global branches + singleton-pole endpoint + a=4
    => the high-pole AC endpoint terminal is impossible.          (FW137)
```

Conditional on (FW108), (FW127)--(FW136), diameter-endpoint introduction and
anchored one-vertex completion, this is an **OBSERVED conditional all-order
exclusion**.  The symbolic model omits the triangular order equation, vertex
budget and several pole-tail
divisibility constraints, so every query is a superset of the corresponding
tree states; UNSAT is therefore in the safe direction.  All 418 queries
return `sat` or `unsat`, never `unknown`.  The verifier, Z3 version, complete
status-transcript hash and dependency hashes are frozen in the full
certificate; the earlier outside-band subterminal is frozen separately:

```text
theory-lab/topwindow/verify_endpoint_ep4_symbolic.py
theory-lab/topwindow/results/endpoint_ep4_symbolic_certificate.json
theory-lab/topwindow/results/endpoint_ep4_outside_symbolic_certificate.json
```

An exact C engine independently rebuilds the same outside-band high-pole `AC` geometry and
checks the finite order-11/order-18 EP3/EP4 regressions, including an exact
eight-shard recombination.  It is only finite corroboration, not the proofs
of (FW137)--(FW138):

```text
theory-lab/threebranch/threebranch_endpoint_exact.c
theory-lab/threebranch/verify_endpoint_exact.py
theory-lab/threebranch/results/endpoint_exact_certificate.json
```

The order-three row also closes, but requires a longer introduction chain.
Write its complete pole as `{0,s,2s}`.  In the notation above, every genuine
state satisfies

```text
q' in {1,2,3,6},                          2k+q'<t<q,
t<=c,                                     q>=3s+1,
h=min(q+2s,c+k+q')-gamma,                 1<=h<t,
N=2s+q+c+(k+q').
```

The order-three topology bound gives `gamma<=13`.  Enumerating every
truncated digit parameter, every allowed `q'`, both `t=c` and `t<c`, and both
alternatives for the actual branch deficit gives exactly

```text
218 classes = 164 outside-band + 54 branch-in-band.
```

Eighteen planted metrics survive, all outside-band.  None saturates the
top-twenty window, and ten admit the first required diameter-endpoint child.
After adding that child, no state saturates the top eighty and six admit a
second child.  After two children, no state saturates the top 160 and two
admit a third child.  Those final two classes both have

```text
gamma=6, s=2, chi_P=0x3, q'=1, delta_B(b)>=gamma,
```

and differ only between `t=c` and `t<c`.  After adding the third child,
neither class saturates the top 160 and neither admits a fourth child.

At each stage the logic is the same exact dichotomy used for (FW137): if the
current selected metric does not contain the whole stated top window, its
highest missing distance is realised somewhere in the full Leech tree;
diameter-endpoint introduction and anchored one-vertex completion force a
previously unselected vertex meeting `x` or `z` at that distance.  Its only
possible locations are an old or new lower leg at `v`, an old or new ray at
`b`, or the remaining `u`--`b` spine.  The symbolic labels retain every leg
or ray created at an earlier stage and offer one fresh label at the next
stage.  Thus the fourth-step failure is a contradiction, not a search cutoff:

```text
exactly three global branches + singleton-pole endpoint + a=3
    => the high-pole AC endpoint terminal is impossible.          (FW138)
```

Conditional on (FW108), (FW127)--(FW136), diameter-endpoint introduction and
anchored one-vertex completion, this is an **OBSERVED conditional all-order
exclusion**.  All queries return `sat` or `unsat`, never `unknown`; Z3 4.15.4
replays all 218 classes on `geo-ws`, while Z3 4.16.0 independently agrees on
the two terminal classes.  The complete structural transcript and dependency
hashes are frozen in

```text
theory-lab/topwindow/verify_endpoint_ep3_symbolic.py
theory-lab/topwindow/results/endpoint_ep3_symbolic_certificate.json
theory-lab/topwindow/results/endpoint_ep3_terminal_crosscheck_certificate.json
```

Consequently (FW137)--(FW138) close both high-pole rows of this conditional
endpoint terminal.  The following argument addresses one half of the
order-one/two `AB/AC` endpoints.

The bounded-radius half of the two low-pole rows can also be closed.  Retain
the notation

```text
H=q+lambda,  mu=t+theta,  gamma=min(H,mu)-h.
```

First suppose `a in {1,2}` and `mu<=H`.  Then `h=mu-gamma<t` gives
`theta<gamma`.  Every vertex of `B` therefore has deficit in the controlled
band, so (FW108) describes the *whole* receiving arm, rather than a truncated
part of it.  If `u` is its attachment root and `b` is the endpoint pivot, put
`ell=d_B(u,b)`.  The pivot ray to `z` has length `k+q'`, whence

```text
theta=ell+k+q',       delta_B(b)=k+q'<gamma.
```

Thus `b` is an occupied band layer, and the deficit-zero and deficit-`q'`
vertices lie in distinct child rays of `b`.  Any other branch centre in `B`
is comparable with `b` and is also visible in the band; it may lie above `b`
on the attachment trunk or below `b` on one pivot ray.  Consequently there
are only the exact one-splitter and the two orientations of the nested
two-splitter metrics of (FW130)--(FW132), now with no outside-band translate.

Canonical enumeration starts from all 15 and 516 capacity-admissible sharp
hole states at pole orders one and two.  Imposing
`delta_B(b)=k+q'`, `k>=q'+1`, `theta=max S_gamma`, and the exact ray metric
leaves no order-one state.  At order two it leaves 13 parameter states and
29 canonical ray metrics.  Every one has `ell=0`.  Nineteen have `b` as the
only branch centre in `B`; ten have the third centre below `b` on a pivot ray.

For the first 19 metrics, the third global branch centre `c` must lie in the
lower part at `v`: the order-two pole is branch-free and `B` is already
complete.  Since `c` is a branch vertex and every lower vertex has `v`-depth
at most `h`, `d(v,c)<h`.  A chosen lower vertex of depth `h` lies either on a
separate leg at `v` or beyond `c` on a leg at `c`.  These two alternatives
give 38 planted metrics.  Four already contain repeated selected distances.
In each of the remaining 34, the selected pairs fail to occupy all of
`N-1,...,N-20`.  At the greatest missing value, diameter-endpoint
introduction forces one new vertex paired with `x` or `z`.  Because the pole
and receiving arm are complete and there is no fourth branch centre, that
vertex lies on a leg at `v`, a leg at `c`, or the `v`--`c` spine.  Splitting
same-leg from new-leg placements gives 136 direct metric queries.  Every one
is infeasible.

In the other ten metrics the third centre already lies below `b`, so every
unselected vertex is on a lower leg incident with `v`.  One planted metric
collides immediately.  None of the other nine saturates the top twenty, and
the 18 same-leg/new-leg diameter introductions are all infeasible.  A second
direct-distance implementation reproduces the identical transcript.

All constraints in this last calculation are integer-linear.  They retain
`N>=153` but deliberately omit `N=binom(n,2)`, the vertex budget and several
edge-order restrictions, so infeasibility is an all-order relaxation rather
than a bounded-order search.  Z3 4.15.4 and 4.16.0 agree with no `unknown`.
A second implementation writes every distance directly, splits the four
candidate locations into separate queries, and reproduces the 4/34 seed
split, 34 failed top-window saturations and 136 infeasible introductions.
Therefore

```text
exactly three global branches + singleton-pole endpoint
 + a in {1,2} + mu<=H  => impossible.                 (FW139)
```

This is an **OBSERVED conditional all-order exclusion**.  The finite topology
reduction, symbolic exclusion and direct-metric replay are respectively

```text
theory-lab/topwindow/verify_endpoint_lowpole_small_radius.py
theory-lab/topwindow/verify_endpoint_lowpole_small_radius_symbolic.py
theory-lab/topwindow/verify_endpoint_lowpole_small_radius_reference.py
theory-lab/topwindow/verify_endpoint_lowpole_small_radius_upper_symbolic.py
theory-lab/topwindow/verify_endpoint_lowpole_small_radius_upper_reference.py
```

with frozen certificates in the adjacent `results/` directory.  The
complementary low-pole branch `mu>H` has a fixed incident gap.  In this branch
`h=H-gamma=q+lambda-gamma<t`, while `t<q`.  Integer strictness gives

```text
1<=q-t<=gamma-lambda-1.                              (FW140)
```

At pole order one `lambda=0`, and the five surviving band masks have
`gamma<=6`; their 15 sharp-hole states therefore have `q-t<=5`.  At pole
order two, substituting the exact visible step (or the lower bound
`lambda>=gamma` for an invisible step) removes 11 of the 59 masks and 30 of
the 223 sharp-hole states.  The remaining 48 masks and 193 holes have
`q-t<=10`; the exact cap distribution for gaps 1 through 10 is

```text
16,17,20,22,26,30,14,14,16,18.
```

The replay is
`theory-lab/topwindow/verify_endpoint_lowpole_high_gap.py`, with frozen
certificate in the adjacent `results/` directory.  Thus (FW139)--(FW140)
give an **OBSERVED conditional all-order reduction** of every low-pole
endpoint to a `q,t` cluster of width at most five or ten.  The clustered
`mu>H` endpoint itself remains **UNVERIFIED**; consequently this does not yet
close the order-one/two `AB/AC` terminal or the all-order three-branch theorem.

The order-one cluster has a further exact doubled top block.  Here the pole
factor is `{0}`, so (FW108) gives a unique receiving-arm vertex `w_delta` at
every deficit `delta=0,...,gamma-1`.  Let `x` be the order-one `q`-arm vertex
and let `l` be a lower vertex of height `h=q-gamma`.  Then

```text
d(x,w_delta)=N-delta,
d(l,w_delta)=N-(gamma+delta).                       (FW141)
```

Thus these planted vertices already realise every value from `N` through
`N-(2gamma-1)`.  Put `D=mu-q>0`.  The separate pair `xl` has deficit

```text
N-d(x,l)=mu-h=D+gamma.
```

If `D<gamma`, this repeats the second pair in (FW141) with `delta=D`.
Consequently every surviving order-one cluster satisfies

```text
mu-q>=gamma,
and the first unplanted top value has deficit at least 2gamma.   (FW142)
```

This is an **OBSERVED conditional all-order top-block extension**, not an
exclusion.  It supplies the next exact boundary condition for the clustered
three-centre prover.

The same argument has a useful factor form which also removes most of the
order-two cluster.  Put `S=S_gamma`, let `l` be a lower vertex of height
`h=H-gamma`, and retain the pole-reflection factor `P`.  If `w_delta` is the
band vertex of deficit `delta` and `x_p` is the pole vertex of reflected
coordinate `p`, then the two types of pairs have top deficits

```text
N-d(x_p,w_delta)=p+delta,
N-d(l,w_delta)=gamma+delta.
```

All vertices on the two sides are distinct, so every representation in

```text
S+(P union {gamma})
```

is a different unordered pair.  This sum must therefore be direct: any
repeated coefficient is already a global distance collision.

For an order-two pole, under the FW140 inequality `gamma>=lambda+2`,
`P={0,lambda}` and (FW108) says that `S` consists of
the alternating on-blocks of length `lambda` truncated at `gamma`.  The sets
`S` and `S+lambda` are disjoint.  Their latter translate overlaps
`S+gamma` exactly when the final `lambda` positions below `gamma` meet an
on-block.  Hence directness is equivalent to

```text
gamma=2m lambda  for some integer m>=1.
```

In that case `S+{0,lambda}={0,...,gamma-1}`, while `S+gamma` begins with the
next `lambda` positions.  Thus this direct cross-pair block is continuous
through deficit `gamma+lambda-1`, with its first absent coefficient at
`gamma+lambda`.  Other already selected pairs are not included in this last
“first absent” statement.

There is one more forced pair family.  Put `D=mu-H>0`.  The pairs `x_p l`
have deficits `D+gamma+p`.  At order one, `S={0,...,gamma-1}`, so `D<gamma`
would collide with `l w_D`.  At order two, if
`D<=gamma-lambda-1`, the alternating blocks put at least one of
`D,D+lambda` in `S`; the corresponding `x_p l` pair then collides with a
pair `l w_delta`.  Combining this with (FW140) gives

```text
a=1: D>=gamma,        direct cross block first absent at 2gamma;
a=2: gamma in 2lambda Z, D>=gamma-lambda,
     direct cross block first absent at gamma+lambda;
both: mu-H=D>q-t.                                      (FW143)
```

The direct planted block also creates a two-sided empty layer, without any
solver.  Write

```text
U=theta-D_B,       V=H-D_C,
F=2gamma                         if a=1,
F=gamma+lambda                   if a=2.
```

The two cross-pair families defining `S+(P union {gamma})` are all cross
pairs at the `t`-cut and represent every deficit in `{0,...,F-1}` exactly
once.  If another `B` vertex had
reflected coordinate `delta<F`, pairing it with the far pole vertex of
coordinate zero would repeat the planted coefficient `delta`.  Likewise, an
additional complement vertex of coordinate `p<F`, paired with the far
receiving vertex of coordinate zero, would repeat coefficient `p`.  Therefore

```text
U intersect {0,...,F-1}=S,
V intersect {0,...,F-1}=P union {gamma}.          (FW144)
```

In particular the attachment root of `B` has reflected coordinate `theta`.
It is not one of the band vertices: at order one (FW143) gives
`theta=D+(q-t)>=gamma+1`, and at order two it gives
`theta=lambda+D+(q-t)>=gamma+1`.  Hence (FW144) sharpens the diameter-arm
separation to

```text
a=1: theta>=2gamma,       D>=2gamma-(q-t),
a=2: theta>=gamma+lambda, D>=gamma-(q-t).
```

For `a=2`, together with (FW143), this is
`D>=gamma-min(lambda,q-t)`.  At `a=1` there is one further root-pair
collision.  Since (FW48) gives `theta<t<H=q`, if `theta+gamma>=H` then
`delta=theta+gamma-H` belongs to `{0,...,gamma-1}`.  The two different
`t`-cross pairs `(u,l)` and `(w_delta,v)` would then have the same deficit.
Here `h=H-gamma>=1`, so `gamma<H`; in particular the displayed pairs cannot
be the same unordered pair.
Consequently

```text
a=1: theta+gamma<H,
     theta<h,  and  mu-h=D+gamma<t.               (FW145)
```

Thus the order-one survivor is not merely a fixed `q,t` cluster: both sides
of the `t`-cut have an exact empty reflected layer, its receiving eccentricity
is smaller than the third arm height, and the entire inherited prefix length
`mu-h` is strictly below the attachment weight.

The symmetric endpoint at both low pole orders can now be removed completely.
Put `Delta=q-t`; then

```text
R=t-h=gamma-lambda-Delta,       1<=R<theta.
```

Apply the coefficient-block dichotomy to the exact `t`-cut prefix (FW73).
If its rooted `B` factor is nonsymmetric, the gap branch already supplies an
edge wholly inside `B` of weight at least `R+1`.  In the symmetric branch,
(FW76) says that the reflected set `U` is also the rooted depth set and is one
of the four complete pole forms of order at most four.  In addition to the
exact truncation in (FW144), the attachment-root conclusion there gives
`theta>=F`.

At order one these two conditions read

```text
U intersect {0,...,2gamma-1}={0,...,gamma-1}.
```

For the five surviving values `gamma=2,3,4,5,6`, the truncation together with
`theta>=2gamma` leaves only

```text
a=1: gamma=2, U={0,1,G,G+1}, G>=4.
```

Here `Delta=1`, `theta=G+1`, and therefore `D=theta-Delta=G`.  The
complement-internal pair `xl` has deficit `D+gamma=G+2`.  On the other hand,
the `B` vertex of reflected coordinate `G`, paired across the `t`-cut with
the lower vertex `l` of coordinate `gamma=2`, has the same deficit.  These
are different unordered pairs, so the last symmetric class collides.

At order two, (FW143) gives `gamma=2m lambda`, and (FW144) requires

```text
U intersect {0,...,gamma+lambda-1}=S,
theta>=gamma+lambda.
```

Since a classified symmetric pole has at most four vertices, the low part
`S` has at most three.  Inspecting the four FW76 forms leaves only

```text
(gamma,lambda,U)=(4,1,{0,2,G,G+2}), G>=5;
(gamma,lambda,U)=(4,2,{0,1,G,G+1}), G>=6.
```

Write `s=2` and `s=1`, respectively, so `theta=G+s`.  For every allowed
`Delta in {1,...,gamma-lambda-1}`, put

```text
p=lambda+Delta-s.
```

In the first class `p=0,1` for `Delta=1,2`; in the second, `p=2` for the
only gap `Delta=1`.  Thus in every case `p` is an actual coordinate of the
pole factor `P`.  From `theta=lambda+D+Delta` we have
`D=G+s-lambda-Delta`, so the complement-internal pair `x_p l` and the
`t`-cross pair joining `l` to the `B` vertex of coordinate `G` both have
deficit

```text
D+gamma+p=G+gamma.
```

Again the pairs are different: `x_p,l` lie in the complement of the `t`-cut,
whereas `w_G` lies in `B`.  This eliminates both infinite tails.  Consequently
every order-one or order-two `mu>H` endpoint takes the strict internal branch:

```text
a in {1,2}, mu>H  =>  B contains an internal edge
  of weight >=t-h+1=gamma-lambda-(q-t)+1.        (FW146)
```

This is an **OBSERVED conditional all-order strict handoff**, not by itself an
exclusion of the full tree: the proper receiving-arm handoff must still be
absorbed by the global descent.  It does, however, remove all five order-one
and all thirteen order-two band masks from the symmetric/small-factor endpoint
terminal.  The exact band replay, finite pole truncations and the three
uniform `G+gamma` tail collisions are replayed by

```text
theory-lab/topwindow/verify_endpoint_lowpole_symmetric.py
theory-lab/topwindow/results/endpoint_lowpole_symmetric_certificate.json
```

The exact finite topology replay makes the order-two saving concrete.  Of
the 48 masks and 193 sharp holes left by (FW140), 35 masks and 150 holes have
an immediate repeated coefficient in `S+{0,lambda,gamma}`.  Only 13 masks and
43 holes survive, at `gamma in {4,6,8,10,12}`; each satisfies the divisibility
and direct-block first-absent formula above.  The order-one row retains its five
masks and 15 holes, now with the stronger separation `D>=gamma` already seen
in (FW142).  The replay and frozen transcript are

```text
theory-lab/topwindow/verify_endpoint_lowpole_factor_collision.py
theory-lab/topwindow/results/endpoint_lowpole_factor_collision_certificate.json
```

This is an **OBSERVED conditional all-order factor-collision reduction**, not
an exclusion of the remaining 13 order-two states or five order-one states.
It replaces the broad clustered endpoint by exact periodic bands plus the
strict separation `mu-H>q-t`.

Combining the endpoint rows is now exhaustive in the exactly-three-branch
singleton-pole normal form.  The order-three/four high-pole rows are excluded
by (FW137)--(FW138).  At pole orders one/two, the branch `mu<=H` is excluded
by (FW139), while `mu>H` takes the strict internal handoff (FW146).  Therefore

```text
exactly three global branches + singleton-pole endpoint
  => contradiction, or an FW85 internal-B gap edge
     e>=t-h+1 with a in {1,2}; FW86--FW87 then close it
     to a cap boundary f>=e (possibly f=t).                (FW147)
```

This is an **OBSERVED conditional all-order endpoint return theorem**.  It
removes the endpoint geometry as a final terminal, but it is not the global
three-branch exclusion: the returned edge must pass through the cap closure
(FW86)--(FW91), whose small-factor/thick-surplus outputs, and the separate
lower-core handoffs, are not all excluded.

The two-small-factor output of that closure is now absolutely bounded when
there are at most three global branch vertices.  Work in the residual
geometry of (FW77), so `n>=36`, and let the two complete rooted pole factors
be

```text
P=lambda-X_A,       U=theta-X_B,
|P|=a<=4,           |U|=b<=4.
```

Put `Q=q-h`, `R=t-h`, and let `C_0` be the centre together with all lower
arms.  If

```text
Z={h-d(v,w):w in C_0},
A_0=Q+lambda,       B_0=R+theta,
E=N-2h=A_0+B_0,
```

then `0 in Z`.  Also (FW54) and `Q<=56` give `h>=134` already at `n=36`,
and the bound only grows with `n`.  Hence `q=h+Q<2h` and `t=h+R<2h`.
All pairs internal to `A`, `B`, or `C_0` therefore have distance at most
`2h`.  The distances strictly above `2h` are exactly the three cross
families, whose deficits from `N` are

```text
P+U,
(R+theta)+(P+Z),
(Q+lambda)+(U+Z),                              (FW148a)
```

with the last two families truncated when the displayed deficit reaches
`E`.  They represent every coefficient in `{0,...,E-1}` exactly once.

Let `g=min(A_0,B_0)`.  Below `g` only `P+U` is available.  At coefficient
`g`, a lower height-`h` vertex supplies a pair from the cross family whose
offset is `g`.  Thus `A_0=B_0` would give two different pairs at coefficient
`g`; equality is impossible.  Moreover `P+U` represents
`0,...,g-1` directly and misses `g`.  In particular

```text
1<=g<=ab<=16.
```

Suppose first that `A_0=g<B_0=g+L`.  Before the other lower cross family
enters, (FW148a) factors exactly as

```text
U + (P union (g+(Z intersect {0,...,L-1})))
       represents 0,...,g+L-1 exactly once.       (FW148b)
```

If `M=|Z intersect {0,...,L-1}|`, counting representations in this prefix
gives

```text
M>=ceil((g+L)/b)-a.                              (FW148c)
```

The reverse inequality `B_0<A_0` gives the same statement after swapping
the two ordered factors.

The `M` lower-band vertices have distinct deficits.  At most `L-1` of their
pairs are ancestor--descendant pairs, since all such distances lie in
`{1,...,L-1}`.  Every other pair has a global branch vertex as its LCA.  For
one fixed LCA the distance has the form `2J-z_1-z_2`, so at most `2L-1`
different values occur.  An order-three or order-four top pole already uses
one distinct global branch vertex at its attachment root.  Consequently,
with

```text
K=3-1_{a>=3}-1_{b>=3},
binom(M,2)-(L-1)<=K(2L-1).                       (FW148d)
```

Equations (FW148c)--(FW148d) make `L` absolutely bounded.  Enumerating the
four complete pole forms only through the sharp coefficient `g` gives 66
ordered truncated factor rows.  Exact integer arithmetic, with a monotone
residue-class proof for every infinite `L` tail, gives

```text
L<=175,       max(A_0,B_0)<=176,
E=A_0+B_0=2g+L<=178.                             (FW148)
```

Thus the at-most-three-branch two-small-factor terminal is an absolute
top-178 affine window, not an unbounded endpoint.  This is an **OBSERVED
conditional all-order fixed-window theorem**, not an exclusion of those 66
truncated rows or of the remaining lower geometry.  The arithmetic replay
and frozen certificate are

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_window.py
theory-lab/topwindow/results/endpoint_two_small_factor_window_certificate.json
```

The fixed window has an exact coefficient recursion through its entire high
spectrum.  Keep the notation above, orient the factors so that `g` is the
earlier interface and `T=g+L` the later one, and write `C` for the factor on
the arm whose lower cross family enters at `g`; let `O` be the other factor.
Thus `(C,O)=(U,P)` when `A_0<B_0`, and the ordered pair is reversed when
`B_0<A_0`.  For `s=0,...,T-1`, let `z_s` be the indicator of `s in Z` and
let `c_j` be the coefficient of `j` in `P+U`.  At coefficient `g+s`, the
pair using `0 in C` introduces `z_s`.  Every other lower-band term uses an
earlier indicator, because the second lower family starts only at `T>g`.
Exact coverage therefore forces

```text
z_s = 1-c_{g+s}
      -sum_{c in C-{0}, c<=s} z_{s-c}
      -1_{g+s>=T} sum_{o in O, o<=g+s-T} z_{g+s-T-o}.
                                                               (FW149a)
```

Every right side must be zero or one.  Conversely, when that happens the
recursion represents every coefficient from `g` through
`g+T-1=E-1` exactly once.  Hence it determines the entire lower reflected
band `Z intersect {0,...,T-1}`, not merely the density lower bound used in
(FW148c).

The remaining parameter box is finite without bounding `n`.  Equations
(FW77) and (FW148) give

```text
1<=R<=16,       R<Q<=56,       lambda<=Q,
A_0,B_0<=176,  A_0+B_0<=178,
```

and every complete pole parameter is smaller than its corresponding
interface.  Enumerating the exact order-one through order-four pole forms in
this box gives 1,312,528 relaxed parameter rows.  The binary recursion
(FW149a) leaves 1,973.  Apply the ancestor/LCA inequality to the *whole*
forced `T`-band, rather than only its first `L` layers:

```text
binom(|Z intersect [0,T-1]|,2)-(T-1)
  <=K(2T-1),       K=3-1_{a>=3}-1_{b>=3}.         (FW149b)
```

Exactly 1,199 necessary rows remain, with the uniform sharper bounds

```text
g<=3,       T<=112,       E=N-2h<=113,
|Z intersect [0,T-1]|<=33.                       (FW149)
```

No surviving row has the receiving factor of order four.  This is an
**OBSERVED conditional all-order exact-high-spectrum reduction**.  It turns
the FW77 output into 1,199 finite affine parameter rows, but it does not
assign the forced lower layers to an actual rooted three-centre topology and
does not exclude them.  The independent replay is single-process and
low-memory:

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_spectrum.py
theory-lab/topwindow/results/endpoint_two_small_factor_spectrum_certificate.json
```

The first rooted-topology class in this catalogue is impossible.  Suppose
both pole orders satisfy `a,b>=3`.  Each attachment root is then a global
branch vertex because its outer pole is complete; the two roots are distinct
from the centre `v`.  With at most three
global branch vertices, `v` is the only branch vertex available in `C_0`.
The forced `T`-band must consequently split into unbranched ray segments
incident with `v`.

On one such ray, the distance between deficits `z_i>z_j` is `z_i-z_j`.
All these differences, across every lower ray, must be distinct and must
avoid every internal distance already used by either top pole.  On two
different rays the distance is `2h-z_i-z_j`, so equal sums are forbidden.
Ignoring all other possible collisions only enlarges the feasible set.

There are 25 FW149 rows with `a,b>=3`.  Canonical unlabeled-ray partitioning
rejects 23 using the band distances alone.  The remaining two admit a band
partition only before the top-pole internal distances are reserved; after
those planted values are included, neither has a ray partition.  Therefore

```text
at most three global branches + FW77/FW149 two-small-factor terminal
  => not(a>=3 and b>=3).                            (FW150)
```

This is an **OBSERVED conditional all-order subcase exclusion**.  It removes
all 25 one-lower-branch-centre rows, leaving 1,174 necessary rows in which
at least one top factor has order at most two; it does not exclude those
remaining rows.  The exhaustive topology replay and frozen certificate are

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_root_topology.py
theory-lab/topwindow/results/endpoint_two_small_factor_root_topology_certificate.json
```

The next rooted-topology class is almost completely rigid.  Suppose exactly
one pole order is at least three.  Its attachment root consumes one global
branch vertex, so besides the centre `v` the lower core has at most one
further branch vertex `c`.  In the range in which this all-order endpoint is
used, `n>=36`; (FW149) gives `E<=113`, hence

```text
h=(N-E)/2>=259>2T.
```

Thus `v` is outside the forced `T`-band.  Canonical one/two-splitter
partitioning, with the internal distances of both planted poles reserved,
is exhaustive after deliberately separating the unknown outside-LCA
translates.  Among the 740 (FW149) rows with exactly one high-order pole, 679
have no such relaxed partition.  The remaining outcomes are 26 one-splitter
and 35 nested two-splitter rows; no survivor places the visible splitter
inside the band.  Therefore

```text
K=2 two-small-factor rows: 740 -> 61.              (FW151)
```

This is an **OBSERVED conditional all-order necessary-state reduction**, not
an exclusion of the 61 rows.  The frozen replay is

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_nested_topology.py
theory-lab/topwindow/results/endpoint_two_small_factor_nested_topology_certificate.json
```

The exact spectrum continues across the `2h` boundary.  For `0<=k<T`, every
non-cross pair involving `v`, or internal to either top arm, has distance
strictly below `2h-k`; all top-arm/lower-core pairs are still in the two
cross families of (FW148a).  An internal lower-core pair at distance
`2h-k` is necessarily a non-ancestor pair.  If its LCA is `v` its deficit
from `2h` is `z_i+z_j`; if its LCA is the sole possible lower splitter `c`
at centre-depth `d`, the deficit is `2d+z_i+z_j`.  Let `I_k` count these
pairs.  The coefficient recursion (FW149a), now at `s=T+k`, becomes

```text
z_{T+k}=1-c_{g+T+k}-I_k
          -sum_{x in C-{0}} z_{T+k-x}
          -sum_{y in O} z_{g+k-y}.                (FW152a)
```

Every right side must again be zero or one.  At `k=0`, `I_0=0`: two
different height-`h` vertices would already duplicate their distances from
`v`.  For the remaining layers, all choices `1<=d<=floor((T-1)/2)` are
enumerated explicitly and all `2d>=T` choices share one inactive state.
Only `z_T` is placed in the relaxed ray topology; the later newly forced
vertices are deliberately left unassigned, so this can only enlarge the
survivor set.

The boundary equation leaves 431 of the 740 rows; the planted two-splitter
filter leaves 31; the first `T` boundary layers leave exactly three relaxed
rows:

```text
(a,b;P,U;A_0,B_0) =
  (1,3; {0},     {0,1,2}; 4,3),   extended Z={0,4};
  (2,3; {0,4},   {0,1,2}; 9,3),   extended Z={0,5,10,15};
  (3,1; {0,1,2}, {0};     6,3),   extended Z={0,4,8}.

K=2 two-small-factor rows: 740 -> 3.               (FW152)
```

This is an independently audited **OBSERVED conditional all-order
three-row reduction**, not yet an exclusion: a hidden lower splitter can
still enter below the assigned band.  The single-process replay peaks below
20 MB RSS and its certificate records all three rows rather than only their
hash:

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_boundary_continuation.py
theory-lab/topwindow/results/endpoint_two_small_factor_boundary_continuation_certificate.json
```

It remains to treat the rows in which both pole orders are at most two.  No
outer pole root then consumes a global branch vertex, so at most three
lower-core branch vertices can occur as LCAs.  For one fixed deficit sum
`s`, all non-ancestor pairs with the same LCA have the same distance.  Thus,
if `s` occurs for `m` unordered pairs of forced-band vertices, at least
`m-3` of those pairs must instead be ancestor pairs.  Their distances are
their positive deficit differences; these differences must be globally
distinct and must avoid the internal distances of both planted poles.

Whether enough such differences can be selected is exactly a bipartite
matching problem: give the sum `s` exactly `max(0,m-3)` demand slots and
join each slot to the allowed differences of pairs having sum `s`.  A
failure of the matching rejects the row.  A success need not define a
transitive ancestor relation and ignores every cross/exact collision, so it
is deliberately weaker than an actual rooted tree.

After the topology-free `z_T` boundary equation, the exact counts are

```text
K=3 rows: 434 -> 376 at distance 2h -> 111 by LCA matching.  (FW153)
```

The largest surviving boundary band has order 16 and the largest matching
demand is 24.  This is an independently audited **OBSERVED conditional
all-order necessary-state reduction**, not an exclusion.  Its sub-second,
low-memory replay is

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_lca_matching.py
theory-lab/topwindow/results/endpoint_two_small_factor_lca_matching_certificate.json
```

The same rows admit a further topology-free continuation.  In (FW152a),
global distance uniqueness gives `I_k in {0,1}`.  Keep the exact `I_0=0`,
but for every `1<=k<T` allow `I_k` to be an independent free bit, without
requiring any real pair.  This strictly relaxes the tree while determining
all possible `Z intersect [0,2T)`.  Applying (FW153)'s matching only after
that free continuation checks 15,020 binary extensions of the 111 rows;
12,514 extensions in 61 parameter rows survive.  The maximum interface is
33, maximum extended-band order is 20, and the largest intermediate state
set is 4,608 (below the frozen 100,000 guard):

```text
K=3 rows: 434 -> 111 -> 61.                         (FW154)
```

This is an independently audited **OBSERVED conditional all-order relaxed
continuation**, not a topology assignment or an exclusion of the 61 rows.
The frozen replay is

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_free_internal_continuation.py
theory-lab/topwindow/results/endpoint_two_small_factor_free_internal_continuation_certificate.json
```

The 64 terminal rows have a common structural output even before their
exclusion.  Let `C_0` be the centre together with all lower arms, let

```text
Z={h-d(v,w): w in C_0},
```

and let `T>g` be the longer and shorter top/lower interfaces.  Define

```text
S={w in C_0: h-d(v,w)>=2T}.
```

Rooted distances from `v` are globally distinct, so the deficit map is
injective.  For the three `K=2` rows, `a+b<=5`, `T<=9`, and therefore
`|Z intersect [0,2T)|<=2T` gives at most 23 omitted vertices.  For the 61
`K=3` rows the frozen free-internal certificate takes the maximum over every
passing relaxed extension and again gives at most 23 omitted vertices.  Thus,
since this terminal is used only for `n>=36`, first

```text
|S|>=n-23>=13.                                      (FW155a)
```

The set `S` is ancestor-closed, hence it induces a nonempty connected proper
subtree `C_S` of the original tree.  Its distinct rooted depths are at most
`h-2T,h-2T-1,...`; consequently

```text
diam(C_S) <= 2h-4T-1
           = N-(g+5T+1) <= N-12.                  (FW155b)
```

The three `K=2` rows have `(g,T)=(3,4),(3,9),(3,6)`, so their individual
diameter gaps are at least 24, 49 and 34.  Equations (FW155a)--(FW155b) are an
independently audited **OBSERVED conditional all-order constant-deletion core
reduction**: every one of the 64 relaxed terminal rows hands to a proper
connected induced subtree of order at least `n-23` and diameter at most
`N-12`.  This is not an exclusion or a descent theorem; the missing step is
to prove that such a shallow core cannot acquire the omitted endpoint pieces
while preserving the Leech spectrum.

The same finite terminal gives a stronger low-distance mass output.  Recall
from (FW78) that `L_0` counts pairs internal to `C_0` below `q`.  Write the two
interface gaps as `Q=q-h` and `R=t-h`; then the enumerator variables are
`outer_gap=Q`, `receiving_gap=R`, and

```text
N-2q=(Q+lambda)+(R+theta)-2Q.
```

Over every passing `K=3` row, the frozen certificate now records

```text
N-2q<=2,
q-L_0<=1+binom(a,2)+binom(b,2)+(Q-R)<=30.          (FW156a)
```

The last term uses the (FW78) fact that the distinct low `B--C_0` offsets lie
in `0,...,Q-R-1`.  The three explicit `K=2` rows have respectively
`N-2q=-1,2,1` and the weaker-side bounds `q-L_0<=7,9,5`, so (FW156a) holds
uniformly across all 64 terminal rows.  Consequently

```text
2L_0>=N-62.                                        (FW156b)
```

This sharpens the generic `q_lo-53` use in (FW78).  Let `m` be the largest
complete lower-arm order and let `s` be the order of the connected induced
core `{x in C_0:d(v,x)<q/2}`.  If both `m<K` and `s<K`, the same two capacity
counts as in (FW78), together with `r<=n-3`, give, for `K<=r+1`,

```text
2L_0 <= (n-3)(K-2)+(K-1)(2(n-2)-K).               (FW156c)
```

Therefore one of those two proper structures has order at least every integer
`K` satisfying

```text
N-62>(n-3)(K-2)+(K-1)(2(n-2)-K).
```

Equivalently, with

```text
rho_n=(3n-6-sqrt(7n^2-50n+324))/2,
K_n=ceil(rho_n)-1,
```

one structure has order at least `K_n`.  Here `K_n<=n-6<=r` for `n>=36` in
this terminal, so the stated range and the monotonic use of the quadratic
capacity bound are valid.  The first target values are

```text
n:    36  38  49  51  64  66  81  83
K_n:   7   7   9  10  12  13  15  16,
```

and asymptotically

```text
K_n=((3-sqrt(7))/2)n+O(1)=0.177124...n+O(1).       (FW156)
```

This is an **OBSERVED conditional all-order terminal mass reduction**, not an
exclusion: the remaining global step must absorb either the large complete
lower arm or the all-low induced core.  Its improvement over (FW78)'s
`0.115562...n` comes from the certified near-half-scale bound on `q`, not from
a wider state search.  The source extrema and the separate integer-arithmetic
replay are frozen at

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_free_internal_continuation.py
theory-lab/topwindow/verify_endpoint_terminal_mass.py
theory-lab/topwindow/results/endpoint_terminal_mass_certificate.json
```

The complete-arm branch of (FW156) now enters the existing global excess
dichotomy without any interval-inheritance assumption.  Let `J` be that arm,
let `w` be its incident edge, put `j=|J|`, and set
`c=min(j,n-j)`.  By (FW48), `diam(J)<w`.  The edge excess

```text
E_w=N+1-j(n-j)-w
```

counts the within-side pairs above `w`; none can lie inside `J`, so all of
them lie in its complementary component.  Apply the all-order rooted-span
bound (2) from `docs/heaviest-edge-rigidity.md`.  Dropping only favourable
ceilings gives

```text
E_w >= [n^2-6nc+7c^2-n-c+4]/4.
```

The numerator is decreasing in `c` for `c<=n/5`.  Hence every complete-arm
output of (FW156) satisfies the exact alternative

```text
c<=n/5:
  the complement of J contains at least n^2/50-3n/10+1
  internal pairs of distance greater than w;

c>n/5:
  j(n-j)=c(n-c)>4n^2/25.                           (FW157)
```

Thus the large-arm half of the terminal reduction feeds either a
complement-localised quadratic thick profile or a balanced **cut** product.
The latter is an input to the weighted edge-excess moment (3), not by itself
a Kruskal merge product: the two light-forest components joined when `w` is
processed may be much smaller than the two sides of the full edge cut.  This
is an **OBSERVED conditional all-order interface**, not the endgame.  A
direct identification with a merge is invalid; (FW161) below gives the exact
merge-or-waste replacement.  A conflicting waste upper bound remains
**UNVERIFIED**, and the other (FW156) output, the all-low connected core,
still needs the quantitative routing given next.

That other output can at least be routed completely into a quantitative
thin-arm/thick-centre alternative.  Suppose the all-low core from (FW156) has
order `s>=K_n`.  For each complete lower arm let `u_i` be the number of its
vertices in this core, so

```text
sum_i u_i=s-1.
```

Fix any integer `d>=2`.  If some `u_i>=(s-1)/d`, its complete arm has order at
least `ceil((s-1)/d)`.  Otherwise

```text
sum_i u_i^2 < (s-1)^2/d.
```

All centre--arm pairs and all pairs in two different lower arms have paths
through `v` and distance below `q`.  Their number `Y_S` therefore satisfies

```text
Y_S=(s-1)+sum_{i<j}u_i u_j
   =(s-1)+((s-1)^2-sum_i u_i^2)/2
   >(s-1)+(d-1)(s-1)^2/(2d).                     (FW158a)
```

Combining this with (FW156), every one of the 64 terminal rows has, for every
fixed `d>=2`, the exact alternative

```text
some complete lower arm has order at least ceil((K_n-1)/d),
or
v supports more than
  (K_n-1)+(d-1)(K_n-1)^2/(2d)
distinct lower cross pairs below q.                              (FW158)
```

For `d=2`, the first target orders `36,38,49,51,64,66,81,83` give arm-order
bounds `3,3,4,5,6,6,7,8`, or respectively at least
`16,16,25,30,42,49,64,72` low cross pairs.  Asymptotically the two outputs are

```text
arm order >= ((3-sqrt(7))/(2d))n+O(1),
or low cross mass >= ((d-1)/(2d))((3-sqrt(7))/2)^2 n^2-O(n).
```

Together, (FW157)--(FW158) remove the unstructured all-low-core label from
this terminal: it now feeds either a linear thin arm (and hence (FW157)) or a
quadratic thick centre at `v`.  This is an **OBSERVED conditional all-order
routing theorem**, not an exclusion; the global project still needs an upper
bound contradicting the balanced-cut/thick-centre outputs.

The arm and shallow-core capacities in (FW156c) can be coupled rather than
maximised separately.  Let the complete lower-arm orders be `s_i`, let `u_i`
of their vertices lie in the all-low core, and put `v_i=s_i-u_i`.  A low
cross pair in two different lower arms must have at least one shallow
endpoint.  Therefore

```text
L_0 <= sum_i binom(s_i,2)+r
       +sum_{i<j}(s_i s_j-v_i v_j)
    = binom(r+1,2)-sum_{i<j}v_i v_j.              (FW159a)
```

Suppose again that both the largest arm and the all-low core have order below
`K`.  Then every `v_i<=K-1`, while

```text
sum_i v_i >= r-K+2.
```

For a total `V` placed in boxes of capacity `c=K-1`, the smallest possible
number of pairs in different boxes is obtained by filling boxes greedily.  If
`V=pc+z`, `0<=z<c`, it is

```text
C_min(V,c)=binom(p,2)c^2+pcz.                     (FW159b)
```

The function
`binom(r+1,2)-C_min(r-K+2,K-1)` is increasing in `r`: adding one deep vertex
increases the cross penalty by at most `r-K+2`, but increases the total-pair
term by `r+1`.  Since `r<=n-3`, (FW159a)--(FW159b) give the joint upper bound

```text
2L_0 <= 2binom(n-2,2)
         -2C_min(n-K-1,K-1).                     (FW159c)
```

Together with (FW156b), every integer `K` satisfying

```text
N-62 > 2binom(n-2,2)-2C_min(n-K-1,K-1)
```

is forced in at least one of the two structures.  Let `Khat_n` be the largest
such integer.  The exact first target values improve to

```text
n:       36  38  49  51  64  66  81  83
Khat_n:   7   8  10  11  13  14  16  17.         (FW159d)
```

At the limiting transition, `(1-x)/x` lies between four and five, so four
boxes are full and the remainder has mass `1-5x`.  The normalised cross
penalty is `4x-14x^2`; equating it to `1/4` gives

```text
Khat_n=((4+sqrt(2))/28)n+O(1)
      =0.1933647700...n+O(1).                     (FW159)
```

The parameterised routing (FW158) remains valid with `Khat_n` in place of
`K_n`.  For `d=2`, the target arm bounds become
`3,4,5,5,6,7,8,8`, while the alternative low-cross counts become
`16,20,30,36,49,56,72,81`.  This joint packing is an **OBSERVED conditional
all-order strengthening** of the terminal mass interface, not an exclusion.

For the finite target orders, the two worst constants in (FW156a) should not
be detached from their pole orders.  For one terminal row put

```text
ell=(N-2q)+2(q-L_0 bound),       r=n-1-a-b.
```

Then its exact input is `2L_0>=N-ell`, and the joint packing upper bound is

```text
2L_0<=2binom(r+1,2)-2C_min(r-K+2,K-1).            (FW160a)
```

The K=3 certificate freezes 42 correlated `(a,b,ell)` profiles representing
all 61 rows; the three K=2 profiles are read directly from their explicit
certificate.  Applying (FW160a) row by row and then taking the weakest result
gives

```text
n:          36  38  49  51  64  66  81  83
Kcorr_n:     8   9  11  11  14  14  17  17.       (FW160)
```

The strict integer margins at those eight thresholds are respectively
`42,5,22,51,16,51,42,111`.  Correlation does not change the all-order leading
constant in (FW159), but it removes a fictitious simultaneous worst case at
every displayed finite order.  With `d=2`, (FW158)'s corresponding arm bounds
are `4,4,5,5,7,7,8,8`, or the alternative low-cross counts are at least
`20,25,36,36,56,56,81,81`.  This is an **OBSERVED conditional exact
finite-target strengthening**, not an exclusion.

The balanced-cut output in (FW157) has an exact Kruskal interpretation at a
singleton centre.  Order the incident edges by weight.  For the edge `w` of
an arm `J` of order `j`, let `L_w` and `H_w` be the total orders of the arms
whose incident edges are lighter and heavier than `w`.  By (FW48), every
internal edge of an arm is lighter than its incident edge.  Immediately
before Kruskal inserts `w`, the two light components therefore have orders
`j` and `1+L_w`.  Hence its actual merge product is

```text
Delta_w=j(1+L_w),
j(n-j)=Delta_w+jH_w.                              (FW161a)
```

This displays precisely why a balanced cut need not be a balanced merge.  It
also controls the alternative.  If `c_e` is the full cut product and
`Delta_e` the Kruskal merge product, the exact waste identity may be written

```text
TW=sum_e w_e(c_e-Delta_e).
```

Thus the edge `w` itself contributes `w jH_w` to `TW`.

In the balanced branch of (FW157), put

```text
C_n=floor(4n^2/25)+1,       B_n=ceil(C_n/2).
```

Then `j(n-j)>=C_n`, so (FW161a) forces either `Delta_w>=B_n` or
`jH_w>=B_n`.  In the first case the Kruskal lower bound gives

```text
TW>=ceil((B_n^2-N)/2).
```

In the second case, both sides of the cut have order greater than `n/5`, in
particular `j>=floor(n/5)+1`.  The `binom(j,2)` internal distances of `J` are
distinct and below `w`, so

```text
w>=binom(floor(n/5)+1,2)+1,
TW>=B_n[binom(floor(n/5)+1,2)+1].                 (FW161b)
```

Taking the smaller of the two bounds yields the exact target table

```text
n:       36    38    49     51     64     66     81     83
TW:    3016  3364  8878  11704  25912  32108  71925  75624. (FW161c)
```

Asymptotically every balanced-cut output of this terminal therefore satisfies

```text
TW>=n^4/625-O(n^3).                               (FW161)
```

This is an **OBSERVED conditional all-order cut-to-waste bridge**.  It repairs
the incorrect shortcut “balanced cut = balanced Kruskal merge”: the valid
conclusion is a balanced merge **or** an already large explicit waste term.
It is still not an exclusion; a terminal-profile upper bound below (FW161),
or a contradiction from the complementary thick profile, remains
**UNVERIFIED**.

The same terminal also gives a bounded-defect inheritance rule at the small
end.  The full lower core `C_0` is connected and induced, has order

```text
m=n-a-b>=n-5,
```

and every one of its edges has weight below `q`: its incident edges are
non-`q` edges and every edge farther down an arm is lighter by (FW48).  Let
`D_0` be its internal distance set.  Since `L_0` counts exactly its distances
below `q`, (FW156a) gives

```text
|{1,...,q-1} minus D_0|=q-1-L_0<=29.              (FW162a)
```

Order the `m-1` edges of `C_0` by weight
`w_1<...<w_{m-1}`.  After its first `k` edges, let `Pi_k` be the number of
vertex pairs connected in that light forest.  For every `w_{k+1}<q`, all but
at most 29 of the values `1,...,w_{k+1}-1` occur internally in `C_0`; a path
of such a value uses only lighter edges.  Hence

```text
Pi_k>=w_{k+1}-30,
w_{k+1}<=Pi_k+30             (0<=k<=m-2).         (FW162)
```

For example, if the final edge of `C_0` splits orders `x,m-x`, then

```text
w_{m-1}<=binom(m,2)-x(m-x)+30.
```

More generally, if the `k`-edge light forest has `p` nontrivial components,
component concentration gives

```text
w_{k+1}<=binom(k-p+2,2)+p+29.
```

Thus the proper `n-O(1)` lower core inherits a complete covering schedule
with additive defect 30, rather than needing to inherit an exact Leech
interval.  This is an **OBSERVED conditional all-order defect-29 inheritance
theorem**.  It is not yet a decreasing induction: a future step must show
that the constant-defect schedule either repairs to a smaller Leech tree or
enters one of the already quantified thick profiles.

The free internal bits in the `K=3` continuation can also be coupled before
attempting that descent.  Let

```text
V_T=Z intersect {0,...,2T-1},
I={k in {0,...,T-1}: I_k=1}.
```

For two vertices with deficits `z_i,z_j`, an ancestor relation gives the
exact distance `|z_i-z_j|`.  Otherwise their LCA is one of the at most three
lower-core branch vertices.  If that LCA has centre-depth `d`, their distance
is

```text
2h-(z_i+z_j+2d).                                  (FW163a)
```

Consequently ancestor differences are globally distinct and avoid the two
planted pole spectra; for one fixed LCA, one deficit sum can be used at most
once.  More importantly, every `k in I` has the form

```text
k=z_i+z_j+2d
```

for one of the same three coherent depths.  Both endpoints then have deficit
below `T`, so no vertex outside the forced first band can supply a missing
`I_k`.  The centre contributes the fixed depth `d=0`; there are at most two
additional positive depths.  Thus the `I_k` are not independent free bits,
even in a topology-relaxed necessary state.

This gives a finite exact pair-resource matching.  Give every unordered pair
of `V_T` one resource: either its ancestor difference, or one LCA sum class.
Difference resources and each fixed-LCA sum resource have capacity one.  For
each required first-`T` layer the corresponding translated-sum resource must
be used exactly once.  Enumerate the two positive depths while they can reach
the first `T` layers; two inactive sentinels safely relax arbitrary deeper or
inside-band LCAs.  For an inactive LCA, translations between different LCA
classes are deliberately not compared, and no tree hierarchy is imposed on
the pair classifications.  Hence every rejection is necessary, while every
survivor remains only a relaxation.

Applied to the 12,514 extensions in (FW154), the coherent support cover first
rejects 178.  Exact capacity matching then rejects 9,019 of the remaining
12,336 and leaves 3,317 extensions in 34 parameter rows:

```text
K=3 rows by pole orders:
  (1,1): 10 -> 9,   (1,2): 1 -> 1,
  (2,1): 48 -> 23,  (2,2): 2 -> 1.

K=3 rows: 61 -> 34;  all terminal rows: 64 -> 37.   (FW163)
```

The resource matcher is independently cross-checked against all 4,756 tiny
bipartite instances through three vertices per side.  The production replay
is single-process, uses at most 190 pair nodes, and peaks near 32 MB RSS:

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_lca_layers.py
theory-lab/topwindow/results/endpoint_two_small_factor_lca_layers_certificate.json
```

This is an **OBSERVED conditional all-order necessary-state reduction**, not
an exclusion.  In particular (FW156)--(FW162), proved on the larger set of 64
rows, remain valid for the 37 survivors.  The next strict filter must impose
the rooted hierarchy of the at most three LCA classes, or close the inherited
defect-29 schedule.

The first exact rooted-hierarchy exclusions can be taken without enlarging
the state space.  Besides the centre `v`, the `K=3` lower core has at most two
branch vertices.  Their rooted branch skeleton is therefore exhaustively one
of

```text
v alone;        v--c;        v--c--d;        c--v--d.
```

For a fixed skeleton, every forced vertex in `V_T` has only three possible
location types: it is an inside-band splitter, lies on a skeleton edge above
such a splitter, or lies on a branch-free ray from one of the splitters.  An
inside-band splitter must itself occur in `V_T`.  An outside-band splitter at
centre-depth `d` is enumerated exactly whenever `2d<T`; all larger depths are
merged into an inactive class.  This last merge ignores exact translations
between deep LCA classes and therefore only enlarges the feasible set.

Process the forced deficits from shallow to deep.  Points on the same ray or
skeleton segment are ancestor-related and use their exact deficit difference.
Otherwise their exact or relaxed LCA class is fixed by the skeleton, and
(FW163a) supplies the translated sum.  Canonical creation of unlabeled rays,
global injectivity of every exact difference/active translated sum, and exact
agreement with the first-`T` internal bits give a finite DFS.  The four
skeleton types are exhaustive because a tree on `v` and two further branch
vertices is either a chain or has the two vertices in different branches of
`v`.

Three FW163 rows finish completely below 100,000 states per extension:

```text
(P,U; Q,R) = ({0},{0}; 9,1):   4 extensions, all impossible;
              ({0},{0};10,1):   2 extensions, all impossible;
            ({0,6},{0};18,1):   1 extension,  impossible.
```

Here `Q,R` denote the outer and receiving gaps used in the frozen rows; the
first two longer interfaces are 9 and 10, while the last is 24 because the
outer factor has span 6.  The seven exhaustive state counts are

```text
17529, 74935, 58703, 61484; 8619, 46498; 6523.
```

No run reaches the cap.  The location predicates are also compared with an
explicit token-path model on all 300 location pairs in the root, one-splitter,
chain and fork micro-skeletons.  Consequently

```text
K=3 rows: 34 -> 31;  all terminal rows: 37 -> 34.   (FW164)
```

This is an **OBSERVED conditional all-order three-row exclusion**, not a
realisation or exclusion of the other 31 `K=3` rows.  Production replay and
frozen certificate:

```text
theory-lab/topwindow/verify_endpoint_two_small_factor_root_hierarchy.py
theory-lab/topwindow/results/endpoint_two_small_factor_root_hierarchy_certificate.json
```

Removing the FW163--FW164 rows also sharpens the inherited core constants.
For every current `K=3` row, recompute the two pointwise quantities

```text
epsilon=N-2q,
D=q-L_0=1+binom(a,2)+binom(b,2)+(Q-R).
```

The 31 rows have `epsilon<=1`, `D<=22`, and, more importantly, the correlated
loss satisfies

```text
epsilon+2D<=28.
```

The three `K=2` rows retain their exact pairs
`(epsilon,D)=(-1,7),(2,9),(1,5)`, whose corresponding losses are 13, 20 and
11.  Hence all 34 FW164 terminal rows obey the strictly stronger bounds

```text
q-L_0<=22,               2L_0>=N-28.              (FW165a)
```

In particular (FW162a) improves from 29 missing values to

```text
|{1,...,q-1} minus D_0|<=21,
w_{k+1}<=Pi_k+22.                                  (FW165)
```

The proper inherited core still has order at least `n-5`; only its defect has
changed.  Replaying the shape-free capacities at
`n=36,38,49,51,64,66,81,83` changes the simple structure orders to

```text
7,8,10,10,12,13,15,16
```

and the jointly packed orders to

```text
8,8,11,11,13,14,17,17.
```

Retaining each row's actual pole orders and loss leaves the already sharper
correlated orders `8,9,11,11,14,14,17,17`, now with strict margins
`45,10,25,54,19,54,45,114`.  Thus the main new information is the defect-21
covering schedule and the pointwise `N-28` mass bound, rather than a new
asymptotic constant.

This is an **OBSERVED conditional all-order refined mass/inheritance
theorem**, not a descent or exclusion of a remaining row.  Arithmetic replay
and frozen certificate:

```text
theory-lab/topwindow/verify_endpoint_terminal_mass_refined.py
theory-lab/topwindow/results/endpoint_terminal_mass_refined_certificate.json
```

There is a substantially sharper *localized* inheritance bound at the
receiving edge `t`.  It does not replace the interval-to-`q` mass estimate in
(FW165a); instead it uses the exact pair partition in (FW78).  Every value
strictly below `t` is realised either by a pair internal to `C_0`, by a pair
internal to `A`, or by a pair internal to `B`: an `A--C_0` pair is at least
`q`, an `A--B` pair is larger still, and a `B--C_0` pair is of the form
`t+x` with `x>=0`.  Global distance uniqueness therefore gives

```text
|{1,...,t-1} minus D_0|<=binom(a,2)+binom(b,2).   (FW166a)
```

Moreover (FW77) gives `t-h=R>=1`.  Every edge of `C_0` lies on a path from
`v` to a lower-core vertex of `v`-depth at most `h`; positivity of the edge
weights makes its own weight at most `h<t`.  Thus (FW166a) covers every edge
rank of `C_0`, not merely an initial segment.  With the notation of (FW162),
all but at most `e=binom(a,2)+binom(b,2)` of the values below
`w_{k+1}` are internal distances of `C_0`.  Every path realising such a value
uses only edges lighter than `w_{k+1}`, so

```text
Pi_k>=w_{k+1}-1-e,
w_{k+1}<=Pi_k+e+1.                                (FW166b)
```

For the 31 then-current `K=3` rows, `a,b<=2` and hence `e<=2`.  The three `K=2`
rows have pole-order pairs `(1,3),(2,3),(3,1)`, giving respectively
`e=3,4,3`.  Uniformly over all 34 rows,

```text
|{1,...,t-1} minus D_0|<=4,
w_{k+1}<=Pi_k+5             (0<=k<=m-2).          (FW166)
```

This is an **OBSERVED conditional all-order defect-four prefix-inheritance
theorem**.  It is not a claim that `C_0` is a Leech tree.  Its missing values
and the rooted cross-sum holes in the finite-hole ladder are different
notions, but they can be composed after explicitly accounting for both kinds
of deficit.  The constant-memory finite replay and frozen certificate are

```text
theory-lab/topwindow/verify_endpoint_terminal_prefix_defect.py
theory-lab/topwindow/results/endpoint_terminal_prefix_defect_certificate.json
```

That accounting gives the first genuinely internal directional bridge.  Fix
an edge of `C_0` of weight `w`, delete it, and root its two components at the
cut endpoints.  If their rooted depth sets are `X` and `Y`, the pairs crossing
the edge have distances

```text
w+x+y,                  x in X, y in Y.
```

Every coefficient of `X+Y` is at most one by global distance uniqueness, and
the two rooted factors have disjoint internal distance sets.  Consider a
deficit `j>=1` with `w+j<t`.  If `j` is absent from `X+Y`, then either
`w+j` is one of the at most `e` lower-core values missing below `t`, or its
unique realising pair lies wholly inside one of the two components of
`C_0-w`.  Therefore, if no such same-side pair occurred through deficit
`K(e)`, the actual rooted factors would give a state surviving the
finite-hole ladder with at most `e` holes through its audited death index
`K(e)`, a contradiction.  Hence

```text
t-w<=K(e),
or some same-side C_0 pair has distance w+j,
   1<=j<=K(e).                                     (FW167a)
```

The boundary is exact: the ladder alternative is used when
`w+K(e)<t`; otherwise integer weights give `t-w<=K(e)`.  The current budget
distribution and audited death indices are

```text
e:                 0   1   2   3   4
current rows:      7  23   1   2   1
K(e):             10  19  22  31  34.
```

In particular all 31 FW164 `K=3` rows have `K(e)<=22`, the three `K=2` rows have
offsets `31,34,31`, and every row in this 34-row relaxation satisfies

```text
t-w<=34,
or one side of C_0-w contains a pair of distance in
   {w+1,...,w+34}.                                  (FW167)
```

The pair in the second alternative is wholly internal to the proper lower
core; neither pole can supply it.  Thus (FW167) closes the former logical gap
between bounded prefix defect and the finite-hole handoff.  It still does
not say that the handoff path contains an edge heavier than `w`, and repeated
applications need not yet choose nested sides.  Turning this strict internal
pair handoff into a nested-edge descent, or proving that every reversal
accumulates at a thick centre, remains **UNVERIFIED**.  The certificate
composition is replayed without rerunning the large ladder search by

```text
theory-lab/topwindow/verify_endpoint_terminal_core_handoff.py
theory-lab/topwindow/results/endpoint_terminal_core_handoff_certificate.json
```

The remaining reversals can now be localized to a bounded core.  Call a
lower-core edge *near* when `t-w<=34`, and let `F` be the forest formed by all
near edges of `C_0`.  Edge weights are distinct integers and every core edge
is below `t`, so there are at most 34 near edges.  Consequently every
component of `F` has order at most 35.  Contract every component of `F` in
`C_0`.  For each remaining edge, choose one of the same-side pairs supplied
by (FW167) and orient the contracted edge toward the side containing that
pair.  The contracted graph is a finite tree, so following arrows terminates
at a sink node.  Lifting that node gives a connected near-edge component `S`
such that

```text
|S|<=35, and every edge on the boundary of S has weight <t-34
and hands to a C_0 pair on the S-side at an offset at most 34.  (FW168)
```

If there are no remaining edges, take `S=C_0`; the same order bound follows
from `|E(C_0)|<=34`.  Thus failure of immediate nested descent is no longer
an unbounded directional corridor: it accumulates at a uniformly bounded
lower-core handoff sink.  This is an **OBSERVED conditional all-order bounded
sink reduction**.  The sink `S` is new and must not be confused with the
original singleton full-window sink `{v}`.  Its incident branch complements
may still be arbitrarily large, and (FW168) alone gives neither a finite
classification nor a contradiction.  The next global task is to combine its
inward low handoffs with the already proved thin-arm/quadratic-thick-centre
dichotomy.

The later rows of the same finite-hole ladder give multiplicity, not just one
handoff.  If `w+51<t`, its hole-eight row says that at least nine of the first
51 positive deficits are not crossing sums.  At most `e<=4` of them are
genuine values missing from `D_0`, so at least `9-e` distinct deficit values
are realised by same-side pairs in `C_0-w`.  The current row distribution is

```text
e:                              0   1   2   3   4
current rows:                   7  23   1   2   1
minimum same-side pairs by 51:  9   8   7   6   5.
```

Thus every row in this 34-row relaxation satisfies

```text
t-w<=51,
or one side of C_0-w contains at least five distinct pairs
   with distances in {w+1,...,w+51}.               (FW169)
```

Every `K=3` row has at least seven such pairs; the three `K=2` rows have at
least `6,5,6`.  This is an **OBSERVED conditional all-order internal-handoff
multiplicity theorem**.  The pairs are distinct for one cut edge, but pairs
selected at different edges may be reused, so their counts cannot simply be
summed.  Constant-memory certificate composition:

```text
theory-lab/topwindow/verify_endpoint_terminal_core_handoff_multiplicity.py
theory-lab/topwindow/results/endpoint_terminal_core_handoff_multiplicity_certificate.json
```

The near-edge sink in (FW168) has a much sharper shape than a general
35-vertex tree.  In the current `n>=36` terminal, (FW148) gives `h>=134`, so
`t=h+R>=135`.  Suppose a lower-core edge `w>=t-34` were internal to one of
the lower arms, whose incident edge is `p`.  By (FW48), `p>w`, and the
`v`-path to an endpoint beyond `w` would have length at least

```text
p+w >= 2t-67 > t > h,
```

contrary to the definition of the lower height `h`.  Hence every edge in the
near window `[t-34,t-1]` is incident with `v`.  Their forest is one star at
`v` plus isolated vertices.  Moreover a lower arm with near incident edge
`w` has rooted eccentricity at most

```text
h-w <= 34-R <=33.
```

Its rooted depths are distinct integers, so the complete arm has order at
most 34.  There are at most 34 such incident edges.  Consequently the sink
of (FW168) can be enlarged, if it contains `v`, by absorbing all of its near
incident arms, giving the exact structural alternative

```text
S* is a singleton not containing v, or
S* contains v and is the union of v with at most 34 complete
   lower arms, each of order at most 34;
in both cases |S*|<=1157 and every boundary edge hands inward. (FW170)
```

This **OBSERVED conditional all-order star-sink reduction** makes the bounded
core topologically explicit.  It still permits unbounded far arms at its
boundary; exclusion requires showing that their inward multiplicities force
the quadratic thick-centre branch, or that one of them admits strict nested
descent.

Every edge strictly inside one of those far lower arms is automatically in
the multiplicity regime.  Let `u` be such an edge and let `p` be the arm's
edge incident with `v`.  Equation (FW48) gives `p>u`.  A `v`-path to an
endpoint beyond `u` contains both positive edges, while every lower-core
vertex has `v`-depth at most `h`.  Therefore

```text
2u+1 <= p+u <= h,
u <= floor((h-1)/2).                               (FW171a)
```

Since the current terminal has `h>=134` and `t=h+R` with `R>=1`,

```text
t-u >= h+R-floor((h-1)/2) >=69>51.                (FW171b)
```

Thus (FW169) applies to **every** non-incident edge of every lower arm: one
side of its core cut contains at least five distinct pairs within 51 above
the edge, and at least seven in every `K=3` row.  Consequently all
uncontrolled near-`t` exceptions are `v`-incident arm boundaries; no
unbounded arm can hide an exceptional internal corridor.  This is an
**OBSERVED conditional all-order internal-arm multiplicity theorem**, not a
descent by itself: the same-side pairs may consistently lie toward `v`, in
which case they accumulate at the star sink rather than move outward into a
nested proper arm.

The global three-branch hypothesis now makes the topology of those arms
exact.  The no-bi-spider theorem says that every target-order tree has at
least three branch vertices, while the present terminal assumes at most
three; hence it has exactly three.  In a `K=2` row the unique order-three top
pole contributes one branch vertex at its attachment root and `v` contributes
a second.  Therefore `C_0` contains exactly one further branch vertex `c`.
The (FW151)--(FW152) topology filter found no surviving placement of `c` in
the forced band, so an actual realisation must place it strictly outside that
band.  In a `K=3` row neither order-one/two pole root is a branch vertex, so
`C_0` contains exactly two further branch vertices `c,d` in addition to `v`.
Their minimal rooted skeleton is necessarily one of

```text
v--c--d,                    or                    c--v--d. (FW172a)
```

The exactly-three-branch normal form then says that every component attached
off this one- or two-segment skeleton is a path.  Consequently

```text
K=2: one hidden lower splitter and otherwise bare path legs;
K=3: exactly two lower splitters in a chain or fork and otherwise
     bare path legs.                                      (FW172)
```

This is an **OBSERVED conditional all-order exact-skeleton reduction**.  It
does not remove a row, because splitters and their compulsory legs can lie
entirely below the finite forced band; treating an unused inactive splitter
as absent would be an unsound exclusion.  Combined with (FW171), however, it
shows that the remaining unbounded objects are bare weighted corridors on a
fixed one-/two-splitter skeleton, not arbitrary rooted trees.  The next proof
must rule out a corridor whose every fivefold handoff points back toward the
bounded star, or turn one outward handoff into strict nested descent.

The fivefold handoff has an exact global accounting consequence.  Use the
Kruskal notation in `docs/kruskal-covering-waste.md`: if `u=w_k`, let

```text
sigma_{k-1}=Pi_{k-1}-(w_k-1).
```

The strengthened exact waste identity proved there is

```text
TW=(sum_j Delta_j^2-N)/2+sum_j Delta_j sigma_{j-1}. (FW173a)
```

Take the at least five same-side pairs supplied by (FW169) for an internal
lower-arm edge `u`.  Their paths do not use `u`.  If one path contains an
edge heavier than `u`, that edge lies in the same proper component of
`C_0-u`, giving the desired strict nested heavier-edge transition.  Otherwise
every one of the five paths uses only edges lighter than `u`.  Before `u` is
inserted, the light forest then realises five distinct distances greater than
`u`, and the exact interpretation of the covering surplus gives

```text
sigma_{k-1}>=5                 (>=7 in every K=3 row). (FW173b)
```

Finally, all edges internal to a lower arm precede that arm's incident edge
by (FW48).  Their Kruskal merge products therefore count precisely the
unordered vertex pairs internal to that arm.  Summing over the lower arms,

```text
sum_{k: w_k internal to a lower arm} Delta_k=I_R.  (FW173c)
```

Consequently the remaining corridors satisfy the all-order alternative

```text
some internal lower-arm handoff contains a heavier edge in its
  proper side; or
TW >= (sum_j Delta_j^2-N)/2 + 5 I_R,
  with 7 I_R in every K=3 row.                         (FW173)
```

This is an **OBSERVED conditional all-order nested-descent versus weighted-
waste theorem**.  It is the first step here that turns consistent reverse
handoffs into an additive global invariant rather than another local shape.
It is not yet a contradiction: when `I_R` is small the lower mass is spread
among many arms and must instead be charged to the quadratic thick-centre
cross pairs; when `I_R` is large, a matching terminal-profile upper bound on
`TW` is still required.  The exact surplus identity is independently replayed
on all five known witnesses (each through both checkers) and on the existing
900 deterministic distinct-distance controls by
`theory-lab/smallend/verify_kruskal_waste.py`.

The complete low interval gives multiplicity growing with the imbalance of
the cut.  Let an internal lower-core edge `u` split `C_0` into orders
`s,m-s`, where `m=n-a-b`.  Among the `t-u-1` integer values in
`{u+1,...,t-1}`, at most `e=binom(a,2)+binom(b,2)<=4` are missing from the
core by (FW166a), and at most `s(m-s)` can be realised by pairs crossing the
edge.  Every remaining value is realised by a same-side pair.  Hence

```text
H_u >= [t-u-1-e-s(m-s)]_+.
```

For an internal arm edge, (FW171a) and `t=h+R` turn this into

```text
H_u >= [floor(h/2)+R-e-s(m-s)]_+.
```

Combining it with the hole-eight finite ladder gives the pointwise bound

```text
kappa(s)=max(9-e, floor(h/2)+R-e-s(m-s)),
H_u>=kappa(s).                                      (FW174a)
```

Exactly as in (FW173b), either one of these paths contains a heavier edge in
the same proper side, or `sigma_{k-1}>=kappa(s)` for `u=w_k`.  Thus the
constant five is needed only near balanced cuts.  If a bare pendant path leg
has order at least `S+1`, its first `S` cuts from the free end have side orders
`1,...,S`; if none yields nested descent, its contribution to the weighted
covering-surplus term is at least

```text
sum_{s=1}^S kappa(s),                              (FW174b)
```

because every corresponding merge product is at least one.  On the current
rows, after the necessary parity filter `h=(N-E)/2 in Z`, the uniform finite
values are

```text
n:                         36   38   49   51   64   66   81   83
S:                          5    5    7    7    9    9   11   12
required leg order S+1:     6    6    8    8   10   10   12   13
sum kappa(s):             315  380  861  987 2013 2220 4191 4520.
```

The scale is cubic, not merely linear.  Uniformly over the finite affine row
set, `m=n-O(1)` and `h=N/2-O(1)`.  Put

```text
alpha=(1-1/sqrt(2))/2,
```

the smaller root of `alpha(1-alpha)=1/8`.  Summing the positive capacity
term through `s=alpha n+O(1)` gives

```text
integral_0^alpha (1/8-x(1-x)) dx
  =(sqrt(2)-1)/48.
```

Therefore every bare leg of order at least `alpha n+O(1)` satisfies

```text
strict nested heavier-edge descent, or
sum Delta_k sigma_{k-1}
  >=((sqrt(2)-1)/48)n^3+O(n^2).                  (FW174)
```

This is an **OBSERVED conditional all-order cut-capacity descent-versus-cubic-
waste theorem**.  It closes the earlier scale mismatch for a long thin leg,
but not the whole terminal: if all legs are shorter than `alpha n+O(1)`, the
vertex mass is distributed among several legs at the fixed three-centre
skeleton and must be handled by the thick-centre cross-arm argument.  The
finite row arithmetic is frozen by the constant-memory replay

```text
theory-lab/topwindow/verify_endpoint_terminal_cut_capacity.py
theory-lab/topwindow/results/endpoint_terminal_cut_capacity_certificate.json
```

The same calculation treats the two bare segments of the three-centre
skeleton, not only pendant legs.  Along a corridor with no off-path attachment
at an internal vertex, orient the edges from one endpoint.  Their core-side
orders are consecutive integers

```text
s_0, s_0+1, ..., s_0+ell-1.
```

If none of the corresponding handoffs contains a nested heavier edge, then
(FW173a)--(FW174a) give the exact profile bound

```text
sum Delta_k sigma_{k-1}
  >=sum_{j=0}^{ell-1} kappa(s_0+j).                (FW175a)
```

After division by `m`, the growing part of `kappa` has limiting density
`1/8-x(1-x)`.  It is positive precisely outside

```text
[alpha,1-alpha],       alpha=(1-1/sqrt(2))/2.
```

Consequently a consistently reversing bare skeleton corridor has the
all-order alternative

```text
it pays cubic weighted covering surplus on every linear portion lying
  outside the central side-order band; or
both endpoint sides of its remaining central portion have order at
  least alpha m-O(1).                               (FW175)
```

This is an **OBSERVED conditional all-order corridor-to-two-thick-blocks
reduction**.  It leaves no third diffuse possibility: long unbalanced
corridor tails are already charged by (FW175a), while an uncharged linear
middle separates two linearly large endpoint blocks.  What remains
**UNVERIFIED** is the collision/waste upper bound for those two thick blocks
on the fixed three-centre skeleton.

The pendant-leg charge can retain its actual Kruskal merge products.  Index
the first `S` edges of a bare leg from its free end.  If the edge whose
free-side order is `s` has global weight rank `k(s)`, write
`Delta_s=Delta_{k(s)}` and `sigma_s^*=sigma_{k(s)-1}`.  For every `r<=S`,
all pairs among the first `r+1` leg vertices have their unique maximum path
edge among those first `r` edges.  Each such pair is first connected at that
edge, so

```text
D_r:=sum_{s=1}^r Delta_s >= binom(r+1,2).          (FW176a)
```

On `1<=s<=m/2`, the profile `kappa(s)` in (FW174a) is nonincreasing.  If none
of the first `S` handoffs contains a nested heavier edge, then
`sigma_s^*>=kappa(s)`, and Abel summation with (FW176a) gives

```text
sum_{s=1}^S Delta_s sigma_s^*
 >=sum_{s=1}^S Delta_s kappa(s)
 >=sum_{s=1}^S s kappa(s).                         (FW176b)
```

At the eight target orders, using the same uniform thresholds as (FW174),
the strengthened finite lower bounds are

```text
n:                         36   38    49    51    64    66     81     83
S:                          5    5     7     7     9     9     11     12
sum s kappa(s):           675  850  2380  2800  6990  7860  17776  19656.
```

Asymptotically,

```text
integral_0^alpha x(1/8-x(1-x)) dx
  =(8sqrt(2)-11)/768,

sum Delta_s sigma_s^*
  >=((8sqrt(2)-11)/768)n^4+O(n^3).                (FW176)
```

This is an **OBSERVED conditional all-order merge-product amplification** of
(FW174), not a terminal exclusion.  Its leading constant is approximately
`0.000408475`, well below the trivial total-distance coefficient `1/8`, so a
single charged leg does not by itself contradict the global budget.  The
remaining task is to aggregate the charges from all legs and skeleton
segments, or obtain the still **UNVERIFIED** sharper upper bound for the two
thick endpoint blocks.  The constant-memory replay and a 46,233-path-order
finite control are

```text
theory-lab/topwindow/verify_endpoint_terminal_merge_amplification.py
theory-lab/topwindow/results/endpoint_terminal_merge_amplification_certificate.json
```

The complementary many-short-leg case admits a connected-bundle
amplification.  Fix a non-root lower-core branch centre and a complete
collection of its bare pendant arms.  Every selected edge is then internal to
a lower arm and is not one of the exceptional edges incident with `v`.  Let
"Complete" here means that each selected arm contains every edge and vertex
from that centre through its leaf; the skeleton edge from the centre toward
`v` is not selected.  Let
the arms' total off-centre order be `V`, and suppose every arm has order at
most `S<=m/2`.  For an edge in one of these arms, let `s` be the order of its
free-side component.  Then `1<=s<=S`, and the profile in (FW174a) is
nonincreasing on this interval.  If none of the selected handoffs contains a
heavier edge in the same proper side, (FW174a) gives

```text
sigma_e>=kappa(s)>=kappa(S).
```

The centre together with all selected arms is a connected induced subtree of
order `V+1`.  The connected-subtree merge-mass inequality therefore yields

```text
sum_{e in the selected arms} Delta_e >= binom(V+1,2),

sum_{e in the selected arms} Delta_e sigma_e
  >=kappa(S) binom(V+1,2).                         (FW177a)
```

Thus the several-short-leg thick centre is no longer charged one edge at a
time.  If

```text
V=beta n+O(1),       S=gamma n+O(1),       gamma<alpha,
alpha=(1-1/sqrt(2))/2,
```

then the terminal rows have `m=n-O(1)`, `h=N/2-O(1)` and bounded `R,e`, so
(FW177a) gives

```text
sum Delta_e sigma_e
 >= beta^2[1/8-gamma(1-gamma)]n^4/2+O(n^3).       (FW177)
```

This is an **OBSERVED conditional all-order short-arm star-bundle
amplification**, not a terminal exclusion.  It handles the diffuse side of
the FW174/FW176 dichotomy at a non-root lower-core centre: a linear mass
spread over uniformly short arms pays quartic weighted covering surplus even
when no individual arm is long.  A bundle of arms incident directly with
`v` is still outside (FW174), as are the missing combination with the
long-corridor charges and the terminal waste upper bound.  The replay checks
profile monotonicity on all 34 FW164 rows and 46,003 small ambient edge
orders:

```text
theory-lab/topwindow/verify_endpoint_terminal_star_bundle.py
theory-lab/topwindow/results/endpoint_terminal_star_bundle_certificate.json
```

There is nevertheless an all-order cap on how many of the lower-core arms
can be incident directly with `v`.  Let

```text
d_v=number of components of C_0-v.
```

Choose a farthest vertex `x_i` in each component and write
`z_i=d(v,x_i)`.  The `z_i` are distinct, because two equal root depths would
already repeat a distance from `v`.  For `i<j`, the vertices lie in different
components of `C_0-v`, so

```text
d(x_i,x_j)=z_i+z_j.
```

Global distance uniqueness says that these restricted pair sums are all
different.  After subtracting `min_i z_i`, the `d_v` depths therefore form a
weak Sidon set in `[0,h-1]`.

The standard weak-Sidon extremal function `f(H)` satisfies

```text
f(H)<=sqrt(H)+O(H^(1/4)).
```

This is a **LITERATURE** theorem due to Ruzsa, with the proof used here read
in Kayll, *Discrete Mathematics* 299 (2005), 141--144; see L21 in the
literature ledger.  Since the current rows have
`h=N/2-O(1)=n^2/4+O(n)`, it gives

```text
d_v<=n/2+O(sqrt(n)).                              (FW178a)
```

For a finite replay no hidden asymptotic constant is needed.  Let
`0<=a_1<...<a_d<=H` be weak Sidon and fix `1<=q<d`.  Select all positive
differences `a_{i+s}-a_i` with `1<=s<=q`.  Their number is

```text
M=qd-q(q+1)/2.
```

Any positive difference occurs at most twice.  Indeed, equality between two
different ordered differences rearranges to equality of two restricted pair
sums unless the two intervals meet at their common middle point.  Thus a
repeat is a three-term arithmetic progression.  Moreover two different
repeats cannot have the same middle member, since their two endpoint pairs
would have the same restricted sum.  Hence at most `d-2` distinct
differences repeat.  Put

```text
r=min(d-2,floor(M/2)).
```

Among `M` positive-integer occurrences with multiplicity at most two and at
most `r` repeats, the minimum sum is obtained from
`1,1,2,2,...,r,r,r+1,...,M-r`.  On the other hand, writing each selected
difference as a sum of adjacent gaps, a fixed span `s` uses every gap at
most `s` times.  The exact necessary inequality is therefore

```text
M(M+1)/2-r(M-r) <= q(q+1)H/2             (1<=q<d). (FW178b)
```

Testing (FW178b) for every `q`, every parity-compatible current row, and the
trivial cardinality cap `d_v<=m-1` gives

```text
n:                                  36  38  49  51  64  66  81  83
uniform upper bound on d_v:         25  27  33  34  42  43  52  53
uniform lower bound on
  non-v-incident C_0 edges:          5   6  10  12  16  18  23  25.
```

Since `C_0` has `m=n-O(1)` vertices and exactly `d_v` of its `m-1` edges are
incident with `v`, the literature asymptotic also gives

```text
#{non-v-incident C_0 edges}>=n/2-O(sqrt(n)).       (FW178)
```

The reduction from root arms to weak Sidon sets and the exact inequality
(FW178b) are **OBSERVED conditional all-order** statements; (FW178a) uses the
separately labelled literature theorem.  This forces a linear number of
lower-core edges into the FW171/FW174 non-incident regime, but is not a
terminal exclusion.  In particular, many arms of order two incident with
`v` can put all their one-edge handoffs back toward `v`; neither (FW177) nor
(FW178) yet aggregates that robust-spider configuration.  The constant-memory
replay, including all weak Sidon subsets of `[0,16]`, is

```text
theory-lab/topwindow/verify_endpoint_terminal_root_arms.py
theory-lab/topwindow/results/endpoint_terminal_root_arms_certificate.json
```

The same weak-Sidon set supplies the missing aggregation at `v`, but through
path slack rather than connected Kruskal mass.  Let `p_1<...<p_d` be the
weights of the `d=d_v` lower-core edges incident with `v`, and let `y_i` be
the opposite endpoint of `p_i`.  For every prefix, the distances
`d(y_i,y_j)=p_i+p_j` show that `{p_1,...,p_i}` is weak Sidon.  Define `G(i)`
to be the largest lower bound on the containing interval obtained from
(FW178b): `G(1)=0`, and for `i>=2`,

```text
G(i)=max_{1<=q<i} ceil(2 L(i,q)/(q(q+1))),
L(i,q)=M(M+1)/2-r(M-r),
M=qi-q(q+1)/2,       r=min(i-2,floor(M/2)).        (FW179a)
```

Translate the first `i` weights by `p_1`.  Their span is `p_i-p_1`, so
(FW178b), positivity and `p_1>=1` give

```text
p_i>=G(i)+1.
```

The path from `y_i` to `y_j` consists of exactly the two edges `p_i,p_j`.
For `i<j`, its contribution to the global path slack `TW` is therefore

```text
(p_i+p_j)-max(p_i,p_j)=p_i.
```

These are distinct paths, so they may be summed without any handoff
multiplicity issue:

```text
TW >= TW_root
   :=sum_{1<=i<j<=d} min(p_i,p_j)
    =sum_{i=1}^d (d-i)p_i
   >=J(d):=sum_{i=1}^d (d-i)(G(i)+1).              (FW179b)
```

This leading term is already self-contained: in (FW179a) choose
`q=floor(sqrt(i))`.  Then `M=i^(3/2)+O(i)`, `r<=i`, and hence
`L(i,q)>=i^3/2-O(i^(5/2))`, while `q(q+1)=i+O(sqrt(i))`.  Therefore
`G(i)>=i^2-O(i^(3/2))`, and consequently

```text
J(d)>=d^4/12-O(d^(7/2)).                           (FW179c)
```

For any fixed `0<beta<1`, the root terminal therefore has the parameterized
alternative

```text
d_v>=beta n:
  TW_root>=beta^4 n^4/12-O(n^(7/2));
or
d_v<beta n:
  #{non-v-incident C_0 edges}>=(1-beta)n-O(1).     (FW179)
```

The exact and asymptotic parts (FW179a)--(FW179c) are **OBSERVED conditional
all-order** statements.  The Kayll/Ruzsa theorem in (FW178a) independently
gives the same scale, but is not load-bearing here.  At the convenient finite
split `d_v>=ceil(n/4)`, the current rows give

```text
n:                               36   38   49   51    64    66    81    83
ceil(n/4):                        9   10   13   13    16    17    21    21
J(ceil(n/4)):                   167  250  713  713  1707  2214  5544  5544
if d_v<ceil(n/4), minimum
  non-v-incident C_0 edges:      22   24   31   34    43    45    55    58.
```

Thus the robust-spider obstruction is now a quantitative dichotomy: a linear
root degree pays quartic path slack directly, while a sparse root leaves
three quarters of the core edges in the non-incident regime.  This is still
not a terminal exclusion because no conflicting terminal upper bound on
`TW` has yet been proved, and the sparse branch still needs the FW176/FW177
charges aggregated over the fixed skeleton.  The constant-memory replay is

```text
theory-lab/topwindow/verify_endpoint_terminal_root_slack.py
theory-lab/topwindow/results/endpoint_terminal_root_slack_certificate.json
```

The sparse side of this dichotomy admits an exact component aggregation that
does not assume that the root arms are paths.  Let

```text
C_1,...,C_d = components of C_0-v,       s_i=|C_i|,
d=d_v,                                   sum_i s_i=m-1.
```

Suppose first that `s_i<=m/2`.  Every edge of `C_i` is non-`v`-incident,
and the smaller side of its core cut has order at most `s_i`.  The profile
`kappa` in (FW174a) is nonincreasing on `[1,m/2]`.  Hence, in the branch in
which none of these handoffs contains a nested heavier edge,

```text
sigma_e>=kappa(s_i)                  (e in E(C_i)).
```

Each `C_i` is a connected induced subtree, so the connected-subtree merge-
mass inequality gives

```text
sum_{e in E(C_i)} Delta_e >= binom(s_i,2).
```

The exact weighted-surplus identity and (FW179b) may therefore be used
separately and combined by taking their maximum (not their sum):

```text
TW >= max(
  J(d),
  sum_{i=1}^d kappa(s_i) binom(s_i,2)
).                                                   (FW180a)
```

This removes the apparent loss from charging one non-root edge at a time.
For a clean all-order consequence, suppose every root component has
`s_i<=m/8`.  Uniformly over the finite affine terminal rows,

```text
kappa(s_i)>=m^2/64-O(m),

sum_i binom(s_i,2)
  >=((m-1)^2/d-(m-1))/2.
```

If `d<=m^(4/5)`, the second entry of (FW180a) is
`Omega(m^(16/5))`; if `d>=m^(4/5)`, (FW179c) makes its first entry
`Omega(m^(16/5))`.  Since `m=n-O(1)`, the exact alternative is

```text
nested heavier-edge descent; or
max_i s_i>m/8; or
TW=Omega(n^(16/5)).                                  (FW180)
```

Thus the sparse-root branch can no longer remain both diffuse and merely
cubic: either it has a linear thick root component, or it pays a uniform
supercubic path-slack charge.  By (FW172), the thick component has at most
the fixed one-/two-splitter skeleton, but reducing that last component to a
charged pendant bundle or the two-thick-block corridor remains
**UNVERIFIED**.  Consequently (FW180) is an **OBSERVED conditional all-order
root-component aggregation theorem**, not a terminal exclusion and not a
global `TW` upper bound.

At the finite split `d<ceil(n/4)`, dynamic programming over component orders
`s_i<=floor(m/8)` gives the following exact lower bounds.  Rows in which the
partition is infeasible already have a component larger than `m/8`.

```text
n:                                  36    38    49    51     64     66     81     83
small-case feasible terminal rows:  13    17    17    17     17     17     17     17
minimum max(FW179b,FW180a):        1680  2312  6735  6405  18405  16671  44691  41640
minimizing d:                         8     9    12    12     15     16     20     20
```

The replay uses `O(md)` memory and performs no tree or edge-weight search:

```text
theory-lab/topwindow/verify_endpoint_terminal_component_aggregation.py
theory-lab/topwindow/results/endpoint_terminal_component_aggregation_certificate.json
```

The linear-component outcome in (FW180) has a shape-independent resolution.
Put

```text
tau=floor(m/8),
```

and take a component `C_i` with `s_i>tau`.  If some edge of `C_i` has
smaller core-cut side at least `tau+1`, that edge already separates two core
blocks of orders at least `tau+1`.  Otherwise every edge `e` of `C_i` has
smaller side `r_e<=tau`.  In the no-nested-descent branch, monotonicity of
the FW174 profile and connected-subtree merge mass give

```text
sum_{e in E(C_i)} Delta_e sigma_e
 >=kappa(tau) sum_{e in E(C_i)} Delta_e
 >=kappa(tau) binom(s_i,2)
 >=kappa(tau) binom(tau+1,2).                     (FW181a)
```

Here

```text
kappa(tau)>=m^2/64-O(m),
```

so (FW181a) is `Omega(n^4)`.  Combining it with (FW180) removes the diffuse
and thick root-component cases simultaneously:

```text
nested heavier-edge descent; or
some core edge has both sides >=floor(m/8)+1; or
TW=Omega(n^(16/5)).                                (FW181)
```

No one-/two-splitter classification is needed for this step.  The remaining
geometric outcome is now exactly a linear two-thick-block cut, rather than an
arbitrary thick component.  The alternative is an **OBSERVED conditional
all-order thick-component reduction**, not an exclusion: the thick cut still
needs its collision/waste treatment, and the large `TW` outcome still needs
a conflicting terminal upper bound.

At the eight target orders the uniform exact lower bounds in the large-
component/no-thick-cut branch are

```text
n:                              36   38    49    51    64    66    81    83
tau=floor(m/8), worst row:        4    4     5     6     7     8     9    10
kappa(tau), worst row:           35   46    82    59   118    87   179   139
kappa(tau) binom(tau+1,2):      350  460  1230  1239  3304  3132  8055  7645
```

The constant-memory replay is

```text
theory-lab/topwindow/verify_endpoint_terminal_thick_component.py
theory-lab/topwindow/results/endpoint_terminal_thick_component_certificate.json
```

The remaining thick cut has a general per-edge path-slack bound.  Let an edge
`e` have weight `u`, full-tree cut product `c_e`, and Kruskal merge product
`Delta_e`.  Exactly `Delta_e` of the `c_e` paths crossing `e` have `e` as
their maximum edge.  Their distances are distinct, one is the one-edge path
of distance `u`, and hence their nonnegative slacks have sum at least
`binom(Delta_e,2)`.  Every other crossing path has `e` as a nonmaximum edge,
so its slack contains at least the summand `u`.  The two path classes are
disjoint, and therefore

```text
TW >= binom(Delta_e,2)+u(c_e-Delta_e).             (FW182a)
```

Minimizing exactly over the integer `1<=Delta_e<=c_e` gives

```text
F(c,u)=binom(c,2),                    u>=c,
F(c,u)=uc-binom(u+1,2),               u<c,

TW>=F(c_e,u).                                      (FW182b)
```

For the FW181 thick edge, put `tau=floor(m/8)`.  Its full cut product is at
least the conservative core product

```text
c_e>=(tau+1)(m-tau-1)=Omega(n^2).
```

If `u>=ceil(m^(6/5))`, (FW182b) is `Omega(n^(16/5))` (and becomes
`Omega(n^4)` when `u` is comparable with or exceeds `c_e`).  Thus (FW181)
sharpens to

```text
nested heavier-edge descent; or
TW=Omega(n^(16/5)); or
a core edge with both sides >=floor(m/8)+1
  and weight u<m^(6/5)+1.                          (FW182)
```

This is an **OBSERVED conditional all-order balanced-edge scale reduction**.
It is not a terminal exclusion: the remaining geometric object is a
subquadratic-weight linear separator, and no conflicting terminal `TW` upper
bound has yet been proved.

The exact finite lower bounds at the threshold weight are

```text
n:                              36    38     49     51     64     66      81      83
ceil(m^(6/5)), worst row:        62    69     94    102    134    142     181     190
conservative cut product:       108   145    228    246    408    432     660     690
F(c,u):                        4743  7590  16967  19839  45627  51191  102989  112955
```

The constant-memory replay is

```text
theory-lab/topwindow/verify_endpoint_terminal_balanced_edge_slack.py
theory-lab/topwindow/results/endpoint_terminal_balanced_edge_slack_certificate.json
```

The defect-four core schedule strengthens (FW182) by using paths disjoint
from the crossing paths.  Let the thick edge split the core into orders
`r,m-r`, put

```text
c_0=r(m-r),
H=[t-u-1-e-c_0]_+,
e=binom(a,2)+binom(b,2)<=4.
```

There are `t-u-1` candidate values in `{u+1,...,t-1}`.  At most `e` are
absent from the core and at most `c_0` are crossing distances, so at least
`H` distinct values are realised by same-side core pairs.  If one of their
paths contains an edge heavier than `u`, that edge gives the strict nested
transition in the same proper side.  Otherwise the path realising `u+j`
has maximum at most `u-1`, and hence slack at least `j+1`.  The `H` offsets
are distinct positive integers, so these same-side paths contribute at least

```text
2+3+...+(H+1)=H(H+3)/2.
```

They are disjoint from every path crossing `u`.  Consequently their direct
path-slack contribution may be added to (FW182b), with the full cut product
again conservatively replaced by `c_0`:

```text
nested heavier-edge descent; or
TW>=F(c_0,u)+H(H+3)/2.                            (FW183a)
```

This has a sharp geometric consequence.  Write `r=m/2+x`.  Uniformly on the
terminal rows,

```text
t=m^2/4+O(m),       c_0=m^2/4-x^2,
H>=[x^2-u-O(m)]_+.
```

After (FW182) has reduced to `u<m^(6/5)+1`, every fixed outer band such as
`min(r,m-r)<=3m/8` has `H=Omega(n^2)` and therefore pays `Omega(n^4)`.
At the finer moving scale, (FW183a) gives the alternative

```text
TW=Omega(n^(16/5)); or
|r-m/2|=O(n^(4/5)).                               (FW183)
```

Thus a low-waste survivor is not merely balanced by a fixed constant: its
low-weight separator must be an asymptotic near-bisection.  This is an
**OBSERVED conditional all-order same-side-hole amplification**, not an
exclusion; the low-weight near-bisection and the terminal `TW` upper bound
remain **UNVERIFIED**.

For reference, the exact unrestricted bound from (FW183a), and its exact
outer-band version under `u<ceil(m^(6/5))`, are

```text
n:                                      36    38    49    51    64    66     81     83
unrestricted minimum:                  540   598  1078  1159  1905  2012   3154   3291
outer band min side<=floor(3m/8):     1390  1473  3283  3406  6673  6844  15309  15556
outer-band same-side H:                 46    47    73    74   106   107    165    166
```

The replay examines 5,987,386 bounded integer parameter states in about six
seconds with constant-size state and no tree enumeration:

```text
theory-lab/topwindow/verify_endpoint_terminal_balanced_edge_holes.py
theory-lab/topwindow/results/endpoint_terminal_balanced_edge_holes_certificate.json
```

The near-bisection geometry cannot occupy a separate low-waste terminal on
the fixed FW172 skeleton.  Suppose, toward the scale contradiction, that no
nested heavier-edge transition occurs and

```text
TW=o(n^(16/5)).
```

Choose the FW181 thick edge and take its side not containing `v`.  By
(FW182)--(FW183), that side has order `m/2+O(n^(4/5))`, in particular linear
order.  It contains at most the two non-root lower splitters from (FW172).
After removing those at most two splitter vertices, its complete inventory is

```text
at most two bare skeleton corridors, and
at most two complete pendant-arm bundles at non-root centres.    (FW184a)
```

Thus one of these at most four bins has linear order.  A linear pendant bin
pays quartically.  Indeed, fix a sufficiently small constant `delta<1/8`.
If one arm has order at least `delta n`, its first `delta n+O(1)` free-end
cuts have `kappa=Omega(n^2)` and connected prefix merge mass
`Omega(n^2)`, as in (FW176).  Otherwise the complete bundle has linear total
order and maximum arm order below `delta n`, so (FW177) again gives
`Omega(n^4)` weighted covering surplus.

A linear bare corridor is equally impossible.  Its core-cut side orders are
consecutive.  Among its balanced edges, (FW182)--(FW183) confine every
low-waste cut to an `O(n^(4/5))` window about `m/2`, hence only `o(n)`
corridor edges.  A remaining linear set of corridor edges has smaller core
side at most `m/8+O(1)`; one of its at most two contiguous tails is linear.
On that tail

```text
kappa>=m^2/64-O(m),
sum Delta_e>=binom(ell+1,2)=Omega(n^2),
```

so FW174 and connected-subtree merge mass also pay `Omega(n^4)`.  Each
possible linear bin contradicts `TW=o(n^(16/5))`.

It follows that the thick-cut outcome of (FW181) is absorbed by the already
charged corridor/bundle alternatives.  Combining this with the dense-root
side of (FW179) gives the current endpoint terminal the uniform synthesis

```text
strict nested heavier-edge descent; or
TW=Omega(n^(16/5)).                                (FW184)
```

This is an **OBSERVED conditional all-order sparse-root fixed-skeleton
synthesis**.  It completes the FW179 sparse-edge aggregation milestone, but
is not a terminal exclusion: the strict descent still has to close into an
already excluded terminal, and the supercubic path-slack branch still needs
a conflicting terminal upper bound.

The dependency and scale replay is

```text
theory-lab/topwindow/verify_endpoint_terminal_sparse_synthesis.py
theory-lab/topwindow/results/endpoint_terminal_sparse_synthesis_certificate.json
```

The root slack in (FW179) can retain the component orders instead of taking
only one endpoint per root branch.  Order the components of `C_0-v` by their
incident weights

```text
p_1<...<p_d,             s_i=|C_i|.
```

For `x in C_i` and `y in C_j`, every edge internal to `C_i` or `C_j` is
lighter than its incident edge by (FW48).  Hence the maximum edge on the
`x`--`y` path is `max(p_i,p_j)`, and that path contributes at least
`min(p_i,p_j)` to `TW`.  Summing these disjoint paths and using (FW179a)
gives the exact size-weighted root bound

```text
TW >= R(s_1,...,s_d)
   :=sum_{1<=i<j<=d} s_i s_j (G(i)+1).             (FW185a)
```

For a fixed multiset of component orders, the right side is minimized by
placing the largest `s_i` first, against the smallest incident weights.  This
follows from one adjacent swap: if positions `i,i+1` contain `x,y` and the
later total mass is `Z`, the original-minus-swapped cost is

```text
Z[(G(i+1)+1)-(G(i)+1)](y-x).
```

Now suppose every `s_i<=m/8`, put `M=m-1` and

```text
Q=sum_i s_i^2.
```

FW180 and the uniform profile lower bound give

```text
TW>=Omega(n^2)(Q-M).                               (FW185b)
```

If `Q>=M^(4/3)`, this is `Omega(n^(10/3))`.  Otherwise choose
`k=floor(M^2/(16Q))`.  Cauchy bounds the total mass in the first `k`
components by `sqrt(kQ)<=M/4`; the later components therefore have total
mass at least `3M/4` and quadratic cross mass.  Every pair of later
components has smaller incident weight at least

```text
p_{k+1}>=G(k+1)+1=Omega(k^2).
```

Thus (FW185a) gives

```text
TW>=Omega(k^2 M^2)=Omega(M^6/Q^2)
  >=Omega(n^(10/3)).                               (FW185c)
```

The large-component side uses the same fixed-skeleton proof as (FW184), now
at the parameter `10/3`: under `TW=o(n^(10/3))`, (FW182) makes every
balanced skeleton edge have weight `o(n^(4/3))`, while (FW183) confines it
to an `o(n^(5/6))` near-bisection window.  Both are subquadratic/sublinear,
so the linear-bin contradiction in (FW184a) is unchanged.  Consequently the
whole current endpoint terminal satisfies the stronger synthesis

```text
strict nested heavier-edge descent; or
TW=Omega(n^(10/3)).                                (FW185)
```

This is an **OBSERVED conditional all-order component-size-weighted root-
slack theorem**, not an exclusion.  It improves the proved waste exponent
from `16/5` to `10/3`; closure of the strict descent and a conflicting
terminal `TW` upper bound remain **UNVERIFIED**.

A conservative exact `Q`-threshold split gives

```text
n:                              36   38    49    51    64    66    81    83
uniform diffuse-case bound:    532  622  1158  1354  2757  2697  5214  5535
optimizing Q threshold:         46   56    69    92   100   125   126   156
optimizing prefix index k:       1    1     1     1     2     2     2     2
```

The replay also checks 2,030 small integer partitions and 1,277 exhaustive
component-order permutations:

```text
theory-lab/topwindow/verify_endpoint_terminal_weighted_root_slack.py
theory-lab/topwindow/results/endpoint_terminal_weighted_root_slack_certificate.json
```

The bounded-window handoff itself cannot run indefinitely toward the near-
`t` star.  Fix one of the current rows and put

```text
e=binom(a,2)+binom(b,2),
K=K(e) in {10,19,22,31,34}.
```

For a core edge of weight `w` with `t-w>K`, choose the same-side pair from
(FW167), of distance `w+j` with `1<=j<=K`.  Its path avoids the cut edge
`w`.  Edge weights are globally distinct, so if `f` is the maximum edge on
that path, exactly one of the following holds:

```text
f<w, giving a light handoff and sigma_{rank(w)-1}>=1; or
w<f<=w+j<=w+K.                                    (FW186a)
```

In the second case move to `f` and repeat.  The edge weight rises strictly at
every move, by at most `K`, and all edges remain in `C_0`.  Since `C_0` has
`m-1` edges, there are at most `m-2` moves before the process either reaches
a light handoff or enters `t-f<=K`.

For an internal lower-arm starting edge, (FW171a) gives

```text
w<=floor((h-1)/2).
```

Reaching the near window would therefore require more rise than is available
whenever

```text
t-floor((h-1)/2)>K(m-1).                          (FW186b)
```

On the current rows, `E=N-2h<=26`, `R=t-h>=1`, `K<=34`, and
`m-1<=n-3`.  Hence the left side of (FW186b) is at least `(N-20)/4`.
The uniform sufficient inequality is

```text
n^2-273n+776>0,
```

which holds for every `n>=271`; direct rowwise parity replay sharpens 271 to
266.  Thus above this threshold every FW167 ascent from an internal lower-arm
edge terminates strictly below the near-`t` star at a light handoff.

The same argument retains the multiplicity in (FW169).  Outside radius 51,
if all five supplied paths are light (seven in every `K=3` row), then the
terminal edge has `sigma>=5` (respectively 7); otherwise choose a heavy path
and rise by at most 51.  Now the uniform polynomial is

```text
n^2-409n+1184>0,
```

so for every `n>=407` the ascent ends at such a fivefold/sevenfold light
handoff rather than at the near star.  This gives the **OBSERVED conditional
all-order bounded-ascent termination theorem**

```text
n>=271: bounded FW167 ascent ends with sigma>=1;
n>=407: bounded FW169 ascent ends with sigma>=5 (>=7 in K=3). (FW186)
```

This is not yet the closure of (FW185).  Different starting edges may merge
into the same terminal ascent basin, so their terminal surplus cannot yet be
added, and the larger-offset handoffs used in (FW174) need not have bounded
weight rise.  What (FW186) rules out is an infinite or near-star escape of
the constant-window directional chain; basin congestion is the remaining
interface.

The constant-memory replay is

```text
theory-lab/topwindow/verify_endpoint_terminal_bounded_ascent.py
theory-lab/topwindow/results/endpoint_terminal_bounded_ascent_certificate.json
```

There is an exact accounting correction at the globally heaviest edge `q`.
It separates the fixed top-window contribution from the part that a terminal
upper bound must actually control.  Let `w_r=q`, let `Delta_i` be the Kruskal
merge products, and retain

```text
Pi(t)=#{pairs whose path maximum is at most t}.
```

Since every edge is at most `q`, `Pi(t)=N` for `t>=q`.  Therefore

```text
TW = binom(N-q+1,2)+RW_q,
RW_q:=sum_{t=1}^{q-1}(Pi(t)-t)>=0.                (FW187a)
```

The first term is not a new conditional charge: it is the unavoidable slack
of the unique paths of distances `q+1,...,N`, measured above their common
maximum-edge ceiling `q`.

The residual also has an exact merge-schedule form.  Put

```text
S=sum_{i<r}Delta_i=N-Delta_r,
E_q=S-(q-1)=sigma_{r-1}.
```

Using `w_i=1+Pi_{i-1}-sigma_{i-1}` and
`sum_{i<r}Pi_{i-1}Delta_i=(S^2-sum_{i<r}Delta_i^2)/2` gives

```text
RW_q = sum_{i<r} binom(Delta_i,2)-binom(E_q,2)
       +sum_{i<r}Delta_i sigma_{i-1}.             (FW187b)
```

In the current endpoint rows,

```text
q=N/2+O(1),             Delta_r=a(n-a)=O(n),
E_q=N-Delta_r-q+1=n^2/4-O(n).
```

Hence the first term in (FW187a) is already

```text
binom(N-q+1,2)=n^4/32+O(n^3).                    (FW187c)
```

Nonnegativity of `RW_q` is equivalently the exact compensation requirement

```text
sum_{i<r}binom(Delta_i,2)
 +sum_{i<r}Delta_i sigma_{i-1}
 >=binom(E_q,2).                                  (FW187d)
```

Both sides of (FW187d) have quartic scale here.  This reframes the terminal
endgame: it is not enough merely to raise an unconditional lower exponent for
the full `TW`.  One must either prove that the fixed three-centre skeleton
cannot supply the compensation in (FW187d), or localise an additional charge
inside `RW_q` and prove a conflicting upper bound for that same residual.

The qualification is essential.  The truncated base

```text
sum_{i<r}binom(Delta_i,2)-binom(E_q,2)
```

can be negative for an abstract valid covering schedule.  Consequently an
existing lower bound for the full `TW`, including (FW185), cannot simply be
added to the top triangle: its paths may already include the distances above
`q`.  This is the **OBSERVED exact heaviest-edge truncated-waste identity and
endgame correction**, not an exclusion or a residual upper bound.

At the eight target orders, the minimum fixed top triangle and minimum final
excess over the 17 parity-compatible rows are

```text
n:                         36     38      49      51      64      66       81       83
min top triangle:       47278  60378  168490  200661  500500  570846  1300078  1440753
min E_q:                  240    248     487     495     877     885     1455     1463
```

The replay exhausts 76,231 abstract covering schedules and checks all five
known Leech witnesses through both independent checkers:

```text
theory-lab/topwindow/verify_endpoint_terminal_truncated_waste.py
theory-lab/topwindow/results/endpoint_terminal_truncated_waste_certificate.json
```

The compensation cannot remain uniformly diffuse.  In the notation of
(FW187), put

```text
A=sum_{i<r}binom(Delta_i,2),       B=sum_{i<r}Delta_i sigma_{i-1},
D=max_{i<r}Delta_i,                Z=max_{i<r}sigma_{i-1},
S=sum_{i<r}Delta_i,                E=E_q.
```

Every `Delta_i` is positive and every covering surplus is nonnegative, so

```text
A<=S(D-1)/2,                       B<=SZ.
```

Combining these inequalities with (FW187d), and retaining the integer
rounding, gives the exact concentration bound

```text
S(D-1+2Z)>=E(E-1),
D+2Z>=1+ceil(E(E-1)/S),                         (FW188a)
max(D,Z)>=ceil((1+ceil(E(E-1)/S))/3).           (FW188b)
```

For the current affine endpoint rows,

```text
S=n^2/2-O(n),                    E=n^2/4-O(n),
```

and therefore

```text
max_{i<r}{Delta_i,sigma_{i-1}}>=n^2/24-O(n).    (FW188)
```

Thus every putative survivor has one of two concrete pre-`q` structures:

```text
large-merge branch:  some Delta_i>=n^2/24-O(n); or
high-surplus branch: some sigma_{i-1}>=n^2/24-O(n).
```

In the first branch, if the two Kruskal components joined by that edge have
orders `x<=y`, then `x+y<=n` and `xy=Delta_i`.  Consequently

```text
x>=((1-sqrt(5/6))/2)n-O(1) ~= 0.04356n-O(1),    (FW188c)
```

so this is a genuinely macroscopic light cut, not merely a large product of
bounded pieces.  The second branch exposes a single quadratically overfilled
covering threshold, which is the appropriate target for a residual-waste
upper bound.

This is the **OBSERVED exact pre-`q` compensation-concentration theorem**.
It is not an exclusion: it neither decides which branch occurs nor yet
contradicts the fixed three-centre geometry.  In particular a quadratic
surplus by itself contributes only one known large summand until its duration
or multiplicity is controlled.

The exact replay checks 76,219 nontrivial abstract covering schedules and all
17 compatible rows at each target order; the parent FW187 certificate carries
the five-by-five double-checker witness audit:

```text
theory-lab/topwindow/verify_endpoint_terminal_compensation_concentration.py
theory-lab/topwindow/results/endpoint_terminal_compensation_concentration_certificate.json
```

The two alternatives in (FW188) can be localised inside the truncated ledger.
For a pre-`q` edge of weight `w`, put `L=q-w`.  The `Delta` paths whose
maximum edge is `w` have distinct distances, one equal to `w`.  After capping
their path slack at `q`, their contribution to `RW_q` is at least

```text
Phi(Delta,L):=sum_{j=0}^{Delta-1}min(j,L).         (FW189a)
```

There is a second, independent area bound.  If
`sigma=Pi(w-1)-(w-1)`, then for `0<=j<=L`, monotonicity of `Pi` gives

```text
Pi(w-1+j)-(w-1+j)>=sigma-j.
```

Consequently

```text
RW_q>=Psi(sigma,L)
    :=sum_{j=0}^{L}max(sigma-j,0).                 (FW189b)
```

Let `M` be the exact right side of (FW188b).  If an FW188 witness has
`w<=q-M+1`, then `L>=M-1`; (FW189a) gives `binom(M,2)` in the large-merge
branch, while (FW189b) gives the still stronger `binom(M+1,2)` in the
high-surplus branch.  Thus the exact alternative is

```text
RW_q>=binom(M,2); or
some pre-q edge w>=q-M+2 has
  Delta_w>=M or sigma_{rank(w)-1}>=M.             (FW189c)
```

This top band lies strictly above every non-incident lower-arm edge.  Indeed,
(FW171a) puts such an edge at most at `floor((h-1)/2)`, and the current-row
arithmetic gives

```text
n:                           36   38    49    51    64    66     81     83
min M:                       35   35    74    73   136   134    230    226
min internal-edge runway:   160  178   296   321   506   538    812    853
min runway margin:          116  129   211   227   355   375    563    590
min binom(M,2):              595  595  2701  2628  9180  8911  26335  25425
```

Here the margin is
`q-floor((h-1)/2)-(M-1)`, minimized separately over compatible rows.
Therefore any witness in the second line of (FW189c) is incident with `v` or
belongs to one of the two bounded outer factors.

The large-merge branch localises still further uniformly.  On all current
affine rows `a,b<=4` and `q<=N/2+8`.  Hence, with

```text
E_0=N/2-4(n-4)-8+1=(n^2-17n+36)/4,
```

the definition of `M` and `S<=N` imply `M>4(n-4)` once

```text
E_0(E_0-1)>N(12(n-4)-1).
```

After multiplication by 16 the difference is

```text
f(n)=n^4-130n^3+845n^2-1548n+1152.
```

Now `f(124)=1362176>0`, and
`f'(n)=n^2(4n-390)+1690n-1548>0` for `n>=124`.  Every edge in an outer factor
has full cut product, and hence merge product, at most `4(n-4)`.  Thus for
`n>=124` the `Delta>=M` witness in (FW189c) must be a `v`-incident lower-arm
edge.  A high-`sigma` witness may additionally occupy one of only
`a+b-1<=7` pre-`q` outer edges.

Asymptotically, (FW189a)--(FW189b) say more: if `RW_q=o(n^4)`, then any
quadratic FW188 witness satisfies `q-w=o(n^2)`.  This gives the
**OBSERVED exact top-localisation theorem**

```text
quartic residual; or
a quadratic event at the top root skeleton.       (FW189)
```

It is not yet an exclusion or an `RW_q` upper bound.  The remaining task is
now sharply separated: control one macroscopic `v`-incident merge, or bound
the duration/multiplicity of one quadratic surplus at the centre or at the
at-most-seven outer positions.

The constant-memory replay checks 76,219 abstract schedules, 278,993 surplus
runways, the exact unique-distance minima, all current rows, and all five
known witnesses through both checkers:

```text
theory-lab/topwindow/verify_endpoint_terminal_top_localization.py
theory-lab/topwindow/results/endpoint_terminal_top_localization_certificate.json
```

The final excess can in fact be transferred unconditionally to one specific
root boundary, without first assuming a small residual.  Let `C_0` have order
`m=n-a-b`, and let `p` be its heaviest edge.  Since every internal edge of a
lower arm is lighter than its incident edge, `p` is incident with `v`.  If
its arm has order `s`, all other `C_0` edges have already been inserted when
Kruskal reaches `p`, so

```text
Delta_p=s(m-s).                                    (FW190a)
```

Every `C_0` edge has weight at most its endpoint's `v`-depth and hence at
most `h`, whereas `t=h+R>h`.  Therefore every edge after `p` and before `q`
lies in the two bounded outer factors.  Their *total* pre-`q` merge mass,
including edges that happen to precede `p`, is exactly

```text
O=binom(a,2)+binom(b,2)+bm.                        (FW190b)
```

Indeed the internal edges of `A` and `B` contribute `binom(a,2)` and
`binom(b,2)`, while the `t`-edge joins the already connected order-`b` arm to
the already connected order-`m` core and contributes `bm`.

Write `sigma_p=Pi(p-1)-(p-1)`.  If the edges strictly between `p` and `q`
have total merge mass `O_p<=O`, the exact covering ledger gives

```text
E_q=sigma_p+Delta_p+O_p-(q-p),
sigma_p+Delta_p=E_q-O_p+(q-p)>=E_q-O.             (FW190c)
```

Thus, with

```text
H=ceil((E_q-O)/2),
```

one and the same `v`-incident edge satisfies the unconditional dichotomy

```text
Delta_p>=H; or sigma_p>=H.                         (FW190d)
```

On the current affine rows `E_q=n^2/4-O(n)` and `O=O(n)`, so

```text
H=n^2/8-O(n).                                      (FW190)
```

This is three times the leading threshold in (FW188), and it is already at a
specified root edge.  In the merge branch, (FW190a) forces

```text
min(s,m-s)>=((1-1/sqrt(2))/2)n-O(1)
          =0.146446...n-O(1).                     (FW190e)
```

The surplus branch also has an exact size consequence.  Immediately before
`p`, the two core components have orders `s,m-s`; the still-detached outer
vertices contribute at most `binom(a,2)+binom(b,2)` already-connected pairs.
Moreover all `binom(s,2)` internal distances of the last arm lie below `p`,
so `p-1>=binom(s,2)`.  Hence

```text
sigma_p<=binom(m-s,2)+binom(a,2)+binom(b,2).       (FW190f)
```

If the second line of (FW190d) holds, the already-connected root side
therefore has order at least the least `y` with

```text
binom(y,2)>=H-binom(a,2)-binom(b,2),
```

which is `n/2-O(1)` asymptotically.

The exact finite ranges are

```text
n:                                  36   38   49   51   64   66   81   83
min H:                              76  105  180  222  353  410  616  690
min root side, surplus branch:      13   15   20   22   27   30   36   38
min smaller side, merge branch:      3    4    5    6    7    8   10   10
```

This is the **OBSERVED exact last-core-boundary transfer theorem**.  It
removes the FW186 basin-coalescence ambiguity at quadratic scale: the mass is
forced onto a single named root boundary.  It is still not an exclusion or a
residual upper bound; the remaining two cases are a macroscopic last arm cut
and a half-order already-connected root component.

The constant-memory replay checks the transfer identity at 278,993 marked
edges in 76,219 schedules, 84,240 component inequalities, every current row,
and the five known witnesses through both checkers:

```text
theory-lab/topwindow/verify_endpoint_terminal_core_boundary_transfer.py
theory-lab/topwindow/results/endpoint_terminal_core_boundary_transfer_certificate.json
```

The merge branch of (FW190d) already pays directly inside the truncated
ledger.  Let `theta_J` be the eccentricity of the last arm `J`, measured from
its attachment root.  Its `binom(s,2)` internal distances are distinct
positive integers, so

```text
diam(J)>=binom(s,2).
```

Every rooted tree has eccentricity at least half its diameter; therefore

```text
theta_J>=ceil(binom(s,2)/2).                       (FW191a)
```

The arm height satisfies `p+theta_J<=h`, and `q=h+Q`.  Hence the max-`p`
paths have the exact runway lower bound

```text
q-p>=Q+ceil(binom(s,2)/2).                         (FW191b)
```

Combining (FW191b) with the local truncated contribution (FW189a) and
`Delta_p=s(m-s)` gives

```text
RW_q>=Phi(s(m-s),Q+ceil(binom(s,2)/2)).            (FW191c)
```

In the FW190 merge branch, `s(m-s)>=H=n^2/8-O(n)` and hence
`s>=alpha n-O(1)`, where

```text
alpha=(1-1/sqrt(2))/2.
```

Thus the two arguments of `Phi` are at least

```text
Delta_p>=n^2/8-O(n),
q-p>=alpha^2 n^2/4-O(n).
```

Since `alpha^2/4<1/8`, the closed form for `Phi` yields the explicit quartic
charge

```text
RW_q>=((7-4sqrt(2))/2048)n^4-O(n^3)
    =0.0006558328859900491... n^4-O(n^3).          (FW191)
```

This is an **OBSERVED conditional all-order merge-runway theorem**.  Unlike
FW184--FW185, its charge is localised entirely inside `RW_q`, so it may be
compared safely with a future residual upper bound.  It resolves the
large-merge half of (FW190), but is not itself an exclusion and says nothing
about the high-surplus half.

Minimizing (FW191c) over every integer arm order satisfying the exact FW190
threshold gives

```text
n:                    36   38    49    51    64    66     81     83
min RW_q:             560  723  1895  2706  5688  7605  18074  18252
minimizing arm order:   3    4     5     6     7     8     10     10
```

The constant-memory replay and certificate are

```text
theory-lab/topwindow/verify_endpoint_terminal_merge_runway.py
theory-lab/topwindow/results/endpoint_terminal_merge_runway_certificate.json
```

The surplus half can be iterated without losing its quadratic scale.  Order
the complete lower arms by increasing incident weight and peel them from the
heaviest end.  Suppose the already peeled arms have total order `z`.  All
merge products belonging to those arms--their internal edges and their
incident edges--have total

```text
U(z)=z(m-z)+binom(z,2).                            (FW192a)
```

The first term counts peeled--unpeeled core pairs and the second counts pairs
within the peeled union.  Some of these edges may lie below the next incident
weight, so `U(z)` is an upper bound for the peeled core mass that actually
occurs later in the covering schedule.  It also satisfies `U(z)<=zn`.

Let `p_i` be the next lower-arm incident edge, with merge product `Delta_i`
and pre-edge surplus `sigma_i`.  The same telescoping as in (FW190c), now
allowing the peeled core edges in the suffix, gives

```text
sigma_i+Delta_i>=E_q-O-U(z).                      (FW192b)
```

There is a uniform quantitative range in which the right side stays
quadratic.  On the current rows

```text
E_q>=N/2-4n+9,             O<=4n+12.
```

If `z<n/16`, then (FW192a) gives `U(z)<n^2/16`, and hence

```text
E_q-O-U(z)>=3n^2/16-33n/4-3>=n^2/8              (n>=133).
```

Thus before the peeled mass reaches `n/16`, every next incident edge has

```text
max(Delta_i,sigma_i)>=n^2/16.                     (FW192c)
```

Suppose for contradiction that along a sequence of current terminal rows
`RW_q=o(n^4)`.  If the first entry of (FW192c) is large, then
`s_i>=Delta_i/n>=n/16`.  Repeating the rooted-eccentricity argument of
(FW191a)--(FW191c) gives

```text
q-p_i>=n^2/2048,
RW_q>=(255/8388608)n^4-o(n^4),
```

a contradiction.  Therefore the surplus entry is at least `n^2/16` at every
peeling step.  Put `L_i=q-p_i`.  The future-area bound (FW189b) implies

```text
L_i=o(n^2).
```

Since the arm eccentricity is at most `h-p_i<=L_i` while (FW191a) bounds it
below by `binom(s_i,2)/2`, every peeled arm has `s_i=o(n)`, uniformly over
the process.

Stop just after the peeled order first reaches `n/16`.  Then

```text
z=n/16+o(n),                    max_i s_i=o(n),
sum_{i<j}s_i s_j
 =(z^2-sum_i s_i^2)/2=Theta(n^2).                 (FW192d)
```

Every pair counted in (FW192d) lies in two different lower arms, so its path
passes through `v`.  Each endpoint has `v`-depth between `p_i` and `h`.
Consequently all these distinct distances lie in

```text
[2q-2 max_i L_i, 2h],
```

an interval of `o(n^2)` integer slots, contradicting (FW192d).

The constants can be made explicit.  Under the contrary bound
`RW_q<kappa n^4`, take

```text
kappa=1/1000000.
```

If `L_i>=sigma_i`, the saturated surplus triangle gives
`RW_q>=binom(sigma_i+1,2)>=n^4/512>kappa n^4`, already a contradiction.
Hence `L_i<sigma_i`; now (FW189b) gives
`RW_q>=sigma_i(L_i+1)/2`, and therefore
`L_i+1<32 kappa n^2`.  It follows that eventually `s_i<=n/64`.  At the
stopping time the cross-arm count is at least
`3n^2/2048`, whereas its distance window has fewer than
`64 kappa n^2+1` slots.  The rational checks

```text
255/8388608 > kappa,
128 kappa < 1/4096,
64 kappa < 3/2048
```

close both alternatives.  Therefore every current affine endpoint terminal
satisfies, for all sufficiently large `n`,

```text
RW_q>=10^(-6)n^4.                                  (FW192)
```

This is the **OBSERVED conditional all-order surplus-peeling theorem**.  It
closes both branches of FW190 at the level of a positive quartic residual
lower bound.  It is not a nonexistence proof: the project still needs a
terminal upper bound for this same `RW_q` below the displayed constant (or a
direct collision that bypasses such a comparison).

The constants in that peeling argument can be sharpened without changing
its logic.  Peel until the removed arm order first reaches `n/7`, and retain
the quadratic term

```text
U(z)=z(m-z)+binom(z,2)=zm-z^2/2-z/2.
```

At `z<n/7`, the final excess less the outer and peeled mass has leading
coefficient `23/196`; the next incident edge therefore has
`max(Delta_i,sigma_i)>=(11/196)n^2-o(n^2)`, with the smaller rational
absorbing all linear terms.  In the merge branch,
`Delta_i<=s_i(n-s_i)` eventually forces `s_i>=n/17`.  Its rooted runway is at
least `n^2/1156-o(n^2)`, and (FW189a) has leading coefficient

```text
(11/196)(1/1156)-(1/2)(1/1156)^2
  =6309/130960928 > 1/25000.
```

In the surplus branch the saturated triangle is already larger.  Otherwise
(FW189b) makes every peeled arm smaller than `n/13` eventually.  At the
stopping time the cross-arm pair coefficient is at least

```text
((1/7)^2-(1/7)(1/13))/2=3/637,
```

while their common distance-window coefficient is below
`(4/25000)/(11/196)=98/34375<3/637`.  Hence every current affine endpoint
terminal satisfies, for all sufficiently large `n`,

```text
RW_q>=n^4/25000.                                    (FW193)
```

This is an independently audited **OBSERVED conditional all-order sharpened
surplus-peeling theorem**.  It remains a lower bound, not an exclusion or a
residual upper bound.  Replay:

```text
theory-lab/topwindow/verify_endpoint_terminal_surplus_peeling_sharp.py
theory-lab/topwindow/results/endpoint_terminal_surplus_peeling_sharp_certificate.json
```

The quartic residual also localizes inside the near-full lower core.  For a
pair `P`, let `M(P)` be the largest edge on its path.  The exact Leech
spectrum and global maximality of `q` give

```text
RW_q=sum_P (min(d(P),q)-M(P)).                     (FW194a)
```

Every summand is nonnegative.  If `RW_C` restricts this sum to pairs inside
the connected induced order-`m` core `C_0`, then

```text
0<=RW_q-RW_C<=(binom(n,2)-binom(m,2))(q-1).       (FW194b)
```

Here `m=n-a-b`, `a+b<=5`, and `q<=N/2+8`, so the right side is `O(n^3)`.
Thus (FW193) implies, for all sufficiently large `n`,

```text
RW_C>=n^4/50000.                                   (FW194c)
```

There is an exact defect schedule form.  Put
`H={1,...,q-1}\D_0` and `A_H=sum_{h in H}(q-h)`.  Kruskal merge products
computed inside `C_0` give

```text
RW_C=q binom(m,2)-binom(q,2)+A_H
     -sum_{e in C_0} w_e Delta_e^{C_0},            (FW194d)
```

where `|H|<=21` by (FW165), so `0<=A_H<=21(q-1)`.  Averaging (FW194c) at
slack threshold `n^2/100000` further shows that at least `n^2/20000` core
pairs eventually have that much capped path slack.  The remaining endgame is
therefore a stability/collision theorem inside a connected order-`n-O(1)`,
defect-21 core; bounded outer factors cannot carry the quartic compensation.
This is an independently audited **OBSERVED conditional all-order
core-residual localization theorem**, not the missing stability theorem or
nonexistence.  Replay checks all 58 connected induced subtrees of the five
known witnesses, with every witness passing both checkers:

```text
theory-lab/topwindow/verify_endpoint_terminal_core_residual.py
theory-lab/topwindow/results/endpoint_terminal_core_residual_certificate.json
```

## The three one-splitter affine tails collide in a fixed prefix

The three `K=2` rows left by (FW152) can now be excluded.  Each row has one
order-three top pole.  Its attachment root consumes the third global branch
vertex, so (FW172) leaves exactly one lower-core splitter `c` besides
the centre `v`; every remaining lower-core piece is a bare ray.  Continue the
exact coefficient recursion below `2h`.  If `T` is the later interface and
`E=g+T=N-2h`, then at coefficient `E+k` it has the form

```text
z_{T+k}=1-c_{E+k}-I_k
          -sum_{x in C-{0}} z_{T+k-x}
          -sum_{y in O} z_{g+k-y}.                (FW195a)
```

As usual, indicators with negative subscripts are zero.  Here `I_k` counts
represented lower-core pairs at distance `2h-k`.  For the finite ranges used
below, (FW195a) is exact rather than a free-bit relaxation.  Indeed `h>=259`,
all represented deficits are at most 36, and every unlisted pair involving
`v` or internal to a top arm has distance at most `h+176<2h-36`.  An ancestor
pair in the lower core has distance at most `h`.  Thus every remaining pair
at distance `2h-k` is a non-ancestor lower-core pair, whose LCA is `v` or
`c`; these are precisely the pairs counted by `I_k`.  The two top/lower cross
families are already the two convolutions displayed in (FW195a).

Assign every represented deficit to a canonical bare ray.  If two vertices
with deficits `z_i,z_j` lie on the same ray, their distance is
`|z_i-z_j|`.  If their LCA is `v`, it is `2h-z_i-z_j`.  If their LCA is `c`
at centre-depth `d`, it is
`2h-2d-z_i-z_j`.  All represented pair distances must be positive, mutually
different, and different from the planted internal distances of the two top
poles.  When the splitter deficit `r=h-d` is larger than the represented
prefix, enforcing only these represented-prefix conditions is a relaxation:
the still-hidden splitter vertex, later vertices, and their additional
collisions are deliberately omitted.

The complementary visible-splitter case is checked separately.  A splitter
with `r<T` would already lie in the FW151 forced band and is impossible.  For
every `T<=r<=Z`, the replay inserts the compulsory vertex `c` exactly at
deficit `r`, partitions smaller deficits among its child rays or other
`v`-rays, and partitions larger deficits between the shared `v--c` trunk and
other `v`-rays.  Distances within the `c`-branch are ancestor differences,
except that two child rays give `2r-z_i-z_j`; distances to another `v`-ray
are `2h-z_i-z_j`.  Every visible value of `r` is excluded in all three rows.
In particular the child--child values are at most `2r<=2Z`, so they enter the
pair-injectivity check but not `I_k`, which concerns the distant value
`2h-k`; here the corresponding deficit would be `2(h-r)+z_i+z_j>32`.
This calculation is also height-stable: its internal distances depend only
on `r`, while the mutually distinct root-LCA family translates upward with
`h` and stays above every internal value for `h>=259`.

An explicit canonical-state replay gives the following sharp empty prefixes:

```text
row  (a,b; P,U; A_0,B_0)                 T   coefficients   max deficit
 0   (1,3; {0},{0,1,2}; 4,3)            4       33             36
 1   (2,3; {0,4},{0,1,2}; 9,3)          9       25             33
 2   (3,1; {0,1,2},{0}; 6,3)            6       19             24
```

The preceding prefix is nonempty in each case (respectively 2, 2 and 3
relaxed states), while the displayed final coefficient leaves no state.  No
tree-order budget is used.

It remains to justify that this finite calculation is uniform in `h`.  Let
`Z` be the displayed maximum deficit and put `r=h-d`.  The only possible
collision between a `v`-LCA distance and a `c`-LCA distance has

```text
2d=s_v-s_c,              0<=s_v,s_c<=2Z,
```

and hence requires `d<=Z`.  A `c`-LCA distance can meet a same-ray or planted
small distance only if

```text
2r=s_c+u<=3Z,
```

and hence `r<=floor(3Z/2)`.  The `v`-LCA distances are already larger than
all small distances because `2h-2Z>Z`.  Therefore every height belongs to
one of three stable regimes: preserve `d` when `d<=Z`, preserve `r` when
`r<=floor(3Z/2)`, and otherwise replace it by any fixed middle depth with
both inequalities strict.  The coefficient recursion sees `d` only through
`2d+s=k`; it is also unchanged by this map.  Since

```text
259 >= Z+floor(3Z/2)+2
```

for all three rows, every state at any `h>=259` maps to a state at `h=259`.
For the hidden-splitter branch, the replay checks the exact
collision/recursion signatures of all near-root and near-band representatives
and the middle representative before enumerating the base height.  Together
with the explicit visible-splitter replay, this is exhaustive.  Consequently

```text
n>=36 + exactly three global branches + FW152 K=2 row
  => contradiction.                                (FW195)
```

This is an independently audited **OBSERVED conditional all-order subcase
exclusion**, not the global three-branch theorem.  It removes all three
`K=2` rows; the `K=3` rows and the other thick/lower-core outputs remain.
The explicit enumerator is independent of the diagnostic SMT encoding and
peaks below 40 MB RSS:

```text
theory-lab/topwindow/verify_endpoint_k2_prefix_pairs.py
theory-lab/topwindow/results/endpoint_k2_prefix_pairs_certificate.json
theory-lab/topwindow/probe_endpoint_k2_tail_smt.py
```

## Quadratic-slack paths live in a large low-edge component

The core residual has an exact threshold-forest interpretation.  Fix an
integer `s>=1`, delete from `C_0` every edge of weight greater than `q-s`,
and call the resulting forest `F_s`.  If its component orders are `c_i`, put

```text
Pi_s=sum_i binom(c_i,2).
```

Recall that `H={1,...,q-1}\D_0` is the low-distance hole set of the core.
Every value in `[1,q-s]\H` is the distance of a core pair.  Positive edge
weights make every edge on that path at most its distance, so the two
endpoints lie in one component of `F_s`.  Consequently

```text
Pi_s>=q-s-|H intersect [1,q-s]|.                  (FW196a)
```

More generally, if `M(P)` is the largest edge on a core path and

```text
min(d(P),q)-M(P)>=s,
```

then `M(P)<=q-s`; hence that whole path lies in one component of `F_s`.
If `L_s` is the largest component order and `m=|C_0|`, then

```text
Pi_s<=m(L_s-1)/2,
L_s>=1+ceil(2 Pi_s/m).                             (FW196b)
```

The current affine endpoint gives `E=N-2h<=113`, `Q=q-h>=2`, `m<=n-2`,
and `|H|<=21`.  Taking `s=ceil(n^2/100000)` therefore gives the explicit
uniform bound

```text
L_s >= 1+ceil(2 max(0,ceil((N-113)/2)+2-s-21)/(n-2))
    = (1/2-1/50000)n-O(1).                         (FW196c)
```

Thus the defect-21 low spectrum already forces one component containing
asymptotically half the core, all joined by edges at most `q-s`.

There is a second localization of the FW194 large-slack pairs.  After the
three `K=2` rows are excluded, the current exact `K=3` skeleton has the three
branch centres `v,c,d`.  Root `C_0` at `v`.  Every pair is either
ancestor-comparable or has LCA `v`, `c`, or `d`.  When FW194 is active, at
least

```text
K=ceil(n^2/20000)
```

core pairs have capped slack at least `s`, and therefore lie within
components of `F_s`.  One of the four classes contains
`B=ceil(K/4)` pairs.  In the ancestor class, counting by the deeper endpoint
produces a low-edge ancestor chain of order at least

```text
1+ceil(B/m) >= n/80000-O(1).                       (FW196d)
```

In an LCA class all endpoints lie in the single `F_s` component containing
that centre.  If `S` is the number of its descendant vertices participating
in that component, then `binom(S,2)>=B`, and hence

```text
S>=n/200-O(1).                                     (FW196e)
```

This is an independently audited **OBSERVED conditional all-order
threshold-component localization theorem**.  It converts the quartic
residual into a half-order low-edge component and a linear chain-or-centred-
mass alternative.  It is not yet an additive collision, an upper bound for
`RW_C`, a descent, or nonexistence.  Replay checks all threshold profiles of
all 58 connected induced subtrees of the five known witnesses, with every
witness first passing both checkers:

```text
theory-lab/topwindow/verify_endpoint_terminal_slack_components.py
theory-lab/topwindow/results/endpoint_terminal_slack_components_certificate.json
```

## The K3 terminal has an almost-full defect-two prefix core

There is a sharper stability statement specific to the then 31 surviving `K=3`
rows.  First note an elementary rooted fact.  Let `C` be any connected
induced subtree rooted at `v`, and let

```text
h=max_{x in C} d(v,x).
```

Every edge of `C` has weight at most `h`.  If an edge has weight exactly
`h`, positivity forces its path from `v` to contain no other edge: it joins
`v` directly to a leaf.  Edge weights are globally distinct, so there is at
most one such leaf.  Delete it if it exists and call the resulting connected
induced subtree `C^-`.  No pair of distance below `h` could have used the
deleted weight-`h` edge, and therefore

```text
max edge(C^-)<=h-1,
D(C^-) intersect [1,h-1]=D(C) intersect [1,h-1]. (FW197a)
```

Apply this to the lower core `C_0`.  For every current `K=3` row both pole
orders are at most two, so (FW166a) has

```text
e=binom(a,2)+binom(b,2)<=2.
```

It says that `C_0` misses at most `e` values below `t`; and `h<t` by
`t=h+R`, `R>=1`.  Removing the two bounded outer poles and the optional
height leaf deletes at most `a+b+1<=5` vertices from the whole tree.  Thus

```text
|C^-|>=n-5,
|[1,h-1]\D(C^-)|<=2,
h=(N-E)/2,                    E<=26.               (FW197)
```

In particular `h=N/2-O(1)`: the unresolved endpoint contains a connected
induced order-`n-O(1)` tree whose edge cap is below `h` and whose internal
spectrum covers the whole first half of the Leech interval with only two
holes.  This is an independently audited **OBSERVED conditional all-order
almost-full prefix-core theorem**.  It is substantially sharper than the
defect-21 statement for this prefix, but `C^-` is not asserted to be a Leech
tree; converting its defect-two prefix and fixed three-centre skeleton into
a collision remains **UNVERIFIED**.  Replay checks the rooted lemma on 122
rooted connected induced subtrees of the five known witnesses, after both
checkers pass:

```text
theory-lab/topwindow/verify_endpoint_terminal_almost_prefix_core.py
theory-lab/topwindow/results/endpoint_terminal_almost_prefix_core_certificate.json
```

## The first two-splitter K3 row dies in 50 coefficients

The exact high-spectrum recursion can now be continued with both lower-core
splitters present.  Start with the first post-FW164 `K=3` row

```text
P=U={0},             Q=2, R=1,
A_0=2, B_0=1,        E=3.                         (FW198a)
```

Process 50 coefficients, so the represented lower-core deficits run through
`0<=z<=51`.  By (FW172), the two non-root splitters form either the chain
`v--c--d` or the fork `c--v--d`.  For each splitter exactly one of the
following applies:

```text
rho=h-depth<T=2:              excluded by FW151;
2<=rho<=51:                   visible, with its compulsory marker z=rho;
rho>51 and depth<=24:         hidden but its translated LCA layer is exact;
rho>51 and depth>=25:         inactive in this prefix.             (FW198b)
```

The last class cannot contribute to a coefficient `k<=49`, because every
such translated layer starts at `2 depth>=50`.  The replay deliberately
relaxes its unknown translate: it retains only the necessary rule that two
pairs with the same inactive LCA cannot have the same deficit sum.

Visible branch vertices, child rays, shared skeleton edges and all other
root rays are placed explicitly.  For represented deficits `z_1,z_2`, the
pair checker uses

```text
ancestor-comparable:              |z_1-z_2|;
visible LCA of deficit rho:        2rho-z_1-z_2;
shallow LCA of centre-depth d:     2h-(2d+z_1+z_2);
root LCA:                          2h-(z_1+z_2).       (FW198c)
```

All exact represented distances are positive and mutually distinct and
avoid the planted pole spectrum.  The last two classes contribute the exact
FW195a internal coefficient with layer `k=2d+z_1+z_2`.  Unrepresented
vertices and every collision involving an inactive translate are omitted,
so the calculation remains a necessary-condition relaxation.

There are exactly 5,552 configurations:

```text
kind                           chain   fork
both shallow                      276    276
shallow + inactive                 24     24
both inactive                       1      1
one visible                     1,250  1,250
both visible                    1,225  1,225
```

Every configuration has empty frontier after the 50th coefficient; no state
cap is hit, and the maximum number of states in one layer is 509 (268 for
fork configurations).

This base-height result is uniform.  Put `Z=51` and `D=24`.  For every
`h>=259`, shallow splitters preserve `d`, visible splitters preserve `rho`,
and all others map to the relaxed inactive class.  The location predicates
and coefficient layers are unchanged.  Exact low distances are at most
`2Z=102`; root depths and the two outer-root values lie between `h-Z` and
`h+2`; and every exact high distance is at least

```text
2h-(2D+2Z).
```

At `h=259` these three bands are respectively

```text
[1,102],          [208,261],          [368,2h],
```

and the separation only grows with `h`.  High--high equality depends only
on equality of translated layers, while both low classes are independent of
`h`.  The replay checks the chain/fork classification map at heights 259 and
396 in 110,317 cases of each type, in addition to the symbolic inequalities.
Thus any state at any `h>=259` would map to one of the empty base states.

Consequently

```text
n>=36 + exact K3 skeleton + row (P,U,Q,R)=({0},{0},2,1)
  => contradiction.                                  (FW198)
```

This is an independently audited **OBSERVED conditional all-order affine-row
exclusion**.  It leaves 30 `K=3` rows; it does not yet exclude the full
endpoint terminal.  The four-worker replay peaks at only a few tens of MB per
worker and has no solver, timeout or accepted cap state:

```text
theory-lab/topwindow/verify_endpoint_k3_first_row.py
theory-lab/topwindow/results/endpoint_k3_first_row_certificate.json
theory-lab/topwindow/probe_endpoint_k3_exact_hierarchy_prefix.py
```

## Seven more K3 rows die in 30 coefficients

The same exact two-splitter recursion closes seven further affine rows with
the shorter horizon `H=30`:

```text
P       U       Q   R     T   E
{0}     {0}     3   1     3   4
{0}     {0}     7   1     7   8
{0}     {0}     8   1     8   9
{0,1}   {0}     3   2     4   6
{0,3}   {0}     3   1     6   7
{0,3}   {0}     4   1     7   8
{0,4}   {0}     4   1     8   9.                 (FW199a)
```

Here `T=max(Q+max(P),R+max(U))` and
`E=(Q+max(P))+(R+max(U))`.  Each row has exactly 1,982 configurations:

```text
kind                         chain   fork
both shallow                    91     91
shallow + inactive              14     14
both inactive                    1      1
one visible                    450    450
both visible                   435    435.
```

All 13,874 configurations have empty frontier, no unknown configuration and
no cap hit.  The maximum number of states in any one layer is 2,933.

The all-height transfer is checked per row rather than borrowing the row in
(FW198).  Put

```text
Z=T+H-1,              D=floor((H-1)/2)=14.
```

For the seven rows `Z<=37`.  At the common base height `h=259`, every exact
represented low distance is at most 74, every represented root/outer-middle distance lies within
`[h-Z,h+T] subset [222,267]`, and every exact high distance is at least 416.
The certificate freezes each row's pole factors, forbidden low set, top
coefficient counter and coefficient interval.  When height increases by
`Delta`, the low signature is fixed, the middle interval translates by
`Delta`, and the high-distance set translates by `2 Delta`; the strict
separation margins increase.  The chain/fork classification map is also
enumerated at heights 259 and 396.  Hence the empty base frontiers cover every
integer `h>=259`.

Consequently

```text
n>=36 + exact K3 skeleton + any row in (FW199a)
  => contradiction.                                  (FW199)
```

This is an independently audited **OBSERVED conditional all-order seven-row
affine exclusion**.  Together with (FW198), it leaves 23 `K=3` rows; it is
not yet the full endpoint contradiction.  The four-worker production replay
and frozen certificate are

```text
theory-lab/topwindow/verify_endpoint_k3_h30_rows.py
theory-lab/topwindow/results/endpoint_k3_h30_rows_certificate.json
```

## Four expensive K3 rows close under exact sharding

Four additional rows pass the same `H=30` recurrence only long enough to make
the two chain-visible configuration families expensive when processed as one
serial task:

```text
P       U       Q   R     T   E
{0,4}   {0}    13   1    17  18
{0,4}   {0}    21   1    25  26
{0,5}   {0}    15   1    20  21
{0,5}   {0}    16   1    21  22.                 (FW200a)
```

This is a scheduling issue, not a new relaxation.  For each row the eight
other configuration kinds contribute 1,097 configurations.  Partition
`chain-out-in` by its 30 visible markers, leaving 15 shallow-or-inactive
parent choices per shard, and partition `chain-in-in` by its exact ordered
marker pair.  Thus each row has

```text
8 bulk kinds:                         1,097 configurations
30 marker shards x 15:                  450 configurations
binom(30,2) exact marker-pair shards:   435 configurations
                                      -----
                                      1,982 configurations.
```

Across four rows the production replay has 1,892 shards and 7,928 exact
configurations.  Every shard has empty frontier, there is no unknown or cap
hit, and the per-row maximum layer-state counts are

```text
13,572,        0,        1,196,        2,193.
```

The sharded families are disjoint and exhaustive: a `chain-out-in`
configuration has one unique visible child marker, while a `chain-in-in`
configuration has one unique ordered parent/child marker pair.  All other
kinds remain in the disjoint bulk set.

Height stability is recomputed per row.  Here `Z=T+29<=54` and `D=14`.  At
`h=259`, represented low distances are at most 108, represented middle
distances lie in `[h-Z,h+T] subset [205,284]`, and represented high distances
are at least 382.  The same fixed/`Delta`/`2 Delta` translation signatures as
in (FW199) are frozen together with every row's recurrence data, and their
strict margins increase for all `h>=259`.

Consequently

```text
n>=36 + exact K3 skeleton + any row in (FW200a)
  => contradiction.                                  (FW200)
```

This is an independently audited **OBSERVED conditional all-order four-row
affine exclusion**.  It leaves 19 `K=3` rows and does not yet exclude the
endpoint terminal.  Replay and certificate:

```text
theory-lab/topwindow/verify_endpoint_k3_h30_split_rows.py
theory-lab/topwindow/results/endpoint_k3_h30_split_rows_certificate.json
```

## Eleven more K3 rows close, leaving eight frontiers

The remaining unscanned affine tail consists of ten singleton-right-factor
rows and one two-by-two factor row:

```text
P={0,k}, U={0}, Q in {k,k+1}, R=1,       6<=k<=10;
P={0,3}, U={0,1}, Q=4, R=1.              (FW201a)
```

The same `H=30` sharding as in (FW200) is run with persistent workers so that
each dependency stack is loaded only once.  Per row the 473 tasks still form
an exact partition of all 1,982 configurations; across the eleven rows this
is

```text
5,203 tasks,        21,802 configurations.
```

Every task has empty frontier, with no unknown or cap hit.  The largest
one-layer state count is 5,320.  The replay locks the parent certificate hash,
all eleven row identities and interfaces, every task/configuration count, and
the per-row observed maxima before accepting an exclusion.

Height stability is again row-specific.  Here `T<=21`, so

```text
Z=T+29<=50,              D=14.
```

At `h=259`, represented low distances are at most 100, represented middle
distances lie in `[h-Z,h+T] subset [209,280]`, and represented high distances
are at least 390.  The certificate freezes each recurrence signature and the
fixed/`Delta`/`2 Delta` height translation, whose margins increase for every
`h>=259`.

Consequently

```text
n>=36 + exact K3 skeleton + any row in (FW201a)
  => contradiction.                                  (FW201)
```

This is an independently audited **OBSERVED conditional all-order eleven-row
affine exclusion**.  It leaves exactly eight `K=3` rows.  Those eight have
relaxed `H=30` frontiers; a frontier is not a Leech tree or SAT witness, and
the endpoint terminal is still open.  Production replay and certificate:

```text
theory-lab/topwindow/probe_endpoint_k3_h30_remaining_shards.py
theory-lab/topwindow/verify_endpoint_k3_h30_remaining_rows.py
theory-lab/topwindow/results/endpoint_k3_h30_remaining_rows_certificate.json
```

## The final eight K3 rows close at mixed horizons

The eight relaxed frontiers left by (FW201) are

```text
row   P       U       Q   R   horizon
  2   {0}     {0}     4   1      50
  3   {0}     {0}     5   1      40
  4   {0}     {0}     6   1      40
  7   {0}     {0,1}   3   1      40
  9   {0,2}   {0}     3   1      40
 13   {0,4}   {0}     5   1      40
 16   {0,5}   {0}     5   1      40
 17   {0,5}   {0}     6   1      40.             (FW202a)
```

No new relaxation is introduced.  For coefficient horizon `H`, put
`D=floor((H-1)/2)`.  The exact chain/fork configuration count is

```text
2 [ binom(D,2) + D + 1 + (D+1)H + binom(H,2) ].
```

As before, the eight cheap kinds remain whole, `chain-out-in` is partitioned
by its unique visible marker, and `chain-in-in` by its unique ordered
parent/child marker pair.  Thus an `H=40` row has 828 shards covering 3,542
configurations, while the `H=50` row has 1,283 shards covering 5,552.  Across
(FW202a) the production replay therefore checks exactly

```text
7,079 shards,        30,346 configurations.
```

Every shard has empty frontier, with no unknown and no 20,000-state cap hit.
The per-row maximum one-layer state counts, in the displayed order, are

```text
876, 833, 738, 642, 528, 4,054, 1,142, 5,246.
```

The replay also checks the symbolic height split independently for each
horizon.  For the seven `H=40` rows, `D=19` and the largest represented
deficit is 50; at `h=259`, low distances are at most 100, middle distances
are at least 209, and high distances are at least 380.  For row 2 at `H=50`,
`D=24` and the largest deficit is 53; the corresponding bounds are 106, 206,
and 364.  Hence the low block is fixed while the middle and high blocks
translate by `Delta` and `2 Delta`; all separation margins increase for every
`h>=259`.  The certificate freezes these signatures at `h=259` and the source
height 396, together with the parent hash, row identities, recurrence data,
shard counts and observed maxima.

Consequently

```text
n>=36 + exact K3 skeleton + any row in (FW202a)
  => contradiction.                                  (FW202)
```

This is an independently audited **OBSERVED conditional all-order final
eight-row affine exclusion**.  Together with (FW198)--(FW201), all 31 `K=3`
affine rows are excluded; together with the separate (FW195) exclusion of the
three `K=2` rows, the present at-most-three-global-branch two-small-factor
affine terminal has no remaining necessary row.  This closes that terminal,
not the global `n>=18` theorem or the other thick-centre/global-branch cases.
Production replay and certificate:

```text
theory-lab/topwindow/probe_endpoint_k3_final_mixed_shards.py
theory-lab/topwindow/verify_endpoint_k3_final_mixed_rows.py
theory-lab/topwindow/results/endpoint_k3_final_mixed_rows_certificate.json
```

## A diameter edge either extends a reflected prefix or exposes a double-deep fork

The preceding endpoint machinery is not by itself a reduction of the genuine
thick--thick case.  The following all-order interface applies before choosing
a singleton centre and gives that case a canonical entry point.

Let `x_0,x_N` be the unique pair at distance `N=binom(n,2)`, and select an
edge `e=uv` of weight `q` on their path.  Delete `e`.  Root the two resulting
sides at `u` and `v`, and let their rooted eccentricities and internal
diameters initially be `lambda_0,mu_0` and `d_0,d_1`.  Relabel the sides as
`A,B`, and relabel the corresponding roots and eccentricities as
`lambda,mu`, so that

```text
D=diam(A)=max(d_0,d_1),       diam(B)<=D.
```

The selected edge lies on the unique global-diameter path, hence the two
diameter endpoints are farthest from its endpoints in the respective sides
and

```text
N=q+lambda+mu.                                      (FW203a)
```

Let `X,Y` be the rooted depth sets of `A,B`, and put

```text
U=lambda-X,                 V=mu-Y.
```

Root depths are distinct because they are pair distances.  Every distance
strictly greater than `D` crosses `e`.  Therefore, with `T=N-D`, the factors
`U,V` represent every coefficient

```text
0,...,T-1
```

exactly once: the coefficient `j` is the reflection of the unique pair at
distance `N-j`, and that pair cannot lie within either side.  There are now
two exhaustive cases.

If `D<q+lambda`, put

```text
R=q+lambda-D>=1,             T=mu+R.
```

Apply (FW34) to the factor `V`, whose maximum is `mu<T`.  In its symmetric
outcome, the complete mixed-radix digit blocks supplied by the proof of
(FW34), not set symmetry alone, allow (FW76) to be invoked.  Thus `B` has
order at most four, with rooted depths of one of the four forms in (FW76).
In the nonsymmetric outcome, `V` has a consecutive gap of at least `R+1`.
Choose a farthest vertex of `B`.  Along its path back to the root, reflected
depth increases monotonically from `0` to `mu`; this path must cross the
gap.  Consequently an edge of that path, wholly in the proper side `B` and
possibly incident with its root, has weight at least

```text
R+1=q+lambda-D+1.                                  (FW203b)
```

If instead `D>=q+lambda`, choose the two endpoints `x,y` of the internal
diameter of `A`.  Write their depths from the root of `A` as `r,s`, let `c`
be their rooted LCA, and write `ell` for the depth of `c`.  Then

```text
D=r+s-2ell,                 r,s<=lambda.
```

Using first `s<=lambda` and then `r<=lambda` gives separately

```text
r >= q+2ell,                s >= q+2ell.
```

Thus the two edge-disjoint tails from `c` to `x,y` both have weight at least
`q+ell`.  Moreover `r!=s`, since two vertices cannot have the same rooted
distance.  Positivity and integrality therefore sharpen their sum by one:

```text
D >= 2q+2ell+1 >= 2q+1.                            (FW203c)
```

The vertex `c` is a genuine global branch vertex.  If `ell>0`, its parent
direction and the two diameter tails are distinct; if `ell=0`, the two tails
and the deleted `q`-edge are distinct directions.  Notice that equality
`D=q+lambda` belongs to this fork case: then the reflected prefix stops at
`mu`, so (FW34) is not available.  Also, the two tails need not consist of
multiple edges unless `q` is separately known to dominate every other edge.

Combining the cases gives the **OBSERVED all-order diameter-edge
prefix/fork interface**

```text
every edge q on the unique global-diameter path
  => (a rooted side of order <=4)
     or (a proper-side edge >=q+lambda-D+1)
     or (a global branch vertex with two tails >=q+ell
         and D>=2q+2ell+1).                         (FW203)
```

In particular, a diameter-path edge with `q>N/2` cannot enter the fork
branch.  This is a routing theorem, not an exclusion: the proper-side large
edge still needs a decreasing measure, and the double-deep fork is precisely
the thick--thick output that must next be combined with the global spectrum.
The proof above is all-order.  A lightweight arithmetic replay checks
8,854,560 prefix identities and 665,856 fork inequalities; it also verifies
the exact prefix for every diameter-path edge of the five known Leech trees,
after passing each tree through both independent checkers.  It uses about
10 MB rather than enumerating topologies:

```text
theory-lab/topwindow/verify_diameter_edge_prefix_fork.py
theory-lab/topwindow/results/diameter_edge_prefix_fork_certificate.json
```

The reflected prefix can be used on both sides before accepting the fork.
Retain the notation above.  The maximum of `U` is `lambda`, so whenever

```text
R_A=T-lambda=q+mu-D>0,
```

(FW34) applied to `U` says that `A` is one of the order-at-most-four rooted
poles in (FW76), or a root-to-farthest path in `A` has an edge of weight at
least `R_A+1`.  Symmetrically, when

```text
R_B=T-mu=q+lambda-D>0,
```

the same conclusion holds in `B`, with threshold `R_B+1`.  These conclusions
hold simultaneously if both remainders are positive.  Therefore the fork is
needed only in the fully blocked case

```text
R_A<=0 and R_B<=0
  => D>=q+max(lambda,mu)=N-min(lambda,mu).          (FW204a)
```

This two-sided form has a useful exact specialization.  Let `e` be the
central edge: the midpoint of the unique global diameter lies strictly
inside it.  Then

```text
lambda<N/2,                 mu<N/2.
```

In the fully blocked case, put `C=N-D`.  Equation (FW204a) gives

```text
D>N/2,                      C< N/2,
C<=min(lambda,mu).                                  (FW204b)
```

Choose a side attaining `D`; ties may be resolved arbitrarily.  Write
`delta` for its rooted eccentricity, `eta` for the other one, and let `a,b`
be the global diameter endpoints in the chosen and opposite sides.  Orient
the endpoints `x,y` of the internal `D`-pair by the four-point orientation
lemma so that

```text
d(a,x)>=D,                  d(b,y)>=D.
```

The vertex `x` is off the global-diameter path.  Let its gate on that path
have coordinate `p` from `a`, and let its off-path height be `h`.  Since the
gate lies in the chosen central half, `p<=delta`, while global diameter
maximality gives

```text
d(a,x)=p+h>=D,              d(b,x)=N-p+h<=N,
h>=D-delta=q+eta-C,         h<=p.                  (FW204c)
```

In particular `h>=q`, because `C<=eta`.  Equality `h=q` would repeat the
distance of the central edge using the distinct unordered pair consisting
of `x` and its gate.  Thus

```text
q+1<=h<=p<=delta.
```

If `h>=C+1`, the internal near-diameter pair has produced a genuinely
`C`-deep off-diameter endpoint, exactly the thin/thick output of the
diameter-cap dichotomy at deficit `C`.  This output is nevertheless absorbed
without pretending that the offshoot already carries an FW92--FW93 cap.  In
every fully blocked state, the internal `D=N-C` pair makes cross coefficient
`C` zero.  Since both reflected factors contain zero, neither can contain
`C`; together with `C<=min(lambda,mu)` this gives `lambda,mu>C`.  The
level-`C` shell on either diameter side therefore lies strictly inside its
open metric half.  Apply (FW207a) there: finite cap-order descent ends at an
FW76 terminal or at a cap-attached deep output of deficit `q'<C`, to which
(FW208) applies.  Thus the generic `C`-deep geometry is not a separate
unrouted terminal after the shell descent.  Otherwise `h<=C`, and (FW204c) gives

```text
2C>=q+eta=N-delta>N/2,
C>N/4,                      D<3N/4,                (FW204d)
q<C.
```

The length-`C` exact reflected prefix uses distinct pairs across the central
cut.  If its two component orders are `a_0,b_0`, then the second outcome also
forces

```text
a_0 b_0>=C>N/4=n(n-1)/8.
```

Writing `s=min(a_0,b_0)` and solving the quadratic inequality gives the exact
linear balance bound

```text
s > (n-sqrt(n(n+1)/2))/2
  = ((1-1/sqrt(2))/2)n-O(1).                       (FW204e)
```

Consequently the central edge has the **OBSERVED all-order two-sided
prefix/offshoot dichotomy**

```text
central edge
  => an FW76 side or a proper-side gap edge;
  or a C-deep thin/thick offshoot;
  or N/2<D<3N/4 and both central sides have linear order. (FW204)
```

This removes the arbitrary thick--thick geometry: the last output is a
balanced macroscopic cut, not a diffuse collection of small pieces.  It is
still not an exclusion.  The next step must either absorb the proper-side
gap edge into a decreasing recurrence, close the existing deep-offshoot
terminal, or contradict the balanced-cut spectrum.  An independent Luna
audit found the two-sided factor conditions, the four-point/gate inequalities
and the strict quarter boundary correct.  A lightweight replay checks
174,784 central parameter rows, 26,704,986 offshoot integer rows and 46,647
balanced-cut rows.  The five known Leech witnesses pass both checkers; two
additional distinct-distance controls exercise the deep and balanced fork
outputs but are explicitly not Leech witnesses:

```text
theory-lab/topwindow/verify_central_edge_prefix_offshoot.py
theory-lab/topwindow/results/central_edge_prefix_offshoot_certificate.json
```

The proper-side gap output in (FW204) has a well-founded global continuation.
Fix the original global diameter `xz` and its metric midpoint.  Let `f` be a
gap-path edge supplied on the `z` side of the central edge.  The farthest
vertex of that rooted factor is precisely `z`, so `f` is an edge of the fixed
global diameter and lies strictly on the `z` side of the midpoint.

This location gives full support without any singleton-pole hypothesis.  For
every diameter edge `k` strictly in that open half, let its endpoint nearer
the midpoint be `p`.  The `p`-to-`x` path has weight greater than `N/2`, while
`k<N/2`.  Hence the centre-side component of `T-k` contains a pair longer
than `k`.

Delete `f` and let `P` be its `z`-side component.  Equality
`diam(P)=f` would repeat the edge distance.  Thus either `diam(P)<f`, already
giving a thin diameter cap, or `f` is bidirectional.  In the latter case take
the maximal connected bidirectional edge-component containing `f` and follow
the fixed diameter toward `z`.  It must have a last boundary edge in that
direction: the final edge at the leaf `z` cannot be supported by its
singleton far side.  Call this boundary `g`.  It is still strictly in the
same open half.  Its centre side supports it, while maximality says its far
side does not; equality is again forbidden.  Therefore its `z`-side component
`C` satisfies

```text
z in C,                     diam(C)<g.             (FW205a)
```

If `f` was bidirectional, `C` is a strict subset of `P`.  The maximal
component may extend toward or even across the central edge; no claim to the
contrary is needed, because only its last `z`-side boundary is used.

Let `c in C,p in T-C` be the endpoints of `g`, and put

```text
alpha=d(c,z),               beta=d(p,x),
E=diam(T-C),                sigma=E-beta>=0.
```

Here `beta>N/2>diam(C)`, so `E` is the larger internal diameter and the
dominance condition of (FW89) is automatic.  Since
`N=alpha+g+beta`, all distances above `E` give the exact reflected prefix

```text
0,...,alpha+R-1,            R=g-sigma.             (FW205b)
```

If `R>0`, apply (FW34) to the reflected `C` factor.  Its symmetric outcome,
including the complete digit blocks supplied by that proof, is an FW76 pole
of order at most four.  In the nonsymmetric outcome, the gap path is again a
strictly deeper segment of the same `c`--`z`/global-diameter path.  Close its
bidirectional run at the far boundary exactly as above.  The resulting cap
has strictly smaller vertex order than `C`.  Boundary weight need not
decrease.  Hence repeated nonsymmetric steps terminate after finitely many
caps.

If instead `R<=0`, put

```text
q'=N-E=alpha+R.
```

The global diameter uses `z`, which is absent from `T-C`, so `E<N`; also
`alpha<=diam(C)<g`.  Consequently

```text
1<=q'<=alpha<g.                                      (FW205c)
```

The four-point orientation and global distance uniqueness, as in
(FW92)--(FW93), force an `E`-diameter pair of the complement to keep the old
opposite endpoint `x`; write it `{x,y}`.  If the gate of `y` on the old
diameter is at distance `s` from `p` and its off-path height is `k`, then

```text
E=beta-s+k=beta+sigma,
k=s+sigma>=sigma>=g>q'.                            (FW205d)
```

Thus this terminal is a genuinely `q'`-deep offshoot with a strictly smaller
deficit than the cap boundary.  Combining the cases proves the **OBSERVED
all-order central-gap cap descent**

```text
a proper-side gap edge from FW204
  => after finitely many strict cap-order decreases,
     an FW76 cap of order <=4 or a smaller-deficit deep offshoot. (FW205)
```

This supplies the missing well-founded measure for the proper-side output;
it does not exclude the final pole or offshoot, nor the separate balanced-cut
line of (FW204).  An independent Luna audit verified that only the last
boundary in the endpoint direction is required and that the component may
cross the central edge in the other direction.  A constant-memory replay
checks 2,678 open-half edges in 900 deterministic distinct-distance trees,
including 982 nontrivial bidirectional closures, and replays every available
cap prefix of the five known Leech trees after both checkers pass:

```text
theory-lab/topwindow/verify_central_gap_cap_descent.py
theory-lab/topwindow/results/central_gap_cap_descent_certificate.json
```

The balanced output of (FW204) has an additional first-hole constraint.  Keep
the fully blocked notation, let `a_0,b_0` be the two central-side orders, and
write `U,V` for their reflected radial-deficit sets.  The exact cross prefix
has one representation of every coefficient `0,...,C-1`.  The coefficient
`C` is zero: it would give a cross pair of distance `N-C=D`, but `D` is already
realised by the distinct internal diameter pair.  Since

```text
max(U)=lambda>=C,           max(V)=mu>=C,
```

the missing coefficient also forces `lambda>C` and `mu>C`.  Put

```text
m=|U intersect [0,C-1]|,   k=|V intersect [0,C-1]|.
```

All `C` prefix representations use these visible factor elements, so
`mk>=C`.  Each factor has at least one further element above `C`; hence

```text
C <= (a_0-1)(b_0-1),
a_0 b_0-C >= (m+1)(k+1)-C >= m+k+1 >= tau(C)+1,   (FW206a)
tau(C)=min_{r>=1}(r+ceil(C/r)) >= ceil(2 sqrt(C)).
```

Here `a_0 b_0-C` is exactly the number of cross pairs below `D`: there are
`C` cross pairs above `D`, none at `D`, and all remaining cross pairs are
below it.  It is a pair count, not an edge or branch count.  Also
`m+k<=n-2`, because each side has an additional element above `C`.  Therefore

```text
C <= floor((n-2)^2/4),
D >= N-floor((n-2)^2/4)
  = ceil(n^2/4+n/2-1).                             (FW206b)
```

In the balanced residual (FW204d), `C>N/4`, so
`m+k>=tau(C)>sqrt(N)`: more than `sqrt(N)` vertices of the two reflected
factors are visible below the first hole.  This visible mass must not be
misread as that many diameter edges.  The tree-realised factors do force one
additional geometric feature on each side.  Along either reflected
root-to-global-endpoint path the coordinate runs from `0` to a value greater
than `C`, but no vertex has coordinate `C`.  Consequently each path has an
edge crossing from at most `C-1` to at least `C+1`, of integer weight at least
two.  The two crossing edges lie on opposite sides of the central edge and
are distinct.

Thus the fully blocked balanced branch satisfies the **OBSERVED all-order
central first-hole mass bound**

```text
C>N/4
  => D>=N-floor((n-2)^2/4),
     m+k>=tau(C)>sqrt(N),
     and one distinct level-C shell edge of weight >=2 on each side. (FW206)
```

This is a mass/shell reduction, not an exclusion: `m+k` counts factor
vertices, and neither (FW206a) nor the two shell edges alone give a distance
collision.  An independent Luna audit verified the exact first-hole count,
the integer envelope and these interpretation limits.  The lightweight
replay checks every abstract unique-prefix state through `C=128`, the exact
integer envelope through order 2000, and the central first-hole signature of
all five known witnesses after both independent checkers pass:

```text
theory-lab/topwindow/verify_central_first_hole_mass.py
theory-lab/topwindow/results/central_first_hole_mass_certificate.json
```

The proof of (FW205) has a useful scope strengthening.  Its initial gap was
used only to locate an edge on the fixed global diameter strictly inside one
open metric half.  Let `f` be any such edge, oriented toward the endpoint
`z`.  Its centre-side component contains a rooted path longer than `N/2`,
whereas `f<N/2`, so that side fully supports `f`.  If the `z`-side component
`P` does not support `f`, distance uniqueness changes the weak inequality to
`diam(P)<f`.  Otherwise follow the maximal bidirectional run toward `z`; its
last endpoint-side boundary exists and cuts off a thin cap, exactly as in
(FW205a).  From that point (FW89), (FW34), and (FW92)--(FW93) use no property
of the initial edge.  Hence

```text
any fixed-diameter edge strictly inside an open metric half
  => after finitely many strict cap-order decreases,
     an FW76 cap of order <=4 or an FW93 deep offshoot.    (FW207a)
```

The level-`C` shell edges of (FW206) retain a strict parameter through this
descent.  Orient one shell toward its global endpoint.  If `x` and `y` are
the reflected coordinates of its endpoint-side and centre-side vertices,
respectively, then

```text
x<=C-1,                    y>=C+1.
```

If this edge already cuts a thin cap, that cap has endpoint radius
`alpha=x<C`.  If a bidirectional run must first be crossed, its last boundary
is strictly closer to the endpoint and has `alpha<x<C`.  Every subsequent
nonsymmetric (FW34) step lies still farther inside the same endpoint cap, so
all nested caps retain `alpha<C`.  The recurrence terminates.  In its
symmetric line (FW76) gives order at most four.  In its nonpositive-remainder
line, (FW205c) sharpens to

```text
1<=q'=alpha+R<=alpha<C,                            (FW207b)
```

and (FW205d) gives an offshoot height at least the current boundary, strictly
greater than `q'`.  Combining (FW206) with this arbitrary-open-half descent
therefore proves the **OBSERVED all-order central-shell cap descent**

```text
the FW204 fully blocked balanced branch
  => an FW76 cap of order <=4
     or an FW93 deep offshoot with strictly smaller deficit q'<C. (FW207)
```

Thus the balanced cut is no longer an independent terminal.  This is still a
routing theorem, not the global exclusion: the contextual small-cap output
and the strictly smaller-deficit deep-offshoot output must themselves be
absorbed.  A
corrected independent Luna audit checked that the proof needs only the
strict-open-half location, not an initial gap lower bound, and verified the
strict `q'<C` coordinate.  A constant-memory replay reruns all 2,678 parent
half edges, tests 3,314 absent-level shells in 450 deterministic controls,
including 373 nontrivial endpointward closures, and replays all available
shell starts of the five known witnesses after both checkers pass:

```text
theory-lab/topwindow/verify_central_shell_cap_descent.py
theory-lab/topwindow/results/central_shell_cap_descent_certificate.json
```

The deep line of this recurrence is itself well founded in its deficit, not
only in cap order.  Consider any terminal thin cap `C_z` with endpoint `z`,
root radius `alpha`, boundary `g`, and dominant complement `D`.  Retain

```text
E=diam(D)=beta+sigma=N-q',
R=g-sigma,                 q'=alpha+R>=1.
```

By (FW89), cross coefficients `0,...,q'-1` are represented exactly once.
Coefficient `q'` is zero, because it would give a cross pair of distance `E`,
which is already realised by the internal `E`-diameter pair of `D`.  In
particular the equality case `R=0` is impossible.  Indeed, then `q'=alpha`;
the cap root contributes reflected coordinate `alpha` and the old opposite
diameter endpoint contributes coordinate zero, so their cross pair has
distance `N-alpha=E`.  It is distinct from the internal pair because the cap
root is not in `D`.  Therefore the deep line is strictly

```text
R<0,                       1<=q'<alpha.            (FW208a)
```

The reflected `z`--cap-root path now crosses the absent level `q'`.  Since
`q'<alpha<g<N/2`, this shell edge lies strictly in the same open half of the
fixed global diameter.  Apply (FW207a) at that edge.  Every nested cap keeps
the same global endpoint `z`, while the complement diameter transfer keeps
the old opposite endpoint `x`; dominance and `E<N` therefore persist.  If
the new descent does not terminate in an FW76 pole, its next deep deficit
satisfies

```text
1<=q''<q'.                                        (FW208b)
```

Induction on the positive integer `q'`, with cap order as the inner measure
for the nonsymmetric (FW34) steps, must terminate.  This proves the
**OBSERVED all-order deep-offshoot deficit descent**

```text
an FW92--FW93 deep terminal of deficit q'
  => through nested endpoint caps and strictly decreasing positive deficits,
     an FW76 cap of order <=4.                    (FW208)
```

This normalises the deep continuation; it does not erase the original
three-tip pivot or exclude the final cap.  The surviving object is therefore
a contextual small cap together with its inherited pivot/descent history,
not a stand-alone claim that small caps cannot occur.  An independent Luna
audit verified the cross/internal collision at `R=0`, persistence of the
same global endpoints, and the lexicographic measure.  The lightweight
arithmetic replay checks 1,999,000 strict rows through radius 2000 and the
maximal unit-drop chain through deficit 100,000, while inheriting the five
double-checked known witnesses from (FW207):

```text
theory-lab/topwindow/verify_deep_offshoot_deficit_descent.py
theory-lab/topwindow/results/deep_offshoot_deficit_descent_certificate.json
```

The contextual pole at the end of (FW208) has an exact all-order digit strip.
Let `J` be that thin cap, let `a=|J|<=4`, and retain its endpoint `z`, root
radius `alpha`, boundary `g`, dominant complement `D`, opposite global
endpoint `x`, and positive remainder `R=g-sigma`.  To avoid confusing the
new deficit with an earlier edge, put

```text
q_0=N-diam(D)=alpha+R>alpha.
```

Write `P` for the reflected cap factor and `V` for the reflected complement
factor.  The terminal symmetric branch is the complete mixed-radix branch of
(FW34), not merely a symmetric set, so (FW76) gives exactly

```text
P={0};
P={0,alpha};
P={0,s,2s};
P={0,s,G,G+s},       G=2s rho with integer rho>=2. (FW209a)
```

The coefficients `0,...,q_0-1` of `P+V` are one and coefficient `q_0` is
zero, the latter because `diam(D)=N-q_0` is already an internal pair.  If
`v_j` is the indicator of `j in V`, coefficient recursion gives

```text
v_j=1-sum_{p in P-{0}, p<=j} v_{j-p},       0<=j<q_0.
```

The complete digit blocks solve this recurrence by the same canonical
indicator as (FW105):

```text
P={0}:                 chi_P(j)=1;
P={0,alpha}:           chi_P(j)=1 iff floor(j/alpha) is even;
P={0,s,2s}:            chi_P(j)=1 iff floor(j/s)=0 mod 3;
P={0,s,G,G+s}:         chi_P(j)=1 iff floor(j/s) and floor(j/G)
                                      are both even.                (FW209b)
```

Thus `v_j=chi_P(j)` below the hole.  At `q_0`, deleting the complement entry
must leave every shifted term zero; equivalently

```text
chi_P(q_0)=1.                                      (FW209c)
```

If `w` complement vertices occur in this visible strip, the `q_0` prefix
pairs give

```text
w>=ceil(q_0/a),
q_0<=a|D|=a(n-a)<=4(n-1).                         (FW209d)
```

The internal diameter pair of `D` keeps the old endpoint `x`.  This follows
from the same four-point argument as (FW92): otherwise a cross distance from
`x` to that pair would equal its diameter and repeat it.  Project its other
endpoint `y` to the old diameter at `b`, write `k=d(b,y)`, and define `r_0`
by `d(b,x)=k+r_0`.  Then

```text
d(b,z)=k+q_0,
N=2k+r_0+q_0,       r_0>=1,       r_0!=q_0.       (FW209e)
```

The strict positivity follows from maximality of the old diameter; equality
`r_0=q_0` would repeat the two rooted distances from `b`.  No lower bound
`k>=g` is asserted in this positive-remainder pole line.

Equations (FW209a)--(FW209e) prove the **OBSERVED all-order terminal-cap
digit/pivot normal form**.  The remaining terminal is no longer an arbitrary
small cap: it is one of four explicit digit strips, has first-hole deficit at
most `4(n-1)`, and carries a fixed endpoint pivot.  It is not yet excluded;
the missing step is a tree-realisation collision or a proper-core induction
for these four strips with the inherited pivot history.  An independent Luna
audit verified the complete-block hypothesis, the first-hole recurrence, the
linear envelope and the endpoint projection.  A constant-memory replay checks
829,751 canonical coefficients, 7,932 order bounds, and all six available
terminal caps of the five known witnesses after both checkers pass:

```text
theory-lab/topwindow/verify_terminal_cap_digit_pivot.py
theory-lab/topwindow/results/terminal_cap_digit_pivot_certificate.json
```

The opposite end of this digit strip gives a constant-width overlap, but one
must separate an ordinary half edge from the central edge.  Retain the
notation of (FW209), and first sharpen its elementary order count.  The
reflected complement factor contains its root value `beta`, while

```text
beta>N/2,                  q_0=N-diam(D)<N/2<beta.
```

Thus the root is an additional complement vertex above the visible strip.
If `w` complement vertices occur below `q_0`, then

```text
q_0<=a w,
w<=n-a-1,
q_0<=a(n-a-1)<=4(n-5).                           (FW210a)
```

There is no complement vertex at reflected coordinate `q_0`.  On the fixed
`x`--`z` diameter, let `f` be the edge crossed by the metric level `q_0`
measured from `x`.  If `f` lies strictly in the open `x`-half, (FW207)--
(FW208) give an `x`-endpoint FW76 terminal cap `K`, of order `b<=4`, whose
root radius `alpha_K` is strictly below `q_0`.

The inference `q_0<N/2 => f is an open-half edge` would be false: `f` may be
the central edge.  In that case write `lambda_x` for the `x`-side central
eccentricity, let `D_c` be the larger of the two central-side internal
diameters, and put `C=N-D_c`.  Since the level lies in the central edge,
`lambda_x<q_0`.  If `C>lambda_x`, apply (FW34) to the `x`-side factor.  Its
symmetric line makes that whole side order at most four; taking its endpoint
singleton if necessary gives a genuine thin terminal cap of radius zero.
Its nonsymmetric line supplies an edge strictly in the `x`-half, to which
(FW205)--(FW208) apply.  If `C<=lambda_x`, the central cross coefficient `C`
is zero because an internal `D_c`-pair already realises `D_c`.  Since the
other factor contains zero, the `x`-factor cannot contain `C`; in particular
`C<lambda_x`.  Its level-`C` shell is strictly in the `x`-half and again
(FW207)--(FW208) apply.  Uniformly, therefore,

```text
J_z of order a<=4 and first hole q_0
  => a disjoint x-terminal K_x of order b<=4,
     with alpha_K<q_0.                             (FW210b)
```

This central-edge split is essential; the known order-four path already
shows why the shorter midpoint argument is invalid.

The caps `J` and `K` are disjoint by their metric locations, not merely by
their radius bounds.  Every vertex of `J` is reached from `x` only after the
complement-root path of length `beta>N/2` and then the positive boundary
edge, whereas `K` is constructed wholly in the strict open `x`-half (or is
the endpoint singleton in the symmetric central fallback).  Hence no vertex
can lie in both caps.

Let

```text
Q=N-diam(T-K)
```

be the first hole of `K`.  The two deficits are unequal.  Indeed, the
diameter pair of `T-J` keeps `x`, while that of `T-K` keeps `z`; if `Q=q_0`,
distance uniqueness would make those pairs identical, which would make them
the global `xz` pair of distance `N`, not `N-q_0`.

Put `m=min(q_0,Q)`.  For every `0<=j<m`, the unique pair at distance `N-j`
crosses both pendant cuts.  Its endpoints must consequently lie one in `J`
and one in `K`.  Hence

```text
m<=ab<=16.                                         (FW210c)
```

This conclusion is stronger than separately observing that both diameter
endpoints are leaves: `K` is tied to the inherited level-`q_0` shell and has
radius below `q_0`.

The nonreversal branch has a complete finite classification.  Suppose
`q_0<Q`, and write `P,S` for the complete FW76 factors of `J,K`.  Now

```text
max(P)=alpha<q_0,             max(S)=alpha_K<q_0.
```

Every complement vertex visible below `q_0` belongs to the opposite cap, so

```text
S={j<q_0: chi_P(j)=1},
P={j<q_0: chi_S(j)=1},
chi_P(q_0)=chi_S(q_0)=1.                          (FW210d)
```

The cross-cap sums are direct, contain `0,...,q_0-1`, and omit `q_0`.
Exhausting the four complete factors of (FW209a) under `q_0<=16` gives 19
oriented rows.  Global uniqueness also makes the two cap-internal spectra
disjoint, leaving exactly the following eleven oriented rows (the displayed
transpose is included whenever the factors differ):

```text
q_0=1:  {0}                 x {0};
q_0=2:  {0}                 x {0,1};
q_0=3:  {0}                 x {0,1,2};
q_0=4:  {0,1}               x {0,2};
q_0=6:  {0,1}               x {0,2,4};
q_0=8:  {0,2}               x {0,1,4,5}.          (FW210e)
```

The removed rows are the alternative order-`6` scale pairing and all rows at
`q_0=9,12,16`; respectively their two caps repeat an internal distance
`3,3,6,6`.  In particular every surviving nonreversal rectangle tiles the
whole interval `0,...,q_0-1` and has `q_0=ab`.

Equations (FW210a)--(FW210e) prove the **OBSERVED all-order opposite-cap
overlap reduction**:

```text
an inherited FW209 terminal
  => Q<q_0 with the strict opposite deficit Q<=16;
     or q_0<Q and one of the eleven fixed oriented rectangles above. (FW210)
```

This is not an exclusion.  In the reversal branch the full original factor
need not lie below `Q`, so the table cannot be applied by symmetry.  The next
step is to absorb that inherited high digit, or to continue the top spectrum
from the eleven fixed rectangles into the proper core.  An independent Luna
audit checked the open-half/central split, radius inheritance, disjoint-cut
count, and scope of the finite table.  The constant-memory replay checks the
19 raw rows, the eight internal-spectrum collisions, the sharpened envelope
through order 2000, and all six available known terminal caps after both
repository checkers pass:

```text
theory-lab/topwindow/verify_terminal_cap_opposite_overlap.py
theory-lab/topwindow/results/terminal_cap_opposite_overlap_certificate.json
```

The eleven nonreversal rectangles have an exact periodic continuation.  Fix
one oriented row of (FW210e), write its factors as `P,S`, and put

```text
a=|P|,                    b=|S|,                    q=ab.
```

The six displayed mixed-radix products give, for every `j>=0`, not merely
through the audited prefix,

```text
chi_S(j)=1  iff  j mod q belongs to P.             (FW211a)
```

Thus the complement of the `S`-cap has the exact visible radial lattice

```text
P+q Z_{>=0}
```

below its own first hole `Q`.  Since `chi_S(Q)=1`, write uniquely

```text
Q=tq+p_*,                 p_* in P,
r=|{p in P:p<p_*}|.
```

There are

```text
w=ta+r
```

visible complement vertices.  Let `u` count all remaining complement
vertices except the complement root, whose reflected coordinate is
`beta>Q`.  Thus `u>=0` and `n-b-1=w+u`.  A direct rearrangement gives the
exact capacity and proper-complement excess identities

```text
delta=br-p_* in {0,1,2},
b(n-b-1)-Q=bu+delta,
N-Q-binom(n-b,2)=binom(b+1,2)+bu+delta.            (FW211b)
```

The first line identifies the old linear first-hole slack with an actual
number `u` of vertices outside the periodic band, up to a phase error of at
most two.  In particular, bounded capacity defect means that all but a fixed
number of complement vertices lie in the displayed lattice; the induced
proper complement then has only the explicit defect in the last line.  This
is the promised return from the digit table to a proper-core stability
parameter, not yet an induction.

The same lattice forces quartic rooted detour mass when `u` is small.  Keep
the first `t` complete blocks, with coordinate set

```text
Lambda_t={ell q+p:0<=ell<t, p in P},       s=at,
M=binom(s,2).
```

Root the complement at its cap-boundary vertex.  For `v,w in Lambda_t`, put

```text
sigma(v,w)=(d(v,w)-|depth(v)-depth(w)|)/2 >=0,
RS_t=sum_{unordered {v,w}} sigma(v,w).
```

All quantities are nonnegative integers.  If

```text
W(P)=sum_{p<p' in P}(p'-p),
```

then the exact sum of absolute rooted-depth differences is

```text
B_t=t W(P)+a^2 q t(t^2-1)/6.                      (FW211c)
```

The `M` actual pair distances are distinct positive integers, so their sum
is at least `M(M+1)/2`.  Consequently

```text
RS_t >= max(0, ceil((M(M+1)/2-B_t)/2))
     = a^4 t^4/16-O_q(t^3).                       (FW211d)
```

Equations (FW211a)--(FW211d) prove the **OBSERVED all-order periodic-lattice
stability reduction**.  If the capacity defect in (FW211b) is bounded, then
`at=n-O(1)` and (FW211d) is `n^4/16-O(n^3)`: the periodic proper complement
nearly saturates the total available distance mass in rooted detours.  This
is substantially stronger than a generic quartic lower bound, but it remains
a lower bound.  A conflicting upper bound, a rigidity theorem for near
saturation, or a decreasing proper-core transfer is still **UNVERIFIED**.
The constant-memory replay checks 110,011 canonical coefficients, every
phase and defect identity, and the exact depth-difference formula through
100 blocks in all eleven oriented rows:

```text
theory-lab/topwindow/verify_terminal_cap_periodic_lattice.py
theory-lab/topwindow/results/terminal_cap_periodic_lattice_certificate.json
```

The strict opposite-deficit reversal in (FW210) can be absorbed into the
same nonreversal table.  First record a general endpoint-peeling identity.
Let a non-singleton terminal cap have factor

```text
P={0=p_0<p_1<...<p_{a-1}}
```

and first hole `q>max(P)`.  Delete its coordinate-zero diameter endpoint.
For every `j<p_1`, the complete cross coefficient at `j` can only use the
cap digit zero, so the unique pair of distance `N-j` uses the deleted
endpoint.  At `j=p_1`, the cap digit `p_1` and the opposite factor digit zero
give a surviving pair.  Consequently the endpoint singleton has exact first
hole

```text
q_singleton=p_1.                                  (FW212a)
```

Now retain the FW210 caps `J_z,K_x`, with radii `alpha,alpha_K` and first
holes `q_0,Q`, and suppose that `Q<q_0`.  Reorient from `K_x` toward `z`.
Because `Q<q_0<N/2`, its level-`Q` shell is in the open `z`-half.  The FW76
endpoint `z` is joined directly to the root of `J` by one edge of weight
`alpha`;
the smaller factor digit `p_1` belongs to other cap geometry and is not a
break point on this diameter edge.  Also `q_0=alpha+R` with `R>0` no larger
than the boundary edge.  Hence the shell
cuts exactly

```text
J,       if alpha<Q<q_0;
{z},     if Q<alpha.
```

Equality `Q=alpha` is impossible: the root of `J` would be a complement
vertex at reflected coordinate `Q`, whereas `Q` is the first missing
coefficient for `K`.  Both displayed caps are already complete FW76 caps
and have radius below `Q`; no further deep descent is needed at this shell.

In the first line, orienting `K,J` gives a nonreversal rectangle immediately.
In the second line put `s=p_1`, the first hole of `{z}` from (FW212a).  If
`Q<s`, orienting `K,{z}` again gives a nonreversal rectangle.  It remains to
consider `s<Q`.  Reorient `{z}` toward `x`.  The same boundary-edge argument
cuts `K` when `alpha_K<s`, and cuts `{x}` when `s<alpha_K`; equality is again
forbidden by the missing coefficient at `s`.  The first outcome is a
nonreversal `{z},K` rectangle.  In the second outcome let `t` be the first
hole of `{x}`.  The holes `s,t` are unequal by the same two-complement
diameter argument used in (FW210).  Applying the two-cut prefix count to the
two endpoint singletons gives

```text
min(s,t)<=1,
```

so their positive smaller hole is exactly one and they form the `q_0=1`
row.  Thus at most two inner endpoint cuts suffice:

```text
every Q<q_0 reversal
  => a nested nonreversal pair in one of the eleven rows (FW210e),
     with no new unbounded spectral type.                       (FW212b)
```

The original outer cap can remain as contextual geometry, so (FW212b) is
not a deletion of vertices or a global induction.  It does, however, remove
the reversal as a separate terminal: applying (FW211) to the resulting
nested nonreversal pair gives the same exact periodic complement lattice.
Consequently all FW209 terminals now feed the single periodic-core stability
problem.  That core still needs a collision, a conflicting upper bound, or a
strictly decreasing proper-core transfer; this final implication remains
**UNVERIFIED**.

The constant-memory replay enumerates the fourteen parameterised high-wrapper
profiles, collapses them to four singleton-base oriented rows, checks the
endpoint-peeling coefficients, and replays the known reversal after both
repository checkers pass:

```text
theory-lab/topwindow/verify_terminal_cap_reversal_absorption.py
theory-lab/topwindow/results/terminal_cap_reversal_absorption_certificate.json
```

The periodic lattice forces a global branch-count alternative.  Keep an
oriented row `(q,P,S)` of (FW210e), with `a=|P|`, `b=|S|`, and take the first
`t` complete blocks from (FW211).  Their `s=at` reflected coordinates lie in

```text
[0,D],                 D=(t-1)q+max(P).
```

Root the complement of the `S`-cap at its boundary vertex and write `beta`
for its maximum rooted depth.  An ancestor-related pair of lattice vertices
has distance equal to the absolute difference of its two coordinates.
Global distance uniqueness therefore permits at most `D` such pairs.  Every
other pair has an LCA that is a global branch vertex.  For one fixed LCA of
rooted depth `d`, its distance is

```text
2beta-2d-y_1-y_2.
```

The two distinct coordinates have a sum in `{1,...,2D-1}`, so that LCA can
serve at most `2D-1` pairs.  If `B_D` is the number of global branch vertices
that can occur as LCAs inside this complement, then

```text
binom(at,2) <= D+B_D(2D-1).                       (FW213a)
```

When `b>=3`, the attachment root of the omitted complete `S`-cap is itself a
global branch vertex and cannot be one of those complement LCAs, exactly as
in the branch accounting of (FW148d).  Therefore the total number `B` of
global branch vertices satisfies

```text
B >= 1_{b>=3}
     +ceil([binom(at,2)-D]_+/(2D-1)).             (FW213b)
```

Since `D<tq=bat`, a convenient uniform consequence is

```text
B>at/(4b)-1.                                      (FW213c)
```

Thus an unbounded periodic band is possible only by forcing a linear number
of global branch vertices.  In particular, the near-saturated case
`at=n-O(1)` from (FW211) gives `B>=n/16-O(1)` because `b<=4`.  This is the
unconditional arbitrary-tree consequence; it is a branch-rich routing
alternative, not yet a contradiction.

There is also a useful conditional absolute bound.  If the whole tree has at
most three global branch vertices, put `K=3-1_{b>=3}` in (FW213a).  This
hypothesis is **not** supplied by (FW203)--(FW212); the following is only its
at-most-three-branch subcase.  The left side is then quadratic in `t` and the
right side linear.  Solving the eleven exact inequalities gives

```text
q; P; S                                  t_max   Q_max
1; {0}; {0}                                 13       13
2; {0}; {0,1}                               27       54
2; {0,1}; {0}                                6       13
3; {0}; {0,1,2}                             29       87
3; {0,1,2}; {0}                              4       14
4; {0,1}; {0,2}                             13       53
4; {0,2}; {0,1}                             13       54
6; {0,1}; {0,2,4}                           14       85
6; {0,2,4}; {0,1}                            9       58
8; {0,2}; {0,1,4,5}                         19      154
8; {0,1,4,5}; {0,2}                          6       53
```

Here `Q_max=t_max q+max(P)` safely maximises over the phase `p_*`.  The first
failed integer in every row has positive and thereafter increasing
left-minus-right forward difference, so the table controls the infinite
tail, not merely the replay horizon.  Conditionally and uniformly,

```text
t<=29,        at<=38,        w=at+r<=39,        Q<=154.  (FW213d)
```

Combining (FW213d) with `n-b-1=w+u` from (FW211) gives, still under that
extra branch-count hypothesis,

```text
u>=n-44.                                             (FW213e)
```

Thus the near-saturated `u=O(1)` periodic core is impossible at unbounded
order in the at-most-three-branch subcase.  Globally, (FW213b)--(FW213c)
instead force branch proliferation.  Neither line is yet the global
exclusion: the high-coordinate remainder in the first line and the
linear-branch geometry in the second remain **UNVERIFIED** terminals.

The constant-memory replay checks the global branch lower bound through
110,000 parameter rows, solves all eleven conditional quadratic
inequalities, proves their monotone tails, and inherits both-checker passage
from (FW212):

```text
theory-lab/topwindow/verify_terminal_cap_lattice_lca_bound.py
theory-lab/topwindow/results/terminal_cap_lattice_lca_bound_certificate.json
```

The visible/unseen split strengthens the global line of (FW213), without any
branch-count hypothesis.  Retain the first `t` complete lattice blocks
`Lambda_t`, put `s=at`, and retain

```text
D=(t-1)q+max(P),              Q=tq+p_*.
```

All `w=at+r` visible complement vertices have reflected coordinate below
`Q`.  The LCA of two vertices of `Lambda_t` is itself a complement vertex.
If that LCA is visible, with coordinate `c<Q`, the pair distance is

```text
2c-y_1-y_2 <= 2(Q-1).
```

This formula includes the ancestor case when the LCA is one endpoint.
Because global distances are unique, at most `2(Q-1)` lattice pairs can have
a visible LCA.  Every remaining LCA is one of the `u` unseen complement
vertices or the complement root.  For any one such fixed LCA, the coordinate
sum `y_1+y_2` again has at most `2D-1` values.  Therefore

```text
binom(at,2) <= 2(Q-1)+(u+1)(2D-1).                (FW214a)
```

Equivalently, for `at>=2`,

```text
u >= max(0,
        ceil([binom(at,2)-2(Q-1)]_+/(2D-1))-1).   (FW214b)
```

This exact inequality has a convenient uniform consequence.  If `at<=12b`,
then `at<=4b(u+3)` is immediate from `u>=0`.  Otherwise use
`D<bat` and `Q<b(at+a)` in (FW214a); after division by `2bat`, and using
`a/(at)=1/t<a/(12b)<=1/(3b)`, the same inequality gives

```text
at <= 4b(u+3).                                    (FW214c)
```

Now `n-b-1=at+r+u`, with `r<=a-1` and `a,b<=4`.  Hence

```text
n <= (4b+1)u+13b+a,
u >= ceil((n-56)/17).                             (FW214d)
```

In particular the exact capacity defect from (FW211b) satisfies

```text
bu+delta >= ceil((n-56)/17).                      (FW214e)
```

Thus bounded defect and an order-`n-O(1)` periodic complement are globally
impossible at unbounded order, not merely in the at-most-three-branch
subcase.  Combining (FW214c) with the global branch count (FW213c) also gives
the resource split `16B+u>n-24`.  The remaining terminal is now explicit:
linearly many complement vertices lie above the first hole, and a long
visible band also forces linearly many branch vertices.  A collision or
strict descent for this high-coordinate/branch-rich remainder remains
**UNVERIFIED**.

The constant-memory replay checks 229,989 exact row/phase balances through
10,000 blocks, the uniform integer bounds, both parent hashes, and inherited
passage through both repository checkers:

```text
theory-lab/topwindow/verify_terminal_cap_visible_unseen_balance.py
theory-lab/topwindow/results/terminal_cap_visible_unseen_balance_certificate.json
```

The high-coordinate part of that remainder has an additional global
heavy-spine alternative (FW215).  Work in the minimal rooted subtree spanning
the first `t` complete periodic blocks, put `s=at`, and keep the coordinate
width `D` from (FW213)--(FW214).  At a high-coordinate branch vertex let its
marked child groups have sizes `x_1,...,x_k`, total `M`, and largest size `L`.
Every cross-child pair has that same LCA.  Its distance is determined by the
sum of two lattice coordinates, so global distance uniqueness gives

```text
binom(M,2)-sum_i binom(x_i,2) <= 2D-1.            (FW215a)
```

Since `sum_i x_i^2<=LM`, the left side is at least `M(M-L)/2`.  While
`M>=ceil(s/2)`, using `D<bs` therefore shows that the heavy-child step sheds
strictly fewer than `8b` marked vertices:

```text
M-L <= 8b-1.                                      (FW215b)
```

On the other hand, a connected visible descendant cannot contain
`ceil(s/2)` marked vertices when `s>=80`: all pairs inside it have visible
LCA and hence distance at most `2(Q-1)`, whereas the eleven exact rows satisfy

```text
binom(ceil(s/2),2) > 2(Q-1).
```

The heavy path must consequently lose more than `s/2` marked vertices before
entering the visible band.  Combining this with (FW215b) gives the exact hop
bound

```text
H > s/[2(8b-1)].                                  (FW215c)
```

Because `b<=4` and `n=b+1+s+r+u` with `b+1+r<=8`, this yields the convenient
all-order routing statement

```text
n>=160  =>  u>=n/2-8  or  H>n/124.                (FW215d)
```

Thus the surviving terminal has either a half-order unseen high-coordinate
part or a linear-hop heavy spine whose high splits shed at most 31 lattice
vertices apiece.  This is an **OBSERVED all-order structural alternative**,
not an exclusion: the pendant bundles along the spine have not yet been
classified, and no collision or decreasing transfer has yet been proved.
The constant-memory replay checks 229,141 row/phase inequalities through
10,000 blocks, the parent hashes, and inherited passage through both checkers:

```text
theory-lab/topwindow/verify_terminal_cap_unseen_spine.py
theory-lab/topwindow/results/terminal_cap_unseen_spine_certificate.json
```

The bounded shedding also forces a quadratic *weighted* span (FW216), not
only many hops.  Follow the FW215 heavy child until its marked order first
drops below `s/2`.  If the successive marked orders are `M_i`, put
`e_i=M_i-M_{i+1}` and `c=8b-1`.  Then

```text
1<=e_i<=c,          s/2-c<=M_H<s/2.
```

At step `i`, every shed--retained pair has the current branch vertex as LCA.
These pair families are disjoint over the steps, and telescoping gives

```text
C_sp=sum_i e_i M_{i+1}
    =(s^2-M_H^2-sum_i e_i^2)/2
   >=ceil(3s^2/8-cs/4-c^2/2).                    (FW216a)
```

If `gamma_i` is the reflected coordinate of that branch vertex, each of
these distinct distances is `2gamma_i-y-z`, with
`Q<gamma_i<=beta` and `0<=y,z<=D`.  They therefore all lie in the common
integer interval `[2Q-2D,2beta]`.  Packing (FW216a) into that interval yields

```text
beta-Q >= ceil((C_sp-1)/2)-D
       >= 3s^2/16-O(bs).                          (FW216b)
```

Thus the heavy-spine output consumes a quadratic high-coordinate span.  This
is an independently audited **OBSERVED all-order span lower bound**, not the
missing contradiction: `beta-Q` is itself allowed to have order `n^2`.
There is not yet an `o(s^2)` upper bound, cross-level translate collision, or
cap/full-support edge on this spine.  The constant-memory replay checks
109,497 exact row/block rounding inequalities and inherited checker passage:

```text
theory-lab/topwindow/verify_terminal_cap_spine_span.py
theory-lab/topwindow/results/terminal_cap_spine_span_certificate.json
```

Taylor parity routes four of the eleven rows directly toward the unseen
alternative (FW217).  For two lattice vertices of reflected coordinates
`y,z`, the tree-distance parity is `y+z mod 2`.  In the four oriented rows

```text
(q,P,S)=(2,{0},{0,1}), (4,{0,2},{0,1}),
        (6,{0,2,4},{0,1}), (8,{0,2},{0,1,4,5}),
```

every visible lattice coordinate is even, so all `s=at` vertices lie in one
Taylor parity class.  If the Taylor integer is `k`, so that
`n=k^2` or `n=k^2+2`, the larger class has order `(n+k)/2`.  Since
`n=b+1+s+r+u` and `r<=a-1`,

```text
u >= (n-k)/2-a-b >= (n-k)/2-6.                  (FW217)
```

This independently audited **OBSERVED all-order parity routing** makes the
unseen part asymptotically half the tree in these four rows.  It does not
classify that unseen core or exclude the other seven rows.  Replay:

```text
theory-lab/topwindow/verify_terminal_cap_parity_routing.py
theory-lab/topwindow/results/terminal_cap_parity_routing_certificate.json
```

There is a shorter global entry into the periodic terminal.  It does not
repair the historical provenance of every FW203--FW208 output; instead it
starts again from the two global diameter endpoints and directly re-proves
the FW209--FW210 data needed in the singleton case.

Let `x,z` be the endpoints of the unique pair at distance
`N=binom(n,2)`.  Both are leaves.  The unique pair at distance `N-1` cannot
use both `x,z`, since their mutual distance is `N`.  Choose the notation so
that it does not use `z`.  Deleting `z` leaves that pair and removes the only
distance-`N` pair, so

```text
diam(T-z)=N-1,                 q_0=N-diam(T-z)=1.       (FW218a)
```

The retained `N-1` pair contains `x`.  Otherwise write it as `{u,v}`.
The four-point sum

```text
d(x,z)+d(u,v)=2N-1
```

would have to tie one of the other two sums.  Every pair in either other
sum is different from both the unique distance-`N` pair and the unique
distance-`N-1` pair, so each term is at most `N-2` and each sum at most
`2N-4`, a contradiction.  Write the retained pair as `{x,y}`.

Let `p` be the neighbour of `z`, let `g=w(pz)`, and project `y` to the
`p`--`x` path at `b`.  Put

```text
k=d(b,y),                    s=d(b,x).
```

Then `s+k=N-1`.  Since `{x,z}` is the unique diameter pair,

```text
d(z,y)=N-s+k<N,
```

so `k<s`.  Define `r_0=s-k>=1`.  Also

```text
d(b,z)=N-s=k+1.
```

If `r_0=1`, the distinct pairs `{b,x}` and `{b,z}` both have distance
`k+1`.  Hence `r_0>=2`, and

```text
d(b,z)=k+1,                  d(b,x)=k+r_0,
N=2k+r_0+1,                 r_0>=2,
g<=k+1<N/2.                                           (FW218b)
```

In particular `beta=d(p,x)=N-g>N/2`.  It is the rooted eccentricity of
`T-z` at `p`: if some `v in T-z` had `d(p,v)>beta`, then
`d(z,v)=g+d(p,v)>N`.  The singleton `J={z}` has `alpha=0`, and with
`D=T-z`,

```text
sigma=diam(D)-beta=g-1,
R=g-sigma=1,
q_0=alpha+R=1>alpha.                                  (FW218c)
```

Thus `P={0}` is the complete singleton factor.  Cross coefficient zero is
the global diameter pair, while cross coefficient one is absent because the
global distance `N-1` is already realised internally in `D`.  Equations
(FW209a)--(FW209d) are immediate for this one-coefficient prefix, and
(FW218b) is exactly (FW209e), with `r_0!=q_0`.  This is a direct singleton
extension of the analytic FW209 package, not a claim that `J` has inherited
the historical FW208 descent provenance.

Deleting `x` removes both the unique `N` pair and the unique `N-1` pair, so

```text
Q=N-diam(T-x)>=2.                                      (FW218d)
```

Replay the FW210 construction from the directly verified singleton data.
Its opposite terminal `K` has integer rooted radius
`alpha_K<q_0=1`; hence `alpha_K=0`, and positive edge weights force
`K={x}`.  Therefore `q_0<Q`, reversal is impossible, and the unique
nonreversal rectangle is

```text
(q,P,S)=(1,{0},{0}).                                  (FW218e)
```

There is one small-order root-location exception before applying the FW211
vertex count.  Root `T-x` at the neighbour of `x`, let `beta_K` be the
reflected coordinate of that root, and use the FW210 `q=1` cross prefix:
there is exactly one complement vertex at each coordinate
`0,...,Q-1`, and none at `Q`.  The equality `beta_K=Q` would put the root
at the hole.  If `beta_K<Q`, then necessarily `beta_K=Q-1`; no coordinate
above `Q` can occur, so `Q=n-1` and the rooted depths are exactly
`0,1,...,n-2`.  Any edge not incident with the root would then repeat its
weight as a root-to-vertex distance.  Hence the complement would be a root
star.  For `n>=5` its leaf weights include `1,2,3`, and the leaf-pair
distance `1+2=3` repeats the third rooted depth.  Consequently

```text
n>=5  =>  beta_K>Q,  Q<=n-2,  u=n-2-Q.               (FW218f)
```

Equations (FW218a)--(FW218f) prove the **OBSERVED all-order universal
endpoint-one singleton extension**:

```text
every Leech tree of order n>=3
  => the unique FW210 rectangle (1,{0},{0});
every Leech tree of order n>=5
  => the full FW211 q=1 normal form.                   (FW218)
```

Thus every hypothetical G18 counterexample enters the single `q=1` row;
the other ten FW210 rows remain valid contextual outputs but are bypassed by
this global endpoint normalization, not excluded.  The remaining theorem is
still the classification, collision or decreasing transfer of the q=1
unseen core.  It is not G18.  The constant-memory replay checks the unique
row, 320,064 pivot integer cases, the root-hit boundary through order 10,000,
and all five known witnesses through both independent checkers:

```text
theory-lab/topwindow/verify_universal_endpoint_one.py
theory-lab/topwindow/results/universal_endpoint_one_certificate.json
```

## The exact q=1 threshold core and boundary forest

Specialise (FW211) using (FW218).  Let `x` be the endpoint singleton on the
opposite side, put `T'=T-x`, and root `T'` at the neighbour `p` of `x`.
Write `beta=d(p,z)` for the rooted eccentricity attained at the other
diameter endpoint and

```text
y(v)=beta-d(p,v)       (v in T').
```

The `q=1` row has

```text
a=b=q=1,   P=S={0},   p_*=r=delta=0,
t=Q,       D=Q-1,     n=Q+u+2.                    (FW219a)
```

Consequently there is exactly one vertex at each reflected coordinate
`0,...,Q-1`, there is no vertex at coordinate `Q`, and the remaining `u+1`
vertices have coordinate greater than `Q`.  Define

```text
H_Q={v in T': y(v)>Q}.
```

The root belongs to `H_Q`.  Moving from a vertex toward the root strictly
increases `y`, so every ancestor of a vertex of `H_Q` is again in `H_Q`.
Thus `H_Q` is a connected induced proper subtree of order `u+1`.  The
`Q` visible vertices form a descendant-closed pendant forest below it.

This core has an exact spectral meaning, not merely a vertex-count meaning.
If `g=w(px)`, then `g+beta=N`, and hence

```text
d(x,v)=g+d(p,v)=N-y(v).                            (FW219b)
```

All internal distances of `T'` lie in `[1,N-Q]`.  For `v in H_Q`, the value
in (FW219b) also lies in this interval and cannot be an internal distance,
because the cross pair `{x,v}` has already used it globally.  There are
exactly

```text
(N-Q)-binom(n-1,2)=n-1-Q=u+1
```

holes in that interval, exactly the order of `H_Q`.  Therefore

```text
Spec(T')=[1,N-Q] minus {d(x,v): v in H_Q}.          (FW219c)
```

In particular the core vertices are in bijection with *all* holes of the
internal spectrum of `T'`.  This does not say that those `u+1` holes form a
prefix, an interval or a bounded-defect set.

Let the connected components of the visible forest have orders
`s_1,...,s_k`.  Two vertices in the same component have a visible LCA of
coordinate `ell<Q`.  If their distinct coordinates are `i,j`, their distance
is

```text
2ell-i-j in [1,2Q-3].
```

Global distance uniqueness makes all such same-component distances distinct,
even between different visible components.  Since `sum_i s_i=Q`,

```text
sum_i binom(s_i,2) <= 2Q-3,
sum_i s_i^2       <= 5Q-6,
k >= ceil(Q^2/(5Q-6)),
max_i s_i <= floor((1+sqrt(16Q-23))/2).             (FW219d)
```

There is also an exact cross-Sidon constraint at every LCA, including LCAs
inside `H_Q`.  For two different child subtrees of an LCA, let `A,B` be their
sets of reflected coordinates and put
`Delta(A)={a-a':a,a' in A}`.  Cross-child distances have the form
`2ell-a-b`.  Since all coordinates are distinct by (FW219b), injectivity for
pairs crossing these two fixed child branches forces the local condition

```text
Delta(A) intersect Delta(B)={0}.                    (FW219e)
```

The exact q=1 specialisations of (FW214a) and (FW213a) give, respectively,

```text
binom(Q,2) <= 2(Q-1)+(u+1)(2Q-3),
(Q-1)(Q-2)/2 <= B(2Q-3),                            (FW219f)
```

where `B` is the number of global branch vertices.  The first quadratic is
already positive at `Q=4u+8` and increases thereafter; the second is already
violated at `Q=4B+3` and its gap likewise increases.  Combining their exact
integer consequences with (FW219a) yields

```text
Q<=4u+7,        u>=ceil((n-9)/5),
Q<=4B+2,        4B+u>=n-4.                          (FW219g)
```

Equations (FW219a)--(FW219g) prove the **OBSERVED all-order exact q=1
threshold-core and boundary-forest theorem**.  They replace a fragmented
unseen remainder by a connected proper core, identify its exact spectral
interface, and add both a linear number of visible boundaries and local
cross-Sidon constraints.  They do not yet normalise all those boundaries to
valid caps, bound the geometry of the `u+1` holes, prove a no-return transfer,
or prove G18.  The constant-memory replay checks 15,999,999 integer rows
through `Q,u<=4000`, the known `L4` path and `L6` threshold geometries, and
inherits both-checker passage for all five known witnesses from (FW218):

```text
theory-lab/topwindow/verify_q1_threshold_core.py
theory-lab/topwindow/results/q1_threshold_core_certificate.json
```

The first proposed strengthening of (FW219e) does not follow from the present
interface.  At stage `i`, start with the coordinate interval
`{i,...,Q-1-i}`, shed its two endpoints, and retain the middle interval.
The only nonzero shed difference is

```text
Q-1-2i,
```

whereas every retained difference has absolute value at most `Q-3-2i`.
Thus (FW219e) holds at every stage.  Taking `floor(Q/4)` stages leaves at
least `ceil(Q/2)` retained coordinates but gives

```text
sum_i(e_i-1)=floor(Q/4),
```

not `O(1)`.  Decreasing LCA coordinates spaced by `Q` put the two
shed--retained distance intervals from each stage in disjoint positive
blocks; all blocks fit inside `1,...,binom(Q+floor(Q/4)+1,2)`.  Hence the
q=1 balances, per-LCA cross-Sidon relation and the exact FW216 modeled-family
packing still admit this scalable double-peel relaxation.

This is an **OBSERVED negative diagnostic**, not a Leech witness and not a
refutation of a stronger A-prime statement with new tree-realisation input:
the terminal retained subtree and the pair classes not counted by FW216 are
deliberately unspecified.  It does refute deriving bounded total shedding
from the currently recorded constraints alone, so that subroute is stopped.
Replay and frozen trust boundary:

```text
theory-lab/topwindow/probe_q1_cross_sidon_double_peel.py
theory-lab/topwindow/results/q1_cross_sidon_double_peel_certificate.json
```

The threshold forest nevertheless contains a canonical strictly smaller cap
interface.  Assume `Q>=4`, and write `v_j` for the unique visible vertex of
coordinate `j`.  Let `W_0` be the visible component containing
`v_0=z`.  By (FW219d) there are at least two visible components.  Define

```text
q'=min{j>=1:v_j not in W_0}.
```

Then `v_0,...,v_{q'-1}` lie in `W_0`, while `v_{q'}` does not.  Deleting
`W_0` removes exactly the unique top pairs
`{x,v_0},...,{x,v_{q'-1}}` and retains `{x,v_{q'}}`.  Hence

```text
diam(T-W_0)=N-q',
1<=q'<=|W_0|<=floor((1+sqrt(16Q-23))/2)<Q.          (FW220a)
```

Let `e` be the unique entry edge of `W_0`.  It lies on the global
`x`--`z` diameter.  Since it is an edge of `T-x`,

```text
w(e)<=N-Q<N-q'=d(x,v_{q'}).
```

Thus the centre side of `e` is supported.  Equality
`diam(W_0)=w(e)` would repeat the edge distance, so exactly two cases remain.

If `diam(W_0)<w(e)`, then `W_0` is already thin.  Let `p_e` be the
centre-side endpoint of `e` and put `c=y(p_e)`.  The equality `c=N/2` is impossible,
because its distances to `x,z` would coincide.  If `c<N/2`, the entry lies
in the open `z`-half and
`d(p_e,x)=N-c>N/2>2Q-3>=diam(W_0)`, so the thin cap is
dominant.  If `c>N/2`, the edge crosses the midpoint and is the central edge;
this is the central-thin branch.

If `diam(W_0)>w(e)`, the edge is bidirectional.  Follow its maximal
bidirectional edge-component toward the leaf `z`, and let `f` be the first
edge leaving that component in the `z` direction.  Such an edge exists
because a leaf edge cannot be bidirectional.  Let `W'_0` be its `z`-side.
The pair `{x,v_{q'}}` lies wholly on the centre side of `f` and has distance
greater than `w(f)`.  Since `f` is not bidirectional and equality with
`w(f)` is forbidden, `diam(W'_0)<w(f)`.

Both endpoints of `f` are visible.  If its centre-side endpoint is `p_f`
and `c_f=y(p_f)`, then

```text
d(p_f,z)=c_f<Q<N/2,
d(p_f,x)=N-c_f>N-Q>2Q-3>=diam(W'_0).               (FW220b)
```

Here `Q<N/2`, `2Q-3<N/2`, and the stronger
`N-Q>2Q-3` all follow from `Q<=n-2`, `Q>=4` and hence `n>=6`.
Therefore `W'_0` is an open-half dominant thin cap.  If

```text
q''=min{j>=1:v_j not in W'_0},
```

the same top-pair argument gives

```text
diam(T-W'_0)=N-q'',
1<=q''<=q'<=|W_0|<Q.                               (FW220c)
```

Equations (FW220a)--(FW220c) prove the **OBSERVED all-order coordinate-zero
smaller-cap bridge**: for `Q>=4`, the q=1 terminal exposes a thin z-cap with
strictly smaller top deficit `q_*<=O(sqrt(Q))`; a bidirectional entry always
produces the nested open-half dominant version, while a direct thin entry is
either open-half dominant or central-thin.  This is a genuine local decrease
before normalisation.  It is not yet the required no-return theorem: the
existing cap machinery could conceivably normalise the new cap back to the
endpoint-one state with opposite hole `Q`.  The constant-memory replay checks
the integer envelopes through `Q=100000`, the direct-thin `L6` control, and
inherits both-checker passage from (FW219):

```text
theory-lab/topwindow/verify_q1_coordinate_zero_cap.py
theory-lab/topwindow/results/q1_coordinate_zero_cap_certificate.json
```

The normalisation return from (FW220) has a finite catalogue.  Let `C` be
one of its thin `z`-caps, with boundary `g`, cap root `c`, complement root
`p`, first hole `q_*`, and `D=T-C`.  Put

```text
alpha=d(c,z)<Q,       beta=d(p,x),
E=diam(D)=N-q_*,      sigma=E-beta>=0,
R=g-sigma.
```

The cap is contained in one visible component, so
`diam(C)<=2Q-3<E`.  Hence every distance above `E` crosses its boundary and
gives the exact reflected prefix through coefficient `q_*-1`, while
coefficient `q_*` is absent because `E` is already internal to `D`.  Since
`N=alpha+g+beta`,

```text
q_*=alpha+R.                                          (FW221a)
```

If `R=0`, the distinct cross pair `{c,x}` also has distance
`g+beta=E`, a collision.  If `R>0`, apply (FW34) to the cap factor; every
nonsymmetric closure is a strict nested `z`-cap inside `C`.  If `R<0`, then
`q_*<alpha<Q`, so the absent-level shell lies on the cap-root--`z` path in
the open endpoint half and enters (FW207)--(FW208).  Thus cap order and then
positive deficit give the same finite lexicographic termination as before,
without requiring the original entry edge to have open-half provenance.

Let the terminal FW76 pole be `J subseteq C` and let its first hole be
`q_0`.  Deleting a subset of `C` retains all of `D`, so its complement
diameter cannot decrease.  Therefore

```text
1<=q_0<=q_*<Q.                                       (FW221b)
```

Now let `g_x` be the leaf edge at the opposite diameter endpoint `x`.  The
tree `T-x` still contains the `x`-neighbour--`z` path of length `N-g_x`.
Since `diam(T-x)=N-Q`,

```text
Q<=g_x.
```

Consequently the level-`q_0` shell lies strictly inside that leaf edge and
cuts exactly the singleton `{x}`.  In the FW210 orientation the opposite
factor is therefore `S={0}`.  Filtering the exact eleven-row table leaves
only

```text
q_0=1:  P={0},       S={0};
q_0=2:  P={0,1},     S={0};
q_0=3:  P={0,1,2},   S={0}.                         (FW221c)
```

The three cap factors are respectively the endpoint singleton, rooted `L2`,
and rooted `L3` with its middle vertex as root.  The last row is realised by
the known `L6` witness, so it cannot be removed without a genuinely
large-order input.

Equations (FW221a)--(FW221c) prove the **OBSERVED all-order q=1 small-return
catalogue** for `Q>=4`.  It is the requested topology-independent finite
catalogue of returns from the FW220 cap: no larger pole or other one of the
eleven periodic rows can return through the original endpoint singleton.
It does not exclude these three rows, control the wrapper `C-J`, treat the
separate original small-hole cases `Q=2,3`, or prove G18.  The replay filters
the frozen FW210 table, covers the monotone endpoint-shell inequalities
symbolically through order 100000, checks `L6` as the `q_0=3` positive
control, and inherits both-checker passage:

```text
theory-lab/topwindow/verify_q1_small_return_catalogue.py
theory-lab/topwindow/results/q1_small_return_catalogue_certificate.json
```

The three catalogue rows carry an exact bounded-defect proper-core
interface.  Let `a=|J| in {1,2,3}`, let `g` be the boundary edge of `J`, and
put `D=T-J`, rooted at the endpoint of `g` in `D`.  Write

```text
F_D(X)=sum_{d in Spec(D)} X^d,
R_D(X)=sum_{v in D} X^{d(root(D),v)},
I_m(X)=X+...+X^m,
A_a(X)=1+X+...+X^{a-1}.
```

The full factors in (FW221c) say that the rooted depth set of `J` is exactly
`{0,...,a-1}`.  Its internal spectrum is the complete Leech interval
`{1,...,binom(a,2)}`.  Every pair crossing `g` has distance

```text
g+r+s,       0<=r<a,       s in depth(D).
```

The internal-`D`, internal-`J`, and cross pair classes are disjoint and
together are all pairs of `T`.  Since the global distance polynomial is
`I_N`, coefficientwise uniqueness gives the exact identity

```text
I_N(X)=F_D(X)+I_binom(a,2)(X)+X^g A_a(X)R_D(X).     (FW222a)
```

The cap is thin, so `g>binom(a,2)`.  Below degree `g` the cross term in
(FW222a) vanishes.  The small cap uses exactly the first `binom(a,2)`
values, and every later coefficient must come from `D`.  Therefore

```text
Spec(D) intersect [1,g-1]
  ={binom(a,2)+1,...,g-1}.                          (FW222b)
```

Thus `D` is a connected induced proper core of order `n-a` with an exact
prefix having respectively `0,1,3` fixed initial holes.  This proves the
**OBSERVED all-order q=1 bounded-defect return-core interface**.  It is the
first requested spectral inheritance statement, but not yet a Leech-core
induction: `g` has not been proved unbounded, and the spectrum of `D` above
`g` remains free.  The next dichotomy is therefore to amplify a growing `g`
through (FW222a), or classify the bounded-`g` endpoint attachments.  The
constant-memory replay checks all three factors, 299,991 counting rows
through order 100000, the exact polynomial partition in the known `L3` and
`L6` controls, and inherited passage through both checkers:

```text
theory-lab/topwindow/verify_q1_return_prefix_interface.py
theory-lab/topwindow/results/q1_return_prefix_interface_certificate.json
```

The part of the spectrum above `g` is not arbitrary once the retained
`q=1` coordinates are kept.  Put `d=n-a`, and list the rooted depths of `D`
as

```text
0=s_0<s_1<...<s_(d-1)=beta.
```

Coefficient injectivity of `A_a R_D` says that its translated blocks

```text
[s_i,s_i+a-1]
```

are pairwise disjoint.  Thus, for `1<=i<d`, there are integers `e_i>=0`
such that

```text
s_i-s_(i-1)=a+e_i.                                  (FW223a)
```

The global maximum is cross and the deepest cap vertex has rooted depth
`a-1`, so

```text
N=g+(a-1)+beta.
```

Consequently the ordinary edge excess of the `J|D` boundary is exactly the
total rooted-gap excess:

```text
E_g=N+1-a(n-a)-g
   =beta-a(d-1)
   =sum_(i=1)^(d-1) e_i.                            (FW223b)
```

There is also a coefficientwise version of this equality.  Between the
cross blocks beginning at `g+s_(i-1)` and `g+s_i`, the only available
coefficients are the `e_i` internal distances of `D`.  Hence (FW222a) is
equivalent to the disjoint interval partition

```text
Spec(D)
  ={binom(a,2)+1,...,g-1}
   disjoint_union
   union_(i=1)^(d-1)
     {g+s_(i-1)+a,...,g+s_i-1}.                    (FW223c)
```

Empty intervals are allowed when `e_i=0`.  In particular `E_g` is not an
unlocated count of high pairs: the `i`th rooted-depth gap carries exactly
the `i`th interval in (FW223c).

The old `q=1` top window anchors the last gap exactly.  Let `v_j` be the
unique vertex of original reflected coordinate `j`, `0<=j<Q`, with
`v_0=z`.  The return factor `J` consists of the vertices at coordinates
`0,...,a-1`.  Therefore `D` retains `x,v_a,...,v_(Q-1)`, and

```text
d(x,v_j)=N-j,              a<=j<Q.
```

Thus `D` contains the complete top interval
`{N-Q+1,...,N-a}`.  The unique pair at distance `N-Q`, namely the diameter
pair of `T-x`, contains `z` by the endpoint-retention part of (FW210); it is
deleted with `J`.  Hence `N-Q` is not a distance of `D`.  Comparing with the
last interval in (FW223c) gives

```text
e_(d-1)=Q-a,
s_(d-1)-s_(d-2)=Q,
last high interval of D={N-Q+1,...,N-a}.            (FW223d)
```

Moreover `s_(d-1)=beta` belongs to `x`, while the cross pair using cap depth
`a-1` and core depth `s_(d-2)` is the unique `N-Q` pair.  Thus the second
deepest rooted vertex of `D` is precisely the mate of `z` in the diameter of
`T-x`.  The unique diameter of `D` is the retained pair `{x,v_a}`.  If `b`
is the projection/LCA of `x,v_a` in `D` rooted at its boundary vertex `p`,
and `ell=d(p,b)`, then

```text
d(p,x)=N-g-a+1,
d(p,v_a)=g-1+2ell.                                  (FW223e)
```

Finally the return boundary has an exact location in the original threshold
geometry.  Its cap root has coordinate `a-1`, so the root `p` on the `D`
side has coordinate

```text
y(p)=g+a-1.
```

Coordinate `Q` is absent.  If `p` is still visible, then `p` lies in the
same visible component as `J` and

```text
g<=Q-a.
```

If `p` lies in the connected threshold core, the boundary is the entry edge
of the coordinate-zero visible component.  Its entire `z`-side is `J`, so
`J=W_0`, and

```text
g>=Q-a+2.
```

There is no intermediate equality `g=Q-a+1`.  Combining this location split
with (FW223a)--(FW223e) proves the **OBSERVED all-order anchored q=1 return
gap ladder**:

```text
visible-root return:
  g<=Q-a and a proper visible wrapper remains;

threshold-core-root return:
  J=W_0 and g>=Q-a+2;

in both branches:
  E_g=sum e_i and e_(d-1)=Q-a.                     (FW223)
```

This replaces the unspecified upper spectrum in (FW222) by exact rooted-gap
intervals and pins one of them to the old opposite hole.  It is not yet a
collision or a decreasing contextual Leech state: the remaining
`e_1,...,e_(d-2)` can still carry quadratic mass.  The next step is now
sharper than an absolute growing-`g`/bounded-`g` split: the visible-root
branch has `g<=Q-a=O(n)` and retains a wrapper, while the threshold-core-root
branch has no discarded wrapper and must be attacked through its remaining
gap mass.  Constant-memory replay and the `L6` positive control:

```text
theory-lab/topwindow/verify_q1_return_gap_ladder.py
theory-lab/topwindow/results/q1_return_gap_ladder_certificate.json
```

The anchored final gap admits an exact simultaneous peel of its two ends.
Let `r` be the neighbour of the opposite endpoint `x`, put `h=w(rx)`, and
write

```text
K=T-(J union {x}),          H=H_Q subset K,
M=N-Q.
```

Root `K` at `p`, the old `J|D` boundary vertex, and root `H` and `K` also at
`r` when a superscript `r` is used.  Write `R_p(K)`, `R_r(K)` and `R_r(H)`
for the corresponding rooted-depth polynomials.  Finally, for an interval
write

```text
I_[A,B](X)=X^A+...+X^B.
```

The exact hole bijection (FW219c) says that the missing distances of `T-x`
inside `1,...,M` are precisely

```text
{d(x,v):v in H}.
```

The set `H` is connected and contains `r`, so its hole polynomial is exactly
`X^h R_r(H)`.  On the other hand, the actual pairs of `T-x` split into the
pairs internal to `K`, the pairs internal to `J`, and the `J|K` cross pairs.
Adding the holes back gives the coefficientwise disjoint tiling

```text
I_M
 =F_K+I_binom(a,2)+X^g A_a R_p(K)+X^h R_r(H).       (FW224a)
```

The same statement from the removed endpoint has a second exact form.  Its
pairs to `H` are the hole factor just displayed.  Every other vertex of `K`
is one of the retained visible vertices `v_a,...,v_(Q-1)`, and its distance
from `x` is `N-a,...,N-Q+1`.  Therefore

```text
X^h R_r(K)
 =X^h R_r(H)+I_[M+1,N-a],                           (FW224b)

depth_r(K-H)={M+1-h,...,N-a-h}.                     (FW224c)
```

The last set is a consecutive rooted-depth block of order `Q-a`; it is not
merely a count.  The cardinality checks are exact:

```text
|K|=n-a-1=(u+1)+(Q-a),
binom(|K|,2)+binom(a,2)+a|K|+(u+1)=M.
```

Equations (FW224a)--(FW224c) prove the **OBSERVED all-order exact q=1
double-peel tiling**.  It is the first strict-size contextual state in the
return route: both `J` and `x` are removed, the ambient complete interval
drops from `N` to `M=N-Q`, and the formerly abstract holes are a rooted
factor of the connected proper core `H`.  The position split in (FW223)
now reads:

```text
p visible:
  g<=Q-a<h, and the H-factor starts strictly after the J-boundary prefix;

p in H:
  J=W_0, and both endpoint factors attach directly through the connected
  threshold core.                                      (FW224d)
```

This is not yet an induction theorem.  A further peel must preserve the
four-class form, or force a collision, with a strictly smaller contextual
parameter; (FW224) alone does not prove that closure.  It does, however,
replace the earlier request for an unspecified inherited hole interface by
an exact two-root polynomial state.  Constant-memory counting replay and the
`L6` partition

```text
1..11 = {4} disjoint_union {1,2,3}
        disjoint_union {5,6,7,9,10,11}
        disjoint_union {8}
```

are frozen by

```text
theory-lab/topwindow/verify_q1_double_peel_tiling.py
theory-lab/topwindow/results/q1_double_peel_tiling_certificate.json
```

The double-peel state is also a linear-defect stability reduction.  Put

```text
k=|K|=n-a-1,       C=binom(k,2),       L=M-C.
```

Using `n=Q+u+2`, the length of the available band above the perfect
order-`k` diameter is exactly

```text
L=(a+1)n-binom(a+2,2)-Q
 =a n+u+1-a(a+3)/2
 =binom(a,2)+a k+(u+1).                             (FW225a)
```

The last expression is exactly the number of coefficients in the three
non-`F_K` terms of (FW224a).  Since `Q>=4` and `a<=3`,

```text
a=1: L<=2n-7;
a=2: L<=3n-10;
a=3: L<=4n-14.                                     (FW225b)
```

Let

```text
B_K={1,...,C} minus Spec(K),
O_K=Spec(K) intersect {C+1,...,M}.
```

The tree `K` has exactly `C` pair distances, all in `1,...,C+L`.  Therefore

```text
|B_K|=|O_K|=:delta<=L,
Spec(K)=({1,...,C} minus B_K) disjoint_union O_K.   (FW225c)
```

Equations (FW225a)--(FW225c) prove the **OBSERVED all-order q=1
double-peel linear-defect stability reduction**.  The proper tree `K` has
order `n-O(1)`, diameter at most `binom(|K|,2)+4n-14`, and its deviations
from a perfect Leech interval are paired low holes/high outliers.  In a
least-counterexample argument, the singleton-return row with `delta=0`
would make `K` a smaller Leech tree (with the separately known order-16
base when `n=18`); the other rows already have their fixed cap holes.

This does not make `delta` bounded.  The next valid split is now

```text
delta bounded:
  finite-hole / endpoint-strip classification of K;

delta growing:
  the same number of low coefficients must be supplied by the two rooted
  factors in (FW224a), where cross-Sidon and connected-H provenance remain
  available.                                           (FW225d)
```

Another generic span lower bound would not close either branch; the required
next lemma is a stability/collision theorem using the rooted provenance of
those `delta` low intrusions.  Arithmetic replay through order `100000` and
the `L6` defect-one positive control are frozen by

```text
theory-lab/topwindow/verify_q1_double_peel_stability.py
theory-lab/topwindow/results/q1_double_peel_stability_certificate.json
```

There is already a sharp separation between the two root-location branches
in (FW223).  Let

```text
S=Depth_p(K),       m=binom(a,2).
```

The supports of the return blocks
`X^(g+s)(1+...+X^(a-1))`, `s in S`, in (FW224a) are coefficientwise
disjoint.  Therefore distinct members of `S` differ by at least `a`.  Split
the `k` rooted depths into

```text
S_low   ={s in S:s<=C-g},
S_shell ={s in S:C-g<s<=C},
S_high  ={s in S:s>C}.
```

If `t=|S_low|>0`, the last of its width-`a` blocks contributes at least one
coefficient at most `C`, while each earlier block contributes all `a` of its
coefficients.  The fixed term `I_m` contributes another `m` such coefficients.
All of them are holes of `F_K` below `C`, so

```text
m+1+a(t-1)<=delta,
t<=ceil((delta-m)/a).                              (FW226a)
```

The same bound is valid when `t=0`.  The interval supporting `S_shell` has
length `g`, hence `|S_shell|<=ceil(g/a)`.  Finally, every `s in S_high` is
itself the distance from `p` to a vertex of `K` and is an outlier of `F_K`
above `C`; consequently `|S_high|<=delta`.  Adding the three classes gives
the exact shell-capacity obstruction

```text
delta+ceil((delta-m)/a)>=k-ceil(g/a).              (FW226b)
```

On the visible-root side of (FW223), `g<=Q-a`, and therefore

```text
delta+ceil((delta-m)/a)
  >=k-ceil(Q/a)+1.                                 (FW226c)
```

This is already linear.  Write `n=Q+u+2`; the q=1 balance in (FW214) gives
`u>=u_0=ceil((n-9)/5)`.  The right side of (FW226c) is nondecreasing as `u`
increases.  At `Q_0=n-u_0-2`, its three exact forms and the corresponding
minimum defects are

```text
a=1: R_1=u_0+1,
     delta>=ceil(R_1/2)=ceil((n-4)/10);

a=2: R_2=floor(Q_0/2)+u_0,
     delta>=ceil(2R_2/3);

a=3: R_3=floor(2Q_0/3)+u_0-1,
     delta>=floor(3R_3/4)+1.                       (FW226d)
```

Thus the visible-root branch has respectively
`delta>=n/10-O(1)`, `delta>=2n/5-O(1)`, and
`delta>=11n/20-O(1)`.  Equivalently, if `delta` is bounded while `n` grows,
(FW226b) forces `g>=a k-O(delta)`; (FW223) then puts the return root in the
connected threshold core rather than the visible band.

Equations (FW226a)--(FW226d) prove the **OBSERVED all-order q=1
visible-return linear-defect theorem**.  They do not exclude the visible
branch: a linear number of low holes may still be supplied by the two rooted
factors of (FW224a).  They do, however, remove visible-root returns from the
bounded-defect catalogue and isolate the threshold-core branch as its only
unbounded-order location.  Constant-memory integer replay through order
`100000`, exhaustive phase checking through order `2000`, and inherited
A/B passage for all five witnesses are frozen by

```text
theory-lab/topwindow/verify_q1_visible_return_defect.py
theory-lab/topwindow/results/q1_visible_return_defect_certificate.json
```

The same shell partition has a second consequence which is useful on the
remaining bounded-defect side.  Every block in `X^g A_a R_p(K)` lies in
`I_M`, so

```text
ecc_p(K)<=M-g-a+1.
```

The `C=binom(k,2)` internal distances of `K` are distinct positive integers,
and hence `diam(K)>=C`.  Since `diam(K)<=2 ecc_p(K)`, this gives

```text
g<=M-a+1-ceil(C/2)
 =floor(C/2)+L-a+1.                                (FW227a)
```

More importantly, consider the components of `K-p` met by the shell rooted
depths in (FW226), and let their shell-vertex counts be
`b_1,...,b_j`.  Every shell depth lies in the integer interval

```text
[C-g+1,M-g-a+1],
```

which contains at most `L-a+1` possible levels.  If two shell vertices lie
in different components of `K-p`, their LCA is `p` and their distance is the
sum of their two rooted depths.  All such cross-component pairs are globally
distinct, and their sums occupy an interval containing at most
`2(L-a)+1` integers.  Therefore, with `S=sum b_i`,

```text
P=sum_(i<j)b_i b_j<=R:=2(L-a)+1.                   (FW227b)
```

This turns bounded spectral defect into bounded topology.  Fix an integer
`Delta>=m=binom(a,2)` and assume `delta<=Delta`.  Put

```text
c_0=Delta+ceil((Delta-m)/a),
S_0=k-c_0.
```

By (FW226a), at most `c_0` rooted vertices are outside the shell, so
`S>=S_0`.  Since `Q>=4`,

```text
u<=k+a-5,
L<= (a+1)k+m+a-4,
R<=2(a+1)k+2m-7.                                  (FW227c)
```

Let `b` be the largest `b_i` and `r=S-b`.  If `b<=S/2`, then
`sum b_i^2<=S^2/2`, so `P>=S^2/4`.  Once `S_0^2>4R`, this is impossible;
hence `b>S/2`.  Now `P>=r(S-r)`.  Substitution in (FW227c) gives the following
fully explicit sufficient thresholds:

```text
a=1 and k>=2c_0+17  => r<=7;
a=2 and k>=2c_0+24  => r<=11;
a=3 and k>=2c_0+32  => r<=15.                     (FW227d)
```

For example, at the least allowed defect caps `Delta=0,1,3`, the three core
thresholds are respectively `k>=17,26,38`.  In general, let `B` be the
component of `K-p` carrying those `b` shell vertices.  Equations
(FW227b)--(FW227d) give

```text
|K-B|<=c_0+4a+3,
|T-B|<=c_0+5a+4.                                   (FW227e)
```

Inside `K`, the branch `B` has one boundary edge, to `p`.  In the original
tree it has at most one additional boundary edge, the endpoint edge at `x`
when its neighbour `r` lies in `B`.  Thus for every fixed defect cap, all
sufficiently large returns consist of one giant connected branch and an
explicitly bounded one- or two-boundary wrapper.

Equations (FW227a)--(FW227e) prove the **OBSERVED all-order q=1
bounded-defect giant-branch compression theorem**.  It is a strict topology
reduction, not yet a finite exclusion: deleting the bounded wrapper can
remove `Theta(k)` pair distances, so the giant branch has not been shown to
inherit a complete Leech interval.  Nor does this theorem classify the
wrapper weights or treat the linear-defect route.  Constant-memory replay
checks the exact envelopes through order `100000`, the fixed-defect
thresholds through `Delta=10000`, 540,634 small component partitions, and
inherited A/B passage for the five witnesses:

```text
theory-lab/topwindow/verify_q1_bounded_defect_giant_branch.py
theory-lab/topwindow/results/q1_bounded_defect_giant_branch_certificate.json
```

Taylor parity passes through the double peel and removes most of the bounded
catalogue.  Colour the vertices of `K` by the parity of their distance from
any root, and let the two class orders be `A,B`.  A pair has odd distance
exactly when its endpoints have different colours, so the number of odd
internal distances is `AB`.  Put

```text
epsilon=|O_K intersect odd|-|B_K intersect odd|,
|epsilon|<=delta.
```

The interval `1,...,C` contains `ceil(C/2)` odd values.  If
`xi=|A-B|`, (FW225c) gives

```text
AB=ceil(C/2)+epsilon,
tau(k)-xi^2=4 epsilon,

tau(k)=k    if C is even,
tau(k)=k-2  if C is odd.                           (FW228a)
```

Now write the Taylor order of the original Leech tree as `n=r^2` or
`n=r^2+2`.  Its own two parity-class orders differ by exactly `r`; moreover
the global maximum `N` is even in the square case and odd in the
square-plus-two case.  The removed set is `J union {x}`.  Relative to the cap
root, `J` has rooted depths `0,...,a-1`, the diameter endpoint `z` has depth
`a-1`, and

```text
d(cap_root,x)=N-(a-1).
```

Consequently the absolute parity imbalance of the removed set is

```text
                 a=1  a=2  a=3
n=r^2              2    1    2
n=r^2+2            0    1    0.                    (FW228b)
```

Its sign relative to the majority class may be either choice.  Subtracting
the signed removed imbalance from `r` gives the parity imbalance `xi` of
`K`.  Substitution in (FW228a), followed by minimisation over the two signs,
is exact and yields

```text
                 a=1                 a=2                 a=3
n=r^2       delta>=r-2       delta>=floor((r-2)/2)  delta>=r-2
n=r^2+2     delta>=0         delta>=floor((r-1)/2)  delta>=1.  (FW228c)
```

There is also a small but useful large-core correction to the two constant
entries in the last row.  From (FW227a) and the uniform bound in (FW227c),

```text
g<=C-a+1
```

for `k>=7,13,18` when `a=1,2,3`, respectively.  The entire width-`a` block
at root depth zero then lies below `C`, in addition to `I_m`, so

```text
delta>=binom(a,2)+a.                               (FW228d)
```

The only relevant Taylor exception is the already excluded order-18 base in
the `a=3` row.  Thus an unbounded sequence with bounded `delta` can occur only
in the two square-plus-two rows

```text
n=r^2+2, a=1: epsilon=0 and delta>=1;
n=r^2+2, a=3: epsilon=-1 and delta>=6.              (FW228e)
```

Equations (FW228a)--(FW228e) prove the **OBSERVED all-order q=1
double-peel Taylor-parity transfer theorem**, using Taylor's parity condition
as **LITERATURE** input.  This is not an exclusion of the square-root-defect
rows, nor a classification of the two surviving bounded rows.  It does cut
the fixed-defect wrapper catalogue from six Taylor/cap combinations to two.
Constant-memory replay checks every `r<=100000`, the exact root-location
cutoffs, and inherited A/B passage:

```text
theory-lab/topwindow/verify_q1_double_peel_parity.py
theory-lab/topwindow/results/q1_double_peel_parity_certificate.json
```

In fact the shell geometry closes the bounded-defect alternative altogether.
Assume the large-core range of (FW228d), and put

```text
A_0={v in K:d(p,v)<=C-g},
ell=ceil((delta-m)/a).
```

Positive edge weights make `A_0` ancestor-closed and connected.  Equation
(FW226a) gives `|A_0|<=ell`.  Remove `A_0`, and retain only the shell vertices
from (FW226).  Their number `S` satisfies

```text
S>=k-delta-ell.                                    (FW229a)
```

Every shell depth lies in

```text
[C-g+1,M-g-a+1],
```

an interval of width `L-a`.  If two shell vertices lie in the same component
of `K-A_0`, their LCA is outside `A_0`; subtracting twice its rooted depth
shows that their distance lies in `1,...,2(L-a)`.  Global uniqueness therefore
allows at most `2(L-a)` such same-component pairs in total.

If two shell vertices lie in different components of `K-A_0`, their LCA is
one of the at most `ell` vertices of `A_0`.  For each fixed LCA, all their
distances lie in one translate of an integer interval having
`2(L-a)+1` possible values.  Again using global uniqueness, the total number
of different-component pairs is at most `ell(2(L-a)+1)`.  Every pair of shell
vertices belongs to exactly one of the two classes, so (FW229a) gives the
exact obstruction

```text
binom(k-delta-ell,2)
 <=2(ell+1)(L-a)+ell,
ell=ceil((delta-binom(a,2))/a).                    (FW229b)
```

If the lower argument of the binomial is below two, (FW229b) is read with
its nonnegative part; that case already has linear `delta`.  Since
`L<=(a+1)k+binom(a,2)+a-4`, (FW229b) has the uniform exact consequences

```text
a=1: delta>=ceil((k-7)/12),
a=2: delta>=ceil((k-11)/9),
a=3: delta>=ceil((k-9)/8).                         (FW229c)
```

The slightly sharper asymptotic relaxation is obtained by putting
`x=delta/k` and `y=(a+1)x/a` in (FW229b):

```text
(1-y)^2<=4y+o(1),
delta/k>=a(3-2sqrt(2))/(a+1)-o(1).                 (FW229d)
```

Thus every q=1 return, including the threshold-core-root branch, carries a
linear number of low holes and matching high outliers.  There is no
unbounded bounded-defect catalogue left to enumerate; (FW227)--(FW228) remain
useful finite/phase refinements, but the only scalable route is now the
rooted collision/energy problem for the two factors in (FW224a).

Equations (FW229a)--(FW229d) prove the **OBSERVED all-order q=1
shell-pair quadratic linear-defect theorem**.  They do not yet force two of
those linear intrusions to collide, so G18 is not inferred.  Constant-memory
replay checks exact minimum defects through core order `100000`, every finite
phase, all residue-class quadratic tails behind (FW229c), and inherited A/B
passage:

```text
theory-lab/topwindow/verify_q1_shell_pair_quadratic.py
theory-lab/topwindow/results/q1_shell_pair_quadratic_certificate.json
```

The two rooted factors actually divide the low holes exactly, so the shell
argument can be run at both roots rather than only at `p`.  Put

```text
q=|supp(X^g A_a R_p(K)) intersect {1,...,C}|,
b=|supp(X^h R_r(H)) intersect {1,...,C}|,
t=|{v in K:d(p,v)<=C-g}|.
```

Coefficientwise disjointness in (FW224a) and (FW225c) gives

```text
delta=m+q+b,             m=binom(a,2).              (FW230a)
```

In the large-core range the root block is wholly below `C`, so `q>=a`.
The return-block starts are separated by at least `a`.  All blocks before
the last one meeting `C` are therefore complete, while the last contributes
between one and `a` coefficients.  Consequently

```text
t=ceil(q/a)=ceil((delta-m-b)/a),
b+a t<=delta.                                      (FW230b)
```

The first exact shell count is (FW229b) with the actual ball order `t`
rather than its old upper bound `ell`.  Crucially, no `delta` subtraction is
needed: every one of the `k-t` remaining p-root depths lies in

```text
[C-g+1,M-g-a+1],
```

whose width is only `L-a`, even when the rooted depth itself exceeds `C`.
The same LCA partition gives

```text
binom(k-t,2)
 <=2(t+1)(L-a)+t.                                  (FW230c)
```

There is a genuinely independent shell at the opposite root.  Let

```text
B_0={v in H:d(r,v)<=C-h};
```

this set is empty or ancestor-closed and has exactly `b` vertices.  Again
there is no outlier subtraction: all `u+1-b` remaining H-vertices lie in

```text
[C-h+1,M-h],
```

an interval of width `L-1`.  Same-component pairs use at most `2(L-1)`
values.  For each of the `b` possible LCAs in `B_0`, different-component
pairs use a translate with `2(L-1)+1` values.  Hence

```text
binom(u+1-b,2)
 <=2(b+1)(L-1)+b.                                  (FW230d)
```

The exact visible block (FW224c) extends this shell without adding a new
low vertex.  Indeed `K-H` has r-depth set

```text
[M+1-h,N-a-h].
```

Together with the non-low H vertices, all `k-b` vertices of `K-B_0` lie in
one interval

```text
[C-h+1,N-a-h]
```

of width

```text
W=N-C-a-1=(a+1)k+binom(a,2)-1.
```

Running the same LCA partition on this full r-root shell gives the stronger
u-independent inequality

```text
binom(k-b,2)<=2(b+1)W+b.                           (FW230e)
```

Equations (FW230a)--(FW230e) are exact at every large-core return.  They
also give a stronger rational asymptotic corollary.  Along any unbounded
sequence put

```text
x=delta/k,   y=b/k,   tau=u/k.
```

Here `1/5-o(1)<=tau<=1+o(1)`, by `Q<=4u+7` and `Q>=4`.  Write
`z=t/k`; then `x=y+az+o(1)` by (FW230a)--(FW230b).  If `x<=c+o(1)`, the
necessary limiting inequalities are

```text
(1-z)^2 <=4z(a+tau),
(1-y)^2<=4y(a+1),
y+az<=c.                                           (FW230f)
```

Exact real-algebra decision over `0<=y<=1`, `z>=0`, and
`1/5<=tau<=1` proves this relaxed system empty for

```text
a=1: c=1/5,
a=2: c=3/14,
a=3: c=2/9.                                       (FW230g)
```

Before rational rounding, (FW230c) and (FW230e) give the closed-form sharp
relaxation

```text
liminf delta/k
 >=(a+1)(2a+3-2sqrt((a+1)(a+2))),
```

namely `0.202041...,0.215390...,0.222912...`.  The exact integer minima of
(FW230c)--(FW230e) at `k=100000` are respectively `20204,21537,22289`,
illustrating that the rational floors leave a strict decision margin.

Equations (FW230a)--(FW230g) prove the **OBSERVED all-order q=1 exact
two-factor shell-allocation theorem** and its **OBSERVED rational asymptotic
corollary**.  This is not yet G18: the two positive-density rooted
intrusions have not been forced to share a coefficient with an internal
K-distance.  Constant-memory replay checks the exact monotonic integer
system, selected minima through core order `100000`, three QF_NRA UNSAT
instances, the frozen parent chain, and inherited A/B witness passage:

```text
theory-lab/topwindow/verify_q1_two_factor_shell_allocation.py
theory-lab/topwindow/results/q1_two_factor_shell_allocation_certificate.json
```

The two complete non-low shells also have a common geometric meaning.  Put

```text
A={v in K:d(p,v)<=C-g},          |A|=t,
B={v in H:d(r,v)<=C-h},          |B|=b,
U=K-(A union B).
```

Let `P` be the p-r path.  From the diameter decomposition through `J` and
`x`,

```text
D=d(p,r)=N-a+1-g-h.
```

Every `v in U` has

```text
d(p,v) in [C-g+1,M-g-a+1],
d(r,v) in [C-h+1,N-a-h].                           (FW231a)
```

Partition `U` into gate fibres relative to `P`: an off-path component is one
fibre, and a vertex of `P` is a singleton fibre.  If `v,w` have different
fibres and the gate of `v` precedes the gate of `w`, then the tree gate
coordinates give

```text
d(v,w)=d(p,w)+d(r,v)-D.
```

The opposite ordering gives the symmetric expression.  Thus every
different-fibre pair distance lies in the single interval

```text
[2C-N+a+1,M-a],
```

whose width and capacity are

```text
W_p+W_r,
W_p=L-a,
W_r=(a+1)k+binom(a,2)-1,
R=W_p+W_r+1.                                       (FW231b)
```

Global distance uniqueness permits at most `R` different-fibre pairs.  Let

```text
S=k-t-b,
rho(S,R)=max{r:0<=r<=S/2 and r(S-r)<=R}.
```

The actual double shell has at least `S` vertices.  If `S^2>4R`, a selected
S-set cannot have every fibre of order at most `S/2`; one genuine off-path
fibre therefore contains at least

```text
S-rho(S,R)                                         (FW231c)
```

vertices.  Moreover, within that fibre all gate-root depths of these crown
vertices lie in an interval of width at most `W_p`.  Its vertices below the
interval belong to `A union B`, so a second LCA partition gives the necessary
contextual inequality

```text
binom(S-rho(S,R),2)
 <=2(t+b+1)W_p+t+b.                                (FW231d)
```

There is a clean uniform version.  Since `delta>=b+a t>=b+t`, either

```text
delta>=ceil(k/2),
```

or `S>=ceil((k+1)/2)`.  In the latter case (FW231c) holds for all

```text
a=1,k>=60;    a=2,k>=94;    a=3,k>=126.            (FW231e)
```

The exact all-order maximum remainder caps from those thresholds are
respectively `15,21,29` (the maxima occur at `k=61,95,127`).  On the
minimum-defect boundary at `k=100000`, the much sharper actual remainders
are `5,7,9`, leaving giant crown fibres of orders `79791,85635,88847`.

Equations (FW231a)--(FW231e) prove the **OBSERVED all-order q=1 bi-root
crown giant-fibre compression theorem**.  They do not say that the giant
off-spine component is thin, that it inherits an interval spectrum, or that
it is a smaller Leech state; the collision/descent and G18 remain
**UNVERIFIED**.  Replay checks the exact remainder formula, the residue-class
quadratic tails, selected boundary rows, frozen parent hashes, and inherited
A/B witness passage:

```text
theory-lab/topwindow/verify_q1_biroot_crown_compression.py
theory-lab/topwindow/results/q1_biroot_crown_compression_certificate.json
```

The giant fibre is tree-realised, so its common depth interval can be used at
every LCA rather than only once at the gate.  Select the `s_c` shell vertices
in the FW231 giant fibre and root their minimal connecting subtree at its
gate.  Their gate depths lie in an interval of width

```text
W=L-a.
```

At a vertex `v`, group the remaining marked vertices by the child of `v`
through which they descend, treating `v` itself as a singleton group when it
is marked.  Every pair in different groups has LCA `v`.  If `v` is below the
shell, their distances lie in one translate of an interval of width `2W`; if
`v` is itself in the shell, they lie in `1,...,2W`.  Global uniqueness hence
gives the common per-LCA capacity

```text
P=2W+1.                                             (FW232a)
```

Suppose `m` marks remain.  If no child has more than `m/2` marks, the
cross-group count is at least `m^2/4`.  Thus, whenever `m^2>4P`, there is a
unique heavy child of marked order `L_m>m/2`.  If `e=m-L_m` marks are shed,
then the heavy--shed pairs alone give

```text
e L_m<=P.                                           (FW232b)
```

Skip vertices at which `e=0` and follow the heavy child until at most

```text
H=floor(sqrt(4P))
```

marks remain.  At a positive step,

```text
m^2-L_m^2=e(2L_m+e)<=3P-1,
```

because `e<L_m`.  Consequently the number `J` of positive-loss vertices on
this one path satisfies

```text
J>=ceil((s_c^2-H^2)/(3P-1)).                       (FW232c)
```

Every such vertex is a genuine branch vertex unless it is itself one of the
shell marks.  If `z_1,...,z_q` are shell marks on one root path, their
pairwise depth differences are `binom(q,2)` distinct global distances in an
interval of width `W`.  Therefore

```text
Z=floor((1+sqrt(1+8W))/2),
B_spine>=max(0,J-Z).                               (FW232d)
```

This is a linear spine theorem, not only a branch-count statement.  The
positive-loss vertices occur in order on one crown path; the distinct
positive edge weights between them also force weighted span at least
`binom(J,2)`.

In the low-defect half of FW231, the all-order remainder caps `15,21,29`
give `s_c>=ceil((k+1)/2)-O(1)`, while
`W<=(a+1)k+binom(a,2)-4`.  Hence (FW232c)--(FW232d) give

```text
a=1: B_spine>=k/48-O(sqrt(k)),
a=2: B_spine>=k/72-O(sqrt(k)),
a=3: B_spine>=k/96-O(sqrt(k)).                     (FW232e)
```

On the sharper FW230 minimum-defect boundary at `k=100000`, the exact branch
floors are respectively `4673,3298,2394`.  Equations (FW232a)--(FW232e)
prove the **OBSERVED all-order q=1 giant-crown heavy branch-spine theorem**.
They convert the crown into a rigid caterpillar-like feeder for the next
cross-level collision/moment pass.  They do not yet make a side hair an
endpoint cap, exclude the separate `delta>=ceil(k/2)` branch, or prove G18;
those conclusions remain **UNVERIFIED**.  Constant-memory replay freezes the
exact square decrements, selected rows, the uniform envelope through core
order `100000`, parent hashes, and inherited A/B witness passage:

```text
theory-lab/topwindow/verify_q1_crown_heavy_spine.py
theory-lab/topwindow/results/q1_crown_heavy_spine_certificate.json
```

The paired hole/outlier count also localises the other side of the FW231
dichotomy.  Let

```text
D_K=diam(K),       q_K=D_K-C-1.
```

Every one of the `delta` outlier pairs has distance at least `C+1`, so it is
`q_K`-far in the distinct-distance tree `K`.  Since `D_K<=C+L`,

```text
0<=q_K<=L-1.
```

Apply the four-point far-pair crowding theorem to the graph of these outlier
pairs.  Its matching number and the order of a maximal-matching pole cover
satisfy

```text
nu<=floor(sqrt(2L-1)),
|P_out|<=2 floor(sqrt(2L-1)).                       (FW233a)
```

Thus some pole is incident with at least

```text
d_out=ceil(delta/(2 floor(sqrt(2L-1))))            (FW233b)
```

outlier pairs.  In the FW231 large-core range, `2(L-1)<C+1`.  The
far-neighbour common-cone theorem at this pole says that all `d_out` paths
share an initial segment of length at least

```text
D_K/2-q_K >= (C-2L+3)/2.                           (FW233c)
```

The `d_out` distinct far neighbours lie strictly beyond this segment.  It
therefore uses at most `k-d_out` edges, and one edge on the common cone has
weight at least

```text
ceil((C-2L+3)/(2(k-d_out))).                       (FW233d)
```

FW230 already gives `delta=Omega(k)` and `L=O(k)`.  Hence every return, not
only the `delta>=ceil(k/2)` branch, has an outlier pole with
`Omega(sqrt(k))` neighbours, a common cone of length `k^2/4-O(k)`, and a
located edge of weight `k/4-O(sqrt(k))`.  In the explicit high-defect half,
the exact scan through `k=100000` gives edge/`k` ratios at least
`0.2258,0.2210,0.21875` from the respective FW231 cutoffs, tending to `1/4`.

Equations (FW233a)--(FW233d) prove the **OBSERVED all-order q=1 core-outlier
pole-cone localisation theorem**.  This replaces an unstructured linear set
of spectral outliers by a quadratic common trunk and a sublinear pole set.
It does not yet identify that pole cone with the FW232 crown spine; forcing
that intersection, a collision, strict descent, and G18 remains
**UNVERIFIED**.  The verifier locks the underlying far-pair
crowding/common-cone source and certificate hashes; those two verifiers were
also replayed separately.  It then checks the exact q=1 envelopes, selected
rows, parent hashes, and inherited A/B witness passage:

```text
theory-lab/topwindow/verify_q1_outlier_pole_cone.py
theory-lab/topwindow/results/q1_outlier_pole_cone_certificate.json
```

The FW232 heavy process also supplies the missing weighted scale of the crown
spine.  Let its successive marked orders be

```text
m_i=m_(i+1)+e_i,
```

where `e_i` marks are shed at the `i`th positive-loss LCA.  Every
shed--retained pair is separated for the first time at exactly one such LCA,
so these pair families are disjoint over `i` and

```text
C_sp=sum_i e_i m_(i+1)
    =(s_c^2-m_f^2-sum_i e_i^2)/2.                 (FW234a)
```

Put again `P=2W+1` and `H=floor(sqrt(4P))`.  The heavy process stops with
`m_f<=H`.  Moreover `e_i<m_(i+1)` and `e_i m_(i+1)<=P`, so

```text
e_i^2<P,
e_i<=E=floor(sqrt(P-1)),
sum_i e_i^2<=E s_c.
```

Consequently

```text
C_sp>=ceil((s_c^2-H^2-E s_c)/2).                  (FW234b)
```

If the gate depths of the first and last positive-loss LCAs differ by
`Gamma`, every cross-level pair in (FW234a) lies in the common integer
interval obtained by translating the shell sum interval through those LCA
depths.  Its capacity is only

```text
2W+2Gamma+1.
```

Global uniqueness and (FW234b) therefore give the exact span floor

```text
Gamma>=ceil((C_sp-2W-1)/2).                       (FW234c)
```

In particular, in the FW231 low-defect branch,

```text
Gamma>=s_c^2/4-O(k^(3/2))
     >=k^2/16-O(k^(3/2)).                         (FW234d)
```

This is much stronger than merely summing distinct spine-edge weights.  On
the sharper FW230 minimum-defect boundary at `k=100000`, the exact span floors
for `a=1,2,3` are

```text
1578444539, 1815868095, 1952390823,
```

approximately `0.15784 k^2,0.18159 k^2,0.19524 k^2`.

Equations (FW234a)--(FW234d) prove the **OBSERVED all-order q=1 crown-spine
quadratic weighted-span theorem**.  Together FW233 and FW234 now give two
located quadratic objects: the outlier pole cone and the heavy crown spine.
Their relative orientation is not yet forced.  Nesting them into a smaller
contextual state, or proving that separation repeats a distance, remains
**UNVERIFIED**, as does G18.  Constant-memory replay freezes the exact
cross-level identity, conservative loss-square bound, selected rows, the
uniform envelope through `k=100000`, parent hashes and inherited A/B passage:

```text
theory-lab/topwindow/verify_q1_crown_spine_quadratic_span.py
theory-lab/topwindow/results/q1_crown_spine_quadratic_span_certificate.json
```

The relative-orientation problem has a first exact separation test.  Start
with the `s_c` selected marks in the FW231 gate fibre.  At the gate, FW232's
per-LCA capacity forces a unique heavy child in the large-order range; write
`h_c` for its marked order.  This child side is an actual one-boundary
half-tree, and its rooted depths still have width `W`.  Let `V` be the
`d_out` far neighbours of the FW233 pole.  The far-neighbour common-cone
theorem puts all of `V` in a second oriented edge side, with rooted-depth
width `q_K<=L-1`.

If these two edge sides are disjoint, every heavy-mark--`V` path passes
through the same two gates.  Its length is a fixed bridge length plus one
rooted depth from each side.  The `h_c d_out` cross pairs are globally distinct, but all
their distances lie in an integer interval of capacity at most

```text
W+q_K+1<=W+L.
```

Therefore

```text
h_c d_out<=W+L                                     (FW235a)
```

is necessary for separated placement.  When (FW235a) fails, the two
oriented edge sides cannot be disjoint.  The elementary half-tree
trichotomy leaves only containment in one direction or the opposing-overlap
orientation; this is an orientation reduction, not yet a contradiction.

The same direct-sum argument localises any transverse attachment along the
FW232 heavy process.  If `m` crown marks remain in the retained heavy side
and the pole side is wholly in another component at that split, then

```text
m d_out<=W+L,
m<=floor((W+L)/d_out).                             (FW235b)
```

Thus a wholly transverse pole branch can occur only in the terminal-small
part of the crown process.  Using only the conservative FW229 defect floors,
the FW231 low-defect mark floors, the exact FW232 gate-loss bound and the
maximum q=1 band length, exact
finite bridging plus residue/parity tails makes (FW235a) fail permanently at

```text
a=1: k>=147464,
a=2: k>=279948,
a=3: k>=524298.                                   (FW235c)
```

The respective last compatible rows are `147463,279947,524297`; the jumps
come from the exact integer pole degree.  Equations (FW235a)--(FW235c) prove
the **OBSERVED all-order q=1 crown--pole separated-side alignment theorem**.
It removes the separated/early-transverse geometry at sufficiently large
low-defect returns.  It does not resolve containment or opposing overlap,
does not apply a crown argument to the separate high-defect branch, does not
construct a smaller contextual Leech state, and does not prove G18; all of
those conclusions remain **UNVERIFIED**.  Constant-memory replay checks
951,447 finite bridge rows, the infinite residue/parity tails, exact selected
rows, parent hashes and inherited A/B witness passage:

```text
theory-lab/topwindow/verify_q1_crown_pole_alignment.py
theory-lab/topwindow/results/q1_crown_pole_alignment_certificate.json
```

The two surviving orientations already force a proper carrier.  Keep the
FW235 heavy crown side `A`, with `h=h_c` selected marks `U`, and the pole
neighbour side `B`, with `d=d_out` selected neighbours `V`; put `C_*=W+L`.
If the two oriented edge sides are nested, their containing side is proper
and contains `U union V`.

Suppose instead that they have opposing overlap.  The pole lies in
`A-B`, while the crown gate lies in `B-A`.  Put

```text
x=|U-B|,       y=|V-A|.
```

For `u in U-B` and `v in V-A`, both boundary gates lie on the `u`--`v`
route, and the exact distance identity is

```text
d(u,v)=d(crown_gate,u)+d(pole,v)-d(pole,crown_gate).
```

These `xy` distances are distinct fixed-bridge sums in an interval of
capacity at most `W+q_K+1<=C_*`.  Hence

```text
xy<=C_*.                                             (FW236a)
```

Define the balanced integer thresholds

```text
X=floor(sqrt(C_* h/d)),       Y=floor(C_*/(X+1)).
```

If `x<=X`, the pole side contains all `d` pole neighbours and at least
`h-X` crown marks.  If `x>X`, then (FW236a) gives `y<=Y`, so the crown side
contains all `h` crown marks and at least `d-Y` pole neighbours.  Since
`hd>C_*`, both retained cross-population floors are positive:

```text
B carries V and at least h-X members of U; or
A carries U and at least d-Y members of V.           (FW236b)
```

With `C_*=O(k)`, `h=Theta(k)` and `d=Omega(sqrt(k))`, (FW236b) becomes

```text
B carries all d pole neighbours and h-O(k^(3/4)) crown marks; or
A carries all h crown marks and d-O(k^(1/4)) pole neighbours. (FW236c)
```

Equations (FW236a)--(FW236c) prove the **OBSERVED q=1 aligned
proper-carrier absorption theorem** on every FW235-excluded separated row.
Thus alignment cannot be paid for by a negligible intersection: a proper
one-boundary context retains both rigid populations, asymptotically almost
all of one across the boundary.  This is still not spectral inheritance or
a repeatable strict descent.  The carrier need not realise a consecutive
internal interval, and the high-defect branch and G18 remain
**UNVERIFIED**.  Constant-memory replay freezes the exact balanced floors,
selected rows, large-order samples, parent hashes and inherited A/B passage:

```text
theory-lab/topwindow/verify_q1_aligned_carrier_absorption.py
theory-lab/topwindow/results/q1_aligned_carrier_absorption_certificate.json
```

The outlier pole can in fact be anchored at a diameter endpoint of `K`,
which is substantially stronger than the arbitrary pole cover used in
FW233.  Let `D_K=diam(K)` and `q_K=D_K-C-1`.  The outlier graph has exactly
`delta` edges, namely all pairs at distance at least `D_K-q_K=C+1`.  If it
has `s` active vertices, then

```text
binom(s,2)>=delta.                                  (FW237a)
```

Fix diameter endpoints `alpha,beta` of `K`.  Diameter domination says that
every active vertex is `q_K`-far from at least one of them.  The edge
`alpha beta` is itself an outlier, so

```text
deg_out(alpha)+deg_out(beta)>=s.
```

Consequently one fixed diameter endpoint, say `alpha`, has at least

```text
d_D=ceil(s/2),
s=min{v:binom(v,2)>=delta}                         (FW237b)
```

outlier neighbours.  All their paths share the initial segment of the fixed
`alpha`--`beta` diameter for weighted length at least

```text
D_K/2-q_K >= (C-2L+3)/2.                          (FW237c)
```

This also repairs the carrier loss completely.  A diameter endpoint of a
positive weighted tree is a leaf.  Hence the first far side at `alpha` is
exactly

```text
K-{alpha},                                         (FW237d)
```

a connected order-`k-1` proper tree containing every one of the `d_D`
selected outlier neighbours and all but at most one selected crown mark.
The carrier is therefore strict in order, not merely a large unspecified
half-tree.

In the low-defect crown branch, apply the FW235 direct-sum test after every
edge of the anchored common cone.  Its stronger endpoint degree makes every
such cone-prefix side meet the first heavy crown side permanently from

```text
a=1: k>=1448,
a=2: k>=2496,
a=3: k>=3978.                                     (FW237e)
```

The last compatible rows are `1447,2495,3977`.  Equations
(FW237a)--(FW237e) prove the **OBSERVED q=1 anchored outlier
diameter-endpoint cone theorem**.  It applies to the outlier localisation in
both defect branches; (FW237e) additionally uses the low-defect crown.  The
one-leaf carrier has globally distinct distances but has not been shown to
inherit a consecutive spectrum or another q=1 four-factor tiling.  Thus
repeatable strict descent, high-defect exclusion and G18 remain
**UNVERIFIED**.  Replay locks the fixed-diameter and common-cone metric
lemmas, 7,645 exact bridge rows, all-order parity tails, the parent chain and
inherited A/B passage:

```text
theory-lab/topwindow/verify_q1_anchored_outlier_diameter_cone.py
theory-lab/topwindow/results/q1_anchored_outlier_diameter_cone_certificate.json
```

The anchored endpoint can be peeled repeatedly while keeping the old
perfect-core threshold `C=binom(k,2)` fixed.  Let `S` be the current
connected induced subtree of `K`, and let `theta` be the number of its pair
distances greater than `C`.  If `theta>0`, the same fixed-diameter argument
inside `S` gives a diameter leaf incident with at least

```text
d(theta)=ceil(s(theta)/2),
s(theta)=min{s:binom(s,2)>=theta}                  (FW238a)
```

old-`C` outlier pairs.  Delete that leaf.  The remaining induced tree is
connected, all of its distances remain globally distinct, and its outlier
count is at most `theta-d(theta)`.

Since `d(theta)>sqrt(theta/2)`, the integer potential

```text
P(theta)=ceil(2 sqrt(2 theta))
```

drops by at least one at each deletion.  Starting from the FW225 defect
`delta`, after at most

```text
t<=ceil(2 sqrt(2 delta))                           (FW238b)
```

successive current-diameter leaf peels, one obtains a connected induced
subtree `K_0` with no distance above the old `C`.  If `t` is the actual
number deleted, then

```text
|K_0|=k-t,
Spec(K_0) subset {1,...,C},
|{1,...,C}-Spec(K_0)|
  =C-binom(k-t,2)
  =t k-binom(t+1,2).                              (FW238c)
```

There is also exact provenance, not only a count.  If the `i`th deleted leaf
has incident weight `w_i` and remaining-tree root `r_i`, then telescoping the
endpoint decomposition gives the coefficientwise-disjoint identity

```text
F_K=F_(K_0)+sum_i X^(w_i) R_(r_i)(K_i-{alpha_i}). (FW238d)
```

All original `delta` outlier coefficients occur in these nested endpoint
rooted factors.  Because `delta<=L=O(k)`, (FW238b) deletes only
`O(sqrt(k))` vertices.  Thus `K_0` has order `k-O(sqrt(k))`; in the
low-defect crown branch it retains `h-O(sqrt(k))` selected crown marks.

Equations (FW238a)--(FW238d) prove the **OBSERVED q=1 old-threshold
outlier endpoint-peeling theorem**.  This is the first near-full connected
strict peel with an exact multi-root factor partition.  Its remaining hole
set has size `O(k^(3/2))`, however, and is not a complete smaller interval.
Closure under a rescaled threshold, high-defect exclusion and G18 therefore
remain **UNVERIFIED**.  Constant-memory replay checks the potential through
one million outliers, selected rows, worst-band samples, parent hashes and
inherited A/B passage:

```text
theory-lab/topwindow/verify_q1_outlier_endpoint_peeling.py
theory-lab/topwindow/results/q1_outlier_endpoint_peeling_certificate.json
```

There is a sharper way to renormalise the first peel without allowing the
whole `O(k^(3/2))` old-threshold hole set to accumulate.  Keep the FW237
anchored diameter endpoint `alpha`, delete only that leaf, and put

```text
K'=K-{alpha},       C'=binom(k-1,2).
```

Let `b_0` be the number of old `K`-holes in `[1,C']`, and let `r_0` be the
number of `alpha`--`K'` distances in `[1,C']`.  The pairs of `K` below `C'`
split disjointly into internal `K'` pairs and these `r_0` endpoint pairs.
Consequently the defect of `K'` at its own perfect threshold is exactly

```text
eta=b_0+r_0.                                         (FW239a)
```

Hence either

```text
eta>=ceil(k/2),
```

or at least `floor(k/2)` vertices of `K'` have `alpha`-depth greater than
`C'`.  Their depths all lie in

```text
[C'+1,diam(K)],
```

an interval of width at most

```text
W_1=k+L-2.                                           (FW239b)
```

Run the FW232 heavy-child process on these shell marks, rooted from
`alpha`.  Every fixed-LCA cross family has capacity

```text
P_1=2W_1+1.
```

The `d_D` FW237 pole neighbours are among the shell marks.  Before their
common cone branches, they all lie in one child.  If the shell-heavy child
were a different child while `m` marks remained, its order would be at least
`floor(m/2)+1`, and fixed-LCA uniqueness would require

```text
d_D(floor(m/2)+1)<=P_1.
```

Thus the shell-heavy path cannot leave the pole child above the exact mark
cap

```text
A_1=2 floor(P_1/d_D)-1.                             (FW239c)
```

Stop when the marked order reaches

```text
T_1=max(floor(sqrt(4P_1)),A_1).
```

If this happens before the pole cone branches, the FW234 cross-level
identity gives a common shell-spine span

```text
Gamma_1 >= ceil((C_sp-2W_1-1)/2),
C_sp >= ceil((s^2-T_1^2-floor(sqrt(P_1-1))s)/2).
```

If instead the pole cone branches first, the two paths have already shared
the FW237 cone length.  Therefore, on the low-`eta` branch, the pole cone
and the normalised shell crown share a path of weighted length at least

```text
min( ceil((C-2L+3)/2), Gamma_1 )
 = k^2/16-O(k^(3/2)).                               (FW239d)
```

Equations (FW239a)--(FW239d) prove the **OBSERVED q=1 one-leaf normalised
shell/pole dichotomy**.  It is important that this statement does not assume
the original low-defect crown: it also routes the former high-defect branch.
After one strict leaf deletion, either the new core already has linear
defect at its own threshold, or the outlier pole and a new half-order shell
crown share a located quadratic path.  This is not yet a collision or a
closed recurrence; the linear-new-defect branch and G18 remain
**UNVERIFIED**.  Constant-memory replay checks the exact defect identity,
the integer heavy/pole threshold, selected rows, a conservative exact FW229
envelope, parent hashes and inherited A/B passage:

```text
theory-lab/topwindow/verify_q1_one_leaf_normalized_shell.py
theory-lab/topwindow/results/q1_one_leaf_normalized_shell_certificate.json
```

The same one-leaf step preserves an exact prefix factorisation, not just the
count (FW239a).  Decompose

```text
F_K=F_(K')+X^w R_(r_alpha)(K'),
```

where `w` is the deleted leaf weight and `r_alpha` its neighbour.  Substitute
this into (FW224a) and restrict coefficientwise to `[1,C']`.  Since the full
FW224 supports were disjoint, their restrictions remain disjoint and give

```text
I_(C') = F_(K')
 + [ I_binom(a,2)
     +X^g A_a R_p(K)
     +X^h R_r(H)
     +X^w R_(r_alpha)(K') ] restricted to [1,C'].  (FW240a)
```

Write `q'`, `b'`, and `r_0` for the restricted coefficient counts of the
three nonfixed rooted factors.  Then

```text
eta=binom(a,2)+q'+b'+r_0.                          (FW240b)
```

In the high branch `eta>=ceil(k/2)`, one supplier therefore has at least

```text
ceil((eta-binom(a,2))/3)
```

coefficients.  Each supplier comes from an ancestor-closed rooted depth
ball.  The `p`-factor contributes blocks of width at most `a`, while the
other two contribute one coefficient per vertex.  Thus its supporting ball
has order at least

```text
ceil( ceil((eta-binom(a,2))/3) / a ).              (FW240c)
```

The endpoint `alpha` can belong to either old ball, but it is a leaf;
intersecting the ball with `K'` loses at most one vertex and preserves
connectivity.  Hence the high-new-defect branch contains a connected induced
rooted supplier carrier in `K'` of order

```text
k/(6a)-O(1),
```

uniformly `k/18-O(1)` for `a<=3`.

Equations (FW240a)--(FW240c) prove the **OBSERVED q=1 normalised four-factor
prefix inheritance and supplier localisation theorem**.  This is the exact
contextual interface missing from a bare distinct-distance carrier: every
new low hole still has a named old-cap, old-core, or deleted-endpoint
provenance.  The large supplier ball has no claimed consecutive internal
spectrum, so a collision/absorption lemma and G18 remain **UNVERIFIED**.
Replay:

```text
theory-lab/topwindow/verify_q1_normalized_four_factor.py
theory-lab/topwindow/results/q1_normalized_four_factor_certificate.json
```

The deleted endpoint factor itself gives a defect-free geometric split.
Among the `k-1` pairs from `alpha` to `K'`, let

```text
B_alpha={v in K':d(alpha,v)<=C'},
S_alpha={v in K':d(alpha,v)>C'}.
```

One of these sets has order at least

```text
t_0=ceil((k-1)/2).                                 (FW241a)
```

The low set `B_alpha` is an ancestor-closed connected ball when `K'` is
rooted at the neighbour of `alpha`.  If it has order `t`, its
`binom(t,2)` internal distances are distinct positive integers.  Hence

```text
diam(B_alpha)>=binom(t,2),
ecc_root(B_alpha)>=ceil(binom(t,2)/2).             (FW241b)
```

Thus the low half contains a rooted path of weighted length
`k^2/16-O(k)`.  If instead the high half has order at least `t_0`, it is
exactly the FW239 normalised shell, and the pole-aligned heavy argument gives
a common path of weighted length `k^2/16-O(k^(3/2))`.  Therefore every
sufficiently large q=1 core, with no condition on the new defect, has after
the first anchored deletion the **OBSERVED endpoint half-ball/half-shell
normal form**:

```text
half-order rooted supplier ball with quadratic radius;
or
half-order top shell with a quadratic pole-aligned common path. (FW241c)
```

This removes the old low/high-defect split from the geometry after one leaf:
the two alternatives are now determined by the actual endpoint factor.
It is still not a collision or an inherited internal Leech interval, and
G18 remains **UNVERIFIED**.  Replay:

```text
theory-lab/topwindow/verify_q1_endpoint_half_ball_shell.py
theory-lab/topwindow/results/q1_endpoint_half_ball_shell_certificate.json
```

The q=1 visible band also admits an exact deletion ledger which retains the
external ownership lost by a naive recursive call.  Keep the notation of
(FW219): `v_j` is the unique vertex with reflected coordinate `j`,
`0<=j<Q`; `H=H_Q` is the connected set above the missing coordinate; and
`M=N-Q`.  Define the nested induced trees

```text
T_j=T[{x} union H union {v_j,...,v_(Q-1)}],  0<=j<=Q. (FW242a)
```

Thus `T_0=T` and `T_Q=T[H union {x}]`.  The parent of `v_j` has reflected
coordinate greater than `j`, so `v_j` is a leaf of `T_j` and
`T_(j+1)=T_j-v_j`.  More exactly,

```text
diam(T_j)=N-j, with unique pair {x,v_j}.             (FW242b)
```

Indeed all larger values are the unique pairs `{x,v_i}`, `i<j`, already
deleted.  If `u` is any remaining vertex other than `x`, then
`d(v_j,u)<=M`: a larger value would duplicate one of the unique pairs
`{x,v_i}`, `i<Q`.  If `e_j` is the leaf edge of `v_j`, `r_j` its parent,
and `R_r(U)` is the rooted-depth polynomial, the endpoint factor therefore
has the exact form

```text
E_j=X^(N-j)+L_j,
L_j=X^(e_j) R_(r_j)(T_(j+1)-x),
supp(L_j) subset [1,M],   |L_j|=n-j-2.               (FW242c)
```

The unique `M`-pair of `T-x` contains `v_0`, while every `x`--`H` distance
is below `M`; hence `diam(T_Q)<=M-1`.  Telescoping
`F_(T_j)=F_(T_(j+1))+E_j` and removing the `Q` top monomials gives the
coefficientwise-disjoint identity

```text
I_M = F_(T_Q)+sum_(j=0)^(Q-1) L_j
    = F_H+X^g R_p(H)+sum_(j=0)^(Q-1) L_j.             (FW242d)
```

This is the **OBSERVED q=1 nested endpoint-prefix ledger theorem**.  It
upgrades the FW219 hole bijection to a complete inherited prefix with every
coefficient assigned to the connected core, the opposite endpoint factor,
or one ordered visible-leaf factor.  Each visible component has exactly one
coordinate `j` whose parent `r_j` lies in `H`, so the component bound in
(FW219d) also supplies at least `ceil(Q^2/(5Q-6))` explicitly rooted
boundary factors.  More generally, the visible--`H` parts of all `Q`
factors are pairwise disjoint translated rooted-depth sets.

Crucially, deleting `v_0` also deletes the unique internal owner of distance
`M`.  Therefore neither `T_1` nor `H` is being declared Leech, and the old
FW209 normalisation cannot simply be restarted without carrying (FW242d).
Compressing this ordered external ledger to a bounded contextual catalogue
or a strictly smaller recursive state remains **UNVERIFIED**, as does G18.
Replay:

```text
theory-lab/topwindow/verify_q1_threshold_endpoint_ledger.py
theory-lab/topwindow/results/q1_threshold_endpoint_ledger_certificate.json
```

There is a second exact reading of the same endpoint deletion at the proper
perfect threshold.  Put

```text
m=n-1,     C=binom(m,2),     h=|H_Q|=u+1.
```

Since `n=Q+u+2`, the diameter bound of `T'=T-x` is

```text
M=N-Q=C+h.                                           (FW243a)
```

By (FW219c), `Spec(T')` is `I_M` with the `h` values
`N-y(v)`, `v in H_Q`, deleted.  Such a deleted value lies at most `C`
exactly when `y(v)>=m`.  Define

```text
A_m={v in H_Q:y(v)>=m},       delta=|A_m|.           (FW243b)
```

The set is empty or an ancestor-closed connected ball at the root `p`.
Its translated rooted depths are exactly the low holes of `T'`:

```text
{1,...,C} minus Spec(T') = {g+d(p,v):v in A_m}.      (FW243c)
```

The order-`m` tree `T'` has exactly `C` pairs and no distance above
`C+h`; hence it has exactly `delta` outliers in `{C+1,...,C+h}`.  Thus one
endpoint leaves an exact near-Leech tree whose paired low defect has a named
connected carrier, rather than an arbitrary hole set.

Taylor parity gives a further **LITERATURE-dependent OBSERVED** floor.  If
`n=r^2` or `r^2+2`, deleting `x` changes the signed colour imbalance from
`r` to `r-1` or `r+1`.  Comparing the odd distances in the near-Leech
spectrum gives

```text
n=r^2:    delta>=floor((r-1)/2),
n=r^2+2:  delta>=floor(r/2).                        (FW243d)
```

In particular `delta` cannot vanish for `n>=5`; equivalently, `T-x` cannot
be a smaller Leech tree at a Taylor-incompatible consecutive order.  This is
the **OBSERVED q=1 one-endpoint exact defect-ball theorem**.  It supplies a
connected low-hole carrier and a growing parity floor, but it does not yet
classify the paired outlier graph or exclude the high-defect alternative.
G18 remains **UNVERIFIED**.  Replay:

```text
theory-lab/topwindow/verify_q1_one_endpoint_defect_ball.py
theory-lab/topwindow/results/q1_one_endpoint_defect_ball_certificate.json
```

The complement of the defect ball is itself an exact rooted shell.  Write
`r=beta-m`.  For every vertex outside `A_m`, put

```text
t=d(p,v)-r=m-y(v).
```

The visible coordinates give every `t` in `{h+1,...,m}`.  The remaining
core vertices give a subset of `{1,...,h-1}`, while `t=h` corresponds to
the absent coordinate `Q`.  More precisely, if

```text
O={o in {1,...,h}:C+o in Spec(T')},
```

then `|O|=delta` and

```text
{t(v):v in T'-A_m}={1,...,m} minus O.              (FW244a)
```

Thus `m-delta` vertices occupy a rooted-depth band of width `m-1`.  Pairs
whose LCA is outside `A_m` lie in `1,...,2m-2`.  Pairs in different
components of `T'-A_m` have one of the `delta` ball vertices as LCA; for a
fixed LCA their distances lie in a translate containing at most `2m-1`
integers.  Global uniqueness gives

```text
binom(m-delta,2)<=2m-2+delta(2m-1).                (FW244b)
```

The exact least permitted defect is therefore

```text
delta_min(m)=ceil((6m-3-sqrt(32m^2-16m-7))/2),    (FW244c)
delta/m>=3-2sqrt(2)-o(1)=0.171572875...-o(1).
```

This supersedes the square-root parity floor asymptotically.  At the first
target orders `n=18,25,27,36,38,49,51`, it gives respectively

```text
delta>=3,4,4,6,6,8,8.
```

The LCA locations also retain quadratic geometry rather than just a count.
Write `s(a)=y(a)-m` on `A_m`.  All pairs with different outside components
and LCA in the ball have distances `t_1+t_2+2s(a)`.  If `Gamma` is the span
of the active `s(a)` values, their union has capacity at most
`2m-1+2Gamma`.  Hence

```text
Gamma>=max(0,ceil((binom(m-delta,2)-4m+3)/2)).     (FW244d)
```

Every outlier pair has its LCA in `A_m` as well: its distance is at most
twice the reflected LCA coordinate, while
`ceil((C+1)/2)>=m` for `m>=5`.  Consequently the low-hole ball, the shell
cross-pair LCAs and the top-outlier LCAs are already aligned in one proper
central carrier.  In particular, if `delta<=m/2`, (FW244d) gives a
quadratic ball spine from `m>=33` onward and a located linear-weight edge.

Equations (FW244a)--(FW244d) prove the **OBSERVED q=1 one-endpoint
shell/LCA linear-defect compression theorem**.  They eliminate bounded and
sublinear defect, but still do not collide the shell with the outlier cone
or exclude the complementary `delta>m/2` high-defect branch.  G18 remains
**UNVERIFIED**.  Replay:

```text
theory-lab/topwindow/verify_q1_one_endpoint_shell_lca.py
theory-lab/topwindow/results/q1_one_endpoint_shell_lca_certificate.json
```

The same defect-ball construction applies at both global diameter endpoints.
Keep `x,z` from (FW218), so `diam(T-z)=N-1`, and put `m=n-1`,
`C=binom(m,2)`.  If an endpoint `e` has leaf weight `w_e`, root its
complement at the neighbour of `e` and define

```text
r_e=C-w_e,
A_e={v in T-e:d(root_e,v)<=r_e},
delta_e=|A_e|.                                      (FW245a)
```

For `e=x` this is (FW243).  For `e=z`, the diameter partner `x` has rooted
offset exactly `m`, while the internal ambient maximum is `C+m-1`.
The same coefficient partition therefore says that `A_z` is exactly the
low-hole carrier, the number of high outliers is `delta_z`, and the outside
offset set is `I_m` minus those outlier offsets.  Hence (FW244) applies to
both endpoints.

There is an exact coupling which is invisible in either one-end state.  Let
`c_0` count the values in `{C+1,...,N-1}` whose unique pair uses neither
`x` nor `z`.  A top value using `z` but not `x` is an outlier of `T-x`; a
top value using `x` but not `z` is an outlier of `T-z`; a value using neither
is an outlier of both.  Consequently

```text
delta_x+delta_z=m-1+c_0,                            (FW245b)
max(delta_x,delta_z)>=ceil((m-1)/2).
```

The two low-hole value sets are disjoint, since their owners are different
global pairs.  Moreover, all `c_0` common top outliers have their LCAs in
the appropriate defect ball from each orientation.

The two balls also overlap geometrically by a fixed quadratic amount.  Let
`L` be the diameter-path distance between the neighbours of `x,z`.  Since
`w_x+L+w_z=N=C+m`,

```text
r_x+r_z-L=C-m.                                     (FW245c)
```

Thus their continuous rooted-radius intervals overlap along the middle
diameter path by exactly `C-m`.  If no middle-path vertex belongs to both
balls, a single edge spanning the overlap has

```text
w>C-m=N-2m.                                        (FW245d)
```

For every order at least five, edge-cut rigidity gives `w<=N-ab`.  Hence
`ab<2m`.  On the open middle path each side already contains an endpoint
and its neighbour; for `m>=6`, a smaller side of order at least three would
have product at least `3(m-2)>=2m`.  Therefore the no-shared-vertex branch
has exactly a **two-vertex endpoint wrapper** on one side of the spanning
edge.

Equations (FW245a)--(FW245d) prove the **OBSERVED q=1 two-endpoint defect
ownership and ball-overlap theorem**.  At every target order, either the two
linear defect carriers share a diameter-path vertex, or one end is reduced
to an explicit two-vertex wrapper across a quadratic edge.  A shared vertex
has not yet been turned into a repeated coefficient, and the two-vertex
wrapper is not yet excluded; G18 remains **UNVERIFIED**.  Replay:

```text
theory-lab/topwindow/verify_q1_two_endpoint_defect_overlap.py
theory-lab/topwindow/results/q1_two_endpoint_defect_overlap_certificate.json
```

The two-vertex wrapper in (FW245d) is already incompatible with the linear
defect theorem.  If the overlap-spanning edge cuts off `{x,p_x}`, then it is
larger than `r_x`; in `T-x` the root `p_x` has no other incident branch on
that side.  Hence

```text
A_x={p_x},       delta_x=1.                        (FW246a)
```

But (FW244c) gives `delta_x>=2` from `m=11` onward.  Thus every hypothetical
Leech tree of order at least 12 has a diameter-path vertex `c` in both
endpoint defect balls.  Its two endpoint distances satisfy

```text
m<=d(x,c)<=C,       m<=d(z,c)<=C,
d(x,c)+d(z,c)=N.                                  (FW246b)
```

For a vertex on a fixed diameter path, its eccentricity is the larger of
its distances to the two diameter endpoints.  Hence `ecc_T(c)<=C`.

This has a useful global graph consequence.  Define the top-distance graph
`G_top` on `V(T)` by

```text
uv in E(G_top) iff d(u,v)>C.                       (FW246c)
```

There are exactly `N-C=m=n-1` such values and hence exactly `n-1` edges.
Equation (FW246b) makes `c` an isolated vertex.  A forest on `n` vertices
with an isolated vertex has at most `n-2` edges, so

```text
G_top contains a cycle.                            (FW246d)
```

Equations (FW246a)--(FW246d) prove the **OBSERVED q=1 shared endpoint-ball
vertex and top-distance-cycle theorem**.  The original high-defect branch
has now been reduced to a central vertex which owns complementary low
endpoint distances and a sparse near-diameter graph which must cycle.  The
cycle may encode a tripod, an opposing double-star, or a more nested thick
centre; classifying those tree-metric cycle forms remains **UNVERIFIED**, as
does G18.  Replay:

```text
theory-lab/topwindow/verify_q1_shared_ball_top_cycle.py
theory-lab/topwindow/results/q1_shared_ball_top_cycle_certificate.json
```

The top cycle has a short exact tree-metric normal form.  Classify a
non-endpoint vertex according as each of its distances to the fixed diameter
endpoints `x,z` is at most or greater than `C`.  Let `I` be low to both, `U`
high to both, and let `c_0` count top-distance pairs avoiding both endpoints.
The two-end ownership identity (FW245a) is equivalently

```text
|I|=|U|+c_0.                                        (FW247a)
```

FW246 gives `I` a shared diameter-path vertex, so the right side is positive.
If `U` is nonempty, `x,z` and any vertex of `U` form a top-distance triangle
containing the diameter.  Otherwise choose a top pair `uv` avoiding `x,z`.
The four-point identity applied to `x,z,u,v` makes one cross matching tie
`N+d(u,v)`.  Both cross distances in that matching are greater than `C`: if
one were at most `C`, the other is at most `N`, while
`N+C<N+d(u,v)`.  These four top edges form a cycle containing `xz`.  A top
diagonal gives a top triangle; if neither diagonal is top, the cycle is an
induced top rectangle.  Writing its four cyclic distances as

```text
N, N-a, N-b, N-c,       a,b,c>0,
```

the tied matching sums give the exact relation

```text
c=a+b.                                               (FW247b)
```

In the triangle case, if its other two distances are `N-a,N-b`, its median
arms are

```text
(N-a-b)/2, (N-a+b)/2, (N+a-b)/2.                    (FW247c)
```

Since every top deficit is at most `m-1`, each arm is greater than
`(C-m)/2`; the gate is therefore genuinely quadratic, not a shallow pendant
configuration.  Equations (FW247a)--(FW247c) prove the **OBSERVED q=1
top-cycle triangle/rectangle normal-form theorem**.  It does not yet locate
the unique owners of the small distances `a,b,a+b`, classify attachments at
the one or two gates, or exclude either normal form; G18 remains
**UNVERIFIED**.  Replay:

```text
theory-lab/topwindow/verify_q1_top_cycle_normal_form.py
theory-lab/topwindow/results/q1_top_cycle_normal_form_certificate.json
```

The rectangle side of FW247 in fact carries the entire top band, not just
one four-cycle.  For a top neighbour `ell` of `x` and a top neighbour `r` of
`z`, put

```text
A(ell)=N-d(x,ell),       B(r)=N-d(z,r).             (FW248a)
```

Both coordinates lie in `{0,...,m-1}`.  A vertex top-adjacent to both
endpoints is already the FW247 triangle branch.  Otherwise the two neighbour
sets `L,R` are disjoint.  The third matching in the four-point identity is
then at most `2C`, and exact comparison gives

```text
ell r is top  iff  A(ell)+B(r)<m,
d(ell,r)=N-A(ell)-B(r).                            (FW248b)
```

Conversely every top pair must join `L` to `R`, since the matching which ties
`N+d(u,v)>N+C` has both of its terms greater than `C`.  The `m` unique top
values therefore give the complete truncated direct sum

```text
#{(a,b) in A x B:a+b=j}=1       (0<=j<m).           (FW248c)
```

The top graph is one connected Ferrers sum component on `L union R`, plus
isolated vertices.  Since it has `m=n-1` edges, its cycle rank is exactly the
number of isolates.  In the q=1 orientation the first factor contains
`0,...,Q-1` and omits `Q`.  Coefficient uniqueness in (FW248c) consequently
forces

```text
min(B minus {0})=Q,                                  (FW248d)
```

and the usual coefficient scan gives the exact alternating mixed-radix
prefix recursion.  Equations (FW248a)--(FW248d) prove the **OBSERVED q=1
triangle-or-exact-Ferrers-factor theorem**.  This is stronger than locating a
single rectangle, but does not yet classify which abstract prefix factors
are realised by the two rooted tree sides or exclude either branch; G18 is
still **UNVERIFIED**.  Replay:

```text
theory-lab/topwindow/verify_q1_top_ferrers_factor.py
theory-lab/topwindow/results/q1_top_ferrers_factor_certificate.json
```

The FW244 shell count can be sharpened without choosing a topology.  For a
raw sum `s`, let `R_m(s)` be the number of representations of `s` by two
distinct elements of `{1,...,m}`.  Removing the `delta` outlier offsets
destroys at most `delta` such representations.  Among the survivors, at most
`delta` pairs with that raw sum can join different outside components: two
with the same ball LCA would have the same actual distance.  Hence at least

```text
max(R_m(s)-2delta,0)
```

pairs of raw sum `s` stay in one outside component.  Their actual distances
are globally distinct and lie in `{1,...,2m-2}`.  The interval sum layers
have the exact capped total

```text
sum_s min(R_m(s),d)=d(2m-2d-1),     d<=floor(m/2). (FW249a)
```

Taking `d=2delta`, when `4delta<m`, gives

```text
binom(m,2)-2delta(2m-4delta-1)<=2m-2,              (FW249b)
(m-4delta)^2-(m-4delta)-4m+4<=0.
```

Therefore every endpoint defect ball obeys the stronger exact floor

```text
delta>=ceil((2m-1-sqrt(16m-15))/8)
     =m/4-sqrt(m)/2+O(1).                          (FW249c)
```

Equations (FW249a)--(FW249c) prove the **OBSERVED q=1 popular-shell-sum
quarter-defect theorem**.  It makes both endpoint balls asymptotically
quarter-order rather than merely `0.1715...m`, but it does not classify their
intersection or exclude either FW248 branch; G18 remains **UNVERIFIED**.
Replay:

```text
theory-lab/topwindow/verify_q1_shell_popular_sums.py
theory-lab/topwindow/results/q1_shell_popular_sums_certificate.json
```

The first positive Ferrers digit also locates a long initial visible band at
one tree gate.  Let `v_j` be the x-side vertex with deficit `j`, let `r_Q` be
the z-side vertex with deficit `Q`, and put

```text
s=min(Q,m-Q).
```

The shared isolate from FW246 rules out `Q=m-1`, so `s>=2`.  Exactly for
`0<=j<s`, the sums `Q+j` remain inside the top prefix, and FW248 gives

```text
d(x,v_j)=N-j,       d(r_Q,v_j)=N-Q-j       (0<=j<s). (FW250a)
```

Their difference is the constant `Q`.  In a tree, the difference of
distances to two fixed vertices depends only on the projection to their
joining path.  Hence these `s` vertices have the same projection `g` on the path
`x--r_Q`.  If `D=d(x,r_Q)` and
`Z=N-(D+Q)/2`, the exact arms are

```text
d(x,g)=(D+Q)/2,       d(g,r_Q)=(D-Q)/2,
d(g,v_j)=Z-j                (0<=j<s).              (FW250b)
```

The nontriangle hypothesis gives `D<=C=N-m`, and therefore

```text
Z>=(N+m-Q)/2.                                      (FW250c)
```

Thus the factor is realised by a single quadratic gate carrying `s`
consecutive crown radii.  Crown pairs are not top.  Rooting their union at
`g` and applying the LCA distance formula to the worst pair gives a common
initial trunk of length at least

```text
ceil((2m-Q-2s+3)/2)
  >=ceil((ceil(m/2)+3)/2).                         (FW250d)
```

Equations (FW250a)--(FW250d) prove the **OBSERVED q=1 Ferrers first-digit
common-consecutive-crown theorem**.  The nontriangle branch is no longer an
abstract digit tiling: it has one located quadratic gate and an unconditional
linear common trunk.  Classifying the crown branching and
later digits or forcing a collision remains **UNVERIFIED**, as does G18.
Replay:

```text
theory-lab/topwindow/verify_q1_ferrers_common_gate.py
theory-lab/topwindow/results/q1_ferrers_common_gate_certificate.json
```

The defect ball lies inside the q=1 threshold core.  Since that core has
order `u+1=m-Q`, (FW249c) immediately improves the global first-hole
envelope to

```text
m-Q>=delta_min(m)=ceil((2m-1-sqrt(16m-15))/8),      (FW251a)
Q<=m-delta_min(m)=3m/4+sqrt(m)/2+O(1).
```

In the conditional Ferrers branch the exact trunk numerator, before division
by two, is

```text
(C-D)+(2m-Q-2s+3),       s=min(Q,m-Q).             (FW251b)
```

Here `C-D>=0` and the second term is always at least `ceil(m/2)+3`.
Moreover (FW251a) gives

```text
s=min(Q,m-Q)>=min(Q,delta_min(m)).                 (FW251c)
```

Equations (FW251a)--(FW251c) prove the **OBSERVED q=1 quarter-dense-core and
uniform-Ferrers-crown-trunk theorem**.  The apparent no-trunk branch was an
overextension beyond the exact prefix `Q+j<m`; with the corrected crown size
it disappears.  Turning the linear trunk into a collision or contextual
handoff remains **UNVERIFIED**, as does G18.
Replay:

```text
theory-lab/topwindow/verify_q1_core_density_trunk_window.py
theory-lab/topwindow/results/q1_core_density_trunk_window_certificate.json
```

The first genuine branch below the common crown trunk is almost one-sided.
Let `h` be the common LCA of the `s` crown marks and partition their indices
`I_s={0,...,s-1}` by the child branch of `h` which contains them (with a
singleton part if `h` itself is marked).  If indices `i,j` lie in different
parts, their distance is

```text
2H-i-j,
```

where `H` is the largest crown depth below `h`.  Thus all cross-part sums
`i+j` are distinct, and there are at most `2s-3` of them.  For `s>=7`, the
convex extremum for a partition with no part of order `s-2` is
`3(s-3)>2s-3`.  Hence one child part contains at least `s-2` marks:

```text
max part order >=s-2.                              (FW252a)
```

If two indices `a<b` lie outside that giant part, uniqueness also requires
`b-a` to be absent from the difference set of `I_s minus {a,b}`.  For
`s>=7` this happens only for the endpoint pair `{0,s-1}`.  Consequently the
crown cross sums at the first split have one of the exact forms

```text
one outside a:       [a,a+s-1] minus {2a};
outside 0,s-1:       [1,2s-3] minus at most {s-1}. (FW252b)
```

The last hole is filled as well when the two endpoints lie in different
parts.  Equations (FW252a)--(FW252b) prove the **OBSERVED q=1 Ferrers-crown
first-split giant-carrier theorem**.  It gives a proper child retaining all
but at most two crown marks and a linear cross interval with at most one
hole.  Unmarked vertices may still occur on both sides, so the global owner
of that hole and a closed contextual recurrence remain **UNVERIFIED**, as
does G18.  Replay:

```text
theory-lab/topwindow/verify_q1_ferrers_first_split.py
theory-lab/topwindow/results/q1_ferrers_first_split_certificate.json
```

The top-triangle alternative has an equally exact shared-ball location.  For
a vertex `u` top-adjacent to both diameter endpoints, write

```text
d(x,u)=N-a,       d(z,u)=N-b,       1<=a,b<m.
```

The two endpoint pairs are distinct, so `a!=b`.  If `g` is the median gate
of `x,z,u`, and `X,Z,R` are its arms toward `x,z,u`, respectively, then

```text
X=(N+b-a)/2,       Z=(N+a-b)/2,       R=(N-a-b)/2. (FW253a)
```

For `m>=5`, both `X,Z<=C`; hence `g` belongs to both endpoint defect balls.
The diameter arms are at least `(N-m+2)/2` and the off-diameter arm at least
`(N-2m+2)/2`.  Vertices with the same gate have fixed difference `b-a` and
distinct radii in the intersection

```text
[X-(m-1),X-1] intersect [Z-(m-1),Z-1].             (FW253b)
```

Thus one gate carries at most `m-1-|a-b|` such radii, all quadratic and in a
linear-width pole fibre.  Equations (FW253a)--(FW253b) prove the **OBSERVED
q=1 shared-ball triangle-gate/pole-fibre theorem**.  It locates the triangle
branch but does not yet bound the number of gates or classify branching
inside one fibre.

There is also a useful exact large-order routing consequence.  FW249 first
has `delta_min(m)>=7` at `m=37`.  Therefore

```text
n>=38 and Ferrers branch
  => Q<=6, or s=min(Q,m-Q)>=7 and FW252 applies.    (FW253c)
```

The small-`Q` Ferrers core, the FW252 giant carrier and the triangle fibres
all remain **UNVERIFIED** as exclusions; so does G18.  Replay:

```text
theory-lab/topwindow/verify_q1_triangle_gate_and_large_ferrers.py
theory-lab/topwindow/results/q1_triangle_gate_and_large_ferrers_certificate.json
```

The remaining `Q<=6` Ferrers interface is genuinely finite at its first
branch.  For `m>=12` its crown has order `s=Q`.  Exhausting the cross-sum
injective partitions of `I_Q` gives respectively

```text
Q:                         2  3  4  5  6
first-LCA partition rows:  1  4  7  7  8,           (FW254a)
```

or 27 rows total.  The same state contains the connected threshold core `H`
of order `h=m-Q`.  Its diameter is at most `N-Q`, so relative to its own
perfect threshold it has only the explicit linear excess

```text
E_Q(m)=(N-Q)-binom(m-Q,2)
      =m(Q+1)-Q(Q+3)/2 <=7m-27.                    (FW254b)
```

The common crown trunk is simultaneously very long:

```text
trunk>=ceil((2m-3Q+3)/2)>=m-7.                    (FW254c)
```

Equations (FW254a)--(FW254c) prove the **OBSERVED q=1 large-order small-Q
27-row crown-interface theorem**.  The formerly open `Q<=6` label now means a
fixed finite crown pattern on an order-`m-O(1)`, linear-excess near-Leech core
with an `m-O(1)` common trunk.  The unmarked core attachments in those 27
rows are not yet classified, so this is not an exclusion or G18.  Replay:

```text
theory-lab/topwindow/verify_q1_small_q_catalogue.py
theory-lab/topwindow/results/q1_small_q_catalogue_certificate.json
```

In the `s>=7` giant-carrier branch, the first crown LCA `h` has an exact
radial shell.  If the largest crown h-depth is `H`, its marked depths are

```text
H,H-1,...,H-s+1.                                  (FW255a)
```

Root distances from the fixed vertex `h` are globally unique, so these are
the unique vertices of `T` at those radii.  Now let `w` lie in an h-child
containing no crown mark and put `t=H-d(h,w)`.  The diameter path `x--v_0`
passes through `h`, so `d(h,w)>H` would give `d(x,w)>N`; hence `t>=0`.
Pairs from `w` to the crown have transformed sums `t+I_s`, which must be
disjoint from the FW252 crown-cross window.  Exact interval comparison gives

```text
one outside mark a:   t>=min(s+a,2s-2);
outside endpoints:    t>=2s-2.                    (FW255b)
```

Equations (FW255a)--(FW255b) prove the **OBSERVED q=1 crown-owned-radial-shell
and crown-free-attachment-gap theorem**.  The outer `s`-shell contains only
the crown, and any entirely new child is pushed through another linear gap.
Unmarked vertices may still lie inside the two marked sides, so the one-hole
owner and closed recurrence remain **UNVERIFIED**, as does G18.  Replay:

```text
theory-lab/topwindow/verify_q1_crown_shell_attachment_gap.py
theory-lab/topwindow/results/q1_crown_shell_attachment_gap_certificate.json
```

The attachment gap is bidirectional once the parent side of `h` is included.
For any vertex in an incident direction of `h` containing no crown mark, keep
the integer shift `t=H-d(h,w)`, now of either sign.  Its full translate
`t+I_s` must avoid the FW252 cross window.  Exact interval avoidance gives

```text
one outside a:   t<=max(a,1)-s  or  t>=min(s+a,2s-2);
endpoint pair:   t<=1-s         or  t>=2s-2.       (FW256a)
```

If an h-cross pair involving the unmarked tails owns the sole missing crown
coefficient, its two shifts must satisfy

```text
t_left+t_right=2a       or       t_left+t_right=s-1, (FW256b)
```

respectively.  Thus the remaining cross ownership is not diffuse: it is an
explicit balance between the negative parent tail and the positive descendant
tail (apart from the named marked-side candidates).  Equations
(FW256a)--(FW256b) prove the **OBSERVED q=1 crown opposing-tail hole-owner
location theorem**.  The balance itself and unmarked vertices inside marked
directions remain **UNVERIFIED**, so this is not yet a recurrence or G18.
Replay:

```text
theory-lab/topwindow/verify_q1_crown_opposing_tails.py
theory-lab/topwindow/results/q1_crown_opposing_tails_certificate.json
```

The opposing balance itself forces a located heavy gateway.  Suppose the
missing coefficient is owned by two unmarked vertices in different incident
directions at `h`.  Every unmarked descendant-side vertex has shift at least
`s`: its `h`-depth is at most `H` by the diameter `x--v_0`, while FW255 says
that the whole shift interval `0,...,s-1` is already owned by the crown.
There is only one parent direction.  Since the missing coefficient is at
most `2s-2`, exactly one owner therefore has negative shift in the parent
direction and the other has positive shift in a descendant direction.  The
positive direction need not be crown-free.  Its nonnegative `h`-depth gives
`H>=t_+`.

This gateway can be fixed on the original diameter.  Write `v_0=z`.  For the
negative owner `w_-`, `d(h,w_-)>H=d(h,z)`, so
`d(w_-,z)>2H` and hence `2H<N`.  The reflected shift of `x` is therefore
`2H-N<0`, and (FW256a) places it in the negative tail.  Along the fixed
diameter segment `x--h`, reflected shift increases monotonically; every
proper path vertex remains in the crown-free parent direction and obeys
(FW256a), while the terminal shift `H` reaches at least the positive tail.
One edge on this segment must therefore cross the entire forbidden shift
window.  Its weight obeys

```text
one outside a:
  w >= min(s+a,2s-2)-(max(a,1)-s) >= 2s-1;

outside endpoints:
  w >= (2s-2)-(1-s) = 3s-3.                       (FW257a)
```

Thus an unmarked opposing-tail hole owner is no longer only an arithmetic
possibility: it forces a specific edge on the fixed `x--h` diameter segment
with linear weight.  Deleting the edge separates `x` from `h` and every crown
mark.  Equation (FW257a) proves the **OBSERVED q=1 crown opposing-owner
fixed-diameter heavy-gateway theorem**.  Turning this gateway cut into a
collision or a strictly smaller contextual state, and controlling unmarked
vertices inside the marked directions, remain **UNVERIFIED**; this is not an
order exclusion or G18.  Replay:

```text
theory-lab/topwindow/verify_q1_crown_opposing_gateway.py
theory-lab/topwindow/results/q1_crown_opposing_gateway_certificate.json
```

The radial shell also makes the owner scope exhaustive.  First, the crown
LCA `h` cannot itself be a crown mark.  Otherwise it is necessarily
`v_(s-1)` and `H=s-1`.  FW252 puts both `v_(s-2)` and `v_(s-3)` in the giant
child.  Its entry edge has positive weight at most one, so its child endpoint
is the unique radius-one vertex `v_(s-2)`; the next mark `v_(s-3)` is one
unit farther down the same child.  The two distinct pairs
`{h,v_(s-2)}` and `{v_(s-2),v_(s-3)}` would both have distance one.  Hence

```text
H>=s.                                                (FW258a)
```

Every unmarked descendant-side vertex now has shift at least `s`, while an
unmarked parent-side vertex has shift outside `I_s`.  There is one further
global exclusion.  For a descendant-side vertex `w`, the path `x--w` passes
through `h`, so its shift is exactly

```text
t=H-d(h,w)=N-d(x,w).
```

It is therefore an FW219 reflected coordinate, and coordinate `Q` is absent.
Thus every positive descendant owner has `t_+!=Q`; similarly the rooted
vertex `h` has coordinate `H` and hence `H!=Q`.  Consider the positive
distance belonging to the one missing crown coefficient.  If its owner is
an `h`-cross pair of two unmarked vertices, two descendant shifts would sum
to at least `2s`, larger than either possible missing coefficient.  Thus one
owner is negative in the parent direction and the other is positive in an
arbitrary descendant direction.  The latter may lie inside a marked child;
FW257 still gives the fixed `x--h` gateway.  The same proof covers an owner
`{h,w}`: its parent endpoint has shift `t=m-H<0`, and the terminal shift `H`
replaces the positive descendant shift.

For a mixed crown--unmarked `h`-cross owner, collision with the already
occupied crown window leaves only

```text
one-outside a=0:     (t,i)=(1-s,s-1);
one-outside a=s-1:   (t,i)=(2s-2,0), if Q!=2s-2,   (FW258b)
```

and no endpoint-hole row.  The first line has the same fixed-diameter
gateway, because `H>=s`.  When the second line is present, the outside-mark
block and the new translate give the exact absorption

```text
[s-1,2s-3] union [2s-2,3s-4]=[s-1,3s-4].          (FW258c)
```

If an owner lies inside one incident direction, two unmarked descendant
shifts already exceed the hole.  Pairing an unmarked vertex with the sole
outside mark also overshoots it, and the analogous endpoint-side pairs do as
well.  Therefore every descendant-internal owner lies in the giant marked
child and includes a crown mark; the only other internal location is the
parent carrier.  The rooted pair `{h,v_i}` is possible only in a one-outside
row, where `H+i=2a`, `H!=Q`, and `i` belongs to the giant.  If the two outside
crown endpoints are in different parts, their own pair fills the possible
endpoint hole and all cross coefficients are exactly `[1,2s-3]`.

Finally, every opposing unmarked owner has one of the exact forms

```text
a=0:             (-s-k, s+k);
1<=a<=s-2:       (a-s-k, a+s+k);
a=s-1:           (-1-k, 2s-1+k);
endpoint row:    (1-s-k, 2s-2+k),

k>=0, and in every row t_+(k)!=Q.                  (FW258d)
```

The negative crown translate, the crown cross window plus its owner, and the
positive crown translate form one consecutive raw-coefficient block when
`k=0` is coordinate-admissible.  When an admissible `k>0`, their complement
inside the same span consists of exactly two intervals of order `k`.  Because
`t_+(k)` is affine of slope one, the new condition deletes at most one `k`
from each opposing row.  The forbidden value, when nonnegative, is respectively
`Q-s`, `Q-a-s`, `Q-(2s-1)`, and `Q-(2s-2)` in the four displayed rows.  This
does not change either block formula.  Equations (FW258a)--(FW258d) prove the
**OBSERVED q=1 complete first-crown hole-owner interface theorem**.  They do
not locate the owners of those two new intervals or give the internal
carriers an inherited spectrum.  Replay:

```text
theory-lab/topwindow/verify_q1_crown_hole_owner_interface.py
theory-lab/topwindow/results/q1_crown_hole_owner_interface_certificate.json
```

There is nevertheless an exact first-layer constraint on the two slack
gaps.  Work in a coordinate-admissible opposing-owner branch of (FW258d), and
let `S` be the raw index sums at the first LCA below `h` of the giant marked
child.  In a
one-outside row that child has `s-1` marks.  Cross-sum uniqueness gives

```text
|S|>=s-2,              max(S)-min(S)<=2s-4.
```

For the sorted elements of `S`, every gap except a chosen largest one is at
least one.  Hence the largest consecutive step is at most `s`.  In the
endpoint giant the corresponding bounds are `|S|>=s-3`, range at most
`2s-8`, and step at most `s-3`.  A translate `S+2ell` cannot therefore jump
across any occupied length-`s` block of FW258.  It is disjoint from all three
such blocks by global uniqueness.  Its coefficients are positive, so it
cannot lie left of the negative block.  The whole family consequently lies
inside one `k`-gap or strictly above the positive block.

The gap line forces

```text
k>=s-2                 (one outside),
k>=s-3                 (endpoint giant).           (FW259a)
```

At an admissible equality it consumes the entire gap, and minimum cross-pair
count forces a singleton-versus-rest split.  If that equality row is forbidden
by `t_+=Q`, it is simply absent.  In the upper line, an upper bound on the
minimum cross sum gives the exact first-LCA depth floors.  If `J_hi` is the
last occupied coefficient, then

```text
ell>=ceil((J_hi+1-c_a)/2),
c_a=s        (a=0),
    s-1      (1<=a<=s-2),
    s-2      (a=s-1),                              (FW259b)

ell>=ceil((2s-1+k)/2)       (endpoint giant).       (FW259c)
```

Equations (FW259a)--(FW259c) prove the **OBSERVED q=1 crown gap-budget or
long-trunk fork** on the admissible FW258 rows.  The `t_+!=Q` restriction only
narrows its premise; the numerical bounds are unchanged.  This is the first
genuine slack consumption statement:
a giant-child split placed in a gap spends at least a linear number of its
values.  The alternative is still only a longer trunk; later LCA levels need
not retain two interval gaps, so a closed iteration and G18 remain
**UNVERIFIED**.  Replay:

```text
theory-lab/topwindow/verify_q1_crown_gap_budget_trunk.py
theory-lab/topwindow/results/q1_crown_gap_budget_trunk_certificate.json
```

The `Q=2` fallback has a separate exact interface.  For `n>=5`, let `H_2`
be the connected FW219 threshold core; it has order `k=n-3`.  The only
visible vertices are `v_0=z` and `v_1`, of reflected coordinates zero and
one.  Since the same-component pair budget is `2Q-3=1`, their visible forest
has exactly two possible forms.

If they lie in one component, it is the rooted edge
`v_0--v_1` of weight one, with `v_1` on the core side.  Let its boundary edge
be `g`, rooted at `p in H_2`, and let the opposite endpoint edge be `f`,
rooted at `r in H_2`.  Here `g,f>=2`.  The internal core pairs, the rooted
`L2` cap, its cross pairs, and the FW219 `x`-distance holes give the exact
coefficientwise identity

```text
I_(N-2)=F_(H_2)+X+X^g(1+X)R_p(H_2)+X^f R_r(H_2).  (FW260a)
```

If the two visible components are singletons, attach them to
`p_0,p_1 in H_2` by `e_0>=3,e_1>=2`, and put
`d=d(v_0,v_1)`.  Then `d` is odd and

```text
I_(N-2)=F_(H_2)+X^d+X^e0 R_p0(H_2)
                  +X^e1 R_p1(H_2)+X^f R_r(H_2).   (FW260b)
```

All displayed supports are pairwise disjoint.  Their counts are exactly
`binom(k,2)+3k+1=N-2`, so neither identity hides an unmodelled pair class.
At `X=-1` the two singleton rooted factors in (FW260b) cancel: their roots
have opposite parity relative to coordinates zero and one, while `d` is
odd.  Thus both cases give the same signed refinement.  If
`D=R_r(H_2)(-1)` and `epsilon=(-1)^f`, then

```text
(D+epsilon)^2=n        if N-2 is even,
(D+epsilon)^2=n-2      if N-2 is odd.              (FW260c)
```

This recovers, internally to the `Q=2` interface, the Taylor square orders;
it does not exclude them.  Equations (FW260a)--(FW260c) prove the
**OBSERVED q=1 exact Q=2 visible-component/core-tiling theorem**.  The
unbounded two/three-root core remains unclassified, so `Q=2` and G18 remain
**UNVERIFIED**.  The known `L4` path is the rooted-`L2` boundary control and
passes both independent checkers.  Replay:

```text
theory-lab/topwindow/verify_q1_q2_core_tiling.py
theory-lab/topwindow/results/q1_q2_core_tiling_certificate.json
```

The original endpoint singleton gives a more general bridge which does not
need the `Q>=4` coordinate-zero return construction.  Work in the universal
q=1 orientation of (FW218)--(FW219), with coordinate-zero endpoint `z`,
opposite endpoint `x`, opposite first hole `Q>=2`, threshold core `H=H_Q`,
and

```text
K=T-{x,z},              M=N-Q.
```

Let `g` be the leaf edge at `z`, rooted at its neighbour `p in K`, and let
`h` be the leaf edge at `x`, rooted at `r in H`.  The actual pairs of `T-x`
are precisely the pairs internal to `K` and the `z--K` pairs.  By (FW219c),
the missing coefficients of `Spec(T-x)` inside `1,...,M` are precisely the
`x--H` distances.  Consequently there is the coefficientwise disjoint
identity

```text
I_M=F_K+X^g R_p(K)+X^h R_r(H).                     (FW261a)
```

The vertices of `K-H` are exactly the visible vertices
`v_1,...,v_(Q-1)`, and `d(x,v_j)=N-j`.  Thus the complete opposite rooted
factor splits as

```text
X^h R_r(K)
 =X^h R_r(H)+I_[M+1,N-1],

depth_r(K-H)={M+1-h,...,N-1-h}.                    (FW261b)
```

This is exactly the four-class shape of (FW224) with the original endpoint
singleton playing the order-one cap, but (FW261a)--(FW261b) are proved
directly: they do not claim that the singleton came from FW220--FW223.  In
particular they apply to the original `Q=2,3` cases.  The cardinalities are

```text
|K|=k=n-2=(u+1)+(Q-1),
binom(k,2)+k+(u+1)=M.
```

Put `C=binom(k,2)` and

```text
B_K={1,...,C} minus Spec(K),
O_K=Spec(K) intersect {C+1,...,M}.
```

Then

```text
|B_K|=|O_K|=:delta,
L=M-C=2n-3-Q=n+u-1<=2n-5.                         (FW261c)
```

There is also an exact first shell obstruction.  Split the `k` distinct
`p`-rooted depths of `K` at `C-g` and `C`.  Those at most `C-g` make
coefficients of `X^gR_p(K)` below `C` and hence account for at most `delta`
low holes of `F_K`; the middle interval contains at most `g` integer levels;
and every depth above `C` is itself an internal `K`-distance above `C`, so
there are at most `delta` of them.  Therefore

```text
k<=2delta+g.                                        (FW261d)
```

Since the reflected coordinate of `p` is exactly `g` and coordinate `Q` is
absent, either

```text
p visible:          g<=Q-1 and delta>=ceil((u+1)/2),
p in H:             g>=Q+1.                        (FW261e)
```

Equations (FW261a)--(FW261e) prove the **OBSERVED universal q=1 direct
endpoint-singleton double-peel and linear-defect theorem**.  It removes the
scope separation between the original `Q=2,3` terminals and the later
return-core algebra: every `n>=5` Leech tree has this exact order-`n-2`
two-root state.  It does not show that another peel preserves the same
state, exclude either root-location branch, exclude an order, or prove G18;
that closure remains **UNVERIFIED**.  The `L4` path is the `Q=2` boundary
control and `L6` is the `Q=4` positive control; all five known witnesses are
inherited through both independent checkers.  Replay:

```text
theory-lab/topwindow/verify_q1_endpoint_singleton_double_peel.py
theory-lab/topwindow/results/q1_endpoint_singleton_double_peel_certificate.json
```

The two rooted factors in (FW261a) already force a uniform positive defect
density.  Below `C=binom(k,2)`, let `q` coefficients be supplied by
`X^gR_p(K)` and let `b` be supplied by `X^hR_r(H)`.  Exact disjointness gives

```text
delta=q+b.                                           (FW262a)
```

For `k>=9`, the diameter/eccentricity bound applied at `p`, together with
`L<=2k-1`, gives `g<=C`; hence `q>=1`.  Apply the ancestor-ball/LCA shell
count used in (FW229) separately to the two named suppliers.  Since
`L=k+u+1` and the complete `r`-rooted factor has its nonlow coefficients in
an interval of width at most `2k-1`, one obtains the exact necessary system

```text
binom(k-q,2)   <=2(q+1)(L-1)+q,
binom(u+1-b,2) <=2(b+1)(L-1)+b,
binom(k-b,2)   <=2(b+1)(2k-1)+b.                   (FW262b)
```

Here `Q=k-u`, so (FW219) gives

```text
ceil((k-7)/5)<=u<=k-2.                              (FW262c)
```

The first and third inequalities alone give the sharp relaxed asymptotic
conclusion.  Put `zeta=q/k`, `y=b/k`, and `tau=u/k`.  Any limiting solution
with `delta/k<10-4sqrt(6)` would satisfy

```text
y,zeta>=0,       1/5<=tau<=1,       y+zeta<10-4sqrt(6),
(1-zeta)^2<=4zeta(1+tau),
(1-y)^2<=8y,
```

but this exact-real system is infeasible.  Indeed `tau<=1` makes each of
`y,zeta` at least the smaller root `5-2sqrt(6)` of
`X^2-10X+1`.  Therefore

```text
delta/k>=10-4sqrt(6)-o(1)=0.202041...-o(1).         (FW262d)
```

Equations (FW262a)--(FW262d) prove the **OBSERVED universal q=1 direct
endpoint-singleton two-root shell theorem**.  In particular the original
`Q=2,3` states now lie in the same linear-defect regime as the later return
states; they are not separate finite terminals.  The theorem still does not
locate the `delta` low owners, collide the two factors, preserve the state
under another peel, exclude an order, or prove G18.  Those steps remain
**UNVERIFIED**.  The replay recomputes the `Q>=2` integer ranges and
worst-case widths, checks exact monotonicity and selected minima, freezes a
QF_NRA UNSAT certificate, and inherits five A/B passes:

```text
theory-lab/topwindow/verify_q1_endpoint_singleton_two_root_shell.py
theory-lab/topwindow/results/q1_endpoint_singleton_two_root_shell_certificate.json
```

The most direct hoped-for recursion from (FW261) is in fact impossible.  Let
`S` contain one or two vertices which can be peeled from `K` while leaving
`K-S` connected, retain the roots `p,r`, and suppose all contributions lost
from the three terms in (FW261a) formed one terminal interval ending at `M`.
At least one `alpha in S` is already a leaf of `K`, hence a leaf of `T`; write
`w` for its edge weight.  The order-`n-1` tree `T-alpha` still has
`binom(n-1,2)` distinct positive-integer distances.  Its diameter is at least
that value, its eccentricity from the neighbour of `alpha` is at least half
the diameter, and therefore

```text
w<=N-ceil(binomial(n-1,2)/2).                       (FW263a)
```

If `t=|S|` and `s=|S intersect H|`, exact disjointness in (FW261a) makes the
number of deleted coefficients

```text
binom(k,2)-binom(k-t,2)+t+s <= 2k+1=2n-3.          (FW263b)
```

Since `M=N-Q` and `Q<=n-2`, a terminal deleted interval would begin at least
at `N-3n+6`.  But for every `n>=14`,

```text
ceil(binomial(n-1,2)/2)>3n-6,                       (FW263c)
```

so the leaf-edge coefficient `w`, which is among the deleted internal pairs,
lies strictly below that terminal interval.  This contradiction proves the
**OBSERVED q=1 one/two-leaf terminal-annulus obstruction**.  It does not
exclude a recurrence which retains or reroots the new incident rooted factor;
in particular it is not an order exclusion or G18.  The `L6` control shows
the obstruction concretely: its three admissible deleted supports are
`{1,3,6,10}`, `{4,9,10,11}` and `{1,3,4,6,9,10,11}`, none terminal.  Replay:

```text
theory-lab/topwindow/verify_q1_two_leaf_terminal_annulus_obstruction.py
theory-lab/topwindow/results/q1_two_leaf_terminal_annulus_obstruction_certificate.json
```

There is a stronger owner-provenance obstruction in a fixed-core
singleton-boundary ledger.  Fix a true `T`-leaf `alpha in K\{p,r}`, put
`K'=K-{alpha}`, and label every external singleton block by its original
`T`-pair.  Put `C=binom(k,2)=binom(n-2,2)`.  The same leaf-radius argument
applies separately to the old endpoint edges `g,h` and the edge `w` at
`alpha`.  Since `N-C=2n-3`, for every `n>=10` it gives

```text
g,h,w <= N-ceil(binomial(n-1,2)/2) < C.            (FW264a)
```

The stipulated exact singleton-boundary prefix on the fixed order-`k-1` core
has coefficient count

```text
M'=binom(k-1,2)+(k-1)+|H'|=C+|H'|>=C,             (FW264b)
```

Here the inherited nonempty-carrier case has `M'>=C+1`.  Thus all three small
coefficients `g,h,w` remain inside the stipulated prefix.
Their globally unique owners are, respectively, the old `z` boundary pair,
the old `x` boundary pair, and the deleted core-leaf edge.  Once `x` and the
core leaf are removed, no remaining actual pair can re-own `h` or `w`.
Consequently the three boundary-singleton labels `zp,xr,alpha-a` must remain
active.  This is a statement about actual-pair labels, not three algebraic
rooted factors: `h,w` may be retained as order-one ghosts, and the argument
does not force retention of all of `X^hR_r(H')` or `X^wR_a(K')`.

Equations (FW264a)--(FW264b), together with FW263, prove the **OBSERVED q=1
one-leaf three-owner retention obstruction** in this fixed-core
singleton-boundary ledger.  Multi-vertex or fragmented cap bundling,
arbitrary nonactual translates, and a core exchange placing `x` or `alpha`
inside the next internal core are outside its scope.  It is not an order
exclusion or G18.  Replay:

```text
theory-lab/topwindow/verify_q1_one_leaf_three_owner_retention.py
theory-lab/topwindow/results/q1_one_leaf_three_owner_retention_certificate.json
```

An arbitrary trunk cut has an exact owner-expanded ledger.  Let an edge
`e=ab` of weight `w` split a positive-integer weighted tree `K` into
`A ni a` and `B ni b`.  Partitioning unordered pairs gives

```text
F_K=F_A+F_B+X^w R_a(A)R_b(B).                     (FW265a)
```

For a fixed `u in A`, all cross pairs from `u` to `B` form one named rooted
shift, so

```text
X^w R_a(A)R_b(B)
  =sum_(u in A) X^(w+d(a,u)) R_b(B).               (FW265b)
```

There are exactly `|A|` such shifts.  If all pair distances in `K` are
distinct, then `F_A`, `F_B` and the whole cross class are pairwise
support-disjoint, the named shifts inside the cross class are pairwise
support-disjoint, and hence the refined family
`{F_A,F_B} union {S_u:u in A}` is pairwise support-disjoint.  This proves the
**OBSERVED universal trunk-cut owner ledger**.  In particular, counting the
unexpanded cross product as one formal boundary factor does not by itself
control the owner-expanded context or certify a decreasing factor measure.

FW265 does not connect an arbitrary edge to the FW259 located-segment
provenance, prove `|A|>2` there, prove any named shift meets a retained prefix,
or prove target B impossible.  The missing statement is a
**UNVERIFIED prefix-locality/absorption lemma** showing that all but boundedly
many shifts avoid or are absorbed by a retained prefix, or an equivalent
bounded-cap theorem.  Replay:

```text
theory-lab/topwindow/verify_q1_trunk_cut_ledger.py
theory-lab/topwindow/results/q1_trunk_cut_ledger_certificate.json
```

There is a sharp limit to what prefix capacity alone can give.  For a named
shift `S_u=lambda_u+D_B`, put `c_u(L)=|S_u intersect I_L|`.  Because the root
depth zero belongs to `D_B`,

```text
S_u intersects I_L  iff  lambda_u<=L.               (FW265c)
```

If `supp(F_B) subset I_L`, the refined disjointness in FW265 gives

```text
sum_u c_u(L)<=L-binomial(b,2),                       (FW265d)
|{u:c_u(L)>=r}|<=floor((L-binomial(b,2))/r).         (FW265e)
```

At a proposed FW261-type receiving endpoint
`L=binomial(b,2)+b+h_B`, `0<=h_B<=b-1`, (FW265e) becomes

```text
|{u:c_u(L)>=r}|<=floor((2b-1)/r).                   (FW265f)
```

Thus at most one complete order-`b` shift lies below the endpoint, but this
bound alone does not exclude `2b-1` one-coefficient grazing shifts.  Equation
(FW265c) identifies the exact missing input as a uniform rooted-ball bound at
the selected trunk cut.  No `O(1)` consequence has been proved from the
current moment/Kruskal/LCA interface, and FW259 neither proves that bound nor
inherits the receiving `B`-prefix.  Equations (FW265c)--(FW265f) are an
**OBSERVED conditional prefix-occupancy bound**, not bounded-cap closure.

Core exchange does not bypass the problem at the same or a lower prefix.  In
the FW261 orientation let

```text
d(x,v_j)=N-j,  1<=j<Q,  M=N-Q.
```

Let `x in C`, put `E=T-C`, and assume the complete positive actual-pair term
`F_C` satisfies `supp(F_C) subset I_(M')`, where `M'=M+s`.  If `v_j in C`,
then the monomial owned by `{x,v_j}` gives

```text
j>=Q-s,
|C intersect {v_1,...,v_(Q-1)}|
    <=max(0,min(Q-1,s)).                            (FW266a)
```

For integer `0<=s<Q`, `M'<N=d(x,z)`, hence `z in E` and

```text
|E|>=Q-s.                                          (FW266b)
```

Equivalently, if `z in E`, `1<=e=|E|<Q`, the `e-1` available places in
`E-{z}` cannot contain all of `v_1,...,v_e`.  Some `v_j`, `j<=e`, remains in
`C`, so

```text
max supp(F_C)>=N-e,
M'>=N-e,  q'=N-M'<=e.                              (FW266c)
```

In particular,

```text
M'<=M=N-Q  implies  |E|>=Q.                        (FW266d)
```

Equations (FW266a)--(FW266d) prove the **OBSERVED q=1 core-exchange top-band
obstruction**.  For the canonical deleted set
`E={z,v_1,...,v_(e-1)}`, its complement `C=T-E` is the FW242 core `T_e`;
raising the endpoint to `N-e` recovers its old exact telescoping ledger rather
than a new recurrence.
FW266 does not exclude a dual-band state, bounded `Q`, `e>=Q`, an identity
without the complete `F_C` term, or signed cancellation.  Replay:

```text
theory-lab/topwindow/verify_q1_core_exchange_top_band.py
theory-lab/topwindow/results/q1_core_exchange_top_band_certificate.json
```

There is also a q-independent reason that the raised ledger cannot forget
its external owner vertices.  Let `T` be a Leech tree of order `n>=5`, and
let an edge `f` cut component orders `a,n-a`.  Strict heaviest-edge rigidity
and `a(n-a)>=n-1` give

```text
w(f)<=N-a(n-a)<=N-(n-1).                           (FW267a)
```

For an arbitrary external set `E` of order `1<=e<=n-2`, put `C=T-E`.  For
each `y in E`, any incident edge `f=yu` satisfies

```text
w(f)<=N-e-1<N-e.                                   (FW267b)
```

The coefficient `w(f)` has the unique actual-pair owner `{y,u}`.  Therefore
every external vertex occurs in the owner-label support of the ambient
near-full prefix `I_(N-e)`.  Equations (FW267a)--(FW267b) prove the
**OBSERVED near-full-prefix external-owner conservation theorem**.  It counts
active external vertices, not distinct coefficients or algebraic factors;
one external--external edge may witness two vertices.  It does not exclude a
rolling exchange, an owner-preserving merger/absorption with an explicit
strictly decreasing fully charged potential, signed cancellation, an
incomplete prefix or a dual-band recurrence.  Replay:

```text
theory-lab/topwindow/verify_q1_near_full_external_owner_conservation.py
theory-lab/topwindow/results/q1_near_full_external_owner_conservation_certificate.json
```

The last proposed escape from this boundary was to orient the position of a
single high-band hole.  Keep the ambient q=1 notation, and for `1<=b<Q` put

```text
C_b=T-{z,v_b}.
```

There are two different eligibility notions.  The condition that `v_b` is a
leaf of `T-z` is equivalent to `C_b` being connected; call it entry
eligibility.  Rolling eligibility additionally requires `v_b` not to be the
neighbour of `z`, equivalently that `v_b` is a true leaf of `T`.  FW242 only
makes `v_b` a leaf at its own nested stage, so it does not supply rolling
eligibility for every `b`.

For every entry-eligible `b`, the actual unordered pairs give the disjoint
ledger

```text
I_(N-1)=F_(C_b)+L_0+X^(N-b)_[owner {x,v_b}]+L_b,    (FW268a)
supp(L_0),supp(L_b) subset I_M,
|L_0|=n-2, |L_b|=n-3.                              (FW268b)
```

Here `L_0` contains the pairs `{z,u}`, `u` different from `z,x`, and `L_b`
contains `{v_b,u}`, `u in C_b-{x}`.  Pair counting and the FW219 top owners
therefore give

```text
Spec(C_b) intersect [M+1,N-1]
   =[M+1,N-1]-{N-b};                               (FW268c)
```

the missing owner's height above `M` is exactly `Q-b`.  This is an exact weak
two-external state, but not the FW261 state again: the retained prefix ends at
`N-1` and its rooted-factor schema is different.

Neither obvious normalization closes this state.  Define
`q_T(u)=N-diam(T-u)`.  The diameter pair remains after deleting every
nonendpoint, while the unique `N-1` pair contains `x`, so

```text
q_T(u)=0 for u not in {x,z},
q_T(z)=1,  q_T(x)=Q>=2.                            (FW268d)
```

Thus ambient FW218 normalization uniquely returns the same `(z,x,Q)` and
cannot reset the directed hole.  Nor can FW218 be applied to `C_b` as a
smaller Leech tree.  If `Q>=3`, some other `v_i` remains and
`d(x,v_i)=N-i>binomial(n-2,2)`.  If `Q=2` and `n>=7`, the leaf edge at `z`
has its unique owner outside `C_b` but lies in
`[1,binomial(n-2,2)]`, contradicting the spectrum required of an
order-`n-2` Leech tree.  Hence

```text
n>=7 and entry-eligible b  =>  C_b is not Leech.    (FW268e)
```

The `L6` witness shows that this is a real no-return obstruction rather than
a missing choice of coarse rank.  Its rolling coordinates `b=1,3` give two
actual-pair ledgers with the same core order, external order, prefix endpoint,
low internal mass and high-band length; their named holes are `N-1` and
`N-3`, and the two choices form an involution inside the fixed ambient owner
ledger.  This is a pressure control, not a certified contextual transition.
Numeric reorientation of the two
non-Leech cores has opposite deficits four and eight.  Consequently a raw
hole coordinate, its complementary height, an internal diameter or a numeric
opposite deficit cannot be required to decrease in both rolling directions.

Equations (FW268a)--(FW268e) prove the **OBSERVED q=1 directed-hole exchange
interface and normalization obstruction**.  They do not rule out a newly
defined owner-aware contextual normalizer, signed cancellation, a dual-band
state or an explicitly irreversible transition with a fully charged
potential.  They give no collision, finite terminal catalogue, order
exclusion or G18.  Replay:

```text
theory-lab/topwindow/verify_q1_directed_hole_interface.py
theory-lab/topwindow/results/q1_directed_hole_interface_certificate.json
```

FW266--FW268 now show why all three tested exits fail: keeping the old prefix
forces at least `Q` external vertices; raising to a near-full prefix preserves
every accumulated external vertex label; and moving a single named hole has
neither a new Leech core nor a no-return rank.  They do not prove that every
possible contextual exchange fails.  This is the controlled stop boundary
for the present q=1 bounded-cap/core-exchange/directed-hole route; it is not
an order exclusion or G18.  The full acceptance criteria and pressure audits
are in `docs/q1-new-mechanism-sprint.md` and
`docs/q1-directed-hole-sprint.md`.

For orientation, peeling through `floor((n-1)/16)` vertices gives the exact
finite transfer floors

```text
n:                     36  38   49   51   64   66   81   83
min next-edge forcing: 47  73  117  155  267  291  434  500
```

The constant-memory replay checks 79,104 ordered-arm identities, the exact
finite rows, the rational constants, and all known witnesses through both
checkers:

```text
theory-lab/topwindow/verify_endpoint_terminal_surplus_peeling.py
theory-lab/topwindow/results/endpoint_terminal_surplus_peeling_certificate.json
```

The finite arithmetic replay
`theory-lab/topwindow/verify_endpoint_pole_first_hole.py` checks 177 pole
parameter rows, 22,833 forced coefficients and 22,656 proposed first-hole
positions against (FW105)--(FW106).  Its frozen summary is
`theory-lab/topwindow/results/endpoint_pole_first_hole_certificate.json`.
This audit is not the all-order proof, which is the coefficient recursion
above.

Thus repeated nonsymmetric cap handoffs are now well-founded: both cap order
and attachment weight strictly decrease.  In finitely many steps they reach
an order-at-most-four rooted factor or make the strict deficit handoff
(FW92) to a complement with the endpoint pivot and deep offshoot
(FW93)--(FW94).  This proves the
previously missing decreasing measure for the inherited-cap branch and
identifies its other terminal with the existing thin/thick endpoint problem.
It does not exclude that endpoint output, nor does it show that the separate
lower-core near-`t` handoffs enter this cap recurrence.

The heavy cap in (FW87) may equal `B` and hence need not itself decrease the
receiving arm.  Equations (FW88)--(FW91) recover strict descent at the
opposite boundary, but may lose the original lower bound `R+1` on the new
boundary weight; the internal bidirectional component also need not itself
be a quotient sink.  In particular one must not claim that the *original gap
edge* `e` already cuts the cap, or that the heavy closing edge is necessarily
internal to `B`.  A
distance-injective rooted path with depths `{0,8,14,17,18}` has reflected set
`{0,1,4,10,18}` and an eight-unit gap, yet the only edge of weight at least
eight cuts off a component of diameter ten; a heavier attachment edge can
close the whole path as the cap allowed by (FW87).  That set cannot participate in
the required exact prefix of length 25: greedy coefficient forcing fails at
coefficient six with two representations.  This is an **OBSERVED negative
diagnostic**, not a counterexample to (FW73).  The calculation is audited by
`theory-lab/topwindow/verify_rooted_gap_transition.py`; its frozen output is
`theory-lab/topwindow/results/rooted_gap_transition_certificate.json`.

Therefore a pole cannot remain both vertically shallow and concentrated: it
either exposes the lower-arm quadratic incident edge (FW65)--(FW66), or hands to the proper
distance-injective lower core `C`, of linear order, whose entire internal
distance set lies below `q`.  One-step inheritance is now controlled by
(FW73)--(FW76), and the inherited-cap branch has the decreasing order/weight
measure (FW88)--(FW91).  What is not yet proved is that the separate
lower-core near-`t` handoffs enter this recurrence, or that the thick-surplus
endpoint and small-factor terminals collide.

The four possible outer orders `a=1,2,3,4` have respective minimum bracket penalties

```text
0, 1, 3, 7.
```

Indeed their maximum depths are respectively `0`, at least `1`, `2s>=2`,
and `G+s>=4`.  Since `rho(b)=b^2/4+O(b)`, dropping `I_R` in (FW62) shows that
the `mu`-arm has `b<=sqrt(2/5)n+O(1)`.  Since `a<=4`, the lower arms therefore
carry at least

```text
(1-sqrt(2/5))n-O(1)
```

vertices, approximately `0.3675n` rather than the `0.2929n` supplied by
(FW60) alone.  For the target orders `18,25,27,36,38,49,51`, the maximum
possible `b` is respectively `11,15,16,22,23,30,32`; after accounting for
the four pole orders, the lower-arm minima are respectively
`[5,4,3,2]`, `[8,7,6,5]`, `[9,8,7,6]`, `[12,11,10,9]`,
`[13,12,11,10]`, `[17,16,15,14]`, and `[17,16,15,14]`.
Thus a pole cannot escape into one giant receiving arm plus a bounded
residue: it hands to a linearly large third-and-lower arm mass.  This is a
reduction, not yet a contradiction, because that mass may be spread over many
small arms.  Identities (FW61)--(FW64) and (FW69)--(FW78) isolate the remaining task more sharply:
one of the extra-low-cross, incident-hole, and rooted-span defects is already
quadratic, and the next descent must convert each alternative into a nested
thick core or a distance collision.

Thus a singleton thick centre has only three surviving interfaces:

1. a thick third arm with (FW51) and `E_q>=3`;
2. a scale handoff `q-h<lambda`, with an internal edge at least `q-h+1` whenever
   the outer factor is nonsymmetric; or
3. a mixed-radix pole of order at most four attached directly to the centre,
   with the top-arm clustering bound (FW55).

Excluding these interfaces, and then treating a non-singleton thick sink
component, remains **UNVERIFIED**.  The audit enumerates 655,454 relaxed arm
summaries, replays the 584,442-state reflected-prefix audit and the complete
pole-factor audit, and checks the known order-six Leech tree with both witness
checkers as a positive geometric control:

```text
theory-lab/topwindow/verify_singleton_thick_centre.py
theory-lab/topwindow/results/singleton_thick_centre_certificate.json
```

## A singleton-corridor reduction

Suppose an allowed orientation has a degree-two sink `v`. Let its incident
weights be `p<q`, and let `q=w_j` be the `j`th smallest edge weight of the
whole tree. Then the following **OBSERVED dichotomy** holds:

```text
(q-p)<=10, or q <= binom(j-1,2)+2.
```

For the proof, take the handoff pair `P` that certifies the direction of the
`p`-edge toward `v`. It lies in the side consisting of `v` and the branch
beyond the `q`-edge, and has distance `d(P)=p+h`, `1<=h<=10`. If
`q-p<=10` the first alternative holds. Otherwise

```text
p+h <= p+10 < q.
```

The pair `P` cannot contain `v`, because every path from `v` into that branch
contains the edge of weight `q`; hence both endpoints of `P` lie beyond the
`q`-edge. Every edge of its nontrivial path has weight less than `q`. Thus,
immediately before weight `q` is added, the light-edge forest has a nontrivial
component beyond the `q`-edge. The component containing the already-present
`p`-edge is a second nontrivial component. The component-concentration
covering theorem with `k=j-1` light edges and at least two nontrivial
components gives

```text
q <= binom(j-1,2)+2.
```

This does not yet exclude the corridor, but it replaces the unrestricted
singleton terminal by near-tied incident weights or a strict fragmented-light-
forest bound. The remaining step is to show that a long bidirectional corridor,
near-tied central weights, or repeated fragmentation is incompatible with the
weighted excess moment.

The nonfragmented case is also rigid in global weight order. Write `p=w_i`.
The standard one-component covering ceiling gives

```text
p <= binom(i,2)+1.
```

If the fragmented alternative fails, then `q>binom(j-1,2)+2`, while the first
alternative gives `q<=p+10`. Combining the three inequalities yields

```text
binom(j-1,2)-binom(i,2) <= 8.                  (1)
```

For `j>=i+2` the left side is at least `i`. Therefore every nonfragmented
singleton satisfies the **OBSERVED rank dichotomy**

```text
i<=8, hence p<=29 and q<=39; or j=i+1.
```

Thus outside a fixed small-weight window the two central edges are consecutive
not merely numerically close but in the complete global edge-weight order.
Immediately after the isolated sink vertex is attached by `p`, the forcing
lemma must already realise every value `p+1,...,q-1` without adding another
edge. This bounded interval is the exact global-coverage condition that the
local affine core by itself was missing.

## The 20-window singleton normal form

The near-tied alternative also has a finite affine normal form. Enlarge the
definition of a supported direction to allow a pair among
`w+1,...,w+20`, contract the resulting 20-bidirectional edges, and suppose its
canonical sink component is again a single degree-two vertex with incident
weights `p<q=w_j`. Assume the fragmented-forest bound fails:

```text
q > binom(j-1,2)+2.
```

The preceding dichotomy gives `q=p+r` for some `1<=r<=10`. Choose a 10-window
handoff of the `p`-edge with offset `h` and one of the `q`-edge with offset
`k`, where `1<=h,k<=10`.

If `h<r`, the `p+h` pair lies wholly beyond the `q`-edge and below `q`, giving
the forbidden second light component. Thus `h>=r`. If `h=r`, uniqueness forces
this pair to be the `q`-edge itself. If `h>r` and the pair avoided `v`, it
would make the `q`-edge 20-bidirectional at offset `h-r`; hence it contains
`v`. In all cases its endpoint beyond the `q`-edge is at residual rooted depth

```text
t=h-r,                  0<=t<=9.
```

Likewise the `q+k` handoff cannot avoid `v`: if it did, it would make the
`p`-edge 20-bidirectional at offset `r+k<=20`. Its endpoint beyond the
`p`-edge is therefore at residual rooted depth

```text
s=r+k,                  2<=s<=20.
```

The two handoff pairs have different distances, so `t!=k`. When `t>0`, the
two residual paths lie in opposite components and are distinct global pairs,
so also `t!=s`. Hence every nonfragmented singleton 20-terminal has the finite
parameter core

```text
(r,h,k,t,s),
1<=r,h,k<=10, h>=r, t=h-r, s=r+k, t!=k,
and t=0 or t!=s.
```

There are exactly 485 such integer rows (100 with `t=0`, 385 with `t>0`).
This is not yet a finite topology catalogue because `p` remains free, but all
geometry beyond the two central weights is rooted within distance 20.

There is also a sharp local barrier. For every one of the 485 rows, set `p=21`
and realise the two residual paths by single edges of weights `s` and, when
`t>0`, `t`. The resulting four- or five-vertex two-arm tree has all pairwise
distances distinct and realises both handoff equations. The audit checks all
4,450 local pair distances and all 970 handoff equations. Consequently no
argument using only this local rooted-parent core can remove even one row. The
next target must intersect the rows with the **global** exact small-distance
forest (or the weighted excess identity), not merely another local sumset
relaxation. The enumeration, local barrier and frozen row hash are audited by
`theory-lab/topwindow/verify_corridor_normal_form.py` and
`theory-lab/topwindow/results/corridor_normal_form_certificate.json`.

## Exact small-rank forced-prefix intersection

The fixed small-weight branch `p<=29,q<=39` can be intersected with the global
forcing lemma without choosing the final order. Before rank 10 every edge
weight is at most 39, so every path weight is at most 390. The diagnostic
therefore enumerates the exact forced forests with target set `1,...,390` and
stops after ten edges. A candidate with two adjacent central edges has used a
nondisjoint edge insertion and hence at most 19 nonisolated vertices, so the
19-vertex workspace does not remove any such all-order prefix.

The enumeration visits

```text
4,537,700 prefix states through rank 10.
```

It enforces the strict failure of the fragmented ceiling and rejects any pair
already making either central edge 20-bidirectional. The 485 affine rows then
collapse to

```text
9 rows, 14 matches, 7 distinct forced forests,
gap r in {2,3}, p in {4,7,16}, q in {6,9,10,18,19}.
```

Every match has `t=0`: the small edge's handoff is exactly the larger central
edge. Moreover `p=binom(i,2)+1`, and the forest before `p` is respectively the
known order-3 tree, one of the two known order-4 trees, or the known order-6
tree. The four distinct positive cores all pass `src/checker_a.py` and
`src/checker_b.py`.

This is an **OBSERVED exact prefix reduction**, not an all-order exclusion.
The one-way test is deliberately monotone: it rejects a state if a forbidden
reverse pair already exists, but a future extension can create a new reverse
pair and thereby leave the singleton-terminal case. Thus the seven survivors
say precisely what remains: a hypothetical canonical singleton corridor must
extend one of four known Leech cores by the displayed two-edge tail, while
preserving the future one-way conditions. Production hook, diagnostic and
independent verifier:

```text
src/forest_search.cpp
theory-lab/topwindow/forest_corridor_prefix.cpp
theory-lab/topwindow/verify_corridor_prefix.py
```

Frozen certificate:
`theory-lab/topwindow/results/corridor_prefix_certificate.json`.

## Large-rank collapse to one prefix-defect core

The consecutive-rank branch has a much sharper all-order form.  Retain the
20-window canonical singleton assumptions above, suppose the fragmented bound
fails, and write

```text
p=w_i, q=w_{i+1}=p+r, C=binom(i,2), delta=C+1-p.
```

For `i>=11`, the following is an **OBSERVED reduction**:

```text
(r,delta) is one of (2,0), (3,0), (3,1).
```

Moreover, in a smallest counterexample of order at least 18, the two
zero-defect rows reduce to a smaller Leech tree and hence cannot occur.  The
only genuinely new large-rank singleton core is therefore

```text
r=3, delta=1, p=C, q=C+3.
```

Here is the proof.  The strict failure of the fragmented bound says

```text
q > C+2.
```

The usual one-component ceiling gives `p<=C+1`.  Hence `delta>=0`, while
substitution of `q=C+1-delta+r` gives

```text
delta <= r-2 <= 8.                              (2)
```

Immediately before `q`, the light forest has `i` edges.  If it had two
nontrivial components, component concentration would give `q<=C+2`, contrary
to the strict inequality.  It therefore has exactly one nontrivial component.
The sink vertex `v` is isolated before `p` (its only incident edges are `p,q`),
so `p` attaches it to a connected `i`-vertex core `K`; the far endpoint of `q`
is still isolated.

This also kills the positive right residual in the affine normal form.  If
`t>0`, its path beyond the `q`-edge has total weight `t<=9`; every edge on that
path is lighter than `p=w_i>=i>=11`, so the far endpoint of `q` would already
belong to a second nontrivial light component.  Thus

```text
t=0 and h=r.
```

By forcing, `K` contains every distance `1,...,p-1`.  It has exactly `C`
vertex pairs.  Since the `p`-edge is a one-way boundary edge of the canonical
20-terminal, its opposite side, and hence `K`, contains no distance among
`p+1,...,p+20`.  Consequently the distance set of `K` has the form

```text
{1,...,C-delta} union D,
|D|=delta, and every d in D is greater than p+20.       (3)
```

Let `u` be the endpoint of `p` in `K`.  Before `q` is inserted, all values
`p+1,...,p+r-1` must already be distances.  Equation (3) says none is internal
to `K`, so for every `1<=ell<r` there is a vertex `z_ell` of `K` with

```text
d_K(u,z_ell)=ell.
```

If `r>=4`, then `d_K(z_1,z_2)<=3<=r-1`.  The same value is already realised by
the distinct pair `(u,z_d)` with `d=d_K(z_1,z_2)`, contradicting distance
uniqueness.  Hence `r<=3`; (2) now leaves exactly the three displayed rows.
For `r=3`, uniqueness further forces `d(z_1,z_2)=3`.  Equality in the rooted
triangle inequality puts them in different branches at `u`; positive integral
weights then show that the weight-1 and weight-2 edges are both incident with
`u`.  Thus the defect-one survivor has a forced rooted `1--2` fork.  The two
other endpoints are not asserted to be leaves; only the common incidence and
the two edge weights are forced.

When `delta=0`, (3) says that `K` itself is a Leech tree of order `i`.  It is a
proper substructure (`i<=n-2`).  In a smallest hypothetical counterexample
with `n>=18`, this contradicts minimality for `i>=18`; for `11<=i<=17`, Taylor's
parity condition and the known order-11/order-16 exclusions close the remaining
possibilities.  Therefore a minimal counterexample leaves only

```text
dist(K)={1,...,C-1,D},  D>=C+21,
```

with the rooted weight-1/weight-2 fork at `u`.

There is a useful parity sieve for this last core.  If `epsilon` is the parity
of `D` and the two parity colour classes of `K` have orders `A,B`, then

```text
A B = floor(C/2)+epsilon.
```

Writing `x=|A-B|`, the necessary square condition is

```text
C even: x^2 is i or i-4;
C odd:  x^2 is i+2 or i-2.                      (4)
```

The first allowed core orders at least 11 are
`11,13,14,16,18,20,23,25,27,29,34,36`; all other orders are excluded by (4).

An exact forced-prefix computation gives a finite base beyond the analytic
reduction.  For each `i=11,12,13,14`, it enumerates every forced forest through
rank `i-1` with the safe universal distance cap

```text
M_i=(i-1)(C-1)-binom(i-1,2),
```

the maximum possible sum of `i-1` distinct edge weights below `C`.  Across
3,690,761,100 terminal prefix states and 162,845 connected `i`-vertex cores,
there are zero cores even with distance set `{1,...,C-1,D}`; the 20-gap and
rooted-fork filters are therefore not reached.  Orders 11--13 are rebuilt
locally; order 14 is a complete 16-shard level-8 run on `geo-ws` with
3,312,897,924 terminal states and 89,984 connected cores.

This finite result is **OBSERVED**, not the missing all-order theorem.  A
selective order-16 version enforces the rooted fork, the single high outlier
and the parity square condition monotonically.  Its complete 512-shard run
visits 39,381,216,516 reported nodes and finds zero connected or target cores.
The transcript is frozen and shard zero is reproduced locally with clang by
`theory-lab/topwindow/verify_prefix_defect_gap.py`.  This strengthens the
finite diagnostic; the full-window singleton argument above is what removes
the branch uniformly, so no induction is inferred from the order-16 run.
The endpoint-strip theorem supplies the next exact interface: if
`D=C+g`, both diameter pendant weights are at least `g+1`, deleting both
diameter endpoints preserves `1,...,g` and the rooted `1--2` fork, and the
three surviving pair classes partition `1,...,C-1` exactly.  This is proved
in `docs/prefix-defect-endpoint-strip.md`; it is a strict reduction but not
yet the required decreasing induction.
Diagnostic, verifier and frozen certificate:

```text
theory-lab/topwindow/forest_prefix_defect.cpp
theory-lab/topwindow/verify_prefix_defect_cores.py
theory-lab/topwindow/results/prefix_defect_core_certificate.json
theory-lab/topwindow/results/prefix_defect_order14_shards/
theory-lab/topwindow/forest_prefix_defect_gap.cpp
theory-lab/topwindow/verify_prefix_defect_gap.py
theory-lab/topwindow/results/prefix_defect_gap_order16_certificate.json
theory-lab/topwindow/results/prefix_defect_gap_order16_shards/
```

## FW269: low-owner cones, the unit-edge domino, and the pure-core-tail stop

Return to the universal FW218--FW219 q=1 orientation.  To avoid overloading
the later root names, call the neighbour of `x` by `o`; put

```text
beta=d(o,z),  y(v)=beta-d(o,v),
H={v:y(v)>Q},  y(v_i)=i (0<=i<Q).
```

The edge `xo` has weight `N-beta>=Q`, because its complementary `o--z` path
survives in `T-x`, whose diameter is `N-Q`.  Hence the actual pair owning any
`1<=d<Q` lies in `T-x`.  If `ell` is its `o`-rooted LCA, then

```text
d=2y(ell)-y(a)-y(b).                                  (FW269a)
```

Ancestor closure of `H` gives four exact cases.  For two core endpoints, the
two nonnegative descents from `ell` sum to `d`.  For `v_i` and a core endpoint,

```text
i>=Q+1-d,
Q+1<=y(b)<=y(ell)<=Q+d-1.
```

For two endpoints in one visible component, their two descents from their
visible LCA again sum to `d`.  For endpoints `v_i,v_j` in different visible
components, put

```text
A=Q-1-i,  B=Q-1-j,  C=y(ell)-(Q+1).
```

Then `A,B,C>=0`, `A!=B`, and

```text
d=4+A+B+2C.                                           (FW269a')
```

Thus this last case has `d>=5`, `i,j>=Q-d+3`, and
`y(ell)<=Q+1+floor((d-5)/2)`.  An owner path of `r` edges also obeys
`binom(r+1,2)<=d`.  These are exact cones, but the core--core and
same-visible-component cones can slide and give no absolute threshold
anchor.

There is a complementary edgewise theorem.  Let an edge `ab` of weight `w`
split any globally distance-distinct positive-integer-weighted tree into
sides `A,B`, and let `D_A,D_B` be the rooted-depth sets from `a,b`.  Injectivity
of the cross-edge sums `w+D_A+D_B`, followed by comparison with an internal
pair, gives

```text
(D_A-D_A) intersect (D_B-D_B)={0},
D_A intersect (D_A+w)=D_B intersect (D_B+w)=empty.   (FW269b)
```

Orient an edge of `T-x` away from `o`, and let `J_e` be the visible indices
on its descendant side.  Since

```text
d(a,v_j)=beta-j-d(o,a),
```

`J_e` contains no two indices differing by `w`.  For the unique unit edge,
`J_e` is an independent set in the path on `0,...,Q-1`, so

```text
|J_e|<=ceil(Q/2).                                     (FW269b')
```

This rules the unit edge out of a trunk carrying two consecutive visible
marks.  It is vacuous on a pure-`H` tail, where `J_e` is empty.

That escape survives a strengthened fixed-prefix metric pressure family.  For

```text
kappa>=1, Q>=kappa+1, L>=1,
m=Q+2+kappa L,  B>=4Q+5,  R=B^(m+2),
C_i=sum_(h=1)^i B^h,  t_a=Q+2+aL,
```

take the spine `r-s_0-...-s_m`, with weights `3R,B,...,B^m`, add `xr` of
weight `Q`, add `v_j` at `s_j` with edge weight `2R-C_j-j`, and add
`ell_a` at `s_(t_a)` with edge weight `a`.  With `z=v_0`, direct summation
gives

```text
diam(T)=5R+Q,
diam(T-z)=5R+Q-1,
diam(T-x)=5R,
y(v_j)=j,
y(s_i)=2R-C_i>Q,
y(ell_a)=2R-C_(t_a)-a>Q.                            (FW269c)
```

All pair distances are distinct.  The proof separates their `R`-layers
`0,2,3,4,5`; inside a layer, signed base-`B` digits have units magnitude below
`B` and higher coefficients at most two, so successive reduction modulo `B`
recovers every interval endpoint and pendant label.  The only distances at
most `kappa` are the `kappa` pendant edges themselves:

```text
Spec(T) intersect [1,kappa]=[1,kappa].               (FW269c')
```

For fixed `Q,kappa`, their anchors have depth `Theta(m)` as `L` grows; the
unit edge has `J_e=empty`.  The detailed layer table and the no-carry proof
are in `docs/q1-low-owner-localization.md`.

FW269c is an **OBSERVED negative metric diagnostic**, not a Leech
counterexample: its order is `m+Q+kappa+3`, while its diameter is
`5B^(m+2)+Q`, and its sparse spectrum fails FW219c and FW261.  It proves that
q=1 top geometry, global distance uniqueness and any fixed initial interval
do not alone anchor low owners.  It does not assert that the full spectrum is
the only possible missing condition or that full spectrum is insufficient.

The **OBSERVED exact** local `I_6` owner catalogue has fifteen signatures, but
it does not bound their attachments.  An independently audited **OBSERVED
external/non-replayed engine diagnostic** with the stronger
permanent-true-leaf condition on the unit edge
already visits 1,351 constructed candidates through insertion depth six,
above the predeclared 100-fold order-11 gate of 1,233.  That count is not part
of the frozen FW269 replay and authorises no new engine.

Thus FW269 proves an **OBSERVED exact low-owner interface and an OBSERVED
negative pressure result**, not owner localisation.  A pure-core-tail
elimination theorem or a full tight-spectrum owner-provenance bridge remains
**UNVERIFIED**.  G18 is unchanged.  Frozen deterministic replay:

```text
theory-lab/topwindow/verify_q1_low_owner_localization.py
theory-lab/topwindow/results/q1_low_owner_localization_certificate.json
```

## FW270: the q=1 pure-tail exactness stop

The two proposed FW269 bridges have now been audited.  First, under the
already proved q=1 top-owner geometry,

```text
I_M=F_(T-x)+X^h R_r(H)
```

is coefficientwise equivalent to `F_T=I_N`: adding the visible `x`-pairs
restores exactly `I_[M+1,N]`.  FW261a--b merely refines the same partition
into `F_K`, `z--K`, `x--H`, the high visible class, and `{x,z}`.  Thus exact
FW219c/FW261 coverage is an **OBSERVED exact-spectrum equivalence**, not a
weaker owner-localisation hypothesis.

For any globally distance-distinct tree and any unit edge `ab`, put
`U=T-{a,b}`, `s_v=min(d(a,v),d(b,v))`, and let `F^T_U` retain ambient
`T`-distances between pairs in the generally disconnected label set `U`.
Then the **OBSERVED** identity is

```text
F_T=F^T_U+X+(1+X) sum_(v in U) X^(s_v).            (FW270b)
```

The starts `s_v` are globally 2-separated.  If the unit edge is a pure-`H`
tail, orient it with root-side endpoint `b`, descendant side `A`, and put
`q_b=d(x,b)`, `sigma=M-1-q_b`.  Parity-aware packing of the visible rooted
depths proves

```text
q_b>=2Q+1,
2|A|-1<=sigma<=M-2Q-2=N-3Q-2.                    (FW270b')
```

These inequalities do not eliminate the tail.  More strongly, FW270c gives
an **OBSERVED negative metric pressure family** for every `P>=Q>=2`: with
`m=P+Q+L`, `B>=8(P+Q+1)+17`, `R=B^(m+2)` and `W=B^(m+1)`, it has globally
distinct distances, exact formal diameter-`D` q=1-shaped top geometry, a
nonpendant pure-`H` unit edge,
and formal diameter-`D` owner suppliers matching the `I_P`-projections of
FW219c/FW261 through `I_P`, while coefficient `P+1` is absent.  It is not an
FW219c/FW261 state.  Its order is `2P+2Q+L+3` and its diameter is `5R+Q`, so
it is not Leech.

The near-perfect proposal that every order-`m` globally distance-distinct
integer tree with a nonpendant unit edge has diameter at least
`binom(m,2)+m-4` remains **UNVERIFIED**.  The check through `m<=12` is only an
**OBSERVED external/non-replayed finite diagnostic**; `m=13` was not closed.
If proved for `T-x`, it would give only `Q<=4` and would not cover a singleton
unit tail.  Therefore this algebraic/local-owner route is stopped.  A rooted
near-perfect realization theorem and a separate singleton-tail theorem are
the next **UNVERIFIED** interface.  No new engine or larger-order search is
authorised, and G18 remains **UNVERIFIED**.  Full statements, construction
and trust boundary: `docs/q1-pure-tail-stop.md`.

## FW271: full-spectrum product, pendant parity, and mechanism audit

FW271 first strengthens the pure-`H` unit-edge interface.  Orient the unit
edge `b--1--a` away from the q=1 root, let `A subset H` be its descendant
side, and put

```text
s=|A|,        q_b=d(x,b),
E={d(a,c):c in A},        rho=max E,
D={0} union (1+E),        T_0={d(b,v_j):0<=j<Q}.
```

The `Q(s+1)` actual pairs in `V x ({b} union A)` give the direct product

```text
T_0 dot+ D subset [M+1-q_b,M].                    (FW271a)
```

Since `0,1 in D`, `2 notin D`, exact filling would make all members of
`T_0` have one parity by the interval mixed-radix lemma.  Their q=1 parities
alternate, so filling is impossible.  Together with the farthest-root and
pure-core bounds this gives the **OBSERVED** inequalities

```text
q_b>=Q(s+1)+1,
q_b>=2Q+rho+1,              q_b<=M-rho-2<=M-2s,
4s<=N-3Q+1,                 s(Q+2)<=N-2Q-1.        (FW271a')
```

The exhaustive high/low alternatives sharpen these to

```text
2q_b>=M+1 => q_b>=(Q+1)(s+1)+1,
              s(Q+3)<=N-2Q-2;

2q_b<=M   => (2Q+1)(s+1)<=M,
              s(2Q+1)<=N-3Q-1.                   (FW271a'')
```

The low-branch product comes from placing the `x`-row and the `Q` visible
rows together in `[q_b,M]`; there is no second owner-disjoint visible block.

Without purity, let the unit cut have sides `A,B`, with `a in A`, `b,x in B`,
`|A|=s`, `m=|T-x|`, and put

```text
r=|V intersect A|,
epsilon_b=1_(b in V),       epsilon_a=1_(a in V).
```

Exact inclusion--exclusion of
`(V intersect B) x ({b} union A)` and
`(V intersect A) x ({a} union (B-{x}))` gives

```text
q_b+1 >= (Q-r)(s+1)-epsilon_b
         +r(m-s+1)-epsilon_a-r(Q-r).              (FW271a''')
```

All owners lie in `[M-q_b,M]`.  This **OBSERVED exact** formula does not
force `r=0` or `Q`.  The `L4` star/path and `L6` controls pass it, while none
has a pure-`H` unit descendant.  The FW270c non-Leech family satisfies all
pure-tail bounds with large slack.  There is only one unit edge in a Leech
tree, so no disjoint multi-tail aggregation follows.

Second, suppose `a--1--b` is pendant and put `S=T-a`,
`rho(v)=d(b,v)`.  Actual pairs give the **OBSERVED exact** self-complement

```text
I_N=F_S dot-union X R_b(S),
Spec(S)=I_N minus (1+{rho(v):v in S}).             (FW271b)
```

The rooted-depth set has order `n-1`, contains zero, and is disjoint from its
unit translate.  If `E,O` are the even/odd `b`-distance classes, with
orders `e,o`, then Taylor gives `eo=ceil(N/2)`.  Removing `a` from `O` and
separating even and odd coefficients yields exact partitions

```text
I_(floor(N/2))
 = {d(u,u')/2:{u,u'} subset E}
   dot-union {d(v,v')/2:{v,v'} subset O-{a}}
   dot-union {(1+rho(v))/2:v in O-{a}},

I_(eo)
 = {1+rho(u)/2:u in E}
   dot-union {(d(u,v)+1)/2:u in E,v in O-{a}}.     (FW271b')
```

The second line is the complete transformed `e x o` cross rectangle with a
distinguished pendant row.  It is not a smaller Leech tree.  Contracting
even-weight components shows that the standard halved graph is a forest iff
the odd-edge quotient tree has maximum degree at most two; the unit leaf
controls only one quotient leaf.  The **LITERATURE** family of Calhoun and
Polhill, perfect-distance forests `t K_(1,3)` for every `t`, also blocks any
claim that forest components must recurse as Leech trees.

In FW219 coordinates `y(v)=N-d(x,v)`, the pendant pair obeys
`y(b)=y(a)+1`.  Since coordinate `Q` is absent, exactly

```text
y(a)=j,y(b)=j+1 with 0<=j<=Q-2,
or Q+1<=y(a)<=N-2Q-2 with both vertices in the pure core. (FW271b'')
```

The first case lies in a terminal component of order at most `j+2`; the
second remains feasible.  At order 18 the parity orders `{7,11}` and their
next Taylor split remain arithmetically feasible.

Finally, FW271 records an **OBSERVED negative mechanism ledger**.  Joint
two-root/no-grazing needs a named inherited receiving cut; all-digit Ferrers
laminarity needs full lower-spectrum absorption; the canonical
triangle/triple boundary neither forces the canonical `M`-owner into a
triangle nor bounds its attachments; covariance determinants/inverse
sparsity forget edge-owner placement; signed derivatives and positive-`q`
Hosoya evaluations reduce to parity moments or rooted ball capacity; finite
characters are reversible owner recodings unless an archimedean no-wrap
theorem is added; and the **LITERATURE** Ma--Yi path-packing gap sees only
collinear pairs, at most `O(n log n)` on balanced trees.  None gives a
collision or a strictly decreasing fully owner-charged state.

Distance-matrix consequences beyond the exact covariance formulas and
parity-cross-rectangle consequences beyond (FW271b') remain **UNVERIFIED
successor work under review**.  FW271 is analytic and has no new verifier or
certificate.  It excludes no order and leaves G18 **UNVERIFIED**.  Full
proofs, controls, formulas and reopening gate:
`docs/q1-full-spectrum-mechanism-audit.md`.

## FW272: pendant-unit mixed-LCA obstruction

FW272 freezes the first exact successor to (FW271b').  Let `a--1--b` be a
pendant unit edge, root at `b`, and write

```text
E={v:d(b,v) even},               O={v:d(b,v) odd},
R_u=d(b,u)/2                     (u in E),
S_v=(d(b,v)-1)/2                 (v in O),
L_(u,v)=d(b,LCA_b(u,v)).
```

The complete odd actual-owner rectangle is

```text
A_(u,v)=(d(u,v)+1)/2
       =1+R_u+S_v-L_(u,v),
{A_(u,v):u in E,v in O}=I_(|E||O|).               (FW272a)
```

If `L` is identically zero, the two rooted coordinate sets give the exact
interval factorisation

```text
R dot+ S=[0,|E||O|-1].                             (FW272b)
```

The **OBSERVED all-order** conclusion is

```text
L identically zero  =>  |E|<=3.                   (FW272c)
```

The local factor proof is owner-sensitive.  The least positive member of
`R` must be one, since otherwise `b` to the corresponding even vertex and
`a` to the forced preceding odd coordinate have the same distance.  Let
`[0,k-1]` be the maximal initial block of `R`.  If `k>=4`, the depth
`2,4,6` vertices collide through the only possible LCA depths `0,1,2`.
If `k=2` or `3` and `P` is the next member of `R`, consecutive interval
coverage forces

```text
P=0 mod k,
{0,k,...,P-k} subset S,
[P,P+k-1] subset R.                               (FW272d)
```

For `k=2`, the depth-`2`/depth-`2P` LCA alternatives repeat either the root
distance at coordinate `P+1` or the pendant-row distance at `S=P-2`.  For
`k=3`, the depth-`2` and depth-`4` vertices first force different root
branches; the depth-`2P` vertex is then forced below the first branch, and
its distance to the depth-`4` vertex repeats the root distance at coordinate
`P+2`.  Hence no later `P` exists and (FW272c) follows.

Taylor's **LITERATURE** parity sizes make both classes at least four in every
candidate of order at least eleven.  Therefore every pendant-unit G18
candidate has a positive mixed-LCA entry, in both the visible and pure-core
q=1 locations.  The `L6` control has `R={0,1}`, `S={0,2,4,6}` and
`L` identically zero, showing why the class-size threshold is necessary.

FW272 does not handle a nonpendant unit edge and does not turn the remaining
positive laminar LCA block into a collision or a bounded-context smaller
state.  That step remains **UNVERIFIED**.  There is no verifier, certificate,
order exclusion or G18 conclusion.  Full proof and trust boundary:
`docs/q1-pendant-mixed-lca.md`.

## FW273: first positive mixed-LCA edge and terminal completion

FW273 retains the pendant edge `a--1--b`, rooted at `b`, and keeps actual
owners in both parity sheets.  Put

```text
z_(u,v)=R_u+S_v-L_(u,v)=(d(u,v)-1)/2,
tau=min{z_(u,v):L_(u,v)>0}.
```

Because the tree is globally distance-distinct, the raw convolution
coefficients are exactly one below `tau` and zero at `tau`.  This explicit
Leech antecedent is essential: the even-channel collisions below do not
follow from the odd rectangle alone.

The **OBSERVED all-order** first-hole theorem is

```text
tau<=3|O|+2.                                      (FW273a)
```

If `1 notin R`, the prefix forces `[0,tau-1] subset S`.  Otherwise the
maximal initial `R` block has radix `k=2` or `3`.  Before any later digit
`P<tau`, prefix coverage first puts all multiples of `k` below `P` into
`S`, and only then proves `P=0 mod k`.  The boundary `P+k=tau` is a direct
raw-hole contradiction; if `P+k<tau`, local coverage forces
`[P,P+k-1] subset R` and the FW272 actual LCA collisions.  Hence
`P+k>tau`, giving (FW273a).

The owner of `tau` is exactly an odd edge not incident with the root.  Indeed its
positive-LCA path avoids `b`; any odd edge on that path is itself a positive
mixed owner, so minimality and positivity collapse the whole path to that
edge.  Therefore

```text
w=2tau+1<=6|O|+5,                                 (FW273b)
```

and every lighter odd edge is incident with `b`.  The two order-eighteen
orientations give `w<=47` and `w<=71`.

The coupled completion is also exact.  Root-branch correction replaces the
raw products `RS` and `R^[2]+X S^[2]` by the actual internal odd/even
polynomials.  For same-parity `u,u'`, the cross matrix recovers the depth of
`LCA(u,u')` exactly iff that LCA-descendant subtree contains the opposite
parity.  At a deepest mixed vertex the relative cross sets form an actual
direct block `A dot+ B`; every unrecovered owner lies inside a maximal pure
child, all of whose edges are even.

Halving those children does not give a recursive handoff.  One pure child of
order `s-2` can retain `Theta(s^2)` free owners and inherits only a punctured
distance set.  Superincreasing even stars and combs red-team this unbounded
completion freedom.  At q=1/order eighteen, the visible `x` suffix starts at
half-index 70 while `tau<=35`, but no owner propagation places the deepest
mixed terminal on the `x` hull.

The n=11 CP-SAT necessary-relaxation result is only **OBSERVED
external/non-replayed diagnostic** evidence: its temporary model and proof
log were not frozen, so it is not a proof, certificate, or order exclusion.
The desired positive-block collision or bounded-context handoff remains
**UNVERIFIED**.  FW273 has no verifier, excludes no order, does not touch the
nonpendant branch, and leaves G18 **UNVERIFIED**.  Full proof, exact formulas,
controls and stop boundary: `docs/q1-first-positive-lca.md`.

## FW274: absolute first odd-edge bound

FW274 keeps the FW273 pendant setting and exact first-hole identity, but the
raw prefix is now used as an exhaustive rooted-coordinate list.  If
`1 notin R`, same-parity capacity gives `tau<=4`.  Otherwise the initial
root-even radix is two or three.  Defining the next later coordinate as
`Q_0=+infinity` when it does not exist, explicit ancestor-placement
collisions give the **OBSERVED all-order** ledger

```text
k=3,Q_0>=tau: tau<=9,        k=2,Q_0>=tau: tau<=10,
k=3,Q_0<tau:  tau<=10,       k=2,Q_0<tau:  tau<=9.
```

The last apparent `tau=11` state has `k=3,Q_0=9`.  Exact prefix coefficient
`c_10=1` leaves only `R_10` or `S_10`: the second hits the raw hole at
eleven through `R_1`, and the first repeats distance twenty between the
already root-separated vertices at `S=3,6`.  Hence

```text
tau<=10,
w=2tau+1<=21.                                      (FW274a)
```

FW272 guarantees the positive mixed LCA for every pendant-unit candidate of
order at least eleven.  The eight-vertex pressure control attains
`tau=10,w=21`, has all pair distances distinct and odd transformed sheet
`I_[0,11]`, but its even half-sheet is not `I_16`; it is not Leech.  The
constant is therefore sharp only for the local interface.

FW274 supplies no full-even-sheet or terminal-absorption theorem, no q=1
suffix propagation, and no nonpendant-unit conclusion.  It excludes no
order and leaves G18 **UNVERIFIED**.  Its frozen deterministic
finite-kernel replay is
`theory-lab/topwindow/verify_q1_absolute_first_odd_edge.py`, with byte-identical
output in `theory-lab/topwindow/results/q1_absolute_first_odd_edge_certificate.json`;
that replay supports the analytic parent-map ledger but is not a Leech search
or an independent all-order proof.  Full proof and trust boundary:
`docs/q1-absolute-first-odd-edge.md`.

## FW275: nonpendant-unit rooted-stability stop

FW275 returns from the pendant orientation to the hard nonpendant `2|b`
unit cut.  For `c--x--a--1--r--B`, `|B|=b`, its **OBSERVED exact**
counterexample wrapper is

```text
O={x} dot-union (1+Y) dot-union (x+1+Y),
D_0=binom(b,2)+3b-2,
F_B dot-union O dot-union H=I_[1,D_0],    |H|=b-3. (FW275a)
```

After removing the root row, the remaining `binom(b-1,2)` coefficients must
be owned by actual nonroot pairs with their actual LCA gates.  An **OBSERVED
analytic** scalable formal family passes every audited
first-pivot/reflection/`2p`-chain constraint, but
its second direct-root pivot collides with two wrapper owners.  Hence a
one-pivot audit is not a rooted-tree induction.

The sharper obstruction is actual.  An **OBSERVED hand-checkable** order-nine
equality tree has a multi-gate owner triangle, so laminarity does not make
row handoff acyclic.  An order-eleven equality tree telescopes a long `2p`
chain and replicates the missing virtual row for one diagonal hole.  Both
have `D=D_0+1`, so they refute only cap-blind local implications, not a
theorem that essentially uses `D<=D_0`.  The cap-blind first-pivot /
chain-boundary / single-virtual-row mechanism is therefore at an **OBSERVED
STOP**, but the near-perfect diameter conjecture remains **UNVERIFIED**.

The exact reopening gate is an **UNVERIFIED** strict-cap global potential on
labelled owner pairs and all LCA gates, robust to cycles and mergers, or an
exact terminal-suffix theorem peeling a rooted terminal set with all incident
distances and one hole per deleted vertex.  FW275 has no verifier, witness or
order exclusion; G18 remains **UNVERIFIED**.  Full controls and trust boundary:
`docs/nonpendant-unit-rooted-stability-stop.md`.

## FW276: first-positive edge cut and exact stop

Return to the pendant FW274 state and cut its first positive edge
`f=pc`, whose weight is `w=2tau+1<=21`.  With `A` the root side and `B` the
descendant side, split the rooted distances from `p,c` by local parity into
`A_0,A_1,B_0,B_1`.  The **OBSERVED exact** owner identities are

```text
J_[0,K-1]=O_A+O_B+X^tau A_0B_0+X^(tau+1)A_1B_1,
J_[1,P]=E_A+E_B+X^(tau+1)(A_0B_1+A_1B_0).          (FW276a)
```

Every summand is coefficientwise owner-disjoint.  Positive-LCA minimality
puts every odd internal `B` owner above `tau`, while `f` alone owns `tau`;
hence `O_A` owns the exact low odd block `J_[0,tau-1]`.  Neither endpoint of
`f` meets the unit edge, so cross even distances start at `w+3`; consequently
`E_A+E_B` owns `J_[1,tau+1]`.

Find-Next adds `f` after the forest of lighter edges.  Every lighter odd edge
is incident with `b`, so the light component containing `c` has only even
edges; after halving, its order is at most `tau+1<=11`.  This does not bound
the full side `B`, which may acquire unbounded later heavy attachments.  The
whole light forest has at most `2tau` edges.  Its root component owns all
`tau` low odd values, so at `tau=10`, order eighteen has `|A|>=7,|B|<=11`;
the formal split `(a_0,a_1;b_0,b_1)=(2,5;6,5)` still passes all resulting
capacities, including Taylor's `7|11` parity count.

For q=1, if `x in A` and `v_j in B`, then
`d(c,v_j)=N-j-d(x,p)-w`; a consecutive visible block would therefore give a
reflected rooted interval.  Such a block is not forced, and no implication
`w>=Q` is available; a pure-core `H--H` cut may contain no visible vertex on
its descendant side.  Closing the cut requires an **UNVERIFIED**
owner-labelled no-grazing/absorption theorem that controls the unbounded
cross-owner rows.  FW276 has no verifier, computation or order exclusion;
G18 remains **UNVERIFIED**.  Full proof and strict stop:
`docs/q1-first-positive-edge-cut.md`.

## FW277: light-quotient cap and visible-row area

Contract the complete forest of edges lighter than the FW276 edge
`f=p--c_f`, and select a degree-one bag of the full quotient on the
away-`b` side of `f`.  This is a genuine pendant even cap `C`, attached by
`r--e--t`.  The **OBSERVED** total nonroot light-bag excess satisfies

```text
tau>=2: E_nb<=tau-1;
tau=1:  F_<3 has only the root unit bag, one nonroot edge-2 bag and isolates.
```

Hence `|C|<=10` and `diam(C)<=108`.  The exact cut and its unit rows are

```text
I_N=F_C+F_R+X^eR_t(C)R_r(R),
(D_C-D_C)^+ disjoint from {1,e,H,H+1,H+e,H+e+1}.
```

On the q=1 branch, an endpoint cap transports all `Q` top owners into
disjoint shifted blocks.  If `x` is outside `C` and `C` contains no visible
vertex, the whole visible-by-cap rectangle occupies one named window; its
parity-aware **OBSERVED** area bound is

```text
2e+rho+sQ+(s-1)(Q mod 2)<=N-Q-1.                  (FW277a)
```

A saturated cap halves to a Leech tree and the full light forest restricts
it to `tau=1,s=2`.  The quotient alternative is a bounded nonendpoint cap or
a heavy descendant corridor ending in the endpoint bag.  The singleton cap
still leaves `I_N=F_R+X^eR_r(R)`, an unrestricted full rooted row rather than
a terminal interval or decreasing exact state.  FW277 is therefore an
**OBSERVED** bounded-cap/row-area theorem with an exact singleton stop, not
an absorption or order exclusion; G18 remains **UNVERIFIED**.  Full proof:
`docs/q1-light-quotient-cap.md`.

## FW278: unit-edge owner propagation audit

For the FW277 singleton cap, delete both it and the pendant unit leaf.  The
remaining core `U` has the exact owner partition

```text
I_N=F_U dot-union (1+D_b(U)) dot-union (e+D_r(U))
    dot-union {1+d_U(b,r)+e}.
```

Projection to the `b`--`r` path gives four fibre rows and at most six
distinct nonzero forbidden depth differences.  Removing the three external
supports and rank-compressing
the internal values yields `I_[1,binom(n-2,2)]`; it is a same-topology Leech
descent exactly when the external-hole count is additive on every core path.
That condition fails for a nonendpoint leaf of `L6`, and q=1 currently gives
no top-to-fibre implication.

For the strict FW275 `x=2` state, the filled virtual-row owner graph satisfies

```text
sum_f w_f(c_f-l_f)=2E.
```

The hard cap converts this into an exact `(E-2)`-hole subset-sum certificate.
It rejects the `b=7` equality pattern after strict truncation, but signed
`E=2,3` controls leave the general certificate open.  An integral congruence
of the bordered additive distance matrix to `H direct-sum diag(-2w_e)` gives
only edge-factor Smith, rank, determinant and inverse data, not cross owners.
These are **OBSERVED mechanism-specific STOPs**, with no verifier, exclusion
or G18 proof.  Full audit: `docs/unit-edge-owner-propagation-audit.md`.

## FW279: closure-architecture decision and exact stops

FW279 decides that the present pendant/nonpendant/small-`Q` A/B/C
architecture is **OBSERVED not closed**.  In the canonical pendant state,
the transformed internal values form a strictly decreasing numeric owner
forest.  Allowing owners to permute, order-`n-2` descent is exact if and only
if transformed path sums are injective and the forest sources are precisely
the top band.  Conditional on injectivity, their displacement is

```text
Delta=sum_(h in H_0)(A_h-B_h),
```

an exact multiscale balance between within-component additive overflow and
repeated above-threshold Kruskal crossings.  Rank anti-coalescence and the
transport inequality forcing `Delta=0` are separate **UNVERIFIED** lemmas.

For an arbitrary nonpendant unit cut of orders `s|t`, the strict cap gives

```text
|H_out|=E-((s-2)(t-2)+2)
```

and an exact signed cut-flow/subset-sum value, with consecutive-run, q=1
suffix and Taylor refinements.  Actual pressure trees show that strict top
coverage is load-bearing; two formal `I_36` coefficient states survive the
entire scalar ledger but fail at the first and second rooted-LCA pivots.
Exact all-pivot reconstruction retains `Theta(m^2)` owner/LCA data and has no
proved decreasing state.  No actual strict counterexample was found.

The restricted order-eighteen pure-`H` `2|15` calculation genuinely excludes
only `Q=10,...,14`.  Weak gate states survive for `Q=5,...,9`; a disclosed
Q9 SMT sentinel ended `UNKNOWN`/cancelled, without a frozen script or proof
certificate.  Thus FW279 proves neither G18 nor any all-order exclusion.
Reopening requires rank anti-coalescence plus multiscale transport, or a
general rooted-realisation stability theorem.  Full quantified audit:
`docs/g18-closure-architecture-audit.md`.

## FW280: pendant rank anti-coalescence mismatch stop

FW280 resolves the first-collision algebra without proving injectivity.  A
first collision reduces to at most two edge-disjoint arms on each side, and
the **OBSERVED exact** identities are

```text
def(P)-def(P')=|D intersect (d(P),d(P')]|,
eta(s,w)=|M^+_(s,w)|-|M^-_(s,w)|.
```

The first identity retains every internal owner in the intervening numeric
window.  The second records every internal/external owner colour change under
prefix translation.  Each mismatch must be non-aligned with the prefix, but
its actual uncrossing depends on an LCA, gate or connector.  Since one side
of a mismatch is external, first-collision minimality does not produce a
smaller core collision.

The full `L6` interval in a noncanonical endpoint orientation has mismatch
owners at complete-overlap, nested and tripod gates, so generic owner
uncrossing has no common direction.  An infinite actual distance-distinct,
non-Leech family with an exact `Q=3` endpoint suffix has one transformed
collision and passes Taylor parity for even parameters; it shows that the top
suffix without full low coverage is insufficient.  A disclosed 464-row
one-gap order-six diagnostic returned `UNSAT`, but it is external/non-replayed
without a retained script or proof log.

Thus canonical top ownership plus full interval coverage remains an
**UNVERIFIED** mismatch-gate transport theorem.  The exact alternative keeps
`Theta(m^2)` owner/LCA entries and has no known strict potential.  FW280
proves no anti-coalescence theorem, order exclusion or G18.  Full stop:
`docs/pendant-rank-anti-coalescence-stop.md`.

## FW281: canonical gate-transport checkpoint

FW281 rewrites a putative collision exactly by threshold profiles: its total
profile difference vanishes on internal-rank thresholds and has positive sum
on external-owner thresholds.  Transformed Kruskal gives the necessary rank
bound `K(j)>=j`; the exact injectivity criterion is instead coefficientwise
separation of all rooted merge convolutions, information of `Theta(m^2)` size
in the direct representation.

Canonical full-spectrum `L6` is injective after transformation, yet its
unit/top shadows form two local lift cycles through different gates and its
AC-2 uncrossings have both connector-positive and overlap-negative corrections.
It rules out least-threshold, same-root, uniform-sign and strict local-lift
proofs, but not a global theorem tied to the first collision.  Noncanonical
`L6` shows scalar Kruskal data are insufficient; an infinite non-Leech `Q=4`
family shows exact top ownership plus Taylor parity are insufficient.  The
232-row `I_4` diagnostic is external/non-replayed and not proof input.

The 60k checkpoint triggers **STOP**.  Only global rooted-merge convolution
separation coupled to AC-1 reopens this route.  FW281 proves no
anti-coalescence theorem, exclusion or G18.  Full stop:
`docs/canonical-mismatch-gate-transport-stop.md`.
