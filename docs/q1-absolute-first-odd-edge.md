# An absolute first odd-edge bound (FW274)

FW274 sharpens the size-dependent first-positive estimate in FW273 to an
absolute constant.  It retains the pendant-unit hypothesis and the full
Leech distance-distinctness antecedent.

* **OBSERVED:** if a pendant-unit Leech tree has a positive mixed LCA, its
  first positive transformed coordinate satisfies

  ```text
  tau<=10.
  ```

* **OBSERVED:** the owner of that coordinate is a single odd edge not
  incident with the root `b`, of weight

  ```text
  w=2tau+1<=21.
  ```

* **OBSERVED:** FW272 supplies the positive-LCA antecedent for every
  pendant-unit candidate of order at least eleven.  Thus every such
  candidate contains an odd edge of weight at most `21` not incident with
  the root `b`.
* **UNVERIFIED:** this absolute localisation does not force a repeated
  distance, absorb the terminal pure child, or produce a smaller Leech
  state.  It says nothing about a nonpendant unit edge and does not exclude
  any order.  In particular G18 remains **UNVERIFIED**.

The proof is analytic and has no finite-search dependency.  A frozen
deterministic replay checks its finite rooted-parent kernel, every named
collision, and the sharp eight-vertex pressure control:

```text
theory-lab/topwindow/verify_q1_absolute_first_odd_edge.py
theory-lab/topwindow/results/q1_absolute_first_odd_edge_certificate.json
```

The replay is support for the written proof, not a Leech search or an
independent proof of the all-order theorem.

**Frozen successor.**  FW276 cuts at the edge `f` found here.  Its two
parity-sheet identities, exact low owner blocks and Find-Next light-component
normal form are in `docs/q1-first-positive-edge-cut.md`.  They bound only the
light component below `f`, not its full descendant side, and do not close
G18.

## 1. Setting and the exact first hole

Let `T` be a Leech tree: its positive integer edge weights give distinct
unordered-pair distances exactly

```text
I_N={1,...,N},                         N=binom(n,2).
```

Suppose that its weight-one edge is the pendant edge `a--1--b`, with `a`
the leaf, and root the tree at `b`.  Put

```text
rho(x)=d(b,x),
E={x:rho(x) is even},                  O={x:rho(x) is odd},
R_u=rho(u)/2                           (u in E),
S_v=(rho(v)-1)/2                       (v in O),
L_(u,v)=rho(LCA_b(u,v)),
z_(u,v)=R_u+S_v-L_(u,v)=(d(u,v)-1)/2.
```

Thus `b=e_0` has `R` coordinate zero and `a=o_0` has `S` coordinate
zero.  Root depths are distinct, since equal root depths would repeat a
distance from `b`; hence `R` and `S` are sets.  The odd actual owners give

```text
{z_(u,v):u in E,v in O}={0,...,|E||O|-1},         (FW274.1)
```

with every coordinate occurring once.

Assume that `L` is not identically zero and define

```text
tau=min{z_(u,v):L_(u,v)>0}.                        (FW274.2)
```

The unique owner of `z=0` is `{b,a}` and has `L=0`, so `tau>=1`.  For

```text
c_m=#{(u,v) in E x O:R_u+S_v=m},
```

FW273's first-hole argument, repeated here for completeness, gives

```text
c_m=1                  for 0<=m<tau,
c_tau=0.                                             (FW274.3)
```

Indeed, a raw owner at `m<tau` with positive LCA would have actual
coordinate `m-L<m<tau`.  Therefore the unique actual owner of `m` has
`L=0` and raw sum `m`, proving existence and uniqueness.  The actual owner
of `tau` with positive LCA has raw sum greater than `tau`.  Any separate raw
owner at `tau` would either have `L=0`, duplicating the actual owner of
`tau`, or have `L>0`, creating an earlier positive coordinate.  This proves
the hole.

The full Leech distance-distinctness hypothesis is used below.  The odd
rectangle (FW274.1) alone does not justify the same-parity collisions.

## 2. Prefix exhaust and the extended next coordinate

Suppose first that `1 in R`.  Let `[0,k-1]` be the maximal initial
consecutive block of `R`:

```text
[0,k-1] subset R,                    k notin R.
```

Define the next root-even coordinate in the extended nonnegative integers,

```text
Q_0=min(R-[0,k-1])       if that set is nonempty,
Q_0=+infinity            otherwise.                 (FW274.4)
```

This convention is essential: it includes the cases in which the root-even
class consists only of its initial block.  Statements such as `Q_0>=tau`
below include `Q_0=+infinity`.

Set `H=min(Q_0,tau)`, with the evident extended-integer meaning.  For every
`m<H`, no `R` coordinate outside `[0,k-1]` can contribute to `c_m`.
Writing `s_j` for the indicator of `j in S`, and putting `s_j=0` for
`j<0`, equation (FW274.3) becomes

```text
s_m+s_(m-1)+...+s_(m-k+1)=1.                       (FW274.5)
```

Here `s_0=1`.  Subtracting the equation at `m-1` from that at `m` first
gives `s_1=...=s_(k-1)=0` and then `s_m=s_(m-k)`.  Consequently

```text
R intersect [0,H-1]=[0,k-1],
S intersect [0,H-1]={qk:qk<H}.                     (FW274.6)
```

This is the prefix-exhaust statement, not merely a list of forced
coordinates.  Every vertex at root depth less than `2H` is one of the
vertices listed in (FW274.6): an even depth is `2r` with `r<H`, and an odd
depth is `2s+1` with `s<H`.  Therefore, when a rooted ancestor is enumerated
below, there is no unlisted vertex at an intermediate depth.  Interior
points of a weighted edge are not vertices and cannot be LCAs.

## 3. The branch `1 notin R`

Assume `1 notin R`.  If there were a least

```text
q in R intersect [1,tau-1],
```

then `q>=2`, and (FW274.3) below `q` would force
`[0,q-1] subset S`.  The two distinct actual pairs

```text
{b,e_q},                         {a,o_(q-1)}
```

would both have distance `2q`.  Hence no positive `R` coordinate is below
`tau`, and the prefix forces

```text
[0,tau-1] subset S.                                  (FW274.7)
```

The corresponding `tau` odd vertices have root depths
`1,3,...,2tau-1`.  Their `binom(tau,2)` same-parity distances are distinct
positive even integers.  After division by two they are distinct positive
integers at most

```text
((2tau-3)+(2tau-1))/2=2tau-2.
```

Thus

```text
binom(tau,2)<=2tau-2,
```

which gives `tau<=4` (with `tau=1` included).  This settles the branch
without assuming that `R` has any positive coordinate.

## 4. The initial radix is two or three

Now assume `1 in R`.  Since `S` contains zero, the raw hole says
`tau notin R`; hence `k<=tau`.  Also `k>=2`.

If `k>=4`, the vertices `e_1,e_2,e_3` have root depths `2,4,6`.  The LCA
of `e_1,e_2` can have only depth `0,1,2`.  The depth-one vertex is the true
leaf `a` and cannot be their LCA.  LCA depth zero gives distance six,
repeating `d(b,e_3)`, while LCA depth two gives distance two, repeating
`d(b,e_1)`.  Therefore

```text
k in {2,3}.                                           (FW274.8)
```

There are two exhaustive cases: no later `R` coordinate lies below `tau`
(`Q_0>=tau`, including `Q_0=+infinity`), or `Q_0<tau`.

## 5. No later root-even coordinate below the hole

Assume `Q_0>=tau` and put

```text
t=ceil(tau/k).
```

The prefix-exhaust identity (FW274.6) says that the odd lattice vertices

```text
o_0,o_k,...,o_((t-1)k)                              (FW274.9)
```

all exist and are the only odd root coordinates below `tau`.  There are no
later even root coordinates below `tau` either.

### 5.1 Radix three

Let

```text
v_i=o_(3i),              rho(v_i)=6i+1.
```

Thus `v_0=a`.  The vertices `e_1,e_2` have depths two and four.  They must
lie in different root branches: if `e_2` descended from `e_1`, their
distance would be two, repeating `d(b,e_1)`.

If `v_1` exists, prefix exhaust leaves only `b,e_1,e_2` as possible
nonleaf shallow ancestors.  Descending from `e_1` or `e_2` gives,
respectively,

```text
d(e_1,v_1)=5=d(a,e_2),
d(e_2,v_1)=3=d(a,e_1).
```

Hence `v_1` lies in a third root branch.  If `v_2` exists, its only
nonroot ancestor candidates are `e_1,e_2,v_1`, and they give

```text
d(e_1,v_2)=11=d(e_2,v_1),
d(e_2,v_2)= 9=d(e_1,v_1),
d(v_1,v_2)= 6=d(e_1,e_2),
```

respectively.  Therefore `v_2` lies in a fourth root branch.  If `v_3`
also existed, the two root-separated pairs would satisfy

```text
d(a,v_3)=20=d(v_1,v_2),
```

a contradiction.  Thus `t<=3`, and

```text
tau<=3t<=9                 when k=3,Q_0>=tau.       (FW274.10)
```

### 5.2 Radix two

Let

```text
u_i=o_(2i),              rho(u_i)=4i+1.
```

Thus `u_0=a`.  The vertex `u_1` cannot descend from `e_1`, since then
`d(e_1,u_1)=3=d(a,e_1)`; it lies in a separate root branch.

Suppose `t>=4`, so that `u_1,u_2,u_3` exist.  Prefix exhaust leaves
`b,e_1,u_1` as the possible deepest shallow ancestors of `u_2`.  The first
two choices collide:

```text
u_2 below e_1:       d(e_1,u_2)= 7=d(e_1,u_1),
u_2 below b:         d(u_1,u_2)=14=d(a,u_3).
```

Therefore `u_2` descends from `u_1`.

Suppose further that `t>=5`, so `u_4` exists.  The possible deepest shallow
ancestors of `u_3` are `b,e_1,u_1,u_2`.  All but `u_1` collide:

```text
u_3 below e_1:       d(e_1,u_3)=11=d(e_1,u_2),
u_3 below b:         d(u_1,u_3)=18=d(a,u_4),
u_3 below u_2:       d(u_2,u_3)= 4=d(u_1,u_2).
```

Thus `u_3` also descends from `u_1`, in a branch separate from `u_2`.
Now enumerate the possible deepest shallow ancestors of `u_4`:

```text
u_4 below e_1:       d(e_1,u_4)=15=d(e_1,u_3),
u_4 below u_1:       d(u_1,u_4)=12=d(u_2,u_3),
u_4 below u_2:       d(u_2,u_4)= 8=d(u_1,u_3),
u_4 below u_3:       d(u_3,u_4)= 4=d(u_1,u_2).
```

The only remaining possibility is a new root branch.  If `u_5` existed,
this forced placement would give

```text
d(a,u_5)=22=d(u_1,u_4).
```

Consequently `t<=5`, and

```text
tau<=2t<=10                when k=2,Q_0>=tau.       (FW274.11)
```

The ancestor lists above are exhaustive by (FW274.6); phrases such as
"below `u_i`" mean that the displayed vertex is the deepest possible
listed ancestor, not that an unlisted weighted-edge point is a vertex.

## 6. A later root-even coordinate below the hole

Assume `Q_0<tau`.  Apply prefix exhaust with `H=Q_0`.  If
`Q_0=qk+r`, `0<r<k`, then the raw coordinate `Q_0` has both owners

```text
Q_0+0,                         r+qk,
```

contrary to `c_(Q_0)=1`.  Therefore

```text
Q_0=tk,                 t>=2,
{0,k,...,(t-1)k} subset S.                         (FW274.12)
```

The equality `Q_0+k=tau` is impossible because `Q_0 in R` and `k in S`
would give a raw owner of the hole.  If `Q_0+k<tau`, uniqueness at
`Q_0` first excludes `Q_0 in S`.  For `1<=j<k`, the base representation

```text
Q_0+k=Q_0+k
```

uses `Q_0 in R,k in S`, while `Q_0+j in S` would give the second
representation `(k-j)+(Q_0+j)`, with `k-j in R`.  Uniqueness at
`Q_0+k` therefore excludes every remaining `S` coordinate through
`Q_0+k-1`.  Covering `Q_0,Q_0+1,...,Q_0+k-1` successively can then use
only the zero coordinate of `S`, and forces

```text
[Q_0,Q_0+k-1] subset R.                            (FW274.13)
```

For `k=2`, the LCA of `e_1,e_(Q_0)` is either `b` or `e_1`; (FW274.12)--
(FW274.13) then give, respectively,

```text
d(e_1,e_(Q_0))=2Q_0+2=d(b,e_(Q_0+1)),
d(e_1,e_(Q_0))=2Q_0-2=d(a,o_(Q_0-2)).
```

For `k=3`, `e_1,e_2` are root-separated.  A root LCA for
`e_1,e_(Q_0)` repeats `d(b,e_(Q_0+1))`, so `e_(Q_0)` would have to
descend from `e_1`; its root LCA with `e_2` then repeats
`d(b,e_(Q_0+2))`.  Both radices are impossible.  We have proved

```text
Q_0+k>tau,
tau<=Q_0+k-1=(t+1)k-1.                            (FW274.14)
```

The lattice ancestor arguments of Section 5 remain valid below `Q_0`:
the new vertex `e_(Q_0)` is deeper than every lattice vertex used there,
and (FW274.6) still exhausts every shallower root coordinate.

For `k=3`, the `v_3` collision gives `t<=3`, initially leaving only
`tau<=11`.  For `k=2`, the `u_5` collision gives `t<=5`.  The extreme
`k=2,t=5` would have `Q_0=10`.  The LCA of `e_1,e_10` is either `e_1`
or `b`, and the two cases give

```text
d(e_1,e_10)=18=d(a,u_4),
d(e_1,e_10)=22=d(u_1,u_4),
```

respectively.  Hence `t<=4` for `k=2,Q_0<tau`, and then `tau<=9`.

It remains only to exclude the extremal possibility

```text
k=3,        t=3,        Q_0=9,        tau=11.      (FW274.15)
```

Here the exhausted prefix gives

```text
R intersect [0,9]={0,1,2,9},
S intersect [0,8]={0,3,6}.
```

The representation `9+0` and `c_9=1` also exclude `9 in S`.  At raw coordinate ten all
other decompositions have already been excluded, so the exact identity is

```text
c_10=1_(10 in R)+1_(10 in S)=1.                   (FW274.16)
```

If `10 in S`, then `1 in R` makes `1+10` a raw owner at eleven,
contradicting `c_tau=c_11=0`.  Therefore `10 in R`.  But Section 5.1 has
already forced `v_1=o_3` and `v_2=o_6` into distinct root branches, so

```text
d(b,e_10)=20=d(v_1,v_2).
```

This final contradiction excludes (FW274.15).

Combining Sections 3--6 proves the absolute theorem

```text
tau<=10.                                            (FW274.17)
```

For reference, the complete case ledger is

```text
1 notin R:                         tau<=4,
k=3,Q_0>=tau (including infinity): tau<=9,
k=2,Q_0>=tau (including infinity): tau<=10,
k=3,Q_0<tau:                       tau<=10,
k=2,Q_0<tau:                       tau<=9.
```

## 7. The first positive owner and the order-eleven gate

Let `(u,v)` own `tau`.  Its path has odd total weight

```text
d(u,v)=2tau+1
```

and, because its mixed LCA has positive depth, does not pass through `b`.
Choose an odd-weight edge `f` on that path.  The endpoints of `f` have
opposite root parity and positive mixed LCA, since `f` is not incident with
`b`.  Minimality of `tau` gives

```text
weight(f)>=2tau+1,
```

while containment in the `u--v` path gives the reverse inequality.
Positivity of all edge weights then forces the path to consist of `f`
alone.  Hence the first positive owner is exactly one odd edge not incident
with the root `b`, every lighter odd edge is incident with `b`, and

```text
w=2tau+1<=21.                                       (FW274.18)
```

Taylor's **LITERATURE** parity sizes make both root-parity classes have
order at least four in every Leech candidate of order at least eleven.
FW272 then rules out an identically zero mixed-LCA matrix for a pendant unit
edge.  Thus every hypothetical pendant-unit Leech tree of order at least
eleven satisfies (FW274.17)--(FW274.18).  This includes both parity
orientations at order eighteen.

## 8. An eight-vertex sharp pressure control

The constant is sharp for the local interface used above.  Consider the
eight-vertex weighted tree with edges

```text
b--a:1,       b--e_1:2,       b--u_1:5,
u_1--u_2:4,  u_1--u_3:8,     b--u_4:17,
e_1--v:21.
```

All twenty-eight pair distances are distinct; in increasing order they are

```text
1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
17,18,19,21,22,23,24,26,28,30,32,36,40.
```

Rooted at `b`, its coordinate sets are

```text
R={0,1},
S={0,2,4,6,8,11}.
```

The `b` and `e_1` mixed rows are, respectively,

```text
{0,2,4,6,8,11},              {1,3,5,7,9,10},
```

so the transformed odd owners are exactly `I_[0,11]`.  The unique positive
mixed owner is the edge `e_1--v` with

```text
tau=10,                         w=21.
```

This tree is not Leech.  Its sixteen same-parity half-distances are

```text
{1,2,3,4,5,6,7,9,11,12,13,14,15,16,18,20},
```

not `I_16`; equivalently its full distance set is not `I_28`.  Thus the
control proves sharpness only for the globally distance-distinct odd-sheet
interface.  It does not provide a Leech tree or weaken the simultaneous
even-sheet obligation.

## 9. Trust boundary and successor

FW274 uses only the pendant geometry, the exact odd actual-owner rectangle,
global pair-distance uniqueness, the raw first-hole lemma, and explicit
rooted ancestor enumeration.  It has no finite-search dependency.  The
frozen replay above returned `VERIFIED`; write and no-write output are
byte-identical.  It checks nine finite parent-map kernels, 23 numeric and
five affine named collisions, and the pressure tree, while deliberately
making no SAT-witness claim and invoking neither Leech witness checker.

The result is localisation, not closure.  The exact same-parity completion
from FW273 can still leave `Theta(n^2)` owners inside one pure monochromatic
terminal child.  FW274 does not show that the complete even sheet absorbs
that child, does not propagate the q=1 terminal suffix through it, and does
not create a strictly smaller state with a complete interval spectrum.
Those terminal-absorption and full-even-sheet steps remain **UNVERIFIED**.

The nonpendant unit-edge branch is untouched.  No order is excluded, and
G18 remains **UNVERIFIED**.

Antecedents and controls:

```text
docs/q1-pendant-mixed-lca.md
docs/q1-first-positive-lca.md
data/known_leech_trees.json
```
