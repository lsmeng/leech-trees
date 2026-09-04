# The pendant-unit mixed-LCA obstruction (FW272)

FW272 is the first exact successor to the pendant parity rectangle in FW271.
It is an all-order theorem: the proof uses the full Leech spectrum and a
pendant unit edge, but it does not use the q=1 coordinate system.

* **OBSERVED:** if the mixed-parity LCA-depth matrix of a pendant-unit Leech
  tree vanishes identically, then the even root-parity class has order at
  most three.
* **OBSERVED:** Taylor's parity arithmetic therefore forces a positive mixed
  LCA entry in every pendant-unit Leech candidate of order at least eleven,
  including order eighteen.
* **UNVERIFIED:** a positive mixed LCA block has not been converted into a
  repeated distance or a smaller state with bounded boundary context.

FW272 has no verifier or certificate.  It excludes no order and leaves G18
**UNVERIFIED**.

## 1. Statement and notation

Let `T` be a Leech tree of order `n`, so its unordered-pair distances are
exactly

```text
I_N={1,...,N},                 N=binom(n,2).
```

Suppose the weight-one edge is a leaf edge `a--1--b`, with `a` the true
leaf, and root `T` at `b`.  Put

```text
rho(v)=d(b,v),
E={v:rho(v) is even},          O={v:rho(v) is odd},
e=|E|,                         o=|O|.
```

Thus `b in E` and `a in O`.  For `u in E` and `v in O`, define

```text
R_u=rho(u)/2,
S_v=(rho(v)-1)/2,
L_(u,v)=rho(LCA_b(u,v)),
A_(u,v)=(d(u,v)+1)/2.
```

All these quantities are nonnegative integers.  The theorem is

> **FW272.** If `L_(u,v)=0` for every `u in E`, `v in O`, then `e<=3`.
> Consequently every pendant-unit Leech candidate with `e>=4` has a mixed
> pair whose paths from `b` share a positive-length initial segment.

The conclusion is asymmetric only because `b` is the even root and its unit
leaf `a` is odd.  The root parity class `E` may be either the smaller or the
larger Taylor class.

## 2. Exact parity partitions and the cross rectangle

There are `floor(N/2)` even values and `ceil(N/2)` odd values in `I_N`.
A pair has odd distance exactly when its endpoints lie in different root
parity classes.  Hence

```text
eo=ceil(N/2).                                      (FW272.1)
```

Put `O'=O-{a}` and `P=floor(N/2)`.  Separating the actual owners of the even
and odd coefficients, and then dividing by two, gives the two exact disjoint
partitions

```text
I_P
 = {d(u,u')/2:{u,u'} subset E}
   dot-union {d(v,v')/2:{v,v'} subset O'}
   dot-union {(1+rho(v))/2:v in O'},               (FW272.2)

I_(eo)
 = {1+rho(u)/2:u in E}
   dot-union {(d(u,v)+1)/2:u in E,v in O'}.        (FW272.3)
```

Indeed, the final class in (FW272.2) consists of the pairs `{a,v}`, whose
distances are `1+rho(v)`.  The first class in (FW272.3) consists of the
pairs `{a,u}`.  Thus (FW272.3) is exactly the complete `E x O` matrix

```text
{A_(u,v):u in E,v in O}=I_(eo),                   (FW272.4)
```

with every value occurring once.

The rooted LCA formula gives

```text
A_(u,v)=1+R_u+S_v-L_(u,v).                        (FW272.5)
```

Equivalently, the distinguished pendant minor is

```text
A_(u,v)+A_(b,a)-A_(u,a)-A_(b,v)=-L_(u,v).         (FW272.6)
```

Root depths are distinct: equal positive depths of two different vertices
would make their two pairs with `b` repeat a distance.  Therefore

```text
R={R_u:u in E},              S={S_v:v in O}
```

are honest sets of orders `e,o`, both containing zero.  If `L` vanishes
identically, (FW272.4)--(FW272.5) become the exact interval direct sum

```text
R dot+ S={0,...,eo-1}.                            (FW272.7)
```

Only the odd partition (FW272.3) is needed for the contradiction below;
(FW272.2) records the simultaneous full-spectrum boundary that any successor
argument must retain.

## 3. The local interval-block lemma

The required interval structure is local and does not assume that either
whole factor is an arithmetic progression.

> **Interval-block lemma.** Let finite nonnegative integer sets `U,W`, both
> containing zero, satisfy
>
> ```text
> U dot+ W={0,...,H}.
> ```
>
> Suppose `[0,k-1] subset U`, `k notin U`, and that `U` has a later
> element.  If
>
> ```text
> P=min(U-[0,k-1]),
> ```
>
> then
>
> ```text
> P is a multiple of k,
> {0,k,2k,...,P-k} subset W,
> [P,P+k-1] subset U.                              (FW272.8)
> ```

Here is the complete local proof.

First, none of `1,...,k-1` lies in `W`, since for such a `t` the two sums
`t+0` and `0+t` would coincide.  Before `P`, the only available members of
`U` are `0,...,k-1`.  Unique consecutive coverage therefore proceeds in
blocks

```text
[0,k-1], [k,2k-1], [2k,3k-1], ... .
```

Equivalently, an induction on the first uncovered integer shows that the
members of `W` below `P` are exactly

```text
0,k,2k,... .                                      (FW272.9)
```

If `P=qk+t` with `0<t<k`, then `P` already has the representation
`t+qk`, in addition to `P+0`.  Hence `t=0`: `P` is a multiple of `k`, and
(FW272.9) gives the middle assertion of (FW272.8).  Since `k notin U`, this
also gives `P>=2k`.  The value `P` cannot lie in `W`, because `P+0` and
`0+P` would then be two representations.

Next fix `1<=t<k`.  If `P+t` belonged to `W`, then `P+k` would have the two
representations

```text
P+k = P+k = (k-t)+(P+t),
```

where `P,k-t in U` and `k,P+t in W`.  The value `P+k` is inside the target
interval because `P in U` and `k in W` already make it a represented sum.
Thus

```text
W intersect [P,P+k-1]=empty.                     (FW272.10)
```

Finally cover `P+t`, successively for `0<=t<k`.  A member of `U` below `P`
lies in `[0,k-1]`; pairing it with a member of `W` would require either a
nonmultiple in `(P-k,P)`, the forbidden value `P`, or a value in
`(P,P+k)`, all excluded by (FW272.9)--(FW272.10).  A previously forced
member `P+j` of `U`, `j<t`, would require the forbidden small member
`t-j in W`.  Consequently the only possible owner is `(P+t)+0`, forcing
`P+t in U`.  This proves the last assertion of (FW272.8).

## 4. Proof of FW272

Assume (FW272.7).  When `r in R`, write `e_r` for the unique even vertex at
root depth `2r`; when `s in S`, write `o_s` for the unique odd vertex at
root depth `2s+1`.  Thus `e_0=b` and `o_0=a`.

The LCA of two vertices is a vertex and hence has an integer root depth.
Moreover `a` is the unique vertex at depth one and, being a true leaf,
cannot be the LCA of two other vertices.

### 4.1 The first positive even coordinate

If `R` has no positive member, then `e=1` and the theorem is immediate.
Otherwise let `r` be its least positive member.  If `r>1`, the unique
coverage of `0,...,r-1` in (FW272.7) forces

```text
[0,r-1] subset S.
```

In particular `r-1 in S`, and the two distinct actual pairs

```text
{b,e_r},                    {a,o_(r-1)}
```

both have distance `2r`.  This is impossible in a Leech tree.  Therefore

```text
1 in R.                                           (FW272.11)
```

Let `k` be the length of the maximal initial consecutive block of `R`:

```text
[0,k-1] subset R,               k notin R.
```

Equation (FW272.11) gives `k>=2`.

### 4.2 Initial block of length at least four

If `k>=4`, the vertices `e_1,e_2,e_3` have depths `2,4,6`.  The LCA of
`e_1,e_2` has depth at most two, so its only possible depths are `0,1,2`.
Depth one is the leaf `a` and is impossible.  Depth zero gives

```text
d(e_1,e_2)=6=d(b,e_3),
```

while depth two gives

```text
d(e_1,e_2)=2=d(b,e_1).
```

Both alternatives repeat a distance.  Hence

```text
k<=3.                                             (FW272.12)
```

### 4.3 Initial block of length two

Suppose `k=2` and `R` has a later element `P`.  The interval-block lemma
gives

```text
P>=4,       P-2 in S,       P,P+1 in R.
```

The LCA of `e_1,e_P` again has possible depths `0,1,2`, with depth one
impossible.  At depth zero,

```text
d(e_1,e_P)=2P+2=d(b,e_(P+1));
```

at depth two,

```text
d(e_1,e_P)=2P-2=d(a,o_(P-2)).
```

Both are collisions.  Thus the `k=2` case has no later element of `R`.

### 4.4 Initial block of length three

Suppose `k=3` and `R` has a later element `P`.  The interval-block lemma
gives

```text
P>=6,             P,P+1,P+2 in R.
```

For `e_1,e_2`, an LCA at depth two gives distance two and repeats
`d(b,e_1)`; depth one is impossible.  Their LCA must therefore be the root
`b`.

For `e_1,e_P`, an LCA at depth zero gives

```text
d(e_1,e_P)=2P+2=d(b,e_(P+1)).
```

Consequently its LCA must have depth two: `e_P` is a descendant of `e_1`.
But `e_1` and `e_2` lie in different root branches, so

```text
LCA_b(e_2,e_P)=b.
```

It follows that

```text
d(e_2,e_P)=2P+4=d(b,e_(P+2)),
```

again a collision.  Thus the `k=3` case also has no later member of `R`.

By (FW272.12), the only surviving possibilities are therefore

```text
R={0,1}  or  R={0,1,2}.
```

In particular `e=|R|<=3`, proving FW272.

## 5. Taylor range, q=1 locations, and the L6 boundary

Taylor's parity condition is **LITERATURE** input whose proof is re-derived
in `docs/literature-ledger.md`.  If `n=q^2`, its two class orders are

```text
q(q-1)/2,                    q(q+1)/2.
```

If `n=q^2+2`, they are

```text
(q^2+2-q)/2,                (q^2+2+q)/2.
```

For a candidate with `n>=11`, the second branch has `q>=3` and smaller
class order at least four; the square branch has `q>=4` and smaller class
order at least six.  Whichever class contains the root `b`, it follows that

```text
n>=11 and a--1--b pendant  =>  some L_(u,v)>0.    (FW272.13)
```

At order eighteen the class orders are `7,11`, so (FW272.13) applies to
both possible parity orientations.

The conclusion also covers both q=1 locations from FW271.  In the FW219
orientation the edge at `x` has weight at least `Q>=2`, so `a!=x`, and
leaf geometry gives `y(b)=y(a)+1`.  Since coordinates `0,...,Q-1` occur and
coordinate `Q` is absent, the pendant pair is either wholly visible,

```text
0<=y(a)<=Q-2,
```

or wholly in the pure core,

```text
y(a)>=Q+1.
```

FW272 did not use `Q` or either location, so no third positional case has
escaped it.

The order-six witness is the necessary asymmetric boundary control.  With the
known labelling

```text
(0,1,1), (0,2,2), (0,3,5), (3,4,4), (3,5,8),
```

take `a=1,b=0`.  Then

```text
R={0,1},                    S={0,2,4,6},
R dot+ S={0,...,7},         L identically zero.
```

Thus a pendant unit edge and a complete cross interval do not by themselves
force a positive LCA entry.  The hypothesis `e>=4` in the corollary cannot
simply be discarded.

## 6. Trust boundary and successor

FW272 uses only:

1. the full Leech spectrum and actual-pair uniqueness;
2. the pendant geometry `d(a,v)=1+d(b,v)` for `v in T-a`;
3. parity and the rooted LCA identity; and
4. the proved local interval-block lemma in Section 3.

It is independent of q=1 and of every finite search.  It does not prove that
the unit edge is pendant, so it says nothing about the nonpendant unit-edge
branch.  In the pendant branch it proves only that the mixed-LCA matrix is
nonzero.  It does not prove that a positive entry, or the associated laminar
descendant block, creates a collision.

The next required statement remains **UNVERIFIED**:

> Under the simultaneous exact parity partitions (FW272.2)--(FW272.3), a
> positive laminar mixed-LCA block either forces a repeated actual distance
> or exposes a strictly smaller state retaining both partitions with bounded
> boundary-owner context.

No such inheritance or bounded-context theorem is currently available.
Accordingly FW272 creates no order exclusion, and G18 remains
**UNVERIFIED**.

Antecedent and controls:

```text
docs/q1-full-spectrum-mechanism-audit.md
docs/literature-ledger.md
data/known_leech_trees.json
```

## 7. Frozen successor (FW273)

FW273 now resolves the first quantitative successor without claiming the
missing descent.  If

```text
tau=min{(d(u,v)-1)/2:L_(u,v)>0},
```

then the raw convolution `R+S` has coefficient one below `tau` and
coefficient zero at `tau`.  Actual-pair collisions in the root-even factor
give the **OBSERVED all-order** bounds

```text
tau<=3|O|+2,
w=2tau+1<=6|O|+5,
```

where the owner of `w` is exactly an odd edge not incident with `b`.  Thus a
pendant-unit order-eighteen candidate has `w<=47` or `w<=71`, according to
orientation.  G18 remains **UNVERIFIED**.

The labelled mixed rectangle also determines a same-parity LCA exactly when
its LCA-descendant subtree contains the opposite parity.  At a deepest mixed
vertex the cross pairs form an exact direct block; all remaining freedom is
inside pure monochromatic children, whose internal edges are even.  A single
such child may retain `Theta(n^2)` undetermined owners after division by two,
so this is not a bounded-context same-type descent.  The q=1 order-eighteen
`x` row occupies half-indices at least 70, whereas `tau<=35`, but no proved
propagation bridges that gap.

The n=11 CP-SAT result recorded with FW273 is only **OBSERVED
external/non-replayed diagnostic** evidence about a necessary relaxation;
it has no frozen proof log and is not a proof or order exclusion.  Full
statement, proof, completion formulas, controls and stop boundary:
`docs/q1-first-positive-lca.md`.
