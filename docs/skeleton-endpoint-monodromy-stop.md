# Compressed endpoint-monodromy stop and owner-overlap successor (FW285)

FW284 constructs a total transition map on the full-window skeleton and
therefore reduces every nontrivial full-window sink to an actual directed
cycle.  It was natural to try to compose the first-owner endpoints around
that cycle.  FW285 audits that proposal and records a **STRICT STOP for the
compressed mechanism**:

```text
one first owner per skeleton edge + lift/drop arcs + endpoint composition.
```

The stop does not refute NSSC.  It identifies information discarded by the
FW284 compression and states the smallest known successor that would have to
recover it from complete Leech coverage.

## 1. What FW284 records

For each skeleton edge `q`, FW284 retains

```text
(q, w_q, eta_q, P_q, tau(q), arc kind, sigma_q or rho_q),
```

where `P_q` is the unique same-side owner of distance `w_q+eta_q` at the
`q`-cut.  The target `r=tau(q)` is a cap boundary containing `P_q`, the
single edge `P_q`, or the maximum-weight skeleton edge crossed by `P_q`.

This gives **edge composition**: `q -> r -> tau(r)` is defined.  It does not
give **owner composition**.  The next record uses `P_r`, the first same-side
owner at the `r`-cut.  No FW284 identity relates `P_q` to `P_r`.

The three arc types fail in different ways.

1. On a cap lift, `P_q` is internal to the target cap and has distance
   strictly below the target boundary.  It is not the target first-hole
   owner and need not meet `P_r`.
2. On an edge lift, `P_q` is the target edge itself.  The next owner `P_r`
   is a different same-side pair; sharing the target edge does not supply a
   shared endpoint, LCA or connector with `P_r`.
3. On a path drop `q -> r`, the target ledger contains the old edge `q` as a
   same-side owner at offset `delta_q` and `P_q` as a cross owner at offset
   `delta_q+eta_q`.  The next first owner `P_r` occurs at the generally
   unrelated offset `eta_r`.  These are three named coefficients, not a
   canonical map between their owners.

Thus the expression `P_q -> P_r` is not defined by FW284.

## 2. Vertex-disjoint cycle control

Consider the order-five path

```text
3 --2-- 2 --8-- 0 --7-- 4 --9-- 1.
```

Its ten pair distances are

```text
{2,7,8,9,10,15,16,17,24,26},
```

so the tree is globally distance-injective.  Its full-window sink is the
nontrivial core `{0,4}`, the core edge has weight `7`, and the first-level
boundaries have weights `8,9`.  Every skeleton transition is total:

```text
7 --edge lift, eta=1--> 8,
8 --edge lift, eta=1--> 9,
9 --path drop, eta=1, rho=2--> 8.
```

The cycle is `8 -> 9 -> 8`, with balance `2=1+1`.  Its consecutive
first-owner pairs are

```text
P_8={1,4},             P_9={0,3},
```

and are vertex-disjoint.  Even at the core edge, retaining the two
side-specific first internal owners gives

```text
offset 1: {0,2},       offset 2: {1,4},
```

but supplies no continuation from `P_9` to the next owner record.

This tree is not Leech and has order below eighteen.  It is therefore not an
NSSC counterexample.  It proves the narrower, mechanism-level fact that a
nontrivial full-window sink, global distance injectivity, a total FW284 map,
the lift/drop equations and side-specific first-owner colors do not by
themselves force shared endpoints around a cycle.

## 3. Cap-lift control

The order-eight path

```text
2 --13-- 3 --2-- 5 --12-- 0 --26-- 1 --4-- 6 --3-- 4 --16-- 7
```

has 28 distinct pair distances.  Its sink core is `{0,3,5}`, with core
weights `2,12` and first-level boundary weights `13,26`.  Its total
transitions are

```text
2  --cap lift, eta=1, sigma=23--> 26,
12 --edge lift, eta=1-----------> 13,
13 --path drop, eta=1, rho=2----> 12,
26 --path drop, eta=1, rho=14---> 13.
```

For the cap lift, the incoming owner is `{4,6}`, of distance `3`, wholly
inside the weight-26 cap.  The target first owner is `{0,2}`, of distance
`27`.  The pairs are vertex-disjoint.  This is an actual-tree demonstration
that containment inside a named cap creates no endpoint continuation to the
cap boundary's next FW284 record.

Again, the tree is not Leech.  It is a pressure control for the compressed
mechanism only.

## 4. What complete coverage may still do

Complete Leech coverage was essential in FW284: it makes every skeleton
transition total.  After that use, FW284 retains only one first-owner record
per edge and discards the remaining coefficients.  The controls above prove
that the retained record does not contain endpoint transport.

They do **not** prove that complete coverage can never force such transport.
That would require either a genuine Leech counterexample or a new theorem.
The correct conclusion is therefore:

> Any continuation must reuse global coefficients that FW284 discarded.  It
> cannot obtain endpoint monodromy merely by composing the existing records.

This qualification is load-bearing.  FW285 is a strict stop for one proof
mechanism, not a negative theorem about every possible use of `[1,N]`.

## 5. Smallest live successor

Keeping the two side-specific first internal owners at each bidirectional
core edge is a necessary improvement because it preserves which side a
returned path enters.  It is not sufficient: it still does not relate the
incoming cross owner to the target-side internal owner.

The next live theorem is therefore the following explicit all-order
obligation.

> **UNVERIFIED Connector-Crossing Owner-Overlap (CCOO).**  Let `q -> r` be a
> path drop in the FW284 map of an order-`n>=18` Leech tree, and let `P_q` be
> its incoming cross owner at the `r`-cut.  Using the complete coefficient
> ledger at `r` and the appropriate side-specific internal owners, force at
> least one of:
>
> 1. an immediate edge return, with the target-side owner equal to `q`;
> 2. an actual shared endpoint with `P_q`; or
> 3. overlapping projections on one named core connector, together with a
>    monotone order rule that composes through the next transition.

An equivalent successor may use the translated interval between offsets
`delta_q` and `delta_q+eta_q`, but a translated window alone is insufficient.
It must also force a shared endpoint or an ordered shared connector
projection.  Cap lifts require an analogous theorem linking an internal cap
owner below the boundary to a later owner record; otherwise endpoint
transport breaks before reaching a path drop.

## 6. Trust boundary

**Proved:** FW284 has edge composition but does not define owner composition;
the two controls are actual globally distance-injective trees with nontrivial
full-window sinks and the stated total transitions; consecutive first-owner
pairs can be vertex-disjoint; cap lift can also have a vertex-disjoint next
owner.

**Not proved:** CCOO, endpoint monodromy, NSSC, nontrivial-sink exclusion,
G18, any new order exclusion, or global Leech-tree nonexistence.  The controls
do not satisfy complete Leech coverage and authorize no claim about what a
future full-spectrum theorem may force.

The deterministic replay is

```text
theory-lab/topwindow/verify_skeleton_endpoint_monodromy_stop.py
theory-lab/topwindow/results/skeleton_endpoint_monodromy_stop_certificate.json
```

and checks both spectra, support-defined sinks and skeletons, every transition,
cycle balance, side-specific core owners, vertex-disjoint cycle owners and
the cap-lift discontinuity.

**Verdict: STRICT STOP.**

## 7. FW286 successor reduction

FW286 resolves the path-drop pair-class part of CCOO more sharply.  For the
ordered decomposition `A--q--B--r--C`, the critical-path endpoint bound and
strict-cap promotion imply `w_r>=eta_q+1`.  Every `AC` owner has `q`-offset at
least `ell+w_r`, so no `AC` owner occurs at offsets at most `eta_q`.  Complete
coverage therefore forces `AB` at offsets `0,...,eta_q-1` and the
distinguished `BC` owner at `eta_q`.

The live path-drop target is now only the **UNVERIFIED Terminal AB-to-BC
Connector** theorem.  Cap-to-boundary transport and later cycle-composition
compatibility remain independent.  See
`docs/two-cut-terminal-owner-switch.md`.

FW287 further writes the terminal crossed swaps in connector coordinates.
Distance injectivity gives four integer cones, and the critical endpoint-edge
bound excludes the whole left-projection cone.  The surviving `R,D,U` modes
all have actual non-Leech realizations and now form the precise path-drop
transport obligation.  See `docs/terminal-four-cone-reduction.md`.

FW288 turns the surviving modes into an exhaustive local record: direct
shared endpoint, earlier `AB` bridge, oriented connector interval, or
sub-source-weight `BC` bridge.  This proves local TABC for one path drop.
Successive-record compatibility and cap-to-boundary transport remain
unverified.  See `docs/terminal-local-transport.md`.

FW289 gives the corresponding cap-lift boundary.  Shallow incoming endpoints
transport directly into the target prefix; equality at the first offset is a
collision; otherwise both endpoints are remote.  The remote pair and target
owner satisfy an exact four-cross-pair rectangle and Leech range bound, but a
pair-cap-contained non-Leech control strictly stops the bounded-prefix
mechanism.  See `docs/cap-endpoint-depth-stop.md`.

FW290 orders the incoming old edge and the target's first owner at every path
drop.  Equality is the exact edge-lift return two-cycle; strict inequality
puts the next owner below the source weight, but a following cap lift can
erase that decrease.  See `docs/pathdrop-target-owner-fork.md`.

FW291 identifies the exact-return two-cycle with a correlated two-root
switchback strip.  Full coverage alone permits the singleton-sink `L6`
instance, while complete local strip data plus a nontrivial connector occurs
in non-Leech controls.  See `docs/exact-return-switchback-stop.md`.
