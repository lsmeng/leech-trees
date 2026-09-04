# Canonical mismatch-gate transport: threshold and merge stop (FW281)

FW281 tests the only reopening left by FW280: whether canonical top ownership
and full low coverage force a common direction on the AC-2 mismatch gates.
The answer is a strict mechanism-specific **STOP**, not a counterexample to
rank anti-coalescence.

* **OBSERVED exact:** a collision has a complete threshold ledger, and the
  transformed Kruskal process obeys a rank covering inequality.
* **OBSERVED exact:** injectivity is equivalent to coefficientwise separation
  of rooted merge convolutions.  The scalar Kruskal schedule forgets exactly
  this information.
* **OBSERVED exact control:** canonical `L6` has full interval coverage and an
  injective transformed core, yet its local shadow/lift and AC-2 transports
  cycle, split gates and have both signs.
* **OBSERVED pressure:** a noncanonical full `L6` orientation defeats the
  scalar Kruskal criterion, and an infinite non-Leech family with an exact
  four-value top row collides while passing Taylor parity.
* **OBSERVED finite, external/non-replayed:** 232 order-six `I_4`-prefix
  models were `UNSAT`.  This is not proof input.

## 1. Canonical state and threshold collision ledger

Use the FW280 state

```text
a--1--b,                 x--e--r,                 U=T-{a,x},
D_0=N-Q,                 D=Spec(U),               H_0=H intersect [1,D_0],
H=(1+B) dot-union (e+R) dot-union {L},            phi(t)=t-|H intersect [1,t]|.
```

For a core edge `f` put `alpha_f=phi(w_f)`.  For an oriented or unoriented
core path `P`, define its threshold profile

```text
kappa_t(P)=#{f in P:w_f>=t}                       (1<=t<=D_0).
```

Layer-cake summation and `D dot-union H_0=I_(D_0)` give the exact identities

```text
d(P)=sum_(t=1 to D_0) kappa_t(P),
F(P)=sum_(d in D) kappa_d(P),
Omega(P):=d(P)-F(P)
        =sum_(h in H_0) kappa_h(P)
        =sum_(f in P) q(w_f),                     (FW281.1)
```

where `q(t)=|H intersect [1,t]|`.  The two-root owner partition further gives

```text
Omega(P)=sum_(u in U) kappa_(1+B_u)(P)
        +sum_(v in U) kappa_(e+R_v)(P)
        +kappa_L(P),                              (FW281.2)
```

with `B_u=d_U(b,u)`, `R_v=d_U(r,v)` and the convention `kappa_t=0` for
`t>D_0`.  Thus every threshold term still has its actual `a`-, `x`-, or
corner owner.

For paths with `d(P)<d(P')`, set

```text
delta_t=kappa_t(P')-kappa_t(P).
```

Then the transformed collision condition is exactly

```text
F(P)=F(P')
 iff sum_(d in D) delta_d=0,
and then
sum_(h in H_0) delta_h=d(P')-d(P)>0.              (FW281.3)
```

This is the threshold form of AC-1.  It locates all positive old-length drift
on external-owner thresholds, but supplies neither a sign for individual
`delta_h` nor a gate matching between them.

## 2. Rank-Kruskal covering and the exact missing invariant

Insert the core edges in increasing transformed weight `alpha`.  Let `G_j`
contain the edges with `alpha_f<=j`, and put

```text
K(j)=sum_(C component of G_j) binom(|C|,2)
    =sum_(alpha_f<=j) Delta_f,                     (FW281.4)
```

where `Delta_f=|A_f||B_f|` is the product of the two light components merged
when `f` is inserted.  The first `j` internal distance owners by rank have
paths entirely in `G_j`; consequently

```text
K(j)>=j.                                          (FW281.5)
```

The inequality is necessary but not sufficient.  Immediately before inserting
`f`, root its two components `A_f,B_f` at the endpoints of `f`, and let

```text
R_f^-(z)=sum_(u in A_f) z^(F(u,root_-)),
R_f^+(z)=sum_(v in B_f) z^(F(root_+,v)).
```

Distinct edge ranks give every core pair a unique last inserted edge.  Hence
the complete transformed pair multiset has the exact rooted merge convolution

```text
M_F(z)=sum_f z^(alpha_f) R_f^-(z)R_f^+(z).        (FW281.6)
```

Rank anti-coalescence is equivalent to every coefficient of `M_F` being at
most one.  The numbers `Delta_f=R_f^-(1)R_f^+(1)` and `K(j)` remember only
total merge mass, not its distribution among exponents.  Restoring all
coefficients, or equivalent owner/LCA data, has `Theta(m^2)` size in general.

## 3. Canonical full-interval `L6`: local transport cycles

Use the exact order-six Leech tree

```text
a--1--b--2--z,             b--5--r--4--y,          r--8--x.
```

Here `x` is the canonical diameter endpoint, `Q=4`, `D_0=11`, and deleting
`a,x` leaves the path `z--2--b--5--r--4--y`.  Its owner partition is

```text
D={2_bz,4_ry,5_br,7_zr,9_by,11_zy},
A={1_ab,3_az,6_ar,10_ay},
X={8_xr,12_xy,13_xb,15_xz},
C={14_ax},                  D dot-union A dot-union X dot-union C=I_15.
                                                        (FW281.7)
```

Already at the smallest shared shadow coordinate there is no unique gate:

```text
3_az --unit shadow--> 2_bz, marked at z,
13_xb --top reflection 15-13--> 2_bz, marked at b. (FW281.8)
```

The marks in (FW281.8) use a fixed owner-path convention.  For the `A` row,
delete the unit edge `ab` from `a-b-z` and retain the core endpoint `z`.  For
the `X` row, use the nested paths `x-b` inside `x-z`; their difference is
`b-z`, and retain the core endpoint `b` of the shorter owner `x-b`.

The inverse lifts return `2_bz` to the two external owners, producing two
local two-cycles.  Thus choosing the least shadow coordinate does not break
the tie, the two lifts need not have the same root, and lift iteration has no
strict local potential.

For completeness, the nonempty AC-2 steps and all reverse/continuation steps
are below.  In the four-endpoint cross-pair sum after swapping endpoints, a
geometric uncrossing correction is `+2c` for a separating connector of length
`c`, and `-2 lambda` for overlap of length `lambda`; these are not single-path
replay increments.
Every first-edge step has `s=0` and empty mismatch sets, so the displayed six
positive-prefix rows exhaust all orientations of all core paths.

| prefix `S`; `(s,w)` | `M^+` with correction | `M^-` with correction | `eta` |
|:---|:---|:---|---:|
| `z-b`; `(2,5)` | `4_ry -> 6_ar[A]`, connector `5`, `+10` | `3_az -> 5_br`, overlap `2`, `-4` | 0 |
| `r-b`; `(5,2)` | empty | empty | 0 |
| `b-r`; `(5,4)` | empty | empty | 0 |
| `y-r`; `(4,5)` | `2_bz -> 6_ar[A]`, connector `5`, `+10`; `4_ry -> 8_xr[X]`, overlap `4`, `-8` | `1_ab -> 5_br`, connector `5`, `+10`; `3_az -> 7_zr`, connector `5`, `+10` | 0 |
| continuation `(7,4)` | empty | empty | 0 |
| continuation `(9,2)` | empty | empty | 0 |

This table exactly rules out four proposed *local* proofs: least-`t`
selection, forced same-root pairing, a uniform correction sign, and strict
descent by repeated lift.  It does **not** refute a theorem using the global
geometry of a first collision.  Indeed the transformed edge weights are
`1,3,2`, and the six transformed path sums are `I_6`; canonical `L6` itself
has no collision.

## 4. Why scalar Kruskal data cannot repair the local failure

In the noncanonical full-spectrum `L6` orientation obtained by deleting the
unit leaf `a=1` and the leaf `x=2`, the core is a three-edge star with old
weights `4,5,8` and transformed weights

```text
1,2,3.
```

The weight-three edge collides with the path using weights one and two, while

```text
K(1)=1,                    K(2)=3,                 K(3)=6. (FW281.9)
```

Thus every inequality `K(j)>=j` holds, even with the complete merge schedule,
but a convolution coefficient repeats.  This is a scalar no-go only.  The
chosen `x` is not canonical, so it is not a counterexample to the target.

## 5. Exact-four-top pressure family

For every integer `k>=5`, take

```text
a--1--b--2--p--k--c--(k+1)--y,          c--(k+5)--x.
```

Its fifteen pair distances are

```text
1_ab,2_bp,3_ap,k_pc,(k+1)_cy,(k+2)_bc,(k+3)_ac,(k+5)_cx,
(2k+1)_py,(2k+3)_by,(2k+4)_ay,(2k+5)_px,(2k+6)_xy,
(2k+7)_bx,(2k+8)_ax.                            (FW281.10)
```

They are distinct.  Relative to the artificial cap `N_k=2k+8`, deleting `x`
leaves diameter `2k+4`, and `x` owns the exact top suffix
`[2k+5,2k+8]`; hence this is a `Q=4` top-row model, not a Leech tree.
In particular it has the exact `I_3` prefix, with

```text
Spec(W_k)={1,2,3} union [k,k+3] union {k+5}
          union {2k+1,2k+3,2k+4} union [2k+5,2k+8].
```

After deleting `a,x`,

```text
D_U={2,k,k+1,k+2,2k+1,2k+3},
A={1,3,k+3,2k+4},
X={k+5,2k+5,2k+6,2k+7},             C={2k+8},
phi(2)=1,              phi(k)=k-2,   phi(k+1)=k-1. (FW281.11)
```

Therefore

```text
F(bp)+F(pc)=1+(k-2)=k-1=F(cy),
M_F={1,k-2,k-1,k-1,2k-3,2k-2}.                  (FW281.12)
```

For odd `k`, weighted parity has classes `4|2`, hence eight odd and seven even
distances, exactly the Taylor split.  At the first parameter `k=5`,

```text
Spec=I_18-{4,9,12},
H={1,3,8,10,14,15,16,17,18},
M_F={1,3,4,4,7,8}.                               (FW281.13)
```

The first missing coefficient is `4`, already in the first translation window
`(s,w)=(2,5)`.  The family shows precisely why the complete low interval is
load-bearing; it is not a canonical full-state counterexample.

## 6. `I_4` finite diagnostic and strict STOP

A temporary external Presburger/SMT audit tested

```text
6 unlabelled order-six topologies,
58 ordered leaf-pair orientations (a,x) in total,
Q in {2,3,4,5}:                       58*4=232 models.
```

Each model imposed positive unbounded integer edge weights, the unit `a` edge,
15 distinct distances, an exact `I_4` prefix, canonical top ownership/deletion
diameter, the actual owner set `H`, and a transformed core collision.  All 232
returned `UNSAT`, with zero `UNKNOWN`, in about 3.54 seconds.

This is only **OBSERVED finite, external/non-replayed**: no script, stdout,
solver hash, proof log, certificate or independent replay was retained.  It
cannot support a lemma.

The 60k checkpoint therefore triggers **STOP**.  Thresholds prove (FW281.3),
scalar Kruskal proves only (FW281.5), and canonical `L6` invalidates all tested
local gate orientations without invalidating the global first-collision
statement.  FW281 proves no anti-coalescence theorem, excludes no order and
does not prove G18.

The route may be reopened only with a genuinely global theorem combining the
rooted merge convolution (FW281.6) with AC-1 (FW280.12) to separate every
coefficient.  A proposal that merely stores all convolution coefficients or
owner/LCA incidences is the known `Theta(m^2)` fallback, not a descent.

Antecedent: `docs/pendant-rank-anti-coalescence-stop.md`.
