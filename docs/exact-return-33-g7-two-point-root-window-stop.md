# Exact-return `(3,3)` `g=7` two-point root/window stop (FW304)

FW303 reduces a two-vertex final cap to an exact punctured tiling.  FW304
uses the complete fixed-core metric, not only its five edge weights.  The
first cross hole is now one of `1,2,3`, the attachment root falls into three
explicit rows, and a missing-slot count turns the cap bound into at least 35
actual high owners in a fixed 66-offset window.  Exact rooted-parent searches
sharpen the first nine holes in every row.

This remains a strict stop.  It does not prove the owner-to-projection lemma
needed to exclude the two-vertex cap.

## 1. Exact state and fixed-core spectrum

Put

```text
k=n-2,       N=binom(n,2),       P=binom(k,2).
```

For the last/heaviest bridge of weight `s`, let `x` be its endpoint in `K`.
The two-vertex rootless cap has edge weight `t<s`, and
`D=R_{K,x}`.  FW303 gives

```text
I_N = F_K + X^t + X^s D(1+X^t),                        (FW304.1)
D intersect (D+t)=empty,
s+max(D)+t<=N,
Spec(K) intersect [1,s-1]=[1,s-1] minus {t},
sigma=N+1-2k-s=P+2-s.                                  (FW304.2)
```

The fixed six-vertex core has edges

```text
z--b_1:1,   z--b_2:2,   c--d_6:6,   z--c:7,   z--a:10.
```

Its complete pair spectrum is

```text
S_0={1,2,3,6,7,8,9,10,11,12,13,14,15,17,23}.          (FW304.3)
```

Since `t` is owned by the cap and is absent from `Spec(K)`, it cannot belong
to `S_0`.  In particular

```text
t>=4.                                                   (FW304.4)
```

## 2. Three exact first-hole/root rows

Let

```text
xi=min({1,2,...} minus (D union (D+t))).
```

Then `s+xi` is the first internal owner above `s`; because the cap has no
internal distance above `s`, it is an actual `K`-pair.

The certified FW283 rooted-prefix table, specialized to the factor
`{0,t}`, has a singleton shallow second factor only at holes `1,2,3`.
Equation (FW304.4) keeps `t` invisible throughout that prefix.  Therefore

```text
xi in {1,2,3},       t>xi.                              (FW304.5)
```

The same table fixes the shallow part of `D`, and the unique fixed edges of
weights one and two identify the root.

```text
R1: xi=1,  1 notin D,          x notin {z,b_1};
R2: xi=2,  D begins {0,1},     x=b_1;
R3: xi=3,  D begins {0,1,2},   x=z.                    (FW304.6)
```

The exact fixed-core root depths in the last two rows are

```text
R2: {0,1,3,8,11,14},
R3: {0,1,2,7,10,13}.                                   (FW304.7)
```

Combining (FW304.3--5) gives the cap regimes

```text
R1:       t in {4,5} or t>=16, with t notin {17,23};
R2,R3:    t=4     or t>=16, with t notin {17,23}.       (FW304.8)
```

The value five is additionally excluded in `R2` by the fixed depth
difference `8-3`, and in `R3` by `7-2`.  In `R2,R3` the cap is coloured `B`,
because its final bridge attaches at `b_1` or `z`.

## 3. Radius bound plus missing-slot gain

Write

```text
A=max(D),      R_0=ceil(P/2),      p=P mod 2.
```

The `P` internal distances of `K` are distinct and at most `2A`, so
`A>=R_0`.  The cap inequality in (FW304.1) gives

```text
sigma >= R_0+t-2k+1.                                   (FW304.9)
```

There is a strict additional gain that is absent from the generic rooted-span
bound.  Put

```text
b=R_0+t-2k+1,       sigma=b+q,       q>=0.
```

The cap gives `A<=R_0+q`.  Hence all `P` distances of `K` lie in
`[1,B]`, where

```text
B=2(R_0+q)=P+p+2q.
```

Exactly `B-P=p+2q` integer slots in this interval are unavailable to `K`.
But `t` and every cross value `s+d,s+t+d` lying below `B` are distinct
unavailable slots.

In `R1`, use only `d=0`.  The three slots `t,s,s+t` are below `B`, because

```text
B-(s+t)=R_0+p-2k-1+3q >=27.                            (FW304.10)
```

Thus `p+2q>=3`, or `q>=2-p`.

In `R2,R3`, use all six fixed depths in (FW304.7).  Their maximum is at most
14, and (FW304.10) leaves at least 27 even when `q=0`.  Therefore `t` plus
the twelve cross values are thirteen distinct missing slots:

```text
p+2q>=13,       q>=7-p.                                (FW304.11)
```

The resulting all-order bounds are:

| row | small cap (`t=4`, also the `R1` value 5) | late cap (`t>=16`) |
| --- | ---: | ---: |
| `R1` | `sigma>=35` | `sigma>=47` |
| `R2,R3` | `sigma>=40` | `sigma>=52` |

The minima occur at `k=16`; the expressions increase thereafter.  Thus the
FW303 value 31 and the first Pro refinement 33 are both superseded.

## 4. Fixed high-owner windows

For an integer `L>=0`, let

```text
m(L)=max{m: binom(m,2)<=2L}.
```

At most `m(L)` vertices can have root depth at most `L`: all their mutual
distances are distinct and at most `2L`.  Consequently the direct cross set
`D union (D+t)` occupies at most

```text
m(L)+m(L-t)                                             (FW304.12)
```

coefficients of `[0,L]`.  All remaining coefficients in the available
deficit span are actual `K`-internal owners.

Applying (FW304.12), with the total-span fallback when the span ends earlier,
gives:

```text
all rows:              xi_35<=66;
all rows, t>=16:       xi_47<=80;
R2 or R3:              xi_40<=73;
R2 or R3, t>=16:       xi_52<=87.                      (FW304.13)
```

For example, `N-s=2k+sigma-1>=66` in every row, while

```text
m(66)+m(62)=16+16=32;
67-32=35.
```

For the late universal row, if `N-s<=79` the forty-seventh hole already lies
there; otherwise `[0,80]` is available and
`81-m(80)-m(64)=81-18-16=47`.  The other two fallback calculations are
identical.  These are actual-owner density statements, not moment estimates.

## 5. Exact specialized first-nine ladders

Fixing the second rooted factor to `{0,t}` makes the finite-hole recursion
much smaller.  The verifier retains every rooted depth support and every
parent map, with no beam or state cutoff.  The generic exact bounds are

| cap regime | `(xi_1,...,xi_9)` upper bounds |
| --- | --- |
| `t=4` | `(3,9,12,14,16,18,21,23,24)` |
| `t=5` | `(3,6,12,13,17,18,20,22,23)` |
| `t>=16` | `(3,5,7,9,10,11,13,14,15)` |

Imposing the exact fixed core depths and parent relations in `R2,R3` gives

| row | cap regime | `(xi_1,...,xi_9)` upper bounds |
| --- | --- | --- |
| `R2` | `t=4` | `(2,6,9,10,13,16,17,20,22)` |
| `R2` | `t>=16` | `(2,4,5,6,7,9,10,12,13)` |
| `R3` | `t=4` | `(3,8,9,12,15,16,19,21,23)` |
| `R3` | `t>=16` | `(3,4,5,6,8,9,11,12,14)` |

For `t>=16`, the search deliberately treats the positive cap depth as still
invisible and does not use the later forbidden difference.  The bounds are
therefore uniform for every allowed late `t`; the exact fixed-parent
look-ahead is safe because later vertices have greater root depth and cannot
repair an earlier parent/LCA collision.

## 6. Sharp local pressure controls

Start with

```text
(0,1,1), (0,2,2), (6,7,4), (8,9,5), (3,4,6),
(0,3,7), (0,5,10), (6,8,16), (4,7,18), (10,11,19).
```

Add one of the following final bridges:

| row | bridge | first compensated `K` owner | sink | maximum distance |
| --- | --- | --- | --- | ---: |
| `R1` | `(7,10,50)` | `51:{0,8}` | `{0,3,4,6,7}` | 110 |
| `R2` | `(1,10,59)` | `61:{5,8}` | `{0,1,3,4,6,7}` | 135 |
| `R3` | `(0,10,63)` | `66:{5,9}` | `{0,3,4,6,7}` | 138 |

Each order-12 tree has all 66 pair distances distinct, exact return
`(3,3,0)`, a direct final rooted sum with `{0,19}`, first cross hole
respectively `1,2,3`, and a nontrivial sink.  All three stay below the ambient
order-18 cap 153.

They are not Leech: all first miss distance 26 and fail the complete identity
(FW304.1).  They show that the two-point factor, root localization, coherent
LCA geometry, a compensated first hole, the sink condition, and the numerical
ambient cap still do not suffice.  The punctured low spectrum and dense high
owner window are load-bearing.

## 7. Exact remaining lemma

> **ROOT-LOCALIZED 66-WINDOW OWNER LEMMA.**  In none of the rows `R1,R2,R3`
> can a rooted distance-injective tree `K` containing the fixed core satisfy
> simultaneously the punctured low spectrum in (FW304.1),
> `D intersect (D+t)=empty`, the global cap, and at least 35 actual
> `K`-internal owners in `[s+1,s+66]`.

A useful proof must convert the actual paths owning those high coefficients
into one of:

1. a rooted-depth difference `t`, contradicting directness;
2. a cross distance above `N`;
3. a proper inherited exact-return state.

The missing step is still LCA-sensitive.  For a high owner `u,v`,

```text
d(u,v)=d(x,u)+d(x,v)-2d(x,LCA_x(u,v));
```

its length does not determine `|d(x,u)-d(x,v)|`.  Neither the finite ladders,
the slot count, parity, first moments, nor reflected support controls that
projection term.

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_two_point_root_window_stop.py
theory-lab/topwindow/results/exact_return_33_g7_two_point_root_window_stop_certificate.json
```

**Proved analytically:** the three root rows, cap regimes, missing-slot excess
bounds, and owner-window bounds.

**Exact finite audit:** all seven specialized first-nine tables and the three
pressure controls.

**Not proved:** the 66-window owner lemma, the two-vertex cap exclusion, the
singleton or `h>=3` branches, `g=7`, ERTC, NSSC, or global Leech-tree
nonexistence.

**Verdict: THREE ROOT ROWS + DENSE OWNER-WINDOW STRICT STOP.**
