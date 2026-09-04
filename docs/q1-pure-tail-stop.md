# The q=1 pure-tail exactness stop (FW270)

This note audits the two proposed successors to FW269: use the exact
FW219c/FW261 spectrum identities to localise a low owner, or eliminate a
unit edge lying wholly in a pure threshold-core tail.  The audit has a sharp
outcome.

* **OBSERVED:** coefficientwise FW219c, after the already proved q=1 top
  owner class is restored, is equivalent to the full Leech spectrum.
  FW261a--b is an owner-labelled refinement of the same equivalence, not an
  intermediate condition below it.
* **OBSERVED:** deleting the endpoints of a unit edge gives an exact domino
  identity.  In a pure-`H` tail its rooted depths obey additional spacing and
  q=1 inequalities, but those inequalities do not eliminate the tail.
* **OBSERVED negative metric diagnostic:** for every pair of integers
  `P>=Q>=2`, a globally distance-distinct integer-weighted pressure tree
  realizes the formal diameter-`D` owner suppliers that match the
  `I_P`-projections of FW219c/FW261, has a nonpendant pure-`H` unit edge, and
  first fails coverage at the next coefficient.  It is neither a Leech tree
  nor an FW219c/FW261 state.
* The proposed near-perfect nonpendant-unit diameter bound remains
  **UNVERIFIED**.  Its evidence through order 12 is finite and
  external/non-replayed here, not an all-order theorem.

Thus the present coefficient/local-owner route is stopped.  This note proves
no order exclusion and does not change G18.  It creates no new verifier or
certificate; the analytic arguments below are the source of FW270.

## 1. Polynomial and q=1 notation

For a positive-integer-weighted tree `S`, write

```text
F_S(X)=sum_{{u,v} subset V(S)} X^d(u,v),
R_p(S;X)=sum_(v in V(S)) X^d(p,v),
I_[a,b]=X^a+...+X^b,       I_b=I_[1,b].
```

For a vertex subset `U subset V(S)`, also write

```text
F^S_U(X)=sum_{{u,v} subset U} X^d_S(u,v),
R^S_p(U;X)=sum_(v in U) X^d_S(p,v)       (p in V(S)).
```

This is the retained-label polynomial in the ambient tree `S`; it remains
defined when the induced subgraph on `U` is disconnected, and the root of
`R^S_p(U)` need not belong to `U`.  Ambient superscripts are suppressed when
the tree is clear.

All polynomial identities below are coefficientwise.  When the ambient tree
has globally distinct pair distances, their displayed summands have disjoint
support and retain the actual owner pair of each coefficient.

For an actual q=1 Leech tree `T` of order `n>=5`, retain the notation of
FW218--FW219:

```text
N=binom(n,2),             M=N-Q,
T'=T-x,                  beta=d(o,z),
y(v)=beta-d(o,v),        H={v in T':y(v)>Q}.
```

There is one visible vertex `v_j` at each coordinate `0<=j<Q`, no vertex at
coordinate `Q`, and

```text
d(x,v_j)=N-j.                                      (FW270.1)
```

The endpoint `z` is `v_0`.  For the double-peel notation put

```text
K=T-{x,z};
g=w(zp), with p the neighbour of z;
h=w(xr), with r the neighbour of x.
```

## 2. FW270a: the exact-spectrum identities are already Leech

Equation (FW270.1) says that the visible pairs incident with `x` own exactly

```text
I_[M+1,N]=I_N-I_M.                                  (FW270a.1)
```

Every other pair is either internal to `T-x` or has the form `{x,u}` with
`u in H`.  Therefore

```text
F_T
 =F_(T-x)+X^h R_r(H)+I_[M+1,N].                    (FW270a.2)
```

It follows immediately that the coefficientwise FW219c identity

```text
I_M=F_(T-x)+X^h R_r(H)                             (FW270a.3)
```

is equivalent, under the already proved q=1 top geometry, to

```text
F_T=I_N.                                           (FW270a.4)
```

The forward implication adds (FW270a.1); the reverse implication subtracts
that disjoint, owner-labelled top class.  This is an equivalence, not merely
a cardinality count.

The same conclusion holds for the double-peel refinement.  FW261 gives

```text
I_M=F_K+X^g R_p(K)+X^h R_r(H),                     (FW270a.5)

X^h R_r(K-H)=I_[M+1,N-1],                         (FW270a.6)
```

and the remaining pair `{x,z}` owns `N`.  Equations (FW270a.5)--(FW270a.6),
together with that last pair, partition `I_N`; conversely the full Leech
spectrum and the q=1 owner theorem recover the same partition.  Thus exact
FW261a--b is only a finer actual-pair labelling of (FW270a.3).

This closes one proposed FW269 successor negatively: an "exact
tight-spectrum bridge" based only on imposing all coefficients of FW219c or
FW261 assumes a condition equivalent to the desired full spectrum.  It does
not provide a strictly weaker descent state.

## 3. FW270b: unit-edge deletion and domino spacing

Let `S` be any globally distance-distinct positive-integer-weighted tree and
let `ab` be an edge of weight one.  Put `U=S-{a,b}`.  For each
`v in V(U)`, define

```text
s_v=min(d(a,v),d(b,v)).
```

Deleting `ab` separates `S` into an `a`-side and a `b`-side.  On the former,
`d(b,v)=d(a,v)+1`; on the latter, `d(a,v)=d(b,v)+1`.  The pairs incident with
`a` or `b` therefore own one singleton and one domino per remaining vertex:

```text
F_S=F^S_U+X+(1+X) sum_(v in V(U)) X^(s_v).         (FW270b.1)
```

In particular the set

```text
S_0={s_v:v in V(U)}
```

consists of distinct positive integers and contains no consecutive pair.
Indeed equality of two starts, or a difference of one, would make two of the
actual pairs in (FW270b.1) own the same distance.  Equivalently, if the edge
cut has sides `A` containing `a` and `B` containing `b`, and

```text
D_A={d(a,u):u in A},       D_B={d(b,v):v in B},
```

then FW269b and the cross-domino comparison give

```text
(D_A-D_A) intersect (D_B-D_B)={0},
D_A intersect (D_A+1)=D_B intersect (D_B+1)=empty,
D_A intersect (D_B+1)=D_B intersect (D_A+1)=empty. (FW270b.2)
```

The zero in each rooted-depth set represents its incident endpoint; after
removing those zeroes, their union is precisely `S_0`.

There is also a useful provenance fact in the q=1 double-peel partition.  If
the unit edge lies in a pure-`H` tail, then each domino in (FW270b.1) is
monochromatic under FW261:

* the domino indexed by `v=x` lies wholly in the `x--H` class;
* the domino indexed by `v=z` lies wholly in the `z--K` class;
* every domino indexed by another vertex lies wholly in `F_K`;
* the singleton `X` for `{a,b}` also lies in `F_K`.

Thus FW261 does not split a domino between suppliers and create an additional
collision.  Once complete coverage is imposed, (FW270b.1) is simply part of
the same actual-pair partition already identified in FW270a.

## 4. Pure-H root-depth pressure

Return to an actual q=1 Leech tree and orient a unit edge `ba` of `T-x` away
from the root `o`, with `b` on the root side.  Let `A` be the descendant
component containing `a`, and assume the pure-tail case

```text
A subset H.
```

Set

```text
q_b=d(x,b),       sigma=M-1-q_b,
t_j=d(b,v_j)      (0<=j<Q).                        (FW270b.3)
```

Because `b in H`, `q_b<=M-1`.  The rooted depth difference of `v_j` and `b`
is

```text
d(o,v_j)-d(o,b)=d(x,v_j)-d(x,b)=N-j-q_b>0.
```

The rooted LCA identity consequently gives

```text
t_j>=N-j-q_b,
t_j congruent N-j-q_b (mod 2).                    (FW270b.4)
```

Since `A` has no visible vertex, every `v_j` is on the `b`-side of the unit
cut.  The two internal pairs `{b,v_j}` and `{a,v_j}` have distances
`t_j,t_j+1`.  Global uniqueness makes the `t_j` pairwise distinct and
nonconsecutive.  Both distances occur inside `T-x`, whose diameter is `M`, so

```text
t_j<=M-1.                                          (FW270b.5)
```

The following elementary packing step is sharp enough for the present
purpose.  Put `r_0=N-q_b`.  If every `t_j<=r_0+Q-1`, then all `Q` starts lie
in the `2Q-1` consecutive positions

```text
[r_0-Q+1,r_0+Q-1].
```

A nonconsecutive `Q`-set in that interval is its unique maximum independent
set, consisting of every other position and hence of a single parity.  But
(FW270b.4) assigns alternating parities as `j` runs through `0,...,Q-1`.
Since `Q>=2`, this is impossible.  Therefore

```text
max_j t_j>=N-q_b+Q.                                 (FW270b.6)
```

Combining (FW270b.5)--(FW270b.6) with `M=N-Q` gives

```text
q_b>=2Q+1.                                          (FW270b.7)
```

Finally, order the distances from `a` to the `|A|` vertices of its cut side.
They start at zero and, by (FW270b.2), have no consecutive values.  Hence
the largest distance from `b` into `A` is at least `2|A|-1`.  Every
`x--A` distance equals `q_b` plus the corresponding `b`-depth.  Since
`A subset H`, it is also `N-y(u)<=N-(Q+1)=M-1`.  Thus

```text
2|A|-1<=sigma<=M-2Q-2=N-3Q-2.                     (FW270b.8)
```

Equations (FW270b.7)--(FW270b.8) are genuine all-order Leech consequences.
They constrain a pure tail but do not make either interval empty in general.

## 5. FW270c: every finite truncation can be satisfied

The failure of finite coefficient pressure is exact.  Choose integers

```text
P>=Q>=2,       L>=1,
m=P+Q+L,
B>=8(P+Q+1)+17,
C_0=0,         C_i=sum_(h=1)^i B^h,
R=B^(m+2),     W=B^(m+1),
t_a=Q+L+a      (1<=a<=P).                          (FW270c.1)
```

Construct a tree on

```text
x,r,s_0,...,s_m,v_0,...,v_(Q-1),
ell_a (1<=a<=P, a!=Q), and c
```

with edges

```text
x--r                 Q,
r--s_0               3R,
s_(i-1)--s_i         B^i                    (1<=i<=m),
s_j--v_j             2R-C_j-j               (0<=j<Q),
s_(t_a)--ell_a       a                      (1<=a<=P, a!=Q),
ell_1--c             W.                             (FW270c.2)
```

The omission of `ell_Q` is intentional: `Q` is owned by `x--r`.  Since
`t_P=m`, every displayed anchor exists.  The order is

```text
n_*=2P+2Q+L+3.                                      (FW270c.3)
```

Put `z=v_0`, `D=5R+Q` and `M=D-Q=5R`.  Direct path summation gives

```text
diam(T)=D,             diam(T-z)=D-1,
diam(T-x)=M,           d(x,v_j)=D-j,
y(v_j)=j,              y(s_i)=2R-C_i,
y(ell_a)=2R-C_(t_a)-a,
y(c)=2R-W-C_(t_1)-1.                               (FW270c.4)
```

All nonvisible values on the last two lines exceed `Q`.  Thus the construction
has the exact formal q=1 top window and its unit edge
`s_(t_1)--ell_1` is nonpendant: its pure-`H` descendant side is
`{ell_1,c}`.

### Global distance uniqueness

For completeness, all pair distances are covered by the following signatures
(`i<k`, `j<k<Q`, and `a,b!=Q` where used):

```text
0R:  Q;
     C_k-C_i;
     a+|C_(t_a)-C_i|;
     a+b+|C_(t_a)-C_(t_b)|;
     W;
     W+1+|C_(t_1)-C_i|;
     W+1+a+|C_(t_1)-C_(t_a)|             (a!=1,Q).

2R:  2R-C_i-j                         (i<=j);
     2R+C_i-2C_j-j                    (i>=j);
     2R+C_(t_a)-2C_j+a-j;
     2R+W+1+C_(t_1)-2C_j-j.

3R:  3R+C_i;                 3R+Q+C_i;
     3R+C_(t_a)+a;           3R+Q+C_(t_a)+a;
     3R+W+C_(t_1)+1;         3R+Q+W+C_(t_1)+1.

4R:  4R-2C_j-j-k.

5R:  5R-j;                  5R+Q-j.                (FW270c.5)
```

These expressions respectively cover spine/pendant/`c` pairs, pairs
incident with a visible leaf, pairs incident with `r` or `x`, two visible
leaves, and a visible leaf with `r` or `x`.

Each expression has the base-`B` form

```text
e_(m+2) R+e_(m+1) W+sum_(i=1)^m e_i B^i+e_0,
```

where every nonconstant digit has absolute value at most five.  All constant
residues lie in `[-(2Q-3),2P]`, an interval of width `2P+2Q-3<B`, while the
difference of two higher-position digits has absolute value at most
`10<B`.  Equality of two distances can therefore be reduced successively
modulo `B`: it first forces equal residues, and after subtraction and
division by `B` it forces equal digits at every position through `R`.

The resulting signature is injective.  In the `0R` layer a nonzero digit
block is a contiguous interval and determines its two spine indices; the
positive residue distinguishes a pendant endpoint, and omitting `ell_Q`
prevents a zero-block collision with `x--r`.  In the `2R` layer the change
from coefficient `-1` to `+1`, when present, determines `j`, and the last
positive digit determines the other spine or anchor index.  When no positive
digit is present, the residue `-j` determines `j` and the last negative digit
determines the remaining spine index, or its absence identifies `i=0`.  The
residue then distinguishes a spine endpoint from `ell_a`, while the `W` digit
identifies `c`.  In the `3R` layer the last nonzero digit gives the spine or
anchor index, or its absence identifies `s_0`; the residue distinguishes `r`
from `x` and a spine endpoint from its pendant;
omitting `ell_Q` also prevents `r--ell_Q` from colliding with
`x--s_(t_Q)`.  In the `4R` layer a nonempty `-2` block recovers `j`, while
its absence identifies `j=0`, and the residue then recovers `k`; the `5R`
layer recovers `j` and the endpoint.
Thus equal signatures have the same unordered endpoint pair, proving global
distance uniqueness.

### Exact truncated ownership and first failure

Every edge not listed with weight at most `P` is larger than `P+1`, and no
path containing two edges of weight at most `P` avoids one of those larger
edges.  Consequently

```text
Spec(T) intersect [1,P+1]=[1,P].                   (FW270c.6)
```

For `a!=Q`, coefficient `a` is owned uniquely by
`s_(t_a)--ell_a`; coefficient `Q` is owned uniquely by `x--r`; and `P+1` is
absent from every owner class.  With `K=T-{x,z}`, the former owners lie in
`F_K`, the latter lies in the `x--H` factor, and the `z--K` factor supplies
no coefficient at most `P`.  Hence the FW219c and FW261a owner partitions are
matched after projection to `I_P` only after formally replacing the Leech cap
`N` by the diameter `D`.  This is not an FW219c/FW261 state.  Independently of
that truncation,

```text
d(x,v_j)=D-j
```

matches the formal diameter-`D`-substituted FW261b high supplier
`I_[M+1,D-1]` for `v_1,...,v_(Q-1)`.

This family is an **OBSERVED analytic pressure construction**, not a Leech
counterexample.  Its formal cap `D=5B^(m+2)+Q` is vastly larger than
`binom(n_*,2)`, and coefficient `P+1` is deliberately missing.  Choosing
`Q=2` and fixed `L` gives `P/n_* -> 1/2`; keeping `Q` fixed and choosing
`L=P` gives `P/n_* -> 1/3` while placing the pure unit tail at hop depth
`Theta(n_*)`.
In either case `P/binom(n_*,2)->0`.  Thus every finite truncation, and even a
linear-size truncation, is compatible with this non-Leech escape; it does not
show that a nearly complete quadratic spectrum is compatible with it.

## 6. The near-perfect proposal remains unproved

The surviving actual-tree proposal is:

> **UNVERIFIED near-perfect nonpendant-unit bound.**  If `S` is a
> positive-integer-weighted, globally distance-distinct tree of order `m>=5`
> and deleting its unit edge leaves two sides of order at least two, then
> `diam(S)>=binom(m,2)+m-4`.

The distinction between nonpendant and pendant is essential.  The known
`L6` Leech tree has its unit edge on a `1+5` cut and is not covered by the
proposal.

There is **OBSERVED external/non-replayed finite evidence through `m<=12`**.
The underlying complete MDD search spaces are documented in
`variants/mdd_forest.cpp` and `variants/RESULTS.md`; the additional
nonpendant-unit filtering was an independent bounded diagnostic and has no
dedicated frozen script or certificate in this repository.  It is therefore
finite evidence, not a machine theorem promoted here.  Two 30-second
fixed-topology attempts at `m=13` returned `UNKNOWN`; they are not exclusions
and are not part of the evidence.

Even the exact coefficient algebra does not prove the proposal.  At `m=9`
the following hand-checkable formal relaxation exists:

```text
R_A=1+X^2,
R_B=1+X^4+X^8+X^15+X^19+X^23+X^27,
F_A=X^2,
F_B=I_36-F_A-X R_A R_B.                            (FW270d.1)
```

The cross product has 14 distinct coefficients, disjoint from `F_A`, and
`F_B` has 21 coefficients, so

```text
I_36=F_A+F_B+X R_A R_B                             (FW270d.2)
```

has exactly the `1+14+21=36` pair count of a `2+7` unit cut and satisfies the
cut, domino and parity-level coefficient constraints.  This is an
**OBSERVED exact polynomial relaxation**, not a weighted-tree witness:
rooted-tree realizability of `(F_B,R_B)` is not supplied.  It locates the
irreducible missing input precisely at rooted-side tree realization, beyond
the owner-partition identities.

If the near-perfect proposal were proved and applied to `S=T-x`, then
`m=n-1` and

```text
N-Q=diam(T-x)>=binom(n-1,2)+(n-1)-4=N-4,
```

so `Q<=4` whenever the pure unit cut has both sides nontrivial.  This would be
a real reduction, but not yet nonexistence; it says nothing when the
descendant side is the singleton `{a}`.

## 7. Stop verdict and next interface

FW270 stops the present algebraic localisation route:

1. exact FW219c/FW261 coverage is equivalent to asking for the full Leech
   spectrum;
2. any prescribed finite owner prefix survives a non-Leech pure-tail pressure
   family;
3. the unit domino and q=1 root-depth inequalities leave a nonempty parameter
   range; and
4. coefficient/count/parity relaxations do not encode rooted-side tree
   realizability.

Reopening requires both of the following genuinely new **UNVERIFIED** inputs:

* a rooted near-perfect realization theorem strong enough to classify or
  exclude the nonpendant pure-`H` unit cut (the proposed diameter bound would
  only reduce it to `Q=2,3,4`); and
* a separate singleton-tail theorem for `A={a}`, which is outside every
  nonpendant-unit bound and must retain actual-pair provenance.

More finite prefixes, unrooted generating-function partitions, generic
moments, or a restatement of exact FW219c/FW261 are not successor mechanisms.
No new forced-prefix engine, order-16 gate, order-25 sentinel, or larger-order
search is authorised by FW270.  G18 remains **UNVERIFIED**.

The frozen q=1 inputs used here remain:

```text
docs/q1-low-owner-localization.md
theory-lab/topwindow/verify_q1_threshold_core.py
theory-lab/topwindow/results/q1_threshold_core_certificate.json
theory-lab/topwindow/verify_q1_endpoint_singleton_double_peel.py
theory-lab/topwindow/results/q1_endpoint_singleton_double_peel_certificate.json
```

## 8. FW271 successor

FW271 replaces the two broad reopening proposals above by a sharper frozen
interface.  The pure-`H` unit cut has an **OBSERVED** strict actual-pair
product/window theorem, including high/low `q_b` branches, and a pendant unit
edge has an **OBSERVED** exact self-complement, parity-halved cross rectangle,
and visible/pure-core coordinate dichotomy.  These statements are stronger
than FW270b but still give neither a collision nor a same-type proper descent.

The cross rectangle itself is frozen; any further distance-matrix or
cross-rectangle consequence is **UNVERIFIED successor work under review**
and is not part of FW271.  The refined negative mechanism ledger and exact
reopening gates are in `docs/q1-full-spectrum-mechanism-audit.md`.  No new
search is authorised, no order is excluded, and G18 remains **UNVERIFIED**.

## 9. FW275 rooted-stability successor audit

FW275 tests the rooted-realisation input requested in Section 7 on the hard
`2|b` nonpendant unit cut.  The wrapper and `b-3`-hole partition below the
near-perfect counterexample cap are **OBSERVED exact**, including actual LCA
ownership for every residual nonroot-pair coefficient.

That ownership does not validate the proposed local induction.  **OBSERVED
analytic** scalable formal states survive all audited
first-pivot/reflection/`2p`-chain tests and fail
only at their second actual pivot.  **OBSERVED hand-checkable** equality trees
at orders nine and eleven then show that actual owner transfers may form a
multi-gate triangle and that a long chain or whole virtual row may telescope
to one boundary/diagonal hole.  Those controls have `D=D_0+1`; they test
cap-blind local LCA implications, not a claim that essentially uses the
strict counterexample cap.

Consequently, only the cap-blind first-pivot / chain-boundary /
single-virtual-row route is at an **OBSERVED STOP**.  The near-perfect
nonpendant-unit bound itself remains **UNVERIFIED**.  The exact successor must
either construct a strict-cap global potential on labelled owner pairs and
all their LCA gates, surviving cycles and row mergers, or prove a
terminal-suffix lemma that peels all distances incident
to a terminal rooted set together with exactly one hole per deleted vertex.
No verifier, witness, new search or order exclusion is supplied, and G18
remains **UNVERIFIED**.  Full state and controls:
`docs/nonpendant-unit-rooted-stability-stop.md`.
