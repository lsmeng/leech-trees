# Cap endpoint-depth reduction and remote-pair stop (FW289)

FW288 completes the local transport record for every path drop.  A cap lift
has different geometry: the incoming owner lies wholly inside the target
strict cap and below its boundary weight.  FW289 proves the exact endpoint
depth dichotomy, adds a full-spectrum rectangle bound, and records a strict
stop for deriving cap transport from the target first prefix alone.

This is an **OBSERVED all-order exact reduction plus a STRICT STOP for the
bounded-prefix mechanism**.  Full cap-to-boundary transport remains open.

## 1. Cap-lift coordinates

Let `q -> f` be a cap lift.  Write

```text
p=w_q,             g=w_f=p+eta+sigma,      sigma>=1.
```

Let `C` be the strict first-level cap outside `f`, with cap root `o` and
inward boundary root `z`.  The incoming owner is

```text
P_q=(c,d) in C x C,
d(c,d)=p+eta=g-sigma<g.                              (FW289.1)
```

Let `theta=eta_f` be the first compensated offset at the target boundary.
Because `diam(C)<g`, the target same-side owner

```text
P_f=(a,b),             d(a,b)=g+theta                 (FW289.2)
```

lies wholly on the inward side.  For `v in C`, put

```text
gamma_v=d(o,v).
```

## 2. Endpoint-depth dichotomy

The pair `(z,v)` crosses `f` and has distance

```text
d(z,v)=g+gamma_v.                                     (FW289.3)
```

There are exactly three possibilities.

1. If `0<=gamma_v<theta`, then `(z,v)` is the unique target-prefix cross
   owner at offset `gamma_v`.  It shares the incoming endpoint `v` with
   `P_q`, giving canonical direct endpoint transport.
2. If `gamma_v=theta`, then `(z,v)` is a cross owner of `g+theta`, while
   (FW289.2) is the distinct same-side owner of the same distance.  This is
   impossible by distance injectivity.
3. If no incoming endpoint gives direct transport, integrality forces

```text
gamma_c,gamma_d>=theta+1.                              (FW289.4)
```

The last state is the **remote--remote residue**.

## 3. Rooted stem identity

Let `s_C` be the depth from `o` to the LCA of `c,d` in the rooted cap.  Then

```text
gamma_c+gamma_d-2s_C=p+eta=g-sigma,                    (FW289.5)
2s_C=gamma_c+gamma_d-g+sigma.                          (FW289.6)
```

Similarly let `beta_a=d(z,a)`, `beta_b=d(z,b)` and let `s_B` be the inward
rooted LCA depth of `a,b`.  Equation (FW289.2) gives

```text
beta_a+beta_b-2s_B=g+theta.                            (FW289.7)
```

These identities retain the two actual common stems; independent rooted
depth multisets would lose them.

## 4. Four-cross-pair rectangle and Leech bound

All four pairs

```text
(a,c), (a,d), (b,c), (b,d)
```

cross `f`.  Their two opposite pairings satisfy the exact rectangle identity

```text
d(a,c)+d(b,d)
 =d(a,d)+d(b,c)
 =3g+p+eta+theta+2(s_C+s_B).                           (FW289.8)
```

In a Leech tree every pair distance is at most `N=n(n-1)/2`.  Therefore every
cap lift must obey

```text
3g+p+eta+theta+2(s_C+s_B)<=2N.                         (FW289.9)
```

In particular `3g+p+eta+theta<=2N`.  This is a genuine complete-spectrum
constraint, but it does not by itself exclude every cap lift.

Equal sums in (FW289.8) are not repeated distances.  The interval spectrum
is not a Sidon set, so the rectangle cannot be declared contradictory without
an additional owner or range argument.

## 5. Why the first-prefix mechanism stops

The earlier order-eight cap-lift control has

```text
p=2, g=26, eta=1, theta=1,
gamma endpoints 4 and 7.
```

It realizes remote--remote, but its four rectangle cross distances exceed
the pair cap `N=28`; thus it could not distinguish a true coverage mechanism
from a simple outlier failure.

FW289 adds an order-nine control with

```text
p=1, g=11, eta=1, theta=2,
gamma endpoints 4 and 6,
four cross distances 15,17,28,30 <= N=36,
rectangle sum 45 <= 2N=72.
```

This tree is globally distance-injective, has a nontrivial full-window sink,
a total target first-prefix record, a strict cap and an actual cap lift.  It
is not Leech: its spectrum is not `[1,36]`.  It proves the narrower fact that
strict thinness, the endpoint-depth dichotomy, pair-cap containment and the
rectangle bound do not eliminate remote--remote.

Therefore the following continuation is frozen:

> **STRICT STOP (FW289).**  Do not infer full cap-to-boundary transport from
> the target first compensated prefix and endpoint depths alone.

The smallest live successor is:

> **UNVERIFIED Remote Cap Rectangle Transport (RCRT).**  In the remote--remote
> state, use complete coefficients beyond `theta` to connect the incoming cap
> pair `(c,d)`, the target inward owner `(a,b)`, and at least one of the four
> named cross owners in (FW289.8), retaining a shared endpoint or an oriented
> common-stem/connector datum consumable by the next FW284 arc.

PRCC for the already proved path-drop records remains a separate obligation.

## 6. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_cap_endpoint_depth_stop.py
theory-lab/topwindow/results/cap_endpoint_depth_stop_certificate.json
```

It checks direct endpoint transport at offsets zero and two, remote states at
`theta=1,2`, the forbidden equality, both rooted stem identities, all four
cross owners, (FW289.8), and the pair-cap status of every control.

**Proved:** the endpoint-depth dichotomy, remote lower bound, rooted-stem and
rectangle identities, and the conditional Leech bound (FW289.9).

**Not proved:** RCRT, full cap-to-boundary transport, PRCC, cycle compatibility,
NSSC, nontrivial-sink exclusion, G18, any new order exclusion, or global
Leech-tree nonexistence.

**Verdict: EXACT REDUCTION + STRICT MECHANISM STOP.**

## 7. FW290 interaction

FW290 proves that a strict path-drop target owner lies below the dropped
source weight, but an actual control then cap-lifts above that source.  Thus a
future strict-branch composition theorem must feed the retained FW288 owner
endpoints into the direct/remote cap record above; scalar weight descent is
insufficient.  See `docs/pathdrop-target-owner-fork.md`.
