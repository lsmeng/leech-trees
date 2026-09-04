# FW314: exhaustive complementary-owner mode audit

## 1. Result

The two FW311 complementary low values have an exact finite owner-class
decomposition at the least remote carrier cut.  Every non-cap owner is
L-internal, J-internal, or cross (`X`).  Up to interchanging the complementary
values, the ordinary signatures are

```text
LL, LJ, LX, JJ, JX, XX,
```

and if one complementary value is the cap-owned distance four, the remaining
signatures are

```text
4L, 4J, 4X.
```

This is a classification, not an exclusion.  Exact controls realize all nine
ordered ordinary class pairs and all three exceptional modes.  Therefore no
proof based only on owner colours or abstract LCA geometry can close the
Remote Complementary-Root Reception Lemma.  The complete punctured low
spectrum and the global no-outlier cap remain load-bearing.

## 2. Certified input

Let the least remote owner have rooted arms

```text
alpha + beta = s + h_0,
c_alpha = alpha - h_0,
c_beta  = beta  - h_0.
```

FW311 gives

```text
c_alpha + c_beta = s - h_0,
c_alpha != c_beta,
B omits a+c_alpha, a+c_alpha+4, a+c_beta, a+c_beta+4.
```

The carrier cut has exact rooted factors `B` on the L side and `R` on the J
side, with

```text
(R-R)_+ intersect (Q-Q)_+ = empty,
Q = B union {a+s,a+s+4}.
```

## 3. Exact owner/LCA consequences

For a nonexceptional complementary value `c`, its unique low-spectrum owner
falls in exactly one of the following classes.

### L-internal

Root the L side at the gate `g`.  If the owner LCA has depth `ell` and its two
outgoing arm lengths are `x,y`, then

```text
x+y=c,
{x,y}_positive is a subset of (B-B)_+,
{x,y}_positive is disjoint from {alpha,beta},
ell-a is not in {x,y,x+4,y+4}.
```

The final condition is exactly the FW311 four-hole condition applied to the
two owner endpoints.  It does not force an endpoint to be rooted at `g`.

### J-internal

Root the carrier at `u`.  If the two outgoing LCA arms are `x,y`, then
`x+y=c` and every positive arm is in `(R-R)_+`.  For each such arm `rho`,
directness forces the additional opposite-root holes

```text
B omits a+s-rho, a+s+4-rho, a+s+rho, a+s+4+rho
```

whenever the displayed depth is nonnegative.  If an arm equals `alpha` or
`beta`, distance injectivity forces literal reuse of the marked arm pair;
otherwise it is a new carrier difference.  Neither alternative is presently
contradictory.

### Cross

If the owner endpoints have rooted depths `b in B` and `r in R`, then

```text
c = w+b+r.
```

With the companion arm `delta=s-c` and `eta=s-w`, this becomes

```text
b+r=eta-delta,
delta<=eta.
```

Directness and uniqueness of the final distances `s,s+4` force

```text
B omits b-delta, b+delta, b+delta+4 (where nonnegative),
R omits r+delta, r+delta+4.
```

These are genuine endpoint-relative holes, but `eta` is not known to be a
first path-drop offset.  FW286--FW288 therefore cannot be imported.

### Exceptional value four

If one complementary value is four, the final cap owns it and the companion
remote arm is `s-4`.  The four rooted holes include `a+4,a+8`.  The marked
arm of length `h_0+4` cannot repeat any fixed-core distance, and the cap gives
the additional necessary inequality

```text
2s+a+w <= N.
```

This branch is constrained but not excluded.

## 4. Independently replayed pressure controls

For the nine ordered ordinary modes use

```text
s=100000, h_0=2, alpha=45000, beta=55002,
c_alpha=44998, c_beta=55000, w=5000, d(b_1,u)=5011.
```

`L(x,y)` denotes two leaves of weights `x,y` at `b_1`; `J(x,y)` denotes two
at `u`; `X(x,y)` denotes one `b_1` leaf of weight `x` and one `u` leaf of
weight `y`.

| mode | owner of 44998 | owner of 55000 |
|---|---|---|
| LL | L(18879,26119) | L(30581,24419) |
| LJ | L(16972,28026) | J(37701,17299) |
| LX | L(31254,13744) | X(32382,17607) |
| JL | J(28743,16255) | L(24086,30914) |
| JJ | J(9603,35395) | J(33843,21157) |
| JX | J(28311,16687) | X(38444,11545) |
| XL | X(18170,21817) | L(18813,36187) |
| XJ | X(17508,22479) | J(15741,39259) |
| XX | X(22030,17957) | X(31903,18086) |

Every control is an order-15 actual weighted tree with 105 distinct pair
distances, exact return `(3,3,0)`, least remote offset two, no root-depth
difference four, and sink vertices `{z,b_1,a,u}`.  Every one first misses
distance five and has maximum distance 160017, far beyond its own cap 105.

For the exceptional modes use

```text
h_0=20, alpha=24, beta=99996,
c_alpha=4, c_beta=99976.
```

The remaining owner is respectively

```text
4L: L(44279,55697)
4J: J(76338,23638)
4X: X(45042,49923).
```

These order-13 controls have all 78 pair distances distinct, the same exact
return and sink, least remote offset 20, first missing distance five, and
maximum distance 205011.  Again they are pressure controls, not Leech trees.

## 5. Strict stop and successor

**Verdict: EXHAUSTIVE OWNER MODES CERTIFIED; NO MODE EXCLUDED.**

The smallest live all-order statement is now:

> **Evasive Complementary-Owner Exclusion.** Under the full punctured-low-
> spectrum and no-outlier hypotheses, exclude every L/J/X/4 signature using
> the class-specific LCA, rooted-hole, and cross-translation constraints.

The most structured first target is an X-containing mode, because it gives
forbidden depths in both rooted factors.  It is still not a path-drop state.

The bounded FW313 target remains separate: its 41 top-strip rows require the
actual named final-cap owner in addition to this carrier-cut classification.

## 6. Replay and trust boundary

Run

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_all_owner_modes.py
```

The replay checks every edge weight, all unordered pair distances, exact
target ownership and cut class, the least remote owner, all four `B` holes,
root-factor directness, `D intersect (D+4)=empty`, exact return, sink support,
first missing distance, and own-order cap failure.

It does **not** prove reception, exclude an owner mode under the full Leech
hypotheses, exclude any FW313 row, prove a descended exact-return state, or
prove global Leech-tree nonexistence.
