# Exact-return `(3,3)` `g=7` complementary root holes (FW311)

FW310 proves that every remote owner meets the unique full-window sink, but
does not exclude the resulting incidence packet.  FW311 uses the least remote
owner, its actual path, and the FW309 simultaneous carrier cut.  That one
critical path splits into two rooted differences and forces four explicit
holes in the opposite rooted factor.

The remaining obligation is now a four-depth root-reception lemma.  Complete
low-spectrum ownership by arbitrary pairs does not yet prove that reception.

## 1. The least remote owner is critical

Let

```text
P=P_(h_0) subset J,       d(P)=s+h_0                         (FW311.1)
```

have the least offset among the remote owners in the FW307 55-owner window.
Every proper subpath of `P` has length below `s`.

Indeed, a proper subpath of length `s` would repeat the final bridge.  A
proper subpath of length `s+j`, with `1<=j<h_0`, would itself be an internal
`K` owner.  Hence `j` would be an earlier final-cut hole and the subpath would
be an earlier remote owner, contrary to the choice of `h_0`.

Consequently both endpoint edges of `P` have weight greater than `h_0`.
Removing an endpoint edge of weight at most `h_0` would leave either distance
`s` or an earlier remote distance.  Since `s` is the globally heaviest edge,
`P` has at least two edges.

## 2. Actual rooted-arm split

Root `J` at the carrier endpoint `u` of `f=gu`.  If the endpoints of `P` lie
in different rooted branches, split at their actual `u`-LCA.  If one is an
ancestor of the other, split at any interior vertex.  This gives two
nonempty ancestor--descendant subpaths of lengths `alpha,beta`, so

```text
alpha,beta in (R-R)_+,
h_0+1 <= alpha,beta <= s-1,
alpha+beta=s+h_0.                                         (FW311.2)
```

The two subpaths are different unordered pairs.  Global distance injectivity
therefore gives

```text
alpha != beta.                                            (FW311.3)
```

Define their complementary low lengths

```text
c_alpha=alpha-h_0=s-beta,
c_beta =beta-h_0 =s-alpha.                                (FW311.4)
```

Then

```text
c_alpha,c_beta>0,
c_alpha!=c_beta,
c_alpha+c_beta=s-h_0.                                     (FW311.5)
```

This reduction retains the actual owner path, split vertex and rooted
ancestor relations; it is not an abstract partition of `s+h_0`.

## 3. Four holes in the opposite rooted factor

Use the exact FW309 carrier notation

```text
a=d(b_1,g),       B=R_(L,g),       R=R_(J,u),
Q=B dotunion {a+s,a+s+4}.                                 (FW311.6)
```

The carrier product is direct, so

```text
(R-R)_+ intersect (Q-Q)_+ = empty.                        (FW311.7)
```

Since `alpha,beta` are positive `R` differences, (FW311.7) forces

```text
B intersect {
  a+c_alpha, a+c_alpha+4,
  a+c_beta,  a+c_beta+4
}=empty.                                                   (FW311.8)
```

For example, if `a+c_alpha` belonged to `B`, its difference from `a+s`
would be

```text
(a+s)-(a+c_alpha)=s-c_alpha=beta,
```

putting `beta` in both positive difference sets.  If `a+c_alpha+4` belonged
to `B`, use `a+s+4`; the two `c_beta` cases similarly produce `alpha`.

Thus one minimal remote path creates four named rooted holes on the fixed-core
side of its own carrier cut.

## 4. Exact six-gate restrictions

The six fixed-core vertices already belong to `L`, so their `g`-rooted depth
set is contained in `B`.  Substituting each possible gate and
`a=d(b_1,g)` into (FW311.8) gives the exact forbidden positive values for
each of `c_alpha,c_beta`:

```text
gate    forbidden values
z       1,2,5,6,8,9,12
b_1     1,3,4,7,8,10,11,14
b_2     2,5,6,8,9,12
c       1,5,9
d_6     1,5,9
a       1,2,6,8,12.                                      (FW311.9)
```

The verifier derives this table from the actual fixed-core distances rather
than hard-coding only the displayed result.

## 5. Exact inheritance failure

Unless `c_alpha=4`, the punctured low spectrum has a unique actual owner of
distance `c_alpha`; similarly for `c_beta`.  At most one complementary length
equals four by (FW311.5).

However, FW309.19 distributes a low owner among

```text
Spec(L),       Spec(J),       or       w+B+R.              (FW311.10)
```

An arbitrary pair of distance `c_alpha` is not necessarily a vertex at
`g`-rooted depth `a+c_alpha` or `a+c_alpha+4`.  Its LCA need not lie on the
`b_1`--`g` connector.  Therefore complete low ownership does not contradict
the rooted holes (FW311.8).

This identifies the remaining remote obligation precisely:

> **Remote Complementary-Root Reception Lemma.**  Under the full `R2,t=4`
> punctured-tiling hypotheses, the least remote critical path forces at least
> one of the four depths in (FW311.8) to occur in `B`.

Together with (FW311.8), that lemma would exclude every remote carrier.  It is
currently unproved.

## 6. Deterministic 55-owner pressure control

FW311 independently constructs an order-119 tree showing that even the whole
55-owner window can occupy one sink-leaf bouquet when the low interval and
global cap are removed.

Take

```text
s=10^12,       f=100012345,
H={2,6,9,10,13,16,17} union [19,66].                     (FW311.11)
```

Attach a center `y` to the fixed core vertex `a` by `f`.  For offsets `h` in
the displayed order, initialize Python's `random.Random(310)`, draw

```text
x_h = randrange(200000000000,400000000000),
y_h = s+h-x_h,                                           (FW311.12)
```

and attach two singleton leaves of weights `x_h,y_h` to `y`.  Finally attach
the weight-four two-vertex cap to `b_1` through the bridge `s`.

The ordered 110-weight list is serialized by

```text
json.dumps(weights,separators=(',',':')).encode()
```

and has SHA-256

```text
ac051b8736f86cd926a0974dbefab3a4aa79636d7cec820de8f892d994b31cfc.
```

The exact replay verifies:

```text
order                                      119
distinct pair distances                    7021
first global missing distance              5
maximum distance                           1799475417580
exact return                               (3,3,0)
D intersect (D+4)                          empty
first 55 final-cut holes                   H
owners of s+h                              the 55 prescribed leaf pairs
full-window sink                           b_1--z--a--y.
```

All 110 endpoint edges are heavier than their offsets.  The carrier boundary
`a--y` is the leaf edge of the sink core, so all 55 owners lie in one actual
leaf-bouquet packet where LPCT has its strongest direct applicability.

The control is not Leech: it first misses five and its maximum distance is far
above its own cap 7021.  It proves only that sink geometry, endpoint heaviness
and 55 owners do not force several carriers, a fixed-core intersection, or
bounded remote complexity.

## 7. Trust boundary

Replay:

```text
theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_complementary_root_holes.py
theory-lab/topwindow/results/exact_return_33_g7_r2_t4_complementary_root_holes_certificate.json
```

**Proved analytically:** criticality of the least remote owner, the actual
rooted-arm split, the four opposite-factor holes, and the six-gate table.

**Exact finite audit:** rooted-difference arithmetic and the fully
deterministic order-119 single-bouquet control.

**Not proved:** complementary-root reception, remote packet exclusion, the
ten-fixed-LCA clause, `R2,t=4`, the two-point cap, `g=7`, ERTC, NSSC, or
global nonexistence.

**Verdict: FOUR COMPLEMENTARY ROOT HOLES; RECEPTION OPEN.**
