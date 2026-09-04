# Terminal four-cone reduction and left-cone exclusion (FW287)

FW286 proves that every path drop has a terminal adjacent owner switch

```text
AB at eta-1  ->  BC at eta.
```

FW287 writes the two crossed swaps in connector coordinates.  Distance
injectivity first confines every disjoint-endpoint state to four integer
cones.  The FW283 endpoint-edge bound then excludes one cone completely.
Three realized escape modes remain.

This is an **OBSERVED all-order exact reduction**.  The left-cone exclusion
inside it is a proved lemma; the remaining modes and NSSC are unverified.

## 1. Terminal coordinates and crossed swaps

Keep the FW286 decomposition

```text
A -- q -- B -- r -- C
```

and write `p=w_q`, `g=w_r`.  Let the terminal owners be

```text
X=d(a,b)=p+eta-1,       (a,b) in A x B,
Y=d(b',c)=p+eta,        (b',c) in B x C.
```

For `z in B`, let `t_z` be the coordinate of its projection on the connector
from the `q`-side root to the `r`-side root, and let `h_z` be its height off
that connector.  Thus

```text
lambda_z=t_z+h_z,             rho_z=ell-t_z+h_z.
```

Put

```text
x=t_(b')-t_b,                 y=h_(b')-h_b.
```

The two crossed pairs have exact distances

```text
X'=d(a,b')=X+x+y,                                      (FW287.1)
Y'=d(b,c) =Y+x-y,                                      (FW287.2)
X'+Y'=X+Y+2x.                                          (FW287.3)
```

These are actual pairs, not formal polynomial terms.

## 2. Injectivity and the four cones

If `b=b'`, then `x=y=0`; the terminal owners share their `B` endpoint and no
transport problem remains at this path drop.  Assume `b!=b'`.  The swapped
pairs are then distinct from both named terminal pairs.  Distance
injectivity gives

```text
x+y not in {0,1},              x-y not in {-1,0}.       (FW287.4)
```

Since all data are integral, exactly one of the following holds.

```text
L: x+y<=-1, x-y<=-2,          hence x<=-2;
R: x+y>= 2, x-y>= 1,          hence x>= 2;
D: x+y<=-1, x-y>= 1,          hence y<=-|x|-1;
U: x+y>= 2, x-y<=-2,          hence y>= |x|+2.          (FW287.5)
```

The letters mean left projection, both swaps rise, height drop and height
rise.  This classification uses injectivity only; it is not yet a Leech
coverage argument.

## 3. Exact four-point identity

If `x!=0`, the projections of `b,b'` are different and

```text
d(b,b')=h_b+h_(b')+|x|.
```

The tree four-point identity becomes

```text
d(a,c)+d(b,b')=max(X+Y,X'+Y').                         (FW287.6)
```

If `x=0`, let `s` be the length of the common off-connector stem of the paths
from `b,b'` to their common projection.  Then

```text
d(b,b')=h_b+h_(b')-2s,
d(a,c)+d(b,b')=X+Y-2s<=X+Y.                            (FW287.7)
```

Equal pair sums in (FW287.6)--(FW287.7) are not distance collisions.  A proof
cannot silently replace distance injectivity by a Sidon condition on sums.

## 4. Cone-L exclusion lemma

The terminal `AB` equation gives

```text
alpha_a+lambda_b=eta-1,        hence lambda_b<=eta-1.   (FW287.8)
```

Assume cone `L`.  Then `t_(b')<t_b` and

```text
lambda_(b')<=lambda_b-1<=eta-2.                         (FW287.9)
```

Let `e'` be the first edge of the distinguished path `P_q` from `b'` toward
`c`.  FW283 gives

```text
w_(e')>=eta+1.                                          (FW287.10)
```

There are two exhaustive cases.

1. If `b'` is off the connector, `e'` lies on its branch toward the
   connector.  Therefore `lambda_(b')>=w_(e')>=eta+1`, contradicting
   (FW287.9).
2. If `b'` lies on the connector, the path to `c in C` follows the connector
   toward `r`, in increasing `t`.  Since `t_(b')<t_b`, the path from the
   `q`-root to the projection of `b` contains `e'`.  Hence
   `lambda_b>=w_(e')>=eta+1`, contradicting (FW287.8).

Thus

```text
cone L is impossible.                                   (FW287.11)
```

There is no connector-root exception.  At the `q`-root the second case still
applies; at the `r`-root `t_(b')<t_b` is impossible; and if `ell=0`, every
projection has coordinate zero, so cone `L` cannot even satisfy `x<0`.

## 5. The three surviving modes

Every disjoint terminal state is therefore in `R`, `D` or `U`.  The endpoint
bound sharpens the mixed modes.

1. In `D`, `b'` must lie on the connector.  Otherwise its first endpoint
   edge would give `h_(b')>=eta+1`, while
   `h_b<=lambda_b<=eta-1`, contradicting the height drop.  Moreover
   `x>=0` and `h_b>=x+1`.
2. In `U`, `b'` must be off the connector and
   `h_(b')>=eta+1`; its height increase satisfies `y>=|x|+2`.
3. In `R`, both crossed swaps rise and `x>=2`.

All three modes occur in actual distance-injective trees with nontrivial
full-window sink cores.  The controls are not Leech, so this realizes the
local states without refuting a future complete-spectrum exclusion.

The path-drop successor is now the explicit obligation:

> **UNVERIFIED RDU transport/exclusion.**  Use complete Leech coverage to
> eliminate `R,D,U`, or assign each a named endpoint/projection transport that
> composes monotonically through the next FW284 arc.

Cap lifts still require their independent cap-to-boundary transport theorem.
Even local `RDU` and cap transports would still need cycle-composition
compatibility before NSSC follows.

## 6. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_terminal_four_cone_reduction.py
theory-lab/topwindow/results/terminal_four_cone_reduction_certificate.json
```

It reconstructs terminal states in five actual distance-injective trees and
checks (FW287.1)--(FW287.7), the injectivity exclusions, connector projections,
the critical endpoint edge and the `D/U` refinements.  The controls include a
shared endpoint, the known `L6` height-rise state, and nontrivial-sink
realizations of each surviving mode `R,D,U`.

**Proved:** the swap identities, four-cone partition, four-point identity,
the complete cone-`L` exclusion, and the stated `D/U` geometric refinements.

**Not proved:** elimination or composable transport of `R,D,U`, cap-to-boundary
transport, cycle compatibility, NSSC, nontrivial-sink exclusion, G18, any new
order exclusion, or global Leech-tree nonexistence.

**Verdict: EXACT REDUCTION.**

## 7. FW288 local transport completion

FW288 interprets every surviving mode as a retained local record.  Mode `D`
has the canonical earlier `AB` owner `(a,b')` at an offset
`0<=j<=eta-2`; mode `U` has the canonical `BC` bridge `(b,c)` of distance
below `p`; mode `R` has an actual oriented marked connector interval of
length at least two.  Together with the direct shared-endpoint state, these
four records complete the single-path-drop local TABC theorem.

Compatibility with the next FW284 arc is a separate unverified theorem, as
is cap-to-boundary transport.  See `docs/terminal-local-transport.md`.

FW289 now reduces the separate cap-lift layer to direct shallow-endpoint
transport or a remote--remote rectangle state, and strictly stops the target
first-prefix mechanism on the latter.  See `docs/cap-endpoint-depth-stop.md`.
