# The first-positive edge cut and its exact stop (FW276)

FW276 cuts at the edge localised by FW274 and keeps the actual owner of
every coefficient.  It is an analytic refinement of the pendant-unit branch,
not a new search and not an order exclusion.

* **OBSERVED:** the first positive mixed-LCA owner is an edge `f=pc` of
  weight `w=2tau+1<=21`; cutting it gives exact, owner-disjoint product
  formulae for both parity sheets.
* **OBSERVED:** the root side owns the complete odd block below `tau`, while
  the two internal sides together own the complete even block through
  `tau+1`.
* **OBSERVED:** immediately before `f` is inserted in Find-Next order, the
  light-edge component containing `c` has only even edges.  After halving it
  is a distinct-distance weighted tree of order at most `tau+1<=11`.
* **UNVERIFIED:** this bounds that one light component, not the whole
  descendant side of the cut.  Heavier edges can attach arbitrarily many
  further vertices.  The cut identities and their order-eighteen capacity
  inequalities do not force a collision, absorption, or smaller Leech state.

The missing successor is an owner-labelled no-grazing or absorption theorem
at this cut.  No such theorem is proved here.  FW276 has no verifier or
certificate, proves no order exclusion, and leaves G18 **UNVERIFIED**.

## 1. Pendant setting and the first positive edge

Let `T` be a Leech tree of order `n>=11`.  Its unordered-pair distances are
distinct and equal

```text
I_N={1,...,N},                         N=binom(n,2).
```

Suppose that the weight-one edge is the pendant edge `a--1--b`, with `a`
the leaf, and root `T` at `b`.  Put

```text
rho(v)=d(b,v),
E={v:rho(v) even},                     O={v:rho(v) odd},
K=|E||O|=ceil(N/2),                    P=floor(N/2).
```

For `u in E` and `v in O`, use the FW274 transformed coordinate

```text
z_(u,v)=(d(u,v)-1)/2,
L_(u,v)=rho(LCA_b(u,v)),
tau=min{z_(u,v):L_(u,v)>0}.
```

FW272 guarantees that this set is nonempty under the stated order and
pendant-unit hypotheses.  Thus `tau` is well defined, and FW274 proves

```text
1<=tau<=10.                                         (FW276.1)
```

Its unique owner is one odd edge not incident with `b`.  Orient that edge
away from the root and write

```text
f=pc,                       p the parent of c,
w=weight(f)=2tau+1<=21.                            (FW276.2)
```

Cutting `f` leaves two vertex sets.  Let `A` be the component containing
`p`, hence also `b` and `a`, and let `B` be the descendant component
containing `c`.

The facts that `a in A` and `f` is not incident with `b` will both matter.
In particular neither endpoint of `f` is `a` or `b`.

## 2. Rooted cut polynomials

Measure local distance from the endpoint belonging to each side:

```text
alpha(x)=d(p,x)       (x in A),
beta(y)=d(c,y)        (y in B).
```

For `i in {0,1}`, define

```text
A_i(X)=sum_(x in A, alpha(x)=i mod 2) X^((alpha(x)-i)/2),
B_i(X)=sum_(y in B, beta(y)=i mod 2)  X^((beta(y)-i)/2). (FW276.3)
```

The coefficients retain labelled vertices.  Equal local depths cannot occur:
two such vertices would give the same global pair distance from `p` or `c`.
Thus each rooted polynomial has zero-one coefficients.

For internal unordered pairs, let

```text
O_A(X)=sum_({x,x'} subset A, d(x,x') odd) X^((d(x,x')-1)/2),
O_B(X)=sum_({y,y'} subset B, d(y,y') odd) X^((d(y,y')-1)/2),

E_A(X)=sum_({x,x'} subset A, d(x,x') even) X^(d(x,x')/2),
E_B(X)=sum_({y,y'} subset B, d(y,y') even) X^(d(y,y')/2).
                                                               (FW276.4)
```

Also write

```text
J_[r,s](X)=X^r+X^(r+1)+...+X^s.
```

Every path from `A` to `B` crosses `f`, so

```text
d(x,y)=alpha(x)+w+beta(y).                         (FW276.5)
```

If the two local parities agree, this distance is odd.  If they differ, it
is even.  Substitution of `w=2tau+1` into (FW276.5) gives the two exact
coefficientwise identities

```text
J_[0,K-1]
 = O_A+O_B+X^tau A_0 B_0+X^(tau+1) A_1 B_1,       (FW276.6)

J_[1,P]
 = E_A+E_B+X^(tau+1)(A_0 B_1+A_1 B_0).            (FW276.7)
```

These are identities in the integer polynomial ring, not merely support
inclusions.  Every summand names the location of its actual owner pair.
Global distance uniqueness implies that every product coefficient is zero or
one and that all displayed summands are pairwise support-disjoint.

For example, if `alpha(x)=2r` and `beta(y)=2s`, then the cross odd exponent
is `r+s+tau`.  If both local distances are odd, the exponent is
`r+s+tau+1`.  The two opposite-parity cases both have even half-index
`r+s+tau+1`.  This proves (FW276.6)--(FW276.7) with their owner provenance.

## 3. The forced low odd block

Every odd internal pair in `B` has endpoints of opposite root parity.  Its
rooted LCA lies in the descendant subtree `B`, at depth at least `rho(c)>0`.
By the definition of `tau`, its transformed odd index is at least `tau`.

It cannot have index exactly `tau`, because that distance is already owned
by the distinct pair `{p,c}`.  Therefore

```text
supp(O_B) subset [tau+1,K-1].                       (FW276.8)
```

The cross odd terms in (FW276.6) start at `tau`.  Their coefficient at
`tau` is exactly the pair `{p,c}`, supplied by the constant terms of
`A_0 B_0`; every other cross owner has larger index.  Hence

```text
[X^j]O_A=1                for 0<=j<tau,
[X^tau](X^tau A_0B_0)=1,
[X^j](O_B+cross terms)=0  for 0<=j<tau.             (FW276.9)
```

Thus `O_A` owns the exact complete low odd block `J_[0,tau-1]`, while `f`
alone owns the next odd coefficient.  Statement (FW276.9) is a truncation;
`O_A` may also have owners above `tau`.

## 4. The forced low even block

The only pair at distance one is `{a,b}`.  Since neither `p` nor `c` is
`a` or `b`, neither endpoint of `f` has a vertex at local distance one.
Every positive odd local distance from `p` or `c` is therefore at least
three.

A cross even pair in (FW276.7) uses one odd local distance.  Its actual
distance is at least

```text
w+3=2tau+4,
```

and hence its even half-index is at least `tau+2`.  It follows that

```text
[X^j](E_A+E_B)=1          for 1<=j<=tau+1,
[X^j](cross even terms)=0 for 1<=j<=tau+1.         (FW276.10)
```

So the two sides internally own the complete even block
`J_[1,tau+1]`.  The cut identities do not decide how that block is divided
between `A` and `B`.

## 5. Necessary cut capacities

Put

```text
a_i=A_i(1),                       b_i=B_i(1).
```

The vertices `p,c` give `a_0,b_0>=1`.  Because `A` also contains the unit
edge `a--b`, it contains both local parities, so `a_1>=1`; `b_1` may be zero.

Counting the owner classes in Sections 3--4 gives

```text
a_0 a_1 >= tau,                                      (FW276.11)

binom(a_0,2)+binom(a_1,2)+binom(b_0,2)+binom(b_1,2)
  >= tau+1,                                           (FW276.12)

a_0 b_0+a_1 b_1 <= K-tau,                            (FW276.13)
a_0 b_1+a_1 b_0 <= P-tau-1.                          (FW276.14)
```

In particular `A_1B_0` is nonempty.  Any one of its owner indices is at
least `tau+2` and at most `P`; hence `P>=tau+2` and the right-hand side of
(FW276.14) is positive.

Every exponent in `B_1` is at least `tau+1`: it is the transformed odd
index of the positive-LCA pair from `c` to that vertex and cannot duplicate
`f`.  Every exponent in `A_1` is at least one because `p` has no
distance-one neighbour.  The available sheet lengths therefore also give

```text
a_0 b_1 <= max(0,P-2tau-1),
a_1 b_1 <= max(0,K-2tau-3),
b_0 b_1 <= max(0,K-tau-1).                          (FW276.15)
```

When `b_1` is nonempty, the corresponding support itself makes the relevant
untruncated right-hand side positive; the `max` convention also states the
zero-class cases correctly.

These inequalities are necessary consequences of exact owner locations.
They contain no tree-realisation or LCA-laminarity converse.

## 6. Find-Next normal form below `f`

Let `F_<w` be the forest formed by all edges of weight strictly less than
`w`.  Since every distance below `w` uses only edges lighter than `w`, this
forest realizes every value in `I_[1,w-1]`.  It cannot realize `w`, because
the edge `f` already owns that distance.  Thus `f` is exactly the next edge
selected by the Find-Next-Weight rule.

FW274 also proves that every lighter odd edge is incident with `b`.  Let
`C_c` be the connected component of `F_<w` containing `c`.  The tree edge
`f` is absent, so `b` is not in `C_c`.  Therefore every edge in `C_c` has
even weight.

Divide all those weights by two.  Pair distances inside `C_c` remain
distinct, and its edge weights become distinct positive integers at most
`tau`.  If `s=|C_c|`, its `s-1` edges consequently satisfy

```text
s-1<=tau,
|C_c|<=tau+1<=11.                                  (FW276.16)
```

This is the exact finite light-component normal form exported by FW276.
It does **not** say

```text
|B|<=tau+1.
```

Vertices of the full descendant side `B` may be separated from `c` in
`F_<w` by edges of weight greater than `w`, and those later attachments are
not bounded by (FW276.16).  The halved component is only a
distinct-distance weighted tree; its distance spectrum need not be an
initial interval.

The same even-edge argument applies to every light component not containing
`b`, but it still bounds components rather than full sides.  Moreover
`F_<w` has at most `w-1=2tau` edges, so its active light signature is finite.

There is a separate root-component consequence.  Let `C_b` be the component
of `F_<w` containing `b`, and let its two root-parity class orders be `r,s`.
All `tau` odd owners of transformed indices `0,...,tau-1` use only light
edges.  Every light odd edge is incident with `b`, so all those owner paths
lie in `C_b`.  Hence

```text
r s>=tau.                                           (FW276.17)
```

For `tau=10`, an order-six component has parity product at most nine, so
`|C_b|>=7`.  Since `C_b subset A`, at order eighteen this gives the distinct
side consequence `|A|>=7` and `|B|<=11`.  It does not identify `B` with
`C_c` or bound the later heavy attachments independently of the fixed total
order.

## 7. Why order-eighteen capacity does not close

At order eighteen,

```text
N=153,                     K=77,                   P=76.
```

Even at the strongest value `tau=10`, the formal local-parity split

```text
(a_0,a_1;b_0,b_1)=(2,5;6,5)                        (FW276.18)
```

passes every displayed capacity inequality.  It also matches Taylor's
`7|11` parity sizes: according to the parity of `p`, the two global class
orders are

```text
a_0+b_1=7,                     a_1+b_0=11.
```

Numerically, the tests are

```text
a_0a_1=10,
sum same-parity internal capacities=1+10+15+10=36>=11,
a_0b_0+a_1b_1=37<=67,
a_0b_1+a_1b_0=40<=65,
a_0b_1=10<=55,
a_1b_1=25<=54,
b_0b_1=30<=66.                                     (FW276.19)
```

This is a formal integer capacity control, not a tree or a Leech witness.
It shows only that (FW276.11)--(FW276.17), even together with the exact
Taylor class sizes, do not exclude order eighteen.

## 8. Conditional q=1 location

Retain the q=1 visible notation

```text
d(x,v_j)=N-j,                         0<=j<Q.
```

If `x in A` and a visible vertex `v_j in B`, its path crosses `f`, so

```text
d(c,v_j)=N-j-d(x,p)-w.                              (FW276.20)
```

Consequently, if a consecutive index block

```text
j_0,j_0+1,...,j_1
```

lies in `B`, then the corresponding rooted distances from `c` form the
reflected consecutive interval

```text
N-d(x,p)-w-j_1, ..., N-d(x,p)-w-j_0.               (FW276.21)
```

This is only a conditional location formula.  Nothing in FW274 or in the
cut identities forces `x` to lie on the stated side, forces even one chosen
visible vertex across `f`, or forces the indices across `f` to be
consecutive.  In particular an `H--H` edge lying wholly inside the q=1 pure
core may cut off no visible vertex at all.  FW276 proves no relation `w>=Q`;
the established edge bound is the upper bound `w<=21`.

## 9. Exact stop and reopening gate

Equations (FW276.6)--(FW276.12) control a bounded initial part of the two
parity sheets.  The cross products may nevertheless contain `Theta(n^2)`
owner pairs, while later heavy attachments can enlarge either side without
changing the finite component in (FW276.16).  This is the same unbounded
pure-child freedom isolated in FW273, now expressed at the first positive
edge cut.

The next theorem must retain actual owners.  A sufficient successor would
prove one of the following **UNVERIFIED** alternatives:

1. all but `O(w)` shifted cross-owner rows are absorbed by a named complete
   internal even block or terminal suffix, forcing a collision unless a
   proper exact state peels off; or
2. only `O(w)` rows can graze the boundary of that named interval, leaving a
   strictly smaller owner-labelled state; or
3. in the q=1 specialisation, a nonempty quantitatively large consecutive
   block of visible indices is forced across `f`, so that (FW276.21) becomes
   an inherited rooted interval rather than an isolated formula.

A cardinality estimate without a named receiving interval does not pass this
gate.  Nor does a statement about the light component `C_c` that silently
replaces it by the full side `B`.

FW276 therefore freezes the exact cut algebra, the low owner blocks, and the
finite Find-Next component, and stops there.  It has no computational input,
no verifier, no certificate, no SAT witness, and no order exclusion.  The
nonpendant-unit branch remains governed separately by FW275.  G18 remains
**UNVERIFIED**.
