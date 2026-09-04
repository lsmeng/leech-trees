# Exact-return `(3,3)` `g=7` final-cap slack and punctured-tiling stop (FW303)

FW302 replaces the false first-activation obstruction by the globally last
activation.  FW303 combines that exact cut with the established rooted-span
bound and finite-hole ladder.  It proves uniform positive room, colours the
first nine holes, and isolates an exact two-vertex final-cap equation.  The
result is a strict stop, not an exclusion of `g=7`.

## 1. Last-cut notation and the fixed six-vertex side

Let a hypothetical Leech completion have order `n>=18`, put
`N=binom(n,2)`, and delete its globally heaviest edge `e=xy` of weight `s`.
Write

```text
x in K, y in H,       |K|=k, |H|=h,
D=R_{K,x},            R=R_{H,y}.
```

The five already fixed edges of weights `1,2,6,7,10` connect the six vertices
`z,b_1,b_2,c,d_6,a`.  A tree of order at least 18 has 17 distinct positive
integer edge weights, so its heaviest weight satisfies `s>=17>10`.  The five
fixed edges therefore all precede `e` and lie in `K`.  Hence

```text
k>=6,       k+h=n>=18.                                  (FW303.1)
```

FW302 gives the exact identity

```text
I_N = F_K + F_H + X^s D R,                              (FW303.2)
```

where `DR` is direct, disjoint from both internal spectra, and supported in
`[s,N]`.  Define the number of internal owners above `s` by

```text
sigma=N+1-kh-s.                                         (FW303.3)
```

## 2. Uniform nine-hole theorem

Let `C_j=binom(j,2)`.  The independently established all-order rooted-span
bound gives

```text
max(D)+max(R)
 >= ceil((C_k+C_h)/2)+min(ceil(C_k/2),ceil(C_h/2)).      (FW303.4)
```

Since `s+max(D)+max(R)<=N`, equations (FW303.3--4) imply the following.

* If `h=1`, then `k>=17` and
  `sigma>=ceil(C_k/2)+1-k>=52`.
* If `h=2`, then `k>=16` and
  `sigma>=ceil((C_k+1)/2)+2-2k>=31`.
* If `h=3`, then `k>=15` and `sigma>=12`.

For each fixed `h<=3`, the displayed lower bound is increasing from its
listed boundary: increasing `k` by one raises its ceiling term by at least
`floor(k/2)` and subtracts only `h`.  If `h>=4`, (FW303.1) gives `kh>=56`:
for `4<=h<=12` the minimum of `h(18-h)` is 56, while `h>=13` gives
`kh>=6*13=78`.  The certified finite-hole ladder already gives
`sigma>=9` whenever `kh>=44`.  Therefore every final cut in the present
branch satisfies

```text
sigma>=9.                                               (FW303.5)
```

If `xi_1<...<xi_9` are the first nine positive deficits absent from `D+R`,
then the same exact ladder locates them:

```text
xi_1<=10, xi_2<=19, xi_3<=22, xi_4<=31, xi_5<=34,
xi_6<=37, xi_7<=40, xi_8<=48, xi_9<=51.                 (FW303.6)
```

Thus every `s+xi_i` is an actual within-component distance, not merely a
formal missing sum.

## 3. Which side owns the holes

The component `H` has `h-1` edge weights, all strictly below the global
heaviest weight `s`.  Consequently at most

```text
binom(h,2)-(h-1)=binom(h-1,2)                           (FW303.7)
```

of its internal pairs can lie above `s`.  Combining (FW303.5--7) with the
stronger small-`h` bounds gives:

| `h` | first nine holes forced into `K` | all `K`-internal distances above `s` |
| ---: | ---: | ---: |
| 1 | 9 | at least 52 |
| 2 | 9 | at least 31 |
| 3 | 8 | at least 11 |
| 4 | 6 | at least 6 |
| 5 | 3 | at least 3 |

For `h>=6`, this elementary side count alone does not force one of the first
nine owners into `K`.

## 4. The exact rooted-difference restriction

Root `K` at the endpoint `x`.  For any edge `uv` of weight `w` in a rooted
tree, one endpoint is the parent of the other, so

```text
|d(x,u)-d(x,v)|=w.
```

The fixed core edges therefore force

```text
{1,2,6,7,10} subset (D-D)^+.                            (FW303.8)
```

Directness of `D+R` is equivalent to
`(D-D)^+ intersect (R-R)^+=empty`.  Hence

```text
(R-R)^+ intersect {1,2,6,7,10}=empty.                   (FW303.9)
```

For a larger `H`, (FW303.9) also excludes virtual differences between two
root depths, so it is stronger than merely saying that edge weights cannot be
reused.  For `h=2`, however, its only positive rooted difference is its edge
weight; in that branch (FW303.9) adds no more than global edge-weight
distinctness.

Reflecting the rooted sets at their maxima produces
`D*=max(D)-D` and `R*=max(R)-R`; their sum is still direct.  If
`M=s+max(D)+max(R)`, then every value in `[M+1,N]` is internally owned.
This exact top reflection does not determine whether those owners are rooted
depth differences, which is the remaining geometric gap.

## 5. Exact singleton and two-vertex final caps

If `h=1`, then `R={0}` and `F_H=0`, so

```text
I_N=F_K+X^sD,       Spec(K) contains [1,s-1].            (FW303.10)
```

All `sigma>=52` internal owners above `s` also lie in `K`.  The rooted
difference condition is vacuous, so this pendant-final-cap branch requires a
separate cap or descent argument.

If `h=2`, let its unique edge have weight `t<s`.  Then `R={0,t}` and
`F_H=X^t`, and (FW303.2) becomes the exact punctured tiling

```text
I_N = F_K + X^t + X^s D(1+X^t),                         (FW303.11)
D intersect (D+t)=empty,
s+max(D)+t<=N,
Spec(K) intersect [1,s-1]=[1,s-1] minus {t}.
```

Here

```text
sigma=N+1-2k-s>=31,                                     (FW303.12)
```

and `H` has no internal owner above `s`.  Therefore all `sigma` internal
owners above `s` lie in `K`; in particular `K` owns `s+xi_i` for the nine
offsets bounded in (FW303.6).

The smallest live successor is now exact.

> **TWO-VERTEX FINAL-CAP PUNCTURED-TILING LEMMA.**  No rooted
> distance-injective weighted tree `K` containing the fixed `q/r` core can
> satisfy (FW303.11--12), the cap, the fixed owner structure, and the nine
> located `K`-internal holes for any `n>=18`.

## 6. Why difference disjointness alone cannot prove it

The following connected order-12 pressure tree has edges

```text
(0,1,1), (0,2,2), (6,7,4), (8,9,5), (3,4,6),
(0,3,7), (0,5,10), (6,8,16), (4,7,18),
(10,11,19), (7,10,50).
```

All 66 pair distances are distinct.  It has the exact `(3,3,0)` return and
the nontrivial sink `{0,3,4,6,7}`.  Its globally heaviest edge is the final
activation `(7,10,50)`.  Deleting that edge gives orders `(10,2)` and

```text
D={0,4,18,20,24,25,31,32,33,41},       R={0,19},
(D-D) intersect (R-R)={0}.                              (FW303.13)
```

It is not Leech: its first missing distance is 26 and its maximum distance is
110, above `N_12=66`.  Thus actual rooted geometry and difference-set
disjointness can coexist; the full interval and global cap in (FW303.11) are
load-bearing.

## 7. Exact remaining bridge and trust boundary

The located values `s+xi_i` have actual owner pairs `u_i,v_i` inside `K`.
They need not equal a rooted-depth difference: if their path crosses branches
relative to `x`, the least-common-ancestor term intervenes.  No current
theorem forces enough of these near-heaviest owner pairs to be
ancestor--descendant pairs or to share a projection gate.  That is the
precise missing bridge in the two-vertex branch.

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_final_cap_punctured_tiling_stop.py
theory-lab/topwindow/results/exact_return_33_g7_final_cap_punctured_tiling_stop_certificate.json
```

**Proved analytically:** the uniform `sigma>=9` theorem, nine located holes,
the side-coloured hole table, the fixed forbidden rooted differences, and the
exact `h=1,2` identities.

**Independently replayed inputs:** heaviest-edge rigidity, the finite-hole
ladder, and the order-12 distance-injective pressure control.

**Not proved:** the two-vertex punctured-tiling lemma, the singleton branch,
the `h>=3` no-grazing branches, exclusion of `g=7`, ERTC, NSSC, or global
Leech-tree nonexistence.

**Verdict: NINE-HOLE LAST-CUT REDUCTION + TWO-VERTEX PUNCTURED-TILING STRICT
STOP.**
