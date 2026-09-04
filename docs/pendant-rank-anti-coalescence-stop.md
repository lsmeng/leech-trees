# Pendant rank anti-coalescence: exact mismatch ledger and stop (FW280)

FW280 isolates the first missing pendant lemma from FW279.  It sharpens the
reduction but does not prove that lemma.

* **OBSERVED exact:** after cancelling their common path, a first transformed
  collision is an equality between two nonempty collections of at most two
  mutually edge-disjoint arms.
* **OBSERVED exact:** the collision-defect difference equals a window of
  distinct actual internal owners, while each path defect is a signed sum of
  owner-labelled internal/external colour mismatches under prefix translation.
* **OBSERVED exact:** every mismatch is geometrically non-aligned; otherwise
  concatenation with the prefix gives its translated coefficient the wrong
  internal/external owner type.
* **OBSERVED stop:** minimality does not resolve the resulting LCA/gate/connector
  correction, because each mismatch has one internal and one external endpoint.
* **OBSERVED pressure / UNVERIFIED target:** an exact-top non-Leech family
  collides, but no canonical full-state counterexample was found.  The missing
  result couples canonical top ownership to full low coverage.

## 1. Canonical scope

Let `T` be a hypothetical Leech tree of order `n`, with

```text
N=binom(n,2),                    Spec(T)=I_N.
```

Retain the canonical pendant state from FW279:

```text
a --1-- b,                      x --e-- r,
```

where `a` is the unit leaf and the distinct leaf `x` is the canonical q=1
distinguished diameter endpoint.  Delete them and put

```text
U=T-{a,x},                      m=n-2,
C=binom(m,2),                   h=d_U(b,r),
B=D_b(U),                       R=D_r(U),
L=1+h+e.
```

The external owner set is the coefficientwise disjoint union

```text
H=(1+B) dot-union (e+R) dot-union {L}.             (FW280.1)
```

A member `1+d_U(b,u)` has owner `{a,u}`, a member `e+d_U(r,v)` has owner
`{x,v}`, and `L` has owner `{a,x}`.  If `Q` is the canonical first-hole
parameter and `D_0=N-Q`, full coverage and top ownership give

```text
H intersect [D_0+1,N]=[D_0+1,N],
D=Spec(U)=[1,D_0]-(H intersect [1,D_0]),
|D|=C.                                               (FW280.2)
```

Define

```text
q(t)=|H intersect [1,t]|,             phi(t)=t-q(t). (FW280.3)
```

For `d in D`, `phi(d)` is its increasing rank in `D`; hence

```text
phi(D)=I_C.                                          (FW280.4)
```

Every core edge has weight at least two because the deleted edge is the unique
distance one.  Reweight an edge `f` of old weight `w_f` by `phi(w_f)`.  For a
core path `P`, write

```text
d(P)=sum_(f in P)w_f,
F(P)=sum_(f in P)phi(w_f).                           (FW280.5)
```

The **UNVERIFIED rank anti-coalescence** target says that distinct core pairs
have distinct `F(P)`.  The complete interval makes every coefficient through
`D_0` an actual internal or external owner; Section 8 shows that an exact top
row without complete low coverage is insufficient.

## 2. First-collision arm normal form

Assume only for the reduction that anti-coalescence fails.  Choose distinct core
paths `P,P'` with equal `F`, first by the common transformed value and then by
the number of edges in their union.  Their old distances differ by global owner
uniqueness; reverse their names so that

```text
F(P)=F(P'),                    d(P)<d(P').           (FW280.6)
```

The intersection `J=P intersect P'` is a connected path, possibly empty.
Cancelling its transformed edges leaves

```text
sum_(f in P-J)phi(w_f)=sum_(f in P'-J)phi(w_f).     (FW280.7)
```

Each remainder is a union of at most two path arms, and the two remainders are
edge-disjoint.  Neither is empty: otherwise one original path is a proper
subpath of the other, contradicting positivity of the transformed edge weights.
If their nonempty arms have old lengths `p_1,p_2` and `q_1,q_2`, omitting a
missing second arm, then

```text
p_1+p_2 != q_1+q_2.                                 (FW280.8)
```

Indeed, adding back `d(J)` gives the distinct old distances in (FW280.6).
This is the exact first-collision normal form: at most two edge-disjoint arms
equal at most two edge-disjoint arms after transformation.

It cannot generally be reduced to two arms sharing one root: a four-arm
equality does not make either cross-recombination equal.

## 3. AC-1: collision defect

Define the rank-additivity defect of a core path by

```text
def(P)=q(d(P))-sum_(f in P)q(w_f).                  (FW280.9)
```

Then

```text
F(P)=phi(d(P))+def(P).                             (FW280.10)
```

Both old distances in (FW280.6) belong to `D`, so

```text
phi(d(P'))-phi(d(P))=|D intersect (d(P),d(P')]|.  (FW280.11)
```

Equations (FW280.6), (FW280.10) and (FW280.11) prove

```text
def(P)-def(P')
  =|D intersect (d(P),d(P')]|.                    (FW280.12)  [AC-1]
```

Every term on the right has a different uniquely determined unordered-pair
owner internal to `U`.  AC-1 is therefore an actual-owner interval ledger,
not a free cardinality supply.  A proof must compare the signed transport on
two unrelated paths with all owners in that interval.

## 4. AC-2: prefix-translation mismatches

Orient a core path with edge weights `w_1,...,w_k` and prefixes

```text
s_i=w_1+...+w_i,                 s_0=0.
```

For `s+w<=D_0`, let

```text
eta(s,w)=q(s+w)-q(s)-q(w).                         (FW280.13)
```

Telescoping gives

```text
def(P)=sum_(i=1 to k)eta(s_(i-1),w_i).             (FW280.14)
```

Translation `t -> t+s` bijects `[1,w]` with `[s+1,s+w]`.  Define

```text
M^+_(s,w)={t in D intersect [1,w]:t+s in H},
M^-_(s,w)={t in H intersect [1,w]:t+s in D}.       (FW280.15)
```

Equal-colour pairs cancel under translation, proving

```text
eta(s,w)=|M^+_(s,w)|-|M^-_(s,w)|.                 (FW280.16)  [AC-2]
```

Every mismatch keeps two actual owners.  In `M^+`, the lower owner is an
internal `U`-pair and the translated owner is incident with `a` or `x`; in
`M^-` the roles reverse.

Expanding the two root rows gives the equivalent exact window formula

```text
q(t)=|B intersect [0,t-1]|+|R intersect [0,t-e]|+1_(L<=t),

eta(s,w)
 = |B intersect [s,s+w-1]|-|B intersect [0,w-1]|
 + |R intersect [s-e+1,s+w-e]|-|R intersect [0,w-e]|
 + 1_(s<L<=s+w)-1_(L<=w).                         (FW280.17)
```

The `B` entries retain owners `{a,u}`, the `R` entries retain `{x,v}`, and
the last term retains `{a,x}`.  Formula (FW280.17) is the FW279 two-root
window; AC-2 also records the internal owner across every colour change.

## 5. No-alignment lemma

Let `S` be the core prefix path of length `s` in an AC-2 step.

> **OBSERVED no-alignment lemma.**
>
> * For `t in M^+_(s,w)`, the internal owner path of `t` cannot share exactly
>   one endpoint with `S`, be otherwise edge-disjoint, and form one simple
>   core path with it.
> * For `t in M^-_(s,w)`, the external owner path of `t` cannot concatenate
>   at its core endpoint with `S` in that way.

In the first case concatenation would make `t+s` a distance internal to `U`,
contrary to `t+s in H`.  In the second, concatenation preserves endpoint `a`
or `x` and would make `t+s` external, contrary to `t+s in D`.  The corner
owner `{a,x}` has no core endpoint at which the second concatenation can occur.

Thus every mismatch forces nontrivial overlap, a different gate, a positive
connector, or a multi-arm source for which no endpoint concatenation realizes
the formal sum.  The result uses the full coefficientwise owner partition,
but supplies no common direction among these outcomes.

## 6. Why minimality stops at the gate

For two rooted depths `alpha,beta`, the actual mutual distance is

```text
alpha+beta-2 lambda,
```

where `lambda` is their LCA depth.  Paths at separate gates instead acquire
connector corrections; in a four-point sum a connector may occur twice.
Hence replacing `t -> t+s` by an actual uncrossed owner introduces a correction
whose sign and size depend on owner geometry.

First-collision minimality does not control it.  A member of `M^+` relates one
internal path to one external path, and a member of `M^-` does the reverse.
Neither is a pair of core paths with equal transformed distance.  Uncrossing
produces legitimate coefficients with actual owners, but not a second smaller
core path at the same `F`-value.

Pairing positive and negative mismatches also has no canonical rule.  Their
source paths can use different gates; one can contain the prefix while another
is separated from it, and their corrections can have opposite signs.  AC-1
fixes only total signed cardinality.  It does not match its interval owners to
the mismatch occurrences.

The exact fallback retains, for every internal coefficient, its unordered-pair
owner and the rooted meet data needed by later translations.  This is a
`Theta(m^2)` owner/LCA state.  No scalar potential or bounded substitute is known.

## 7. Full-spectrum L6 gate-splitting control

Use the known order-six Leech labelling

```text
0--1:1,       0--2:2,       0--3:5,
3--4:4,       3--5:8.
```

Take `a=1,b=0,x=4,r=3,e=4` and `U={0,2,3,5}`.  This `x` is deliberately
noncanonical: vertex `4` is not a diameter endpoint.  The full owner partition
is nevertheless exact:

```text
D={2,5,7,8,13,15},
H={1,3,4,6,9,10,11,12,14},
D dot-union H=I_15.                                (FW280.18)
```

For the path with edge sequence `5,8`, its second step `(s,w)=(5,8)` has

```text
M^+_(5,8)={5,7},            M^-_(5,8)={3},
eta(5,8)=1.                                         (FW280.19)
```

The actual mismatch owners split as follows.

| sign | lower owner | translated owner | relation to prefix `b--r` |
|:---:|:---|:---|:---|
| `+` | `{b,r}`, distance 5 | `{a,x}`, distance 10 | source equals prefix |
| `+` | `{2,r}`, distance 7 | `{x,5}`, distance 12 | source contains prefix |
| `-` | `{a,2}`, distance 3 | `{r,5}`, distance 8 | tripod at gate `b` |

One signed window thus contains complete overlap, nested overlap and a
different-gate tripod.  Its corrections have no common strict direction.

This does **not** refute canonical anti-coalescence.  The canonical diameter
endpoint here is the weight-eight leaf `5`, not the selected leaf `4`.
Deleting the canonical leaf makes every remaining total path defect zero and
creates no collision.  L6 controls only generic full-interval uncrossing.

## 8. Infinite exact-top collision pressure family

For each integer `k>=4`, take

```text
a--1--b--(k+1)--c--(2k)--r--3--x,
                    |
                    k
                    |
                    y
```

The fifteen actual distances are

| owner | distance | owner | distance | owner | distance |
|:---|---:|:---|---:|:---|---:|
| `ab` | 1 | `rx` | 3 | `cy` | `k` |
| `bc` | `k+1` | `ac` | `k+2` | `cr` | `2k` |
| `by` | `2k+1` | `ay` | `2k+2` | `cx` | `2k+3` |
| `ry` | `3k` | `br` | `3k+1` | `ar` | `3k+2` |
| `xy` | `3k+3` | `bx` | `3k+4` | `ax` | `3k+5` |

They are pairwise distinct, with

```text
Spec(T_k)={1,3} union [k,k+2] union [2k,2k+3]
                    union [3k,3k+5].               (FW280.20)
```

At the artificial metric cap `D_k=3k+5`, deleting `x` leaves diameter
`3k+2`, while

```text
D_x={3,2k+3,3k+3,3k+4,3k+5}.
```

Thus `x` owns the exact top suffix `[D_k-2,D_k]`, and its first missing
deficit coordinate is `Q=3`.  This is q=1-shaped relative to `D_k`; it is not
the Leech identity `D_k=binom(6,2)`.

After deleting `a,x`, the core is the three-arm star at `c`, with weights
`k,k+1,2k`.  Its rooted data are

```text
B={0,k+1,2k+1,3k+1},
R={0,2k,3k,3k+1},             h=3k+1, e=3,

H=(1+B) dot-union (3+R) dot-union {3k+5}
 ={1,3,k+2,2k+2,2k+3,3k+2,3k+3,3k+4,3k+5}.
                                                        (FW280.21)
```

The external-hole transform satisfies

```text
phi(k)=k-2,       phi(k+1)=k-1,       phi(2k)=2k-3.
```

Hence the edge owner `{c,r}` of old distance `2k` and the path owner `{b,y}`
of old distance `2k+1` collide:

```text
phi(2k)=phi(k)+phi(k+1)=2k-3.                      (FW280.22)
```

The transformed core multiset is

```text
{k-2,k-1,2k-3,2k-3,3k-5,3k-4},                  (FW280.23)
```

with exactly one repetition.  When `k` is even, weighted parity splits the
vertices `4|2`, giving eight odd and seven even pair distances, exactly the
Taylor count for `I_15`.

The family is **not Leech**.  It always misses coefficient two and more low
values.  At `k=4`,

```text
Spec(T_4)=I_17-{2,7};                              (FW280.24)
```

relative to `I_15`, values `16,17` replace holes `2,7`.  The family conditions
force `k>=4`, so this analytic family cannot become a one-gap control.  It
shows that exact top ownership, two actual root rows, owner uniqueness and
Taylor parity do not replace full low coverage.

## 9. One-gap order-six diagnostic

An external temporary Z3 4.16.0 audit tested the gap between Sections 7 and 8:

```text
6 unlabelled order-six topologies,
58 ordered leaf pairs (a,x),
D in {15,16}, Q in {2,3,4,5},
464 rows.
```

Each row required a unit leaf at `a`, fifteen positive distinct actual tree
distances bounded by `D`, all non-`x` distances at most `D-Q`, the full
`x`-owned suffix `[D-Q+1,D]`, the transform from the actual incident-owner
set `H`, and a collision among the six transformed core distances.  All 464
rows returned `UNSAT`.  The encoding did not require a non-`x` distance to
equal `D-Q`, so it slightly relaxed exact endpoint deletion.

This is only **OBSERVED finite, external/non-replayed**.  No script, model
hash, proof log, certificate or independent replay was retained.  It is not
a hand proof or an all-order premise.  Its boundary is sharp in the tested
sense: dropping canonical `Q>=2` permits a noncanonical L6 collision, while
retaining exact `Q=3` but allowing two low holes permits `T_4` immediately.

No full-interface survivor was found.  Requiring an actual core, its actual
rows, actual leaf attachments, owner uniqueness and

```text
I_N=Spec(U) dot-union (1+B) dot-union (e+R) dot-union {L}
```

is no longer a relaxation: attaching the leaves gives an actual Leech tree.
A survivor would be a new Leech witness.

## 10. STOP and trust boundary

The exact progression reaches owner-labelled translation mismatches and then
stops: no-alignment forces gate/LCA/connector geometry, while minimality gives
no pairing or common direction for its corrections.

The next sufficient statement is:

> **UNVERIFIED canonical mismatch-gate transport theorem.**  Under canonical
> q=1 top ownership and full `I_N`, all AC-2 owner paths admit a global pairing
> or orientation which prevents equal transformed sums of different core paths.

Canonical top ownership and full low coverage must be used jointly.  L6 shows
that full coverage alone does not align gates; the pressure family shows that
exact top ownership alone does not prevent collision.  The fallback is the
`Theta(m^2)` owner/LCA state, for which no strict recursion is known.

Sections 2--6 use only path intersection in a tree, positive transformed
weights, the full coefficientwise partition, interval translation and actual
owner uniqueness.  The L6 and infinite-family calculations are exact hand
arithmetic.  Neither is a canonical full-state counterexample.  Section 9 is
external/non-replayed and not proof input.

FW280 creates no verifier or certificate, proves no anti-coalescence theorem,
excludes no order and does not prove G18.  Antecedents and controls:

```text
docs/unit-edge-owner-propagation-audit.md
docs/g18-closure-architecture-audit.md
data/known_leech_trees.json
```

Successor: FW281 derives the exact threshold and rooted-Kruskal convolution
ledgers, but canonical `L6` defeats every tested local gate orientation.  The
60k checkpoint therefore stops at `docs/canonical-mismatch-gate-transport-stop.md`.
