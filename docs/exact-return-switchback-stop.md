# Exact-return two-root switchback reduction and stop (FW291)

FW290 reduces every path drop to a strict target-owner branch or an exact
path-drop/edge-lift return.  FW291 writes the exact-return branch as a complete
two-root owner strip.  The strip is stronger than the scalar two-cycle
balance, but actual controls show that it is not by itself ERTC.

This is an **OBSERVED all-order exact reduction plus a STRICT STOP for the
local switchback mechanism**.  Exact-return two-cycle exclusion remains open.

## 1. Exact-return setup

Assume

```text
q --path drop--> r --edge lift--> q,
p=w_q>g=w_r,
delta=p-g=eta_r,             eta=eta_q.
```

Removing the two edges gives

```text
A -- q -- B -- r -- C.
```

Use rooted depths

```text
U      on A from the q-outer root,
Lambda on B from the q-inner root,
Rho    on B from the r-inner root,
W      on C from the r-outer root.
```

For each `v in B`, the `Lambda` and `Rho` entries are matched by the actual
connector projection:

```text
lambda_v=t_v+h_v,
rho_v=ell-t_v+h_v,
lambda_v+rho_v=ell+2h_v.                              (FW291.1)
```

## 2. Forced owner strip

At the `r` cut, offsets `0,...,delta-1` precede the first same-side owner and
are cross.  Their class is `BC`: an `AC` pair would already cross `q` and has
`r`-offset at least `p+ell>delta`.

At offset `delta`, the owner is the old edge `q`, of class `AB`.  FW286 says
that the next `eta-1` global values are also `AB`, and that the distinguished
owner `P_q` at the following value is `BC`.  Thus the complete strip is

```text
r-offsets 0,...,delta-1             BC,
r-offsets delta,...,delta+eta-1     AB,
r-offset  delta+eta                 BC.               (FW291.2)
```

Equivalently, in absolute distances,

```text
g,...,p-1            BC,
p,...,p+eta-1        AB,
p+eta                BC.                              (FW291.3)
```

Every entry has its unique actual unordered-pair owner.

## 3. Complementary rooted convolutions

The `AB` and `BC` cross polynomials are

```text
U*Lambda,             Rho*W.
```

Equation (FW291.2) is exactly the coefficient pattern

```text
[X^j](U*Lambda)=1,    0<=j<eta,
[X^eta](U*Lambda)=0,                                  (FW291.4)

[X^j](Rho*W)=1,       0<=j<delta,
[X^j](Rho*W)=0,       delta<=j<delta+eta,
[X^(delta+eta)](Rho*W)=1.                              (FW291.5)
```

The second factor therefore has its first cross hole at `delta`, an entire
gap of length `eta`, and an exact cross return at `delta+eta`.  The missing
block is supplied by the shifted `AB` factor:

```text
X^delta(U*Lambda).
```

This is the two-root switchback state.  `Lambda` and `Rho` may not be
permuted independently because of (FW291.1).

## 4. Pressure controls and strict stop

Known `L6` is globally Leech and realizes

```text
delta=3, eta=1, ell=0,
BC,BC,BC,AB,BC.
```

Its full-window sink is a singleton, so it does not test the nontrivial-core
hypothesis required by ERTC.

Three actual distance-injective non-Leech trees with nontrivial sinks realize
the same switchback geometry:

```text
delta=1, eta=1, ell=7,
delta=1, eta=2, ell=3,
delta=1, eta=1, ell=2.
```

In each case the entire strip lies inside the pair cap and has exactly the
stated owners.  These trees do not have spectrum `[1,N]`.

The controls separate the load-bearing conjunction:

```text
complete global coverage + nontrivial connector.
```

The first condition alone permits `L6`; the second together with the complete
local strip permits the non-Leech controls.  Hence:

> **STRICT STOP (FW291).**  Do not claim ERTC from the switchback strip,
> matched connector profiles, local pair-cap containment, or scalar cycle
> balance alone.

The smallest live theorem is still ERTC, now in its exact form:

> **UNVERIFIED ERTC.**  Prove that the correlated rooted state
> (FW291.1), (FW291.4), (FW291.5) cannot extend to complete `[1,N]` coverage
> when the full-window sink connector is nontrivial.

Any successor must use coefficients outside the bounded switchback strip and
the nontrivial connector simultaneously.  Extending only one rooted prefix
reopens the FW283 remote-gate failure.

## 5. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_exact_return_switchback_stop.py
theory-lab/topwindow/results/exact_return_switchback_stop_certificate.json
```

It reconstructs the two cuts, every strip owner, both rooted convolution
coefficient arrays and every matched `B` projection on the four controls.

**Proved:** the all-order owner strip (FW291.2)--(FW291.3), rooted convolution
patterns (FW291.4)--(FW291.5), and their actual connector matching.

**Not proved:** ERTC, extension impossibility, PRCC, RCRT, cap-to-boundary
transport, NSSC, nontrivial-sink exclusion, G18, any order exclusion, or
global Leech-tree nonexistence.

**Verdict: EXACT REDUCTION + STRICT LOCAL STOP.**
