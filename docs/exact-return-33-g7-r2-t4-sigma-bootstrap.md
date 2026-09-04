# Exact-return `(3,3)` `g=7` `R2,t=4` slack bootstrap (FW307)

FW306 proves `xi_45<=70`.  FW307 runs one deeper exact rooted-support dynamic
program with a global budget of 54 holes.  The minimum hole count at each
layer simultaneously recovers eleven nested budget deaths.  Feeding each
death back into the exact deficit-span identity bootstraps every all-order
`R2,t=4` state to

```text
sigma>=55,       xi_55<=82.                            (FW307.1)
```

This is an exact finite reduction.  It still does not locate owner endpoints
or LCAs.

## 1. One global state space

The fixed row is

```text
k=n-2>=16,      P=binom(k,2),      N=binom(k+2,2),
s=P+2-sigma,
I_N=F_K+X^4+X^sD(1+X^4),
D intersect (D+4)=empty.                              (FW307.2)
```

Every rooted support contains

```text
D_0={0,1,3,8,11,14},
1<-0, 3<-1, 8<-1, 11<-1, 14<-8.                      (FW307.3)
```

The search processes offsets in increasing order.  It stores each feasible
depth support with the least number of holes used to reach it.  A complete
fixed-parent/LCA backtrack is called whenever a new depth is inserted; it
exhausts every smaller-depth parent and rejects repeated distances or distance
four.  Supports using more than 54 holes are discarded.  There is no other
state cutoff.

For a smaller budget `b<=54`, its exact death layer is the first offset at
which every global state has minimum hole count greater than `b`.  Thus one
global run certifies all smaller budgets without rerunning or sampling them.

The peak live layer contains 536,697 rooted-depth supports.

## 2. Exact nested deaths

The certified table is

| allowed holes `b` | first dead offset |
| ---: | ---: |
| 44 | 70 |
| 45 | 71 |
| 46 | 72 |
| 47 | 73 |
| 48 | 74 |
| 49 | 75 |
| 50 | 76 |
| 51 | 78 |
| 52 | 80 |
| 53 | 81 |
| 54 | 82 |

For example, death `44:70` means that any feasible rooted factor extending
through offset 70 has at least 45 holes.  Death `54:82` means that any factor
extending through 82 has at least 55.

## 3. Self-consistent all-order bootstrap

The exact available deficit span is

```text
W=N-s=2k+sigma-1.                                     (FW307.4)
```

Suppose the current proved lower bound is `sigma>=r`.  If the budget-`b`
death lies at or before `2k+r-1`, then every hypothetical value
`r<=sigma<=b` is impossible: its exact span already reaches the dead layer
but contains only `sigma<=b` holes.  Hence `sigma>=b+1`.

Starting with the FW304 row bounds gives:

```text
k=16: 40 ->45 ->46 ->...->55;
k=17: 46 ->47 ->...->55;
k=18: 52 ->53 ->54 ->55;
k>=19: FW304 already gives sigma>=59 and then increases. (FW307.5)
```

Therefore `sigma>=55` uniformly for every `k>=16`.  Its minimum exact span is

```text
W>=2(16)+55-1=86,                                     (FW307.6)
```

so the budget-54 death at 82 always lies inside the complete identity.  Every
one of those 55 holes is compensated by a unique actual internal pair of
`K`, proving (FW307.1).

The FW305 high-bridge condition `2s>N+2` requires

```text
sigma<=floor((P-2k)/2).
```

FW307 eliminates that branch completely at `k=16,17`; it can first reappear
at `k=18`.  This is a consequence, not a closure of the remaining orders.

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_sigma_bootstrap.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_sigma_bootstrap_certificate.json
```

**Exact finite proof:** the global budget-54 state space and all eleven
induced death layers.

**Proved all-order consequence:** `sigma>=55`, `xi_55<=82`, and elimination
of the high-bridge branch at `k=16,17`.

**Not proved:** any endpoint/LCA projection for the 55 owners, exclusion of
`R2,t=4`, the two-point cap, `g=7`, ERTC, NSSC, or global nonexistence.

**Verdict: SELF-CONSISTENT 55-OWNER/82-WINDOW STRICT STOP.**
