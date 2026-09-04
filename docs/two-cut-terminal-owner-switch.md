# Two-cut terminal owner-switch reduction (FW286)

FW285 stopped endpoint composition from the compressed FW284 record and left
a full-spectrum connector-crossing owner-overlap obligation.  FW286 uses the
discarded coefficients in the shortest possible interval.  At every path drop
the whole translated band has a forced pair-class pattern: a block of `AB`
owners followed by one terminal `BC` owner.  The previously contemplated
`AB -> AC` first switch cannot occur.

This is an **OBSERVED all-order exact reduction**, not the missing connector
theorem and not NSSC.

## 1. Two-cut coordinates

Let `q -> r` be a path drop in the FW284 skeleton map.  Write the source and
target weights as `w_q` and `w_r`, and let `eta=eta_q`.  Removing `q` and `r`
gives the ordered decomposition

```text
A -- q -- B -- r -- C.
```

The notation names vertex sets; either displayed connector may have length
zero between its incident inner endpoints.  The six pair classes behave at
the two cuts as follows.

```text
pair class    q-cut    r-cut
AA            same     same
BB            same     same
CC            same     same
AB            cross    same
BC            same     cross
AC            cross    cross
```

The old edge `q` is an `AB` owner of distance `w_q`.  The distinguished
first same-side owner `P_q` has distance `w_q+eta`; because this is a path
drop to `r`, it is a `BC` pair.

## 2. Target-edge lower bound

FW283's critical-path lemma says that `P_q` has at least two edges, all of
them have weight below `w_q`, and each endpoint edge has weight at least

```text
eta+1.                                                   (FW286.1)
```

Every endpoint edge promotes to a skeleton edge of at least the same weight.
There are three apparent cases, but only two mechanisms.

1. If the endpoint edge is already a core edge or first-level boundary, it
   is a skeleton edge directly.  This includes an endpoint at a core vertex.
2. Otherwise it is internal to a unique first-level cap.  Since `P_q` is a
   path drop rather than a cap lift, its other endpoint is not in that cap.
   The path therefore exits across the cap boundary `f`.  Strict thinness
   gives

```text
w_f > w_(endpoint edge) >= eta+1.                         (FW286.2)
```

The target `r` is the unique maximum-weight skeleton edge crossed by `P_q`.
Edge weights are globally distinct, so the maximum is unique.  Either
endpoint promotion therefore proves

```text
w_r >= eta+1.                                            (FW286.3)
```

This proof is unchanged for a two-vertex core.  If the inner endpoints of
`q` and `r` coincide, the connector length below is simply zero.

## 3. Elimination of AC from the translated band

Let `ell` be the distance in `B` between the inner endpoints of `q` and `r`.
Every `AC` path crosses both edges, so its distance is at least

```text
w_q + ell + w_r.
```

Its offset in the `q` ledger is consequently at least

```text
ell+w_r >= eta+1.                                        (FW286.4)
```

Thus no coefficient at `q`-offset `j<=eta` can have an `AC` owner.

Complete Leech coverage and the definition of the first compensated hole say
that every coefficient with `0<=j<eta` is cross-owned at the `q` cut.  Its
class is therefore `AB` or `AC`; (FW286.4) removes the second option.  At
`j=eta`, the unique owner is the distinguished `BC` pair `P_q`.  Hence the
entire band is forced:

```text
j = 0,1,...,eta-1 : AB,
j = eta           : BC.                                 (FW286.5)
```

In particular there is no interior `AB -> AC` switch to analyse.  The exact
full-spectrum content of a path drop is one terminal adjacent switch

```text
AB at eta-1  ->  BC at eta.                              (FW286.6)
```

## 4. What remains

FW286 replaces the path-drop part of CCOO by the strictly smaller obligation:

> **UNVERIFIED Terminal AB-to-BC Connector (TABC).**  For the unique owners
> of `w_q+eta-1` and `w_q+eta` in (FW286.6), use their actual endpoints,
> their projections to the named `q--r` connector, the vertexwise identity
> `lambda_x+rho_x=ell+2h_x`, and unused global coverage to force an actual
> shared endpoint, a composable ordered overlap of projections, or a repeated
> distance.

The adjacent values alone do not imply that the two owner pairs share their
`B` endpoint.  The FW285 controls already warn that local owner records may
be vertex-disjoint.  TABC must use actual tree geometry and additional global
coefficients, not a formal factor swap.

Two independent layers also remain.

1. **UNVERIFIED Cap-to-Boundary Owner Transport:** a cap lift must transport
   an internal owner to usable data at the boundary.
2. **UNVERIFIED composition compatibility:** even valid local transports must
   compose consistently around an FW284 directed cycle before NSSC follows.

Proving TABC alone would therefore not prove NSSC.

## 5. Replay and trust boundary

The deterministic replay is

```text
theory-lab/topwindow/verify_two_cut_terminal_owner_switch.py
theory-lab/topwindow/results/two_cut_terminal_owner_switch_certificate.json
```

It reconstructs the support-defined skeleton and checks every path drop in
five actual distance-injective controls.  These exercise `eta=1`, `eta=2`,
`ell=0`, a two-vertex core, promotion of an endpoint edge from inside a
strict cap, and two path drops in one skeleton.  The known `L6` control is
Leech but has a singleton sink; the other controls are not Leech and lie
below order eighteen.

**Proved:** the all-order inequalities (FW286.1)--(FW286.4) and forced
pair-class band (FW286.5), under the FW283/FW284 hypotheses for a path drop.

**Not proved:** TABC, cap-to-boundary transport, composition compatibility,
NSSC, nontrivial-sink exclusion, G18, any new order exclusion, or global
Leech-tree nonexistence.

**Verdict: EXACT REDUCTION.**

## 6. FW287 successor reduction

FW287 resolves the first exact geometry of the terminal `AB -> BC` pair.  In
connector coordinates, the two crossed swaps differ from the named adjacent
distances by `x+y` and `x-y`.  Injectivity confines every disjoint state to
four integer cones, and the FW283 critical endpoint-edge bound excludes the
entire left-projection cone, including both connector roots and `ell=0`.

Three modes remain and are realized by actual non-Leech distance-injective
trees: both swaps rise (`R`), connector height drops (`D`), or connector
height rises (`U`).  The live path-drop target is therefore an explicit
`RDU` elimination or composable-transport theorem.  See
`docs/terminal-four-cone-reduction.md`.

FW288 supplies the exact local transport interpretation: `D` retains an
earlier `AB` bridge, `U` a sub-source-weight `BC` bridge, and `R` an oriented
marked connector interval.  The single-path-drop TABC obligation is therefore
proved locally.  Its outputs are not yet known to compose with the next
skeleton arc.  See `docs/terminal-local-transport.md`.
