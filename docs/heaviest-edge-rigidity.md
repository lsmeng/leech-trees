# Edge-cut sumset rigidity and heaviest-edge consequences

**OBSERVED theorem.** Let `T` be a Leech tree of order `n`, let `e` be any
edge of weight `w`, and let deleting `e` leave components of orders `a,b`.
Then

```text
w <= N+1-ab,                 N=binom(n,2),
```

and equality at any edge is possible only for the known Leech trees of orders
`2,3,4`. Consequently every edge of every Leech tree of order `n>=5`
satisfies the strict improvement

```text
w <= N-ab.
```

This closes the zero-excess branch of the central/mixed-radix programme. It
does **not** yet bound the positive excess uniformly, so the general
nonexistence theorem remains **UNVERIFIED**.

**OBSERVED bounded-handoff theorem.** In fact the two rooted distance sets on
the sides of a globally distinct-distance tree cannot have unique sums
covering all of `0,1,...,10`. Consequently, for every edge with `ab>=11`, at
least one of the ten values immediately above that edge is realised wholly
inside a proper component:

```text
there is h in {1,...,10} with d(x,y)=w+h,
and x,y lie on the same side of the edge.
```

## From cut containment equality to an interval factorization

Root the two components at the endpoints of `e` and let

```text
A = {d(root_A,x): x in component A},
B = {d(root_B,y): y in component B}.
```

Both sets contain zero. Every cross distance is

```text
w+alpha+beta,       alpha in A, beta in B.
```

All `ab` sums are distinct. The standard containment count gives
`w<=N+1-ab`. If equality holds, there are exactly `N-ab=w-1` within-component
pairs. They must realise `1,...,w-1`, while the cross pairs must realise
`w,...,N`. Hence

```text
A direct-sum B = {0,1,...,ab-1}.                 (1)
```

## Mixed-radix normal form

For completeness, every two-set factorization (1) has an alternating
mixed-radix form. Orient the factors so that `1` lies in `A`, and let `r` be
the first positive integer absent from `A`. Coefficient comparison, block by
block, gives

```text
A = {0,...,r-1} + r A',
B = r B',
A' direct-sum B' = {0,...,ab/r-1}.
```

Iterate. Consecutive quotient digits assigned to the same factor can be
merged, so a canonical factorization is described by radices
`r_1,...,r_k>=2`, with the digit positions alternating between `A` and `B`.

The verifier independently checks this description by direct polynomial-
coefficient recursion for every interval length `2,...,40` (197 normalized
factorizations); the proof above, rather than that finite check, supplies the
all-length reduction.

## Which factors can be rooted tree depth sets?

Let `S={0=s_0<s_1<...<s_m}` be the complete root-distance set of a positively
weighted tree whose vertex-pair distances are all distinct. Every nonroot
vertex has a unique parent at a smaller depth. Conversely, choosing a parent
for every `s_i` among `s_0,...,s_{i-1}` fixes every edge weight and every pair
distance. Thus rooted realizability is a finite exact parent-map problem.

There is also a terminating all-order bound. If a radix `r` is appended at
place value `G` to a currently feasible factor `S`, the enlarged factor has

```text
m = r |S| vertices,
H = max(S)+G(r-1) maximum root depth.
```

Its `binom(m,2)` distinct positive distances all lie at most `2H`, so
`binom(m,2)<=2H`. This quadratic inequality leaves finitely many `r`. If a
prefix depth set has no rooted realization, later radix digits cannot repair
it: all later depths are larger, whereas a parent or least common ancestor of
an existing vertex must have smaller depth.

Exhausting this finite recursion leaves exactly nine normalized candidates:

```text
(2), (3),
(2,2), (2,3), (3,2), (3,3),
(2,2,2), (2,3,2),
(2,2,2,2).
```

The largest has factor sizes `4+4=8`. Exhausting the parent maps on both sides,
joining them with `w=N+1-ab`, and checking the full distance multiset leaves
only:

```text
order 2: the single edge;
order 3: the path with weights 1,2;
order 4: the star with weights 1,2,4;
order 4: the path with weights 1,3,2.
```

Every positive witness passes both `src/checker_a.py` and `src/checker_b.py`.
The exact audit is
`theory-lab/topwindow/verify_heaviest_edge_rigidity.py`; its frozen summary is
`theory-lab/topwindow/results/heaviest_edge_rigidity_certificate.json`.

## A uniform 10-value handoff

The same rooted-parent oracle can be used without assuming a complete interval
factorization. Start with `A=B={0}` and scan `k=1,2,...`. If `k` already has
one representation, uniqueness forbids inserting `k` in either factor. If it
has none, exact prefix coverage requires inserting `k` in exactly one factor.
After each insertion, reject the state unless parent maps on both sides give
distinct internal pair distances and the two internal distance sets are
disjoint. The latter is mandatory because both components belong to one
globally distinct-distance tree. A later vertex has larger root depth and
therefore cannot become the parent or least common ancestor needed to repair
an earlier rejected prefix.

The exact numbers of surviving normalized states after processing
`k=1,...,10` are

```text
2,4,2,4,6,2,2,4,2,0.
```

Thus 10 cross deficits `0,...,9` are possible abstractly, but 11 are not.
For a Leech tree, cross distances over the edge have the form `w+A+B`. If
`ab>=11`, containment gives `w+10<=N`. Were every value `w,...,w+10` cross,
`A+B` would cover the forbidden
prefix. Since `w` itself is cross, one of `w+1,...,w+10` must instead be a
within-component distance. `QED` (finite rooted-prefix audit).

The extremal delay is rigid. If all ten values `w,...,w+9` are cross, then,
up to swapping the sides, the shallow root-depth sets and their unique parent
maps are

```text
A = {0,1,4,5}:  root--1--4 and root--5   (edge weights 1,3,5),
B = {0,2,8}:    root--2 and root--8      (edge weights 2,8).
```

Thus the last surviving prefix is a fixed Fibonacci-weighted two-root core;
the first missing cross deficit is 10. Any larger hypothetical tree delaying
the handoff that long must extend this core only by vertices at greater root
depth.

This is a genuine constant-loss transition into a proper component. It is not
yet an induction: after the handoff, that component need not inherit every
integer distance in the next window.

An independent clean-room audit constructs all 38 factor pairs covering ten
values and all 46 factor pairs that would cover eleven, then directly iterates
4,039,455 rooted parent maps without the incremental feasibility pruning. It
finds the same two symmetric positive controls at length ten and zero compatible
pairs at length eleven:
`theory-lab/topwindow/verify_heaviest_handoff_cleanroom.py`. Its frozen summary
is `theory-lab/topwindow/results/heaviest_handoff_cleanroom_certificate.json`.

## Finite-hole excess ladder

The prefix recursion remains finite when a bounded number of cross-sum holes
is allowed. For a hole budget `e`, retain every compatible rooted-factor
state, allow at most `e` uncovered values, and stop at the first deficit where
no state remains. There is no beam or state-count cutoff. For `e=0,...,8`, the
exact death indices are

```text
e              0   1   2   3   4   5   6   7   8
death K(e)    10  19  22  31  34  37  40  48  51
```

Thus compatible rooted sumsets with at most `e` holes have total span length
at most `K(e)`. At every edge the span length is exactly `N-w+1=ab+E`, where
`E=N+1-ab-w` is the actual number of within-component distances above `w`.
Therefore the ladder is edgewise: cut product thresholds
`ab>=11,19,21,29,31,33,35,42,44` force `E>=1,...,9`, respectively. For the
heaviest edge, `ab>=n-1`, giving

```text
n>=20 => E>=2,     n>=22 => E>=3,
n>=30 => E>=4,     n>=32 => E>=5,
n>=34 => E>=6,     n>=36 => E>=7,
n>=43 => E>=8,     n>=45 => E>=9.
```

In particular the relevant Taylor orders satisfy

```text
n=25,27: E>=3;     n=36,38: E>=7;     n=49,51: E>=9.
```

The death indices also locate the holes. If
`h_1<h_2<...` are the missing cross deficits, then the audited layers give

```text
h_1<=10, h_2<=19, h_3<=22, h_4<=31, h_5<=34,
h_6<=37, h_7<=40, h_8<=48, h_9<=51.
```

Thus orders 25/27 have at least three within-component distances among
`w+1,...,w+22`; orders 36/38 have at least seven among
`w+1,...,w+40`; and orders 49/51 have at least nine among
`w+1,...,w+51`. This is a finite-order thick handoff, not merely a count of
unlocated excess.

There is also a direct merge-waste gain. Put `m=ab` and
`S=A+B`. If `r` guaranteed holes lie below `m`, then replacing them in the
`m`-element set `S` requires at least the values `m,...,m+r-1`, so

```text
sum(S) >= binom(m,2) + r m + binom(r,2) - sum_{i=1}^r h_i.
```

Using `m>=n-1` and the bounds above gives an improvement over the standard
final-merge term `binom(m,2)` of at least 24 at order 25/27 (first three
holes), 69 at 36/38 (first five), and 164 at 49/51 (first seven).
Already the first hole gives the all-order refinement

```text
TW >= (sum_k Delta_k^2-N)/2 + ab-10              (n>=12),
```

because the standard quadratic proof contributes `binom(ab,2)` at the final
merge and omitting some `h<=10<ab` raises that merge sum by at least `ab-h`.

The exact verifier reaches 104,249 simultaneous states and 69,721,840 rooted
parent-search states at `e=8`:
`theory-lab/topwindow/verify_heaviest_excess_ladder.py`; frozen summary:
`theory-lab/topwindow/results/heaviest_excess_ladder_certificate.json`.
This finite ladder is rigorous, but extrapolating linear growth beyond `e=8`
is **UNVERIFIED**.

## An all-order rooted-span lower bound

There is a complementary bound that depends on the two component orders, not
only their product. Let `H_A=max(A)`, `H_B=max(B)` and put

```text
C_A=binom(a,2),       C_B=binom(b,2).
```

All `C_A+C_B` within-component distances are globally distinct. If, for
example, `H_A<=H_B`, then the `A`-side distances are at most `2H_A`, while the
union of both sides' distance sets is at most `2H_B`. Hence

```text
H_A >= ceil(C_A/2),       H_B >= ceil((C_A+C_B)/2).
```

Interchanging the sides when `H_B<=H_A` gives the unconditional bound

```text
H_A+H_B >= ceil((C_A+C_B)/2)
             + min(ceil(C_A/2),ceil(C_B/2)).
```

Since the largest cross deficit is `H_A+H_B` and the full deficit interval has
length `ab+E`, every edge satisfies the **OBSERVED all-order inequality**

```text
E >= g(a,b)
  := max(0, ceil((C_A+C_B)/2)
              + min(ceil(C_A/2),ceil(C_B/2)) + 1-ab).       (2)
```

Unlike the finite-hole ladder, `g(a,b)` grows quadratically on sufficiently
unbalanced cuts. For example, every leaf cut at order 18 has `E>=52`. The
bound is checked on every edge of the five known witnesses and combined with
the finite ladder in the topology diagnostic below. It still eliminates none
of the frozen order-18 topologies, but lowers the minimum weighted-moment
margin from 27,523 to 12,784. Thus it is a genuine all-order strengthening,
not yet the terminal contradiction.

## Global edge-excess budget

The edgewise form can be summed. For each edge `e`, write `c_e=a_e b_e` and
`E_e=N+1-c_e-w_e`. Since `sum_e c_e` is the unweighted Wiener index
`W_hop(T)`, one has the exact identity

```text
sum_e E_e = (n-1)(N+1) - W_hop(T) - sum_e w_e.
```

The diameter path has weighted length `N`, so `sum_e w_e>=N`. If `f(c)` is
the edgewise ladder lower bound

```text
c>=11,19,21,29,31,33,35,42,44
  => f(c)>=1,2,3,4,5,6,7,8,9,
```

then every Leech tree must satisfy

```text
sum_e f(c_e) <= (n-2)N+(n-1)-W_hop(T).
```

This does not yet contradict every topology, but it turns the local handoff
catalogue into a global topology-dependent budget and is the natural interface
to the thick-branch endgame.

The fixed first moment of all Leech distances gives a stronger exact identity.
Every edge lies on exactly `c_e` vertex-pair paths, so

```text
N(N+1)/2 = sum_e c_e w_e.
```

Substituting `w_e=N+1-c_e-E_e` gives

```text
sum_e c_e E_e
  = (N+1) W_hop(T) - sum_e c_e^2 - N(N+1)/2.       (3)
```

Consequently the finite ladder supplies the topology-only necessary condition

```text
sum_e c_e f(c_e)
  <= (N+1) W_hop(T) - sum_e c_e^2 - N(N+1)/2.
```

Equation (3) weights central, nearly balanced cuts much more heavily than the
unweighted budget. Its audit checks all 14 edges of the five known witnesses,
with every witness passing both independent checkers, and evaluates all
2,105,739 edge rows in the 123,867 frozen order-18 topologies. The present
finite ladder eliminates none of those topologies: the minimum remaining
margin is 27,523 (the star topology). This negative diagnostic is important:
the moment identity is an interface for a future thick-centre bound, not by
itself a nonexistence proof. Verifier and frozen output:
`theory-lab/topwindow/verify_edge_excess_moments.py` and
`theory-lab/topwindow/results/edge_excess_moments_certificate.json`.

## Remaining nesting problem

Write

```text
E = N+1-ab-w.
```

The theorem applies afresh to every edge; a receiving component does not need
to inherit the Leech interval. This removes the former interval-inheritance
obstruction. What remains is directional: after choosing an edge on a
within-side handoff path and applying the theorem again, the next handoff may
land on the side containing the previous edge rather than in a nested proper
side. The next target is a dichotomy proving either strict nested descent or
accumulation of a thick branch profile. Extending the finite excess ladder
uniformly would also feed directly into the Kruskal merge-waste identity.
