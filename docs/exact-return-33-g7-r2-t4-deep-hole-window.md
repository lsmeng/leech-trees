# Exact-return `(3,3)` `g=7` `R2,t=4` deep hole window (FW306)

FW305 identifies the uniquely forced first seven owner paths and gives an
endpoint-trim reduction.  FW306 pushes the same exact rooted-support search
past the local prefix.  A complete 44-hole-budget enumeration dies at offset
70.  Since every hypothetical completion reaches that offset, the row has at
least 45 actual `K` owners by offset 70 and `sigma>=45`.

This is a certified finite strengthening of the owner window, not the missing
owner-to-projection theorem.

## 1. Exact search state

Use the FW305 row

```text
k=n-2>=16,       P=binom(k,2),       N=binom(k+2,2),
s=P+2-sigma,
I_N=F_K+X^4+X^s D(1+X^4),
D intersect (D+4)=empty,
s+max(D)+4<=N.                                      (FW306.1)
```

The final bridge root is `b_1`, and every state contains the exact rooted
core

```text
D_0={0,1,3,8,11,14},
1<-0,   3<-1,   8<-1,   11<-1,   14<-8.             (FW306.2)
```

At offset `j`, the cross coefficient is

```text
1_D(j)+1_D(j-4).                                     (FW306.3)
```

The search stores every surviving depth support and the number of holes used.
Whenever a new depth is inserted, a complete parent/LCA backtrack tries every
smaller-depth parent, subject only to the five fixed parents in (FW306.2).
It rejects a parent choice exactly when it creates a nonpositive distance, a
repeated pair distance, or distance four.  It stops at the first feasible
complete parent map only because the state question is existential.  There is
no beam, topology sample, state cap, or heuristic parent choice.

## 2. Exhaustive death

Allow at most 44 holes.  The live depth-support counts at selected offsets are

| processed offset | live supports |
| ---: | ---: |
| 10 | 1 |
| 20 | 3 |
| 30 | 45 |
| 40 | 460 |
| 50 | 4,618 |
| 60 | 39,365 |
| 70 | 0 |

The maximum live layer contains 51,833 supports.  Emptying while processing
70 means that no feasible rooted factor can have only 44 holes through that
offset.  Therefore

```text
xi_45<=70.                                             (FW306.4)
```

The indexing is important: budget 44 proves a bound on the forty-fifth hole.

## 3. Why offset 70 is inside every completion

FW304 already proves `sigma>=40` in this row.  The exact deficit span is

```text
N-s=2k+sigma-1>=2(16)+40-1=71.                         (FW306.5)
```

Thus all coefficients through offset 70 belong to the complete identity
(FW306.1); the search never relies on a coefficient beyond the available
span.  Every hole there must be compensated by a unique actual internal pair
of `K`.  Consequently

```text
sigma>=45,
#(Spec(K) intersect [s+1,s+70])>=45.                  (FW306.6)
```

At the minimum order `k=16`, this replaces FW304's `sigma>=40` by 45.  In
particular it eliminates FW305's high-bridge alternative `2s>N+2` at that
order, because that alternative would require `sigma<=44`.  For larger `k`
the high-bridge alternative can remain, but it now coexists with the same
45-owner/offset-70 obligation.

The progression of certified windows is therefore

```text
FW304: 40 owners by offset 73  (capacity bound),
FW305: 45 owners by offset 79  in the complementary branch,
FW306: 45 owners by offset 70  in every R2,t=4 state.   (FW306.7)
```

## 4. Remaining projection problem

The finite search knows which coefficients must have internal owners but not
the endpoints of those owners.  For a named owner `u,v`, its offset still
contains the uncontrolled term

```text
d(u,v)=d(b_1,u)+d(b_1,v)-2d(b_1,LCA(u,v)).             (FW306.8)
```

Thus 45 located values do not yet imply that two root depths differ by four.
The next falsifiable target is now smaller and denser:

> **70-window projection lemma.**  A rooted distance-injective `K` containing
> the fixed core cannot have the punctured low spectrum from (FW306.1),
> `D intersect (D+4)=empty`, the cap, and 45 actual internal owners in
> `[s+1,s+70]`.

The first seven of these owners are exactly
`2,6,9,10,13,16,17` and carry the endpoint-trim alternatives already proved
in FW305.  Any useful next proof should retain those endpoints and project
the remaining owner paths to the fixed `b_1--z` edge or to their common
intersection tree.

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_deep_hole_window.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_deep_hole_window_certificate.json
```

**Exact finite proof:** the 44-hole state space is empty at offset 70, with
all rooted-parent realizations exhausted.

**Proved consequence:** every all-order `R2,t=4` completion has `sigma>=45`
and at least 45 actual `K` owners by offset 70.

**Not proved:** the 70-window projection lemma, exclusion of `R2,t=4`, the
two-point cap, `g=7`, ERTC, NSSC, or global Leech-tree nonexistence.

**Verdict: EXACT 45-OWNER/70-WINDOW STRICT STOP.**
