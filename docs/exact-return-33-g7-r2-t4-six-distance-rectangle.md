# FW316: exact six-distance monotone rectangle

FW315 forces actual owners for the reflected low values but does not give
their rooted provenance.  The sharper FW312 monotone cross--cross row has
four named endpoints, so all six distances among them can instead be kept
exactly.  This removes several affine parameter lines and proves an anchored
reflected-X lemma, but it still does not exclude a complete branch.

## 1. Four rooted endpoints

Root the fixed side at `g` and the carrier side at `u`, with `d(g,u)=w`.
Let the two L endpoints have depths `b,b+1`.  Let the two J endpoints have
strict `u`-LCA depth `m` and outgoing arms `ell,ell+3`.  Put

```text
A = w+b+m,
q = A+ell,
D = A-ell,
S = w+m+kappa,
```

where `kappa` is the `g`-LCA depth of the L endpoints.  The four cross
distances are

```text
q, q+1, q+3, q+4.
```

The two internal distances are

```text
J = 2ell+3 = q+3-D,
L = 2(b-kappa)+1 = q+D+1-2S.
```

These are actual endpoint-pair identities.  No rooted-depth reception or
path-drop statement is used.

## 2. Exact collision classification

Distance injectivity first requires the J pair to avoid the four cross
pairs.  This excludes

```text
D in {3,2,0,-1}
```

and leaves exactly

```text
lower:   D>=4,
middle:  D=1,
upper:   D<=-2.
```

The L pair collides with a cross pair exactly on

```text
D in {2S-1,2S,2S+2,2S+3},
```

and collides with the J pair exactly when `D=S+1`.

Therefore the surviving parameter regimes are:

```text
lower:   D>=4 and
         D not in {S+1,2S-1,2S,2S+2,2S+3};

middle:  D=1 and S>=2;

upper:   D<=-2.
```

No one of the three regimes is empty.

The value `q+2` has two distinguished internal receptions:

- in the middle regime, the J pair owns `q+2`;
- in the lower regime, the L pair owns `q+2` exactly on `D=2S+1`.

In the upper regime the six distances have the rigid order

```text
L <= q-3 < q < q+1 < q+3 < q+4 < J.
```

Thus, when `q+2` belongs to the complete low window, its owner is external to
these four endpoints.  This does not give that external pair any prescribed
rooted depth or carrier incidence.

## 3. Anchored reflected-X lemma

For the original cross owner `(P,Q)`, suppose the `q_B` cross owner shares
`P` and the `q_R` cross owner shares `Q`.  Their other endpoints `Q'` and
`P'` then satisfy

```text
d(u,Q') = delta-w = d(g,P').
```

If `delta<w`, these depths are negative.  If `delta>w`, the two distinct
named root pairs `(u,Q')` and `(g,P')` repeat the same positive distance.
Global distance injectivity excludes both cases.  Hence `delta=w`; then
`Q'=u` and `P'=g`, so the reflected owners collapse to the boundary pairs
`(P,u)` and `(g,Q)`.

This excludes one simultaneous secondary-X incidence pattern, not an entire
X-containing signature.

## 4. Cap localization and stop

The only available cap inequalities from these endpoints are

```text
d(P1,Q1)=q+4 <= N,
d(Q0,Q1)=J <= N,
d(P0,P1)=L <= N.
```

In the upper regime the named J pair has exact excess

```text
J-(q+4) = ell-A-1 >= 1.
```

The next single obligation is therefore the **Upper-Rectangle Cap-Slack
Exclusion**:

```text
prove N-(q+4) < ell-A-1
```

from the frozen `g in {a,d_6}` data and the global no-outlier cap, or construct
an actual pressure control showing that this inequality need not follow.

Without that comparison, no lower, middle, or upper branch is excluded.

## 5. Replay and trust boundary

Run

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_six_distance_rectangle.py
```

The replay exhausts a bounded box of the actual integer parameters and checks
every displayed identity, collision line, surviving regime, and anchored
sign case.  It constructs no weighted tree and is not a finite proof of the
analytic statement.

**VERIFIED exact parameter refinement; no owner mode or global conjecture is
excluded.**
