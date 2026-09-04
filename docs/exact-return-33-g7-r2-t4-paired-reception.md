# Exact-return `(3,3)` `g=7` paired low-owner reception (FW312)

FW311 turns the least remote carrier path into two complementary lengths
`c_alpha,c_beta` and four forbidden depths in the opposite rooted factor.
FW312 asks where the actual low-distance owners of one forbidden pair can
live. For every order at least 36, the smaller complementary length produces
two receiving distances separated by four inside the punctured low interval.
Their carrier-cut colors give nine finite cases; the cross--cross case reduces
to three exact rectangles.

This is a reception-state reduction, not a reception exclusion.

## 1. The paired receiving distances

Retain the FW311 notation

```text
c_alpha+c_beta=s-h_0,       c_alpha,c_beta>0,
a=d(b_1,g),                 0<=a<=14.                    (FW312.1)
```

Choose

```text
c=min(c_alpha,c_beta),       t=a+c.                       (FW312.2)
```

Then

```text
c<=floor((s-h_0)/2).                                      (FW312.3)
```

There are `n-1` distinct positive edge weights, all at most the globally
heaviest edge `s`. Hence `n-1<=s`. If `n>=36`, then `s>=35`; using
`h_0>=2` and `a<=14` gives

```text
s+h_0>=37>=2a+9,
t+4=a+c+4<=s-1.                                          (FW312.4)
```

Thus `t,t+4` lie in the low interval below `s`. Both are owned by unique
actual pairs except that the punctured value four has no required owner. The
only singleton rows are

```text
t=4:       (g=z,c=3) or (g=b_2,c=1).                      (FW312.5)
```

All orders `18<=n<=35` remain a separate bounded obligation.

The no-outlier cap also localizes the four FW311 holes. If `rho=max R`, then
the carrier cap gives `a+w+rho<=W-4`; since each rooted-arm difference is at
most `rho`, all four forbidden depths are at most `W-w-h_0`. This confines
the reception problem to the actual capped rooted window, but does not choose
their owners.

## 2. Nine owner colors

Cut the fixed-core side `L` from the remote carrier side `J`. Each unique
owner of `t` and `t+4` is exactly one of

```text
L-internal,       J-internal,       cross.                (FW312.6)
```

The ordered pair of colors therefore has nine possibilities. FW311.8 says
that neither receiving depth occurs in the rooted factor `B`; it does not
exclude an internal pair elsewhere in `L`, an internal pair in `J`, or a
cross pair. The LCA and endpoint identities must be retained in the next
step; the distance values alone lose the needed rooted information.

## 3. Exact cross--cross rectangle

Suppose both owners cross the carrier cut. Write their decompositions as

```text
w+r+b=t,
w+r'+b'=t+4,                                             (FW312.7)
```

where `w` is the carrier boundary weight and `r,r'` and `b,b'` are the rooted
depths on the `J` and `L` sides. Put

```text
x=r'-r,       y=b'-b.                                    (FW312.8)
```

Then

```text
x+y=4.                                                    (FW312.9)
```

Rooted support uniqueness gives the complete classification:

1. `x=0`: the two owners share their `J` endpoint and the `L` rooted depth
   changes by four.
2. In the monotone range `0<x<4`, the fixed-core rooted-difference table
   contains one and two at every gate and contains three except at gates
   `d_6,a`. Hence only the `d_6/a` row `(x,y)=(3,1)` survives.
3. Otherwise `x<0` or `x>4`: one rooted factor rises while the other falls,
   a genuine switch rectangle.

The alternative `y=0` would give `x=4`, contradicting the inherited
`D intersect (D+4)=empty` condition. In a switch rectangle the other two
cross distances are

```text
t+4-x,       t+x.                                        (FW312.10)
```

These two values, together with their actual owners and LCAs, are the next
available constraints from complete low coverage and the global cap.

## 4. Three exact pressure controls

The verifier extends the deterministic FW311 bouquet to order 123 in three
ways. In every control the receiving distances are the same `t,t+4`, both
are absent from `B`, all 7503 pair distances are distinct, the exact-return
type is `(3,3,0)`, `D intersect (D+4)` is empty, and the full-window sink is
the canonical path `b_1--z--a--y`.

The added owners realize:

```text
control             owner of t       owner of t+4
J_internal_pair     J-internal        J-internal
L_internal_pair     L-internal        L-internal
cross_switch_pair   cross             cross switch.       (FW312.11)
```

For the switch control,

```text
x=28512239,       y=-28512235,       x+y=4.               (FW312.12)
```

The other two corners have distances `219518123662` and `219575148136`.
These controls first miss five and violate their own global caps. They do not
refute the full Leech hypotheses; they show that distance injectivity, exact
return, the shift-four exclusion, the canonical sink, and the four root holes
do not individually exclude the three displayed owner states.

## 5. Successor obligation

The remote branch is now reduced to:

> **Paired Reception Exclusion.** Under the full `R2,t=4` punctured-tiling
> hypotheses, exclude the internal-owner rows and the three cross rectangles
> for the unique owners of `t,t+4`; separately discharge `18<=n<=35`.

The promising inputs are the other two cross distances in (FW312.10), actual
LCA projections on both rooted sides, complete low coverage, and the
no-outlier cap. A value-only argument is insufficient.

## 6. Trust boundary

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_paired_reception.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_paired_reception_certificate.json
```

**Proved analytically:** the all-order receiving window for `n>=36`, the two
singleton `t=4` rows, the nine owner colors, and the cross--cross rectangle
classification.

**Exact finite audit:** the window arithmetic, six fixed-core rooted
difference sets, and three deterministic pressure controls.

**Not proved:** paired-reception exclusion, the bounded orders `18<=n<=35`,
remote packet exclusion, the ten-fixed-LCA clause, `R2,t=4`, the two-point
cap, `g=7`, ERTC, NSSC, or global nonexistence.

**Verdict: PAIRED RECEPTION COLORS FINITE; EXCLUSION OPEN.**

