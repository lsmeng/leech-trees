# Exact-return `(3,3)` `g=7` `R2,t=4` owner-trim stop (FW305)

FW304 leaves three two-point final-cap rows.  FW305 fixes the smallest one,
`R2,t=4`, and keeps the complete rooted geometry instead of only the first
nine numerical hole bounds.  The first seven holes are uniquely forced; their
actual `K`-owner paths obey a recursive endpoint-trim law.  A new exact
dichotomy either removes every small endpoint trim or increases the dense
owner obligation to 45 owners by offset 79.

This is still a strict stop.  It does not classify how the resulting owner
paths intersect in the interior.

## 1. Fixed row

Keep the notation of FW304.  Thus

```text
k=n-2>=16,        P=binom(k,2),        N=binom(k+2,2),
s=P+2-sigma,
I_N=F_K+X^4+X^s D(1+X^4),
Spec(K) intersect [1,s-1]=[1,s-1] minus {4},
D intersect (D+4)=empty,
s+max(D)+4<=N.                                      (FW305.1)
```

The final bridge endpoint is `x=b_1`.  The six fixed rooted depths and their
parent relations are

```text
D_0={0,1,3,8,11,14},
1<-0,   3<-1,   8<-1,   11<-1,   14<-8.             (FW305.2)
```

The complete fixed-core pair spectrum is

```text
S_0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,23},       (FW305.3)
```

where the actual core edge weights are only `{1,2,6,7,10}`.

## 2. Exact forced prefix

Enumerate every possible rooted support `D` through offset 22.  A state keeps
the current depth support; for every state the oracle enumerates all complete
positive-weight parent maps.  At offset `j` the coefficient of the two-point
cross factor is

```text
1_D(j)+1_D(j-4).                                      (FW305.4)
```

States with coefficient two, a rooted pair distance four, a wrong fixed-core
parent, or an unrealizable rooted metric are rejected.  Future fixed depths
from (FW305.2) are present in every realizability check.  This look-ahead is
safe: a later vertex has greater root depth and cannot change an earlier
vertex's parent or the LCA distance of an already present pair.

There is exactly one depth-support state after every offset through 18.  Its
hole set is

```text
H_7={2,6,9,10,13,16,17}.                              (FW305.5)
```

Branching begins only at 19.  The numbers of exact depth-support states after offsets
`19,20,21,22` are respectively `2,3,5,6`; every one retains the same first
seven holes.  Thus (FW305.5) strengthens FW304's coordinatewise upper bounds:
these are the uniquely forced first seven holes, not merely seven holes that
occur no later than the displayed offsets.

By the complete identity (FW305.1), for every `h` in `H_7` there is a unique
actual `K`-pair path `P_h` of length

```text
length(P_h)=s+h.                                      (FW305.6)
```

The exact enumeration is finite evidence replayed by the FW305 verifier.  No
beam, state cap, or heuristic parent choice is used.

## 3. Endpoint-trim recursion

The following step is analytic and all-order.

> **Endpoint-trim lemma.**  Let `P_h` be a `K`-owner path of length `s+h`,
> where `h` is a cross hole.  If an endpoint edge of `P_h` has weight
> `w<=h`, then `w<h`, `h-w` is an earlier cross hole, and deleting that edge
> leaves exactly the unique owner path `P_(h-w)`.

Indeed, deleting the endpoint edge leaves a `K`-pair at distance
`s+h-w`.  If `w=h`, this repeats the final bridge's distance `s`.  If
`w<h` and `h-w` is cross-owned, it repeats that cross distance.  Distance
injectivity leaves only the earlier-hole case, whose internal owner is unique.

An edge weight belonging to `S_0` but not to `{1,2,6,7,10}` is also
impossible: the corresponding fixed-core non-edge pair already owns that
distance.  Weight four is absent from `Spec(K)`.  Applying these facts at both
ends of every path in (FW305.5) gives the complete table

| owner | possible endpoint trim `w -> earlier owner` | otherwise each endpoint edge is at least |
| --- | --- | ---: |
| `P_2` | none | 3 |
| `P_6` | none | 7 |
| `P_9` | `7 -> P_2` | 10 |
| `P_10` | `1 -> P_9` | 11 |
| `P_13` | `7 -> P_6` | 14 |
| `P_16` | `6 -> P_10`, `7 -> P_9`, `10 -> P_6` | 17 |
| `P_17` | `1 -> P_16`, `7 -> P_10` | 18 |

Every surviving small trim is therefore one of the already fixed core edges.
It is not a free edge of the same weight.

## 4. High-bridge versus dense-window dichotomy

Put `A=max(D)`.  From the cap in (FW305.1),

```text
A<=N-s-4.                                             (FW305.7)
```

Suppose a surviving trim exposes `P_j` at the inner endpoint of its fixed
core edge.  If that endpoint has `b_1`-depth `delta`, the triangle inequality
and (FW305.7) give

```text
s+j<=A+delta<=N-s-4+delta,
2s<=N+delta-j-4.                                      (FW305.8)
```

Checking the seven displayed trim types, the largest right correction is
`delta-j-4=2`, attained only by `P_9 -> P_2` across the weight-seven edge,
whose deeper endpoint has depth eight.  Hence

```text
2s>N+2                                                (FW305.9)
```

eliminates every small trim simultaneously.  In that branch all fourteen
endpoint incidences of the seven paths satisfy the lower bounds in the last
column of the table.

The complementary branch automatically supplies more owners.  Since

```text
s=P+2-sigma,       N=P+2k+1,
```

condition (FW305.9) is equivalent to

```text
sigma<=floor((P-2k)/2).                               (FW305.10)
```

If (FW305.10) fails, then `sigma>=45` for every `k>=16`; equality can occur
only at `k=16`.  The rooted-capacity function

```text
m(L)=max{m: binom(m,2)<=2L}
```

gives `m(79)=18` and `m(75)=17`.  If the deficit span reaches 79, at least

```text
80-m(79)-m(75)=45                                    (FW305.11)
```

offsets in `[0,79]` are holes.  If the span ends earlier, all `sigma>=45`
holes have already occurred.  Thus every hypothetical completion satisfies
the exact alternative

```text
(A) 2s>N+2 and all seven P_h are endpoint-heavy; or
(B) at least 45 actual K owners occur in [s+1,s+79].  (FW305.12)
```

This supersedes the undifferentiated `40`-owner/offset-73 statement only in
the complementary branch; it does not claim 45 owners in branch (A).

## 5. Sharp `t=4` local pressure control

The fixed core itself yields a useful actual control.  Add a cap edge of
weight four and join its root to `b_1` by a final bridge of weight 21:

```text
(0,1,1), (0,2,2), (3,4,6), (0,3,7), (0,5,10),
(6,7,4), (1,6,21).                                    (FW305.13)
```

This order-eight tree has all 28 pair distances distinct, the exact
`R2,t=4` rooted core, first cross hole two, and an actual compensating owner
`23:{4,5}=s+2`.  Its maximum distance is 39, below the ambient order-18 cap
153.  It first misses global distance five, so it does not satisfy the
almost-complete low spectrum and is not Leech.

The control shows that the exact root, cap weight, coherent LCA geometry, and
an actual first-hole owner do not themselves contradict distance injectivity.

## 6. Exact remaining intersection problem

Branch (A) leaves the smaller theorem-shaped target:

> **Seven-path intersection lemma.**  No rooted distance-injective tree
> satisfying (FW305.1--3) can contain the seven unique paths (FW305.6) if
> every endpoint edge of `P_h` is greater than `h`.

A proof must use how the seven paths share interior segments and projection
gates.  Endpoint heaviness alone does not determine their LCAs.  Branch (B)
retains the owner-to-projection problem, now with 45 actual owners by offset
79.

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_owner_trim_stop.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_owner_trim_stop_certificate.json
```

**Proved analytically:** the endpoint-trim lemma and the high-bridge/dense-
window dichotomy.

**Exact finite audit:** the unique seven-hole prefix, all small-trim rows, and
the order-eight `t=4` pressure control.

**Not proved:** the seven-path intersection lemma, the dense owner-to-
projection lemma, exclusion of `R2,t=4`, the two-point cap, `g=7`, ERTC, NSSC,
or global Leech-tree nonexistence.

**Verdict: SEVEN FORCED OWNERS + ENDPOINT-TRIM DICHOTOMY STRICT STOP.**
