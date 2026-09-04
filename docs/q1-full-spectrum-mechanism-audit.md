# The q=1 full-spectrum mechanism audit (FW271)

This note freezes the analytic successor audit to FW270.  It separates two
new exact consequences of the full Leech spectrum from a collection of
mechanisms that were pressure-tested and did not close.

* **OBSERVED:** a unit edge whose descendant side is wholly in the q=1
  threshold core gives an actual-pair product inside one named top window.
  The product is strictly smaller than that window, and it yields the
  all-order inequalities in Section 2, including separate high- and
  low-`q_b` bounds.
* **OBSERVED:** a pendant unit edge gives an exact self-complement identity,
  an exact even/odd coefficient split, and a complete parity-halved cross
  rectangle.  The q=1 coordinates put the leaf edge either in one visible
  consecutive pair or wholly in the pure core.
* **OBSERVED negative mechanism audit:** the two-root, all-digit Ferrers,
  top-triangle, covariance-kernel, signed-moment, positive-`q` Hosoya,
  finite-character, and path-packing routes listed in Section 4 do not yet
  produce a collision or a strictly decreasing fully owner-charged state.
* The parity cross rectangle is a new exact reduction, not a smaller Leech
  tree and not a recursive state.  Any further distance-matrix or
  cross-rectangle consequence is still **UNVERIFIED** and is not frozen in
  FW271.

No statement below excludes an order.  In particular G18 remains
**UNVERIFIED**.  This is an analytic theorem/audit, so FW271 creates no
verifier or certificate and introduces no SAT witness.

## 1. Notation and actual-pair scope

Let `T` be a hypothetical q=1 Leech tree of order `n>=5`, and put

```text
N=binom(n,2),              M=N-Q,              m=n-1.
```

Use the FW218--FW219 endpoint `x`.  In `T-x` there is exactly one visible
vertex `v_j` at every coordinate `0<=j<Q`, no vertex at coordinate `Q`, and

```text
V={v_0,...,v_(Q-1)},       d(x,v_j)=N-j.          (FW271.1)
```

The threshold core is

```text
H={u in T-x:N-d(x,u)>Q}.
```

Every displayed union of coefficient sets below is an actual unordered-pair
disjoint union.  It is not merely equality of cardinalities.  As in FW270,
write

```text
F_S(X)=sum_{{u,v} subset V(S)} X^d(u,v),
R_p(S;X)=sum_(v in V(S)) X^d(p,v),
I_k=X+...+X^k.
```

## 2. FW271a: the pure-H product/window theorem

Let `ba` be the unique weight-one edge, oriented away from the FW219 root,
with `b` on the root side.  Let `A` be the component containing `a` after
deleting `ba`, and assume

```text
A subset H,                 s=|A|,                 q_b=d(x,b).
```

For this section define

```text
E={d(a,c):c in A},          rho=max E,
D={d(b,u):u in {b} union A}={0} union (1+E),
t_j=d(b,v_j),               T_0={t_j:0<=j<Q}.
```

Here `|D|=s+1`, `0,1 in D`, and `2 notin D`.  The last fact follows from
global uniqueness: a second pair at distance one would collide with
`{a,b}`.

### 2.1 The product occupies one exact window

Every visible vertex lies outside `A`.  Therefore the path from `v_j` to
`u in {b} union A` passes through `b`, and

```text
d(v_j,u)=t_j+d(b,u).
```

These `Q(s+1)` actual pairs are all distinct.  The rooted LCA formula and
(FW271.1) give

```text
t_j>=N-j-q_b>=M+1-q_b,
```

while all these pairs lie in `T-x`, whose diameter is `M`.  Hence

```text
T_0 dot+ D subset [M+1-q_b,M],
q_b>=Q(s+1).                                      (FW271a.1)
```

The direct sum cannot fill the window.  Indeed, equality in (FW271a.1),
after translating its minimum to zero, would be a unique factorisation

```text
(T_0-L) dot+ D=[0,q_b-1].
```

The elementary interval-factorisation lemma says that when one factor
contains `0,1` but not `2`, its first mixed-radix digit is `{0,1}` and every
element of the other factor has the same parity.  On the other hand the LCA
identity gives

```text
t_j congruent N-j-q_b (mod 2),
```

so the `Q>=2` starts alternate in parity.  Thus equality is impossible and

```text
q_b>=Q(s+1)+1.                                    (FW271a.2)
```

This strict `+1` is owner-sensitive: it uses the same product that occupies
the window, rather than adding an unrelated count.

### 2.2 Radius and core bounds

The FW270 parity-aware packing argument for the visible starts gives

```text
max T_0>=N-q_b+Q.
```

Since `max D=rho+1` and `max(T_0+D)<=M`, while the `s` elements of `E`
start at zero and contain no consecutive pair,

```text
q_b>=2Q+rho+1,                 rho>=2s-2.          (FW271a.3)
```

For a farthest `c in A`, purity gives

```text
d(x,c)=q_b+1+rho<=M-1,
q_b<=M-rho-2<=M-2s.                               (FW271a.4)
```

Combining (FW271a.2)--(FW271a.4) yields the two unconditional pure-tail
consequences

```text
4s<=N-3Q+1,
s(Q+2)<=N-2Q-1.                                   (FW271a.5)
```

### 2.3 High and low branches

The `x`-row against the same rooted factor has distances `q_b+D`.  If

```text
2q_b>=M+1,
```

then the `x`-row and all `Q` visible rows lie in the common window
`[M+1-q_b,M]`.  Their `(Q+1)(s+1)` owners are distinct.  Exact filling is
again impossible by the radix-two/alternating-parity argument, so

```text
q_b>=(Q+1)(s+1)+1,
s(Q+3)<=N-2Q-2.                                   (FW271a.6)
```

If instead

```text
2q_b<=M,
```

the same owners all lie in `[q_b,M]`.  Its length gives

```text
(Q+1)(s+1)<=M-q_b+1.
```

Combining this with (FW271a.2), rather than counting a fictitious second
visible rectangle, gives

```text
(2Q+1)(s+1)<=M,
s(2Q+1)<=N-3Q-1.                                  (FW271a.7)
```

Thus both branch refinements are **OBSERVED**.  In particular the low-branch
product is valid, but its proof is the shortened joint window, not a second
owner-disjoint `Q`-row.

### 2.4 The exact general visible-split capacity

There is also an exact statement without the pure-`H` hypothesis.  Let `A`
and `B` be the two sides of `ba` in the full tree, with `a in A`, `b,x in B`,
and `|A|=s`.
Put

```text
r=|V intersect A|,
epsilon_b=1 if b in V and 0 otherwise,
epsilon_a=1 if a in V and 0 otherwise.
```

Consider the two actual-pair rectangles

```text
P_b=(V intersect B) x ({b} union A),
P_a=(V intersect A) x ({a} union (B-{x})),
```

with the invalid diagonals `{b,b}` and `{a,a}` removed when present.
Their intersection is exactly the `r(Q-r)` cross-visible pairs.  Consequently
their union has size

```text
C_split=(Q-r)(s+1)-epsilon_b
        +r(m-s+1)-epsilon_a-r(Q-r).                (FW271a.8)
```

Every owner in this union has distance in `[M-q_b,M]`: on the `b` rectangle
this follows from `d(x,v_j)=N-j` and `d(x,b)=q_b`; on the `a` rectangle use
`d(x,a)=q_b+1`.  Therefore

```text
q_b+1>=C_split.                                    (FW271a.9)
```

This exact split formula does not force `r` to be `0` or `Q`.  Even after
optimising and ignoring the at-most-two diagonal corrections, the first
mixed row contributes only order `m`, while `q_b` can have order `m^2`.

### 2.5 Controls and trust boundary

The known small Leech trees are boundary controls, not premises of the
proof.  The `L4` star has empty `H`; the `L4` path has its unit descendant
visible; and `L6` has a visible singleton unit descendant.  Thus none is a
counterexample to the pure-`H` theorem.  The general split rows are exactly

```text
              (Q,m,s,r)   (epsilon_b,epsilon_a)   C_split   q_b+1
L4 star       (3,3,1,1)          (1,1)               3        5
L4 path       (2,3,1,1)          (1,1)               2        6
L6            (4,5,1,1)          (1,1)               6       14.
```

The FW270c pressure family also survives every displayed inequality.  Its
pure unit tail has `s=2`, `rho=W`,

```text
q_b=Q+3R+C_(t_1),               M=5R,
```

and lies in the high branch with large slack.  This control is globally
distance-distinct but not Leech: its formal cap is exponentially larger than
its pair count and its next low coefficient is absent.

A Leech tree has only one weight-one edge, so (FW271a.1) cannot be summed
over multiple ambient unit tails.  Replacing it by several heavier pure
gates loses the radix-two strictness, and their windows can overlap.  The
resulting union count has no additive strictly decreasing measure.  FW271a
is therefore a genuine local theorem and not a global closure theorem.

## 3. FW271b: pendant-unit self-complement and parity halving

Now assume the weight-one edge is a true leaf edge `a--1--b`, with `a` the
leaf.  Put `S=T-a` and, initially, define

```text
rho(v)=d_T(b,v)  (v in S),       Y={rho(v):v in S}.
```

### 3.1 Exact self-complement

Pairs retained in `S` and pairs incident with `a` partition the full
spectrum:

```text
I_N=F_S dot-union X R_b(S).                         (FW271b.1)
```

Thus

```text
Spec(S)=I_N minus (1+Y),
|Y|=n-1,                   0 in Y,
Y intersect (Y+1)=empty.                            (FW271b.2)
```

The last assertion is also actual-pair uniqueness: a positive rooted depth
`rho(v)` is owned by `{b,v}`, whereas `1+rho(u)` is owned by `{a,u}`.

With `U=T-{a,b}`, the finer retained-ambient identity is

```text
I_N=F^T_U dot-union X
    dot-union (1+X) sum_(v in U) X^rho(v).          (FW271b.3)
```

The polynomial complement is exact.  Neither `S` nor the formal factors in
(FW271b.3) are asserted to be Leech trees.

### 3.2 Exact parity split and cross rectangle

Extend `rho(v)=d_T(b,v)` to all vertices of `T`, and let `E,O` be its even
and odd parity classes.  Then `b in E`, `a in O`.  Write

```text
e=|E|,       o=|O|,       P=floor(N/2),       O'=O-{a}.
```

Taylor's parity count gives

```text
e+o=n,                       eo=ceil(N/2).          (FW271b.4)
```

Separating the even and odd coefficients of `I_N`, then dividing by two,
gives the following two exact actual-pair partitions:

```text
I_P = {d(u,u')/2:{u,u'} subset E}
      dot-union {d(v,v')/2:{v,v'} subset O'}
      dot-union {(1+rho(v))/2:v in O'},             (FW271b.5)

I_(eo) = {1+rho(u)/2:u in E}
         dot-union {(d(u,v)+1)/2:u in E,v in O'}.   (FW271b.6)
```

Equation (FW271b.6) is a complete `e x o` parity-halved cross-distance
rectangle with the `a`-row distinguished.  This is a new exact reduction.
Its entries are transformed distances, however, and the two factors do not
form a smaller rooted Leech state; no recursive closure follows from the
rectangle alone.

### 3.3 What graph halving does and does not preserve

Contract every connected component of even-weight edges of `T`.  The odd
edges form a quotient tree `Q_odd`.  In the standard distance-halving
construction, the halved graph contains the even-edge components with their
weights divided by two and, at each quotient vertex `C`, a clique on the
outside endpoints of the odd quotient edges incident with `C`.  Therefore

```text
the halved graph is a forest  iff  Delta(Q_odd)<=2. (FW271b.7)
```

The unit leaf makes the block `{a}` a leaf of `Q_odd`, but gives no control
over branching elsewhere.  Even when `Q_odd` is a path, `a` is only an
isolate or leaf in the halved forest, and its components need not themselves
have interval spectra.

This is a real boundary, not just a missing local lemma.  Calhoun and
Polhill prove that `t K_(1,3)` admits a perfect-distance forest labelling for
every `t` (**LITERATURE**: *Perfect distance forests*, Australas. J. Combin.
42 (2008), 211--222,
<https://ajc.maths.uq.edu.au/pdf/42/ajc_v42_p211.pdf>).  Thus even an arbitrary
number of star components after halving is not, by itself, contradictory.

### 3.4 Exact q=1 location of the leaf edge

Use the FW219 coordinate

```text
y(v)=N-d(x,v)                 (v in T-x).
```

The edge at `x` has weight at least `Q>=2`, so `a!=x`; leaf geometry gives
`y(b)=y(a)+1`.  Since every coordinate `0,...,Q-1` is visible and coordinate
`Q` is absent, exactly one of the following holds:

```text
visible case:    y(a)=j, y(b)=j+1,       0<=j<=Q-2;
pure-core case:  y(a)>=Q+1, y(b)>=Q+2.                   (FW271b.8)
```

In the visible case, let `c` be the order of the `b`-side of the last edge
on the path `x--b`.  The containment bound at
`d(x,b)=N-j-1` gives

```text
2<=c<=j+2.                                          (FW271b.9)
```

In the pure-core case FW270 gives `q_b=d(x,b)>=2Q+1`, equivalently

```text
Q+1<=y(a)<=N-2Q-2.                                 (FW271b.10)
```

This interval is feasible; (FW271b.10) is not an exclusion.

### 3.5 Top-graph control and small witnesses

Put `C=binom(n-1,2)` and join two vertices in `G_C` when their distance is
greater than `C`.  For every `v` different from `a,b`,

```text
d(a,v)=d(b,v)+1,
N_(G_C)(b) subset N_(G_C)(a),
|N_(G_C)(a) minus N_(G_C)(b)|<=1.                 (FW271b.11)
```

In the FW248 rectangle branch, two nonisolated vertices of this form lie on
the same Ferrers side at consecutive deficit coordinates; this reproduces
the mixed-radix factorisation rather than contradicting it.  If one is
isolated, the other has degree at most one.  A pendant cut also makes any
claim requiring common top neighbours on both cut sides vacuous.

The known controls locate the leaf pair visibly: `L3` and the `L4` path have
`j=0,c=2`; the `L4` star and `L6` have `j=1,c=3` (with `L2` the base case).
Their halvings do not recurse componentwise.  In particular `L6` produces
spectra `{1}` and `{2,...,7}`; the latter component is a star with weights
`2,3,4`, not a Leech component.  In its top graph, `a,b` have degree one and
a common neighbour while a top triangle occurs elsewhere, so false twins
and a top cycle do not collide.

At order 18, (FW271b.4) gives `{e,o}={7,11}`.  Even if one additionally
assumes the halved graph is a forest, the next Taylor split remains
arithmetically feasible:

```text
alpha(7-alpha)+gamma(11-gamma)=38
```

has, up to complements, the split `2+5` and `4+7`.  First-level or
second-level parity arithmetic therefore does not exclude order 18.

## 4. FW271c: negative full-spectrum mechanism ledger

The following entries are **OBSERVED audit verdicts** about the stated
mechanisms, not impossibility theorems for every refinement of them.

| Mechanism | Exact surviving statement | Minimal missing input / pressure control |
|---|---|---|
| Joint two-root / no-grazing | In the FW261 deficit coordinates, a named `p--r` gate gives the owner-expanded cut ledger `D_(uv)=Y_u+Z_v`; the unique `M`-owner is `{z,w}` with `Z_w=Q`. | This separately reproduces the FW265 cut ledger and FW248/FW250 top factor.  In `L6`, the translates `{5,6}` and `{9,10}` across the `0--3` cut allow the latter to graze either cutoff by one coefficient.  Missing: a named inherited cut, a two-boundary receiving tiling, and a fully charged strict potential. |
| All-digit Ferrers propagation | Complete mixed-radix stages force the marked hulls to be edge-disjoint and their gate chain to be laminar and monotone. | A scalable globally distance-distinct positive-integer comb relaxation realises arbitrary binary digit depth, constant laminar gates, and the exact top band while leaving the low spectrum sparse.  Missing: full lower-spectrum absorption or an owner-level no-grazing theorem. |
| Canonical top triangle / triple boundary | Let `w` be the canonical endpoint of the unique owner `{z,w}` of `M=N-Q`.  In the favourable triangle case the three deficits are `(0,delta,Q)` and the marked Steiner-tripod arms are `(N+Q-delta)/2`, `(N+delta-Q)/2`, `(N-delta-Q)/2`; in that subcase `w` is a true leaf. | The owner theorem does not force canonical `w` into the triangle (and outside that subcase does not force `w` to be a true leaf).  Deleting the three marked terminals leaves unbounded attachments and a forbidden diagonal at a shared gate, not three independent smaller states.  `L4`/`L6` and scalable integer relaxations satisfy the count, span, and parity ledgers.  Missing: the owner of the diagonal hole and a full-low-spectrum inequality controlling isolates/cycle rank. |
| Tree covariance kernel | Section 4.1 gives exact determinant and inverse formulas. | The off-diagonal multiset does not locate tree edges.  The `L4` star and path have the same full spectrum but different edge sets and determinant factors.  Missing: pair/triple-to-edge owner localisation or a same-type punctured-spectrum state after deletion. |
| Signed derivatives at `-1` | Section 4.2 gives the exact parity-imbalance cut identity. | Signs cancel, and a leaf deletion introduces an unbounded rooted signed-depth moment.  Higher derivatives retain multi-edge owner incidence.  The result refines Taylor arithmetic but supplies no monotone state. |
| Positive-`q` Hosoya inequality | Section 4.3 gives the exact nonnegative LCA-slack decomposition. | Deep-LCA slack is bounded by the same rooted branch/ball pair capacities already present; no theorem forces a positive density of pairs to have a linearly deep named LCA.  The five small witnesses allow both zero and positive slack. |
| Finite group characters | All characters of the actual cut-owner indicator give Fourier inversion/Parseval; only the order-two character removes the LCA phase. | `X=i` and higher characters retain the factor from `-2 depth(LCA)`.  A Taylor-compatible order-six modular control survives the whole 2-adic character tower while having actual diameter `23>15`.  Missing: an archimedean, no-wrap, named-window owner theorem. |
| Ma--Yi path packing | The positive-density gap for disjoint fixed-`t` Golomb-ruler difference packings, `t>=6`, applies to pair-disjoint collinear `t`-vertex path blocks (**LITERATURE**, Ma--Yi, *An Almost-Covering Threshold for Golomb-Ruler Difference Packings*, arXiv:2608.13739, 2026). | Such blocks account for at most a constant times the rooted ancestor-pair count `A_r`; a balanced binary tree has `A_r=O(n log n)`, so almost all `Theta(n^2)` pairs remain noncollinear.  Cross-branch sums can tile intervals.  Missing: a decomposition covering more than about `N/2` actual pairs by collinear blocks; pure topology cannot provide it. |

### 4.1 Covariance kernel: exact formulas and decisive control

For `0<q<1`, put

```text
K(q)_(uv)=q^d(u,v),                 rho_e=q^w_e.
```

Direct leaf elimination gives

```text
det K(q)=product_(e in E(T)) (1-rho_e^2),          (FW271c.1)
```

and the inverse is supported exactly on the tree:

```text
K(q)^(-1)_(uv)=-rho_e/(1-rho_e^2)   if e=uv,
K(q)^(-1)_(uv)=0                    if uv is not an edge,
K(q)^(-1)_(uu)=1+sum_(e incident u) rho_e^2/(1-rho_e^2). (FW271c.2)
```

These identities are exact for every positive weighted tree.  They do not
turn the Leech off-diagonal multiset `q,q^2,...,q^N` into its placement in
the matrix.  The `L4` star and `L4` path both have pair-distance spectrum
`I_6`, but their edge-weight multisets are respectively `{1,2,4}` and
`{1,2,3}`.  Hence their determinants, cyclotomic zeros, eigenvalues, and
inverse zero patterns differ despite the identical off-diagonal multiset.

The `q->0` coefficients recover only the already known owners of `1`, `2`
and the first branching alternative at `3`.  At `q=-1`, every determinant
factor vanishes and only its Taylor data remain.  Fischer, matching, and PSD
inequalities likewise forget the named actual-pair owner needed for a
collision or descent.  This route is stopped at (FW271c.1)--(FW271c.2).

### 4.2 Signed first derivative: exact cut identity

Fix a root and set

```text
chi(v)=(-1)^d(root,v),       R=sum_v chi(v).
```

For each edge `e`, let `B_e` be the sum of `chi` on either one of its cut
sides.  Expanding each path distance edge by edge gives

```text
sum_{{u,v}} d(u,v)(-1)^d(u,v)
 =sum_e w_e B_e(R-B_e)
 =(-1)^N ceil(N/2).                                (FW271c.3)
```

The last equality uses `F_T=I_N`.  This is a genuine parity-refined Wiener
identity, but its edge terms have both signs and may vanish.  Rooted `L4`
star/path controls reach the same target with different imbalance profiles.
Higher derivatives count paths using several named edges and therefore add,
rather than remove, the missing owner provenance.  No strict potential is
obtained.

### 4.3 Positive-q Hosoya decomposition

For a rooted weighted tree `U`, let `t_u` be the root depth and

```text
R_U(q)=sum_u q^t_u.
```

The LCA formula gives the exact decomposition, for `0<q<1`,

```text
F_U(q)-(R_U(q)^2-R_U(q^2))/2
 =sum_{u<v} q^(t_u+t_v)
             (q^(-2t_(LCA(u,v)))-1)>=0.           (FW271c.4)
```

The slack is supported precisely on pairs whose LCA is below the root.  Of
these, the pairs satisfying `t_(LCA(u,v))>=h` lie together in one descendant
component below the level-`h` cut.  If those component orders are `s_i`,
their number is at most

```text
sum_i binom(s_i,2),
```

This is the same branch/ball capacity already used in the q=1 route;
(FW271c.4) does not give
a lower bound for it.  Taking `q=exp(-c/N)` turns shallow LCA depth into the
ordinary moment scale, while `q->0` returns the low-owner forcing.  Thus the
positive evaluation is dominated by existing ball bounds unless a new
named deep-LCA density theorem is supplied.

### 4.4 Finite characters: exact cut transform

For an edge `e=A|B` of weight `w`, rooted at its two endpoints, the exact cut
polynomial is

```text
F_T(X)=F_A(X)+F_B(X)+X^w R_A(X)R_B(X).             (FW271c.5)
```

Let `k=N+1` and let `zeta` be a primitive `k`-th root.  A Leech spectrum
gives `F_T(zeta^j)=-1` for `1<=j<k`.  Since the cross term in (FW271c.5) is
the indicator of `ab` distinct residues, Parseval gives

```text
sum_(j=1)^(k-1) |R_A(zeta^j)|^2 |R_B(zeta^j)|^2
 =ab(k-ab),                  a=|A|, b=|B|.         (FW271c.6)
```

Using every character simply Fourier-inverts the same actual cross-owner
indicator.  In rooted LCA form, the character version of (FW271c.4) retains
`zeta^(-2 depth(LCA))`; only `zeta=-1` removes that phase and returns Taylor.
The five known witnesses pass (FW271c.5)--(FW271c.6) on all 14 of their cuts.
An order-eight modular control over `Z_29` passes all group/cut identities but
wraps (`68>28`), and the stronger Taylor-compatible order-six control over
`Z_16` has unwrapped diameter `23>15` while surviving the entire 2-adic
character tower.  These are modular pressure controls, not Leech witnesses.

### 4.5 Top-graph spectrum check

The FW246 top graph has `n-1` edges; its nonisolated part is connected in the
Ferrers branch, and its cycle rank equals its number of isolates.  A shared
defect-ball vertex supplies an isolate and hence a cycle.  The triangle gate
and the three residual Ferrers factors do not force further isolates, and
they do not upper-bound the cycle rank: unmarked attachments can absorb the
missing low owners.  This is the precise full-spectrum gap in the
triple-boundary proposal, rather than a missing count of top edges.

## 5. Stop verdict and successor boundary

FW271 advances FW270 in two exact ways: the pure-`H` unit cut now has a
strict product/window theorem with high/low refinements, and a pendant unit
edge now has the self-complement, parity rectangle, and visible/pure-core
dichotomy.  None supplies a same-type proper contextual state or an explicit
strictly decreasing fully owner-charged measure.

The strongest currently identified **UNVERIFIED** reopening inputs are:

1. exclude the consecutive pure-core coordinates `y(a),y(a)+1` joined by a
   pendant unit edge using full LCA owner provenance;
2. prove all-level 2-adic stability together with bounded-context closure of
   the resulting perfect-distance forest; or
3. prove a named lower-spectrum absorption/no-grazing theorem that charges
   the Ferrers or triangle hole to a proper inherited receiving state.

First-step halving, another finite prefix, a positive-kernel inequality, or
another count/span bound does not meet this gate.  Consequences proposed from
the distance matrix beyond (FW271c.1)--(FW271c.2), and consequences proposed
from the parity cross rectangle beyond (FW271b.5)--(FW271b.6), remain
**UNVERIFIED successor work under review** and are deliberately not part of
FW271.

The first such successor is now frozen separately as FW272.  For a pendant
unit edge rooted at its nonleaf endpoint, write `R,S` for the half-scaled
even/odd root-depth sets and `L` for the mixed-parity LCA-depth matrix.
The **OBSERVED all-order** result is

```text
L identically zero  =>  |E|<=3.
```

It follows from the exact cross rectangle and a local interval-block
classification, not from another parity count.  Taylor's **LITERATURE**
class sizes therefore force a positive mixed-LCA entry in every
pendant-unit candidate of order at least eleven, including both q=1
locations at order eighteen.  This does not contradict the candidate: the
positive laminar block still lacks an **UNVERIFIED** collision or
bounded-context inheritance theorem.  FW272 excludes no order and leaves
G18 **UNVERIFIED**.  Complete theorem, proof and trust boundary:
`docs/q1-pendant-mixed-lca.md`.

The main frozen antecedents are:

```text
docs/q1-low-owner-localization.md
docs/q1-pure-tail-stop.md
docs/q1-two-root-closure-sprint.md
docs/q1-new-mechanism-sprint.md
docs/q1-directed-hole-sprint.md
data/known_leech_trees.json
variants/results/mod_cpsat_8.jsonl
variants/RESULTS.md
theory-lab/topwindow/verify_q1_trunk_cut_ledger.py
```

No order exclusion, no new finite search, and no G18 conclusion follows.
