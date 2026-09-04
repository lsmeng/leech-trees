# Exact-return `(3,3)` `g=7` small-order top-strip handoff (FW313)

FW312 puts the paired receiving distances `t,t+4` in the punctured low
interval for every order at least 36, but left `18<=n<=35` as a bounded
obligation. FW313 combines Taylor's necessary order condition, the
repository's independently replicated order-18 exclusion, the forced
`R2,t=4` hole prefix, and the exact gate table. The whole bounded interval
collapses to 41 arithmetic rows at orders 25 and 27, and every row lands in
the five-value top strip `s,...,s+4` whose owner is already named.

This is a finite handoff, not an exclusion of those 41 rows.

## 1. Removing the unstructured bounded interval

Taylor's necessary condition says that a Leech-tree order is a square or a
square plus two. Hence the only admissible orders in `18<=n<36` are

```text
18, 25, 27.                                                (FW313.1)
```

The repository's four-way replicated forced-forest computation excludes
order 18. Thus a failure of the FW312 receiving-window inequality below order
36 can occur only at order 25 or 27.

All `n-1` edge weights are distinct positive integers and are bounded by the
globally heaviest edge `s). Therefore

```text
s>=n-1>=24.                                               (FW313.2)
```

## 2. Exceptional gates and offsets

Recall

```text
c=min(c_alpha,c_beta),
c<c_other,       c+c_other=s-h_0,
t=a+c.                                                   (FW313.3)
```

FW312 puts `t+4` below `s` whenever

```text
s+h_0>=2a+9.                                             (FW313.4)
```

If (FW313.4) fails, (FW313.2) and `h_0>=2` immediately exclude every gate
with `a<=8`. Only

```text
gate g=a:        a=11,
gate g=d_6:      a=14                                   (FW313.5)
```

remain. Failure also gives `h_0<=12`. The exact forced hole prefix through
12 is

```text
{2,6,9,10}.                                             (FW313.6)
```

Consequently every exception satisfies

```text
g in {a,d_6},       h_0 in {2,6,9,10}.                  (FW313.7)
```

## 3. Exact 41-row enumeration

For each case in (FW313.7), the replay enumerates every integer tuple obeying

```text
s>=24,
1<=c<c_other,
c+c_other=s-h_0,
c,c_other not in the FW311 forbidden set for g,
a+c+4>=s.                                               (FW313.8)
```

The result is exactly:

| statistic | count |
| --- | ---: |
| union rows for orders 25 and 27 | 41 |
| rows still available at order 27 (`s>=26`) | 23 |
| gate `a` | 3 |
| gate `d_6` | 38 |
| `h_0=2,6,9,10` | 29, 9, 1, 2 |
| `t-s=-4,-3,-2,-1,0` | 19, 11, 6, 3, 2 |

No row has `s>33`. The complete ordered row list is frozen in the
certificate with SHA-256

```text
d5af5b66b0df4d7a21b35c3ae3a7694d6192c3e983af5c38c56d2bc040bf48a1.
                                                               (FW313.9)
```

Thus the bounded exception is not an arbitrary order range or low-owner
problem:

```text
t in {s-4,s-3,s-2,s-1,s},
t+4 in {s,s+1,s+2,s+3,s+4}.                            (FW313.10)
```

## 4. Every second receiver is named

The exact final-cap identity names the unique owner of every value in the
right-hand set of (FW313.10):

| value | exact owner relative to the remote carrier |
| --- | --- |
| `s` | final bridge edge, entirely on the `L` side |
| `s+1` | final-cap cross owner at fixed `b_1`-depth 1, on the `L` side |
| `s+2` | the unique internal owner `P_2` |
| `s+3` | final-cap cross owner at fixed depth 3, on the `L` side |
| `s+4` | final bridge followed by the weight-four cap, on the `L` side |

When `h_0=2`, `P_2` is the chosen minimal remote owner and is
`J`-internal. When `h_0>2`, `P_2` cannot be `J`-internal relative to
this remote packet—otherwise offset two would be an earlier remote
owner—but it can still be `L`-internal or cross the carrier. This distinction
is retained in every certificate row.

For the two rows with `t=s`, the first receiver is itself the named final
bridge. In the other 44 rows, `t<s` and has its unique punctured-low
`K`-owner.

## 5. Successor obligation

The small-order branch is now:

> **Top-Strip Reception Exclusion.** Exclude the 41 certified rows using the
> named owner of `t+4`, the actual owner of `t`, the carrier direct product,
> LCA geometry, and the no-outlier cap.

For 35 of the 41 rows, the owner of `t+4` is a completely fixed `L`-side
cap/bridge path. Six rows use `P_2); their `h_0=2` versus `h_0>2`
carrier class is already separated. This is strictly smaller than a generic
bounded-order search.

## 6. Trust boundary

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_small_order_top_strip.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_small_order_top_strip_certificate.json
```

**Proved analytically:** reduction to gates `a,d_6`, offsets
`2,6,9,10`, and the named top-strip owners, conditional on Taylor and the
order-18 theorem.

**Exact finite audit:** all 41 integer rows, their counts, hashes, and owner
classes.

**External inputs:** Taylor's necessary order condition is literature input;
the order-18 exclusion is the repository's replicated computational main
theorem and is not rerun by this verifier.

**Not proved:** top-strip reception exclusion, large-order paired-reception
exclusion, remote packet exclusion, `R2,t=4`, the two-point cap, `g=7`,
ERTC, NSSC, or global nonexistence.

**Verdict: BOUNDED INTERVAL COLLAPSED TO 41 NAMED TOP-STRIP ROWS.**
